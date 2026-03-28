"""Phase 6 analysis — structural constraints.

Extends Phase 3 with:
- Hoop stress constraint (material yield limit)
- Cylinder length constraint (bending mode resonance)
- Rotational stability constraint (Iz/Ix >= 1.2)

Key questions:
1. Do structural constraints change the feasible radius band?
2. What is the maximum safe length for single vs. paired cylinders?
3. How do material choices (steel vs. CFRP) affect the design space?
4. Which constraint is binding for cylinder length?
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

from habitat_constraints.constraints.atmosphere import (
    AtmosphereConstraint,
)
from habitat_constraints.constraints.coriolis import CoriolisConstraint
from habitat_constraints.constraints.cross_coupling import (
    CrossCouplingConstraint,
)
from habitat_constraints.constraints.cylinder_length import (
    CylinderLengthConstraint,
)
from habitat_constraints.constraints.gravity_gradient import (
    GravityGradientConstraint,
)
from habitat_constraints.constraints.gravity_level import (
    GravityLevelConstraint,
)
from habitat_constraints.constraints.hoop_stress import (
    HoopStressConstraint,
)
from habitat_constraints.constraints.population import (
    PopulationConstraint,
)
from habitat_constraints.constraints.radiation import (
    RadiationConstraint,
)
from habitat_constraints.constraints.rim_speed import RimSpeedConstraint
from habitat_constraints.constraints.rotational_stability import (
    RotationalStabilityConstraint,
)
from habitat_constraints.constraints.vestibular import (
    VestibularConstraint,
)
from habitat_constraints.core.parameters import (
    HabitatParameters,
    HumanAssumptions,
)
from habitat_constraints.core.solver import FeasibleRegionSolver

OUTPUT_DIR = Path(__file__).parent / "output"


def phase3_constraints() -> list:
    """The 9 constraints from Phase 3."""
    return [
        VestibularConstraint(),
        GravityLevelConstraint(),
        GravityGradientConstraint(),
        CoriolisConstraint(),
        CrossCouplingConstraint(),
        RimSpeedConstraint(),
        RadiationConstraint(),
        AtmosphereConstraint(),
        PopulationConstraint(),
    ]


def all_constraints() -> list:
    """All 12 constraints including Phase 6 structural."""
    return phase3_constraints() + [
        CylinderLengthConstraint(),
        HoopStressConstraint(),
        RotationalStabilityConstraint(),
    ]


def experiment_1_full_scorecard() -> dict:
    """12-constraint scorecard at key design points."""
    print("=== Experiment 1: Full 12-constraint scorecard ===")

    designs = [
        ("Min viable (single)", 982.0, 1276.0, 8000, False),
        ("Min viable (old L)", 982.0, 2000.0, 8000, False),
        ("Kalpana One", 250.0, 325.0, 500, False),
        ("O'Neill (paired)", 3200.0, 32000.0, 1_000_000, True),
        ("O'Neill (single)", 3200.0, 32000.0, 1_000_000, False),
    ]

    scorecards = []
    for name, r, length, pop, paired in designs:
        assumptions = HumanAssumptions(counter_rotating_pair=paired)
        params = HabitatParameters.from_radius_and_gravity(
            r,
            length_m=length,
            population=pop,
        )
        solver = FeasibleRegionSolver(
            constraints=all_constraints(),
            assumptions=assumptions,
        )
        results = solver.evaluate_point(params)

        card = {
            "design": name,
            "radius_m": r,
            "length_m": length,
            "population": pop,
            "counter_rotating": paired,
            "rpm": round(params.rpm, 3),
            "rim_speed_m_s": round(params.rim_speed_m_s, 1),
            "all_pass": all(cr.feasible for cr in results),
            "constraints": {},
        }
        all_pass = all(cr.feasible for cr in results)
        tag = "ALL PASS" if all_pass else "FAIL"
        print(f"\n  {name} (r={r}m, L={length}m): {tag}")
        for cr in results:
            status = "PASS" if cr.feasible else "FAIL"
            card["constraints"][cr.constraint_name] = {
                "feasible": cr.feasible,
                "details": {
                    k: round(v, 4) for k, v in cr.details.items()
                },
            }
            if not cr.feasible:
                print(f"    {cr.constraint_name}: {status}")
        scorecards.append(card)

    return {"name": "Full 12-constraint scorecard", "data": scorecards}


def experiment_2_length_limits() -> dict:
    """Compare rotational stability vs. bending mode length limits."""
    print("\n=== Experiment 2: Length limit comparison ===")
    print("  Radius | Rot. Stability | Bending Mode | Binding")
    print("  -------|---------------|-------------|--------")

    rot = RotationalStabilityConstraint()
    bend = CylinderLengthConstraint()
    assumptions = HumanAssumptions()

    rows = []
    for r in [250, 500, 982, 1500, 2000, 3200, 5000]:
        # Evaluate at a tiny length to read max_length from details
        params = HabitatParameters.from_radius_and_gravity(
            float(r), length_m=1.0
        )
        rot_result = rot.evaluate(params, assumptions)
        bend_result = bend.evaluate(params, assumptions)

        rot_max = rot_result.details["max_length_m"]
        bend_max = bend_result.details["max_length_m"]
        binding = (
            "rotational" if rot_max < bend_max else "bending"
        )

        row = {
            "radius_m": r,
            "rot_stability_max_m": rot_max,
            "bending_mode_max_m": bend_max,
            "binding": binding,
            "ratio": round(bend_max / rot_max, 2),
        }
        rows.append(row)
        print(
            f"  {r:>6} | {rot_max:>13,.0f} | "
            f"{bend_max:>11,.0f} | {binding}"
        )

    return {"name": "Length limit comparison", "data": rows}


def experiment_3_material_comparison() -> dict:
    """Hoop stress at different radii with different materials."""
    print("\n=== Experiment 3: Material comparison (hoop stress) ===")

    materials = [
        ("Structural steel", 400.0, 7900.0),
        ("High-strength steel", 1200.0, 7900.0),
        ("Titanium Ti-6Al-4V", 900.0, 4540.0),
        ("CFRP", 3500.0, 1550.0),
    ]

    hoop = HoopStressConstraint()
    rows = []

    for mat_name, yield_mpa, density in materials:
        print(f"\n  {mat_name} (σy={yield_mpa} MPa, ρ={density}):")
        for r in [982, 3200, 5000, 8000, 15000]:
            assumptions = HumanAssumptions(
                yield_strength_mpa=yield_mpa,
            )
            params = HabitatParameters.from_radius_and_gravity(
                float(r),
                length_m=1000.0,
                hull_density_kg_m3=density,
            )
            result = hoop.evaluate(params, assumptions)
            status = "PASS" if result.feasible else "FAIL"

            row = {
                "material": mat_name,
                "radius_m": r,
                "sigma_rot_mpa": result.details["sigma_rot_mpa"],
                "sigma_pressure_mpa": result.details[
                    "sigma_pressure_mpa"
                ],
                "sigma_hoop_mpa": result.details["sigma_hoop_mpa"],
                "allowable_mpa": result.details["allowable_mpa"],
                "margin_pct": result.details["margin_pct"],
                "feasible": result.feasible,
            }
            rows.append(row)
            margin = result.details["margin_pct"]
            print(
                f"    r={r:>6}m: σ_hoop="
                f"{result.details['sigma_hoop_mpa']:>7.1f} MPa, "
                f"margin={margin:>6.1f}% {status}"
            )

    return {"name": "Material comparison", "data": rows}


def experiment_4_counter_rotating_impact() -> dict:
    """Compare single vs. counter-rotating at key design points."""
    print("\n=== Experiment 4: Single vs. counter-rotating ===")

    radii = [982, 2000, 3200]
    results_data = []

    for r in radii:
        for paired in [False, True]:
            mode = "paired" if paired else "single"
            assumptions = HumanAssumptions(
                counter_rotating_pair=paired,
            )

            # Find max feasible length by binary search
            lo, hi = 0.0, 50000.0
            rot = RotationalStabilityConstraint()
            bend = CylinderLengthConstraint()

            while hi - lo > 10.0:
                mid = (lo + hi) / 2.0
                params = HabitatParameters.from_radius_and_gravity(
                    float(r), length_m=mid
                )
                r1 = rot.evaluate(params, assumptions)
                r2 = bend.evaluate(params, assumptions)
                if r1.feasible and r2.feasible:
                    lo = mid
                else:
                    hi = mid

            max_length = lo
            land_area_km2 = (
                3.14159 * r * max_length / 1e6
            )

            row = {
                "radius_m": r,
                "mode": mode,
                "max_length_m": round(max_length, 0),
                "land_area_km2": round(land_area_km2, 2),
                "population_at_40m2": int(
                    land_area_km2 * 1e6 / 40
                ),
            }
            results_data.append(row)
            print(
                f"  r={r}m, {mode:>6}: "
                f"L_max={max_length:>8,.0f}m, "
                f"land={land_area_km2:>7.2f} km², "
                f"pop≈{row['population_at_40m2']:>9,}"
            )

    return {
        "name": "Single vs. counter-rotating",
        "data": results_data,
    }


def experiment_5_radius_sweep_with_structural() -> dict:
    """Sweep radius with all 12 constraints, find new feasible band."""
    print(
        "\n=== Experiment 5: Radius sweep "
        "(12 constraints, L=1.3r) ==="
    )

    assumptions = HumanAssumptions()
    constraints = all_constraints()
    solver = FeasibleRegionSolver(
        constraints=constraints,
        assumptions=assumptions,
    )

    feas_min = None
    feas_max = None
    binding_at_min = []
    binding_at_max = []

    sweep_data = []
    for r in range(100, 15001, 50):
        # Set length to max stable: L = 1.3r
        length = assumptions.max_length_to_radius_ratio * r
        params = HabitatParameters.from_radius_and_gravity(
            float(r),
            length_m=length,
            population=max(98, int(length * r * 0.001)),
        )
        results = solver.evaluate_point(params)
        feasible = all(cr.feasible for cr in results)
        failing = [
            cr.constraint_name
            for cr in results
            if not cr.feasible
        ]

        sweep_data.append(
            {
                "radius_m": r,
                "length_m": round(length, 0),
                "feasible": feasible,
                "failing": failing,
            }
        )

        if feasible:
            if feas_min is None:
                feas_min = r
            feas_max = r
        elif feas_min is not None and feas_max == r - 50:
            binding_at_max = failing

    # Find binding constraints at minimum
    if feas_min:
        r_below = feas_min - 50
        if r_below > 0:
            length = assumptions.max_length_to_radius_ratio * r_below
            params = HabitatParameters.from_radius_and_gravity(
                float(r_below),
                length_m=length,
                population=max(
                    98, int(length * r_below * 0.001)
                ),
            )
            results = solver.evaluate_point(params)
            binding_at_min = [
                cr.constraint_name
                for cr in results
                if not cr.feasible
            ]

    print(f"  Feasible band: [{feas_min}, {feas_max}] m")
    print(f"  Binding at lower: {binding_at_min}")
    print(f"  Binding at upper: {binding_at_max}")

    return {
        "name": "Radius sweep with structural constraints",
        "feasible_min_m": feas_min,
        "feasible_max_m": feas_max,
        "binding_at_min": binding_at_min,
        "binding_at_max": binding_at_max,
        "n_points": len(sweep_data),
    }


def main() -> dict:
    all_results = {
        "phase": 6,
        "n_constraints": 12,
        "experiments": [
            experiment_1_full_scorecard(),
            experiment_2_length_limits(),
            experiment_3_material_comparison(),
            experiment_4_counter_rotating_impact(),
            experiment_5_radius_sweep_with_structural(),
        ],
    }
    return all_results


if __name__ == "__main__":
    results = main()

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    out_path = OUTPUT_DIR / "phase6_results.json"
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nResults saved to {out_path}")
