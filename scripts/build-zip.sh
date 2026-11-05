#!/usr/bin/env bash
# build-zip.sh: check the Blueprint skill folder, then zip it as blueprint/.
#
# Usage: bash scripts/build-zip.sh [skill-folder] [output-zip]
#   skill-folder  default: skill/ next to this scripts/ folder
#   output-zip    default: dist/blueprint-v2.zip in the repository
# Exit 0 when every check passes and the zip is built; exit 1 otherwise.
#
# Checks (planning/design.md sections 4.1 and 4.2, build brief section 5):
#   1. SKILL.md exists and starts with a frontmatter block.
#   2. Frontmatter uses only the allowed fields, each at most once.
#   3. name is "blueprint" and follows the naming rules.
#   4. description is 1-1,024 characters, has no angle brackets, and ends
#      with a "Not for:" clause.
#   5. license is MIT; compatibility, if present, is at most 500 characters.
#   6. SKILL.md body is at most 4,500 tokens (characters / 4; hard limit).
#   7. Every file in references/ and templates/ is linked from SKILL.md.
#   8. Every link in every Markdown file resolves inside the skill folder.
#   9. No uppercase word TODO in any file of the skill.
#  10. LICENSE is present, is MIT, and names "The Blueprint authors".
#
# Allowed frontmatter fields: name, description, license, compatibility,
# metadata, allowed-tools. Sources, checked 2026-11-04: the Agent Skills
# specification (https://agentskills.io/specification, frontmatter table) and
# skill-creator's quick_validate.py, ALLOWED_PROPERTIES
# (github.com/anthropics/skills, skills/skill-creator/scripts/quick_validate.py,
# main branch). Both list the same six fields. Re-check them when either
# source changes. The design (4.2) uses only name, description and license;
# the other three are allowed by the specification, so they pass here.
#
# Uses bash, Python 3 standard library and zip only (build brief section 5).

set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
repo_dir="$(cd "$script_dir/.." && pwd)"
skill_dir="${1:-$repo_dir/skill}"
out_zip="${2:-$repo_dir/dist/blueprint-v2.zip}"

if [ ! -d "$skill_dir" ]; then
  echo "FAIL: skill folder not found: $skill_dir"
  exit 1
fi
skill_dir="$(cd "$skill_dir" && pwd)"

echo "Checking $skill_dir"

if ! python3 -I - "$skill_dir" <<'PY'
import math
import os
import re
import sys

skill = sys.argv[1]
failures = []
ALLOWED = ["name", "description", "license", "compatibility", "metadata", "allowed-tools"]
REQUIRED = ["name", "description", "license"]
TOKEN_CAP = 4500
DESC_MAX = 1024
COMPAT_MAX = 500


def fail(check, message):
    failures.append((check, message))


def rel(path):
    return os.path.relpath(path, skill)


def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def unquote(value):
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
        inner = value[1:-1]
        if value[0] == "'":
            return inner.replace("''", "'")
        return inner.replace('\\"', '"').replace("\\\\", "\\")
    return value


def parse_frontmatter(text):
    """Read the simple YAML subset skills use: top-level 'key: value' lines,
    quoted values, '>' and '|' blocks, and indented maps or continuations."""
    lines = text.split("\n")
    if not lines or lines[0].strip() != "---":
        return None, None, "SKILL.md does not start with a '---' frontmatter line"
    end = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            end = i
            break
    if end is None:
        return None, None, "the frontmatter has no closing '---' line"
    fields = []
    current = None
    for line in lines[1:end]:
        if not line.strip() or line.lstrip().startswith("#"):
            if current and current["block"]:
                current["lines"].append("")
            continue
        m = re.match(r"^([A-Za-z0-9_-]+):(?:\s+(.*))?$", line)
        if m and not line[0].isspace():
            current = {"key": m.group(1), "first": (m.group(2) or "").strip(), "lines": []}
            current["block"] = current["first"][:1] in (">", "|")
            fields.append(current)
        elif current is not None:
            current["lines"].append(line.strip())
        else:
            return None, None, "frontmatter line not understood: " + line.strip()
    values = {}
    for f in fields:
        first, more = f["first"], f["lines"]
        if f["block"]:
            joiner = "\n" if first.startswith("|") else " "
            value = joiner.join(more).strip()
        elif more and not first:
            value = {"(map)": more}
        else:
            value = unquote(" ".join([first] + more))
        f["value"] = value
    body = "\n".join(lines[end + 1:])
    return fields, body, None


