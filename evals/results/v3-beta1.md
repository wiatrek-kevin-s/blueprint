# Results: Blueprint 3.0.0-beta.1

Evals of the skill released as 3.0.0-beta.1 (main at dd1d354), run on 2026-11-05. How the runners work: `evals/README.md`.

## Routing (REQ-1, new, resume, amend and negatives)

Audit, Redesign and Operate prompts were not run: those routes come in later pre-releases.

- **Date:** 2026-11-05
- **Model:** claude-sonnet-5-5 (Claude Code 2.1.318)
- **Mode:** v3 · skill from `origin/main` (dd1d354) · fixtures from `origin/main` (dd1d354)
- **Runner:** `python3 evals/run_routing.py --mode v3 --max-turns 4`: one `claude -p` process per prompt in a temporary folder outside the clone, with `--setting-sources project`, tools limited to Skill,Read,Glob,Grep,Bash,Write,Edit, no MCP servers, no browser
- **Total:** 28 of 28 passed

| Group | Passed | Of |
|---|---|---|
| new | 8 | 8 |
| resume (new) | 3 | 3 |
| amend | 3 | 3 |
| none (must not trigger) | 14 | 14 |

| ID | Expected | Result | Detail |
|---|---|---|---|
| new-1 | new | pass | route new |
| new-2 | new | pass | route new |
| new-3 | new | pass | route new |
| new-4 | new | pass | route new |
| new-5 | new | pass | route new |
| new-6 | new | pass | route new |
| new-7 | new | pass | route new |
| new-8 | new | pass | route new |
| res-1 | new | pass | route new |
| res-2 | new | pass | route new |
| res-3 | new | pass | route new |
| am-1 | amend | pass | route amend |
| am-2 | amend | pass | route amend |
| am-3 | amend | pass | route amend |
| neg-1 | none | pass | did not trigger |
| neg-2 | none | pass | did not trigger |
| neg-3 | none | pass | did not trigger |
| neg-4 | none | pass | did not trigger |
| neg-5 | none | pass | did not trigger |
| neg-6 | none | pass | did not trigger |
| neg-7 | none | pass | did not trigger |
| neg-8 | none | pass | did not trigger |
| neg-9 | none | pass | did not trigger |
| neg-10 | none | pass | did not trigger |
| neg-11 | none | pass | did not trigger |
| neg-12 | none | pass | did not trigger |
| neg-13 | none | pass | did not trigger |
| neg-14 | none | pass | did not trigger |

**Reading:** every new idea, resume and amendment reached its route and named it; no negative triggered. Earlier runs during development: 27 of 28 on commit 076da1b (one resume used its turns before naming the route; the resume rule now writes the Route line first) and 3 of 3 resumes with 8 turns on 8c6400b, each restating phase 3 and asking its next round without restarting intake (REQ-5).

Cost reported by Claude Code for this run: about 1.31 USD.

## End to end (REQ-4, small kit)

- **Command:** `python3 evals/run_behaviour.py --skill-ref origin/main --prompt "I have an idea for a small script that emails me every Sunday with a list of which of my houseplants need watering that week, based on a simple list of plants I keep. Can you help me plan it?"`
- **Person:** `evals/personas/you-decide.md`
- **Model:** claude-sonnet-5-5 (Claude Code 2.1.318)
- **Result:** pass. Route named: new. Blueprint wrote a small kit (`kit-lite.md`, `04-final-review.md`, 6 tasks) after 4 replies from the person. `check_kit.py` exit 0, also with `--coded`; "Keeping it running" has 7 lines: owner and time, a weekly heartbeat email, what expires (the mail app password) with a reminder date, updates, data changes, no unattended agents, a review after one month.
- **Cost reported by Claude Code:** about 1.47 USD.
