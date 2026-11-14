# Lightning mode

Lightning mode runs route New fast: ask nothing, assume every answer, write the kit, check it, and send one message at the end.

## When it applies

- **Trigger:** the person asks for it ("lightning", "fast mode", "skip the questions", "just build it" while planning). Route New's opening message offers it in one line.
- **Route New only.** For Audit, Redesign, Operate or Amend, say in one line that lightning covers new projects only, and run the normal route.
- **Mid-run:** keep what is decided and assume the rest. If the person starts answering or asks to discuss, return to the normal flow; open assumptions become questions.
- Write `- **Mode:** lightning` in the state file under the Route line.

## What is skipped, and what is kept

Skipped: Explore, every question round, the reframe round, the primer, design direction rounds, and waiting at gates. Record G1 to G4 as "assumed in lightning mode" with the date.

Kept: intake, brief research, the decision map with doors marked, the non-coder checklist when coded, the readiness check, one dry run, and every Rule in `SKILL.md` (Rule 10 has one exception, below). The design goes straight into the kit's brief.

## Research, briefly

One pass, by one subagent when you have them (`references/04-research.md`): does something existing already do the job, and what are the current versions, prices and limits of the stack you choose? List what you couldn't verify.

## Assume, and record each one

For every decision the normal flow would ask, choose your recommended option. Record it in the state file and the kit's brief as "assumed in lightning mode", with the reason, so the builder and later amendments know nobody confirmed it.

- **Intent:** write the intent statement from the request as given, and plan the method the person named. If you see a clearly better route (`references/01-intake-and-intent.md`, reframe), note it in one line in the brief and in the final message. Don't ask, and don't switch.
- **One-way doors take the safe default:** private, not public or indexed; every account, domain and repository in the person's own name; payments in test mode only; nothing published or deployed live; no real messages sent, test addresses only; the least personal data the core job needs. Each is cheap to loosen later.
- **Where the work happens:** Claude Code with a private git repository for anything coded; a Claude project otherwise. Check-ins at milestones and before anything irreversible only.
- **Size:** from the request (`SKILL.md`, sizing); the personal-data floor still applies.
- **Screens:** no direction round. State one plain, readable direction in the brief (`references/design-principles.md`).
- **Two-way doors:** the boring default.
- **Never assumed:** passwords, keys and account sign-ups. List them as homework, with where the person types each one, never into the chat.

## The kit

Write it at the size the project needs, from `references/07-handoff-kit.md` and its templates: the small kit or the full kit. Coded kits include the security baseline and the Checklist coverage line, with each item's assumed outcome.

## Readiness check

1. Run `python3 scripts/check_kit.py <kit folder>`, adding `--coded` for software and `--screens` only if you wrote `design-spec.md`. Without code execution, walk its checklist by hand.
2. When you have subagents, give one fresh subagent, never a fork of this chat, only the kit folder and the dry-run prompt in `references/06-review.md`. Without subagents, do a labelled self-review and say so in the final message.
3. Fix what they find by assuming the safe default and recording it, not by asking.

## The final message

One message, in plain words, with no bare IDs (`references/writing-rules.md`):

1. What you made and where the kit files are.
2. What you assumed, one-way choices first, each in one line ("Kept private: nobody else can see it until you say so"), so the person can veto any of them in one reply.
3. A better route, if you saw one, in one line.
4. Homework only they can do.
5. The offer: "Say 'build it' to start, or tell me what to change."

A veto changes that decision in the kit, then re-runs the check. It does not open a round of questions.

## Build hand-off

In Claude Code with a project folder, on "build it", you may put the kit in place. This is Rule 10's one exception, at the person's request. Place the files as `references/07-handoff-kit.md` says (the instructions file becomes `CLAUDE.md`; the rest goes into `docs/`). Then recommend whichever keeps the builder's context clean:

- **This chat is still short:** continue as the builder. Read `CLAUDE.md` and follow it from its first task; from here on the kit governs, not this file.
- **This chat is long:** tell the person to type `/clear` and send the kit's first message, because a builder starting from a clean context makes fewer mistakes.

Outside Claude Code, give the setup steps from the kit's start-here file instead.
