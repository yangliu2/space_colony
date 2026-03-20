"""Tests for the cross-coupled rotation constraint."""

from habitat_constraints.core.parameters import (
    HabitatParameters,
    HumanAssumptions,
)
from habitat_constraints.constraints.cross_coupling import (
    CrossCouplingConstraint,
)


class TestCrossCouplingConstraint:
    """Verify cross-coupled angular acceleration constraint."""

    def test_oneill_feasible(
        self,
        oneill_params: HabitatParameters,
        default_assumptions: HumanAssumptions,
    ) -> None:
        c = CrossCouplingConstraint()
        result = c.evaluate(oneill_params, default_assumptions)
        assert result.feasible
        # 0.53 RPM should produce low cross-coupling (~3.3 deg/s²)
        assert result.details["cross_coupled_deg_s2"] < 6.0

    def test_small_habitat_infeasible(
        self,
        small_habitat_params: HabitatParameters,
        default_assumptions: HumanAssumptions,
    ) -> None:
        c = CrossCouplingConstraint()
        result = c.evaluate(small_habitat_params, default_assumptions)
        # At r=100m, ~3 RPM, cross-coupling ~ 18.8 deg/s²
        assert result.details["cross_coupled_deg_s2"] > 6.0
        assert not result.feasible

    def test_manual_calculation(self) -> None:
        """Verify against hand calculation."""
        c = CrossCouplingConstraint()
        # At exactly 2 RPM: omega = 2*pi*2/60 = 0.2094 rad/s
        # Head turn at 60 deg/s = 1.0472 rad/s
        # alpha_cc = 0.2094 * 1.0472 = 0.2193 rad/s²
        # In deg/s² = 0.2193 * 180/pi = 12.566 deg/s²
        # Simpler: omega_rpm * head_rate_deg * (2pi/60) = cross_coupling
        params = HabitatParameters.from_radius_and_gravity(224.0)
        assumptions = HumanAssumptions()
        result = c.evaluate(params, assumptions)
        # ~2 RPM * 60 deg/s => expect ~12.5 deg/s²
        cc = result.details["cross_coupled_deg_s2"]
        assert 12.0 < cc < 13.0

    def test_adapted_threshold(self) -> None:
        """Higher threshold (adapted crew) allows smaller habitats."""
        c = CrossCouplingConstraint()
        params = HabitatParameters.from_radius_and_gravity(500.0)
        strict = HumanAssumptions(max_cross_coupling_deg_s2=3.0)
        relaxed = HumanAssumptions(max_cross_coupling_deg_s2=15.0)
        assert not c.evaluate(params, strict).feasible
        assert c.evaluate(params, relaxed).feasible

    def test_bounds_omega_and_radius(
        self,
        default_assumptions: HumanAssumptions,
    ) -> None:
        c = CrossCouplingConstraint()
        bounds = c.compute_bounds(default_assumptions)
        assert len(bounds) == 2
        names = {b.parameter_name for b in bounds}
        assert "angular_velocity_rad_s" in names
        assert "radius_m" in names

    def test_slower_head_turns_relaxes(self) -> None:
        """Slower head turns reduce cross-coupling."""
        c = CrossCouplingConstraint()
        params = HabitatParameters.from_radius_and_gravity(300.0)
        fast_head = HumanAssumptions(head_turn_rate_deg_s=90.0)
        slow_head = HumanAssumptions(head_turn_rate_deg_s=30.0)
        r_fast = c.evaluate(params, fast_head)
        r_slow = c.evaluate(params, slow_head)
        assert (
            r_fast.details["cross_coupled_deg_s2"]
            > r_slow.details["cross_coupled_deg_s2"]
        )
