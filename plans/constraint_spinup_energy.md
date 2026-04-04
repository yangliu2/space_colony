# Constraint: Spin-Up Energy

## Overview

A rotating habitat must be spun from rest to its operating angular
velocity $\omega$. The rotational kinetic energy $E = \frac{1}{2}I\omega^2$
must be supplied by external power systems (solar arrays, nuclear reactors,
or ion thrusters). This constraint checks that the spin-up can be completed
within an acceptable time given available power.

## Physics

### Rotational Kinetic Energy

$$E_{\text{rot}} = \frac{1}{2} I_z \, \omega^2$$

where $I_z$ is the moment of inertia about the spin axis (cylinder
longitudinal axis).

### Moment of Inertia Components

The total rotating mass has four components, each with a different radial
distribution:

**1. Hull barrel** — thin cylindrical shell at radius $r$:

$$m_{\text{hull}} = \rho_{\text{hull}} \cdot 2\pi r L \cdot t$$

$$I_{\text{hull}} = m_{\text{hull}} \cdot r^2$$

**2. Endcaps** — two flat disks of thickness $t$:

$$m_{\text{caps}} = \rho_{\text{hull}} \cdot 2\pi r^2 \cdot t$$

$$I_{\text{caps}} = \frac{1}{2} m_{\text{caps}} \cdot r^2$$

(solid disk about its axis)

**3. Radiation shielding** — distributed on the outer shell surface:

$$m_{\text{shield}} = \sigma_{\text{shield}} \cdot A_{\text{total}}$$

where $A_{\text{total}} = 2\pi r L + 2\pi r^2$ (barrel + endcaps) and
$\sigma_{\text{shield}}$ is the areal density (kg/m²). Since shielding
sits at or near radius $r$:

$$I_{\text{shield,barrel}} = \sigma_{\text{shield}} \cdot 2\pi r L \cdot r^2$$

$$I_{\text{shield,caps}} = \frac{1}{2} \cdot \sigma_{\text{shield}} \cdot 2\pi r^2 \cdot r^2$$

**4. Atmosphere** — fills the interior as a uniform-density gas:

$$m_{\text{atm}} = \rho_{\text{air}} \cdot \pi r^2 L$$

where $\rho_{\text{air}} = P / (R_{\text{specific}} \cdot T)$ with
$R_{\text{specific}} = 287$ J/(kg·K) for air and $T \approx 293$ K
(20°C):

$$I_{\text{atm}} = \frac{1}{2} m_{\text{atm}} \cdot r^2$$

(solid cylinder of gas about its axis)

### Total Moment of Inertia

$$I_z = (m_{\text{hull}} + m_{\text{shield,barrel}}) \cdot r^2
  + \frac{1}{2}(m_{\text{caps}} + m_{\text{shield,caps}} + m_{\text{atm}}) \cdot r^2$$

### Simplification for 1g

At constant gravity $g$, $\omega = \sqrt{g/r}$, so:

$$E = \frac{1}{2} I_z \cdot \frac{g}{r}$$

For the dominant barrel terms ($I \approx m r^2$):

$$E \approx \frac{1}{2} m \cdot g \cdot r$$

Energy scales **linearly** with radius at constant gravity — a key
insight for comparing habitat sizes.

### Spin-Up Time

Assuming constant applied power $P_{\text{avail}}$:

$$t_{\text{spinup}} = \frac{E_{\text{rot}}}{P_{\text{avail}}}$$

This is an idealized lower bound — real spin-up involves variable torque,
structural settling, and atmospheric drag losses. A practical estimate
would add 20–50% overhead, but we use the ideal value for the constraint.

## Reference Numbers

### Reference design ($r = 982$ m, $L = 1{,}276$ m, steel $t = 0.2$ m)

| Component | Mass (Mt) | $I_z$ (kg·m²) |
|-----------|-----------|----------------|
| Hull barrel | 12.4 | $1.20 \times 10^{16}$ |
| Endcaps | 9.6 | $4.63 \times 10^{15}$ |
| Shielding (barrel) | 35.4 | $3.42 \times 10^{16}$ |
| Shielding (caps) | 27.2 | $1.31 \times 10^{16}$ |
| Atmosphere | 3.6 | $1.74 \times 10^{15}$ |
| **Total** | **88.2** | **$5.59 \times 10^{16}$** |

At 1g: $\omega = 0.0999$ rad/s, $E = 2.79 \times 10^{14}$ J = **279 TJ**

| Available Power | Spin-Up Time |
|-----------------|-------------|
| 1 GW | 3.2 days |
| 10 GW | 7.7 hours |
| 100 GW | 46 minutes |

### O'Neill cylinder ($r = 3{,}200$ m, $L = 32{,}000$ m)

Total mass ~6,000 Mt → $E \approx 9.4 \times 10^{16}$ J = **94 PJ**

| Available Power | Spin-Up Time |
|-----------------|-------------|
| 1 GW | 3.0 years |
| 10 GW | 109 days |
| 100 GW | 11 days |

## Constraint Definition

**Pass condition:** Spin-up time ≤ maximum allowed spin-up time.

$$\frac{E_{\text{rot}}}{P_{\text{avail}}} \leq t_{\max}$$

### Default Assumptions

| Parameter | Default | Rationale |
|-----------|---------|-----------|
| $P_{\text{avail}}$ | 10 GW | ~37 km² solar array at L5 (20% efficiency) |
| $t_{\max}$ | 1.0 year | Engineering patience for colony-scale construction |

The constraint is **soft** — spin-up time is always finite and adjustable
by adding more power. But it provides useful engineering feedback: a design
requiring 10 years of spin-up with available power is impractical even if
structurally sound.

## Output Details

The constraint reports:
- `total_rotating_mass_kg`: sum of all mass components
- `moment_of_inertia_kg_m2`: total $I_z$
- `kinetic_energy_j`: rotational KE
- `spinup_time_s`: time at available power
- `spinup_time_days`: same, in days
- `power_w`: available power used

## References

- O'Neill, Gerard K. "The Colonization of Space." *Physics Today*,
  vol. 27, no. 9, 1974, pp. 32–40.
- NASA. *Space Settlements: A Design Study* (SP-413). 1977, ch. 5.
- Johnson, Richard D., and Charles Holbrow, eds. *Space Settlements:
  A Design Study*. NASA SP-413, 1977.
