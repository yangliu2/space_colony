"""Tests for HabitatParameters and HumanAssumptions."""

import math

import pytest
from pydantic import ValidationError

from habitat_constraints.core.parameters import (
    EARTH_G,
    HabitatParameters,
    HumanAssumptions,
)


class TestHabitatParameters:
    def test_oneill_reference_values(self) -> None:
        """Validate against O'Neill's reference design."""
        params = HabitatParameters(radius_m=3200.0, angular_velocity_rad_s=0.05537)
        assert params.rpm == pytest.approx(0.5288, rel=0.01)
        assert params.period_s == pytest.approx(113.5, rel=0.01)
        assert params.rim_speed_m_s == pytest.approx(177.2, rel=0.01)
        assert params.gravity_g == pytest.approx(1.0, rel=0.02)

    def test_from_radius_and_gravity_1g(self) -> None:
        """Factory method should produce correct omega for 1g."""
        params = HabitatParameters.from_radius_and_gravity(3200.0)
        assert params.gravity_g == pytest.approx(1.0, rel=1e-6)
        expected_omega = math.sqrt(EARTH_G / 3200.0)
        assert params.angular_velocity_rad_s == pytest.approx(expected_omega)

    def test_from_radius_and_gravity_03g(self) -> None:
        """Factory method with 0.3g target."""
        params = HabitatParameters.from_radius_and_gravity(1000.0, target_gravity_g=0.3)
        assert params.gravity_g == pytest.approx(0.3, rel=1e-6)

    def test_radius_must_be_positive(self) -> None:
        with pytest.raises(ValidationError):
            HabitatParameters(radius_m=0, angular_velocity_rad_s=0.1)

    def test_omega_must_be_positive(self) -> None:
        with pytest.raises(ValidationError):
            HabitatParameters(radius_m=100, angular_velocity_rad_s=-0.1)

    def test_small_radius_high_rpm(self) -> None:
        """r=100m at 1g should be ~3 RPM."""
        params = HabitatParameters.from_radius_and_gravity(100.0)
        assert params.rpm == pytest.approx(2.99, rel=0.02)


class TestHumanAssumptions:
    def test_defaults(self) -> None:
        a = HumanAssumptions()
        assert a.person_height_m == 1.8
        assert a.max_comfortable_rpm == 2.0
        assert a.min_gravity_g == 0.3
        assert a.max_gravity_g == 1.0

    def test_custom_values(self) -> None:
        a = HumanAssumptions(
            person_height_m=2.0,
            max_comfortable_rpm=3.0,
        )
        assert a.person_height_m == 2.0
        assert a.max_comfortable_rpm == 3.0

    def test_validation_rejects_negative(self) -> None:
        with pytest.raises(ValidationError):
            HumanAssumptions(person_height_m=-1.0)
