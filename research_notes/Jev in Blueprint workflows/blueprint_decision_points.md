# Blueprint's architecture, constraints and decision points: where a typed "decision model" (Jev) could plug in

Scope: primary-source reading of the local repository `/home/user/blueprint` (HEAD `88d0e8b`, "Blueprint 3.2.1: trim pass"). Nothing was modified. All "sources" below are repository files cited as `path:line`; line numbers were taken from each file read on its own with `cat -n`. "Jev" facts (System One model, typed questions in, typed answers with calibrated probabilities out, ~70–500 ms, cheap, no text generation or multi-step reasoning) come from the assignment brief, not from this repository; the repository never mentions Jev, TypeSafe AI, or any decision/classifier model.

Shape test used throughout: a decision point is **Jev-shaped** if the question can be posed as a typed question (bool / enum / number) over state that already exists in a structured or readable form, and the answer needs no generated prose and no multi-step research. It is **partly Jev-shaped** if a typed sub-decision exists but the surrounding step needs generation, research or the person. It is **not Jev-shaped** if the step's output is prose, a plan, research, or a conversation.

---

## 1. What Blueprint is and how it runs

### Takeaway
Blueprint is a pure-instructions Claude skill (Markdown references and templates plus two standard-library Python check scripts) that Claude itself executes inside the Claude app or Claude Code; it plans and hands over an "execution kit" for a separate builder agent, and has no runtime of its own, no API calls and no model of its own. Every "decision" in it is currently made by the host Claude model reading Markdown rules, or by deterministic Python checks.

### Cited Findings
- Blueprint "plans projects at any stage … and hands over an **execution kit**: a few documents a fresh agent … builds from without guessing. Every kit also says how the result is kept running." — [skill/SKILL.md:9](skill/SKILL.md)
- README: "Blueprint plans; it never builds or edits the project itself." Written "for people who may not code and can't judge security, good practice or technical choices on their own"; "asks only about choices that are hard to undo, and decides the rest with a stated reason." — [README.md:3-5](README.md)
- Runtime surfaces: Claude app (web, desktop, mobile) via uploaded `blueprint.zip`, which requires "code execution and file creation" on; Claude Code via `~/.claude/skills/blueprint/` or `.claude/skills/blueprint/`. — [README.md:45-60](README.md)
- The zip holds only `skill/`: "`SKILL.md`, the route and phase references, the templates, and the kit and task-list checks in `skill/scripts/`. This is the only folder the zip holds." `evals/` and `scripts/` are repo-only. — [README.md:62-69](README.md); "Nothing here ships in the skill zip." — [evals/README.md:3](evals/README.md)
- Capability check at intake records "web search, subagents, code execution, file output, the artifact types it can publish, and design systems" and picks fallbacks ("no code execution → walk the scripts' checklists by hand; no web search → state what couldn't be verified"). — [skill/SKILL.md:30-32](skill/SKILL.md)
- **Five routes** (table): New ("A new idea, or a repository with nothing in it yet"), Audit, Redesign ("only its look and feel should change"), Operate ("upkeep: updates, fixes, automation, or a choice of tools"), Amend ("A delivered Blueprint kit needs a change"). — [skill/SKILL.md:34-44](skill/SKILL.md)
- Route selection is an ordered rule list: state file → resume; delivered kit + change or stuck build → Amend; nothing exists → New; something exists → by what the person wants; two fit → the one named first, offer the other at the first gate; "Nothing fits clearly … ask one question naming the five routes in plain words." Switch route "only at a gate, with the person's agreement". — [skill/SKILL.md:46-55](skill/SKILL.md)
- **Phases** for New: 0 Intake → E Explore → 1 Intent (G1) → 2 Landscape (G2) → 3 Decide (G3) → 3D Design direction → 4 Design → 5 Review (G4: "no unresolved 'fail' finding") → 6 Kit (G5: "readiness check passed; the person approves; kit delivered"). Audit/Redesign/Operate run their own first phases and join at phase 4 (Redesign at 3D). — [skill/SKILL.md:59-73](skill/SKILL.md)
- **Lightning mode** (route New only): "ask nothing, assume every answer, write the kit, check it, and send one message at the end"; one-way doors "take the safe default: private, not public or indexed; every account … in the person's own name; payments in test mode only; nothing published or deployed live …". — [skill/references/lightning.md:3](skill/references/lightning.md), [lightning.md:27](skill/references/lightning.md)
- Lightning "Build hand-off" is "Rule 10's one exception, at the person's request": on "build it" in Claude Code, Blueprint places the kit (`CLAUDE.md` + `docs/`) and tells the person to `/clear` and send "Continue the build". — [skill/references/lightning.md:56-60](skill/references/lightning.md)
- Sizing table (small/medium/large) sets question rounds (1–2 / 2–4 / 3–6), total questions (10 / 20 / 35), kit shape (small: `project-instructions.md` <700 words + `kit-lite.md` <3,000; medium/large: full kit, brief <8,000 words or in parts). Anything holding other people's accounts or personal data "is at least medium". — [skill/SKILL.md:75-90](skill/SKILL.md)
- **Kit files** (medium/large): `START-HERE.md`, `project-instructions.md` (renamed `CLAUDE.md` in Claude Code), `build-brief.md`, `progress-log.md`, `tasks.json`, `final-review.md`, `design-spec.md`. — [skill/references/07-handoff-kit.md:9-19](skill/references/07-handoff-kit.md)
- **Coordinator/worker builder model** in the kit: "You coordinate; workers build." Hand out each ready task (respecting `depends_on`) to a fresh worker subagent; "**Verify** by running its checks yourself; a worker's 'done' is a claim. Read output, not code."; replace a worker that "is done, runs long or fails twice"; if the second attempt fails, "mark the task blocked, continue, and raise it at the next checkpoint with a recommended answer." — [skill/templates/kit-01-project-instructions.md:32-37](skill/templates/kit-01-project-instructions.md); mirrored planner-side in [skill/references/context-and-agents.md:36-43](skill/references/context-and-agents.md)
- `tasks.json` schema: `id`, `title`, `session`, `depends_on`, `done_by` (claude/person/both), `delivers` (REQ-n/AF-n), `acceptance` [{`how`, `expected`}], `status` (todo/in_progress/blocked/done), `evidence`. — [skill/templates/kit-tasks.json:1-45](skill/templates/kit-tasks.json); enums at [skill/scripts/check_tasks.py:25-30](skill/scripts/check_tasks.py)
- Builder "When to stop and ask": checkpoints, a stop list ("publishing or deploying, spending or signing up, deleting or overwriting data or history, sending messages, adding scope"), homework, and "a change touching a one-way door (… mark it 'Sent to Blueprint')". "Decide everything else within the plan and log it." — [skill/templates/kit-01-project-instructions.md:61-70](skill/templates/kit-01-project-instructions.md)
- Progress log has typed-ish tables: Tasks, Decisions ("Asked or decided"), Change requests with "Status: raised, approved, declined, or Sent to Blueprint". — [skill/templates/kit-03-progress-log.md:13-30](skill/templates/kit-03-progress-log.md)
- Context discipline: "Research, drafting long documents …, reviews and dry runs go to fresh subagents, never forks of this chat". — [skill/SKILL.md:96](skill/SKILL.md)

