import { useCallback, useEffect, useRef, useState } from "react";
import type {
  DesignParams,
  EvaluateResponse,
  FeasibleRangesResponse,
  SweepResponse,
} from "../types/api";

const API = import.meta.env.VITE_API_URL ?? "http://127.0.0.1:8042";

export function useConstraintSolver(params: DesignParams) {
  const [evalResult, setEvalResult] = useState<EvaluateResponse | null>(null);
  const [sweepResult, setSweepResult] = useState<SweepResponse | null>(null);
  const [feasibleRanges, setFeasibleRanges] =
    useState<FeasibleRangesResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const abortRef = useRef<AbortController | null>(null);

  const refresh = useCallback(async () => {
    abortRef.current?.abort();
    const ctrl = new AbortController();
    abortRef.current = ctrl;
    setLoading(true);

    try {
      const [evalRes, sweepRes, rangesRes] = await Promise.all([
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
            ...params,
          }),
          signal: ctrl.signal,
        }),
        fetch(`${API}/api/feasible_ranges`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(params),
          signal: ctrl.signal,
        }),
      ]);

      if (!ctrl.signal.aborted) {
        setEvalResult(await evalRes.json());
        setSweepResult(await sweepRes.json());
        setFeasibleRanges(await rangesRes.json());
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

  return { evalResult, sweepResult, feasibleRanges, loading };
}
