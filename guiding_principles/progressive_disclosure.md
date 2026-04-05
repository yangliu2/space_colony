# progressive_disclosure.md — Easy-to-hard ordering for human-facing content

## Rule

Anything shown to a human must progress from easy/familiar to hard/surprising.
Never lead with conclusions, jargon, or edge cases.

## Applies to

- Documentation site navigation and page structure
- Demo UI layout (sliders, panels, constraint cards)
- README sections
- Presentation of research findings

## Ordering principles

1. **Motivation first** — why does this matter? What is the reader trying to understand?
2. **Intuition before math** — plain-language explanation before equations
3. **Expected before surprising** — confirm what people already believe, then introduce the finding that contradicts it
4. **Constraints in order of obviousness** — start with constraints everyone would guess (RPM, gravity), end with constraints that require deeper analysis (cross-coupling, cylinder length)
5. **Findings last** — conclusions belong after the reasoning that produces them

## Example: docs nav order

Wrong: Conclusions → Constraint Plans → Physics Intuition
Right: Physics Intuition → Human Comfort → Structural Limits → Findings

## Example: the cylinder length finding

Wrong: "The max length at r=982m is 7,309m."
Right: "O'Neill imagined 32 km cylinders. The bending resonance formula allows that — but
only because he used counter-rotating pairs. A single cylinder at our minimum viable radius
is limited to 3,575m by rotational stability. Longer cylinders require paired counter-rotation."

## Anti-patterns to avoid

- Opening with a results table before explaining what the parameters mean
- Nav sections titled with constraint names before explaining what constraints are
- Burying the surprising finding at the end of a long derivation
