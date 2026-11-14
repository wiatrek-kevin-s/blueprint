#!/usr/bin/env python3
"""Run one Blueprint behaviour eval: a whole conversation with a simulated person.

Usage:
  python3 evals/run_behaviour.py --prompt TEXT [options]

Options:
  --prompt TEXT       the person's first message (an invented idea or request)
  --skill-ref REF     git ref whose skill/ folder is the copy under test (default HEAD)
  --no-skill          baseline: the same run with no Blueprint installed (the
                      skill at --skill-ref is still used for check_kit.py);
                      the conversation also stops when a reply asks nothing
                      more, since no kit marker will appear
  --fixture PATH      a path under evals/fixtures/ to copy into the eval folder
  --repo-ref REF      instead of a fixture, copy every tracked file of this
                      repository at REF into the eval folder as repo-copy/
                      (for Operate on this repository; never planning/,
                      CLAUDE.md or other untracked files)
  --persona NAME      the simulated person: a name in evals/personas/
                      (you-decide, the default; disagrees; goes-quiet) or a file
  --runs N            repeat the whole run N times (default 1) and report the
                      spread: runs passed, and words per kit file, min to max
  --rounds N          most replies from the person before stopping (default 14)
  --max-turns N       turns per Blueprint reply (default 40)
  --model M           model alias or name for Blueprint, passed to claude
                      --model (default: Claude Code's default); also the
                      person's model unless --person-model is given
  --person-model M    model for the simulated person
  --allow-subagents   add the subagent tool (Agent) to the allowlist, so the
                      fresh-reviewer steps can use a subagent
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
    START-HERE.md (00-START-HERE.md before 3.0.1), the files phase 6 writes on every route) in the eval
    folder or in Claude Code's scratchpad for it, and either
    its latest message asks nothing more or it is the reply to the
    person's approval of that kit (the hand-off), or after --rounds
    replies, or when the person's reply is "[no reply]" (the goes-quiet
    persona). Then it runs check_kit.py (from the skill under test) on the
    kit folder and reports whether "Keeping it running" is filled (in
    kit-lite.md or the build brief, under its 3.0.1 or numbered name, at
    the kit root or in docs/), and the words in each kit file. A run whose
    person went quiet before a kit passes when Blueprint saved a state file.
  - The person is told its reply number, so a persona can change after a
    number of replies.
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
  - It flags, without failing the run, every file Blueprint wrote outside
    the eval folder and its scratchpad: Write and Edit paths, and Bash
    redirections to an absolute path. Commands that write in other ways
    are not detected.
  - With --repo-ref, the first message says that repo-copy/ leaves out the
    git history, so Blueprint does not read the copy as a project without
    version history.
  - With --screens, the runner (this process, never the Blueprint session)
    opens each .html page of the fixture copy from its local file with the
    preinstalled Python Playwright and its Chromium build (build brief D-15)
    and saves screens/<page>-375.png and screens/<page>-1280.png. Blueprint
    gets no extra tool rights: its Bash stays limited to python3. The
    first message tells it where the screenshots are, so the run tests R1
    with screenshots the person supplies. Every image the run wrote is
    listed too.

Exit 0 when every run passed: check_kit.py passes, the section is non-empty
(or, if the person went quiet first, a state file was saved), the fixture's
checksums are unchanged, no network use was seen and, with --screens, the
screenshots exist and Blueprint cites them; 1 otherwise. Without --keep, the
eval folders, scratchpads and transcripts are deleted.
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
SUBAGENT_TOOL = "Agent"  # Claude Code's subagent tool ("Task" in older versions)
KIT_MARKERS = ("kit-lite.md", "START-HERE.md", "00-START-HERE.md")
# Where "Keeping it running" may be: kit-lite, then the brief under its 3.0.1
# name, its numbered name before 3.0.1, either in docs/, then brief parts
# (build-brief-1.md, ...) when a long brief is split.
UPKEEP_FILES = ("kit-lite.md", "build-brief.md", "02-build-brief.md",
                os.path.join("docs", "build-brief.md"), os.path.join("docs", "02-build-brief.md"))
UPKEEP_PARTS = ("build-brief-*.md", "02-build-brief-*.md", os.path.join("docs", "build-brief-*.md"))
PERSONA_DIR = os.path.join(rr.REPO, "evals", "personas")
SILENCE = "[no reply]"  # a persona's reply when the person has stopped answering
STATE_RE = re.compile(r"^#\s*Blueprint state\b|^\s*-\s*\*\*Route:\*\*", re.M)
IMAGE_EXT = (".png", ".jpg", ".jpeg")
SCREEN_DIR = "screens"
SCREEN_WIDTHS = (375, 1280)
# A browser opening a web address other than localhost counts as network use.
WEB_URL_RE = re.compile(r"(?:google-chrome|chromium|goto)\b[^\n]*https?://(?!localhost|127\.0\.0\.1)")
REPO_COPY = "repo-copy"
WEB_TOOLS = {"WebSearch", "WebFetch"}
# A network program in command position (after the start, a space or ; | & ( `),
# so paths such as ./.git are not read as the git command; or a Python
# network module anywhere.
NETWORK_RE = re.compile(r"(?:^|[\s;|&(`])(curl|wget|gh|git|ssh|scp|pip3?|npm|npx)(?=$|[\s;|&)`])"
                        r"|\b(urllib|requests|http\.client|socket|urlopen)\b", re.M)


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


REDIRECT_RE = re.compile(r">>?\s*['\"]?(/[^\s'\";|&)]+)")


def outside_writes(transcript, roots):
    """Absolute paths outside roots that Write, Edit or a Bash redirection
    wrote to; flagged, never failed, because cheap detection misses some."""
    found = set()
    if not os.path.isfile(transcript):
        return []
    real = [os.path.realpath(r) for r in roots]

    def outside(path):
        rp = os.path.realpath(path)
        return not any(rp == r or rp.startswith(r + os.sep) for r in real) and rp != "/dev/null"
    for line in open(transcript, encoding="utf-8"):
        try:
            d = json.loads(line)
        except ValueError:
            continue
        if d.get("type") != "assistant":
            continue
        for c in d.get("message", {}).get("content") or []:
            if not (isinstance(c, dict) and c.get("type") == "tool_use"):
                continue
            inp = c.get("input") or {}
            if c.get("name") in ("Write", "Edit") and inp.get("file_path"):
                paths = [inp["file_path"]]
            elif c.get("name") == "Bash":
                paths = REDIRECT_RE.findall(network_text(str(inp.get("command", ""))))
            else:
                paths = []
            found |= {p for p in paths if os.path.isabs(p) and outside(p)}
    return sorted(found)


def transcript_path(folder):
    return os.path.join(os.path.dirname(folder), os.path.basename(folder) + "-transcript.jsonl")


def blueprint_turn(folder, text, session, args):
    cmd = ["claude", "-p", text, "--setting-sources", "project", "--tools", args.tools,
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
    with open(transcript_path(folder), "a", encoding="utf-8") as f:
        f.write(proc.stdout)
    r = rr.parse(proc.stdout, text, args.tools)
    if args.no_skill and (r["skills"] or r["tools"]):
        # The baseline passes isolation when no blueprint skill is listed at all.
        named = [x for x in r["skills"] if x.endswith("blueprint")]
        allowed = {t.strip() for t in args.tools.split(",") if t.strip()}
        extra = sorted(set(r["tools"]) - allowed)
        r["isolation_ok"] = not named and not r["triggered"] and not extra and bool(r["tools"])
        r["isolation_note"] = "" if r["isolation_ok"] else (
            f"blueprint skills listed: {named}; tools beyond the allowlist: {extra}")
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


def person_turn(home, persona, message, args, number):
    prompt = ("Blueprint, the planner, just wrote the message below. Reply as the person, "
              "following your instructions exactly. Reply with the person's words only.\n"
              f"This is your reply number {number}.\n\n"
              "--- Blueprint's message ---\n" + message)
    cmd = ["claude", "-p", prompt, "--setting-sources", "project", "--tools", "",
           "--strict-mcp-config", "--no-chrome", "--system-prompt", persona,
           "--max-turns", "1", "--output-format", "json"]
    if args.person_model or args.model:
        cmd += ["--model", args.person_model or args.model]
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
    names = list(UPKEEP_FILES)
    for pattern in UPKEEP_PARTS:
        names += sorted(os.path.relpath(p, kit) for p in glob.glob(os.path.join(kit, pattern)))
    for name in names:
        p = os.path.join(kit, name)
        if os.path.isfile(p):
            text = open(p, encoding="utf-8").read()
            m = re.search(r"^##\s+Keeping it running\s*$(.*?)(?=^##\s|\Z)", text, re.M | re.S)
            if m:
                return name, m.group(1).strip()
    return None, ""


def written_files(folder, skip):
    """Every file the run wrote in the eval folder and its scratchpad, outside
    .claude, screens/ and the project copy."""
    found = []
    for top in output_roots(folder):
        for root, dirs, files in os.walk(top):
            dirs[:] = [d for d in dirs if d not in (".claude", SCREEN_DIR) and os.path.join(root, d) != skip]
            found += [os.path.join(root, f) for f in files]
    return sorted(found)


def word_counts(paths, base):
    """Words in each Markdown, JSON or text file, keyed by path relative to base."""
    counts = {}
    for p in paths:
        if p.lower().endswith((".md", ".json", ".txt")):
            text = open(p, encoding="utf-8", errors="replace").read()
            counts[os.path.relpath(p, base)] = len(text.split())
    return counts


def kit_files(kit):
    out = []
    for root, dirs, files in os.walk(kit):
        dirs[:] = [d for d in dirs if d not in (".claude", SCREEN_DIR)]
        out += [os.path.join(root, f) for f in files]
    return sorted(out)


def state_files(folder, skip):
    """Files that look like a Blueprint state file (its heading or Route line)."""
    found = []
    for p in written_files(folder, skip):
        if p.endswith(".md"):
            if STATE_RE.search(open(p, encoding="utf-8", errors="replace").read()):
                found.append(p)
    return found


def resolve_persona(value):
    """A persona file path, or a name in evals/personas/ (with or without .md)."""
    if os.path.isfile(value):
        return value
    name = value if value.endswith(".md") else value + ".md"
    path = os.path.join(PERSONA_DIR, name)
    if os.path.isfile(path):
        return path
    known = sorted(f[:-3] for f in os.listdir(PERSONA_DIR) if f.endswith(".md"))
    sys.exit(f"usage: --persona {value} is neither a file nor one of: {', '.join(known)}")


def run_once(args, stage, persona, number):
    """One whole conversation; returns a dict with ok, cost, model and word counts."""
    folder = rr.make_folder(stage, "behaviour", args.fixture or None)
    if args.no_skill:
        shutil.rmtree(os.path.join(folder, ".claude", "skills", "blueprint"))
    home = tempfile.mkdtemp(prefix="blueprint-behaviour-person-")
    transcript = transcript_path(folder)
    label = "no skill (baseline)" if args.no_skill else f"{args.skill_ref} ({rr.rev(args.skill_ref)})"
    print(f"\n===== Run {number} of {args.runs} =====\nEval folder: {folder}\nSkill under test: {label}")
    fixture_copy = os.path.join(folder, os.path.basename(args.fixture.rstrip("/"))) if args.fixture else ""
    before = checksums(fixture_copy) if os.path.isdir(fixture_copy) else None
    prompt = args.prompt
    shots = []
    if args.screens:
        if not os.path.isdir(fixture_copy):
            sys.exit("usage: --screens needs --fixture")
        shots = capture_screens(fixture_copy, os.path.join(folder, SCREEN_DIR))
        print(f"Screenshots captured by the runner: {', '.join(shots)}")
        prompt += (f"\n\nI've attached screenshots of every page at phone width (375 px) and "
                   f"computer width (1,280 px). They're in the {SCREEN_DIR} folder: "
                   + ", ".join(os.path.basename(s) for s in shots) + ".")

    session, message, cost = None, "", 0.0
    text, model, isolation_ok, route, tools = prompt, "", True, "", []
    approved_kit = False  # the person approved after a kit was written
    went_quiet = 0        # the person's reply number that was SILENCE, if any
    for n in range(args.rounds + 1):
        print(f"\n--- person ({n}) ---\n{text[:600]}", flush=True)
        session, message, r = blueprint_turn(folder, text, session, args)
        cost += r["cost"]
        model = r["model"] or model
        route = route or r["route"]
        tools = tools or r["tools"]
        if r["skills"] or r["tools"]:
            isolation_ok &= r["isolation_ok"]
            if not r["isolation_ok"]:
                print(f"Isolation: {r['isolation_note']}")
        print(f"--- blueprint ({n}) ---\n{message[:1500]}", flush=True)
        kit = find_kit(folder, fixture_copy)
        if kit and (not asks_more(message) or approved_kit):
            break
        if args.no_skill and not asks_more(message):
            break
        if n == args.rounds:
            break
        text, c = person_turn(home, persona, message, args, n + 1)
        cost += c
        if text.strip().strip('"').lower().startswith(SILENCE):
            went_quiet = n + 1
            print(f"\n--- person ({n + 1}) ---\n{SILENCE}: the person stopped replying; the conversation ends here.")
            break
        approved_kit = bool(kit) and bool(re.search(r"\bapprove", text, re.I))

    kit = find_kit(folder, fixture_copy)
    print(f"\nModel: {model}; route named: {route or 'none'}; isolation ok: {isolation_ok}")
    print(f"Tools listed at start: {', '.join(tools) or 'none'}")
    print(f"Cost reported by Claude Code: about {cost:.2f} USD")
    fixture_ok = True
    if before is not None:
        after = checksums(fixture_copy)
        changed = sorted(p for p in set(before) | set(after) if before.get(p) != after.get(p))
        fixture_ok = not changed
        print(f"Fixture checksums ({len(before)} files before, {len(after)} after): "
              + ("identical" if fixture_ok else "CHANGED: " + ", ".join(changed)))
    uses = tool_uses(transcript)
    commands = [cmd for name, cmd in uses if name == "Bash"]
    web = sorted({name for name, _ in uses if name in WEB_TOOLS})
    subagents = sum(1 for name, _ in uses if name in ("Agent", "Task"))
    risky = [cmd for cmd in commands
             if NETWORK_RE.search(network_text(cmd)) or WEB_URL_RE.search(network_text(cmd))]
    network_ok = not web and not risky
    print(f"Tool calls: {len(uses)}; Bash commands: {len(commands)}; subagent calls: {subagents}; "
          f"web tools used: {web or 'none'}")
    for cmd in commands:
        print(f"  $ {cmd[:200]}")
    print("Network: no web tool and no network command" if network_ok
          else "Network: CHECK FAILED: " + "; ".join(web + [c[:120] for c in risky]))
    for top in output_roots(folder):
        for base, dirs, files in os.walk(top):
            dirs[:] = [d for d in dirs if d != ".claude" and os.path.join(base, d) != fixture_copy]
            if "audit-report.md" in files:
                print(f"Audit report: {os.path.join(base, 'audit-report.md')}")
    away = outside_writes(transcript, output_roots(folder))
    print("Writes outside the eval folder and scratchpad (flagged, not failed): "
          + (", ".join(away) if away else "none seen"))
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

    # Word counts: the kit's files, or, with no kit (a baseline or a person
    # who went quiet), every text file the run wrote.
    if kit:
        words = word_counts(kit_files(kit), kit)
        print(f"Kit words per file (kit in {kit}):")
    else:
        roots = output_roots(folder)
        words = {}
        for p in written_files(folder, fixture_copy):
            base = next((r for r in roots if p.startswith(r + os.sep)), folder)
            words.update(word_counts([p], base))
        print("Words per file written (no kit found):")
    for name, w in sorted(words.items()):
        print(f"  {w:>6}  {name}")
    print(f"  {sum(words.values()):>6}  total")

    ok = False
    base_ok = isolation_ok and fixture_ok and network_ok and screens_ok
    if went_quiet and not kit:
        # The person stopped answering: Blueprint passes when it saved a state
        # file the person can resume from, and broke nothing on the way.
        saved = state_files(folder, fixture_copy)
        print(f"Person went quiet after reply {went_quiet}; state files saved: "
              + (", ".join(saved) if saved else "none"))
        ok = base_ok and bool(saved)
        print("RESULT PASS" if ok else "RESULT FAIL")
    elif not kit:
        print("RESULT FAIL: no kit was written")
    else:
        checker = os.path.join(stage, "skill", "scripts", "check_kit.py")
        proc = subprocess.run([sys.executable, checker, kit] + (["--screens"] if args.screens else []),
                              capture_output=True, text=True)
        print(proc.stdout.strip())
        name, body = upkeep_section(kit)
        lines = [ln for ln in body.split("\n") if ln.strip()]
        print(f"check_kit.py exit {proc.returncode}; Keeping it running in {name}: {len(lines)} non-empty lines")
        ok = proc.returncode == 0 and bool(lines) and base_ok
        print("RESULT PASS" if ok else "RESULT FAIL")
    if went_quiet and kit:
        print(f"Person went quiet after reply {went_quiet}, after a kit was written.")
    if args.keep:
        print(f"Kept: {folder} and its transcript {transcript}")
    else:
        for top in output_roots(folder):
            shutil.rmtree(top, ignore_errors=True)
        shutil.rmtree(home, ignore_errors=True)
        if os.path.isfile(transcript):
            os.remove(transcript)
    return {"ok": ok, "cost": cost, "model": model, "route": route, "words": words,
            "kit": bool(kit), "quiet": went_quiet, "subagents": subagents}


def spread(results, args):
    """The summary across runs: pass count, cost, and kit words min to max."""
    n = len(results)
    passed = sum(1 for r in results if r["ok"])
    lines = [f"\n===== Summary: {passed} of {n} runs passed =====",
             f"Skill: {'none (baseline, --no-skill)' if args.no_skill else args.skill_ref}; "
             f"persona: {os.path.basename(args.persona)}; subagents allowed: {args.allow_subagents}",
             "Models: " + ", ".join(sorted({r['model'] or 'unknown' for r in results})),
             "Routes named: " + ", ".join(r["route"] or "none" for r in results),
             f"Kits written: {sum(1 for r in results if r['kit'])} of {n}; "
             f"subagent calls per run: {', '.join(str(r['subagents']) for r in results)}",
             f"Cost: about {sum(r['cost'] for r in results):.2f} USD in all"]
    totals = [sum(r["words"].values()) for r in results]
    lines.append(f"Words written per run: {', '.join(map(str, totals))} (min {min(totals)}, max {max(totals)})")
    names = sorted({k for r in results for k in r["words"]})
    if names:
        lines.append("Words per file, min to max across runs (runs with the file):")
        for name in names:
            vals = [r["words"][name] for r in results if name in r["words"]]
            lines.append(f"  {name}: {min(vals)} to {max(vals)} ({len(vals)} of {n})")
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--prompt", required=True)
    ap.add_argument("--skill-ref", default="HEAD")
    ap.add_argument("--no-skill", action="store_true",
                    help="baseline: the same run with no Blueprint installed")
    ap.add_argument("--fixture", default="")
    ap.add_argument("--repo-ref", default="")
    ap.add_argument("--persona", default="you-decide",
                    help="a name in evals/personas/ (you-decide, disagrees, goes-quiet) or a file")
    ap.add_argument("--runs", type=int, default=1, help="repeat the run N times and report the spread")
    ap.add_argument("--rounds", type=int, default=14)
    ap.add_argument("--max-turns", type=int, default=40)
    ap.add_argument("--model", default="", help="model for Blueprint (and the person, unless --person-model)")
    ap.add_argument("--person-model", default="", help="model for the simulated person (default: --model)")
    ap.add_argument("--allow-subagents", action="store_true",
                    help=f"add the {SUBAGENT_TOOL} tool, so fresh-eyes reviews can use a subagent")
    ap.add_argument("--screens", action="store_true")
    ap.add_argument("--keep", action="store_true")
    args = ap.parse_args()
    if args.runs < 1:
        ap.error("--runs must be at least 1")
    if args.fixture and args.repo_ref:
        ap.error("give --fixture or --repo-ref, not both")
    args.persona = resolve_persona(args.persona)
    args.tools = TOOLS + ("," + SUBAGENT_TOOL if args.allow_subagents else "")
    if shutil.which("claude") is None:
        sys.exit("FAIL: the claude command is not installed")

    stage = tempfile.mkdtemp(prefix="blueprint-behaviour-stage-")
    # The skill is staged even with --no-skill: the kit check runs from it.
    rr.git_archive(args.skill_ref, "skill", stage)
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
        args.prompt += (f"\n\nNote: the {REPO_COPY} folder holds the repository's tracked files only. "
                        "It leaves out the git history, which is kept on GitHub.")
    persona = open(args.persona, encoding="utf-8").read()
    print(f"Persona: {args.persona}; runs: {args.runs}; model: {args.model or 'default'}; "
          f"tools: {args.tools}")
    results = [run_once(args, stage, persona, n) for n in range(1, args.runs + 1)]
    shutil.rmtree(stage, ignore_errors=True)
    print(spread(results, args))
    return 0 if all(r["ok"] for r in results) else 1


if __name__ == "__main__":
    sys.exit(main())
