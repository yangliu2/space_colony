"""Pydantic models for habitat design parameters and constraint results."""

from __future__ import annotations

import math

from pydantic import BaseModel, Field

# Earth standard gravity (m/s^2)
EARTH_G = 9.80665


class HabitatParameters(BaseModel):
    """Primary design variables for a rotating cylinder habitat.

    All values in SI units. Convenience properties provide derived
    quantities and common unit conversions.
    """

    radius_m: float = Field(gt=0, description="Cylinder inner radius (m)")
    angular_velocity_rad_s: float = Field(gt=0, description="Angular velocity (rad/s)")
    length_m: float = Field(
        default=0.0,
        ge=0,
        description="Cylinder length (m). 0 = not specified.",
    )
    population: int = Field(
        default=0,
        ge=0,
        description="Habitat population. 0 = not specified.",
    )
    internal_pressure_kpa: float = Field(
        default=101.3,
        gt=0,
        description="Internal atmospheric pressure (kPa)",
    )
    o2_fraction: float = Field(
        default=0.21,
        gt=0,
        le=1.0,
        description="O2 mole fraction in atmosphere",
    )
    shielding_areal_density_kg_m2: float = Field(
        default=4500.0,
        ge=0,
        description="Radiation shielding areal density (kg/m²)",
    )
    wall_thickness_m: float = Field(
        default=0.2,
        gt=0,
        description="Structural hull wall thickness (m). Default 200mm.",
    )
    hull_density_kg_m3: float = Field(
        default=7900.0,
        gt=0,
        description="Hull material density (kg/m³). Default: steel.",
    )

    @property
    def gravity_g(self) -> float:
        """Effective gravity at the rim, in multiples of Earth g."""
        return (self.angular_velocity_rad_s**2 * self.radius_m) / EARTH_G

    @property
    def rpm(self) -> float:
        """Rotation rate in revolutions per minute."""
        return self.angular_velocity_rad_s * 60.0 / (2.0 * math.pi)

    @property
    def rim_speed_m_s(self) -> float:
        """Tangential speed at the rim (m/s)."""
        return self.angular_velocity_rad_s * self.radius_m

    @property
    def period_s(self) -> float:
        """Rotation period (seconds per revolution)."""
        return 2.0 * math.pi / self.angular_velocity_rad_s

    @property
    def o2_partial_pressure_kpa(self) -> float:
        """Oxygen partial pressure (kPa)."""
        return self.internal_pressure_kpa * self.o2_fraction

    @property
    def barrel_area_m2(self) -> float:
        """Barrel (cylindrical) surface area (m²). 0 if length not set."""
        if self.length_m <= 0:
            return 0.0
        return 2.0 * math.pi * self.radius_m * self.length_m

    @property
    def endcap_area_m2(self) -> float:
        """Combined end-cap area (m²)."""
        return 2.0 * math.pi * self.radius_m**2

    @property
    def total_shell_area_m2(self) -> float:
        """Total outer shell area (barrel + end caps) (m²)."""
        return self.barrel_area_m2 + self.endcap_area_m2

    @property
    def interior_volume_m3(self) -> float:
        """Interior volume (m³). 0 if length not set."""
        if self.length_m <= 0:
            return 0.0
        return math.pi * self.radius_m**2 * self.length_m

    @property
    def volume_per_person_m3(self) -> float:
        """Interior volume per person (m³). 0 if not calculable."""
        if self.population <= 0 or self.interior_volume_m3 <= 0:
            return 0.0
        return self.interior_volume_m3 / self.population

    @staticmethod
    def from_radius_and_gravity(
        radius_m: float,
        target_gravity_g: float = 1.0,
        length_m: float = 0.0,
        population: int = 0,
        internal_pressure_kpa: float = 101.3,
        o2_fraction: float = 0.21,
        shielding_areal_density_kg_m2: float = 4500.0,
        wall_thickness_m: float = 0.2,
        hull_density_kg_m3: float = 7900.0,
    ) -> HabitatParameters:
        """Create parameters for a given radius that achieves target gravity."""
        omega = math.sqrt(target_gravity_g * EARTH_G / radius_m)
        return HabitatParameters(
            radius_m=radius_m,
            angular_velocity_rad_s=omega,
            length_m=length_m,
            population=population,
            internal_pressure_kpa=internal_pressure_kpa,
            o2_fraction=o2_fraction,
            shielding_areal_density_kg_m2=shielding_areal_density_kg_m2,
            wall_thickness_m=wall_thickness_m,
            hull_density_kg_m3=hull_density_kg_m3,
        )


