"""Tests for cylinder length constraint."""

from __future__ import annotations

import pytest

from habitat_constraints.constraints.cylinder_length import (
    CylinderLengthConstraint,
)
from habitat_constraints.core.parameters import (
    HabitatParameters,
    HumanAssumptions,
)


@pytest.fixture
def constraint() -> CylinderLengthConstraint:
    return CylinderLengthConstraint()


@pytest.fixture
def assumptions() -> HumanAssumptions:
    return HumanAssumptions()


class TestCylinderLengthConstraint:
    def test_protocol_properties(
        self,
        constraint: CylinderLengthConstraint,
    ) -> None:
        assert constraint.name == "cylinder_length"
        assert "bending" in constraint.description.lower()

    def test_oneill_design_feasible(
        self,
        constraint: CylinderLengthConstraint,
        assumptions: HumanAssumptions,
    ) -> None:
        """O'Neill: r=3200m, L=32000m — this is the calibration point."""
        params = HabitatParameters.from_radius_and_gravity(
            3200.0, length_m=32000.0
        )
        result = constraint.evaluate(params, assumptions)
        assert result.feasible

    def test_our_minimum_viable_feasible(
        self,
        constraint: CylinderLengthConstraint,
        assumptions: HumanAssumptions,
    ) -> None:
        """Our baseline: r=982m, L=2000m — well within limits."""
        params = HabitatParameters.from_radius_and_gravity(
            982.0, length_m=2000.0
        )
        result = constraint.evaluate(params, assumptions)
        assert result.feasible
        assert result.details["margin_pct"] > 50

    def test_too_long_for_radius_infeasible(
        self,
        constraint: CylinderLengthConstraint,
        assumptions: HumanAssumptions,
    ) -> None:
        """r=500m can support ~2900m, so 10000m should fail."""
        params = HabitatParameters.from_radius_and_gravity(
            500.0, length_m=10000.0
        )
        result = constraint.evaluate(params, assumptions)
        assert not result.feasible

    def test_zero_length_is_feasible(
        self,
        constraint: CylinderLengthConstraint,
        assumptions: HumanAssumptions,
    ) -> None:
        """Length=0 (unspecified) should not fail."""
        params = HabitatParameters.from_radius_and_gravity(1000.0)
        result = constraint.evaluate(params, assumptions)
        assert result.feasible

    def test_max_length_scales_with_radius(
        self,
        constraint: CylinderLengthConstraint,
        assumptions: HumanAssumptions,
    ) -> None:
        """Doubling radius should more than double max length."""
        p1 = HabitatParameters.from_radius_and_gravity(
            1000.0, length_m=1000.0
        )
        p2 = HabitatParameters.from_radius_and_gravity(
            2000.0, length_m=1000.0
        )
        r1 = constraint.evaluate(p1, assumptions)
        r2 = constraint.evaluate(p2, assumptions)
        assert r2.details["max_length_m"] > 2 * r1.details["max_length_m"]

    def test_details_include_length_to_diameter(
        self,
        constraint: CylinderLengthConstraint,
        assumptions: HumanAssumptions,
    ) -> None:
        params = HabitatParameters.from_radius_and_gravity(
            982.0, length_m=2000.0
        )
        result = constraint.evaluate(params, assumptions)
        expected_ld = 2000.0 / (2 * 982.0)
        assert result.details["length_to_diameter"] == pytest.approx(
            expected_ld, rel=0.01
        )

    def test_bounds_structure(
        self,
        constraint: CylinderLengthConstraint,
        assumptions: HumanAssumptions,
    ) -> None:
        bounds = constraint.compute_bounds(assumptions)
        assert len(bounds) == 1
        assert bounds[0].parameter_name == "length_m"
        assert bounds[0].constraint_name == "cylinder_length"

    def test_custom_coefficient(
        self,
        constraint: CylinderLengthConstraint,
    ) -> None:
        """Stricter coefficient should reject more designs."""
        strict = HumanAssumptions(max_length_coefficient=0.5)
        params = HabitatParameters.from_radius_and_gravity(
            982.0, length_m=5000.0
        )
        result = constraint.evaluate(params, strict)
        assert not result.feasible

    def test_oneill_calibration_point(
        self,
        constraint: CylinderLengthConstraint,
        assumptions: HumanAssumptions,
    ) -> None:
        """C=1.33 should give L_max ≈ 32000m at r=3200m."""
        params = HabitatParameters.from_radius_and_gravity(
            3200.0, length_m=1.0
        )
        result = constraint.evaluate(params, assumptions)
        L_max = result.details["max_length_m"]
        assert L_max == pytest.approx(32000, rel=0.03)
