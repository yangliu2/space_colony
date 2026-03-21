# Phase 3: Biological Constraints, Monte Carlo, and Mass Budget

**Date:** 2026-03-20
**Model version:** habitat-constraints 0.1.0 (Phase 3)
**Constraints:** 6 rotational + 3 biological = 9 total
**Experiment script:** `models/habitat_constraints/experiments/run_phase3_analysis.py`
**Plots:** `models/habitat_constraints/experiments/output/`

---

## Summary

Phase 3 extends the model in three directions: (1) biological constraints (radiation, atmosphere, population), (2) Monte Carlo simulation to quantify uncertainty, and (3) mass budget estimation. The biological constraints do not change the feasible radius band — rotational dynamics remain dominant. But they reveal that **radiation shielding is the single largest mass driver**, consuming 82.8 Mt for the minimum viable cylinder. The Monte Carlo analysis shows the feasible band is **robust**: 96.4% of random parameter samples produce a feasible region, but the minimum radius varies widely (P5 = 286m, P95 = 3,630m), confirming that **cross-coupling threshold and head turn rate are the critical unknowns**.

---

## Phase 2 → Phase 3 Comparison

| Metric | Phase 2 (6 constraints) | Phase 3 (9 constraints) | Notes |
|--------|------------------------|------------------------|-------|
| Constraint count | 6 rotational | 9 (+ radiation, atmo, population) | Biological added |
| Min radius at 1g | 982m | 982m | **Unchanged** — rotational still binding |
| Max radius at 1g | 9,177m | 9,177m | **Unchanged** |
| Feasible band | [982m, 9,177m] | [982m, 9,177m] | Biological constraints orthogonal to radius |
| New insight | — | Shielding = 82.8 Mt for minimum cylinder | Mass budget quantified |
| Monte Carlo feasibility | — | 96.4% of trials feasible | Band is robust |

---

## Experiment Results

### 1. Full 9-Constraint Scorecard

Both reference designs pass all 9 constraints:

| Constraint | Minimum Viable (982m × 2km) | O'Neill (3,200m × 32km) |
|------------|:--:|:--:|
| Vestibular (RPM) | ✓ 0.95 RPM (margin: 1.05) | ✓ 0.53 RPM (margin: 1.47) |
| Gravity level | ✓ 1.0g | ✓ 1.0g |
| Gravity gradient | ✓ 0.18% | ✓ 0.06% |
| Coriolis | ✓ ratio 0.061 | ✓ ratio 0.034 |
| Cross-coupling | ✓ 6.0 deg/s² (margin: 0.004) | ✓ 3.3 deg/s² (margin: 2.7) |
| Rim speed | ✓ 98 m/s (margin: 67%) | ✓ 177 m/s (margin: 41%) |
| Radiation shielding | ✓ 4,500 kg/m² | ✓ 4,500 kg/m² |
| Atmosphere ($pO_2$) | ✓ 21.3 kPa | ✓ 21.3 kPa |
| Population | ✓ 8,000 (min: 98) | ✓ 1,000,000 (min: 98) |

**Key observation:** The minimum viable cylinder has near-zero margin on cross-coupling (0.004 deg/s²). This is the tightest constraint in the entire system. At 982m radius, it's barely feasible — any increase in head turn rate or decrease in crew adaptation would push it infeasible.

### 2. Atmosphere Feasibility Map

The atmosphere constraint is independent of radius — it depends only on pressure and $O_2$ fraction. The safe operating region for $pO_2 \in [16, 50]$ kPa:

| Total Pressure | Min $O_2$ Fraction | Max $O_2$ Fraction | Feasible Range |
|---------------|-------------------|-------------------|----------------|
| 51.0 kPa (SP-413) | 31.4% | 98.0% | Wide — but 21% Earth-normal fails! |
| 56.5 kPa (NASA exploration) | 28.3% | 88.5% | Wide |
| 101.3 kPa (Earth) | 15.8% | 49.4% | Narrow — Earth-normal (21%) just inside |

**Critical finding:** At half-atmosphere (51 kPa), Earth-normal 21% $O_2$ fails — $pO_2$ = 10.7 kPa, well below the 16 kPa hypoxia threshold. The SP-413 design used 44.5% $O_2$ at 51 kPa for this reason ($pO_2$ = 22.7 kPa). This means **you cannot simply halve the pressure** without enriching the $O_2$ percentage.

