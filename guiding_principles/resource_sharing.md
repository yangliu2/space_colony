# Resource Sharing Between Constraints

## Principle

Physical resources inside an O'Neill cylinder are finite and partitioned.
When two or more constraints claim the same surface area, mass, volume, or power budget,
the model must account for the shared claim — or results will be optimistic.

**Every time you add a new constraint, check whether it consumes a resource already
claimed (in whole or in part) by an existing constraint.**

---

## Known Shared Resources

| Resource | Constraints | Resolution |
|---|---|---|
| **End-cap area** (`endcap_area_m2`) | Energy (solar panels) + Thermal (radiators) | Thermal subtracts solar panel footprint before counting available radiator area. End caps are partitioned: panels first, radiators get the rest. |
| **Barrel area** (`barrel_area_m2`) | Thermal (windows + land strips) + Agriculture (floor area is part of the interior surface) | Currently separate: thermal works with the exterior hull; agriculture uses `agriculture_area_m2` as an independent parameter. Revisit if interior surface area is ever modelled jointly. |
| **Hull mass** | Hoop-stress (wall thickness), Spin-up energy (moment of inertia), Radiation (shielding areal density) | All three use the same structural shell. Currently each takes the design variables (`wall_thickness_m`, `shielding_areal_density_kg_m2`) as independent inputs. No double-counting of physical mass — each constraint reads the same parameter and interprets it for its own physics. |

---

## What Is NOT a Resource Conflict

**Design variables are not consumed resources.** Radius, length, pressure, wall thickness —
these are shared inputs that multiple constraints can bound simultaneously.
That is normal constraint composition, not resource contention.

**Population is not consumed.** Agriculture, energy, and thermal all use `population`
to scale their demands. Each models its own subsystem independently.

---

## Checklist: Adding a New Constraint

Before implementing, answer these questions:

1. **Does this constraint claim any surface area?**
   - Which surface: barrel, end cap, interior floor, other?
   - Is any of that area already allocated by another constraint?
   - If yes → implement a shared-area calculation (subtract the other's footprint first).

2. **Does this constraint claim power or energy?**
   - Is the power source (solar panels) already sized by another constraint?
   - If yes → either draw from the existing budget or document the independence.

3. **Does this constraint claim structural mass or hull material?**
   - Does any other constraint assume the same hull material is available?

4. **Does this constraint claim interior volume?**
   - Population and atmosphere already constrain habitable volume.

5. **Record the answer in the table above**, even if the answer is "no conflict."

---

## Anti-Patterns

- Assuming 100% of end-cap area is available for radiators — solar panels take 2–7% first.
- Assuming 100% of barrel area is available for windows — radiator strips take the rest.
- Adding a water tank constraint that assumes all interior volume not occupied by people is available, without checking agriculture (grows in interior space).

---

## Existing Clean Bills of Health (as of Phase 6)

All 16 constraints audited 2026-04-11:
- **No double-counting of design variables** (radius, length, pressure, thickness).
- **Endcap area** — resolved: thermal subtracts solar panel footprint.
- **No other physical resource conflicts found.**
