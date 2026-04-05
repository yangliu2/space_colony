# Deployment — Hosting and CI/CD

## Live URLs

| Service | URL |
|---------|-----|
| Interactive demo | [spinhabitat.com](https://spinhabitat.com) |
| Docs | [docs.spinhabitat.com](https://docs.spinhabitat.com) |
| API | [api.spinhabitat.com](https://api.spinhabitat.com) |
| API (fallback) | [space-colony-api.fly.dev](https://space-colony-api.fly.dev) |

## Stack

| Piece | Service | Cost |
|-------|---------|------|
| Interactive demo (React + Three.js) | Vercel | Free (hobby) |
| Constraint API (FastAPI) | Fly.io | Free allowance; requires credit card |
| Docs (MkDocs Material) | GitHub Pages | Free |
| Domain + DNS | Cloudflare Registrar | ~$10/year (.com at cost) |

## DNS Records (Cloudflare → spinhabitat.com)

| Type | Name | Value | Proxy |
|------|------|-------|-------|
| `A` | `@` | `216.198.79.1` | OFF |
| `CNAME` | `www` | `71e2059f344b27d8.vercel-dns-017.com` | OFF |
| `CNAME` | `docs` | `yangliu2.github.io` | OFF |
| `CNAME` | `api` | `space-colony-api.fly.dev` | OFF |

Proxy must be OFF (gray cloud) — Vercel, GitHub Pages, and Fly.io each manage their own CDN and SSL.

## CI/CD — Never deploy manually

Push to `main` → GitHub Actions deploys everything automatically.
Never `ssh`, restart by hand, or run `fly deploy` from localhost.

| Trigger | Workflow | Target |
|---------|----------|--------|
| Push to `main` (any file) | Vercel (direct GitHub integration) | `spinhabitat.com` |
| Push to `main` (`models/habitat_constraints/**`) | `.github/workflows/deploy_api.yml` | Fly.io |
| Push to `main` (any file) | `.github/workflows/deploy_docs.yml` | `docs.spinhabitat.com` |

## Secrets and env vars

- `FLY_API_TOKEN` — GitHub repo secret (Settings → Secrets → Actions); never expires by default
- `VITE_API_URL` — Vercel environment variable set to `https://api.spinhabitat.com`

Never commit `.env` files. Never set env vars on the server directly.

## Vercel setup notes

- Custom domains: `spinhabitat.com` (308 → www) and `www.spinhabitat.com` (Production)
- SPA routing: `demo/vercel.json` rewrites all paths to `index.html`
- Ignored Build Step: `if [ "$VERCEL_GIT_COMMIT_REF" = "gh-pages" ]; then exit 0; fi; exit 1`
  (prevents `gh-pages` branch from triggering Vercel builds)
- Build command: `npm run build` (runs `tsc -b && vite build`) from `demo/` directory

## GitHub Pages setup notes

- Branch: `gh-pages` (auto-deployed by MkDocs via `deploy_docs.yml`)
- Custom domain: `docs.spinhabitat.com` — set in repo Settings → Pages
- HTTPS enforced: yes

## Free tier realities

**Vercel**: Genuinely free for non-commercial use. No sleeping.

**Fly.io**: Free allowance (~$5/month credit), not a true free tier.

- Requires credit card on file
- Scales to zero → 1–3s cold start on first request
- To eliminate cold starts: set `min_machines_running = 1` in `fly.toml` (~$2/month)

**GitHub Pages**: Genuinely free, 1 GB storage limit.

**Cloudflare Registrar**: At-cost pricing, no markup on renewals.

## Rollback

- **Demo**: Vercel dashboard → deployment history → instant rollback
- **API**: `flyctl releases list` then `flyctl deploy --image <image-id>`
- **Docs**: revert the commit, push to `main`
