# Phase 2: landscape

Goal: teach the decisions this kind of project forces before asking anything, because the person can't ask about a decision they don't know exists. Outputs: a primer, a decision map with one-way doors marked, and assumptions, all in the state file.

## Research

Follow `references/04-research.md`. Cover two to four standard ways such projects are built; three to five comparable projects, with what they had to decide and what they later rewrote or regretted; and what changed in the last year (versions, prices, laws).

## Calibrate, then write the primer

Record the person's familiarity with each area (new / used it / knows it well); for technical areas, assume "new" unless they say otherwise, because a primer pitched too high fails silently while one pitched low costs a skim.

Write the primer from `templates/primer.md`: one page for medium and large projects, five to eight lines in chat for small ones. Take its terms from `references/glossary.md`, at most ten, because one wording everywhere keeps terms from reading as new things. Ask the person to mark anything new, surprising or wrong; the marks feed phase 3.

## Decision map

List every decision the project forces, not only the person's. Draw on: comparable projects (a rewrite or regret marks a one-way door); what a senior architect, security reviewer, designer, finance or legal person would ask first; each "must" and "will not" in the intent; and a premortem ("a year on we rewrote a major part; what was it?", answered three times).

Check every project against these seams: data and storage; integrations and extensibility (who controls what gets added later); identity and access; deployment; scale; failure and recovery; change over time; cost and licences; compliance and policy; ownership and maintenance; experience and interface; how work is saved; and the **execution environment** (a Claude project, Claude Code with a repository, or steps the person does on a platform), which is a one-way door decided before the kit. Business plans add customer, value, pricing, channels, legal structure and funding. List seams that don't apply in one line under the map.

**Coded projects:** run `references/non-coder-checklist.md` against the map, as far as the size allows (`SKILL.md`, budgets). Each item ends as a decision row, a "not applicable" entry in one line, or a risk the person accepts, because an unlisted item becomes the builder's guess.

### Doors

A decision is a **one-way door** if reversing it means rewriting a core part, migrating stored data, breaking a shared format or link, renegotiating a licence or contract, or retraining users. One-way doors get options, a recommendation and the person's choice in phase 3. Two-way doors get a stated default. Don't plan "start with X, replace it later" for a one-way door, because "later" is the rewrite.

## Assumptions

Log each assumption with its confidence, evidence, cost if wrong and how to check it. Check the costly, low-confidence ones first, by research or in phase 3.

## Gate G2

The person has seen the primer and could mark it; every seam is checked; one-way doors marked; assumptions logged. Save the state file.
