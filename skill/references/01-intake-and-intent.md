# Phases 0 and 1: intake and intent

## Phase 0: intake

Goal: know the type, size, appetite and tools in one short exchange.

1. Let the person describe the idea in their own words first, because structure too early cuts off what they meant. In route New's first reply, offer lightning mode in one line ("Or say 'lightning' and I'll assume every answer and write the kit without questions"; `references/lightning.md`).
2. Read everything they bring (notes, files, a state file) before asking.
3. Classify the **type** (software, website, application, business plan, process change, other), the **size** (`SKILL.md`, sizing) and who will use the result.
4. Ask the **appetite**: "How much time is this worth to you before the first usable version?" Offer anchored choices: an afternoon · a weekend · a few weekends · a month or more · "it's work, ask me about the budget". Appetite fixes the time and lets scope vary (`references/heuristics.md`).
5. Run the **capability check** in `SKILL.md` and record the tools and fallbacks.
6. List inputs only the person has (data, content, brand assets, account access, policies) as homework, each with how to get it and when it's needed.
7. Tell the person the type, size and why in one line, create the state file from `templates/state.md`, and suggest a Claude project as its home if this chat has none.

## Phase 1: intent

Goal: a short intent statement the person confirms (G1). Building the requested thing instead of the needed one is the costliest mistake, and this is the cheapest place to fix it. People often bundle a method into the request (a tool, a file format, a platform). Your job here is to find what they need, show them a better route when one exists, concisely, and then respect their choice.

### Questioning (Mom Test)

Ask about what happened, not what might happen (Fitzpatrick, 2013), because opinions about the future are polite guesses.

Good: "Last time a booking was missed, what happened, and what did it cost you?"
Bad: "Would customers like booking online?" It gets a yes that predicts nothing.

### Techniques

- **Goal or method:** split the request into the goal and the method bundled into it. Record the method as a preference and plan from the goal.
- **Ladder up:** ask "what would that let you do?" two or three times until you reach a purpose that isn't a solution.
- **Why it happens:** ask why the problem exists at all. Preventing it upstream usually beats detecting it downstream.
- **Trace the inputs:** where does each input come from, who makes it, how often, in what form? Data copied or downloaded by hand can often be fetched automatically, or the work can live where the data already is.
- **What they can change:** ask what they are able, allowed or tasked to change. If detection is all that's in their hands, or exactly what they were asked to build, plan that, and plan it well.
- **Picture success:** "A year from now this worked. What's different, and for whom?" Push for something observable.
- **Everyone involved:** who uses, pays, approves, maintains, and who is affected but not asked.
- **Constraints, non-goals, the future:** "What will you want to add or connect in a year?"

### Reframe (widening step)

Unless phase E ran, research briefly (`references/04-research.md`): existing products and open-source tools, the platforms the person already uses, and each option's cost, lock-in and fit with their tools. Then show, in a few lines, what they asked for beside the better route or routes you found, each with its main trade-off, and recommend one. Include "use something that exists" whenever it fits, because the best plan is sometimes not to build. If the request is already the best route, say so in one line and why.

Size it as `SKILL.md` sets: small projects carry it in their one round, beside one better route; medium in round 2, beside up to two; large in a round of its own. It is the same reframe at every size, only shorter. Whatever the person chooses, record it with any dissent, and plan the chosen route fully.

**Worked example.** Asked for: "an Esri Python toolbox that reads our roadbed-width Excel sheet and outputs a point file of the problem spots." The goal is roadbed data with fewer errors; the toolbox, the sheet and the point file are a method. Why do the errors happen, and could they be stopped where the data is entered? Where does the sheet come from? If it is exported from a system with an API, the check could run by itself on every export. Must it live in Esri? An open-source library runs anywhere for free. And what are they able to change? The round might say:

> You asked for a toolbox that finds width errors. Two other routes: (a) check widths where the data is entered, so errors stop at the source; (b) fetch the data from its API and run the check automatically each night, in open-source Python that works with or without Esri. Recommended: (b), because it removes the manual step and the lock-in. If finding errors is the part that's yours to change, the toolbox it is, built well.

### Intent statement

> **For** [who], **who** [situation], **[name]** will [what changes]. **We will know it works when** [observable result]. **It must** [hard constraints]. **It will not** [non-goals].

Add one line: **Asked for:** [the request as first framed] · **Chosen route:** [the route] · **Why:** [reason], so the builder and later amendments see the reframe.

Offer your reading as the first option, so the person confirms rather than composes.

### Gate G1

The person confirms the statement and the outcome, both saved in the state file:

- **Build:** the route the person chose, as asked or reframed; go to phase 2.
- **Use something existing:** recommend what, why, cost and setup; heavy setup can be planned as a project.
- **Stop:** say so plainly with the reasons.

If they can't confirm, spend one more round on purpose, or record the doubt as an open question.
