# Literature Review: Structural Constraints

Validation of formulas and parameter values used in the habitat constraint
model against published research.

## 1. Hoop Stress Formula — Confirmed

Our combined formula:

$$\sigma_{\text{hoop}} = \rho \, \omega^2 r^2 + \frac{P \cdot r}{t}$$

is confirmed by McKendree (2000), NASA SP-413 (1975), and the community
analysis at *Masses of Space Habitats* (Reassembly). All decompose the load
into the same two components: centrifugal self-weight and pressure vessel
stress.

**Key identity:** since $\omega^2 r = g$ at the rim, the rotational term
simplifies to $\sigma_{\text{rot}} = \rho \, g \, r$. This is independent
of wall thickness — adding material increases both the load and the
cross-section proportionally. McKendree expresses maximum radius as:

$$R_{\max} = \frac{\sigma_{\text{allowable}}}{\rho \cdot g}$$

This is the "breaking length" concept from materials science.

### Numerical Validation

| Design Point | Our $\sigma_{\text{rot}}$ | Published | Status |
|-------------|--------------------------|-----------|--------|
| $r = 982$ m, steel | 76 MPa | 76 MPa (multiple) | Confirmed |
| $r = 3{,}200$ m, steel | 248 MPa | ~248 MPa (O'Neill) | Confirmed |
| Stanford Torus ($r = 830$ m, Al) | 22 MPa | 22 MPa | Confirmed |
| Kalpana One ($r = 250$ m, steel) | 19 MPa | 19 MPa | Confirmed |

**Pressure dominance confirmed:** at small-to-medium radii, the pressure
term dominates total hoop stress. NASA SP-413 confirmed "habitat structural
mass increases linearly in proportion to internal pressures."

### Safety Factor — Confirmed

Our FoS of 2.0 matches McKendree's 50% design stress convention and exceeds
NASA-STD-5001B's 1.4 for standard spacecraft. For a permanent colony, the
2.0–2.5 range is well justified.

### Maximum Radii by Material — Confirmed

| Material | $\sigma_y$ (MPa) | $\rho$ (kg/m³) | $R_{\max}$ (no FoS) | $R_{\max}$ (FoS=2) |
|----------|-------------------|-----------------|---------------------|---------------------|
| Structural steel | 400–1,200 | 7,900 | 5–15 km | 2.5–8 km |
| Aluminum 7075-T6 | 570 | 2,700 | 22 km | 11 km |
| Titanium Ti-6Al-4V | 900–1,100 | 4,540 | 20–25 km | 10–14 km |
| CFRP | 3,500–7,000 | 1,550 | 230–460 km | 115–230 km |
| CNT (McKendree) | 50,000 | 1,300 | ~3,900 km | ~1,950 km |

Our table in `structural_engineering.md` (steel 8–14 km, CFRP 2,250–4,500
kN·m/kg specific strength) aligns with McKendree and community analyses.

### Maximum Rim Speed — Reasonable

Our 300 m/s default is between mild steel's theoretical max (178 m/s) and
high-strength steel (374 m/s). No single published source gives 300 m/s as
a standard — it is derived from material properties with engineering
judgment. O'Neill's design has rim speed of 177 m/s at $r = 3{,}200$ m,
consistent with structural steel limits.


## 2. Cylinder Length — Partially Validated

### L/D Ratios — Confirmed

O'Neill Island Three: $L/D = 5.0$ (at $D = 6.4$ km) or $L/D = 4.0$ (at
$D = 8.0$ km — the 1974 Physics Today value). Both are published variants.
Kalpana One revised: $L/D = 0.65$ (Globus and Arora 2007).

### Our $L_{\max} = C \cdot r^{5/4}$ Formula — Original to This Project

This formula derives from combining beam bending frequency
($f_1 \propto r^{3/2}/L^2$) with rotation frequency
($f_{\text{rot}} \propto 1/\sqrt{r}$). The derivation is physically sound,
but **this specific formula does not appear in published literature**. It
should be labeled as original work calibrated to O'Neill's design point.

### Primary Length Constraint: Rotational Stability, Not Bending Modes

**Important finding:** the published literature identifies **rotational
stability** as the dominant length constraint, not bending mode resonance:

- **Globus et al. (2006, 2007):** the spin-axis moment of inertia must
  exceed any transverse axis by ≥20% ($I_z/I_x \geq 1.2$). For flat-capped
  cylinders: $L < 1.3r$ ($L/D < 0.65$). This drove Kalpana One's design.
- **Globus (2024):** "Design Limits on Large Space Stations" (arXiv:2408.00152)
  continues to emphasize rotational stability.
- **O'Neill's solution:** counter-rotating pairs cancel net angular momentum
  and provide gyroscopic stabilization. A single cylinder at $L/D = 5$
  would tumble.

**Implemented:** `RotationalStabilityConstraint` enforces $L < 1.3r$ for
passively stable single cylinders, with a `counter_rotating_pair` option
that relaxes the limit to $L < 10r$ for O'Neill-style paired designs. The
bending mode constraint ($C \cdot r^{5/4}$) remains as a secondary
structural check.

### Citation Correction

Our document cites "Globus and Hall 2017" for Kalpana One. The correct
source for the revised $L/D = 0.65$ design is Globus and Arora (2007).


## 3. Half-Atmosphere (51.7 kPa) — Confirmed

O'Neill proposed ~20 kPa $p_{O_2}$ + ~30 kPa $p_{N_2}$ = ~50 kPa total.
Confirmed in O'Neill (1977), NASA SP-413, and McKendree (2000, uses
50.8 kPa). Structural benefit is real: halving pressure roughly halves
the pressure hoop stress term. **Fire risk trade-off:** 40% $O_2$
concentration increases flammability (Apollo 1 precedent). NASA's
Exploration Atmosphere (56.5 kPa, 34% $O_2$) is a more conservative
compromise.

