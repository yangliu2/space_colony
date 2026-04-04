# deployment.md — Hosting and CI/CD

## Stack

| Piece | Service | Cost |
|---|---|---|
| Interactive demo (React + Three.js) | Vercel | Free (hobby, non-commercial) |
| Constraint API (FastAPI) | Fly.io | Free allowance; requires credit card |
| Docs + conclusions | GitHub Pages + MkDocs | Free |
| Domain + DNS | Cloudflare Registrar | ~$10/year |

Free URLs: `space-colony.vercel.app` · `space-colony-api.fly.dev` · `<user>.github.io/space_colony`

## Never deploy manually

Push to `main` → GitHub Actions deploys everything.
Never `ssh`, restart by hand, or `fly deploy` from localhost.

Workflows: `.github/workflows/deploy_api.yml`, `.github/workflows/deploy_docs.yml`
Vercel connects directly to GitHub — no workflow needed.

## Env vars and secrets

- `FLY_API_TOKEN` — GitHub repo secret (Settings → Secrets → Actions)
- `VITE_API_URL` — Vercel environment variable (not a GitHub secret)

Never commit `.env` files. Never set env vars on the server directly.

## Free tier realities

**Vercel**: Genuinely free for non-commercial use. No sleeping.

**Fly.io**: Free allowance (~$5/month), not a true free tier.
- Requires credit card on file
- Scales to zero → 1–3s cold start on first request
- To eliminate: set `min_machines_running = 1` in `fly.toml` (~$2/month)

**GitHub Pages**: Genuinely free.

## Rollback

- Frontend: Vercel dashboard → deployment history → instant rollback
- Backend: `flyctl releases list` then `flyctl deploy --image <image-id>`
- Docs: revert the commit, push to `main`
