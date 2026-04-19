# Constraint 17: Water Recycling Efficiency

## Physical Motivation

A space habitat has no connection to Earth's hydrological cycle. Every litre of
water that escapes the system — through evaporation venting, chemical reactions,
equipment losses, or biological output that is not recaptured — must be replaced
by water launched from Earth or extracted from local resources (lunar ice,
asteroids). At current launch costs, water is the most mass-expensive consumable
to resupply. The habitat's water recycling loop must therefore approach
thermodynamic closure.

## The Closed-Loop Water Balance

Let $N$ be the colony population, $D_{pp}$ the daily domestic water demand per
person (L/day), and $\eta$ the recycling efficiency (fraction recovered per
cycle). The total daily water throughput is:

$$D_{total} = D_{pp} \cdot N \quad [\text{L/day}]$$

Water that is not recovered constitutes a net daily loss:

$$L_{day} = D_{total} \cdot (1 - \eta) \quad [\text{L/day}]$$

Since the density of water is approximately 1 kg/L, the annual mass loss is:

$$L_{year} = L_{day} \cdot 365 \quad [\text{kg/year}]$$

For long-term self-sufficiency without routine resupply, the recycling efficiency
must meet a minimum threshold $\eta_{min}$:

$$\eta \geq \eta_{min}$$

**This is the feasibility condition.**

## What This Model Covers

This constraint models **domestic water** only: drinking, food preparation,
hygiene, and laundry. Agricultural water is a separate, largely self-contained
subsystem — evapotranspiration from crops is recovered via greenhouse
condensation at efficiencies >97%, making it a tighter loop than the domestic
system **(Hendrickx et al. 2019)**. Modelling the two separately reflects how
they are engineered in practice (ECLSS handles domestic; the greenhouse handles
agricultural).

## Numerical Reference

NASA's Baseline Values and Assumptions Document (BVAD) specifies domestic water
demand for a space habitat at approximately 22 L/person/day **(Hanford 2004)**:

| Use | Demand (L/person/day) |
|---|---|
| Potable (drinking/cooking) | 2.0 |
| Oral hygiene | 0.4 |
| Hand/face wash | 4.1 |
| Shower | 2.7 |
| Clothes washing | 12.5 |
| Urinal flush | 0.5 |
| **Total** | **~22** |

The model default of 20 L/person/day is close to this figure.

## ISS ECLSS Baseline

The International Space Station Environmental Control and Life Support System
(ECLSS) has progressed through two distinct performance eras:

**Pre-BPA era (~2009–2021): ~93% recovery**

Original ECLSS achieved approximately 93% water recovery through two
subsystems **(Carter et al. 2009)**:

- **Urine Processor Assembly (UPA):** Distils urine to brine; ~85% recovery
- **Water Recovery System (WRS):** Processes condensate + UPA distillate;
  combined recovery ~93%

**Current era (with BPA, 2024): 98% recovery**

NASA's Brine Processor Assembly (BPA), activated in 2023–2024, recovers
approximately 95–98% of the residual water from the UPA brine output.
Combined with an improved UPA achieving ~87–98% urine recovery, the total
system now achieves **98% water recovery** — the Mars mission threshold
**(Gatens et al. 2024)**. This was described as a milestone for long-duration
exploration.

ISS net consumption is approximately 3.6 L/person/day — a result of severe
rationing, not of high efficiency. A comfortable long-duration colony running
full sanitation at 20 L/person/day at the historical 93% efficiency would
lose 1.4 L/person/day per person.

At 8,000 people, that historical 93% loss rate is 11,200 L/day =
**4,088 tonnes/year** — roughly 1,360 Falcon 9 payloads annually. Even at the
current ISS level of 98%, loss is 818 t/year. For a fully isolated habitat,
any non-zero loss eventually depletes the supply; 98% is viable only if loss
is covered by local resource extraction (ISRU) or very infrequent resupply.

One analysis of the 98% regime noted the operational margin is **"too small
for comfort"** when accounting for disposal paths — hygiene towels, wipes,
and contamination losses — that bypass the recovery system entirely.
Future designs targeting 99%+ are an active NASA research direction.

## Required Efficiency for Self-Sufficiency

For a colony of $N$ people at demand $D_{pp}$ and a target maximum annual loss of
$L_{max}$ kg/year, the required efficiency is:

$$\eta_{min} = 1 - \frac{L_{max}}{D_{pp} \cdot N \cdot 365}$$

For $L_{max} = 0$ (fully closed loop): $\eta_{min} = 1.0$, which is physically
unachievable. In practice the goal is to reduce losses to a level manageable
by local resource extraction (lunar ice mining, comet ice) or very infrequent
resupply.

The model default $\eta_{min} = 0.98$ represents the minimum efficiency for a
colony where annual water loss is small enough to be covered by in-situ resource
utilisation (ISRU).

## Consequences of Failing the Constraint

| $\eta$ | Annual loss (8,000 people, 20 L/day) | Equivalent launches |
|---|---|---|
| 0.90 (ISS level) | 4,088 t/year | ~1,360/year |
| 0.95 | 2,044 t/year | ~680/year |
| 0.98 (threshold) | 818 t/year | ~273/year |
| 0.99 | 409 t/year | ~136/year |
| 0.999 | 41 t/year | ~14/year |

The Falcon 9 equivalent is based on ~3 t useful payload to orbit.

## Model Inputs

| Symbol | Parameter | Default | Source |
|---|---|---|---|
| $D_{pp}$ | `water_per_person_day_liters` | 20 L/day | Hanford 2004 |
| $\eta$ | `water_recycling_efficiency` | 0.98 | Design target |
| $\eta_{min}$ | `min_water_recycling_efficiency` | 0.98 | Design target |

## Key Insight

The default (0.98) represents NASA's stated minimum for Mars/permanent missions
and has now been demonstrated on the ISS (2024) with the BPA. It is
well-supported by the literature.

One important caveat: 98% is the thermodynamic recovery from the active ECLSS
loop. Actual habitat water loss also includes passive disposal paths (wipes,
hygiene towels, contaminated water) not captured by the system. The effective
whole-habitat efficiency may be lower. For a permanent colony, the "system
efficiency" the model checks is the ECLSS fraction; the designer must separately
minimise non-loop waste paths.

Users can slide `water_recycling_efficiency` below 0.98 to see what pre-BPA
ISS-level loss rates imply at colony scale.

## References

- Carter, Layne, et al. "Water Recovery System (WRS) and Urine Processor Assembly
  (UPA) Status." *38th International Conference on Environmental Systems.* 2009.
  **(Carter et al. 2009)** — Documents pre-BPA 93% performance.
- Gatens, Robyn, et al. "Status of ISS Water Management and Recovery." *54th
  International Conference on Environmental Systems.* NTRS 20240005472. 2024.
  **(Gatens et al. 2024)** — Documents 98% BPA achievement and Mars mission
  requirement.
- Hanford, Anthony J. *Advanced Life Support Baseline Values and Assumptions
  Document.* NASA/CR-2004-208941. NASA, 2004. **(Hanford 2004)**
- Hendrickx, Lieve, et al. "Microbial ecology of the closed artificial ecosystem
  MELiSSA." *Advances in Space Research* 23.12 (2019): 1–15.
  **(Hendrickx et al. 2019)**
- Wieland, Paul O. *Designing for Human Presence in Space: An Introduction to
  Environmental Control and Life Support Systems.* NASA Reference Publication
  1324. NASA, 1994. **(Wieland 1994)**
