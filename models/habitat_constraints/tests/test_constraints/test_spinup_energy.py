"""Tests for spin-up energy constraint."""

from __future__ import annotations

import math

import pytest

from habitat_constraints.constraints.spinup_energy import (
    SpinUpEnergyConstraint,
    _compute_spinup,
)
from habitat_constraints.core.parameters import (
    HabitatParameters,
    HumanAssumptions,
)


@pytest.fixture
def constraint() -> SpinUpEnergyConstraint:
    return SpinUpEnergyConstraint()


@pytest.fixture
def assumptions() -> HumanAssumptions:
    return HumanAssumptions()


class TestSpinUpEnergyConstraint:
    def test_protocol_properties(
        self,
        constraint: SpinUpEnergyConstraint,
    ) -> None:
        assert constraint.name == "spinup_energy"
        assert "spin" in constraint.description.lower()

    def test_reference_design_feasible(
        self,
        constraint: SpinUpEnergyConstraint,
        assumptions: HumanAssumptions,
    ) -> None:
        """r=982m, L=1276m at 10 GW should spin up in hours."""
        params = HabitatParameters.from_radius_and_gravity(982.0, length_m=1276.0)
        result = constraint.evaluate(params, assumptions)
        assert result.feasible
        # Should complete in less than a few days
        assert result.details["spinup_time_days"] < 5.0

    def test_zero_length_passes(
        self,
        constraint: SpinUpEnergyConstraint,
        assumptions: HumanAssumptions,
    ) -> None:
        """L=0 means length not specified — should pass by default."""
        params = HabitatParameters.from_radius_and_gravity(982.0, length_m=0.0)
        result = constraint.evaluate(params, assumptions)
        assert result.feasible
        assert result.details["kinetic_energy_j"] == 0.0

    def test_very_large_habitat_may_exceed_time(
        self,
        constraint: SpinUpEnergyConstraint,
    ) -> None:
        """O'Neill-class at low power should take a long time."""
        low_power = HumanAssumptions(
            available_spinup_power_w=1e9,  # 1 GW
            max_spinup_time_years=0.5,
        )
        params = HabitatParameters.from_radius_and_gravity(3200.0, length_m=32000.0)
        result = constraint.evaluate(params, low_power)
        # At 1 GW, O'Neill needs ~3 years → should fail at 0.5yr
        assert not result.feasible

    def test_energy_scales_linearly_with_radius(
        self,
        assumptions: HumanAssumptions,
    ) -> None:
        """E ≈ ½mgr for barrel-dominated mass at constant g."""
        p1 = HabitatParameters.from_radius_and_gravity(1000.0, length_m=1000.0)
        p2 = HabitatParameters.from_radius_and_gravity(2000.0, length_m=1000.0)
        d1 = _compute_spinup(p1, assumptions)
        d2 = _compute_spinup(p2, assumptions)
        # Barrel mass scales with r, energy with r²·ω²=r·g
        # But endcaps/shield scale with r², pushing ratio above 2
        # At fixed L, endcap terms dominate more at larger r
        ratio = d2["kinetic_energy_j"] / d1["kinetic_energy_j"]
        assert 1.5 < ratio < 8.0

    def test_more_power_reduces_spinup_time(
        self,
        constraint: SpinUpEnergyConstraint,
    ) -> None:
        """Doubling power should halve spin-up time."""
        params = HabitatParameters.from_radius_and_gravity(982.0, length_m=1276.0)
        a1 = HumanAssumptions(available_spinup_power_w=1e10)
        a2 = HumanAssumptions(available_spinup_power_w=2e10)
        r1 = constraint.evaluate(params, a1)
        r2 = constraint.evaluate(params, a2)
        assert r1.details["spinup_time_s"] == pytest.approx(
            2.0 * r2.details["spinup_time_s"], rel=0.01
        )

    def test_details_include_all_fields(
        self,
        constraint: SpinUpEnergyConstraint,
        assumptions: HumanAssumptions,
    ) -> None:
        params = HabitatParameters.from_radius_and_gravity(982.0, length_m=1276.0)
        result = constraint.evaluate(params, assumptions)
        expected_keys = {
            "total_rotating_mass_kg",
            "moment_of_inertia_kg_m2",
            "kinetic_energy_j",
            "spinup_time_s",
            "spinup_time_days",
            "power_w",
            "max_spinup_time_days",
        }
        assert expected_keys <= set(result.details.keys())

    def test_bounds_structure(
        self,
        constraint: SpinUpEnergyConstraint,
        assumptions: HumanAssumptions,
    ) -> None:
        bounds = constraint.compute_bounds(assumptions)
        assert len(bounds) == 1
        assert bounds[0].parameter_name == "radius_m"
        assert bounds[0].constraint_name == "spinup_energy"

    def test_manual_moment_of_inertia(
        self,
        assumptions: HumanAssumptions,
    ) -> None:
        """Verify I_z against hand calculation for simple case."""
        r, L, t = 1000.0, 2000.0, 0.2
        rho = 7900.0
        params = HabitatParameters.from_radius_and_gravity(
            r, length_m=L, wall_thickness_m=t, hull_density_kg_m3=rho
        )
        data = _compute_spinup(params, assumptions)

        # Hull barrel: rho * 2pi*r*L*t
        m_barrel = rho * 2 * math.pi * r * L * t
        # Endcaps: rho * 2*pi*r^2*t
        m_caps = rho * 2 * math.pi * r**2 * t
        # Shield barrel: 4500 * 2*pi*r*L
        m_s_barrel = 4500 * 2 * math.pi * r * L
        # Shield caps: 4500 * 2*pi*r^2
        m_s_caps = 4500 * 2 * math.pi * r**2
        # Atm: rho_air * pi*r^2*L
        rho_air = 101300 / (287.0 * 293.0)
        m_atm = rho_air * math.pi * r**2 * L

        I_expected = (m_barrel + m_s_barrel) * r**2 + 0.5 * (
            m_caps + m_s_caps + m_atm
        ) * r**2

        assert data["moment_of_inertia_kg_m2"] == pytest.approx(I_expected, rel=1e-6)

    def test_half_atmosphere_reduces_energy(
        self,
        constraint: SpinUpEnergyConstraint,
        assumptions: HumanAssumptions,
    ) -> None:
        """Lower internal pressure → less atmospheric mass → less E."""
        p_full = HabitatParameters.from_radius_and_gravity(
            982.0,
            length_m=1276.0,
            internal_pressure_kpa=101.3,
        )
        p_half = HabitatParameters.from_radius_and_gravity(
            982.0,
            length_m=1276.0,
            internal_pressure_kpa=50.0,
        )
        r_full = constraint.evaluate(p_full, assumptions)
        r_half = constraint.evaluate(p_half, assumptions)
        assert r_half.details["kinetic_energy_j"] < r_full.details["kinetic_energy_j"]
