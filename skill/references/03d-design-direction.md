# Phase 3D: design direction

Goal: give the person a real say in look and feel by reaction to concrete directions, and end with `design-spec.md`. Defaults (tokens, borrowing, accessibility, states, emphasis) and the generic-AI-look table: `references/design-principles.md`.

## Taste by reaction

Most people can't name what they like but recognise it (Benedek and Miner, 2002), so in one question round ask for:

- two or three references they like and one they dislike, from any field, and what about each;
- three to five words from: calm, bold, playful, serious, warm, crisp, friendly, premium, technical, handmade, minimal, lively;
- two or three "this, not that" pairs (dense, not airy; friendly, not corporate).

## Screens, content and component library

Name the main task and its user before any look, because a look chosen first gets defended against the task (Sullivan, 1896). Agree the screen list, main task first, and the real content each shows (real names, prices, text; gaps marked missing), because filler text hides layout problems and styling the wrong structure wastes a round. There is no separate greyscale wireframe round: this structure goes into every direction's key screen.

The component library is a one-way door you own (Rule 11): recommend the default in `references/design-principles.md` and list it for veto.

## Default design system

If the capability check found a design system on the person's account, ask whether to build on it, because it may already carry their brand.

## Directions

Make the number of directions, and use the rounds, the size allows (`SKILL.md`), because people choose better by comparing than by describing. They differ on at least three of: type, colour, density, shape (radius and borders), layout emphasis, imagery, because smaller differences look like one option. Each is:

- a **style tile:** fonts, colours, a button, a form field, a card, spacing;
- one **key screen at medium detail:** the agreed structure and real content in that direction's type and colour, without every state or interaction.

Keep structure and content the same across directions, so only style is compared. Check each for contrast with a tool and against the generic-AI-look table before showing it.

## Choosing and merging

Show the directions side by side. Ask what to keep and what to lose from each, and recommend one with its reason. Merge at token level (type from one, colour from another), not by splicing screens, because tokens combine cleanly and screens don't. Then make a deletion pass and a consistency pass on spacing, radius, alignment and wording (Rams), because each extra element competes for attention.

## Writing design-spec.md

Fill `templates/design-spec.md` with the chosen tokens, the component library, the screens, the states and the "don't" list. Mockups are for choosing, never handed over as code, because mockup code skips states, accessibility and the real stack; the builder works from the spec.

## Tools and fallbacks

Check the session's artifact types. Use the Design type when it is listed; otherwise publish an HTML page; otherwise write a local HTML file the person opens. Whichever tool, the tokens go into `design-spec.md`, because the spec is the kit's only copy of the look.
