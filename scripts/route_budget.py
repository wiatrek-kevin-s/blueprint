#!/usr/bin/env python3
"""route_budget.py: tokens of skill files a medium run of each route reads.

Usage: python3 scripts/route_budget.py [skill-folder] [--files]
  skill-folder  default: skill/ next to this scripts/ folder
  --files       also list each counted file with its tokens

Prints one line per route: the route, its token count and its limit.
Exit 0 when every measured route is within its limit, 1 when any is over or
a file a route needs is missing, 2 on a usage error.

Tokens are characters divided by 4, rounded up, per file, the same estimate
build-zip.sh uses. Each file counts once per route, however often a run
reads it.

What a route counts (build brief REQ-11): SKILL.md plus every file the
route's phase rows name, for a medium coded project with screens. "Name"
means the Read column of each row, plus the template each row produces or
names: the state file at intake, the primer at G2, the design spec in step
3D, and the kit templates for a medium coded kit built in Claude Code. A
step skipped only in some runs (Explore when the idea is clear) is counted,
because the budget is for the run that reads the most. Files a run reads
only on demand (heuristics, writing rules, subagent briefs, working state)
are not counted, because no phase row names them.

Routes and the files they count (paths inside the skill folder):

  new (Blueprint 2's phases 0 to 6; SKILL.md phase table)
    SKILL.md
    references/01-intake-and-intent.md   phases 0 and 1
    references/00-explore.md             phase E
    references/02-landscape.md           phase 2
    references/04-research.md            phase 2
    references/glossary.md               phase 2
    references/non-coder-checklist.md    phase 2, coded
    references/03-questioning.md         phase 3
    references/03d-design-direction.md   phase 3D, screens
    references/design-principles.md      phase 3D, screens
    references/05-design-doc.md          phase 4
    references/type-adaptations.md       phase 4
    references/software-design-detail.md phase 4, coded
    references/06-review.md              phase 5
    references/07-handoff-kit.md         phase 6
    templates/state.md                   phase 0 (state file)
    templates/primer.md                  phase 2 (primer)
    templates/design-spec.md             phase 3D (design spec)
    templates/kit-00-start-here.md       phase 6, medium
    templates/kit-01-project-instructions.md
    templates/kit-02-build-brief.md
    templates/kit-03-progress-log.md
    templates/kit-04-final-review.md
    templates/kit-tasks.json             phase 6, coded kit in Claude Code
    From T-10, also references/keeping-it-running.md (phase 4 of every
    route), once that file exists.

  audit, redesign, operate
    Measured only once the route's own file exists (references/route-audit.md,
    route-redesign.md, route-operate.md); until then the line says so. The
    task that writes each route (T-13, T-19, T-16) replaces its draft list
    below with the files its phase rows name. Drafts, from the build brief's
    design: SKILL.md, the route file, references/keeping-it-running.md, and
    the shared phases (design, review, kit) with their files as in "new"
    from 05-design-doc.md onward.

Limits (REQ-11): new at most NEW_BASELINE + 1,500 tokens, where NEW_BASELINE
is Blueprint 2.0.0's count for new from this script (T-8, recorded in
evals/results/v2-baseline.md); audit, redesign and operate at most 27,000
each.

Python 3 standard library only.
"""
import math
import os
import sys

NEW_BASELINE = 20743  # Blueprint 2.0.0, measured by this script on 2026-11-05 (T-8)
NEW_ALLOWANCE = 1500
ROUTE_LIMIT = 27000

NEW_FILES = [
    "SKILL.md",
    "references/01-intake-and-intent.md",
    "references/00-explore.md",
    "references/02-landscape.md",
    "references/04-research.md",
    "references/glossary.md",
    "references/non-coder-checklist.md",
    "references/03-questioning.md",
    "references/03d-design-direction.md",
    "references/design-principles.md",
    "references/05-design-doc.md",
    "references/type-adaptations.md",
    "references/software-design-detail.md",
    "references/06-review.md",
    "references/07-handoff-kit.md",
    "templates/state.md",
    "templates/primer.md",
    "templates/design-spec.md",
    "templates/kit-00-start-here.md",
    "templates/kit-01-project-instructions.md",
    "templates/kit-02-build-brief.md",
    "templates/kit-03-progress-log.md",
    "templates/kit-04-final-review.md",
    "templates/kit-tasks.json",
]
# Counted only when present, so the same script measures v2 and v3.
NEW_OPTIONAL = ["references/keeping-it-running.md"]

