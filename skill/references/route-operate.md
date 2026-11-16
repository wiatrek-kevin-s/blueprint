# Route: Operate

For one project or a set of projects that already exist and need upkeep: updates, fixes, automation, or a choice of tools to run them with. The route ends with an operations kit: setup tasks that put the upkeep in place, each with a check that proves it works, and a runbook the person follows in under 15 minutes a month. Blueprint sets up nothing itself (Rule 10).

Read `references/existing-projects.md` first; it holds the gate and read-only rules for this route.

## Phases

Run them in order and save the state file (`- **Route:** operate`, `- **Phase:** O0` to `O4`) after every round and gate.

| # | Phase | Read | Ends with |
|---|---|---|---|
| O0 | Intake | this file, `existing-projects` | Projects, hours, cost cap, current tools, size and capabilities in the state file |
| O1 | Inventory | this file | Inventory table, one row per project, and a coverage list |
| O2 | Intent | `01-intake-and-intent` (intent statement) | **G1:** what "kept running" means, confirmed; an outcome for each project |
| O3 | Landscape | `04-research`, `glossary`, `keeping-it-running`, `templates/primer.md` | **G2:** dated, sourced options; primer read; decision map with one-way doors marked |
| O4 | Decide | `03-questioning` | **G3:** tool choice and policy decided; one-way doors decided |
| 4 to 6 | Design, review, kit | The phase table in `SKILL.md` | An operations kit with setup tasks and the runbook |

## Gates come before recommendations

G1 shows the intent with each project's outcome; G2 shows the options with the primer and the decision map. Recommend no tool, and write no design or kit, before the reply, because a tool chosen before the goal and the options are seen gets chosen again. In a small run, hours, cost cap and the homework you can see are stated defaults; a one-way door the request names, such as letting an agent merge on its own, goes into the G1 message.

## Read-only: operate specifics

- Never change a live system: no settings, rulesets, secrets, apps, workflows, schedules, issues or pull requests, and never start a workflow or a job. Each of these is a setup task in the kit, done or approved by the person.
- Ask before reading live data, accounts or services too, such as a code host's settings, a hosting dashboard or billing. What you could not see goes in the coverage list as "could not check: needs <what>", and the kit gets a task whose check confirms it.
- When a project is or may become public, kit material that names an unfixed weak point, such as the premortem's accepted risks, goes outside the kit folder (`references/existing-projects.md`, "The kit").

## O0: Intake

1. Which projects, where each one lives (repository, folder, platform) and where it is hosted, and who uses each.
2. What goes stale or breaks today, in the person's words.
3. The hours a month the person will give, and the most they will pay a month for running costs and tools.
4. The tools and agent apps they already use, because a tool they know beats a better one they must learn.
5. Homework: the accounts and access the setup will need from the person (the code host, hosting, any agent app or key).
6. Add "can read each project" to the capability check; set the size from the number of projects and the harm a bad unattended change could do; create the state file.

Separate the goal from the method: "set up Dependabot everywhere" may really be "stop things breaking", which retiring an unused project or a monthly routine may serve better.

## O1: Inventory

Write the inventory as a Markdown table, with a header row and one row per project, even for a single project, because a paragraph hides the cell nobody filled. Its columns: stack and versions, hosting, accounts and who owns each, dependencies and how they are updated, existing CI and automation (workflows, bots, schedules, required checks), backups, monitoring, and things that expire (domains, certificates, keys, tokens, free tiers, schedules that pause when idle) with dates where the files show them. Write "not seen" in a cell you could not check, never a guess. Use subagents for more than about five projects.

Under the table, the coverage list has four headings: read, sampled, skipped (each with the reason), and could not check, with what each would need. Repository settings, secrets, hosting dashboards, billing and version history often belong under "could not check". The limits go only there, never in the risks, the premortem or a task to fix them; at most, a setup task records what exists first. Version history you could not confirm can go under "could not check: version history, not in this copy" instead of the question.

A project that is broken, not merely stale, is outside this route's scope: say so and offer Audit for it.

## O2: Intent (G1)

