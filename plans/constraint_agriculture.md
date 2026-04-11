# Agriculture Area Constraint

## Summary

Food self-sufficiency requires a minimum cultivated area per person. For an
isolated colony, all calories **and protein** must be produced on-habitat.

**Model assumption: plant-dominant diet.**
The baseline figure of 200 m²/person (NASA BVAD) covers a plant-based diet
with legumes, grains, and vegetables supplying protein — no dairy, no
traditional livestock. This is the standard assumption in space habitat
literature because it is the most area-efficient closed-loop food system.

A `diet_land_multiplier` (default 1.0) can scale the requirement upward to
model animal protein additions (aquaculture, poultry, etc.) in sensitivity
analysis.

### Nutritional completeness caveat

A plant-based diet without animal products is nutritionally challenging in
practice. Key concerns relevant to a space colony:

- **Calcium / bone density** — dairy is the most efficient dietary calcium source.
  Plant sources (kale, tofu, fortified foods) are adequate but require careful
  menu planning. Calcium deficiency over generations could reduce average
  bone density and stature — as seen historically in East Asian populations
  with low dairy intake (Abelow et al. 1992).
- **Vitamin B12** — absent in plants; must be supplemented or supplied via
  fermented foods or insects.
- **Vitamin D** — requires UV exposure or supplementation; no sunlight in
  the traditional sense inside a cylinder.
- **Complete protein** — plant proteins are individually incomplete; requires
  deliberate pairing (e.g., rice + legumes) to cover all essential amino acids.

These are engineering and menu-planning problems, not fundamental physical
constraints — they do not change the area requirement modeled here. But they
are real challenges that a colony food system must solve, and they may
influence crew physical capacity and long-term health outcomes.

---

## Physics and Derivation

### Caloric requirement

An adult needs roughly 2,000–2,500 kcal/day and ~50–60 g of protein/day.
The minimum growing area per person depends on two independent factors:

1. **Farming method** — how efficiently calories are produced per m²
2. **Diet composition** — the protein source, since animal products require
   significantly more land per calorie than plant sources

### Farming method

| Method | Area per person (plant diet) | Source |
|---|---|---|
| Open-field (Earth average) | ~2,000 m²/person (0.2 ha) | FAO (2012) |
| Controlled-environment agriculture (CEA) | 200–400 m²/person | Hendrickx et al. (2006) |
| Hydroponics (single-tier) | ~200 m²/person | NASA BVAD (Hanford 2004) |
| Vertical farming (multi-tier, 5–10 tiers) | 20–100 m²/person | Despommier (2010) |

For an O'Neill colony the baseline is **single-tier hydroponics at
200 m²/person** — the NASA BVAD figure for CELSS studies. It represents
a diet of ~2,100 kcal/day with plant protein (legumes, soy, wheat).

### Diet composition and protein sources

The 200 m²/person baseline assumes **plant-based protein**. Animal products
require additional growing area because feed conversion is inefficient: it
takes several kg of plant biomass to produce 1 kg of animal protein.

| Protein source | Land multiplier vs. plant baseline | Viability in habitat |
|---|---|---|
| Plant protein (legumes, soy) | 1.0× | ✅ included in baseline |
| Insects (mealworms, crickets) | ~1.1× | ✅ viable — ~2 kg feed/kg protein |
| Aquaculture (fish, tilapia) | ~1.3–1.5× | ✅ viable — closed-loop recirculating |
| Poultry / eggs | ~3–4× | ⚠️ significant area penalty |
| Pork | ~5–7× | ⚠️ very large penalty |
| Beef | ~15–20× | ❌ not viable at habitat scale |

Sources: Poore and Nemecek (2018) for land-use ratios; Nakagaki and DeFoliart
(1991) for insect conversion; Verdegem et al. (2006) for aquaculture.

Traditional livestock (cow, pig, chicken) are impractical for space habitats
because of the compounding area costs: the animals need housing, their feed
crops need growing area, and waste processing adds further complexity. O'Neill
(1977) explicitly assumed vegetarian diets for the Island Three population.

The most credible animal-protein additions for a habitat are:
- **Aquaculture** — tilapia or carp in recirculating systems; produces high-quality
  protein with modest additional area
- **Insects** — high protein density, low feed ratio, minimal footprint
- **Cultured meat** — cellular agriculture requires negligible growing area
  (essentially zero multiplier once the technology matures)

