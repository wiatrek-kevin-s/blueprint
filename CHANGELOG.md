# Changelog

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