### Inferences
- Because the shipped skill is Markdown executed by the host model, there is no Blueprint "process" that could call Jev on its own; any Jev call inside a Blueprint run would have to be a tool call (Bash/`python3`, or an MCP connector) made by Claude during the conversation. In the Claude app this depends on code execution having network egress; in Claude Code it depends on permissions.
- The kit's builder (coordinator + workers) is a separate runtime the person owns after hand-off. It is a more natural home for a typed verification/triage call than the planner, because it runs long, repeats the same typed judgments per task, and already has a machine-readable state (`tasks.json`).

### Gaps
- The repository does not say whether Claude-app code execution has outbound network access; that determines whether a skill-side Jev call is even possible on that surface.

---

## 2. Hard constraints relevant to adding an external API (block or shape a Jev integration)

### Takeaway
Several of Blueprint's rules would block a Jev call in the shipped planner by default (privacy of the person's project, no keys in chat, ask before network on the project's behalf, standard-library scripts, token budgets, "never take options from a list stored in this skill") and strongly shape any "use Jev" advice to users (must be researched at run time with "as of" dates, boring-technology bias, account in the person's name, AI security baseline). The least-constrained place is the repository's own eval harness, which is not shipped and already calls a paid model.

### Cited Findings
**Plans, never builds; network and live services**
- Rule 10: "Never build or change the project … In Audit, Redesign and Operate you may read it and run commands that write nothing outside a temporary copy; ask before anything that touches live data, live services or the network on the project's behalf." — [skill/SKILL.md:24](skill/SKILL.md)
- Read-only rule: "Ask before anything that touches live data, live services or accounts, or uses the network on the project's behalf, installing dependencies included. … Looking up public data by name (advisories, versions, licences, a tool's documentation and prices) is research … not acting on the project's behalf." — [skill/references/existing-projects.md:25](skill/references/existing-projects.md); same in [README.md:19](README.md)
- Operate: "Never change a live system … Ask before reading live data, accounts or services too". — [skill/references/route-operate.md:26-27](skill/references/route-operate.md)
- Behaviour evals fail a run "on any network command in Bash (`curl`, `wget`, `gh`, `git`, `ssh`, `pip`, `npm` or a Python network module, which covers every install)" and on WebFetch to non-public hosts; only `PUBLIC_DATA_HOSTS` such as `pypi.org`, `osv.dev`, `github.com` are allowed. — [evals/README.md:125](evals/README.md)

