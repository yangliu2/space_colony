# Docs Sync (mkdocs.yml)

## Principle

Every new `plans/constraint_*.md` file must be added to `mkdocs.yml` **in the same
commit** that creates the file. The rendered docs at `docs.spinhabitat.com` are the
public face of this work — a constraint that exists in code but not in docs is invisible.

---

## Where to Register

File: `mkdocs.yml` at the project root.

The `nav:` section is the only thing that controls what appears on the docs site.
**MkDocs does not auto-discover files.** If the file is not in `nav:`, it will not render.

### Current nav structure

| Section | Contains |
|---|---|
| `1. How Does It Work?` | Physics intuition pages |
| `2. Can Humans Live There?` | Human-factors constraints (vestibular, gravity, Coriolis, atmosphere) |
| `3. Will the Structure Hold?` | Structural constraints (hoop stress, rim speed, length, stability, spin-up) |
| `4. Life Support` | Systems constraints (agriculture, thermal, energy) |
| `5. The Design` | Mirror geometry, interior space, materials |
| `6. Findings` | Conclusion docs |
| `Reference` | Literature reviews, Q&A |

### Adding a new constraint

1. Create `plans/constraint_<name>.md`.
2. Find the correct section in `mkdocs.yml` (match the constraint category).
3. Add one line:
   ```yaml
   - "Constraint Label": plans/constraint_<name>.md
   ```
4. Verify locally with `mkdocs serve` if possible, or just confirm the file path is correct.
5. Include the `mkdocs.yml` change in the **same commit** as the constraint implementation.

---

## Anti-Patterns

- Creating a plan file and only committing it later (docs site stays stale for days/weeks).
- Numbering sections in the nav title (`"4. Life Support"`) without updating later sections
  when a new section is inserted — always renumber all affected sections.
- Pointing the nav at a file that doesn't exist — MkDocs will build but warn, and the page
  will 404 in production.

---

## Checklist (part of constraint workflow step 4)

- [ ] `plans/constraint_<name>.md` created
- [ ] Entry added to correct `mkdocs.yml` nav section
- [ ] No stale section numbers (renumber if a section was inserted)
- [ ] Both files committed together
