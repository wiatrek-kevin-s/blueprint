# Audit report: <PROJECT NAME>

<Health check or deep audit> · as of <DATE> · version audited: <commit, tag or upload date> · by Blueprint

Saved in its own folder beside the fix kit's folder, never inside it, and never copied into a project that is or may become public, because it lists the project's weak points; the brief names it as an evidence file marked "keep outside the project", pasted in when the builder asks. Secrets appear by file, line and kind only, never by value.

## Summary

<Five lines at most, in plain words: what the project is today, the top risks named by what could happen to the person (IDs in brackets after the plain name, never alone), how many findings by label, and the recommended next step.>

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

<The confirmed intent statement (G1), the outcome or combined outcomes (such as fix and finish), and where the as-intended or updated spec lives.>

## Standards checklist

<Small health check: the three plain lines the person saw at G2 first, then this table.>

| Item | Source | As of | Met, missed or not applicable |
|---|---|---|---|

## Findings

Problems in the project only; limits of the audit go under "What this audit could not check". Sorted Fix now first, then Fix when convenient, then Accept; within each label, by severity times likelihood, highest first. Status: verified (seen or reproduced) or suspected (inferred). Re-check: the fresh reviewer's result for every "Fix now" finding, or "self-review" without subagents.

| ID | Finding and why it matters | Evidence | Status | Severity | Likelihood | Label | Re-check |
|---|---|---|---|---|---|---|---|
| AF-1 | <plain-words title; why it matters to the person> | <file:line, command and output, or link> | | | | <Fix now, Fix when convenient or Accept> | |

## What this audit could not check

Limits of the audit, not problems in the project, so none of them is in the findings table: commands or tests not run (including any that would write outside the copy), files not read, advisories not looked up, no version history.

- <what, why, and what it would take to check it>

## Recommended fix set

<The findings recommended for the fix kit, each named as in the Summary, with what it protects the person from, and the one-way doors the person decides (at G1 when the request named them, otherwise at G3), each with the recommended answer.>
