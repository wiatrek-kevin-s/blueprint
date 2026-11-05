# Phase 3D: design direction

Goal: give the person a real say in look and feel by reaction to concrete directions, and end with `design-spec.md`. Defaults and the generic-AI-look table: `references/design-principles.md`.

## Top 10 design heuristics

1. **Function first** (Sullivan, 1896): name the main task and its user before any look, because a look chosen first gets defended against the task.
2. **Borrow structure, never skin** (Eliot, 1920; Jakob's Law): start from known patterns and an established kit, because people already know them; the borrowing rules are in `references/design-principles.md`.
3. **Different directions, then a recommendation** (Nielsen's parallel design): people choose better by comparing than by describing.
4. **Taste by reaction** (Benedek and Miner, 2002): most people can't name what they like, but they recognise it.
5. **Structure before skin** (NN/g, 2025): agree screens and content first, because styling the wrong structure wastes a round.
6. **Systems, not pixels** (Wathan and Schoger, 2018): every value comes from a small token set, because tokens make later style changes cheap.
7. **Group with space, rank with weight and colour** (Gestalt proximity): the eye reads closeness as belonging; one primary action per view.
8. **Accessibility is a requirement** (WCAG 2.2 AA): it is a legal and practical floor, not a taste.
9. **Self-evident, with feedback** (Krug, 2000; Norman, 1988): every action answers, and every screen has empty, loading, error and success states, because a silent screen looks broken.
10. **Subtract, then sweat the details** (Rams): a deletion pass, then a consistency pass on spacing, radius, alignment and wording, because each extra element competes for attention.

## Taste by reaction

In one question round, ask for:

- two or three references they like and one they dislike, from any field, and what about each;
- three to five words from: calm, bold, playful, serious, warm, crisp, friendly, premium, technical, handmade, minimal, lively;
- two or three "this, not that" pairs (dense, not airy; friendly, not corporate).

## Screens, content and component library

Agree the screen list, main task first, and the real content each shows (real names, prices, text; gaps marked missing), because filler text hides layout problems. There is no separate greyscale wireframe round: this structure goes into every direction's key screen, so the person spends one round fewer.

The component library is a one-way door: ask, recommending the default in `references/design-principles.md`.

## Default design system

If the capability check found a design system on the person's account, ask whether to build on it, because it may already carry their brand.

## Directions

Make the number of directions the size allows (`SKILL.md`). They differ on at least three of: type, colour, density, shape (radius and borders), layout emphasis, imagery, because smaller differences look like one option. Each is:

- a **style tile:** fonts, colours, a button, a form field, a card, spacing;
- one **key screen at medium detail:** the agreed structure and real content in that direction's type and colour, without every state or interaction.

Keep structure and content the same across directions, so only style is compared. Check each for contrast with a tool and against the generic-AI-look table before showing it.

## Choosing and merging

Show the directions side by side. Ask what to keep and what to lose from each, and recommend one with its reason. Merge at token level (type from one, colour from another), not by splicing screens, because tokens combine cleanly and screens don't. Stay within the rounds the size allows.

## Writing design-spec.md

Fill `templates/design-spec.md` with the chosen tokens, the component library, the screens, the states and the "don't" list. Mockups are for choosing, never handed over as code, because mockup code skips states, accessibility and the real stack; the builder works from the spec.

## Tools and fallbacks

Check the session's artifact types. Use the Design type when it is listed; otherwise publish an HTML page; otherwise write a local HTML file the person opens. Whichever tool, the tokens go into `design-spec.md`, because the spec is the kit's only copy of the look.
