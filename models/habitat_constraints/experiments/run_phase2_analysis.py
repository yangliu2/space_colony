"""Phase 2 boundary analysis — all 6 constraints including Coriolis,
cross-coupling, and structural rim speed.

Builds on Phase 1 experiments and adds sensitivity analysis.
"""

from __future__ import annotations

import json
import sys

from habitat_constraints.core.parameters import (
    EARTH_G,
    HabitatParameters,
    HumanAssumptions,
)
from habitat_constraints.core.solver import FeasibleRegionSolver
from habitat_constraints.constraints.vestibular import VestibularConstraint
from habitat_constraints.constraints.gravity_level import GravityLevelConstraint
from habitat_constraints.constraints.gravity_gradient import (
    GravityGradientConstraint,
)
from habitat_constraints.constraints.coriolis import CoriolisConstraint
from habitat_constraints.constraints.cross_coupling import (
    CrossCouplingConstraint,
)
from habitat_constraints.constraints.rim_speed import RimSpeedConstraint
from habitat_constraints.analysis.sensitivity import run_sensitivity


def all_constraints() -> list:
    return [
        VestibularConstraint(),
        GravityLevelConstraint(),
        GravityGradientConstraint(),
        CoriolisConstraint(),
        CrossCouplingConstraint(),
        RimSpeedConstraint(),
    ]


def find_min_feasible_radius(
    solver: FeasibleRegionSolver,
    target_g: float = 1.0,
    precision: float = 1.0,
) -> float | None:
    """Binary search with scan for feasible point first."""
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


def find_max_feasible_radius(
    solver: FeasibleRegionSolver,
    target_g: float = 1.0,
    precision: float = 1.0,
) -> float | None:
    """Find the largest feasible radius (upper bound from rim speed)."""
    # Find a feasible point first
    feasible_r = None
    for r in [1000, 2000, 3200, 5000, 8000]:
        params = HabitatParameters.from_radius_and_gravity(r, target_g)
        if solver.is_feasible(params):
            feasible_r = r

    if feasible_r is None:
        return None

    # Binary search up
    lo, hi = feasible_r, 50000.0
    # Check if hi is feasible — if so, no upper bound in range
    params = HabitatParameters.from_radius_and_gravity(hi, target_g)
    if solver.is_feasible(params):
        return hi

    while hi - lo > precision:
        mid = (lo + hi) / 2.0
        params = HabitatParameters.from_radius_and_gravity(mid, target_g)
        if solver.is_feasible(params):
            lo = mid
        else:
            hi = mid
    return lo


def experiment_1_full_constraint_map() -> dict:
    """Evaluate all 6 constraints across the radius range."""
    print("=== Experiment 1: Full 6-constraint map at 1g ===")
    solver = FeasibleRegionSolver(constraints=all_constraints())

    sample_radii = [
        100,
        200,
        300,
        500,
        750,
        981,
        1000,
        1500,
        2000,
        3200,
        5000,
        8000,
        9177,
        10000,
    ]
    samples = []
    for r in sample_radii:
        params = HabitatParameters.from_radius_and_gravity(r)
        results = solver.evaluate_point(params)
        failing = [cr.constraint_name for cr in results if not cr.feasible]
        passing = [cr.constraint_name for cr in results if cr.feasible]
        all_ok = len(failing) == 0

        entry = {
            "radius_m": r,
            "rpm": round(params.rpm, 3),
            "rim_speed_m_s": round(params.rim_speed_m_s, 1),
            "all_feasible": all_ok,
            "failing": failing,
            "passing": passing,
        }
        # Add key details
        for cr in results:
            entry[f"{cr.constraint_name}_details"] = {
                k: round(v, 4) for k, v in cr.details.items()
            }
        samples.append(entry)
        status = "PASS" if all_ok else f"FAIL [{', '.join(failing)}]"
        print(f"  r={r}m ({params.rpm:.2f} RPM): {status}")

    r_min = find_min_feasible_radius(solver)
    r_max = find_max_feasible_radius(solver)
    print(f"\n  Feasible radius range: [{r_min:.0f}m, {r_max:.0f}m]")

    return {
        "name": "Full 6-constraint map at 1g",
        "feasible_radius_min_m": round(r_min, 1) if r_min else None,
        "feasible_radius_max_m": round(r_max, 1) if r_max else None,
        "samples": samples,
    }


