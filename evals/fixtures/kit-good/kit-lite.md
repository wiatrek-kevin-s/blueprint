# Execution kit (lite): Receipt Sorter

Kit version 1.0 · as of 2026-10-30 · prepared with Blueprint · size: small

Setup: put `project-instructions.md`, `kit-lite.md` and `final-review.md` in an empty project folder, start Claude Code there and send: "Set up the kit: rename project-instructions.md to CLAUDE.md, move kit-lite.md and final-review.md into docs/ unchanged (if a CLAUDE.md is already here, ask me first), then follow CLAUDE.md and begin."

Before you start: Python 3 and git on the computer (both already installed); a copy of the scans folder for the trial in the last task. Nothing in this project needs a password or key.

## Brief

> For a person who scans paper receipts into one messy folder, Receipt Sorter will move each scan into a folder named for the month on the receipt's file date, so that finding last March's receipts takes one click. We will know it works when a folder of 200 mixed scans is sorted with none lost. It must never delete or overwrite a file. It will not read the text on the receipts.

Appetite: two evenings; if it runs out, cut the end-of-run list of unknown files first and raise it at the next checkpoint.

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

## Keeping it running

- **Owner and time:** the person, 10 minutes a month; if they stop using it, the script simply stays unused, with nothing to switch off.
- **Change streams:** Python updates on the computer; nothing else changes and nothing expires.
- **Who handles them:** the person runs the tests after a Python upgrade; an agent may propose fixes, the person approves.
- **Automation:** none; nothing runs unattended.
- **Safety net:** the repository's history; the script never deletes, so a bad run is undone by moving files back.
- **Runbook:** once a month, run the script on the scans folder and glance at the "left in place" list.
- **Tool choice:** no tools to choose; revisit if receipts move to a cloud folder.

## Tasks

| Task | Title | Done by | How | Expected | Status |
|---|---|---|---|---|---|
| T-1 | Sort a folder of sample scans end to end | Claude | Run the script on a test folder of 20 dated sample files | Every file is in its month folder; the count before equals the count after | Not started |
| T-2 | Handle name clashes and unknown files | Claude | Run the tests for clashes and non-PDF files | Clashes get a number; unknown files stay and are listed | Not started |
| T-3 | Person's trial on a copy of real scans (checkpoint) | the person | The person runs the script on a copy of the scans folder | The person confirms the months look right | Not started |

## Progress log

- **Where things stand:** not started
- **Decisions made while building:** none yet
- **Saved for the next checkpoint:** none yet
- **Change requests:** none yet
- **Handoff note:** none yet

## Definition of done

Every task's check passes with evidence; the tests pass; the success measure is met on 200 sample scans. Then the final review.
