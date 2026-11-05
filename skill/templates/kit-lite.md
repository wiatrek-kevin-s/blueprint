# Execution kit (lite): <PROJECT NAME>

Kit version <1.0> · as of <DATE> · prepared with Blueprint · size: small

Setup: <Claude project: paste the Instructions part into the project instructions and add this file to its knowledge. Claude Code: save this file as CLAUDE.md in the project folder.> Keep `04-final-review.md` for the end. First message: "Let's start: read the kit, tell me where things stand, and begin."

## Instructions

You are building <one-line description> for <who> from an agreed plan. Follow it, verify every step, and ask when it doesn't settle something. Don't redesign it, because its decisions have reasons you may not see.

- **Sources:** this file only. The Brief says what and why; the Tasks table is the work; the Progress log says what has happened.
- **Each session:** read the Progress log and the Tasks; check where work was last saved; say in two lines where things stand; do the next tasks in order; update the log as you go.
- **Evidence:** a task is done only when its check passes and the log records a pointer plus one line of result, because an unverified "done" is how builds fail. Never weaken a check to pass it.
- **Saving work:** <the policy (D-n)>. Work is saved after every task and any change can be undone. Secrets never go into files or history.
- **The person's steps:** click by click, say what to paste back, and wait.
- **Stop and ask** when the plan can be read two ways, an assumption turns out false, or anything would change a decision, the scope, cost, security or the intent. At most four questions, each with options, the recommended one first. Never ask for passwords or keys; say where to enter them.
- **Never without approval:** <publishing, spending, deleting, sending, adding scope>.
- **Changes:** decide small matters, such as <versions, file layout, test data>, and log them with the reason. A change to a one-way door is marked "Sent to Blueprint" in the log, and that task pauses.
- **Context:** start a fresh chat when this one grows long, and re-read this file after any compaction.
- **At the end:** offer the final review in a fresh chat, from `04-final-review.md`.

## Brief

> <The confirmed intent statement.>

<Context and design in a few lines; versions with an "as of" date.>

| ID | Decision | Choice | Why | Door |
|---|---|---|---|---|

**Rules and examples:** <each rule with one worked example, covering empty, duplicate, boundary, wrong order, changed later, deleted or left unfinished, and two at once>.

**Formats that last:** <each format others depend on, field by field: name, type, required or not, allowed values, example; dates stored as ISO 8601; for files also the header row, separator, quoting and line endings; for linked records, what deleting one does>.

### Security baseline

<Coded: the ten baseline items, each applied, not applicable or accepted risk (D-n, shown to the person), one line each.>

## Keeping it running

<5 to 10 lines: who looks after it and for how many hours a month; how updates and security alerts are checked; what expires and when; what agents may do unattended, if anything.>

## Tasks

| Task | Title | Done by | How | Expected | Status |
|---|---|---|---|---|---|

<The first task is a thin version that works end to end. "How" names who runs the check and what it needs; "Expected" is a visible pass mark.>

## Progress log

- **Where things stand:** <not started>
- **Decisions made while building:** <date: decision, why>
- **Handoff note:** <done, loose ends, next>

## Definition of done

<Every task's check passes with evidence; formatter and scanners clean, if coded; each success measure met.> Then the final review.
