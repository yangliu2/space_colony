import { useMemo, useRef } from "react";
import CylinderScene, {
  getCameraPresets,
  sceneScale,
  type CameraControlHandle,
} from "./components/CylinderScene";
import StatsPanel from "./components/StatsPanel";
import { useConstraintSolver } from "./hooks/useConstraintSolver";
import { useSceneToggles } from "./hooks/useSceneToggles";
import { useDesignParams } from "./hooks/useDesignParams";
import "./App.css";

const EARTH_G = 9.80665;

export default function Scene3D() {
  const { params } = useDesignParams();
  const { evalResult } = useConstraintSolver(params);
  const { toggles, setToggles } = useSceneToggles();
  const cameraRef = useRef<CameraControlHandle>(null);

  const omega = useMemo(
    () => Math.sqrt((params.target_gravity_g * EARTH_G) / params.radius_m),
    [params.radius_m, params.target_gravity_g],
  );

  const cameraPresets = useMemo(() => {
    const { r, l } = sceneScale(params.radius_m, params.length_m);
    return getCameraPresets(r, l);
  }, [params.radius_m, params.length_m]);

  const toggleGroups = [
    {
      label: "Structure",
      items: [
        ["showStrips", "Land/Window strips"],
        ["showEndCaps", "End caps"],
        ["showCables", "Tension cables"],
        ["showMirrors", "External mirrors"],
        ["showBearing", "Bearing connection"],
      ] as const,
    },
    {
      label: "Engineering",
      items: [
        ["showInteriorZones", "Interior zones"],
        ["showAgriculture", "Agriculture pods"],
      ] as const,
    },
    {
      label: "Physics",
      items: [
        ["showGravityRings", "Gravity rings"],
        ["showHuman", "Human figure"],
        ["showCoriolis", "Coriolis arrow"],
        ["showGravityLabel", "Gravity label"],
        ["showAxis", "Rotation axis"],
      ] as const,
    },
    {
      label: "Exploration",
      items: [
        ["showHotspots", "📍 Viewpoint markers"],
        ["showInteriorLighting", "💡 Interior lighting"],
      ] as const,
    },
  ];

  return (
    <div className="scene3d-layout">
      {/* Left sidebar — statistics */}
      <aside className="scene3d-stats">
        <a href="/" className="back-link">&larr; Dashboard</a>
        <StatsPanel params={params} result={evalResult} />
      </aside>

      {/* Center — 3D scene */}
      <div className="scene3d-main">
        <CylinderScene
          radiusM={params.radius_m}
          lengthM={params.length_m}
          omegaRadS={omega}
          result={evalResult}
          toggles={toggles}
          fullPage
          cameraRef={cameraRef}
        />
      </div>

      {/* Right sidebar — toggles & camera */}
      <aside className="scene3d-sidebar">
        <span className={`status-pill ${evalResult?.all_feasible ? "pass" : "fail"}`}>
          {evalResult?.all_feasible ? "FEASIBLE" : "INFEASIBLE"}
        </span>

        {/* Camera presets */}
        <h3>📷 Views</h3>
        <div className="preset-grid">
          {cameraPresets.map((preset) => (
            <button
              key={preset.name}
              className="preset-btn"
              onClick={() => cameraRef.current?.goToPreset(preset)}
            >
              {preset.name}
            </button>
          ))}
        </div>

        {/* Toggle groups */}
        {toggleGroups.map((group) => (
          <div key={group.label}>
            <h3>{group.label}</h3>
            {group.items.map(([key, label]) => (
              <label key={key} className="toggle-label">
                <input
                  type="checkbox"
                  checked={toggles[key]}
                  onChange={(e) => setToggles({ [key]: e.target.checked })}
                />
                {label}
              </label>
            ))}
          </div>
        ))}
      </aside>
    </div>
  );
}
