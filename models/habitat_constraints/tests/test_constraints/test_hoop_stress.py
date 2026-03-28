"""Tests for structural hoop stress constraint."""

from __future__ import annotations

import pytest

from habitat_constraints.constraints.hoop_stress import (
    HoopStressConstraint,
)
from habitat_constraints.core.parameters import (
    HabitatParameters,
    HumanAssumptions,
)


@pytest.fixture
def constraint() -> HoopStressConstraint:
    return HoopStressConstraint()


@pytest.fixture
def assumptions() -> HumanAssumptions:
    return HumanAssumptions()


class TestHoopStressConstraint:
    def test_protocol_properties(
        self,
        constraint: HoopStressConstraint,
    ) -> None:
        assert constraint.name == "hoop_stress"
        assert "yield" in constraint.description.lower()

    def test_min_viable_feasible_with_defaults(
        self,
        constraint: HoopStressConstraint,
        assumptions: HumanAssumptions,
    ) -> None:
        """r=982m, t=0.2m, high-strength steel: should be feasible."""
        params = HabitatParameters.from_radius_and_gravity(982.0)
        result = constraint.evaluate(params, assumptions)
        assert result.feasible
        assert result.details["sigma_hoop_mpa"] < 600

    def test_thin_wall_infeasible(
        self,
        constraint: HoopStressConstraint,
        assumptions: HumanAssumptions,
    ) -> None:
        """Very thin wall at r=982m should fail."""
        params = HabitatParameters.from_radius_and_gravity(
            982.0, wall_thickness_m=0.01
        )
        result = constraint.evaluate(params, assumptions)
        assert not result.feasible

    def test_rotational_stress_independent_of_thickness(
        self,
        constraint: HoopStressConstraint,
        assumptions: HumanAssumptions,
    ) -> None:
        """σ_rot should be the same regardless of wall thickness."""
        p1 = HabitatParameters.from_radius_and_gravity(
            982.0, wall_thickness_m=0.1
        )
        p2 = HabitatParameters.from_radius_and_gravity(
            982.0, wall_thickness_m=1.0
        )
        r1 = constraint.evaluate(p1, assumptions)
        r2 = constraint.evaluate(p2, assumptions)
        assert r1.details["sigma_rot_mpa"] == r2.details["sigma_rot_mpa"]

    def test_pressure_stress_inversely_proportional_to_thickness(
        self,
        constraint: HoopStressConstraint,
        assumptions: HumanAssumptions,
    ) -> None:
        """Doubling thickness should halve pressure stress."""
        p1 = HabitatParameters.from_radius_and_gravity(
            982.0, wall_thickness_m=0.2
        )
        p2 = HabitatParameters.from_radius_and_gravity(
            982.0, wall_thickness_m=0.4
        )
        r1 = constraint.evaluate(p1, assumptions)
        r2 = constraint.evaluate(p2, assumptions)
        assert r1.details["sigma_pressure_mpa"] == pytest.approx(
            2.0 * r2.details["sigma_pressure_mpa"], rel=0.01
        )

    def test_cfrp_enables_larger_radius(
        self,
        constraint: HoopStressConstraint,
    ) -> None:
        """CFRP (low density, high strength) should pass at larger radii."""
        cfrp_assumptions = HumanAssumptions(
            yield_strength_mpa=3500.0,
            structural_safety_factor=2.0,
        )
        params = HabitatParameters.from_radius_and_gravity(
            982.0,
            wall_thickness_m=0.2,
            hull_density_kg_m3=1550.0,
        )
        result = constraint.evaluate(params, cfrp_assumptions)
        assert result.feasible
        # CFRP has much lower rotational stress
        assert result.details["sigma_rot_mpa"] < 20

    def test_details_include_all_components(
        self,
        constraint: HoopStressConstraint,
        assumptions: HumanAssumptions,
    ) -> None:
        params = HabitatParameters.from_radius_and_gravity(982.0)
        result = constraint.evaluate(params, assumptions)
        assert "sigma_rot_mpa" in result.details
        assert "sigma_pressure_mpa" in result.details
        assert "sigma_hoop_mpa" in result.details
        assert "allowable_mpa" in result.details
        assert "safety_factor" in result.details
        assert "margin_pct" in result.details

    def test_bounds_structure(
        self,
        constraint: HoopStressConstraint,
        assumptions: HumanAssumptions,
    ) -> None:
        bounds = constraint.compute_bounds(assumptions)
        assert len(bounds) == 1
        assert bounds[0].parameter_name == "radius_m"
        assert bounds[0].constraint_name == "hoop_stress"

    def test_stricter_safety_factor_reduces_allowable(
        self,
        constraint: HoopStressConstraint,
    ) -> None:
        """Higher FoS means lower allowable stress."""
        strict = HumanAssumptions(structural_safety_factor=3.0)
        params = HabitatParameters.from_radius_and_gravity(982.0)
        result = constraint.evaluate(params, strict)
        # Default yield is 1200 MPa, FoS=3.0 → 400 MPa
        assert result.details["allowable_mpa"] == pytest.approx(
            400.0, rel=0.01
        )

    def test_manual_calculation(
        self,
        constraint: HoopStressConstraint,
        assumptions: HumanAssumptions,
    ) -> None:
        """Verify against hand calculation for r=982m defaults."""
        params = HabitatParameters.from_radius_and_gravity(982.0)
        result = constraint.evaluate(params, assumptions)
        # σ_rot = 7900 * (√(9.80665/982))² * 982² = 7900 * 9.80665/982 * 982²
        #       = 7900 * 9.80665 * 982 = 76.1 MPa
        assert result.details["sigma_rot_mpa"] == pytest.approx(
            76.1, abs=0.5
        )
        # σ_p = 101300 * 982 / 0.2 = 497.4 MPa
        assert result.details["sigma_pressure_mpa"] == pytest.approx(
            497.4, abs=1.0
        )
