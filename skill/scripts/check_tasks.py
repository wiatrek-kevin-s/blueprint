#!/usr/bin/env python3
"""Check a kit's task list (tasks.json).

Usage: python3 check_tasks.py <tasks.json> [<baseline tasks.json>]

Checks the fields every task must have, that depends_on names tasks in the
list and has no loops (a task that waits on itself, directly or through
others, can never start), and that the optional "delivers" list holds
requirement or finding IDs (such as REQ-1 or AF-1) in the right form. It
does not check that every requirement has a task: nothing here reads the
brief's requirements, so that stays a planner's check. Given a baseline (the task list as the kit delivered it), it
also checks that the builder changed only each task's status and evidence
and added only R-n tasks (fixes from the final review); every other field,
delivers included, stays as delivered. The builder must not rewrite its own
acceptance checks, because then "done" stops meaning what the plan meant.

Malformed input (an id that isn't text, nested lists, a baseline of the
wrong shape) is reported as a problem, never as a crash. Exit 0 when every
check passes, 1 when any fails, 2 when a file can't be read. Python 3 standard library only.
"""
import json
import re
import sys

FIELDS = ["id", "title", "session", "depends_on", "done_by",
          "acceptance", "status", "evidence"]
OPTIONAL = ["delivers"]
DONE_BY = {"claude", "person", "both"}
STATUS = {"todo", "in_progress", "blocked", "done"}
ID_RE = re.compile(r"^[TR]-[1-9][0-9]*$")
DELIVERS_RE = re.compile(r"^[A-Z][A-Z0-9]*-[0-9]+$")
EDITABLE = {"status", "evidence"}


def blank(value):
    return not isinstance(value, str) or not value.strip()


def check_schema(data):
    """Return a list of problems in plain words; empty when the list is valid."""
    problems = []
    if not isinstance(data, dict) or not isinstance(data.get("tasks"), list):
        return ["the file must be an object with a 'tasks' list"]
    tasks = data["tasks"]
    if not tasks:
        problems.append("the task list is empty")
    ids = []
    for n, t in enumerate(tasks, 1):
        if not isinstance(t, dict):
            problems.append(f"task number {n} is not an object")
            continue
        name = t.get("id") if isinstance(t.get("id"), str) else f"task number {n}"
        for f in FIELDS:
            if f not in t:
                problems.append(f"{name}: field '{f}' is missing")
        for f in t:
            if f not in FIELDS and f not in OPTIONAL:
                problems.append(f"{name}: field '{f}' is not part of the format")
        if "id" in t:
            if not isinstance(t["id"], str) or not ID_RE.match(t["id"]):
                problems.append(f"{name}: id must look like T-1 or R-1")
            elif t["id"] in ids:
                problems.append(f"{name}: id is used twice")
            else:
                ids.append(t["id"])
        for f in ("title", "session"):
            if f in t and blank(t[f]):
                problems.append(f"{name}: '{f}' is empty")
        if "done_by" in t and (not isinstance(t["done_by"], str) or t["done_by"] not in DONE_BY):
            problems.append(f"{name}: done_by must be claude, person or both")
        if "status" in t and (not isinstance(t["status"], str) or t["status"] not in STATUS):
            problems.append(f"{name}: status must be todo, in_progress, blocked or done")
        if "depends_on" in t and (not isinstance(t["depends_on"], list)
                                  or not all(isinstance(d, str) for d in t["depends_on"])):
            problems.append(f"{name}: depends_on must be a list of task ids")
        if "delivers" in t and (not isinstance(t["delivers"], list)
                                or not all(isinstance(d, str) and DELIVERS_RE.match(d)
                                           for d in t["delivers"])):
            problems.append(f"{name}: delivers must be a list of requirement or finding IDs, such as REQ-1 or AF-1")
        acc = t.get("acceptance")
        if "acceptance" in t:
            if not isinstance(acc, list) or not acc:
                problems.append(f"{name}: needs at least one acceptance check")
            else:
                for k, a in enumerate(acc, 1):
                    if not isinstance(a, dict) or blank(a.get("how")) or blank(a.get("expected")):
                        problems.append(f"{name}: acceptance check {k} needs both 'how' and 'expected'")
                    elif set(a) - {"how", "expected"}:
                        problems.append(f"{name}: acceptance check {k} has fields other than 'how' and 'expected'")
        if "evidence" in t and not isinstance(t["evidence"], str):
            problems.append(f"{name}: evidence must be text")
        elif t.get("status") == "done" and blank(t.get("evidence")):
            problems.append(f"{name}: is done but has no evidence")
    # Only well-formed ids and string dependencies take part from here on;
    # the problems above already name the rest.
    by_id = {t["id"]: t for t in tasks if isinstance(t, dict) and isinstance(t.get("id"), str)}
    for t in tasks:
        if not isinstance(t, dict) or not isinstance(t.get("depends_on"), list):
            continue
        for d in t["depends_on"]:
            if not isinstance(d, str):
                continue
            if d not in by_id:
                problems.append(f"{t.get('id')}: depends on {d}, which is not in the list")
            elif t.get("status") == "done" and by_id[d].get("status") != "done":
                problems.append(f"{t.get('id')}: is done but {d}, which it depends on, is not")
    problems += find_cycles(by_id)
    return problems