At full atmosphere (101.3 kPa), Earth-normal 21% $O_2$ gives $pO_2$ = 21.3 kPa — safely inside the range. But 50% $O_2$ at full pressure already exceeds the toxicity limit ($pO_2$ = 50.6 kPa).

**Implication:** Lower pressure saves structural mass but **locks you into a narrower $O_2$ management window** and **increases fire risk** from elevated $O_2$ percentage. For a permanent habitat, full Earth atmosphere is the safest choice.

### 3. Monte Carlo Simulation (500 Trials)

Varied 6 key parameters simultaneously with normal distributions:

| Parameter | Mean | Std Dev | Clip Range |
|-----------|------|---------|------------|
| $\omega_{\max}$ (RPM) | 2.0 | 0.5 | [0.5, 6.0] |
| Cross-coupling threshold (deg/s²) | 6.0 | 2.0 | [2.0, 15.0] |
| Head turn rate (deg/s) | 60.0 | 15.0 | [20, 120] |
| Max Coriolis ratio | 0.25 | 0.05 | [0.05, 0.50] |
| Max rim speed (m/s) | 300.0 | 50.0 | [150, 600] |
| Max gravity gradient (%) | 1.0 | 0.3 | [0.3, 5.0] |

**Results:**

| Metric | Value |
|--------|-------|
| Feasibility rate | **96.4%** |
| Min radius P5 | 286m |
| Min radius P25 | ~550m |
| Min radius P50 (median) | **971m** |
| Min radius P95 | 3,630m |
| Max radius P50 | 9,274m |

**Interpretation:**

- **The median minimum radius (971m) almost exactly matches the deterministic baseline (982m).** The Monte Carlo confirms the Phase 2 result is not an outlier — it's the central tendency.
- **The P5–P95 range spans more than 10× (286m to 3,630m).** This enormous spread comes almost entirely from uncertainty in the cross-coupling threshold. If humans adapt better than expected (threshold > 10 deg/s²), much smaller habitats become feasible. If they don't adapt (threshold = 3 deg/s²), you need radii > 3,000m.
- **96.4% feasibility rate** means only 3.6% of random parameter samples yield no feasible region at all. These are extreme cases (very low RPM tolerance + very low cross-coupling threshold simultaneously).
- **The upper bound (max radius) is less variable** than the lower bound, because rim speed has a tighter distribution. The median max radius of 9,274m is consistent with the deterministic 9,177m.

### 4. Sensitivity Analysis (Extended)

The top 3 most impactful parameters (±20% perturbation):

| Rank | Parameter | Radius Range | Spread |
|------|-----------|-------------|--------|
| 1 | `max_gravity_g` | infeasible at −20% | ∞ (breaks model) |
| 2 | `max_cross_coupling_deg_s2` | [682m, 1,533m] | 851m |
| 3 | `head_turn_rate_deg_s` | [628m, 1,413m] | 785m |

**`max_gravity_g`** shows infinite spread because decreasing the maximum acceptable gravity below 0.8g while targeting 1.0g makes all designs infeasible by definition. This is not a real sensitivity — it's a constraint definition issue. The real actionable sensitivities are cross-coupling threshold and head turn rate, which together dominate the feasible band width.

**All other parameters have zero spread** — meaning ±20% variation in RPM tolerance, gradient tolerance, Coriolis ratio, and rim speed does not change the minimum feasible radius at 1g. These are non-binding constraints with large margins.

### 5. Mass Budget

#### Minimum Viable Cylinder ($r = 982$ m, $L = 2{,}000$ m)

| Component | Mass (Mt) | Fraction |
|-----------|-----------|----------|
| Structural shell (steel, SF=3) | 3.3 | 3.8% |
| **Radiation shielding** (4,500 kg/m²) | **82.8** | **95.0%** |
| Atmosphere (101.3 kPa) | 0.5 | 0.6% |
| Soil (50% area, 0.75m depth) | 0.5 | 0.5% |
| Water | 0.0 | ~0% |
| **Total** | **~87 Mt** | |

#### O'Neill Island Three ($r = 3{,}200$ m, $L = 32{,}000$ m)

