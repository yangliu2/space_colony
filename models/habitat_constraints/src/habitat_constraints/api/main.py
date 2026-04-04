"""FastAPI app — exposes the constraint solver over HTTP."""

from __future__ import annotations

import math
from typing import Any

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from habitat_constraints.constraints.atmosphere import AtmosphereConstraint
from habitat_constraints.constraints.cylinder_length import (
    CylinderLengthConstraint,
)
from habitat_constraints.constraints.rotational_stability import (
    RotationalStabilityConstraint,
)
from habitat_constraints.constraints.spinup_energy import (
    SpinUpEnergyConstraint,
)
from habitat_constraints.constraints.hoop_stress import (
    HoopStressConstraint,
)
from habitat_constraints.constraints.coriolis import CoriolisConstraint
from habitat_constraints.constraints.cross_coupling import (
    CrossCouplingConstraint,
)
from habitat_constraints.constraints.gravity_gradient import (
    GravityGradientConstraint,
)
from habitat_constraints.constraints.gravity_level import (
    GravityLevelConstraint,
)
from habitat_constraints.constraints.population import PopulationConstraint
from habitat_constraints.constraints.radiation import RadiationConstraint
from habitat_constraints.constraints.rim_speed import RimSpeedConstraint
from habitat_constraints.constraints.vestibular import VestibularConstraint
from habitat_constraints.core.parameters import (
    EARTH_G,
    HabitatParameters,
    HumanAssumptions,
)
from habitat_constraints.core.solver import FeasibleRegionSolver

