expect: 0
expect-tasks: 0 docs/tasks.json
expect-tasks: 1 docs/tasks-changed.json docs/tasks.json
Expected: READY (tasks list the requirement IDs they deliver). check_tasks.py docs/tasks.json passes; check_tasks.py docs/tasks-changed.json docs/tasks.json fails, because the builder may not change 'delivers'. Run: python3 skill/scripts/check_kit.py evals/fixtures/check-tasks-delivers