class HumanAssumptions(BaseModel):
    """Assumed biological and comfort constants.

    These are the 'soft' parameters we vary in sensitivity analysis.
    Each field has a sensible default based on literature.
    """

    person_height_m: float = Field(default=1.8, gt=0, description="Standing height (m)")
    walking_speed_m_s: float = Field(
        default=1.4, gt=0, description="Typical walking speed (m/s)"
    )
    running_speed_m_s: float = Field(
        default=3.0, gt=0, description="Typical running speed (m/s)"
    )
    max_comfortable_rpm: float = Field(
        default=2.0, gt=0, description="Vestibular comfort RPM limit"
    )
    min_gravity_g: float = Field(
        default=0.3, gt=0, description="Minimum acceptable gravity (g)"
    )
    max_gravity_g: float = Field(
        default=1.0, gt=0, description="Maximum acceptable gravity (g)"
    )
    max_gravity_gradient_pct: float = Field(
        default=1.0,
        gt=0,
        description="Max head-to-foot gravity gradient (%)",
    )
    max_coriolis_ratio: float = Field(
        default=0.25,
        gt=0,
        description="Max Coriolis-to-gravity acceleration ratio",
    )
    max_cross_coupling_deg_s2: float = Field(
        default=6.0,
        gt=0,
        description=(
            "Max cross-coupled angular acceleration (deg/s^2) "
            "from head turns during rotation. "
            "~3 for unadapted, ~6 for adapted crew."
        ),
    )
    head_turn_rate_deg_s: float = Field(
        default=60.0,
        gt=0,
        description="Typical head turn rate (deg/s)",
    )
    max_rim_speed_m_s: float = Field(
        default=300.0,
        gt=0,
        description=(
            "Max tangential rim speed (m/s) — " "structural and aerodynamic limit"
        ),
    )

    # --- Phase 3: Biological constraints ---
    min_o2_partial_pressure_kpa: float = Field(
        default=16.0,
        gt=0,
        description="Minimum O2 partial pressure (kPa) to avoid hypoxia",
    )
    max_o2_partial_pressure_kpa: float = Field(
        default=50.0,
        gt=0,
        description=("Maximum O2 partial pressure (kPa) " "to avoid pulmonary toxicity"),
    )
    min_shielding_areal_density_kg_m2: float = Field(
        default=4500.0,
        gt=0,
        description=(
            "Minimum radiation shielding areal density (kg/m²). "
            "SP-413: 4500 for <0.5 rem/yr."
        ),
    )
    min_population: int = Field(
        default=98,
        gt=0,
        description=(
            "Minimum viable population for genetic diversity. "
            "98 = bare survival (Marin & Beluffi 2020)."
        ),
    )
    min_volume_per_person_m3: float = Field(
        default=100.0,
        gt=0,
        description=(
            "Minimum habitable volume per person (m³). "
            "NASA: 25 minimum, 100+ for >1 year."
        ),
    )

    # --- Phase 6: Structural constraints ---
    max_length_coefficient: float = Field(
        default=1.33,
        gt=0,
        description=(
            "Coefficient C in L_max = C * r^(5/4). "
            "Calibrated to O'Neill: L=32km at r=3.2km."
        ),
    )
    max_length_to_radius_ratio: float = Field(
        default=1.3,
        gt=0,
        description=(
            "Max L/r for passive rotational stability. "
            "Iz/Ix >= 1.2 requires L < 1.3r for flat caps "
            "(Globus and Arora 2007). Counter-rotating pairs "
            "can exceed this limit."
        ),
    )
    counter_rotating_pair: bool = Field(
        default=False,
        description=(
            "Whether the habitat uses counter-rotating pairs "
            "(O'Neill design). If True, the rotational stability "
            "constraint is relaxed to L/r < 10."
        ),
    )
    yield_strength_mpa: float = Field(
        default=1200.0,
        gt=0,
        description=(
            "Hull material yield strength (MPa). "
            "Default: high-strength structural steel."
        ),
    )
    structural_safety_factor: float = Field(
        default=2.0,
        gt=1.0,
        description=(
            "Structural safety factor (ultimate FoS). "
            "NASA-STD-5001B: 1.4 for spacecraft, "
            "2.0+ recommended for permanent colony."
        ),
    )


class ParameterBound(BaseModel):
    """A bound on a single design parameter produced by a constraint."""

    parameter_name: str
    lower: float | None = None
    upper: float | None = None
    constraint_name: str
    description: str


class ConstraintResult(BaseModel):
    """Output of evaluating one constraint at a specific design point."""

    constraint_name: str
    feasible: bool
    bounds: list[ParameterBound]
    details: dict[str, float] = Field(default_factory=dict)
