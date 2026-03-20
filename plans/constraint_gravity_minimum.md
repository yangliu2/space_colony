# Minimum Gravity for Long-Term Human Survival: What We Know and Don't Know

## 1. The Central Question

What is the minimum gravity level that allows humans to live, work, and reproduce indefinitely without progressive physiological deterioration?

**The honest answer: we don't know.** No human has ever lived for more than brief minutes in any gravity between 0g and 1g. All partial-gravity data comes from animal studies, short-duration centrifuge experiments, and extrapolation from microgravity exposure on the ISS.

---

## 2. What Happens at 0g (Microgravity)

Decades of ISS experience have thoroughly documented zero-gravity effects:

| System | Effect | Rate | Reversible? |
|--------|--------|------|-------------|
| Bone | Density loss (especially weight-bearing bones) | 1–2% per month | Partially; takes years to recover |
| Muscle | Atrophy (especially legs, back) | Up to 30% over 6 months | Mostly, with rehabilitation |
| Cardiovascular | Heart remodeling, fluid shift to head, reduced blood volume | Weeks | Mostly |
| Vision | Intracranial pressure → optic disc swelling (SANS) | Months | Often permanent |
| Immune | Suppressed immune function, reactivation of latent viruses | Weeks to months | Unknown |
| Balance | Vestibular deconditioning, difficulty walking post-flight | Immediate upon return | Days to weeks |

**Key point:** Exercise (2.5 hours/day, 6 days/week on ISS) slows but does not prevent all degradation. After 6–12 months, astronauts return with measurable bone loss, vision changes, and cardiovascular deconditioning despite intensive countermeasures.

---

## 3. What Happens at Partial Gravity: The Data We Have

### 3.1 Lunar gravity (0.16g) — Insufficient

Apollo astronauts spent only hours to days on the Moon. No long-term health data exists. However:

- NASA centrifuge studies concluded: **"Moon gravity (0.16g) is not effective for preventing cardiovascular deconditioning following spaceflight"** (Clément and Bukley 2015)
- Sensorimotor perception thresholds lie between 0.16g and 0.38g — at lunar gravity, your vestibular system may not reliably detect "which way is down"
- Bone loading at 0.16g is approximately 1/6 of Earth, well below the mechanical stimulus threshold for bone maintenance

**Assessment: 0.16g is almost certainly insufficient for long-term health.**

### 3.2 Martian gravity (0.38g) — Unknown, possibly insufficient

Mars is the most studied partial-gravity case, but all data is indirect:

- **Bone:** Mechanical loading at 0.38g is roughly 38% of Earth. The bone remodeling threshold (the minimum load needed to maintain bone density) is estimated at 0.2–0.5g depending on the bone and the study. Mars may be below this for some weight-bearing bones.
- **Muscle:** 0.38g provides meaningful resistance for daily activities but may be insufficient for maintaining Earth-level muscle mass
- **Cardiovascular:** Hydrostatic pressure gradients at 0.38g are about 38% of Earth — enough to maintain head-to-foot pressure differences but with reduced cardiovascular work
- **Development:** No data exists for fetal development, childhood growth, or puberty at 0.38g

From the issues file in this project: *"Moon have gravity of 0.166g and Mars have gravity 0.38g... Lower gravity result in multiple problems for humans evolved on earth, including muscle atrophy, bone density loss, heart and blood vessel problem, and most importantly reproductive and developmental concerns."*

**Assessment: 0.38g might sustain healthy adults for years but is likely inadequate for reproduction and child development. The data is too sparse to be confident.**

### 3.3 NASA ISS centrifuge rodent studies — In progress

NASA is conducting the most relevant experiment: mice on the ISS exposed to 0.25g, 0.50g, 0.75g, and 1.0g via onboard centrifuge (launched March 2023). This will provide the first dose-response data for bone, muscle, and neuromotor function at partial gravity levels.

**Preliminary findings** (from conference abstracts, not yet peer-reviewed):
- 1g centrifuge mice showed bone and gait parameters similar to ground controls
- 0.67g mice showed **lower vertebral strength** than ground controls
- Artificial gravity effects were "gravity-dose dependent" — more gravity = better outcomes
- Full results for the 0.25g and 0.50g groups are pending

**Assessment: The most important experiment for answering this question is literally in progress. Full results expected 2025–2026.**

### 3.4 Human centrifuge studies on Earth

Short-radius centrifuge experiments on Earth can simulate partial gravity, but:
- Subjects only experience it for minutes to hours
- Earth's 1g gravity is always present (the centrifuge adds to it, doesn't replace it)
- No long-term physiological adaptation data

Key finding: **Humans can perceive gravity between 0.22g and 0.50g** depending on head position (Clément and Bukley 2015). Below 0.22g, the vestibular system may not register gravity at all.

---

## 4. Estimated Thresholds by System

Based on available research, here are our best estimates for minimum gravity by physiological system:

| System | Estimated Minimum | Confidence | Basis |
|--------|-------------------|------------|-------|
| Bone density maintenance | 0.3–0.5g | Low | Bone remodeling threshold extrapolations |
| Muscle maintenance | 0.2–0.4g | Low | Bed rest studies, animal models |
| Cardiovascular function | 0.3–0.5g | Low | Centrifuge studies, fluid dynamics models |
| Vestibular orientation | 0.2–0.5g | Medium | Parabolic flight perception studies |
| Immune function | Unknown | Very low | No partial-gravity data |
| Vision (SANS prevention) | Unknown | Very low | Fluid shift models suggest > 0.3g |
| Fetal development | Unknown | Essentially none | No animal data at partial gravity |
| Childhood bone growth | Unknown | Essentially none | No data whatsoever |
| Reproductive function | Unknown | Essentially none | Limited rodent data |

