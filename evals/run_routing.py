#!/usr/bin/env python3
"""Run Blueprint's routing evals with headless Claude Code (claude -p).

Usage:
  python3 evals/run_routing.py --mode v2|v3 [options]
  python3 evals/run_routing.py --probe [options]

Options:
  --skill-ref REF     git ref whose skill/ folder is the copy under test (default HEAD)
  --fixtures-ref REF  git ref whose evals/fixtures/ are used (default HEAD)
  --set FILE          eval set, format F-5 (default evals/routing.jsonl)
  --ids a,b           run only these ids
  --max-turns N       turns per run (default 4; routing needs only the first reply)
  --model M           model alias or name (default: Claude Code's default)
  --jobs N            runs in parallel (default 4)
  --out FILE          write the Markdown summary here (default: print only)
  --tools LIST        built-in tools the run may use, comma separated
                      (default Skill,Read,Glob,Grep,Bash,Write,Edit)
  --keep              keep the temporary eval folders and transcripts

Why it works this way (see evals/README.md):
  - Every eval is a separate `claude -p` process, started in its own new
    temporary folder outside the clone, so it starts fresh and never sees the
    clone's CLAUDE.md, planning notes or answer keys.
  - The folder is built from tracked files only (`git archive`): the skill
    under test goes to .claude/skills/blueprint (a project skill), and the
    eval's fixture, if any, is copied in under its own name.
  - `--setting-sources project` stops Claude Code loading user-level settings
    and skills, so another installed copy named blueprint (for example one
    synced from the Claude app) can't answer instead.
  - `--tools` (an allowlist of built-in tools), `--disallowedTools Projects`,
    `--strict-mcp-config` and `--no-chrome` remove the tools that reach
    outside the folder: the host's Projects tool (which can read documents
    attached to a Claude project, such as private planning notes), connector
    and MCP tools, and the browser.
  - Each run checks all of this from what Claude Code lists at start: the
    skills must include `blueprint` exactly once and no other skill whose
    name ends in "blueprint", and every tool must be on the allowlist, or the
    eval fails.
  - The run's environment drops the variables through which a host session
    hands its own context to child processes (an attached Claude project,
    memory, extra directories, session links; ENV_DROP below), so a run
    started from inside a Claude Code session still starts clean.

Scoring:
  - Triggered: the run calls the Skill tool with skill "blueprint", or the
    prompt starts with /blueprint (the host loads the skill directly).
  - v2 mode (baseline): a should_trigger prompt passes when Blueprint
    triggers (every expected route is one v3 also triggers on); a negative
    passes when it does not.
  - v3 mode: a should_trigger prompt passes when Blueprint triggers and the
    route it names matches expected_route; a negative passes when it does not
    trigger. The route is read from a "Route: name" line (state-file format
    F-1, with or without bold) in the replies or in files the run writes.

Probe (T-6 check 4): runs one known prompt and one question about loaded
instructions, then prints the skills Claude Code listed at start, which copy
of blueprint answered (its base directory) and the answer to the question.

Python 3 standard library only. Needs git and the claude command.
"""
import argparse
import concurrent.futures
import datetime
import io
import json
import os
import re
import shutil
import subprocess
import sys
import tarfile
import tempfile

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROUTES = ["new", "audit", "redesign", "operate", "amend", "none"]
ROUTE_RE = re.compile(r"\broute\W{0,6}\s*(new|audit|redesign|operate|amend)\b", re.I)
BASE_DIR_RE = re.compile(r"Base directory for this skill:\s*(\S+)")
PROBE_PROMPT = ("I have an idea for an app that helps neighbours lend each other "
                "garden tools. Can you help me plan it?")
PROBE_QUESTION = ("Answer in two short lines. (1) Is any CLAUDE.md, other project "
                  "instruction file, or attached project document listed in your "
                  "context? Name the files, or say none. (2) Is there any memory or "
                  "profile about the user in your context? Say yes or no only, with "
                  "no details.")
DEFAULT_TOOLS = "Skill,Read,Glob,Grep,Bash,Write,Edit"
# Variables a host Claude Code session passes to child processes that would
# carry its context into the eval: an attached Claude project, memory, extra
# directories and their CLAUDE.md files, and links to the parent session.
ENV_DROP = ["CLAUDE_PROJECT_UUID", "CLAUDE_PROJECT_TOOL", "CLAUDE_ADDITIONAL_DIRECTORIES",
            "CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD", "CLAUDE_CODE_POST_TURN_MEMORY",
            "CLAUDE_CODE_POST_TURN_MEMORY_CONFIG", "CLAUDECODE", "CLAUDE_CODE_CHILD_SESSION",
            "CLAUDE_CODE_MESSAGING_SOCKET", "CLAUDE_CODE_MESSAGING_TOKEN",
            "CLAUDE_CODE_SESSION_ID", "CLAUDE_CODE_REMOTE_SESSION_ID"]


