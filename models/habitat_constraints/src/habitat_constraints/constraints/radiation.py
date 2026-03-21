"""Radiation shielding constraint — minimum areal density."""

from __future__ import annotations

from habitat_constraints.core.parameters import (
    ConstraintResult,
    HabitatParameters,
    HumanAssumptions,
    ParameterBound,
)


class RadiationConstraint:
    """Radiation shielding must meet minimum areal density.

    In deep space, galactic cosmic rays (GCR) require substantial
    passive shielding. The SP-413 found 4,500 kg/m² minimum for
    <0.5 rem/yr.  At intermediate thicknesses (~2,000 kg/m²),
    secondary particle production can *increase* dose — this
    constraint enforces the safe minimum.

    Note: this constraint only checks that the *specified* shielding
    meets the threshold.  The mass implications are computed
    separately (shielding_mass = areal_density × shell_area).
    """

    @property
    def name(self) -> str:
        return "radiation_shielding"

    @property
    def description(self) -> str:
        return "Radiation shielding areal density must meet " "minimum for crew safety"

    def evaluate(
        self,
        params: HabitatParameters,
        assumptions: HumanAssumptions,
    ) -> ConstraintResult:
        actual = params.shielding_areal_density_kg_m2
        required = assumptions.min_shielding_areal_density_kg_m2
        feasible = actual >= required
        margin_pct = ((actual - required) / required) * 100.0

        # Compute shielding mass if geometry is specified
        shielding_mass_mt = 0.0
        if params.total_shell_area_m2 > 0:
            shielding_mass_mt = actual * params.total_shell_area_m2 / 1e9  # megatonnes

        bounds = self.compute_bounds(assumptions)
        return ConstraintResult(
            constraint_name=self.name,
            feasible=feasible,
            bounds=bounds,
            details={
                "shielding_kg_m2": actual,
                "required_kg_m2": required,
                "margin_pct": margin_pct,
                "shielding_mass_mt": shielding_mass_mt,
            },
        )

    def compute_bounds(
        self,
        assumptions: HumanAssumptions,
    ) -> list[ParameterBound]:
        req = assumptions.min_shielding_areal_density_kg_m2
        return [
            ParameterBound(
                parameter_name="shielding_areal_density_kg_m2",
                lower=req,
                constraint_name=self.name,
                description=(
                    f"shielding >= {req:.0f} kg/m² " f"for <0.5 rem/yr GCR protection"
                ),
            ),
        ]
