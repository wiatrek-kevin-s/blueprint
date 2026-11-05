# Blueprint state: Shift Board

Keep in the Blueprint project; a new chat resumes from it. Updated 2026-10-28.

- **Type · size · appetite:** web app · medium (holds volunteers' names and phone numbers, so account choices are one-way) · about 6 weeks of evenings
- **Calibration:** web apps: new; hosting: new; volunteer scheduling: knows it well
- **Tools and fallbacks:** web search yes; subagents yes; code yes; files yes; artifacts yes
- **Phase:** 3 · **Gates:** G1 2026-10-21, G2 2026-10-27
- **Outcome:** build
- **Idea brief:** none (the idea was clear at intake)
- **Design direction:** none yet (step 3D comes after G3)
- **Execution:** not decided yet (D-1 open) · saved in not decided · check-ins weekly
- **Readiness:** not started · **Kit version:** none
- **Artifacts:** primer (in this project, primer.md); decision map below
- **Next step:** question round 2 of phase 3: sign-in method (D-3) and where the data lives (D-4)

## Intent (G1)

> For volunteer coordinators of small community groups, who fill weekly shifts by phone and group chat, Shift Board will let volunteers see open shifts and claim one in under a minute, so that no shift goes unfilled without the coordinator knowing a day ahead. We will know it works when a coordinator fills a week of shifts without a single phone call. It must keep volunteers' phone numbers visible only to coordinators. It will not handle payments or payroll.

## Research summary

Chat files don't reach a new chat, so findings live here.

- Similar tools: several hosted shift schedulers exist, most priced per volunteer per month; none offers a free tier for groups over 15 people (web search, 2026-10-25).
- Sign-in: magic links by email are the simplest for volunteers who forget passwords; they need a reliable email-sending service (provider documentation, 2026-10-26).
- Text messages cost money per message in every provider checked (provider pricing pages, 2026-10-26).

## Homework

| ID | What only the person can provide | How to get it | Needed by | Status |
|---|---|---|---|---|
| H-1 | How many volunteers and shifts a typical week has | Count last month's rota | Phase 3 | Received: about 40 volunteers, 25 shifts a week |

## Decision map

Decide one-way doors before drafting; give two-way doors a default the person can override. Open rows are the open questions.

| ID | Seam | Decision | Options | Recommendation, why | Door | Confirmed or assumed | Decide by | Decided by | Status |
|---|---|---|---|---|---|---|---|---|---|
| D-1 | Execution environment | Where the build happens | Claude Code; Claude project | Claude Code, because the app needs a repository and tests | One-way | | Before the kit | | Open |
| D-2 | Notifications | How volunteers hear about open shifts | Email; text message; none | Email, because text messages cost money per message | Two-way | Confirmed | G3 | The person, round 1 | Decided |
| D-3 | Sign-in | How volunteers sign in | Magic link; password; none | Magic link, because volunteers forget passwords | One-way | | G3 | | Open |
| D-4 | Data | Where volunteer data lives | Managed database; spreadsheet | Managed database, because phone numbers need access rules | One-way | | G3 | | Open |

Not applicable: payments, public interfaces for other developers.

### D-2: How volunteers hear about open shifts

Status: accepted · 2026-10-28 · two-way · decided by the person in round 1. Email only; text messages can be added later if the group pays for them.

## Assumption register

Check important, unsure ones first.

| ID | Assumption | Confidence (H/M/L) | Evidence | Cost if wrong | How to check | Status |
|---|---|---|---|---|---|---|
| A-1 | Every volunteer has an email address they check weekly | M | The coordinator's estimate | Some volunteers miss shifts | Ask the group | Unchecked |