**Privacy**
- Rule 6: "Nothing private goes into documents meant to be public, because a kit is often shared or published and can't be recalled." — [skill/SKILL.md:21](skill/SKILL.md)
- Secrets: "Report a secret by file, line and kind only. Never copy its value into the report, the state file, the chat or a command line". — [skill/references/existing-projects.md:28](skill/references/existing-projects.md)
- Repo-level privacy check `scripts/check_private.py`: whole-word, case-insensitive match of private terms (from `.private-terms` or the `PRIVATE_TERMS` secret) across tracked files, zips and commit messages; "never prints a term or the text of a matching line, because the output can land in a public CI log". — [scripts/check_private.py:1-40](scripts/check_private.py); monthly check step 0 in [README.md:98](README.md)
- Eval results: "Never transcripts of private runs." "Every prompt and fixture is invented and generic." — [evals/README.md:16-18](evals/README.md)

**Keys and accounts**
- Rule 9: "Never ask for passwords or keys, because a chat is not a safe place for them; tell the person where to enter them instead." — [skill/SKILL.md:23](skill/SKILL.md); lightning: "Never assumed: passwords, keys and account sign-ups." — [skill/references/lightning.md:32](skill/references/lightning.md)
- Account ownership one-way item: "Every account (domain, hosting, database, payments, code host, AI provider) is in the person's name … Whoever holds the accounts owns the product." — [skill/references/non-coder-checklist.md:16](skill/references/non-coder-checklist.md)

**Standard-library-only scripts**
- `check_kit.py`: "Python 3 standard library only. Where code can't run, walk the same list by hand." — [skill/scripts/check_kit.py:55](skill/scripts/check_kit.py); `check_tasks.py` same — [skill/scripts/check_tasks.py:19](skill/scripts/check_tasks.py); `route_budget.py` same — [scripts/route_budget.py:137](scripts/route_budget.py). Imports in all scripts and eval runners are stdlib only (json, re, os, sys, subprocess, argparse, …). "The checks need bash and Python 3 only". — [README.md:75](README.md)

**Token budgets**
- Per-route limits: "new at most 25,000 tokens …; SKILL.md alone at most 4,200; audit, redesign, operate and lightning at most 27,000 each." Tokens = chars/4. Purpose: "a regression guard against drift back to bloat". — [scripts/route_budget.py:15-26](scripts/route_budget.py), [route_budget.py:130-135](scripts/route_budget.py)
- Current headroom: Route New reads 23,462 tokens (3.2.1), SKILL.md 3,692 — [CHANGELOG.md:8-10](CHANGELOG.md); earlier "24,819 of 25,000; SKILL.md is 4,009 of 4,200" — [CHANGELOG.md:39](CHANGELOG.md). Files read only on demand (heuristics, writing rules, subagent briefs) "are not counted". — [scripts/route_budget.py:34-36](scripts/route_budget.py)

**Audience, plain words, AI credit lines**
- Rule 11: "Assume the person can't review code: own the security, privacy, cost and accessibility calls and explain each in one line". — [skill/SKILL.md:25](skill/SKILL.md)
- Ask only what a non-coder can answer; "never how the code or its tools work. Find technical facts yourself." — [skill/references/existing-projects.md:14](skill/references/existing-projects.md)
- AI credit lines off by default: kits set `"attribution": {"commit": "", "pr": "", "sessionUrl": false}` unless the person chose credit lines. — [skill/templates/kit-02-build-brief.md:63](skill/templates/kit-02-build-brief.md); [README.md:27](README.md); [skill/references/route-operate.md:81](skill/references/route-operate.md)

**Choosing third-party services or vendors for users' projects**
- Research rules: "Look up anything that can change (versions, prices, limits, licences …) however familiar it seems"; "Prefer primary sources"; "Write 'as of YYYY-MM-DD' beside every current-state fact"; "Label opinion, inference, vendor benchmarks and single-author claims"; "Seek the strongest case against each recommendation before adopting it." — [skill/references/04-research.md:7-14](skill/references/04-research.md)
- Tool choice: "compare current options with the tools the person already uses, researched now with an 'as of' date … Never take the options from a list stored in this skill, because products and their limits change monthly." — [skill/references/keeping-it-running.md:15](skill/references/keeping-it-running.md); Operate repeats "Never take the options or their facts from a list stored in this skill". — [skill/references/route-operate.md:57](skill/references/route-operate.md)
- "Choose boring technology: well-known stacks for non-coders and AI builders alike." — [skill/SKILL.md:118](skill/SKILL.md); heuristic: "Pick stacks the builder knows well; justify each new one … Count the joins between tools, not novelty". — [skill/references/heuristics.md:19](skill/references/heuristics.md)
- Default stacks table (dated "as of 2026-11-03", re-research if over six months old) lists no AI/model vendor at all. — [skill/references/software-design-detail.md:26-36](skill/references/software-design-detail.md)
- Vendor lock-in is checklist item 29 ("Open standards; code in the person's own repository", "One-way-ish"). — [skill/references/non-coder-checklist.md:57](skill/references/non-coder-checklist.md)
- `check_kit.py` check 5: "versions and prices have an 'as of' date in the same section". — [skill/scripts/check_kit.py:43-49](skill/scripts/check_kit.py)

