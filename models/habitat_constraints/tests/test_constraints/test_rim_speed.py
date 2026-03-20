"""Tests for the structural rim speed constraint."""

from habitat_constraints.core.parameters import (
    HabitatParameters,
    HumanAssumptions,
)
from habitat_constraints.constraints.rim_speed import RimSpeedConstraint


class TestRimSpeedConstraint:
    """Verify rim speed constraint evaluation and bounds."""

    def test_small_habitat_feasible(
        self,
        small_habitat_params: HabitatParameters,
        default_assumptions: HumanAssumptions,
    ) -> None:
        c = RimSpeedConstraint()
        result = c.evaluate(small_habitat_params, default_assumptions)
        assert result.feasible
        # r=100m at 1g => v_rim ~31 m/s, well under 300 m/s
        assert result.details["rim_speed_m_s"] < 50.0

    def test_oneill_feasible(
        self,
        oneill_params: HabitatParameters,
        default_assumptions: HumanAssumptions,
    ) -> None:
        c = RimSpeedConstraint()
        result = c.evaluate(oneill_params, default_assumptions)
        assert result.feasible
        # r=3200m at 1g => v_rim ~177 m/s, under 300 m/s
        assert result.details["rim_speed_m_s"] < 200.0

    def test_huge_habitat_infeasible(self) -> None:
        c = RimSpeedConstraint()
        # r=10000m at 1g => v_rim ~313 m/s, exceeds 300 m/s
        params = HabitatParameters.from_radius_and_gravity(10000.0)
        assumptions = HumanAssumptions(max_rim_speed_m_s=300.0)
        result = c.evaluate(params, assumptions)
        assert not result.feasible
        assert result.details["rim_speed_m_s"] > 300.0

    def test_margin_reported(
        self,
        oneill_params: HabitatParameters,
        default_assumptions: HumanAssumptions,
    ) -> None:
        c = RimSpeedConstraint()
        result = c.evaluate(oneill_params, default_assumptions)
        assert result.details["margin_pct"] > 0

    def test_bounds_radius_upper(
        self,
        default_assumptions: HumanAssumptions,
    ) -> None:
        c = RimSpeedConstraint()
        bounds = c.compute_bounds(default_assumptions)
        r_bounds = [b for b in bounds if b.parameter_name == "radius_m"]
        assert len(r_bounds) == 1
        assert r_bounds[0].upper is not None
        # At 300 m/s: r_max = 300^2 / 9.80665 ~ 9177m
        assert 9000 < r_bounds[0].upper < 10000

    def test_km_h_conversion(
        self,
        oneill_params: HabitatParameters,
        default_assumptions: HumanAssumptions,
    ) -> None:
        c = RimSpeedConstraint()
        result = c.evaluate(oneill_params, default_assumptions)
        expected_km_h = result.details["rim_speed_m_s"] * 3.6
        assert abs(result.details["rim_speed_km_h"] - expected_km_h) < 0.1
