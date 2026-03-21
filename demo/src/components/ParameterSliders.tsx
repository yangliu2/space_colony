import type { DesignParams } from "../types/api";

interface SliderDef {
  key: keyof DesignParams;
  label: string;
  min: number;
  max: number;
  step: number;
  unit: string;
}

const DESIGN_SLIDERS: SliderDef[] = [
  { key: "radius_m", label: "Radius", min: 50, max: 15000, step: 10, unit: "m" },
  { key: "target_gravity_g", label: "Target gravity", min: 0.1, max: 1.5, step: 0.05, unit: "g" },
  { key: "length_m", label: "Cylinder length", min: 500, max: 50000, step: 500, unit: "m" },
  { key: "population", label: "Population", min: 50, max: 100000, step: 100, unit: "" },
];

const ASSUMPTION_SLIDERS: SliderDef[] = [
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
}

function SliderRow({ def, value, onChange }: { def: SliderDef; value: number; onChange: (v: number) => void }) {
  return (
    <div className="slider-row">
      <label>
        <span className="slider-label">{def.label}</span>
        <span className="slider-value">
          {typeof value === "number" ? value.toLocaleString(undefined, { maximumFractionDigits: 2 }) : value}
          {def.unit && ` ${def.unit}`}
        </span>
      </label>
      <input
        type="range"
        min={def.min}
        max={def.max}
        step={def.step}
        value={value}
        onChange={(e) => onChange(Number(e.target.value))}
      />
    </div>
  );
}

export default function ParameterSliders({ params, onChange }: Props) {
  const set = (key: keyof DesignParams, v: number) =>
    onChange({ ...params, [key]: key === "population" ? Math.round(v) : v });

  return (
    <div className="panel sliders-panel">
      <h2>Design Parameters</h2>
      {DESIGN_SLIDERS.map((d) => (
        <SliderRow key={d.key} def={d} value={params[d.key] as number} onChange={(v) => set(d.key, v)} />
      ))}

      <h2>Human Assumptions</h2>
      {ASSUMPTION_SLIDERS.map((d) => (
        <SliderRow key={d.key} def={d} value={params[d.key] as number} onChange={(v) => set(d.key, v)} />
      ))}
    </div>
  );
}
