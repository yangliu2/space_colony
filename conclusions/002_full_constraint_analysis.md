# Full 6-Constraint Habitat Feasibility Analysis

**Date:** 2026-03-19  
**Model version:** habitat-constraints 0.1.0 (Phase 2)  
**Constraints:** vestibular (RPM), gravity level, gravity gradient, Coriolis effect, cross-coupled rotation, structural rim speed  
**Experiment script:** `models/habitat_constraints/experiments/run_phase2_analysis.py`

---

## Summary

Adding Coriolis, cross-coupled rotation, and structural rim speed constraints fundamentally changes the picture from Phase 1. The minimum viable radius at 1g jumps from **224m to 982m**, driven by cross-coupled angular acceleration from head turns. The feasible design band is now **[982m, 9177m]** — bounded below by vestibular cross-coupling and above by structural rim speed. O'Neill's 3,200m sits comfortably in the middle with margins on every constraint.

---

## Phase 1 → Phase 2 Comparison

| Metric | Phase 1 (3 constraints) | Phase 2 (6 constraints) | Change |
|--------|------------------------|------------------------|--------|
| Min radius at 1g | 224m | 982m | **+4.4×** |
| Max radius at 1g | ∞ | 9,177m | Now bounded |
| Binding lower constraint | Vestibular (2 RPM) | Cross-coupling (6 deg/s²) | New constraint dominates |
| Binding upper constraint | None | Rim speed (300 m/s) | New upper bound |
| O'Neill margin (tightest) | RPM: 74% | Cross-coupling: 45% | Reduced but still comfortable |

---

## Experiment Results

### 1. Full Constraint Map at 1g

| Radius (m) | RPM  | Rim Speed (m/s) | Result | Failing Constraints |
|------------|------|------------------|--------|---------------------|
| 100        | 2.99 | 31.3             | FAIL   | vestibular, gradient, cross-coupling |
| 200        | 2.11 | 42.0             | FAIL   | vestibular, cross-coupling |
| 300        | 1.73 | 54.2             | FAIL   | cross-coupling |
| 500        | 1.34 | 70.0             | FAIL   | cross-coupling |
| 750        | 1.09 | 85.7             | FAIL   | cross-coupling |
| **982**    | **0.95** | **98.1**     | **PASS** | — |
| 1,000      | 0.95 | 99.0             | PASS   | — |
| 3,200      | 0.53 | 177.1            | PASS   | — |
| 5,000      | 0.42 | 221.4            | PASS   | — |
| 8,000      | 0.33 | 280.0            | PASS   | — |
| 9,177      | 0.31 | 300.0            | PASS   | — (at rim speed limit) |
| 10,000     | 0.30 | 313.2            | FAIL   | rim_speed |

**Feasible design band: r ∈ [982m, 9,177m] at 1g.**

The constraint "waterfall" as radius increases:
1. **r < 180m:** Vestibular + gradient + cross-coupling all fail
2. **180m ≤ r < 225m:** Gradient passes, vestibular + cross-coupling fail
3. **225m ≤ r < 982m:** Vestibular passes, only cross-coupling fails
4. **982m ≤ r ≤ 9,177m:** ALL PASS — feasible region
5. **r > 9,177m:** Rim speed fails

### 2. Constraint Transition Points

| Constraint | Becomes Feasible At | Becomes Infeasible At |
|------------|--------------------|-----------------------|
| Gravity gradient | ~200m | — |
| Vestibular | ~225m | — |
| Cross-coupling | ~982m | — |
| Rim speed | — (always feasible below) | ~9,177m |
| Gravity level | — (always feasible at 1g) | — |
| Coriolis | — (always feasible at 0.25 threshold) | — |

**Cross-coupling is the last constraint to become feasible and thus determines the minimum viable radius.**

### 3. Feasible Band Across Gravity Levels

| Target Gravity | Min Radius (m) | Max Radius (m) | Band Width (m) |
|----------------|-----------------|-----------------|-----------------|
| 0.3g           | 294             | 30,591          | 30,297          |
| 0.4g           | 393             | 22,943          | 22,550          |
| 0.5g           | 490             | 18,355          | 17,864          |
| 0.6g           | 589             | 15,296          | 14,707          |
| 0.7g           | 687             | 13,110          | 12,424          |
| 0.8g           | 785             | 11,472          | 10,686          |
| 0.9g           | 883             | 10,197          | 9,314           |
| 1.0g           | 982             | 9,177           | 8,196           |

**Key findings:**
- Lower gravity targets dramatically expand the feasible band on both ends
- At 0.3g, you can build as small as 294m (vs 982m at 1g) — a 3.3× reduction
- The upper bound also expands because lower gravity → lower omega → lower rim speed at same radius
- The band width at 0.5g (17,864m) is more than double that at 1g (8,196m)

### 4. Sensitivity Analysis (±20% Perturbation)

**Baseline minimum radius at 1g: 982m**

| Parameter | −20% Value | +20% Value | Radius at −20% | Radius at +20% | Spread (m) |
|-----------|------------|------------|-----------------|-----------------|------------|
| **max_cross_coupling_deg_s2** | 4.8 | 7.2 | 1,533m | 682m | **851m** |
| **head_turn_rate_deg_s** | 48 | 72 | 628m | 1,413m | **785m** |
| max_gravity_g | 0.8 | 1.2 | N/A* | 982m | — |
| max_comfortable_rpm | 1.6 | 2.4 | 982m | 982m | 0m |
| max_gravity_gradient_pct | 0.8 | 1.2 | 982m | 982m | 0m |
| max_coriolis_ratio | 0.2 | 0.3 | 982m | 982m | 0m |
| max_rim_speed_m_s | 240 | 360 | 982m | 982m | 0m |
| person_height_m | 1.44 | 2.16 | 982m | 982m | 0m |
| running_speed_m_s | 2.4 | 3.6 | 982m | 982m | 0m |

