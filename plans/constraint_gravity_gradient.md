# Gravity Gradient Constraint: Why Your Head Is Lighter Than Your Feet

## 1. The Problem

In a rotating habitat, artificial gravity comes from $a = \omega^2 r$. The "$r$" is the distance from the rotation axis. Your feet stand on the floor at radius $r$, but your head is at radius $r - h$ (where $h$ is your height). Since gravity is proportional to $r$, **your head experiences less gravity than your feet**.

On Earth, this gradient exists too — gravity decreases with altitude — but it's negligible over human height ($\sim 0.00003\%$ per meter). In a small rotating habitat, it can be enormous.

---

## 2. The Physics

### Gravity at your feet (floor level):

$$
g_{\text{feet}} = \omega^2 r
$$

### Gravity at your head:

$$
g_{\text{head}} = \omega^2 (r - h)
$$

### The gradient (difference as a fraction of foot-level gravity):

$$
\frac{\Delta g}{g} = \frac{g_{\text{feet}} - g_{\text{head}}}{g_{\text{feet}}} = \frac{\omega^2 r - \omega^2(r - h)}{\omega^2 r} = \frac{h}{r}
$$

This is a beautifully simple result: **the gradient depends only on the ratio of your height to the radius.** It doesn't depend on the rotation rate, the gravity level, or anything else.

$$
\boxed{\text{Gradient} = \frac{h}{r}}
$$

---

## 3. What This Feels Like

At gradient = 0 (Earth, or $r \to \infty$): your head and feet weigh the same relative to each other. Normal.

At gradient = 1% ($r = 180$ m for $h = 1.8$ m): your head experiences 1% less gravity than your feet. Imperceptible.

At gradient = 5% ($r = 36$ m): your head is noticeably lighter. Reaching up feels slightly different from reaching down. Probably tolerable.

At gradient = 20% ($r = 9$ m): your head is dramatically lighter than your feet. Blood pools differently, balance is affected. Inner ear gives conflicting signals. Extremely disorienting.

At gradient = 100% ($r = h = 1.8$ m): your head is at the rotation axis. Zero gravity at your head, full gravity at your feet. Catastrophically disorienting — you'd fall over immediately.

---

## 4. The Constraint

$$
\frac{h}{r} \leq \text{gradient}_{\max}
$$

Which gives a minimum radius:

$$
r_{\min} = \frac{h}{\text{gradient}_{\max}}
$$

### What $\text{gradient}_{\max}$ Should Be

Historical recommendations vary widely:

| Source | Year | Max Gradient | Min Radius (h=1.8m) |
|--------|------|-------------|----------------------|
| Payne | 1960 | 15% | 12 m |
| Gilruth (NASA) | 1968 | 15% (over 6 ft) | 12 m |
| Stone | 1970 | 50% (over 2 m) | 4 m |
| Cramer | 1983 | ~6% (0.01g/ft at 1g) | 30 m |
| Our model (conservative) | — | 1% | 180 m |

The historical values (15%) are remarkably generous — they allow radii as small as 12 meters. These were acceptable for short-duration space stations, not permanent colonies.

For long-term habitation, a 1% gradient is a conservative engineering choice. At 1%, the difference between head and foot gravity is:

$$
\Delta g = 0.01 \times 9.807 = 0.098 \; \text{m/s}^2 \approx 0.01g
$$

This is below human perception threshold and wouldn't affect balance, blood circulation, or any daily activity.

---

## 5. Why Gradient Matters Beyond Comfort

### Blood pressure regulation
Your cardiovascular system uses baroreceptors to regulate blood pressure between your head and feet. A large gravity gradient means the pressure difference changes depending on where you are in the habitat. Your body would need to constantly readjust, potentially causing orthostatic intolerance (dizziness when standing up).

### Inner ear confusion
The vestibular system in your ear uses tiny calcium crystals (otoliths) to sense gravity direction and magnitude. If the gravity magnitude changes significantly between your ear level and your feet, you get conflicting spatial information.

### Locomotion
Walking in a steep gravity gradient means your center of mass experiences different forces at different heights during each step. Running and jumping would feel particularly strange — you'd "float" slightly at the top of each stride.

### Activities at different heights
In a multi-story building, each floor has noticeably different gravity. Climbing stairs means getting lighter. A ball thrown upward curves differently than one thrown downward.

---

## 6. Reference Table

| Radius (m) | Gradient (h=1.8m) | g at head (if 1g at feet) | What it feels like |
|------------|-------------------|---------------------------|-------------------|
| 10         | 18.0%             | 0.82g                     | Head noticeably light, balance impaired |
| 50         | 3.6%              | 0.964g                    | Perceptible if looking for it |
| 100        | 1.8%              | 0.982g                    | Barely perceptible |
| 180        | 1.0%              | 0.990g                    | Imperceptible — our model's threshold |
| 500        | 0.36%             | 0.9964g                   | Negligible |
| 3,200      | 0.056%            | 0.9994g                   | Essentially zero (O'Neill) |

---

## 7. Interaction with Other Constraints

The gradient constraint ($r \geq 180$ m) is less restrictive than the vestibular constraint ($r \geq 224$ m at 2 RPM) and much less restrictive than the cross-coupling constraint ($r \geq 982$ m at 6 deg/s²). **In the full model, gravity gradient is never the binding constraint** — it's always satisfied before the others become feasible.

It would only become binding if we tightened the threshold below ~0.8%, or if we relaxed the RPM and cross-coupling constraints significantly.

---

## 8. The One-Liner

> The gravity gradient $h/r$ is beautifully simple and purely geometric — it depends only on how tall you are relative to the cylinder. At any radius large enough to satisfy vestibular and cross-coupling constraints, the gradient is already negligible.

---

## References

- Cramer, D. Bryant. "Physiological Considerations of Artificial Gravity." *Applications of Tethers in Space*, vol. 1, NASA CP-2364, 1983, pp. 3.95–3.107.

- Gilruth, Robert R. "Manned Space Stations — Gateway to Our Future in Space." *Manned Laboratories in Space*, edited by S. Fred Singer, Springer, 1969, pp. 1–10.

- Hall, Theodore W. "Artificial Gravity and the Architecture of Orbital Habitats." *Journal of the British Interplanetary Society*, vol. 52, 1999, pp. 455–465.

- Payne, Peter R. "The Dynamics of Human Restraint Systems." *Impact Acceleration Stress*, National Academy of Sciences, 1962, pp. 195–257.

- Stone, Ralph W. "An Overview of Artificial Gravity." *Fifth Symposium on the Role of the Vestibular Organs in Space Exploration*, NASA SP-314, 1970, pp. 23–33.
