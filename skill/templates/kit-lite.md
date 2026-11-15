# Execution kit (lite): <PROJECT NAME>

Kit version <1.0> · as of <DATE> · prepared with Blueprint · size: small

<This template makes two files: the Instructions part becomes `project-instructions.md`, headed "# Project instructions: <PROJECT NAME>"; everything else becomes `kit-lite.md`.>

Setup: <Claude Code: put `project-instructions.md`, `kit-lite.md` and `final-review.md` in the project folder (not files the Brief keeps outside the project), start Claude Code there and, the first time only, send: "Set up the kit, unless CLAUDE.md already holds it: rename project-instructions.md to CLAUDE.md and move kit-lite.md and final-review.md into docs/ unchanged (if another CLAUDE.md is here, ask me first). Then follow CLAUDE.md and begin." After any stop (a closed laptop, a usage limit, a `/clear`), send: "Continue the build." Claude project: paste `project-instructions.md` into the project instructions, add this file to its knowledge, keep `final-review.md` for the end, and send: "Let's start: read the kit, tell me where things stand, and begin.">

Before you start: <what only the person can provide, how and when; Claude Code: installing it and the tools the build needs (such as git), signing in to the code host, and where each secret is typed, never into the chat.> Stuck, or asked something you can't answer? Bring Blueprint the builder's last message, the Progress log and the failing check's output.

## Instructions

You are building <one-line description> for <who> from a plan agreed in advance with the person. Don't redesign it: its decisions have reasons you may not see.

- **Final review:** started to do it? These instructions don't apply: follow <`docs/final-review.md`> and change nothing.
- **Sources:** <`docs/kit-lite.md`> (Brief: what and why; Tasks: the work; Progress log: what has happened) and evidence files the Brief names; not earlier chats or Claude's memory. In the Tasks table, change only Status and Evidence.
- **How you work:** you coordinate and workers build, so your chat stays small. On start or "Continue the build", read the Progress log and carry on. Give each task to a fresh worker subagent, never a fork, with a stand-alone brief: the task and its check, the Brief parts it needs, Saving work, the stop list, what to return. Do a task too small to grow your chat (a one-file change) yourself. Run the check yourself, record the evidence, save. Replace a worker that is done, runs long or fails twice with a fresh one, told what was tried; if that fails, park the task, log both attempts, continue, and raise it at the next checkpoint with a recommended answer. Chat long, or just compacted? Write the handoff note and carry on; only if you can't, ask the person to type `/clear` and send "Continue the build". Started as a worker? Do your task only and return what the brief asks.
- **Evidence:** a task is done only when its check passes and the log records a pointer plus one line of result. A check that can only pass later (a scheduled run) becomes a dated checkpoint item, not a blocker. Never weaken a check to pass it.
- **Saving work:** <the policy (D-n)>. Work is saved after every task and any change can be undone. Secrets never go into files or history. <With git:> Commits and pull requests carry no AI credit lines ("Co-Authored-By: Claude", "Generated with Claude Code")<, unless the person chose them (D-n)>.
- <Claude Code, coded: **Project settings:** the first task writes `.claude/settings.json` exactly as the Brief says, and its check compares them; change it only with approval.>
- **Stop and wait for the person only:** at a checkpoint (a few steps to try and what they should see); before anything on the never list; for their own steps (click by click, with what to paste back); for a change touching a one-way door, the scope, cost, security or the intent. Decide the rest, taking the reading that serves the intent, and log it. Save other questions for the next checkpoint and keep working. An unanswered or timed-out question is never approval.
- **How to ask:** at most four questions, each with 2–4 options in all, the recommended one first with its reason, "You decide" among them. Never ask for secrets in the chat; say where to type them.
- **Never without approval:** <publishing, spending, deleting, sending, adding scope>.
- **Changes:** a change to a one-way door is marked "Sent to Blueprint" in the log, and that task is parked. Apply an amendment from Blueprint to `kit-lite.md` yourself, section by section, keeping the Progress log; never replace the whole file.
- **Compact Instructions:** keep task states, evidence, decisions, failed approaches, saved questions and the next step.
- **Plain words:** name things as the person would ("the import step"); an ID such as T-2 may follow in brackets, never stand alone.
- <Claude project: no workers or code here: do the tasks yourself; deliver outputs as files, plus the updated `kit-lite.md` after each task for the person to replace in knowledge.>
- **At the end:** offer the final review, by a fresh reviewer <Claude Code: a fresh subagent, never a fork, given `docs/final-review.md`; Claude project: a new chat from `final-review.md`>.

## Brief

> <The confirmed intent statement.>

Appetite: <time>; if it runs out, cut <T-n> first, carry on, and raise it at the next checkpoint (unless the cut touches a one-way door).

<Context and design in a few lines; versions with an "as of" date; any file to keep outside the project, such as an audit report for a public project.>

| ID | Decision | Choice | Why | Door |
|---|---|---|---|---|

**Rules and examples:** <each rule with one worked example, covering empty, duplicate, boundary, wrong order, changed later, deleted or left unfinished, and two at once>.

**Formats that last:** <each format others depend on, field by field: name, type, required or not, allowed values, example; dates stored as ISO 8601; for files also the header row, separator, quoting and line endings; for linked records, what deleting one does>.

### Security baseline

<Coded: the ten baseline items, each applied, not applicable or accepted risk (D-n, shown to the person), one line each.>

Checklist coverage: <coded: each checklist item: D-n, F-n or "N/A: reason">

### Project settings

<Claude Code, coded: the exact `.claude/settings.json` the first task writes, as of <DATE>, in a code block: deny reading `.env*` and secret folders; `"env": {"CLAUDE_CODE_FORK_SUBAGENT": "0"}`; ask before this design's deploy, publish and force-push commands; `"attribution": {"commit": "", "pr": "", "sessionUrl": false}` unless the person chose credit lines. Otherwise "None".>

## Keeping it running

<5 to 10 lines: who looks after it and for how many hours a month; how updates and security alerts are checked; what expires and when; what agents may do unattended, if anything.>

## Tasks

| Task | Title | Delivers | Done by | How | Expected | Status |
|---|---|---|---|---|---|---|

<The first task is a thin version that works end to end. "How" names who runs the check and what it needs; "Expected" is a visible pass mark. Mark which tasks end at a checkpoint.>

## Progress log

- **Where things stand:** <not started>
- **Decisions made while building:** <date: decision, why>
- **Saved for the next checkpoint:** <none yet>
- **Change requests:** <none yet>
- **Handoff note:** <done, loose ends, next>

## Definition of done

<Every task's check passes with evidence; formatter and scanners clean, if coded; each success measure met.> Then the final review.