skill_md = os.path.join(skill, "SKILL.md")
fields, body = [], ""
if not os.path.isfile(skill_md):
    fail("SKILL.md", "SKILL.md is missing")
else:
    fields, body, err = parse_frontmatter(read(skill_md))
    if err:
        fail("frontmatter", err)
        fields, body = [], ""

# 2. Allowed fields, no duplicates, required fields present.
keys = [f["key"] for f in fields]
values = {f["key"]: f["value"] for f in fields}
for k in sorted(set(keys)):
    if k not in ALLOWED:
        fail("frontmatter fields", f"field '{k}' is not allowed (allowed: {', '.join(ALLOWED)})")
    if keys.count(k) > 1:
        fail("frontmatter fields", f"field '{k}' appears {keys.count(k)} times")
if fields:
    for k in REQUIRED:
        if k not in values:
            fail("frontmatter fields", f"required field '{k}' is missing")

# 3. Name.
name = values.get("name")
if isinstance(name, str):
    if name != "blueprint":
        fail("name", f"name is '{name}', expected 'blueprint' (it must match the zipped folder name)")
    if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", name) or len(name) > 64:
        fail("name", "name must be 1-64 lowercase letters, digits and single hyphens, not starting or ending with a hyphen")
elif name is not None:
    fail("name", "name must be a single text value")

# 4. Description.
desc = values.get("description")
if isinstance(desc, str):
    if not desc:
        fail("description", "description is empty")
    if len(desc) > DESC_MAX:
        fail("description", f"description is {len(desc)} characters; the limit is {DESC_MAX}")
    if "<" in desc or ">" in desc:
        fail("description", "description contains an angle bracket (< or >), which skill validators reject")
    pos = desc.find("Not for:")
    if pos == -1:
        fail("description", "description has no 'Not for:' clause naming near-misses")
    elif pos == 0 or desc.count("Not for:") > 1:
        fail("description", "the 'Not for:' clause must appear once, after what the skill does")
    elif re.search(r"[.!?]\s+\S", desc[pos:]):
        fail("description", "the 'Not for:' clause must be the last sentence of the description")
elif desc is not None:
    fail("description", "description must be a single text value")

# 5. License and compatibility fields.
lic = values.get("license")
if lic is not None and lic != "MIT":
    fail("license field", f"license is '{lic}', expected 'MIT'")
compat = values.get("compatibility")
if isinstance(compat, str) and not (1 <= len(compat) <= COMPAT_MAX):
    fail("compatibility field", f"compatibility must be 1-{COMPAT_MAX} characters")

# 6. Token cap on the SKILL.md body.
body_tokens = math.ceil(len(body) / 4)
if body_tokens > TOKEN_CAP:
    fail("token cap", f"SKILL.md body is about {body_tokens} tokens; the hard limit is {TOKEN_CAP}")

# Collect files.
all_files = []
for root, dirs, files in os.walk(skill):
    dirs[:] = sorted(d for d in dirs if d not in ("__pycache__", ".git"))
    for fn in sorted(files):
        if fn == ".DS_Store":
            continue
        all_files.append(os.path.join(root, fn))
md_files = [p for p in all_files if p.endswith(".md")]

FENCE = re.compile(r"^\s*(```|~~~)")
MD_LINK = re.compile(r"\]\(\s*<?([^)>\s]+)>?(?:\s+\"[^\"]*\")?\s*\)")
TICK_PATH = re.compile(r"`((?:references|templates|scripts)/[^`\s]+)`")
PLACEHOLDER = re.compile(r"[<>*{}\[\]|]|\.\.\.|…")


def links_in(text):
    """Yield (line number, target) for Markdown links and backticked skill
    paths outside fenced code blocks."""
    in_fence = False
    for n, line in enumerate(text.split("\n"), 1):
        if FENCE.match(line):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        for m in MD_LINK.finditer(line):
            yield n, m.group(1), "md"
        for m in TICK_PATH.finditer(line):
            yield n, m.group(1), "tick"


