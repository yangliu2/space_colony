import {
  Area,
  CartesianGrid,
  ComposedChart,
  ReferenceLine,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import type { SweepResponse } from "../types/api";

interface Props {
  sweep: SweepResponse | null;
  currentRadius: number;
}

export default function FeasibleRegionChart({ sweep, currentRadius }: Props) {
  if (!sweep) return <div className="panel chart-panel"><h2>Feasible Region</h2><p className="muted">Waiting…</p></div>;

  const data = sweep.points.map((p) => ({
    radius: Math.round(p.radius_m),
    rpm: Number(p.rpm.toFixed(3)),
    rimSpeed: Math.round(p.rim_speed_m_s),
    feasible: p.feasible ? 1 : 0,
    binding: p.binding_constraints.join(", ") || "none",
  }));

  return (
    <div className="panel chart-panel">
      <h2>Feasible Region (radius sweep)</h2>
      {sweep.feasible_min_radius && sweep.feasible_max_radius && (
        <p className="band-label">
          Feasible band: {sweep.feasible_min_radius.toLocaleString(undefined, { maximumFractionDigits: 0 })} m
          &nbsp;–&nbsp;
          {sweep.feasible_max_radius.toLocaleString(undefined, { maximumFractionDigits: 0 })} m
        </p>
      )}
      <ResponsiveContainer width="100%" height={280}>
        <ComposedChart data={data} margin={{ top: 10, right: 20, bottom: 20, left: 0 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="#333" />
          <XAxis
            dataKey="radius"
            type="number"
            domain={[0, 'auto']}
            tickCount={10}
            label={{ value: "Radius (m)", position: "insideBottom", offset: -8, fill: "#aaa" }}
            tick={{ fill: "#aaa", fontSize: 11 }}
          />
          <YAxis domain={[0, 1.1]} hide />
          <Tooltip
            contentStyle={{ background: "#1a1a2e", border: "1px solid #444", borderRadius: 6 }}
            labelStyle={{ color: "#ccc" }}
            itemStyle={{ color: "#ccc" }}
            formatter={(_: unknown, name: string | number | undefined, props: { payload?: { binding: string } }) => {
              if (name === "feasible") {
                return props.payload?.binding === "none" ? "PASS" : `FAIL: ${props.payload?.binding ?? ""}`;
              }
              return String(_);
            }}
            labelFormatter={(v) => `r = ${Number(v).toLocaleString()} m`}
          />
          <Area
            type="stepAfter"
            dataKey="feasible"
            stroke="#22c55e"
            fill="#22c55e"
            fillOpacity={0.15}
            strokeWidth={2}
            isAnimationActive={false}
          />
          <ReferenceLine x={Math.round(currentRadius)} stroke="#f97316" strokeDasharray="5 3" label={{ value: "current", fill: "#f97316", fontSize: 11 }} />
        </ComposedChart>
      </ResponsiveContainer>
    </div>
  );
}
