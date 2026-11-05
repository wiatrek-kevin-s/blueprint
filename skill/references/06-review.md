# Phase 5: review

Goal: catch what is wrong or missing before the kit leaves (G4: no unresolved "fail"). A fail sends work back to the phase that caused it.

Run every review in a fresh context: a subagent that sees only the documents named, else a new chat the person opens, else a labelled self-review (`SKILL.md`, capability check). Reviewers who saw the reasoning inherit its blind spots.

## Premortem

"A year from now this failed or needed a major amendment. Why?" Answer as four people: the **user**, the **operator** who runs it, an **attacker**, and the **maintainer** who changes it later. Rank the causes by likelihood, because a lone reviewer invents threats. Fail if a cause points to a one-way door missing from the decision map, or to a costly unchecked assumption.

## Fresh-reader test

Give a fresh agent only the design: "Without asking anyone: what is built, for whom, the first three things you'd build, how you'd know each works, and every guess you'd have to make." Fail if the answers differ from the intent or milestones, or a guess touches a one-way door.

## Completeness check

Walk the checks in `scripts/check_kit.py` by hand on the design now; run the script on the kit in phase 6.

## Findings

Each finding is **fail** (the build would go wrong), **warn** (a real risk) or **info**. Act only on fail and warn findings that name a concrete consequence, because reviewers always find something and vague findings waste a round. Show the person one table: review, finding, level, action.

## Dry run of the kit (phase 6)

Give a fresh agent only the kit folder: "You are starting this project. What do you do first, what will you ask, where do you stop, and where is work saved? List every guess you'd have to make. Mark it one-way if it is hard to reverse once in use (platform, hosting, how data is stored or shaped, accounts and sign-in, personal data or payments, licence, anything public, anything that costs money), and harmful if a wrong answer would lose data, open a security or privacy hole, cost money, create a legal duty or fix a public name." Also ask it to list:

- every contradiction between kit files (X-4), because two sources for one fact will drift;
- every acceptance check it couldn't run, and why (X-5), because a check the builder can't run proves nothing.

Close every harmful one-way guess, contradiction and unrunnable check: decide it with a reason, or ask the person in the approval message if only they can. Close other one-way guesses the same way when cheap, because they still cost a migration. Small projects get one dry run; medium and large dry-run again with a new agent, up to three runs in all, until no harmful one-way guess is left, because each fix adds text a builder can misread. For two-way guesses, widen the brief's "decide yourself" list instead of writing each one out.
