# readme_sync.md — Keep README.md current with every commit

## Rule

README.md must reflect the actual state of the project at every commit.
Do not commit new constraints, features, or completed phases without
updating README.md in the same commit.

## What to update

| Change made | README section to update |
|---|---|
| New constraint added | "What's Been Done" constraint list and count; remove from "What's Next" |
| Phase completed | Phase status in "What's Been Done" |
| New test files | Testing counts (Python pytest, TypeScript/vitest) |
| New demo feature | "Interactive Demo" description |
| New viewpoint image | "What It Looks Like" section |
| New conclusions doc | "Analysis Outputs" if relevant |

## Checklist — add to every constraint commit

Before finalising the commit message, verify:

- [ ] Constraint count in "What's Been Done" heading is correct
- [ ] New constraint appears in the numbered list with correct category
- [ ] Constraint removed from "What's Next" list
- [ ] Python test file count is accurate
- [ ] Any new `HumanAssumptions` sliders mentioned if significant

## What NOT to do

- Do not leave "What's Next" listing constraints that are already implemented
- Do not leave the constraint count at a stale number
- Do not mention outdated phase completion status
- Do not write "9-constraint model" when 15 constraints exist

## Format guidance

Keep README.md scannable. Use the existing structure:
- Short, factual bullet points in constraint lists
- Bold the binding/surprising results
- Keep "What's Next" honest — only list genuinely unimplemented items
