# Execution kit (lite): Club Library

Kit version 1.0 · as of 2026-10-12 · prepared with Blueprint · size: small

Setup: in Claude Code, save this file as CLAUDE.md in an empty project folder. Keep `04-final-review.md` for the end. First message: "Let's start: read the kit, tell me where things stand, and begin."

## Instructions

You are building a small website where book club members see which books others can lend, for a club of about 30 readers, from an agreed plan. Follow it, verify every step, and ask when it doesn't settle something. Don't redesign it, because its decisions have reasons you may not see.

- **Sources:** this file only. The Brief says what and why; the Tasks table is the work; the Progress log says what has happened.
- **Each session:** read the Progress log and the Tasks; check where work was last saved; say in two lines where things stand; do the next tasks in order; update the log as you go.
- **Evidence:** a task is done only when its check passes and the log records a pointer plus one line of result, because an unverified "done" is how builds fail. Never weaken a check to pass it.
- **Saving work:** a private git repository, one commit per task (D-3). Work is saved after every task and any change can be undone. Secrets never go into files or history.
- **The person's steps:** click by click, say what to paste back, and wait.
- **Stop and ask** when the plan can be read two ways, an assumption turns out false, or anything would change a decision, the scope, cost, security or the intent. At most four questions, each with options, the recommended one first. Never ask for passwords or keys; say where to enter them.
- **Never without approval:** publishing the site, spending money, adding scope.
- **Changes:** decide small matters, such as file layout and test data, and log them with the reason. A change to a one-way door is marked "Sent to Blueprint" in the log, and that task pauses.
- **Context:** start a fresh chat when this one grows long, and re-read this file after any compaction.
- **At the end:** offer the final review in a fresh chat, from `04-final-review.md`.

## Brief

> For a book club of about 30 readers, Club Library will show one shared list of books members are willing to lend, so that anyone can find a book and ask its owner in under a minute. We will know it works when every member can find a listed book without asking in the group chat. It must show only first names. It will not track loans or due dates.

The list lives in one spreadsheet the coordinator edits; the site reads it and shows it as a searchable page. A button exports the list as a CSV file. The site is hosted on a free static hosting service (chosen 2026-10-10; its free plan was checked as of 2026-10-10).

| ID | Decision | Choice | Why | Door |
|---|---|---|---|---|
| D-1 | Where the list lives | One shared spreadsheet | The coordinator already edits it weekly | Two-way |
| D-2 | Hosting | A free static hosting service | No running cost and no server to look after | Two-way |
| D-3 | Saving work | Private git repository, one commit per task | Every change can be undone | Two-way |
| D-4 | Who can see it | Anyone with the link; first names only | No sign-in keeps it simple; first names limit what leaks | One-way |

**Rules and examples:** an empty spreadsheet shows "No books listed yet"; two copies of the same title are both shown with their owners; a search for part of a title finds it; a row without an owner's name is skipped and counted at the bottom; the export holds exactly the rows shown.

**Formats that last:** the spreadsheet has the header row Title, Author, Owner first name, Added (ISO 8601 date); the export is UTF-8 CSV with the same header, comma separated, LF line endings.

### Security baseline

No accounts, no secrets in the site, first names only (D-4); the spreadsheet is shared read-only with the site; every other baseline item is not applicable to a static page.

## Tasks

| Task | Title | Done by | How | Expected | Status |
|---|---|---|---|---|---|
| T-1 | Show the list from a sample spreadsheet end to end | Claude | Open the local page with a 10-row sample | All 10 books appear and search finds a title by part of its name | Not started |
| T-2 | CSV export | Claude | Click Export and open the file | The file has the header row and the 10 rows | Not started |
| T-3 | Publish | both | The person connects the hosting account; Claude deploys | The public link shows the list on a phone | Not started |

## Progress log

- **Where things stand:** not started
- **Decisions made while building:** none yet
- **Handoff note:** none yet

## Definition of done

Every task's check passes with evidence; the page works at phone and desktop widths; the success measure is met. Then the final review.
