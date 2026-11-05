#!/usr/bin/env python3
"""Check a kit's task list (tasks.json).

Usage: python3 check_tasks.py <tasks.json> [<baseline tasks.json>]

Checks the fields every task must have, and, given a baseline (the task
list as the kit delivered it), that the builder changed only each task's
status and evidence and added only R-n tasks (fixes from the final review).
The builder must not rewrite its own acceptance checks, because then
"done" stops meaning what the plan meant.

Exit 0 when every check passes, 1 when any fails, 2 when a file can't be
read. Python 3 standard library only.
"""
import json
import re
import sys

FIELDS = ["id", "title", "session", "depends_on", "done_by",
          "acceptance", "status", "evidence"]
DONE_BY = {"claude", "person", "both"}
STATUS = {"todo", "in_progress", "blocked", "done"}
ID_RE = re.compile(r"^[TR]-[1-9][0-9]*$")
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
            if f not in FIELDS:
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
        if "done_by" in t and t["done_by"] not in DONE_BY:
            problems.append(f"{name}: done_by must be claude, person or both")
        if "status" in t and t["status"] not in STATUS:
            problems.append(f"{name}: status must be todo, in_progress, blocked or done")
        if "depends_on" in t and (not isinstance(t["depends_on"], list)
                                  or not all(isinstance(d, str) for d in t["depends_on"])):
            problems.append(f"{name}: depends_on must be a list of task ids")
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
    by_id = {t.get("id"): t for t in tasks if isinstance(t, dict)}
    for t in tasks:
        if not isinstance(t, dict) or not isinstance(t.get("depends_on"), list):
            continue
        for d in t["depends_on"]:
            if d not in by_id:
                problems.append(f"{t.get('id')}: depends on {d}, which is not in the list")
            elif t.get("status") == "done" and by_id[d].get("status") != "done":
                problems.append(f"{t.get('id')}: is done but {d}, which it depends on, is not")
    return problems


def check_baseline(data, base):
    """Only status and evidence may change; only R-n tasks may be added."""
    problems = []
    if not isinstance(base, dict) or not isinstance(base.get("tasks"), list):
        return ["the baseline file must be an object with a 'tasks' list"]
    for key in set(data) | set(base):
        if key != "tasks" and data.get(key) != base.get(key):
            problems.append(f"top-level field '{key}' changed; only status and evidence may change")
    now = {t.get("id"): t for t in data["tasks"] if isinstance(t, dict)}
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
