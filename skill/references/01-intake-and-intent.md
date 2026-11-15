# Phases 0 and 1: intake and intent

## Phase 0: intake

Goal: know the type, size, appetite and tools in one short exchange.

1. Let the person describe the idea in their own words first, because structure too early cuts off what they meant. In route New's first reply, offer lightning mode in one line ("Or say 'lightning' and I'll assume every answer and write the kit without questions"; `references/lightning.md`).
2. Read everything they bring (notes, files, a state file) before asking.
3. Classify the **type** (software, website, application, business plan, process change, other), the **size** (`SKILL.md`, sizing) and who will use the result.
4. Ask the **appetite**: "How much time is this worth to you before the first usable version?" Offer anchored choices: an afternoon · a weekend · a few weekends · a month or more · "it's work, ask me about the budget". Appetite fixes the time and lets scope vary (`references/heuristics.md`).
5. Run the **capability check** in `SKILL.md` and record the tools and fallbacks.
6. List inputs only the person has (data, content, brand assets, account access, policies) as homework, each with how to get it and when it's needed.
7. Tell the person the type, size and why in one line, create the state file from `templates/state.md`, and suggest a Claude project named "Blueprint: <project name>" as its home if this chat has none.

## Phase 1: intent

Goal: a short intent statement the person confirms (G1). This is the cheapest place to apply Rule 1: people often bundle a method (a tool, a file format, a platform) into the request.

### Questioning (Mom Test)

Ask about what happened, not what might happen (Fitzpatrick, 2013); opinions about the future are polite guesses.

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

Size it as the budgets in `SKILL.md` set; it is the same reframe at every size, only shorter. Whatever the person chooses, record it with any dissent, and plan the chosen route fully.

**Worked example.** Asked for: "a spreadsheet macro that lists last week's missed appointments from our booking export, so I can phone those patients." The goal is fewer missed appointments; the macro, export and calls are a method. Would a reminder the day before prevent misses? Ask whether the booking system has reminders, an export or an API, rather than assuming. What do other practices use, at what cost and lock-in? Is their job reducing misses, or chasing them? The round might say:

> You asked for a weekly list of missed appointments. Another route: text reminders the day before, which prevent misses rather than count them; many booking systems include them (which do you use?). Recommended: reminders, if yours has them. If chasing misses is your part, the list it is, fetched from the system rather than copied by hand if it allows.

A narrow remit limits the scope, not the method.

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
