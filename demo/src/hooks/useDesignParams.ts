import { useState, useEffect, useCallback } from "react";
import { DEFAULT_PARAMS, type DesignParams } from "../types/api";

const STORAGE_KEY = "habitat-design-params";

function load(): DesignParams {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (raw) return { ...DEFAULT_PARAMS, ...JSON.parse(raw) };
  } catch {
    // ignore
  }
  return DEFAULT_PARAMS;
}

/**
 * Shared design parameters persisted in localStorage.
 * Changes on the main page are picked up by the /3d page and vice versa.
 */
export function useDesignParams() {
  const [params, setParamsRaw] = useState<DesignParams>(load);

  // Listen for storage events from other tabs/pages
  useEffect(() => {
    const handler = (e: StorageEvent) => {
      if (e.key === STORAGE_KEY && e.newValue) {
        setParamsRaw({ ...DEFAULT_PARAMS, ...JSON.parse(e.newValue) });
      }
    };
    window.addEventListener("storage", handler);
    return () => window.removeEventListener("storage", handler);
  }, []);

  const setParams = useCallback((update: DesignParams) => {
    setParamsRaw(update);
    localStorage.setItem(STORAGE_KEY, JSON.stringify(update));
  }, []);

  return { params, setParams };
}
