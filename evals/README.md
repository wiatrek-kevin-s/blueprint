# Evals

How Blueprint is tested. Nothing here ships in the skill zip.

## What is here

| Path | What it is |
|---|---|
| `routing.jsonl` | The routing set: prompts with the route each should reach, or `none` when Blueprint must not trigger. One JSON object per line: `id`, `prompt`, `expected_route` (new, audit, redesign, operate, amend, none), `should_trigger` (true or false), `fixture` (a path under `evals/fixtures/`) when the prompt needs files, and `mode` (`lightning`) when the reply must also be in that mode. |
| `run_routing.py` | Runs the routing set with headless Claude Code and scores it. |
| `run_behaviour.py` | Runs one whole Blueprint conversation with the simulated person, then checks the kit it writes. |
| `run_build.py` | The outcome eval: a fresh builder builds from a kit (or, as the baseline, from a plain plan), a simulated person answers at checkpoints, then a fresh final review runs. See "Build evals". |
| `fixtures/` | Small invented projects and kits the evals copy into their temporary folders. |
| `keys/` | Answer keys. They stay outside `fixtures/`, because eval runs copy only the fixture, so the run never sees its key. |
| `personas/` | The simulated people for behaviour evals. `you-decide.md` (the default) answers "You decide" to every question and "approve" at every approval, so a full run needs no human. `disagrees.md` turns down Blueprint's first recommendation and holds that choice. `goes-quiet.md` gives a partial answer, then a wrong one, then stops replying. `build-person.md` is the person in build evals: answers only at checkpoints, won't read code, and keeps everything local. |
| `results/` | Summaries of eval runs: pass counts, date and model. Never transcripts of private runs. |

Every prompt and fixture is invented and generic.

## Fixtures

| Fixture | Used for |
|---|---|
| `v2-state.md` | A Blueprint 2 state file at phase 3 with no Route line; resume prompts must continue it as route New |
| `delivered-kit/` | A delivered small kit with its state file; Amend prompts change it. It keeps the numbered name `04-final-review.md`, so the check still accepts kits from before 3.0.1 |
| `empty-repo/` | A repository with only a title README; routes to New |
| `kit-good/` | A small kit that passes `check_kit.py`, including a filled "Keeping it running" section; its final review has the current name, `final-review.md` |
| `kit-missing-upkeep/` | The same kit without "Keeping it running"; passes Blueprint 2's check and must fail Blueprint 3's, which requires the section |
| `check-*/` | Regression fixtures for `check_kit.py` and `check_tasks.py`, one behaviour each (below). CI runs every one. |
| `audit-sample/` | A tiny command-line project with planted problems for Audit evals; its key is `keys/audit-sample.md` |
| `redesign-sample/` | A two-page static site with known contrast failures for Redesign evals; its key is `keys/redesign-sample.md` |

### Readiness-check fixtures

Each `check-*` folder holds a kit (or task list) that tests one rule of `check_kit.py` or `check_tasks.py`, and a `README.txt` that says why. The README's first lines are the expectations CI checks ("Readiness-check fixtures" in `.github/workflows/ci.yml`), one run per line:

- `expect: <exit code> [--flag ...] [| text]`: `check_kit.py <fixture> [--flag ...]` must exit with that code and, when `| text` is given, print that text.
- `expect-tasks: <exit code> <tasks.json> [<baseline>]`: `check_tasks.py` on those files (paths inside the fixture) must exit with that code.

CI fails on any other exit code, missing text or traceback. Exit codes: 0 ready, 1 not ready, 2 a file that can't be read.

| Fixture | Expected |
|---|---|
| `check-blank-title/` | Not ready: a task row has no title |
| `check-brief-parts/` | Ready: a brief split into `build-brief-1.md` and `build-brief-2.md` |
| `check-brief-parts-gap/` | Not ready: a part is missing, a section is missing across the parts, and a part is over the word limit |
| `check-coded-flag/` | Ready without flags, with a note to re-run with `--coded` for software; not ready with `--coded` (no security baseline) |
| `check-evidence-files/` | Ready: an audit report and an amendment dated once near the top |
| `check-html-in-prose/` | Ready: HTML tags such as `<label>` named in prose |
| `check-ip-address/` | Ready: `127.0.0.1` is not a version number |
| `check-lite-renamed/` | Ready as a small kit: `kit-lite.md` renamed to `CLAUDE.md` |
| `check-not-utf8/` | Exit 2: a file not saved as UTF-8 |
| `check-placeholder-like-tag/` | Not ready: placeholders that start with a tag word, such as `<header row, separator, …>` and `<section name>`, beside real tags |
| `check-prose-false-alarms/` | Ready: `< 3` comparisons, a `<Button>` component, "2 hours per month", a version in Sources, and a task with one row per check |
| `check-tasks-cycle/` | Not ready: `depends_on` loops; `check_tasks.py` fails too |
| `check-tasks-delivers/` | Ready with `delivers` lists; `check_tasks.py` fails when the builder changes `delivers` against the baseline |
| `check-undated-version/` | Not ready: a version without an "as of" date in a kit file |