Agree what "kept running" means, as things the person can observe: how fresh dependencies stay (for example "no security alert open longer than 14 days"), uptime where it matters, the security floor, the monthly cost cap and the person's hours. Write the intent statement as in `references/01-intake-and-intent.md`.

G1 records an outcome for each project: **keep running**, **reduce** (less upkeep, fewer features), **hand over** or **retire**, because upkeep spent on a project nobody needs is wasted.

## O3: Landscape (G2)

Research the current options for each change stream (`references/keeping-it-running.md`), following `references/04-research.md`: managed update bots, agents in CI, scheduled agent runs, the tools the person already uses, and a manual routine. For each option record what it costs, its limits (such as schedules that pause, run quotas, which events it can start from), its safety notes (the access it needs, where its secrets live, whether it can merge), the source and the "as of" date. Never take the options or their facts from a list stored in this skill, because products and their limits change monthly. Without web search, say which facts you could not check, and give the kit a task that confirms them before anything depends on them.

Write the primer from `templates/primer.md`, and seed the decision map with: tool choice for each stream, who may merge, the permissions each agent or bot gets, where secrets live, spending caps, schedules, where notifications go, and setup shared across projects or per project. Letting any agent merge, deploy or push to a live branch without the person's approval is a one-way door, because one bad unattended change can reach users or leak a secret before anyone looks.

## O4: Decide (G3)

Recommend a choice for each decision on the map, starting from the default policy: agents propose (pull requests, drafts, reports) and the person approves; nothing merges to the live branch without its required checks passing and the person's approval. Ask in a question round (`references/03-questioning.md`), and record each choice with its reason.

## Joining the shared phases

- **Phase 4:** the design holds the seven parts of Keeping it running for each project; parts shared by every project are written once. For setup that already exists, the design says what exists and keeps it, or changes it with the reason, so the person can tell a deliberate change from an oversight.
- **Phase 5:** review as usual. The premortem's attacker names at least these five causes, each answered by a decision or task (a defence) or by an accepted risk with its reason:
  1. Instructions planted in issues, pull requests, comments, commit messages or dependency updates that an agent reads.
  2. An agent that merges, deploys or pushes to a live branch alone.
  3. A workflow that hands secrets to outside code, such as a `pull_request_target` workflow or one that runs code from untrusted forks.
  4. An agent that triggers itself in a loop, or runs up cost with no cap.
  5. A token, bot or app with more access than its job needs.

  Write the premortem into the kit, under the brief's security baseline: each cause ranked, with its defence or accepted risk, because the builder and the person check the setup against it later.
- **Phase 6:** the operations kit, as in `references/existing-projects.md`.
  - The person is needed at checkpoints and for their own steps. The inventory table and its coverage list go in the brief's Context as a table and a list, never as a paragraph.
  - Most setup tasks are done by both, because the person adds secrets, installs apps and changes settings. Give click-by-click steps for the person's part, and a check that proves the setup works, such as "start the workflow by hand; a draft pull request appears and nothing merges".
  - A task for setup the inventory could not see, such as a setting or a ruleset, first records what already exists, keeps what meets the decision, and changes only the rest, because the person may have set it up already.
  - Keeping it running holds the runbook: the monthly routine with minutes per step; what to do when each alert arrives; and how to hand a problem to an agent (Audit for something broken, Amend to change this kit). Operate kits get every part of Keeping it running at any size; this overrides the 5-to-10-line rule for small kits.
  - Where agents open pull requests or commit, their commits and pull requests carry no AI credit lines ("Co-Authored-By: Claude", "Generated with Claude Code") unless the person chose them (D-n): put the attribution setting in the brief's Project settings block, the one source the first task writes `.claude/settings.json` from (a small kit adds that block to kit-lite's Brief), or the equivalent setting of the agent tool chosen, as of its docs' date, because a setting kept in the project travels with it into cloud runs, where personal settings may not be read.
  - The routine fits under 15 minutes in every month, or in less when the person said less; never assume more time than that. Put quarterly or twice-yearly work in its own short slot with its minutes and months, and state two totals: a usual month and the busiest month. If the busiest month is 15 minutes or more, cut, spread or automate steps until it fits; never skip a step to make it fit, because a routine that fits only by skipping a step gets skipped.