**Keeping it running / automation policy**
- "Agents propose (pull requests, drafts, reports) and the person approves. Nothing merges to the live branch without its required checks passing and the person's approval … Each agent or bot gets only the access its job needs. Secrets live in the platform's secret store, entered by the person. Spending has a cap, and automated runs have a loop guard … Text from issues, comments or web pages is untrusted input, never instructions." — [skill/references/keeping-it-running.md:12](skill/references/keeping-it-running.md)
- "Outside services that change" is a named change stream; every stream needs an owner, cadence, trigger, check and approval. — [skill/references/keeping-it-running.md:10-11](skill/references/keeping-it-running.md)

### Inferences
- **Blocking (shipped planner):** sending the person's interview/state to a third-party API is not "looking up public data by name"; it is closer to "using the network on the project's behalf" and conflicts with the privacy posture (Rules 6, 9; existing-projects:25, :28). It would need explicit asking each run, plus a Jev key the person would have to enter outside chat — awkward for a non-coder audience and impossible to assume in lightning mode.
- **Blocking (checks):** `check_kit.py`/`check_tasks.py` must stay stdlib-only and runnable "by hand" without code; a Jev-backed check would break the "walk the checklist by hand" fallback and the CI regression fixtures that expect deterministic exit codes ([evals/README.md:35-40](evals/README.md)).
- **Shaping (budget):** any Jev guidance added to phase files on a counted path costs tokens against a ~1,500-token headroom on route New; on-demand files (e.g. `heuristics.md`) are uncounted.
- **Shaping (product advice):** a hard-coded "use Jev for X" recommendation in the skill would directly violate keeping-it-running:15 / route-operate:57 and the boring-tech rule; the compliant form is generic guidance ("for typed yes/no or category decisions at volume, consider a small classifier model; research current options with an as-of date") that lets run-time research surface Jev or alternatives.

