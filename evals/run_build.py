#!/usr/bin/env python3
"""Run one build-from-kit eval: a fresh builder works from a kit, then a fresh final review.

Usage:
  python3 evals/run_build.py --kit PATH [options]
  python3 evals/run_build.py --no-skill-plan FILE [options]

This is the outcome eval (review-2 item B1). Every other eval measures
documents; this one measures what a builder makes from them, against a
plain plan with no Blueprint.

Options:
  --kit PATH            a kit folder: one a behaviour run kept (run_behaviour.py
                        --keep prints it) or a fixture such as
                        evals/fixtures/kit-good (taken from tracked files only)
  --no-skill-plan FILE  the baseline: a plain plan instead of a kit, such as
                        the plan a run_behaviour.py --no-skill run wrote or
                        one Claude Code's plan mode wrote; it goes in as
                        docs/plan.md, with no CLAUDE.md, and the builder gets
                        a plain first message (BASELINE_FIRST below)
  --persona NAME        the simulated person: a name in evals/personas/
                        (default build-person) or a file
  --turns N             most builder turns (claude -p calls, resumed) before
                        stopping (default 30)
  --max-turns N         tool turns per builder turn (default 80)
  --budget USD          stop after the turn that passes this cost (default 30)
  --minutes M           stop after the turn that passes this wall time (default 240)
  --model M             model for the builder and the reviewer (default:
                        Claude Code's default); also the person's unless
                        --person-model is given
  --person-model M      model for the simulated person
  --skill-ref REF       git ref whose skill/ gives the review procedure and
                        the security baseline both runs are reviewed against
                        (default HEAD)
  --coded               the project is software: the review also scores the
                        ten security-baseline items
  --runs N              repeat the whole run N times (default 1)
  --keep                keep the project folders and transcripts

How it works (see evals/README.md, "Build evals"):
  - The project folder is a new, empty temporary folder outside the clone.
    The kit goes in as its own next steps say for Claude Code, and the
    builder gets the kit's own first message (from START-HERE.md, or the
    small kit's setup line; DEFAULT_FIRST when none is found).
    START-HERE.md and the state file stay aside. From 3.2 that message has
    the builder set the kit out (rename the instructions file to CLAUDE.md,
    move the rest into docs/), so the files go in as delivered and the
    runner reports whether CLAUDE.md and docs/ exist at the end. For older
    kits the runner does it: the instructions file (project-instructions.md,
    its numbered name, or kit-lite.md) becomes CLAUDE.md and every other
    kit file goes into docs/ unchanged.
  - The builder runs as one `claude -p` session in that folder, resumed for
    every turn, with the routing runs' isolation (project settings only, a
    tool allowlist, no MCP servers, no browser, a clean environment) and no
    skills. It works as the kit's coordinator: the subagent tool is on the
    allowlist so it can hand tasks to fresh workers, and it may edit files,
    run any command and install packages, because building needs them.
    Deploys and anything that reaches a real account are denied
    (DENY_COMMANDS), its environment carries no tokens or cloud keys, and
    git uses an empty config with a test identity and no credentials. Local
    and test setups only.
  - After each builder turn, the person (a separate `claude -p` with no
    tools, in its own empty folder, the persona as its system prompt)
    answers the builder's latest message. The persona answers only at
    checkpoints, refuses to read code, and says "carry on" to a report that
    asks nothing; those are counted apart ("carry-on nudges"), because a
    builder that runs with minimal input needs none.
  - The run stops when the builder is finished (every builder task in
    docs/tasks.json is done, or its message offers the final review after
    saying all tasks are done), or after --turns, --budget or --minutes.
  - Then a fresh reviewer (`claude -p`, no resume, the same isolation, no
    subagents, Edit off) runs the final review: the kit's
    docs/final-review.md when there is one, and the skill's final-review
    procedure, with the ten security-baseline items under --coded, for
    both runs, so kit and baseline are reviewed the same way. It ends with
    "FIX-NOW: n" and "SECURITY-BASELINE: m of 10" lines, which the runner
    reads.
  - Minutes to the first passing check: a watcher polls the folder every
    POLL seconds and records the first time a task in docs/tasks.json is
    done with evidence, or a Markdown file gains a line that records a
    pass (a "passed" result or a ticked box). It is coarse by POLL.

Reports per run: person turns (answers and carry-on nudges), builder turns,
subagent calls, dollars (builder, person, reviewer), minutes to the first
passing check, total minutes, Fix-now findings, security-baseline items met,
and every denied irreversible command the builder tried.

Exit 0 when every run reached the final review, the review gave its counts,
isolation held and no irreversible command was tried; 1 otherwise. The
counts are for comparing a kit with the baseline, not pass marks.
Python 3 standard library only. Needs git and the claude command.
"""
import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import threading
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import run_routing as rr  # noqa: E402
import run_behaviour as rb  # noqa: E402

