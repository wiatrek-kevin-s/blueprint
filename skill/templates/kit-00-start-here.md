# Start here: <PROJECT NAME>

Kit <1.0> · <DATE> · prepared with Blueprint

This kit lets a fresh Claude build <one-line description>, one session per chat.

## Before you start

<What only you can provide, how to get it, and which session needs it.>

## Set up

Use the brief's environment (<D-n>).

- **Claude project:** create a new project (not the planning one), so it starts clean. Paste `01-project-instructions.md` into its instructions; add `02-build-brief.md`, `03-progress-log.md` and any `design-spec.md` to its knowledge; keep `04-final-review.md` for the end; turn on file creation and web search.
- **Claude Code:** in <the private repository or folder you own>, save `01-project-instructions.md` as `CLAUDE.md` and the rest in `docs/` without their number prefixes (such as `docs/build-brief.md`). Start Claude Code there.

## First message

> Let's start. Read the progress log and the task list, tell me where things stand, and begin session 1.

Each later session: a new chat, then "Continue with the next session."

## Kit files

Only these files count; planning notes and drafts don't: `01-project-instructions.md` (how Claude works), `02-build-brief.md` (the plan), `03-progress-log.md` (what has happened), `tasks.json` (the tasks; in a Claude project, a table in the log), `04-final-review.md` (the review at the end) and `design-spec.md` (the look, if any).

## How it will work

- Your steps: <person-done steps>. Claude says exactly what to do and paste back.
- Claude stops and asks at <checkpoints in plain words>, with a recommended answer; "you decide" is fine.
- In a Claude project, replace `03-progress-log.md` with each new one Claude gives you.
- A change marked "Sent to Blueprint" touches a core decision: take it to your Blueprint project for an amended kit.
