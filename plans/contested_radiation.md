# Contested: Radiation Limits and the Linear No-Threshold Model

## The Question

Two separate debates are entangled here: (1) how dangerous is deep-space
radiation quantitatively, and (2) does LEO habitat placement make the problem
tractable? The answer to both depends heavily on which cancer-risk model you
accept — and that model is itself contested.

## The Radiation Environment: Hard Numbers

The Curiosity rover's RAD (Radiation Assessment Detector) instrument produced
the first direct measurements of deep-space radiation during the
Earth-to-Mars transit (2011–2012) **(Zeitlin et al. 2013)**:

| Environment | Dose rate | Annual equivalent |
|---|---|---|
| Earth surface | $\sim 2.4\ \text{mSv/year}$ | 2.4 mSv |
| ISS (LEO, ~400 km) | $\sim 0.5\ \text{mSv/day}$ | ~200 mSv |
| Deep space transit | $\sim 1.84\ \text{mSv/day}$ | ~670 mSv |
| Mars surface | $\sim 0.7\ \text{mSv/day}$ | ~250 mSv |

A round-trip Mars transit at 180 days each way delivers approximately
**662 mSv** — before landing. NASA's most conservative career radiation limit
(early-career female astronaut) is approximately **600 mSv lifetime**
**(NASA-STD-3001 2015)**. A single Mars round-trip statistically exceeds
NASA's own safety standard before the mission begins.

The dose consists primarily of two sources:

- **Galactic Cosmic Rays (GCR):** High-energy charged particles from outside
  the solar system. Constant flux; modulated slightly by solar cycle.
  Effectively impossible to fully shield without enormous material mass:
  $$m_{\text{shield}} \approx \sigma_{\text{areal}} \cdot A_{\text{hull}}$$
  where $\sigma_{\text{areal}} \approx 4{,}500\ \text{kg/m}^2$ for meaningful
  GCR attenuation — the dominant mass driver for any deep-space habitat.

- **Solar Particle Events (SPE):** Unpredictable bursts from solar flares.
  Relatively easy to shield against (lower energy than GCR); a storm shelter
  with $\sim 30\ \text{g/cm}^2$ aluminium equivalent provides adequate
  protection.

## Contested Layer 1: The Linear No-Threshold Model

**What LNT says:** Every additional millisievert of radiation linearly
increases cancer mortality risk, with no threshold below which additional
exposure is harmless. The BEIR VII report (2006) — the most authoritative
review — upholds LNT as the policy-appropriate model:

$$\text{Excess cancer risk} = r_0 + \alpha \cdot D$$

where $D$ is dose and $\alpha \approx 5\%$ excess lifetime mortality risk per
Sievert for a mixed-age population **(BEIR VII 2006)**.

Under LNT, a deep-space radiation dose of 662 mSv (Mars round trip) implies
approximately **3.3% excess lifetime cancer mortality** — roughly equivalent
to adding 25–30 years of terrestrial background exposure.

**Camp 1 — LNT is correct (NASA, mainstream radiobiology):**

The LNT model is well-supported at moderate doses (>100 mSv) by atomic bomb
survivor data (Life Span Study) and occupational radiation studies. It is
deliberately conservative below 100 mSv because the mechanism (radiation
damage to DNA) is real and observable at the cellular level. Until evidence
clearly shows otherwise, designing to LNT is appropriate.

**Camp 2 — LNT overstates risk at moderate doses:**

