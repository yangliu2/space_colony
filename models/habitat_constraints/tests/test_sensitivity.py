"""Tests for the sensitivity analysis module."""

from __future__ import annotations

from habitat_constraints.analysis.sensitivity import (
    run_sensitivity,
    PERTURBABLE_PARAMS,
)
from habitat_constraints.constraints.vestibular import VestibularConstraint
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


def _all_constraints() -> list:
    return [
        VestibularConstraint(),
        GravityLevelConstraint(),
        GravityGradientConstraint(),
        CoriolisConstraint(),
        CrossCouplingConstraint(),
        RimSpeedConstraint(),
    ]


class TestSensitivityAnalysis:
    """Verify sensitivity analysis produces valid results."""

    def test_baseline_has_result(self) -> None:
        report = run_sensitivity(_all_constraints())
        assert report.baseline_min_radius is not None
        assert report.baseline_min_radius > 0

    def test_all_params_perturbed(self) -> None:
        report = run_sensitivity(_all_constraints())
        # 2 results per param (low + high)
        assert len(report.results) == len(PERTURBABLE_PARAMS) * 2

    def test_tornado_sorted_by_spread(self) -> None:
        report = run_sensitivity(_all_constraints())
        spreads = [t.spread for t in report.tornado]
        for i in range(len(spreads) - 1):
            assert spreads[i] >= spreads[i + 1]

    def test_cross_coupling_is_most_sensitive(self) -> None:
        report = run_sensitivity(_all_constraints())
        # With all 6 constraints, cross-coupling dominates minimum radius
        top_3 = [t.parameter_name for t in report.tornado[:3]]
        assert "max_cross_coupling_deg_s2" in top_3 or "head_turn_rate_deg_s" in top_3

    def test_custom_perturbation(self) -> None:
        report = run_sensitivity(
            _all_constraints(),
            perturbation_pct=50.0,
            parameters=["max_comfortable_rpm"],
        )
        assert len(report.results) == 2
        assert report.perturbation_pct == 50.0

    def test_subset_params(self) -> None:
        subset = ["max_comfortable_rpm", "max_coriolis_ratio"]
        report = run_sensitivity(
            _all_constraints(),
            parameters=subset,
        )
        assert len(report.tornado) == 2
        names = {t.parameter_name for t in report.tornado}
        assert names == set(subset)
