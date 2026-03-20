"""Gravity level constraint — effective gravity must be in acceptable range."""

from __future__ import annotations

import math

from habitat_constraints.core.parameters import (
    EARTH_G,
    ConstraintResult,
    HabitatParameters,
    HumanAssumptions,
    ParameterBound,
)

# Relative tolerance for floating-point gravity comparisons.
_REL_TOL = 1e-9


class GravityLevelConstraint:
    """Effective gravity g_eff = omega^2 * r must fall within
    [min_gravity_g, max_gravity_g] for long-term habitation.
    """

    @property
    def name(self) -> str:
        return "gravity_level"

    @property
    def description(self) -> str:
        return "Effective gravity must be within acceptable range"

    def evaluate(
        self,
        params: HabitatParameters,
        assumptions: HumanAssumptions,
    ) -> ConstraintResult:
        g_eff = params.gravity_g
        low = assumptions.min_gravity_g * (1.0 - _REL_TOL)
        high = assumptions.max_gravity_g * (1.0 + _REL_TOL)
        feasible = low <= g_eff <= high

        bounds = self._bounds_for_radius(params.radius_m, assumptions)
        return ConstraintResult(
            constraint_name=self.name,
            feasible=feasible,
            bounds=bounds,
            details={
                "gravity_g": g_eff,
                "min_gravity_g": assumptions.min_gravity_g,
                "max_gravity_g": assumptions.max_gravity_g,
            },
        )

    def compute_bounds(
        self,
        assumptions: HumanAssumptions,
    ) -> list[ParameterBound]:
        # General bounds: gravity_g in [min, max] doesn't reduce to
        # a single radius/omega bound without fixing the other.
        # We express the relationship for reference.
        return [
            ParameterBound(
                parameter_name="gravity_g",
                lower=assumptions.min_gravity_g,
                upper=assumptions.max_gravity_g,
                constraint_name=self.name,
                description=(
                    f"gravity in [{assumptions.min_gravity_g}g, "
                    f"{assumptions.max_gravity_g}g]"
                ),
            ),
        ]

    def _bounds_for_radius(
        self,
        radius_m: float,
        assumptions: HumanAssumptions,
    ) -> list[ParameterBound]:
        """Compute omega bounds for a specific radius."""
        omega_min = math.sqrt(assumptions.min_gravity_g * EARTH_G / radius_m)
        omega_max = math.sqrt(assumptions.max_gravity_g * EARTH_G / radius_m)
        return [
            ParameterBound(
                parameter_name="angular_velocity_rad_s",
                lower=omega_min,
                upper=omega_max,
                constraint_name=self.name,
                description=(
                    f"omega in [{omega_min:.4f}, {omega_max:.4f}] rad/s "
                    f"for r={radius_m}m"
                ),
            ),
        ]
