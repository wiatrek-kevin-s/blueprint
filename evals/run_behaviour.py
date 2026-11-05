#!/usr/bin/env python3
"""Run one Blueprint behaviour eval: a whole conversation with a simulated person.

Usage:
  python3 evals/run_behaviour.py --prompt TEXT [options]

Options:
  --prompt TEXT       the person's first message (an invented idea or request)
  --skill-ref REF     git ref whose skill/ folder is the copy under test (default HEAD)
  --fixture PATH      a path under evals/fixtures/ to copy into the eval folder
  --persona FILE      the simulated person (default evals/personas/you-decide.md)
  --rounds N          most replies from the person before stopping (default 14)
  --max-turns N       turns per Blueprint reply (default 40)
  --model M           model alias or name (default: Claude Code's default)
  --keep              keep the eval folder and transcripts

How it works (see evals/README.md, "Behaviour evals"):
  - The eval folder is a new temporary folder outside the clone, built from
    tracked files only (git archive), with the skill under test at
    .claude/skills/blueprint, the same isolation as run_routing.py: project
    settings only, a tool allowlist, no MCP servers, no browser, and a clean
    environment. Each run checks that `blueprint` is the only blueprint skill.
  - Blueprint runs as one `claude -p` session in that folder, resumed with
    --resume for every reply. Edits inside the folder are accepted, and Bash
    may run only python3 (Blueprint's check scripts).
  - The person is a separate `claude -p` process in its own empty folder
    with no skills and no tools; its system prompt is the persona file and
    it sees only Blueprint's latest message.
  - The run stops when Blueprint has written a kit (kit-lite.md or
    00-START-HERE.md, the files phase 6 writes on every route) and either
    its latest message asks nothing more or it is the reply to the
    person's approval of that kit (the hand-off), or after --rounds
    replies. Then it runs check_kit.py (from the skill under test) on the
    kit folder and reports whether "Keeping it running" is filled.
  - With --fixture, it records the sha256 checksum of every file in the
    fixture's copy before the first reply and after the last, and reports
    any file added, removed or changed, because Audit, Redesign and Operate
    never edit the project (build brief REQ-7). It also names any
    audit-report.md written, for scoring against evals/keys/.

Exit 0 when check_kit.py passes, the section is non-empty and the fixture's
checksums are unchanged, 1 otherwise.
Python 3 standard library only. Needs git and the claude command.
"""
import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import run_routing as rr  # noqa: E402

TOOLS = "Skill,Read,Glob,Grep,Bash,Write,Edit"
KIT_MARKERS = ("kit-lite.md", "00-START-HERE.md")


def blueprint_turn(folder, text, session, args):
    cmd = ["claude", "-p", text, "--setting-sources", "project", "--tools", TOOLS,
           "--disallowedTools", "Projects", "--strict-mcp-config", "--no-chrome",
           "--permission-mode", "acceptEdits", "--allowedTools", "Bash(python3:*)",
           "--max-turns", str(args.max_turns), "--output-format", "stream-json", "--verbose"]
    if session:
        cmd += ["--resume", session]
    if args.model:
        cmd += ["--model", args.model]
    proc = subprocess.run(cmd, cwd=folder, stdin=subprocess.DEVNULL, env=rr.clean_env(),
                          capture_output=True, text=True, timeout=1800)
    with open(os.path.join(folder, "..", os.path.basename(folder) + "-transcript.jsonl"), "a",
              encoding="utf-8") as f:
        f.write(proc.stdout)
    r = rr.parse(proc.stdout, text, TOOLS)
    sid = session
    last = ""
    for line in proc.stdout.splitlines():
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


def person_turn(home, persona, message, args):
    prompt = ("Blueprint, the planner, just wrote the message below. Reply as the person, "
              "following your instructions exactly. Reply with the person's words only.\n\n"
              "--- Blueprint's message ---\n" + message)
    cmd = ["claude", "-p", prompt, "--setting-sources", "project", "--tools", "",
           "--strict-mcp-config", "--no-chrome", "--system-prompt", persona,
           "--max-turns", "1", "--output-format", "json"]
    if args.model:
        cmd += ["--model", args.model]
    proc = subprocess.run(cmd, cwd=home, stdin=subprocess.DEVNULL, env=rr.clean_env(),
                          capture_output=True, text=True, timeout=600)
    try:
        d = json.loads(proc.stdout)
        return (d.get("result") or "").strip() or "You decide", d.get("total_cost_usd") or 0.0
    except ValueError:
        return "You decide", 0.0


def checksums(root):
    """sha256 of every file under root, keyed by its path relative to root."""
    sums = {}
    for base, dirs, files in os.walk(root):
        for name in files:
            path = os.path.join(base, name)
            with open(path, "rb") as f:
                sums[os.path.relpath(path, root)] = hashlib.sha256(f.read()).hexdigest()
    return sums


