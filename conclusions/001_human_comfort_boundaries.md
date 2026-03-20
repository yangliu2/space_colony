# Human Comfort Boundaries in Rotating Habitats

**Date:** 2026-03-19  
**Model version:** habitat-constraints 0.1.0  
**Constraints used:** vestibular (RPM), gravity level (g-range), gravity gradient (head-to-foot)  
**Experiment script:** `models/habitat_constraints/experiments/run_boundary_analysis.py`

---

## Summary

The minimum viable radius for a 1g rotating habitat is **~224m**, driven entirely by the vestibular comfort limit of 2 RPM. Below this radius, humans cannot achieve Earth-normal gravity without spinning faster than the vestibular system tolerates. O'Neill's original 3,200m design operates with massive margins on every constraint.

---

## Experiment Results

### 1. Radius Sweep at 1g — Where Each Constraint Activates

| Radius (m) | RPM  | Rim Speed (m/s) | Period (s) | Vestibular | Gravity Level | Gravity Gradient |
|------------|------|------------------|------------|------------|---------------|------------------|
| 100        | 2.99 | 31.3             | 20.1       | FAIL       | PASS          | FAIL (1.8%)      |
| 180        | 2.23 | 42.0             | 26.9       | FAIL       | PASS          | PASS (1.0%)      |
| 224        | 2.00 | 46.9             | 30.0       | PASS       | PASS          | PASS (0.8%)      |
| 300        | 1.73 | 54.2             | 34.8       | PASS       | PASS          | PASS (0.6%)      |
| 500        | 1.34 | 70.0             | 44.9       | PASS       | PASS          | PASS (0.36%)     |
| 1,000      | 0.95 | 99.0             | 63.4       | PASS       | PASS          | PASS (0.18%)     |
| 3,200      | 0.53 | 177.1            | 113.5      | PASS       | PASS          | PASS (0.06%)     |
| 5,000      | 0.42 | 221.4            | 141.9      | PASS       | PASS          | PASS (0.04%)     |

**Constraint transition radii at 1g:**
- Gravity gradient becomes feasible at **~180m** (gradient drops below 1%)
- Vestibular becomes feasible at **~224m** (RPM drops below 2.0)
- Gravity level is always feasible when targeting exactly 1g

**The binding constraint at 1g is vestibular (RPM limit), not gravity gradient.**

### 2. Minimum Radius Across Gravity Levels

| Target Gravity | Min Radius (m) | RPM at Min Radius | Binding Constraint |
|----------------|-----------------|--------------------|--------------------|
| 0.3g           | 180             | 1.22               | Gravity gradient   |
| 0.4g           | 180             | 1.41               | Gravity gradient   |
| 0.5g           | 180             | 1.58               | Gravity gradient   |
| 0.6g           | 180             | 1.73               | Gravity gradient   |
| 0.7g           | 180             | 1.86               | Gravity gradient   |
| 0.8g           | 180             | 1.99               | Gravity gradient   |
| 0.9g           | 202             | 2.00               | Vestibular         |
| 1.0g           | 224             | 2.00               | Vestibular         |

**Key finding:** Below ~0.85g, the gravity gradient constraint (r >= 180m for 1.8m person at 1% max gradient) is the binding constraint, not vestibular comfort. The crossover happens because lower gravity targets require lower omega at the same radius, so RPM stays below 2.0. At 0.3g–0.8g, you can build as small as 180m and still pass all constraints.

This has a practical implication: if partial gravity (e.g. 0.5g) is acceptable for human health, the minimum habitat size drops from 224m to 180m — a **20% reduction in radius** and a significant reduction in structural mass.

### 3. RPM Threshold Sensitivity

| RPM Limit | Min Radius at 1g (m) | Binding Constraint at Min |
|-----------|----------------------|---------------------------|
| 1.0       | 895                  | Vestibular                |
| 1.5       | 398                  | Vestibular                |
| 2.0       | 224                  | Vestibular                |
| 2.5       | 180                  | Gravity gradient          |
| 3.0       | 180                  | Gravity gradient          |
| 4.0       | 180                  | Gravity gradient          |
| 6.0       | 180                  | Gravity gradient          |

