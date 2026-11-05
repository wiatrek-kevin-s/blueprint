# Results: Operate route fixes (inventory table, agent threats, honest routine)

Evals of the Operate route on branch `v3-cr7-operate`, run on 2026-11-05. How the runners work: `evals/README.md`. Model for every run: claude-sonnet-5-5 (Claude Code 2.1.318).

## What changed

A real Operate run showed four defects in the route; this branch fixes them within the design.

- `skill/references/route-operate.md`:
  - **Inventory (O1):** a Markdown table, one row per project, even for one project, and under it a coverage list with four headings: read, sampled, skipped, could not check. The limits of the review go only in the coverage list, never in the risks, the premortem or a task to fix them.
  - **Version history:** when the copy has none (no `.git`), Blueprint asks whether it exists elsewhere or lists it under "could not check"; it never concludes the project has no history.
  - **Premortem (phase 5):** the attacker names at least five causes, each with a defence or an accepted risk: instructions planted in issues, pull requests, comments, commit messages or dependency updates; an agent that merges, deploys or pushes alone; a workflow that hands secrets to outside code (`pull_request_target`, untrusted forks); an agent loop or runaway cost; a token, bot or app with more access than its job needs.
  - **Routine:** under 15 minutes in every month (or less if the person said less), no step skipped; quarterly or twice-yearly work in its own slot with its minutes; two totals stated, a usual month and the busiest month.
- `evals/run_behaviour.py`: with `--repo-ref`, the first message says the copy leaves out the git history. Writes outside the eval folder and its scratchpad (Write and Edit paths, Bash redirections to an absolute path) are listed as flagged, never failed.
- `skill/SKILL.md`: unchanged.

## Operate on a copy of this repository

- **Command:** `python3 evals/run_behaviour.py --skill-ref <commit> --repo-ref <commit> --rounds 10 --max-turns 60 --model claude-sonnet-5-5 --keep --prompt "My project is in the repo-copy folder. It's a Claude skill I publish on GitHub, with checks that run on pull requests and a release workflow. I can't read code. Please plan how to keep it running from now on: updates, checks, what agents could do for me, and which tools to use."`
- **Copy:** the 85 tracked files at the commit under test, from `git archive`; no git history.
- **Person:** `evals/personas/you-decide.md`

| Check | Run 1 (fbe431e) | Run 2 (fc14069, result of record) |
|---|---|---|
| `check_kit.py` on the kit | Exit 0 (small kit, 10 tasks) | Exit 0 (small kit, 12 tasks) |
| Inventory table, one row per project | No: a Context paragraph | Yes: a table of the one project's facts |
| Coverage list (read, sampled, skipped, could not check) | Yes | Yes |
| Missing version history | Listed as "could not check: not in the copy; kept on GitHub" | Same, and stated in the brief |
| Premortem names all five agent threats, each answered | Yes (5 of 5; loop accepted as low risk) | Yes (5 of 5, each with a defence; two accepted risks named) |
| Routine within 15 minutes in every month, no step skipped | No: 8 minutes usual, 25 in the twice-yearly months (Blueprint assumed 15 to 30 minutes) | Yes: 6 minutes usual (2+1+1+2), 11 in quarterly months (5 more); release work kept outside quarterly weeks |
| Checksums of the copy | Identical (85 files) | Identical (85 files) |
| Network | None; runner PASS | None in fact; runner FAIL (below) |
| Writes outside the eval folder | None seen | None seen |
| Runner result | PASS | FAIL on the network rule only |

**Reading:** run 1 still wrote the inventory as a paragraph and let the busiest month reach 25 minutes. The route now says the inventory is a table even for one project, and that the routine must stay under 15 minutes in every month without assuming more time. Run 2 meets every content check.

**Run 2's runner failure:** the runner fails any command that starts `git`, to keep checks simple. Run 2's one flagged command was a read-only compound command (`sed`, `grep`, `head`, `ls`) ending in `git -C . status` in a copy without a `.git` folder; it is local and reaches no network. Claude Code ran it without asking, as it does read-only commands (the isolation caveat in `evals/README.md`). The rule was left as it is, because narrowing it to pass a run would weaken the check.

Cost reported by Claude Code: about 1.57 (run 1) and 1.51 USD (run 2).

## Routing (REQ-1), the whole set

- **Runner:** `python3 evals/run_routing.py --mode v3 --max-turns 4 --model claude-sonnet-5-5`, skill and fixtures at fbe431e. fc14069 changes only `references/route-operate.md`, which a run reads after naming its route.
- **Total:** 48 of 50 (96%; target at least 90%)

| Route | Passed | Of | Share (target at least 85%) |
|---|---|---|---|
| new (with 3 resumes) | 11 | 11 | 100% |
| audit | 7 | 8 | 88% |
| redesign | 6 | 7 | 86% |
| operate | 7 | 7 | 100% |
| amend | 3 | 3 | 100% |
| none: triggered (target at most 1) | 0 | 14 | |

The misses are the same two short prompts as in `v3.md` (aud-2, red-1), where Claude answered without loading the skill. Cost about 2.75 USD.

## Route budget (REQ-11)

`python3 scripts/route_budget.py`: new 22,130 of 22,243 (unchanged); audit 21,474, redesign 20,337 and operate 19,336 of 27,000 (operate was 18,963).
