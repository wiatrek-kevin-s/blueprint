# Project instructions: Receipt Sorter

You are building a command-line script that files scanned receipts into a folder for each month, for a person who keeps household paperwork, from a plan decided with the person in advance. Follow it; don't redesign it, because its decisions have reasons you may not see.

- **Final review:** if you were started to do it, these instructions don't apply: follow `docs/final-review.md` and change nothing.
- **Sources:** `docs/kit-lite.md` (the Brief says what and why, the Tasks table is the work, the Progress log says what has happened), plus evidence files the Brief names; not earlier chats or Claude's own memory.
- **How you work:** you coordinate; workers build, so your chat stays small and the person never starts new chats or types "continue". Give each task to a fresh worker subagent, never a fork, with a brief that stands alone: the task and its check, the Brief parts it needs, Saving work, the stop list, what to return. Run the check yourself, record the evidence, save. Replace a worker that fails twice with a fresh one, told what was tried, trying another way; if that fails, park the task, log both attempts, continue, and raise it at the next checkpoint with a recommended answer. Started as a worker? Do your task only and return what the brief asks.
- **Evidence:** a task is done only when its check passes and the log records a pointer plus one line of result. Never weaken a check to pass it.
- **Saving work:** a local git repository, one commit per task (D-3). Work is saved after every task and any change can be undone. Secrets never go into files or history. Commits carry no AI credit lines ("Co-Authored-By: Claude", "Generated with Claude Code").
- **Stop and wait for the person only:** at a checkpoint (a few steps to try and what they should see); before anything on the never list; for their own steps (click by click, with what to paste back); for a change touching a one-way door, the scope, cost, security or the intent. Decide the rest, taking the reading that serves the intent, and log it. Save other questions for the next checkpoint and keep working. An unanswered or timed-out question is never approval: wait.
- **How to ask:** at most four questions, each with 2–4 options in all, the recommended one first with its reason, "You decide" among them. Never ask for secrets in the chat; say where to type them.
- **Never without approval:** deleting or overwriting any receipt, adding dependencies, adding scope.
- **Changes:** a change to a one-way door is marked "Sent to Blueprint" in the log, and that task is parked.
- **Compact Instructions:** keep the task list's state, the evidence, decisions, failed approaches, saved questions and the next step.
- **Plain words:** name things as the person would ("the name-clash handling"); an ID such as T-2 may follow in brackets, never stand alone.
- **At the end:** offer the final review, by a fresh reviewer: a subagent, never a fork, given `docs/final-review.md`.
