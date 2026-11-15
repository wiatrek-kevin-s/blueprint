# Build brief: Bakery Pricing Plan

## Intent

For a bakery owner who guesses prices, this plan sets each price from ingredient cost and time, so that every item earns its keep.

## Decisions

| ID | Decision | Choice | Why |
|---|---|---|---|
| D-1 | Margin | Cost times three | The owner's accountant recommends it |

## Rules and examples

A loaf whose ingredients cost 1 pound sells for 3 pounds.

## Formats that last

The plan is a plain Markdown table, one row per item.

## Security baseline

Sign-in uses the hosting platform's built-in accounts (D-2); secrets live in the host's settings page, never in files; every other baseline item is applied as the design says.

Checklist coverage: whose data: D-2; sign-in: D-2; payments: N/A: nothing is sold online; publishing: D-3; backups: F-1; personal data: N/A: no customer data is kept.

## Project settings

The `.claude/settings.json` the first task writes, as of 2026-11-14:

```json
{
  "permissions": {
    "deny": ["Read(./.env)", "Read(./.env.*)", "Read(./secrets/**)"],
    "ask": ["Bash(git push --force *)"]
  },
  "env": {"CLAUDE_CODE_FORK_SUBAGENT": "0"},
  "attribution": {"commit": "", "pr": "", "sessionUrl": false}
}
```

## Keeping it running

The owner reviews prices once a month, for 20 minutes, against new receipts.

## Tasks

The tasks are in `tasks.json`.

## Definition of done

Every item has a price, and the owner has approved the plan.
