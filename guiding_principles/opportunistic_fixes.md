# Opportunistic Fixes

## Rule

Fix errors and friction points the moment you see them — even if they pre-date the current
session, even if you already worked around them. An agent has no attention budget constraints;
there is no excuse for leaving a known problem unfixed.

## Why

Errors that persist across sessions compound: each red line in the feedback screen erodes
trust and wastes diagnostic time. A human might overlook a pre-existing issue; an agent must
not. The cost of a 30-second fix now is far lower than seeing the same failure next session.

## How to apply

1. **Pre-existing errors are not exempt.** If you notice a failing command, broken config,
   or stale path — fix it, even if it was already there when the session started.

2. **Workaround ≠ fix.** If you made a failing command succeed by changing how you called it
   (e.g., adding `PATH=...` inline), also fix the root cause (e.g., update `launch.json` so
   the next call works without the workaround).

3. **Failed commands require a durable correction.** When any command fails — even if you
   recover — ask: *will this fail again next session?* If yes, fix the config/script/file
   before moving on.

4. **Small improvements are always in scope.** Seeing a stale comment, wrong default,
   or minor inconsistency? Fix it as you pass. Don't save it for a "cleanup session" that
   never comes.

## Concrete examples from this project

- `launch.json` had `"runtimeExecutable": "npm"` which failed because the preview server
  doesn't inherit shell PATH. Fixed to `/bin/sh -c "PATH=/opt/homebrew/bin:$PATH npm run dev"`.
  The inline workaround worked once; the file fix prevents it failing every future session.

- Pre-commit hook failed with `npx: command not found` in a prior session. Fix was adding
  `/opt/homebrew/bin` to PATH before committing. That pattern should have been locked in
  immediately so it never fails again.
