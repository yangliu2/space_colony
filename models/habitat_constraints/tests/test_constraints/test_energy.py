"""Tests for energy budget constraint."""

from __future__ import annotations

import math
import pytest

from habitat_constraints.constraints.energy import EnergyConstraint
from habitat_constraints.core.parameters import HabitatParameters, HumanAssumptions


@pytest.fixture
def constraint() -> EnergyConstraint:
    return EnergyConstraint()


@pytest.fixture
def assumptions() -> HumanAssumptions:
    return HumanAssumptions()


class TestEnergyConstraint:
    def test_minimum_viable_passes_with_defaults(
        self,
        constraint: EnergyConstraint,
        assumptions: HumanAssumptions,
    ) -> None:
        # r=982m, pop=8000 → panel fraction ~2.4%
        params = HabitatParameters.from_radius_and_gravity(982.0, population=8000)
        result = constraint.evaluate(params, assumptions)
        assert result.feasible
        assert result.details["panel_area_fraction"] < 0.1

    def test_oneill_reference_passes_with_defaults(
        self,
        constraint: EnergyConstraint,
        assumptions: HumanAssumptions,
    ) -> None:
        # r=3200m, pop=10000 → panel fraction ~0.3%
        params = HabitatParameters.from_radius_and_gravity(3200.0, population=10000)
        result = constraint.evaluate(params, assumptions)
        assert result.feasible
        assert result.details["panel_area_fraction"] < 0.01

    def test_extreme_population_density_fails(
        self,
        constraint: EnergyConstraint,
        assumptions: HumanAssumptions,
    ) -> None:
        # At r=982m, max supportable ~330,000 at defaults.
        # Force failure with very high power demand per person.
        greedy = HumanAssumptions(power_per_person_w=50000.0)
        params = HabitatParameters.from_radius_and_gravity(982.0, population=100000)
        result = constraint.evaluate(params, greedy)
        assert not result.feasible
        assert result.details["panel_area_fraction"] > 1.0

    def test_zero_population_skips_check(
        self,
        constraint: EnergyConstraint,
        assumptions: HumanAssumptions,
    ) -> None:
        params = HabitatParameters.from_radius_and_gravity(982.0)  # population=0
        result = constraint.evaluate(params, assumptions)
        assert result.feasible
        assert result.details["total_power_demand_w"] == 0.0

    def test_details_contain_expected_keys(
        self,
        constraint: EnergyConstraint,
        assumptions: HumanAssumptions,
    ) -> None:
        params = HabitatParameters.from_radius_and_gravity(982.0, population=8000)
        result = constraint.evaluate(params, assumptions)
        for key in (
            "total_power_demand_w",
            "required_panel_area_m2",
            "available_panel_area_m2",
            "panel_area_fraction",
        ):
            assert key in result.details

    def test_power_demand_formula(
        self,
        constraint: EnergyConstraint,
        assumptions: HumanAssumptions,
    ) -> None:
        params = HabitatParameters.from_radius_and_gravity(982.0, population=8000)
        result = constraint.evaluate(params, assumptions)
        expected = 5000.0 * 8000
        assert result.details["total_power_demand_w"] == pytest.approx(
            expected, rel=1e-6
        )

    def test_required_area_formula(
        self,
        constraint: EnergyConstraint,
        assumptions: HumanAssumptions,
    ) -> None:
        params = HabitatParameters.from_radius_and_gravity(982.0, population=8000)
        result = constraint.evaluate(params, assumptions)
        expected = (5000.0 * 8000) / (0.20 * 1361.0)
        assert result.details["required_panel_area_m2"] == pytest.approx(
            expected, rel=1e-4
        )

    def test_available_area_is_endcap_area(
        self,
        constraint: EnergyConstraint,
        assumptions: HumanAssumptions,
    ) -> None:
        params = HabitatParameters.from_radius_and_gravity(982.0, population=8000)
        result = constraint.evaluate(params, assumptions)
        expected = 2.0 * math.pi * 982.0**2
        assert result.details["available_panel_area_m2"] == pytest.approx(
            expected, rel=1e-6
        )

    def test_higher_efficiency_reduces_required_area(
        self,
        constraint: EnergyConstraint,
        assumptions: HumanAssumptions,
    ) -> None:
        efficient = HumanAssumptions(solar_panel_efficiency=0.30)
        params = HabitatParameters.from_radius_and_gravity(982.0, population=8000)
        r_default = constraint.evaluate(params, assumptions)
        r_efficient = constraint.evaluate(params, efficient)
        assert (
            r_efficient.details["required_panel_area_m2"]
            < r_default.details["required_panel_area_m2"]
        )

    def test_lower_power_demand_reduces_required_area(
        self,
        constraint: EnergyConstraint,
        assumptions: HumanAssumptions,
    ) -> None:
        lean = HumanAssumptions(power_per_person_w=1000.0)
        params = HabitatParameters.from_radius_and_gravity(982.0, population=8000)
        r_default = constraint.evaluate(params, assumptions)
        r_lean = constraint.evaluate(params, lean)
        assert (
            r_lean.details["required_panel_area_m2"]
            < r_default.details["required_panel_area_m2"]
        )

    def test_power_demand_scales_linearly_with_population(
        self,
        constraint: EnergyConstraint,
        assumptions: HumanAssumptions,
    ) -> None:
        p1 = HabitatParameters.from_radius_and_gravity(982.0, population=8000)
        p2 = HabitatParameters.from_radius_and_gravity(982.0, population=16000)
        r1 = constraint.evaluate(p1, assumptions)
        r2 = constraint.evaluate(p2, assumptions)
        assert r2.details["total_power_demand_w"] == pytest.approx(
            2.0 * r1.details["total_power_demand_w"], rel=1e-6
        )

    def test_fraction_consistent_with_areas(
        self,
        constraint: EnergyConstraint,
        assumptions: HumanAssumptions,
    ) -> None:
        params = HabitatParameters.from_radius_and_gravity(982.0, population=8000)
        result = constraint.evaluate(params, assumptions)
        expected_fraction = (
            result.details["required_panel_area_m2"]
            / result.details["available_panel_area_m2"]
        )
        assert result.details["panel_area_fraction"] == pytest.approx(
            expected_fraction, rel=1e-6
        )

    def test_bounds_return_one_entry(
        self,
        constraint: EnergyConstraint,
        assumptions: HumanAssumptions,
    ) -> None:
        bounds = constraint.compute_bounds(assumptions)
        assert len(bounds) == 1
        assert bounds[0].parameter_name == "power_per_person_w"
        assert bounds[0].constraint_name == "energy"
