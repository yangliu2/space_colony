"""Tests for WaterRecyclingConstraint."""

from __future__ import annotations

import pytest

from habitat_constraints.constraints.water_recycling import WaterRecyclingConstraint
from habitat_constraints.core.parameters import HabitatParameters, HumanAssumptions


def _params(population: int = 8000) -> HabitatParameters:
    return HabitatParameters.from_radius_and_gravity(
        radius_m=982.0,
        target_gravity_g=1.0,
        length_m=1276.0,
        population=population,
    )


def _assumptions(**kwargs) -> HumanAssumptions:
    return HumanAssumptions(**kwargs)


@pytest.fixture
def constraint() -> WaterRecyclingConstraint:
    return WaterRecyclingConstraint()


class TestBasicProperties:
    def test_name(self, constraint: WaterRecyclingConstraint) -> None:
        assert constraint.name == "water_recycling"

    def test_description_non_empty(self, constraint: WaterRecyclingConstraint) -> None:
        assert len(constraint.description) > 0


class TestFeasibility:
    def test_fails_at_iss_efficiency(self, constraint: WaterRecyclingConstraint) -> None:
        """Default 0.90 efficiency fails the 0.98 minimum threshold."""
        result = constraint.evaluate(_params(), _assumptions())
        assert result.feasible is False

    def test_passes_at_target_efficiency(
        self, constraint: WaterRecyclingConstraint
    ) -> None:
        result = constraint.evaluate(
            _params(),
            _assumptions(water_recycling_efficiency=0.98),
        )
        assert result.feasible is True

    def test_passes_above_threshold(self, constraint: WaterRecyclingConstraint) -> None:
        result = constraint.evaluate(
            _params(),
            _assumptions(water_recycling_efficiency=0.999),
        )
        assert result.feasible is True

    def test_fails_below_threshold(self, constraint: WaterRecyclingConstraint) -> None:
        result = constraint.evaluate(
            _params(),
            _assumptions(
                water_recycling_efficiency=0.95,
                min_water_recycling_efficiency=0.98,
            ),
        )
        assert result.feasible is False

    def test_skips_at_zero_population(
        self, constraint: WaterRecyclingConstraint
    ) -> None:
        result = constraint.evaluate(_params(population=0), _assumptions())
        assert result.feasible is True
        assert result.details["total_daily_demand_liters"] == 0.0
        assert result.details["annual_loss_kg"] == 0.0


class TestFormulas:
    def test_daily_demand_formula(self, constraint: WaterRecyclingConstraint) -> None:
        pop = 500
        demand_pp = 30.0
        result = constraint.evaluate(
            _params(population=pop),
            _assumptions(water_per_person_day_liters=demand_pp),
        )
        assert result.details["total_daily_demand_liters"] == pytest.approx(
            demand_pp * pop
        )

    def test_daily_loss_formula(self, constraint: WaterRecyclingConstraint) -> None:
        pop = 1000
        demand_pp = 20.0
        eta = 0.95
        result = constraint.evaluate(
            _params(population=pop),
            _assumptions(
                water_per_person_day_liters=demand_pp,
                water_recycling_efficiency=eta,
                min_water_recycling_efficiency=0.90,
            ),
        )
        expected_loss = demand_pp * pop * (1.0 - eta)
        assert result.details["daily_loss_liters"] == pytest.approx(expected_loss)

    def test_annual_loss_is_365x_daily(
        self, constraint: WaterRecyclingConstraint
    ) -> None:
        result = constraint.evaluate(
            _params(),
            _assumptions(
                water_recycling_efficiency=0.95,
                min_water_recycling_efficiency=0.90,
            ),
        )
        assert result.details["annual_loss_kg"] == pytest.approx(
            result.details["daily_loss_liters"] * 365.0
        )

    def test_efficiency_margin_positive_when_passing(
        self, constraint: WaterRecyclingConstraint
    ) -> None:
        result = constraint.evaluate(
            _params(),
            _assumptions(
                water_recycling_efficiency=0.99,
                min_water_recycling_efficiency=0.98,
            ),
        )
        assert result.details["efficiency_margin"] == pytest.approx(0.01)

    def test_efficiency_margin_negative_when_failing(
        self, constraint: WaterRecyclingConstraint
    ) -> None:
        result = constraint.evaluate(
            _params(),
            _assumptions(
                water_recycling_efficiency=0.90,
                min_water_recycling_efficiency=0.98,
            ),
        )
        assert result.details["efficiency_margin"] == pytest.approx(-0.08)


class TestDetails:
    def test_details_contains_required_keys(
        self, constraint: WaterRecyclingConstraint
    ) -> None:
        result = constraint.evaluate(_params(), _assumptions())
        expected_keys = {
            "total_daily_demand_liters",
            "daily_loss_liters",
            "annual_loss_kg",
            "recycling_efficiency",
            "min_recycling_efficiency",
            "efficiency_margin",
        }
        assert set(result.details.keys()) == expected_keys

    def test_recycling_efficiency_in_details(
        self, constraint: WaterRecyclingConstraint
    ) -> None:
        eta = 0.95
        result = constraint.evaluate(
            _params(),
            _assumptions(
                water_recycling_efficiency=eta,
                min_water_recycling_efficiency=0.90,
            ),
        )
        assert result.details["recycling_efficiency"] == pytest.approx(eta)

    def test_min_recycling_efficiency_in_details(
        self, constraint: WaterRecyclingConstraint
    ) -> None:
        min_eta = 0.97
        result = constraint.evaluate(
            _params(),
            _assumptions(
                water_recycling_efficiency=0.98,
                min_water_recycling_efficiency=min_eta,
            ),
        )
        assert result.details["min_recycling_efficiency"] == pytest.approx(min_eta)


class TestBounds:
    def test_bounds_structure(self, constraint: WaterRecyclingConstraint) -> None:
        bounds = constraint.compute_bounds(
            _assumptions(min_water_recycling_efficiency=0.98)
        )
        assert len(bounds) == 1
        assert bounds[0].parameter_name == "water_recycling_efficiency"
        assert bounds[0].lower == pytest.approx(0.98)
        assert bounds[0].constraint_name == "water_recycling"

    def test_result_includes_bounds(self, constraint: WaterRecyclingConstraint) -> None:
        result = constraint.evaluate(_params(), _assumptions())
        assert len(result.bounds) == 1


class TestScaling:
    def test_loss_scales_linearly_with_population(
        self, constraint: WaterRecyclingConstraint
    ) -> None:
        r1 = constraint.evaluate(
            _params(population=1000),
            _assumptions(
                water_recycling_efficiency=0.95,
                min_water_recycling_efficiency=0.90,
            ),
        )
        r2 = constraint.evaluate(
            _params(population=2000),
            _assumptions(
                water_recycling_efficiency=0.95,
                min_water_recycling_efficiency=0.90,
            ),
        )
        assert r2.details["annual_loss_kg"] == pytest.approx(
            2.0 * r1.details["annual_loss_kg"]
        )

    def test_perfect_efficiency_has_zero_loss(
        self, constraint: WaterRecyclingConstraint
    ) -> None:
        result = constraint.evaluate(
            _params(),
            _assumptions(
                water_recycling_efficiency=1.0,
                min_water_recycling_efficiency=0.98,
            ),
        )
        assert result.details["daily_loss_liters"] == pytest.approx(0.0)
        assert result.details["annual_loss_kg"] == pytest.approx(0.0)
        assert result.feasible is True
