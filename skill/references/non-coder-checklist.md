# Non-coder checklist

Decisions a person who doesn't code rarely knows exist. Each becomes a row on the decision map, because an unasked decision becomes the builder's guess.

## How to use it

- Run it against the decision map in phase 2, as far as the size allows (`SKILL.md`, budgets). Each item ends as a decision, "not applicable" in one line, or an accepted risk the person approves.
- The safe default is your recommendation. Ask the person only about one-way doors, with the reason in one plain line.
- The technical controls are the security baseline in `references/software-design-detail.md`; this list holds the decisions.
- Legal items are flags, not legal advice. Name privacy laws by where users live (EU, UK, US state laws and others), never one place alone, because users come from anywhere.

## One-way items for every size

These apply wherever they fit, at every size, coded or not, because each is costly to undo and otherwise gets guessed.

- **Licence.** Who may reuse the work. Private work needs none; published work defaults to MIT unless there's a reason. Past grants can't be revoked.
- **Account ownership.** Every account (domain, hosting, database, payments, code host, AI provider) is in the person's name, with two-step sign-in and saved recovery codes; the kit says who pays. Whoever holds the accounts owns the product.
- **Publishing.** What becomes public, where and when: the repository, the live site, a store listing. Published work can't be recalled, so default to private until the person decides.
- **Lasting formats.** Anything real data or other people will depend on: file layouts, log lines, database tables, workbook sheets and columns, exports, public links. The kit writes each out field by field (name, type, allowed values, example), because changing it once data exists means migrating or breaking things.

## The checklist

| # | Item | Why it matters | Safe default | Door |
|---|---|---|---|---|
| | **People and data** | | | |
| 1 | Who the users are | Sets the need for accounts, privacy notice, moderation | The person or invited people; public later | Two-way until launch |
| 2 | Data collected | Every field is a liability and can trigger laws | The minimum; no ID documents, health, precise location or children's data unless essential | One-way once leaked |
| 3 | Privacy laws | They follow where users live, not the owner | Flagged; a privacy notice from the start; no selling data; consent before sensitive data; data region and outside processors named; no under-13s unless designed for them | One-way for sensitive and children's data |
| 4 | Retention and deletion | Old data leaks; laws and stores require deletion | Delete what's not needed; "delete my account" from version one | Two-way |
| 5 | Where data lives | Hard to move; sets backups and cost | A managed standard database; a single-file database for one-person tools | One-way |
| 6 | Backups | People and agents delete things; free tiers often have none | Daily automatic backups; a restore tested before launch | Two-way, if set up |
| | **Access** | | | |
| 7 | Sign-in | Home-made login is a top failure | A managed sign-in service; two-step sign-in for admins | One-way |
| 8 | Access rules | Users seeing others' data is the commonest flaw | Deny by default; enforced by the server or database, not the browser | One-way once data leaks |
| 9 | Secrets and keys | A leaked key can mean stolen data or a large bill in hours | Server-side only; never in browser code or git; each key narrowly scoped | The damage is one-way |
| 10 | Rate limits | Bots drain credits and spam sign-up | Limits on sign-in, sign-up and AI calls; a challenge on public forms | Two-way |
| | **Money** | | | |
| 11 | Who pays; spending caps | Alerts don't stop spending; limits can rise silently | The person pays; hard caps where offered; low alert thresholds | Two-way |
| 12 | Hosting and its cost | Free tiers may bar commercial use, pause when idle or lack backups | A static host for sites, a mainstream host for apps; the upgrade trigger stated | One-way-ish for apps |
| 13 | Payments | Holding card numbers brings heavy rules (PCI DSS) | A hosted checkout page; no stored card numbers | One-way if cards were stored |
| | **Accounts and publishing** | | | |
| 14 | Account ownership | See above | As above | One-way |
| 15 | Domain | Losing it loses the brand and its email | Registered in the person's name; auto-renew on | One-way (the name) |
| 16 | Licence | See above | As above | One-way |
| 17 | Publishing | See above | As above | One-way once public |
| 18 | App stores | Fees, review, tester rules, required account deletion | A phone-friendly web app first | One-way-ish once listed |
| 19 | Lasting formats | See above | As above | One-way once data exists |
| | **Building and running** | | | |
| 20 | Version control | Without it mistakes can't be undone | A private repository from day one; secret files ignored | Two-way |
| 21 | Test and live setups | Agents have wiped live databases | Separate data and keys; the builder gets test only | Needed before real users |
| 22 | Dependencies | Fake, hijacked or abandoned packages | Few, popular, pinned; each checked to exist first | Two-way |
| 23 | Dependency updates | Flaws appear after launch | Automatic alerts and a regular update check | Two-way |
| 24 | Dependency licences | Copyleft (GPL, AGPL) can force releasing your code | Permissive (MIT, Apache, BSD); copyleft flagged first | One-way once shipped |
| 25 | HTTPS | Needed for sign-in and payments | The host's automatic HTTPS | Two-way |
| 26 | Email sending | Resets and receipts land in spam | An email-sending service with sender checks set up | Two-way |
| 27 | Logs and monitoring | Nobody notices breakage or attack | Host logs, error tracking, uptime check; no secrets or personal data logged | Two-way |
| 28 | Accessibility | Legal exposure; excluded users | WCAG 2.2 AA basics, checked by tool | Two-way, costly to retrofit |
| 29 | Vendor lock-in | Some platforms are hard to leave | Open standards; code in the person's own repository | One-way-ish |
| 30 | AI inside the product | Hijacked prompts, runaway cost, wrong answers | Server-side calls, caps, per-user limits, confirmation before destructive actions | Two-way |
| 31 | Keeping it running | Software decays; accounts and certificates expire | The kit's Keeping it running section: an owner and hours, each change stream handled, agents propose and the person approves | Two-way |

## Which items apply by project type

| Type | Items |
|---|---|
| Every project | 14, 16, 17, 19 where they fit (the one-way items) |
| Script or tool for the person alone | Add 5, 6, 9, 20, 22–24, 31 |
| Static website | Add 1–3, 12, 15, 25, 27, 28 |
| Web or phone app with users | All |
| Business plan, process change | The one-way items only (document licence, accounts, publishing, workbook layout) |
