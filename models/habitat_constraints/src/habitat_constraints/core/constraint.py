"""Constraint protocol for habitat design bounds."""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from habitat_constraints.core.parameters import (
    ConstraintResult,
    HabitatParameters,
    HumanAssumptions,
    ParameterBound,
)


@runtime_checkable
class Constraint(Protocol):
    """Protocol that all habitat constraints must satisfy.

    Each constraint is independent and self-contained. Implement both
    methods to participate in the solver's feasible-region computation.
    """

    @property
    def name(self) -> str:
        """Short identifier for this constraint."""
        ...

    @property
    def description(self) -> str:
        """Human-readable description of what this constraint checks."""
        ...

    def evaluate(
        self,
        params: HabitatParameters,
        assumptions: HumanAssumptions,
    ) -> ConstraintResult:
        """Evaluate feasibility at a specific design point.

        Returns a ConstraintResult with feasibility flag, any bounds
        this constraint imposes, and computed detail values.
        """
        ...

    def compute_bounds(
        self,
        assumptions: HumanAssumptions,
    ) -> list[ParameterBound]:
        """Compute parameter bounds independent of a specific design point.

        These bounds represent the constraint's limits in general,
        used by the solver to find the feasible region.
        """
        ...
