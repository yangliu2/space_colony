import { useCallback, useEffect, useRef, useState } from "react";
import type {
  DesignParams,
  EvaluateResponse,
  SweepResponse,
} from "../types/api";

const API = "http://127.0.0.1:8042";

export function useConstraintSolver(params: DesignParams) {
  const [evalResult, setEvalResult] = useState<EvaluateResponse | null>(null);
  const [sweepResult, setSweepResult] = useState<SweepResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const abortRef = useRef<AbortController | null>(null);

  const refresh = useCallback(async () => {
    abortRef.current?.abort();
    const ctrl = new AbortController();
    abortRef.current = ctrl;
    setLoading(true);

    try {
      const [evalRes, sweepRes] = await Promise.all([
        fetch(`${API}/api/evaluate`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(params),
          signal: ctrl.signal,
        }),
        fetch(`${API}/api/sweep`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            r_min: 100,
            r_max: 15000,
            n_points: 300,
            target_gravity_g: params.target_gravity_g,
            max_comfortable_rpm: params.max_comfortable_rpm,
            max_cross_coupling_deg_s2: params.max_cross_coupling_deg_s2,
            head_turn_rate_deg_s: params.head_turn_rate_deg_s,
            max_coriolis_ratio: params.max_coriolis_ratio,
            max_rim_speed_m_s: params.max_rim_speed_m_s,
            max_gravity_gradient_pct: params.max_gravity_gradient_pct,
            min_gravity_g: params.min_gravity_g,
            max_gravity_g: params.max_gravity_g,
          }),
          signal: ctrl.signal,
        }),
      ]);

      if (!ctrl.signal.aborted) {
        setEvalResult(await evalRes.json());
        setSweepResult(await sweepRes.json());
      }
    } catch (e) {
      if (e instanceof DOMException && e.name === "AbortError") return;
      console.error("API error:", e);
    } finally {
      if (!ctrl.signal.aborted) setLoading(false);
    }
  }, [params]);

  // Debounce: refresh 150ms after params stop changing
  useEffect(() => {
    const t = setTimeout(refresh, 150);
    return () => clearTimeout(t);
  }, [refresh]);

  return { evalResult, sweepResult, loading };
}
