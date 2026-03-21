"""Atmosphere constraint — oxygen partial pressure range."""

from __future__ import annotations

from habitat_constraints.core.parameters import (
    ConstraintResult,
    HabitatParameters,
    HumanAssumptions,
    ParameterBound,
)


class AtmosphereConstraint:
    """Oxygen partial pressure must be within survivable range.

    Below ~16 kPa pO₂: hypoxia, cognitive impairment, death.
    Above ~50 kPa pO₂: pulmonary oxygen toxicity (continuous).

    This is a hard physiological constraint with no adaptation
    or engineering workaround — the atmosphere *must* deliver
    O₂ within this range at the breathing zone.
    """

    @property
    def name(self) -> str:
        return "atmosphere"

    @property
    def description(self) -> str:
        return "O2 partial pressure must be within safe range"

    def evaluate(
        self,
        params: HabitatParameters,
        assumptions: HumanAssumptions,
    ) -> ConstraintResult:
        po2 = params.o2_partial_pressure_kpa
        po2_min = assumptions.min_o2_partial_pressure_kpa
        po2_max = assumptions.max_o2_partial_pressure_kpa
        feasible = po2_min <= po2 <= po2_max

        if po2 < po2_min:
            margin_kpa = po2 - po2_min  # negative
        elif po2 > po2_max:
            margin_kpa = po2_max - po2  # negative
        else:
            margin_kpa = min(po2 - po2_min, po2_max - po2)

        bounds = self.compute_bounds(assumptions)
        return ConstraintResult(
            constraint_name=self.name,
            feasible=feasible,
            bounds=bounds,
            details={
                "o2_partial_pressure_kpa": po2,
                "min_o2_kpa": po2_min,
                "max_o2_kpa": po2_max,
                "total_pressure_kpa": params.internal_pressure_kpa,
                "o2_fraction": params.o2_fraction,
                "margin_kpa": margin_kpa,
            },
        )

    def compute_bounds(
        self,
        assumptions: HumanAssumptions,
    ) -> list[ParameterBound]:
        return [
            ParameterBound(
                parameter_name="o2_partial_pressure_kpa",
                lower=assumptions.min_o2_partial_pressure_kpa,
                upper=assumptions.max_o2_partial_pressure_kpa,
                constraint_name=self.name,
                description=(
                    f"pO2 in "
                    f"[{assumptions.min_o2_partial_pressure_kpa:.0f}, "
                    f"{assumptions.max_o2_partial_pressure_kpa:.0f}] kPa"
                ),
            ),
        ]
