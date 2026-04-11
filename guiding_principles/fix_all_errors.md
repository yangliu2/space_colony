# Fix All Errors

Fix every lint, mypy, black, flake8, test, or type error encountered — regardless
of whether the current session introduced it.

**The measure of quality is a clean codebase, not a clean diff.**

## What this means in practice

- Run the full linter / type-checker suite after any code change.
- If pre-existing errors appear in the output, fix them before ending the session.
- Never leave a session with known failing checks, even if they were failing before
  you started.
- When time or scope makes a full fix impractical, document the errors in a TODO
  comment or issue and flag them explicitly to the user — but do not silently ignore
  them.

## Rationale

Attributing errors to "someone else's code" is a broken-windows failure mode.
Errors accumulate, become normalized, and eventually mask real regressions.
Every session is an opportunity to leave the codebase slightly healthier.
