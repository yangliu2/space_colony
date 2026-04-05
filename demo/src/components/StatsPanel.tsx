import type { DesignParams, EvaluateResponse } from "../types/api";

const EARTH_G = 9.80665;

interface Props {
  params: DesignParams;
  result: EvaluateResponse | null;
  compact?: boolean;
}

export default function StatsPanel({ params, result, compact }: Props) {
  const omega = Math.sqrt((params.target_gravity_g * EARTH_G) / params.radius_m);
  const rpm = (omega * 60) / (2 * Math.PI);
  const period = omega > 0 ? (2 * Math.PI) / omega : 0;
  const rimSpeed = omega * params.radius_m;
  const diameter = params.radius_m * 2;
  const circumference = 2 * Math.PI * params.radius_m;
  const stripWidth = circumference / 6;
  const landArea = Math.PI * params.radius_m * params.length_m; // 3 strips × (π/3) × r × L
  const totalSurface = 2 * Math.PI * params.radius_m * params.length_m;
  const volume = Math.PI * params.radius_m * params.radius_m * params.length_m;
  const areaPerCapita = landArea / params.population;
  const maxLength = 75.22 * Math.pow(params.radius_m, 0.75);

  // Coriolis ratio from result
  const coriolisRatio =
    result?.constraints.find((c) => c.name === "coriolis")?.details
      .coriolis_to_gravity_running ?? 0;

  // Gravity gradient
  const gravityGradient =
    result?.constraints.find((c) => c.name === "gravity_gradient")?.details
      .gradient_pct ?? 0;

  const stats = [
    {
      group: "Feasibility",
      items: [
        {
          label: "Status",
          value: result?.all_feasible ? "FEASIBLE" : "INFEASIBLE",
          className: result?.all_feasible ? "stat-pass" : "stat-fail",
        },
        {
          label: "Passing",
          value: result
            ? `${result.constraints.filter((c) => c.feasible).length}/${result.constraints.length}`
            : "—",
        },
      ],
    },
    {
      group: "Rotation",
      items: [
        { label: "Angular velocity", value: `${omega.toFixed(4)} rad/s` },
        { label: "RPM", value: `${rpm.toFixed(2)} rpm` },
        { label: "Period", value: `${period.toFixed(1)} s/rev` },
        { label: "Rim speed", value: `${rimSpeed.toFixed(1)} m/s` },
        { label: "Demo speed", value: "10× real-time", className: "stat-muted" },
      ],
    },
    {
      group: "Gravity",
      items: [
        { label: "Surface gravity", value: `${params.target_gravity_g.toFixed(2)} g` },
        { label: "Gradient (head–foot)", value: `${gravityGradient.toFixed(3)}%` },
        { label: "Coriolis ratio", value: `${(coriolisRatio * 100).toFixed(1)}% of g` },
      ],
    },
    {
      group: "Geometry",
      items: [
        { label: "Radius", value: `${params.radius_m.toLocaleString()} m` },
        { label: "Diameter", value: `${diameter.toLocaleString()} m` },
        { label: "Length", value: `${params.length_m.toLocaleString()} m` },
        { label: "L/D ratio", value: (params.length_m / diameter).toFixed(2) },
        { label: "Max safe length", value: `${Math.round(maxLength).toLocaleString()} m` },
        { label: "Strip width", value: `${Math.round(stripWidth).toLocaleString()} m` },
      ],
    },
    {
      group: "Habitation",
      items: [
        { label: "Land area (3 strips)", value: `${(landArea / 1e6).toFixed(2)} km²` },
        { label: "Total surface", value: `${(totalSurface / 1e6).toFixed(2)} km²` },
        { label: "Interior volume", value: `${(volume / 1e9).toFixed(2)} km³` },
        { label: "Population", value: params.population.toLocaleString() },
        {
          label: "Area per capita",
          value: `${Math.round(areaPerCapita)} m² (${(areaPerCapita / 10000).toFixed(2)} ha)`,
        },
      ],
    },
    {
      group: "Atmosphere",
      items: [
        { label: "Pressure", value: `${params.internal_pressure_kpa.toFixed(1)} kPa` },
        { label: "O₂ fraction", value: `${(params.o2_fraction * 100).toFixed(0)}%` },
        {
          label: "Air mass",
          value: `${Math.round(
            (volume * 1.225 * params.internal_pressure_kpa) / 101.3
          ).toLocaleString()} t`,
        },
      ],
    },
  ];

  const groupElements = stats.map((section) => (
    <div key={section.group} className="stats-group">
      <h3>{section.group}</h3>
      {section.items.map((item) => (
        <div key={item.label} className={`stat-row ${item.className ?? ""}`}>
          <span className="stat-label">{item.label}</span>
          <span className="stat-value">{item.value}</span>
        </div>
      ))}
    </div>
  ));

  return (
    <div className={`stats-panel ${compact ? "stats-compact" : ""}`}>
      <h2>📊 Statistics</h2>
      {compact ? (
        <div className="stats-groups-grid">{groupElements}</div>
      ) : (
        groupElements
      )}
    </div>
  );
}
