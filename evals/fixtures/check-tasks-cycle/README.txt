expect: 1 | depend on each other in a loop
expect-tasks: 1 docs/tasks.json
Expected: NOT READY: T-1 and T-2 depend on each other, and T-3 depends on itself. Also: python3 skill/scripts/check_tasks.py evals/fixtures/check-tasks-cycle/docs/tasks.json fails (exit 1). Run: python3 skill/scripts/check_kit.py evals/fixtures/check-tasks-cycle
