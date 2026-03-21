"""Tests for population constraint."""

from __future__ import annotations

import pytest

from habitat_constraints.constraints.population import (
    PopulationConstraint,
)
from habitat_constraints.core.parameters import (
    HabitatParameters,
    HumanAssumptions,
)


@pytest.fixture
def constraint() -> PopulationConstraint:
    return PopulationConstraint()


@pytest.fixture
def assumptions() -> HumanAssumptions:
    return HumanAssumptions()


class TestPopulationConstraint:
    def test_large_population_passes(
        self,
        constraint: PopulationConstraint,
        assumptions: HumanAssumptions,
    ) -> None:
        params = HabitatParameters.from_radius_and_gravity(
            3200.0,
            length_m=32000.0,
            population=10000,
        )
        result = constraint.evaluate(params, assumptions)
        assert result.feasible

    def test_tiny_population_fails(
        self,
        constraint: PopulationConstraint,
        assumptions: HumanAssumptions,
    ) -> None:
        params = HabitatParameters.from_radius_and_gravity(
            3200.0,
            length_m=32000.0,
            population=50,
        )
        result = constraint.evaluate(params, assumptions)
        assert not result.feasible

    def test_zero_population_skips_check(
        self,
        constraint: PopulationConstraint,
        assumptions: HumanAssumptions,
    ) -> None:
        # population=0 means "not specified" — passes by default
        params = HabitatParameters.from_radius_and_gravity(1000.0)
        result = constraint.evaluate(params, assumptions)
        assert result.feasible

    def test_insufficient_volume_fails(
        self,
        constraint: PopulationConstraint,
        assumptions: HumanAssumptions,
    ) -> None:
        # Tiny cylinder, lots of people
        params = HabitatParameters.from_radius_and_gravity(
            100.0,
            length_m=100.0,
            population=1000000,
        )
        result = constraint.evaluate(params, assumptions)
        assert not result.feasible

    def test_adequate_volume_passes(
        self,
        constraint: PopulationConstraint,
        assumptions: HumanAssumptions,
    ) -> None:
        params = HabitatParameters.from_radius_and_gravity(
            982.0,
            length_m=2000.0,
            population=8000,
        )
        result = constraint.evaluate(params, assumptions)
        assert result.feasible
        assert result.details["volume_per_person_m3"] > 100.0

    def test_bounds_include_both_checks(
        self,
        constraint: PopulationConstraint,
        assumptions: HumanAssumptions,
    ) -> None:
        bounds = constraint.compute_bounds(assumptions)
        assert len(bounds) == 2
        names = {b.parameter_name for b in bounds}
        assert "population" in names
        assert "volume_per_person_m3" in names
