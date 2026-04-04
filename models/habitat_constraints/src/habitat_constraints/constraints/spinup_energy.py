"""Spin-up energy constraint for rotating cylinder habitats.

The habitat must be spun from rest to operating angular velocity ω.
The rotational kinetic energy E = ½Iω² must be supplied by external
power systems.  This constraint checks that spin-up can complete
within an acceptable time given available power.

Mass components contributing to moment of inertia:
  Hull barrel:   I = ρ_hull · 2πrL · t · r²        (thin shell)
  Endcaps:       I = ½ · ρ_hull · 2πr²·t · r²      (solid disks)
  Shielding:     barrel at r², caps as ½r²
  Atmosphere:    I = ½ · ρ_air · πr²L · r²          (solid cylinder)

See plans/constraint_spinup_energy.md for full derivation.
"""

from __future__ import annotations

import math

from habitat_constraints.core.parameters import (
    ConstraintResult,
    HabitatParameters,
    HumanAssumptions,
    ParameterBound,
)

# Air gas constant and assumed temperature for density calculation
R_SPECIFIC_AIR = 287.0  # J/(kg·K)
T_AIR = 293.0  # K (20°C)


def _compute_spinup(
    params: HabitatParameters,
    assumptions: HumanAssumptions,
) -> dict[str, float]:
    """Compute spin-up energy and time from habitat parameters."""
    r = params.radius_m
    L = params.length_m
    t = params.wall_thickness_m
    rho_hull = params.hull_density_kg_m3
    omega = params.angular_velocity_rad_s
    P_pa = params.internal_pressure_kpa * 1000.0  # kPa → Pa
    sigma_shield = params.shielding_areal_density_kg_m2

    # --- Mass components ---
    # Hull barrel (thin cylindrical shell)
    m_hull_barrel = rho_hull * 2.0 * math.pi * r * L * t
    # Endcaps (two solid disks of thickness t)
    m_endcaps = rho_hull * 2.0 * math.pi * r**2 * t
    # Shielding on barrel
    m_shield_barrel = sigma_shield * 2.0 * math.pi * r * L
    # Shielding on endcaps
    m_shield_caps = sigma_shield * 2.0 * math.pi * r**2
    # Atmosphere (ideal gas)
    rho_air = P_pa / (R_SPECIFIC_AIR * T_AIR)
    m_atm = rho_air * math.pi * r**2 * L

    total_mass = m_hull_barrel + m_endcaps + m_shield_barrel + m_shield_caps + m_atm

    # --- Moment of inertia about spin axis ---
    # Barrel components: all mass at radius r → I = mr²
    I_barrel = (m_hull_barrel + m_shield_barrel) * r**2
    # Cap/atmosphere components: disk/cylinder → I = ½mr²
    I_disk = 0.5 * (m_endcaps + m_shield_caps + m_atm) * r**2
    I_total = I_barrel + I_disk

    # --- Energy and time ---
    E_rot = 0.5 * I_total * omega**2
    power_w = assumptions.available_spinup_power_w
    spinup_time_s = E_rot / power_w if power_w > 0 else float("inf")

    return {
        "total_rotating_mass_kg": total_mass,
        "moment_of_inertia_kg_m2": I_total,
        "kinetic_energy_j": E_rot,
        "spinup_time_s": spinup_time_s,
        "spinup_time_days": spinup_time_s / 86400.0,
        "power_w": power_w,
        "max_spinup_time_days": (assumptions.max_spinup_time_years * 365.25),
    }


class SpinUpEnergyConstraint:
    """Spin-up time must be within acceptable limit."""

    @property
    def name(self) -> str:
        return "spinup_energy"

    @property
    def description(self) -> str:
        return (
            "Spin-up energy: time to reach operating rotation "
            "must be within power/time budget"
        )

    def evaluate(
        self,
        params: HabitatParameters,
        assumptions: HumanAssumptions,
    ) -> ConstraintResult:
        # Skip if length not specified (can't compute mass)
        if params.length_m <= 0:
            return ConstraintResult(
                constraint_name=self.name,
                feasible=True,
                bounds=self.compute_bounds(assumptions),
                details={
                    "total_rotating_mass_kg": 0.0,
                    "moment_of_inertia_kg_m2": 0.0,
                    "kinetic_energy_j": 0.0,
                    "spinup_time_s": 0.0,
                    "spinup_time_days": 0.0,
                    "power_w": assumptions.available_spinup_power_w,
                    "max_spinup_time_days": (assumptions.max_spinup_time_years * 365.25),
                },
            )

        data = _compute_spinup(params, assumptions)
        max_time_s = assumptions.max_spinup_time_years * 365.25 * 86400.0
        feasible = data["spinup_time_s"] <= max_time_s

        # Round for display
        details = {
            "total_rotating_mass_kg": round(data["total_rotating_mass_kg"], 0),
            "moment_of_inertia_kg_m2": data["moment_of_inertia_kg_m2"],
            "kinetic_energy_j": data["kinetic_energy_j"],
            "spinup_time_s": round(data["spinup_time_s"], 1),
            "spinup_time_days": round(data["spinup_time_days"], 2),
            "power_w": data["power_w"],
            "max_spinup_time_days": round(data["max_spinup_time_days"], 1),
        }

        return ConstraintResult(
            constraint_name=self.name,
            feasible=feasible,
            bounds=self.compute_bounds(assumptions),
            details=details,
        )

    def compute_bounds(
        self,
        assumptions: HumanAssumptions,
    ) -> list[ParameterBound]:
        days = assumptions.max_spinup_time_years * 365.25
        power_gw = assumptions.available_spinup_power_w / 1e9
        return [
            ParameterBound(
                parameter_name="radius_m",
                upper=None,
                constraint_name=self.name,
                description=(f"Spin-up ≤ {days:.0f} days " f"at {power_gw:.0f} GW"),
            ),
        ]
