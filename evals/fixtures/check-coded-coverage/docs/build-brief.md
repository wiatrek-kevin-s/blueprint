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

## Keeping it running

The owner reviews prices once a month, for 20 minutes, against new receipts.

## Tasks

The tasks are in `tasks.json`.

## Definition of done

Every item has a price, and the owner has approved the plan.
