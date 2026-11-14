expect: 1 --coded | the 'Checklist coverage:' line is empty
expect: 1 --coded | NOTE: the brief has no 'Project settings' section
expect: 0
Expected: NOT READY with --coded: a small coded kit (no tasks.json) whose "Checklist coverage:" line has nothing after it, and which has no Project settings section (a NOTE, not a fail). READY without flags, since only --coded asks for the security baseline. Run: python3 skill/scripts/check_kit.py evals/fixtures/check-lite-coded-gaps [--coded]
