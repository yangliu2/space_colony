# Space Habitat Study Plan (Hybrid Track)
## Designed for: 5–8 hrs/week, 6–12 month horizon

---

# Weekly Schedule (Repeatable)

## Total: ~6 hours/week

### Day 1 (2 hrs) — Build Track (Core)
- Work on current model (coding / simulation)
- Implement 1 new feature or constraint
- Output: graph or result

### Day 2 (2 hrs) — Physics Track
- Study 1 concept (mechanics / rotation / relativity basics)
- Solve 3–5 problems (must write out solutions)

### Day 3 (2 hrs) — Integration
- Apply physics concept into your model
- Write short notes:
  - What changed?
  - What assumption is unrealistic?

---

# Phases (Implementation Track)

## Phase 1: Rotational Dynamics Core ✅
**Constraints:** vestibular RPM, gravity level, gravity gradient

**Deliverables:**
- Pydantic models for `HabitatParameters`, `HumanAssumptions`
- `Constraint` protocol with `evaluate()` and `compute_bounds()`
- `FeasibleRegionSolver` (sweep, binary search, feasible range)
- 7 boundary analysis experiments
- Result: minimum radius 224m at 1g (RPM-dominated)

## Phase 2: Full Rotational Constraint Set ✅
**Constraints:** + Coriolis, cross-coupling, rim speed (6 total)

**Deliverables:**
- Sensitivity analysis module (tornado chart data)
- 6 Phase 2 experiments with feasible band discovery
- Result: minimum radius jumps to 982m (cross-coupling dominated)
- Feasible band at 1g: [982m, 9,177m]

## Phase 3: Biological & Environmental Constraints ✅
**Constraints:** + radiation shielding, atmosphere, minimum viable population (9 total)

**Deliverables:**
- Extended `HabitatParameters` with geometry (length, population)
- Extended `HumanAssumptions` with biological thresholds
- `RadiationConstraint` — shielding areal density ≥ minimum (GCR/SPE)
- `AtmosphereConstraint` — pO₂ within [16, 50] kPa
- `PopulationConstraint` — population ≥ genetic minimum (MVP)
- Full test suite for all 3 biological constraints
- Phase 3 experiment script (`run_phase3_analysis.py`)
- Conclusions document: `003_biological_constraints_and_monte_carlo.md`

**Biological constraints from `constraint_biological.md`:**

