# Rim Speed Constraint: Why Habitats Can't Be Arbitrarily Large

## 1. The Problem

Phase 1 of our model found only a lower bound on radius. "Just build it bigger" seemed like it always helped — larger radius means lower RPM, less Coriolis, less cross-coupling. But there's a catch: **as radius grows, the rim moves faster**, and eventually the structure can't hold itself together.

The rim speed is:

$$
v_{\text{rim}} = \omega r
$$

For 1g, substituting $\omega = \sqrt{g/r}$:

$$
v_{\text{rim}} = \sqrt{g \cdot r}
$$

This grows with $\sqrt{r}$. At O'Neill's 3,200 m: $v_{\text{rim}} = 177$ m/s (637 km/h). At 10,000 m: $v_{\text{rim}} = 313$ m/s (1,128 km/h — supersonic).

---

## 2. The Physics: Hoop Stress

A rotating cylinder experiences **hoop stress** — the tensile force per unit area in the circumferential direction. The cylinder wall must resist being torn apart by its own rotation.

For a thin-walled rotating cylinder:

$$
\sigma_{\text{hoop}} = \rho \cdot v_{\text{rim}}^2
$$

Where $\rho$ is the material density (kg/m³) and $v_{\text{rim}}$ is the tangential velocity.

This is the same stress equation that governs flywheels, centrifuges, and rotating machinery. The critical insight: **hoop stress depends on $v_{\text{rim}}^2$, not on radius or mass independently.**

---

## 3. Material Limits

| Material | Density (kg/m³) | Yield Strength (MPa) | Max v_rim (m/s) | Max radius at 1g (m) |
|----------|------------------|-----------------------|-------------------|------------------------|
| Structural steel (A36) | 7,850 | 250 | 178 | 3,240 |
| High-strength steel (4340) | 7,850 | 1,100 | 374 | 14,290 |
| Aluminum 7075-T6 | 2,810 | 503 | 423 | 18,240 |
| Titanium Ti-6Al-4V | 4,430 | 880 | 446 | 20,260 |
| Carbon fiber (CFRP) | 1,600 | 1,500 | 968 | 95,560 |
| Kevlar 49 | 1,440 | 3,600 | 1,581 | 254,900 |

Where max $v_{\text{rim}} = \sqrt{\sigma_y / \rho}$ and max radius $= v_{\text{rim}}^2 / g$.

**Important:** These are theoretical maximums with zero safety factor. Real structures need safety factors of 2–4×, joints and welds are weaker than base material, and fatigue over decades degrades strength. Practical limits are roughly half the theoretical maximum.

---

## 4. The Constraint

$$
v_{\text{rim}} = \omega r \leq v_{\max}
$$

For 1g:

$$
r \leq \frac{v_{\max}^2}{g}
$$

Our model uses $v_{\max} = 300$ m/s as a practical steel limit (with safety factor). This gives:

$$
r_{\max} = \frac{300^2}{9.807} = 9{,}177 \; \text{m}
$$

This creates the **upper bound** on habitat radius that Phase 1 was missing.

---

## 5. The Feasible Band

Combining with the lower bound from cross-coupling (982 m):

$$
982 \; \text{m} \leq r \leq 9{,}177 \; \text{m} \quad \text{(at 1g, steel construction)}
$$

With carbon fiber:

$$
982 \; \text{m} \leq r \leq \sim 24{,}000 \; \text{m} \quad \text{(at 1g, with safety factor)}
$$

O'Neill's 3,200 m sits at 35% of the steel limit — a reasonable engineering margin.

---

## 6. Why This Matters Beyond Stress

### Aerodynamic drag

A rotating cylinder contains atmosphere. The walls drag the air along, but the air near the axis has less angular momentum. This creates atmospheric circulation patterns. At high rim speeds, the energy to maintain the atmosphere's co-rotation becomes significant.

### Spin-up energy

The rotational kinetic energy of a cylinder scales as $r^2 \omega^2 \propto r \cdot g$ (for 1g). Larger habitats require more energy to spin up, proportional to radius.

### Micrometeorite vulnerability

A larger circumference means more surface area exposed to micrometeorite impact. A puncture at high rim speed creates a dynamic failure that propagates faster in a more stressed structure.

---

## 7. The One-Liner

> Rim speed scales as $\sqrt{r}$ for a given gravity. Build too large and the walls tear themselves apart. Steel limits you to ~9 km radius at 1g; carbon fiber pushes this to ~24 km. This creates the upper bound that makes the design space finite.

---

## References

- ASM International. *ASM Handbook, Volume 1: Properties and Selection — Irons, Steels, and High-Performance Alloys*. ASM International, 1990.

- Hall, Theodore W. "Artificial Gravity and the Architecture of Orbital Habitats." *Journal of the British Interplanetary Society*, vol. 52, 1999, pp. 455–465.

- O'Neill, Gerard K. *The High Frontier: Human Colonies in Space*. William Morrow, 1977.

- Peters, S. T., editor. *Handbook of Composites*. 2nd ed., Chapman & Hall, 1998.
