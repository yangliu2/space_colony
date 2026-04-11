import type { DesignParams, FeasibleRangesResponse, ParamRange } from "../types/api";

interface SliderDef {
  key: keyof DesignParams;
  label: string;
  min: number;
  max: number;
  step: number;
  unit: string;
}

// Bending resonance limit: L_max = 75.22 * r^0.75 (see plans/constraint_cylinder_length.md)
// Slider max = 20% above limit, rounded to nearest 500m, so the green bar end is visible.
const C_BENDING = 75.22;
function lengthSliderMax(radiusM: number): number {
  const bendingMax = C_BENDING * Math.pow(radiusM, 0.75);
  return Math.ceil((bendingMax * 1.2) / 500) * 500;
}
function lengthSliderStep(max: number): number {
  // ~200 steps across the range, rounded to nearest 50m
  return Math.max(50, Math.round(max / 200 / 50) * 50);
}

const STATIC_DESIGN_SLIDERS: SliderDef[] = [
  { key: "radius_m", label: "Radius", min: 50, max: 15000, step: 10, unit: "m" },
  { key: "target_gravity_g", label: "Target gravity", min: 0.1, max: 1.5, step: 0.05, unit: "g" },
  { key: "population", label: "Population", min: 50, max: 100000, step: 100, unit: "" },
  { key: "agriculture_area_m2", label: "Agriculture area", min: 100000, max: 10000000, step: 100000, unit: "m²" },
  { key: "wall_thickness_m", label: "Wall thickness", min: 0.05, max: 3.0, step: 0.05, unit: "m" },
  { key: "internal_pressure_kpa", label: "Atmosphere", min: 50, max: 150, step: 1, unit: "kPa" },
];

const ASSUMPTION_SLIDERS: SliderDef[] = [
  { key: "diet_land_multiplier", label: "Diet land multiplier", min: 1.0, max: 8.0, step: 0.1, unit: "×" },
  { key: "window_solar_transmittance", label: "Solar transmittance", min: 0.05, max: 0.8, step: 0.05, unit: "" },
  { key: "power_per_person_w", label: "Power per person", min: 500, max: 15000, step: 500, unit: "W" },
  { key: "solar_panel_efficiency", label: "Solar panel efficiency", min: 0.10, max: 0.40, step: 0.01, unit: "" },
  { key: "max_comfortable_rpm", label: "Max RPM", min: 0.5, max: 6, step: 0.1, unit: "rpm" },
  { key: "max_cross_coupling_deg_s2", label: "Max cross-coupling", min: 1, max: 15, step: 0.5, unit: "°/s²" },
  { key: "head_turn_rate_deg_s", label: "Head turn rate", min: 20, max: 120, step: 5, unit: "°/s" },
  { key: "max_coriolis_ratio", label: "Max Coriolis ratio", min: 0.05, max: 0.5, step: 0.01, unit: "" },
  { key: "max_rim_speed_m_s", label: "Max rim speed", min: 100, max: 600, step: 10, unit: "m/s" },
  { key: "max_gravity_gradient_pct", label: "Max gravity gradient", min: 0.1, max: 5, step: 0.1, unit: "%" },
  { key: "min_gravity_g", label: "Min gravity", min: 0.1, max: 0.9, step: 0.05, unit: "g" },
  { key: "max_gravity_g", label: "Max gravity", min: 0.5, max: 2.0, step: 0.05, unit: "g" },
];

interface Props {
  params: DesignParams;
  onChange: (p: DesignParams) => void;
  feasibleRanges?: FeasibleRangesResponse | null;
}

function SliderRow({
  def,
  value,
  onChange,
  feasible,
}: {
  def: SliderDef;
  value: number;
  onChange: (v: number) => void;
  feasible?: ParamRange | null;
}) {
  const span = def.max - def.min;
  const fMin = feasible?.min;
  const fMax = feasible?.max;
  const hasRange = fMin != null && fMax != null && span > 0;
  const leftPct = hasRange ? ((fMin - def.min) / span) * 100 : 0;
  const widthPct = hasRange ? ((fMax - fMin) / span) * 100 : 0;

  return (
    <div className="slider-row">
      <label>
        <span className="slider-label">{def.label}</span>
        <span className="slider-value">
          {typeof value === "number" ? value.toLocaleString(undefined, { maximumFractionDigits: 2 }) : value}
          {def.unit && ` ${def.unit}`}
        </span>
      </label>
      <div className="slider-track-wrapper">
        {hasRange && (
          <div
            className="feasible-bar"
            style={{ left: `${leftPct}%`, width: `${widthPct}%` }}
          />
        )}
        <input
          type="range"
          min={def.min}
          max={def.max}
          step={def.step}
          value={value}
          onChange={(e) => onChange(Number(e.target.value))}
        />
      </div>
    </div>
  );
}

const RANGE_KEYS: Record<string, keyof FeasibleRangesResponse> = {
  radius_m: "radius_m",
  wall_thickness_m: "wall_thickness_m",
  length_m: "length_m",
  internal_pressure_kpa: "internal_pressure_kpa",
};

export default function ParameterSliders({ params, onChange, feasibleRanges }: Props) {
  const set = (key: keyof DesignParams, v: number) =>
    onChange({ ...params, [key]: key === "population" ? Math.round(v) : v });

  const lMax = lengthSliderMax(params.radius_m);
  const lengthSlider: SliderDef = {
    key: "length_m",
    label: "Cylinder length",
    min: 100,
    max: lMax,
    step: lengthSliderStep(lMax),
    unit: "m",
  };

  // Insert length slider after radius (index 0)
  const designSliders = [
    STATIC_DESIGN_SLIDERS[0],
    lengthSlider,
    ...STATIC_DESIGN_SLIDERS.slice(1),
  ];

  return (
    <div className="panel sliders-panel">
      <h2>Design Parameters</h2>
      {designSliders.map((d) => (
        <SliderRow
          key={d.key}
          def={d}
          value={params[d.key] as number}
          onChange={(v) => set(d.key, v)}
          feasible={feasibleRanges?.[RANGE_KEYS[d.key]] ?? null}
        />
      ))}

      <h2>Human Assumptions</h2>
      {ASSUMPTION_SLIDERS.map((d) => (
        <SliderRow key={d.key} def={d} value={params[d.key] as number} onChange={(v) => set(d.key, v)} />
      ))}
    </div>
  );
}
