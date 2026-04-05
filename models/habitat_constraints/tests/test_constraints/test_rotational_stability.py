"""Tests for rotational stability constraint."""

from __future__ import annotations

import pytest

from habitat_constraints.constraints.rotational_stability import (
    RotationalStabilityConstraint,
)
from habitat_constraints.core.parameters import (
    HabitatParameters,
    HumanAssumptions,
)


@pytest.fixture
def constraint() -> RotationalStabilityConstraint:
    return RotationalStabilityConstraint()


@pytest.fixture
def assumptions() -> HumanAssumptions:
    return HumanAssumptions()


class TestRotationalStabilityConstraint:
    def test_protocol_properties(
        self,
        constraint: RotationalStabilityConstraint,
    ) -> None:
        assert constraint.name == "rotational_stability"
        assert "stability" in constraint.description.lower()

    def test_kalpana_one_feasible(
        self,
        constraint: RotationalStabilityConstraint,
        assumptions: HumanAssumptions,
    ) -> None:
        """Kalpana One: r=250m, L=325m, L/r=1.3 — at the limit."""
        params = HabitatParameters.from_radius_and_gravity(250.0, length_m=325.0)
        result = constraint.evaluate(params, assumptions)
        assert result.feasible

    def test_stubby_cylinder_feasible(
        self,
        constraint: RotationalStabilityConstraint,
        assumptions: HumanAssumptions,
    ) -> None:
        """r=982m, L=1000m, L/r≈1.02 — well within limit."""
        params = HabitatParameters.from_radius_and_gravity(982.0, length_m=1000.0)
        result = constraint.evaluate(params, assumptions)
        assert result.feasible
        assert result.details["margin_pct"] > 20

    def test_long_single_cylinder_infeasible(
        self,
        constraint: RotationalStabilityConstraint,
    ) -> None:
        """r=982m, L=2000m, L/r≈2.04 — exceeds 1.3 limit for single cylinder."""
        single = HumanAssumptions(counter_rotating_pair=False)
        params = HabitatParameters.from_radius_and_gravity(982.0, length_m=2000.0)
        result = constraint.evaluate(params, single)
        assert not result.feasible

    def test_oneill_single_cylinder_infeasible(
        self,
        constraint: RotationalStabilityConstraint,
    ) -> None:
        """O'Neill: r=3200m, L=32000m, L/r=10 — infeasible without
        counter-rotating pair."""
        single = HumanAssumptions(counter_rotating_pair=False)
        params = HabitatParameters.from_radius_and_gravity(3200.0, length_m=32000.0)
        result = constraint.evaluate(params, single)
        assert not result.feasible

    def test_oneill_counter_rotating_feasible(
        self,
        constraint: RotationalStabilityConstraint,
    ) -> None:
        """O'Neill with counter-rotating pair: L/r=10 is feasible."""
        paired = HumanAssumptions(counter_rotating_pair=True)
        params = HabitatParameters.from_radius_and_gravity(3200.0, length_m=32000.0)
        result = constraint.evaluate(params, paired)
        assert result.feasible

    def test_zero_length_is_feasible(
        self,
        constraint: RotationalStabilityConstraint,
        assumptions: HumanAssumptions,
    ) -> None:
        """Length=0 (unspecified) should not fail."""
        params = HabitatParameters.from_radius_and_gravity(1000.0)
        result = constraint.evaluate(params, assumptions)
        assert result.feasible

    def test_details_include_ratio(
        self,
        constraint: RotationalStabilityConstraint,
    ) -> None:
        """Single-cylinder mode returns L/r limit of 1.3."""
        single = HumanAssumptions(counter_rotating_pair=False)
        params = HabitatParameters.from_radius_and_gravity(1000.0, length_m=1200.0)
        result = constraint.evaluate(params, single)
        assert result.details["length_to_radius"] == pytest.approx(1.2, rel=0.01)
        assert result.details["max_length_to_radius"] == 1.3

    def test_counter_rotating_flag_in_details(
        self,
        constraint: RotationalStabilityConstraint,
    ) -> None:
        paired = HumanAssumptions(counter_rotating_pair=True)
        params = HabitatParameters.from_radius_and_gravity(1000.0, length_m=5000.0)
        result = constraint.evaluate(params, paired)
        assert result.details["counter_rotating"] == 1.0

    def test_bounds_structure(
        self,
        constraint: RotationalStabilityConstraint,
    ) -> None:
        """Single-cylinder bounds description mentions 1.3 limit."""
        single = HumanAssumptions(counter_rotating_pair=False)
        bounds = constraint.compute_bounds(single)
        assert len(bounds) == 1
        assert bounds[0].parameter_name == "length_m"
        assert bounds[0].constraint_name == "rotational_stability"
        assert "1.3" in bounds[0].description

    def test_bounds_counter_rotating(
        self,
        constraint: RotationalStabilityConstraint,
    ) -> None:
        paired = HumanAssumptions(counter_rotating_pair=True)
        bounds = constraint.compute_bounds(paired)
        assert "counter-rotating" in bounds[0].description

    def test_custom_ratio(
        self,
        constraint: RotationalStabilityConstraint,
    ) -> None:
        """Curved endcaps can extend stable L/r to ~2.0."""
        curved = HumanAssumptions(max_length_to_radius_ratio=2.0)
        params = HabitatParameters.from_radius_and_gravity(982.0, length_m=1800.0)
        result = constraint.evaluate(params, curved)
        assert result.feasible  # L/r ≈ 1.83 < 2.0

    def test_manual_calculation(
        self,
        constraint: RotationalStabilityConstraint,
    ) -> None:
        """Hand-verify single cylinder: r=1000m, max_ratio=1.3 → max_L=1300m."""
        single = HumanAssumptions(counter_rotating_pair=False)
        params = HabitatParameters.from_radius_and_gravity(1000.0, length_m=1300.0)
        result = constraint.evaluate(params, single)
        assert result.feasible
        assert result.details["max_length_m"] == 1300.0
        assert result.details["margin_pct"] == pytest.approx(0.0, abs=0.1)
