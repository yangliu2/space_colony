# parameter_dependencies.md — Dynamic parameter ranges when one depends on another

## Rule

If a constraint document states that parameter A's limit depends on parameter B,
the UI slider for A must update its range dynamically as B changes.
Never use a fixed slider max when the physics imposes a variable one.

## Known dependencies in this project

| Parameter | Depends on | Formula | Source |
|-----------|-----------|---------|--------|
| `length_m` max | `radius_m` | $L_\text{max} = 1.33 \cdot r^{5/4}$ | `plans/constraint_cylinder_length.md` |

## How to implement

- Compute the dynamic max in the slider component from the current param value
- Add 10–20% headroom above the physical limit so the green bar end is visible
- Round to a human-readable step (e.g. nearest 500 m)
- Update the API sweep upper bound to match the same formula

## How to discover new dependencies

When writing or reviewing a constraint plan, ask:
> "Does the limit on this parameter change as another parameter changes?"

If yes, update:
1. The slider component (dynamic max)
2. The API feasible_ranges sweep (same formula)
3. This document (add a row to the table above)

## Anti-patterns

- `max: 10000` hardcoded in slider when the true max is `f(radius)`
- API sweep stopping before the feasible boundary for large-radius cases
- Slider range that never updates as the user moves another slider