def experiment_2_constraint_contribution() -> dict:
    """Which constraint is binding at each radius?"""
    print("\n=== Experiment 2: Binding constraint by radius ===")
    solver = FeasibleRegionSolver(constraints=all_constraints())

    # Fine sweep through transition zones
    radii = list(range(100, 1200, 25)) + list(range(1200, 10000, 200))
    binding_map = []
    for r in radii:
        params = HabitatParameters.from_radius_and_gravity(r)
        results = solver.evaluate_point(params)
        failing = [cr.constraint_name for cr in results if not cr.feasible]
        binding_map.append(
            {
                "radius_m": r,
                "rpm": round(params.rpm, 3),
                "failing_constraints": failing,
                "n_failing": len(failing),
            }
        )

    # Find transition points
    transitions = {}
    constraint_names = [
        "vestibular",
        "gravity_gradient",
        "coriolis",
        "cross_coupling",
        "rim_speed",
    ]
    for cname in constraint_names:
        prev_failing = True
        for entry in binding_map:
            currently_failing = cname in entry["failing_constraints"]
            if prev_failing and not currently_failing:
                transitions[f"{cname}_becomes_feasible"] = entry["radius_m"]
            if not prev_failing and currently_failing:
                transitions[f"{cname}_becomes_infeasible"] = entry["radius_m"]
            prev_failing = currently_failing

    print("  Transition points:")
    for k, v in transitions.items():
        print(f"    {k}: {v}m")

    return {
        "name": "Binding constraint by radius",
        "transitions": transitions,
        "binding_map": binding_map,
    }


