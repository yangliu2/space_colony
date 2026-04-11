# Thermal Management Constraint

## Summary

A space habitat has no atmosphere to conduct or convect heat away — radiation
is the only heat-rejection mechanism. The habitat must shed heat equal to:

1. **Solar gain** — sunlight entering through windows
2. **Internal waste heat** — people, lighting, equipment

The constraint checks whether the available radiator area on the outer hull is
sufficient to reject the total heat load at a comfortable operating temperature.

---

## Physics and Derivation

### Stefan-Boltzmann radiation

A surface at temperature $T$ radiates power:

$$P_\text{rad} = \varepsilon \sigma A_\text{rad} T^4$$

where $\varepsilon$ is emissivity (~0.9 for coated radiator panels),
$\sigma = 5.67 \times 10^{-8}$ W m⁻² K⁻⁴ is the Stefan-Boltzmann constant,
and $A_\text{rad}$ is the radiating area. Radiation scales as $T^4$, so
operating temperature is the dominant lever on radiator size.

### Heat sources

**Solar gain** through windows:

$$P_\text{solar} = I_\odot \cdot A_\text{window} \cdot \alpha$$

where $I_\odot = 1{,}361$ W/m² is the solar irradiance at 1 AU (L5 is
essentially at Earth's distance), $A_\text{window}$ is the window area, and
$\alpha$ is the net solar transmittance through the mirror-and-window system.

For an O'Neill cylinder with alternating land and window strips (three of
each), window area is approximately 50% of the barrel area:

$$A_\text{window} = f_w \cdot 2\pi r L, \quad f_w \approx 0.5$$

The mirrors outside each window can tilt to modulate $\alpha$. In practice
$\alpha \approx 0.2$–$0.5$ is achievable — the default model value of 0.3
represents a well-controlled mirror system reflecting roughly 70% of incident
sunlight back to space.

**Internal waste heat** from people and systems:

$$P_\text{internal} = \dot{q}_\text{pp} \cdot N$$

NASA BVAD (Hanford 2004) estimates $\dot{q}_\text{pp} \approx 350$ W/person
for a mixed-use habitat (metabolic heat + lighting + equipment).

### Thermal equilibrium

At steady state, heat in equals heat out:

$$P_\text{solar} + P_\text{internal} = \varepsilon \sigma A_\text{rad} T^4$$

Solving for required radiator area:

$$A_\text{rad,req} = \frac{I_\odot \cdot f_w \cdot 2\pi r L \cdot \alpha + \dot{q}_\text{pp} \cdot N}{\varepsilon \sigma T^4}$$

### Available radiator area

Radiators occupy the non-window hull area (land strips) plus the end caps:

$$A_\text{rad,avail} = (1 - f_w) \cdot 2\pi r L + 2\pi r^2$$

The constraint is:

$$A_\text{rad,req} \leq A_\text{rad,avail}$$

### Scaling behaviour

For large $L \gg r$, end-cap area becomes negligible and the ratio simplifies:

$$\frac{A_\text{rad,req}}{A_\text{rad,avail}} \approx
\frac{I_\odot \cdot f_w \cdot \alpha}{\varepsilon \sigma T^4 \cdot (1 - f_w)}$$

This is **independent of cylinder size** — it depends only on the four
thermal parameters. With default values ($\alpha = 0.3$, $T = 320$ K,
$\varepsilon = 0.9$, $f_w = 0.5$):

$$\text{ratio} \approx \frac{1361 \times 0.5 \times 0.3}{0.9 \times 5.67 \times 10^{-8} \times 320^4 \times 0.5}
= \frac{204.2}{267.7} \approx 0.76$$

So at defaults, roughly 76% of the land-strip area is needed for radiators —
feasible, but leaving only 24% for structure and external modules.

If mirror control degrades to $\alpha = 0.5$, the ratio rises to 1.27 —
infeasible without external radiator panels extending beyond the hull.

### Reference design spot-checks

| Design | $r$ (m) | $L$ (m) | $N$ | Ratio | Feasible? |
|---|---|---|---|---|---|
| Minimum viable | 982 | 1,276 | 8,000 | 0.30 | ✅ |
| O'Neill Island Three | 3,200 | 32,000 | 8,000 | 0.64 | ✅ |
| Alpha = 0.5 (poor mirror control) | 982 | 1,276 | 8,000 | 0.50 | ✅ |
| Alpha = 0.5 (poor mirror control) | 3,200 | 32,000 | 8,000 | 1.27 | ❌ |

The small habitat benefits from its large end-cap area relative to barrel
area; elongated cylinders are thermally tighter.

---

## Thresholds and Default Values

| Parameter | Default | Range | Basis |
|---|---|---|---|
| Solar irradiance $I_\odot$ | 1,361 W/m² | fixed (L5 ≈ 1 AU) | Kopp & Lean (2011) |
| Window fraction $f_w$ | 0.5 | 0.3–0.6 | O'Neill (1977) |
| Solar transmittance $\alpha$ | 0.3 | 0.1–0.8 | Mirror control |
| Waste heat per person $\dot{q}_\text{pp}$ | 350 W | 200–600 W | NASA BVAD (Hanford 2004) |
| Radiator temperature $T$ | 320 K | 280–400 K | Engineering choice |
| Radiator emissivity $\varepsilon$ | 0.9 | 0.85–0.95 | Coated aluminium |

---

## Implementation Notes

- Constraint is skipped when `length_m == 0` (geometry unavailable).
- All thermal parameters live in `HumanAssumptions` (sensitivity knobs);
  no new `HabitatParameters` fields are needed.
- The key UI slider is `window_solar_transmittance` — it represents mirror
  quality/angle control and is the dominant lever on feasibility.
- `details` reports: `solar_gain_w`, `internal_heat_w`, `total_heat_w`,
  `required_radiator_area_m2`, `available_radiator_area_m2`,
  `radiator_area_fraction`.

---

## References

- Hanford, Anthony J. *Advanced Life Support Baseline Values and Assumptions
  Document*. NASA/CR-2004-208941, 2004.
- Kopp, G., and J. L. Lean. "A new, lower value of total solar irradiance:
  Evidence and climate significance." *Geophysical Research Letters* 38.1
  (2011).
- O'Neill, Gerard K. *The High Frontier: Human Colonies in Space*. William
  Morrow, 1977.
- Siegel, R., and J. Howell. *Thermal Radiation Heat Transfer*. 4th ed.
  Taylor & Francis, 2002.
