"""Cylinder length constraint based on bending mode resonance.

Maximum safe length scales as L_max = C * r^(5/4), where C is
calibrated to O'Neill's design (L=32 km at r=3.2 km, giving C≈2.74).
See plans/constraint_cylinder_length.md for derivation.
"""

from __future__ import annotations

from habitat_constraints.core.parameters import (
    ConstraintResult,
    HabitatParameters,
    HumanAssumptions,
    ParameterBound,
)


class CylinderLengthConstraint:
    """Cylinder length must not exceed bending-mode limit."""

    @property
    def name(self) -> str:
        return "cylinder_length"

    @property
    def description(self) -> str:
        return (
            "Cylinder length limited by bending mode resonance: "
            "L <= C * r^(5/4)"
        )

    def evaluate(
        self,
        params: HabitatParameters,
        assumptions: HumanAssumptions,
    ) -> ConstraintResult:
        C = assumptions.max_length_coefficient
        r = params.radius_m
        L = params.length_m
        L_max = C * r ** 1.25

        feasible = L <= L_max if L > 0 else True
        margin_pct = ((L_max - L) / L_max * 100.0) if L_max > 0 else 0.0

        bounds = self.compute_bounds(assumptions)
        return ConstraintResult(
            constraint_name=self.name,
            feasible=feasible,
            bounds=bounds,
            details={
                "length_m": L,
                "max_length_m": round(L_max, 1),
                "coefficient": C,
                "margin_pct": round(margin_pct, 1),
                "length_to_diameter": (
                    round(L / (2 * r), 2) if r > 0 else 0.0
                ),
            },
        )

    def compute_bounds(
        self,
        assumptions: HumanAssumptions,
    ) -> list[ParameterBound]:
        C = assumptions.max_length_coefficient
        return [
            ParameterBound(
                parameter_name="length_m",
                upper=None,  # depends on radius, not a fixed bound
                constraint_name=self.name,
                description=(
                    f"L <= {C} * r^(5/4) "
                    f"(bending mode resonance limit)"
                ),
            ),
        ]
