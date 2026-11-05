# Adaptations by project type

Use with `references/05-design-doc.md` and the seams in `references/02-landscape.md`.

| Type | Add to the design | Typical one-way doors | Design direction? | Final review lenses |
|---|---|---|---|---|
| Software (script, library, service) | Public interface; package layout; dependency policy; packaging | Public interface and data formats; packaging; licence | Only if it has screens | Security, correctness, failure handling, maintainability |
| Website | Page list; content model; hosting and domain; accessibility; who edits content | Static or CMS; host; link structure; data collected by forms | Yes | Accessibility, content, phone layout, privacy, speed |
| Application | Screens and key flows; offline; sign-in; updates; platforms | Framework; data storage and sync; sign-in; distribution | Yes | Security, access rules, each flow end to end, accessibility |
| Business plan | Market, customers, competition, pricing, operations, three-year numbers, risks, funding | Target customer; pricing model; legal structure; funding route | Only for a pitch deck | Numbers and their sources, assumptions, legal and financial exposure, internal consistency |
| Process change | Current and future process; roles; training; transition; measures | Process owner; mandated tools; what is retired | No | Roles, handovers, training, measures, failure points |

## Requirements (coded projects)

The brief carries a requirements list, because each requirement then has an owner task and a test:

- An ID (`REQ-001`), one measurable statement and a priority: Must, Should, Could, or Won't this time.
- Must and Should get Given / When / Then checks, with at least one edge case and one failure case.
- Speed, availability and accessibility get numbers ("under 2 seconds for 10,000 rows"), not adjectives.
- Every task lists the IDs it delivers, and every ID appears in a task, so nothing is quietly dropped.
