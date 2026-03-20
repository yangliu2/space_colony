"""Coriolis effect constraint — lateral acceleration during movement."""

from __future__ import annotations

from habitat_constraints.core.parameters import (
    EARTH_G,
    ConstraintResult,
    HabitatParameters,
    HumanAssumptions,
    ParameterBound,
)


class CoriolisConstraint:
    """Coriolis acceleration felt by a person moving in the rotating frame.

    a_cor = 2 * omega * v_rel  (perpendicular to motion)

    Expressed as a fraction of effective gravity, the ratio is:
        a_cor / g_eff = 2 * v_rel / (omega * r) = 2 * v_rel / v_rim

    At high rotation rates (small radii), the Coriolis force becomes
    a significant fraction of gravity, causing disorientation when
    walking, running, or moving radially (climbing stairs, elevators).

    The constraint checks that the ratio stays below the assumed
    maximum for *running* speed (worst-case daily activity).
    """

    @property
    def name(self) -> str:
        return "coriolis"

    @property
    def description(self) -> str:
        return "Coriolis lateral acceleration during movement"

    def evaluate(
        self,
        params: HabitatParameters,
        assumptions: HumanAssumptions,
    ) -> ConstraintResult:
        omega = params.angular_velocity_rad_s
        g_eff = params.gravity_g * EARTH_G

        walk_cor = 2.0 * omega * assumptions.walking_speed_m_s
        run_cor = 2.0 * omega * assumptions.running_speed_m_s

        walk_ratio = walk_cor / g_eff
        run_ratio = run_cor / g_eff

        # Feasibility checked against running (worst case)
        feasible = run_ratio <= assumptions.max_coriolis_ratio

        bounds = self.compute_bounds(assumptions)
        return ConstraintResult(
            constraint_name=self.name,
            feasible=feasible,
            bounds=bounds,
            details={
                "coriolis_walking_m_s2": walk_cor,
                "coriolis_running_m_s2": run_cor,
                "coriolis_to_gravity_walking": walk_ratio,
                "coriolis_to_gravity_running": run_ratio,
                "max_coriolis_ratio": assumptions.max_coriolis_ratio,
            },
        )

    def compute_bounds(
        self,
        assumptions: HumanAssumptions,
    ) -> list[ParameterBound]:
        # From a_cor/g_eff <= max_ratio and g_eff = omega^2 * r:
        #   2*v*omega / (omega^2 * r) <= max_ratio
        #   2*v / (omega * r) <= max_ratio
        #   But omega * r = v_rim, so 2*v / v_rim <= max_ratio
        #   v_rim >= 2*v / max_ratio
        #
        # For 1g: v_rim = omega*r, omega = sqrt(g/r), so v_rim = sqrt(g*r)
        #   sqrt(g*r) >= 2*v / max_ratio
        #   r >= (2*v / max_ratio)^2 / g
        v = assumptions.running_speed_m_s
        max_ratio = assumptions.max_coriolis_ratio
        r_min_1g = (2.0 * v / max_ratio) ** 2 / EARTH_G

        return [
            ParameterBound(
                parameter_name="radius_m",
                lower=r_min_1g,
                constraint_name=self.name,
                description=(
                    f"r >= {r_min_1g:.1f} m for Coriolis/g <= "
                    f"{max_ratio} at 1g (running at "
                    f"{assumptions.running_speed_m_s} m/s)"
                ),
            ),
        ]
