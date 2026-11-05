#!/usr/bin/env python3
"""Readiness check for a Blueprint execution kit.

Usage: python3 check_kit.py <kit folder> [--coded] [--screens]

  --coded    the project is software: the brief needs a security baseline
             (on by default when the kit has docs/tasks.json)
  --screens  step 3D ran: the kit needs design-spec.md

Checks, each because a fresh builder can't ask what the planner meant:
  1. Required files and sections are present, and no required section is empty.
  2. No template placeholders such as <PROJECT NAME> remain.
  3. Every task has a title, who does it, and an acceptance check with an
     expected result (docs/tasks.json, "### T-n:" headings, or a task table).
  4. Every decision row (D-n) has a reason.
  5. Versions and prices have an "as of" date in the same section.
  6. Relative links resolve.
  7. Word counts are within the size budgets.

Exit 0 when every check passes, 1 when any fails, 2 on a usage error.
Python 3 standard library only. Where code can't run, walk the same list
by hand. The section names below must match the kit templates.
"""
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from check_tasks import check_schema  # noqa: E402

# Kit roles: accepted file names (Claude project first, then Claude Code).
ROLES = {
    "start": ["00-START-HERE.md"],
    "instructions": ["01-project-instructions.md", "CLAUDE.md"],
    "brief": ["02-build-brief.md", "docs/build-brief.md"],
    "log": ["03-progress-log.md", "docs/progress-log.md"],
    "review": ["04-final-review.md", "docs/final-review.md"],
    "spec": ["design-spec.md", "docs/design-spec.md"],
    "lite": ["kit-lite.md"],
    "tasks": ["docs/tasks.json"],
}
SECTIONS = {
    "start": ["Before you start", "Set up", "First message", "Kit files"],
    "instructions": ["Intent", "Start of every session", "Evidence", "Context",
                     "Saving work", "When to stop and ask", "Final review"],
    "brief": ["Intent", "Decisions", "Rules and examples", "Formats that last",
              "Tasks", "Definition of done"],
    "log": ["Where things stand", "Decisions", "Change requests", "Handoff notes"],
    "review": ["Run the product", "Lenses", "Scoring", "What the person sees"],
    "spec": ["Tokens", "Component library", "Required states",
             "Accessibility checks", "Do", "Don't", "Screenshot check"],
    "lite": ["Instructions", "Brief", "Tasks", "Progress log", "Definition of done"],
}
WORD_LIMITS = {"brief": 8000, "instructions": 1200, "lite": 3000}
LITE_INSTRUCTIONS_LIMIT = 600

HTML_TAGS = {"a", "b", "br", "code", "details", "div", "em", "hr", "i", "img",
             "kbd", "li", "mark", "ol", "p", "pre", "s", "small", "span",
             "strong", "sub", "summary", "sup", "table", "td", "th", "tr",
             "u", "ul"}
PLACEHOLDER = re.compile(r"<([^<>\n]{1,80})>")
FENCE = re.compile(r"^\s*(```|~~~)")
HEADING = re.compile(r"^(#{1,6})\s+(.*?)\s*#*\s*$")
MD_LINK = re.compile(r"\]\(\s*<?([^)>\s]+)>?(?:\s+\"[^\"]*\")?\s*\)")
VERSION = re.compile(r"\bv\d+(\.\d+)+\b|\b\d+\.\d+\.\d+\b|\bversion \d", re.I)
PRICE = re.compile(r"[$€£]\s?\d|\b\d[\d,.]*\s?(USD|EUR|GBP)\b|\bper month\b|/month\b|/mo\b", re.I)
AS_OF = re.compile(r"\bas of\b", re.I)

failures = []


def fail(where, message):
    failures.append(f"{where}: {message}")


def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def strip_code(text):
    """Blank out fenced blocks and inline code, keeping line numbers."""
    out, in_fence = [], False
    for line in text.split("\n"):
        if FENCE.match(line):
            in_fence = not in_fence
            out.append("")
            continue
        out.append("" if in_fence else re.sub(r"`[^`]*`", "", line))
    return out


def norm(heading):
    h = re.sub(r"^\d+(\.\d+)*\.?\s+", "", heading.strip())  # "3. Tasks" -> "Tasks"
    return h.replace("’", "'").strip("*_ ").lower()


