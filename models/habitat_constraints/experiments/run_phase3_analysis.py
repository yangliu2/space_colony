"""Phase 3 analysis — biological constraints, Monte Carlo, visualization.

Extends Phase 2 with:
- 3 biological constraints (radiation, atmosphere, population)
- Monte Carlo simulation over assumption distributions
- Matplotlib visualizations (feasible region, tornado, histograms)
- Mass budget analysis for minimum and O'Neill-class cylinders
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

from habitat_constraints.core.parameters import (
    HabitatParameters,
    HumanAssumptions,
)
from habitat_constraints.core.solver import FeasibleRegionSolver
from habitat_constraints.constraints.vestibular import (
    VestibularConstraint,
)
from habitat_constraints.constraints.gravity_level import (
    GravityLevelConstraint,
)
from habitat_constraints.constraints.gravity_gradient import (
    GravityGradientConstraint,
)
from habitat_constraints.constraints.coriolis import CoriolisConstraint
from habitat_constraints.constraints.cross_coupling import (
    CrossCouplingConstraint,
)
from habitat_constraints.constraints.rim_speed import RimSpeedConstraint
from habitat_constraints.constraints.radiation import (
    RadiationConstraint,
)
from habitat_constraints.constraints.atmosphere import (
    AtmosphereConstraint,
)
from habitat_constraints.constraints.population import (
    PopulationConstraint,
)
from habitat_constraints.analysis.sensitivity import run_sensitivity
from habitat_constraints.analysis.monte_carlo import run_monte_carlo
from habitat_constraints.visualization.plots import (
    plot_feasible_region,
    plot_tornado,
    plot_radius_sweep,
    plot_monte_carlo_histogram,
    plot_mass_budget,
)

OUTPUT_DIR = Path(__file__).parent / "output"


def rotational_constraints() -> list:
    return [
        VestibularConstraint(),
        GravityLevelConstraint(),
        GravityGradientConstraint(),
        CoriolisConstraint(),
        CrossCouplingConstraint(),
        RimSpeedConstraint(),
    ]


def all_constraints() -> list:
    return rotational_constraints() + [
        RadiationConstraint(),
        AtmosphereConstraint(),
        PopulationConstraint(),
    ]


def find_min_feasible_radius(
    solver: FeasibleRegionSolver,
    target_g: float = 1.0,
    precision: float = 1.0,
) -> float | None:
    for r in [50, 100, 200, 500, 1000, 2000, 3200, 5000, 8000]:
        params = HabitatParameters.from_radius_and_gravity(r, target_g)
        if solver.is_feasible(params):
            break
    else:
        return None

    lo, hi = 10.0, r
    while hi - lo > precision:
        mid = (lo + hi) / 2.0
        params = HabitatParameters.from_radius_and_gravity(mid, target_g)
        if solver.is_feasible(params):
            hi = mid
        else:
            lo = mid
    return hi


def experiment_1_full_scorecard() -> dict:
    """Full 9-constraint scorecard at two design points."""
    print("=== Experiment 1: Full 9-constraint scorecard ===")
    designs = [
        ("Minimum Viable", 982.0, 2000.0, 8000),
        ("O'Neill Island Three", 3200.0, 32000.0, 1000000),
    ]

    scorecards = []
    for name, r, length, pop in designs:
        params = HabitatParameters.from_radius_and_gravity(
            r,
            length_m=length,
            population=pop,
        )
        solver = FeasibleRegionSolver(constraints=all_constraints())
        results = solver.evaluate_point(params)

        card = {
            "design": name,
            "radius_m": r,
            "length_m": length,
            "population": pop,
            "rpm": round(params.rpm, 3),
            "rim_speed_m_s": round(params.rim_speed_m_s, 1),
            "all_pass": all(cr.feasible for cr in results),
            "constraints": {},
        }
        print(f"\n  {name} (r={r}m, L={length}m, pop={pop}):")
        for cr in results:
            status = "PASS" if cr.feasible else "FAIL"
            card["constraints"][cr.constraint_name] = {
                "feasible": cr.feasible,
                "details": {k: round(v, 4) for k, v in cr.details.items()},
            }
            print(f"    {cr.constraint_name}: {status}")
        scorecards.append(card)

    return {"name": "Full 9-constraint scorecard", "data": scorecards}


def experiment_2_biological_sweep() -> dict:
    """Sweep atmosphere and shielding parameters."""
    print("\n=== Experiment 2: Biological parameter sweep ===")

    # Atmosphere: vary O2 fraction at different pressures
    atmo_results = []
    for p_kpa in [51.0, 56.5, 101.3]:
        for o2_frac in [0.10, 0.15, 0.21, 0.34, 0.50, 0.80, 1.0]:
            po2 = p_kpa * o2_frac
            feasible = 16.0 <= po2 <= 50.0
            atmo_results.append(
                {
                    "pressure_kpa": p_kpa,
                    "o2_fraction": o2_frac,
                    "po2_kpa": round(po2, 1),
                    "feasible": feasible,
                }
            )
            status = "PASS" if feasible else "FAIL"
            print(f"  P={p_kpa}kPa, O2={o2_frac:.0%}: " f"pO2={po2:.1f}kPa {status}")

    return {
        "name": "Biological parameter sweep",
        "atmosphere": atmo_results,
    }


def experiment_3_monte_carlo() -> dict:
    """Monte Carlo simulation with 500 trials."""
    print("\n=== Experiment 3: Monte Carlo (500 trials) ===")

    report = run_monte_carlo(
        rotational_constraints(),
        n_trials=500,
        seed=42,
    )

    p5 = report.percentile_min_radius(5)
    p50 = report.percentile_min_radius(50)
    p95 = report.percentile_min_radius(95)

    print(f"  Feasibility rate: {report.feasibility_rate:.1%}")
    print(f"  Min radius P5: {p5:.0f}m" if p5 else "  P5: N/A")
    print(f"  Min radius P50: {p50:.0f}m" if p50 else "  P50: N/A")
    print(f"  Min radius P95: {p95:.0f}m" if p95 else "  P95: N/A")

    p5_max = report.percentile_max_radius(5)
    p50_max = report.percentile_max_radius(50)
    p95_max = report.percentile_max_radius(95)

    print(f"  Max radius P5: {p5_max:.0f}m" if p5_max else "")
    print(f"  Max radius P50: {p50_max:.0f}m" if p50_max else "")
    print(f"  Max radius P95: {p95_max:.0f}m" if p95_max else "")

    # Save plots
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    plot_monte_carlo_histogram(
        report,
        output_path=OUTPUT_DIR / "monte_carlo_histogram.png",
    )
    print("  Saved: output/monte_carlo_histogram.png")

    return {
        "name": "Monte Carlo simulation",
        "n_trials": report.n_trials,
        "feasibility_rate": round(report.feasibility_rate, 4),
        "min_radius_p5": round(p5, 1) if p5 else None,
        "min_radius_p50": round(p50, 1) if p50 else None,
        "min_radius_p95": round(p95, 1) if p95 else None,
        "max_radius_p50": round(p50_max, 1) if p50_max else None,
    }


def experiment_4_visualizations() -> dict:
    """Generate all visualization plots."""
    print("\n=== Experiment 4: Generating visualizations ===")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    solver = FeasibleRegionSolver(constraints=rotational_constraints())

    # Feasible region plot
    plot_feasible_region(
        solver,
        output_path=OUTPUT_DIR / "feasible_region.png",
    )
    print("  Saved: output/feasible_region.png")

    # Radius sweep
    sweep = solver.sweep_radius(50, 15000, n_points=200)
    plot_radius_sweep(
        sweep,
        output_path=OUTPUT_DIR / "radius_sweep.png",
    )
    print("  Saved: output/radius_sweep.png")

    # Sensitivity tornado
    report = run_sensitivity(rotational_constraints())
    plot_tornado(
        report,
        output_path=OUTPUT_DIR / "tornado_chart.png",
    )
    print("  Saved: output/tornado_chart.png")

    # Mass budgets
    for name, r, length in [
        ("minimum", 982, 2000),
        ("oneill", 3200, 32000),
    ]:
        plot_mass_budget(
            r,
            length,
            output_path=OUTPUT_DIR / f"mass_budget_{name}.png",
        )
        print(f"  Saved: output/mass_budget_{name}.png")

    return {"name": "Visualizations generated", "plots_saved": 5}


def experiment_5_sensitivity_with_bio() -> dict:
    """Sensitivity analysis including biological parameters."""
    print("\n=== Experiment 5: Extended sensitivity analysis ===")

    # Only rotational constraints for sensitivity
    # (biological ones need geometry, which doesn't vary with radius)
    report = run_sensitivity(
        rotational_constraints(),
        perturbation_pct=20.0,
    )

    print(
        f"  Baseline min radius: " f"{report.baseline_min_radius:.1f}m"
        if report.baseline_min_radius
        else "  No baseline"
    )
    print("  Top 5 sensitive parameters:")
    for t in report.tornado[:5]:
        r_lo = f"{t.radius_at_low:.0f}" if t.radius_at_low else "N/A"
        r_hi = f"{t.radius_at_high:.0f}" if t.radius_at_high else "N/A"
        spread = f"{t.spread:.0f}" if t.spread != float("inf") else "inf"
        print(f"    {t.parameter_name}: " f"[{r_lo}, {r_hi}]m (spread={spread}m)")

    return {
        "name": "Extended sensitivity analysis",
        "baseline_min_radius": (
            round(report.baseline_min_radius, 1) if report.baseline_min_radius else None
        ),
        "top_3": [
            {
                "param": t.parameter_name,
                "spread": round(t.spread, 1) if t.spread != float("inf") else None,
            }
            for t in report.tornado[:3]
        ],
    }


def main() -> dict:
    all_results = {
        "phase": 3,
        "n_constraints": 9,
        "experiments": [
            experiment_1_full_scorecard(),
            experiment_2_biological_sweep(),
            experiment_3_monte_carlo(),
            experiment_4_visualizations(),
            experiment_5_sensitivity_with_bio(),
        ],
    }
    return all_results


if __name__ == "__main__":
    results = main()
    json.dump(results, sys.stdout, indent=2)
    print()
