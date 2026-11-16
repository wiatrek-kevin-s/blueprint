# Jev (TypeSafe AI) — Product Facts for Integration (as of 16 Nov 2026)

> **Method and reliability note (read first).** Every WebFetch in this session failed because the hosts are outside the session's allowed network: docs.typesafe.ai, vercel.com, openrouter.ai and thenewstack.io all failed, so I stopped trying to fetch pages. **I could not open any page in full.** Everything below comes from web-search results: titles, URLs and the search tool's summaries of their snippets. Treat each line as "this source reportedly says X". Before relying on API details, confirm them against docs.typesafe.ai, which needs network allow-listing. I tag claims as **[VENDOR]** (TypeSafe or its official channels), **[GATEWAY]** (Vercel, Netlify, OpenRouter, Cloudflare and similar), **[3P]** (third-party blog or aggregator) or **[INDEP]** (independent testing).
>
> **Lookalike-domain warning:** many unofficial sites use Jev branding, for example typesafe-jev.com, jevapi.org, jevapi.dev, jev-ai.org, jev-ai.live, jevai.tools, jevainews.com, mrjev.com, jev101.org, madewithjev.com and shipwithjev.com. None of them is shown to be official. The official domains appear to be typesafe.ai, docs.typesafe.ai, help.typesafe.ai, console.typesafe.ai and api.typesafe.ai, plus the X account @typesafeai.

## 1. What does Jev take as input and return? (API shape, answer types, batch evaluation)

### Takeaway
Jev is a non-generative "System One" model. You send a `state` (text or JSON) and a set of typed `questions`. It returns one answer per question, each with probabilities over the allowed outputs, and it never generates prose. Three question types are reported: `choice`, `score` and `noul` (yes/no). All questions are evaluated against the same state in one parallel pass.

