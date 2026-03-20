# Space Colony Project

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