### Constraint formula

Let:

- $A_\text{agr}$ = dedicated agriculture area (m²)
- $a_\text{min}$ = minimum area per person for a plant-based diet (m²/person)
- $m_\text{diet}$ = diet land multiplier (1.0 = plant-only, higher = more animal protein)
- $N$ = population

The feasibility condition is:

$$A_\text{agr} \geq a_\text{min} \cdot m_\text{diet} \cdot N$$

For the default O'Neill design ($N = 8{,}000$, $a_\text{min} = 200$
m²/person, $m_\text{diet} = 1.0$):

$$A_\text{required} = 200 \times 1.0 \times 8{,}000 = 1{,}600{,}000 \text{ m}^2 = 160 \text{ ha}$$

Adding aquaculture ($m_\text{diet} = 1.4$) raises the requirement to 224 ha.
Adding significant poultry ($m_\text{diet} = 3.0$) raises it to 480 ha —
tripling the module area.

### Where does agriculture fit?

O'Neill's Island Three design places agriculture in **external agricultural
modules** — separate cylinders attached near the end caps (O'Neill 1977).
This allows independent photoperiod control, elevated CO₂, and quarantine
separation from living quarters.

The **interior barrel surface** could support agriculture, but window strips
(~50% of barrel area) and residential/industrial zones limit agricultural use
to ~20–30% of barrel area. For the minimum feasible habitat ($r = 982$ m,
$L = 1{,}276$ m):

$$A_\text{barrel} = 2\pi r L \approx 7.87 \times 10^6 \text{ m}^2$$

At 25% agricultural fraction, this gives ~1.97 × 10⁶ m² — sufficient for a
plant-only diet but tight once any animal protein is added.

### Sensitivity

The two dominant levers are $a_\text{min}$ (farming technology) and
$m_\text{diet}$ (protein source). Switching from plant-only to a
poultry-inclusive diet multiplies required area by ~3×, easily exceeding
interior barrel capacity and requiring substantially larger external modules.

---

## Thresholds

| Parameter | Default | Range | Basis |
|---|---|---|---|
| $a_\text{min}$ | 200 m²/person | 20–2,000 m²/person | NASA BVAD (Hanford 2004) |
| $m_\text{diet}$ | 1.0 | 1.0–5.0 | Poore and Nemecek (2018) |

---

## Implementation Notes

- `agriculture_area_m2` is a `HabitatParameters` field (0 = not specified,
  constraint skipped).
- `min_agriculture_area_per_person_m2` and `diet_land_multiplier` are
  `HumanAssumptions` fields (technology and diet sensitivity knobs).
- The effective threshold is `min_agriculture_area_per_person_m2 * diet_land_multiplier`.
- If `population == 0` the constraint is also skipped.
- The `details` dict reports `required_area_m2`, `effective_area_per_person_m2`,
  `area_per_person_m2`, and `area_margin_m2` for the dashboard.

---

## References

- Abelow, B.J., et al. "Cross-cultural association between dietary animal
  protein and hip fracture: a hypothesis." *Calcified Tissue International*
  50.1 (1992): 14–18.
- Despommier, Dickson. *The Vertical Farm: Feeding the World in the 21st
  Century*. Thomas Dunne Books, 2010.
- FAO. *The State of the World's Land and Water Resources for Food and
  Agriculture*. Food and Agriculture Organization, 2012.
- Hanford, Anthony J. *Advanced Life Support Baseline Values and Assumptions
  Document*. NASA/CR-2004-208941, 2004.
- Hendrickx, L., et al. "Microbial ecology of the closed artificial ecosystem
  MELiSSA." *Advances in Space Research* 38.6 (2006): 1228–1235.
- Nakagaki, B.J., and G.R. DeFoliart. "Comparison of diets for mass-rearing
  Acheta domesticus." *Journal of Economic Entomology* 84.3 (1991): 891–896.
- O'Neill, Gerard K. *The High Frontier: Human Colonies in Space*. William
  Morrow, 1977.
- Poore, J., and T. Nemecek. "Reducing food's environmental impacts through
  producers and consumers." *Science* 360.6392 (2018): 987–992.
- Verdegem, M.C.J., et al. "Contribution of aquaculture to food production."
  *Aquaculture* 261.1 (2006): 67–74.
