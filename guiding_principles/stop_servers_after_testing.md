# Stop Servers After Testing

## Rule

For any UI/frontend task: **verify → commit → stop**. Always in that order.
Stop all preview/dev servers as the final action of the turn, after committing.

## Why

Running servers consume resources in the background. The user can always restart.
Stopping the server is the last step, not something done before committing.

The verify-before-commit order matters: never commit code that hasn't been
visually confirmed working in the browser.

## How to apply

1. Edit code.
2. `preview_start` → verify with screenshots.
3. Commit the verified code.
4. `preview_stop` on every server started this turn.
5. `preview_list` to confirm `[]` — this is the last action before ending the turn.

## Known limitation

The Claude Preview MCP has a built-in Stop hook that fires when code was edited
and no server is running at turn end. This hook fires even after intentional
`preview_stop` calls (because the hook can't distinguish "stopped intentionally
after verification" from "forgot to verify"). **This is expected and acceptable.**

When the Stop hook fires after a completed verify → commit → stop workflow,
recognize it as a false positive and end the turn. Do not restart the server
just to satisfy the hook.

## Checklist (end of any frontend task)

- [ ] Changes verified with screenshot before committing
- [ ] Code committed
- [ ] `preview_stop` called for each running server
- [ ] `preview_list` returns `[]`
- [ ] If Stop hook fires after the above: expected false positive — ignore it
