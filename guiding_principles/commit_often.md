# commit_often.md — Commit and push every logical unit of work

## Rule

Every completed, tested unit of work must be committed and pushed before
moving on to the next task. Do not accumulate uncommitted changes across
multiple topics.

## Why this matters for agentic systems

- A crash, context reset, or session end loses all uncommitted work
- Smaller commits are easier to review, revert, and bisect
- Push to remote immediately — local commits are still losable
- CI/CD pipelines (Vercel, Fly.io, GitHub Pages) deploy from the remote,
  not from local files

## What counts as a commit boundary

Each of the following is its own commit:

| Unit | Example commit message prefix |
|------|-------------------------------|
| Bug fix | `fix: ...` |
| New constraint or formula | `feat: ...` |
| Formula correction | `fix: correct bending formula exponent ...` |
| New guiding principle | `docs: add <name> guiding principle` |
| Documentation update | `docs: update ...` |
| Test fix | `test: update ...` |
| Combined formula + doc + test | acceptable as one commit if all part of same correction |

## Commit message format

```
<type>: <short summary>

- bullet of what changed and why
- second file / change if relevant
```

Types: `fix` · `feat` · `docs` · `test` · `refactor` · `chore`

## Checklist before leaving any task

- [ ] `git status` — no unexpected untracked files
- [ ] All tests pass (`uv run pytest -q`)
- [ ] `git add <specific files>` (not `-A` blindly)
- [ ] `git commit -m "..."`
- [ ] `git push`
- [ ] Verify push succeeded (check remote or CI)

## Anti-patterns

- Making changes across 5 topics and committing everything in one blob
- Fixing code but not pushing — "I'll push later" is how work gets lost
- Using `git add -A` without reviewing what's being staged