def clean_env():
    return {k: v for k, v in os.environ.items()
            if k not in ENV_DROP and not k.startswith("CLAUDE_PROJECT_")}


def git_archive(ref, path, dest):
    """Extract the tracked files of `path` at `ref` into `dest`."""
    data = subprocess.run(["git", "-C", REPO, "archive", "--format=tar", ref, path],
                          check=True, capture_output=True).stdout
    with tarfile.open(fileobj=io.BytesIO(data)) as tar:
        if hasattr(tarfile, "data_filter"):
            tar.extractall(dest, filter="data")
        else:
            tar.extractall(dest)


def outside_repo(path):
    real, repo = os.path.realpath(path), os.path.realpath(REPO)
    return os.path.commonpath([real, repo]) != repo


def make_folder(stage, eval_id, fixture):
    folder = tempfile.mkdtemp(prefix=f"blueprint-eval-{eval_id}-")
    if not outside_repo(folder):
        sys.exit(f"FAIL: eval folder {folder} is inside the clone; set TMPDIR elsewhere")
    os.makedirs(os.path.join(folder, ".claude", "skills"))
    shutil.copytree(os.path.join(stage, "skill"), os.path.join(folder, ".claude", "skills", "blueprint"))
    if fixture:
        src = os.path.join(stage, fixture)
        dst = os.path.join(folder, os.path.basename(fixture.rstrip("/")))
        if os.path.isdir(src):
            shutil.copytree(src, dst)
        elif os.path.isfile(src):
            shutil.copy2(src, dst)
        else:
            raise FileNotFoundError(f"fixture {fixture} is not tracked at the fixtures ref")
    return folder


def run_claude(folder, prompt, args):
    cmd = ["claude", "-p", prompt, "--setting-sources", "project",
           "--tools", args.tools, "--disallowedTools", "Projects",
           "--strict-mcp-config", "--no-chrome",
           "--max-turns", str(args.max_turns), "--output-format", "stream-json", "--verbose"]
    if args.model:
        cmd += ["--model", args.model]
    try:
        proc = subprocess.run(cmd, cwd=folder, stdin=subprocess.DEVNULL, env=clean_env(),
                              capture_output=True, text=True, timeout=600)
        out = proc.stdout
    except subprocess.TimeoutExpired as e:
        out = e.stdout.decode() if isinstance(e.stdout, bytes) else (e.stdout or "")
    with open(os.path.join(folder, "transcript.jsonl"), "w", encoding="utf-8") as f:
        f.write(out)
    return parse(out, prompt, args.tools)


def parse(out, prompt, allowed_tools):
    r = {"skills": [], "slash": [], "tools": [], "model": "", "triggered": False, "trigger_kind": "",
         "other_skills": [], "base_dirs": [], "texts": [], "route": "", "cost": 0.0,
         "result": "no result"}
    written = []
    for line in out.splitlines():
        try:
            d = json.loads(line)
        except ValueError:
            continue
        t = d.get("type")
        if t == "system" and d.get("subtype") == "init":
            r["skills"] = d.get("skills") or []
            r["slash"] = d.get("slash_commands") or []
            r["tools"] = d.get("tools") or []
            r["model"] = d.get("model", "")
        elif t in ("assistant", "user"):
            content = d.get("message", {}).get("content")
            if isinstance(content, str):
                content = [{"type": "text", "text": content}]
            for c in content or []:
                if c.get("type") == "text":
                    if t == "assistant":
                        r["texts"].append(c["text"])
                    r["base_dirs"] += BASE_DIR_RE.findall(c["text"])
                elif c.get("type") == "tool_use":
                    inp = c.get("input") or {}
                    if c.get("name") == "Skill":
                        name = str(inp.get("skill", "")).lstrip("/")
                        if name == "blueprint":
                            r["triggered"], r["trigger_kind"] = True, "Skill tool"
                        elif name.endswith("blueprint"):
                            r["other_skills"].append(name)
                    for key in ("content", "new_string"):
                        if isinstance(inp.get(key), str):
                            written.append(inp[key])
                elif c.get("type") == "tool_result":
                    cc = c.get("content")
                    text = cc if isinstance(cc, str) else " ".join(
                        x.get("text", "") for x in cc or [] if isinstance(x, dict))
                    r["base_dirs"] += BASE_DIR_RE.findall(text)
        elif t == "result":
            r["result"] = d.get("subtype", "")
            r["cost"] = d.get("total_cost_usd") or 0.0
    if not r["triggered"] and prompt.lstrip().startswith("/blueprint") and "blueprint" in r["slash"]:
        r["triggered"], r["trigger_kind"] = True, "slash command"
    for text in r["texts"] + written:
        m = ROUTE_RE.search(text)
        if m:
            r["route"] = m.group(1).lower()
            break
    named = [s for s in r["skills"] if s.endswith("blueprint")]
    allowed = {t.strip() for t in allowed_tools.split(",") if t.strip()}
    extra = sorted(set(r["tools"]) - allowed)
    r["isolation_ok"] = named == ["blueprint"] and not r["other_skills"] and not extra and bool(r["tools"])
    r["isolation_note"] = "" if r["isolation_ok"] else (
        f"blueprint skills listed: {named}; other invoked: {r['other_skills']}; "
        f"tools beyond the allowlist: {extra}")
    return r


