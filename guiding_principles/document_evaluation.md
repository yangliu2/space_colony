# document_evaluation.md — Evaluate new documents against existing research

## Rule

Before finalising any new document, check it against all prior documents in the repo.
A new finding that contradicts an existing one must be resolved — either the old document
is updated, or the contradiction is explicitly explained as a refinement.

## Checklist for every new document

1. **Consistency check** — does this contradict any existing constraint plan, conclusion, or literature review?
   - If yes: update the older document or add a "Revised by:" note
   - If no: proceed

2. **Novelty check** — has this been published or noted by others?
   - Search literature (Globus, O'Neill, NASA SP-413, arXiv) before claiming a novel finding
   - If it's known: cite the source; do not present as original
   - If it appears novel: flag it clearly and note the absence of prior citation

3. **Progressive narrative check** — does the new document build on prior ones?
   - Each document should reference what was established before it
   - Surprising findings must be set up by the expected result first (see progressive_disclosure.md)

4. **Scope check** — does the document evaluate the habitat as a whole system?
   - Isolated constraints must note their interaction with other constraints
   - Example: cylinder length cannot be discussed without rotational stability and counter-rotation

## Trigger

Run this evaluation whenever:
- A new constraint plan is created
- A conclusion document is written
- An existing finding is revised

## Anti-patterns

- Claiming a finding is novel without a literature search
- Updating a constraint value without checking if prior conclusions still hold
- Adding a document that silently reframes a prior finding without acknowledging the change
