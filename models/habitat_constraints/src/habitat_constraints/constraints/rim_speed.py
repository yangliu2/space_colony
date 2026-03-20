"""Structural rim speed constraint — tangential velocity limit."""

from __future__ import annotations

from habitat_constraints.core.parameters import (
    EARTH_G,
    ConstraintResult,
    HabitatParameters,
    HumanAssumptions,
    ParameterBound,
)


class RimSpeedConstraint:
    """Tangential rim speed must stay within structural limits.

    The hoop stress in a rotating cylinder is proportional to v_rim^2:
        sigma = rho * v_rim^2

    For steel (rho ~ 7800 kg/m³), the speed limit before yield is
    roughly 300-400 m/s. For carbon fiber composites, it can exceed
    600 m/s. This constraint imposes an upper bound on rim speed,
    which translates to a joint bound on radius and angular velocity.

    Additionally, higher rim speeds create aerodynamic drag on the
    internal atmosphere and increase the energy required for spin-up.
    """

    @property
    def name(self) -> str:
        return "rim_speed"

    @property
    def description(self) -> str:
        return "Structural/aerodynamic limit on tangential rim speed"

    def evaluate(
        self,
        params: HabitatParameters,
        assumptions: HumanAssumptions,
    ) -> ConstraintResult:
        v_rim = params.rim_speed_m_s
        v_max = assumptions.max_rim_speed_m_s
        feasible = v_rim <= v_max
        margin_pct = ((v_max - v_rim) / v_max) * 100.0

        bounds = self.compute_bounds(assumptions)
        return ConstraintResult(
            constraint_name=self.name,
            feasible=feasible,
            bounds=bounds,
            details={
                "rim_speed_m_s": v_rim,
                "max_rim_speed_m_s": v_max,
                "margin_pct": margin_pct,
                "rim_speed_km_h": v_rim * 3.6,
            },
        )

    def compute_bounds(
        self,
        assumptions: HumanAssumptions,
    ) -> list[ParameterBound]:
        # v_rim = omega * r <= v_max
        # For 1g: omega = sqrt(g/r), v_rim = sqrt(g*r)
        #   sqrt(g*r) <= v_max  =>  r <= v_max^2 / g
        v_max = assumptions.max_rim_speed_m_s
        r_max_1g = v_max**2 / EARTH_G

        return [
            ParameterBound(
                parameter_name="rim_speed_m_s",
                upper=v_max,
                constraint_name=self.name,
                description=(f"v_rim <= {v_max:.0f} m/s " f"({v_max * 3.6:.0f} km/h)"),
            ),
            ParameterBound(
                parameter_name="radius_m",
                upper=r_max_1g,
                constraint_name=self.name,
                description=(
                    f"r <= {r_max_1g:.0f} m for 1g at " f"v_rim <= {v_max:.0f} m/s"
                ),
            ),
        ]
