"""Tests for the gravity level constraint."""

import pytest

from habitat_constraints.core.parameters import (
    HabitatParameters,
    HumanAssumptions,
)
from habitat_constraints.constraints.gravity_level import (
    GravityLevelConstraint,
)


class TestGravityLevelConstraint:
    def setup_method(self) -> None:
        self.constraint = GravityLevelConstraint()
        self.assumptions = HumanAssumptions()

    def test_protocol_properties(self) -> None:
        assert self.constraint.name == "gravity_level"

    def test_1g_is_feasible(self, oneill_params: HabitatParameters) -> None:
        result = self.constraint.evaluate(oneill_params, self.assumptions)
        assert result.feasible is True
        assert result.details["gravity_g"] == pytest.approx(1.0, rel=0.01)

    def test_03g_is_feasible(self) -> None:
        """0.3g is the lower bound, should be feasible."""
        params = HabitatParameters.from_radius_and_gravity(1000.0, target_gravity_g=0.3)
        result = self.constraint.evaluate(params, self.assumptions)
        assert result.feasible is True

    def test_01g_is_infeasible(self) -> None:
        """0.1g is below the 0.3g minimum."""
        params = HabitatParameters.from_radius_and_gravity(1000.0, target_gravity_g=0.1)
        result = self.constraint.evaluate(params, self.assumptions)
        assert result.feasible is False

    def test_15g_is_infeasible(self) -> None:
        """1.5g exceeds the 1.0g maximum."""
        params = HabitatParameters.from_radius_and_gravity(1000.0, target_gravity_g=1.5)
        result = self.constraint.evaluate(params, self.assumptions)
        assert result.feasible is False

    def test_bounds_gravity_range(self) -> None:
        bounds = self.constraint.compute_bounds(self.assumptions)
        g_bound = next(b for b in bounds if b.parameter_name == "gravity_g")
        assert g_bound.lower == 0.3
        assert g_bound.upper == 1.0