def sections(lines):
    """[(heading, level, body lines)] for every heading."""
    found, current = [], None
    for line in lines:
        m = HEADING.match(line)
        if m:
            current = (m.group(2), len(m.group(1)), [])
            found.append(current)
        elif current:
            current[2].append(line)
    return found


def section_text(secs, i):
    """A section's own text plus its subsections' text."""
    level, body = secs[i][1], list(secs[i][2])
    for h, lv, b in secs[i + 1:]:
        if lv <= level:
            break
        body += [h] + b
    return "\n".join(body)


def matches(heading, name):
    h, n = norm(heading), name.lower()
    return h == n or (h.startswith(n) and not h[len(n)].isalnum())


def words(text):
    return len(re.findall(r"\S+", text))


def table_rows(lines):
    """Yield (header cells, row cells) for Markdown tables."""
    header = None
    for line in lines:
        s = line.strip()
        if not s.startswith("|"):
            header = None
            continue
        cells = [c.strip() for c in s.strip("|").split("|")]
        if header is None:
            header = cells
        elif all(re.fullmatch(r":?-{2,}:?", c) for c in cells if c):
            continue
        else:
            yield header, cells


def col(header, *names):
    for i, h in enumerate(header):
        if any(n in h.lower() for n in names):
            return i
    return None