## How a routing eval runs

Each prompt runs in its own `claude -p` process, started in a new temporary folder outside the clone. The folder is built from tracked files only, with `git archive`:

- the skill under test goes to `.claude/skills/blueprint`, as a project skill;
- the prompt's fixture, if any, is copied in under its own name (for example `v2-state.md` or `delivered-kit/`).

So the run never sees anything that isn't committed: no local notes, no answer keys.

### Only the copy under test may answer

Another copy named `blueprint` may be installed for the same user, for example one synced from the Claude app into Claude Code, and a Claude Code session can carry its own context (an attached Claude project, memory) into processes it starts. So the runner starts each eval with:

- `--setting-sources project`: skips user-level settings and skills, so only the project copy of `blueprint` loads;
- `--tools Skill,Read,Glob,Grep,Bash,Write,Edit`, `--disallowedTools Projects`, `--strict-mcp-config` and `--no-chrome`: no tool that reaches outside the folder, such as a tool that reads documents attached to a Claude project, connectors or the browser;
- an environment without the variables that hand the parent session's project, memory, extra directories and session links to child processes (`ENV_DROP` in `run_routing.py`).

Every run checks the result from what Claude Code lists at start: the skills must contain `blueprint` exactly once and no other skill whose name ends in `blueprint`, and every tool must be on the allowlist, or that eval fails. The probe proves the whole set once per machine:

```bash
python3 evals/run_routing.py --probe --max-turns 2
```

It passes when the only blueprint skill listed is `blueprint`, every tool is on the allowlist, the skill's base directory is inside the temporary folder, and Claude reports no CLAUDE.md, project documents or memory in its context. Proven on 2026-11-05 with Claude Code 2.1.318 and model claude-sonnet-5-5. On the same machine, without these settings, Claude Code also listed the app-synced copy (`anthropic-skills:blueprint`) and the names of documents attached to the session's Claude project, and could read them; that is why each setting is there.

### Running the set

```bash
python3 evals/run_routing.py --mode v3 --out evals/results/routing-v3.md
python3 evals/run_routing.py --mode v2 --skill-ref v2.0.0 --max-turns 3 --out evals/results/v2-baseline.md
```

- `--skill-ref` picks the commit whose `skill/` is tested (default `HEAD`); `--fixtures-ref` does the same for the fixtures.
- `--ids new-1,aud-2` runs only some prompts; `--jobs` sets how many run at once (default 4); `--model` passes a model to `claude --model`; `--keep` keeps the folders and transcripts for reading. Without `--keep` they are deleted.
- The runner lists every missed prompt, and exits 1 only when the run is below the pass mark in Scoring (`PASS_OVERALL`, `PASS_ROUTE` and `MAX_NEGATIVES_TRIGGERED` in `run_routing.py`), so a script or CI job can tell a regression from a pass. Run on a few `--ids`, one miss in a route can put that route below its mark.
- Routing needs only the first reply, so keep `--max-turns` small: the v2 baseline used 3, so a run that looks at the folder first still gets to trigger; v3 may need 4 to name its route.
- Each run uses the account Claude Code is signed in with. The runner prints the cost Claude Code reports; the 50-prompt set cost about 3 USD on 2026-11-05.

### Scoring

- **Triggered:** the run calls the Skill tool with `blueprint`, or the prompt starts with `/blueprint` (the host loads the skill directly).
- **v3:** a prompt that should trigger passes when Blueprint triggers and names the expected route in a `Route: name` line, in its reply or in a state file it writes. A negative passes when Blueprint does not trigger.
- **v2 baseline:** Blueprint 2 has no routes, so a prompt that should trigger passes when Blueprint 2 triggers, and a negative passes when it does not. Route accuracy is measured from v3 only.
- **Lightning mode:** a row with `"mode": "lightning"` (`lt-*`) must also show the mode: the replies or a written file mention "lightning" (or "assumed", the mark lightning mode puts on each assumption), and no reply holds a question round (read as two or more question marks in one reply). It is a heuristic on purpose; read the transcript (`--keep`) when one fails. Lightning runs keep working after routing, so `--max-turns 4` cuts them off; that is fine, because only the opening is scored.
- **Stuck builds:** `am-4` to `am-6` are a build that is stuck or asking something the person can't answer, with a delivered kit present; they must reach Amend, not Audit. `neg-15` is the must-not-trigger partner: a TypeError with no kit is a code fix, not Blueprint's.
- The target is in the build brief's REQ-1: at least 90% overall, each route at least 85%, and at most 1 of the negatives triggering.

