"""Tests for the gravity gradient constraint."""

import pytest

from habitat_constraints.core.parameters import (
    HabitatParameters,
    HumanAssumptions,
)
from habitat_constraints.constraints.gravity_gradient import (
    GravityGradientConstraint,
)


class TestGravityGradientConstraint:
    def setup_method(self) -> None:
        self.constraint = GravityGradientConstraint()
        self.assumptions = HumanAssumptions()

    def test_protocol_properties(self) -> None:
        assert self.constraint.name == "gravity_gradient"

    def test_oneill_is_feasible(self, oneill_params: HabitatParameters) -> None:
        """At r=3200m, gradient = 1.8/3200 = 0.056%, well under 1%."""
        result = self.constraint.evaluate(oneill_params, self.assumptions)
        assert result.feasible is True
        assert result.details["gradient_pct"] == pytest.approx(0.05625, rel=0.01)

    def test_small_habitat_infeasible(
        self, small_habitat_params: HabitatParameters
    ) -> None:
        """At r=100m, gradient = 1.8/100 = 1.8%, exceeds 1%."""
        result = self.constraint.evaluate(small_habitat_params, self.assumptions)
        assert result.feasible is False
        assert result.details["gradient_pct"] == pytest.approx(1.8, rel=0.01)

    def test_medium_habitat_feasible(
        self, medium_habitat_params: HabitatParameters
    ) -> None:
        """At r=500m, gradient = 1.8/500 = 0.36%, under 1%."""
        result = self.constraint.evaluate(medium_habitat_params, self.assumptions)
        assert result.feasible is True
        assert result.details["gradient_pct"] == pytest.approx(0.36, rel=0.01)

    def test_head_vs_foot_gravity(self, oneill_params: HabitatParameters) -> None:
        """Head gravity should be less than foot gravity."""
        result = self.constraint.evaluate(oneill_params, self.assumptions)
        assert result.details["gravity_at_head_g"] < result.details["gravity_at_feet_g"]

    def test_bounds_r_min(self) -> None:
        """r_min = 1.8 / (1.0/100) = 180m."""
        bounds = self.constraint.compute_bounds(self.assumptions)
        r_bound = bounds[0]
        assert r_bound.parameter_name == "radius_m"
        assert r_bound.lower == pytest.approx(180.0)

    def test_taller_person_needs_larger_radius(self) -> None:
        """A 2.0m tall person needs r_min = 200m vs 180m."""
        tall = HumanAssumptions(person_height_m=2.0)
        bounds = self.constraint.compute_bounds(tall)
        r_bound = bounds[0]
        assert r_bound.lower == pytest.approx(200.0)
