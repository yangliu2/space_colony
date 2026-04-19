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
    agriculture_area_m2: float = Field(
        default=0.0,
        ge=0,
        description=(
            "Dedicated agriculture area (m²). " "0 = not specified; constraint skipped."
        ),
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
        agriculture_area_m2: float = 0.0,
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
            agriculture_area_m2=agriculture_area_m2,
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

    # --- Phase 6: Agriculture constraint ---
    min_agriculture_area_per_person_m2: float = Field(
        default=200.0,
        gt=0,
        description=(
            "Minimum agriculture area per person (m²/person) for a "
            "plant-based diet. NASA BVAD: 200 m²/person for single-tier "
            "hydroponics (Hanford 2004). Range: 20 (vertical farm) to "
            "2000 (open field). Multiplied by diet_land_multiplier."
        ),
    )
    diet_land_multiplier: float = Field(
        default=1.0,
        ge=1.0,
        description=(
            "Multiplier on min_agriculture_area_per_person_m2 to account "
            "for animal protein in the diet. "
            "1.0 = plant-only (NASA CELSS baseline); "
            "1.1 = insects; 1.4 = aquaculture; "
            "3–4 = poultry/eggs; 5–7 = pork; 15–20 = beef. "
            "(Poore and Nemecek 2018)"
        ),
    )

    # --- Phase 6: Thermal management constraint ---
    solar_irradiance_w_m2: float = Field(
        default=1361.0,
        gt=0,
        description=(
            "Solar irradiance at the habitat location (W/m²). "
            "1,361 W/m² at 1 AU (L5). (Kopp and Lean 2011)"
        ),
    )
    window_fraction: float = Field(
        default=0.5,
        gt=0,
        lt=1.0,
        description=(
            "Fraction of barrel area occupied by windows. "
            "O'Neill Island Three: 3 window + 3 land strips → 0.5."
        ),
    )
    window_solar_transmittance: float = Field(
        default=0.3,
        gt=0,
        le=1.0,
        description=(
            "Net fraction of incident solar energy transmitted into the "
            "habitat through mirrors + windows. 0.3 = well-managed mirrors "
            "reflecting ~70% back to space. Range: 0.1 (near-closed) to "
            "0.8 (fully open)."
        ),
    )
    waste_heat_per_person_w: float = Field(
        default=350.0,
        gt=0,
        description=(
            "Internal waste heat per person (W/person): metabolic + "
            "lighting + equipment. NASA BVAD: ~350 W/person (Hanford 2004)."
        ),
    )
    radiator_temperature_k: float = Field(
        default=320.0,
        gt=0,
        description=(
            "Operating temperature of radiator panels (K). "
            "Higher T → smaller required area (scales as T⁴). "
            "Typical range: 280–400 K."
        ),
    )
    radiator_emissivity: float = Field(
        default=0.9,
        gt=0,
        le=1.0,
        description=(
            "Emissivity of radiator surface. " "Coated aluminium / Kapton: 0.85–0.95."
        ),
    )

    # --- Phase 6: Structural constraints ---
    max_length_coefficient: float = Field(
        default=75.22,
        gt=0,
        description=(
            "Coefficient C in L_max = C * r^(3/4). "
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
        default=True,
        description=(
            "Whether the habitat uses counter-rotating pairs "
            "(O'Neill design). True reflects the baseline design: "
            "two counter-rotating cylinders cancel net angular momentum, "
            "relaxing rotational stability from L/r < 1.3 to L/r < 10. "
            "The 3D model already shows two cylinders — this default "
            "matches that geometry."
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

    # --- Phase 6: Spin-up energy ---
    available_spinup_power_w: float = Field(
        default=1e10,
        gt=0,
        description=(
            "Available power for spin-up (W). "
            "Default: 10 GW (~37 km² solar at L5, 20% eff)."
        ),
    )
    max_spinup_time_years: float = Field(
        default=1.0,
        gt=0,
        description=("Maximum acceptable spin-up duration (years). " "Default: 1 year."),
    )

    # --- Phase 6: Energy budget ---
    power_per_person_w: float = Field(
        default=5000.0,
        gt=0,
        description=(
            "Electrical power demand per person (W/person). "
            "Covers life support, LED agriculture, lighting, and equipment. "
            "Default: 5,000 W/person (residential + light-industrial colony). "
            "ISS: ~12,000 W/person (research station, IEA 2023)."
        ),
    )
    solar_panel_efficiency: float = Field(
        default=0.20,
        gt=0,
        le=1.0,
        description=(
            "Photovoltaic panel efficiency (fraction). "
            "Current commercial silicon: ~0.20; high-efficiency GaAs: ~0.29. "
            "Default: 0.20 (NREL 2024)."
        ),
    )

    # --- Phase 6: Water recycling ---
    water_per_person_day_liters: float = Field(
        default=20.0,
        gt=0,
        description=(
            "Domestic water demand per person per day (L/day): drinking, "
            "cooking, hygiene, laundry. NASA BVAD minimum: ~22 L/day "
            "(Hanford 2004). Does not include agricultural water "
            "(separate closed loop)."
        ),
    )
    water_recycling_efficiency: float = Field(
        default=0.98,
        gt=0,
        le=1.0,
        description=(
            "Fraction of water recovered and reused per cycle. "
            "ISS pre-BPA (~2009): ~0.93 (Carter et al. 2009). "
            "ISS with BPA (2024): 0.98 (Gatens et al. 2024). "
            "0.98 is NASA's stated minimum for Mars / permanent missions. "
            "Note: effective whole-habitat efficiency may be lower due to "
            "disposal paths (wipes, hygiene waste) not captured by ECLSS."
        ),
    )
    min_water_recycling_efficiency: float = Field(
        default=0.98,
        gt=0,
        le=1.0,
        description=(
            "Minimum recycling efficiency for long-term self-sufficiency "
            "without routine water resupply."
        ),
    )

    # --- Phase 6: Micrometeorite hull penetration ---
    meteoroid_penetrating_flux_m2_yr: float = Field(
        default=5e-8,
        gt=0,
        description=(
            "Effective flux of meteoroids that penetrate the habitat shield "
            "(impacts m⁻² yr⁻¹). ISS basic Whipple: ~6e-5; purpose-built "
            "multi-layer bumper: ~1e-7; regolith-covered surface: ~1e-10. "
            "(Grün et al. 1985; Christiansen et al. 2009)"
        ),
    )
    habitat_lifespan_years: float = Field(
        default=100.0,
        gt=0,
        description="Design lifespan of the habitat (years).",
    )
    max_annual_perforations: float = Field(
        default=1.0,
        gt=0,
        description=(
            "Maximum acceptable hull penetrations per year. "
            "1.0 = one manageable repair event per year."
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
