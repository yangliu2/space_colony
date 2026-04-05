# formula_sync.md — Keep every copy of a physics formula in sync

## Rule

A physics formula that appears in more than one file is a maintenance hazard.
When the formula changes in the constraint model, **every other copy must be
updated in the same commit** — no exceptions.

## Known formula copies that must stay in sync

| Formula | Canonical source | All copies |
|---------|-----------------|-----------|
| $L_\text{max} = 75.22 \cdot r^{3/4}$ | `constraints/cylinder_length.py` | `core/parameters.py` (coefficient field), `api/main.py` (sweep upper bound), `ParameterSliders.tsx` (`C_BENDING`), `StatsPanel.tsx` (`maxLength`), `sceneGeometry.ts` (`C_BENDING_SCENE` — controls 3D display cap) |

## How to find all copies before changing a formula

1. Search the entire repo for the coefficient: `grep -r "1.33\|75.22\|2.74"` (adapt as needed).
2. Search for the exponent pattern: `grep -r "1\.25\|0\.75\|5.*4\|3.*4"` in JS/TS/Python files.
3. Search for the variable name: `grep -r "maxLength\|C_BENDING\|max_length_coefficient"`.
4. Check the docs site source (`docs/`, `plans/`, `conclusions/`) for any table or formula that
   will now show wrong numbers.

## Checklist when a formula changes

- [ ] Constraint class (`constraints/<name>.py`)
- [ ] Parameters defaults (`core/parameters.py`)
- [ ] API sweep bounds (`api/main.py`)
- [ ] Slider component (`ParameterSliders.tsx`) — slider max
- [ ] Stats panel (`StatsPanel.tsx`) — any displayed derived stat
- [ ] Scene geometry (`sceneGeometry.ts`) — 3D display cap (`maxPhysicalLength`)
- [ ] Plan document (`plans/constraint_<name>.md`) — derivation and tables
- [ ] Guiding principle cross-reference (`parameter_dependencies.md`)
- [ ] Tests — update expected values and scaling assertions
- [ ] Docs site (conclusions, feasible design space) — check displayed numbers

## Anti-patterns

- Updating the constraint class but leaving the stats panel on the old formula
- Updating the slider but leaving the API sweep on the old coefficient
- Copy-pasting a coefficient as a raw number (`2.74`, `1.33`) without a comment
  saying where it comes from — makes grep harder and breakage more likely
- Changing the formula in two places but forgetting the third because it used
  a slightly different variable name (`maxLength` vs `bendingMax`)
