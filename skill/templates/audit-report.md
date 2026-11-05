# Audit report: <PROJECT NAME>

<Health check or deep audit> · as of <DATE> · version audited: <commit, tag or upload date> · by Blueprint

Kept outside the project folder. Secrets appear by file, line and kind only, never by value.

## Summary

<Five lines at most, in plain words: what the project is today, the top risks, how many findings by label, and the recommended next step.>

## As-built summary

<What exists and what it does today: structure, stack and versions, entry points, data stores, outside services, tests, CI, documents.>

## Coverage

What the audit read, sampled or skipped, so nothing unread passes as checked.

| Area or path | Read, sampled or skipped | Reason |
|---|---|---|

| Command or test | Where it ran | Run or not run | Result or reason |
|---|---|---|---|
| <such as the test command> | <temporary copy> | <run> | <passed 12, failed 2> |

## Intent and spec

<The confirmed intent statement (G1), the outcome, and where the as-intended or updated spec lives.>

## Standards checklist

| Item | Source | As of | Met, missed or not applicable |
|---|---|---|---|

## Findings

Sorted by severity times likelihood, highest first. Status: verified (seen or reproduced) or suspected (inferred). Re-check: the fresh reviewer's result for every "Fix now" finding.

| ID | Finding and why it matters | Evidence | Status | Severity | Likelihood | Label | Re-check |
|---|---|---|---|---|---|---|---|
| AF-1 | | <file:line, command and output, or link> | | | | <Fix now, Fix when convenient or Accept> | |

## Not checked or could not verify

- <what, and why>

## Recommended fix set

<The findings recommended for the fix kit, by ID, and the one-way doors the person decides at G3.>
