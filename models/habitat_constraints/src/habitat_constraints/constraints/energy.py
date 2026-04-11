"""Energy budget constraint — solar panel area must cover colony power demand."""

from __future__ import annotations

import math

from habitat_constraints.core.parameters import (
    ConstraintResult,
    HabitatParameters,
    HumanAssumptions,
    ParameterBound,
)


class EnergyConstraint:
    """Solar panel area on end caps must meet total colony power demand.

    Power demand: P_total = power_per_person_w * population
    Required panel area: A_solar = P_total / (eta * I_solar)
    Available panel area: end-cap exterior = 2 * pi * r^2

    End caps are the natural mounting surface: they face axially, receive
    consistent solar flux, and avoid the rotation problem of the barrel.

    The constraint is skipped when population == 0 (no demand defined).
    """

    @property
    def name(self) -> str:
        return "energy"

    @property
    def description(self) -> str:
        return (
            "Solar panel area on end caps must supply " "power_per_person_w * population"
        )

    def evaluate(
        self,
        params: HabitatParameters,
        assumptions: HumanAssumptions,
    ) -> ConstraintResult:
        # Skip if population not specified
        if params.population <= 0:
            return ConstraintResult(
                constraint_name=self.name,
                feasible=True,
                bounds=self.compute_bounds(assumptions),
                details={
                    "total_power_demand_w": 0.0,
                    "required_panel_area_m2": 0.0,
                    "available_panel_area_m2": params.endcap_area_m2,
                    "panel_area_fraction": 0.0,
                },
            )

        # --- Power demand ---
        total_power_w = assumptions.power_per_person_w * params.population

        # --- Required solar panel area ---
        power_per_m2 = (
            assumptions.solar_panel_efficiency * assumptions.solar_irradiance_w_m2
        )
        required_area = total_power_w / power_per_m2

        # --- Available area (end caps) ---
        available_area = params.endcap_area_m2  # 2 * pi * r^2

        fraction = required_area / available_area if available_area > 0 else math.inf
        feasible = required_area <= available_area

        return ConstraintResult(
            constraint_name=self.name,
            feasible=feasible,
            bounds=self.compute_bounds(assumptions),
            details={
                "total_power_demand_w": total_power_w,
                "required_panel_area_m2": required_area,
                "available_panel_area_m2": available_area,
                "panel_area_fraction": fraction,
            },
        )

    def compute_bounds(
        self,
        assumptions: HumanAssumptions,
    ) -> list[ParameterBound]:
        return [
            ParameterBound(
                parameter_name="power_per_person_w",
                upper=assumptions.power_per_person_w,
                constraint_name=self.name,
                description=(
                    f"Power per person <= {assumptions.power_per_person_w:.0f} W "
                    f"at eta={assumptions.solar_panel_efficiency:.2f}, "
                    f"I={assumptions.solar_irradiance_w_m2:.0f} W/m² "
                    f"to keep panel fraction <= 1.0"
                ),
            ),
        ]
