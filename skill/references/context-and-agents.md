# Context and agents

Context is a budget: the longer a chat grows, the less reliably early detail is recalled (Anthropic, 2025; Chroma, 2025). These rules spend it where it pays.

## Who does what

Blueprint's main chat keeps the interview, the questions and the decisions, because those need the person and the whole conversation; fresh subagents do the bulk (`SKILL.md`, context discipline). It reads their summaries, not their bulk.

A subagent here is always a named agent given only the files, never a fork, because a forked reviewer also shares the author's blind spots. As of 2026-11, fork mode is on by default in Claude Code; check its current docs at build time.

Split work by the context it needs, never by role (planner, coder, tester), because each relay loses detail. Keep quick edits in the main chat. Several agents cost several times the tokens of one (Anthropic, 2025): one for a lookup, two to four for a comparison.

## The subagent brief

The subagent sees only this message, so it must stand alone.

```
Objective: <one sentence: what to find or check, and why it matters>
Scope: <what is in; what is out>
Inputs: <file paths and links, not pasted content>
Output: <format; at most about 1,500 tokens; bulky results go to a file, and only its path and a summary come back>
Tools and sources: <tools allowed; sources preferred; facts whose date must be checked>
Boundaries: <what not to do, such as editing outside a folder, publishing or signing up>
Start: <a fresh named agent>
Could not verify: <listed separately, never guessed>
```

## When to start a fresh chat

At each pivot named in `SKILL.md`, save the handoff note with the state file. Without subagents, suggest a fresh chat at those pivots and also when:

- the goal changes direction;
- two corrections of the same problem have failed, because one clear prompt in a new chat beats a third correction;
- signs of drift appear (below), or a compaction happened mid-task, because summaries drop instructions given only in chat.

## Coordinating workers (the kit mirrors this)

The kit makes the builder's main session a coordinator in the same way:

- **Brief:** each worker gets one task, or a small group, as a stand-alone message: the task and its checks, the brief sections and decision IDs it needs, the save-work policy, its boundaries, and what to return (what changed, check results, guesses made).
- **Verify:** the coordinator runs the task's checks itself and logs the evidence, because a worker's "done" is a claim.
- **End and replace:** end a worker when its task is done, when it has run long or drifted, or after two failed attempts. Start a fresh one with a handoff note and a different approach; if that fails too, park the task, go on with others, and ask at the next checkpoint.
- **Stay small:** the coordinator reads workers' reports and the progress log, never code in bulk.

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