def score(row, r, mode):
    if not r["isolation_ok"]:
        return False, "isolation failed: " + r["isolation_note"]
    if not row["should_trigger"]:
        return (not r["triggered"]), ("triggered" if r["triggered"] else "did not trigger")
    if not r["triggered"]:
        return False, "did not trigger"
    if mode == "v2":
        return True, "triggered"
    if r["route"] == row["expected_route"]:
        return True, f"route {r['route']}"
    return False, f"route {r['route'] or 'not named'}"


def load_set(path, ids):
    rows = []
    with open(path, encoding="utf-8") as f:
        for n, line in enumerate(f, 1):
            if line.strip():
                row = json.loads(line)
                for k in ("id", "prompt", "expected_route", "should_trigger"):
                    if k not in row:
                        sys.exit(f"FAIL: {path} line {n} has no {k}")
                if row["expected_route"] not in ROUTES:
                    sys.exit(f"FAIL: {path} line {n} has expected_route {row['expected_route']}")
                rows.append(row)
    if ids:
        want = set(ids.split(","))
        rows = [r for r in rows if r["id"] in want]
    return rows


def summary(rows, results, args, model):
    lines = []
    today = datetime.date.today().isoformat()
    groups = {}
    for row in rows:
        key = "resume (new)" if row.get("fixture", "").endswith("v2-state.md") else row["expected_route"]
        groups.setdefault(key, []).append(row["id"])
    total_pass = sum(1 for row in rows if results[row["id"]][0])
    lines.append(f"- **Date:** {today}")
    lines.append(f"- **Model:** {model or 'unknown'} (Claude Code {claude_version()})")
    lines.append(f"- **Mode:** {args.mode} · skill from `{args.skill_ref}` "
                 f"({rev(args.skill_ref)}) · fixtures from `{args.fixtures_ref}` ({rev(args.fixtures_ref)})")
    lines.append(f"- **Runner:** `python3 evals/run_routing.py --mode {args.mode} --max-turns {args.max_turns}`: "
                 "one `claude -p` process per prompt in a temporary folder outside the clone, "
                 f"with `--setting-sources project`, tools limited to {args.tools}, no MCP servers, no browser")
    lines.append(f"- **Total:** {total_pass} of {len(rows)} passed")
    lines.append("")
    lines.append("| Group | Passed | Of |")
    lines.append("|---|---|---|")
    order = ["new", "resume (new)", "audit", "redesign", "operate", "amend", "none"]
    for key in order + sorted(set(groups) - set(order)):
        if key in groups:
            p = sum(1 for i in groups[key] if results[i][0])
            label = "none (must not trigger)" if key == "none" else key
            lines.append(f"| {label} | {p} | {len(groups[key])} |")
    lines.append("")
    lines.append("| ID | Expected | Result | Detail |")
    lines.append("|---|---|---|---|")
    for row in rows:
        ok, detail = results[row["id"]]
        lines.append(f"| {row['id']} | {row['expected_route']} | {'pass' if ok else 'FAIL'} | {detail} |")
    return "\n".join(lines) + "\n"


def rev(ref):
    try:
        return subprocess.run(["git", "-C", REPO, "rev-parse", "--short", ref],
                              check=True, capture_output=True, text=True).stdout.strip()
    except subprocess.CalledProcessError:
        return "unknown"


def claude_version():
    try:
        return subprocess.run(["claude", "--version"], capture_output=True, text=True,
                              timeout=60).stdout.split()[0]
    except (OSError, IndexError, subprocess.TimeoutExpired):
        return "unknown"