def main(argv):
    args = [a for a in argv[1:] if not a.startswith("--")]
    flags = {a for a in argv[1:] if a.startswith("--")}
    if len(args) != 1 or flags - {"--coded", "--screens"} or not os.path.isdir(args[0]):
        print(__doc__.strip().split("\n\n")[1].split("\n")[0])
        return 2
    kit = os.path.abspath(args[0])

    files = {}
    for role, names in ROLES.items():
        for n in names:
            if os.path.isfile(os.path.join(kit, n)):
                files[role] = n
                break
    small = "lite" in files
    coded = "--coded" in flags or "tasks" in files
    needed = ["lite", "review"] if small else ["start", "instructions", "brief", "log", "review"]
    if "--screens" in flags:
        needed.append("spec")
    if "CLAUDE.md" == files.get("instructions") and not small:
        needed.append("tasks")
    for role in needed:
        if role not in files:
            fail("files", f"{' or '.join(ROLES[role])} is missing")

    # 1. Sections, and 7. word counts.
    for role, name in files.items():
        if role not in SECTIONS:
            continue
        text = read(os.path.join(kit, name))
        secs = sections(strip_code(text))
        required = list(SECTIONS[role])
        if role in ("brief", "lite") and coded:
            required.append("Security baseline")
        if role == "log" and "tasks" not in files:
            required.append("Tasks")
        for req in required:
            idx = [i for i, s in enumerate(secs) if matches(s[0], req)]
            if not idx:
                fail(name, f"section '{req}' is missing")
            elif not section_text(secs, idx[0]).strip():
                fail(name, f"section '{req}' is empty")
        if role in WORD_LIMITS and words(text) > WORD_LIMITS[role]:
            fail(name, f"{words(text):,} words; the budget is under {WORD_LIMITS[role]:,}")
        if role == "lite":
            for i, s in enumerate(secs):
                if matches(s[0], "Instructions") and words(section_text(secs, i)) > LITE_INSTRUCTIONS_LIMIT:
                    fail(name, f"the instructions part is over {LITE_INSTRUCTIONS_LIMIT} words")

    md_files, all_files = [], []
    for root, dirs, fs in os.walk(kit):
        dirs[:] = sorted(d for d in dirs if not d.startswith("."))
        for f in sorted(fs):
            p = os.path.join(root, f)
            all_files.append(p)
            if f.endswith(".md"):
                md_files.append(p)

    # 2. Placeholders (Markdown and JSON).
    for p in all_files:
        if not p.endswith((".md", ".json")):
            continue
        lines = strip_code(read(p)) if p.endswith(".md") else read(p).split("\n")
        for n, line in enumerate(lines, 1):
            for m in PLACEHOLDER.finditer(line):
                inner = m.group(1).strip()
                tag = re.match(r"/?([a-zA-Z][a-zA-Z0-9]*)(\s[^>]*)?/?$", inner)
                if inner.startswith(("!--", "http://", "https://", "mailto:")):
                    continue
                if tag and tag.group(1).lower() in HTML_TAGS:
                    continue
                fail(os.path.relpath(p, kit), f"line {n} still has the placeholder <{inner}>")

    # 3. Tasks.
    task_count = 0
    if "tasks" in files:
        try:
            data = json.loads(read(os.path.join(kit, files["tasks"])))
        except ValueError as e:
            data = None
            fail(files["tasks"], f"is not valid JSON ({e})")
        if data is not None:
            for problem in check_schema(data):
                fail(files["tasks"], problem)
            task_count += len(data.get("tasks", [])) if isinstance(data, dict) else 0
    for role in ("brief", "lite", "log"):
        if role not in files:
            continue
        name = files[role]
        secs = sections(strip_code(read(os.path.join(kit, name))))
        for i, (h, lv, body) in enumerate(secs):
            m = re.match(r"(T-\d+)\s*[:.]?\s*(.*)", h.strip())
            if not m:
                continue
            task_count += 1
            text = section_text(secs, i)
            if not m.group(2).strip():
                fail(name, f"{m.group(1)} has no title")
            if not re.search(r"done by:?\**\s*\**\s*(claude|the person|person|both)", text, re.I):
                fail(name, f"{m.group(1)} doesn't say who does it (Done by: Claude, person or both)")
            if not re.search(r"expected:?\**\s*\S", text, re.I):
                fail(name, f"{m.group(1)} has no acceptance check with an expected result")
        for header, cells in table_rows(strip_code(read(os.path.join(kit, name)))):
            if not cells or not re.fullmatch(r"T-\d+", cells[0]):
                continue
            ti, di, ei = col(header, "title", "task"), col(header, "done by"), col(header, "expected")
            if di is None and ei is None:
                continue  # a status table, not a task list
            task_count += 1
            for idx, what in ((ti, "a title"), (di, "who does it"), (ei, "an expected result")):
                if idx is None or idx >= len(cells) or not cells[idx]:
                    fail(name, f"{cells[0]} has no {what} in its table row")
    if task_count == 0:
        fail("tasks", "no tasks found (docs/tasks.json, '### T-n: title' headings, or a task table)")

    # 4. Decision reasons.
    for p in md_files:
        for header, cells in table_rows(strip_code(read(p))):
            if not cells or not re.fullmatch(r"D-\d+", cells[0]):
                continue
            ri = col(header, "reason", "why")
            if ri is None or ri >= len(cells) or not cells[ri]:
                fail(os.path.relpath(p, kit), f"decision {cells[0]} has no reason")

    # 5. "As of" beside versions and prices, and 6. links.
    for p in md_files:
        rel = os.path.relpath(p, kit)
        lines = strip_code(read(p))
        secs = sections(lines) or [("", 0, lines)]
        for i, (h, lv, body) in enumerate(secs):
            own = h + "\n" + "\n".join(body)
            if (VERSION.search(own) or PRICE.search(own)) and not AS_OF.search(own):
                where = f"section '{h}'" if h else "the text"
                fail(rel, f"{where} has a version or price without an 'as of' date")
        for n, line in enumerate(lines, 1):
            for m in MD_LINK.finditer(line):
                target = m.group(1).split("#", 1)[0]
                if not target or re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", target):
                    continue
                cands = [os.path.join(os.path.dirname(p), target), os.path.join(kit, target)]
                if not any(os.path.exists(os.path.normpath(c)) for c in cands):
                    fail(rel, f"line {n} links to '{target}', which doesn't exist")

    print(f"Checking the kit in {kit}")
    print(f"Kit type: {'small (kit-lite)' if small else 'full'}; "
          f"{'coded' if coded else 'not coded'}; {task_count} tasks found")
    if failures:
        print(f"\nNOT READY: {len(failures)} problem(s) to fix:")
        for f in failures:
            print(f"  FAIL  {f}")
        return 1
    print("\nREADY by this check: files, sections, placeholders, tasks, decision "
          "reasons, dates, links and word counts all pass.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
