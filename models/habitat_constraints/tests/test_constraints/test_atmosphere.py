"""Tests for atmosphere constraint."""

from __future__ import annotations

import pytest

from habitat_constraints.constraints.atmosphere import (
    AtmosphereConstraint,
)
from habitat_constraints.core.parameters import (
    HabitatParameters,
    HumanAssumptions,
)


@pytest.fixture
def constraint() -> AtmosphereConstraint:
    return AtmosphereConstraint()


@pytest.fixture
def assumptions() -> HumanAssumptions:
    return HumanAssumptions()


class TestAtmosphereConstraint:
    def test_earth_normal_passes(
        self,
        constraint: AtmosphereConstraint,
        assumptions: HumanAssumptions,
    ) -> None:
        # 101.3 kPa, 21% O2 => pO2 = 21.3 kPa
        params = HabitatParameters.from_radius_and_gravity(1000.0)
        result = constraint.evaluate(params, assumptions)
        assert result.feasible
        assert 20.0 < result.details["o2_partial_pressure_kpa"] < 22.0

    def test_hypoxic_atmosphere_fails(
        self,
        constraint: AtmosphereConstraint,
        assumptions: HumanAssumptions,
    ) -> None:
        # Very low O2 fraction
        params = HabitatParameters.from_radius_and_gravity(
            1000.0,
            o2_fraction=0.10,
        )
        result = constraint.evaluate(params, assumptions)
        # 101.3 * 0.10 = 10.13 kPa < 16 kPa
        assert not result.feasible

    def test_hyperoxic_atmosphere_fails(
        self,
        constraint: AtmosphereConstraint,
        assumptions: HumanAssumptions,
    ) -> None:
        # Pure O2 at standard pressure
        params = HabitatParameters.from_radius_and_gravity(
            1000.0,
            o2_fraction=1.0,
        )
        result = constraint.evaluate(params, assumptions)
        # 101.3 kPa > 50 kPa
        assert not result.feasible

    def test_sp413_atmosphere_passes(
        self,
        constraint: AtmosphereConstraint,
        assumptions: HumanAssumptions,
    ) -> None:
        # SP-413: 51 kPa, 44.5% O2 => pO2 = 22.7 kPa
        params = HabitatParameters.from_radius_and_gravity(
            1000.0,
            internal_pressure_kpa=51.0,
            o2_fraction=0.445,
        )
        result = constraint.evaluate(params, assumptions)
        assert result.feasible

    def test_nasa_exploration_atmosphere_passes(
        self,
        constraint: AtmosphereConstraint,
        assumptions: HumanAssumptions,
    ) -> None:
        # 56.5 kPa, 34% O2 => pO2 = 19.2 kPa
        params = HabitatParameters.from_radius_and_gravity(
            1000.0,
            internal_pressure_kpa=56.5,
            o2_fraction=0.34,
        )
        result = constraint.evaluate(params, assumptions)
        assert result.feasible

    def test_bounds_have_range(
        self,
        constraint: AtmosphereConstraint,
        assumptions: HumanAssumptions,
    ) -> None:
        bounds = constraint.compute_bounds(assumptions)
        assert len(bounds) == 1
        assert bounds[0].lower == 16.0
        assert bounds[0].upper == 50.0
