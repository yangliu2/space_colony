"""Population constraint — minimum viable population for genetics."""

from __future__ import annotations

from habitat_constraints.core.parameters import (
    ConstraintResult,
    HabitatParameters,
    HumanAssumptions,
    ParameterBound,
)


class PopulationConstraint:
    """Population must meet minimum for genetic viability.

    For a truly isolated colony (no immigration), the minimum
    viable population depends on assumptions about breeding
    management:

    - 98 (Marin & Beluffi 2020): agent-based simulation, managed
    - 500: classic conservation genetics (effective population)
    - 10,000-40,000 (Smith 2014): accounts for catastrophes

    This constraint also checks habitable volume per person
    if geometry is specified.
    """

    @property
    def name(self) -> str:
        return "population"

    @property
    def description(self) -> str:
        return (
            "Population must meet genetic minimum; " "volume per person must be adequate"
        )

    def evaluate(
        self,
        params: HabitatParameters,
        assumptions: HumanAssumptions,
    ) -> ConstraintResult:
        pop = params.population
        min_pop = assumptions.min_population

        # Population check (only if specified)
        pop_feasible = pop >= min_pop if pop > 0 else True
        pop_margin = pop - min_pop if pop > 0 else 0

        # Volume per person check (only if geometry specified)
        vol_pp = params.volume_per_person_m3
        min_vol = assumptions.min_volume_per_person_m3
        vol_feasible = vol_pp >= min_vol if vol_pp > 0 else True
        vol_margin = vol_pp - min_vol if vol_pp > 0 else 0.0

        feasible = pop_feasible and vol_feasible

        bounds = self.compute_bounds(assumptions)
        return ConstraintResult(
            constraint_name=self.name,
            feasible=feasible,
            bounds=bounds,
            details={
                "population": float(pop),
                "min_population": float(min_pop),
                "pop_margin": float(pop_margin),
                "volume_per_person_m3": vol_pp,
                "min_volume_m3": min_vol,
                "vol_margin_m3": vol_margin,
            },
        )

    def compute_bounds(
        self,
        assumptions: HumanAssumptions,
    ) -> list[ParameterBound]:
        return [
            ParameterBound(
                parameter_name="population",
                lower=float(assumptions.min_population),
                constraint_name=self.name,
                description=(
                    f"population >= {assumptions.min_population} "
                    f"for genetic viability"
                ),
            ),
            ParameterBound(
                parameter_name="volume_per_person_m3",
                lower=assumptions.min_volume_per_person_m3,
                constraint_name=self.name,
                description=(
                    f"volume >= "
                    f"{assumptions.min_volume_per_person_m3:.0f} "
                    f"m³/person for long-term habitation"
                ),
            ),
        ]
