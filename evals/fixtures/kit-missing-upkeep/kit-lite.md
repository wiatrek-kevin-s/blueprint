# Execution kit (lite): Receipt Sorter

Kit version 1.0 · as of 2026-10-30 · prepared with Blueprint · size: small

Setup: in Claude Code, save this file as CLAUDE.md in an empty project folder. Keep `04-final-review.md` for the end. First message: "Let's start: read the kit, tell me where things stand, and begin."

## Instructions

You are building a command-line script that files scanned receipts into a folder for each month, for a person who keeps household paperwork, from an agreed plan. Follow it, verify every step, and ask when it doesn't settle something. Don't redesign it, because its decisions have reasons you may not see.

- **Sources:** this file only. The Brief says what and why; the Tasks table is the work; the Progress log says what has happened.
- **Each session:** read the Progress log and the Tasks; check where work was last saved; say in two lines where things stand; do the next tasks in order; update the log as you go.
- **Evidence:** a task is done only when its check passes and the log records a pointer plus one line of result, because an unverified "done" is how builds fail. Never weaken a check to pass it.
- **Saving work:** a local git repository, one commit per task (D-3). Work is saved after every task and any change can be undone. Secrets never go into files or history.
- **The person's steps:** click by click, say what to paste back, and wait.
- **Stop and ask** when the plan can be read two ways, an assumption turns out false, or anything would change a decision, the scope, cost, security or the intent. At most four questions, each with options, the recommended one first. Never ask for passwords or keys; say where to enter them.
- **Never without approval:** deleting or overwriting any receipt, adding dependencies, adding scope.
- **Changes:** decide small matters, such as file layout and test data, and log them with the reason. A change to a one-way door is marked "Sent to Blueprint" in the log, and that task pauses.
- **Context:** start a fresh chat when this one grows long, and re-read this file after any compaction.
- **At the end:** offer the final review in a fresh chat, from `04-final-review.md`.

## Brief

> For a person who scans paper receipts into one messy folder, Receipt Sorter will move each scan into a folder named for the month on the receipt's file date, so that finding last March's receipts takes one click. We will know it works when a folder of 200 mixed scans is sorted with none lost. It must never delete or overwrite a file. It will not read the text on the receipts.

The script uses Python's standard library only, so nothing needs installing beyond Python 3 (as of 2026-10-30).

| ID | Decision | Choice | Why | Door |
|---|---|---|---|---|
| D-1 | Language | Python 3, standard library only | Already on the person's computer; nothing to install | Two-way |
| D-2 | Name clashes | Add a number to the new name, never overwrite | The intent forbids losing a file | One-way |
| D-3 | Saving work | Local git repository, one commit per task | Every change can be undone | Two-way |

**Rules and examples:** a scan dated 2026-03-14 goes to `2026-03/`; an empty input folder prints "nothing to sort" and exits 0; a second file with the same name becomes `name (2).pdf`; a file that is not a PDF or image is left where it is and listed at the end; running the script twice moves nothing the second time.

**Formats that last:** month folders are named `YYYY-MM` (ISO 8601), one per month, created only when needed.

### Security baseline

The script reads and moves files in one folder the person names; it opens no network connections and stores no secrets. Each other baseline item is not applicable to a local script.

## Tasks

| Task | Title | Done by | How | Expected | Status |
|---|---|---|---|---|---|
| T-1 | Sort a folder of sample scans end to end | Claude | Run the script on a test folder of 20 dated sample files | Every file is in its month folder; the count before equals the count after | Not started |
| T-2 | Handle name clashes and unknown files | Claude | Run the tests for clashes and non-PDF files | Clashes get a number; unknown files stay and are listed | Not started |
| T-3 | Person's trial on a copy of real scans | the person | The person runs the script on a copy of the scans folder | The person confirms the months look right | Not started |

## Progress log

- **Where things stand:** not started
- **Decisions made while building:** none yet
- **Handoff note:** none yet

## Definition of done

Every task's check passes with evidence; the tests pass; the success measure is met on 200 sample scans. Then the final review.
