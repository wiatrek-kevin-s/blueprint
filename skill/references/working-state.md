# Working state, resuming and talking to the person

## The state file

A Blueprint project can span several chats, so keep a state file (`templates/state.md`). It records the project name, size, phase, gates passed, intent statement, decisions by id, open questions, assumptions, research files and artifacts produced.

- Workspace files don't survive into a new chat, so the state file carries short summaries of the research and of every decision, not only pointers.
- At each save (`SKILL.md`, context discipline), give it to the person to save into their Claude project's knowledge, or write it there yourself if you can, and say which in one line: "Save this so the next chat can pick up where we left off."

## Resuming

If a state file is in the project or pasted in, read it first and write its `Route:` line. A file without a Route line comes from Blueprint 2: it is route New at its recorded phase, and the next save adds `- **Route:** new`. Then read the current phase's file, restate in two lines where things stand, and continue from the recorded phase. Don't redo a passed gate unless the person asks or something changed, because repeated questions waste their effort.

## Fresh chats

Without subagents, at the pivots named in `SKILL.md`, suggest: "Good point to start a fresh chat: save the state file, then say 'continue Blueprint'." Triggers and the handoff note: `references/context-and-agents.md`.

## Talking to the person

- Open every new idea with one line on what will happen: "I'll first make sure I understand what you're after, then show you what this kind of project involves before asking you to decide anything."
- Keep them oriented: at each gate, one line on what was settled, what comes next and roughly how many questions remain.

## Without subagents

Research and draft in sequence yourself. For a review, ask the person to paste the review prompt into a new chat and return the answer, within the chore budget (`SKILL.md`); if they decline, review it yourself and label it a self-review.

## Documents

- Deliver the kit as shareable documents where the interface offers them, else as Markdown files to download. The kit also exists as plain Markdown, because it gets pasted into a new project. The design document is not delivered separately: it lives on in the brief.
- Draw anything with structure (architecture, flows, timelines) where the interface supports diagrams; otherwise use Mermaid.