SHARED_TAIL = [
    "references/05-design-doc.md",
    "references/type-adaptations.md",
    "references/software-design-detail.md",
    "references/06-review.md",
    "references/07-handoff-kit.md",
    "templates/state.md",
    "templates/kit-00-start-here.md",
    "templates/kit-01-project-instructions.md",
    "templates/kit-02-build-brief.md",
    "templates/kit-03-progress-log.md",
    "templates/kit-04-final-review.md",
    "templates/kit-tasks.json",
    "references/keeping-it-running.md",
]

# route: (file that must exist before the route is measured, files counted)
ROUTES = {
    "new": (None, NEW_FILES),
    "audit": ("references/route-audit.md",
              ["SKILL.md", "references/route-audit.md", "references/04-research.md",
               "templates/audit-report.md"] + SHARED_TAIL),
    "redesign": ("references/route-redesign.md",
                 ["SKILL.md", "references/route-redesign.md",
                  "references/03d-design-direction.md", "references/design-principles.md",
                  "templates/design-spec.md"] + SHARED_TAIL),
    "operate": ("references/route-operate.md",
                ["SKILL.md", "references/route-operate.md", "references/04-research.md",
                 "references/glossary.md", "templates/primer.md"] + SHARED_TAIL),
}
LIMITS = {"new": NEW_BASELINE + NEW_ALLOWANCE, "audit": ROUTE_LIMIT,
          "redesign": ROUTE_LIMIT, "operate": ROUTE_LIMIT}


def tokens(path):
    with open(path, encoding="utf-8") as f:
        return math.ceil(len(f.read()) / 4)


def main(argv):
    args = [a for a in argv[1:] if not a.startswith("--")]
    flags = {a for a in argv[1:] if a.startswith("--")}
    if len(args) > 1 or flags - {"--files"}:
        print("usage: python3 scripts/route_budget.py [skill-folder] [--files]")
        return 2
    here = os.path.dirname(os.path.abspath(__file__))
    skill = os.path.abspath(args[0] if args else os.path.join(here, "..", "skill"))
    if not os.path.isfile(os.path.join(skill, "SKILL.md")):
        print(f"FAIL: no SKILL.md in {skill}")
        return 2

    print(f"Route budgets for {skill} (tokens = characters / 4, each file once)")
    failed = False
    for route, (needs, files) in ROUTES.items():
        if needs and not os.path.isfile(os.path.join(skill, needs)):
            print(f"{route}: SKIPPED, {needs} does not exist yet (limit {LIMITS[route]:,})")
            continue
        counted = list(files)
        if route == "new":
            counted += [f for f in NEW_OPTIONAL if os.path.isfile(os.path.join(skill, f))]
        missing = [f for f in counted if not os.path.isfile(os.path.join(skill, f))]
        if route != "new":
            missing = [f for f in missing if f != "references/keeping-it-running.md"]
            counted = [f for f in counted if os.path.isfile(os.path.join(skill, f))]
        if missing:
            print(f"{route}: FAIL, files missing: {', '.join(missing)}")
            failed = True
            continue
        sizes = [(f, tokens(os.path.join(skill, f))) for f in counted]
        total = sum(t for _, t in sizes)
        ok = total <= LIMITS[route]
        failed |= not ok
        print(f"{route}: {total:,} tokens in {len(sizes)} files "
              f"(limit {LIMITS[route]:,}){'' if ok else ' FAIL: over the limit'}")
        if "--files" in flags:
            for f, t in sizes:
                print(f"  {t:>6}  {f}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
