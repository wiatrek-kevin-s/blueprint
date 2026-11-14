# Answer key: redesign-sample

Only for scoring Redesign evals. Eval runs copy `evals/fixtures/redesign-sample/` alone.

The site has two pages, `index.html` and `about.html`, sharing `styles.css`. The behaviour that must stay: both pages, the header links between them, the class list and table, the contact email link and the button links.

Known contrast failures against WCAG 2.2 level AA (4.5:1 for normal text), ratios computed with the WCAG relative-luminance formula:

| # | Element | Colours | Ratio | File and line |
|---|---|---|---|---|
| 1 | Intro paragraph (`.intro`) | `#aaaaaa` on `#ffffff` | 2.32:1 | `styles.css:26` |
| 2 | Button text (`.button`) | `#ffffff` on `#f5c518` | 1.63:1 | `styles.css:32` to `styles.css:33` |
| 3 | Links (`a`) | `#7fb3ff` on `#ffffff` | 2.14:1 | `styles.css:39` |
| 4 | Footer text | `#b5b5b5` on `#f2f2f2` | 1.83:1 | `styles.css:44` |

Pairs that pass: body text `#333333` on `#ffffff` (12.63:1) and header text and header links `#ffffff` on `#2e5e4e` (7.43:1; `header a` at `styles.css:15` overrides failure 3, so only links outside the header fail). Ratios checked against the fixture on 2026-11-14.

The site is static, so it opens straight from its files and needs no run in a copy; after the eval the fixture's file checksums are unchanged, and the screenshots and mockups are outside it.
