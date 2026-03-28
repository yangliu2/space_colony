"""Rotational stability constraint for spinning cylinder habitats.

A cylinder spinning about its symmetry axis (minimum moment of inertia)
is in an unstable equilibrium — energy dissipation from internal
activity drives rotation toward the maximum-I axis (the Explorer 1
problem). Passive stability requires the spin axis to be the
maximum-I axis, which constrains length relative to radius.

For a uniform thin-walled cylinder with flat end caps:
    Iz = m * r²           (spin axis, along length)
    Ix = m * (r²/2 + L²/12)   (transverse)

Passive stability requires Iz/Ix >= 1.2 (20% margin), giving:
    L < sqrt(6 * (1/1.2 - 0.5)) * r ≈ 1.29r

Rounded to L < 1.3r (Globus and Arora 2007, Kalpana One design).

Counter-rotating pairs (O'Neill design) bypass this limit by
cancelling net angular momentum and using active control.

References:
    Globus, Al, and Nitin Arora. "Kalpana One." NSS, 2007.
    Globus, Al. "Design Limits on Large Space Stations." arXiv, 2024.
"""

from __future__ import annotations

from habitat_constraints.core.parameters import (
    ConstraintResult,
    HabitatParameters,
    HumanAssumptions,
    ParameterBound,
)


class RotationalStabilityConstraint:
    """Cylinder length limited by rotational stability (Iz >= 1.2 Ix)."""

    @property
    def name(self) -> str:
        return "rotational_stability"

    @property
    def description(self) -> str:
        return (
            "Rotational stability: L/r must stay below threshold "
            "for passive spin stability (Globus and Arora 2007)"
        )

    def evaluate(
        self,
        params: HabitatParameters,
        assumptions: HumanAssumptions,
    ) -> ConstraintResult:
        r = params.radius_m
        L = params.length_m

        if assumptions.counter_rotating_pair:
            # Counter-rotating pairs relax the limit significantly.
            # Use L/r < 10 as a generous structural bound.
            max_ratio = 10.0
        else:
            max_ratio = assumptions.max_length_to_radius_ratio

        max_length = max_ratio * r

        # L=0 means length not specified — pass by default
        feasible = L <= max_length if L > 0 else True
        margin_pct = (max_length - L) / max_length * 100.0 if max_length > 0 else 0.0

        actual_ratio = L / r if r > 0 else 0.0

        bounds = self.compute_bounds(assumptions)
        return ConstraintResult(
            constraint_name=self.name,
            feasible=feasible,
            bounds=bounds,
            details={
                "length_m": L,
                "max_length_m": round(max_length, 1),
                "length_to_radius": round(actual_ratio, 3),
                "max_length_to_radius": max_ratio,
                "margin_pct": round(margin_pct, 1),
                "counter_rotating": (1.0 if assumptions.counter_rotating_pair else 0.0),
            },
        )

    def compute_bounds(
        self,
        assumptions: HumanAssumptions,
    ) -> list[ParameterBound]:
        if assumptions.counter_rotating_pair:
            ratio = 10.0
            desc = "L < 10r (counter-rotating pair, " "active stabilization)"
        else:
            ratio = assumptions.max_length_to_radius_ratio
            desc = f"L < {ratio}r (passive rotational stability, " f"Iz/Ix >= 1.2)"
        return [
            ParameterBound(
                parameter_name="length_m",
                upper=None,  # depends on radius
                constraint_name=self.name,
                description=desc,
            ),
        ]
