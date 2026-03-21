import { useState, useMemo } from "react";
import CylinderScene from "./components/CylinderScene";
import { useConstraintSolver } from "./hooks/useConstraintSolver";
import { useSceneToggles } from "./hooks/useSceneToggles";
import { DEFAULT_PARAMS, type DesignParams } from "./types/api";
import "./App.css";

const EARTH_G = 9.80665;

export default function Scene3D() {
  const [params] = useState<DesignParams>(DEFAULT_PARAMS);
  const { evalResult } = useConstraintSolver(params);
  const { toggles, setToggles } = useSceneToggles();

  const omega = useMemo(
    () => Math.sqrt((params.target_gravity_g * EARTH_G) / params.radius_m),
    [params.radius_m, params.target_gravity_g],
  );

  const toggleDefs = [
    ["showStrips", "Land/Window strips"],
    ["showEndCaps", "End caps"],
    ["showGravityRings", "Gravity rings"],
    ["showHuman", "Human figure"],
    ["showCoriolis", "Coriolis arrow"],
    ["showGravityLabel", "Gravity label"],
    ["showAxis", "Rotation axis"],
  ] as const;

  return (
    <div className="scene3d-layout">
      <div className="scene3d-main">
        <CylinderScene
          radiusM={params.radius_m}
          lengthM={params.length_m}
          omegaRadS={omega}
          result={evalResult}
          toggles={toggles}
          fullPage
        />
      </div>
      <aside className="scene3d-sidebar">
        <a href="/" className="back-link">&larr; Dashboard</a>
        <span className={`status-pill ${evalResult?.all_feasible ? "pass" : "fail"}`}>
          {evalResult?.all_feasible ? "FEASIBLE" : "INFEASIBLE"}
        </span>
        <h3>Display</h3>
        {toggleDefs.map(([key, label]) => (
          <label key={key} className="toggle-label">
            <input
              type="checkbox"
              checked={toggles[key]}
              onChange={(e) => setToggles({ [key]: e.target.checked })}
            />
            {label}
          </label>
        ))}
      </aside>
    </div>
  );
}
