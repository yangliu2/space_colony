"""Micrometeorite hull penetration constraint — annual perforation rate check."""

from __future__ import annotations

import math

from habitat_constraints.core.parameters import (
    ConstraintResult,
    HabitatParameters,
    HumanAssumptions,
    ParameterBound,
)


class MicrometeoiteConstraint:
    """Annual hull penetration rate must stay below a manageable threshold.

    Exposed area (cannot be covered by regolith):
        A_exposed = window_fraction * barrel_area + endcap_area

    Land strips are shielded by construction mass; window strips and end
    caps are exposed to the meteoroid flux.

    Expected annual perforations (Poisson process, Grün et al. 1985):
        N_annual = flux * A_exposed

    Expected lifetime perforations:
        N_lifetime = N_annual * lifespan_years

    Cumulative Poisson reliability (probability of zero events):
        P_zero = exp(-N_lifetime)

    Feasibility condition:
        N_annual <= max_annual_perforations

    ISS calibration: ~6e-5 m⁻²yr⁻¹ gives 0.25 perforations/yr at 4,200 m².
    Purpose-built habitat shield targets ~1e-7 m⁻²yr⁻¹.

    The maximum permissible flux is geometry-dependent and reported in
    details["max_flux_to_pass_m2_yr"] rather than as a ParameterBound.
    """

    @property
    def name(self) -> str:
        return "micrometeorite"

    @property
    def description(self) -> str:
        return (
            "Annual hull penetration rate must be below "
            "max_annual_perforations (Poisson model, Grün 1985)"
        )

    def evaluate(
        self,
        params: HabitatParameters,
        assumptions: HumanAssumptions,
    ) -> ConstraintResult:
        # Exposed area: windows + end caps (cannot be regolith-shielded)
        exposed_barrel = assumptions.window_fraction * params.barrel_area_m2
        exposed_endcap = params.endcap_area_m2
        exposed_area = exposed_barrel + exposed_endcap

        shielded_area = (1.0 - assumptions.window_fraction) * params.barrel_area_m2

        flux = assumptions.meteoroid_penetrating_flux_m2_yr
        annual_perforations = flux * exposed_area
        lifetime_perforations = annual_perforations * assumptions.habitat_lifespan_years

        # Poisson P(zero events over full lifespan)
        reliability_lifetime = math.exp(-min(lifetime_perforations, 700.0))

        feasible = annual_perforations <= assumptions.max_annual_perforations

        max_flux = (
            assumptions.max_annual_perforations / exposed_area
            if exposed_area > 0
            else math.inf
        )

        return ConstraintResult(
            constraint_name=self.name,
            feasible=feasible,
            bounds=self.compute_bounds(assumptions),
            details={
                "exposed_area_m2": exposed_area,
                "shielded_area_m2": shielded_area,
                "expected_annual_perforations": annual_perforations,
                "expected_lifetime_perforations": lifetime_perforations,
                "reliability_lifetime": reliability_lifetime,
                "penetrating_flux_m2_yr": flux,
                "max_flux_to_pass_m2_yr": max_flux,
            },
        )

    def compute_bounds(
        self,
        assumptions: HumanAssumptions,
    ) -> list[ParameterBound]:
        # The flux bound depends on habitat geometry (exposed area), which is
        # not available here. See details["max_flux_to_pass_m2_yr"] in evaluate().
        return []
