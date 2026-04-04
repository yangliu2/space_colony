# deployment.md — Hosting and CI/CD

## Stack

| Piece | Service | Cost |
|---|---|---|
| Interactive demo (React + Three.js) | Vercel | Free (hobby, non-commercial) |
| Constraint API (FastAPI) | Fly.io | Free allowance; requires credit card |
| Docs + conclusions | GitHub Pages + MkDocs | Free |
| Domain + DNS | Cloudflare Registrar | ~$10/year |

URLs:
- `spacedemo.yourdomain.com` → Vercel (frontend)
- `api.yourdomain.com` → Fly.io (backend)
- `docs.yourdomain.com` or `yourdomain.com/docs` → GitHub Pages (MkDocs)

## Never deploy manually

Push to `main` → GitHub Actions deploys everything.
Never `ssh` into a server, restart a process by hand, or `fly deploy` from localhost.

## CI/CD — three workflows

**1. Frontend** (`.github/workflows/deploy_demo.yml`)
Vercel connects directly to GitHub — no YAML needed.
Configure once in the Vercel dashboard: Root Directory = `demo`, Framework = Vite.
Every push to `main` auto-deploys. PRs get preview URLs automatically.

**2. Backend** (`.github/workflows/deploy_api.yml`)
```yaml
on:
  push:
    branches: [main]
    paths: ['models/habitat_constraints/**']

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: superfly/flyctl-actions/setup-flyctl@master
      - run: flyctl deploy --remote-only
        working-directory: models/habitat_constraints
        env:
          FLY_API_TOKEN: ${{ secrets.FLY_API_TOKEN }}
```

**3. Docs** (`.github/workflows/deploy_docs.yml`)
```yaml
on:
  push:
    branches: [main]
    paths: ['docs/**', 'conclusions/**', 'plans/**', 'mkdocs.yml']

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: '3.x' }
      - run: pip install mkdocs-material
      - run: mkdocs gh-deploy --force
```

## Env vars and secrets

Set in GitHub Secrets → passed via `deploy.yml` env block.
Never commit `.env` files. Never set env vars on the server directly.

Required secrets:
- `FLY_API_TOKEN` — Fly.io deploy token
- `VITE_API_URL` — set as Vercel environment variable (not a GitHub secret)

## Free tier realities

**Vercel**: Genuinely free for non-commercial use. No sleeping, no cold starts for static assets.

**Fly.io**: Free *allowance* (~$5/month credit), not a true free tier.
- Requires a credit card on file
- Machines scale to zero when idle → 1–3 second cold start on first request
- To eliminate cold starts: set `min_machines_running = 1` in `fly.toml` (~$2/month)

**GitHub Pages**: Genuinely free. No account beyond GitHub needed.

## Fly.io — required files

Add to `models/habitat_constraints/`:

`fly.toml`:
```toml
app = "space-colony-api"
primary_region = "sjc"

[build]
  dockerfile = "Dockerfile"

[http_service]
  internal_port = 8000
  force_https = true
  auto_stop_machines = "stop"
  auto_start_machines = true
  min_machines_running = 0

[[vm]]
  memory = "256mb"
  cpu_kind = "shared"
  cpus = 1
```

`Dockerfile`:
```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY . .
RUN pip install uv && uv sync --no-dev
CMD ["uv", "run", "uvicorn", "habitat_constraints.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## MkDocs — required file

`mkdocs.yml` at repo root:
```yaml
site_name: Space Colony — Constraint Study
theme:
  name: material
  features:
    - navigation.sections
  palette:
    scheme: slate

markdown_extensions:
  - pymdownx.arithmatex:
      generic: true

extra_javascript:
  - https://unpkg.com/mathjax@3/es5/tex-mml-chtml.js

nav:
  - Overview: conclusions/feasible_habitat_design_space.md
  - Conclusions:
    - Structural Constraints: conclusions/004_structural_constraints.md
  - Plans:
    - Study Plan: plans/space_habitat_study_plan.md
    - Literature Review (Structural): plans/literature_review_structural.md
    - Literature Review (Human Factors): plans/literature_review_human_factors.md
```

## Rollback

Frontend: Vercel keeps deployment history — instant rollback from the dashboard.
Backend: `flyctl releases list` then `flyctl deploy --image <image-id>`.
Docs: revert the commit, push to `main`.