BUILDER_TOOLS = "Read,Glob,Grep,Bash,Write,Edit,WebSearch,WebFetch," + rb.SUBAGENT_TOOL
REVIEW_TOOLS = "Read,Glob,Grep,Bash,Write,WebSearch,WebFetch"
# Denied for every session: deploys, publishing, pushes and real-account CLIs.
# IRREVERSIBLE_RE finds the same commands at the start of a command line or
# after ; | & ( `, so the runner can report attempts the deny list refused.
DENY_COMMANDS = [
    "Bash(git push:*)", "Bash(git remote add:*)", "Bash(gh:*)", "Bash(ssh:*)", "Bash(scp:*)",
    "Bash(npm publish:*)", "Bash(npx vercel:*)", "Bash(vercel:*)", "Bash(netlify:*)",
    "Bash(npx netlify:*)", "Bash(firebase:*)", "Bash(npx firebase:*)", "Bash(fly:*)",
    "Bash(flyctl:*)", "Bash(heroku:*)", "Bash(wrangler:*)", "Bash(npx wrangler:*)",
    "Bash(supabase link:*)", "Bash(npx supabase link:*)", "Bash(aws:*)", "Bash(gcloud:*)",
    "Bash(az:*)", "Bash(docker push:*)", "Bash(twine:*)", "Bash(stripe:*)",
]
IRREVERSIBLE_RE = re.compile(
    r"(?:^|[;|&(`])\s*(?:npx\s+|sudo\s+)?(?:git\s+push|git\s+remote\s+add|gh|ssh|scp|npm\s+publish|vercel|netlify|"
    r"firebase|flyctl|fly|heroku|wrangler|supabase\s+link|aws|gcloud|az|docker\s+push|twine|stripe)"
    r"(?=$|[\s;|&)`])", re.M)
# Environment variables that could reach a real account; the claude login stays.
SECRET_ENV_RE = re.compile(r"TOKEN|SECRET|PASSWORD|API_KEY|ACCESS_KEY|CREDENTIAL|^AWS_|^GH_|"
                           r"^GITHUB_|^NPM_|^GOOGLE_|^AZURE_|^VERCEL|^NETLIFY|^STRIPE", re.I)
KEEP_ENV = {"ANTHROPIC_API_KEY", "ANTHROPIC_AUTH_TOKEN", "CLAUDE_CODE_OAUTH_TOKEN"}
INSTRUCTION_NAMES = ("project-instructions.md", "01-project-instructions.md", "kit-lite.md", "CLAUDE.md")
ASIDE_NAMES = ("START-HERE.md", "00-START-HERE.md", "state.md")  # the person's, not the builder's
DEFAULT_FIRST = "Let's start. Read the progress log and the task list, tell me where things stand, and begin."
BASELINE_FIRST = ("I planned this project, and the plan is in docs/plan.md. Please build it, checking "
                  "your work as you go. Ask me only when you need something from me.")
QUOTE_RE = re.compile(r"[\"“]([^\"”\n]{12,})[\"”]")
FINISHED_RE = re.compile(r"\bfinal review\b", re.I)
ALL_DONE_RE = re.compile(r"\b(all|every)\b[^.\n]{0,60}\b(tasks?|done|complete[d]?)\b", re.I)
PASS_LINE_RE = re.compile(r"\bpass(?:ed|es)?\b|\[x\]|✅", re.I)
POLL = 15
SKIP_DIRS = {".git", "node_modules", ".venv", "venv", "__pycache__", ".claude", "dist", "build"}