## Behaviour evals

A behaviour eval runs a whole Blueprint conversation in the same kind of temporary folder, with the persona file as the person:

```bash
python3 evals/run_behaviour.py --prompt "I have an idea for a small script that ..." --keep
```

- Blueprint runs as one `claude -p` session, resumed for each reply, with the same isolation as the routing runs; it may edit files inside the folder, and Bash may run only `python3` (its check scripts).
- The person is a separate `claude -p` process in its own empty folder, with no skills and no tools; its system prompt is the persona file, and it sees only Blueprint's latest message.
- The run stops when Blueprint has written a kit (`kit-lite.md` or `START-HERE.md` (`00-START-HERE.md` before 3.0.1), in the eval folder or in the scratchpad folder Claude Code gives that session) and either asks nothing more or has just answered the person's approval of it (the hand-off), or after `--rounds` replies (default 14), then runs `check_kit.py` on the kit and reports whether "Keeping it running" is filled. `--fixture` copies a fixture in, for routes that need a project; `--repo-ref REF` instead copies every tracked file of this repository at that commit in as `repo-copy/`, for Operate on this repository; the first message then tells Blueprint that the copy leaves out the git history, so a missing `.git` folder is not read as a project without history. The runner also lists every command and web lookup the run used. Public web search and fetch are allowed (`WebSearch` and `WebFetch` are on the allowlist), because looking up public advisory, version or licence data by package name is research, not acting on the project's behalf; an Audit is expected to check advisories. The run still fails on any network command in Bash (`curl`, `wget`, `gh`, `git`, `ssh`, `pip`, `npm` or a Python network module, which covers every install) and on a `WebFetch` to the project's own services: `localhost` or a private address, or a host that a URL in the fixture's files names, unless that host is a public registry or advisory source (`PUBLIC_DATA_HOSTS` in `run_behaviour.py`, such as `pypi.org`, `osv.dev` or `github.com`). `--no-web` restores the rule before 3.2: no web tools at all. It flags, without failing, files Blueprint wrote outside the eval folder and its scratchpad (Write and Edit paths, and Bash redirections to an absolute path); other ways of writing are not detected.

The same file names are found before and after 3.0.1: the kit is the folder holding `kit-lite.md`, `START-HERE.md` or `00-START-HERE.md`, and "Keeping it running" is read from `kit-lite.md` or the build brief (`build-brief.md`, `02-build-brief.md`, either one in `docs/`, or brief parts such as `build-brief-1.md`). The run prints the words in each kit file. Without `--keep`, the eval folder, its scratchpad and the transcript are deleted; with it, their paths are printed. The runner exits 1 when any run failed.

### Behaviour eval options

| Option | What it does |
|---|---|
| `--runs N` | Repeats the whole run N times (default 1) and ends with the spread: runs passed, routes named, cost, and words per kit file, min to max. One run is an anecdote; three show whether a result is stable. |
| `--no-skill` | The baseline: the same prompt, persona and isolation with no Blueprint installed. Isolation then requires that no blueprint skill is listed. The conversation also ends when a reply asks nothing more. Without a kit the run fails, and it reports the words of every file written, so Blueprint can be compared with no skill, not only with Blueprint 2. |
| `--model M` | Passed to `claude --model` for Blueprint (an alias such as `opus`, `sonnet` or `haiku`, or a full model name); the person uses it too unless `--person-model` is given. Keep the person on one model when comparing Blueprint across models. The model each run used is printed. |
| `--person-model M` | The simulated person's model. |
| `--allow-subagents` | Adds Claude Code's subagent tool (`Agent`; older versions call it `Task`) to the allowlist, so the fresh-reviewer steps run as real fresh reviews instead of labelled self-reviews. The run prints the tools listed at start and the number of subagent calls; check the tools line shows `Agent`. |
| `--coded` | The project is software: `check_kit.py` runs with `--coded`, so a kit without a security baseline fails the run. Without it, a kit with `tasks.json` only gets a note. |
| `--persona NAME` | `you-decide` (default), `disagrees` or `goes-quiet`, or a path to another persona file. The person is told its reply number. |
| `--no-web` | Takes `WebSearch` and `WebFetch` off the allowlist and fails the run on any web tool. |

