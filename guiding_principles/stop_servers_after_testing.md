# Stop Servers After Testing

## Rule

Always stop all preview/dev servers immediately after verification is complete.
Never leave a server running at the end of a task.

## Why

Running servers consume resources in the background and can interfere with future
sessions. The user can always restart a server when needed — it costs nothing to
reopen. Leaving servers running is wasteful and clutters the environment.

## How to apply

1. After every `preview_start` + verification workflow, call `preview_stop` on
   every server that was started.
2. Before ending your turn after any UI/frontend task, call `preview_list` to
   confirm no servers are still running.
3. If `preview_stop` returns "not found", call `preview_list` to verify — the
   server may have already stopped or the ID may have changed.
4. This applies to all servers: frontend dev servers, backend API servers, etc.

## Checklist (end of any preview verification)

- [ ] `preview_stop` called for each server started this session
- [ ] `preview_list` returns `[]`