def build_env(home):
    """The routing runs' clean environment, without tokens or cloud keys, and
    with git confined to an empty config and a test identity."""
    env = {k: v for k, v in rr.clean_env().items() if k in KEEP_ENV or not SECRET_ENV_RE.search(k)}
    config = os.path.join(home, "gitconfig")
    with open(config, "w", encoding="utf-8") as f:
        f.write("[user]\n\tname = Build Eval\n\temail = build-eval@example.invalid\n"
                "[init]\n\tdefaultBranch = main\n[credential]\n\thelper =\n")
    env.update({"GIT_CONFIG_GLOBAL": config, "GIT_CONFIG_NOSYSTEM": "1", "GIT_TERMINAL_PROMPT": "0"})
    return env


def kit_source(path, stage):
    """The kit folder to copy: a fixture inside the clone comes from tracked
    files only (git archive), like every other eval; any other path as it is."""
    real = os.path.realpath(path)
    if not os.path.isdir(real):
        sys.exit(f"usage: --kit {path} is not a folder")
    if rr.outside_repo(real):
        return real
    rel = os.path.relpath(real, rr.REPO)
    if not rel.startswith(os.path.join("evals", "fixtures") + os.sep):
        sys.exit(f"usage: --kit {path} is inside the clone but not under evals/fixtures/")
    rr.git_archive("HEAD", rel, stage)
    return os.path.join(stage, rel)


def is_state_file(path):
    if os.path.basename(path) in ASIDE_NAMES:
        return True
    if path.endswith(".md"):
        return bool(rb.STATE_RE.search(open(path, encoding="utf-8", errors="replace").read()))
    return False


def first_message(kit):
    """The first message the kit's next steps give for Claude Code: a quoted
    message under "First message" in START-HERE.md, or after "First
    message" or "send:" in a small kit's setup line. A message that sets
    the kit out (it names CLAUDE.md) is preferred, since that is the Claude
    Code one; DEFAULT_FIRST when none is found."""
    found = []
    for name in ("START-HERE.md", "00-START-HERE.md"):
        p = os.path.join(kit, name)
        if os.path.isfile(p):
            m = re.search(r"^#+\s*First message\s*$(.*?)(?=^#|\Z)",
                          open(p, encoding="utf-8").read(), re.M | re.S)
            if m:
                found += QUOTE_RE.findall(m.group(1))
                quote = " ".join(ln.lstrip("> ").strip() for ln in m.group(1).splitlines()
                                 if ln.startswith(">")).strip()
                if quote and not found:
                    found.append(quote)
    for name in INSTRUCTION_NAMES:
        p = os.path.join(kit, name)
        if os.path.isfile(p):
            for m in re.finditer(r"(?:First message|send):?\**\s*" + QUOTE_RE.pattern,
                                 open(p, encoding="utf-8").read()):
                found.append(m.group(1))
    found = [f.strip() for f in found if f.strip()]
    return next((f for f in found if "CLAUDE.md" in f), found[0] if found else DEFAULT_FIRST)


def lay_out(kit, project, by_builder):
    """Put the kit in place as its next steps say. by_builder: the first
    message has the builder set the files out, so every kit file except
    START-HERE.md and the state file goes into the folder as delivered;
    otherwise (kits before 3.2) the runner renames the instructions file to
    CLAUDE.md and moves the rest into docs/. Returns (instructions file,
    files kept aside)."""
    names = sorted(os.listdir(kit))
    instr = next((n for n in INSTRUCTION_NAMES if n in names), None)
    if not instr:
        sys.exit(f"usage: no instructions file ({', '.join(INSTRUCTION_NAMES)}) in {kit}")
    docs = os.path.join(project, "docs")
    if not by_builder:
        os.makedirs(docs, exist_ok=True)
    aside = []
    for name in names:
        src = os.path.join(kit, name)
        if os.path.isfile(src) and is_state_file(src):
            aside.append(name)
        elif by_builder:
            (shutil.copytree if os.path.isdir(src) else shutil.copy2)(src, os.path.join(project, name))
        elif name == instr:
            shutil.copy2(src, os.path.join(project, "CLAUDE.md"))
        elif name == "docs" and os.path.isdir(src):
            shutil.copytree(src, docs, dirs_exist_ok=True)
        elif os.path.isdir(src):
            shutil.copytree(src, os.path.join(docs, name))
        else:
            shutil.copy2(src, os.path.join(docs, name))
    return instr, aside


