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
(ECLSS) currently achieves approximately 93% water recovery through two
subsystems **(Carter et al. 2009)**:

- **Urine Processor Assembly (UPA):** Distils urine to brine; ~85% recovery
- **Water Recovery System (WRS):** Processes condensate + UPA distillate;
  combined recovery ~93%

ISS net consumption is approximately 3.6 L/person/day — a result of severe
rationing, not of high efficiency. A comfortable long-duration colony running
full sanitation at 20 L/person/day at 93% efficiency would still lose
1.4 L/person/day.

At 8,000 people, that is 11,200 L/day = **4,088 tonnes/year** of irrecoverable
water — the equivalent of roughly 1,360 Falcon 9 payload deliveries annually.
This makes the 93% ISS level entirely non-viable for a permanent colony.

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
| $\eta$ | `water_recycling_efficiency` | 0.90 | Carter et al. 2009 |
| $\eta_{min}$ | `min_water_recycling_efficiency` | 0.98 | Design target |

## Key Insight

The constraint fails by default (0.90 < 0.98) — current ISS technology does
not meet the threshold for permanent habitation. Achieving 0.98 requires two
advances beyond ECLSS: (1) improved brine drying to recover the last water from
the UPA brine, and (2) solid-waste water extraction. Both are active NASA
research areas **(Wieland 1994)**.

## References

- Carter, Layne, et al. "Water Recovery System (WRS) and Urine Processor Assembly
  (UPA) Status." *38th International Conference on Environmental Systems.* 2009.
  **(Carter et al. 2009)**
- Hanford, Anthony J. *Advanced Life Support Baseline Values and Assumptions
  Document.* NASA/CR-2004-208941. NASA, 2004. **(Hanford 2004)**
- Hendrickx, Lieve, et al. "Microbial ecology of the closed artificial ecosystem
  MELiSSA." *Advances in Space Research* 23.12 (2019): 1–15.
  **(Hendrickx et al. 2019)**
- Wieland, Paul O. *Designing for Human Presence in Space: An Introduction to
  Environmental Control and Life Support Systems.* NASA Reference Publication
  1324. NASA, 1994. **(Wieland 1994)**