**Key finding:** The RPM comfort threshold is the single most sensitive parameter in the model. Changing the assumed limit from 2.0 to 1.0 RPM quadruples the minimum radius (224m to 895m). Relaxing it to 2.5 RPM has no further effect — the gravity gradient constraint takes over at 180m.

This means: **if the true human RPM tolerance is 1.5 rather than 2.0, the minimum habitat nearly doubles in size.** The literature on vestibular comfort is sparse and mostly from short-duration centrifuge studies. This is the highest-priority unknown for habitat sizing.

### 4. Gravity Gradient Sensitivity

| Max Gradient (%) | Min Radius at 1g (m) | Binding Constraint |
|------------------|----------------------|--------------------|
| 0.25             | 720                  | Gravity gradient   |
| 0.50             | 361                  | Gravity gradient   |
| 1.00             | 224                  | Vestibular         |
| 2.00             | 224                  | Vestibular         |
| 3.00             | 224                  | Vestibular         |
| 5.00             | 224                  | Vestibular         |

**Key finding:** Tightening the gradient threshold below 1% dramatically increases minimum radius. At 0.25% (a strict comfort standard), the minimum radius jumps to 720m. Relaxing it beyond 1% has no effect — vestibular is already the binding constraint.

The gradient constraint only matters if we demand very uniform gravity. For a 1% threshold (1.8% difference between head and feet gravity at the boundary), the effect is imperceptible in daily life but may matter for precision activities, medical procedures, or long-term musculoskeletal health.

### 5. Person Height Sensitivity

| Height (m) | Min Radius at 1g (m) | Gradient at Min Radius (%) |
|------------|----------------------|----------------------------|
| 1.5        | 224                  | 0.67                       |
| 1.6        | 224                  | 0.71                       |
| 1.7        | 224                  | 0.76                       |
| 1.8        | 224                  | 0.80                       |
| 1.9        | 224                  | 0.85                       |
| 2.0        | 224                  | 0.89                       |
| 2.1        | 224                  | 0.94                       |

**Key finding:** Person height has negligible effect on the minimum feasible radius under current assumptions. This is because the vestibular constraint (224m) already dominates the gradient constraint (180m for h=1.8m). Even a 2.1m person only needs r >= 210m for gradient, still below the vestibular floor. Height would only matter if the gradient threshold were tightened below ~0.8%.

### 6. Boundary Analysis — What It Feels Like at the Edge

At the minimum feasible radius (r=224m, 2.0 RPM, 30-second rotation period):

| Metric | Value | Assessment |
|--------|-------|------------|
| Rotation rate | 2.00 RPM | At the vestibular comfort limit |
| Gravity at feet | 1.00g | Earth-normal |
| Gravity at head | 0.99g | 0.8% lighter — imperceptible |
| Rotation period | 30 seconds | One full rotation every 30s |
| Rim speed | 46.9 m/s (169 km/h) | Moderate structural requirement |
| Vestibular margin | 0.002 RPM | Essentially zero margin |

For comparison, at r=500m (a "comfortable" design):

| Metric | Value | Assessment |
|--------|-------|------------|
| Rotation rate | 1.34 RPM | 33% margin to vestibular limit |
| Gravity gradient | 0.36% | Imperceptible |
| Rotation period | 44.9 seconds | Slow, comfortable rotation |
| Rim speed | 70.0 m/s (252 km/h) | Higher structural load |

### 7. Coriolis Effect Preview (Not Yet a Formal Constraint)

Coriolis acceleration = 2 * omega * v_relative. Expressed as a fraction of effective gravity:

| Radius (m) | Walking (1.4 m/s) | Running (3.0 m/s) | Assessment |
|------------|-------------------|-------------------|------------|
| 100        | 8.9% of g         | 19.2% of g        | Severely disorienting |
| 224        | 6.0% of g         | 12.8% of g        | Noticeable, uncomfortable |
| 300        | 5.2% of g         | 11.1% of g        | Noticeable |
| 500        | 4.0% of g         | 8.6% of g         | Perceptible |
| 1,000      | 2.8% of g         | 6.1% of g         | Mildly perceptible |
| 3,200      | 1.6% of g         | 3.4% of g         | Barely noticeable |
| 5,000      | 1.3% of g         | 2.7% of g         | Negligible |

**Key finding:** Coriolis effects are perceptible at every radius tested. Even at the minimum feasible radius (224m), a runner experiences 12.8% lateral acceleration relative to gravity — equivalent to walking on a ~7-degree slope that switches direction when you turn around. At O'Neill's 3,200m, running Coriolis drops to 3.4% — still perceptible but manageable.

**When the Coriolis constraint is formally added with a 25% threshold, it will not tighten the minimum radius.** But at more conservative thresholds (e.g., 5% for walking comfort), it could push the minimum well above 224m.

---

## Conclusions

### 1. The Minimum Viable 1g Habitat is ~224m Radius

This is set by the vestibular RPM limit (2 RPM), not by gravity gradient. The habitat would spin once every 30 seconds at 2.00 RPM with essentially zero margin. This is a hard lower bound given current understanding of human vestibular tolerance.

### 2. The RPM Tolerance Is the Critical Unknown

The single parameter that most changes the answer is `max_comfortable_rpm`. Moving it from 2.0 to 1.0 quadruples the minimum radius. The existing literature is based on short-duration centrifuge experiments, not long-term habitation. **Resolving this parameter should be the top research priority for habitat sizing.**

### 3. Partial Gravity Opens Design Space

If 0.5g is sufficient for human health (an open question), the minimum radius drops to 180m and the binding constraint shifts to gravity gradient. This represents a fundamentally different — and cheaper — design regime.

### 4. Gravity Gradient Is a Secondary Concern

At 1% threshold, gradient only constrains the design below 180m, which is already below the vestibular floor. It becomes relevant only under strict uniformity requirements (< 0.5%).

### 5. Coriolis Is the Next Constraint to Formalize

Even at feasible radii, Coriolis forces are non-trivial. A runner at 224m experiences 12.8% lateral acceleration. This doesn't prevent habitation, but it affects sports, fluid dynamics (plumbing, weather), and daily movement patterns. The threshold for "acceptable" Coriolis is poorly defined in the literature and likely activity-dependent.

### 6. O'Neill's 3,200m Design Has Massive Margins

At 3,200m, every constraint has over 70% margin. RPM is 0.53 (74% below limit), gradient is 0.06% (94% below limit), and running Coriolis is 3.4% of g. This design was deliberately conservative — the question for future work is how much smaller we can actually go.

---

## Limitations of This Analysis

1. **Only 3 constraints modeled.** Coriolis, rim speed / structural stress, and cross-coupled angular motion are not yet formal constraints.
2. **Static analysis only.** Does not account for activities (jumping, climbing, throwing) that amplify Coriolis effects.
3. **Binary feasibility.** Constraints are pass/fail at a threshold. In reality, comfort degrades gradually.
4. **No structural feasibility.** Rim speed at 224m is moderate (47 m/s), but actual structural analysis (hoop stress, material selection, safety factors) is not included.
5. **Threshold values from limited data.** The 2 RPM vestibular limit comes from short-duration centrifuge studies, not long-term habitation experiments.

---

## Next Steps

1. **Implement Coriolis constraint** with activity-dependent thresholds (walking vs running vs sports)
2. **Implement rim speed / structural constraint** with material parameters (steel, carbon fiber, etc.)
3. **Sensitivity analysis module** — systematic perturbation of all assumptions with tornado charts
4. **Interactive demo** — React + Three.js visualization for parameter exploration