### The reproductive and developmental unknowns are the most critical

Adults can exercise, take medication, and use countermeasures. A developing fetus cannot. If bone formation, organ development, or neural wiring requires gravity signals above 0.38g, then Mars-level gravity is fundamentally incompatible with human reproduction — not as a matter of comfort, but of biology.

**This is why the issues file correctly identifies developmental concerns as "most importantly."**

---

## 5. What the Literature Converges On

Despite the enormous uncertainties, a rough consensus emerges:

### < 0.2g: Almost certainly insufficient
The vestibular system may not reliably detect gravity. Bone loading is far below the remodeling threshold. Cardiovascular adaptation is minimal.

### 0.2–0.4g: Possibly sufficient for healthy adults, probably insufficient for development
Mars gravity (0.38g) falls here. Adults might maintain function with exercise. Reproduction and child development are unknown and possibly at risk.

### 0.4–0.6g: Probably sufficient for most physiological systems
Bone loading reaches significant fractions of Earth normal. Cardiovascular work is meaningful. Vestibular function is reliable. This is where partial gravity likely "works" for adults.

### 0.5–0.7g: Likely sufficient for development (speculative)
No direct evidence, but mechanical loading, fluid dynamics, and vestibular signals are all within the range where Earth-evolved systems can plausibly function normally.

### > 0.8g: Almost certainly sufficient for everything
At 80%+ of Earth gravity, all physiological systems experience near-normal loading. The remaining 20% deficit is comparable to the variation humans experience at different altitudes and latitudes on Earth.

---

## 6. Our Model's Approach

Given the uncertainty, our model uses:
- **min_gravity_g = 0.3g**: aggressive lower bound, assumes healthy adult crew
- **max_gravity_g = 1.0g**: no reason to exceed Earth normal

For a colony with families and children, the responsible engineering choice is probably:
- **min_gravity_g = 0.5g**: conservative lower bound for development
- Or better: **target 1.0g and don't take the risk**

### Why targeting 1g is the safest engineering decision

As the issues file noted: *"To solve all those problem separate is going to be close to impossible. So creating close to 1g gravity is the most likely solution."*

This is sound engineering reasoning. The cost of being wrong about partial gravity is:
- Irreversible developmental damage to children
- Bone density loss requiring medical intervention
- Cardiovascular deconditioning in the elderly
- Unknown reproductive failures

The cost of being conservative (building for 1g when 0.5g would suffice) is:
- A larger radius (more material, more cost)

Given that the radius is already constrained to > 982 m by cross-coupling, and 1g at 982 m is achievable, **there is no compelling reason to target partial gravity for a permanent habitat.**

---

## 7. Open Questions for Future Research

1. **What is the bone remodeling threshold in actual partial gravity?** (NASA ISS rodent experiment will help)
2. **Can mammals reproduce and develop normally at 0.38g?** (No experiment planned)
3. **Is there a gravity threshold below which SANS (vision damage) cannot be prevented?**
4. **How does partial gravity interact with radiation exposure for cancer risk?**
5. **Do children need full 1g for normal vestibular and motor development?**

---

## 8. The One-Liner

> We know 0g is deadly and 1g is fine. Everything in between is a guess. For a permanent colony with children, the only responsible choice is to target 1g until we have data proving otherwise.

---

## References

- Clément, Gilles, and Angelia P. Bukley. "Artificial Gravity as a Countermeasure for Mitigating Physiological Deconditioning during Long-Duration Space Missions." *Frontiers in Systems Neuroscience*, vol. 9, 2015. *PMC*, https://pmc.ncbi.nlm.nih.gov/articles/PMC4470275/.

- Hall, Theodore W. "Artificial Gravity Design Parameters." *SpinCalc*, 2006, http://www.artificial-gravity.com/Dissertation/2_2.htm.

- Stavnichuk, Mariya, et al. "The Effects of Microgravity on Bone Structure and Function." *npj Microgravity*, vol. 8, no. 45, 2022. *Nature*, https://www.nature.com/articles/s41526-022-00194-8.

- Sture, Ola, et al. "Studying Effects of Partial Gravity on Musculoskeletal Systems of Mice — NASA ISS Mission." *Micro Photonics*, 2023, https://www.microphotonics.com/studying-effects-partial-gravity-musculoskeletal-systems-mice-nasa-iss-mission/.

- Terry, Hadley. "How Much Artificial Gravity Do We Really Need to Stay Healthy in Space?" *H. Terry*, 2023, https://hterry.com/science/how-much-artificial-gravity-do-we-really-need-to-stay-healthy-in-space/.

- Waldie, James M., et al. "The Partial Gravity of the Moon and Mars Appears Insufficient to Prevent Cardiovascular Deconditioning." *International Conference on Environmental Systems*, ICES-2021-142, NASA, 2021. *NTRS*, https://ntrs.nasa.gov/api/citations/20210019591/downloads/ICES-2021-142.pdf.

- Wikipedia contributors. "Effect of Spaceflight on the Human Body." *Wikipedia*, Wikimedia Foundation, https://en.wikipedia.org/wiki/Effect_of_spaceflight_on_the_human_body.

- NASA. "Astronaut Physiological Deconditioning Report." NASA SP-20250000273, Jan. 2025, https://nasa.gov/wp-content/uploads/2025/02/sp-20250000273.pdf.
