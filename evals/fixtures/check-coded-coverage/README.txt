expect: 1 --coded | no 'Checklist coverage:' line
expect: 1 --coded | NOTE: the brief has no 'Project settings' section
expect: 0 | re-run with --coded
Expected: NOT READY with --coded: the Security baseline lacks its "Checklist coverage:" line (a fail for a medium or large coded kit), and the missing Project settings section prints a NOTE, not a fail. READY without --coded. Run: python3 skill/scripts/check_kit.py evals/fixtures/check-coded-coverage [--coded]
