import { useMemo, useState } from "react";
import ParameterSliders from "./components/ParameterSliders";
import ConstraintPanel from "./components/ConstraintPanel";
import StatsPanel from "./components/StatsPanel";
import FeasibleRegionChart from "./components/FeasibleRegionChart";
import CylinderScene from "./components/CylinderScene";
import { useConstraintSolver } from "./hooks/useConstraintSolver";
import { useSceneToggles } from "./hooks/useSceneToggles";
import { useDesignParams } from "./hooks/useDesignParams";
import "./App.css";

const EARTH_G = 9.80665;

type MobileTab = "params" | "3d" | "stats" | "chart";

function App() {
  const { params, setParams } = useDesignParams();
  const { evalResult, sweepResult, feasibleRanges, loading } = useConstraintSolver(params);
  const { toggles } = useSceneToggles();
  const [activeTab, setActiveTab] = useState<MobileTab>("3d");

  const omega = useMemo(
    () => Math.sqrt((params.target_gravity_g * EARTH_G) / params.radius_m),
    [params.radius_m, params.target_gravity_g],
  );

  return (
    <div className="app-layout">
      <header className="app-header">
        <h1>O'Neill Cylinder Constraint Explorer</h1>
        {loading && <span className="loading-dot" />}
      </header>

      <nav className="mobile-tab-bar" aria-label="Section navigation">
        {(["params", "3d", "stats", "chart"] as const).map((tab) => (
          <button
            key={tab}
            className={`tab-btn${activeTab === tab ? " tab-btn-active" : ""}`}
            onClick={() => setActiveTab(tab)}
          >
            {tab === "params"
              ? "Params"
              : tab === "3d"
                ? "3D"
                : tab === "stats"
                  ? "Stats"
                  : "Chart"}
          </button>
        ))}
      </nav>

      <div className="main-grid">
        <aside className={`sidebar${activeTab !== "params" ? " mobile-hidden" : ""}`}>
          <ParameterSliders params={params} onChange={setParams} feasibleRanges={feasibleRanges} />
        </aside>

        <main className="content">
          <div className={`top-row${activeTab !== "3d" ? " mobile-hidden" : ""}`}>
            <ConstraintPanel result={evalResult} />
            <CylinderScene
              radiusM={params.radius_m}
              lengthM={params.length_m}
              omegaRadS={omega}
              result={evalResult}
              toggles={toggles}
            />
          </div>
          <div className={activeTab !== "stats" ? "mobile-hidden" : undefined}>
            <StatsPanel params={params} result={evalResult} compact />
          </div>
          <div className={activeTab !== "chart" ? "mobile-hidden" : undefined}>
            <FeasibleRegionChart sweep={sweepResult} currentRadius={params.radius_m} />
          </div>
        </main>
      </div>
    </div>
  );
}

export default App;
