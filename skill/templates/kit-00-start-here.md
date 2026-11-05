# Start here: <PROJECT NAME>

Kit <1.0> · <DATE> · prepared with Blueprint

This kit lets a fresh Claude build <one-line description>, one session per chat.

## Before you start

<What only you can provide, how to get it, and which session needs it.>

## Set up

Use the brief's environment (<D-n>).

- **Claude project:** create a new project (not the planning one), so it starts clean. Paste `project-instructions.md` into its instructions; add `build-brief.md`, `progress-log.md` and any `design-spec.md` to its knowledge; keep `final-review.md` for the end; turn on file creation and web search.
- **Claude Code:** in <the project folder>, rename `project-instructions.md` to `CLAUDE.md`; create a `docs` folder and move the other kit files into it as they are (`build-brief.md`, `progress-log.md`, `tasks.json`, `final-review.md`<, `design-spec.md`>). Keep this file for yourself. Start Claude Code in <the project folder>.

## First message

> Let's start. Read the progress log and the task list, tell me where things stand, and begin session 1.

Each later session: a new chat, then "Continue with the next session."

## Kit files

Only these files count; planning notes and drafts don't: `project-instructions.md` (how Claude works; `CLAUDE.md` in Claude Code), `build-brief.md` (the plan), `progress-log.md` (what has happened), `tasks.json` (the tasks; in a Claude project, a table in the log), `final-review.md` (the review at the end) and `design-spec.md` (the look, if any).

## How it will work

- Your steps: <person-done steps>. Claude says exactly what to do and paste back.
- Claude stops and asks at <checkpoints in plain words>, with a recommended answer; "you decide" is fine.
- In a Claude project, replace `progress-log.md` with each new one Claude gives you.
- A change marked "Sent to Blueprint" touches a core decision: take it to your Blueprint project for an amended kit.
