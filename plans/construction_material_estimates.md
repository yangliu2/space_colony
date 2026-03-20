# Material Requirements for O'Neill Cylinder Habitats

**Date:** 2026-03-20  
**Scope:** Quantitative mass estimates for two cylinder scenarios  
**Inputs from:** Phase 2 constraint analysis (002), NASA SP-413, O'Neill (1977)

---

## Design Scenarios

| Parameter | Scenario 1: Minimum Viable | Scenario 2: O'Neill-Class |
|-----------|---------------------------|---------------------------|
| Radius | 982 m | 3,200 m |
| Length | 2,000 m (see §A) | 32,000 m |
| Target gravity | 1.0 g | 1.0 g |
| RPM | 0.95 | 0.53 |
| Rim speed | 98.1 m/s | 177.1 m/s |
| Population (est.) | ~8,000 | ~1,000,000+ |
| Surface area ($2\pi r L$) | 12.34 km² | 643.4 km² |
| End cap area ($2 \times \pi r^2$) | 6.06 km² | 64.34 km² |
| Total shell area | 18.4 km² | 707.7 km² |
| Interior volume ($\pi r^2 L$) | $6.06 \times 10^9$ m³ | $1.03 \times 10^{12}$ m³ |
| Usable floor area (~50% of barrel) | 6.17 km² | 321.7 km² |

### §A. Minimum Viable Length

The NASA SP-413 cylinder design used a 10:1 length-to-radius ratio. For a minimum viable habitat, a 2:1 ratio (L = 2,000 m) is defensible: it provides enough length for a meaningful community while keeping end-cap structural penalties manageable. Below ~1 km length, the end-cap mass fraction becomes prohibitive and the interior feels claustrophobic. A 2 km cylinder at 982 m radius provides ~6 km² of barrel surface, comparable to the Stanford torus's 6.8 × 10⁵ m² projected area but with far more volume.

---

## 1. Structural Shell Mass

### Hoop Stress Analysis

A rotating cylinder under internal atmospheric pressure and centripetal loading experiences hoop stress. For a thin-walled cylinder:

**Atmospheric hoop stress:**

$$
\sigma_{\text{atm}} = \frac{P \cdot r}{t}
$$

where $P$ = internal pressure, $r$ = radius, $t$ = wall thickness.

