"""Tests for radiation shielding constraint."""

from __future__ import annotations

import pytest

from habitat_constraints.constraints.radiation import (
    RadiationConstraint,
)
from habitat_constraints.core.parameters import (
    HabitatParameters,
    HumanAssumptions,
)


@pytest.fixture
def constraint() -> RadiationConstraint:
    return RadiationConstraint()


@pytest.fixture
def assumptions() -> HumanAssumptions:
    return HumanAssumptions()


class TestRadiationConstraint:
    def test_adequate_shielding_passes(
        self,
        constraint: RadiationConstraint,
        assumptions: HumanAssumptions,
    ) -> None:
        params = HabitatParameters.from_radius_and_gravity(
            3200.0,
            shielding_areal_density_kg_m2=4500.0,
        )
        result = constraint.evaluate(params, assumptions)
        assert result.feasible

    def test_insufficient_shielding_fails(
        self,
        constraint: RadiationConstraint,
        assumptions: HumanAssumptions,
    ) -> None:
        params = HabitatParameters.from_radius_and_gravity(
            3200.0,
            shielding_areal_density_kg_m2=2000.0,
        )
        result = constraint.evaluate(params, assumptions)
        assert not result.feasible

    def test_exact_threshold_passes(
        self,
        constraint: RadiationConstraint,
        assumptions: HumanAssumptions,
    ) -> None:
        params = HabitatParameters.from_radius_and_gravity(
            1000.0,
            shielding_areal_density_kg_m2=4500.0,
        )
        result = constraint.evaluate(params, assumptions)
        assert result.feasible

    def test_shielding_mass_computed_with_geometry(
        self,
        constraint: RadiationConstraint,
        assumptions: HumanAssumptions,
    ) -> None:
        params = HabitatParameters.from_radius_and_gravity(
            982.0,
            length_m=2000.0,
            shielding_areal_density_kg_m2=4500.0,
        )
        result = constraint.evaluate(params, assumptions)
        assert result.details["shielding_mass_mt"] > 0

    def test_bounds_have_lower_limit(
        self,
        constraint: RadiationConstraint,
        assumptions: HumanAssumptions,
    ) -> None:
        bounds = constraint.compute_bounds(assumptions)
        assert len(bounds) == 1
        assert bounds[0].lower == 4500.0

    def test_custom_threshold(
        self,
        constraint: RadiationConstraint,
    ) -> None:
        relaxed = HumanAssumptions(
            min_shielding_areal_density_kg_m2=2000.0,
        )
        params = HabitatParameters.from_radius_and_gravity(
            1000.0,
            shielding_areal_density_kg_m2=2500.0,
        )
        result = constraint.evaluate(params, relaxed)
        assert result.feasible
