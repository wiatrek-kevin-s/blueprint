#!/usr/bin/env python3
"""Run one Blueprint behaviour eval: a whole conversation with a simulated person.

Usage:
  python3 evals/run_behaviour.py --prompt TEXT [options]

Options:
  --prompt TEXT       the person's first message (an invented idea or request)
  --skill-ref REF     git ref whose skill/ folder is the copy under test (default HEAD)
  --fixture PATH      a path under evals/fixtures/ to copy into the eval folder
  --repo-ref REF      instead of a fixture, copy every tracked file of this
                      repository at REF into the eval folder as repo-copy/
                      (for Operate on this repository; never planning/,
                      CLAUDE.md or other untracked files)
  --persona FILE      the simulated person (default evals/personas/you-decide.md)
  --rounds N          most replies from the person before stopping (default 14)
  --max-turns N       turns per Blueprint reply (default 40)
  --model M           model alias or name (default: Claude Code's default)
  --screens           the route designs screens (Redesign): before the first
                      reply, the runner captures every page of the fixture
                      copy at 375 and 1,280 px into screens/ in the eval
                      folder and tells Blueprint, as if the person had
                      attached them; check_kit.py runs with --screens, and
                      the run fails unless Blueprint's files or replies
                      cite the screenshots at both widths
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
    00-START-HERE.md, the files phase 6 writes on every route) in the eval
    folder or in Claude Code's scratchpad for it, and either
    its latest message asks nothing more or it is the reply to the
    person's approval of that kit (the hand-off), or after --rounds
    replies. Then it runs check_kit.py (from the skill under test) on the
    kit folder and reports whether "Keeping it running" is filled.
  - With --fixture, it records the sha256 checksum of every file in the
    fixture's copy before the first reply and after the last, and reports
    any file added, removed or changed, because Audit, Redesign and Operate
    never edit the project (build brief REQ-7). It also names any
    audit-report.md written, for scoring against evals/keys/.
  - It lists every Bash command and web tool the Blueprint session used,
    and fails the run if any web tool was used or a command looks like it
    reaches the network (curl, wget, gh, git, ssh, pip, npm, or Python
    network modules), because these routes make no network call on the
    project's behalf without asking (Rule 10).
  - With --screens, the runner (this process, never the Blueprint session)
    opens each .html page of the fixture copy from its local file with the
    preinstalled Python Playwright and its Chromium build (build brief D-15)
    and saves screens/<page>-375.png and screens/<page>-1280.png. Blueprint
    gets no extra tool rights: its Bash stays limited to python3. The
    first message tells it where the screenshots are, so the run tests R1
    with screenshots the person supplies. Every image the run wrote is
    listed too.

Exit 0 when check_kit.py passes, the section is non-empty, the fixture's
checksums are unchanged, no network use was seen and, with --screens, the
screenshots exist and Blueprint cites them, 1 otherwise.
Python 3 standard library only, except --screens, which needs Python
Playwright with Chromium installed outside the repository (D-15). Needs git
and the claude command.
"""
import argparse
import glob
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
IMAGE_EXT = (".png", ".jpg", ".jpeg")
SCREEN_DIR = "screens"
SCREEN_WIDTHS = (375, 1280)
# A browser opening a web address other than localhost counts as network use.
WEB_URL_RE = re.compile(r"(?:google-chrome|chromium|goto)\b[^\n]*https?://(?!localhost|127\.0\.0\.1)")


HEREDOC_RE = re.compile(r"<<-?\s*['\"]?(\w+)['\"]?")


def network_text(cmd):
    """The command without the bodies of heredocs that only write a file
    (cat > file <<EOF ... EOF), because a kit written that way may name
    tools such as gh or git without running them. Other heredocs, such as
    a Python program fed to python3, are kept and checked."""
    out, end = [], None
    for line in cmd.split("\n"):
        if end is not None:
            if line.strip() == end:
                end = None
            continue
        out.append(line)
        m = HEREDOC_RE.search(line)
        if m and re.search(r"\b(cat|tee)\b[^|;&]*(>|<<)", line):
            end = m.group(1)
    return "\n".join(out)


def tool_uses(transcript):
    """(name, Bash command or '') for every tool call in a stream-json transcript."""
    uses = []
    if not os.path.isfile(transcript):
        return uses
    for line in open(transcript, encoding="utf-8"):
        try:
            d = json.loads(line)
        except ValueError:
            continue
        if d.get("type") != "assistant":
            continue
        for c in d.get("message", {}).get("content") or []:
            if isinstance(c, dict) and c.get("type") == "tool_use":
                uses.append((c.get("name", ""), str((c.get("input") or {}).get("command", ""))))
    return uses


