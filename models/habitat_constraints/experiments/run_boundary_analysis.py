"""Boundary analysis experiments for human comfort in rotating habitats.

Explores the parameter space to find where constraints transition
from feasible to infeasible, and how sensitive boundaries are to
assumed human tolerance values.
"""

from __future__ import annotations

import json
import math
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


def find_minimum_feasible_radius(
    solver: FeasibleRegionSolver,
    target_g: float = 1.0,
    precision: float = 1.0,
) -> float | None:
    """Binary search for the smallest feasible radius at a given gravity."""
    lo, hi = 10.0, 10000.0
    if not solver.is_feasible(HabitatParameters.from_radius_and_gravity(hi, target_g)):
        return None
    while hi - lo > precision:
        mid = (lo + hi) / 2.0
        params = HabitatParameters.from_radius_and_gravity(mid, target_g)
        if solver.is_feasible(params):
            hi = mid
        else:
            lo = mid
    return hi


def experiment_1_sweep_at_1g() -> dict:
    """Sweep radius at 1g to find where each constraint kicks in."""
    print("=== Experiment 1: Radius sweep at 1g ===")
    solver = FeasibleRegionSolver(
        constraints=[
            VestibularConstraint(),
            GravityLevelConstraint(),
            GravityGradientConstraint(),
        ],
    )
    sweep = solver.sweep_radius(r_min=50, r_max=5000, n_points=500, target_gravity_g=1.0)

    # Find transition points per constraint
    constraint_names = ["vestibular", "gravity_level", "gravity_gradient"]
    transitions: dict[str, float | None] = {}

    for cname in constraint_names:
        prev_feasible = False
        for pt in sweep:
            cr = next(r for r in pt.constraint_results if r.constraint_name == cname)
            if cr.feasible and not prev_feasible:
                transitions[cname] = pt.radius_m
                break
            prev_feasible = cr.feasible
        else:
            transitions[cname] = None

    # Find overall minimum feasible radius
    min_r = find_minimum_feasible_radius(solver)

    # Sample points at key radii
    sample_radii = [100, 180, 224, 300, 500, 1000, 2000, 3200, 5000]
    samples = []
    for r in sample_radii:
        params = HabitatParameters.from_radius_and_gravity(r)
        results = solver.evaluate_point(params)
        samples.append(
            {
                "radius_m": r,
                "rpm": round(params.rpm, 3),
                "rim_speed_m_s": round(params.rim_speed_m_s, 1),
                "period_s": round(params.period_s, 1),
                "constraints": {
                    cr.constraint_name: {
                        "feasible": cr.feasible,
                        "details": {k: round(v, 4) for k, v in cr.details.items()},
                    }
                    for cr in results
                },
            }
        )

    result = {
        "name": "Radius sweep at 1g",
        "target_gravity_g": 1.0,
        "constraint_transition_radii": transitions,
        "minimum_feasible_radius_m": round(min_r, 1) if min_r else None,
        "sample_points": samples,
    }
    print(f"  Min feasible radius: {min_r:.1f}m")
    for cname, r in transitions.items():
        print(
            f"  {cname} becomes feasible at: {r:.0f}m"
            if r
            else f"  {cname}: never feasible"
        )
    return result


