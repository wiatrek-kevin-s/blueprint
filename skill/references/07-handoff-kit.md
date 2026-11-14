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

**Small projects:** `kit-lite.md` (instructions under 600 words, a short brief with a task table, an empty progress log, the definition of done; renamed `CLAUDE.md` in Claude Code) plus `final-review.md` (into `docs/`), from `templates/kit-lite.md`.

Deliver these exact names, so files drop into `docs/` unchanged; only the instructions file is renamed, because a file delivered as `CLAUDE.md` takes over whichever Claude Code session it lands in.

## Kit rules

- **One source per fact:** each decision lives in one kit file; others cite its ID, so the kit can't contradict itself.
- **Checks the builder can run:** every acceptance check names who runs it and what it needs (`how`) and a pass mark the builder can see, a number or exact output (`expected`), because "works well" can't be checked.
- **Planning files kept apart:** the state file, research and drafts stay outside the kit folder; `START-HERE.md` names the kit files as the only sources; there is no all-in-one copy, because a second copy drifts.

## The build brief

Fill every section of `templates/kit-02-build-brief.md` from the reviewed design, plus: the security baseline (coded; every accepted risk shown to the person in the approval message); the design spec by reference (screens); **Rules and examples** from the edge-case sweep; **Keeping it running** from the design, at its size; open questions and assumptions, each tied to the task where it is settled.

## Tasks

The fields are in `templates/kit-tasks.json` and checked by `scripts/check_tasks.py`; the builder changes only `status` and `evidence`, so "done" keeps its meaning. A good task produces one verifiable result: one flow working end to end, one page, one sourced section. Order tasks so inputs exist first and the riskiest comes early.

**Sessions:** one area of work per session, a few tasks each, ending at a natural boundary (checks passing, a checkpoint), because long mixed sessions drift.

**Checkpoints:** from phase 3's check-in answer, plus always: after the first task, at each milestone, before anything irreversible (publishing, spending, deleting data, sending messages), and at each "decide by" point.

## Saving work (policy)

From phase 3's answer, the kit states what must be true and the builder chooses the commands: work is saved after every task and any task can be rolled back, so a stopped session loses nothing and a bad change can be undone. With git, the version-control policy in `references/software-design-detail.md` applies. In a Claude project, outputs are delivered as files with where to save them, because chat files don't persist.

## Project instructions

Under 1,200 words, because they load at the start of every session. Fill every section of `templates/kit-01-project-instructions.md`; take the session table's task IDs from the task list, never their titles.

## Final review

One sceptical reviewer in a fresh context runs the product, scores each finding and fixes nothing; the person approves a fix set, which becomes `R-n` tasks with one re-check. Lenses: `references/type-adaptations.md`; steps and scoring: `templates/kit-04-final-review.md`.

## Gate G5 and delivery

Run the readiness check and the dry run; fix what they find; walk the person through the tasks, checkpoints and what they'll be asked; get their approval. Deliver each kit file as a separate file, under the names above, and give them the final state file for later amendments (kept outside the project folder).

End the final message with a numbered **Your next steps** block using real names and the project folder (ask for it at approval if unknown), because the person follows it literally. Claude Code: download the kit into `<folder>`; rename `project-instructions.md` (or `kit-lite.md`) to `CLAUDE.md`; create `<folder>/docs`; move `<the other kit files, by name>` into it; keep `START-HERE.md` and the state file aside; start Claude Code in `<folder>` and send "<first message>". Claude project: what to create, paste and add, and the first message.
