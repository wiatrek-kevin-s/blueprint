# Design principles

Defaults every direction starts from, so the person's attention goes to choices that matter. Every visual value is a design token (a named value such as `--primary`, set once), because tokens make style cheap to change; the token setup itself is the one-way door.

## Safe defaults

| Item | Default | Door |
|---|---|---|
| Component library | The platform's established kit (as of 2026-11-04: shadcn/ui for React, Apple's system components, Material 3), never home-made, because accessibility comes built in | One-way |
| Styling | Semantic tokens for colour, type, spacing, radius and motion; no hard-coded values | One-way; makes the rest two-way |
| Navigation | A standard pattern: top bar (site), sidebar (dashboard), 3–5 tabs (phone) | One-way once content exists |
| Dark mode | Decide scope before building; if in, every colour token gets both themes | One-way without tokens |
| Fonts | One or two families with fixed roles, openly licensed (SIL OFL), self-hosted where privacy law applies | Two-way |
| Type | Body at least 16 px; scale ratio 1.2 (dense) or 1.25; 6–8 sizes; 2–3 weights; line height 1.4–1.6; lines 60–75 characters | Two-way |
| Spacing | Steps of 4 px (4, 8, 12, 16, 24, 32, 48, 64); smaller gaps inside a group than between groups | Two-way |
| Colour | One tinted neutral scale, one accent on about 10% of the surface, plus success, warning, danger; in OKLCH so contrast is predictable | Two-way |
| Contrast | WCAG 2.2 AA: text 4.5:1, large text 3:1, controls, icons and focus rings 3:1 | A requirement, not a style |
| Targets | At least 24 px (WCAG 2.2 AA); 44–48 px for main touch controls | Two-way |
| Radius, shadow, motion | One radius token; shadows only on layered items; 150–250 ms motion, off when the reduced-motion setting is on | Two-way |
| States | Controls: hover, focus, disabled, loading, error. Screens: empty, loading, error, success | Put them in acceptance checks, because they get forgotten |

## The generic AI look, and how to avoid it

Without a specific spec, models pick the commonest look they were trained on (Anthropic, 2025; NN/g, 2025). Banning one default brings the next, so the spec gives exact values, not only bans. Prevention lines go into the spec's "don't" list.

| Failure | Prevention line |
|---|---|
| Purple gradients, glow, blur, heavy rounding | Only what the tokens list |
| One default font, one weight | Named fonts only; headings 600–700, body 400 |
| Cards everywhere, nested | Cards only for repeated, independent items; group with space first |
| Uneven or uniform spacing | Scale values only |
| Low contrast; placeholder as label | Contrast checked by tool; visible labels |
| Everything emphasised | One primary action per view |
| Template hero: headline, two buttons, three icon cards | Layout follows the agreed screen structure |
| Emoji and mixed icon sets | One named icon set; no emoji in the interface |
| Only the happy path | Every state above is built |
| Filler text, invented quotes or stats | Real content; gaps marked missing |
| Phone as an afterthought | Mobile first; checked at 375 and 1280 px |
| Pretty but confusing | Walk the main task step by step before sign-off |

## Borrowing rules

- Borrow structure, never skin: layouts, flows and patterns are conventions people already know; logos, illustrations, photos, copy and colour identity belong to their owners.
- Mix several references and re-skin with the project's tokens, because copying one whole reads as a knock-off.
- Fine: common layouts, navigation and forms; open design systems under their licence; measuring a site's spacing to learn.
- Not fine: brand assets or copy; unlicensed paid fonts; a distinctive overall look that could confuse people about who made it (it can be protected as trade dress); reference screenshots used as assets.
- The kit says: "Use references for structure only; never reproduce their logo, imagery, copy or colour identity." Practical guidance, not legal advice.
