# Space Colony Project

## File Reading
Since you cannot read files more than 10,000 tokens, don't create any file 
more than 10,000 tokens. 

## Environment

- **Python:** 3.14.2 (via homebrew)
- **Package manager:** uv (binary at `/Users/fangfanglai/anaconda3/envs/space/bin/uv`)
- **Virtualenv:** `models/habitat_constraints/.venv` (managed by uv)
- `conda activate space` is required to put `uv` on PATH

## Habitat Constraints Package

Located at `models/habitat_constraints/`. Uses uv for dependency management.

```bash
conda activate space
cd models/habitat_constraints

# Install dependencies
uv sync --all-extras

# Run tests
uv run pytest

# Formatting / linting / type checking
uv run black --check src/ tests/
uv run flake8 src/ tests/
uv run mypy src/
```

### Code Style
- black & flake8: line-length=89
- mypy: strict mode
- pytest: with coverage

### Document Style (`plans/`)
- **All equations and formulas** use LaTeX (`$$` blocks for display, `$...$` for inline)
  - Never use code blocks (`` ``` ``) for formulas
  - Variables in prose must also be LaTeX: `$r$`, `$\omega$`, `$\sigma_y$`
- Source citations use **MLA format**
- Section is named **"References"** (not "Sources")
- Inline citations use **(Author Year)** format, e.g. `(Clément and Bukley 2015)`
  - Two authors: `(Lackner and DiZio 1998)`
  - Three+ authors: `(Hallgren et al. 2025)`
  - Never use bare PMC IDs, DOIs, or URLs as inline citations
- Every inline citation must have a corresponding full entry in the References section
- References section entries follow MLA 9th edition:
  - `Author(s). "Title." *Journal*, vol. X, no. Y, Year, pp. Z. *Database*, URL.`

## Literature Review

All constraint parameter values and formulas must be validated against
published research. Two review documents track this:

- `plans/literature_review_structural.md` — hoop stress, cylinder length,
  material limits, safety factors, half-atmosphere
- `plans/literature_review_human_factors.md` — rotation comfort (RPM,
  cross-coupling, Coriolis, gravity gradient), minimum gravity, radiation,
  atmosphere, minimum viable population

**Key findings from review:**
- Hoop stress formula and numerical results: **confirmed** by McKendree,
  NASA SP-413, and community analyses
- Cylinder length: our $L_{\max} = C \cdot r^{5/4}$ is **original work**;
  published literature uses rotational stability ($L < 1.3r$) as the
  primary length constraint
- Rotation 2 RPM: **confirmed** as conservative standard (Gilruth 1969,
  SP-413); 4 RPM defensible for adapted residents (Globus and Hall 2017)
- Cross-coupling 6 deg/s²: **reasonable interpolation**, not from a single
  source (sits between illusion onset at 3.4 and nausea at 34.4)
- Gravity gradient 1%: **6–15× more conservative** than published sources
  (never binding in practice)
- Min gravity 0.3g: matches Gilruth floor but **likely too low for
  families** based on recent NASA research
- Radiation 4500 kg/m²: reasonable for regolith but **material-dependent**;
  hydrogen-rich materials are more effective

When adding new constraints or modifying existing ones, update the relevant
literature review document with validation against published sources.

## Constraint Development Workflow

Each new constraint follows this pipeline:

1. **Study plan** — add the constraint to `plans/space_habitat_study_plan.md`
   with physics description, formula, and references
2. **Implementation** — write the constraint class in
   `models/habitat_constraints/src/.../constraints/`, add to
   `HumanAssumptions` if needed, register in `api/main.py`
3. **Tests** — write tests in `models/habitat_constraints/tests/test_constraints/`,
   run `uv run pytest`, `black`, `flake8`, `mypy`
4. **Plan document** — write `plans/constraint_<name>.md` explaining the
   physics, derivation, published values, and proposed thresholds
5. **Literature review** — validate values against published research,
   update `plans/literature_review_structural.md` or
   `plans/literature_review_human_factors.md`
6. **Experiment** — write or extend experiment script in
   `models/habitat_constraints/experiments/` (scorecard, sweeps,
   comparisons)
7. **Conclusions** — write `conclusions/NNN_<topic>.md` with dated results,
   update `conclusions/feasible_habitat_design_space.md` synthesis
8. **Demo update** — add constraint card to interactive demo UI, update
   3D model if the constraint affects geometry

Do not skip steps. Each constraint should have a paper trail from
literature validation through implementation to experimental results.

## Interactive Demo

Located at `demo/`. React + Three.js + Recharts frontend, FastAPI backend.
For 3D rendering details (coordinate system, geometry, mirrors), see
`plans/demo_3d_rendering.md`.