def project_files(project, suffix):
    for base, dirs, files in os.walk(project):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for f in files:
            if f.endswith(suffix):
                yield os.path.join(base, f)


def tasks(project):
    p = os.path.join(project, "docs", "tasks.json")
    try:
        return json.load(open(p, encoding="utf-8")).get("tasks") or []
    except (OSError, ValueError, AttributeError):
        return []


def pass_lines(project):
    """Lines that record a pass, keyed by their text (so a kit file the
    builder moves into docs/ adds nothing new), with where each is: tasks
    done with evidence, and Markdown lines with a pass or a ticked box."""
    found = {f"task {t.get('id')} done": "docs/tasks.json" for t in tasks(project)
             if str(t.get("status", "")).lower() == "done" and t.get("evidence")}
    for p in project_files(project, ".md"):
        try:
            text = open(p, encoding="utf-8", errors="replace").read()
        except OSError:
            continue
        for ln in text.splitlines():
            if PASS_LINE_RE.search(ln):
                found.setdefault(ln.strip(), os.path.relpath(p, project))
    return found


class Watcher(threading.Thread):
    """Records the minutes from the start to the first new pass line."""

    def __init__(self, project, start):
        super().__init__(daemon=True)
        self.project, self.start_time = project, start
        self.initial = pass_lines(project)
        self.first = None
        self.first_line = ""
        self.stop = threading.Event()

    def check(self):
        if self.first is None:
            now = pass_lines(self.project)
            new = sorted(set(now) - set(self.initial))
            if new:
                self.first = (time.time() - self.start_time) / 60
                self.first_line = f"{now[new[0]]}: {new[0]}"[:160]

    def run(self):
        while not self.stop.wait(POLL):
            self.check()


def finished(project, message):
    ts = [t for t in tasks(project) if str(t.get("done_by", "claude")).lower() in ("claude", "both")]
    if ts and all(str(t.get("status", "")).lower() == "done" for t in ts):
        return True
    return bool(FINISHED_RE.search(message) and ALL_DONE_RE.search(message))


def claude_turn(folder, text, session, tools, args, env, extra=()):
    cmd = ["claude", "-p", text, "--setting-sources", "project", "--tools", tools,
           "--strict-mcp-config", "--no-chrome", "--permission-mode", "acceptEdits",
           "--allowedTools", "Bash", "--max-turns", str(args.max_turns),
           "--output-format", "stream-json", "--verbose", *extra,
           "--disallowedTools", "Projects", *DENY_COMMANDS]
    if session:
        cmd += ["--resume", session]
    if args.model:
        cmd += ["--model", args.model]
    try:
        out = subprocess.run(cmd, cwd=folder, stdin=subprocess.DEVNULL, env=env,
                             capture_output=True, text=True, timeout=3600).stdout
    except subprocess.TimeoutExpired as e:
        out = e.stdout.decode() if isinstance(e.stdout, bytes) else (e.stdout or "")
    with open(rb.transcript_path(folder), "a", encoding="utf-8") as f:
        f.write(out)
    r = rr.parse(out, text, tools)
    # No skill is installed: isolation holds when no blueprint skill is listed
    # and every tool is on the allowlist.
    allowed = {t.strip() for t in tools.split(",") if t.strip()}
    extra_tools = sorted(set(r["tools"]) - allowed)
    named = [s for s in r["skills"] if s.endswith("blueprint")]
    r["isolation_ok"] = not named and not extra_tools and bool(r["tools"])
    r["isolation_note"] = "" if r["isolation_ok"] else (
        f"blueprint skills listed: {named}; tools beyond the allowlist: {extra_tools}")
    sid, last = session, ""
    for line in out.splitlines():
        try:
            d = json.loads(line)
        except ValueError:
            continue
        if d.get("type") == "system" and d.get("subtype") == "init":
            sid = d.get("session_id") or sid
        elif d.get("type") == "result":
            last = d.get("result") or last
    if not last and r["texts"]:
        last = r["texts"][-1]
    return sid, last, r


