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

## Interactive Demo

Located at `demo/`. React + Three.js + Recharts frontend, FastAPI backend.
For 3D rendering details (coordinate system, geometry, mirrors), see
`plans/demo_3d_rendering.md`.
