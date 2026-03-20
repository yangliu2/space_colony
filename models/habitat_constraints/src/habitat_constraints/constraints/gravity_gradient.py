"""Gravity gradient constraint — head-to-foot gravity difference."""

from __future__ import annotations

from habitat_constraints.core.parameters import (
    ConstraintResult,
    HabitatParameters,
    HumanAssumptions,
    ParameterBound,
)


class GravityGradientConstraint:
    """Head-to-foot gravity gradient: delta_g/g = h/r.

    A person standing radially in a rotating habitat experiences
    stronger gravity at their feet (larger r) than at their head
    (smaller r). Large gradients cause discomfort and physiological
    issues.
    """

    @property
    def name(self) -> str:
        return "gravity_gradient"

    @property
    def description(self) -> str:
        return "Head-to-foot gravity gradient (delta_g/g = h/r)"

    def evaluate(
        self,
        params: HabitatParameters,
        assumptions: HumanAssumptions,
    ) -> ConstraintResult:
        gradient_pct = (assumptions.person_height_m / params.radius_m) * 100.0
        max_pct = assumptions.max_gravity_gradient_pct
        feasible = gradient_pct <= max_pct

        # Gravity at feet vs head
        g_feet = params.gravity_g
        g_head = g_feet * (1.0 - assumptions.person_height_m / params.radius_m)

        bounds = self.compute_bounds(assumptions)
        return ConstraintResult(
            constraint_name=self.name,
            feasible=feasible,
            bounds=bounds,
            details={
                "gradient_pct": gradient_pct,
                "max_gradient_pct": max_pct,
                "gravity_at_feet_g": g_feet,
                "gravity_at_head_g": g_head,
            },
        )

    def compute_bounds(
        self,
        assumptions: HumanAssumptions,
    ) -> list[ParameterBound]:
        r_min = assumptions.person_height_m / (
            assumptions.max_gravity_gradient_pct / 100.0
        )
        return [
            ParameterBound(
                parameter_name="radius_m",
                lower=r_min,
                constraint_name=self.name,
                description=(
                    f"r >= {r_min:.1f} m for gradient <= "
                    f"{assumptions.max_gravity_gradient_pct}%"
                ),
            ),
        ]