def person_turn(home, persona, message, args, number, env):
    prompt = ("The builder working on your project just wrote the message below. Reply as the "
              "person, following your instructions exactly. Reply with the person's words only.\n"
              f"This is your reply number {number}.\n\n--- The builder's message ---\n" + message)
    cmd = ["claude", "-p", prompt, "--setting-sources", "project", "--tools", "",
           "--strict-mcp-config", "--no-chrome", "--system-prompt", persona,
           "--max-turns", "1", "--output-format", "json"]
    if args.person_model or args.model:
        cmd += ["--model", args.person_model or args.model]
    proc = subprocess.run(cmd, cwd=home, stdin=subprocess.DEVNULL, env=env,
                          capture_output=True, text=True, timeout=600)
    try:
        d = json.loads(proc.stdout)
        return (d.get("result") or "").strip() or "OK, carry on.", d.get("total_cost_usd") or 0.0
    except ValueError:
        return "OK, carry on.", 0.0


def review_prompt(stage, coded):
    procedure = open(os.path.join(stage, "skill", "templates", "kit-04-final-review.md"),
                     encoding="utf-8").read()
    text = ("You are the final reviewer of this project, not its builder. Whatever CLAUDE.md says "
            "about building, you fix nothing: you run, read and report. If docs/final-review.md "
            "exists, follow it. Use the general procedure below as well, skipping its placeholders "
            "(text in angle brackets), so every project is reviewed the same way.\n\n"
            "--- General procedure ---\n" + procedure)
    if coded:
        detail = open(os.path.join(stage, "skill", "references", "software-design-detail.md"),
                      encoding="utf-8").read()
        m = re.search(r"^## Security baseline\s*$(.*?)(?=^## )", detail, re.M | re.S)
        text += ("\n\n--- Security baseline: judge each of the ten items as met (the build applies it, "
                 "with evidence you checked), not applicable (one line why) or not met ---\n"
                 + (m.group(1).strip() if m else "(not found in the skill under test)"))
    text += ("\n\nWrite your report to review-report.md in this folder. End your reply with exactly two "
             "lines: 'FIX-NOW: <number of Fix now findings>' and 'SECURITY-BASELINE: <items met> of "
             "<items that apply>' (or 'SECURITY-BASELINE: n/a' when the project has no code).")
    return text


def review_counts(project, message):
    text = message
    report = os.path.join(project, "review-report.md")
    if os.path.isfile(report):
        text += "\n" + open(report, encoding="utf-8", errors="replace").read()
    m = re.search(r"FIX-NOW:\s*(\d+)", text)
    fix_now = int(m.group(1)) if m else None
    if fix_now is None and os.path.isfile(report):
        fix_now = sum(1 for ln in text.splitlines() if ln.startswith("|") and re.search(r"\bFix now\b", ln))
    m = re.search(r"SECURITY-BASELINE:\s*(\d+)\s*of\s*(\d+)", text)
    baseline = f"{m.group(1)} of {m.group(2)}" if m else (
        "n/a" if re.search(r"SECURITY-BASELINE:\s*n/?a", text, re.I) else None)
    return fix_now, baseline


