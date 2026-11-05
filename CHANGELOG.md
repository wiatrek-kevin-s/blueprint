# Changelog

## 3.0.0-beta.1 (2026-11-05): router and Keeping it running

First pre-release of Blueprint 3. Blueprint now plans projects at any stage, and every kit says how the result is kept running.

What's new:

- **Routes.** Blueprint picks one of five kinds of planning and names it in its first reply (`Route: new`): New (an idea), Audit, Redesign, Operate (upkeep of projects you already have) and Amend (changing a delivered kit). This release runs New and Amend; Audit, Redesign and Operate are named and come in later pre-releases, and until then Blueprint says so and offers to plan the work as a new project.
- **Keeping it running.** Every kit has a section saying who looks after the result and for how many hours a month, what changes or expires, what agents may do unattended (they propose, you approve), the safety net, and a monthly routine under 15 minutes. The kit check fails a kit without it, and the final review asks whether you could follow the routine next month.
- **Read-only look at existing projects.** Rule 10 now lets the coming routes read a project and run commands that write nothing outside a temporary copy; Blueprint still never builds or edits the project.
- **Blueprint 2 compatibility.** A Blueprint 2 state file resumes where it stopped, without repeating passed steps. Amending a Blueprint 2 kit offers to add the new section.

Known limitations of this release:

- Audit, Redesign and Operate are not available yet.
- Kits made by Blueprint 2 fail this version's kit check until they gain a "Keeping it running" section; Amend offers to add it.
- On a medium project, route New reads about 22,100 tokens of Blueprint's own files, within its limit of 22,243 but with little room to spare.
- Measured on 2026-11-05 with one model (claude-sonnet-5-5): routing results are in `evals/results/v3-beta1.md`; Audit, Redesign and Operate routing is not measured yet.

## 2.0.0 (2026-11-04): first public release

Blueprint turns an idea into an execution kit: a short set of documents a fresh AI agent can build from without guessing. It plans; it never builds.

What it does:

- Explores a vague idea, confirms the goal, and explains each decision in plain words before asking about it.
- Asks you only about choices that are hard to undo, decides the rest with named rules of thumb, and records every decision with its reason.
- For anything with screens, shows you a few look-and-feel directions to choose from.
- Gives coded projects a security and privacy baseline for people who don't code.
- Checks the kit for gaps before handing it over; every kit ends with an independent review of what was built.

Known limitations of this release:

- Kits for medium-sized web apps with user accounts can still leave a few hard-to-undo details to the builder's guess, where a wrong guess affects safety, cost or legal duties. In the last test, the kit for a club members' app left 9, such as whether members can change their own role. The kit tells the builder to stop and ask about such details.
- No kit has yet been built in full and passed its independent final review. In testing, only the sign-in and roles part of one app was built, and its tests passed.
- On a medium project, Blueprint can read slightly more of its own files than its target (about 25,600 tokens, not 25,000).
