# Energy Budget Constraint

## Problem Statement

The habitat needs electricity for life support, lighting, agriculture, communications,
and general use. In space, the only practical source at L5 is photovoltaic solar panels.
The constraint asks: **do the solar panels fit on the available hull area?**

## Power Demand

Total electrical demand scales with population:

$$P_\text{total} = P_\text{pp} \cdot N$$

where $P_\text{pp}$ is power per person (W/person) and $N$ is population.

**Baseline:** NASA's ISS operates at roughly 75–84 kW for 6–7 crew, or ~12 kW/person
(Howell 2021). But ISS is an experimental station with heavy scientific equipment.
A residential colony with efficient LED agriculture and industrial loads is modelled at
**5,000 W/person** (5 kW/person), consistent with modern developed-world residential +
light-industrial usage at high energy efficiency (IEA 2023).

| Use case | W/person |
|---|---|
| ISS (research station) | ~12,000 |
| Colony baseline (this model) | 5,000 |
| Efficient colony (LED + heat pumps) | 3,000 |
| Minimal survival | 1,000 |

## Required Solar Panel Area

Solar panels convert sunlight to electricity:

$$A_\text{solar} = \frac{P_\text{total}}{\eta \cdot I_\odot}$$

where:
- $\eta$ — photovoltaic efficiency (dimensionless). Current high-efficiency panels:
  ~20% silicon, ~29% GaAs (NREL 2024). Default: **0.20**.
- $I_\odot = 1{,}361\ \text{W/m}^2$ — solar irradiance at 1 AU / L5 (Kopp and Lean 2011).

## Available Panel Area

Solar panels mount on the **exterior end caps**, which face axially and receive a
consistent average flux. The end caps are on the non-rotating bearing framework
(or use slip rings), keeping panels sun-tracking without mechanical complexity.

$$A_\text{avail} = A_\text{endcaps} = 2\pi r^2$$

The barrel surface is unsuitable: it rotates at roughly 1 RPM, so panels would
constantly shadow each other and average less than half the end-cap flux.

## Constraint

$$A_\text{solar} \leq A_\text{avail}$$

i.e.:

$$\frac{P_\text{pp} \cdot N}{\eta \cdot I_\odot} \leq 2\pi r^2$$

## Numerical Results

### Minimum viable cylinder ($r = 982\ \text{m}$, $N = 8{,}000$)

$$A_\text{solar} = \frac{5{,}000 \times 8{,}000}{0.20 \times 1{,}361} \approx 146{,}900\ \text{m}^2$$

$$A_\text{avail} = 2\pi (982)^2 \approx 6{,}065{,}000\ \text{m}^2$$

**Panel coverage fraction: ~2.4%.** End caps could power roughly 40× the population.

### O'Neill Island Three reference ($r = 3{,}200\ \text{m}$, $N = 10{,}000$)

$$A_\text{solar} \approx 183{,}600\ \text{m}^2$$

$$A_\text{avail} \approx 64{,}339{,}000\ \text{m}^2$$

**Panel coverage fraction: ~0.29%.** Trivially feasible.

### Maximum supportable population at $r = 982\ \text{m}$

Setting $A_\text{solar} = A_\text{avail}$:

$$N_\text{max} = \frac{\eta \cdot I_\odot \cdot 2\pi r^2}{P_\text{pp}}
= \frac{0.20 \times 1{,}361 \times 6{,}065{,}000}{5{,}000} \approx 330{,}000$$

Energy becomes binding only at extreme population densities far beyond what
the radiation-shielded surface area can support.

## Physical Insight

This constraint is **not a binding limit** in normal O'Neill designs.
End-cap solar panel area scales as $r^2$, while power demand scales as $N$,
and $N$ scales approximately as the interior surface area $\propto rL$.
For $L \propto r$ (aspect-ratio-constant designs) the panel-to-demand ratio
grows as $r / L \sim$ constant, always comfortable.

The only scenario where energy becomes tight is if you pack the habitat with
a much larger population than the surface area suggests — essentially a
high-density urban habitat.

## Model Inputs

| Parameter | Default | Location | Notes |
|---|---|---|---|
| $P_\text{pp}$ | 5,000 W | `HumanAssumptions.power_per_person_w` | Sensitivity knob |
| $\eta$ | 0.20 | `HumanAssumptions.solar_panel_efficiency` | Sensitivity knob |
| $I_\odot$ | 1,361 W/m² | `HumanAssumptions.solar_irradiance_w_m2` | Shared with thermal |
| $N$ | design param | `HabitatParameters.population` | — |
| $r$ | design param | `HabitatParameters.radius_m` | — |

## Skip Condition

The constraint is **skipped** (returns feasible) when `population == 0`, since
no power demand is defined.

## References

- Howell, Elizabeth. "International Space Station." NASA, 2021.
  <https://www.nasa.gov/reference/international-space-station>
- IEA (International Energy Agency). *World Energy Outlook 2023.* OECD/IEA, 2023.
- Kopp, Greg, and Judith L. Lean. "A new, lower value of total solar irradiance:
  Evidence and climate significance." *Geophysical Research Letters* 38.1 (2011).
  **(Kopp and Lean 2011)**
- NREL (National Renewable Energy Laboratory). *Best Research-Cell Efficiency Chart.*
  2024. <https://www.nrel.gov/pv/cell-efficiency.html>
- O'Neill, Gerard K. *The High Frontier: Human Colonies in Space.* Morrow, 1977.