**Centripetal hoop stress** (from the shell's own mass and interior loading):

$$
\sigma_{\text{cent}} = \rho_{\text{shell}} \cdot \omega^2 \cdot r^2
$$

where $\rho_{\text{shell}}$ is the areal mass density of everything at the rim.

For the structural shell alone under atmospheric pressure, solving for minimum wall thickness:

$$
t_{\min} = \frac{P \cdot r}{\sigma_y}
$$

### Material Properties

| Material | Density (kg/m³) | Yield Strength (MPa) | Specific Strength (kN·m/kg) |
|----------|----------------|----------------------|-----------------------------|
| Mild steel (A36) | 7,850 | 250 | 32 |
| High-strength steel (maraging) | 8,000 | 1,400 | 175 |
| Aluminum 6061-T6 | 2,700 | 276 | 102 |
| Aluminum 7075-T6 | 2,810 | 503 | 179 |
| Titanium Ti-6Al-4V | 4,430 | 880 | 199 |
| Carbon fiber composite (CFRP) | 1,600 | 1,500 | 938 |

### Wall Thickness Calculations

**Scenario 1 (r = 982 m, P = 51 kPa at half-atmosphere per SP-413):**

| Material | t_min (mm) | t with SF=2 (mm) | t with SF=4 (mm) |
|----------|-----------|-------------------|-------------------|
| Mild steel | 200 | 400 | 800 |
| High-strength steel | 36 | 71 | 143 |
| Aluminum 6061-T6 | 181 | 361 | 722 |
| Aluminum 7075-T6 | 99 | 199 | 397 |
| Titanium Ti-6Al-4V | 57 | 114 | 228 |
| CFRP | 33 | 67 | 133 |

**Scenario 2 (r = 3,200 m, P = 101.3 kPa at full atmosphere):**

| Material | t_min (mm) | t with SF=2 (mm) | t with SF=4 (mm) |
|----------|-----------|-------------------|-------------------|
| Mild steel | 1,297 | 2,594 | 5,187 |
| High-strength steel | 231 | 463 | 926 |
| Aluminum 6061-T6 | 1,174 | 2,348 | 4,696 |
| Aluminum 7075-T6 | 644 | 1,289 | 2,578 |
| Titanium Ti-6Al-4V | 368 | 737 | 1,473 |
| CFRP | 216 | 432 | 864 |

*Note:* Full atmosphere (101.3 kPa) doubles the pressure load compared to the SP-413 half-atmosphere design (51 kPa). The "comfortable" scenario uses full atmosphere for Earth-normal conditions.

### Structural Shell Mass Estimates

$$
M_{\text{shell}} = \rho_{\text{material}} \times t_{\text{design}} \times A_{\text{surface}}
$$

**Scenario 1** (982 m radius, 2 km length, half-atmosphere):
Using high-strength steel at SF=3 ($t = 107$ mm):

$$
M_{\text{shell}} = 8{,}000 \times 0.107 \times 18.4 \times 10^6 = 15.7 \; \text{Mt}
$$

This is excessive. The NASA SP-413 found that cylinders require ~4× more structural mass per unit area than tori, which is why they rejected pure cylinders.

Using the SP-413's preferred aluminum at SF=2, with half-atmosphere:
For the barrel only (12.34 km²), aluminum 7075-T6, $t = 199$ mm:

$$
M_{\text{barrel}} = 2{,}810 \times 0.199 \times 12.34 \times 10^6 = 6.9 \; \text{Mt}
$$

**However**, the more relevant calculation follows the SP-413 approach. The NASA study found structural masses empirically:

| Configuration | Radius (m) | Structural Mass (kt) | Source |
|--------------|-----------|----------------------|--------|
| Stanford torus (r=830m) | 830 | 150 | SP-413 Table 4-1 |
| Cylinder (r=895m, L=8950m) | 895 | 42,300 | SP-413 Table 4-1 |
| Sphere (r=895m) | 895 | 3,545 | SP-413 Table 4-1 |
| SP-413 torus (built) | 895 | 156 | SP-413 Table 5-2 |

The SP-413 cylinder at r=895m, L=8950m had structural mass 42,300 kt = 42.3 Mt. Scaling:

**Scenario 1** — scaling from SP-413 cylinder by surface area ratio:

$$
A_{\text{SP-413}} = 2\pi \times 895 \times 8{,}950 = 50.3 \; \text{km}^2
$$

$$
A_{\text{S1}} = 2\pi \times 982 \times 2{,}000 = 12.3 \; \text{km}^2
$$

$$
M_{\text{struct,1}} \approx 42{,}300 \times \frac{12.3}{50.3} \approx 10{,}350 \; \text{kt} \approx 10.4 \; \text{Mt}
$$

But this overestimates because the SP-413 cylinder used full atmosphere. At half-atmosphere:

$$
M_{\text{struct,1}} \approx 10.4 \times 0.5 \approx 5.2 \; \text{Mt}
$$

**More realistic estimate using the torus shell density as a baseline:**
The Stanford torus shell was 156,000 t for a surface area of $2.1 \times 10^6$ m² = 74 kg/m².
A cylinder at the same radius faces higher hoop stress (larger radius of curvature in the longitudinal cross-section is infinite vs. 65m for the torus). The SP-413 found cylinders need ~4× more mass per unit projected area. Applying a 2× structural penalty over the torus:

$$
M_{\text{struct,1}} \approx 150 \; \text{kg/m}^2 \times 12.34 \times 10^6 \; \text{m}^2 = 1.85 \; \text{Mt}
$$

**Best estimate for Scenario 1 structural shell: 2 - 5 Mt** depending on material and safety factor choices.

**Scenario 2** — scaling from SP-413:

$$
A_{\text{S2}} = 2\pi \times 3{,}200 \times 32{,}000 = 643 \; \text{km}^2
$$

Direct calculation with high-strength steel, SF=3, full atmosphere, barrel only:

$$
t = \frac{3 \times 101{,}300 \times 3{,}200}{1{,}400 \times 10^6} = 0.695 \; \text{m}
$$

$$
M_{\text{barrel}} = 8{,}000 \times 0.695 \times 643 \times 10^6 = 3{,}575 \; \text{Mt}
$$

With CFRP, SF=3:

$$
t = \frac{3 \times 101{,}300 \times 3{,}200}{1{,}500 \times 10^6} = 0.649 \; \text{m}
$$

$$
M_{\text{barrel}} = 1{,}600 \times 0.649 \times 643 \times 10^6 = 668 \; \text{Mt}
$$

With aluminum 7075-T6, SF=3:

$$
t = \frac{3 \times 101{,}300 \times 3{,}200}{503 \times 10^6} = 1.934 \; \text{m}
$$

$$
M_{\text{barrel}} = 2{,}810 \times 1.934 \times 643 \times 10^6 = 3{,}493 \; \text{Mt}
$$

**Best estimate for Scenario 2 structural shell: 700 Mt (CFRP) to 3,500 Mt (steel/aluminum)**

*Key insight: structural shell mass scales as $r^2 \times L \times P / \sigma_y$. The O'Neill-class cylinder is enormously more massive due to the 3.26× radius increase and 16× length increase combined with doubled pressure.*

---

## 2. Radiation Shielding Mass

### Shielding Requirements

| Protection Level | Areal Density | Equivalent | Source |
|-----------------|---------------|------------|--------|
| Earth atmosphere | 1,033 g/cm² = 10,330 kg/m² | 10.3 t/m² | Standard physics |
| SP-413 design | 4,500 kg/m² | 4.5 t/m² | NASA SP-413 Ch. 4 |
| Minimum for 0.5 rem/yr | ~4,500 kg/m² | 4.5 t/m² | SP-413 (accounts for oblique incidence) |
| Minimum for 5 rem/yr (worker limit) | ~2,000 kg/m² | 2.0 t/m² | Estimated from SP-413 scaling |
| "Barely survivable" | ~1,500 kg/m² | 1.5 t/m² | See note below |

**Critical physics note from SP-413 Chapter 2:** At intermediate shielding depths (a few t/m²), cosmic ray dose *increases* to ~20 rem/yr due to secondary particle production (spallation). You must push through this "dose bump" to thicker shielding to reach the protective regime. The SP-413 found 4.5 t/m² was the minimum to get below 0.5 rem/yr. Going thinner than ~3 t/m² is actually *worse* than no shielding at all for cosmic rays.

**"Barely survivable" minimum:** Accepting 5 rem/yr (the radiation worker limit), and using water or hydrogen-rich materials (which produce fewer secondary neutrons than regolith), ~2 t/m² may be acceptable. But this is the occupational limit, not safe for families/children. For a true minimum with children, 4.5 t/m² is the floor.

### Shielding Geometry

The shielding must cover the projected cross-sectional area against isotropic cosmic rays. For a cylinder, the total surface requiring shielding is the full outer surface (barrel + end caps) since cosmic rays come from all directions.

**Scenario 1** ($r = 982$ m, $L = 2{,}000$ m):

$$
A_{\text{shield}} = 18.4 \times 10^6 \; \text{m}^2
$$

$$
\text{At } 4.5 \; \text{t/m}^2: \quad M_{\text{shield}} = 4{,}500 \times 18.4 \times 10^6 = 82.8 \; \text{Mt}
$$

$$
\text{At } 2.0 \; \text{t/m}^2: \quad M_{\text{shield}} = 2{,}000 \times 18.4 \times 10^6 = 36.8 \; \text{Mt}
$$

**Scenario 2** ($r = 3{,}200$ m, $L = 32{,}000$ m):

$$
A_{\text{shield}} = 707.7 \times 10^6 \; \text{m}^2
$$

$$
\text{At } 4.5 \; \text{t/m}^2: \quad M_{\text{shield}} = 4{,}500 \times 707.7 \times 10^6 = 3{,}185 \; \text{Mt}
$$

$$
\text{At } 10.3 \; \text{t/m}^2: \quad M_{\text{shield}} = 10{,}330 \times 707.7 \times 10^6 = 7{,}313 \; \text{Mt}
$$

### Shielding Material Options

| Material | Density (kg/m³) | Thickness for 4.5 t/m² | Notes |
|----------|----------------|------------------------|-------|
| Lunar regolith | 1,500 | 3.0 m | Primary SP-413 choice |
| Water | 1,000 | 4.5 m | Better H content, fewer secondaries |
| Lunar slag (processed) | 2,500 | 1.8 m | Denser, thinner layer |
| Polyethylene | 950 | 4.7 m | Best H density, expensive to produce |

**The SP-413 Stanford torus used 9.9 Mt of lunar regolith shielding** — this was by far the dominant mass component (~95% of total). The shielding was 1.7 m thick at the torus surface.

### Shielding Mass Summary

| Scenario | Minimum (2 t/m²) | SP-413 Standard (4.5 t/m²) | Earth-Equivalent (10.3 t/m²) |
|----------|------------------|-----------------------------|-------------------------------|
| 1: Minimum | 36.8 Mt | 82.8 Mt | 190 Mt |
| 2: O'Neill | 1,415 Mt | 3,185 Mt | 7,313 Mt |

---

## 3. Atmospheric Mass

### Atmospheric Pressure Options

| Atmosphere | Total Pressure | O₂ | N₂ | Notes |
|-----------|---------------|-----|-----|-------|
| SP-413 design | 51 kPa (0.5 atm) | 22.7 kPa | 26.6 kPa | Half-pressure, safe with enriched O₂ |
| Earth standard | 101.3 kPa (1 atm) | 21.2 kPa | 79.0 kPa | Full atmosphere |

### Atmospheric Mass Calculation

For a cylinder, the atmosphere fills the entire volume. Using the ideal gas law:

$$
M_{\text{atm}} = \frac{P \cdot V \cdot \bar{M}}{R \cdot T}
$$

where $\bar{M}$ is the mean molar mass (28.97 g/mol for Earth mix, ~26 g/mol for SP-413 mix), $R = 8.314$ J/(mol·K), and $T \approx 293$ K.

At sea level density $\rho_{\text{air}} = 1.225$ kg/m³ (Earth) or $\approx 0.7$ kg/m³ (SP-413 mix at 51 kPa):

**Scenario 1** ($V = 6.06 \times 10^9$ m³):

$$
\text{At 51 kPa:} \quad M_{\text{atm}} \approx 0.7 \times 6.06 \times 10^9 = 4.2 \; \text{Mt}
$$

$$
\text{At 101.3 kPa:} \quad M_{\text{atm}} \approx 1.225 \times 6.06 \times 10^9 = 7.4 \; \text{Mt}
$$

**Scenario 2** ($V = 1.03 \times 10^{12}$ m³):

$$
\text{At 101.3 kPa:} \quad M_{\text{atm}} \approx 1.225 \times 1.03 \times 10^{12} = 1{,}260 \; \text{Mt}
$$

$$
\text{At 51 kPa:} \quad M_{\text{atm}} \approx 0.7 \times 1.03 \times 10^{12} = 721 \; \text{Mt}
$$

**Cross-check with SP-413:** The SP-413 cylinder ($r = 895$ m, $L = 8{,}950$ m, $V = 2.25 \times 10^{10}$ m³) had atmospheric mass 14,612 kt = 14.6 Mt at 51 kPa. This gives $\rho \approx 0.65$ kg/m³, consistent with the lower molecular weight SP-413 mix.

### Atmospheric Mass Summary

| Scenario | SP-413 mix (51 kPa) | Earth standard (101.3 kPa) |
|----------|---------------------|---------------------------|
| 1: Minimum (982m × 2km) | 4.2 Mt | 7.4 Mt |
| 2: O'Neill (3200m × 32km) | 721 Mt | 1,260 Mt |

*Note: atmospheric mass is large but not dominant compared to shielding. For Scenario 2, it becomes a very significant fraction.*

---

## 4. Soil and Water Mass

### Soil Requirements

| Parameter | Minimum | Comfortable | Source |
|-----------|---------|-------------|--------|
| Soil depth for agriculture | 0.5 m | 1.0 - 2.0 m | SP-413, agricultural science |
| Dry soil density | 1,300 kg/m³ | 1,500 kg/m³ | Typical topsoil |
| Water content in soil | 10% by mass | 20% by mass | Agricultural standard |
| Agricultural area per person | 20 m² | 50 m² | SP-413 Table 5-4 |
| Residential area per person | 43 m² | 67 m² | SP-413 Ch. 3 & 4 |

### Soil Mass Estimates

**Scenario 1** (usable floor area $\approx 6.17$ km², ~50% agricultural):

$$
A_{\text{ag}} = 3.1 \; \text{km}^2 = 3.1 \times 10^6 \; \text{m}^2
$$

$$
M_{\text{soil}} = 0.5 \times 1{,}300 \times 3.1 \times 10^6 = 2.0 \; \text{Mt}
$$

$$
M_{\text{water in soil}} = 0.1 \times M_{\text{soil}} = 0.2 \; \text{Mt}
$$

**Scenario 2** (usable floor area $\approx 321.7$ km², generous allocation):

$$
M_{\text{ag soil}} = 1.5 \times 1{,}500 \times 10^8 = 225 \; \text{Mt}
$$

$$
M_{\text{parks}} = 0.5 \times 1{,}500 \times 10^8 = 75 \; \text{Mt}
$$

$$
M_{\text{water in soil}} = 0.2 \times 300 = 60 \; \text{Mt}
$$

$$
M_{\text{soil, total}} = 225 + 75 + 60 = 360 \; \text{Mt}
$$

### Water Requirements

**SP-413 reference:** 42,000 t water (20,000 t free water + 22,000 t in soil) for 10,000 people = 4.2 t/person.

| Water Category | Scenario 1 | Scenario 2 |
|---------------|------------|------------|
| Soil moisture | 0.2 Mt | 60 Mt |
| Rivers/lakes/reservoirs | 0.5 Mt | 200 Mt |
| Industrial/recycling | 0.1 Mt | 50 Mt |
| Humidity (in atmosphere) | ~0.1 Mt | ~10 Mt |
| **Total water** | **~1 Mt** | **~320 Mt** |

### Soil + Water Summary

| Component | Scenario 1 | Scenario 2 |
|-----------|------------|------------|
| Dry soil | 2.0 Mt | 300 Mt |
| Water (all forms) | 1.0 Mt | 320 Mt |
| **Total** | **3.0 Mt** | **620 Mt** |

---

## 5. Interior Mass (Buildings, Infrastructure, People)

### SP-413 Reference Data (10,000 population)

| Component | Mass (kt) | Per Capita (t/person) |
|-----------|----------|----------------------|
| Structures | 77 | 7.7 |
| Machinery | 40 | 4.0 |
| Biomass (plants) | 5 | 0.5 |
| Furnishings | 25 | 2.5 |
| People (avg 70 kg) | 0.7 | 0.07 |
| **Total interior** | **148** | **14.8** |

### Scaled Estimates

**Scenario 1** (population ~8,000):

$$
M_{\text{interior}} \approx 8{,}000 \times 14.8 = 118 \; \text{kt} \approx 0.12 \; \text{Mt}
$$

Rounding up for safety: **~0.2 Mt**

**Scenario 2** (population ~1,000,000):

$$
M_{\text{interior}} \approx 1{,}000{,}000 \times 14.8 = 14{,}800 \; \text{kt} \approx 14.8 \; \text{Mt}
$$

With more generous infrastructure (parks, transport, industry): **~30 Mt**

---

## 6. Total Mass Estimates

### Scenario 1: "Barely Survivable" Minimum Cylinder (982m × 2km)

| Component | Minimum Mass | Notes |
|-----------|-------------|-------|
| Structural shell | 2 Mt | CFRP, SF=2, half-atmosphere |
| Radiation shielding | 37 Mt | 2.0 t/m², worker-limit dose |
| Atmosphere | 4.2 Mt | SP-413 mix at 51 kPa |
| Soil + water | 3.0 Mt | Minimal agriculture |
| Interior | 0.2 Mt | Spartan infrastructure |
| **TOTAL** | **~46 Mt** | |

With SP-413 standard shielding (4.5 t/m²): **~92 Mt**

### Scenario 2: "Most Comfortable" O'Neill-Class Cylinder (3200m × 32km)

| Component | Mass | Notes |
|-----------|------|-------|
| Structural shell | 700 Mt (CFRP) to 3,500 Mt (metal) | SF=3, full atmosphere |
| Radiation shielding | 3,185 Mt (SP-413) to 7,313 Mt (Earth-equiv.) | 4.5 - 10.3 t/m² |
| Atmosphere | 1,260 Mt | Full Earth atmosphere |
| Soil + water | 620 Mt | Deep soil, lakes, rivers |
| Interior | 30 Mt | Full urban infrastructure |
| **TOTAL (CFRP + SP-413 shielding)** | **~5,800 Mt** | |
| **TOTAL (metal + Earth-equiv. shielding)** | **~12,700 Mt** | |

### Comparison with Literature

| Reference | Design | Total Mass | Notes |
|-----------|--------|-----------|-------|
| SP-413 (1975) | Stanford torus (r=830m) | ~10.5 Mt | Dominated by 9.9 Mt shielding |
| SP-413 (1975) | Cylinder (r=895m, L=8950m) | ~80+ Mt | 42.3 Mt structure + 23.3 Mt shield + 14.6 Mt atmo |
| O'Neill (1977) | Island Three (r=3200m, L=32km) | ~several thousand Mt | Order-of-magnitude consistent |
| ISS | LEO station | 0.00042 Mt (420 t) | For scale reference |

**The ISS comparison:** The "barely survivable" minimum cylinder is approximately **100,000× the mass of the ISS**. The O'Neill-class cylinder is roughly **10 million × the ISS mass**. This illustrates the extraordinary scale difference between current space construction and permanent habitats.

---

## 7. Material Sourcing

### Lunar Regolith Composition (by mass)

| Oxide | Fraction | Useful Elements |
|-------|----------|----------------|
| SiO₂ | 45% | Silicon, oxygen |
| Al₂O₃ | 15% | Aluminum |
| FeO | 15% | Iron |
| CaO | 10% | Calcium |
| MgO | 10% | Magnesium |
| TiO₂ | 5% | Titanium |

Lunar regolith provides: structural metals (Al, Fe, Ti), radiation shielding (bulk regolith/slag), oxygen (for atmosphere), silicon (for glass/solar cells). What it lacks: hydrogen (for water), carbon, nitrogen — these must come from asteroids, comets, or Earth.

### Source Requirements

**Scenario 1 (46 Mt minimum):**
- Shielding (37 Mt): Lunar regolith, minimally processed
- Structure (2 Mt): Lunar aluminum or asteroid iron/nickel
- Atmosphere N₂ (2.6 Mt): Asteroid volatiles or Earth import
- Atmosphere O₂ (1.6 Mt): Lunar regolith extraction
- Water (1 Mt): Asteroid ice or lunar polar ice
- Soil (2 Mt): Lunar regolith with organic amendments from asteroidal carbon

**Scenario 2 (5,800 Mt minimum):**
- Shielding (3,185 Mt): Lunar regolith — at SP-413's 1.2 Mt/yr extraction rate, this alone would take **2,654 years**. Multiple orders of magnitude increase in mining infrastructure required, or asteroid capture.
- Atmosphere N₂ (~1,000 Mt): Cannot come from the Moon (nitrogen-poor). Requires massive asteroidal/cometary sources.
- Water (320 Mt): Asteroid ice capture on industrial scale.

### The Nitrogen Problem

Earth's atmosphere is 78% N₂ by volume. The SP-413 half-atmosphere design reduces N₂ requirements, but even so, the Moon contains negligible nitrogen. For Scenario 2, ~1,000 Mt of nitrogen is needed. Carbonaceous chondrite asteroids contain 1-3% nitrogen by mass, so capturing and processing **30,000 - 100,000 Mt of asteroid material** would be required for nitrogen alone.

---

## 8. Key Formulas Summary

**Hoop stress (thin-walled cylinder):**

$$
\sigma = \frac{P \cdot r}{t}, \qquad t_{\min} = \frac{P \cdot r}{\sigma_y}, \qquad t_{\text{design}} = \frac{\text{SF} \cdot P \cdot r}{\sigma_y}
$$

**Shell mass:**

$$
M_{\text{shell}} = \rho_{\text{material}} \cdot t_{\text{design}} \cdot A_{\text{surface}}
$$

$$
A_{\text{barrel}} = 2\pi r L, \qquad A_{\text{endcaps}} = 2\pi r^2
$$

**Atmospheric mass:**

$$
M_{\text{atm}} = \rho_{\text{air}} \cdot V = \rho_{\text{air}} \cdot \pi r^2 L, \qquad \rho_{\text{air}} = \frac{P \cdot \bar{M}}{R \cdot T}
$$

At 101.3 kPa, 293 K: $\rho_{\text{air}} = 1.225$ kg/m³. At 51 kPa, 293 K: $\rho_{\text{air}} \approx 0.65$ kg/m³.

**Shielding mass:**

$$
M_{\text{shield}} = \sigma_{\text{areal}} \cdot A_{\text{total}}
$$

where $\sigma_{\text{areal}}$ is the areal density requirement (kg/m²).

**Centripetal acceleration (artificial gravity):**

$$
a = \omega^2 r = g_{\text{target}}, \qquad \omega = \sqrt{\frac{g}{r}}
$$

---

## References

- Johnson, Richard D., and Charles Holbrow, editors. *Space Settlements: A Design Study*. NASA SP-413, National Aeronautics and Space Administration, 1977. Chapter 4 (habitat selection), Chapter 5 (colony design), Chapter 6 (construction).

- O'Neill, Gerard K. *The High Frontier: Human Colonies in Space*. William Morrow and Company, 1977. Island Three specifications: paired cylinders, 3.2 km radius, 32 km length, ~1 million population.

- O'Neill, Gerard K. "The Colonization of Space." *Physics Today*, vol. 27, no. 9, 1974, pp. 32-40. Original proposal for L5 colonies using lunar materials.

- NASA SP-413, Chapter 2: "Physical Properties of Space." Cosmic ray flux of ~10 rem/yr unshielded; secondary particle production at intermediate shielding depths; 4.5 t/m² minimum for 0.5 rem/yr.

- NASA SP-413, Chapter 3: "Human Needs in Space." Atmospheric requirements (51 kPa total, 22.7 kPa O₂, 26.6 kPa N₂), gravity (0.95 ± 0.05 g), radiation (<0.5 rem/yr), area per person (67 m²).

- NASA SP-413, Chapter 4, Table 4-1: Comparison of habitat configurations — structural mass, shielding mass, and atmospheric mass for torus, cylinder, sphere, and dumbbell geometries at 1 rpm, 0.95g.

- NASA SP-413, Chapter 5, Tables 5-2 and 5-3: Stanford torus mass breakdown — 9.9 Mt shielding, 156 kt shell, 220 kt soil, 42 kt water, 530 kt interior total.

- Globus, Al, and Tom Marotta. "The High Frontier: An Easier Way." *NSS Space Settlement Journal*, 2018. Updated analysis arguing for smaller habitats at lower Earth orbits within the Van Allen belts (reducing shielding requirements).

---

## Conclusions

1. **Shielding dominates everything.** In both scenarios, radiation shielding is the largest or second-largest mass component. The SP-413 found this in 1975, and it remains true. Any design optimization must start with shielding.

2. **The structural shell is the second crisis.** At O'Neill-class scales with full atmosphere, even CFRP requires ~700 Mt of structural shell. The hoop stress scales linearly with both radius and pressure. The SP-413's decision to use half-atmosphere (51 kPa) and a torus (smaller radius of curvature) were driven by this structural reality.

3. **Atmospheric mass is non-trivial.** The O'Neill cylinder contains 1,260 Mt of air at full atmosphere — more than the structural shell in some material scenarios. The nitrogen sourcing problem is severe.

4. **The minimum viable cylinder (~46 Mt) is achievable with lunar resources** in principle, though it requires industrial-scale lunar mining far beyond current capabilities.

5. **The O'Neill-class cylinder (~5,800 Mt minimum) requires asteroid mining** in addition to lunar resources, particularly for nitrogen and water. At current launch costs (~$2,700/kg to LEO with Starship), even moving 1 Mt from Earth would cost $2.7 trillion. All mass must come from space resources.

6. **The SP-413 torus at 10.5 Mt was the most mass-efficient design** among the options studied in 1975. It achieved comparable living area to much larger cylinders at a fraction of the mass. The cylinder's structural penalty is severe.