| Component | Mass (Mt) | Fraction |
|-----------|-----------|----------|
| Structural shell | 73.4 | 2.2% |
| **Radiation shielding** | **3,184.8** | **95.6%** |
| Atmosphere | 17.2 | 0.5% |
| Soil | 52.4 | 1.6% |
| Water | 3.1 | 0.1% |
| **Total** | **~3,331 Mt** | |

**The overwhelming dominance of shielding mass** (95%+ in both scenarios) means that:

1. Structural optimization (better materials, thinner walls) barely matters for total mass
2. Atmospheric composition choices (half vs. full atmosphere) barely matter
3. **The only way to significantly reduce total mass is to reduce shielding requirements** — either through location choice (inside the Van Allen belts), active magnetic shielding, or accepting higher radiation dose rates

This echoes the SP-413 finding from 1975: shielding dominated the Stanford torus mass budget at 9.9 Mt out of 10.5 Mt total (94%).

---

## Visualization Outputs

All plots saved to `models/habitat_constraints/experiments/output/`:

| Plot | Description |
|------|-------------|
| `feasible_region.png` | Constraint map: radius × gravity, colored by failing constraint |
| `radius_sweep.png` | Pass/fail per constraint across 50–15,000m radius at 1g |
| `tornado_chart.png` | Sensitivity tornado showing parameter impact on min radius |
| `monte_carlo_histogram.png` | Distribution of min radius and feasible band width (500 trials) |
| `mass_budget_minimum.png` | Mass breakdown for 982m × 2km cylinder |
| `mass_budget_oneill.png` | Mass breakdown for 3,200m × 32km cylinder |

---

## Key Findings

1. **Biological constraints are orthogonal to rotational constraints.** Radiation, atmosphere, and population do not change the feasible radius band — they impose requirements on shielding mass, atmospheric composition, and minimum population that are independent of cylinder geometry.

2. **Radiation shielding dominates the mass budget at 95%.** Everything else — structure, atmosphere, soil, water — is rounding error by comparison. This is the single most important engineering challenge.

3. **The feasible band is robust under uncertainty.** 96.4% of Monte Carlo trials find a feasible region. The median minimum radius (971m) matches the deterministic result (982m). The design space is not fragile.

4. **But the minimum radius is highly uncertain.** The P5–P95 range spans 286m to 3,630m, a 12.7× range driven almost entirely by uncertainty in cross-coupling tolerance. Resolving this uncertainty — through human centrifuge experiments at relevant rotation rates — would dramatically narrow the design space.

5. **Half-atmosphere requires O₂ enrichment.** You cannot simply use Earth-normal 21% O₂ at half pressure — the pO₂ drops below the hypoxia threshold. This was known in 1975 (SP-413 used 44.5% O₂) but is a critical design constraint that interacts with fire safety.

6. **The minimum viable cylinder masses ~87 Mt.** This is 8× the SP-413 Stanford torus (10.5 Mt) but in the same order of magnitude. The O'Neill cylinder at ~3,331 Mt is two orders of magnitude larger and requires asteroid-scale mining operations.

---

## What This Means for the Project

The constraint model now has **9 constraints across 2 domains** (rotational dynamics + biological). The Monte Carlo simulation confirms the results are stable. The next priorities are:

1. **Resolve the cross-coupling uncertainty** — this is the single most valuable piece of information for habitat design
2. **Investigate shielding alternatives** — active magnetic shielding, Van Allen belt placement (Globus and Marotta 2018), or acceptable dose rate trade-offs
3. **Add thermal, agricultural, and energy constraints** (Phase 6) to complete the integrated model
4. **Build interactive visualization** for parameter exploration

---

## References

- Johnson, Richard D., and Charles Holbrow, editors. *Space Settlements: A Design Study*. NASA SP-413, National Aeronautics and Space Administration, 1977.

- Globus, Al, and Tom Marotta. "The High Frontier: An Easier Way." *NSS Space Settlement Journal*, 2018.

- Marin, Frédéric, and Camille Beluffi. "Minimum Number of Settlers for Survival on Another Planet." *Scientific Reports*, vol. 10, 2020, article 9700. *Nature*, https://www.nature.com/articles/s41598-020-66740-0.

- O'Neill, Gerard K. *The High Frontier: Human Colonies in Space*. William Morrow and Company, 1977.