def experiment_3_gravity_vs_radius_with_all() -> dict:
    """Feasible band across gravity levels with all constraints."""
    print("\n=== Experiment 3: Feasible band across gravity levels ===")
    gravity_levels = [0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
    results = []

    for g in gravity_levels:
        solver = FeasibleRegionSolver(constraints=all_constraints())
        r_min = find_min_feasible_radius(solver, target_g=g)
        r_max = find_max_feasible_radius(solver, target_g=g)

        if r_min and r_max:
            params_min = HabitatParameters.from_radius_and_gravity(r_min, g)
            params_max = HabitatParameters.from_radius_and_gravity(r_max, g)
            entry = {
                "gravity_g": g,
                "min_radius_m": round(r_min, 1),
                "max_radius_m": round(r_max, 1),
                "rpm_at_min": round(params_min.rpm, 3),
                "rpm_at_max": round(params_max.rpm, 3),
                "rim_speed_at_max_m_s": round(params_max.rim_speed_m_s, 1),
                "feasible_band_width_m": round(r_max - r_min, 1),
            }
            print(
                f"  {g}g: r ∈ [{r_min:.0f}, {r_max:.0f}]m "
                f"(band = {r_max - r_min:.0f}m)"
            )
        else:
            entry = {"gravity_g": g, "min_radius_m": None, "max_radius_m": None}
            print(f"  {g}g: no feasible region")
        results.append(entry)

    return {"name": "Feasible band across gravity levels", "data": results}


def experiment_4_sensitivity() -> dict:
    """Full sensitivity analysis with tornado chart data."""
    print("\n=== Experiment 4: Sensitivity analysis (±20%) ===")
    report = run_sensitivity(
        all_constraints(),
        perturbation_pct=20.0,
    )

    tornado_data = []
    print(f"  Baseline min radius: {report.baseline_min_radius:.1f}m")
    print(f"  Tornado chart (sorted by impact):")
    for t in report.tornado:
        r_lo = f"{t.radius_at_low:.0f}" if t.radius_at_low else "N/A"
        r_hi = f"{t.radius_at_high:.0f}" if t.radius_at_high else "N/A"
        spread = f"{t.spread:.0f}" if t.spread != float("inf") else "inf"
        print(
            f"    {t.parameter_name}: "
            f"[{t.low_value:.2f}, {t.high_value:.2f}] → "
            f"radius [{r_lo}, {r_hi}]m (spread={spread}m)"
        )
        tornado_data.append(
            {
                "parameter": t.parameter_name,
                "baseline_value": t.baseline_value,
                "low_value": round(t.low_value, 4),
                "high_value": round(t.high_value, 4),
                "radius_at_low": round(t.radius_at_low, 1) if t.radius_at_low else None,
                "radius_at_high": (
                    round(t.radius_at_high, 1) if t.radius_at_high else None
                ),
                "spread_m": round(t.spread, 1) if t.spread != float("inf") else None,
            }
        )

    return {
        "name": "Sensitivity analysis",
        "baseline_min_radius_m": (
            round(report.baseline_min_radius, 1) if report.baseline_min_radius else None
        ),
        "perturbation_pct": 20.0,
        "tornado": tornado_data,
    }


def experiment_5_cross_coupling_deep_dive() -> dict:
    """Cross-coupling is the new binding constraint. Explore its parameter space."""
    print("\n=== Experiment 5: Cross-coupling deep dive ===")

    head_rates = [30, 45, 60, 90, 120]
    thresholds = [3.0, 6.0, 10.0, 15.0]

    results = []
    for head_rate in head_rates:
        for threshold in thresholds:
            assumptions = HumanAssumptions(
                head_turn_rate_deg_s=head_rate,
                max_cross_coupling_deg_s2=threshold,
            )
            solver = FeasibleRegionSolver(
                constraints=all_constraints(),
                assumptions=assumptions,
            )
            r_min = find_min_feasible_radius(solver)
            entry = {
                "head_turn_rate_deg_s": head_rate,
                "threshold_deg_s2": threshold,
                "min_radius_m": round(r_min, 1) if r_min else None,
            }
            results.append(entry)
            r_str = f"{r_min:.0f}m" if r_min else "infeasible"
            print(
                f"  head={head_rate}°/s, threshold={threshold}°/s²: " f"r_min = {r_str}"
            )

    return {
        "name": "Cross-coupling parameter space",
        "data": results,
    }


def experiment_6_oneill_scorecard() -> dict:
    """Detailed scorecard for O'Neill's 3200m design."""
    print("\n=== Experiment 6: O'Neill 3200m scorecard ===")
    params = HabitatParameters.from_radius_and_gravity(3200.0)
    solver = FeasibleRegionSolver(constraints=all_constraints())
    results = solver.evaluate_point(params)

    scorecard = {
        "radius_m": 3200.0,
        "rpm": round(params.rpm, 4),
        "rim_speed_m_s": round(params.rim_speed_m_s, 1),
        "period_s": round(params.period_s, 1),
        "all_feasible": all(cr.feasible for cr in results),
        "constraints": {},
    }
    for cr in results:
        scorecard["constraints"][cr.constraint_name] = {
            "feasible": cr.feasible,
            "details": {k: round(v, 4) for k, v in cr.details.items()},
        }
        status = "PASS" if cr.feasible else "FAIL"
        print(f"  {cr.constraint_name}: {status}")
        for k, v in cr.details.items():
            print(f"    {k}: {v:.4f}")

    return {"name": "O'Neill 3200m scorecard", "scorecard": scorecard}


def main() -> dict:
    all_results = {
        "phase": 2,
        "n_constraints": 6,
        "experiments": [
            experiment_1_full_constraint_map(),
            experiment_2_constraint_contribution(),
            experiment_3_gravity_vs_radius_with_all(),
            experiment_4_sensitivity(),
            experiment_5_cross_coupling_deep_dive(),
            experiment_6_oneill_scorecard(),
        ],
    }
    return all_results


if __name__ == "__main__":
    results = main()
    json.dump(results, sys.stdout, indent=2)
    print()
