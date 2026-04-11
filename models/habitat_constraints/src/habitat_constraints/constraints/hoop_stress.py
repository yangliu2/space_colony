"""Structural hoop stress constraint for the rotating cylinder.

The hull experiences two additive hoop stress components:
  σ_rot = ρ · ω² · r²     (centrifugal self-weight)
  σ_p   = P · r / t        (internal atmospheric pressure)

The total must satisfy σ_hoop · FoS ≤ σ_yield.
See plans/structural_engineering.md for derivation.
"""

from __future__ import annotations

from habitat_constraints.core.parameters import (
    ConstraintResult,
    HabitatParameters,
    HumanAssumptions,
    ParameterBound,
)


class HoopStressConstraint:
    """Total hoop stress must remain within material yield strength."""

    @property
    def name(self) -> str:
        return "hoop_stress"

    @property
    def description(self) -> str:
        return (
            "Hoop stress (rotational + pressure) must not exceed "
            "material yield strength with safety factor"
        )

    def evaluate(
        self,
        params: HabitatParameters,
        assumptions: HumanAssumptions,
    ) -> ConstraintResult:
        rho = params.hull_density_kg_m3
        omega = params.angular_velocity_rad_s
        r = params.radius_m
        P = params.internal_pressure_kpa * 1000.0  # kPa → Pa
        t = params.wall_thickness_m

        sigma_rot = rho * omega**2 * r**2  # Pa
        sigma_p = P * r / t  # Pa
        sigma_hoop = sigma_rot + sigma_p  # Pa
        sigma_hoop_mpa = sigma_hoop / 1e6  # → MPa

        allowable_mpa = (
            assumptions.yield_strength_mpa / assumptions.structural_safety_factor
        )
        feasible = sigma_hoop_mpa <= allowable_mpa
        margin_pct = (
            (allowable_mpa - sigma_hoop_mpa) / allowable_mpa * 100.0
            if allowable_mpa > 0
            else 0.0
        )

        bounds = self.compute_bounds(assumptions)
        return ConstraintResult(
            constraint_name=self.name,
            feasible=feasible,
            bounds=bounds,
            details={
                "sigma_rot_mpa": round(sigma_rot / 1e6, 1),
                "sigma_pressure_mpa": round(sigma_p / 1e6, 1),
                "sigma_hoop_mpa": round(sigma_hoop_mpa, 1),
                "allowable_mpa": round(allowable_mpa, 1),
                "safety_factor": assumptions.structural_safety_factor,
                "margin_pct": round(margin_pct, 1),
            },
        )

    def compute_bounds(
        self,
        assumptions: HumanAssumptions,
    ) -> list[ParameterBound]:
        allowable = assumptions.yield_strength_mpa / assumptions.structural_safety_factor
        return [
            ParameterBound(
                parameter_name="radius_m",
                upper=None,  # depends on ω, ρ, P, t
                constraint_name=self.name,
                description=(
                    f"σ_hoop ≤ {allowable:.0f} MPa "
                    f"(σ_y={assumptions.yield_strength_mpa:.0f} MPa "
                    f"/ FoS={assumptions.structural_safety_factor})"
                ),
            ),
        ]
