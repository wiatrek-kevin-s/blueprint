# Route: Redesign

For a project that exists and works, whose look and feel should change while its behaviour stays the same. The route ends with a design spec and a kit that a builder carries out: same pages, same content, same links and forms, new look. Blueprint restyles nothing itself (Rule 10).

Read `references/existing-projects.md` first; it holds the gate and read-only rules for this route.

## Phases

Run them in order and save the state file (`- **Route:** redesign`, `- **Phase:** R0` to `R2`, then `3D` and `4` to `6`) after every round and gate.

| # | Phase | Read | Ends with |
|---|---|---|---|
| R0 | Intake | this file, `existing-projects` | How to see it, what is wrong, what must stay, size and capabilities in the state file |
| R1 | Inventory | this file | Screenshots at 375 and 1,280 px, the current tokens, the accessibility baseline and a coverage list |
| R2 | Intent | `01-intake-and-intent` (intent statement) | **G1 and G2:** intent and the must-stay list confirmed; inventory and decision map read |
| 3D | Design direction | `03d-design-direction`, `design-principles`, `03-questioning` | **G3:** a direction chosen, "refresh the current look" always among them; one-way doors decided |
| 4 to 6 | Design, review, kit | The phase table in `SKILL.md` | `design-spec.md` and a kit with Keeping it running |

## Gates come before directions

G1 and G2 are one message: the intent statement, the must-stay list, the inventory summary with the accessibility baseline, and the decision map. Show no direction, and write no spec or kit, before the reply.

- **Small:** two rounds before the final message: the G1 and G2 message, then the directions (G3), because the person must see the directions before the spec is written. The G1 and G2 message also carries the open intake and taste questions, one-way doors first, then the ones that most change the directions. After the direction reply, run phases 4 to 6 without stopping, and put the approval into the final message.
- **Medium and large:** G1 and G2, the directions, and any merge round are separate rounds.

## Read-only: redesign specifics

- A static site opens straight from its files; anything else runs only from the temporary copy.
- Asking first covers opening a live address, signing in, and installing a browser. A screen you could not see goes in the coverage list as "not seen: needs <what>". Looking up a font's licence is research.

## R0: Intake

1. How you can see it: a local folder, an attached repository or uploaded files, a live address, or screenshots. Add "can see the screens" to the capability check, with the method from R1.
2. What is wrong with the current look, in the person's words, and who uses it on which devices.
3. What must stay: the brand (logo, name, any colours or fonts they keep), the content, the pages and their addresses, and the flows (links, forms, buttons, sign-in).
4. The appetite; set the size as for any project, from the number of screens and the cost of a wrong look; create the state file.

Separate the goal from the method: "make it look modern" may really be "people can't read it on a phone" or "it doesn't look trustworthy"; name the real goal in the intent.

## R1: Inventory

**Screens.** List every screen and page, and the states you can reach (empty, error, signed in). Capture each at 375 and 1,280 px wide, full page, and save the images with the width in the name, such as `before/index-375.png`. Pick the method at intake:

1. A browser tool in the session.
2. Code execution with a headless browser that is already installed, such as Playwright: a short script opens each page (a static site from its files, otherwise the temporary copy run locally) at both widths and saves the images. Installing a browser uses the network, so ask first.
3. Otherwise, ask the person for screenshots at both widths, click by click, and say which screens.

Look at every image before you judge the look, because the files describe the intent and the screens show the result.

**Current tokens.** Extract the values the project uses today into a table: each colour with its role and file and line, the font families, sizes, weights and line heights, the spacing values, radius, borders and shadows, the breakpoints, and the components (header, navigation, buttons, links, tables, forms, cards, footer). Mark values used once or inconsistently, because a redesign usually replaces many near-duplicates with one token.

**Accessibility baseline.** Check against WCAG 2.2 AA, by tool where code can run: the contrast of every text and background pair (computed with the WCAG formula, ratio and file and line for each), text size, target size, a visible focus ring, labels, image text alternatives, heading order, the page language, and reflow at 375 px (no sideways scrolling). Record each failure; the redesign must fix every one the look causes.

**Behaviour that must stay.** List every page, link, form, button target and script the project has, with file and line. The design changes none of them, and the kit's checks prove it.

The coverage list marks screens captured, sampled or not seen, with the reason; never put its limits in the baseline. Problems beyond the look, such as a broken link or form, a security hole or missing pages, also go in an "outside this redesign" list.

## R2: Intent (G1 and G2)

Agree what the redesign must achieve, as things the person can observe, such as "every text passes 4.5:1", "reads without zooming on a phone" or "looks like a studio, not a template". Write the intent statement as in `references/01-intake-and-intent.md`, with the must-stay list as its constraint.

G1 records the outcome: **redesign**, **switch to Audit** (the problems go beyond the look), or **stop**. The same message is G2: the inventory summary, the current tokens and the baseline stand in for the primer, and the decision map marks the one-way doors from `references/design-principles.md`: the component library, the token setup, the navigation pattern and dark mode.

## 3D: Design direction (G3)

Follow `references/03d-design-direction.md`, with these changes:

- The current project is the main reference. The taste questions ask what to keep and lose from the current look, plus references the person likes.
- **"Refresh the current look" is always one direction:** it keeps the current identity (colours shifted only as far as contrast needs, the same or similar fonts, the same layout) and fixes the baseline failures and inconsistencies. It costs least and changes least, so the person can always choose it. The other directions differ from it on at least three of the qualities 03d lists.
- Structure and content are the current screens with their real content, the same in every direction, so only the look is compared.
- Build each direction's key screen as a mockup file in Blueprint's own folder and capture it at 375 and 1,280 px when a method exists. Check every text pair's contrast by tool before showing it.

Show the directions side by side with your recommendation and its reason. The chosen direction, and the one-way doors decided with it, are G3.

## Joining the shared phases

- **Phase 4:** the design covers the presentation layer only: tokens, styles, fonts, images and icons, and the markup a style or an accessibility fix needs (landmarks, labels, focus). It changes no content, page, address, link, form field or action, script or data. `design-spec.md` follows `templates/design-spec.md`, adds a map from each current value to its new token, and lists every screen from the inventory: none removed, none added. Keeping it running says how the look stays consistent: tokens as the only source for new pages, a contrast check whenever a colour changes, and font licences and hosting.
- **Phase 5:** review as usual, with two more lenses: does any line of the design change behaviour (compare it with the must-stay list), and does every baseline failure have a fix.
- **Phase 6:** the kit, as in `references/existing-projects.md`, plus `design-spec.md` at every size; the readiness check adds `--screens`.
  - The before screenshots go in the kit folder as the builder's reference. When the project is or may become public, screenshots of signed-in or private screens, and the "outside this redesign" list when it names a security hole, go outside the kit folder. The person's hands-on check at each milestone is the before-and-after look, named in plain words.
  - Each task's check includes screenshots at 375 and 1,280 px, the contrast ratios by tool, and proof that every page, link and form on the must-stay list still works. T-1 records browser tests for the must-stay list against the current project, before any style change; every later task runs them.
