#!/usr/bin/env python3
"""Private-terms check: make sure no private term reaches the public repository.

Usage:
  python3 scripts/check_private.py [--terms FILE] [--tracked]
                                   [--all-branches] [--range REV_RANGE ...]
                                   [PATH ...]

  PATH            files to check; "-" reads standard input. Any path works,
                  inside or outside the clone. A .zip file is opened and each
                  text file inside it is checked.
  --tracked       check every file git tracks (git ls-files), and their names.
  --all-branches  check the message of every commit on every local branch.
  --range R       check the message of every commit in the git range R, for
                  example BASE..HEAD, or a single commit. May be repeated.
  --terms FILE    the terms file; default .private-terms at the repository root.

Where the terms come from: the PRIVATE_TERMS environment variable (the
GitHub secret, in CI) and the terms file (on the owner's computer), both
if both exist. Format: one term per line; blank lines and lines starting
with "#" are ignored. With no terms at all, the check prints
"private-terms check skipped: no terms available" and exits 0, so pull
requests from forks, which get no secrets, still run the other checks.

Matching: case-insensitive and whole-word. The repository's own GitHub
address (from "git remote get-url origin", or GITHUB_REPOSITORY in CI) and
its owner/name form are removed from each line before matching, so links
to the repository are not hits.

Output: each hit as "HIT: <where>:<line>". The check never prints a term
or the text of a matching line, because the output can land in a public
CI log, and it does not rely on how GitHub masks secrets.

Exit 0 when nothing matches (or there are no terms), 1 on any hit, 2 when
something can't be read or the arguments are wrong.
Python 3 standard library only.
"""
import argparse
import os
import re
import subprocess
import sys
import zipfile

SKIP_MESSAGE = "private-terms check skipped: no terms available"
WORD = r"[A-Za-z0-9_]"


def git(args, cwd):
    """Run git and return its output, or None when git fails."""
    try:
        out = subprocess.run(["git"] + args, cwd=cwd, capture_output=True,
                             text=True, encoding="utf-8", errors="replace")
    except OSError:
        return None
    if out.returncode != 0:
        return None
    return out.stdout


def repo_root():
    here = os.path.dirname(os.path.abspath(__file__))
    top = git(["rev-parse", "--show-toplevel"], here)
    return top.strip() if top else os.path.dirname(here)


def parse_terms(text):
    terms = []
    for line in text.replace("\r\n", "\n").replace("\r", "\n").split("\n"):
        term = line.strip()
        if term and not term.startswith("#"):
            terms.append(term)
    return terms


def load_terms(terms_path):
    terms = parse_terms(os.environ.get("PRIVATE_TERMS", ""))
    if terms_path and os.path.isfile(terms_path):
        with open(terms_path, encoding="utf-8", errors="replace") as f:
            terms += parse_terms(f.read())
    # Longest first, so a longer term wins over a shorter one inside it.
    return sorted(set(terms), key=lambda t: (-len(t), t.lower()))


def term_pattern(terms):
    parts = [f"(?<!{WORD}){re.escape(t)}(?!{WORD})" for t in terms]
    return re.compile("|".join(parts), re.IGNORECASE)


def address_pattern(root):
    """Pattern for the repository's own address, or None when unknown."""
    slug = None
    url = git(["remote", "get-url", "origin"], root)
    if url:
        m = re.search(r"github\.com[:/]+([^/\s]+)/([^/\s]+?)(?:\.git)?/?\s*$", url.strip())
        if m:
            slug = (m.group(1), m.group(2))
    if slug is None and "/" in os.environ.get("GITHUB_REPOSITORY", ""):
        slug = tuple(os.environ["GITHUB_REPOSITORY"].split("/", 1))
    if slug is None:
        return None
    owner, name = (re.escape(s) for s in slug)
    full = rf"(?:https?://|ssh://)?(?:www\.|git@)?github\.com[:/]+{owner}/{name}(?:\.git)?"
    return re.compile(rf"{full}|(?<!{WORD}){owner}/{name}(?!{WORD})", re.IGNORECASE)


