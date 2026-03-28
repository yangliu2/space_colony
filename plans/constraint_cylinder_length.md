# Cylinder Length Constraints

## Summary

The length of an O'Neill cylinder does not affect simulated gravity ($a = \omega^2 r$), but it is structurally constrained. The maximum safe length depends on the cylinder radius — wider cylinders can be longer. This relationship creates a **length-to-diameter ratio** ($L/D$) constraint that should be tracked alongside the existing rotational and biological constraints.

## Why Length Matters Structurally

### 1. Bending Mode Resonance (Critical Speed)

A rotating cylinder behaves like a spinning shaft in mechanical engineering. Every shaft has **critical speeds** — rotational frequencies at which bending resonance modes are excited. If the operating RPM coincides with a bending natural frequency, catastrophic vibration results.

The first bending natural frequency of a thin-walled cylinder is approximately:

$$f_1 \approx \frac{\pi}{2 L^2} \sqrt{\frac{E I}{\rho A}}$$

where:
- $L$ = cylinder length
- $E$ = Young's modulus of hull material
- $I$ = second moment of area of the cross-section
- $\rho$ = effective density (hull + contents)
- $A$ = cross-sectional area

For a thin-walled cylinder shell, $I \approx \pi r^3 t$, where $t$ is wall thickness. This means:

$$f_1 \propto \frac{r^{3/2} \sqrt{t}}{L^2}$$

**The constraint:** the first bending frequency $f_1$ must be well above the rotation frequency $f_\text{rot}$:

$$f_1 > k \cdot f_\text{rot}$$

where $k \geq 3$ provides a safety margin (standard engineering practice for rotating machinery).

Since $f_1 \propto r^{3/2} / L^2$ and $f_\text{rot} \propto 1/\sqrt{r}$ (from $\omega = \sqrt{g/r}$), combining gives:

$$L_\text{max} \propto r^{5/4} \cdot t^{1/4}$$

**Key insight:** maximum safe length grows faster than linearly with radius. Doubling the radius allows more than doubling the length.

### 2. Euler Buckling Under Axial Loads

While the cylinder is primarily in hoop tension, axial compressive loads arise from:
- Atmospheric pressure on end caps transmitted through the shell
- Asymmetric mass distribution creating bending moments
- Thermal gradients along the length

The critical buckling load for a thin-walled cylinder under axial compression is:

$$\sigma_\text{cr} = \frac{E t}{r \sqrt{3(1 - \nu^2)}}$$

This is independent of length but sets a minimum wall thickness. However, **column buckling** of the overall cylinder (Euler buckling) does depend on length:

$$P_\text{cr} = \frac{\pi^2 E I}{L^2}$$

Longer cylinders are more susceptible to overall column buckling under any net axial force.

### 3. Gravity Gradient Along Length

While length doesn't affect the magnitude of artificial gravity, a very long cylinder creates **different tidal effects** at the ends vs. the center if the cylinder orbits a massive body (e.g., at L5, the Sun's gravity gradient across 32 km is measurable though small). At L5 this is negligible but becomes relevant for very long structures ($L > 100$ km).

### 4. Atmospheric Considerations

The total atmospheric mass scales as $\pi r^2 L \rho_\text{air}$:

| $r$ (m) | $L$ (m) | Air mass (tonnes) |
|---------|---------|-------------------|
| 982     | 2,000   | ~3,700            |
| 982     | 10,000  | ~18,500           |
| 3,200   | 32,000  | ~1,260,000        |

More atmosphere means:
- More mass to contain (higher end cap forces: $F = P \times \pi r^2$, independent of length, but structural mass of end caps increases)
- Longer convection cells — weather becomes harder to manage
- Greater pressure variation from Coriolis-deflected air circulation

### 5. Construction and Material Mass

Hull structural mass scales roughly as $2\pi r t L \rho_\text{steel}$. Doubling length doubles hull mass but also doubles livable area, so mass per capita stays constant — length is efficient for adding capacity.

However, the **shielding mass** ($2\pi r L \times \rho_\text{shield}$) also doubles, and shielding dominates total mass. Length is expensive in terms of raw material.

## Length-to-Diameter Ratios in Literature

| Design | $r$ (m) | $L$ (m) | $D$ (m) | $L/D$ | Source |
|--------|---------|---------|---------|-------|--------|
| O'Neill Island Three | 3,200 | 32,000 | 6,400 | 5.0 | (O'Neill 1976) |
| Kalpana One | 250 | 325 | 500 | 0.65 | (Globus and Hall 2017) |
| Stanford Torus | 830 (major) | N/A | N/A | N/A | (Johnson and Holbrow 1977) |
| Our minimum viable | 982 | 2,000 | 1,964 | 1.0 | This study |

O'Neill's $L/D = 5$ appears to be the upper practical limit for steel/aluminum construction. Kalpana One's $L/D = 0.65$ is very conservative, optimized for short cylinders where end cap losses are minimized relative to livable area.

## Proposed Constraint

### Simple ratio constraint

$$L \leq L/D_\text{max} \times 2r$$

With $L/D_\text{max} = 5$ (O'Neill's design point) as default, adjustable.

### Refined constraint (accounting for radius dependence)

Based on the bending mode analysis, the maximum length scales as $r^{5/4}$. Calibrating to O'Neill's design:

$$L_\text{max} = C \cdot r^{5/4}$$

where $C$ is calibrated so that $L_\text{max} = 32{,}000$ m when $r = 3{,}200$ m:

$$C = \frac{32{,}000}{3{,}200^{5/4}} \approx 1.33$$

This gives:

| $r$ (m) | $L_\text{max}$ (m) | $L/D_\text{max}$ |
|---------|-------------------|-----------------|
| 500     | 3,144             | 3.1             |
| 982     | 7,309             | 3.7             |
| 2,000   | 17,783            | 4.4             |
| 3,200   | 32,000            | 5.0             |

Our minimum viable cylinder ($r = 982$ m, $L = 2{,}000$ m) is well within limits — we could extend to ~7.3 km safely.

## Recommendation

Add a **soft constraint** to the model that warns when $L > C \cdot r^{5/4}$ with $C \approx 1.33$. This is not a hard biological limit like the vestibular constraints, but a structural feasibility boundary.

The constraint does not affect the existing 9 rotational/biological constraints but should appear as a separate structural constraint in the evaluation panel.

## Effect on Livable Area and Population

Livable area (3 land strips, each 60° arc):

$$A_\text{land} = 3 \times \frac{\pi}{3} r \times L = \pi r L$$

For our minimum viable cylinder: $A_\text{land} = \pi \times 982 \times 2{,}000 \approx 6.17 \text{ km}^2$

At the maximum safe length: $A_\text{land} = \pi \times 982 \times 7{,}309 \approx 22.54 \text{ km}^2$

This is significant — tripling the length triples the population capacity without changing any rotational constraint.

## References

Globus, Al, and Theodore Hall. "Space Settlement Population Rotation Tolerance." *NSS Space Settlement Journal*, 2017. https://space.nss.org/space-settlement-population-rotation-tolerance/

Johnson, Richard D., and Charles Holbrow, editors. *Space Settlements: A Design Study*. NASA SP-413, 1977.

O'Neill, Gerard K. *The High Frontier: Human Colonies in Space*. William Morrow, 1976.