def find_cycles(by_id):
    """Report each depends_on loop once, e.g. 'T-1 -> T-2 -> T-1'."""
    problems, state, seen = [], {}, set()

    def deps(tid):
        d = by_id[tid].get("depends_on")
        return [x for x in d if isinstance(x, str) and x in by_id] if isinstance(d, list) else []

    for start in by_id:
        if start in state:
            continue
        stack, path = [(start, iter(deps(start)))], [start]
        state[start] = "open"
        while stack:
            tid, it = stack[-1]
            nxt = next(it, None)
            if nxt is None:
                state[tid] = "closed"
                stack.pop()
                path.pop()
            elif state.get(nxt) == "open":
                loop = path[path.index(nxt):] + [nxt]
                key = frozenset(loop)
                if key not in seen:
                    seen.add(key)
                    if len(loop) == 2:
                        problems.append(f"{nxt}: depends on itself, so it can never start")
                    else:
                        problems.append(f"{' -> '.join(loop)}: these tasks depend on each other "
                                        "in a loop, so none of them can start")
            elif nxt not in state:
                state[nxt] = "open"
                stack.append((nxt, iter(deps(nxt))))
                path.append(nxt)
    return problems


def check_baseline(data, base):
    """Only status and evidence may change; only R-n tasks may be added."""
    problems = []
    if not isinstance(base, dict) or not isinstance(base.get("tasks"), list):
        return ["the baseline file must be an object with a 'tasks' list"]
    if not all(isinstance(b, dict) and isinstance(b.get("id"), str) for b in base["tasks"]):
        return ["every task in the baseline file must be an object with a text id"]
    for key in set(data) | set(base):
        if key != "tasks" and data.get(key) != base.get(key):
            problems.append(f"top-level field '{key}' changed; only status and evidence may change")
    now = {t["id"]: t for t in data["tasks"] if isinstance(t, dict) and isinstance(t.get("id"), str)}
    for b in base["tasks"]:
        tid = b.get("id")
        if tid not in now:
            problems.append(f"{tid}: was removed")
            continue
        t = now[tid]
        for f in sorted(set(b) | set(t)):
            if f not in EDITABLE and b.get(f) != t.get(f):
                problems.append(f"{tid}: field '{f}' changed; only status and evidence may change")
    base_ids = [b.get("id") for b in base["tasks"]]
    for tid in now:
        if tid not in base_ids and not (isinstance(tid, str) and tid.startswith("R-")):
            problems.append(f"{tid}: new task; only R-n tasks (chosen review fixes) may be added")
    return problems


def load(path):
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except UnicodeDecodeError:
        print(f"Can't read {path}: not UTF-8; re-save it as UTF-8")
        sys.exit(2)
    except (OSError, ValueError) as e:
        print(f"Can't read {path}: {e}")
        sys.exit(2)


def main(argv):
    if len(argv) not in (2, 3):
        print(__doc__.strip().split("\n\n")[1])
        return 2
    data = load(argv[1])
    problems = check_schema(data)
    if len(argv) == 3 and not problems:
        problems = check_baseline(data, load(argv[2]))
    if problems:
        print(f"FAIL: {argv[1]} has {len(problems)} problem(s):")
        for p in problems:
            print(f"  - {p}")
        return 1
    extra = " and changes only status and evidence" if len(argv) == 3 else ""
    print(f"PASS: {argv[1]}: {len(data['tasks'])} tasks, every field present{extra}.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
