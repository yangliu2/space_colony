"""Pydantic models for habitat design parameters and constraint results."""

from __future__ import annotations

import math

from pydantic import BaseModel, Field

# Earth standard gravity (m/s^2)
EARTH_G = 9.80665


class HabitatParameters(BaseModel):
    """Primary design variables for a rotating cylinder habitat.

    All values in SI units. Convenience properties provide derived
    quantities and common unit conversions.
    """

    radius_m: float = Field(gt=0, description="Cylinder inner radius (m)")
    angular_velocity_rad_s: float = Field(gt=0, description="Angular velocity (rad/s)")

    @property
    def gravity_g(self) -> float:
        """Effective gravity at the rim, in multiples of Earth g."""
        return (self.angular_velocity_rad_s**2 * self.radius_m) / EARTH_G

    @property
    def rpm(self) -> float:
        """Rotation rate in revolutions per minute."""
        return self.angular_velocity_rad_s * 60.0 / (2.0 * math.pi)

    @property
    def rim_speed_m_s(self) -> float:
        """Tangential speed at the rim (m/s)."""
        return self.angular_velocity_rad_s * self.radius_m

    @property
    def period_s(self) -> float:
        """Rotation period (seconds per revolution)."""
        return 2.0 * math.pi / self.angular_velocity_rad_s

    @staticmethod
    def from_radius_and_gravity(
        radius_m: float,
        target_gravity_g: float = 1.0,
    ) -> HabitatParameters:
        """Create parameters for a given radius that achieves target gravity."""
        omega = math.sqrt(target_gravity_g * EARTH_G / radius_m)
        return HabitatParameters(
            radius_m=radius_m,
            angular_velocity_rad_s=omega,
        )


class HumanAssumptions(BaseModel):
    """Assumed biological and comfort constants.

    These are the 'soft' parameters we vary in sensitivity analysis.
    Each field has a sensible default based on literature.
    """

    person_height_m: float = Field(default=1.8, gt=0, description="Standing height (m)")
    walking_speed_m_s: float = Field(
        default=1.4, gt=0, description="Typical walking speed (m/s)"
    )
    running_speed_m_s: float = Field(
        default=3.0, gt=0, description="Typical running speed (m/s)"
    )
    max_comfortable_rpm: float = Field(
        default=2.0, gt=0, description="Vestibular comfort RPM limit"
    )
    min_gravity_g: float = Field(
        default=0.3, gt=0, description="Minimum acceptable gravity (g)"
    )
    max_gravity_g: float = Field(
        default=1.0, gt=0, description="Maximum acceptable gravity (g)"
    )
    max_gravity_gradient_pct: float = Field(
        default=1.0,
        gt=0,
        description="Max head-to-foot gravity gradient (%)",
    )
    max_coriolis_ratio: float = Field(
        default=0.25,
        gt=0,
        description="Max Coriolis-to-gravity acceleration ratio",
    )
    max_cross_coupling_deg_s2: float = Field(
        default=6.0,
        gt=0,
        description=(
            "Max cross-coupled angular acceleration (deg/s^2) "
            "from head turns during rotation. "
            "~3 for unadapted, ~6 for adapted crew."
        ),
    )
    head_turn_rate_deg_s: float = Field(
        default=60.0,
        gt=0,
        description="Typical head turn rate (deg/s)",
    )
    max_rim_speed_m_s: float = Field(
        default=300.0,
        gt=0,
        description=(
            "Max tangential rim speed (m/s) — " "structural and aerodynamic limit"
        ),
    )


class ParameterBound(BaseModel):
    """A bound on a single design parameter produced by a constraint."""

    parameter_name: str
    lower: float | None = None
    upper: float | None = None
    constraint_name: str
    description: str


class ConstraintResult(BaseModel):
    """Output of evaluating one constraint at a specific design point."""

    constraint_name: str
    feasible: bool
    bounds: list[ParameterBound]
    details: dict[str, float] = Field(default_factory=dict)