What each persona tests:

- **you-decide:** the whole route runs without a human. Pass: check_kit passes and "Keeping it running" is filled.
- **disagrees:** Blueprint says why once, records the person's choice and its own dissent, and designs around the choice (`03-questioning.md`, rule 7). The runner scores the kit as usual; whether the kit kept the person's choice is scored by reading it, so note it in the result summary.
- **goes-quiet:** the person answers part of the first question, then gives a wrong answer, then replies `[no reply]`, which ends the conversation. Before a kit, the run passes when Blueprint saved a state file (a file with the state heading or a `Route:` line) that the person could resume from. Read the transcript too: Blueprint should have noticed the gap and the contradiction, not recorded guesses as the person's answers.

## Build evals

Every other eval measures documents. `run_build.py` measures what a builder makes from them, against a plan made without Blueprint:

```bash
python3 evals/run_build.py --kit /tmp/blueprint-eval-behaviour-.../kit --coded --keep
python3 evals/run_build.py --no-skill-plan plan.md --coded --keep
```

- **The kit run:** `--kit` takes a kit folder that a behaviour run kept (`run_behaviour.py --keep` prints where), or a fixture under `evals/fixtures/` (tracked files only). The runner puts it in a new, empty temporary folder as the kit's own next steps say for Claude Code, keeps `START-HERE.md` and the state file aside, and sends the kit's own first message. From 3.2 that message has the builder set the kit out (the instructions file renamed `CLAUDE.md`, the rest moved into `docs/` unchanged), so the files go in as delivered and the runner reports whether `CLAUDE.md` and `docs/` exist at the end; for older kits the runner does the renaming and moving itself.
- **The baseline:** `--no-skill-plan FILE` runs the same steps from a plain plan, such as the plan a `run_behaviour.py --no-skill` run wrote or one Claude Code's plan mode wrote. The plan goes in as `docs/plan.md`, with no `CLAUDE.md`, and the builder gets a plain first message ("I planned this project … build it").
- **The builder** is one `claude -p` session, resumed every turn, with the routing runs' isolation and no skills. It works as the kit's coordinator, so the subagent tool (`Agent`) is on its allowlist, with file edits, any command, installs and public web search and fetch. **Local and test setups only:** deploys, pushes and real-account CLIs are denied (`DENY_COMMANDS`), the environment carries no tokens or cloud keys, and git runs with an empty config, a test identity and no credentials. Every such command the builder tries is listed, and the run is marked incomplete.
- **The person** (`personas/build-person.md`) answers the builder after each turn: only at checkpoints, never reading code, choosing the recommended option, keeping everything local, and saying "carry on" to a report that asks nothing. Those "carry-on nudges" are counted apart, because a builder that runs with minimal input after hand-off needs none.
- **Stopping:** when every builder task in `docs/tasks.json` is done, or the builder offers the final review after saying all tasks are done; otherwise after `--turns` (default 30), `--budget` USD (default 30) or `--minutes` (default 240).
- **The final review** then runs fresh (no resume, Edit off, no subagents): the kit's `docs/final-review.md` when there is one, plus the skill's final-review procedure for every run, and under `--coded` the ten security-baseline items from `software-design-detail.md`, so kit and baseline are reviewed the same way. It writes `review-report.md` and ends with `FIX-NOW: n` and `SECURITY-BASELINE: m of k`.

It reports person turns (answers and carry-on nudges), builder turns, subagent calls, dollars (builder, person, reviewer), minutes to the first passing check (a watcher polls every 15 seconds for a task done with evidence or a new "passed" line or ticked box in a Markdown file, so it is coarse), Fix-now findings and security-baseline items met. Exit 0 means every run reached the final review with its counts and nothing irreversible was tried; the counts are for comparison, not pass marks. A model persona is not a real non-coder, so read the transcripts too. The review that proposed it estimated 20 to 60 USD per comparison (one kit run and one baseline run); that is an estimate until the first runs are recorded in `results/`.

### Recommended matrix for each release

Fourteen behaviour runs, the build comparison (8 build runs) and the routing set: expect roughly 100 to 280 USD: the behaviour runs and routing set about 20 to 40 USD, judging by the 2026-11-05 costs (routing set about 3 USD, an Audit behaviour run on Sonnet about 1.3 USD), and the four build comparisons the rest, an estimate. Opus-class runs cost more.

