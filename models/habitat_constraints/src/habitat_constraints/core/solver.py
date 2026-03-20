"""Feasible region solver — aggregates constraints and finds bounds."""

from __future__ import annotations

import math
from collections import defaultdict
from dataclasses import dataclass, field

from habitat_constraints.core.constraint import Constraint
from habitat_constraints.core.parameters import (
    EARTH_G,
    ConstraintResult,
    HabitatParameters,
    HumanAssumptions,
    ParameterBound,
)


@dataclass
class SweepPoint:
    """Result of evaluating all constraints at one radius."""

    radius_m: float
    angular_velocity_rad_s: float
    rpm: float
    gravity_g: float
    rim_speed_m_s: float
    all_feasible: bool
    constraint_results: list[ConstraintResult] = field(default_factory=list)


class FeasibleRegionSolver:
    """Aggregates multiple constraints and finds their intersection.

    The solver does not optimize. It discovers the feasible region
    by intersecting bounds from independent constraints.
    """

    def __init__(
        self,
        constraints: list[Constraint],
        assumptions: HumanAssumptions | None = None,
    ) -> None:
        self.constraints = list(constraints)
        self.assumptions = assumptions or HumanAssumptions()

    def add_constraint(self, constraint: Constraint) -> None:
        """Add a constraint to the solver."""
        self.constraints.append(constraint)

    def remove_constraint(self, name: str) -> None:
        """Remove a constraint by name."""
        self.constraints = [c for c in self.constraints if c.name != name]

    def compute_all_bounds(
        self,
    ) -> dict[str, list[ParameterBound]]:
        """Collect all bounds from all constraints, grouped by parameter."""
        bounds_by_param: dict[str, list[ParameterBound]] = defaultdict(list)
        for constraint in self.constraints:
            for bound in constraint.compute_bounds(self.assumptions):
                bounds_by_param[bound.parameter_name].append(bound)
        return dict(bounds_by_param)

    def feasible_range(
        self,
        parameter_name: str,
    ) -> tuple[float | None, float | None]:
        """Intersect all bounds for a parameter. Returns (lower, upper).

        Returns (None, None) if no bounds exist for the parameter.
        The region is infeasible if lower > upper.
        """
        all_bounds = self.compute_all_bounds()
        param_bounds = all_bounds.get(parameter_name, [])

        if not param_bounds:
            return (None, None)

        lower: float | None = None
        upper: float | None = None

        for bound in param_bounds:
            if bound.lower is not None:
                lower = max(lower, bound.lower) if lower is not None else bound.lower
            if bound.upper is not None:
                upper = min(upper, bound.upper) if upper is not None else bound.upper

        return (lower, upper)

    def evaluate_point(
        self,
        params: HabitatParameters,
    ) -> list[ConstraintResult]:
        """Check all constraints at a specific design point."""
        return [c.evaluate(params, self.assumptions) for c in self.constraints]

    def is_feasible(self, params: HabitatParameters) -> bool:
        """Check if a design point satisfies all constraints."""
        return all(r.feasible for r in self.evaluate_point(params))

    def sweep_radius(
        self,
        r_min: float,
        r_max: float,
        n_points: int = 200,
        target_gravity_g: float = 1.0,
    ) -> list[SweepPoint]:
        """Sweep radius range at a fixed gravity target.

        For each radius, compute the omega that achieves target_gravity_g,
        then evaluate all constraints. Returns a list of SweepPoint
        results ordered by radius.
        """
        results: list[SweepPoint] = []
        step = (r_max - r_min) / max(n_points - 1, 1)

        for i in range(n_points):
            r = r_min + i * step
            omega = math.sqrt(target_gravity_g * EARTH_G / r)
            params = HabitatParameters(
                radius_m=r,
                angular_velocity_rad_s=omega,
            )
            constraint_results = self.evaluate_point(params)
            all_feasible = all(cr.feasible for cr in constraint_results)

            results.append(
                SweepPoint(
                    radius_m=r,
                    angular_velocity_rad_s=omega,
                    rpm=params.rpm,
                    gravity_g=params.gravity_g,
                    rim_speed_m_s=params.rim_speed_m_s,
                    all_feasible=all_feasible,
                    constraint_results=constraint_results,
                )
            )

        return results
