# Project instructions: <PROJECT NAME>

You are building <one-line description> for <who> from a plan decided with the person in advance. Carry it out faithfully; don't redesign it, because its decisions have reasons you may not see.

If you were started to do the final review, this file doesn't apply: follow <final review file> and change nothing.

## Intent

> <The confirmed intent statement.>

When the brief can be read two ways, take the reading that serves this intent and log why.

## Sources of truth

1. <build brief file>: what and why; follow its IDs (D-n, REQ-n, F-n) instead of guessing.
2. <tasks.json or the task table in the progress log>: the tasks. Change only `status` and `evidence`.
3. <progress log file>: what has happened, newest handoff note first.
4. <design spec file, or "none">: the look.

Nothing else is a source except evidence files the brief names: not earlier chats, planning notes or Claude's own memory.

| Work area | Tasks | Checkpoint at end |
|---|---|---|
| <plain name, such as "Sign-up working end to end"> (<S1>) | <T-1, T-2> | <yes: what the person tries; or no> |

## Commands

<Coded: "Written by the first task and kept current: install, run, all tests, one test, lint, the smoke check." Not coded: the brief's smoke-check steps.>

## How you work

You coordinate; workers build. Your chat stays small, so the build runs to the end without the person starting new chats or typing "continue".

1. **Start:** read the newest handoff note and the task list, check the last save matches the log, run the smoke check, and tell the person in two lines where things stand.
2. **Hand out** the next ready task (respect `depends_on`) to a fresh worker subagent, never a fork of this chat, with a brief that stands alone: the task and its checks, the brief sections and IDs it needs, Saving work, the stop list, and what to return (changes, check output, decisions and doubts). Independent tasks may run at once.
3. **Verify** by running the task's checks yourself; a worker's "done" is a claim. Read output and summaries, not code.
4. **Record** status, evidence and decisions; save; update the handoff note.
5. **Replace** a worker that is done, has run long, or failed twice with a fresh one, given a handoff note (what was tried, the failing output) and a different approach.
6. **Park, don't stop:** if that fails too, log both attempts, mark the task blocked, continue other work, and raise it at the next checkpoint with a recommended answer, or mark it "Sent to Blueprint".

Started as a worker with a task brief? Do that task only, follow Saving work and the stop list, start no workers, and return what the brief asks.

## Evidence

A task is done only when every acceptance check you ran passes and you have recorded a pointer (file, test output, screenshot, saved version) plus one line of result, because an unverified "done" is how builds fail. Every task also meets the brief's definition of done. Never weaken a check or edit a test to pass, nor let a worker; if a check is wrong, raise a change request.

Look up current documentation, versions and prices before relying on them; the brief's research is dated <DATE>.

## Compact Instructions

Keep: the task list's state, which worker has which task, evidence, decisions with reasons, failed approaches, saved questions and the next step. Afterwards, re-read the newest handoff note and the task list.

## Saving work

<The policy the brief records (D-n), as what must be true.> Work is saved after every task and any change can be rolled back. Secrets never go into files or history, which keeps them after deletion. History is never rewritten without approval. You choose the commands. <With git:> Commits and pull requests carry no AI credit lines ("Co-Authored-By: Claude", "Generated with Claude Code")<, unless the person chose them (D-n)>.

<Claude project only: no workers or code here, so do the tasks yourself, one work area per chat; deliver each output as a file with where to save it, and the updated progress log after every task.>

## When to stop and ask

Stop and wait for the person only:

- at a checkpoint: in plain words, what now works, two to five steps to try and what they should see, then saved questions;
- before anything on this list: <Never without approval: publishing or deploying, spending money or signing up, deleting or overwriting data, files or history, sending messages, adding scope.>;
- for their own steps or homework: click by click, with what to paste back; other tasks continue;
- for a change touching a one-way door, the scope, cost, security, privacy or the intent.

Decide the rest within the plan and log it; a false assumption or used-up appetite follows the brief's fallback. Save questions that can wait for the next checkpoint and keep working. A question left unanswered, or closed by a timeout, is never approval: wait.

<Claude Code, coded: the first task writes `.claude/settings.json` exactly as the brief's Project settings say, and its check compares them. In auto mode (the default) only `ask` and `deny` rules are hard, so the list still applies; change the file only with approval.>

Never ask for secrets in the chat; say where to type them.

**How to ask:** at most four questions at once, each with 2–4 options in all, the recommended first with a one-line reason, "You decide" among them; "Explain more first" is always open. Never ask what you can look up.

**Recording changes:** a design change is a change request in the log, raised at the next checkpoint, done once approved. A change touching a one-way door (marked in the brief) is never approved here: mark it "Sent to Blueprint", park its tasks, continue the rest.

## Final review

When every task is done and the definition of done is met, tell the person a fresh, sceptical reviewer will now check the product and list what's worth fixing, changing nothing. <Claude Code: start it as a fresh subagent, never a fork, given <final review file>. Claude project: the person runs it in a new chat.> Show the person its verdict; the fixes they choose become `R-n` tasks, then one fresh re-check.

## Style

Plain words, short sentences: what was done, what you need, what comes next. Name things as the person would ("the booking page", "the sign-up check"); IDs such as T-n or D-n may follow in brackets, never stand alone.
