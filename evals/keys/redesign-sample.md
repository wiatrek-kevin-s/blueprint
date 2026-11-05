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

Pairs that pass: body text `#333333` on `#ffffff` (12.63:1) and header text `#ffffff` on `#2e5e4e` (7.43:1).
