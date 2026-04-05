# model_3d_sync.md — Keep 3D model in sync with constraint model

## Rule

The 3D visualization must reflect the same physical assumptions as the constraint model.
When a constraint changes the geometry or parameters of the habitat, the 3D model must
be updated to match.

## What must stay in sync

| Constraint model | 3D model |
|-----------------|----------|
| `counter_rotating_pair = True` | Two counter-rotating cylinders shown |
| Default `radius_m` | Scene scale calibrated to that radius |
| Default `length_m` | Cylinder length in the scene |
| Mirror count / angle | Three external mirrors at 45° |
| Strip layout (3 land, 3 window) | Six strips at 60° each |
| End cap geometry | Hemispherical caps shown |
| Agriculture pod placement | Pods outside cylinder end, not penetrating hull |

## Slider ranges must cover the feasible region

Slider `max` values must be set beyond the green bar endpoint, not at it.
The user needs to see where feasibility ends — not have the slider stop at the boundary.

- `length_m`: slider max > bending resonance limit for the default radius
- `wall_thickness_m`: slider max > upper feasible bound from hoop stress sweep
- `internal_pressure_kpa`: slider max > upper feasible bound from atmosphere sweep

The API `feasible_ranges` sweep bounds must match slider bounds exactly.

## When a new constraint is added

1. Check whether the constraint affects any rendered geometry
2. If yes: update `CylinderScene.tsx` and `sceneGeometry.ts` to reflect it
3. If no: no 3D change needed, but document why in the constraint plan

## Anti-patterns

- Slider range stopping exactly at the feasible boundary (green bar cut off)
- 3D model showing a single cylinder when `counter_rotating_pair = True`
- Default length in the demo exceeding the structural limit for the default radius
