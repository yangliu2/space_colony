# Space Colony Project

## Guiding Principles
Read and follow all rules in `guiding_principles/` before starting any task.
Key principles: `progressive_disclosure.md` · `document_evaluation.md` ·
`model_3d_sync.md` · `parameter_dependencies.md` · `epistemic_humility.md` ·
`formula_sync.md` · `commit_often.md` · `opportunistic_fixes.md` · `stop_servers_after_testing.md` · `fix_all_errors.md` · `readme_sync.md`

## File Reading
Keep all files under 10,000 tokens.

## Environment

- **Python:** 3.14.2 — **Package manager:** uv at `/Users/fangfanglai/anaconda3/envs/space/bin/uv`
- `conda activate space` is required to put `uv` on PATH
- Virtualenv: `models/habitat_constraints/.venv`

## Habitat Constraints Package

```bash
conda activate space && cd models/habitat_constraints
uv sync --all-extras   # install
uv run pytest          # test
uv run black --check src/ tests/ && uv run flake8 src/ tests/ && uv run mypy src/
```

- black & flake8: line-length=89 — mypy: strict mode — pytest: with coverage

## Document Style (`plans/`)

- Equations: LaTeX only — `$$` display, `$...$` inline. Never code blocks for formulas.
- Variables in prose must be LaTeX: `$r$`, `$\omega$`, `$\sigma_y$`
- Citations: MLA format, **(Author Year)** inline, full entry in **References** section
  - Two authors: `(Lackner and DiZio 1998)` — Three+: `(Hallgren et al. 2025)`
  - Never bare DOIs or URLs as inline citations

## Literature Review

Files: `plans/literature_review_structural.md`, `plans/literature_review_human_factors.md`

When adding or modifying constraints, validate values against published sources and
update the relevant review file. Key findings summary: `docs/literature_review_summary.md`

## Constraint Development Workflow

1. **Study plan** — add to `plans/space_habitat_study_plan.md`
2. **Implementation** — constraint class in `src/.../constraints/`, register in `api/main.py`
3. **Tests** — `tests/test_constraints/`, run pytest + black + flake8 + mypy
4. **Plan doc** — `plans/constraint_<name>.md` with physics, derivation, thresholds
5. **Literature review** — validate and update the relevant review file
6. **Experiment** — script in `models/habitat_constraints/experiments/`
7. **Conclusions** — `conclusions/NNN_<topic>.md`, update `conclusions/feasible_habitat_design_space.md`
8. **Demo update** — add constraint card to UI, update 3D model if geometry changes
9. **README update** — update constraint count, list, and "What's Next" in README.md (see `readme_sync.md`)

Do not skip steps.

## Interactive Demo

`demo/` — React + Three.js + Recharts frontend, FastAPI backend.
3D rendering details: `plans/demo_3d_rendering.md`
Deployment: `docs/deployment.md`

**Dev server:** use `preview_start` with name `demo` (configured in `.claude/launch.json`).
Node/npm are at `/opt/homebrew/bin/` — the launch config uses `/bin/sh -c "PATH=/opt/homebrew/bin:$PATH npm run dev"` to ensure they're found.
For git commits, always prefix: `PATH="/opt/homebrew/bin:$PATH" git commit ...`
