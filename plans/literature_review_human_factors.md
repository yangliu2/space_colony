# Literature Review: Human Factors & Biological Constraints

Validation of rotation comfort thresholds and biological parameter values
used in the habitat constraint model against published research.

## 1. Maximum Rotation Rate (2 RPM) — Confirmed (Conservative)

| Source | Year | RPM Limit | Context |
|--------|------|-----------|---------|
| Clark and Hardy | 1960 | 0.1 | Illusion threshold (extremely conservative) |
| Hill and Schnitzer | 1962 | 4.0 | NASA Langley comfort chart at 1g |
| Gilruth | 1969 | 2.0 optimal, 6.0 sickness | Most cited NASA standard |
| Stone | 1973 | 6.0 | Performance-based; accepted 3× nausea threshold |
| NASA SP-413 | 1975 | 1–2 | Became the design standard for settlements |
| Graybiel | various | 1.0 symptom-free | Adapted to 10 RPM incrementally over 10 days |
| Globus and Hall | 2017 | 4.0 residents, 6.0 trained | Argues 1–2 RPM is overly conservative |
| Clément and Bukley | 2007 | 2–4, possibly 6 | Recent data suggests adaptation is robust |

**Verdict:** our 2 RPM default matches Gilruth's "optimal comfort" and
NASA SP-413. Globus and Hall (2017) make a strong case for 4 RPM for
adapted residents. Our model could offer a "relaxed" mode at 4 RPM.

**Key finding (Fong et al. 2020):** an incremental vestibular acclimation
protocol increased subjects' cross-coupling tolerance from 1.8 RPM to
17.7 RPM over 10 days.


## 2. Cross-Coupling Threshold (6 deg/s²) — Reasonable Interpolation

| Source | Threshold | Context |
|--------|-----------|---------|
| Clark and Hardy (1960) | 3.4 deg/s² | Illusion onset |
| Clark and Hardy (1960) | 34.4 deg/s² | Nausea onset |
| Stone (1970) | 115 deg/s² | Performance-based (very generous) |
| Our model (unadapted) | 3 deg/s² | Near illusion onset |
| Our model (adapted) | 6 deg/s² | Interpolation |

**Verdict:** our 3 deg/s² unadapted value aligns closely with Clark and
Hardy's illusion onset (3.4 deg/s²). The 6 deg/s² adapted threshold is a
**reasonable interpolation** between illusion and nausea, but no single
published source gives this exact number.

**Lackner and DiZio (1998, 2003):** cross-coupling severity is
**gravity-dependent** — less provocative below 1g, more above 1g. This
means ground-based data may overestimate the problem for partial-gravity
habitats. Adaptation to Coriolis perturbations occurs within 10–20
arm movements.


## 3. Coriolis-to-Gravity Ratio (0.25) — Exact Match

Our 0.25 maximum traces directly to Stone (1970) and was codified by
Cramer (1983) as the standard. No published source contradicts it.

**Practical note:** at any radius satisfying the cross-coupling constraint
($r > 982$ m), the Coriolis ratio for running at 3 m/s is already only
~6% — well below 25%. The Coriolis constraint is never binding in practice
for our design space.


## 4. Gravity Gradient (1%) — More Conservative Than Literature

| Source | Max Gradient | Min Radius (1.8 m person) |
|--------|-------------|--------------------------|
| Gilruth (1969) | 15% | ~12 m |
| Payne (1960) | 15% | ~12 m |
| Cramer (1983) | ~6% | ~30 m |
| **Our model** | **1%** | **180 m** |

**Verdict:** our 1% is **6–15× more conservative** than any published
source. However, it is never binding — vestibular (224 m) and
cross-coupling (982 m) constraints are stricter. The 1% value represents
an "imperceptible gradient" design philosophy for permanent habitation.


## 5. Minimum Gravity (0.3g) — At the Floor

