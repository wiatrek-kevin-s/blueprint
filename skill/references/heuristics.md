# Decision heuristics

Chosen for how they change what you do, not for fame. Name one to the person only when the name helps them decide.

## The table

| Phase | Heuristic (who, year) | What you do differently | Caveat |
|---|---|---|---|
| Decide | One-way and two-way doors (Bezos, 2015) | Ask the person only about choices costly to undo; default the rest; note when a door will close | Doors close as people come to rely on a choice |
| Decide | Decide at about 70% (Bezos, 2016) | Stop researching a two-way door when more facts won't change it | Not for one-way doors; a rule of thumb |
| Intent | Jobs to be done (Christensen, 2005) | Ask when the problem shows up and what they do about it today | Users may hire it for different jobs |
| Intent | The Mom Test (Fitzpatrick, 2013) | Ask about real past events, never "would you use it?" | Lighter when they build for themselves |
| Intent | Appetite (Singer, 2019) | Ask what the idea is worth in time; fit scope to it | Someone must cut scope at the limit |
| Explore | Inversion (Munger, 1986) | Ask what would make it useless; design that out first | Pair it with a positive goal |
| Design | Gall's Law (Gall, 1975) | The first milestone is a thin version that works end to end | Shared interfaces still need settling first |
| Design | Subtraction: YAGNI (Beck, 1990s); question, then delete (Musk, 2021) | Trace each requirement to a person; cut the rest, logged as later options | Never delete legal, safety or accessibility needs |
| Research | Chesterton's fence (Chesterton, 1929) | Before removing an existing step, find why it exists | Time-box the search |
| Design | Do things that don't scale (Graham, 2013) | Mark deliberate manual steps, each with a trigger to automate | Manual steps can become permanent chores |
| Decide | Choose boring technology (McKinley, 2015) | Pick stacks the builder knows well; justify each new one | Count the joins between tools, not novelty (Glyph, 2024) |
| Decide | Hyrum's Law (Wright, via Winters) | Anything others rely on (links, formats, columns) is one-way once shared; define it field by field | Matters less with very few users |
| Design | Strict input (Thomson and Schinazi, 2023) | Reject malformed machine input clearly; don't guess | Be forgiving where people type |
| Kit | Technical debt (Cunningham, 1992) | Log each deliberate shortcut with the event that repays it | Not a licence for messy work |
| Kit | Kill criteria; hardest part first (Duke, 2022; Teller) | Write a dated stop-or-pivot condition; riskiest task first | Needs an owner who enforces it |
| Review | Premortem (Klein, 2007) | Before freezing the kit, assume it failed; list causes as user, operator, attacker, maintainer; fix the likeliest | A solo agent invents threats; rank them |
| Review | Fresh-eyes review (Zenko, 2015; Anthropic, 2025) | Review in a fresh context; state the strongest case against the plan (Feynman, 1974) | Reviewers always find something; triage |
| Kit | A way to verify (Anthropic, 2025) | Every task has a visible pass mark | A target gets gamed (Goodhart, 1975): check behaviour, not counts |
| Kit | One task at a time (Anthropic, 2025) | Pass/fail task list, progress log, smoke check first | Tested mainly on web apps |
| Kit | Context is finite (Anthropic, 2025) | Short top file; detail loaded only when needed | Measure what the builder reads |

## Misattributions to avoid

- "55 minutes defining the problem" isn't Einstein (Aley, 1945); "as simple as possible, but not simpler" is a paraphrase (Sessions, 1950).
- The drill-and-hole line is Leo McGivena's, via Levitt (1969); "make it work, make it right, make it fast" is Johnson and Kernighan (1983), not Beck.
- "Premature optimization" is Knuth (1974), not Hoare, and means measure first; the "Feynman technique" is Scott Young's (about 2011).
- Goodhart's popular wording is Hoskin's (1996) and Strathern's (1997); "disagree and commit" predates Amazon.
- Brooks withdrew "plan to throw one away" in 1995.
