# Start here: <PROJECT NAME>

Kit <1.0> · <DATE> · prepared with Blueprint

This kit lets Claude build <one-line description> from your plan. Once started, it runs the build itself.

## Before you start

Do the homework in <the brief file>'s Homework section: what only you can provide, how and when.

<Claude Code: install it and the tools the build needs (such as git); sign in to <the code host>; know where you will type each secret, never into the chat.>

## Set up

<Claude Code: put every kit file except this one and any the brief keeps outside the project into <the project folder>; start Claude Code there and send the first message.>

<Claude project: create a new project (not the planning one), so it starts clean. Paste `project-instructions.md` into its instructions; add `build-brief.md` or its parts, `progress-log.md` and any `design-spec.md` to its knowledge; keep `final-review.md` for the end; turn on file creation and web search.>

## First message

> <Claude Code: "Set up the kit, unless CLAUDE.md already holds it: rename project-instructions.md to CLAUDE.md and move the other kit files into docs/ unchanged, except any the brief keeps outside the project (if another CLAUDE.md is here, ask me first). Then follow CLAUDE.md and begin." Claude project: "Let's start. Read the progress log and the task list, tell me where things stand, and begin.">

<Claude Code: send it once. After any stop (a closed laptop, a usage limit, `/clear`), send "Continue the build." instead.>

## Kit files

Only these files count; planning notes and drafts don't: `project-instructions.md` (how Claude works; `CLAUDE.md` in Claude Code), `build-brief.md`, or `build-brief-1.md`, `build-brief-2.md`… for large projects (the plan), `progress-log.md` (what has happened), `tasks.json` (the work; in a Claude project, a table in the log), `final-review.md` (the review at the end) and `design-spec.md` (the look, if any), plus evidence files the brief names.

## How it will work

- Claude hands each piece of work to a fresh helper, checks it and logs its decisions. You don't start new chats between pieces of work.
- It stops for you only: at <the checkpoints, in plain words>, with a few steps to try and what you should see; before anything that can't be undone; and for what only you can provide. Other questions wait for the next checkpoint, with a recommended answer; "you decide" is fine.
- A change marked "Sent to Blueprint" touches a core decision: take it to your Blueprint project for an amended kit.
- Stuck, or asked something you can't answer? Bring Blueprint the builder's last message, the progress log and the failing check's output.
- <Claude project: no helpers there, so you relay files: replace `progress-log.md` with each new one, and start a new chat for each area of work with "Continue with the next area of work.">
