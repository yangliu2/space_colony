import { useState, useEffect, useCallback } from "react";

const STORAGE_KEY = "habitat-scene-toggles";

export interface SceneToggles {
  showStrips: boolean;
  showGravityRings: boolean;
  showHuman: boolean;
  showCoriolis: boolean;
  showGravityLabel: boolean;
  showAxis: boolean;
  showEndCaps: boolean;
}

const DEFAULTS: SceneToggles = {
  showStrips: false,
  showGravityRings: false,
  showHuman: false,
  showCoriolis: false,
  showGravityLabel: false,
  showAxis: false,
  showEndCaps: false,
};

function load(): SceneToggles {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (raw) return { ...DEFAULTS, ...JSON.parse(raw) };
  } catch {
    // ignore
  }
  return DEFAULTS;
}

/**
 * Shared toggle state persisted in localStorage.
 * Changes on the /3d page are picked up by the main page on next render.
 */
export function useSceneToggles() {
  const [toggles, setTogglesRaw] = useState<SceneToggles>(load);

  // Listen for storage events from other tabs/pages
  useEffect(() => {
    const handler = (e: StorageEvent) => {
      if (e.key === STORAGE_KEY && e.newValue) {
        setTogglesRaw({ ...DEFAULTS, ...JSON.parse(e.newValue) });
      }
    };
    window.addEventListener("storage", handler);
    return () => window.removeEventListener("storage", handler);
  }, []);

  const setToggles = useCallback((update: Partial<SceneToggles>) => {
    setTogglesRaw((prev) => {
      const next = { ...prev, ...update };
      localStorage.setItem(STORAGE_KEY, JSON.stringify(next));
      return next;
    });
  }, []);

  return { toggles, setToggles };
}
