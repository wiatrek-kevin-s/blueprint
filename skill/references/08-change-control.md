# Change control (after the kit is delivered)

A delivered kit is never silently rewritten. Changes are made through **decision records** and numbered **amendments**, and the kit is reissued with a new version.

## When the person (or the executing project) wants a change

1. Identify what kind of change it is:
   - **Two-way door:** record a decision, update the affected sections, bump the kit's minor version (1.0 → 1.1).
   - **One-way door, or new scope:** run a short Blueprint cycle on just that decision (research → primer if new to the person → question → decision), then write an amendment and bump the major version (1.x → 2.0).
2. Write the amendment from `templates/amendment.md`:
   - First paragraph: what changes, and which sections it supersedes.
   - A table of affected sections, before and after.
   - Why, with the research behind it.
   - The new design, at the same level of detail as the original.
   - Effect on tasks, checkpoints and open questions, including any work already done that must be revisited.
   - One line naming the cause (see "Learning" below).
3. Produce an updated kit (all files, new version number) and the amendment, and tell the person what to replace in their execution project.

## Changes raised by the executing project

The execution kit tells the executing project to stop and raise a **change request** when it meets a one-way door that the kit does not settle, or evidence that a decision is wrong. The person can paste that request here; handle it as above.

## Learning

Every amendment names its cause: unstated intent, an unknown unknown that the decision map missed, a calibration miss, a premature solution, stale research, an unchallenged assumption, or sequencing that implied rework. If a cause recurs, add the missing item to the standard seams in `02-landscape.md` or the question bank in `03-questioning.md`, and say so to the person.
