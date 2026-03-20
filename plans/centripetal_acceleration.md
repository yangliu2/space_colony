# Deriving Centripetal Acceleration & Artificial Gravity in an O'Neill Cylinder

## 1. Starting Point: Uniform Circular Motion

When an object moves in a circle at constant speed, it continuously changes direction. That change in direction **is** acceleration — centripetal acceleration, directed radially inward.

---

## 2. The Derivation

### 2.1 Angular Velocity

An object on a circular path of radius $r$ with tangential speed $v$ has angular velocity:

$$
\omega = \frac{v}{r}
$$

Rearranging:

$$
v = \omega \cdot r
$$

| Symbol    | Meaning                          | Unit      |
|-----------|----------------------------------|-----------|
| $\omega$  | Angular velocity                 | rad/s     |
| $v$       | Tangential (linear) speed        | m/s       |
| $r$       | Radius of circular path          | m         |

### 2.2 Centripetal Acceleration (in terms of $v$)

From kinematics of circular motion:

$$
a_c = \frac{v^2}{r}
$$

This is the magnitude of acceleration required to keep an object on a curved path. Direction is **radially inward**.

### 2.3 Substitution: $v = \omega r$

Replace $v$:

$$
a_c = \frac{v^2}{r} = \frac{(\omega \cdot r)^2}{r} = \frac{\omega^2 \cdot r^2}{r}
$$

$$
\boxed{a_c = \omega^2 \cdot r}
$$

| Symbol   | Meaning                                          | Unit        |
|----------|--------------------------------------------------|-------------|
| $a_c$    | Centripetal acceleration (felt as "gravity")      | m/s²        |
| $\omega$ | Angular velocity of the cylinder                  | rad/s       |
| $r$      | Radius from the axis of rotation                  | m           |

---

## 3. Connecting to $F = ma$

On the inner surface of a rotating habitat, the hull pushes you inward (normal force). In the rotating reference frame, you experience a fictitious outward "centrifugal force":

$$
F = m \cdot a_c = m \cdot \omega^2 \cdot r
$$

This is Newton's second law applied directly. The floor exerts a real contact force of $m \omega^2 r$ on you, and you perceive it as **weight**.

---

## 4. Application: The O'Neill Cylinder

An O'Neill cylinder is a proposed space habitat — a large rotating cylinder where inhabitants live on the **inner surface**. The structure's own gravitational pull is negligible. Rotation alone produces the sensation of gravity.

### 4.1 Condition for 1g

Set $a_c$ equal to Earth's surface gravity $g$:

$$
\omega^2 \cdot r = g = 9.81 \; \text{m/s}^2
$$

Solving for the required spin rate at a given radius:

$$
\omega = \sqrt{\frac{g}{r}}
$$

Solving for the required radius at a given spin rate:

$$
r = \frac{g}{\omega^2}
$$

The rotation period $T$ (time for one full revolution):

$$
T = \frac{2\pi}{\omega}
$$

### 4.2 O'Neill's Design: $r = 3{,}200$ m

$$
\omega = \sqrt{\frac{9.81}{3200}} = \sqrt{0.003066} \approx 0.0554 \; \text{rad/s}
$$

$$
T = \frac{2\pi}{0.0554} \approx 113.4 \; \text{s} \approx 1.9 \; \text{min}
$$

> One full rotation roughly every **two minutes** — slow enough that Coriolis effects are manageable.

### 4.3 Reference Table

| $r$ (m) | $\omega$ (rad/s) | RPM   | $T$ (s) | Notes                       |
|---------|-------------------|-------|----------|-----------------------------|
| 100     | 0.313             | 2.99  | 20.1     | Too fast, severe Coriolis   |
| 500     | 0.140             | 1.34  | 44.9     | Near human comfort threshold|
| 1,000   | 0.099             | 0.95  | 63.5     | Reasonable                  |
| 3,200   | 0.055             | 0.53  | 113.4    | O'Neill's original design   |
| 5,000   | 0.044             | 0.42  | 142.3    | Very comfortable            |

---

## 5. Why Radius Can't Be Too Small

At small radii you must spin faster to reach 1g. This causes real problems:

### Coriolis Effect

In a rotating frame, any motion not aligned with the rotation axis produces a Coriolis acceleration:

$$
\vec{a}_{\text{Cor}} = -2\,\vec{\omega} \times \vec{v}_{\text{rel}}
$$

Walk in the spin direction → you feel heavier. Walk against it → you feel lighter. At high $\omega$, this is nauseating.

### Head-to-Foot Gravity Gradient

If the cylinder radius is $r$ and you stand at height $h$:

$$
\frac{\Delta g}{g} = \frac{h}{r}
$$

| $r$ (m) | $h = 2$ m | Gradient |
|---------|-----------|----------|
| 100     | 2         | 2.0%     |
| 500     | 2         | 0.4%     |
| 3,200   | 2         | 0.06%   |

At $r = 3{,}200$ m, the gradient is negligible. At $r = 100$ m, your head is noticeably lighter than your feet.

### Accepted Minimums

- **~500 m** radius at **~1.3 RPM** is generally considered the lower bound for human comfort.
- O'Neill's 3,200 m is conservative by design.

---

## 6. Summary

The entire derivation is three steps:

$$
F = ma \quad \longrightarrow \quad v = \omega r \quad \longrightarrow \quad \boxed{a = \omega^2 r}
$$

Set $a = 9.81 \; \text{m/s}^2$, choose your radius, and you have artificial gravity. The O'Neill cylinder at $r \approx 3.2$ km spins once every ~2 minutes to produce a full 1g on the inner surface.
