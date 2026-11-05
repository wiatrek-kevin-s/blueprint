# Design detail for coded projects

Read in phase 4 for anything coded. Use only the parts the project needs; each becomes a section of the design and the brief. The decisions behind these items are in `references/non-coder-checklist.md`.

## Security baseline

Every coded kit carries these ten items. Each gets one status: **applied** (where in the build), **not applicable** (you decide, one line), or **accepted risk** (the person approves; logged as a decision). Weakening any part of an item makes it an accepted risk: name its decision ID and show it to the person in the approval message, because a risk they never saw is not accepted.

1. Access rules enforced by the server or database, deny by default, with row-level security where the platform has it, because rules in the browser can be bypassed.
2. Secrets never in browser code or git, with secret scanning on, because a leaked key acts as you.
3. Hard spending caps and narrowly scoped keys, because alerts don't stop a runaway bill.
4. Separate test and live setups, preview copies included, which never reach live data; the builder never holds live credentials; backups proved by a restore, because agents have wiped live data.
5. Few, popular, pinned dependencies, each checked to exist and be maintained before install, because AI tools invent package names that attackers then register.
6. Managed services for sign-in and payments; no home-made password storage or stored card numbers, because those are the commonest serious failures.
7. Legal triggers flagged for the person: privacy laws by where users live (such as EU, UK and US state laws), children's data, accessibility, app-store rules. This is not legal advice.
8. Rate limits on sign-in, sign-up and AI calls, because bots find open forms within days.
9. If the product uses AI: calls from the server, spend caps, least-privilege tools, confirmation before destructive actions, untrusted input kept apart from instructions.
10. Verification the person can trust without reading code (below), because a builder's own "it's secure" is not evidence.

## Verification without reading code

- **Automated scanners** in the definition of done: secret scanning before anything is saved, dependency audits, static analysis on every change.
- **Click-through tests the person runs,** written as plain steps with the expected result, one per access rule: "Sign in as A, copy the address of A's item, sign in as B, open it: you see 'not allowed'."
- **Browser tests** (Playwright) for web interfaces, so the click-throughs repeat on every change.
- **The final review** in a fresh context (`references/07-handoff-kit.md`).

## Default stacks (as of 2026-11-03)

Re-check names and versions before recommending one, and pin versions at build time, because this table dates; if it is over six months old, research afresh.

| Project | Default | Why |
|---|---|---|
| Static site | Plain HTML and CSS, or Astro; a static host | No server or login, so little to attack |
| Web app with accounts | Next.js with TypeScript, Supabase (database, sign-in, storage), Stripe Checkout for payments | Most documented; managed sign-in; row-level security on every table |
| Web app, Python-leaning | Django with Postgres or SQLite | Sign-in, admin and safe queries built in |
| Script or command-line tool | Python with uv, Typer and pytest | One tool for environments; few dependencies |
| Phone app | A phone-friendly web app first; Expo if native is needed | Avoids store fees and review |

## What the design decides

- **Data:** entities and links, rules that must always hold, delete policy, how migrations are reversed, which fields are personal.
- **Interfaces:** every operation with inputs, outputs and an error model; whether repeats are safe; versioning, a one-way door once anyone depends on it.
- **Testing:** depth by risk (impact × likelihood); every Must requirement has a test; an end-to-end check at each milestone.
- **Release:** version numbers, a changelog, and a rollback plan tried once before it is needed.

## Conventions and version control (policy only)

The brief states what must be true and the builder chooses the tools and commands, because it already knows git. Work is saved and pushed after every task, so nothing is lost if a session stops; any change can be rolled back; secrets are never committed, because history keeps them after deletion; history is never rewritten without the person's approval, because rewriting can destroy work. One formatter and linter run in the definition of done.
