# Space Colony — Constraint Study

A physics-based feasibility study asking: **what does an O'Neill cylinder actually need to work?**

This started as a curiosity after reading science fiction — wondering what space habitats in the near future might realistically look like. Rather than doing theoretical physics, the approach here is practical: model the constraints, find the limits, and see what the math actually says.

## The Surprising Finding

O'Neill's original *Island Three* design imagined cylinders **32 km long and 6.4 km in diameter**.

This study finds that **material stress makes long cylinders structurally unsafe**. The length is constrained by radius — wider cylinders can be longer, but the ratio is far more limiting than O'Neill assumed. The feasible geometry is much stubbier than the classic vision.

## Feasible Design at 1g

| Parameter | Lower bound | Upper bound |
|-----------|------------|------------|
| Radius | **982 m** | **9,177 m** |
| Binding constraint | Cross-coupling | Rim speed (300 m/s) |
| O'Neill reference (3,200 m) | ✅ comfortably inside the band | |

## How to Read This

The documentation follows the order of discovery — from first principles to surprising results:

1. **[How does it work?](plans/intuition_artificial_gravity.md)** — the physics of spin gravity
2. **[Can humans live there?](plans/constraint_vestibular.md)** — comfort and physiology limits
3. **[Will the structure hold?](plans/constraint_rim_speed.md)** — material and geometry limits, including the cylinder length surprise
4. **[Findings](conclusions/001_human_comfort_boundaries.md)** — what the model concludes

[→ Interactive demo](https://spinhabitat.com){ .md-button .md-button--primary }
