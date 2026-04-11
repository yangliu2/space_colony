"""Tests for thermal management constraint."""

from __future__ import annotations

import math
import pytest

from habitat_constraints.constraints.thermal import (
    STEFAN_BOLTZMANN,
    ThermalConstraint,
)
from habitat_constraints.core.parameters import HabitatParameters, HumanAssumptions


@pytest.fixture
def constraint() -> ThermalConstraint:
    return ThermalConstraint()


@pytest.fixture
def assumptions() -> HumanAssumptions:
    return HumanAssumptions()


class TestThermalConstraint:
    def test_minimum_viable_passes_with_defaults(
        self,
        constraint: ThermalConstraint,
        assumptions: HumanAssumptions,
    ) -> None:
        # r=982m, L=1276m, default alpha=0.3 → fraction ≈ 0.30
        params = HabitatParameters.from_radius_and_gravity(
            982.0, length_m=1276.0, population=8000
        )
        result = constraint.evaluate(params, assumptions)
        assert result.feasible
        assert result.details["radiator_area_fraction"] < 1.0

    def test_oneill_reference_passes_with_defaults(
        self,
        constraint: ThermalConstraint,
        assumptions: HumanAssumptions,
    ) -> None:
        # r=3200m, L=32000m, default alpha=0.3 → fraction ≈ 0.64
        params = HabitatParameters.from_radius_and_gravity(
            3200.0, length_m=32000.0, population=8000
        )
        result = constraint.evaluate(params, assumptions)
        assert result.feasible
        assert result.details["radiator_area_fraction"] < 1.0

    def test_high_transmittance_large_cylinder_fails(
        self,
        constraint: ThermalConstraint,
        assumptions: HumanAssumptions,
    ) -> None:
        # alpha=0.5 with large cylinder → fraction > 1.0
        hot = HumanAssumptions(window_solar_transmittance=0.5)
        params = HabitatParameters.from_radius_and_gravity(
            3200.0, length_m=32000.0, population=8000
        )
        result = constraint.evaluate(params, hot)
        assert not result.feasible
        assert result.details["radiator_area_fraction"] > 1.0

    def test_high_transmittance_small_cylinder_may_pass(
        self,
        constraint: ThermalConstraint,
        assumptions: HumanAssumptions,
    ) -> None:
        # Small cylinder has proportionally large end caps — may still pass at alpha=0.5
        hot = HumanAssumptions(window_solar_transmittance=0.5)
        params = HabitatParameters.from_radius_and_gravity(
            982.0, length_m=1276.0, population=8000
        )
        result = constraint.evaluate(params, hot)
        # End-cap bonus helps; fraction should be < 1.0
        assert result.feasible

    def test_zero_length_skips_check(
        self,
        constraint: ThermalConstraint,
        assumptions: HumanAssumptions,
    ) -> None:
        params = HabitatParameters.from_radius_and_gravity(982.0)  # length_m=0
        result = constraint.evaluate(params, assumptions)
        assert result.feasible
        assert result.details["required_radiator_area_m2"] == 0.0

    def test_details_contain_expected_keys(
        self,
        constraint: ThermalConstraint,
        assumptions: HumanAssumptions,
    ) -> None:
        params = HabitatParameters.from_radius_and_gravity(
            982.0, length_m=1276.0, population=8000
        )
        result = constraint.evaluate(params, assumptions)
        for key in (
            "solar_gain_w",
            "internal_heat_w",
            "total_heat_w",
            "required_radiator_area_m2",
            "available_radiator_area_m2",
            "solar_panel_area_m2",
            "radiator_area_fraction",
        ):
            assert key in result.details

    def test_solar_panels_reduce_endcap_for_radiators(
        self,
        constraint: ThermalConstraint,
        assumptions: HumanAssumptions,
    ) -> None:
        """Higher power per person → more panel area → less end-cap for radiators."""
        params = HabitatParameters.from_radius_and_gravity(
            982.0, length_m=1276.0, population=8000
        )
        lean = HumanAssumptions(power_per_person_w=1000.0)
        greedy = HumanAssumptions(power_per_person_w=10000.0)
        r_lean = constraint.evaluate(params, lean)
        r_greedy = constraint.evaluate(params, greedy)
        assert (
            r_greedy.details["solar_panel_area_m2"]
            > r_lean.details["solar_panel_area_m2"]
        )
        assert (
            r_greedy.details["available_radiator_area_m2"]
            < r_lean.details["available_radiator_area_m2"]
        )

    def test_zero_population_has_no_solar_panel_area(
        self,
        constraint: ThermalConstraint,
        assumptions: HumanAssumptions,
    ) -> None:
        params = HabitatParameters.from_radius_and_gravity(
            982.0, length_m=1276.0, population=0
        )
        result = constraint.evaluate(params, assumptions)
        assert result.details["solar_panel_area_m2"] == pytest.approx(0.0)

    def test_solar_panel_area_formula(
        self,
        constraint: ThermalConstraint,
        assumptions: HumanAssumptions,
    ) -> None:
        params = HabitatParameters.from_radius_and_gravity(
            982.0, length_m=1276.0, population=8000
        )
        result = constraint.evaluate(params, assumptions)
        expected = (
            assumptions.power_per_person_w
            * 8000
            / (assumptions.solar_panel_efficiency * assumptions.solar_irradiance_w_m2)
        )
        assert result.details["solar_panel_area_m2"] == pytest.approx(expected, rel=1e-6)

    def test_solar_gain_formula(
        self,
        constraint: ThermalConstraint,
        assumptions: HumanAssumptions,
    ) -> None:
        params = HabitatParameters.from_radius_and_gravity(
            982.0, length_m=1276.0, population=0
        )
        result = constraint.evaluate(params, assumptions)
        barrel = 2 * math.pi * 982.0 * 1276.0
        expected_solar = 1361.0 * 0.5 * barrel * 0.3
        assert result.details["solar_gain_w"] == pytest.approx(expected_solar, rel=1e-4)

    def test_internal_heat_scales_with_population(
        self,
        constraint: ThermalConstraint,
        assumptions: HumanAssumptions,
    ) -> None:
        p1 = HabitatParameters.from_radius_and_gravity(
            982.0, length_m=1276.0, population=8000
        )
        p2 = HabitatParameters.from_radius_and_gravity(
            982.0, length_m=1276.0, population=16000
        )
        r1 = constraint.evaluate(p1, assumptions)
        r2 = constraint.evaluate(p2, assumptions)
        diff = r2.details["internal_heat_w"] - r1.details["internal_heat_w"]
        assert diff == pytest.approx(8000 * 350.0, rel=1e-4)

    def test_zero_population_has_no_internal_heat(
        self,
        constraint: ThermalConstraint,
        assumptions: HumanAssumptions,
    ) -> None:
        params = HabitatParameters.from_radius_and_gravity(
            982.0, length_m=1276.0, population=0
        )
        result = constraint.evaluate(params, assumptions)
        assert result.details["internal_heat_w"] == pytest.approx(0.0)

    def test_required_area_formula(
        self,
        constraint: ThermalConstraint,
        assumptions: HumanAssumptions,
    ) -> None:
        params = HabitatParameters.from_radius_and_gravity(
            982.0, length_m=1276.0, population=0
        )
        result = constraint.evaluate(params, assumptions)
        rad_power = 0.9 * STEFAN_BOLTZMANN * 320.0**4
        expected = result.details["total_heat_w"] / rad_power
        assert result.details["required_radiator_area_m2"] == pytest.approx(
            expected, rel=1e-4
        )

    def test_higher_temperature_reduces_required_area(
        self,
        constraint: ThermalConstraint,
        assumptions: HumanAssumptions,
    ) -> None:
        hot = HumanAssumptions(radiator_temperature_k=380.0)
        params = HabitatParameters.from_radius_and_gravity(
            982.0, length_m=1276.0, population=8000
        )
        r_default = constraint.evaluate(params, assumptions)
        r_hot = constraint.evaluate(params, hot)
        assert (
            r_hot.details["required_radiator_area_m2"]
            < r_default.details["required_radiator_area_m2"]
        )

    def test_lower_transmittance_reduces_required_area(
        self,
        constraint: ThermalConstraint,
        assumptions: HumanAssumptions,
    ) -> None:
        closed = HumanAssumptions(window_solar_transmittance=0.1)
        params = HabitatParameters.from_radius_and_gravity(
            982.0, length_m=1276.0, population=8000
        )
        r_default = constraint.evaluate(params, assumptions)
        r_closed = constraint.evaluate(params, closed)
        assert (
            r_closed.details["required_radiator_area_m2"]
            < r_default.details["required_radiator_area_m2"]
        )

    def test_bounds_return_one_entry(
        self,
        constraint: ThermalConstraint,
        assumptions: HumanAssumptions,
    ) -> None:
        bounds = constraint.compute_bounds(assumptions)
        assert len(bounds) == 1
        assert bounds[0].parameter_name == "window_solar_transmittance"
        assert bounds[0].constraint_name == "thermal"
