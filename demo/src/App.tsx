import { useMemo } from "react";
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

function App() {
  const { params, setParams } = useDesignParams();
  const { evalResult, sweepResult, feasibleRanges, loading } = useConstraintSolver(params);
  const { toggles } = useSceneToggles();

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

      <div className="main-grid">
        <aside className="sidebar">
          <ParameterSliders params={params} onChange={setParams} feasibleRanges={feasibleRanges} />
        </aside>

        <main className="content">
          <div className="top-row">
            <ConstraintPanel result={evalResult} />
            <CylinderScene
              radiusM={params.radius_m}
              lengthM={params.length_m}
              omegaRadS={omega}
              result={evalResult}
              toggles={toggles}
            />
          </div>
          <StatsPanel params={params} result={evalResult} compact />
          <FeasibleRegionChart sweep={sweepResult} currentRadius={params.radius_m} />
        </main>
      </div>
    </div>
  );
}

export default App;
