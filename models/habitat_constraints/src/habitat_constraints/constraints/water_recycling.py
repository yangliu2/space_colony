"""Water recycling constraint — closed-loop efficiency must meet minimum threshold."""

from __future__ import annotations

from habitat_constraints.core.parameters import (
    ConstraintResult,
    HabitatParameters,
    HumanAssumptions,
    ParameterBound,
)


class WaterRecyclingConstraint:
    """Water recycling efficiency must support closed-loop self-sufficiency.

    Daily water demand:  D = water_per_person_day_liters * population
    Daily net loss:      L = D * (1 - recycling_efficiency)
    Annual loss (kg):    L_year = L * 365   (1 L water ≈ 1 kg)

    Feasibility condition:
        recycling_efficiency >= min_water_recycling_efficiency

    ISS ECLSS achieves ~0.93; a permanent habitat needs ~0.98.
    The constraint fails by default, showing that current technology
    is insufficient for permanent habitation.

    The constraint is skipped when population == 0 (no demand defined).
    """

    @property
    def name(self) -> str:
        return "water_recycling"

    @property
    def description(self) -> str:
        return (
            "Water recycling efficiency must meet minimum "
            "for closed-loop self-sufficiency"
        )

    def evaluate(
        self,
        params: HabitatParameters,
        assumptions: HumanAssumptions,
    ) -> ConstraintResult:
        if params.population <= 0:
            return ConstraintResult(
                constraint_name=self.name,
                feasible=True,
                bounds=self.compute_bounds(assumptions),
                details={
                    "total_daily_demand_liters": 0.0,
                    "daily_loss_liters": 0.0,
                    "annual_loss_kg": 0.0,
                    "recycling_efficiency": assumptions.water_recycling_efficiency,
                    "min_recycling_efficiency": (
                        assumptions.min_water_recycling_efficiency
                    ),
                    "efficiency_margin": (
                        assumptions.water_recycling_efficiency
                        - assumptions.min_water_recycling_efficiency
                    ),
                },
            )

        total_daily_demand = assumptions.water_per_person_day_liters * params.population
        daily_loss = total_daily_demand * (1.0 - assumptions.water_recycling_efficiency)
        annual_loss_kg = daily_loss * 365.0

        efficiency_margin = (
            assumptions.water_recycling_efficiency
            - assumptions.min_water_recycling_efficiency
        )
        feasible = (
            assumptions.water_recycling_efficiency
            >= assumptions.min_water_recycling_efficiency
        )

        return ConstraintResult(
            constraint_name=self.name,
            feasible=feasible,
            bounds=self.compute_bounds(assumptions),
            details={
                "total_daily_demand_liters": total_daily_demand,
                "daily_loss_liters": daily_loss,
                "annual_loss_kg": annual_loss_kg,
                "recycling_efficiency": assumptions.water_recycling_efficiency,
                "min_recycling_efficiency": assumptions.min_water_recycling_efficiency,
                "efficiency_margin": efficiency_margin,
            },
        )

    def compute_bounds(
        self,
        assumptions: HumanAssumptions,
    ) -> list[ParameterBound]:
        return [
            ParameterBound(
                parameter_name="water_recycling_efficiency",
                lower=assumptions.min_water_recycling_efficiency,
                constraint_name=self.name,
                description=(
                    f"water_recycling_efficiency >= "
                    f"{assumptions.min_water_recycling_efficiency:.3f} "
                    f"for closed-loop self-sufficiency"
                ),
            ),
        ]
