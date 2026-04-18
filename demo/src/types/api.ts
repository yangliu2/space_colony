/** Shared types matching the FastAPI response schemas. */

export interface ConstraintStatus {
  name: string;
  feasible: boolean;
  details: Record<string, number>;
}

export interface EvaluateResponse {
  all_feasible: boolean;
  radius_m: number;
  omega_rad_s: number;
  rpm: number;
  rim_speed_m_s: number;
  gravity_g: number;
  constraints: ConstraintStatus[];
}

export interface SweepPoint {
  radius_m: number;
  rpm: number;
  rim_speed_m_s: number;
  feasible: boolean;
  binding_constraints: string[];
}

export interface SweepResponse {
  points: SweepPoint[];
  feasible_min_radius: number | null;
  feasible_max_radius: number | null;
}

export interface ParamRange {
  min: number | null;
  max: number | null;
}

export interface FeasibleRangesResponse {
  radius_m: ParamRange;
  wall_thickness_m: ParamRange;
  length_m: ParamRange;
  internal_pressure_kpa: ParamRange;
}

/** All tuneable parameters — sent to both /evaluate and /sweep. */
export interface DesignParams {
  radius_m: number;
  target_gravity_g: number;
  length_m: number;
  population: number;
  internal_pressure_kpa: number;
  o2_fraction: number;
  shielding_areal_density_kg_m2: number;
  wall_thickness_m: number;
  agriculture_area_m2: number;
  diet_land_multiplier: number;
  window_solar_transmittance: number;
  power_per_person_w: number;
  solar_panel_efficiency: number;
  water_per_person_day_liters: number;
  water_recycling_efficiency: number;
  min_water_recycling_efficiency: number;
  max_comfortable_rpm: number;
  max_cross_coupling_deg_s2: number;
  head_turn_rate_deg_s: number;
  max_coriolis_ratio: number;
  max_rim_speed_m_s: number;
  max_gravity_gradient_pct: number;
  min_gravity_g: number;
  max_gravity_g: number;
}

export const DEFAULT_PARAMS: DesignParams = {
  radius_m: 982,
  target_gravity_g: 1.0,
  length_m: 1276,
  population: 8000,
  internal_pressure_kpa: 101.3,
  o2_fraction: 0.21,
  shielding_areal_density_kg_m2: 4500,
  wall_thickness_m: 0.2,
  agriculture_area_m2: 1_600_000,
  diet_land_multiplier: 1.0,
  window_solar_transmittance: 0.3,
  power_per_person_w: 5000.0,
  solar_panel_efficiency: 0.20,
  water_per_person_day_liters: 20.0,
  water_recycling_efficiency: 0.90,
  min_water_recycling_efficiency: 0.98,
  max_comfortable_rpm: 2.0,
  max_cross_coupling_deg_s2: 6.0,
  head_turn_rate_deg_s: 60.0,
  max_coriolis_ratio: 0.25,
  max_rim_speed_m_s: 300.0,
  max_gravity_gradient_pct: 1.0,
  min_gravity_g: 0.3,
  max_gravity_g: 1.0,
};