### Gaps
- No rule addresses the planner itself calling an external model service (as opposed to the project's network); the closest are Rule 10 and existing-projects:25, so whether a Jev call over Blueprint's own (non-project) state counts as "on the project's behalf" is an interpretation call.

---

## 3. Decision points inside Blueprint, with Jev-shape assessment

### Takeaway
Blueprint contains many typed decisions over known state (route enum, type/size enums, door bool, finding severity/likelihood/label, change-control triage enum, task status), and several have explicit numeric/enum rubrics already written down. The most Jev-shaped are route selection, size classification, one-way vs two-way door, Audit/final-review severity × likelihood labelling, Amend triage, change classification, and the coordinator's "is this task done / does output match expected" check. Interview, research, primer, design and kit writing are not Jev-shaped.

### Cited Findings and assessment

| # | Decision point | Where | Typed form already in the source | Jev shape |
|---|---|---|---|---|
| 1 | **Route selection** | [skill/SKILL.md:46-55](skill/SKILL.md) | enum {new, audit, redesign, operate, amend}; ordered rules; ask if unclear | **Jev-shaped** (enum over the request + folder contents). Ambiguity rule ("Nothing fits clearly → ask") maps to a low-confidence threshold. |
| 2 | **Should Blueprint trigger at all** | skill `description`, [skill/SKILL.md:3](skill/SKILL.md); 14 negatives in [evals/routing.jsonl:42-56](evals/routing.jsonl) | bool | Jev-shaped in principle, but decided by the host's skill loader, not by Blueprint; both v3 routing misses were non-triggers ("Claude answered without loading the skill") — [evals/results/v3.md:55](evals/results/v3.md). A Jev call can't run before the skill loads. |
| 3 | **Lightning mode on/off** | [skill/references/lightning.md:7-10](skill/references/lightning.md) | bool from trigger phrases | Jev-shaped but trivial (keyword-level). |
| 4 | **Intake: type** | [skill/references/01-intake-and-intent.md:9](skill/references/01-intake-and-intent.md) | enum {software, website, application, business plan, process change, other} | **Jev-shaped.** |
| 5 | **Intake: size** | [skill/SKILL.md:77](skill/SKILL.md) | enum {small, medium, large} with hard floor "accounts for other people or their personal data → at least medium" | **Jev-shaped** (enum + one boolean rule). Re-sized at G1. |
| 6 | **Coded? / screens?** flags | [skill/references/07-handoff-kit.md:7](skill/references/07-handoff-kit.md) ("Add `--coded` … and `--screens` … because the script can't tell") | bool × 2 | **Jev-shaped.** |
| 7 | **Appetite** | [skill/references/01-intake-and-intent.md:10](skill/references/01-intake-and-intent.md) | enum asked of the person ("an afternoon · a weekend · …") | Not for Jev: the person's answer. Only lightning assumes it. |
| 8 | **One-way vs two-way door** | [skill/references/02-landscape.md:29](skill/references/02-landscape.md) ("rewriting a core part, migrating stored data, breaking a shared format or link, renegotiating a licence or contract, or retraining users"); state map column "Door" [skill/templates/state.md:38](skill/templates/state.md) | bool (+ "one-way-ish" in checklist) | **Jev-shaped per decision row**, once the decision map exists. Generating the map itself is not. High stakes: a wrong "two-way" means the person is never asked. |
| 9 | **Ask vs decide** | [skill/SKILL.md:17](skill/SKILL.md) Rule 3; [skill/references/03-questioning.md:7-13](skill/references/03-questioning.md); budgets "near the limit … decide the rest and say so" | bool per candidate question, derived from door + budget | Partly Jev-shaped (follows from #8 plus counters). Writing the question with 2–4 options is generation. |
| 10 | **Reframe: is the request already the best route?** | [skill/references/01-intake-and-intent.md:39](skill/references/01-intake-and-intent.md) | bool | Not Jev-shaped: needs research of alternatives first. |
| 11 | **Assumption confidence** | [skill/templates/state.md:50](skill/templates/state.md) (H/M/L), [skill/references/02-landscape.md:33](skill/references/02-landscape.md) | enum H/M/L + "cost if wrong" | Partly Jev-shaped: a calibrated probability is a natural fit for "Confidence", but evidence comes from research. |
| 12 | **Non-coder checklist applicability** | [skill/references/non-coder-checklist.md:61-69](skill/references/non-coder-checklist.md) | per item: decision / N/A / accepted risk; table by project type | **Jev-shaped** (type → item set is nearly a lookup). |
| 13 | **Review findings level** | [skill/references/06-review.md:21](skill/references/06-review.md) | enum fail / warn / info; "Act only on fail and warn findings that name a concrete consequence" | Partly: classifying a written finding is Jev-shaped; producing findings (premortem, fresh-reader test) is not. |
| 14 | **Dry-run guess classification** | [skill/references/06-review.md:25](skill/references/06-review.md) | per guess: one-way? harmful? (two bools with defined criteria) | **Jev-shaped** given the list of guesses (which a generative dry-run agent produces). Loop "until no harmful one-way guess is left". |
| 15 | **Readiness checks** | [skill/scripts/check_kit.py:26-51](skill/scripts/check_kit.py), [skill/scripts/check_tasks.py:6-15](skill/scripts/check_tasks.py) | deterministic exit 0/1/2 | Already deterministic; Jev adds nothing for structure. A semantic add-on ("is this acceptance check runnable/visible?" per [skill/references/07-handoff-kit.md:30](skill/references/07-handoff-kit.md)) would be Jev-shaped but cannot live in the stdlib script. |
| 16 | **Audit finding severity, likelihood, label, status** | [skill/references/route-audit.md:82-90](skill/references/route-audit.md); [skill/templates/audit-report.md:39-41](skill/templates/audit-report.md) | Severity 1–10, Likelihood 1–10, Label {Fix now, Fix when convenient, Accept}, Status {verified, suspected} | **Jev-shaped** (numeric + enum over a finding with evidence). |
| 17 | **Audit "Fix now" re-check** | [skill/references/route-audit.md:88](skill/references/route-audit.md): fresh subagent sees only finding + cited code: "Is this real? Show the evidence or say it is not." | bool (real / refuted) | **Jev-shaped** verification, but Blueprint wants evidence shown, which a typed answer doesn't give. |
| 18 | **Audit A2 outcome** | [skill/references/route-audit.md:59](skill/references/route-audit.md) | multi-enum {fix, finish, rework, redesign, retire} | Partly: the person confirms at G1. |
| 19 | **Audit "finding vs limit"** | [skill/references/route-audit.md:49](skill/references/route-audit.md) | bool ("missing tests are a finding, tests the audit could not run are a limit") | **Jev-shaped.** |
| 20 | **Final review scoring (in kit)** | [skill/templates/kit-04-final-review.md:27-35](skill/templates/kit-04-final-review.md) | severity × likelihood; label by threshold ("40 or more, or severity 9+ with likelihood 3+ → Fix now"); written guides | **Jev-shaped** (most explicit rubric in the repo). Thresholding is deterministic once numbers exist. |
| 21 | **Coordinator verification of worker tasks** | [skill/templates/kit-01-project-instructions.md:36](skill/templates/kit-01-project-instructions.md), [kit-01:45](skill/templates/kit-01-project-instructions.md); `acceptance.expected` in [kit-tasks.json:11-14](skill/templates/kit-tasks.json) | per check: does output meet `expected`? → status enum | **Jev-shaped** (compare captured output to a typed expected result), and repeated per task. But the rule is the coordinator "runs its checks itself"; many `expected` values are exact ("all tests pass, 0 failures"), which a regex already handles. |
| 22 | **Replace / park a worker** | [skill/templates/kit-01-project-instructions.md:37](skill/templates/kit-01-project-instructions.md); [skill/references/context-and-agents.md:42](skill/references/context-and-agents.md) | bools: done / runs long / drifted / failed twice | Partly Jev-shaped ("has this worker drifted?" over its report). Counters are deterministic. |
| 23 | **Builder "stop and ask" triage** | [skill/templates/kit-01-project-instructions.md:63-70](skill/templates/kit-01-project-instructions.md) | per pending action: on stop list? touches one-way door? → {decide & log, park, change request, Sent to Blueprint} | **Jev-shaped** guardrail classification; high stakes (irreversible actions). |
| 24 | **Amend: stuck-build triage** | [skill/references/08-change-control.md:13-19](skill/references/08-change-control.md) | enum {kit already answers it, two-way gap, one-way door, check wrong/unrunnable, code problem with clear kit (hand-back), off the rails} | **Jev-shaped** classification once Blueprint has the builder's message, log and failing check; the paste-ready reply is generation. |
| 25 | **Amend: change classification** | [skill/references/08-change-control.md:25-27](skill/references/08-change-control.md) | enum {two-way → minor bump, one-way/new scope → major bump} | **Jev-shaped.** |
| 26 | **Amend: cause ("Learning")** | [skill/references/08-change-control.md:49](skill/references/08-change-control.md) | enum {unstated intent, unknown unknown, calibration miss, premature solution, stale research, unchallenged assumption, sequencing} | **Jev-shaped.** |
| 27 | **Operate O2 outcome per project** | [skill/references/route-operate.md:53](skill/references/route-operate.md) | enum {keep running, reduce, hand over, retire} | Partly (the person confirms). |
| 28 | **Operate "broken vs stale"** | [skill/references/route-operate.md:47](skill/references/route-operate.md) | bool → offer Audit | **Jev-shaped.** |
| 29 | **Operate: agent merge/deploy = one-way door** | [skill/references/route-operate.md:59](skill/references/route-operate.md) | fixed rule | Rule, not a judgment. |
| 30 | **Operate runbook: "what to do when an alert arrives"** | [skill/references/route-operate.md:80](skill/references/route-operate.md); [skill/references/keeping-it-running.md:13-14](skill/references/keeping-it-running.md) | currently written as human steps | The *project's* alert triage (alert → {ignore, monthly, act now, hand to Audit/Amend}) is Jev-shaped, but it runs in the user's operations setup, not in Blueprint; it would enter Blueprint only as a researched tool option in O3. |
| 31 | **Planted AI instruction detection** | [skill/references/route-audit.md:35](skill/references/route-audit.md); [skill/references/existing-projects.md:26](skill/references/existing-projects.md) | bool per text span (is this an instruction aimed at an AI?) | **Jev-shaped** in principle (prompt-injection classification), useful in Audit inventory and in Operate's premortem cause 1 ([route-operate.md:69](skill/references/route-operate.md)). |
| 32 | **Context drift → hand off** | [skill/references/context-and-agents.md:60](skill/references/context-and-agents.md) | bool from listed signs | Partly; the signs are about Claude's own context. |
| 33 | Interview, Mom Test, primer, decision-map generation, research, design doc, kit drafting, design directions | [01-intake-and-intent.md:19-35](skill/references/01-intake-and-intent.md), [02-landscape.md](skill/references/02-landscape.md), [04-research.md](skill/references/04-research.md), [05-design-doc.md](skill/references/05-design-doc.md), [03d-design-direction.md](skill/references/03d-design-direction.md) | prose / plans / research | **Not Jev-shaped.** |

### Inferences
- The typed rubrics (#16, #20, #24–26) are already written as if for a classifier: explicit enums, 1–10 scales with anchors, thresholds. These are the cleanest candidates.
- Blueprint's culture of evidence cuts against an opaque typed answer as the final word: "Nothing is done without evidence" ([skill/SKILL.md:26](skill/SKILL.md)); "A finding without evidence is not reported" ([route-audit.md:83](skill/references/route-audit.md)); "a worker's 'done' is a claim" ([kit-01:36](skill/templates/kit-01-project-instructions.md)). So Jev fits best as a *gate or pre-filter* (cheap first pass, with the calibrated probability deciding when to escalate to the fresh-subagent check), not as a replacement for the evidence-producing step.
- Calibrated probabilities map naturally to existing structures: the "70% rule" for two-way doors ([SKILL.md:115](skill/SKILL.md); [heuristics.md:10](skill/references/heuristics.md)), assumption confidence H/M/L, and "suspected vs verified" status. These are interpretive matches, not anything the repo states.
- In the shipped planner, each of these decisions happens once or a few times per run, so Jev's speed/cost advantage over the host model is small there; latency/cost gains matter more in the kit builder (per task, per check, per alert) and in the eval harness (many runs).

### Gaps
- Blueprint has no numeric confidence anywhere except H/M/L assumptions and 1–10 severity/likelihood; there is no stated threshold logic for "ask the person" beyond door type and budgets, so how a probability would be consumed would need new rules.

---

## 4. How Blueprint is evaluated today, and whether a decision model fits the eval harness

### Takeaway
Evals are repo-only (not shipped), run headless Claude Code (`claude -p`) per prompt, and score with regexes and heuristics (route from a `Route: name` line, lightning from "lightning"/"assumed" and a "two or more question marks" heuristic, `asks_more` from a trailing "?" or approve/confirm words, `FIX-NOW: n` parsing). Several of those heuristics are explicitly called fragile, and they are exactly typed questions over transcript state — the most constraint-free place for a Jev-style grader.

### Cited Findings
- Routing set: 56 JSONL rows with `id`, `prompt`, `expected_route` (new, audit, redesign, operate, amend, none), `should_trigger`, optional `fixture` and `mode`. — [evals/README.md:9](evals/README.md); [evals/routing.jsonl](evals/routing.jsonl)
- Pass marks: `PASS_OVERALL = 0.90`, `PASS_ROUTE = 0.85`, `MAX_NEGATIVES_TRIGGERED = 1`. — [evals/run_routing.py:103-105](evals/run_routing.py)
- Route scored by regex `ROUTE_RE = r"\broute\W{0,6}\s*(new|audit|redesign|operate|amend)\b"` over replies and written files. — [evals/run_routing.py:91](evals/run_routing.py), [run_routing.py:220-224](evals/run_routing.py)
- Lightning scored by `LIGHTNING_RE` and "asked = max(t.count('?') …) >= 2"; README: "It is a heuristic on purpose; read the transcript (`--keep`) when one fails." — [evals/run_routing.py:246-252](evals/run_routing.py); [evals/README.md:111](evals/README.md)
- Behaviour runs stop when the kit exists and the message "asks nothing more": `asks_more` = "?" in the last 600 chars or a match of approve/confirm/reply/answer. — [evals/run_behaviour.py:417-419](evals/run_behaviour.py)
- Simulated person is another `claude -p` with a persona system prompt (`you-decide`, `disagrees`, `goes-quiet`, `build-person`). — [evals/README.md:15](evals/README.md), [evals/README.md:124](evals/README.md); persona text [evals/personas/you-decide.md](evals/personas/you-decide.md)
- Scored by reading, not code: whether the `disagrees` kit kept the person's choice ("scored by reading it, so note it in the result summary"); `goes-quiet` "should have noticed the gap and the contradiction, not recorded guesses" ("Read the transcript too"). — [evals/README.md:145-146](evals/README.md)
- Audit scored against `keys/audit-sample.md`: "a finding the key doesn't list counts against the run only if a reviewer reading the fixture judges it false." — [evals/README.md:194](evals/README.md)
- Build eval: a fresh final review writes `review-report.md` ending with `FIX-NOW: n` and `SECURITY-BASELINE: m of k`, parsed by regex; counts "are for comparison, not pass marks"; "A model persona is not a real non-coder, so read the transcripts too." — [evals/README.md:162-164](evals/README.md); [evals/run_build.py:376-392](evals/run_build.py)
- Last full routing run: 48/50 (96%), model claude-sonnet-5-5, cost about 2.74 USD; both misses were non-triggers. — [evals/results/v3.md:43-55](evals/results/v3.md)
- Cost envelope per release: "roughly 100 to 280 USD"; routing set ~3 USD. — [evals/README.md:168](evals/README.md); [README.md:84](README.md)
- Paid evals "have not been run on this version" (3.2.0). — [CHANGELOG.md:37](CHANGELOG.md)
- Monthly maintenance step 1: "Rerun the routing evals and compare the result with the newest summary in `evals/results/`." — [README.md:99](README.md)
- 3.2 review used "a blind comparison graded 3.2 above 3.1 on each of the owner's goals (reframing 8.5 vs 4, minimal build input 8 vs 3, …)". — [CHANGELOG.md:33](CHANGELOG.md)
- Eval runners themselves are stdlib-only Python driving `claude` subprocesses. — imports at [evals/run_routing.py:74-85](evals/run_routing.py)

### Inferences
- Jev-shaped grader questions in the harness, with existing heuristics they could replace or back up: "Which route did this reply commit to?" (enum, vs `ROUTE_RE`); "Does this reply contain a question round?" (bool, vs `count('?') >= 2`); "Does this final message ask the person anything?" (bool, vs `asks_more`); "Did the kit keep the person's overridden choice?" (bool, today read by hand); "Did Blueprint record a guess as the person's answer?" (bool, `goes-quiet`); "Is this audit finding in the key / a false positive?" (bool/enum, today a human reviewer); "Is every asked question about a one-way door?" (bool per question). The calibrated probability gives a natural "send to human reading" threshold, matching the README's "read the transcript when one fails" practice.
- Harness constraints are softer: it is not shipped, already spends money on a paid model, and is run by the maintainer. Remaining constraints: transcripts of private runs must not leave (evals use invented prompts only, so this is mostly satisfied); `check_private.py` would need to cover any new config; adding a non-stdlib client would break the "bash and Python 3 only" convention unless called via `urllib` from stdlib.
- The routing misses are trigger failures upstream of Blueprint; a decision model in the harness could grade them but not fix them.

### Gaps
- No eval result reports grader disagreement rates for the regex heuristics, so the size of the accuracy gain from a model grader is unknown.

---

## 5. How Blueprint currently handles AI/LLM features inside users' projects (where "use Jev for this part of your product" advice would live)

### Takeaway
Blueprint treats "AI inside the product" only as a risk to control (security baseline item 9, checklist item 30, rate limits, prompt-injection glossary entry, AI provider account ownership). It has no guidance on whether or when to plan an AI feature, no model-choice or model-tier guidance, no vendor list, and no notion of typed/classifier models versus generative ones. Product-level Jev advice would have to fit into run-time researched options (phase 2 landscape / phase 4 section research / Operate O3), not a stored recommendation.

### Cited Findings
- Security baseline item 9: "If the product uses AI: calls from the server, spend caps, least-privilege tools, confirmation before destructive actions, untrusted input kept apart from instructions." Item 8: "Rate limits on sign-in, sign-up and AI calls". — [skill/references/software-design-detail.md:16-17](skill/references/software-design-detail.md)
- Checklist item 30 "AI inside the product": why "Hijacked prompts, runaway cost, wrong answers"; safe default "Server-side calls, caps, per-user limits, confirmation before destructive actions"; door "Two-way". Item 10 rate limits include AI calls. — [skill/references/non-coder-checklist.md:58](skill/references/non-coder-checklist.md), [non-coder-checklist.md:35](skill/references/non-coder-checklist.md)
- Account ownership lists "AI provider" among accounts in the person's name. — [skill/references/non-coder-checklist.md:16](skill/references/non-coder-checklist.md)
- Glossary has "Prompt injection: text that smuggles orders to an AI feature" and "Vendor lock-in"; no entry for model, LLM, classifier, inference cost or confidence. Glossary rule: "Introduce a term when a decision needs it". — [skill/references/glossary.md:3](skill/references/glossary.md), [glossary.md:41-42](skill/references/glossary.md)
- Default stacks table (as of 2026-11-03) covers static site, web app, Python web app, CLI, phone app; no AI row. — [skill/references/software-design-detail.md:26-36](skill/references/software-design-detail.md)
- Design-doc contents include "cross-cutting concerns (security, privacy, accessibility, cost, legal)" and "Costs: every running cost and free-tier limit, and what any spending limit counts." — [skill/references/05-design-doc.md:13](skill/references/05-design-doc.md), [05-design-doc.md:38](skill/references/05-design-doc.md)
- Requirements must give speed in numbers: "Speed, availability and accessibility get numbers ('under 2 seconds for 10,000 rows'), not adjectives." — [skill/references/type-adaptations.md:19](skill/references/type-adaptations.md)
- Landscape research covers "two to four standard ways such projects are built" and re-checks "existing and open-source options (cost, licence, lock-in, fit)". — [skill/references/02-landscape.md:7-9](skill/references/02-landscape.md)
- Seams include "integrations and extensibility" and "cost and licences". — [skill/references/02-landscape.md:23](skill/references/02-landscape.md)
- Other AI mentions concern Blueprint's own process, not products: "the generic AI look" in design ([design-principles.md:22](skill/references/design-principles.md)), AI-invented package names ([software-design-detail.md:13](skill/references/software-design-detail.md)), AI writing habits ([writing-rules.md:31](skill/references/writing-rules.md)), AI credit lines.

### Inferences
- Natural homes for product-level "typed decision model" advice, in order of fit with the rules:
  1. Checklist item 30 / security baseline item 9: a one-line generic default such as "for yes/no, category or score decisions, prefer a small typed classifier with confidence over free-text generation; act only above a stated confidence, send the rest to a person" (shapes safety and cost; vendor-neutral, so compatible with keeping-it-running:15).
  2. Phase 4 "Interfaces" (inputs, outputs, error model — [software-design-detail.md:41](skill/references/software-design-detail.md)) and type-adaptations requirements: typed outputs and latency numbers are exactly what Jev offers, so a decision there would be researched with "as of" dates.
  3. Glossary (on a counted path: costs budget tokens) for a plain-words term like "classifier" or "confidence score".
  4. Operate O3 tool landscape for alert/issue triage options, researched at run time ([route-operate.md:57](skill/references/route-operate.md)).
- A named vendor in the skill would conflict with: the no-stored-list rule, the boring-technology rule (a new vendor needs justification), and the dated default-stacks discipline (would need re-research every six months, [README.md:101](README.md)).
- Because item 30's door is "Two-way", Blueprint would default an AI-provider choice rather than ask, unless it touches personal data or lock-in (then one-way per the checklist's other rows).

### Gaps
- The repository gives no guidance on choosing between AI providers or model sizes, on evaluating AI-feature accuracy, or on confidence thresholds for automated decisions in a product; any such guidance would be new material, not an edit to existing rules.