def run_once(args, stage, persona, number):
    project = tempfile.mkdtemp(prefix="blueprint-build-")
    if not rr.outside_repo(project):
        sys.exit(f"FAIL: project folder {project} is inside the clone; set TMPDIR elsewhere")
    home = tempfile.mkdtemp(prefix="blueprint-build-person-")
    env = build_env(home)
    transcript = rb.transcript_path(project)
    print(f"\n===== Run {number} of {args.runs} =====\nProject folder: {project}")
    if args.kit:
        text = first_message(args.kit_dir)
        by_builder = "CLAUDE.md" in text
        instr, aside = lay_out(args.kit_dir, project, by_builder)
        print(f"Kit: {args.kit}; {instr} -> CLAUDE.md "
              + ("by the builder, as the first message asks" if by_builder else "by the runner")
              + f"; kept aside: {', '.join(aside) or 'none'}")
    else:
        os.makedirs(os.path.join(project, "docs"))
        shutil.copy2(args.no_skill_plan, os.path.join(project, "docs", "plan.md"))
        text = BASELINE_FIRST
        print(f"Baseline plan: {args.no_skill_plan} -> docs/plan.md (no CLAUDE.md)")
    print("Files in place: " + ", ".join(sorted(os.path.relpath(p, project)
                                               for p in project_files(project, ""))))

    start = time.time()
    watcher = Watcher(project, start)
    watcher.start()
    session, cost, person_cost = None, 0.0, 0.0
    answers = nudges = builder_turns = 0
    isolation_ok, model, stop = True, "", f"turn limit ({args.turns})"
    for n in range(args.turns):
        print(f"\n--- person ({n}) ---\n{text[:600]}", flush=True)
        session, message, r = claude_turn(project, text, session, BUILDER_TOOLS, args, env)
        builder_turns += 1
        cost += r["cost"]
        model = r["model"] or model
        if r["skills"] or r["tools"]:
            isolation_ok &= r["isolation_ok"]
            if not r["isolation_ok"]:
                print(f"Isolation: {r['isolation_note']}")
        print(f"--- builder ({n}) ---\n{message[:1500]}", flush=True)
        watcher.check()
        if finished(project, message):
            stop = "builder finished"
            break
        if cost + person_cost > args.budget:
            stop = f"budget ({args.budget:.2f} USD)"
            break
        if (time.time() - start) / 60 > args.minutes:
            stop = f"time ({args.minutes} minutes)"
            break
        if n == args.turns - 1:
            break
        if rb.asks_more(message):
            answers += 1
        else:
            nudges += 1
        text, c = person_turn(home, persona, message, args, n + 1, env)
        person_cost += c
    build_minutes = (time.time() - start) / 60
    if args.kit:
        placed = os.path.isfile(os.path.join(project, "CLAUDE.md")) and os.path.isdir(os.path.join(project, "docs"))
        print(f"Kit set out (CLAUDE.md and docs/ present at the end): {placed}")
    watcher.check()
    watcher.stop.set()

    print("\n--- final review (fresh session) ---", flush=True)
    _, review_msg, rv = claude_turn(project, review_prompt(stage, args.coded), None, REVIEW_TOOLS, args, env)
    if rv["skills"] or rv["tools"]:
        isolation_ok &= rv["isolation_ok"]
    print(review_msg[:1500])
    fix_now, baseline = review_counts(project, review_msg)

    uses = rb.tool_uses(transcript)
    commands = [c for name, c in uses if name == "Bash"]
    subagents = sum(1 for name, _ in uses if name in ("Agent", "Task"))
    tried = [c for c in commands if IRREVERSIBLE_RE.search(rb.network_text(c))]
    total = cost + person_cost + rv["cost"]
    print("\n===== Build result =====")
    print(f"Plan: {'kit ' + args.kit if args.kit else 'baseline ' + args.no_skill_plan}; model: {model or 'default'}")
    print(f"Stopped: {stop}; builder turns: {builder_turns}; subagent calls: {subagents}; "
          f"Bash commands: {len(commands)}")
    print(f"Person turns: {answers + nudges} (answers {answers}, carry-on nudges {nudges})")
    print("Minutes to the first passing check: "
          + (f"{watcher.first:.1f} ({watcher.first_line})" if watcher.first is not None else "not seen"))
    print(f"Minutes building: {build_minutes:.1f}; with the review: {(time.time() - start) / 60:.1f}")
    print(f"Cost: builder {cost:.2f}, person {person_cost:.2f}, review {rv['cost']:.2f}, total {total:.2f} USD")
    print(f"Final review: Fix-now findings: {fix_now if fix_now is not None else 'not reported'}; "
          f"security baseline met: {baseline or 'not reported'}")
    print("Irreversible commands tried (denied): " + ("; ".join(c[:120] for c in tried) if tried else "none"))
    print(f"Isolation ok: {isolation_ok}")
    ok = (stop == "builder finished" and fix_now is not None and isolation_ok and not tried
          and (baseline is not None or not args.coded))
    print("RESULT COMPLETE" if ok else "RESULT INCOMPLETE")
    if args.keep:
        print(f"Kept: {project} and its transcript {transcript}")
    else:
        shutil.rmtree(project, ignore_errors=True)
        if os.path.isfile(transcript):
            os.remove(transcript)
    shutil.rmtree(home, ignore_errors=True)
    return {"ok": ok, "cost": total, "person": answers + nudges, "nudges": nudges,
            "first": watcher.first, "fix_now": fix_now, "baseline": baseline, "stop": stop,
            "minutes": build_minutes}


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    plan = ap.add_mutually_exclusive_group(required=True)
    plan.add_argument("--kit", help="a kit folder from a behaviour run or a fixture")
    plan.add_argument("--no-skill-plan", metavar="FILE", help="baseline: a plain plan file instead of a kit")
    ap.add_argument("--persona", default="build-person",
                    help="a name in evals/personas/ (default build-person) or a file")
    ap.add_argument("--turns", type=int, default=30, help="most builder turns")
    ap.add_argument("--max-turns", type=int, default=80, help="tool turns per builder turn")
    ap.add_argument("--budget", type=float, default=30.0, help="stop after passing this cost in USD")
    ap.add_argument("--minutes", type=float, default=240.0, help="stop after passing this wall time")
    ap.add_argument("--model", default="")
    ap.add_argument("--person-model", default="")
    ap.add_argument("--skill-ref", default="HEAD")
    ap.add_argument("--coded", action="store_true", help="also score the ten security-baseline items")
    ap.add_argument("--runs", type=int, default=1)
    ap.add_argument("--keep", action="store_true")
    args = ap.parse_args()
    if args.runs < 1 or args.turns < 1 or args.max_turns < 1:
        ap.error("--runs, --turns and --max-turns must be at least 1")
    if args.budget <= 0 or args.minutes <= 0:
        ap.error("--budget and --minutes must be above 0")
    if args.no_skill_plan and not os.path.isfile(args.no_skill_plan):
        ap.error(f"--no-skill-plan {args.no_skill_plan} is not a file")
    persona = open(rb.resolve_persona(args.persona), encoding="utf-8").read()
    if shutil.which("claude") is None:
        sys.exit("FAIL: the claude command is not installed")

    stage = tempfile.mkdtemp(prefix="blueprint-build-stage-")
    rr.git_archive(args.skill_ref, "skill", stage)
    if args.kit:
        args.kit_dir = kit_source(args.kit, stage)
    print(f"Persona: {args.persona}; runs: {args.runs}; model: {args.model or 'default'}; "
          f"builder tools: {BUILDER_TOOLS}; limits: {args.turns} turns, {args.budget:.2f} USD, "
          f"{args.minutes:.0f} minutes")
    results = [run_once(args, stage, persona, n) for n in range(1, args.runs + 1)]
    shutil.rmtree(stage, ignore_errors=True)
    if args.runs > 1:
        def span(key, fmt="{}"):
            vals = [r[key] for r in results if r[key] is not None]
            return f"{fmt.format(min(vals))} to {fmt.format(max(vals))}" if vals else "none"
        print(f"\n===== Summary: {sum(r['ok'] for r in results)} of {args.runs} runs complete =====")
        print(f"Person turns: {span('person')}; carry-on nudges: {span('nudges')}; "
              f"cost: {span('cost', '{:.2f}')} USD; first passing check: {span('first', '{:.1f}')} min; "
              f"Fix now: {span('fix_now')}; security baseline met: "
              + ", ".join(str(r["baseline"]) for r in results))
    return 0 if all(r["ok"] for r in results) else 1


if __name__ == "__main__":
    sys.exit(main())
