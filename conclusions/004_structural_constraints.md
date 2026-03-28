# Structural Constraint Analysis (Phase 6)

**Date:** 2026-03-28 (updated from 2026-03-27)
**Model version:** habitat-constraints 0.1.0 (Phase 6)
**Constraints:** 12 total — Phase 3's 9 + hoop stress, cylinder length,
rotational stability
**Experiment script:**
`models/habitat_constraints/experiments/run_phase6_analysis.py`

---

## Summary

Adding three structural constraints reveals that **material choice,
wall thickness, and cylinder geometry are now the dominant design
drivers**. The rotational stability constraint ($L < 1.3r$ for single
cylinders) is far more restrictive than bending mode resonance,
reducing maximum length by 5–8× at typical radii.

**Key update (2026-03-28):** Wall thickness is now a tunable design
parameter across the full stack (API, solver, UI). The feasible radius
band is **not fixed at ~997m** — it widens substantially with thicker
walls or stronger materials:

| Wall thickness | Material | Feasible radius band | Band width |
|---------------|----------|---------------------|------------|
| $t = 0.2$ m | HS steel | 982–1,000 m | ~18 m |
| $t = 0.5$ m | HS steel | 982–2,100 m | ~1,100 m |
| $t = 1.0$ m | HS steel | 982–3,100 m | ~2,100 m |
| $t = 0.2$ m | CFRP | 982–3,200+ m | ~2,200+ m |

The interactive demo now shows **green feasible-range indicators** on
sliders for radius, wall thickness, cylinder length, and atmosphere
pressure, allowing real-time exploration of the design trade space.

---

## Phase 3 → Phase 6 Comparison

| Metric | Phase 3 (9 constraints) | Phase 6 (12 constraints) |
|--------|------------------------|--------------------------|
| Min radius at 1g | 982 m | 982 m (unchanged) |
| Max radius at 1g | 9,177 m (rim speed) | ~1,000 m (steel, $t = 0.2$ m) |
| Binding lower | Cross-coupling | Cross-coupling (unchanged) |
| Binding upper | Rim speed | **Hoop stress** |
| Max cylinder length | Unbounded | $L < 1.3r$ (single) |
| O'Neill feasible? | Yes (all 9 pass) | **No** (hoop stress fails) |

**Critical insight:** the Phase 3 feasible band was optimistic because
it ignored structural material limits. With steel at 0.2m wall
thickness, the hoop stress constraint ($\sigma = \rho \omega^2 r^2 +
Pr/t$) is dominated by the **pressure term** ($Pr/t$), which alone is
497 MPa at $r = 982$ m. This leaves almost no margin for the rotational
stress component.

---

## Experiment Results

### 1. Full 12-Constraint Scorecard

| Design | $r$ (m) | $L$ (m) | Paired? | Result | Failing |
|--------|---------|---------|---------|--------|---------|
| Min viable (single) | 982 | 1,276 | No | **PASS** | — |
| Min viable (old $L$) | 982 | 2,000 | No | FAIL | rotational stability |
| Kalpana One | 250 | 325 | No | FAIL | cross-coupling |
| O'Neill (paired) | 3,200 | 32,000 | Yes | FAIL | hoop stress |
| O'Neill (single) | 3,200 | 32,000 | No | FAIL | hoop stress, rot. stability |

**Key observations:**
- Our previous "minimum viable" design at $L = 2{,}000$ m now **fails**
  rotational stability ($L/r = 2.04 > 1.3$). The corrected maximum
  length is $L = 1{,}276$ m for a single cylinder.
- O'Neill's design fails hoop stress with our default steel — it would
  require CFRP or a much thicker wall.
- Kalpana One's $r = 250$ m fails cross-coupling regardless (too small).

### 2. Length Limit Comparison

Rotational stability is **always the binding length constraint** for
single cylinders. Bending mode resonance only matters for
counter-rotating pairs.

| $r$ (m) | Rotational stability | Bending mode | Ratio |
|---------|---------------------|-------------|-------|
| 250 | 325 m | 1,322 m | 4.1× |
| 982 | 1,277 m | 7,311 m | 5.7× |
| 2,000 | 2,600 m | 17,788 m | 6.8× |
| 3,200 | 4,160 m | 32,010 m | 7.7× |
| 5,000 | 6,500 m | 55,920 m | 8.6× |

The ratio grows with radius because rotational stability scales as
$L \propto r$ while bending mode scales as $L \propto r^{5/4}$.

### 3. Material Comparison (Hoop Stress)

At $r = 982$ m, $g = 1.0$, $t = 0.2$ m, $P = 101.3$ kPa:

| Material | $\sigma_y$ (MPa) | $\sigma_{\text{hoop}}$ (MPa) | Margin | Status |
|----------|-------------------|------------------------------|--------|--------|
| Structural steel (A36) | 400 | 574 | −187% | **FAIL** |
| High-strength steel (4340) | 1,200 | 574 | +4% | Barely pass |
| Titanium Ti-6Al-4V | 900 | 541 | −20% | **FAIL** |
| CFRP | 3,500 | 512 | +71% | **PASS** |

