#!/usr/bin/env python3
"""Readiness check for a Blueprint execution kit.

Usage: python3 check_kit.py <kit folder> [--coded] [--screens]

  --coded    the project is software: the brief needs a security baseline.
             Only this flag sets it; having tasks.json does not, because a
             Claude Code kit for a business plan has tasks.json too.
  --screens  step 3D ran: the kit needs design-spec.md

A large brief may be split into build-brief-1.md, build-brief-2.md, ...
(in the kit folder or docs/): each part is held to the brief's word limit,
and the required sections are looked for across the parts together.
kit-lite.md renamed to CLAUDE.md, as its setup line says, still counts as
a small kit when it has "Instructions" and "Brief" sections.

Checks, each because a fresh builder can't ask what the planner meant:
  1. Required files and sections are present, and no required section is empty.
     The brief and kit-lite need "Keeping it running", because every kit
     says who looks after the result and how.
  2. No template placeholders such as <PROJECT NAME> remain (common HTML
     tags in prose, such as <label>, are not placeholders).
  3. Every task has a title, who does it, and an acceptance check with an
     expected result (tasks.json, "### T-n:" headings, or a task table with
     a "Title" column); tasks.json passes check_tasks.py, which also rejects
     depends_on loops.
  4. Every decision row (D-n) has a reason.
  5. In the kit files the builder follows, versions and prices have an
     "as of" date in the same section. Other Markdown files kept in the kit
     as evidence (an audit report, an amendment) may instead carry one
     "as of" date near the top that covers the whole file. The kit's own
     version number ("Kit version 1.1") needs no date.
  6. Relative links resolve.
  7. Word counts are within the size budgets.

Exit 0 when every check passes, 1 when any fails, 2 on a usage error or
a file that can't be read (for example, one not saved as UTF-8).
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
    # Names as delivered first, then as placed in Claude Code, then the
    # numbered names that kits before 3.0.1 used, so older kits still check.
    "start": ["START-HERE.md", "00-START-HERE.md"],
    "instructions": ["project-instructions.md", "CLAUDE.md", "01-project-instructions.md"],
    "brief": ["build-brief.md", "docs/build-brief.md", "02-build-brief.md"],
    "log": ["progress-log.md", "docs/progress-log.md", "03-progress-log.md"],
    "review": ["final-review.md", "docs/final-review.md", "04-final-review.md"],
    "spec": ["design-spec.md", "docs/design-spec.md"],
    "lite": ["kit-lite.md"],
    "tasks": ["tasks.json", "docs/tasks.json"],
}
SECTIONS = {
    "start": ["Before you start", "Set up", "First message", "Kit files"],
    "instructions": ["Intent", "Start of every session", "Evidence", "Context",
                     "Saving work", "When to stop and ask", "Final review"],
    "brief": ["Intent", "Decisions", "Rules and examples", "Formats that last",
              "Keeping it running", "Tasks", "Definition of done"],
    "log": ["Where things stand", "Decisions", "Change requests", "Handoff notes"],
    "review": ["Run the product", "Lenses", "Scoring", "What the person sees"],
    "spec": ["Tokens", "Component library", "Required states",
             "Accessibility checks", "Do", "Don't", "Screenshot check"],
    "lite": ["Instructions", "Brief", "Keeping it running", "Tasks", "Progress log",
             "Definition of done"],
}
WORD_LIMITS = {"brief": 8000, "instructions": 1200, "lite": 3000}
LITE_INSTRUCTIONS_LIMIT = 600

# Lowercase HTML tags a kit may name in prose ("add a <label>"). Words the
# templates use as placeholders, such as <time>, <source> and <title>, are
# left out, and the match is case-sensitive, so <LABEL> is still flagged.
HTML_TAGS = {"a", "abbr", "article", "aside", "audio", "b", "blockquote", "br",
             "button", "canvas", "code", "details", "div", "em", "fieldset",
             "figcaption", "figure", "footer", "form", "h1", "h2", "h3", "h4",
             "h5", "h6", "header", "hr", "i", "iframe", "img", "input", "kbd",
             "label", "li", "main", "mark", "nav", "ol", "p", "pre", "s",
             "script", "section", "small", "span", "strong", "sub", "summary",
             "sup", "svg", "table", "tbody", "td", "textarea", "th", "thead",
             "tr", "u", "ul", "video"}
PLACEHOLDER = re.compile(r"<([^<>\n]{1,80})>")
FENCE = re.compile(r"^\s*(```|~~~)")
HEADING = re.compile(r"^(#{1,6})\s+(.*?)\s*#*\s*$")
MD_LINK = re.compile(r"\]\(\s*<?([^)>\s]+)>?(?:\s+\"[^\"]*\")?\s*\)")
# x.y.z, but not a dotted-quad IP address such as 127.0.0.1.
VERSION = re.compile(r"\bv\d+(\.\d+)+\b|(?<![\d.])\d+\.\d+\.\d+(?!\.?\d)|\bversion \d", re.I)
KIT_VERSION = re.compile(r"\bkit version \S+", re.I)
FILE_AS_OF_LINES = 15  # an evidence file's "as of" must sit this near the top
BRIEF_PART = re.compile(r"^build-brief-([1-9][0-9]*)\.md$")
PRICE = re.compile(r"[$€£]\s?\d|\b\d[\d,.]*\s?(USD|EUR|GBP)\b|\bper month\b|/month\b|/mo\b", re.I)
AS_OF = re.compile(r"\bas of\b", re.I)

failures = []


class Unreadable(Exception):
    pass


def fail(where, message):
    failures.append(f"{where}: {message}")


def read(path):
    try:
        with open(path, encoding="utf-8") as f:
            return f.read()
    except UnicodeDecodeError:
        raise Unreadable(f"{os.path.relpath(path)}: not UTF-8; re-save it as UTF-8")
    except OSError as e:
        raise Unreadable(f"{os.path.relpath(path)}: can't be read ({e.strerror})")


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


def col(header, *names, skip_first=False):
    for i, h in enumerate(header):
        if skip_first and i == 0:
            continue
        if any(n in h.lower() for n in names):
            return i
    return None


def title_col(header):
    """The task-title column: an exact "Title" header first, then a header
    containing "title", then one containing "task" other than the ID column."""
    for i, h in enumerate(header):
        if h.strip("*_ ").lower() == "title":
            return i
    found = col(header, "title")
    return found if found is not None else col(header, "task", skip_first=True)


def brief_parts(kit):
    """build-brief-1.md, build-brief-2.md... in the kit folder, else docs/."""
    for sub in ("", "docs"):
        folder = os.path.join(kit, sub)
        if not os.path.isdir(folder):
            continue
        matched = [(BRIEF_PART.match(f), f) for f in os.listdir(folder)]
        parts = sorted((int(m.group(1)), os.path.join(sub, f) if sub else f)
                       for m, f in matched if m)
        if parts:
            return parts
    return []


def main(argv):
    try:
        return run(argv)
    except Unreadable as e:
        print(f"Can't check the kit: {e}")
        return 2


def run(argv):
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
    # kit-lite renamed to CLAUDE.md, as its setup line tells the person to.
    if "lite" not in files and files.get("instructions") == "CLAUDE.md":
        heads = [h for h, lv, b in sections(strip_code(read(os.path.join(kit, "CLAUDE.md"))))]
        if (any(matches(h, "Instructions") for h in heads)
                and any(matches(h, "Brief") for h in heads)):
            files["lite"] = files.pop("instructions")
    # A large brief in numbered parts.
    parts = brief_parts(kit)
    briefs = ([files["brief"]] if "brief" in files else []) + [n for i, n in parts]
    if parts:
        files.setdefault("brief", parts[0][1])
        numbers = [i for i, n in parts]
        for gap in sorted(set(range(1, max(numbers) + 1)) - set(numbers)):
            fail("files", f"build-brief-{gap}.md is missing between the brief's parts")
    small = "lite" in files
    coded = "--coded" in flags
    needed = ["lite", "review"] if small else ["start", "instructions", "brief", "log", "review"]
    if "--screens" in flags:
        needed.append("spec")
    if "CLAUDE.md" == files.get("instructions") and not small:
        needed.append("tasks")
    for role in needed:
        if role not in files:
            extra = " (or a brief in parts: build-brief-1.md, build-brief-2.md...)" if role == "brief" else ""
            fail("files", f"{' or '.join(ROLES[role])} is missing{extra}")

    # 1. Sections, and 7. word counts.
    for role, name in files.items():
        if role not in SECTIONS:
            continue
        group = briefs if role == "brief" else [name]
        texts = {n: read(os.path.join(kit, n)) for n in group}
        secs = [s for n in group for s in sections(strip_code(texts[n]))]
        name = " + ".join(group)
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
        for n, text in texts.items():
            if role in WORD_LIMITS and words(text) > WORD_LIMITS[role]:
                fail(n, f"{words(text):,} words; the budget is under {WORD_LIMITS[role]:,}"
                     + (" (split the brief into build-brief-1.md, build-brief-2.md...)"
                        if role == "brief" else ""))
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
                if tag and tag.group(1) in HTML_TAGS:
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
    task_files = briefs + [files[r] for r in ("lite", "log") if r in files]
    for name in task_files:
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
            ti, di, ei = title_col(header), col(header, "done by"), col(header, "expected")
            if di is None and ei is None:
                continue  # a status table, not a task list
            task_count += 1
            for idx, what in ((ti, "a title"), (di, "who does it (Done by)"), (ei, "an expected result")):
                if idx is None or idx >= len(cells) or not cells[idx]:
                    fail(name, f"{cells[0]}'s table row is missing {what}")
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
    kit_files = {os.path.normpath(os.path.join(kit, n)) for n in list(files.values()) + briefs}
    for p in md_files:
        rel = os.path.relpath(p, kit)
        lines = strip_code(read(p))
        secs = sections(lines) or [("", 0, lines)]
        # Evidence files (not kit roles) may be dated once, near the top.
        file_dated = (os.path.normpath(p) not in kit_files
                      and AS_OF.search("\n".join(read(p).split("\n")[:FILE_AS_OF_LINES])))
        for i, (h, lv, body) in enumerate([] if file_dated else secs):
            own = KIT_VERSION.sub("", h + "\n" + "\n".join(body))
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
