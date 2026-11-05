# Evals

How Blueprint is tested. Nothing here ships in the skill zip.

## What is here

| Path | What it is |
|---|---|
| `routing.jsonl` | The routing set: prompts with the route each should reach, or `none` when Blueprint must not trigger. One JSON object per line: `id`, `prompt`, `expected_route` (new, audit, redesign, operate, amend, none), `should_trigger` (true or false), and `fixture` (a path under `evals/fixtures/`) when the prompt needs files. |
| `run_routing.py` | Runs the routing set with headless Claude Code and scores it. |
| `run_behaviour.py` | Runs one whole Blueprint conversation with the simulated person, then checks the kit it writes. |
| `fixtures/` | Small invented projects and kits the evals copy into their temporary folders. |
| `keys/` | Answer keys. They stay outside `fixtures/`, because eval runs copy only the fixture, so the run never sees its key. |
| `personas/you-decide.md` | The simulated person for behaviour evals: answers "You decide" to every question and "approve" at every approval, so a full run needs no human. |
| `results/` | Summaries of eval runs: pass counts, date and model. Never transcripts of private runs. |

Every prompt and fixture is invented and generic.

## Fixtures

| Fixture | Used for |
|---|---|
| `v2-state.md` | A Blueprint 2 state file at phase 3 with no Route line; resume prompts must continue it as route New |
| `delivered-kit/` | A delivered small kit with its state file; Amend prompts change it |
| `empty-repo/` | A repository with only a title README; routes to New |
| `kit-good/` | A small kit that passes `check_kit.py`, including a filled "Keeping it running" section |
| `kit-missing-upkeep/` | The same kit without "Keeping it running"; passes Blueprint 2's check and must fail Blueprint 3's, which requires the section |
| `audit-sample/` | A tiny command-line project with planted problems for Audit evals; its key is `keys/audit-sample.md` |
| `redesign-sample/` | A two-page static site with known contrast failures for Redesign evals; its key is `keys/redesign-sample.md` |

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
- `--ids new-1,aud-2` runs only some prompts; `--jobs` sets how many run at once (default 4); `--keep` keeps the folders and transcripts for reading.
- Routing needs only the first reply, so keep `--max-turns` small: the v2 baseline used 3, so a run that looks at the folder first still gets to trigger; v3 may need 4 to name its route.
- Each run uses the account Claude Code is signed in with. The runner prints the cost Claude Code reports; the 50-prompt set cost about 2 USD on 2026-11-05.

### Scoring

- **Triggered:** the run calls the Skill tool with `blueprint`, or the prompt starts with `/blueprint` (the host loads the skill directly).
- **v3:** a prompt that should trigger passes when Blueprint triggers and names the expected route in a `Route: name` line, in its reply or in a state file it writes. A negative passes when Blueprint does not trigger.
- **v2 baseline:** Blueprint 2 has no routes, so a prompt that should trigger passes when Blueprint 2 triggers, and a negative passes when it does not. Route accuracy is measured from v3 only.
- The target is in the build brief's REQ-1: at least 90% overall, each route at least 85%, and at most 1 of the negatives triggering.

## Behaviour evals

A behaviour eval runs a whole Blueprint conversation in the same kind of temporary folder, with the persona file as the person:

```bash
python3 evals/run_behaviour.py --prompt "I have an idea for a small script that ..." --keep
```

- Blueprint runs as one `claude -p` session, resumed for each reply, with the same isolation as the routing runs; it may edit files inside the folder, and Bash may run only `python3` (its check scripts).
- The person is a separate `claude -p` process in its own empty folder, with no skills and no tools; its system prompt is the persona file, and it sees only Blueprint's latest message.
- The run stops when Blueprint has written a kit (`kit-lite.md` or `00-START-HERE.md`, in the eval folder or in the scratchpad folder Claude Code gives that session) and either asks nothing more or has just answered the person's approval of it (the hand-off), or after `--rounds` replies (default 14), then runs `check_kit.py` on the kit and reports whether "Keeping it running" is filled. `--fixture` copies a fixture in, for routes that need a project; `--repo-ref REF` instead copies every tracked file of this repository at that commit in as `repo-copy/`, for Operate on this repository; the first message then tells Blueprint that the copy leaves out the git history, so a missing `.git` folder is not read as a project without history. The runner also lists every command and web tool the run used, and fails it on any web tool or network command, because these routes make no network call on the project's behalf without asking. It flags, without failing, files Blueprint wrote outside the eval folder and its scratchpad (Write and Edit paths, and Bash redirections to an absolute path); other ways of writing are not detected.

Redesign evals add `--screens`. Before the first reply, the runner itself (not the Blueprint session) opens every page of the fixture copy from its local file, with web requests blocked, and saves screenshots at 375 and 1,280 px wide in `screens/` in the eval folder, such as `screens/index-375.png`. The first message tells Blueprint where they are, as if the person had attached them, so the run tests the route's inventory with screenshots the person supplies. The runner then runs `check_kit.py --screens` and fails the run unless the screenshots exist and Blueprint cites both widths (it reads them, or names them in a reply or a file it writes).

The screenshots come from Python Playwright with its Chromium build, installed outside the repository on the eval machine of 2026-11-05 (build brief D-15); nothing is added to `skill/` or the repository. On a machine without it, install Playwright and Chromium in a temporary virtual environment outside the clone and start the runner with that environment's `python3`. Blueprint gets no extra tool rights for this: its Bash stays limited to `python3`, because widening an unattended agent's rights is a risk the eval doesn't need. In session 6's first two runs Blueprint tried to capture screens itself with an installed headless browser; the first was refused by the permission rules and the second hung, so both runs planned without screenshots.

Bash in a behaviour run is allowed only `python3`, but Claude Code also runs some commands without asking: read-only ones such as `ls`, `cat`, `find` or `which` (seen in sessions 5 and 6), and, because of `--permission-mode acceptEdits`, file commands such as `mkdir` and `cp` inside the eval folder (session 6, where Blueprint copied screenshots into its kit). Tightening this would need a deny list per command, so the runner records them instead: it lists every command, fails the run on any network command or web tool, and fails a fixture run whose project files changed.

Audit, Redesign and Operate evals run their whole route this way. After each run, the fixture's file checksums must be unchanged, because those routes never edit the project; with `--fixture`, the runner compares them and fails the run if any file was added, removed or changed. Audit results are scored against `keys/audit-sample.md`: a finding the key doesn't list counts against the run only if a reviewer reading the fixture judges it false.