app = FastAPI(title="Habitat Constraints API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

ALL_CONSTRAINTS = [
    VestibularConstraint(),
    GravityLevelConstraint(),
    GravityGradientConstraint(),
    CoriolisConstraint(),
    CrossCouplingConstraint(),
    RimSpeedConstraint(),
    AtmosphereConstraint(),
    RadiationConstraint(),
    PopulationConstraint(),
    CylinderLengthConstraint(),
    HoopStressConstraint(),
    RotationalStabilityConstraint(),
    SpinUpEnergyConstraint(),
]


# ── Request / Response schemas ───────────────────────────────────


class EvaluateRequest(BaseModel):
    """Evaluate all constraints at a single design point."""

    radius_m: float = Field(gt=0)
    target_gravity_g: float = Field(default=1.0, gt=0)
    length_m: float = Field(default=1276.0, ge=0)
    population: int = Field(default=8000, ge=0)
    internal_pressure_kpa: float = Field(default=101.3, gt=0)
    o2_fraction: float = Field(default=0.21, gt=0, le=1.0)
    shielding_areal_density_kg_m2: float = Field(default=4500.0, ge=0)
    wall_thickness_m: float = Field(default=0.2, gt=0)
    # Human assumptions overrides
    max_comfortable_rpm: float = Field(default=2.0, gt=0)
    max_cross_coupling_deg_s2: float = Field(default=6.0, gt=0)
    head_turn_rate_deg_s: float = Field(default=60.0, gt=0)
    max_coriolis_ratio: float = Field(default=0.25, gt=0)
    max_rim_speed_m_s: float = Field(default=300.0, gt=0)
    max_gravity_gradient_pct: float = Field(default=1.0, gt=0)
    min_gravity_g: float = Field(default=0.3, gt=0)
    max_gravity_g: float = Field(default=1.0, gt=0)


class ConstraintStatus(BaseModel):
    name: str
    feasible: bool
    details: dict[str, float]


class EvaluateResponse(BaseModel):
    all_feasible: bool
    radius_m: float
    omega_rad_s: float
    rpm: float
    rim_speed_m_s: float
    gravity_g: float
    constraints: list[ConstraintStatus]


class SweepRequest(BaseModel):
    r_min: float = Field(default=100.0, gt=0)
    r_max: float = Field(default=15000.0, gt=0)
    n_points: int = Field(default=200, gt=1, le=1000)
    target_gravity_g: float = Field(default=1.0, gt=0)
    # Design parameters applied at each sweep point
    length_m: float = Field(default=1276.0, ge=0)
    population: int = Field(default=8000, ge=0)
    internal_pressure_kpa: float = Field(default=101.3, gt=0)
    o2_fraction: float = Field(default=0.21, gt=0, le=1.0)
    shielding_areal_density_kg_m2: float = Field(default=4500.0, ge=0)
    wall_thickness_m: float = Field(default=0.2, gt=0)
    # Human assumptions overrides
    max_comfortable_rpm: float = Field(default=2.0, gt=0)
    max_cross_coupling_deg_s2: float = Field(default=6.0, gt=0)
    head_turn_rate_deg_s: float = Field(default=60.0, gt=0)
    max_coriolis_ratio: float = Field(default=0.25, gt=0)
    max_rim_speed_m_s: float = Field(default=300.0, gt=0)
    max_gravity_gradient_pct: float = Field(default=1.0, gt=0)
    min_gravity_g: float = Field(default=0.3, gt=0)
    max_gravity_g: float = Field(default=1.0, gt=0)


class SweepPoint(BaseModel):
    radius_m: float
    rpm: float
    rim_speed_m_s: float
    feasible: bool
    binding_constraints: list[str]


class SweepResponse(BaseModel):
    points: list[SweepPoint]
    feasible_min_radius: float | None
    feasible_max_radius: float | None


class ParamRange(BaseModel):
    min: float | None
    max: float | None


class FeasibleRangesResponse(BaseModel):
    radius_m: ParamRange
    wall_thickness_m: ParamRange
    length_m: ParamRange
    internal_pressure_kpa: ParamRange


# ── Helpers ──────────────────────────────────────────────────────


def _build_assumptions(req: EvaluateRequest | SweepRequest) -> HumanAssumptions:
    return HumanAssumptions(
        max_comfortable_rpm=req.max_comfortable_rpm,
        max_cross_coupling_deg_s2=req.max_cross_coupling_deg_s2,
        head_turn_rate_deg_s=req.head_turn_rate_deg_s,
        max_coriolis_ratio=req.max_coriolis_ratio,
        max_rim_speed_m_s=req.max_rim_speed_m_s,
        max_gravity_gradient_pct=req.max_gravity_gradient_pct,
        min_gravity_g=req.min_gravity_g,
        max_gravity_g=req.max_gravity_g,
    )


# ── Endpoints ────────────────────────────────────────────────────


@app.post("/api/evaluate", response_model=EvaluateResponse)
def evaluate(req: EvaluateRequest) -> Any:
    """Evaluate all constraints at a single design point."""
    omega = math.sqrt(req.target_gravity_g * EARTH_G / req.radius_m)
    params = HabitatParameters(
        radius_m=req.radius_m,
        angular_velocity_rad_s=omega,
        length_m=req.length_m,
        population=req.population,
        internal_pressure_kpa=req.internal_pressure_kpa,
        o2_fraction=req.o2_fraction,
        shielding_areal_density_kg_m2=req.shielding_areal_density_kg_m2,
        wall_thickness_m=req.wall_thickness_m,
    )
    assumptions = _build_assumptions(req)
    solver = FeasibleRegionSolver(ALL_CONSTRAINTS, assumptions)
    results = solver.evaluate_point(params)

    statuses = [
        ConstraintStatus(
            name=r.constraint_name,
            feasible=r.feasible,
            details=r.details,
        )
        for r in results
    ]

    return EvaluateResponse(
        all_feasible=all(r.feasible for r in results),
        radius_m=params.radius_m,
        omega_rad_s=params.angular_velocity_rad_s,
        rpm=params.rpm,
        rim_speed_m_s=params.rim_speed_m_s,
        gravity_g=params.gravity_g,
        constraints=statuses,
    )


@app.post("/api/sweep", response_model=SweepResponse)
def sweep(req: SweepRequest) -> Any:
    """Sweep radius range and return feasibility at each point."""
    assumptions = _build_assumptions(req)
    solver = FeasibleRegionSolver(ALL_CONSTRAINTS, assumptions)
    raw = solver.sweep_radius(
        req.r_min,
        req.r_max,
        req.n_points,
        req.target_gravity_g,
        extra_params={
            "length_m": req.length_m,
            "population": req.population,
            "internal_pressure_kpa": req.internal_pressure_kpa,
            "o2_fraction": req.o2_fraction,
            "shielding_areal_density_kg_m2": req.shielding_areal_density_kg_m2,
            "wall_thickness_m": req.wall_thickness_m,
        },
    )

    points: list[SweepPoint] = []
    feas_min: float | None = None
    feas_max: float | None = None

    for sp in raw:
        binding = [cr.constraint_name for cr in sp.constraint_results if not cr.feasible]
        points.append(
            SweepPoint(
                radius_m=sp.radius_m,
                rpm=sp.rpm,
                rim_speed_m_s=sp.rim_speed_m_s,
                feasible=sp.all_feasible,
                binding_constraints=binding,
            )
        )
        if sp.all_feasible:
            if feas_min is None:
                feas_min = sp.radius_m
            feas_max = sp.radius_m

    return SweepResponse(
        points=points,
        feasible_min_radius=feas_min,
        feasible_max_radius=feas_max,
    )


@app.post(
    "/api/feasible_ranges",
    response_model=FeasibleRangesResponse,
)
def feasible_ranges(req: EvaluateRequest) -> Any:
    """Sweep each key design parameter to find its feasible range."""
    assumptions = _build_assumptions(req)
    solver = FeasibleRegionSolver(ALL_CONSTRAINTS, assumptions)

    omega = math.sqrt(req.target_gravity_g * EARTH_G / req.radius_m)
    base: dict[str, Any] = {
        "radius_m": req.radius_m,
        "angular_velocity_rad_s": omega,
        "length_m": req.length_m,
        "population": req.population,
        "internal_pressure_kpa": req.internal_pressure_kpa,
        "o2_fraction": req.o2_fraction,
        "shielding_areal_density_kg_m2": (req.shielding_areal_density_kg_m2),
        "wall_thickness_m": req.wall_thickness_m,
    }

    def _sweep(
        name: str,
        lo: float,
        hi: float,
        n: int = 200,
        recalc_omega: bool = False,
    ) -> ParamRange:
        fmin: float | None = None
        fmax: float | None = None
        for i in range(n):
            v = lo + i * (hi - lo) / max(n - 1, 1)
            kw = dict(base)
            kw[name] = v
            if recalc_omega:
                kw["angular_velocity_rad_s"] = math.sqrt(
                    req.target_gravity_g * EARTH_G / v
                )
            params = HabitatParameters(**kw)
            results = solver.evaluate_point(params)
            if all(r.feasible for r in results):
                if fmin is None:
                    fmin = v
                fmax = v
        return ParamRange(min=fmin, max=fmax)

    return FeasibleRangesResponse(
        radius_m=_sweep("radius_m", 50, 15000, recalc_omega=True),
        wall_thickness_m=_sweep("wall_thickness_m", 0.05, 2.0),
        length_m=_sweep("length_m", 100, 5000),
        internal_pressure_kpa=_sweep("internal_pressure_kpa", 50, 101.3),
    )


@app.get("/api/defaults")
def defaults() -> dict[str, Any]:
    """Return default parameter values for the UI."""
    h = HumanAssumptions()
    return {
        "radius_m": 982.0,
        "target_gravity_g": 1.0,
        "length_m": 1276.0,
        "population": 8000,
        "internal_pressure_kpa": 101.3,
        "o2_fraction": 0.21,
        "shielding_areal_density_kg_m2": 4500.0,
        "max_comfortable_rpm": h.max_comfortable_rpm,
        "max_cross_coupling_deg_s2": h.max_cross_coupling_deg_s2,
        "head_turn_rate_deg_s": h.head_turn_rate_deg_s,
        "max_coriolis_ratio": h.max_coriolis_ratio,
        "max_rim_speed_m_s": h.max_rim_speed_m_s,
        "max_gravity_gradient_pct": h.max_gravity_gradient_pct,
        "min_gravity_g": h.min_gravity_g,
        "max_gravity_g": h.max_gravity_g,
    }
