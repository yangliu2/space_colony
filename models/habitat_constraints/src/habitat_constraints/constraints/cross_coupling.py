"""Cross-coupled rotation constraint — head turn nausea in rotating frame."""

from __future__ import annotations

import math

from habitat_constraints.core.parameters import (
    EARTH_G,
    ConstraintResult,
    HabitatParameters,
    HumanAssumptions,
    ParameterBound,
)


class CrossCouplingConstraint:
    """Cross-coupled (Coriolis) angular acceleration from head turns.

    When a person turns their head about one axis while the habitat
    rotates about another, they experience a cross-coupled angular
    acceleration that stimulates the semicircular canals in an
    unexpected direction. This causes motion sickness (canal
    sickness / mal de débarquement).

    The cross-coupled angular acceleration magnitude is:
        alpha_cc = omega_habitat * omega_head * sin(theta)

    where theta is the angle between the two rotation axes. Worst case
    is theta=90° (sin=1), giving:
        alpha_cc = omega_habitat * omega_head

    Expressed in deg/s²:
        alpha_cc_deg = (omega_hab_rad/s) * (head_turn_rate_deg/s) * (180/pi)
        But more simply: both in rad/s then convert product.

    Literature (Lackner & DiZio, 2005; Reason & Brand, 1975) suggests
    that cross-coupled stimulation above ~3 deg/s² reliably produces
    nausea in unadapted individuals, with adaptation possible up to
    about 6 deg/s² over days to weeks.
    """

    @property
    def name(self) -> str:
        return "cross_coupling"

    @property
    def description(self) -> str:
        return (
            "Cross-coupled angular acceleration from "
            "head turns during habitat rotation"
        )

    def evaluate(
        self,
        params: HabitatParameters,
        assumptions: HumanAssumptions,
    ) -> ConstraintResult:
        omega_hab = params.angular_velocity_rad_s
        omega_head_rad = math.radians(assumptions.head_turn_rate_deg_s)

        # Cross-coupled angular acceleration (worst case: orthogonal axes)
        alpha_cc_rad = omega_hab * omega_head_rad
        alpha_cc_deg = math.degrees(alpha_cc_rad)

        max_cc = assumptions.max_cross_coupling_deg_s2
        feasible = alpha_cc_deg <= max_cc

        bounds = self.compute_bounds(assumptions)
        return ConstraintResult(
            constraint_name=self.name,
            feasible=feasible,
            bounds=bounds,
            details={
                "cross_coupled_deg_s2": alpha_cc_deg,
                "max_cross_coupled_deg_s2": max_cc,
                "margin_deg_s2": max_cc - alpha_cc_deg,
                "habitat_rpm": params.rpm,
                "head_turn_rate_deg_s": assumptions.head_turn_rate_deg_s,
            },
        )

    def compute_bounds(
        self,
        assumptions: HumanAssumptions,
    ) -> list[ParameterBound]:
        # alpha_cc = omega_hab * omega_head (both in rad/s), then
        # convert to deg/s²:
        #   degrees(omega_hab * radians(head_rate_deg)) <= max_cc_deg
        #   omega_hab <= radians(max_cc_deg) / radians(head_rate_deg)
        #   omega_hab <= max_cc_deg / head_rate_deg  (ratio of deg values)
        omega_head_rad = math.radians(assumptions.head_turn_rate_deg_s)
        max_cc_rad = math.radians(assumptions.max_cross_coupling_deg_s2)
        omega_max = max_cc_rad / omega_head_rad

        # For 1g: r_min = g / omega_max^2
        r_min_1g = EARTH_G / (omega_max**2)

        return [
            ParameterBound(
                parameter_name="angular_velocity_rad_s",
                upper=omega_max,
                constraint_name=self.name,
                description=(
                    f"omega <= {omega_max:.4f} rad/s for "
                    f"cross-coupling <= "
                    f"{assumptions.max_cross_coupling_deg_s2} deg/s²"
                ),
            ),
            ParameterBound(
                parameter_name="radius_m",
                lower=r_min_1g,
                constraint_name=self.name,
                description=(
                    f"r >= {r_min_1g:.1f} m for 1g at max " f"cross-coupling tolerance"
                ),
            ),
        ]
