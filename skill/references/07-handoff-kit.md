# Phase 6: the execution kit

Goal: turn the reviewed design into a kit a fresh agent builds from without guessing (G5: the person approves). The builder never sees this conversation and reads literally, so everything it needs is in the kit.

## Readiness

A kit is ready when `scripts/check_kit.py <kit folder>` passes (or its checklist is walked by hand where code can't run), the fresh-agent dry run in `references/06-review.md` finds no harmful one-way guess, and the person approves. The script lists its checks, with reasons, at its top. Add `--coded` (coded) and `--screens` (3D ran), because the script can't tell.

## Kit files (medium and large)

| File | Claude project | Claude Code | Template |
|---|---|---|---|
| `START-HERE.md` | Read by the person | Read by the person | `templates/kit-00-start-here.md` |
| `project-instructions.md` | Project instructions | Renamed `CLAUDE.md` | `templates/kit-01-project-instructions.md` |
| `build-brief.md` | Project knowledge | `docs/build-brief.md` | `templates/kit-02-build-brief.md` |
| `progress-log.md` | Project knowledge | `docs/progress-log.md` | `templates/kit-03-progress-log.md` |
| `tasks.json` | A table in the log | `docs/tasks.json` | `templates/kit-tasks.json` |
| `final-review.md` | Kept for a new chat | `docs/final-review.md` | `templates/kit-04-final-review.md` |
| `design-spec.md` | Project knowledge | `docs/design-spec.md` | `templates/design-spec.md`, where 3D ran |

**Large projects** split the brief as `build-brief-1.md`, `build-brief-2.md`…, each under 8,000 words, all named wherever the brief is.

**Small projects,** from `templates/kit-lite.md`: `project-instructions.md` (its Instructions part, under 700 words), `kit-lite.md` (the rest) and `final-review.md`. Claude Code: the first becomes `CLAUDE.md`, the others go into `docs/`.

Deliver these exact names, so files drop into `docs/` unchanged; only the instructions file is renamed, because a file delivered as `CLAUDE.md` takes over whichever Claude Code session it lands in.

## Kit rules

- **One source per fact:** each decision lives in one kit file; others cite its ID, so the kit can't contradict itself.
- **Checks the builder can run:** every acceptance check names who runs it and what it needs (`how`) and a pass mark the builder can see, a number or exact output (`expected`), because "works well" can't be checked.
- **Planning files kept apart:** the state file, research and drafts stay outside the kit folder; there is no all-in-one copy, because a second copy drifts.
- **Kept outside the project:** no setup step moves in a file the brief keeps outside the project, such as a public project's audit report.

## The build brief

Fill every section of `templates/kit-02-build-brief.md` from the reviewed design; **Rules and examples** come from the edge-case sweep, **Keeping it running** from the design, at its size.

## Tasks

The fields are in `templates/kit-tasks.json` and checked by `scripts/check_tasks.py`. A good task produces one verifiable result: one flow working end to end, one page, one sourced section. Order tasks so inputs exist first and the riskiest comes early.

**Work areas:** a few tasks each, named in plain words, ending at a natural boundary (checks passing, a checkpoint); a task's `session` field holds its area's ID.

**Checkpoints:** from phase 3's check-in answer, plus always after the first task, at each milestone and at each "decide by" point; the instructions' stop list covers anything irreversible.

## Saving work (policy)

From phase 3's answer, as what must be true (the instructions' Saving work); the builder chooses the commands. With git, the version-control policy in `references/software-design-detail.md` applies.

## Project instructions

Under 1,200 words, because they load at the start of every session. They make the builder a coordinator of fresh workers that needs the person only at checkpoints, before anything irreversible, for homework and for one-way changes, so every decision the build needs belongs in the kit. Fill every section of `templates/kit-01-project-instructions.md`; take the work-area table's task IDs from the task list.

## Final review

From `templates/kit-04-final-review.md`, with the lenses from `references/type-adaptations.md`.

## Gate G5 and delivery

Run the readiness check and the dry run; fix what they find; walk the person through the tasks, checkpoints and what they'll be asked; get their approval. Lead the approval message with one screen, in plain words: the intent, the one-way decisions, the first three pieces of work, the checkpoints and any accepted risk. Deliver each kit file as a separate file, under the names above, and give them the final state file for later amendments (kept outside the project folder).

End the final message with a numbered **Your next steps** block using real names and the project folder (ask for it at approval if unknown), because the person follows it literally. Claude Code: do "Before you start" (in `START-HERE.md` or `kit-lite.md`); put every kit file except `START-HERE.md` and those kept outside the project into `<folder>`, the state file elsewhere; start Claude Code there and send the set-up message once; after any stop, "Continue the build." Claude project: what to create, paste and add, and the first message.