### Cited Findings
- [VENDOR] The official quick-start shows requests going to `https://api.typesafe.ai/v1/systemone`, with a `state` and typed `questions`, using model `jev-latest` — [TypeSafe docs: Quick start](https://docs.typesafe.ai/introduction/quickstart) (search summary only; page not fetched)
- [3P] The three question types are lowercase: `choice` (pick from labeled options or criteria), `score` (rating on a scale you define) and `noul` (yes/no). One guide warns that uppercase type names get an HTTP 400 — [Ramon Chancay blog](https://www.ramonchancay.me/blog/what-is-jev-typesafe-ai); the same three types appear in [typesafe-jev.com API reference (unofficial domain)](https://typesafe-jev.com/en/guides/api/)
- [3P] Output is "a yes/no probability, a choice from a list you define, or a score on a scale you define", one answer per question, and then the call stops — [Flavio Copes: How to build typed decisions with Jev](https://flaviocopes.com/jev/)
- [3P] Node SDK usage: `client.systemOne()` takes a state and questions built with helpers `noul()`, `choice()` and `score()`. The Python client exposes `system_one()` — [Flavio Copes: Node.js](https://flaviocopes.com/jev-nodejs/); [Flavio Copes: Python](https://flaviocopes.com/jev-python/)
- [VENDOR via 3P] Each question is scored independently against the same state, and the output is a probability distribution over the options you defined — [Flavio Copes](https://flaviocopes.com/jev/)
- [3P] Caveat: although questions are evaluated separately, the resulting probabilities are not statistically independent — [Flavio Copes / related analysis](https://flaviocopes.com/jev/)
- [3P] Interpretation tip: a `noul` probability near 0.5 means "can't tell", not "medium" — [Flavio Copes: Jev with Claude Code, Codex and Cursor](https://flaviocopes.com/jev-coding-agents/)
- [3P] It uses a "parallel sampler that computes all outputs in a single pass" and answers typed questions about text or JSON — [AI Wiki "Jev (AI model)"](https://aiwiki.ai/wiki/jev/raw); [Sanity glossary](https://www.sanity.io/glossary/jev-typesafe-ai-model)
- [3P] It is "designed to not generate text"; it answers typed questions with "a calibrated probability for every possible answer" — [DataCamp](https://www.datacamp.com/blog/system-one-models-jev)
- [GATEWAY] Alternative hosts use different request wrappers: AIMLAPI uses `/v1/decisions` ([AIMLAPI docs](https://docs.aimlapi.com/api-references/decision-models/typesafe/jev)) and Cloudflare uses its `ai/run` endpoint under `typesafe/jev` ([Cloudflare AI docs](https://developers.cloudflare.com/ai/models/typesafe/jev/))
- [VENDOR via press] Doom demo: Jev chose actions from structured game-state data, not screen images — [The Register, 16 Sep 2026](https://www.theregister.com/ai-and-ml/2026/09/16/typesafe-ai-debuts-model-for-machines-that-plays-doom/5296711); the "not on images (yet…)" wording is reported by [jev-ai.org (unofficial)](https://jev-ai.org/blog/why-can-jev-play-doom/)

### Inferences
- Answer types are limited to categorical (`choice`), ordinal or numeric-scale (`score`) and boolean (`noul`). I found no evidence of free-form numbers, strings, arrays or nested objects as answer types. "Numbers" appear to mean a bounded scale you define, not open regression.
- Many questions per request against one shared state is the natural way to batch. I found no separate batch endpoint for many states.

### Gaps
- **Exact response JSON schema:** field names for probabilities, top answer and per-option distributions. I couldn't confirm it because docs.typesafe.ai could not be reached. The only "probability 0–1" typing I found is in a third-party TypeScript comment.
- The maximum number of questions per request, the maximum number of options per `choice`, and the allowed `score` scale ranges.
- Whether a `state` may contain images or other modalities. Current evidence says text or JSON only.

## 2. SDKs, gateways and Vercel AI SDK compatibility

### Takeaway
TypeSafe ships official SDKs for TypeScript/JavaScript (`@typesafe-ai/sdk`) and Python (`typesafe-sdk`). Jev is listed on Netlify AI Gateway (with first-party changelog entries, including Jev 1.14.0), Vercel AI Gateway, OpenRouter, Cloudflare AI Gateway, AIMLAPI, CometAPI and ZenMux, among others. I could not confirm whether it works through the Vercel AI SDK's normal `generateText`/`generateObject` interface.

### Cited Findings
- [3P] npm package `@typesafe-ai/sdk`, reportedly version 0.6.0, requiring Node 20+ — summarized in search results alongside [Netlify changelog](https://www.netlify.com/changelog/typesafe-jev-ai-gateway/) and [jevai.tools (unofficial)](https://jevai.tools/learn/typesafe-ai) (version and Node requirement are third-party and unverified)
- [3P] Python package `typesafe-sdk` (Python 3.10+); a PyPI package named `typesafe-ai` is reportedly a redirect shim — same search result set; see also [Flavio Copes: Python](https://flaviocopes.com/jev-python/)
- [GATEWAY] Netlify: "TypeSafe Jev now available in AI Gateway", with zero configuration. Credentials are handled automatically and usage is billed to Netlify credits. A later entry says "TypeSafe Jev 1.14.0 Now Available in AI Gateway" — [Netlify changelog (Jev)](https://www.netlify.com/changelog/typesafe-jev-ai-gateway/); [Netlify changelog (1.14.0)](https://www.netlify.com/changelog/typesafe-jev-1-14-0-ai-gateway/)
- [GATEWAY] Netlify docs: in Functions and Edge Functions, the TypeSafe SDK automatically reads `TYPESAFE_API_KEY` and `TYPESAFE_BASE_URL`. Listed model IDs are `jev-1.13.0`, `jev-1.14.0`, `jev-latest` and `jev-preview` — [Netlify AI Gateway overview](https://docs.netlify.com/build/ai-gateway/overview/)
- [GATEWAY] Vercel AI Gateway lists `typesafe-ai/jev` (32K context) — [vercel.com/ai-gateway/models/jev](https://vercel.com/ai-gateway/models/jev.md) (could not fetch; search summary only)
- [GATEWAY] OpenRouter lists "Jev 1.13" at `typesafe/jev-1.13` — [OpenRouter](https://openrouter.ai/typesafe/jev-1.13)
- [GATEWAY] Cloudflare — [Cloudflare AI Gateway models: typesafe/jev](https://developers.cloudflare.com/ai-gateway/models/typesafe/jev/); AIMLAPI — [AIMLAPI docs](https://docs.aimlapi.com/api-references/decision-models/typesafe/jev); ZenMux — [zenmux.ai/typesafe/jev-1.13](https://zenmux.ai/typesafe/jev-1.13); CometAPI — [cometapi.com](https://www.cometapi.com/en/models/typesafe-ai/jev)
- [3P] Model versions: stable `jev-1.13.0`, alias `jev-latest` — [AI Wiki](https://aiwiki.ai/wiki/jev/raw). The SDKs default to `jev-latest`, which reportedly pointed to 1.13.0 before 1.14.0 shipped — search summary of the [Netlify changelog](https://www.netlify.com/changelog/typesafe-jev-1-14-0-ai-gateway/)
- [3P] Community tooling: [awesome-jev list](https://github.com/cobanov/awesome-jev), [jev-gateway (use Jev with coding agents)](https://github.com/vinilana/jev-gateway), and Flavio Copes' guide to using Jev from [Claude Code, Codex and Cursor](https://flaviocopes.com/jev-coding-agents/)

### Inferences
- Jev's request shape (state plus typed questions) is not a chat-completions shape. Gateways therefore either proxy TypeSafe's SDK or base URL (Netlify's approach) or define their own wrapper (AIMLAPI, Cloudflare). This makes plain Vercel AI SDK `generateText` usage unlikely without a custom provider. That is unconfirmed.

### Gaps
- Vercel AI SDK provider support: not confirmed either way, and vercel.com could not be fetched.
- I did not find "LLM Gateway" (llmgateway.io) in results.
- Official GitHub org and SDK repos were not located. npm and PyPI pages were not fetched.

## 3. Pricing, latency, context, rate limits, access status, credits, SLA, retention, region

### Takeaway
**[VENDOR]** Pricing is $0.042 per 1M input tokens, and output is free. Some sources call this early-access pricing. **[VENDOR]** End-to-end latency is 70–500 ms. The context window is disputed: 32K per Vercel and others versus 262,144 per an OpenRouter listing. Signups opened 20 Sep, were paused 22 Sep and reopened 27 Sep 2026 without the $5 free credit. I found no report of a later change through mid-November. Data retention is unspecified ("as long as necessary"), zero data retention (ZDR) is enterprise-only, hosting is US-only, and I found no published SLA.

### Cited Findings
**Pricing**
- [VENDOR] TypeSafe help center: "How much does Jev cost?" gives $0.042 per million input tokens, with output tokens free — [help.typesafe.ai](https://help.typesafe.ai/articles/5187202169-how-much-does-jev-cost)
- [GATEWAY] Vercel AI Gateway reportedly lists $0.04 per 1M input — search summary referencing [vercel.com](https://vercel.com/ai-gateway/models/jev.md) (not fetched)
- [3P] Described as early-access pricing, "subject to change" — [developersdigest.tech](https://www.developersdigest.tech/blog/typesafe-jev-system-one-models-release-guide-2026); [swytchcode](https://www.swytchcode.com/content/jev-pricing-explained-what-1-million-agent-decisions-actually-cost)
- [3P] Doom demo cost was estimated at about ten decisions per second and roughly $7 per hour — [madewithjev.com (unofficial)](https://madewithjev.com/builds/jev-plays-doom)

**Latency**
- [VENDOR] 70–500 ms end-to-end — search summary of [Firecrawl](https://www.firecrawl.dev/blog/what-is-jev) and [DataCamp](https://www.datacamp.com/blog/system-one-models-jev); a "70 ms decision model" tagline is used by [madewithjev.com](https://madewithjev.com/what-is-jev)
- [GATEWAY] OpenRouter reports P50 of about 0.08 s for its best provider — [OpenRouter](https://openrouter.ai/typesafe/jev-1.13) (search summary)
- [VENDOR via press] Doom demo: Jev answered in 0.114 s versus 8.566 s for OpenAI's "GPT-5.6 Terra" — [The Register](https://www.theregister.com/ai-and-ml/2026/09/16/typesafe-ai-debuts-model-for-machines-that-plays-doom/5296711)
- [VENDOR] A "193.6× faster" claim exists; it is vendor-reported and not independently benchmarked — [llmrumors.com](https://www.llmrumors.com/news/typesafe-ai-jev-system-one-model-use-cases)

**Context window (conflict)**
- 32,000 tokens — [Vercel AI Gateway listing](https://vercel.com/ai-gateway/models/jev.md) and other aggregators such as [letsdatascience](https://letsdatascience.com/news/typesafe-ai-launches-jev-decision-model-889a38c0); **contradicted by** OpenRouter's reported 262,144-token listing for Jev 1.13 — [OpenRouter](https://openrouter.ai/typesafe/jev-1.13). The conflict is unresolved, and 1.14 may differ.

**Rate limits (conflicting, secondary sources only)**
- Reported figures vary: 100K tokens/s with 80 req/s; or, per a changelog dated 30 Sep 2026, 40 req/s with 100K tokens/s; and older pages cite 250K tokens/s with 1,200 req/min. Limits are per-organization and dynamic, and are visible in the console — [mrjev.com changelog (unofficial)](https://mrjev.com/changelog/); [hokai.io](https://hokai.io/hub/models/jev); [beamseree/hana issue #102](https://github.com/beamseree/hana/issues/102)

**Access and signup status (timeline)**
- 15 Sep 2026: launched in early access — [AI Wiki](https://aiwiki.ai/wiki/jev/raw); [The Register](https://www.theregister.com/ai-and-ml/2026/09/16/typesafe-ai-debuts-model-for-machines-that-plays-doom/5296711)
- 20 Sep 2026: self-serve signups opened with $5 credit — [aiextracash.com](https://aiextracash.com/tools/jev/jev-free-credit/) (secondary)
- 22 Sep 2026 (about 06:19 UTC): [VENDOR] "We have seen such an immense swell of demand that we have to temporarily pause signups for Jev… existing signups… will continue to function" — [@typesafeai on X](https://x.com/typesafeai/status/2102281508950307159); [aifront-page](https://aifront-page.com/typesafe-ai-pauses-jev-ai-model-signups-demand-surge/)
- 27 Sep 2026 (about 22:30 UTC; reported as 28 Sep 07:30 JST): [VENDOR] "Jev is back. Capacity has increased and signups are open!" — [@typesafeai on X](https://x.com/typesafeai/status/2104337822350221795); [VENDOR] "Note that new signups no longer get free credits; we hope to bring these back as soon as possible" — [@typesafeai on X](https://x.com/typesafeai/status/2104337824292220981); also reported by [Qualiteg](https://journal.qualiteg.com/jev-typesafe-ai-pricing-python-hands-on/) and [aifront-page](https://aifront-page.com/typesafe-ai-reopens-jev-sign-ups-free-credit-suspended/)
- [3P] The $5 credit was still paused as of 22 Oct 2026 — [aiextracash.com](https://aiextracash.com/tools/jev/jev-free-credit/)
- **Conflicts:** [jev-ai.live](https://jev-ai.live/get-access/) and [explainx.ai](https://www.explainx.ai/blog/jev-general-availability-no-waitlist-2026) still advertise the $5 credit and "no waitlist", which looks stale. Some third-party sites still say direct access needs a waitlisted key. Gateway access (Vercel, OpenRouter, Netlify) bypasses TypeSafe's signup entirely.

**Retention, training, region, SLA**
- [3P quoting terms] Retention is "as long as necessary", with no number given. ZDR is for enterprise accounts only, arranged via sales — [jev101.org privacy guide (unofficial)](https://jev101.org/guides/jev-privacy-guide); [neuraltrust.ai](https://neuraltrust.ai/blog/jev-typesafe-ai-security)
- [3P] No training on customer inputs. Since 1.14, customers can opt in to share requests for debugging, which are reportedly still not used for training — same sources
- [3P] US-only hosting (US West Coast); no EU region or EU data residency is documented — [colchix.com](https://colchix.com/blog/can-european-enterprises-use-jev); [jev101.org](https://jev101.org/guides/jev-privacy-guide)
- [GATEWAY] ZDR is available via OpenRouter (the `zdr` setting) and via Vercel AI Gateway provider options (ZDR, no-training) — search summary of the same result set

### Inferences
- With output free and input at $0.042 per 1M, cost is driven almost entirely by the size of the state multiplied by the number of calls. That is roughly 1/50th to 1/100th of the input price of mainstream LLMs. Pricing is labeled early-access, so it could change.
- For a developer starting today, gateway access (Netlify or Vercel) is the lowest-friction route, and it sidesteps TypeSafe's signup and credit changes.

### Gaps
- No SLA or uptime commitment was found.
- I found no official rate-limit numbers; only unofficial or conflicting figures exist.
- I found no source confirming signup status in November 2026. The last confirmed vendor statement is the 27 Sep reopening.
- Jev 1.14.0's release date and changes (beyond the debugging opt-in) were not confirmed.

## 4. Recommended use cases and what Jev is NOT for

### Takeaway
TypeSafe and secondary sources position Jev as a fast decision layer: classification, routing, scoring, moderation, guardrails and verification ("harness engineering"), and bulk labeling over corpora. It is explicitly not a text generator, and it is weak on multi-step reasoning, arithmetic and counting. Your application code, not Jev, decides which actions to take on its probabilities.

### Cited Findings
- [VENDOR] Official docs include an "Example use cases" page that lists model routing (Jev picks which LLM receives each prompt, with thresholds set in your code) — [docs.typesafe.ai/concepts/use-case-map](https://docs.typesafe.ai/concepts/use-case-map) (search summary only)
- [VENDOR via 3P] "Harness engineering" is named as a core use: verification, guardrails, and checking tool calls before execution — [pjburnhill project-reference gist](https://gist.github.com/pjburnhill/adf8d28efcad9df037bfdece178ef965)
- [3P] Moderation pattern: combine severity and confidence to choose allow, warn, review or block — [ayautomate](https://www.ayautomate.com/blog/jev-use-cases). A vision model converts images to text and Jev does the final classification — [cloudraft](https://www.cloudraft.io/blog/top-use-cases-of-jev-typesafe-ai-model)
- [3P] Map-reduce over corpora: apply one label set to every record, then aggregate. This is explicitly an inferred pattern, not one TypeSafe has verified — [explainx.ai](https://www.explainx.ai/blog/top-10-jev-typesafe-ai-use-cases-2026)
- [3P] Not for: writing copy or summaries, which belong with an LLM — [sellingwithnas](https://www.sellingwithnas.com/how-to-use-jev-typesafe-ai). Jev does not decide which actions are permitted; application code does — [gist](https://gist.github.com/pjburnhill/adf8d28efcad9df037bfdece178ef965)
- [VENDOR via 3P] Single-pass design makes step-by-step reasoning a poor fit. TypeSafe lists arithmetic and counting among the weak spots — search summary of [DataCamp](https://www.datacamp.com/blog/system-one-models-jev) / [vals.ai](https://www.vals.ai/blogs/independent-evaluation-of-jev)
- [3P] "Fuzzy if statement for code" framing — [Flavio Copes](https://flaviocopes.com/jev/)
- [VENDOR via press] TypeSafe itself reportedly said a conventional, non-AI Doom bot could play better than Jev — [awesomejev.app (unofficial)](https://www.awesomejev.app/blog/register-jev-doom/)

### Inferences
- In a workflow, Jev fits as a gate or router around LLM steps (pre-checks, post-verification, triage). It does not replace the LLM steps that generate or plan.

### Gaps
- I could not read the exact official "not for" wording on docs.typesafe.ai.

## 5. Company, founders, funding and maturity signals

### Takeaway
TypeSafe AI is a San Francisco company founded in 2024. The CEO is Diogo Almeida, a co-author of InstructGPT. It reportedly raised a $40M seed led by DCVC and then a reported $870M Series A at a $7.5B valuation in October 2026, though that round is disputed by one aggregator. Maturity signals include The Register coverage, a Doom demo, wide gateway listings, many independent benchmarks and a DeepLearning.AI *The Batch* mention. I found **no Wikipedia article**, only an AI Wiki page.

### Cited Findings
- [3P] Founders: Diogo Almeida (CEO, InstructGPT co-author), Erik Gafni (CTO) and Sasha Sheng (COO); founded 2024 — [jevai.tools (unofficial)](https://jevai.tools/learn/typesafe-ai); [Firecrawl](https://www.firecrawl.dev/blog/what-is-jev). Also "a former OpenAI researcher" in San Francisco — [AI Wiki](https://aiwiki.ai/wiki/jev/raw)
- [3P] Seed: $40M led by DCVC on exiting stealth — search summary of [Firecrawl](https://www.firecrawl.dev/blog/what-is-jev) / [jevai.tools](https://jevai.tools/learn/typesafe-ai)
- [3P/press] Series A: $870M at $7.5B, led by Andreessen Horowitz with Sequoia and DCVC — [Tech Times, 13 Oct 2026](https://www.techtimes.com/articles/328875/20261013/typesafe-ai-raises-870m-jev-decision-model-that-never-generates-text.htm); [swytchcode](https://www.swytchcode.com/content/typesafe-ai-870m-series-a). **Disputed:** one aggregator says the announced round was smaller. A further "$1B+ at $10B+" raise rumor is unverified.
- [Press] The Register (16 Sep 2026), "TypeSafe AI debuts model for machines that plays Doom", notes that TypeSafe's "hallucination-free" claim isn't a fair comparison because Jev doesn't output natural language — [The Register](https://www.theregister.com/ai-and-ml/2026/09/16/typesafe-ai-debuts-model-for-machines-that-plays-doom/5296711)
- [Press] DeepLearning.AI *The Batch*: "Jev, a classification model, takes the developer world by storm, inspires imitators" — [The Batch](https://www.deeplearning.ai/the-batch/models-built-to-do-one-thing-well)
- [INDEP] An open-model replica of Jev's API played the Doom demos, but its authors could not verify TypeSafe's training, latency or pricing claims — [blocks.ai](https://blocks.ai/blog/jev-open-model-doom). A community post also promotes "the open version" during the signup pause — [X post](https://x.com/0xTreff/article/2106096330422518102)
- [3P] Wikipedia: none found. The closest is [AI Wiki "Jev (AI model)"](https://aiwiki.ai/wiki/jev/raw), last updated 16 Sep 2026
- [3P] TypeSafe has not published Jev's architecture or a technical paper — search summary of the benchmark result set ([vals.ai](https://www.vals.ai/blogs/independent-evaluation-of-jev))

### Inferences
- The product is about two months old, in early access, with fast-moving pricing and limits and a capacity-constrained signup history. It has heavy hype and SEO lookalike activity. Treat it as pre-GA from a reliability standpoint.

### Gaps
- I could not confirm the funding round from a primary source, such as a TypeSafe or a16z announcement.
- I could not find a Wikipedia "Jev (AI model)" page. If the brief's mention of one comes from a specific source, it may refer to the AI Wiki page.

## 6. Is "calibrated probability" defined and evidenced?

### Takeaway
TypeSafe markets Jev's outputs as calibrated probabilities but reportedly publishes **no** calibration metrics: no ECE, reliability plots, Brier score or log loss. Independent evaluations are mixed. Jev is well calibrated on some tasks (routing ECE 0.025 in one benchmark) and worse than frontier LLMs on others (spam), and it is a mediocre correctness predictor in an arXiv study. TypeSafe's own performance evaluation was self-conducted, and the company acknowledges possible bias.

### Cited Findings
- [3P] TypeSafe reportedly publishes no ECE, reliability plot, Brier score or log loss for Jev on any dataset — search summary of [vals.ai independent evaluation](https://www.vals.ai/blogs/independent-evaluation-of-jev) / [Medium independent benchmark](https://medium.com/@pravvich/typesafes-jev-beyond-the-hype-an-independent-benchmark-8bdc1c99d000)
- [INDEP] Its aggregate calibration error is not clearly better than an LLM's; on spam, a frontier model had lower ECE than Jev — [Medium: "Jev beyond the hype"](https://medium.com/@pravvich/typesafes-jev-beyond-the-hype-an-independent-benchmark-8bdc1c99d000)
- [INDEP] Jev vs Claude benchmark: routing ECE 0.025 (best of the three models tested), less impressive on other tasks — [stern9/jev-bench](https://github.com/stern9/jev-bench)
- [INDEP] As a correctness predictor over 1,718 responses: AUROC 0.666, Brier 0.240, ECE 0.133, strongest on short factual answers and weakest on multi-step reasoning — [arXiv 2609.24881 "Pinocchio"](https://arxiv.org/pdf/2609.24881)
- [INDEP] "Level with mid-price LLMs, behind the frontier" on accuracy after eight days of tests — [DEV Community](https://dev.to/gde/jev-after-eight-days-of-independent-tests-level-with-mid-price-llms-behind-the-frontier-1kln)
- [INDEP] Other evaluations: [vals.ai](https://www.vals.ai/blogs/independent-evaluation-of-jev), [JevBench leaderboard](https://github.com/fstandhartinger/jevbench), [Qualiteg (301 API calls)](https://journal.qualiteg.com/jev-typesafe-ai-pricing-python-hands-on/), and the explainer [victordibia.com "How Jev works: calibrated decision models"](https://victordibia.com/explainers/jev/)
- [3P] TypeSafe's own evaluation was self-conducted, and the company acknowledges possible bias. "Immune to hallucination" is a company claim — search summary (launch coverage; see [letsdatascience](https://letsdatascience.com/news/typesafe-ai-launches-jev-decision-model-889a38c0))
- [3P] One comparison notes that internal benchmarks show lower raw accuracy than general models, despite the latency advantage — search summary (pricing result set, e.g. [developersdigest](https://www.developersdigest.tech/blog/typesafe-jev-system-one-models-release-guide-2026))

### Inferences
- "Calibrated" should be treated as a vendor design goal, not a verified property. Anyone integrating Jev should measure calibration on their own labeled data per task and set thresholds empirically, since quality varies by task.

### Gaps
- I couldn't find TypeSafe's formal definition of "calibrated probability", or any vendor calibration curves.
- I could not read the full independent reports, so the dataset details and model versions tested are unknown.
