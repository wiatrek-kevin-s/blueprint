# Final review: Receipt Sorter

## Who runs it and when

One sceptical reviewer in a fresh chat, after every task is done. Read the kit and the progress log, then use the product. You fix nothing: you report, and the person decides.

## Run the product

1. Run every acceptance check in the task list; note any that fail now.
2. Run the tests and a secret scan of the repository.
3. Negative tests: an empty input folder, a file that isn't what it claims to be, and running the same command twice.

Record what you ran and each result, because a review that ran nothing is only opinion.

## Lenses

Correctness, failure handling and maintainability. Also: does it serve the intent and meet each success measure?

## Scoring

Only findings with a concrete harm scenario count. Score severity and likelihood from 1 to 10 each; priority is severity times likelihood.

| Priority | Label |
|---|---|
| 40 or more, or severity 9+ with likelihood 3+ | Fix now |
| 20 to 39 | Fix when convenient |
| Under 20 | Accept |

## What the person sees

- Three lines: the verdict, the worst risk, and what you recommend.
- One table of findings with harm scenario, severity, likelihood, priority, label and suggested fix.
- The recommended fix set, for the person to approve or change.

## After the review

The fixes the person chooses become R-n tasks, done like any task, with evidence. One targeted re-check in a fresh context follows.