def blueprint_turn(folder, text, session, args):
    cmd = ["claude", "-p", text, "--setting-sources", "project", "--tools", TOOLS,
           "--disallowedTools", "Projects", "--strict-mcp-config", "--no-chrome",
           "--permission-mode", "acceptEdits",
           "--allowedTools", "Bash(python3:*)",
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


def output_roots(folder):
    """The eval folder, plus the scratchpad folders Claude Code gives the
    Blueprint session there, because Blueprint writes its own files outside
    the project and may choose its scratchpad (named after the folder)."""
    pattern = os.path.join(tempfile.gettempdir(), "claude-*", folder.replace(os.sep, "-"))
    return [folder] + sorted(glob.glob(pattern))


def find_kit(folder, skip=""):
    """The kit Blueprint wrote: the first folder holding a kit marker, never
    inside .claude or the project copy (skip), which may hold kits of its own."""
    for top in output_roots(folder):
        for root, dirs, files in os.walk(top):
            dirs[:] = [d for d in dirs if d != ".claude" and os.path.join(root, d) != skip]
            for m in KIT_MARKERS:
                if m in files:
                    return root
    return None


def capture_screens(copy, out):
    """Screenshots of every .html page in copy, opened from local files only,
    at each width in SCREEN_WIDTHS; returns the paths, relative to out's parent."""
    from playwright.sync_api import sync_playwright  # eval-only tool (D-15)
    os.makedirs(out)
    shots = []
    pages = sorted(f for f in os.listdir(copy) if f.endswith(".html"))
    with sync_playwright() as p:
        browser = p.chromium.launch()
        for page_name in pages:
            for w in SCREEN_WIDTHS:
                page = browser.new_page(viewport={"width": w, "height": 900})
                page.route(re.compile(r"^(?!file:)"), lambda route: route.abort())
                page.goto("file://" + os.path.join(copy, page_name))
                name = f"{page_name[:-5]}-{w}.png"
                page.screenshot(path=os.path.join(out, name), full_page=True)
                page.close()
                shots.append(os.path.join(SCREEN_DIR, name))
        browser.close()
    return shots


def cited(folder, skip, transcript, shots):
    """Screenshot names that Blueprint read with the Read tool, or named in
    a file it wrote or in a reply."""
    names = {os.path.basename(s) for s in shots}
    seen = set()
    if os.path.isfile(transcript):
        for line in open(transcript, encoding="utf-8"):
            seen |= {n for n in names if n in line and ('"Read"' in line or '"text"' in line)}
    for top in output_roots(folder):
        for root, dirs, files in os.walk(top):
            dirs[:] = [d for d in dirs if d not in (".claude", SCREEN_DIR)
                       and os.path.join(root, d) != skip]
            for f in files:
                if f.endswith(".md"):
                    text = open(os.path.join(root, f), encoding="utf-8", errors="replace").read()
                    seen |= {n for n in names if n in text}
    return sorted(seen)


def images(folder, skip):
    """Every image the run wrote, outside .claude and the project copy."""
    found = []
    for top in output_roots(folder):
        for root, dirs, files in os.walk(top):
            dirs[:] = [d for d in dirs if d != ".claude" and os.path.join(root, d) != skip]
            found += [os.path.join(root, f) for f in files if f.lower().endswith(IMAGE_EXT)]
    return sorted(found)


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
    ap.add_argument("--repo-ref", default="")
    ap.add_argument("--persona", default=os.path.join(rr.REPO, "evals", "personas", "you-decide.md"))
    ap.add_argument("--rounds", type=int, default=14)
    ap.add_argument("--max-turns", type=int, default=40)
    ap.add_argument("--model", default="")
    ap.add_argument("--screens", action="store_true")
    ap.add_argument("--keep", action="store_true")
    args = ap.parse_args()
    if shutil.which("claude") is None:
        sys.exit("FAIL: the claude command is not installed")

    stage = tempfile.mkdtemp(prefix="blueprint-behaviour-stage-")
    rr.git_archive(args.skill_ref, "skill", stage)
    if args.fixture and args.repo_ref:
        sys.exit("usage: give --fixture or --repo-ref, not both")
    if args.fixture:
        rr.git_archive("HEAD", "evals/fixtures", stage)
    if args.repo_ref:
        copy = os.path.join(stage, REPO_COPY)
        os.makedirs(copy)
        rr.git_archive(args.repo_ref, ".", copy)
        for private in ("CLAUDE.md", "planning", ".private-terms"):
            if os.path.exists(os.path.join(copy, private)):
                sys.exit(f"FAIL: {private} reached the repository copy; it must never be tracked")
        args.fixture = REPO_COPY
    folder = rr.make_folder(stage, "behaviour", args.fixture or None)
    home = tempfile.mkdtemp(prefix="blueprint-behaviour-person-")
    persona = open(args.persona, encoding="utf-8").read()
    print(f"Eval folder: {folder}\nSkill under test: {args.skill_ref} ({rr.rev(args.skill_ref)})")
    fixture_copy = os.path.join(folder, os.path.basename(args.fixture.rstrip("/"))) if args.fixture else ""
    before = checksums(fixture_copy) if os.path.isdir(fixture_copy) else None
    shots = []
    if args.screens:
        if not os.path.isdir(fixture_copy):
            sys.exit("usage: --screens needs --fixture")
        shots = capture_screens(fixture_copy, os.path.join(folder, SCREEN_DIR))
        print(f"Screenshots captured by the runner: {', '.join(shots)}")
        args.prompt += (f"\n\nI've attached screenshots of every page at phone width (375 px) and "
                        f"computer width (1,280 px). They're in the {SCREEN_DIR} folder: "
                        + ", ".join(os.path.basename(s) for s in shots) + ".")

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
        kit = find_kit(folder, fixture_copy)
        if kit and (not asks_more(message) or approved_kit):
            break
        if n == args.rounds:
            break
        text, c = person_turn(home, persona, message, args)
        cost += c
        approved_kit = bool(kit) and bool(re.search(r"\bapprove", text, re.I))

    kit = find_kit(folder, fixture_copy)
    print(f"\nModel: {model}; route named: {route or 'none'}; isolation ok: {isolation_ok}")
    print(f"Cost reported by Claude Code: about {cost:.2f} USD")
    fixture_ok = True
    if before is not None:
        after = checksums(fixture_copy)
        changed = sorted(p for p in set(before) | set(after) if before.get(p) != after.get(p))
        fixture_ok = not changed
        print(f"Fixture checksums ({len(before)} files before, {len(after)} after): "
              + ("identical" if fixture_ok else "CHANGED: " + ", ".join(changed)))
    transcript = os.path.join(folder, "..", os.path.basename(folder) + "-transcript.jsonl")
    uses = tool_uses(transcript)
    commands = [cmd for name, cmd in uses if name == "Bash"]
    web = sorted({name for name, _ in uses if name in WEB_TOOLS})
    risky = [cmd for cmd in commands
             if NETWORK_RE.search(network_text(cmd)) or WEB_URL_RE.search(network_text(cmd))]
    network_ok = not web and not risky
    print(f"Tool calls: {len(uses)}; Bash commands: {len(commands)}; web tools used: {web or 'none'}")
    for cmd in commands:
        print(f"  $ {cmd[:200]}")
    print("Network: no web tool and no network command" if network_ok
          else "Network: CHECK FAILED: " + "; ".join(web + [c[:120] for c in risky]))
    for top in output_roots(folder):
        for base, dirs, files in os.walk(top):
            dirs[:] = [d for d in dirs if d != ".claude" and os.path.join(base, d) != fixture_copy]
            if "audit-report.md" in files:
                print(f"Audit report: {os.path.join(base, 'audit-report.md')}")
    written = images(folder, fixture_copy)
    print(f"Images in the eval folder and scratchpad: {len(written)}")
    for p in written:
        print(f"  {p}")
    screens_ok = True
    if args.screens:
        present = [s for s in shots if os.path.isfile(os.path.join(folder, s))]
        cites = cited(folder, fixture_copy, transcript, shots)
        both = all(any(f"-{w}.png" in c for c in cites) for w in SCREEN_WIDTHS)
        screens_ok = len(present) == len(shots) > 0 and both
        print(f"Screenshots: {len(present)} of {len(shots)} present; cited by Blueprint: "
              f"{', '.join(cites) or 'none'}; " + ("PASS" if screens_ok else "FAIL"))
    ok = False
    if not kit:
        print("RESULT FAIL: no kit was written")
    else:
        checker = os.path.join(folder, ".claude", "skills", "blueprint", "scripts", "check_kit.py")
        proc = subprocess.run([sys.executable, checker, kit] + (["--screens"] if args.screens else []),
                              capture_output=True, text=True)
        print(proc.stdout.strip())
        name, body = upkeep_section(kit)
        lines = [ln for ln in body.split("\n") if ln.strip()]
        print(f"check_kit.py exit {proc.returncode}; Keeping it running in {name}: {len(lines)} non-empty lines")
        ok = (proc.returncode == 0 and bool(lines) and isolation_ok and fixture_ok
              and network_ok and screens_ok)
        print("RESULT PASS" if ok else "RESULT FAIL")
    if not args.keep:
        for top in output_roots(folder):
            shutil.rmtree(top, ignore_errors=True)
        shutil.rmtree(home, ignore_errors=True)
    shutil.rmtree(stage, ignore_errors=True)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
