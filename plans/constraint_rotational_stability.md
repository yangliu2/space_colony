# Rotational Stability Constraint

## Summary

A cylinder spinning about its symmetry axis for artificial gravity is in
**unstable equilibrium** if the spin axis has the smallest moment of
inertia. Energy dissipation from internal activity (people walking,
weather, machinery vibration) drives rotation toward the maximum-$I$ axis
— the classic **Explorer 1 problem**. Passive stability requires the spin
axis to be the maximum-$I$ axis, which places a hard upper limit on
cylinder length relative to radius.

This is the **primary length constraint in published literature** (Globus
and Arora 2007, Globus 2024), more binding than bending mode resonance
for most practical designs.

## The Explorer 1 Problem

Explorer 1 (1958), a pencil-shaped satellite, was spin-stabilized about
its long axis (minimum $I$). Within hours, flexible whip antennas
dissipated rotational energy, and the satellite transitioned to tumbling
about its maximum-$I$ axis. The total angular momentum $\vec{L}$ was
conserved, but kinetic energy was minimized — which for a given
$|\vec{L}|$ means spinning about the axis with the **largest** moment of
inertia.

Any rotating space habitat faces the same physics. Internal energy
dissipation is unavoidable (atmospheric friction, human activity,
machinery), so the spin axis must be the maximum-$I$ axis for passive
stability.

## Moment of Inertia Analysis

For a uniform thin-walled cylinder of radius $r$, length $L$, and
mass $m$:

**Spin axis** (along the cylinder length):

$$I_z = m r^2$$

**Transverse axis** (perpendicular to length):

$$I_x = m \left(\frac{r^2}{2} + \frac{L^2}{12}\right)$$

Passive stability requires $I_z > I_x$, with a 20% margin for
robustness (Globus and Arora 2007):

$$\frac{I_z}{I_x} \geq 1.2$$

Substituting:

$$\frac{r^2}{\frac{r^2}{2} + \frac{L^2}{12}} \geq 1.2$$

Solving for $L$:

$$L^2 \leq 12 r^2 \left(\frac{1}{1.2} - \frac{1}{2}\right) = 12 r^2 \times \frac{1}{3} = 4 r^2$$

Wait — let me redo this carefully:

$$\frac{r^2}{\frac{r^2}{2} + \frac{L^2}{12}} \geq 1.2$$

$$r^2 \geq 1.2 \left(\frac{r^2}{2} + \frac{L^2}{12}\right)$$

$$r^2 \geq 0.6 r^2 + 0.1 L^2$$

$$0.4 r^2 \geq 0.1 L^2$$

$$L^2 \leq 4 r^2$$

$$L \leq 2r$$

With the 20% stability margin ($I_z/I_x \geq 1.2$), this gives $L \leq 2r$
for a pure thin-walled cylinder. However, Globus and Arora (2007) arrive
at $L < 1.3r$ for Kalpana One because flat end caps add transverse moment
of inertia, making the constraint tighter. The exact ratio depends on
end cap geometry and internal mass distribution.

## Published Design Values

| Design | $r$ (m) | $L$ (m) | $L/r$ | Stability | Source |
|--------|---------|---------|-------|-----------|--------|
| Kalpana One (revised) | 250 | 325 | 1.3 | Passive | (Globus and Arora 2007) |
| Kalpana One (original) | 250 | 550 | 2.2 | **Unstable** | (Globus and Bajoria 2006) |
| O'Neill Island Three | 3,200 | 32,000 | 10.0 | Active (paired) | (O'Neill 1976) |
| Our minimum viable | 982 | 1,277 | 1.3 | Passive (max) | This study |

**Key observation:** O'Neill's $L/r = 10$ is **passively unstable**. His
solution was counter-rotating pairs — two cylinders spinning in opposite
directions, coupled by bearings. The pair cancels net angular momentum
and provides gyroscopic cross-stabilization. This is an active/
architectural solution, not passive stability.

## Counter-Rotating Pairs

O'Neill proposed pairing two cylinders spinning in opposite directions,
connected at the ends. Benefits:

1. **Gyroscopic stabilization** — precession forces from each cylinder
   cancel, allowing much higher $L/r$
2. **Zero net angular momentum** — simplifies orbital station-keeping
3. **Attitude control** — differential speed adjustments enable pointing

The engineering cost is significant: massive bearings at the connection
points must handle the full rotational loads. But it removes the $L/r$
limit as a hard constraint — replacing it with a softer structural limit
on the bearing system.

Our model handles this with a `counter_rotating_pair` flag that relaxes
the limit from $L/r < 1.3$ to $L/r < 10$.

## Effect on Our Design Space

With the default $L/r \leq 1.3$ for a single passively stable cylinder:

| $r$ (m) | $L_{\max}$ (m) | Land area (km²) | Population at 40 m²/person |
|---------|---------------|-----------------|---------------------------|
| 982 | 1,277 | 3.94 | 98,400 |
| 2,000 | 2,600 | 16.34 | 408,400 |
| 3,200 | 4,160 | 41.82 | 1,045,500 |

Compare with the bending mode limit ($L_{\max} = 1.33 \cdot r^{5/4}$):

| $r$ (m) | Rotational stability | Bending mode | Binding constraint |
|---------|---------------------|-------------|-------------------|
| 982 | 1,277 m | 7,309 m | **Rotational stability** |
| 2,000 | 2,600 m | 17,783 m | **Rotational stability** |
| 3,200 | 4,160 m | 32,000 m | **Rotational stability** |

**Rotational stability is always the binding length constraint** for
single cylinders. The bending mode limit only becomes relevant for
counter-rotating pairs at very high $L/r$.

## Constraint Implementation

```
class RotationalStabilityConstraint:
    L <= max_length_to_radius_ratio × r    (default: 1.3)

    If counter_rotating_pair=True:
        L <= 10 × r                        (relaxed limit)
```

Parameters in `HumanAssumptions`:
- `max_length_to_radius_ratio`: 1.3 (default, flat caps)
- `counter_rotating_pair`: False (default)

Adjustable for curved end caps ($L/r \approx 2.0$) or other geometries.

## References

Globus, Al, and Nitin Arora. "Kalpana One: Analysis and Design of a
Space Colony." *NSS*, 2007.
https://nss.org/wp-content/uploads/2017/07/Kalpana-One-2007.pdf

Globus, Al. "Design Limits on Large Space Stations." *arXiv*, 2024,
arXiv:2408.00152. https://arxiv.org/abs/2408.00152

Globus, Al. "Space Station Rotational Stability." *arXiv*, 2024,
arXiv:2408.00155. https://arxiv.org/abs/2408.00155

O'Neill, Gerard K. *The High Frontier: Human Colonies in Space*.
William Morrow, 1976.