class Checker:
    def __init__(self, terms, address):
        self.pattern = term_pattern(terms)
        self.address = address
        self.hits = []
        self.sources = 0

    def check_text(self, where, text):
        self.sources += 1
        for n, line in enumerate(text.split("\n"), 1):
            if self.address is not None:
                line = self.address.sub(" ", line)
            if self.pattern.search(line):
                self.hits.append(f"{where}:{n}")

    def check_name(self, path):
        """A file name can leak a term too."""
        line = path if self.address is None else self.address.sub(" ", path)
        if self.pattern.search(line):
            self.hits.append(f"{path} (file name):0")


def decode(data):
    if b"\0" in data[:8192]:
        return None  # binary
    return data.decode("utf-8", errors="replace")


def check_file(checker, path, label, terms_path):
    if terms_path and os.path.exists(path) and os.path.exists(terms_path) \
            and os.path.samefile(path, terms_path):
        print(f"note: {label} is the terms file itself; not checked")
        return
    with open(path, "rb") as f:
        data = f.read()
    if zipfile.is_zipfile(path):
        with zipfile.ZipFile(path) as z:
            for info in z.infolist():
                if info.is_dir():
                    continue
                checker.check_name(f"{label}!{info.filename}")
                text = decode(z.read(info))
                if text is not None:
                    checker.check_text(f"{label}!{info.filename}", text)
        return
    text = decode(data)
    if text is not None:
        checker.check_text(label, text)


def commit_messages(root, rev_args):
    """Yield (short sha, message) for commits named by git rev-list arguments."""
    out = git(["log", "--format=%h%x00%B%x1e"] + rev_args + ["--"], root)
    if out is None:
        raise RuntimeError("git log failed for the given commits")
    for record in out.split("\x1e"):
        record = record.lstrip("\n")
        if not record:
            continue
        sha, _, msg = record.partition("\0")
        yield sha, msg


def main(argv):
    parser = argparse.ArgumentParser(description="Check text for private terms; never prints a term.")
    parser.add_argument("paths", nargs="*", help="files to check; '-' for standard input")
    parser.add_argument("--terms", help="terms file (default: .private-terms at the repository root)")
    parser.add_argument("--tracked", action="store_true", help="check every tracked file")
    parser.add_argument("--all-branches", action="store_true", help="check every commit message on every local branch")
    parser.add_argument("--range", action="append", default=[], metavar="REV_RANGE",
                        help="check commit messages in this git range (repeatable)")
    args = parser.parse_args(argv)

    root = repo_root()
    terms_path = args.terms if args.terms else os.path.join(root, ".private-terms")
    terms = load_terms(terms_path)
    if not terms:
        print(SKIP_MESSAGE)
        return 0
    if not (args.paths or args.tracked or args.all_branches or args.range):
        parser.error("nothing to check: give files, --tracked, --all-branches or --range")

    checker = Checker(terms, address_pattern(root))
    try:
        for p in args.paths:
            if p == "-":
                checker.check_text("<stdin>", sys.stdin.read())
            else:
                checker.check_name(p)
                check_file(checker, p, p, terms_path)
        if args.tracked:
            listing = git(["ls-files", "-z"], root)
            if listing is None:
                raise RuntimeError("git ls-files failed")
            for rel in filter(None, listing.split("\0")):
                checker.check_name(rel)
                full = os.path.join(root, rel)
                if os.path.isfile(full):
                    check_file(checker, full, rel, terms_path)
        rev_sets = [["--branches"]] if args.all_branches else []
        rev_sets += [[r] for r in args.range]
        for revs in rev_sets:
            for sha, msg in commit_messages(root, revs):
                checker.check_text(f"commit {sha} message", msg)
    except (OSError, RuntimeError, zipfile.BadZipFile) as e:
        # Errors name files and commands only, never terms.
        print(f"private-terms check error: {type(e).__name__}: {getattr(e, 'filename', None) or e}")
        return 2

    if checker.hits:
        for hit in checker.hits:
            print(f"HIT: {hit}")
        print(f"private-terms check FAILED: {len(checker.hits)} hit(s); "
              "terms are not printed. Remove them before pushing.")
        return 1
    print(f"private-terms check passed: {checker.sources} source(s) checked, no hits")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