| Constraint | Modelable? | Priority | Status |
|------------|-----------|----------|--------|
| Radiation (GCR/SPE) | Yes — shielding mass vs. dose | High | ✅ Implemented |
| Atmosphere (pO₂ range) | Yes — pressure/composition bounds | High | ✅ Implemented |
| Psychology (population) | Yes — minimum viable population | Medium | ✅ Implemented |
| Circadian lighting | No — purely engineerable | Low | Skipped (soft) |
| Psychology (volume) | Partially — volume per person | Medium | Skipped (soft at O'Neill scale) |
| Acoustics | No — purely engineerable | Low | Skipped (soft) |
| Microbiome / ecosystem | Partially — O₂/CO₂ balance rate | Medium | Not yet modeled |
| Reproduction | No — insufficient data | Low | Cannot model yet |
| Magnetic field | No — purely engineerable | Low | Skipped (soft) |

## Phase 4: Uncertainty Modeling ✅
**Focus:** Monte Carlo simulation, probability distributions

**Deliverables:**
- `analysis/monte_carlo.py` — samples assumptions from distributions, 1,000+ trials
- Feasible region statistics and probability distributions of minimum radius
- Variance decomposition to identify which uncertainties matter most
- Test suite (`test_monte_carlo.py`)

## Phase 5: Integrated Model & Visualization ✅
**Focus:** Combine all modules, interactive exploration, publication-quality outputs

**Deliverables:**
- `visualization/plots.py` — matplotlib feasible region plot, tornado chart, constraint map
- `analysis/sensitivity.py` — one-at-a-time perturbation analysis
- FastAPI backend (`api/main.py`) with `/evaluate`, `/sweep`, `/defaults` endpoints
- Interactive React + Three.js demo (`demo/`):
  - Parameter sliders (radius, gravity, length, population, human assumptions)
  - Constraint status panel (9 constraints, green/red cards)
  - 2D feasible region chart (Recharts)
  - 3D rotating O'Neill cylinder with land/window strips, human figure, Coriolis arrows
  - Standalone `/3d` page with toggle controls
- Three phase conclusion documents in `conclusions/`
- **"Feasible Habitat Design Space" summary**: `conclusions/feasible_habitat_design_space.md`

## Phase 6: Advanced Constraints ← NEXT
**Focus:** Systems engineering constraints beyond rotation and biology

**TODO:**
- **Rotational stability & spin-up energy** — the cylinder spins about its long axis (minimum $I$), but energy dissipation from internal activity (people, weather, machinery) drives rotation toward the maximum-$I$ axis (Explorer 1 problem). Requires active stabilization. Also: spin-up energy budget ($E = \frac{1}{2}I\omega^2$ with $I \approx mr^2$ for a thin shell) and how long it takes with realistic thrust
- Thermal management (radiator area vs. waste heat)
- Structural dynamics (vibration modes, seismic equivalent, precession/nutation from internal mass redistribution)
- Agriculture area vs. population (food self-sufficiency)
- Water recycling efficiency
- Energy budget (solar panel area, power distribution)

---

# Month-by-Month Plan

## Month 1: Rotation & Artificial Gravity ✅
Goal:
- Understand $a = \omega^2 r$

Build:
- Model radius vs spin rate vs gravity

Checkpoint:
- Can explain why large radius is required

---

## Month 2: Human Constraints ✅
Study:
- Vestibular limits (~2 rpm)
- Bone density vs gravity
- Cross-coupling, Coriolis

Build:
- Add constraints: max spin, min gravity, gradient, Coriolis, cross-coupling, rim speed

Checkpoint:
- Define "safe operating zone" → [982m, 9,177m] at 1g

---

## Month 3: Biological Constraints & System Scaling ✅
Study:
- Radiation shielding physics (GCR, SPE, secondary particles)
- Atmospheric composition requirements
- Closed ecosystem challenges (Biosphere 2 lessons)
- Material requirements and mass budgets

Build:
- 3 biological constraint implementations (radiation, atmosphere, population)
- Monte Carlo simulation module
- Phase 3 experiment script + conclusions document

Checkpoint:
- ✅ Identified binding biological constraints (radiation shielding dominates mass)
- ✅ Quantified mass budget via `construction_material_estimates.md`

---

## Month 4: Uncertainty Modeling ✅
Study:
- Monte Carlo simulation
- Variance decomposition

Build:
- ✅ `monte_carlo.py` with configurable trial counts
- ✅ Sensitivity analysis module (`sensitivity.py`)

Checkpoint:
- ✅ Probability distributions of feasible region
- ✅ Variance decomposition identifies cross-coupling and radiation as dominant uncertainties

---

## Month 5–6: Integrated Model & Visualization ✅
Build:
- ✅ Combined all 9 constraints into unified solver
- ✅ Matplotlib visualization module (`plots.py`)
- ✅ FastAPI backend + React/Three.js interactive demo
- ✅ 3D O'Neill cylinder with land/window strips, human figure, Coriolis arrows

Output:
- ✅ Three conclusions documents (phases 1, 2, 3)
- ✅ Interactive web dashboard at `demo/`

---

# Key Principle

Simulation is not prediction.

Simulation is:
- Constraint discovery
- Sensitivity analysis
- Assumption testing

---

# What "Success" Looks Like

By Month 3: ✅
- You can reject bad designs quickly
- **Achieved:** Model rejects $r < 982$ m at 1g in < 1 second across 9 constraints

By Month 6: ✅
- You can defend a design logically
- **Achieved:** Full scorecard for any design point; sensitivity analysis shows which assumptions matter; Monte Carlo gives confidence intervals; interactive demo for exploration

By Month 12:
- You can publish / share a meaningful model

---

# Final Reminder

You are not trying to "prove biology."

You are trying to:
- Bound the problem
- Understand limits
- Reduce unknowns

That is exactly how engineering progresses.
