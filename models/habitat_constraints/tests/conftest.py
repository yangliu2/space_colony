"""Shared fixtures for habitat constraint tests."""

from __future__ import annotations

import pytest

from habitat_constraints.core.parameters import (
    HabitatParameters,
    HumanAssumptions,
)
from habitat_constraints.constraints.vestibular import (
    VestibularConstraint,
)
from habitat_constraints.constraints.gravity_level import (
    GravityLevelConstraint,
)
from habitat_constraints.constraints.gravity_gradient import (
    GravityGradientConstraint,
)
from habitat_constraints.constraints.coriolis import CoriolisConstraint
from habitat_constraints.constraints.cross_coupling import (
    CrossCouplingConstraint,
)
from habitat_constraints.constraints.rim_speed import RimSpeedConstraint
from habitat_constraints.constraints.radiation import (
    RadiationConstraint,
)
from habitat_constraints.constraints.atmosphere import (
    AtmosphereConstraint,
)
from habitat_constraints.constraints.population import (
    PopulationConstraint,
)


@pytest.fixture
def default_assumptions() -> HumanAssumptions:
    """Default human assumptions."""
    return HumanAssumptions()


@pytest.fixture
def oneill_params() -> HabitatParameters:
    """O'Neill's reference design: r=3200m, ~1g."""
    return HabitatParameters.from_radius_and_gravity(3200.0)


@pytest.fixture
def small_habitat_params() -> HabitatParameters:
    """Small habitat at r=100m, 1g — known to be problematic."""
    return HabitatParameters.from_radius_and_gravity(100.0)


@pytest.fixture
def medium_habitat_params() -> HabitatParameters:
    """Medium habitat at r=500m, 1g — near thresholds."""
    return HabitatParameters.from_radius_and_gravity(500.0)


@pytest.fixture
def rotational_constraints() -> (
    list[
        VestibularConstraint
        | GravityLevelConstraint
        | GravityGradientConstraint
        | CoriolisConstraint
        | CrossCouplingConstraint
        | RimSpeedConstraint
    ]
):
    """Rotational constraints only (Phase 1 + Phase 2)."""
    return [
        VestibularConstraint(),
        GravityLevelConstraint(),
        GravityGradientConstraint(),
        CoriolisConstraint(),
        CrossCouplingConstraint(),
        RimSpeedConstraint(),
    ]


@pytest.fixture
def all_constraints() -> (
    list[
        VestibularConstraint
        | GravityLevelConstraint
        | GravityGradientConstraint
        | CoriolisConstraint
        | CrossCouplingConstraint
        | RimSpeedConstraint
        | RadiationConstraint
        | AtmosphereConstraint
        | PopulationConstraint
    ]
):
    """All constraints (Phase 1 + Phase 2 + Phase 3)."""
    return [
        VestibularConstraint(),
        GravityLevelConstraint(),
        GravityGradientConstraint(),
        CoriolisConstraint(),
        CrossCouplingConstraint(),
        RimSpeedConstraint(),
        RadiationConstraint(),
        AtmosphereConstraint(),
        PopulationConstraint(),
    ]