def probe(stage, args):
    print("Probe: one known prompt, then one question about loaded instructions.")
    folder = make_folder(stage, "probe", None)
    r = run_claude(folder, PROBE_PROMPT, args)
    expected_dir = os.path.join(folder, ".claude", "skills", "blueprint")
    print(f"  eval folder: {folder} (outside the clone: {outside_repo(folder)})")
    print(f"  model: {r['model']}")
    print(f"  skills listed at start that end in 'blueprint': {[s for s in r['skills'] if s.endswith('blueprint')]}")
    print(f"  tools listed at start: {r['tools']}")
    print(f"  isolation check: {'ok' if r['isolation_ok'] else r['isolation_note']}")
    print(f"  triggered: {r['triggered']} ({r['trigger_kind'] or 'no'})")
    print(f"  base directory of the copy that answered: {r['base_dirs']}")
    under_test = any(os.path.realpath(d) == os.path.realpath(expected_dir) for d in r["base_dirs"])
    print(f"  copy under test answered: {under_test}")
    folder2 = make_folder(stage, "probe-q", None)
    q = run_claude(folder2, PROBE_QUESTION, args)
    answer = " ".join(q["texts"]).strip().replace("\n", " ")
    print(f"  loaded-instructions answer: {answer[:300]}")
    low = answer.lower()
    clean = "none" in low and ".md" not in low.replace("claude.md", "") and "yes" not in low
    print(f"  no instructions, project documents or memory reported: {clean}")
    ok = r["isolation_ok"] and r["triggered"] and under_test and q["isolation_ok"] and clean
    print("PROBE PASS" if ok else "PROBE FAIL")
    if not args.keep:
        shutil.rmtree(folder, ignore_errors=True)
        shutil.rmtree(folder2, ignore_errors=True)
    return 0 if ok else 1


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--mode", choices=["v2", "v3"])
    ap.add_argument("--probe", action="store_true")
    ap.add_argument("--skill-ref", default="HEAD")
    ap.add_argument("--fixtures-ref", default="HEAD")
    ap.add_argument("--set", default=os.path.join(REPO, "evals", "routing.jsonl"))
    ap.add_argument("--ids", default="")
    ap.add_argument("--max-turns", type=int, default=4)
    ap.add_argument("--model", default="")
    ap.add_argument("--jobs", type=int, default=4)
    ap.add_argument("--out", default="")
    ap.add_argument("--tools", default=DEFAULT_TOOLS)
    ap.add_argument("--keep", action="store_true")
    args = ap.parse_args()
    if not args.probe and not args.mode:
        ap.error("give --mode v2 or v3, or --probe")
    if shutil.which("claude") is None:
        sys.exit("FAIL: the claude command is not installed")

    stage = tempfile.mkdtemp(prefix="blueprint-eval-stage-")
    if not outside_repo(stage):
        sys.exit(f"FAIL: staging folder {stage} is inside the clone; set TMPDIR elsewhere")
    git_archive(args.skill_ref, "skill", stage)
    if args.probe:
        code = probe(stage, args)
        shutil.rmtree(stage, ignore_errors=True)
        return code
    git_archive(args.fixtures_ref, "evals/fixtures", stage)

    rows = load_set(args.set, args.ids)
    results, models, folders, cost = {}, set(), [], 0.0

    def one(row):
        folder = make_folder(stage, row["id"], row.get("fixture"))
        r = run_claude(folder, row["prompt"], args)
        return row, folder, r

    with concurrent.futures.ThreadPoolExecutor(max_workers=args.jobs) as pool:
        for row, folder, r in pool.map(one, rows):
            ok, detail = score(row, r, args.mode)
            results[row["id"]] = (ok, detail)
            models.add(r["model"])
            folders.append(folder)
            cost += r["cost"]
            print(f"{'pass' if ok else 'FAIL'}  {row['id']:<8} {detail}  ({r['result']})", flush=True)

    text = summary(rows, results, args, ", ".join(sorted(m for m in models if m)))
    print()
    print(text)
    print(f"Cost reported by Claude Code: about {cost:.2f} USD")
    if args.out:
        with open(args.out, "w", encoding="utf-8", newline="\n") as f:
            f.write(text)
        print(f"Summary written to {args.out}")
    if args.keep:
        print("Eval folders kept (transcripts in transcript.jsonl):")
        for f in folders:
            print("  " + f)
    else:
        for f in folders:
            shutil.rmtree(f, ignore_errors=True)
    shutil.rmtree(stage, ignore_errors=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
