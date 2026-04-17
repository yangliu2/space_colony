# Contested: Maximum Tolerable Rotation Rate

## The Question

What is the highest rotation rate (RPM) at which humans can live and work
comfortably over months and years? This single number determines the minimum
viable radius of any rotating habitat — and therefore its entire economics.

## Why It Matters So Much

At $1g$ target gravity, minimum radius scales as:

$$r_{\min} = \frac{g}{\omega^2} = \frac{9.81}{(n \cdot 2\pi/60)^2}$$

| RPM limit | Minimum radius at 1g |
|---|---|
| 1 RPM | 895 m |
| 2 RPM | 224 m |
| 3 RPM | 99 m |
| 4 RPM | 56 m |
| 6 RPM | 25 m |

The difference between accepting 2 RPM and accepting 4 RPM is a factor of 4
in radius — roughly $16\times$ in interior floor area, and the difference
between a structure that requires asteroid mining to build and one that could
plausibly be assembled in low Earth orbit with near-term technology.

## The Primary Data Source: Graybiel (1969–1977)

Ashton Graybiel's experiments at the Naval Aerospace Medical Research
Laboratory remain the foundational dataset **(Graybiel 1969; Graybiel et al.
1977)**. Subjects were exposed to rotating rooms at various RPMs:

| Rotation rate | Reported effects |
|---|---|
| 1 RPM | No symptoms. Universal tolerance. |
| 3 RPM | Initial nausea and disorientation during head movements; most subjects adapted within days |
| 5.4 RPM | Significant symptoms; minority adapted, majority did not |
| 10 RPM | Intolerable; no adaptation observed |

The physiological mechanism is well understood. When a person moves their head
inside a rotating environment, the Coriolis force creates an unexpected
cross-axis angular acceleration:

$$\vec{a}_{\text{Coriolis}} = -2\,\vec{\omega} \times \vec{v}_{\text{head}}$$

The vestibular system interprets this as an unexpected tilt or rotation.
Lackner and DiZio (1998) quantified the relationship precisely: the
disturbance magnitude scales linearly with $\omega$ and with the angular
velocity of the head movement **(Lackner and DiZio 1998)**. Slower rotation →
smaller Coriolis disturbance → less disorientation.

## Camp 1: 2 RPM Maximum (NASA / Conservative Standard)

**Position:** The Graybiel data shows reliable symptoms emerging above 3 RPM,
and individual variation is large. A conservative engineering standard of
2 RPM protects the most sensitive individuals and leaves margin for unplanned
head movements (sneezing, stumbling, rapid turns).

**The habituation caveat:** Proponents acknowledge that 3 RPM showed
adaptation in most subjects — but note that Graybiel's experiments lasted
days to weeks. Long-term stability of that adaptation is unknown. Symptoms
could return at month 6 or year 2 in ways the short studies could not detect.

**Supporting evidence for caution:**
- The linear $\omega$-scaling means that as rotation rises, every head
  movement costs more vestibular disruption
- Individual variation in Graybiel's 3 RPM trials was substantial — some
  subjects never adapted. A habitat cannot be designed for the median tolerance
  if the worst-case 10% experience chronic nausea
- Lackner and DiZio's work shows that adaptation acquired in one rotating
  environment does not fully transfer when the environment changes (speed,
  direction) — suggesting adaptation may be context-specific

## Camp 2: 4 RPM Is Supportable (Globus and Hall 2017)

**Position:** The Graybiel data has been over-conservatively interpreted.
Careful re-analysis supports 4 RPM as a workable standard.

**Key arguments:**

1. **Adaptation was observed at 3 RPM.** Most subjects in Graybiel's 3 RPM
   trials adapted fully within 4–12 days. The 2 RPM standard was set below
   the adaptation threshold, leaving substantial tolerance unexploited.

2. **The critical experiment has not been done.** No study has exposed subjects
   to 3–4 RPM for 6+ months. The adaptation observed at shorter timescales is
   encouraging; the absence of long-term data is not evidence of failure.

3. **Gradual habituation protocols.** Lackner and DiZio's work suggests that
   incremental exposure — starting at low RPM and gradually increasing —
   produces more robust adaptation than sudden exposure to the target rate.
   Graybiel's studies did not use graduated protocols.

4. **Head movement restriction.** At 4 RPM, simply training residents to move
   their heads more slowly when changing orientation may be sufficient to
   eliminate acute symptoms. Lackner and DiZio showed that Coriolis disturbance
   is proportional to head angular velocity; at slow head movements even 6 RPM
   may be tolerable **(Lackner and DiZio 1998)**.

Globus and Hall (2017) propose a design standard of 4 RPM based on this
evidence, which reduces minimum viable radius at $1g$ to 56 m — potentially
enabling orbital habitats buildable with current heavy-lift launch vehicles.

## The Unresolved Issue: Short-Duration Studies and Long-Term Stability

Both camps accept the same underlying data. The disagreement is about inference:

| Question | Conservative answer | Globus answer |
|---|---|---|
| Is adaptation at 3 RPM real? | Yes, but short-term | Yes, and likely stable |
| Is 4 RPM tolerable with training? | Possibly, but unproven | Probably yes |
| Does adaptation persist for months? | Unknown — requires study | Plausibly yes |
| What about sensitive individuals? | Must design for worst case | Train or screen |

The "worst-case individual" framing is an important philosophical split. NASA
habitually designs for the most sensitive 5th-percentile astronaut. A
permanent colony of 10,000 people might adopt a population-health framing
instead — accepting that some residents experience minor chronic symptoms while
the majority are comfortable — in the same way Earth's rotating amusement parks
are not designed to the motion-sickness sensitivity of the most susceptible 5%.

## Implications for This Model

This model uses a default `max_comfortable_rpm` of **2.0 RPM**, consistent
with the conservative NASA standard. The slider permits exploration up to
6 RPM. The cross-coupling constraint — which evaluates the angular acceleration
experienced during a head turn at the habitat's rotation rate — is the
binding lower-radius constraint in most designs; this is the formalized
version of the Graybiel/Lackner physics.

The empirical question of whether 4 RPM is acceptable for months-to-years
duration remains open. Its resolution would shift the minimum viable habitat
radius from $\sim 980\ \text{m}$ to $\sim 56\ \text{m}$ — a change with
civilization-scale economic implications.

## References

- Graybiel, Ashton. "Structural Elements in the Concept of Motion Sickness."
  *Aerospace Medicine* 40.4 (1969): 351–367. **(Graybiel 1969)**
- Graybiel, Ashton, et al. "Experiment M-131: Human vestibular function."
  *Biomedical Results from Skylab* (1977): 74–103. **(Graybiel et al. 1977)**
- Globus, Al, and Theodore Hall. "Space Settlement: An Easier Way."
  *NSS Space Settlement Journal* (2017). **(Globus and Hall 2017)**
- Lackner, James R., and Paul DiZio. "Adaptation in a rotating artificial
  gravity environment." *Brain Research Reviews* 28.1–2 (1998): 194–202.
  **(Lackner and DiZio 1998)**
