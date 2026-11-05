#!/usr/bin/env python3
"""check_version.py: check that a release tag matches the newest CHANGELOG entry.

Usage: python3 scripts/check_version.py TAG [--changelog FILE] [--notes-out FILE]
  TAG              the release tag, "v" then major.minor.patch, optionally
                   "-beta.N" (for example v3.0.0 or v3.0.0-beta.1)
  --changelog FILE default: CHANGELOG.md next to this scripts/ folder
  --notes-out FILE write the newest entry's text (without its heading) to FILE,
                   for the release notes

Exit 0 when the tag is well formed and the newest "## " heading of the
changelog is "## X.Y.Z (YYYY-MM-DD): title" with the same version as the tag.
Exit 1 otherwise, naming both versions.

Uses the Python 3 standard library only.
"""

import argparse
import os
import re
import sys

TAG = re.compile(r"^v(\d+\.\d+\.\d+(?:-beta\.\d+)?)$")
HEADING = re.compile(r"^## (\d+\.\d+\.\d+(?:-beta\.\d+)?) \((\d{4}-\d{2}-\d{2})\): (\S.*)$")


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    parser = argparse.ArgumentParser(description="Check a release tag against the newest CHANGELOG entry.")
    parser.add_argument("tag")
    parser.add_argument("--changelog", default=os.path.join(here, "..", "CHANGELOG.md"))
    parser.add_argument("--notes-out")
    args = parser.parse_args()

    m = TAG.match(args.tag)
    if not m:
        print(f"FAIL: tag '{args.tag}' is not 'v' then major.minor.patch, optionally '-beta.N' (example: v3.0.0-beta.1)")
        return 1
    tag_version = m.group(1)

    try:
        with open(args.changelog, encoding="utf-8") as f:
            lines = f.read().split("\n")
    except OSError as e:
        print(f"FAIL: cannot read the changelog: {e}")
        return 1

    start = next((i for i, line in enumerate(lines) if line.startswith("## ")), None)
    if start is None:
        print(f"FAIL: tag version {tag_version}, but the changelog has no '## ' heading")
        return 1
    heading = lines[start]
    h = HEADING.match(heading)
    if not h:
        print(f"FAIL: tag version {tag_version}, but the newest changelog heading is not "
              f"'## X.Y.Z (YYYY-MM-DD): title': {heading}")
        return 1
    log_version = h.group(1)
    if log_version != tag_version:
        print(f"FAIL: tag version {tag_version} differs from the newest changelog version {log_version}")
        return 1

    end = next((i for i in range(start + 1, len(lines)) if lines[i].startswith("## ")), len(lines))
    notes = "\n".join(lines[start + 1:end]).strip() + "\n"
    if args.notes_out:
        with open(args.notes_out, "w", encoding="utf-8") as f:
            f.write(notes)
    print(f"OK: tag version {tag_version} matches the newest changelog entry ({h.group(2)}: {h.group(3)})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