### 3.1 Half-Atmosphere and Reproduction — Likely Safe

The habitat's proposed atmosphere (50 kPa total, ~35–40% $O_2$,
$p_{O_2} \approx 21$ kPa) constitutes a **hypobaric normoxic**
environment. The key question is whether reduced barometric pressure
with normal oxygen partial pressure affects reproduction.

**High-altitude evidence points to hypoxia, not pressure:**

- Fetal growth restriction at altitude (~100 g birth weight decline per
  1,000 m) is driven by reduced uterine blood flow and placental
  metabolic switching to anaerobic glycolysis — both responses to
  **hypoxia** (Julian 2011; Sanchez-Gonzalez et al. 2024).
- Fertility impairment at altitude (reduced sperm quality, disrupted
  ovulation) is caused by oxidative stress from hypoxia acting on the
  hypothalamus–pituitary–gonad axis (Jing et al. 2020).
- Adapted populations (Tibetans, Andeans) show genetic protection via
  hypoxia-sensing genes ($EPAS1$, $EGLN1$) that preserve uterine artery
  blood flow (Beall 2014; Moore et al. 2001).

**Hypobaric normoxia studies show negligible effects:**

- Rat lung growth in hypobaric normoxia: slight somatic growth reduction,
  but lung biochemistry unaffected; hypoxic conditions caused significant
  hyperplasia (Sekhon and Bhullar 1995).
- Human exercise under hypobaric normoxia: maximal $\dot{V}O_2$ and
  arterial $SpO_2$ unchanged vs. sea level (Ogawa et al. 2019).

**NASA precedent:** Skylab operated at 34.5 kPa / 70% $O_2$
($p_{O_2} \approx 24$ kPa) for up to 84 days with no adverse effects.
NASA-STD-3001 accepts 34.5–103 kPa for indefinite human exposure
provided $p_{O_2}$ is 16–50 kPa.

**Assessment:** The reproductive risks documented at high altitude are
attributable to hypoxia, which the enriched-$O_2$ design eliminates.
Half-atmosphere with normal $p_{O_2}$ is **probably safe for
reproduction**. However, this specific combination has never been tested
for mammalian reproductive outcomes — a **data gap** that should be
closed through animal studies before committing to a multigenerational
colony design.

| Factor | Risk | Basis |
|--------|------|-------|
| Hypoxia-mediated FGR | Low | Eliminated by normal $p_{O_2}$ |
| Fertility impairment | Low | Hypoxia-driven, not pressure-driven |
| Neonatal respiratory adaptation | Unknown | No studies on birth in low-density air |
| Long-term developmental effects | Unknown | No multigenerational studies exist |


## References

Beall, Cynthia M. "Adaptation to High Altitude: Phenotypes and
Genotypes." *Annual Review of Anthropology*, vol. 43, 2014, pp. 251–272.

Globus, Al, and Nitin Arora. "Kalpana One: Analysis and Design of a
Space Colony." 2007. *NSS*, https://nss.org/wp-content/uploads/2017/07/Kalpana-One-2007.pdf

Globus, Al. "Design Limits on Large Space Stations." *arXiv*, 2024,
arXiv:2408.00152. https://arxiv.org/abs/2408.00152

McKendree, Tom. "Implications of Molecular Nanotechnology Technical
Performance Parameters on Previously Defined Space System Architectures."
*Nanotechnology*, vol. 11, 2000, pp. 1–15.
https://www.zyvex.com/nanotech/nano4/mckendreePaper.html

NASA. *Space Settlements: A Design Study*. NASA SP-413, 1975.
http://large.stanford.edu/courses/2016/ph240/martelaro2/docs/nasa-sp-413.pdf

NASA. *Structural Design and Test Factors of Safety for Spaceflight
Hardware*. NASA-STD-5001B, 2016.

O'Neill, Gerard K. *The High Frontier: Human Colonies in Space*. William
Morrow, 1977.

Jing, Xu, et al. "Reproductive Challenges at High Altitude: Fertility,
Pregnancy and Neonatal Well-Being." *Reproduction*, vol. 161, no. 1,
2021, pp. R13–R32.

Julian, Colleen G. "Humans at High Altitude: Hypoxia and Fetal Growth."
*Respiratory Physiology and Neurobiology*, vol. 178, no. 1, 2011,
pp. 129–139.

"Masses of Space Habitats." *Reassembly / Anisoptera Games*, 2023.
https://www.anisopteragames.com/masses-of-space-habitats/

Moore, Lorna G., et al. "Tibetan Protection from Intrauterine Growth
Restriction (IUGR) and Reproductive Loss at High Altitude." *Human
Biology*, vol. 73, no. 5, 2001, pp. 629–644.

NASA. "Habitable Atmosphere." *OCHMO Technical Brief*, OCHMO-TB-003
Rev A, 2023.

Ogawa, Tomoyuki, et al. "Effect of Hypobaria on Maximal Ventilation,
Oxygen Uptake, and Exercise Performance during Running under Hypobaric
Normoxic Conditions." *Physiological Reports*, vol. 7, no. 3, 2019.

Sanchez-Gonzalez, Carlos, et al. "Cause of Fetal Growth Restriction
during High-Altitude Pregnancy." *iScience*, vol. 27, no. 5, 2024.

Sekhon, H. S., and K. S. Bhullar. "Lung Growth in Hypobaric Normoxia,
Normobaric Hypoxia, and Hypobaric Hypoxia in Growing Rats." *Journal
of Applied Physiology*, vol. 78, no. 1, 1995, pp. 124–131.
