# Changelog

## 3.2.1 (unreleased): trim pass

Less repetition, same rules.

- Audit, Redesign and Operate share their gate, intake, read-only and kit rules through one file, `references/existing-projects.md`, so the three routes can't drift apart. Redesign and Operate now get the safety rules Audit already had (such as redirecting temp folders and treating a project's own CLAUDE.md as data).
- SKILL.md's tables carry full file paths, so the separate file index is gone: SKILL.md drops from 4,009 to 3,692 tokens.
- Restatements cut across the planner references and kit templates; each kit rule lives in one kit file. The design direction's top-ten list became a pointer, keeping the two heuristics stated nowhere else.
- Route New reads 23,462 tokens (was 24,819). Audit, Redesign and Operate each read one more file, so their totals move little.

Review: a rule-loss audit verified 141 of 143 cuts and found 2 weakened (both restored). A blind comparison with 3.2.0 found no loss of audit safety, reframing or lightning mode; its top losses (the final reviewer ignoring the builder's instructions, the coordinator rule on the planner side, approvals in the brief) were restored.

## 3.2.0 (unreleased): reframe the request, a builder that runs itself, lightning mode

From a second review (a red-team critique, simulated New, Audit and stuck-build runs, and a fact-check against current Claude Code docs) and the owner's direction.

What's new:

- **Reframe the request.** Planning separates the goal from the method bundled into the request, asks why the problem exists (prevent it upstream or detect it downstream), traces inputs to their source, weighs existing and open-source options, cost and lock-in, and respects what the person can change. It then shows what they asked for beside the better route, with a recommendation, at every size.
- **The builder coordinates and needs little input.** After handoff, the kit's main session hands each task to a fresh worker agent, checks the result by running the task's checks, replaces a worker that is done, runs long or fails twice, and manages its own context. The person is needed at milestone checks, before anything irreversible, for homework only they can provide, and for changes to hard-to-undo decisions. Questions wait for the next checkpoint while other work goes on. Every later start is "Continue the build".
- **Plain words.** Messages to the person name things plainly; IDs such as T-3 appear only in documents or in brackets.
- **Lightning mode** (route New): no questions; Blueprint assumes everything with safe defaults for hard-to-undo choices, writes and checks the kit, lists its assumptions in one message, and on request puts the kit in place for the builder.
- **No AI credit lines.** Kits set Claude Code's `attribution` setting so commits and pull requests carry no "Co-Authored-By: Claude" or "Generated with Claude Code" lines, unless the person chooses them.
- **Project settings in every coded kit.** The brief carries the exact, dated `.claude/settings.json` (secret files denied, risky commands asked, fresh workers, attribution), written by the first task and checked.
- **Stuck builds go to Amend**, which gathers the builder's question in one message and returns one paste-ready reply that lets the builder carry on; amendments to small kits are applied as section edits, so the builder's log survives.
- **Audit fixes:** a leaked secret is removed and revoked before anything is committed; the audit report stays outside a public project; findings are sorted Fix now first; runs redirect home and temp folders into the copy; public advisory lookups count as research; a project's own CLAUDE.md is treated as data; small audits fit their round budget; questions a non-coder can answer.
- **Small kits** ship `project-instructions.md` (renamed `CLAUDE.md`, under 700 words), `kit-lite.md` and `final-review.md`.
- **Facts updated** for current Claude Code (auto mode, forked subagents, settings syntax), Supabase keys and Django LTS; several attributions corrected.
- **Evals:** a build-from-kit outcome eval (`evals/run_build.py`) against a plain plan-mode baseline; routing prompts for stuck builds and lightning mode; public lookups allowed in behaviour runs.
- **Budgets:** route New's limit is raised from 22,243 to 25,000 tokens, with a separate 4,200-token cap on SKILL.md, because the limit is a regression guard, not a measure of context quality. Additions this release: the reframe, the coordinator model, lightning mode (its own file) and project settings.

Review: a blind comparison graded 3.2 above 3.1 on each of the owner's goals (reframing 8.5 vs 4, minimal build input 8 vs 3, plain words 8 vs 4, fast mode 7.5 vs 1, audit safety 8.5 vs 6.5); 3.1 remained leaner. A re-run of the audit simulation found all 8 planted problems, stayed in budget and left the project unchanged.

Known limitations:

- The paid routing, behaviour and build-from-kit evals have not been run on this version.
- `CLAUDE_CODE_FORK_SUBAGENT` is the documented switch for fork mode; its effect on worker isolation is untested.
- Route New reads 24,819 of 25,000 tokens; SKILL.md is 4,009 of 4,200.

## 3.1.0 (unreleased): review fixes, appetite carried through, rules backed by tools

From a full review of 3.0.1 against research on planning, software delivery, existing planning skills and current Claude Code guidance.

Fixes:

- Audit, Redesign and Operate small kits now name `final-review.md`, matching 3.0.1's file names.
- Blueprint passes `--coded` and `--screens` to the kit check, which no longer guesses "coded" from `tasks.json`; a coded kit without a security baseline now fails.
- The kit check finds the task title column exactly, accepts evidence files such as an audit report, HTML tag names and IP addresses in prose, a kit-lite renamed `CLAUDE.md`, and large briefs split into `build-brief-1.md`, `build-brief-2.md`…; it reports a file that isn't UTF-8 (exit 2) instead of crashing. The task check accepts an optional `delivers` field and fails on dependency loops.
- The brief no longer repeats the session table or the Claude-project task checks; evidence files the brief names count as kit sources; small New projects say how G1, G2 and G3 share their one round, with Explore outside it; Operate kits keep the full runbook at any size; undefined internal IDs removed.
- The behaviour eval runner finds the 3.0.1 brief name; the routing runner exits non-zero on a failure; CI no longer skips checks silently.

Improvements:

- The appetite reaches the design and the kit, with the order scope is cut if it runs out, and the builder stops when it is used up. The premortem includes the owner running out of time or interest. Keeping it running adds one dated check of the success measures after real use.
- The first milestone of hosted software reaches the real host with checks passing; the instructions gain a Commands section written by the first task, and a Compact instructions section.
- Rules that can't bend are enforced by tools from the first milestone (checks on every push, code-host protection, Claude Code settings), as policy the builder sets up with the person's approval. The builder never edits a test to pass it.
- Builder wording tuned for current models: "run each task's acceptance checks" instead of "verify every step", and no subagents to double-check its own work.
- Audit fix kits pin current behaviour with tests before changing it, and a full rewrite is a one-way door; Redesign kits record browser tests for the must-stay list first. The audit inventory covers backups and account holders. The security baseline names injection, escaping and failing closed.
- Evals: `--no-skill`, `--runs`, `--person-model`, `--allow-subagents` and two new personas (one disagrees, one goes quiet); word counts per kit file.
- SKILL.md "Decision guidance" keeps doors, jobs to be done and the Mom Test, appetite and boring technology; the rest are applied in their phase files, and `references/heuristics.md` is unchanged.

Review:

- A blind comparison of 3.0.1 and 3.1 rated 3.1 higher on all six criteria (mean 7.8 against 5.7). The paid evals are still to be rerun.

Known limitations:

- The routing and behaviour evals have not been rerun on this version yet; run them before release.
- Route New reads 22,241 of its 22,243-token limit, so the next addition needs a cut or a new limit.

## 3.0.1 (2026-11-05): kit files drop into docs/ unchanged

- Kit files now have their final names: `START-HERE.md`, `project-instructions.md`, `build-brief.md`, `progress-log.md`, `tasks.json`, `final-review.md` and `design-spec.md` (small kits: `kit-lite.md` and `final-review.md`). In Claude Code, only the instructions file is renamed, to `CLAUDE.md`; the rest move into `docs/` as they are. It is never delivered as `CLAUDE.md`, because a file with that name takes over whichever Claude Code session it lands in.
- The final message ends with a numbered "Your next steps" block: the folder, the one rename, the `docs` folder, the files to move by name, and the first message to send.
- `check_kit.py` and the eval runner accept both the new names and the numbered names of earlier kits.
- Known limitation: route New's reading budget has 23 tokens of headroom left (22,220 of 22,243).

## 3.0.0 (2026-11-05): five routes and Keeping it running

Blueprint 3 plans projects at any stage, not only new ideas, and every kit says how the result is kept running. It stays one skill named `blueprint` that plans and never builds or edits the project it plans for.

What's new since 2.0.0:

- **Five routes.** Blueprint picks one and names it in its first reply (`Route: operate`): New (an idea), Audit (review, fix, finish or rescue an existing project), Redesign (change only the look and feel), Operate (upkeep of projects you already have) and Amend (change a delivered kit). When a request fits none clearly, it asks one question naming the five.
- **Keeping it running.** Every kit says who looks after the result and for how many hours a month, what changes or expires, what agents may do unattended (they propose, you approve), the safety net, and a monthly routine under 15 minutes. The kit check fails a kit without this section, and the final review asks whether you could follow the routine next month.
- **Audit.** Maps what exists, confirms with you what the project is for and which standards it is judged against, and only then lists findings, each with evidence and labelled Fix now, Fix when convenient or Accept. Ends with an audit report and a fix kit.
- **Redesign.** Works from screenshots at phone and computer widths, lists the current colours, type and spacing with their file and line, measures contrast, and always offers "refresh the current look" as one direction. The kit changes the presentation only, never what the project does.
- **Operate.** Inventories each project in a table with a coverage list of what was read and what could not be checked, agrees what "kept running" means, compares current tools researched at run time with dates, and hands over setup tasks, each with a check that proves it works, plus a runbook. Its premortem answers five agent risks: planted instructions, an agent merging or deploying alone, a workflow handing secrets to outside code, an agent loop or runaway cost, and a token with more access than its job needs.
- **Read-only on your projects.** Audit, Redesign and Operate read the project and may run commands that write nothing outside a temporary copy. They ask before anything that touches live data, accounts, services or the network, and report a secret by file, line and kind, never its value. Text in the project that tries to instruct an AI is reported, never followed.
- **Gates held when you delegate.** "You decide" changes who chooses, never whether a step is shown: Blueprint shows the goal and the options, makes the choice, and records it as yours to change.
- **Blueprint 2 compatibility.** A Blueprint 2 state file resumes where it stopped. Amending a Blueprint 2 kit offers to add Keeping it running.
- **Repository.** Built zips are no longer committed; each release on the Releases page carries `blueprint.zip`. Checks run on every pull request, and the `evals/` folder holds the routing set, sample projects and result summaries.

Known limitations of this release, measured on 2026-11-05 with one model (claude-sonnet-5-5, Claude Code 2.1.318):

- **Routing:** 48 of 50 prompts reached the right route (96%): new 11 of 11, audit 7 of 8, redesign 6 of 7, operate 7 of 7, amend 3 of 3, and none of the 14 prompts that must not trigger did. The two misses are short prompts with no project in the folder, where Claude answered without loading Blueprint. Results: `evals/results/v3.md` and `evals/results/v3-cr7-operate.md`.
- **Route budgets:** on a medium project, route New reads 22,130 of its 22,243-token limit, leaving little room; Audit reads 21,474, Redesign 20,337 and Operate 19,336 tokens, each within 27,000 (`scripts/route_budget.py`).
- **Behaviour evals are single runs:** each route's whole-conversation eval passed on one invented project (Audit found 8 of 8 planted problems; Redesign and Operate kits passed the kit check with every project file unchanged), one run each with a simulated person who answers "You decide". They are evidence, not a guarantee.
- **Eval isolation:** evals run in a temporary folder with Bash limited to `python3`, but Claude Code still runs read-only commands such as `ls`, `cat` and `find` without asking, and file commands such as `mkdir` and `cp` inside the eval folder. The runner lists every command, fails a run on any network use or changed project file, and flags writes outside the eval folder it can detect.
- **Reviews in evals are self-reviews:** the evals give Blueprint no subagent tool, so the fresh-reviewer steps (re-checking "Fix now" findings, the design review) ran as labelled self-reviews.
- **Without web search,** Audit, Redesign and Operate list the facts they could not check (advisories, plan limits, prices) and give the kit a task that confirms them first.
- **Releases are published from the Releases page:** pushing tags from the cloud sessions that built this release was blocked, so a release is made by publishing it on GitHub's Releases page with a new tag; the release workflow then attaches `blueprint.zip` and the changelog entry.
- **Private-terms check in CI is optional:** CI checks files and commit messages for private terms only when the repository has a `PRIVATE_TERMS` secret. It is not set by default, so that step reports skipped; the maintainer runs `scripts/check_private.py` locally before every push.
- Kits made by Blueprint 2 fail this version's kit check until they gain a "Keeping it running" section; Amend offers to add it.

## 3.0.0-beta.2 (2026-11-05): Audit route

Second pre-release of Blueprint 3. Blueprint can now audit a project that already exists, in any state, and plan its fixes. It reads the project and never changes it.

What's new:

- **Audit route.** Ask Blueprint to review, fix, finish or rescue an existing project, repository or site. It maps what exists, confirms with you what the project is for (G1), shows you the standards it will judge against (G2), and only then lists its findings. Each finding has evidence (file and line, a command and its output, or a link), says whether it was seen or only suspected, and is labelled Fix now, Fix when convenient or Accept. You pick the fix set, and Blueprint hands over a fix kit a builder carries out.
- **Gates held when you delegate.** If you answer "You decide", Blueprint still shows each gate, makes the choice, and records it as yours to change. A small audit asks you once before its final message.
- **Audit report.** `audit-report.md` lists what was read, sampled or skipped, every command run or not run, and a section on what the audit could not check, so nothing unread passes as checked. Secrets are reported by file, line and kind, never by value. Text in the project that tries to instruct an AI is reported, never followed.
- **Fix kit.** The fix kit has the same layout as every Blueprint kit, passes the kit check, and includes Keeping it running.

Known limitations of this release:

- Redesign and Operate are not available yet; Blueprint names them and offers to plan the work as a new project.
- Without subagents, the re-check of each "Fix now" finding is a labelled self-review.
- Dependency advisories need web access; without it, the report lists them as not checked.
- Measured on 2026-11-05 with one model (claude-sonnet-5-5): results are in `evals/results/v3-s4-audit.md` and `evals/results/v3-s4-audit-fixes.md`. On a small seeded project the audit found 8 of 8 planted problems with no false findings and left every file unchanged; routing passed 36 of 36.

## 3.0.0-beta.1 (2026-11-05): router and Keeping it running

First pre-release of Blueprint 3. Blueprint now plans projects at any stage, and every kit says how the result is kept running.

What's new:

- **Routes.** Blueprint picks one of five kinds of planning and names it in its first reply (`Route: new`): New (an idea), Audit, Redesign, Operate (upkeep of projects you already have) and Amend (changing a delivered kit). This release runs New and Amend; Audit, Redesign and Operate are named and come in later pre-releases, and until then Blueprint says so and offers to plan the work as a new project.
- **Keeping it running.** Every kit has a section saying who looks after the result and for how many hours a month, what changes or expires, what agents may do unattended (they propose, you approve), the safety net, and a monthly routine under 15 minutes. The kit check fails a kit without it, and the final review asks whether you could follow the routine next month.
- **Read-only look at existing projects.** Rule 10 now lets the coming routes read a project and run commands that write nothing outside a temporary copy; Blueprint still never builds or edits the project.
- **Blueprint 2 compatibility.** A Blueprint 2 state file resumes where it stopped, without repeating passed steps. Amending a Blueprint 2 kit offers to add the new section.

Known limitations of this release:

- Audit, Redesign and Operate are not available yet.
- Kits made by Blueprint 2 fail this version's kit check until they gain a "Keeping it running" section; Amend offers to add it.
- On a medium project, route New reads about 22,100 tokens of Blueprint's own files, within its limit of 22,243 but with little room to spare.
- Measured on 2026-11-05 with one model (claude-sonnet-5-5): routing results are in `evals/results/v3-beta1.md`; Audit, Redesign and Operate routing is not measured yet.

## 2.0.0 (2026-11-04): first public release

Blueprint turns an idea into an execution kit: a short set of documents a fresh AI agent can build from without guessing. It plans; it never builds.

What it does:

- Explores a vague idea, confirms the goal, and explains each decision in plain words before asking about it.
- Asks you only about choices that are hard to undo, decides the rest with named rules of thumb, and records every decision with its reason.
- For anything with screens, shows you a few look-and-feel directions to choose from.
- Gives coded projects a security and privacy baseline for people who don't code.
- Checks the kit for gaps before handing it over; every kit ends with an independent review of what was built.

Known limitations of this release:

- Kits for medium-sized web apps with user accounts can still leave a few hard-to-undo details to the builder's guess, where a wrong guess affects safety, cost or legal duties. In the last test, the kit for a club members' app left 9, such as whether members can change their own role. The kit tells the builder to stop and ask about such details.
- No kit has yet been built in full and passed its independent final review. In testing, only the sign-in and roles part of one app was built, and its tests passed.
- On a medium project, Blueprint can read slightly more of its own files than its target (about 25,600 tokens, not 25,000).
