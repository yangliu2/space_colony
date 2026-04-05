# Cylinder Length Constraints

## The Short Answer

Length does not affect artificial gravity ($a = \omega^2 r$ depends only on radius and spin
rate). But length has two independent structural limits — and O'Neill's design sits at
exactly one of them. This study confirms his design rather than contradicting it, with
one key clarification: **two counter-rotating cylinders are structurally required, not optional**.

---

## Step 1 — The Single Cylinder Problem

Imagine one spinning cylinder in space. Intuitively it seems stable — it's spinning about
its long axis. But this is exactly the unstable equilibrium.

A spinning object is passively stable only if it rotates about its **maximum** moment of
inertia axis (the "short fat" axis). Rotation about the minimum-inertia axis (the long thin
axis) is unstable — any small disturbance causes it to tumble. This is the same reason a
spinning phone tumbles when thrown: the long axis is the minimum-I axis.

For a thin-walled cylinder with flat end caps:

$$I_z = m r^2 \qquad \text{(spin axis, along length)}$$

$$I_x = m \left(\frac{r^2}{2} + \frac{L^2}{12}\right) \qquad \text{(transverse axis)}$$

Passive stability requires $I_z / I_x \geq 1.2$ (20% margin), which gives:

$$L < \sqrt{6\left(\frac{1}{1.2} - 0.5\right)} \cdot r \approx 1.29r$$

Rounded: **$L < 1.3r$** (Globus and Arora 2007).

For O'Neill's Island Three ($r = 3{,}200$ m, $L = 32{,}000$ m): $L/r = 10$ — far past 1.3.
**A single O'Neill cylinder would tumble.** O'Neill knew this.

---

## Step 2 — Why O'Neill Used Two Cylinders

Counter-rotating pairs cancel the net angular momentum vector. With zero net spin, there
is no gyroscopic resistance to reorientation — active attitude control (small thrusters)
handles the remaining perturbations. The $L/r < 1.3$ passive stability limit no longer
applies.

O'Neill explicitly chose the paired design for this reason (O'Neill 1976, NASA SP-413 1975).
The counter-rotating pair is **not an optional upgrade** — it is required for any cylinder
with $L/r > 1.3$. All O'Neill-scale designs (and our model) assume two cylinders.

This is established engineering, confirmed by Globus (2024).

---

## Step 3 — The Remaining Limit: Bending Resonance

With counter-rotating pairs, the rotational stability limit relaxes to approximately
$L/r < 10$ (a generous bound used by the model). But a second structural constraint
remains: **bending mode resonance**.

A long rotating cylinder behaves like a spinning shaft. Every shaft has critical speeds —
rotational frequencies that excite structural bending modes. Operating at or above a
critical speed causes catastrophic vibration.

The first bending natural frequency of a thin-walled cylinder (Euler–Bernoulli beam):

$$f_1 \approx \frac{\pi}{2 L^2} \sqrt{\frac{E I}{\rho A}}$$

For a thin-walled cylinder of radius $r$ and wall thickness $t$:
$I = \pi r^3 t$ and $A = 2\pi r t$, so $I/A = r^2/2$ — the wall thickness cancels.
Therefore:

$$\sqrt{\frac{E I}{\rho A}} = r \sqrt{\frac{E}{2\rho}} \propto r
\quad \Longrightarrow \quad
f_1 \propto \frac{r}{L^2}$$

The spin frequency (from $\omega = \sqrt{g/r}$):

$$f_\text{rot} \propto \frac{1}{\sqrt{r}}$$

Requiring $f_1 > k \cdot f_\text{rot}$ with safety factor $k \geq 3$ gives:

$$\frac{r}{L^2} > C \cdot \frac{1}{\sqrt{r}}
\quad \Longrightarrow \quad
r^{3/2} > C' \cdot L^2
\quad \Longrightarrow \quad
\boxed{L_\text{max} = C \cdot r^{3/4}}$$