def is_checkable(target):
    if re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", target) or target.startswith("#"):
        return False  # web address, mailto, or in-page anchor
    if PLACEHOLDER.search(target):
        return False  # a placeholder such as <path> or references/*.md
    if "/" not in target and "." not in target:
        return False  # a bare word such as (url) is a placeholder, not a file
    return True


def resolve(md_path, target):
    target = target.split("#", 1)[0].split("?", 1)[0]
    if not target:
        return None, True
    candidates = [os.path.normpath(os.path.join(skill, target)),
                  os.path.normpath(os.path.join(os.path.dirname(md_path), target))]
    for c in candidates:
        inside = c == skill or c.startswith(skill + os.sep)
        if inside and os.path.exists(c):
            return c, True
    return None, False


# 7 and 8. Links resolve; every reference and template is linked from SKILL.md.
skill_md_targets = set()
for md in md_files:
    text = read(md)
    for n, target, kind in links_in(text):
        if not is_checkable(target):
            continue
        found, ok = resolve(md, target)
        if not ok:
            fail("links", f"{rel(md)} line {n} links to '{target}', which is not in the skill folder")
        elif found and md == skill_md:
            skill_md_targets.add(os.path.normpath(found))
for p in all_files:
    top = rel(p).split(os.sep)[0]
    if top in ("references", "templates") and os.path.isfile(skill_md):
        if os.path.normpath(p) not in skill_md_targets:
            fail("file index", f"{rel(p)} is not linked directly from SKILL.md")

# 9. No uppercase TODO.
for p in all_files:
    try:
        text = read(p)
    except UnicodeDecodeError:
        continue
    for n, line in enumerate(text.split("\n"), 1):
        if re.search(r"\bTODO\b", line):
            fail("no TODO", f"{rel(p)} line {n} contains the word TODO")

# 10. LICENSE.
lic_path = os.path.join(skill, "LICENSE")
if not os.path.isfile(lic_path):
    fail("LICENSE", "LICENSE file is missing")
else:
    lt = read(lic_path)
    if "MIT License" not in lt and "Permission is hereby granted, free of charge" not in lt:
        fail("LICENSE", "LICENSE does not look like the MIT licence")
    if "The Blueprint authors" not in lt:
        fail("LICENSE", "LICENSE does not name 'The Blueprint authors' as copyright holder")

# Report.
print(f"SKILL.md body: about {body_tokens} tokens (limit {TOKEN_CAP})")
if isinstance(desc, str):
    print(f"Description: {len(desc)} characters (limit {DESC_MAX})")
print("Sizes of Markdown files (tokens = characters / 4):")
for md in md_files:
    print(f"  {math.ceil(len(read(md)) / 4):>6}  {rel(md)}")
if failures:
    print(f"\n{len(failures)} problem(s) found:")
    for check, message in failures:
        print(f"  FAIL [{check}] {message}")
    sys.exit(1)
print("\nAll checks passed.")
PY
then
  echo "Not building the zip: fix the problems above first."
  exit 1
fi

# Build the zip: the folder inside is named blueprint/.
stage="$(mktemp -d)"
trap 'rm -rf "$stage"' EXIT
mkdir -p "$stage/blueprint"
cp -R "$skill_dir/." "$stage/blueprint/"
find "$stage/blueprint" \( -name .DS_Store -o -name __pycache__ \) -prune -exec rm -rf {} +
mkdir -p "$(dirname "$out_zip")"
out_zip="$(cd "$(dirname "$out_zip")" && pwd)/$(basename "$out_zip")"
rm -f "$out_zip"
(cd "$stage" && zip -q -r -X "$out_zip" blueprint)

if ! unzip -l "$out_zip" | grep -q " blueprint/SKILL.md$"; then
  echo "FAIL: the zip does not contain blueprint/SKILL.md"
  exit 1
fi
echo "Built $out_zip ($(unzip -l "$out_zip" | tail -1 | awk '{print $2}') entries)"
