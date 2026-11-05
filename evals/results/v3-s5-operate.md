# Results: Operate route (session 5)

Evals of the Operate route on branch `v3-s5-operate`, run on 2026-11-05. How the runners work: `evals/README.md`.

## What changed

- `skill/references/route-operate.md`: phases O0 to O4 with gates G1 to G3, held before any recommendation; read-only rules that also cover live systems (settings, rulesets, secrets, workflows); options researched at run time with dates, never from a stored list; agents propose and the person approves; the operations kit uses the shared kit layout, with setup tasks, a premortem under the brief's security baseline, and a runbook under 15 minutes a month.
- `skill/SKILL.md`: the Operate row and the file index point to the route file. Redesign still says "Coming in a later release".
- `scripts/route_budget.py`: Operate counts the files its phase rows name.
- `evals/run_behaviour.py`: `--repo-ref` copies this repository's tracked files in as `repo-copy/`; every run lists the commands and web tools it used and fails on network use; the kit search skips the project copy.

## Operate on a copy of this repository (REQ-7, REQ-9)

- **Command:** `python3 evals/run_behaviour.py --skill-ref HEAD --repo-ref HEAD --rounds 10 --max-turns 60 --model claude-sonnet-5-5 --keep --prompt "My project is in the repo-copy folder. It's a Claude skill I publish on GitHub, with checks that run on pull requests and a release workflow. I can't read code. Please plan how to keep it running from now on: updates, checks, what agents could do for me, and which tools to use."`
- **Copy:** the 82 tracked files at the commit under test, from `git archive`; no `CLAUDE.md`, no planning notes, no terms file, no git history. The runner refuses to start if any of those reach the copy.
- **Person:** `evals/personas/you-decide.md`
- **Model:** claude-sonnet-5-5 (Claude Code 2.1.318). No web tool is on the allowlist, so every tool fact in the kits is marked unverified, with a task that confirms it.

Replies are numbered from 0, the first Blueprint reply.

| Run | Skill | G1 and G2 | Kit | `check_kit.py` | Premortem names planted instructions | Existing setup checked first | Checksums | Network |
|---|---|---|---|---|---|---|---|---|
| 1 | 7027bad | Reply 0, then waited | Reply 1, `kit-lite.md` and `04-final-review.md` | Exit 0 by hand; runner FAIL (it took a fixture kit inside `repo-copy/`) | No premortem written | No: re-creates a ruleset it could not see | Identical (82 files) | None; runner FAIL (words inside a heredoc that wrote the kit) |
| 2 | 0c98fbf | Reply 0, then waited | Reply 1 | Exit 0 | Yes, cause 4 of 7 | Yes (T-1 records, T-2 keeps what meets D-3) | Identical (82 files) | None; runner FAIL (paths such as `./.git`) |
| 3 | 3fdee4c | Reply 0, then waited | Reply 1; approved and handed over in reply 2 | Exit 0 (also with `--coded`); runner PASS | Yes, cause 1 of 7 | Yes (T-1 records; T-3 and T-5 skip what exists) | Identical (82 files) | None; runner PASS |

**Reading:** run 1 showed one route defect and two runner defects. The route reviewed its kit without writing the premortem down, and planned to create settings it could not see. `route-operate.md` now writes the ranked premortem under the brief's security baseline, and setup tasks for unseen settings first record what exists. The runner now skips the project copy when it looks for the kit, ignores the body of a heredoc that only writes a file, and matches network programs only where a command starts. Every command of all three runs was re-checked with the final runner: no web tool and no network command. Run 3 is the result of record; run 2 meets the same checks.

### Setup in the kit compared with what session 1 built (run 3)

| What session 1 built | Run 3's kit | Difference and the kit's reason |
|---|---|---|
| `ci.yml`: job `ci` on pull requests and pushes to `main`, read-only, `pull_request` event, steps skipped until their inputs exist | Kept and described in the brief's Context. T-7 makes the skipped steps fail | The inputs now exist, so a skip would hide a deleted check (premortem cause 4) |
| `release.yml`: publishes on a version tag, manual runs are dry runs, write access only in the publish job | Kept; T-9 rehearses a dry run | Adds D-3, a tag ruleset limiting `v*` tags to the owner, because whoever pushes a matching tag publishes (cause 2). Session 1 has no tag rule |
| Ruleset on `main`: pull request and `ci` required, force pushes and deletion blocked, 0 approvals | D-2: pull request and `ci` required, force pushes blocked, no bypass, no reviewer count | Same rule. The kit could not see settings, so T-1 records what exists and T-5 adds only what is missing, which keeps session 1's deletion block |
| Private-terms check: `scripts/check_private.py` run locally before every push; the CI step reads a secret the owner chose not to add, so it reports skipped | D-4 keeps the secret out of outside code; T-1 records whether it is present | The kit assumes the secret exists, because the copy cannot show settings. It records the answer in T-1 but does not say what to do when the secret is absent; the owner's choice to rely on the local check would come up there |
| Action pins reviewed by hand every 6 months | D-5: Dependabot proposes updates monthly, at most 3 pull requests; the owner merges | Replaces the manual review with proposals the owner approves (cause 1 in run 2) |
| Secret scanning and push protection turned on by the owner | T-3 turns them on, skipping any already on | Same; checked first |

New in the kit, with no session 1 counterpart: `MAINTENANCE.md` with the monthly routine and the agent prompt; email alerts; the runbook (about 15 minutes a month); a cost cap of 0 USD beyond the owner's plan.

Cost reported by Claude Code: about 1.37 (run 1), 0.81 (run 2) and 1.42 USD (run 3).

## Routing (REQ-1)

- **Skill:** 7027bad. Later commits change only `references/route-operate.md`, which a run reads after naming its route, and the runner.
- **Runner:** `python3 evals/run_routing.py --mode v3 --max-turns 4 --model claude-sonnet-5-5 --ids <every prompt except redesign>`
- **Total:** 43 of 43 passed

| Group | Passed | Of |
|---|---|---|
| new | 8 | 8 |
| resume (new) | 3 | 3 |
| audit | 8 | 8 |
| operate | 7 | 7 |
| amend | 3 | 3 |
| none (must not trigger) | 14 | 14 |

Cost reported by Claude Code: about 2.40 USD.

## Route budget (REQ-11)

`python3 scripts/route_budget.py`: new 22,154 of 22,243 (was 22,144); audit 21,498 of 27,000; operate 18,987 of 27,000.