def experiment_2_gravity_levels() -> dict:
    """How does minimum viable radius change across gravity levels?"""
    print("\n=== Experiment 2: Minimum radius vs gravity level ===")
    solver = FeasibleRegionSolver(
        constraints=[
            VestibularConstraint(),
            GravityLevelConstraint(),
            GravityGradientConstraint(),
        ],
    )

    gravity_levels = [0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
    results = []
    for g in gravity_levels:
        min_r = find_minimum_feasible_radius(solver, target_g=g)
        if min_r:
            params = HabitatParameters.from_radius_and_gravity(min_r, g)
            results.append(
                {
                    "gravity_g": g,
                    "min_radius_m": round(min_r, 1),
                    "rpm_at_min_radius": round(params.rpm, 3),
                    "rim_speed_m_s": round(params.rim_speed_m_s, 1),
                }
            )
            print(f"  {g}g: min radius = {min_r:.1f}m, {params.rpm:.2f} RPM")
        else:
            results.append({"gravity_g": g, "min_radius_m": None})
            print(f"  {g}g: no feasible radius found")

    return {"name": "Minimum radius vs gravity level", "data": results}


def experiment_3_rpm_sensitivity() -> dict:
    """How does the RPM comfort threshold affect minimum radius?"""
    print("\n=== Experiment 3: RPM threshold sensitivity ===")
    rpm_thresholds = [1.0, 1.5, 2.0, 2.5, 3.0, 4.0, 6.0]
    results = []

    for rpm_limit in rpm_thresholds:
        assumptions = HumanAssumptions(max_comfortable_rpm=rpm_limit)
        solver = FeasibleRegionSolver(
            constraints=[
                VestibularConstraint(),
                GravityLevelConstraint(),
                GravityGradientConstraint(),
            ],
            assumptions=assumptions,
        )
        min_r = find_minimum_feasible_radius(solver)
        if min_r:
            params = HabitatParameters.from_radius_and_gravity(min_r)
            results.append(
                {
                    "rpm_limit": rpm_limit,
                    "min_radius_m": round(min_r, 1),
                    "actual_rpm": round(params.rpm, 3),
                }
            )
            print(f"  RPM limit {rpm_limit}: min radius = {min_r:.1f}m")
        else:
            results.append({"rpm_limit": rpm_limit, "min_radius_m": None})
            print(f"  RPM limit {rpm_limit}: no feasible radius")

    return {"name": "RPM threshold sensitivity", "data": results}


def experiment_4_gradient_sensitivity() -> dict:
    """How does acceptable gravity gradient affect minimum radius?"""
    print("\n=== Experiment 4: Gravity gradient threshold sensitivity ===")
    gradient_thresholds = [0.25, 0.5, 1.0, 2.0, 3.0, 5.0]
    results = []

    for grad_pct in gradient_thresholds:
        assumptions = HumanAssumptions(max_gravity_gradient_pct=grad_pct)
        solver = FeasibleRegionSolver(
            constraints=[
                VestibularConstraint(),
                GravityLevelConstraint(),
                GravityGradientConstraint(),
            ],
            assumptions=assumptions,
        )
        min_r = find_minimum_feasible_radius(solver)
        if min_r:
            params = HabitatParameters.from_radius_and_gravity(min_r)
            gradient_actual = (assumptions.person_height_m / min_r) * 100
            results.append(
                {
                    "max_gradient_pct": grad_pct,
                    "min_radius_m": round(min_r, 1),
                    "actual_gradient_pct": round(gradient_actual, 3),
                    "rpm": round(params.rpm, 3),
                }
            )
            print(f"  Gradient limit {grad_pct}%: min radius = {min_r:.1f}m")
        else:
            results.append({"max_gradient_pct": grad_pct, "min_radius_m": None})
            print(f"  Gradient limit {grad_pct}%: no feasible radius")

    return {"name": "Gravity gradient threshold sensitivity", "data": results}


def experiment_5_person_height() -> dict:
    """How does person height affect constraints?"""
    print("\n=== Experiment 5: Person height sensitivity ===")
    heights = [1.5, 1.6, 1.7, 1.8, 1.9, 2.0, 2.1]
    results = []

    for h in heights:
        assumptions = HumanAssumptions(person_height_m=h)
        solver = FeasibleRegionSolver(
            constraints=[
                VestibularConstraint(),
                GravityLevelConstraint(),
                GravityGradientConstraint(),
            ],
            assumptions=assumptions,
        )
        min_r = find_minimum_feasible_radius(solver)
        if min_r:
            gradient = (h / min_r) * 100
            results.append(
                {
                    "height_m": h,
                    "min_radius_m": round(min_r, 1),
                    "gradient_at_min_pct": round(gradient, 3),
                }
            )
            print(f"  Height {h}m: min radius = {min_r:.1f}m")
        else:
            results.append({"height_m": h, "min_radius_m": None})

    return {"name": "Person height sensitivity", "data": results}


def experiment_6_combined_stress_test() -> dict:
    """What happens at the boundary — detail every constraint at the minimum viable radius."""
    print("\n=== Experiment 6: Detailed analysis at boundary radius ===")
    solver = FeasibleRegionSolver(
        constraints=[
            VestibularConstraint(),
            GravityLevelConstraint(),
            GravityGradientConstraint(),
        ],
    )
    min_r = find_minimum_feasible_radius(solver, precision=0.1)
    if not min_r:
        return {"name": "Boundary analysis", "error": "No feasible radius found"}

    # Analyze at boundary, slightly below, and at key reference points
    test_radii = [
        ("below_boundary", min_r - 5),
        ("at_boundary", min_r),
        ("above_boundary", min_r + 50),
        ("comfortable", 500.0),
        ("oneill_reference", 3200.0),
    ]
    analyses = []
    for label, r in test_radii:
        params = HabitatParameters.from_radius_and_gravity(r)
        results = solver.evaluate_point(params)
        analysis = {
            "label": label,
            "radius_m": round(r, 1),
            "rpm": round(params.rpm, 3),
            "rim_speed_m_s": round(params.rim_speed_m_s, 1),
            "period_s": round(params.period_s, 1),
            "all_feasible": all(cr.feasible for cr in results),
            "constraints": {},
        }
        for cr in results:
            analysis["constraints"][cr.constraint_name] = {
                "feasible": cr.feasible,
                "details": {k: round(v, 4) for k, v in cr.details.items()},
            }
        analyses.append(analysis)
        status = "PASS" if analysis["all_feasible"] else "FAIL"
        print(f"  {label} (r={r:.1f}m, {params.rpm:.2f} RPM): {status}")

    return {
        "name": "Boundary analysis",
        "minimum_feasible_radius_m": round(min_r, 1),
        "analyses": analyses,
    }


def experiment_7_coriolis_preview() -> dict:
    """Preview Coriolis effects at various radii (computed manually, constraint not yet implemented).

    a_cor = 2 * omega * v_rel
    Ratio to gravity: a_cor / g_eff = 2 * v_rel / (omega * r) = 2 * v_rel / v_rim
    """
    print("\n=== Experiment 7: Coriolis effect preview ===")
    assumptions = HumanAssumptions()
    radii = [100, 224, 300, 500, 1000, 2000, 3200, 5000]
    results = []

    for r in radii:
        params = HabitatParameters.from_radius_and_gravity(r)
        omega = params.angular_velocity_rad_s
        g_eff = params.gravity_g * EARTH_G

        walk_coriolis = 2 * omega * assumptions.walking_speed_m_s
        run_coriolis = 2 * omega * assumptions.running_speed_m_s
        walk_ratio = walk_coriolis / g_eff
        run_ratio = run_coriolis / g_eff

        entry = {
            "radius_m": r,
            "rpm": round(params.rpm, 3),
            "coriolis_walking_m_s2": round(walk_coriolis, 4),
            "coriolis_running_m_s2": round(run_coriolis, 4),
            "coriolis_to_gravity_walking": round(walk_ratio, 4),
            "coriolis_to_gravity_running": round(run_ratio, 4),
            "walking_perceptible": walk_ratio > 0.01,
            "running_perceptible": run_ratio > 0.01,
        }
        results.append(entry)
        print(
            f"  r={r}m: walk Coriolis/g = {walk_ratio:.3f}, "
            f"run Coriolis/g = {run_ratio:.3f}"
        )

    return {
        "name": "Coriolis effect preview",
        "walking_speed_m_s": assumptions.walking_speed_m_s,
        "running_speed_m_s": assumptions.running_speed_m_s,
        "perceptibility_threshold": 0.01,
        "data": results,
    }


def main() -> dict:
    all_results = {
        "experiments": [
            experiment_1_sweep_at_1g(),
            experiment_2_gravity_levels(),
            experiment_3_rpm_sensitivity(),
            experiment_4_gradient_sensitivity(),
            experiment_5_person_height(),
            experiment_6_combined_stress_test(),
            experiment_7_coriolis_preview(),
        ]
    }
    return all_results


if __name__ == "__main__":
    results = main()
    json.dump(results, sys.stdout, indent=2)
    print()
