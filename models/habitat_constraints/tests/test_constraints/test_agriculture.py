"""Tests for agriculture area constraint."""

from __future__ import annotations

import pytest

from habitat_constraints.constraints.agriculture import AgricultureConstraint
from habitat_constraints.core.parameters import HabitatParameters, HumanAssumptions


@pytest.fixture
def constraint() -> AgricultureConstraint:
    return AgricultureConstraint()


@pytest.fixture
def assumptions() -> HumanAssumptions:
    return HumanAssumptions()


class TestAgricultureConstraint:
    def test_sufficient_area_passes(
        self,
        constraint: AgricultureConstraint,
        assumptions: HumanAssumptions,
    ) -> None:
        # 8,000 people × 200 m²/person = 1,600,000 m² required; we provide more
        params = HabitatParameters.from_radius_and_gravity(
            982.0,
            population=8000,
            agriculture_area_m2=2_000_000.0,
        )
        result = constraint.evaluate(params, assumptions)
        assert result.feasible

    def test_exact_minimum_passes(
        self,
        constraint: AgricultureConstraint,
        assumptions: HumanAssumptions,
    ) -> None:
        # Exactly at threshold: 8,000 × 200 = 1,600,000 m²
        params = HabitatParameters.from_radius_and_gravity(
            982.0,
            population=8000,
            agriculture_area_m2=1_600_000.0,
        )
        result = constraint.evaluate(params, assumptions)
        assert result.feasible
        assert result.details["area_margin_m2"] == pytest.approx(0.0)

    def test_insufficient_area_fails(
        self,
        constraint: AgricultureConstraint,
        assumptions: HumanAssumptions,
    ) -> None:
        # Half the required area
        params = HabitatParameters.from_radius_and_gravity(
            982.0,
            population=8000,
            agriculture_area_m2=800_000.0,
        )
        result = constraint.evaluate(params, assumptions)
        assert not result.feasible
        assert result.details["area_margin_m2"] < 0

    def test_zero_area_skips_check(
        self,
        constraint: AgricultureConstraint,
        assumptions: HumanAssumptions,
    ) -> None:
        # agriculture_area_m2 = 0 means not specified — pass by default
        params = HabitatParameters.from_radius_and_gravity(
            982.0,
            population=8000,
            agriculture_area_m2=0.0,
        )
        result = constraint.evaluate(params, assumptions)
        assert result.feasible

    def test_zero_population_skips_check(
        self,
        constraint: AgricultureConstraint,
        assumptions: HumanAssumptions,
    ) -> None:
        params = HabitatParameters.from_radius_and_gravity(
            982.0,
            population=0,
            agriculture_area_m2=500_000.0,
        )
        result = constraint.evaluate(params, assumptions)
        assert result.feasible

    def test_details_contain_expected_keys(
        self,
        constraint: AgricultureConstraint,
        assumptions: HumanAssumptions,
    ) -> None:
        params = HabitatParameters.from_radius_and_gravity(
            982.0,
            population=8000,
            agriculture_area_m2=1_600_000.0,
        )
        result = constraint.evaluate(params, assumptions)
        for key in (
            "agriculture_area_m2",
            "required_area_m2",
            "area_per_person_m2",
            "effective_area_per_person_m2",
            "diet_land_multiplier",
            "area_margin_m2",
        ):
            assert key in result.details

    def test_area_per_person_computed_correctly(
        self,
        constraint: AgricultureConstraint,
        assumptions: HumanAssumptions,
    ) -> None:
        params = HabitatParameters.from_radius_and_gravity(
            982.0,
            population=4000,
            agriculture_area_m2=1_200_000.0,
        )
        result = constraint.evaluate(params, assumptions)
        assert result.details["area_per_person_m2"] == pytest.approx(300.0)

    def test_custom_threshold_tighter(
        self,
        constraint: AgricultureConstraint,
        assumptions: HumanAssumptions,
    ) -> None:
        # Require open-field area (2,000 m²/person)
        strict = HumanAssumptions(min_agriculture_area_per_person_m2=2000.0)
        params = HabitatParameters.from_radius_and_gravity(
            982.0,
            population=8000,
            agriculture_area_m2=1_600_000.0,  # fine for hydroponics, fails here
        )
        result = constraint.evaluate(params, strict)
        assert not result.feasible

    def test_custom_threshold_looser(
        self,
        constraint: AgricultureConstraint,
        assumptions: HumanAssumptions,
    ) -> None:
        # Vertical farming: 40 m²/person
        loose = HumanAssumptions(min_agriculture_area_per_person_m2=40.0)
        params = HabitatParameters.from_radius_and_gravity(
            982.0,
            population=8000,
            agriculture_area_m2=400_000.0,  # 50 m²/person — passes at 40
        )
        result = constraint.evaluate(params, loose)
        assert result.feasible

    def test_bounds_return_one_entry(
        self,
        constraint: AgricultureConstraint,
        assumptions: HumanAssumptions,
    ) -> None:
        bounds = constraint.compute_bounds(assumptions)
        assert len(bounds) == 1
        assert bounds[0].parameter_name == "agriculture_area_m2"
        assert bounds[0].constraint_name == "agriculture"

    def test_diet_multiplier_aquaculture(
        self,
        constraint: AgricultureConstraint,
        assumptions: HumanAssumptions,
    ) -> None:
        # Aquaculture multiplier 1.4 — 8000 × 200 × 1.4 = 2,240,000 m²
        aqua = HumanAssumptions(diet_land_multiplier=1.4)
        params = HabitatParameters.from_radius_and_gravity(
            982.0,
            population=8000,
            agriculture_area_m2=1_600_000.0,  # passes plant-only, fails with fish
        )
        result = constraint.evaluate(params, aqua)
        assert not result.feasible
        assert result.details["effective_area_per_person_m2"] == pytest.approx(280.0)

    def test_diet_multiplier_aquaculture_sufficient_area(
        self,
        constraint: AgricultureConstraint,
        assumptions: HumanAssumptions,
    ) -> None:
        aqua = HumanAssumptions(diet_land_multiplier=1.4)
        params = HabitatParameters.from_radius_and_gravity(
            982.0,
            population=8000,
            agriculture_area_m2=2_240_000.0,  # exactly 8000 × 200 × 1.4
        )
        result = constraint.evaluate(params, aqua)
        assert result.feasible
        assert result.details["area_margin_m2"] == pytest.approx(0.0)

    def test_diet_multiplier_poultry_fails(
        self,
        constraint: AgricultureConstraint,
        assumptions: HumanAssumptions,
    ) -> None:
        # Poultry multiplier 3.5 — 8000 × 200 × 3.5 = 5,600,000 m²
        poultry = HumanAssumptions(diet_land_multiplier=3.5)
        params = HabitatParameters.from_radius_and_gravity(
            982.0,
            population=8000,
            agriculture_area_m2=2_000_000.0,
        )
        result = constraint.evaluate(params, poultry)
        assert not result.feasible

    def test_diet_multiplier_in_details(
        self,
        constraint: AgricultureConstraint,
        assumptions: HumanAssumptions,
    ) -> None:
        custom = HumanAssumptions(diet_land_multiplier=2.0)
        params = HabitatParameters.from_radius_and_gravity(
            982.0,
            population=8000,
            agriculture_area_m2=3_200_000.0,
        )
        result = constraint.evaluate(params, custom)
        assert result.details["diet_land_multiplier"] == pytest.approx(2.0)
        assert result.details["effective_area_per_person_m2"] == pytest.approx(400.0)