A significant minority of radiobiologists argue that LNT is a conservative
extrapolation below $\sim 100\ \text{mSv}$, not an empirically established
relationship **(Calabrese and O'Connor 2014)**. The competing evidence:

- **High-background radiation populations:** Inhabitants of Kerala, India
  (average $\sim 70\ \text{mSv/year}$) and Ramsar, Iran (up to
  $\sim 260\ \text{mSv/year}$) show no elevated cancer incidence compared
  to control populations despite lifetime exposures far exceeding nominal
  safety limits. **(Ghiassi-nejad et al. 2002)**

- **Radiation hormesis:** At low-to-moderate doses, radiation may activate
  DNA repair pathways and immune surveillance, resulting in a net protective
  effect. This "inverted-U" dose-response is well-documented in cellular and
  animal models **(Calabrese and Baldwin 2001)**.

- **BEIR VII's own language:** The report states that LNT at low doses is a
  "policy assumption" in the absence of direct evidence, not a mechanistic
  certainty. The LNT vs. threshold vs. hormesis debate is explicitly
  acknowledged.

The practical consequence: if LNT is wrong at the dose ranges relevant to
space settlement (200–700 mSv/year), the cancer risk from deep-space
habitation may be materially lower than current NASA limits assume, and
missions currently classified as unsafe under NASA's framework would be
acceptable.

## Contested Layer 2: LEO vs. Deep Space — The Magnetosphere Argument

Globus and Hall (2017) observe that Earth's magnetosphere provides
substantial GCR protection in low Earth orbit — essentially for free. At
$\sim 500\ \text{km}$ altitude (above most atmospheric drag, below the
inner Van Allen belt), the radiation environment is approximately
**10–20× Earth surface background** rather than the 100–300× of deep space.

**The LEO advantage:**

$$\text{Shielding mass reduction} \approx \frac{\sigma_{\text{deep space}}}{\sigma_{\text{LEO}}} \approx \frac{4{,}500}{300\text{–}500}\ \text{kg/m}^2$$

This is not a minor calibration. A habitat at L5 requires ~4,500 kg/m² of
shielding material — the primary reason O'Neill-style construction required
lunar mass drivers to be economically feasible. A LEO habitat requires
perhaps one-tenth of that, enabling construction with near-Earth materials
and existing heavy-lift vehicles.

**Arguments against LEO:**

1. **Van Allen belt passes:** Spacecraft at $\sim 500\ \text{km}$ in certain
   orbital inclinations make repeated passes through the inner Van Allen belt
   (electrons and protons trapped by Earth's magnetic field). ISS mitigates
   this by flying at $51.6°$ inclination; permanent habitats might require
   careful orbit selection.

2. **Solar Particle Events:** The magnetosphere partially attenuates SPE flux
   but does not eliminate it at LEO altitudes. A severe SPE during a period
   of reduced magnetospheric protection could deliver acute doses that would
   be problematic.

3. **The long-term question:** ISS radiation data (200 mSv/year) is still
   substantially above Earth surface levels. Long-duration habitation at
   these doses over decades is not well-characterized.

## The Compounded Uncertainty

The two debates interact: if LNT overstates risk, then the 200 mSv/year LEO
environment may be entirely safe for permanent habitation. If LNT is correct,
LEO is still somewhat elevated but within acceptable ranges for a productive
life, while deep-space/L5 habitation is a genuine multi-decade cancer sentence.

| LNT correct? | LEO acceptable? | Deep space acceptable? |
|---|---|---|
| Yes | Borderline (~3–4% excess risk per decade) | No (mission exceeds career limit) |
| No (threshold ~100 mSv) | Yes | Possibly |
| Hormesis | Yes (possibly beneficial) | Probably yes |

No other single scientific question more directly determines where humans can
permanently live in space, and no other single question has a harder time being
resolved given the ethical barriers to controlled human radiation exposure
studies.

## Implications for This Model

This model treats shielding as a constraint parameter:
`shielding_areal_density_kg_m2`, defaulting to $4{,}500\ \text{kg/m}^2$
(NASA's GCR standard for deep space). The radiation constraint is currently
a feasibility check on whether this value is met — it does not model the
probabilistic cancer risk directly. The LNT vs. threshold debate therefore
sits outside the current model's scope, but it is the dominant uncertainty
over whether the $4{,}500\ \text{kg/m}^2$ figure is the right target at all.

## References

- BEIR VII (Committee on the Biological Effects of Ionizing Radiation).
  *Health Risks from Exposure to Low Levels of Ionizing Radiation: BEIR VII
  Phase 2.* National Academies Press, 2006. **(BEIR VII 2006)**
- Calabrese, Edward J., and Linda A. Baldwin. "Hormesis: the dose-response
  revolution." *Annual Review of Pharmacology and Toxicology* 43.1 (2001):
  175–197. **(Calabrese and Baldwin 2001)**
- Calabrese, Edward J., and M. K. O'Connor. "Estimating risk of low radiation
  doses — a critical review of the BEIR VII report and its use of the linear
  no-threshold (LNT) hypothesis." *Radiation Research* 182.5 (2014): 463–474.
  **(Calabrese and O'Connor 2014)**
- Ghiassi-nejad, M., et al. "Very high background radiation areas of Ramsar,
  Iran: preliminary biological studies." *Health Physics* 82.1 (2002): 87–93.
  **(Ghiassi-nejad et al. 2002)**
- Globus, Al, and Theodore Hall. "Space Settlement: An Easier Way."
  *NSS Space Settlement Journal* (2017). **(Globus and Hall 2017)**
- NASA-STD-3001. *NASA Space Flight Human-System Standard, Vol. 1: Crew
  Health.* Rev B. NASA, 2015. **(NASA-STD-3001 2015)**
- Zeitlin, Cary, et al. "Measurements of Energetic Particle Radiation in
  Transit to Mars on the Mars Science Laboratory." *Science* 340.6136 (2013):
  1080–1084. **(Zeitlin et al. 2013)**