| Source | Min Gravity | Notes |
|--------|------------|-------|
| Gilruth (1969) | 0.3g | "Mobility limit" from parabolic flights |
| Clément and Bukley (2015) | 0.22–0.5g | Vestibular perception threshold |
| Waldie et al. (2021) | >0.38g? | Moon/Mars gravity insufficient for cardiovascular health |
| NASA rodent study (2023) | >0.67g? | 0.67g mice had lower bone strength than controls |

**Verdict:** our 0.3g matches Gilruth's floor but recent NASA research
suggests even Mars gravity (0.38g) may be inadequate for long-term
cardiovascular health. For reproduction and child development, 0.3g is
almost certainly too low. It should be understood as a **theoretical
floor for healthy adults with countermeasures**, not a design target.
The model's default of 1.0g as $g_{\max}$ is the responsible design
target for families.


## 6. Radiation Shielding (4500 kg/m²) — Outdated but Reasonable

Our 4500 kg/m² comes from NASA SP-413 for <0.5 rem/yr (5 mSv/yr) with
regolith shielding. Key updates:

- **NASA-STD-3001 (2022):** career limit now 600 mSv (universal), annual
  limit 20 mSv/yr. Our SP-413 target of 5 mSv/yr is *stricter* than
  current NASA limits — appropriate for permanent settlers.
- **Secondary neutron problem:** at 20–30 g/cm² of aluminum or regolith,
  secondary neutron buildup *increases* dose. Polyethylene and
  hydrogen-rich materials avoid this problem (ScienceDirect 2022).
- **Material dependence:** 4500 kg/m² is reasonable for regolith but
  hydrogen-rich materials (polyethylene, water) could achieve equal
  protection at lower mass.

**Recommendation:** make the shielding threshold material-dependent in
future model versions. Note that the <0.5 rem/yr target is intentionally
stricter than NASA career limits.


## 7. Atmosphere (16–50 kPa pO₂) — Well Validated

- **Lower bound (16 kPa):** NASA-STD-3001 confirms 16.9 kPa (127 mmHg)
  shows "no indication of degraded health" for indefinite exposure.
  Impairment begins at ~10.7 kPa arterial.
- **Upper bound (50 kPa):** NCBI confirms pulmonary toxicity onset at
  ≥51 kPa with continuous exposure. CNS toxicity at ~160 kPa.
- **NASA Exploration Atmosphere:** 56.5 kPa total, 34% O₂ → 19.2 kPa
  pO₂, well within our range.

**No disagreements found.** The 16–50 kPa range is consistent across NASA,
diving medicine, aviation physiology, and submarine literature.


## 8. Minimum Viable Population (98) — Contested

| Study | MVP | Method |
|-------|-----|--------|
| Marin and Beluffi (2018) | 98 | Monte Carlo with managed breeding |
| Salotti (2020) | 110 | Labor requirements model |
| Moore (2002) | 150–180 | Conservation biology |
| 50/500 rule (genetics) | 50/500 | Effective population theory |
| Smith (2014) | 14,000–44,000 | Genetics + anthropology + catastrophes |

**Critical caveat:** the 98 figure requires "intelligent interventions"
(centralized breeding control). Effective population is typically 25–50%
of census — so 98 people may have an effective population of only 25–50,
below the classic 50-person short-term threshold. Salotti (2020)
independently arrived at 110 from labor analysis, providing convergent
support for the ~100 order of magnitude.

Our documentation already presents this correctly: 98 as bare survival,
10,000+ for a culturally viable colony.

**Biosphere 2 lesson:** O₂ dropped from 21% to 14% in 16 months due to
soil microbes and chemical sinks (CO₂ reacting with concrete). Even a
200,000 m³ ecosystem could not passively maintain atmospheric homeostasis.


## 9. Water Recycling Efficiency (0.98) — Well-Supported, Demonstrated

