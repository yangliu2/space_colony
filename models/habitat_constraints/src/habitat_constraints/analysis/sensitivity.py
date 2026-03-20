"""Sensitivity analysis — systematic parameter perturbation."""

from __future__ import annotations

from dataclasses import dataclass, field
from habitat_constraints.core.constraint import Constraint
from habitat_constraints.core.parameters import (
    HabitatParameters,
    HumanAssumptions,
)
from habitat_constraints.core.solver import FeasibleRegionSolver


@dataclass
class SensitivityResult:
    """Result of perturbing one assumption parameter."""

    parameter_name: str
    baseline_value: float
    perturbed_value: float
    direction: str  # "low" or "high"
    baseline_min_radius: float | None
    perturbed_min_radius: float | None
    delta_radius: float | None  # perturbed - baseline
    delta_pct: float | None  # percentage change


@dataclass
class TornadoEntry:
    """One row in a tornado chart — shows low/high impact."""

    parameter_name: str
    baseline_value: float
    low_value: float
    high_value: float
    radius_at_low: float | None
    radius_at_high: float | None
    baseline_radius: float | None
    spread: float  # |radius_at_high - radius_at_low|


@dataclass
class SensitivityReport:
    """Full sensitivity analysis output."""

    baseline_assumptions: dict[str, float]
    baseline_min_radius: float | None
    target_gravity_g: float
    perturbation_pct: float
    results: list[SensitivityResult] = field(default_factory=list)
    tornado: list[TornadoEntry] = field(default_factory=list)


def _find_min_feasible_radius(
    solver: FeasibleRegionSolver,
    target_g: float = 1.0,
    precision: float = 1.0,
) -> float | None:
    """Binary search for minimum feasible radius.

    First scans to find *any* feasible point (handles upper-bounded
    constraints like rim speed), then binary searches below it.
    """
    # Scan for a feasible point in the range
    feasible_r: float | None = None
    for r in [
        50,
        100,
        200,
        500,
        1000,
        2000,
        3200,
        5000,
        8000,
        12000,
        20000,
    ]:
        params = HabitatParameters.from_radius_and_gravity(r, target_g)
        if solver.is_feasible(params):
            feasible_r = r
            break

    if feasible_r is None:
        return None

    # Binary search: find minimum feasible radius below the found point
    lo, hi = 10.0, feasible_r
    while hi - lo > precision:
        mid = (lo + hi) / 2.0
        params = HabitatParameters.from_radius_and_gravity(mid, target_g)
        if solver.is_feasible(params):
            hi = mid
        else:
            lo = mid
    return hi


# Parameters we can perturb, with their field names on HumanAssumptions
PERTURBABLE_PARAMS: list[str] = [
    "max_comfortable_rpm",
    "max_gravity_gradient_pct",
    "max_coriolis_ratio",
    "max_cross_coupling_deg_s2",
    "head_turn_rate_deg_s",
    "max_rim_speed_m_s",
    "person_height_m",
    "walking_speed_m_s",
    "running_speed_m_s",
    "min_gravity_g",
    "max_gravity_g",
]


def run_sensitivity(
    constraints: list[Constraint],
    baseline_assumptions: HumanAssumptions | None = None,
    target_gravity_g: float = 1.0,
    perturbation_pct: float = 20.0,
    parameters: list[str] | None = None,
) -> SensitivityReport:
    """Perturb each assumption ± perturbation_pct and measure min radius change.

    Parameters
    ----------
    constraints
        List of constraint instances to use.
    baseline_assumptions
        Starting assumptions. Defaults to HumanAssumptions().
    target_gravity_g
        Gravity target for the sweep.
    perturbation_pct
        Percentage to perturb each parameter up and down.
    parameters
        Which parameters to perturb. Defaults to all perturbable params.

    Returns
    -------
    SensitivityReport with per-parameter results and tornado chart data.
    """
    baseline = baseline_assumptions or HumanAssumptions()
    params_to_test = parameters or PERTURBABLE_PARAMS

    # Baseline min radius
    solver = FeasibleRegionSolver(constraints=list(constraints), assumptions=baseline)
    baseline_r = _find_min_feasible_radius(solver, target_gravity_g)

    report = SensitivityReport(
        baseline_assumptions={p: getattr(baseline, p) for p in params_to_test},
        baseline_min_radius=baseline_r,
        target_gravity_g=target_gravity_g,
        perturbation_pct=perturbation_pct,
    )

    for param_name in params_to_test:
        base_val = getattr(baseline, param_name)
        low_val = base_val * (1.0 - perturbation_pct / 100.0)
        high_val = base_val * (1.0 + perturbation_pct / 100.0)

        # Ensure positive
        low_val = max(low_val, 1e-6)

        for direction, perturbed_val in [
            ("low", low_val),
            ("high", high_val),
        ]:
            perturbed = baseline.model_copy(update={param_name: perturbed_val})
            solver_p = FeasibleRegionSolver(
                constraints=list(constraints), assumptions=perturbed
            )
            perturbed_r = _find_min_feasible_radius(solver_p, target_gravity_g)

            if baseline_r is not None and perturbed_r is not None:
                delta = perturbed_r - baseline_r
                delta_pct = (delta / baseline_r) * 100.0
            else:
                delta = None
                delta_pct = None

            report.results.append(
                SensitivityResult(
                    parameter_name=param_name,
                    baseline_value=base_val,
                    perturbed_value=perturbed_val,
                    direction=direction,
                    baseline_min_radius=baseline_r,
                    perturbed_min_radius=perturbed_r,
                    delta_radius=delta,
                    delta_pct=delta_pct,
                )
            )

    # Build tornado entries
    for param_name in params_to_test:
        low_result = next(
            r
            for r in report.results
            if r.parameter_name == param_name and r.direction == "low"
        )
        high_result = next(
            r
            for r in report.results
            if r.parameter_name == param_name and r.direction == "high"
        )
        r_low = low_result.perturbed_min_radius
        r_high = high_result.perturbed_min_radius

        if r_low is not None and r_high is not None:
            spread = abs(r_high - r_low)
        else:
            spread = float("inf")

        report.tornado.append(
            TornadoEntry(
                parameter_name=param_name,
                baseline_value=getattr(baseline, param_name),
                low_value=low_result.perturbed_value,
                high_value=high_result.perturbed_value,
                radius_at_low=r_low,
                radius_at_high=r_high,
                baseline_radius=baseline_r,
                spread=spread,
            )
        )

    # Sort tornado by spread (largest first)
    report.tornado.sort(key=lambda t: t.spread, reverse=True)

    return report
