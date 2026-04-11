import type { EvaluateResponse } from "../types/api";

/** Human-readable constraint names & key detail to show. */
const META: Record<string, { label: string; detail: string; format: (v: number) => string }> = {
  vestibular: { label: "Vestibular (RPM)", detail: "current_rpm", format: (v) => `${v.toFixed(2)} rpm` },
  gravity_level: { label: "Gravity Level", detail: "gravity_g", format: (v) => `${v.toFixed(2)} g` },
  gravity_gradient: { label: "Gravity Gradient", detail: "gradient_pct", format: (v) => `${v.toFixed(3)}%` },
  coriolis: { label: "Coriolis", detail: "coriolis_to_gravity_running", format: (v) => `${(v * 100).toFixed(1)}% of g` },
  cross_coupling: { label: "Cross-Coupling", detail: "cross_coupled_deg_s2", format: (v) => `${v.toFixed(1)} °/s²` },
  rim_speed: { label: "Rim Speed", detail: "rim_speed_m_s", format: (v) => `${v.toFixed(0)} m/s` },
  radiation_shielding: { label: "Radiation Shield", detail: "shielding_kg_m2", format: (v) => `${v.toFixed(0)} kg/m²` },
  atmosphere: { label: "Atmosphere (pO₂)", detail: "o2_partial_pressure_kpa", format: (v) => `${v.toFixed(1)} kPa` },
  population: { label: "Population", detail: "population", format: (v) => `${v.toLocaleString()}` },
  cylinder_length: { label: "Cylinder Length", detail: "length_to_diameter", format: (v) => `L/D = ${v.toFixed(2)}` },
  hoop_stress: { label: "Hoop Stress", detail: "sigma_hoop_mpa", format: (v) => `${v.toFixed(0)} MPa` },
  rotational_stability: { label: "Rotational Stability", detail: "length_to_radius", format: (v) => `L/r = ${v.toFixed(2)}` },
  spinup_energy: { label: "Spin-Up Energy", detail: "spinup_time_days", format: (v) => `${v.toFixed(1)} days` },
  agriculture: { label: "Agriculture Area", detail: "area_per_person_m2", format: (v) => `${v.toFixed(0)} m²/person` },
};

interface Props {
  result: EvaluateResponse | null;
}

export default function ConstraintPanel({ result }: Props) {
  if (!result) return <div className="panel constraint-panel"><h2>Constraints</h2><p className="muted">Waiting for API…</p></div>;

  return (
    <div className="panel constraint-panel">
      <h2>Constraints</h2>
      <div className="status-banner" data-ok={result.all_feasible}>
        {result.all_feasible ? "ALL PASS" : "INFEASIBLE"}
      </div>
      <div className="derived">
        <span>ω = {result.omega_rad_s.toFixed(4)} rad/s</span>
        <span>{result.rpm.toFixed(2)} rpm</span>
        <span>{result.rim_speed_m_s.toFixed(1)} m/s rim</span>
        <span>{result.gravity_g.toFixed(2)} g</span>
      </div>
      <div className="constraint-cards">
        {result.constraints.map((c) => {
          const meta = META[c.name];
          const detailVal = meta ? c.details[meta.detail] : undefined;
          return (
            <div key={c.name} className="constraint-card" data-feasible={c.feasible}>
              <div className="card-indicator" />
              <div className="card-body">
                <div className="card-name">{meta?.label ?? c.name}</div>
                <div className="card-detail">
                  {detailVal !== undefined && meta ? meta.format(detailVal) : "—"}
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
