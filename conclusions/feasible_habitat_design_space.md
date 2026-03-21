# Feasible Habitat Design Space

## Summary of Current Model (Phases 1–5)

This document synthesizes all constraint analysis performed to date into a single reference for the feasible design space of an O'Neill-type rotating space habitat. The model evaluates 9 independent constraints across rotational dynamics, human physiology, and environmental life support.

---

## 1. Constraints Implemented

### Rotational / Structural (Phase 1–2)

| # | Constraint | Parameter | Threshold | Physics |
|---|-----------|-----------|-----------|---------|
| 1 | Vestibular comfort | RPM | $\leq 2.0$ rpm | Semicircular canal stimulation from rotation rate |
| 2 | Gravity level | $g_{\text{eff}} = \omega^2 r$ | $0.3g \leq g \leq 1.0g$ | Centripetal acceleration at rim |
| 3 | Gravity gradient | $\Delta g / g = h/r$ | $\leq 1.0\%$ | Head-to-foot gravity difference |
| 4 | Coriolis effect | $a_{\text{cor}} / g$ | $\leq 0.25$ | Lateral force during radial motion |
| 5 | Cross-coupling | $\dot{\alpha} \times \omega$ | $\leq 6.0$ °/s² | Vestibular cross-coupled angular acceleration |
| 6 | Rim speed | $v = \omega r$ | $\leq 300$ m/s | Hoop stress limited by structural material |

### Biological / Environmental (Phase 3)

| # | Constraint | Parameter | Threshold | Physics |
|---|-----------|-----------|-----------|---------|
| 7 | Radiation shielding | Areal density | $\geq 4{,}500$ kg/m² | GCR/SPE attenuation to $< 0.5$ rem/yr |
| 8 | Atmosphere | $p_{\text{O}_2}$ | $16$–$50$ kPa | Partial pressure of oxygen for human respiration |
| 9 | Population | Inhabitants | $\geq 98$ | Minimum viable population for genetic diversity |

---

## 2. Feasible Design Band

### At 1g Target Gravity

$$\boxed{r_{\min} = 982 \text{ m}, \quad r_{\max} = 9{,}177 \text{ m}}$$

| Boundary | Value | Binding Constraint |
|----------|-------|-------------------|
| Lower (minimum radius) | 982 m | Cross-coupling (6.0 °/s²) |
| Upper (maximum radius) | 9,177 m | Rim speed (300 m/s) |

The feasible band spans nearly one order of magnitude. Below 982 m, crew members performing normal head turns while rotating experience disorienting cross-coupled angular accelerations. Above 9,177 m, rim velocity exceeds what steel structures can sustain against hoop stress.

### Across Gravity Levels

| Target Gravity | $r_{\min}$ (m) | $r_{\max}$ (m) | Band Width (m) |
|---|---|---|---|
| 0.3g | 294 | 30,591 | 30,297 |
| 0.5g | 490 | 18,355 | 17,864 |
| 0.8g | 786 | 11,472 | 10,686 |
| 1.0g | 982 | 9,177 | 8,196 |

Lower gravity targets dramatically expand the feasible region. At 0.5g the minimum radius drops to 490 m — less than half of the 1g requirement. Whether 0.5g suffices for long-term human health remains an open question.

---

## 3. Constraint Activation Waterfall (at 1g)

As radius increases from small to large, constraints "turn off" in sequence:

| Radius Range | Failing Constraints |
|---|---|
| $r < 180$ m | Vestibular + gravity gradient + cross-coupling |
| $180 \leq r < 225$ m | Vestibular + cross-coupling |
| $225 \leq r < 982$ m | Cross-coupling only |
| $982 \leq r \leq 9{,}177$ m | **None — all pass** |
| $r > 9{,}177$ m | Rim speed |

Cross-coupling is the last constraint to be satisfied as radius grows, making it the binding lower bound. Rim speed is the first to fail as radius grows large.

---

## 4. Reference Design Scorecard

### O'Neill Island Three ($r = 3{,}200$ m, $L = 32$ km)

| Constraint | Value | Threshold | Margin |
|---|---|---|---|
| Vestibular | 0.53 rpm | 2.0 rpm | 74% |
| Gravity level | 1.0g | 0.3–1.0g | — |
| Gravity gradient | 0.056% | 1.0% | 94% |
| Coriolis (running) | 3.4% of $g$ | 25% | 86% |
| Cross-coupling | 3.32 °/s² | 6.0 °/s² | 45% |
| Rim speed | 177 m/s | 300 m/s | 41% |
| Radiation shielding | 4,500 kg/m² | 4,500 kg/m² | 0% (by design) |
| Atmosphere ($p_{\text{O}_2}$) | 21.3 kPa | 16–50 kPa | pass |
| Population | 8,000 | 98 | 8,000% |

Cross-coupling and rim speed have the tightest margins at 45% and 41% respectively. All other constraints are satisfied with wide margins.

### Minimum Viable Cylinder ($r = 982$ m, $L = 2$ km)

| Constraint | Value | Threshold | Margin |
|---|---|---|---|
| Vestibular | 0.95 rpm | 2.0 rpm | 53% |
| Gravity gradient | 0.18% | 1.0% | 82% |
| Coriolis (running) | 6.1% of $g$ | 25% | 76% |
| Cross-coupling | 6.0 °/s² | 6.0 °/s² | **~0%** |
| Rim speed | 98 m/s | 300 m/s | 67% |
| Radiation shielding | 4,500 kg/m² | 4,500 kg/m² | 0% (by design) |
| Atmosphere ($p_{\text{O}_2}$) | 21.3 kPa | 16–50 kPa | pass |
| Population | 8,000 | 98 | pass |