| Source | Year | Efficiency | Context |
|--------|------|-----------|---------|
| Carter et al. | 2009 | 0.93 | ISS ECLSS before Brine Processor Assembly (BPA) |
| ISS operational | 2021 | ~0.93–0.94 | UPA + WPA without BPA |
| Gatens et al. | 2024 | 0.98 | ISS with BPA; stated as Mars mission milestone |
| NASA official guidance | ongoing | 0.98 | "At least 98%" required for no-resupply missions |

**Verdict:** Our 0.98 threshold is **well-supported and now demonstrated** in
hardware. The ISS reached 98% total recovery in 2023–2024 with the Brine
Processor Assembly (BPA), which recovers 95–98% of water from the UPA brine
output. NASA officially states that 98% is required for permanent missions
without routine water resupply.

**Key caveat:** The 98% is the ECLSS loop efficiency. Whole-habitat effective
efficiency is lower because hygiene wipes, contaminated water, and similar
disposal paths bypass the recovery system. For a permanent colony, minimising
these non-loop losses is a critical secondary engineering problem not modelled
here. Some analyses describe the 98% regime as having "too small a margin for
comfort" without accounting for these disposal paths.

**ISS pre-BPA at colony scale (why 0.93 fails):** At 8,000 people demanding
20 L/day with η = 0.93, annual water loss is 4,088 t/year — roughly 1,360
Falcon 9 deliveries per year. Even 0.95 produces 2,044 t/year. Only above
~0.98 does annual loss drop to a level potentially manageable by in-situ
resource utilisation (ISRU).


## References

Clark, Carl C., and James D. Hardy. "Gravity Problems in Manned Space
Stations." *Aerospace Engineering*, 1960.

Clément, Gilles, and Angelia Bukley. "Artificial Gravity as a
Countermeasure for Mitigating Physiological Deconditioning During
Long-Duration Space Missions." *Frontiers in Systems Neuroscience*,
vol. 9, 2015. *PubMed Central*, PMC4470275.

Fong, Ajilon, et al. "Improved Feasibility of Rotating Artificial
Gravity Through Incremental Vestibular Acclimation." *University of
Colorado*, 2020.

Gilruth, Robert R. "Manned Space Stations — Gateway to Our Future
in Space." *NASA*, 1969. *NTRS*, 19690029825.

Globus, Al, and Theodore Hall. "Space Settlement Population Rotation
Tolerance." *NSS Space Settlement Journal*, 2017.
http://space.alglobus.net/papers/RotationPaper.pdf

Lackner, James R., and Paul DiZio. "Gravitoinertial Force Background
Level Affects Adaptation to Coriolis Force Perturbations of Reaching
Movements." *Journal of Neurophysiology*, vol. 80, 1998.

Marin, Frédéric, and Camille Beluffi. "Computing the Minimal Crew
for a Multi-Generational Space Journey." *arXiv*, 2018,
arXiv:1806.03856.

Salotti, Jean-Marc. "Minimum Number of Settlers for Survival on
Another Planet." *Scientific Reports*, vol. 10, 2020.

Carter, Layne, et al. "Water Recovery System (WRS) and Urine Processor
Assembly (UPA) Status." *38th International Conference on Environmental
Systems*, 2009. — Documents pre-BPA 93% ISS performance.

Gatens, Robyn, et al. "Status of ISS Water Management and Recovery."
*54th International Conference on Environmental Systems*, NTRS 20240005472,
2024. — Documents 98% BPA milestone and Mars requirement.

Smith, Cameron M. "Estimation of a Genetically Viable Population for
Multigenerational Interstellar Voyaging." *Acta Astronautica*, vol.
97, 2014, pp. 16–29.

Stone, Ralph W. "An Overview of Artificial Gravity." *NASA*, 1970.

Waldie, James M.A., et al. "Partial Gravity of Moon and Mars as
Countermeasure." *NASA*, 2021. *NTRS*, 20210019591.
