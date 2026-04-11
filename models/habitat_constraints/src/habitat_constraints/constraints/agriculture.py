"""Agriculture area constraint — food self-sufficiency requires minimum growing area."""

from __future__ import annotations

from habitat_constraints.core.parameters import (
    ConstraintResult,
    HabitatParameters,
    HumanAssumptions,
    ParameterBound,
)


class AgricultureConstraint:
    """Dedicated agriculture area must be sufficient to feed the population.

    Minimum area depends on two factors:

    1. **Farming method** (min_agriculture_area_per_person_m2):
       - Open field (Earth): ~2,000 m²/person
       - Hydroponics (single-tier, NASA BVAD): ~200 m²/person
       - Vertical farming (5–10 tiers): ~20–100 m²/person

    2. **Diet composition** (diet_land_multiplier):
       - 1.0 = plant-only diet (NASA CELSS baseline)
       - ~1.1 = with insects
       - ~1.4 = with aquaculture
       - ~3–4 = with poultry/eggs
       - ~5–7 = with pork
       - ~15–20 = with beef (not viable at habitat scale)

    Effective threshold = min_agriculture_area_per_person_m2 * diet_land_multiplier.

    The check is skipped when ``agriculture_area_m2 == 0`` (not specified) or
    when ``population == 0``.
    """

    @property
    def name(self) -> str:
        return "agriculture"

    @property
    def description(self) -> str:
        return "Agriculture area must be sufficient to feed the population"

    def evaluate(
        self,
        params: HabitatParameters,
        assumptions: HumanAssumptions,
    ) -> ConstraintResult:
        agr_area = params.agriculture_area_m2
        pop = params.population
        min_area_pp = assumptions.min_agriculture_area_per_person_m2
        multiplier = assumptions.diet_land_multiplier
        effective_area_pp = min_area_pp * multiplier

        # Skip if either value is unspecified
        if agr_area <= 0 or pop <= 0:
            return ConstraintResult(
                constraint_name=self.name,
                feasible=True,
                bounds=self.compute_bounds(assumptions),
                details={
                    "agriculture_area_m2": agr_area,
                    "required_area_m2": 0.0,
                    "area_per_person_m2": 0.0,
                    "effective_area_per_person_m2": effective_area_pp,
                    "diet_land_multiplier": multiplier,
                    "area_margin_m2": 0.0,
                },
            )

        required_area = effective_area_pp * pop
        area_per_person = agr_area / pop
        margin = agr_area - required_area
        feasible = agr_area >= required_area

        return ConstraintResult(
            constraint_name=self.name,
            feasible=feasible,
            bounds=self.compute_bounds(assumptions),
            details={
                "agriculture_area_m2": agr_area,
                "required_area_m2": required_area,
                "area_per_person_m2": area_per_person,
                "effective_area_per_person_m2": effective_area_pp,
                "diet_land_multiplier": multiplier,
                "area_margin_m2": margin,
            },
        )

    def compute_bounds(
        self,
        assumptions: HumanAssumptions,
    ) -> list[ParameterBound]:
        effective = (
            assumptions.min_agriculture_area_per_person_m2
            * assumptions.diet_land_multiplier
        )
        return [
            ParameterBound(
                parameter_name="agriculture_area_m2",
                lower=None,  # depends on population; expressed per-person
                constraint_name=self.name,
                description=(
                    f"agriculture_area >= {effective:.0f} m²/person "
                    f"({assumptions.min_agriculture_area_per_person_m2:.0f} "
                    f"× {assumptions.diet_land_multiplier:.1f} diet multiplier)"
                ),
            ),
        ]
