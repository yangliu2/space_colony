# Space Habitat Study Plan — Project Complete

**Status:** All 18 constraints implemented. Model validated against published literature.
**Completed:** April 2026 · [Future Research Directions](#future-research-directions) below.

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

## Phase 6: Advanced Constraints ✅
**Focus:** Systems engineering constraints beyond rotation and biology

**Research completed:**
- `structural_engineering.md` — hoop stress analysis, tension-dominant architecture,
  material selection (steel vs CFRP vs CNT), Monte Carlo reliability framework,
  safety factors (NASA-STD-5001B), micrometeorite cumulative damage modeling
- `interior_space_utilization.md` — O'Neill's interior zoning (rim habitation,
  mid-zone industry, zero-g axis), external agriculture modules, gravity gradient
  utilization, counter-rotating pair design, psychological considerations
- `constraint_cylinder_length.md` — maximum cylinder length depends on radius via
  bending mode resonance ($L_\text{max} \propto r^{3/4}$). O'Neill's $L/D = 5$ as
  upper limit. Constraint: $L \leq 75.22 \cdot r^{3/4}$

**Constraints implemented (9 new → 18 total):**
- [x] **Cylinder length limit** — $L_\text{max} = C \cdot r^{3/4}$ from bending mode analysis
- [x] **Rotational stability** — $I_z/I_x \geq 1.2$; single cylinders limited to $L < 1.3r$;
  counter-rotating pair relaxes to $L < 10r$ (Globus and Arora 2007)
- [x] **Spin-up energy** — $E = \frac{1}{2}I\omega^2$ with configurable power and time budget
- [x] **Structural hoop stress** — $\sigma = \rho \omega^2 r^2 + Pr/t$ with safety factor ≥ 2.0
- [x] **Agriculture area vs. population** — food self-sufficiency; diet multiplier for animal protein
- [x] **Thermal management** — radiator area vs. solar input through windows + internal waste heat
- [x] **Energy budget** — solar panel area on end caps vs. colony demand (5 kW/person)
- [x] **Water recycling efficiency** — closed-loop budget; ≥98% required (ISS BPA milestone 2024)
- [x] **Micrometeorite reliability** — Poisson model, Grün 1985 flux; purpose-built shield → ~1 hit/yr

**Deferred (not blocking):**
- Mirror diagrams — previous exploration diagrams need correction; purely cosmetic/documentation
- L5 point documentation — why L5 is preferred over L4, HEO, etc.; purely educational

**3D model enhancements (deferred):**
- Ring ribs (circumferential frames every ~50–100 m)
- Gravity gradient shading (color gradient from rim to axis)
- External mirrors (3 hinged panels outside windows)
- Axial spine / docking ports

---

# Month-by-Month Plan

## Month 1: Rotation & Artificial Gravity ✅
Checkpoint achieved: Can explain why large radius is required ($a = \omega^2 r$).

## Month 2: Human Constraints ✅
Checkpoint achieved: "Safe operating zone" defined → [982m, 9,177m] at 1g.

## Month 3: Biological Constraints & System Scaling ✅
Checkpoint achieved: Binding biological constraints identified (radiation shielding
dominates mass); mass budget quantified via `construction_material_estimates.md`.

## Month 4: Uncertainty Modeling ✅
Checkpoint achieved: Monte Carlo probability distributions; variance decomposition
identifies cross-coupling and radiation as dominant uncertainties.

## Month 5–6: Integrated Model & Visualization ✅
Checkpoint achieved: 18-constraint interactive web dashboard operational.

## Month 12: Publish / Share ✅
Checkpoint achieved: Parametric feasibility model with validated parameters,
full literature review, interactive demo, and structured future research roadmap.

---

# What "Success" Looks Like

By Month 3: ✅ Model rejects $r < 982$ m at 1g in < 1 second across 9 constraints.

By Month 6: ✅ Full scorecard for any design point; sensitivity analysis; Monte Carlo
confidence intervals; interactive demo for exploration.

By Month 12: ✅ 18-constraint model validated against published literature; documented
in `plans/literature_review_human_factors.md` and `plans/literature_review_structural.md`;
future research directions identified and prioritized.

---

# Key Principle

Simulation is not prediction.

Simulation is:
- Constraint discovery
- Sensitivity analysis
- Assumption testing

---

# Future Research Directions

The 18-constraint model covers all primary first-principles feasibility boundaries.
The following gaps were identified via literature review and are candidates for
future development.

## Priority: High — Physically Binding

### Thermal Fatigue from Day/Night Cycling
The habitat orbits Earth/Sun and experiences cyclic thermal loading as windows open
and close to sunlight. At L5, orbital period is ~1 year; if the cylinder's own rotation
creates a "day" cycle, the hull sees ΔT ≈ 150–300 K per revolution. High-cycle
fatigue at these temperatures limits structural lifetime and is not captured in the
current static hoop stress model.

- **What to add:** Cyclic stress amplitude model; fatigue life estimation (S-N curves
  for steel/CFRP); interaction with micrometeorite damage accumulation.
- **Key reference:** Space station thermal cycling literature (ISS truss); CFRP
  fatigue behavior in vacuum.

### Closed Ecosystem: CO₂/O₂ Mass Balance
The Biosphere 2 lesson: O₂ dropped from 21% to 14% in 16 months at 200,000 m³
due to soil microbe respiration and CO₂ absorption by unsealed concrete. Atmospheric
homeostasis is an active control problem, not a passive equilibrium. The current
`AtmosphereConstraint` checks static pO₂ but not the dynamic balance rate.

- **What to add:** CO₂/O₂ production/consumption model; minimum plant biomass
  required to close the loop; soil microbial carbon sink; buffer volume for transients.
- **Key reference:** MELiSSA project (ESA); Biosphere 2 post-mortem analyses.

### Cumulative Hull Pressure Loss
Micrometeorite impacts create microcracks. Each individual impact is non-lethal,
but cumulative porosity raises the habitat's slow-leak rate. The current model
counts "penetrating" impacts (catastrophic) but ignores sub-threshold damage that
accumulates into a continuous pressure loss requiring active repressurisation.

- **What to add:** Sub-threshold damage accumulation model; pressure loss rate as
  a function of integrated flux and impact energy distribution; required active
  make-up pressure rate; comparison to ISRU gas supply capability.
- **Key reference:** Christiansen et al. 2009; NASA Hypervelocity Impact Technology.

## Priority: Medium — Second-Order Engineering

### Non-Loop Water Losses
The current water recycling model checks ECLSS loop efficiency (0.98). Actual
habitat water loss is higher because hygiene wipes, contaminated water, and
biological outputs bypass the recovery system. For a 8,000-person colony, even
1% of daily demand escaping the loop is ~58 t/year — manageable by ISRU but not
currently modelled.

- **What to add:** Disposal-path fraction as a tunable parameter; effective
  whole-habitat efficiency = ECLSS efficiency × loop fraction.

### Redundancy and Repair Margins
All current constraints check "nominal" operation. A resilient colony needs
redundancy (N+1 subsystems), repair capability, and graceful degradation modes.
The structural safety factor (2.0) partially captures this, but life support,
water, and power constraints have no redundancy budget.

- **What to add:** Required redundancy multiplier per subsystem; minimum spare
  parts mass; mean time to repair assumptions.

### Population Dynamics and Growth
The minimum viable population (MVP) constraint checks a static floor (98 people)
but does not model growth trajectories, age structure, or birth/death rate. A
colony starting at 1,000 people has very different long-term genetic outcomes than
one starting at 10,000. Smith (2014) argues 14,000–44,000 is needed without
managed breeding.

- **What to add:** Simple demographic model (cohort-based); inbreeding coefficient
  trajectory; required initial population for given genetic health target after
  N generations.

## Out of Scope (Insufficient Data or Non-Parametric)

| Topic | Reason |
|-------|--------|
| **Biological validation at partial gravity** | No multi-month human data below 0.38g; Mars and Moon missions would be required before constraining a model |
| **Psychological architecture** | Highly individual; HERA and Antarctic isolation studies exist but do not translate to design parameters |
| **Manufacturing and supply chain closure** | Depends on technology roadmap (asteroid mining, additive manufacturing in space); too speculative for a physics model |
| **Child development and reproduction** | Essentially no data on fetal development in partial gravity; cannot model until animal experiments at Moon/Mars gravity |
| **Political and governance constraints** | Not a physics problem |

---

# References

See `plans/literature_review_human_factors.md` and
`plans/literature_review_structural.md` for full citation lists with verdicts
on each parameter value used in the model.
