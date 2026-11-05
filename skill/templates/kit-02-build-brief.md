# Build brief: <PROJECT NAME>

Version <1.0> · as of <DATE> · prepared with Blueprint · size: <medium or large>

<Two sentences: what is built, for whom, and the most important choice.>

Each fact lives in one section; elsewhere, cite its ID (D-n, REQ-n, F-n, T-n), so the brief can't contradict itself.

## Intent

> <The confirmed intent statement.>

Users: <who>. Success measures: <observable results>. Non-goals: <what it deliberately won't do>.

## Context

<What exists today, the constraints, and what research found, with sources and dates.>

## Design

<Overview first, with a diagram for any flow; then each part: what it does, its data and interfaces, exact technologies and versions with an "as of" date. Screens: see the design spec.>

## Requirements

<Coded: one measurable statement each, with Given / When / Then checks for Must and Should, including an edge case and a failure case.>

| ID | Requirement | Priority | Task |
|---|---|---|---|

## Decisions

| ID | Decision | Choice | Why | Door | Status |
|---|---|---|---|---|---|

<Each one-way door: the options and why this one won.>

Decide yourself, and log with the reason, two-way details within this design, such as <exact versions within the named stack, file layout, test data, internal names>. Ask before touching a one-way door, the scope, cost, security or the intent.

## Rules and examples

Each rule with one worked example, so the edges aren't guessed. Cover: empty, duplicate, boundary, wrong order, changed later, deleted or left unfinished, two at once; and, where there are roles, that removing a person or a role ends their rights and sessions at once (with a click-through test).

| Rule | Example | Expected result |
|---|---|---|

## Formats that last

Every format real data or other people depend on, field by field, because changing one later means migrating data. Dates are stored as ISO 8601. For each file: <header row, separator, quoting, encoding, line endings>. For each link between records: <what deleting the linked record does: keep, empty or delete>.

| ID | Format | Field | Type | Required in storage | Allowed values | Example |
|---|---|---|---|---|---|---|

## Security baseline

<Coded: the ten baseline items, each applied (where), not applicable (why) or accepted risk (D-n, shown to the person). Weakening part of an item makes it an accepted risk.>

## Where the work happens

<Environment (D-n); where outputs live; the save-work policy; what the person does because Claude can't, such as sign-ins and payments.>

## Keeping it running

<From the design: owner and hours a month, and what happens if they stop; the change streams, each with who handles it, how often, its trigger, its check and what needs approval; the automation policy; the safety net; the person's monthly runbook; tool choice with an "as of" date.>

## Homework

| ID | What only the person can provide | How to get it | Needed by |
|---|---|---|---|

## Tasks

<Claude Code: the tasks are in tasks.json. Claude project: one "### T-n: title" per task, with "Done by:", depends on, delivers, and each check as "How:" and "Expected:".> The first milestone is a thin version that works end to end.

| Session | Tasks | Area | Checkpoint at end |
|---|---|---|---|

## Checkpoints

After the first task, at each milestone, before anything irreversible, and <at the named points>.

## Open questions and assumptions

| ID | Question or assumption | Settled at | If false or unanswered |
|---|---|---|---|

## Never without approval

- <publishing, spending, deleting, sending, adding scope>

## Definition of done

Every task: <checks pass with evidence; formatter and linter clean; scanners clean>. The project: <each success measure met>. Then the final review.

## Sources

- <title, publisher, date, link>
