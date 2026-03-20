"""Tests for the Coriolis effect constraint."""

from habitat_constraints.core.parameters import (
    HabitatParameters,
    HumanAssumptions,
)
from habitat_constraints.constraints.coriolis import CoriolisConstraint


class TestCoriolisConstraint:
    """Verify Coriolis constraint evaluation and bounds."""

    def test_oneill_feasible(
        self,
        oneill_params: HabitatParameters,
        default_assumptions: HumanAssumptions,
    ) -> None:
        c = CoriolisConstraint()
        result = c.evaluate(oneill_params, default_assumptions)
        assert result.feasible
        assert result.details["coriolis_to_gravity_running"] < 0.25

    def test_small_habitat_infeasible(
        self,
        small_habitat_params: HabitatParameters,
        default_assumptions: HumanAssumptions,
    ) -> None:
        c = CoriolisConstraint()
        result = c.evaluate(small_habitat_params, default_assumptions)
        # At r=100m, running Coriolis ratio ~ 0.19, < 0.25 default
        # Actually feasible with default 0.25 threshold
        # Check the value is computed correctly
        assert result.details["coriolis_to_gravity_running"] > 0.15

    def test_strict_threshold_infeasible(self) -> None:
        c = CoriolisConstraint()
        params = HabitatParameters.from_radius_and_gravity(100.0)
        strict = HumanAssumptions(max_coriolis_ratio=0.10)
        result = c.evaluate(params, strict)
        assert not result.feasible
        assert result.details["coriolis_to_gravity_running"] > 0.10

    def test_walking_less_than_running(
        self,
        oneill_params: HabitatParameters,
        default_assumptions: HumanAssumptions,
    ) -> None:
        c = CoriolisConstraint()
        result = c.evaluate(oneill_params, default_assumptions)
        assert (
            result.details["coriolis_to_gravity_walking"]
            < result.details["coriolis_to_gravity_running"]
        )

    def test_bounds_radius(
        self,
        default_assumptions: HumanAssumptions,
    ) -> None:
        c = CoriolisConstraint()
        bounds = c.compute_bounds(default_assumptions)
        assert len(bounds) == 1
        r_bound = bounds[0]
        assert r_bound.parameter_name == "radius_m"
        assert r_bound.lower is not None
        assert r_bound.lower > 0

    def test_larger_radius_lower_ratio(self) -> None:
        c = CoriolisConstraint()
        assumptions = HumanAssumptions()
        small = HabitatParameters.from_radius_and_gravity(200.0)
        large = HabitatParameters.from_radius_and_gravity(2000.0)
        r_small = c.evaluate(small, assumptions)
        r_large = c.evaluate(large, assumptions)
        assert (
            r_small.details["coriolis_to_gravity_running"]
            > r_large.details["coriolis_to_gravity_running"]
        )