**Pressure dominates:** at $t = 0.2$ m, the pressure term
$\sigma_p = Pr/t = 101.3 \times 982 / 0.2 = 497$ MPa is ~87% of total
hoop stress. The rotational component ($\rho g r = 76$ MPa for steel)
is secondary. Increasing wall thickness is the most direct way to
reduce $\sigma_p$, but it adds mass.

At $r = 3{,}200$ m, only CFRP survives (4.6% margin). No material
in our set can handle $r = 5{,}000$ m at this wall thickness.

### 4. Single vs. Counter-Rotating Pairs

Counter-rotating pairs unlock dramatically more usable space:

| $r$ (m) | Mode | $L_{\max}$ (m) | Land area (km²) | Pop. capacity |
|---------|------|----------------|-----------------|---------------|
| 982 | Single | 1,276 | 3.9 | 98,000 |
| 982 | **Paired** | **7,306** | **22.5** | **563,000** |
| 2,000 | Single | 2,594 | 16.3 | 407,000 |
| 2,000 | **Paired** | **17,786** | **111.8** | **2,794,000** |
| 3,200 | Single | 4,156 | 41.8 | 1,045,000 |
| 3,200 | **Paired** | **31,995** | **321.6** | **8,041,000** |

Counter-rotating pairs provide **5.7–7.7× more length** and
proportionally more population capacity. This explains why O'Neill chose
paired cylinders — a single cylinder at $r = 3{,}200$ m can only be
4.2 km long, not 32 km.

### 5. Radius Sweep — Wall Thickness as Design Lever

The feasible radius band is **not a single point**. It widens as wall
thickness increases (reducing the pressure term $Pr/t$):

| $t$ (m) | $\sigma_p$ at 982 m (MPa) | Feasible $r_{\min}$ | Feasible $r_{\max}$ |
|---------|--------------------------|---------------------|---------------------|
| 0.2 | 497 | 982 m | ~1,000 m |
| 0.5 | 199 | 982 m | ~2,100 m |
| 1.0 | 99 | 982 m | ~3,100 m |
| 2.0 | 50 | 982 m | ~5,000+ m |

- **Lower binding:** cross-coupling (unchanged from Phase 3)
- **Upper binding:** hoop stress — but now **controllable** via $t$
- **Atmosphere pressure** also affects the band: half-atmosphere
  (50 kPa) roughly halves $\sigma_p$, equivalent to doubling $t$

The interactive demo's `/api/feasible_ranges` endpoint computes these
ranges dynamically, and green bars on the sliders show viable values
in real time.

---

## Design Implications

### 1. Our Minimum Viable Cylinder Must Be Shorter

The previous default of $L = 2{,}000$ m at $r = 982$ m is infeasible
for a single cylinder. The corrected design:

| Parameter | Old | New (single) | New (paired) |
|-----------|-----|-------------|-------------|
| $r$ | 982 m | 982 m | 982 m |
| $L$ | 2,000 m | **1,276 m** | 7,306 m |
| $L/D$ | 1.02 | **0.65** | 3.72 |
| Land area | 6.2 km² | **3.9 km²** | 22.5 km² |

### 2. O'Neill Requires Advanced Materials

O'Neill's Island Three ($r = 3{,}200$ m) fails hoop stress with
any steel at $t = 0.2$ m. Feasible paths:
- **CFRP hull:** passes with 4.6% margin (but CFRP at this scale is
  speculative)
- **Thicker steel walls:** $t \geq 0.4$ m would halve $\sigma_p$ to
  ~280 MPa, but doubles hull mass
- **Half-atmosphere (50 kPa):** halves $\sigma_p$, at the cost of
  40% O₂ (fire risk)

### 3. Counter-Rotating Pairs Are Not Optional

For any cylinder longer than $1.3r$, counter-rotating pairs are a
structural requirement, not a luxury. O'Neill understood this —
it's why his design specifies paired cylinders. Our model now
captures this constraint explicitly.

---

## What Changed in the Model

| Component | Change |
|-----------|--------|
| `HumanAssumptions` | Added `max_length_to_radius_ratio` (1.3), `counter_rotating_pair` (False) |
| `RotationalStabilityConstraint` | New — enforces $L < 1.3r$ (single) or $L < 10r$ (paired) |
| `CylinderLengthConstraint` | Existing — $L < C \cdot r^{5/4}$ (bending mode) |
| `HoopStressConstraint` | Existing — $\sigma_{\text{hoop}} \cdot \text{FoS} \leq \sigma_y$ |
| Total constraints | 9 → **12** |

---

## Next Steps

1. ~~Wall thickness as a design variable~~ — **DONE** (2026-03-28).
   Wall thickness slider in UI, passed through API/sweep/solver.
2. ~~Update the interactive demo~~ — **DONE** (2026-03-28). All 12
   constraints shown, green feasible-range indicators on sliders.
3. **Material selection in the API** — expose material presets (steel,
   titanium, CFRP) rather than raw $\sigma_y$ and $\rho$
4. **CFRP as default material** — documented in `structural_engineering.md`
   §3.2; needs API integration
5. **Spin-up energy budget** — $E = \frac{1}{2} I \omega^2$, time to
   spin up with ion thrusters or solar sails
6. **Half-atmosphere reproduction safety** — literature review
   (§3.1 of `literature_review_structural.md`) shows likely safe,
   but animal studies needed before committing to colony design