| Run | Command (add `--prompt`, and `--fixture` where the route needs one) | Why |
|---|---|---|
| Routing set, once | `run_routing.py --mode v3 --out evals/results/<version>.md` | Every route is reached; negatives don't trigger |
| New, medium, ×3 on the default model (Sonnet-class) | `run_behaviour.py --coded --runs 3` | Stability of the main route, and kit word counts for the word caps |
| New, medium, once on an Opus-class model | `run_behaviour.py --coded --model opus --person-model sonnet` | The skill is likely run on Opus in practice |
| New, medium, once on a Haiku-class model | `run_behaviour.py --coded --model haiku --person-model sonnet` | The floor: what a small model does with the skill |
| New, medium, once with no skill | `run_behaviour.py --no-skill` | The baseline Blueprint must beat |
| New, medium, once with subagents | `run_behaviour.py --coded --allow-subagents` | Fresh-eyes reviews as designed, not self-reviews |
| One run per new persona | `run_behaviour.py --persona disagrees`, then `--persona goes-quiet` | Real people disagree and give up |
| Audit, Redesign and Operate, once each | `--fixture evals/fixtures/audit-sample`, `--fixture evals/fixtures/redesign-sample --coded --screens`, `--repo-ref HEAD` | Each route end to end, with the project unchanged; Audit with public web lookups allowed (the default) |
| Lightning mode, once | `run_behaviour.py --coded --prompt "Lightning mode: I want a script that renames my photos by date"` | No question rounds, every assumption recorded, a kit that passes `check_kit.py`, and one final message listing the assumptions |
| Stuck build, once | `run_behaviour.py --fixture evals/fixtures/delivered-kit --prompt "<a stuck-build message, as in am-4>"` | Routes to Amend, asks for the builder's last message, the progress log and the failing check in one message, and ends with a paste-ready reply for the builder |
| Build from the kit against the baseline, 2 runs each | `run_build.py --kit <a kept kit> --coded --runs 2`, then `run_build.py --no-skill-plan <the --no-skill run's plan> --coded --runs 2`, for one small and one medium project | The core question: does a kit build better, with fewer person turns, than a plain plan? |

New medium runs use a software idea, so they add `--coded`: without it a kit missing its security baseline would still pass. `--screens` needs a fixture with pages to capture, so it goes on Redesign runs (`--coded --screens`), not on New. Drop `--coded` for a prompt that isn't software, such as a business plan.

Record each in `evals/results/` with the date, model, pass count of N and the word-count spread; for build runs, every count above for the kit and the baseline side by side.

Redesign evals add `--screens`. Before the first reply, the runner itself (not the Blueprint session) opens every page of the fixture copy from its local file, with web requests blocked, and saves screenshots at 375 and 1,280 px wide in `screens/` in the eval folder, such as `screens/index-375.png`. The first message tells Blueprint where they are, as if the person had attached them, so the run tests the route's inventory with screenshots the person supplies. The runner then runs `check_kit.py --screens` and fails the run unless the screenshots exist and Blueprint cites both widths (it reads them, or names them in a reply or a file it writes).

The screenshots come from Python Playwright with its Chromium build, installed outside the repository on the eval machine of 2026-11-05 (build brief D-15); nothing is added to `skill/` or the repository. On a machine without it, install Playwright and Chromium in a temporary virtual environment outside the clone and start the runner with that environment's `python3`. Blueprint gets no extra tool rights for this: its Bash stays limited to `python3`, because widening an unattended agent's rights is a risk the eval doesn't need. In session 6's first two runs Blueprint tried to capture screens itself with an installed headless browser; the first was refused by the permission rules and the second hung, so both runs planned without screenshots.

Bash in a behaviour run is allowed only `python3`, but Claude Code also runs some commands without asking: read-only ones such as `ls`, `cat`, `find` or `which` (seen in sessions 5 and 6), and, because of `--permission-mode acceptEdits`, file commands such as `mkdir` and `cp` inside the eval folder (session 6, where Blueprint copied screenshots into its kit). Tightening this would need a deny list per command, so the runner records them instead: it lists every command, fails the run on any network command or call to the project's own services, and fails a fixture run whose project files changed.

Audit, Redesign and Operate evals run their whole route this way. After each run, the fixture's file checksums must be unchanged, because those routes never edit the project; with `--fixture`, the runner compares them and fails the run if any file was added, removed or changed. Audit results are scored against `keys/audit-sample.md`: a finding the key doesn't list counts against the run only if a reviewer reading the fixture judges it false.