def find_kit(folder):
    for root, dirs, files in os.walk(folder):
        dirs[:] = [d for d in dirs if d != ".claude"]
        for m in KIT_MARKERS:
            if m in files:
                return root
    return None


def asks_more(message):
    tail = message.strip()[-600:]
    return "?" in tail or bool(re.search(r"\b(approve|confirm|reply|answer)\b", tail, re.I))


def upkeep_section(kit):
    for name in ("kit-lite.md", "02-build-brief.md", os.path.join("docs", "build-brief.md")):
        p = os.path.join(kit, name)
        if os.path.isfile(p):
            text = open(p, encoding="utf-8").read()
            m = re.search(r"^##\s+Keeping it running\s*$(.*?)(?=^##\s|\Z)", text, re.M | re.S)
            if m:
                return name, m.group(1).strip()
    return None, ""


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--prompt", required=True)
    ap.add_argument("--skill-ref", default="HEAD")
    ap.add_argument("--fixture", default="")
    ap.add_argument("--persona", default=os.path.join(rr.REPO, "evals", "personas", "you-decide.md"))
    ap.add_argument("--rounds", type=int, default=14)
    ap.add_argument("--max-turns", type=int, default=40)
    ap.add_argument("--model", default="")
    ap.add_argument("--keep", action="store_true")
    args = ap.parse_args()
    if shutil.which("claude") is None:
        sys.exit("FAIL: the claude command is not installed")

    stage = tempfile.mkdtemp(prefix="blueprint-behaviour-stage-")
    rr.git_archive(args.skill_ref, "skill", stage)
    if args.fixture:
        rr.git_archive("HEAD", "evals/fixtures", stage)
    folder = rr.make_folder(stage, "behaviour", args.fixture or None)
    home = tempfile.mkdtemp(prefix="blueprint-behaviour-person-")
    persona = open(args.persona, encoding="utf-8").read()
    print(f"Eval folder: {folder}\nSkill under test: {args.skill_ref} ({rr.rev(args.skill_ref)})")
    fixture_copy = os.path.join(folder, os.path.basename(args.fixture.rstrip("/"))) if args.fixture else ""
    before = checksums(fixture_copy) if os.path.isdir(fixture_copy) else None

    session, message, cost = None, "", 0.0
    text, model, isolation_ok, route = args.prompt, "", True, ""
    approved_kit = False  # the person approved after a kit was written
    for n in range(args.rounds + 1):
        print(f"\n--- person ({n}) ---\n{text[:600]}", flush=True)
        session, message, r = blueprint_turn(folder, text, session, args)
        cost += r["cost"]
        model = r["model"] or model
        route = route or r["route"]
        if r["skills"] or r["tools"]:
            isolation_ok &= r["isolation_ok"]
        print(f"--- blueprint ({n}) ---\n{message[:1500]}", flush=True)
        kit = find_kit(folder)
        if kit and (not asks_more(message) or approved_kit):
            break
        if n == args.rounds:
            break
        text, c = person_turn(home, persona, message, args)
        cost += c
        approved_kit = bool(kit) and bool(re.search(r"\bapprove", text, re.I))

    kit = find_kit(folder)
    print(f"\nModel: {model}; route named: {route or 'none'}; isolation ok: {isolation_ok}")
    print(f"Cost reported by Claude Code: about {cost:.2f} USD")
    fixture_ok = True
    if before is not None:
        after = checksums(fixture_copy)
        changed = sorted(p for p in set(before) | set(after) if before.get(p) != after.get(p))
        fixture_ok = not changed
        print(f"Fixture checksums ({len(before)} files before, {len(after)} after): "
              + ("identical" if fixture_ok else "CHANGED: " + ", ".join(changed)))
    for base, dirs, files in os.walk(folder):
        dirs[:] = [d for d in dirs if d != ".claude"]
        if "audit-report.md" in files:
            print(f"Audit report: {os.path.join(base, 'audit-report.md')}")
    ok = False
    if not kit:
        print("RESULT FAIL: no kit was written")
    else:
        checker = os.path.join(folder, ".claude", "skills", "blueprint", "scripts", "check_kit.py")
        proc = subprocess.run([sys.executable, checker, kit], capture_output=True, text=True)
        print(proc.stdout.strip())
        name, body = upkeep_section(kit)
        lines = [ln for ln in body.split("\n") if ln.strip()]
        print(f"check_kit.py exit {proc.returncode}; Keeping it running in {name}: {len(lines)} non-empty lines")
        ok = proc.returncode == 0 and bool(lines) and isolation_ok and fixture_ok
        print("RESULT PASS" if ok else "RESULT FAIL")
    if not args.keep:
        shutil.rmtree(folder, ignore_errors=True)
        shutil.rmtree(home, ignore_errors=True)
    shutil.rmtree(stage, ignore_errors=True)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
