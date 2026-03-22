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

```bash
# Terminal 1 — API server (port 8042)
conda activate space
cd models/habitat_constraints
uv run uvicorn habitat_constraints.api.main:app --host 127.0.0.1 --port 8042 --reload

# Terminal 2 — Frontend dev server (port 5173)
cd demo
npm install   # first time only
npm run dev
```

Open http://localhost:5173 in browser. Both servers must be running.

### 3D Scene Coordinate System (`CylinderScene.tsx`)

All components inside the `<group rotation={[-PI/2, 0, 0]}>` use this **local** system:

- **Y** = cylinder long axis (rotation axis), from `-length/2` to `+length/2`
- **XZ** = radial cross-section plane (circular)
- A point on the rim at angle `a`: `[cos(a) * radius, y, sin(a) * radius]`
- Center of cylinder at any y-position: `[0, y, 0]`
- "Down" (toward rim) at angle 0: `+X` direction
- "Up" (toward center) at angle 0: `-X` direction

**Three.js geometry defaults:**
- `cylinderGeometry`: height along Y, circles in XZ ✓ (matches our system)
- `capsuleGeometry`: tall along Y
- `planeGeometry` / `ringGeometry`: lies in XY plane, normal along Z

**Placing objects on the rim surface:**
- Position at `[radius, 0, 0]` puts it on the rim at angle=0
- To stand something "upright" (radially), rotate `[0, 0, PI/2]` which maps Y → -X
- The outer `rotation={[-PI/2, 0, 0]}` maps local Y → world Z for display only

**Key rule:** Never use world coordinates inside the rotation group. Always use
local Y=long axis, XZ=radial.

### External Mirrors — Lessons Learned

The diagonal mirrors at the anti-sun end went through many broken iterations.
The root cause was **Euler rotation errors compounding invisibly** — each rotation
looked plausible in code but produced wrong geometry that's hard to catch without
a physical reference frame.

**What finally worked: custom BufferGeometry with explicit vertex positions.**

Instead of `planeGeometry` + Euler rotations, the mirror is a hand-built quad:
```
Inner edge (at hinge):  (0, 0, -t) and (0, 0, +t)
Outer edge (diagonal):  (d, d, -t) and (d, d, +t)
```
where `d` = axial extent, `t` = half tangential width. The 45° diagonal is
baked into the vertex positions `(d, d, …)` — no rotation needed on the mesh.

**Why Euler rotations kept failing:**

1. **`R_Y(α)` sign trap:** Three.js `R_Y(α)` maps `+X → (cos α, 0, -sin α)`.
   To get `+X = radial outward = (cos θ, 0, sin θ)`, you need `α = -θ`, NOT `+θ`.
   Using `+θ` flips the Z component and sends the mirror **radially inward**.

2. **No visual reference in space:** Unlike terrestrial scenes with ground/sky,
   a cylinder floating in space has no fixed "up." A mirror extending inward at
   45° looks almost identical to one extending outward at 45° from many camera
   angles. The error is invisible until you check from the right viewpoint.

3. **Compound rotations are fragile:** Group rotation + mesh rotation + geometry
   defaults = 3 layers of transforms. Getting any one sign or axis wrong silently
   produces geometry that looks plausible but is physically wrong.

**Rule: For any geometry that must be at a specific angle to the cylinder
(mirrors, solar panels, antennas), use custom BufferGeometry with explicit
vertex positions. Never rely on Euler rotations for critical angular placement.**
