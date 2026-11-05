# Blueprint

Blueprint is a Claude skill that turns an idea into an **execution kit**: a researched, decided and reviewed set of documents that a fresh Claude project or Claude Code session can build from without guessing. Blueprint plans; it never builds the product itself.

It is written for people who may not code and can't judge security, good practice or technical choices on their own. It explains each decision in plain words, asks only about choices that are hard to undo, and decides the rest with a stated reason.

## What it does

1. **Explore and confirm the goal.** A few questions about what you want and why, then a short brief you confirm.
2. **Map the decisions.** A primer of the terms you'll meet, and a list of the decisions the project needs, with the hard-to-undo ones marked.
3. **Decide.** A few rounds of multiple-choice questions, each with a recommended option and its reason. You can always say "You decide".
4. **Choose a look** (anything with screens). A few design directions side by side; your pick becomes a design spec.
5. **Design and review.** A design document, checked by a fresh reviewer for gaps and risks.
6. **Hand over the kit.** Start page, instructions for the builder, build brief, task list, progress log and a final-review plan. Small projects get a one-file kit.

Start it by saying "I have an idea for…", asking to plan or spec a project, or typing `/blueprint`.

See `CHANGELOG.md` for this release's known limitations.

## Install

- **Claude apps:** download `blueprint-v2.zip` from this repository's Releases page. In Claude, open **Settings → Capabilities**, make sure code execution and file creation is on, then in the **Skills** section click **Upload skill** and choose the zip.
- **Claude Code:** copy the `skill/` folder to `~/.claude/skills/blueprint/` (all your projects) or to `.claude/skills/blueprint/` inside one repository.

Keep only one skill named `blueprint` switched on, so Claude loads the right copy.

## What's in this repository

- `skill/`: the skill itself.
- `scripts/build-zip.sh`: checks the skill folder and builds the zip (`bash scripts/build-zip.sh`).
- `release/blueprint-v2.zip`: the built skill, ready to upload.

## Licence

MIT. See `LICENSE`, and `skill/NOTICE.md` for the work Blueprint draws on.
