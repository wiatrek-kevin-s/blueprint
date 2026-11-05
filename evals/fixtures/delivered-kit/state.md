# Blueprint state: Club Library

Keep in the Blueprint project; a new chat resumes from it. Updated 2026-10-12.

- **Type · size · appetite:** website · small (one page, no accounts) · two weekends
- **Calibration:** websites: used it; hosting: new
- **Tools and fallbacks:** web search yes; subagents yes; code yes; files yes; artifacts yes
- **Phase:** delivered · **Gates:** G1 2026-10-05, G2 2026-10-07, G3 2026-10-09, G4 2026-10-11, G5 2026-10-12
- **Outcome:** build
- **Idea brief:** none
- **Design direction:** the club's existing colours, plain list layout
- **Execution:** Claude Code · saved in a private git repository · check-ins after each task
- **Readiness:** check_kit 2026-10-12 passed; one dry run, no one-way guesses; approved 2026-10-12 · **Kit version:** 1.0
- **Artifacts:** kit-lite.md and 04-final-review.md in this folder
- **Next step:** build from the kit; amend it here if something changes

## Intent (G1)

> For a book club of about 30 readers, Club Library will show one shared list of books members are willing to lend, so that anyone can find a book and ask its owner in under a minute.

## Decision map

| ID | Seam | Decision | Options | Recommendation, why | Door | Confirmed or assumed | Decide by | Decided by | Status |
|---|---|---|---|---|---|---|---|---|---|
| D-1 | Data | Where the list lives | Spreadsheet; database | Spreadsheet, already edited weekly | Two-way | Confirmed | G3 | The person | Decided |
| D-2 | Hosting | Where the site runs | Free static host; paid host | Free static host, no running cost | Two-way | Confirmed | G3 | Delegated, Claude's choice | Decided |
| D-3 | Execution environment | Where the build happens | Claude Code; Claude project | Claude Code, the site needs a repository | One-way | Confirmed | Before the kit | The person | Decided |
| D-4 | Privacy | Who can see the list | Link only, first names; sign-in | Link only, first names, simplest | One-way | Confirmed | G3 | The person | Decided |
