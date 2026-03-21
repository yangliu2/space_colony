"""Tests for Monte Carlo simulation module."""

from __future__ import annotations

from habitat_constraints.analysis.monte_carlo import (
    MonteCarloReport,
    ParameterDistribution,
    run_monte_carlo,
)
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


def _all_rotational_constraints() -> (
    list[
        VestibularConstraint
        | GravityLevelConstraint
        | GravityGradientConstraint
        | CoriolisConstraint
        | CrossCouplingConstraint
        | RimSpeedConstraint
    ]
):
    return [
        VestibularConstraint(),
        GravityLevelConstraint(),
        GravityGradientConstraint(),
        CoriolisConstraint(),
        CrossCouplingConstraint(),
        RimSpeedConstraint(),
    ]


class TestMonteCarlo:
    def test_basic_run(self) -> None:
        report = run_monte_carlo(
            _all_rotational_constraints(),
            n_trials=20,
            seed=42,
        )
        assert isinstance(report, MonteCarloReport)
        assert len(report.results) == 20

    def test_feasibility_rate_positive(self) -> None:
        report = run_monte_carlo(
            _all_rotational_constraints(),
            n_trials=50,
            seed=42,
        )
        # Most trials should find a feasible region
        assert report.feasibility_rate > 0.5

    def test_percentiles_ordered(self) -> None:
        report = run_monte_carlo(
            _all_rotational_constraints(),
            n_trials=50,
            seed=42,
        )
        p5 = report.percentile_min_radius(5)
        p50 = report.percentile_min_radius(50)
        p95 = report.percentile_min_radius(95)
        assert p5 is not None
        assert p50 is not None
        assert p95 is not None
        assert p5 <= p50 <= p95

    def test_reproducible_with_seed(self) -> None:
        r1 = run_monte_carlo(
            _all_rotational_constraints(),
            n_trials=10,
            seed=123,
        )
        r2 = run_monte_carlo(
            _all_rotational_constraints(),
            n_trials=10,
            seed=123,
        )
        for a, b in zip(r1.results, r2.results):
            assert a.min_feasible_radius == b.min_feasible_radius

    def test_custom_distributions(self) -> None:
        dists = [
            ParameterDistribution(
                name="max_comfortable_rpm",
                mean=3.0,
                std=0.5,
                lower_clip=1.0,
            ),
        ]
        report = run_monte_carlo(
            _all_rotational_constraints(),
            n_trials=10,
            distributions=dists,
            seed=42,
        )
        assert len(report.results) == 10
        # With higher RPM tolerance, should find smaller radii
        for r in report.results:
            if r.min_feasible_radius is not None:
                assert r.min_feasible_radius > 0

    def test_min_radii_list(self) -> None:
        report = run_monte_carlo(
            _all_rotational_constraints(),
            n_trials=20,
            seed=42,
        )
        radii = report.min_radii
        assert len(radii) > 0
        assert all(r > 0 for r in radii)
