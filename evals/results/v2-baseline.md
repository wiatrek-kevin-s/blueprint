# Baseline: Blueprint 2.0.0

Measurements of Blueprint 2.0.0 (the repository's `skill/` before v3) for v3 to compare against.

## Routing (REQ-1)

Blueprint 2 has no routes, so here a prompt that should trigger passes when Blueprint 2 triggers, and a negative passes when it does not (evals/README.md, Scoring). Route accuracy is measured from v3 only.

- **Date:** 2026-11-05
- **Model:** claude-sonnet-5-5 (Claude Code 2.1.318)
- **Mode:** v2 · skill from `origin/main` (5da64fb) · fixtures from `HEAD` (61c2a5f)
- **Runner:** `python3 evals/run_routing.py --mode v2 --max-turns 3`: one `claude -p` process per prompt in a temporary folder outside the clone, with `--setting-sources project`, tools limited to Skill,Read,Glob,Grep,Bash,Write,Edit, no MCP servers, no browser
- **Total:** 38 of 50 passed

| Group | Passed | Of |
|---|---|---|
| new | 8 | 8 |
| resume (new) | 3 | 3 |
| audit | 0 | 8 |
| redesign | 6 | 7 |
| operate | 4 | 7 |
| amend | 3 | 3 |
| none (must not trigger) | 14 | 14 |

| ID | Expected | Result | Detail |
|---|---|---|---|
| new-1 | new | pass | triggered |
| new-2 | new | pass | triggered |
| new-3 | new | pass | triggered |
| new-4 | new | pass | triggered |
| new-5 | new | pass | triggered |
| new-6 | new | pass | triggered |
| new-7 | new | pass | triggered |
| new-8 | new | pass | triggered |
| res-1 | new | pass | triggered |
| res-2 | new | pass | triggered |
| res-3 | new | pass | triggered |
| aud-1 | audit | FAIL | did not trigger |
| aud-2 | audit | FAIL | did not trigger |
| aud-3 | audit | FAIL | did not trigger |
| aud-4 | audit | FAIL | did not trigger |
| aud-5 | audit | FAIL | did not trigger |
| aud-6 | audit | FAIL | did not trigger |
| aud-7 | audit | FAIL | did not trigger |
| aud-8 | audit | FAIL | did not trigger |
| red-1 | redesign | FAIL | did not trigger |
| red-2 | redesign | pass | triggered |
| red-3 | redesign | pass | triggered |
| red-4 | redesign | pass | triggered |
| red-5 | redesign | pass | triggered |
| red-6 | redesign | pass | triggered |
| red-7 | redesign | pass | triggered |
| op-1 | operate | pass | triggered |
| op-2 | operate | FAIL | did not trigger |
| op-3 | operate | FAIL | did not trigger |
| op-4 | operate | pass | triggered |
| op-5 | operate | FAIL | did not trigger |
| op-6 | operate | pass | triggered |
| op-7 | operate | pass | triggered |
| am-1 | amend | pass | triggered |
| am-2 | amend | pass | triggered |
| am-3 | amend | pass | triggered |
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

**Reading:** Blueprint 2 triggers on every new idea, resume and amendment, and on no negative. It never triggers on the audit prompts, because its description excludes existing code ("Not for: writing or fixing code now") and it has no audit route; it misses some redesign and upkeep prompts for the same reason. These are the gaps v3's router and description (T-9) must close without losing the negatives.

Cost reported by Claude Code for this run: about 2.01 USD.
