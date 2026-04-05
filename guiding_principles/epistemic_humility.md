# epistemic_humility.md — Be careful and humble about new findings

## Rule

When you derive something that appears to be a new result, treat it as a hypothesis,
not a fact. Triple-check the derivation, search the literature, and document
uncertainty clearly — even after the checks pass.

## Checklist for any "new" result

1. **Re-derive from scratch** — work through every step independently; do not
   trust the first derivation.
2. **Check units and scaling** — verify the exponent makes physical sense.
   If $I/A$ cancels a variable (e.g., wall thickness), confirm that before
   propagating the scaling.
3. **Calibrate and sanity-check** — apply the formula to known design points
   (e.g., O'Neill Island Three). Does it reproduce the known answer?
4. **Search the literature** — look for the formula in structural engineering,
   aerospace, and space-habitat sources. Use Google Scholar, arXiv, NASA TR,
   and any domain review files (`plans/literature_review_*.md`).
5. **Write hedged language** — use phrases like *"original to this study,"*
   *"pending independent verification,"* *"not found in published space-habitat
   literature as of [date]."* Never say "proven" or "confirmed" for a
   first-principles derivation.

## Known case: bending resonance formula

The formula $L_\text{max} = 75.2 \cdot r^{3/4}$ was initially written with the
wrong exponent ($r^{5/4}$) and wrong coefficient (1.33) because a derivation
step was not double-checked: for a thin-walled cylinder $I/A = r^2/2$, not
$r^3/2$. The wall thickness $t$ cancels entirely, changing the scaling from
$r^{3/2}$ to $r$, and therefore the final exponent from $5/4$ to $3/4$.

Lesson: **always verify that intermediate quantities simplify correctly.**
A missed cancellation shifted the practical limit for $r = 982$ m from 7.3 km
to 13.2 km — a factor of 1.8.

## Anti-patterns

- Stating a novel derivation as established fact in documentation
- Writing $C \approx 1.33$ without checking the derivation of the exponent first
- Skipping the unit/scaling check because the calibration point "looks right"
  (O'Neill calibrates correctly for *any* exponent if $C$ is set post-hoc)
- Claiming literature-search exhaustiveness without documenting the search terms used
