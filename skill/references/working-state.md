# Working state, resuming and talking to the person

## The state file

A Blueprint project can span several chats, so keep a state file (`templates/state.md`). It records the project name, size, phase, gates passed, intent statement, decisions by id, open questions, assumptions, research files and artifacts produced.

- Workspace files don't survive into a new chat, so the state file carries short summaries of the research and of every decision, not only pointers.
- Save it after every question round and at every gate, because you can't tell when a chat will end. Give it to the person to save into their Claude project's knowledge, or write it there yourself if you can, and say which in one line: "Save this so the next chat can pick up where we left off."
- Outside a Claude project, suggest creating one named "Blueprint: <project name>", so the state file has a home.

## Resuming

If a state file is in the project or pasted in, read it first and write its `Route:` line. A file without a Route line comes from Blueprint 2: it is route New at its recorded phase, and the next save adds `- **Route:** new`. Then read the current phase's file, restate in two lines where things stand, and continue from the recorded phase. Don't redo a passed gate unless the person asks or something changed, because repeated questions waste their effort.

## Fresh chats

Blueprint follows the discipline it writes into kits: long chats drift. At the pivots named in `SKILL.md`, save the state file and suggest: "Good point to start a fresh chat: save the state file, then say 'continue Blueprint'." Triggers and the handoff note are in `references/context-and-agents.md`.

## Talking to the person

- Open every new idea with one line on what will happen: "I'll first make sure I understand what you're after, then show you what this kind of project involves before asking you to decide anything."
- Explain before asking: the primer or the question itself defines any term the person may not know.
- Calibrate: check what they know about each area (phase 2) instead of guessing, and match the depth to their answers.
- Keep them oriented: at each gate, one line on what was settled, what comes next and roughly how many questions remain.
- If a request names a solution, ask what it is for, because the need may have a simpler answer.

## Without subagents

Research in sequence yourself. For reviews, ask the person to paste the review prompt into a new chat (a truly fresh reader) and return the answer; only if they decline, review it yourself and label it a self-review, because a reader who saw the reasoning misses the gaps.

## Documents

- Deliver the design document and the kit as shareable documents where the interface offers them, else as Markdown files to download. The kit also exists as plain Markdown, because it gets pasted into a new project.
- Draw anything with structure (architecture, flows, timelines) where the interface supports diagrams; otherwise use Mermaid.
