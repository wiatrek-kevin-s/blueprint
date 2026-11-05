# Context and agents

Context is a budget: the longer a chat grows, the less reliably early detail is recalled (Anthropic, 2025; Chroma, 2025). These rules spend it where it pays.

## When to delegate

Use a subagent only when one of these holds, because a fresh agent must regather context and several agents cost several times the tokens of one (Anthropic, 2025):

- **Bulky output you'd mostly discard**: wide research, or reading large files for a few facts.
- **Truly independent parallel work**: separate topics with no shared decisions.
- **Fresh eyes**: reviews and dry runs, which must not see the author's reasoning, or they inherit its blind spots.

Keep in the main chat anything that needs the person, shares decisions or is a quick edit. Split work by the context it needs, never by role (planner, coder, tester), because each relay loses detail. Default to none: one for a lookup, two to four for a comparison.

## The subagent brief

The subagent sees only this message, so it must stand alone.

```
Objective: <one sentence: what to find or check, and why it matters>
Scope: <what is in; what is out>
Inputs: <file paths and links, not pasted content>
Output: <format; at most about 1,500 tokens; bulky results go to a file, and only its path and a summary come back>
Tools and sources: <tools allowed; sources preferred; facts whose date must be checked>
Boundaries: <what not to do, such as editing outside a folder, publishing or signing up>
Could not verify: <listed separately, never guessed>
```

## When to start a fresh chat

Suggest one, within the person's chore budget, when:

- the next phase is unrelated, or the goal changes direction;
- two corrections of the same problem have failed, because one clear prompt in a new chat beats a third correction;
- signs of drift appear (below);
- a compaction happened mid-task, because summaries drop instructions given only in chat.

Before it, save the state file and finish the handoff note.

## The handoff note

Write it as you go, not only at the end, because a chat can stop without warning. Keep it under about 500 tokens so the next session reads it whole.

- **Goal**: what the session set out to do.
- **Status**: what is done, each claim marked verified (checked by a command or test this session) or unverified, because a note records belief, not fact.
- **Decisions and why**: each with its reason.
- **Files**: what changed, and where.
- **Blockers**: open questions and who owns them.
- **Next**: the first step for the next session.

The next session re-checks unverified claims before building on them.

## Signs of drift

Hand off when you notice any of these, because each means detail has been lost and pressing on compounds it: forgetting an earlier instruction; re-proposing an option the person rejected; contradicting a recorded decision; repeating yourself; fixing one file while losing sight of the whole; being unsure what was done.
