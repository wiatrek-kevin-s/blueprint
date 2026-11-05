# Final review: <PROJECT NAME>

## Who runs it and when

One sceptical reviewer in a fresh chat, after every task is done. You didn't build this, so you see what the builder stopped seeing. Read the brief, the design spec if any, and the progress log; then use the product. You fix nothing: you report, and the person decides.

<Large projects, optional: first a blind pass by a reviewer given only the deliverables, in a separate folder or chat outside the project, so it judges what was made, not what was meant.>

## Run the product

1. Run every acceptance check in the task list; note any that fail now.
2. Run the automated audits the brief names: <tests, linter, secret scan, dependency audit, accessibility audit>.
3. For web interfaces, run browser tests of each main flow at 375 and 1,280 px wide.
4. Negative tests: the wrong user (open another user's data), bad input (empty, huge, malformed), no network or a failing service, and repeated actions (double submit).
5. For coded projects, confirm each security baseline item marked applied.

Record what you ran and each result, because a review that ran nothing is only opinion.

## Lenses

<The lenses for this type, such as security, correctness, failure handling and maintainability.> Also: does it serve the intent and meet each success measure?

## Scoring

Only findings with a concrete harm scenario count: who is hurt, how, and what triggers it. Score severity and likelihood from 1 to 10 each; priority is severity × likelihood.

| Priority | Label |
|---|---|
| 40 or more, or severity 9+ with likelihood 3+ | Fix now |
| 20 to 39 | Fix when convenient |
| Under 20 | Accept |

Severity guide: 10 data lost or leaked, or money lost; 7 a main flow broken; 4 a workaround needed; 1 cosmetic. Likelihood guide: 10 every user, every time; 5 some users, often; 1 rare and unusual.

## What the person sees

- Three lines: the verdict, the worst risk, and what you recommend.
- One table:

| # | Finding | Harm scenario | Severity | Likelihood | Priority | Label | Suggested fix |
|---|---|---|---|---|---|---|---|

- The recommended fix set: every fix-now finding, plus any cheap fix-when-convenient ones, for the person to approve or change.

## After the review

The fixes the person chooses become `R-n` tasks, done like any task, with evidence. Then one targeted re-check in a fresh context, of those fixes only, confirms each one and that nothing next to it broke.
