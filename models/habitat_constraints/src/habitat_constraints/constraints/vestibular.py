"""Vestibular comfort constraint — limits rotation rate (RPM)."""

from __future__ import annotations

import math

from habitat_constraints.core.parameters import (
    EARTH_G,
    ConstraintResult,
    HabitatParameters,
    HumanAssumptions,
    ParameterBound,
)


class VestibularConstraint:
    """The human vestibular system becomes uncomfortable above ~2 RPM.

    This imposes an upper bound on angular velocity and, for a given
    gravity target, a lower bound on radius.
    """

    @property
    def name(self) -> str:
        return "vestibular"

    @property
    def description(self) -> str:
        return "Vestibular comfort limit on rotation rate (RPM)"

    def evaluate(
        self,
        params: HabitatParameters,
        assumptions: HumanAssumptions,
    ) -> ConstraintResult:
        current_rpm = params.rpm
        max_rpm = assumptions.max_comfortable_rpm
        feasible = current_rpm <= max_rpm
        margin = max_rpm - current_rpm

        bounds = self.compute_bounds(assumptions)
        return ConstraintResult(
            constraint_name=self.name,
            feasible=feasible,
            bounds=bounds,
            details={
                "current_rpm": current_rpm,
                "max_rpm": max_rpm,
                "margin_rpm": margin,
            },
        )

    def compute_bounds(
        self,
        assumptions: HumanAssumptions,
    ) -> list[ParameterBound]:
        omega_max = assumptions.max_comfortable_rpm * 2.0 * math.pi / 60.0
        # For 1g at this omega: r_min = g / omega^2
        r_min_1g = EARTH_G / (omega_max**2)

        return [
            ParameterBound(
                parameter_name="angular_velocity_rad_s",
                upper=omega_max,
                constraint_name=self.name,
                description=(
                    f"omega <= {omega_max:.4f} rad/s "
                    f"({assumptions.max_comfortable_rpm} RPM)"
                ),
            ),
            ParameterBound(
                parameter_name="radius_m",
                lower=r_min_1g,
                constraint_name=self.name,
                description=(
                    f"r >= {r_min_1g:.1f} m for 1g at "
                    f"{assumptions.max_comfortable_rpm} RPM"
                ),
            ),
        ]