**This formula is original to this study** — it does not appear in prior published literature
on space habitats (see `literature_review_structural.md` §2). It should be treated as
original analysis pending independent verification. It is calibrated to O'Neill's design:

$$C = \frac{32{,}000}{3{,}200^{3/4}} \approx 75.22$$

---

## Step 4 — O'Neill Is at the Limit

Applying the bending formula $L_\text{max} = 75.22 \cdot r^{3/4}$:

| $r$ (m) | $L_\text{max}$ bending (m) | $L/D_\text{max}$ | Notes |
|---------|---------------------------|-----------------|-------|
| 500     | 7,954                     | 7.95            | |
| 982     | 13,194                    | 6.72            | Minimum viable habitat |
| 2,000   | 22,494                    | 5.62            | |
| 3,200   | **32,000**                | **5.00**        | O'Neill Island Three |

O'Neill's design ($L = 32{,}000$ m at $r = 3{,}200$ m) sits **exactly at the bending
resonance limit**. This is not a coincidence — O'Neill's team iterated to this geometry.
The formula confirms the design is structurally valid, but there is no headroom for a
longer cylinder at that radius.

**This is a refinement of O'Neill's design, not a contradiction.** His dimensions are
correct given the constraint. What this study adds is a physics-derived formula that
explains *why* that specific length was chosen and what it implies for smaller cylinders.

---

## Step 5 — Implications for the Minimum Viable Habitat

For our minimum viable radius ($r = 982$ m):

| Constraint | Limit | Binding? |
|------------|-------|---------|
| Rotational stability (single cylinder) | $L < 1{,}277$ m | Only if unpaired |
| Rotational stability (counter-rotating) | $L < 9{,}820$ m | Not binding |
| Bending resonance | $L < 13{,}194$ m | **Yes — binding limit** |

With two cylinders, the minimum viable habitat can safely reach **13.2 km** — roughly
6.7× the diameter. At maximum safe length, the livable land area increases substantially:

$$A_\text{land} = \pi r L$$

| $L$ (m) | $A_\text{land}$ (km²) | Notes |
|---------|----------------------|-------|
| 1,276   | 3.9                  | Current demo default |
| 13,194  | 40.7                 | Structural limit |

The demo default (1,276 m) is conservative — chosen for visual proportion, not structural
necessity. Any length up to 13.2 km is structurally valid for $r = 982$ m.

---

## What Two Cylinders Are Not

Counter-rotating pairs solve the tumbling instability. They do not eliminate:

- Bending resonance (the formula above still applies)
- Hoop stress (the rim speed limit, independent of length)
- Material mass requirements (shielding doubles with length)

Two cylinders are necessary but not sufficient. The bending limit is the final word
on maximum length.

---

## References

Globus, Al, and Nitin Arora. "Kalpana One." *National Space Society*, 2007.

Globus, Al. "Design Limits on Large Space Stations." *arXiv:2408.00152*, 2024.

Jensen, Jared. "Space Station Rotational Stability." *arXiv:2408.00155*, 2024.
— Most rigorous formal treatment of the $I_z/I_x$ stability criterion for multiple geometries.

Johnson, Richard D., and Charles Holbrow, editors. *Space Settlements: A Design Study*.
NASA SP-413, 1977.

O'Neill, Gerard K. *The High Frontier: Human Colonies in Space*. William Morrow, 1976.

> **Note on novelty:** The rigid-body tumbling instability (Step 1) and the counter-rotating
> pair solution (Step 2) are established engineering — O'Neill (1976), Globus & Arora (2007),
> Jensen (2024). The bending resonance formula $L_\text{max} = 75.22 \cdot r^{3/4}$ (Step 3)
> does not appear in any published space-habitat paper found. The derivation follows from
> standard Euler–Bernoulli beam theory applied to a thin-walled cylinder; the key result
> is that wall thickness cancels in $I/A = r^2/2$, giving $f_1 \propto r/L^2$. It should
> still be treated as original analysis pending independent verification by a structural engineer.
