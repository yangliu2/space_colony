"""Thermal management constraint — radiator area must reject total heat load."""

from __future__ import annotations

import math

from habitat_constraints.core.parameters import (
    ConstraintResult,
    HabitatParameters,
    HumanAssumptions,
    ParameterBound,
)

# Stefan-Boltzmann constant (W m^-2 K^-4)
STEFAN_BOLTZMANN = 5.670374419e-8


class ThermalConstraint:
    """Available radiator area must be sufficient to reject the habitat's heat load.

    Heat sources:
    - Solar gain through windows: I_sun * window_area * transmittance
    - Internal waste heat: waste_heat_per_person_w * population

    Heat rejection by radiation only (no convection in space):
        P_rad = emissivity * sigma * A_rad * T^4

    Required radiator area is compared to the non-window hull area
    (land strips + end caps). The constraint is skipped when geometry
    is not specified (length_m == 0).
    """

    @property
    def name(self) -> str:
        return "thermal"

    @property
    def description(self) -> str:
        return (
            "Radiator area on non-window hull must reject "
            "solar gain + internal waste heat"
        )

    def evaluate(
        self,
        params: HabitatParameters,
        assumptions: HumanAssumptions,
    ) -> ConstraintResult:
        # Skip if geometry is not specified
        if params.length_m <= 0:
            return ConstraintResult(
                constraint_name=self.name,
                feasible=True,
                bounds=self.compute_bounds(assumptions),
                details={
                    "solar_gain_w": 0.0,
                    "internal_heat_w": 0.0,
                    "total_heat_w": 0.0,
                    "required_radiator_area_m2": 0.0,
                    "available_radiator_area_m2": 0.0,
                    "radiator_area_fraction": 0.0,
                },
            )

        # --- Heat sources ---
        window_area = assumptions.window_fraction * params.barrel_area_m2
        solar_gain_w = (
            assumptions.solar_irradiance_w_m2
            * window_area
            * assumptions.window_solar_transmittance
        )

        pop = params.population
        internal_heat_w = assumptions.waste_heat_per_person_w * pop if pop > 0 else 0.0

        total_heat_w = solar_gain_w + internal_heat_w

        # --- Required radiator area ---
        rad_power_per_m2 = (
            assumptions.radiator_emissivity
            * STEFAN_BOLTZMANN
            * assumptions.radiator_temperature_k**4
        )
        required_area = total_heat_w / rad_power_per_m2

        # --- Available radiator area (non-window hull) ---
        land_strip_area = (1.0 - assumptions.window_fraction) * params.barrel_area_m2
        available_area = land_strip_area + params.endcap_area_m2

        fraction = required_area / available_area if available_area > 0 else math.inf
        feasible = required_area <= available_area

        return ConstraintResult(
            constraint_name=self.name,
            feasible=feasible,
            bounds=self.compute_bounds(assumptions),
            details={
                "solar_gain_w": solar_gain_w,
                "internal_heat_w": internal_heat_w,
                "total_heat_w": total_heat_w,
                "required_radiator_area_m2": required_area,
                "available_radiator_area_m2": available_area,
                "radiator_area_fraction": fraction,
            },
        )

    def compute_bounds(
        self,
        assumptions: HumanAssumptions,
    ) -> list[ParameterBound]:
        rad_power_per_m2 = (
            assumptions.radiator_emissivity
            * STEFAN_BOLTZMANN
            * assumptions.radiator_temperature_k**4
        )
        return [
            ParameterBound(
                parameter_name="window_solar_transmittance",
                upper=assumptions.window_solar_transmittance,
                constraint_name=self.name,
                description=(
                    f"Solar transmittance <= "
                    f"{assumptions.window_solar_transmittance:.2f} to keep "
                    f"radiator fraction <= 1.0 at T="
                    f"{assumptions.radiator_temperature_k:.0f} K "
                    f"({rad_power_per_m2:.0f} W/m² radiated)"
                ),
            ),
        ]
