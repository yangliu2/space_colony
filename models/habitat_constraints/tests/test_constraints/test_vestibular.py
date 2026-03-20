"""Tests for the vestibular comfort constraint."""

import math

import pytest

from habitat_constraints.core.parameters import (
    EARTH_G,
    HabitatParameters,
    HumanAssumptions,
)
from habitat_constraints.constraints.vestibular import VestibularConstraint


class TestVestibularConstraint:
    def setup_method(self) -> None:
        self.constraint = VestibularConstraint()
        self.assumptions = HumanAssumptions()

    def test_protocol_properties(self) -> None:
        assert self.constraint.name == "vestibular"
        assert "RPM" in self.constraint.description

    def test_oneill_is_feasible(self, oneill_params: HabitatParameters) -> None:
        """O'Neill at 0.53 RPM is well within 2 RPM limit."""
        result = self.constraint.evaluate(oneill_params, self.assumptions)
        assert result.feasible is True
        assert result.details["current_rpm"] == pytest.approx(0.53, rel=0.02)

    def test_small_habitat_infeasible(
        self, small_habitat_params: HabitatParameters
    ) -> None:
        """r=100m at 1g requires ~3 RPM, exceeds 2 RPM limit."""
        result = self.constraint.evaluate(small_habitat_params, self.assumptions)
        assert result.feasible is False
        assert result.details["current_rpm"] > 2.0

    def test_bounds_omega_max(self) -> None:
        """Upper omega bound should correspond to 2 RPM."""
        bounds = self.constraint.compute_bounds(self.assumptions)
        omega_bound = next(
            b for b in bounds if b.parameter_name == "angular_velocity_rad_s"
        )
        expected_omega = 2.0 * 2.0 * math.pi / 60.0
        assert omega_bound.upper == pytest.approx(expected_omega)

    def test_bounds_r_min_1g(self) -> None:
        """Minimum radius for 1g at 2 RPM should be ~224m."""
        bounds = self.constraint.compute_bounds(self.assumptions)
        r_bound = next(b for b in bounds if b.parameter_name == "radius_m")
        # r_min = g / omega_max^2
        omega_max = 2.0 * 2.0 * math.pi / 60.0
        expected_r = EARTH_G / omega_max**2
        assert r_bound.lower == pytest.approx(expected_r)
        assert r_bound.lower == pytest.approx(224.0, rel=0.02)

    def test_custom_rpm_limit(self) -> None:
        """With 4 RPM limit, smaller radii become feasible."""
        relaxed = HumanAssumptions(max_comfortable_rpm=4.0)
        result = self.constraint.evaluate(
            HabitatParameters.from_radius_and_gravity(100.0),
            relaxed,
        )
        # 100m at 1g is ~3 RPM, within 4 RPM limit
        assert result.feasible is True
