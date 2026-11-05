# Phase 4: the design document

Goal: a design a stranger could build from; it becomes the core of the kit. Draft only after G3, because a design built on open one-way doors gets rebuilt.

## Process

1. Show the outline (headings, one line each) first, so the person can redirect cheaply.
2. Fill one section at a time, researching its details (`references/04-research.md`).
3. A new decision found while drafting goes on the decision map; if it is a one-way door, stop and ask before writing past it.

## Contents

Adapt with `references/type-adaptations.md`. Summary (what, for whom); intent, users, success measures and non-goals; context and research, with sources and dates; the design, overview first with a diagram for any flow; alternatives for each one-way door; cross-cutting concerns (security, privacy, accessibility, cost, legal); keeping it running (`references/keeping-it-running.md`); implementation detail (exact names, versions, formats); milestones with tested gates; decisions; open questions with owner and "decide by"; assumptions.

- **Coded projects** add the security baseline section (`references/software-design-detail.md`), each item applied, not applicable or accepted.
- **Projects with screens** add the design spec from phase 3D by reference, not by copy.

## First milestone

The first milestone is always a thin version that works end to end (Gall's Law), because a complex system that works grows from a simple one that worked.

## Subtraction pass

Before review, question every requirement and delete what isn't needed, after finding out why it exists (Chesterton's fence). Log cuts as later options. Never cut legal, safety or accessibility needs, because those are the person's obligations, not features.

## Edge-case sweep (X-1)

Give each core rule a worked example, then check it against these cases: empty, duplicate, boundary (the limit itself and one past it), wrong order, changed later, deleted or left unfinished, and two at once. Write the answer for each case that applies, because a builder meeting an unstated case guesses. The results go into the brief's "Rules and examples" section.

Example: "A member may book at most 2 slots a week." Boundary: the 2nd booking succeeds and the 3rd is refused with "You have 2 bookings this week". Changed later: cancelling one frees a slot. Two at once: two taps in the same second still give only one booking.

## Hard-to-undo details

State these, because builders guess them and each is costly to change once people use the product:

- **Removal:** how long each kind of personal record is kept, active ones included, and when its clock starts; what deleting or anonymising one does to the records that point to it and to any counts; what happens to records never finished.
- **Control:** who holds admin rights and every second factor, how roles are given and taken away, and which account connects each tool. Removing a person or taking away a role ends their rights and open sessions at once, with a click-through test, because a demoted admin otherwise keeps access until their session expires.
- **Costs:** every running cost and free-tier limit, and what any spending limit counts.
- **Fixed at first launch:** app and storage names, the exact web address (with or without `www`), and settings that are hard to undo, such as HSTS preload.

## Length

1–3 pages for small, 4–10 for medium, 10–20 for large; split beyond that. Save length by cutting repetition, never a detail the builder needs.
