# Stop Servers After Testing

## Rule

For any UI/frontend task: **verify → commit → stop**. Always in that order.
Stop all preview/dev servers as the final action of the turn, after committing.
Never leave a server running between turns.

## Why

Running servers consume resources in the background and can interfere with future
sessions. The user can always restart a server when needed. Leaving servers running
is wasteful and clutters the environment.

The verify-before-commit order also matters: never commit code that hasn't been
visually confirmed working in the browser. Stopping the server is the last step,
not something done before committing.

## How to apply

1. Edit code.
2. `preview_start` → verify with screenshots.
3. Commit the verified code.
4. `preview_stop` on every server started this turn.
5. `preview_list` to confirm `[]` — this is the last action before ending the turn.

## Checklist (end of any frontend task)

- [ ] Changes verified with screenshot before committing
- [ ] Code committed
- [ ] `preview_stop` called for each running server
- [ ] `preview_list` returns `[]`
