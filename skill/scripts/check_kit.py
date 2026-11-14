#!/usr/bin/env python3
"""Readiness check for a Blueprint execution kit.

Usage: python3 check_kit.py <kit folder> [--coded] [--screens]

  --coded    the project is software: the brief needs a security baseline,
             and a medium or large brief its "Checklist coverage:" line.
             Only this flag sets it; having tasks.json does not, because a
             Claude Code kit for a business plan has tasks.json too. A kit
             with tasks.json checked without it prints a NOTE (not a fail),
             and so does a coded one with tasks.json (built in Claude Code)
             whose brief has no "Project settings" section.
  --screens  step 3D ran: the kit needs design-spec.md

A large brief may be split into build-brief-1.md, build-brief-2.md, ...
(in the kit folder or docs/): each part is held to the brief's word limit,
and the required sections are looked for across the parts together.
A small kit is project-instructions.md (CLAUDE.md in Claude Code, under
600 words) plus kit-lite.md and final-review.md (or docs/ copies). Kits
from before 3.2 kept the instructions inside kit-lite.md, as its
"Instructions" section, and may have renamed the whole file to CLAUDE.md;
both still count as small kits.

Checks, each because a fresh builder can't ask what the planner meant:
  1. Required files and sections are present, and no required section is empty.
     The brief and kit-lite need "Keeping it running", because every kit
     says who looks after the result and how.
  2. No template placeholders such as <PROJECT NAME> remain. Not
     placeholders: common HTML tags written as real tags (<label>, </label>,
     <br/>, <input type="email" required>), one PascalCase component name
     (<Button>), and a "<" followed by a space or by a number and more words
     ("< 3 letters"), which is a comparison in prose.
  3. Every task has a title, who does it, and an acceptance check with an
     expected result (tasks.json, "### T-n:" headings, or a task table with
     a "Title" column); tasks.json passes check_tasks.py, which also rejects
     depends_on loops. In a table, a task with several checks may take one
     row per check: later rows (same T-n, or a blank Task cell) need only
     the expected result. Tasks are counted by unique ID.
  4. Every decision row (D-n) has a reason.
  5. In the kit files the builder follows, versions and prices have an
     "as of" date in the same section. Other Markdown files kept in the kit
     as evidence (an audit report, an amendment) may instead carry one
     "as of" date near the top that covers the whole file. The kit's own
     version number ("Kit version 1.1") and versions in a "Sources" section
     need no date. A price is a money amount (a currency symbol or code) or
     a "free tier"; "2 hours per month" is not a price.
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
    "lite": ["kit-lite.md", "docs/kit-lite.md"],
    "tasks": ["tasks.json", "docs/tasks.json"],
}
# A tuple lists the names a section may have, newest first; the older ones
# are from kits before 3.2, so those still check.
SECTIONS = {
    "start": ["Before you start", "Set up", "First message", "Kit files"],
    "instructions": ["Intent", ("How you work", "Start of every session"), "Evidence",
                     ("Compact Instructions", "Context"), "Saving work",
                     "When to stop and ask", "Final review"],
    "lite_instructions": [],
    "brief": ["Intent", "Decisions", "Rules and examples", "Formats that last",
              "Keeping it running", "Tasks", "Definition of done"],
    "log": ["Where things stand", "Decisions", "Change requests", "Handoff notes"],
    "review": ["Run the product", "Lenses", "Scoring", "What the person sees"],
    "spec": ["Tokens", "Component library", "Required states",
             "Accessibility checks", "Do", "Don't", "Screenshot check"],
    "lite": ["Brief", "Keeping it running", "Tasks", "Progress log",
             "Definition of done"],
}
WORD_LIMITS = {"brief": 8000, "instructions": 1200, "lite": 3000, "lite_instructions": 600}
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
# Attributes that may stand without a value (<input required>). Any other
# bare word after a tag name makes it a placeholder (<input file>,
# <header row, separator>), because a false READY is the worst outcome.
BOOLEAN_ATTRS = {"allowfullscreen", "async", "autofocus", "autoplay", "checked",
                 "controls", "default", "defer", "disabled", "formnovalidate",
                 "hidden", "inert", "ismap", "loop", "multiple", "muted",
                 "nomodule", "novalidate", "open", "playsinline", "readonly",
                 "required", "reversed", "selected"}
PLACEHOLDER = re.compile(r"<([^<>\n]{1,80})>")
# Real tag syntax only: a tag name, then name="value", name='value' or a
# boolean attribute, then an optional "/".
TAG = re.compile(r"""/?([a-z][a-z0-9]*)((?:\s+[a-z][a-z0-9_:.-]*(?:\s*=\s*(?:"[^"]*"|'[^']*'))?)*)\s*/?""")
ATTR = re.compile(r"""([a-z][a-z0-9_:.-]*)(\s*=\s*(?:"[^"]*"|'[^']*'))?""")
# A component name in prose (<Button>, </DatePicker>, <Button/>).
COMPONENT = re.compile(r"/?[A-Z][a-z0-9]+(?:[A-Z][a-z0-9]*)*\s*/?")
FENCE = re.compile(r"^\s*(```|~~~)")
HEADING = re.compile(r"^(#{1,6})\s+(.*?)\s*#*\s*$")
MD_LINK = re.compile(r"\]\(\s*<?([^)>\s]+)>?(?:\s+\"[^\"]*\")?\s*\)")
# x.y.z, but not a dotted-quad IP address such as 127.0.0.1.
# "version 2.1" counts; "version 1" in prose ("out of scope for version 1")
# does not, so an undotted "version 5" goes unflagged.
VERSION = re.compile(r"\bv\d+(\.\d+)+\b|(?<![\d.])\d+\.\d+\.\d+(?!\.?\d)|\bversion \d+\.\d", re.I)
COVERAGE = re.compile(r"checklist coverage\**\s*:", re.I)
KIT_VERSION = re.compile(r"\bkit version \S+", re.I)
FILE_AS_OF_LINES = 15  # an evidence file's "as of" must sit this near the top
BRIEF_PART = re.compile(r"^build-brief-([1-9][0-9]*)\.md$")
# A money amount: a currency symbol or code, or "free tier". "Per month"
# alone is not a price ("2 hours per month"); it counts only after money.
PRICE = re.compile(r"[$€£¥₹]\s?\d|\b\d[\d,.]*\s?(USD|EUR|GBP|CAD|AUD|JPY|CHF|INR)\b"
                   r"|\b(USD|EUR|GBP|CAD|AUD|JPY|CHF|INR)\s?\d|\bfree tier\b", re.I)
AS_OF = re.compile(r"\bas of\b", re.I)

failures = []
notes = []


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


def is_placeholder(inner):
    """Whether the text between < and > is an unfilled template placeholder."""
    if inner[:1].isspace():
        return False  # "< 3 letters": a comparison in prose
    if inner[:1].isdigit() and re.search(r"\s", inner):
        return False  # "<3 letters shows nothing; with >"; <1.0> stays flagged
    if inner.startswith(("!--", "http://", "https://", "mailto:")):
        return False
    if COMPONENT.fullmatch(inner):
        return False  # <Button>: one PascalCase word, a component name
    tag = TAG.fullmatch(inner)
    if not tag or tag.group(1) not in HTML_TAGS:
        return True
    for attr in ATTR.finditer(tag.group(2)):
        if not attr.group(2) and attr.group(1) not in BOOLEAN_ATTRS:
            return True  # <input file>, <section name>: words, not attributes
    return False


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
    # A 3.2 small kit keeps its instructions in their own file; an older one
    # keeps them in kit-lite.md's "Instructions" section.
    lite_has_instructions = small and any(
        matches(h, "Instructions") for h, lv, b in sections(strip_code(read(os.path.join(kit, files["lite"])))))
    if small and "instructions" in files:
        files["lite_instructions"] = files.pop("instructions")
    coded = "--coded" in flags
    needed = ["lite", "review"] if small else ["start", "instructions", "brief", "log", "review"]
    if small and not lite_has_instructions:
        needed.append("lite_instructions")
    if "--screens" in flags:
        needed.append("spec")
    if "CLAUDE.md" == files.get("instructions") and not small:
        needed.append("tasks")
    for role in needed:
        if role not in files:
            extra = " (or a brief in parts: build-brief-1.md, build-brief-2.md...)" if role == "brief" else ""
            names = ROLES["instructions"][:2] if role == "lite_instructions" else ROLES[role]
            what = " (the small kit's instructions)" if role == "lite_instructions" else ""
            fail("files", f"{' or '.join(names)} is missing{what}{extra}")

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
        if role == "lite" and lite_has_instructions:
            required.insert(0, "Instructions")
        for req in required:
            alts = req if isinstance(req, tuple) else (req,)
            idx = [i for i, s in enumerate(secs) if any(matches(s[0], a) for a in alts)]
            if not idx:
                fail(name, f"section '{alts[0]}' is missing")
            elif not section_text(secs, idx[0]).strip():
                fail(name, f"section '{alts[0]}' is empty")
        if role == "brief" and coded:
            base = [i for i, s in enumerate(secs) if matches(s[0], "Security baseline")]
            if base and not any(COVERAGE.search(section_text(secs, i)) for i in base):
                fail(name, "the Security baseline has no 'Checklist coverage:' line "
                     "(every checklist item: D-n, F-n or 'N/A: reason')")
            if "tasks" in files and not any(matches(s[0], "Project settings") for s in secs):
                notes.append("NOTE: the brief has no 'Project settings' section: a coded kit "
                             "built in Claude Code should carry the exact .claude/settings.json "
                             "its first task writes")
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
                if is_placeholder(m.group(1)):
                    fail(os.path.relpath(p, kit), f"line {n} still has the placeholder "
                         f"<{m.group(1).strip()}> (fill it in; if it is code, wrap it in backticks)")

    # 3. Tasks, counted by unique ID.
    task_ids = set()
    if "tasks" in files:
        try:
            data = json.loads(read(os.path.join(kit, files["tasks"])))
        except ValueError as e:
            data = None
            fail(files["tasks"], f"is not valid JSON ({e})")
        if data is not None:
            for problem in check_schema(data):
                fail(files["tasks"], problem)
            tasks = data.get("tasks") if isinstance(data, dict) else None
            for k, t in enumerate(tasks if isinstance(tasks, list) else [], 1):
                tid = t.get("id") if isinstance(t, dict) else None
                task_ids.add(tid if isinstance(tid, str) else f"{files['tasks']} #{k}")
    task_files = briefs + [files[r] for r in ("lite", "log") if r in files]
    for name in task_files:
        secs = sections(strip_code(read(os.path.join(kit, name))))
        for i, (h, lv, body) in enumerate(secs):
            m = re.match(r"(T-\d+)\s*[:.]?\s*(.*)", h.strip())
            if not m:
                continue
            task_ids.add(m.group(1))
            text = section_text(secs, i)
            if not m.group(2).strip():
                fail(name, f"{m.group(1)} has no title")
            if not re.search(r"done by:?\**\s*\**\s*(claude|the person|person|both)", text, re.I):
                fail(name, f"{m.group(1)} doesn't say who does it (Done by: Claude, person or both)")
            if not re.search(r"expected:?\**\s*\S", text, re.I):
                fail(name, f"{m.group(1)} has no acceptance check with an expected result")
        # A task with several checks takes one row per check, as the log
        # template says: a later row with the same ID, or a blank ID cell
        # right after a task row, continues that task and needs only its
        # expected result.
        seen, last, last_header = set(), None, None
        for header, cells in table_rows(strip_code(read(os.path.join(kit, name)))):
            if header is not last_header:
                last, last_header = None, header
            first = cells[0] if cells else ""
            if re.fullmatch(r"T-\d+", first):
                tid = first
            elif not first and last:
                tid = last
            else:
                last = None
                continue
            ti, di, ei = title_col(header), col(header, "done by"), col(header, "expected")
            if di is None and ei is None:
                continue  # a status table, not a task list
            last = tid
            task_ids.add(tid)
            checks = [(ei, "an expected result")]
            if tid not in seen:
                checks = [(ti, "a title"), (di, "who does it (Done by)")] + checks
            seen.add(tid)
            for idx, what in checks:
                if idx is None or idx >= len(cells) or not cells[idx]:
                    fail(name, f"{tid}'s table row is missing {what}")
    task_count = len(task_ids)
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
            # A Sources list names versions in its titles ("Django 5.1
            # release notes"); each entry carries its own date.
            version = VERSION.search(own) and not matches(h, "Sources")
            if (version or PRICE.search(own)) and not AS_OF.search(own):
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
    if "tasks" in files and not coded:
        print("NOTE: not checked as coded: if this is software, re-run with --coded "
              "(the security baseline is checked only then)")
    for n in notes:
        print(n)
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
