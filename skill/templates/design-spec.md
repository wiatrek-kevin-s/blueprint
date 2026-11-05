# Design spec: <PROJECT NAME>

As of <DATE>. The only source for the look: every visual value in the product comes from this file. Mockups were for choosing; don't copy their code.

## Direction and rationale

<The chosen direction in one line, what was kept and lost from the others, and why.>

## Tokens

| Token | Value | Role |
|---|---|---|
| Colour: <role> | <oklch value> | <where used> |
| Font: <role> | <family, weights> | <where used> |
| Type scale | <sizes in px> | |
| Spacing scale | <steps in px> | |
| Radius, shadows | <values> | |
| Breakpoints | <widths in px> | |

One colour row per role: background, surface, text, muted text, accent, success, warning, danger, focus.

## Component library

<Its name with an "as of" date, or "none: plain components built from the tokens", and why.>

## Screens

| Screen | Purpose | Key content |
|---|---|---|

## Required states

Screens: empty, loading, error, success. Controls: hover, focus, disabled, loading, error. <Any states this project adds.>

## Accessibility checks

WCAG 2.2 AA, checked by tool: text contrast 4.5:1, large text, controls and focus rings 3:1; targets at least 24 px; every action works by keyboard with a visible focus ring; fields have visible labels; errors say how to fix them.

## Do

- <exact choices, such as "primary buttons: accent on background, weight 600">

## Don't

- <what to avoid, such as gradients, glow, emoji as icons, or placeholder text as labels>

## Screenshot check

A screen is done only when screenshots at 375 and 1,280 px wide show tokens only, every required state, and nothing overflowing or overlapping. Record the screenshot paths as evidence.
