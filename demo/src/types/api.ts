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
  max_comfortable_rpm: 2.0,
  max_cross_coupling_deg_s2: 6.0,
  head_turn_rate_deg_s: 60.0,
  max_coriolis_ratio: 0.25,
  max_rim_speed_m_s: 300.0,
  max_gravity_gradient_pct: 1.0,
  min_gravity_g: 0.3,
  max_gravity_g: 1.0,
};
