# Phase 3: decide

Goal: settle every one-way door (G3). Question format and plain words: `SKILL.md`, "Who you're working with".

## Rules

1. **Look up first;** never ask what research can answer.
2. **Each decision question names the decision it settles,** because a question that changes nothing spends the person's attention for free. Past-event questions and confirming the intent are exempt (`SKILL.md`).
3. **One-way doors first,** ordered by how much depends on them; two-way doors get defaults.
4. **Budgets:** rounds and total questions by size (`SKILL.md`). Near the limit, decide the rest and say so, because a tired person answers at random.
5. **"Decide the rest for me" from round 1,** once per round. The rest are recorded as delegated with your choice and reason; one-way doors are then listed for the person to veto in one look.
6. **Stopping research:** decide a two-way door at about 70% of the information you'd like (Bezos, 2016), because more rarely changes it. A one-way door also needs the strongest case against your recommendation, stated to the person.
7. **Disagree and commit:** if the person picks against your advice, say why once, record their choice and your dissent, then design around their choice fully, because a half-hearted design fails for both reasons.
8. **Record every answer** in the state file: decided with its reason; "You decide" as delegated with your choice; unanswered as an assumption with your default. Don't re-ask anything recorded.

## Execution preferences

Ask before phase 6, because they shape the kit:

- **Where the work happens:** a Claude project, Claude Code with a repository, or steps the person does on a platform. A one-way door. For anything coded, recommend Claude Code and list it for veto rather than asking, because only it can run the checks.
- **How work is saved:** git (and which host) or a local folder. A two-way door until real work exists, so default to the simplest that fits; with git, AI credit lines in commits stay off unless the person wants them.
- **Check-ins:** default to each milestone and before anything irreversible (publishing, spending, deleting data, sending messages), because the builder works on its own between them and the person front-loaded their answers here. Also ask what the builder never does without asking.

Small projects fold these into their one round.

## Teams

Record who decides each one-way door and approves checkpoints, because the builder needs one person to ask.

## Example round

> **Round 3 of 4 · 3 questions · or "Decide the rest for me"**
>
> **1. Who can see members' phone numbers?** Hard to undo: a number already shared can't be unshared.
> a. Only organisers (Recommended): members asked for privacy, and organisers need them to call
> b. All members: easier carpooling, but every member holds everyone's number
> c. You decide
>
> **2. Who can find the booking page?** Hard to undo: a page search engines have listed stays findable.
> a. Only people you send the link to (Recommended): you can open it up later
> b. Anyone, listed on search engines from launch · c. You decide
>
> **3. When should the builder check in with you?** Easy to change later.
> a. At each milestone and before anything that can't be undone (Recommended): you try each finished part, and nothing goes live without you
> b. Only when it is stuck · c. You decide
>
> I'll plan the build in Claude Code, saved to a private GitHub repository, because only it can run the checks. Say "no" to change it. Or ask me to explain any of these first.

## Gate G3

Every one-way door is decided, delegated, or open with an owner and a "decide by" point. Tell the person drafting starts.