At the minimum viable radius, cross-coupling has **near-zero margin** — this is the binding constraint that defines the lower boundary.

---

## 5. Sensitivity Analysis

### Which Parameters Matter?

A ±20% perturbation of each human assumption parameter reveals which ones actually shift the feasible boundary:

| Parameter | $r_{\min}$ Range | Spread |
|---|---|---|
| `max_cross_coupling_deg_s2` | 682 – 1,533 m | 851 m |
| `head_turn_rate_deg_s` | 628 – 1,413 m | 785 m |
| All others | 982 m (unchanged) | 0 m |

**Only two parameters matter**: the cross-coupling tolerance threshold and the assumed head turn rate during daily activities. All other parameters (RPM limit, gravity gradient, Coriolis ratio, rim speed, person height, running speed) are non-binding at the 1g design point.

### Implication

Research priority should focus on:
1. Measuring cross-coupling thresholds in long-duration centrifuge studies
2. Characterizing typical head turn rates during daily life (not just lab conditions)

---

## 6. Monte Carlo Results (500 Trials)

Sampling all 6 key human assumption parameters from distributions around their nominal values:

| Statistic | Value |
|---|---|
| Feasibility rate | 96.4% |
| $r_{\min}$ — 5th percentile | 286 m |
| $r_{\min}$ — 25th percentile | ~550 m |
| $r_{\min}$ — median | 971 m |
| $r_{\min}$ — 95th percentile | 3,630 m |
| $r_{\max}$ — median | 9,274 m |

The P5–P95 range for minimum radius spans **286 m to 3,630 m** (12.7× spread), driven almost entirely by cross-coupling threshold uncertainty. The median (971 m) closely matches the deterministic result (982 m), confirming model stability.

---

## 7. Mass Budget

Radiation shielding dominates the mass budget at every scale.

### Minimum Viable Cylinder ($r = 982$ m, $L = 2$ km)

| Component | Mass (Mt) | Fraction |
|---|---|---|
| Structural shell (steel, SF=3) | 3.3 | 3.8% |
| **Radiation shielding** | **82.8** | **95.0%** |
| Atmosphere | 0.5 | 0.6% |
| Soil (50% area, 0.75 m depth) | 0.5 | 0.5% |
| **Total** | **~87** | |

### O'Neill Island Three ($r = 3{,}200$ m, $L = 32$ km)

| Component | Mass (Mt) | Fraction |
|---|---|---|
| Structural shell | 73.4 | 2.2% |
| **Radiation shielding** | **3,184.8** | **95.6%** |
| Atmosphere | 17.2 | 0.5% |
| Soil | 52.4 | 1.6% |
| Water | 3.1 | 0.1% |
| **Total** | **~3,331** | |

**Key insight**: Structural optimization is rounding error. The only way to meaningfully reduce habitat mass is to find alternatives to passive radiation shielding (active magnetic shielding, strategic orbital placement in Van Allen belts, or acceptance of higher dose rates).

---

## 8. Key Findings

1. **Cross-coupling dominates the lower bound.** The minimum feasible radius is set by vestibular cross-coupling, not RPM comfort or gravity gradient. This was not obvious before Phase 2 analysis.

2. **The feasible band is robust.** At 1g, the band spans 982–9,177 m with a 96.4% Monte Carlo feasibility rate. The O'Neill reference design (3,200 m) sits comfortably within this range.

3. **Only two parameters matter for the lower bound.** Cross-coupling threshold and head turn rate account for all sensitivity. Every other parameter is non-binding.

4. **Biological constraints are orthogonal.** Radiation, atmosphere, and population constraints do not change the feasible radius band — they are satisfied independently. However, radiation shielding dominates mass.

5. **Radiation shielding is 95% of total mass.** This is the single biggest engineering challenge and the primary target for mass reduction research.

6. **Lower gravity dramatically opens design space.** If 0.5g is adequate for human health, the minimum radius drops from 982 m to 490 m and the mass budget roughly halves.

7. **Crew adaptation is a structural requirement.** Head turn rate training can reduce minimum radius from 3,923 m to 245 m — a 16× reduction. This is not optional comfort training; it is load-bearing for structural sizing.

---

## 9. What This Model Does Not Cover

The following are identified for Phase 6 but not yet implemented:

| Domain | Why It Matters |
|---|---|
| Thermal management | Radiator area scales with population and sunlight exposure |
| Structural dynamics | Vibration modes, wobble, seismic-equivalent loads |
| Agriculture | Food self-sufficiency constrains minimum land area |
| Water recycling | Closed-loop efficiency determines water mass budget |
| Energy budget | Solar collection area, power distribution, day/night cycle |

These would add constraints to the model but are unlikely to change the rotational feasible band, which is dominated by human vestibular physiology. They will primarily affect mass budget and minimum cylinder length.

---

## 10. Interactive Exploration

The full constraint model is available as an interactive web application:

```bash
# Backend (port 8042)
cd models/habitat_constraints
uv run uvicorn habitat_constraints.api.main:app --host 127.0.0.1 --port 8042 --reload

# Frontend (port 5173)
cd demo
npm run dev
```

The dashboard provides:
- **Parameter sliders** for all 9 constraints with real-time evaluation
- **Constraint status panel** showing pass/fail with computed values
- **2D feasible region chart** showing the radius sweep
- **3D rotating O'Neill cylinder** with toggleable land/window strips, human figure, Coriolis arrows, gravity gradient rings, and rotation axis

The 3D model visualizes all constraint effects: cylinder color (green = feasible, red = infeasible), rotation speed proportional to $\omega$, human figure lean proportional to Coriolis ratio, and the O'Neill 3-land / 3-window alternating strip pattern.
