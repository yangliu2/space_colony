"""Monte Carlo simulation — stochastic feasibility analysis."""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np

from habitat_constraints.core.constraint import Constraint
from habitat_constraints.core.parameters import (
    HabitatParameters,
    HumanAssumptions,
)
from habitat_constraints.core.solver import FeasibleRegionSolver


@dataclass
class ParameterDistribution:
    """Distribution specification for a single assumption parameter."""

    name: str
    mean: float
    std: float
    dist_type: str = "normal"  # "normal" or "uniform"
    lower_clip: float | None = None  # clip to avoid negative
    upper_clip: float | None = None


@dataclass
class MonteCarloResult:
    """Result of one Monte Carlo trial."""

    trial: int
    assumptions: dict[str, float]
    min_feasible_radius: float | None
    max_feasible_radius: float | None
    feasible_band_width: float | None


@dataclass
class MonteCarloReport:
    """Aggregated Monte Carlo simulation output."""

    n_trials: int
    target_gravity_g: float
    distributions: list[ParameterDistribution]
    results: list[MonteCarloResult] = field(default_factory=list)

    @property
    def min_radii(self) -> list[float]:
        """All non-None minimum feasible radii."""
        return [
            r.min_feasible_radius
            for r in self.results
            if r.min_feasible_radius is not None
        ]

    @property
    def max_radii(self) -> list[float]:
        """All non-None maximum feasible radii."""
        return [
            r.max_feasible_radius
            for r in self.results
            if r.max_feasible_radius is not None
        ]

    @property
    def feasibility_rate(self) -> float:
        """Fraction of trials that found a feasible region."""
        if not self.results:
            return 0.0
        n_feasible = sum(1 for r in self.results if r.min_feasible_radius is not None)
        return n_feasible / len(self.results)

    def percentile_min_radius(self, pct: float) -> float | None:
        """Percentile of minimum feasible radius distribution."""
        radii = self.min_radii
        if not radii:
            return None
        return float(np.percentile(radii, pct))

    def percentile_max_radius(self, pct: float) -> float | None:
        """Percentile of maximum feasible radius distribution."""
        radii = self.max_radii
        if not radii:
            return None
        return float(np.percentile(radii, pct))


# Default distributions based on literature uncertainty ranges
DEFAULT_DISTRIBUTIONS: list[ParameterDistribution] = [
    ParameterDistribution(
        name="max_comfortable_rpm",
        mean=2.0,
        std=0.5,
        lower_clip=0.5,
        upper_clip=6.0,
    ),
    ParameterDistribution(
        name="max_cross_coupling_deg_s2",
        mean=6.0,
        std=2.0,
        lower_clip=2.0,
        upper_clip=15.0,
    ),
    ParameterDistribution(
        name="head_turn_rate_deg_s",
        mean=60.0,
        std=15.0,
        lower_clip=20.0,
        upper_clip=120.0,
    ),
    ParameterDistribution(
        name="max_coriolis_ratio",
        mean=0.25,
        std=0.05,
        lower_clip=0.05,
        upper_clip=0.50,
    ),
    ParameterDistribution(
        name="max_rim_speed_m_s",
        mean=300.0,
        std=50.0,
        lower_clip=150.0,
        upper_clip=600.0,
    ),
    ParameterDistribution(
        name="max_gravity_gradient_pct",
        mean=1.0,
        std=0.3,
        lower_clip=0.3,
        upper_clip=5.0,
    ),
]


def _find_min_feasible_radius(
    solver: FeasibleRegionSolver,
    target_g: float,
    precision: float = 5.0,
) -> float | None:
    """Quick scan-then-binary-search for minimum feasible radius."""
    feasible_r: float | None = None
    for r in [50, 100, 200, 500, 1000, 2000, 3200, 5000, 8000, 12000]:
        params = HabitatParameters.from_radius_and_gravity(r, target_g)
        if solver.is_feasible(params):
            feasible_r = r
            break

    if feasible_r is None:
        return None

    lo, hi = 10.0, feasible_r
    while hi - lo > precision:
        mid = (lo + hi) / 2.0
        params = HabitatParameters.from_radius_and_gravity(mid, target_g)
        if solver.is_feasible(params):
            hi = mid
        else:
            lo = mid
    return hi


def _find_max_feasible_radius(
    solver: FeasibleRegionSolver,
    target_g: float,
    precision: float = 5.0,
) -> float | None:
    """Quick scan-then-binary-search for maximum feasible radius."""
    feasible_r: float | None = None
    for r in [1000, 2000, 3200, 5000, 8000, 12000]:
        params = HabitatParameters.from_radius_and_gravity(r, target_g)
        if solver.is_feasible(params):
            feasible_r = r

    if feasible_r is None:
        return None

    lo, hi = feasible_r, 50000.0
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


def _sample_assumptions(
    rng: np.random.Generator,
    distributions: list[ParameterDistribution],
    baseline: HumanAssumptions,
) -> HumanAssumptions:
    """Sample one set of assumptions from distributions."""
    updates: dict[str, float] = {}
    for dist in distributions:
        if dist.dist_type == "normal":
            val = rng.normal(dist.mean, dist.std)
        elif dist.dist_type == "uniform":
            lo = dist.mean - dist.std
            hi = dist.mean + dist.std
            val = rng.uniform(lo, hi)
        else:
            val = dist.mean

        if dist.lower_clip is not None:
            val = max(val, dist.lower_clip)
        if dist.upper_clip is not None:
            val = min(val, dist.upper_clip)

        updates[dist.name] = val

    return baseline.model_copy(update=updates)


def run_monte_carlo(
    constraints: list[Constraint],
    n_trials: int = 1000,
    target_gravity_g: float = 1.0,
    distributions: list[ParameterDistribution] | None = None,
    baseline_assumptions: HumanAssumptions | None = None,
    seed: int = 42,
) -> MonteCarloReport:
    """Run Monte Carlo simulation over assumption distributions.

    Parameters
    ----------
    constraints
        List of constraint instances to evaluate.
    n_trials
        Number of random trials to run.
    target_gravity_g
        Gravity target for all trials.
    distributions
        Parameter distributions to sample from.
        Defaults to DEFAULT_DISTRIBUTIONS.
    baseline_assumptions
        Starting assumptions (non-varied params use these).
    seed
        Random seed for reproducibility.

    Returns
    -------
    MonteCarloReport with per-trial results and statistics.
    """
    dists = distributions or DEFAULT_DISTRIBUTIONS
    baseline = baseline_assumptions or HumanAssumptions()
    rng = np.random.default_rng(seed)

    report = MonteCarloReport(
        n_trials=n_trials,
        target_gravity_g=target_gravity_g,
        distributions=dists,
    )

    for i in range(n_trials):
        sampled = _sample_assumptions(rng, dists, baseline)
        solver = FeasibleRegionSolver(
            constraints=list(constraints),
            assumptions=sampled,
        )

        r_min = _find_min_feasible_radius(solver, target_gravity_g)
        r_max = _find_max_feasible_radius(solver, target_gravity_g)

        band = None
        if r_min is not None and r_max is not None:
            band = r_max - r_min

        report.results.append(
            MonteCarloResult(
                trial=i,
                assumptions={d.name: getattr(sampled, d.name) for d in dists},
                min_feasible_radius=r_min,
                max_feasible_radius=r_max,
                feasible_band_width=band,
            )
        )

    return report