*\*At max_gravity_g = 0.8, targeting 1.0g is infeasible by definition.*

**Only two parameters matter: cross-coupling threshold and head turn rate.** Everything else is dominated. This is a dramatic shift from Phase 1 where RPM tolerance was the key unknown.

### 5. Cross-Coupling Deep Dive

Minimum feasible radius (m) as a function of head turn rate and adaptation threshold:

| Head Turn Rate | 3 deg/s² (unadapted) | 6 deg/s² (adapted) | 10 deg/s² (well-adapted) | 15 deg/s² (trained) |
|----------------|----------------------|---------------------|---------------------------|---------------------|
| 30°/s (slow)   | 982                  | 245                 | 224                       | 224                 |
| 45°/s (normal) | 2,207                | 552                 | 224                       | 224                 |
| 60°/s (fast)   | 3,923                | 982                 | 354                       | 224                 |
| 90°/s (quick)  | **infeasible**       | 2,207               | 795                       | 354                 |
| 120°/s (snap)  | **infeasible**       | 3,923               | 1,413                     | 628                 |

**Key findings:**
- For unadapted humans (3 deg/s²) with fast head turns (60°/s), you need r ≥ 3,923m — *larger than O'Neill's design*
- For adapted crew (6 deg/s²) with normal head turns (45°/s), you can go as small as 552m
- Snap head turns (120°/s) at unadapted thresholds make the entire design space infeasible (cross-coupling exceeds limit even at r = ∞ because the rotation period floor is ~0.05 rad/s minimum to produce any gravity)
- **Training and adaptation are not optional — they are structural requirements**

### 6. O'Neill 3,200m Scorecard

| Constraint | Value | Limit | Margin | Status |
|------------|-------|-------|--------|--------|
| Vestibular | 0.53 RPM | 2.0 RPM | 74% | ✓ |
| Gravity level | 1.00g | [0.3, 1.0]g | at target | ✓ |
| Gravity gradient | 0.056% | 1.0% | 94% | ✓ |
| Coriolis (running) | 3.4% of g | 25% | 86% | ✓ |
| **Cross-coupling** | **3.32 deg/s²** | **6.0 deg/s²** | **45%** | ✓ |
| Rim speed | 177 m/s | 300 m/s | 41% | ✓ |

Cross-coupling has the tightest margin at 45%. Notably, at 3.32 deg/s², O'Neill's design *exceeds* the unadapted threshold of 3 deg/s². This means even O'Neill's design requires some crew adaptation — it was never intended for completely naive passengers.

---

## Conclusions

### 1. Cross-Coupled Rotation Is the Dominant Constraint

The minimum viable radius at 1g jumped from 224m (Phase 1) to 982m (Phase 2), driven entirely by cross-coupled angular acceleration from head turns. This constraint was not in the original Phase 1 analysis. **The previous 224m estimate was dangerously optimistic.**

### 2. The Design Space Is Now Bounded Above and Below

Phase 1 only had a lower bound. With rim speed added, the feasible region is a finite band: **[982m, 9,177m] at 1g**. This is the engineering "sweet spot" for rotating habitats. Designs outside this range are physically impossible given the constraints.

### 3. Two Parameters Dominate All Others

Only `max_cross_coupling_deg_s2` and `head_turn_rate_deg_s` meaningfully affect the minimum radius. All other parameters (RPM tolerance, gradient, Coriolis ratio, person height, running speed) have zero impact at ±20% perturbation because cross-coupling completely dominates.

### 4. Crew Adaptation Is a Structural Design Requirement

Even O'Neill's 3,200m design produces 3.3 deg/s² cross-coupling, exceeding the unadapted threshold of 3 deg/s². Smaller habitats absolutely require adapted crew. The adaptation schedule and failure modes need to be treated as engineering constraints, not optional training.

### 5. Partial Gravity Transforms the Design Space

At 0.5g, the minimum radius drops to 490m and the maximum extends to 18,355m. If partial gravity is biologically sufficient, the engineering becomes dramatically easier.

### 6. The Coriolis Constraint Is Non-Binding at Default Thresholds

With a 25% max ratio, Coriolis is always satisfied when cross-coupling passes. However, tightening the Coriolis threshold to ~5% would push the minimum radius higher. The default 25% is generous — real comfort may require <10%.

---

## Limitations

1. **Cross-coupling threshold uncertainty.** The 6 deg/s² "adapted" threshold is based on limited centrifuge studies. Long-term (years) adaptation data does not exist.
2. **Head turn rate is activity-dependent.** 60 deg/s is a normal turn; sports, startling, or childplay can reach 120+ deg/s.
3. **No coupled optimization.** Constraints are evaluated independently. In reality, Coriolis during a head turn creates a compound effect.
4. **Rim speed limit is material-dependent.** 300 m/s assumes steel. Carbon fiber could extend to 500+ m/s, pushing the upper bound to ~25,000m.
5. **No atmospheric/thermal constraints.** A spinning atmosphere creates Coriolis winds and thermal gradients not yet modeled.

---

## Next Steps

1. **Implement atmospheric Coriolis constraint** — wind patterns in a rotating cylinder
2. **Add material-parameterized structural model** — steel, aluminum, carbon fiber, each with different rim speed limits
3. **Model adaptation curves** — how cross-coupling tolerance changes over days/weeks
4. **Multi-objective analysis** — not just "is it feasible?" but "how comfortable on a 0-10 scale?"
5. **Couple with mass/cost model** — translate radius bounds to structural mass and launch cost
