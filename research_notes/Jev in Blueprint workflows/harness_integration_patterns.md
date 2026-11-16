# Jev and typed decision models in LLM agent harnesses: integration patterns

> Method note (read first): page fetches were blocked by this session's network policy, including composio.dev, langchain.com and openclawdatabase.com. Every finding below comes from web-search result summaries and snippets, not from reading the full pages. Treat specific numbers as "reported by the cited page" and re-verify them before any of them goes into the kit as fact. I found no width.ai page and no HackerNoon "Inside Jev" article. The closest matches are listed under Gaps. Vendor claims are marked **[vendor]**, community or third-party claims **[3p]**, and primary docs or papers **[primary]**.

## Q1: What harness patterns do TypeSafe and commentators describe for Jev?

### Takeaway
Commentators agree on one framing: "the LLM writes, Jev decides, code acts." Jev is a non-generative "System One" model. It answers narrow typed questions (Choice, Score, and Noul primitives) with probabilities, and host code turns those answers into actions. The patterns that keep recurring are tool-call gating, model and intent routing, compaction or stop triggers, triage before an expensive model, and per-file relevance scoring over a repo. TypeSafe says plainly that Jev does not replace the coding agent. It is a component you call from your own harness.

### Cited Findings
- **What it is.** Jev is TypeSafe AI's "System One" decision model. It does not generate text. It answers typed questions with probabilities. **[3p summarising vendor]** [LangChain blog: Building a Harness with Jev](https://www.langchain.com/blog/building-a-harness-with-jev); [flaviocopes deep dive](https://flaviocopes.com/jev/)
- **Launch and access.** TypeSafe came out of stealth on 15 Sept 2026 with $40M seed funding, and Jev was its first public model. It is served through a hosted "System One API". **[3p reporting vendor]** [The New Stack](https://thenewstack.io/typesafe-jev-system-one/); [Firecrawl: What is Jev](https://www.firecrawl.dev/blog/what-is-jev)
- **Latency.** TypeSafe claims answers in "as little as 150 ms". **[vendor]** [Firecrawl](https://www.firecrawl.dev/blog/what-is-jev). Independent and third-party numbers are covered in Q4.
- **Three primitives.** Choice (pick one of N), Score, and Noul. A Leanpub book has chapters on all three and on the TypeScript SDK. **[3p]** [Leanpub: Jev](https://leanpub.com/Jev). Composio's toolkit exposes "Evaluate State", which runs Choice, Score or Noul questions, and "List Models". **[3p]** [Composio: TypeSafe Jev Guide, 6 use cases](https://composio.dev/content/typesafe-jev-guide-and-best-practical-usecases)
- **Canonical loop.** The harness observes state and builds a candidate list. Jev picks one candidate. The harness executes it and observes again. Typical uses listed are gating tool calls, routing between models, deciding when to compact context, and checking answers. **[3p]** [DEV: How to engineer a Jev harness](https://dev.to/arthurkatcher/how-to-engineer-a-jev-harness-2f22); [Level Up: decision models inside an agent harness](https://levelup.gitconnected.com/decision-models-inside-an-agent-harness-4f605b4d1ef2)
- **Four-question permit pattern.** The LLM proposes an action. Jev answers four narrow yes/no questions. Pure host code maps those answers to `permit`, `proposal_only`, `reject` or `unavailable`. **[3p]** [aibuilderclub: Jev Engineering, LLM Writes, Jev Decides, Code Acts](https://www.aibuilderclub.com/blog/jev-engineering-guide)
- **LangChain middleware example.** It covers a guardrail on the bash tool and model routing. A related tutorial blocks anything Jev scores at or above a set threshold. **[3p]** [LangChain blog](https://www.langchain.com/blog/building-a-harness-with-jev)
- **Irreversible actions.** Jev *can* be the only check on an irreversible action. The recommended pattern is to let Jev gate the call and to require a human for the destructive branch. **[3p]** [DEV harness guide](https://dev.to/arthurkatcher/how-to-engineer-a-jev-harness-2f22)
- **"10 levels of Jev in an agent harness" video (28 Sept 2026).** The title lists gates, routing, compaction and cheap file reads. One demo uses a custom "ask Jev" tool that takes a path and a question, plus a sibling tool that classifies files by role. The main agent answered questions about token validation and real credentials using about 2K tokens without reading either file. **[3p]** [openclawdatabase summary](https://openclawdatabase.com/news/videos/2026-09-28-jev-ten-levels-agent-harness-gates-routing-file-reads/)
- **Triage before an expensive model.** Jev triages or classifies a large volume of items cheaply, and only the relevant subset goes to a full model. **[3p]** [MindStudio: Jev use cases automation](https://www.mindstudio.ai/blog/jev-use-cases-automation)
- **Escalation.** Results Jev is uncertain about go to a fallback model or a human reviewer. **[3p]** [Composio](https://composio.dev/content/typesafe-jev-guide-and-best-practical-usecases)
- **Model-tier and effort routing for coding agents.** A "Jev Codex Router" picks the model tier and reasoning effort before a task runs. A LinkedIn post lists a "memory promotion gate" among its use cases. **[3p]** [LinkedIn: Top 12 agentic use cases for Jev](https://sg.linkedin.com/in/canhld)
- **Browser agent action selection.** Jev picks the next browser action from DOM state, and a small generative model handles the text-heavy steps (a Browser Use experiment, reported secondhand). **[3p]** [Zimaspace: Jev use cases](https://shop.zimaspace.com/blogs/tech-ai-hub/jev-use-cases-decision-model-examples)
- **Map-reduce over repo files.**
  - **Jevgrep** (dzhng, MIT). It walks the repository hierarchy, follows branches that qualify, and selects files from content previews. It claims about 30% lower agent cost. Its own measurement is 28.6% on 10 Python SWE-bench tasks, where both arms solved 8 of 10, and that figure *excludes Jev's own cost*. A third-party write-up notes at least $1.57 in Jev charges left out of the saving, and says the result is not shown to hold for larger repos or other languages. **[3p, including critique]** [jevgrep wiki](https://github.com/dzhng/jevgrep/wiki); [RuntimeWire critique](https://runtimewire.com/article/david-zhang-jevgrep-coding-agent-costs)
  - **FlashBob** (hackathon project). An MCP tool calls Jev to score every file in a workspace mirror for relevance and importance. **[3p]** [lablab.ai FlashBob](https://lablab.ai/ai-hackathons/ibm-bob-2-hackathon/conquerors/flashbob)
  - **Devin "agentic map reduce"** (not Jev-specific). A deterministic filter selects files, batches go to parallel workers, and a reduce step synthesises the results. It cites a study finding that reading and searching took more than half of tool-use turns and nearly half of the main agent's tokens. **[3p]** [Devin blog](https://devin.ai/blog/agentic-map-reduce)
- **Agent evaluation.** Jev is used as a cheap grader of agent traces. **[3p]** [Daily Dose of DS](https://blog.dailydoseofds.com/p/jev-clearly-explained); [Towards AI: Build an AI agent evaluation with JEV](https://pub.towardsai.net/build-an-ai-agent-evaluation-with-jev-392c146ca816)
- **Stated limitation.** TypeSafe says Jev cannot break the declared output schema, but it *can* pick the wrong valid option with high confidence. Type safety prevents malformed output. It does not prevent bad judgement. **[vendor, via 3p]** [DEV harness guide](https://dev.to/arthurkatcher/how-to-engineer-a-jev-harness-2f22)
- **Name collision.** "Jev Harness" (Apixly) is a separate open-source MCP project. The primary AI defines tools, observation and completion checks, and Jev chooses the next tool and its arguments. **[3p]** [Glama: Jev Harness (Apixly)](https://glama.ai/mcp/servers/lh1hlo49ub)

### Inferences
- For a planning skill that hands off to a coordinator and workers, the patterns that fit most clearly are:
  - (a) a **PreToolUse gate** on risky worker actions, with "deny or ask a human" for destructive branches.
  - (b) **routing or triage** of which worker or model tier gets a task.
  - (c) a **Stop/SubagentStop "is this task actually done?" check** that escalates to the LLM or a human on low confidence.
  - (d) **map-reduce relevance scoring** of repo files during an audit or "review an existing project" phase.
  - (e) **cheap scoring of candidates**, such as plan options or risk flags, ahead of LLM synthesis.
- The pattern that consistently works keeps Jev's output as a **typed signal that deterministic code acts on**. It never acts as a free-form instruction to the agent.

### Gaps
- No width.ai article titled "where it fits in an agent harness" turned up in search. A HackerNoon "Inside Jev" article was not found either. The only HackerNoon hit was ["using jev in production"](https://hackernoon.com/using-jev-in-production), and its content could not be read.
- I could not read Composio's full list of "6 best practical use cases" because the fetch was blocked. Only the toolkit description and the escalation point came through.
- The full list of the 10 levels in the openclawdatabase video summary is unknown, since only its title and one demo came through. Whether Noul means "none of the above" or "null/abstain" is unconfirmed.

## Q2: General agent-engineering patterns (routers and cascades, guardrails, judges vs classifiers, abstain, stuck detectors)

### Takeaway
Routing, guardrail screening and evaluator loops are established agent patterns. Anthropic describes them, and the cascade literature (FrugalGPT, RouteLLM) reports large cost savings from sending easy queries to cheap models. Jev-specific evidence says its probabilities rank decisions well enough to support "accept if confident, otherwise escalate". Stuck-loop detection, though, is best handled by deterministic counters outside the model, not by a fuzzy classifier.

### Cited Findings
- **Anthropic patterns.** Anthropic's "Building effective agents" names five patterns. **[primary]** [Anthropic: Building effective agents](https://www.anthropic.com/research/building-effective-agents)
  - **Routing** classifies an input and sends it to a specialised follow-up, for example simpler queries to smaller, cheaper models.
  - **Guardrails** use one model instance to screen queries while another does the core work. Anthropic says this tends to work better than one call doing both.
  - **Parallelization** comes in two forms, sectioning and voting.
  - **Evaluator-optimizer** works best when clear evaluation criteria exist.
  - **Start simple** and add complexity only when it is needed. One version of the page notes that much of its tooling has changed since Dec 2024.
- **FrugalGPT (Stanford, 2023).** An LLM cascade with a scorer matched the best single model at up to 98% lower cost, or reached about 4% higher accuracy at the same cost. Per-dataset savings were 98.3%, 73.3% and 59.2%. **[primary]** [FrugalGPT arXiv 2305.05176](https://arxiv.org/pdf/2305.05176); [DeepLearning.AI summary](https://charonhub.deeplearning.ai/frugalgpt-a-method-to-cut-ai-costs-and-maintain-quality/)
- **RouteLLM (LMSYS, ICLR 2025).** Secondary sources report about 85% cost reduction on MT-Bench at 95% of GPT-4 quality, with 14% of queries sent to the strong model. Another blog reports about 2x savings with no measurable quality loss on Chatbot Arena at threshold 0.5. The two sets of figures differ by benchmark and threshold, and I did not verify either against the primary paper. **[3p]** [neuraltrust: LLM model routing](https://neuraltrust.ai/blog/llm-model-routing); [intuitionlabs](https://intuitionlabs.ai/articles/ai-model-routing-cost-quality)
- **Abstain and confidence thresholds with Jev.**
  - An RL preprint finds Jev's probabilities calibrated when pooled but *not* within individual benchmarks. Keeping the half of decisions with the largest |p − 0.5| raised median accuracy from 0.793 to 0.933, which supports routing low-confidence decisions to a judge or a human. **[primary, preprint]** [arXiv 2609.29429: Just Ask Jev](https://arxiv.org/pdf/2609.29429)
  - In a medical benchmark preprint, Jev's answers with p ≥ 0.9 were 93.4% accurate and covered 52.9% of questions. Where ranking failed (DiagnosisArena-MCQ), no threshold compensated. **[primary, preprint]** [arXiv 2609.34024](https://arxiv.org/abs/2609.34024)
- **Calibrated classifier vs LLM-as-judge.** A prompt-based Stop hook in Claude Code is LLM-as-judge, and it uses Haiku by default. A Jev gate is the calibrated-classifier alternative. **[3p on hooks]** [hexisteme: Stop hooks as behavioral gates](https://hexisteme.github.io/notes/stop-hook-gates.html). External reviewer gates already exist, for example Bouncer, "an independent quality gate that audits Claude Code's output before it can stop". **[3p]** [buildingopen/bouncer](https://gh.r-mj.com/buildingopen/bouncer)
- **Stuck or looping agents.**
  - Keep the detector outside the model. Exact-repeat detection catches the obvious loops. One source argues *against* semantic-similarity detection because it moves a safety decision into a fuzzy classifier. **[3p]** [DEV: Semantic loop detection](https://dev.to/praveenlavu/semantic-loop-detection-catching-stuck-ai-agents-1nd6); [MatrixTrak](https://matrixtrak.com/blog/agents-loop-forever-how-to-stop)
  - Backoff and polling loops look like stalls and cause false alarms. **[3p]** [DEV: detect when your agent is stuck](https://dev.to/clawgenesis/how-to-detect-when-your-ai-agent-is-stuck-and-what-to-do-about-it-ce9)
  - Escalate when the agent lacks information, authority or a safe next action. Treat policy blocks as stop or escalate, never retry. A typed outcome set (ASK / REFUSE / UNKNOWN / PROCEED) is recommended. **[3p]** [DEV: Escalation rules for agents](https://dev.to/dowhatmatters/escalation-rules-for-agents-ask-vs-refuse-vs-unknown-scope-is-a-contract-not-a-vibe-4gj6); [DEV: Stopping conditions for multi-agent loops](https://dev.to/dowhatmatters/stopping-conditions-that-actually-stop-multi-agent-loops-bnb)
- **Claude Code "done" gates.** Common practice is to run the test suite in a Stop hook so failing tests force Claude to keep working. Hooks must check `stop_hook_active` to avoid infinite loops. **[3p]** [codeongrass: make Done mean tests passed](https://codeongrass.com/blog/claude-code-hooks-done-means-tests-passed/); [claudefa.st: stop hook task enforcement](https://claudefa.st/blog/tools/hooks/stop-hook-task-enforcement)

### Inferences
- **Verification order for the coordinator.** Use deterministic checks first: tests, lint, file exists, iteration counters. Use a Jev typed check second, for semantic questions such as "does this diff address acceptance criterion X?" Escalate to the LLM, or to a human for destructive actions, only when Jev's |p − 0.5| is small. This matches the cascade and abstain literature and Anthropic's "start simple".
- **Loop and stuck detection** should stay a deterministic counter in the coordinator, with Jev at most as a secondary signal. That matches the practitioner consensus.

### Gaps
- I did not verify primary RouteLLM figures.
- I found no OpenAI or Google agent-guide citations in this pass.
- I found no Jev-specific published case of stuck-agent detection.

## Q3: Claude Code and Agent SDK integration points, and whether a Jev MCP server or SDK integration exists

### Takeaway
Claude Code offers several places to call an external classifier:
- PreToolUse, which can allow, deny, ask, defer, or modify a call.
- PostToolUse.
- Stop and SubagentStop, which can block "done" and force the agent to continue.
- UserPromptSubmit.
- Hooks of type `mcp_tool`, which call an MCP server directly.
- MCP tools the agent calls itself.
- Skills that run scripts.

TypeSafe ships an official agent skill that installs as a Claude Code plugin. Whether TypeSafe also runs its own MCP server is disputed. Community MCP servers (jev-mcp, Composio toolkit, Apixly Jev Harness) do exist. Jev is also reachable through OpenRouter, Vercel AI Gateway, Pydantic AI and LangChain.

### Cited Findings
- **PreToolUse.** It runs before a tool executes. It can block with exit code 2 or return a JSON decision, and it can allow, deny, ask, defer, or modify the tool input. **[3p summarising docs]** [pushary: Claude Code hooks explained](https://pushary.com/blog/claude-code-hooks-explained); [Penligent](https://www.penligent.ai/hackinglabs/inside-claude-code-the-architecture-behind-tools-memory-hooks-and-mcp/). When several hooks disagree, the most restrictive wins: deny > defer > ask > allow. **[3p]** [Blake Crosley](https://blakecrosley.com/blog/claude-code-hooks-explained)
- **Agent SDK.** Hook callbacks are passed in the `hooks` option of `query()`, with matchers such as `Bash` or `Read`. MCP tools appear as `mcp__<server>__<tool>`. **[primary]** [Claude Code Docs: Agent SDK hooks](https://code.claude.com/docs/en/agent-sdk/hooks)
- **`mcp_tool` hooks.** A PreToolUse hook can be of type `mcp_tool` and call a policy MCP server. If the response cannot be read (over 16 MiB), the call is refused. Only one hook should rewrite a given tool's input, because updated inputs are not merged. **[3p]** [buildthisnow: MCP tool hooks](https://www.buildthisnow.com/blog/tools/hooks/mcp-tool-hooks); [claude-howto hooks README](https://github.com/luongnv89/claude-howto/blob/main/06-hooks/README.md)
- **Stop and SubagentStop.**
  - Exit code 2 prevents the stop and continues the conversation. Exit code 1 is non-blocking, which is a common pitfall.
  - Prompt-type hooks send a verifier prompt to a model (Haiku by default).
  - `stop_hook_active` signals a forced continuation.

  The JSON schema is reported inconsistently: `decision: "block"` + `reason` in one source, `{ok:false, reason}` for prompt hooks in another, with possible deprecation in favour of `hookSpecificOutput`. **[3p, conflicting]** [hexisteme](https://hexisteme.github.io/notes/stop-hook-gates.html); [mintlify claude-code-best-practice hooks](https://mintlify.com/shanraisshan/claude-code-best-practice/concepts/hooks); [smithery hook-developer](https://smithery.ai/skills/parcadei/hook-developer)
- **Official TypeSafe agent skill.**
  - Repo: `typesafe-ai/skills`. Install it as a Claude Code plugin from that marketplace and invoke it as `/typesafe:typesafe-ai`. Other agents can use `npx skills add typesafe-ai/skills --skill typesafe-ai`.
  - The repo is reported as MIT-licensed.
  - It is a skill for *building with* the System One API, not a runtime gate. **[primary, vendor docs]** [TypeSafe docs: Agent skill](https://docs.typesafe.ai/agent-skill); [GitHub typesafe-ai/skills](https://github.com/typesafe-ai/skills); [TypeSafe quickstart](https://docs.typesafe.ai/introduction/quickstart)
- **No drop-in model setting.** TypeSafe's coding-agents page reportedly says there is no `model: "jev-latest"` setting that turns Claude Code into a Jev agent. Jev is a component inside the agent you build. **[vendor, via 3p]** [DEV harness guide](https://dev.to/arthurkatcher/how-to-engineer-a-jev-harness-2f22); [flaviocopes: Jev with Claude Code, Codex and Cursor](https://flaviocopes.com/jev-coding-agents/)
- **MCP: conflicting reports.**
  - Flavio Copes and jevaiguide say the docs site answers as a remote MCP server at `https://docs.typesafe.ai/mcp`. That is a *docs* MCP, not a decision endpoint. [flaviocopes](https://flaviocopes.com/jev-coding-agents/); [jevaiguide](https://jevaiguide.com/integrations/claude-code/)
  - APIMaster says TypeSafe ships no MCP server of its own. It points to the community `jkudish/jev-mcp`, which exposes ten typed judgments as MCP tools for Claude Code and Codex. [APIMaster: four routes](https://apimaster.ai/blog/jev-claude-code-codex)
  - Other MCP listings: [mcpmarket jev-2](https://mcpmarket.com/server/jev-2), [withone.ai Jev MCP](https://www.withone.ai/mcp/jev), the Composio toolkit (Evaluate State and List Models through Tool Router, bring your own Jev key) [Composio](https://composio.dev/content/typesafe-jev-guide-and-best-practical-usecases), and Apixly Jev Harness [mcpservers.org](https://mcpservers.org/servers/apixly-ai/jev-harness). **[3p]**
- **SDKs and gateways.**
  - TypeSafe offers Python and JS SDKs. The Python SDK uses `TYPESAFE_API_KEY` and defaults to `jev-latest`.
  - Through OpenRouter, pin an exact version such as `typesafe/jev-1.13`.
  - Jev is also on Vercel AI Gateway, Pydantic AI and LangChain. **[3p/primary mix]** [Pydantic AI: TypeSafe model docs](https://pydantic.dev/docs/ai/models/typesafe.md); [LangChain JS TypeSafe provider](https://docs.langchain.com/oss/javascript/integrations/providers/typesafe); [Vercel: jev agent control](https://vercel.com/i/jev-agent-control)

### Inferences
- **Lowest-friction integration for a Blueprint kit.** A small script, Python or TS SDK with a pinned model version, called from:
  - (1) a **PreToolUse** command hook on `Bash|Write|Edit` for worker risk gating.
  - (2) a **SubagentStop** hook as the coordinator's "did the worker meet its acceptance criteria?" first pass.
  - (3) skill-invoked scripts for batch triage, such as file relevance and task routing.

  Use a community MCP server only if the agent itself should choose when to ask Jev. Hooks are deterministic and cannot be skipped by the model, while MCP tools are optional for the model.
- **Pin the model version.** Use an exact version (for example `jev-1.13`) instead of `jev-latest` so gate behaviour stays reproducible across kit runs.

### Gaps
- I could not confirm from TypeSafe's own docs whether `docs.typesafe.ai/mcp` exists or what it exposes.
- I did not read the official Claude Code hooks reference directly, so the exact current JSON field names for Stop and SubagentStop blocking need checking against [code.claude.com/docs hooks](https://code.claude.com/docs/en/agent-sdk/hooks).
- I could not read the contents of the `jkudish/jev-mcp` tool list.

## Q4: Cost, latency and accuracy break-even: when is an extra model call worth it?

### Takeaway
Jev is cheap and fast. Reported prices are around $0.04 per million input tokens, with about 150–400 ms per call. Its accuracy and calibration, though, vary a lot by task: competitive on some classification benchmarks, clearly worse than a frontier LLM on harder reasoning, and sometimes no better calibrated than a scikit-learn baseline. It is worth calling when the decision is narrow and frequent, when it replaces a full LLM turn or many file reads, and when low-confidence cases can be escalated. It is not worth calling for rare, high-context, reasoning-heavy judgements the main LLM is already making in context.

### Cited Findings
- **Price.** One tutorial reports $0.042 per million input tokens, "under a third of" GLM 5.3 Flash's input price. **[3p; verify with vendor]** [LangChain blog / search summary](https://www.langchain.com/blog/building-a-harness-with-jev)
- **Latency.**
  - TypeSafe claims about 150 ms. **[vendor]** [Firecrawl](https://www.firecrawl.dev/blog/what-is-jev)
  - Median 194 ms on 60-ticket triage. **[3p]** [OpenRouter: Jev vs LLM](https://openrouter.ai/blog/tutorials/jev-vs-llm-when-to-use-each/)
  - 140 ms server-side, 0.84 s end to end through a reseller. **[3p]** [AI/ML API: What is Jev](https://aimlapi.com/blog/what-is-jev)
  - Median 0.27–0.31 s. **[preprint]** [arXiv 2609.34024](https://arxiv.org/abs/2609.34024)
  - A practitioner measured median 0.37 s and p95 0.61 s with eight questions per call. **[3p]** (reported in search summary of [jev-benchmarks](https://github.com/AbdelStark/jev-benchmarks))
- **Accuracy vs a frontier LLM (medical preprint).** Jev ≈ GPT-6 Sol (medium reasoning) on PubMedQA (78.4% vs 78.2%), lower on MetaMedQA (74.8% vs 82.7%), and "much lower" on other tasks. Jev was better calibrated on MetaMedQA (ECE 0.063 vs 0.146). **[preprint]** [arXiv 2609.34024](https://arxiv.org/html/2609.34024v1)
- **Calibration critiques.**
  - A scikit-learn rebuild matched or beat Jev's calibration on Banking77. A threshold chosen without labels missed its precision target by 2.6 points. **[3p]** [Towards Data Science](https://towardsdatascience.com/scikit-learn-matched-or-beat-jevs-calibration-on-banking77/)
  - On DAIR Emotion, Jev's Brier score was worse (0.846 vs 0.668). **[3p]** [AbdelStark/jev-benchmarks](https://github.com/AbdelStark/jev-benchmarks)
  - A further audit exists. **[3p]** [jujumilk3/jev-calibration-audit FINDINGS](https://github.com/jujumilk3/jev-calibration-audit/blob/main/FINDINGS.md)
  - Amplitude's verdict: "faster and cheaper, but watch the accuracy". In other tests, both LLMs and decision models missed against labelled data. **[3p]** [Amplitude: Jev analysis](https://amplitude.com/blog/jev-analysis)
  - Another reproducible lab: **[3p]** [jev-dspy-lab](https://github.com/jmanhype/jev-dspy-lab)
- **Net savings can be overstated.** Jevgrep's 28.6% agent-cost saving excluded Jev's own charges, and it rests on a sample of 10 tasks. **[3p]** [RuntimeWire](https://runtimewire.com/article/david-zhang-jevgrep-coding-agent-costs)
- **Cascade economics in general.** Savings come from most queries resolving at the cheap tier. FrugalGPT reports 59–98% savings depending on the dataset. **[primary]** [FrugalGPT](https://arxiv.org/pdf/2305.05176)

### Inferences
- **When an extra Jev call pays off**, roughly:
  - **Volume.** The decision repeats many times per run: per file, per tool call, per worker turn.
  - **Displacement.** Each call replaces a full LLM turn, Haiku prompt hook, or file read that costs far more than about $0.04/M tokens and about 300 ms.
  - **Escalation.** Ambiguous cases (small |p − 0.5|) have a defined path to the LLM or a human.
  - **Validation.** You can build a small labelled set (even 30–100 examples from the project) to choose thresholds. The calibration critiques show that thresholds set without labels can miss.
- **When it does not pay off.**
  - One-off decisions inside a turn where the main LLM already holds the context, such as the planner choosing between options it just reasoned about.
  - Reasoning-heavy judgements where Jev trails frontier models.
  - Safety-critical irreversible actions without a human or deterministic backstop.
  - Anything a deterministic check already settles, such as tests passing or a file existing.
- **For Blueprint specifically.** Treat Jev as an **optional, version-pinned accelerator**: the kit must still work if Jev is unavailable, mapping to the `unavailable` outcome from the four-question pattern. Note the integration in the kit, but leave enabling it to the user, because it adds an external API key, data egress to TypeSafe, and a non-Anthropic dependency.

### Gaps
- I found no authoritative current TypeSafe price list, rate limits or data-retention terms, because fetches were blocked.
- I found no published head-to-head of Jev vs Haiku prompt hooks for Stop/SubagentStop verification in coding agents.
- I found no independent benchmark of Jev on code-specific decisions such as diff-meets-criterion or file relevance at scale beyond the 10-task Jevgrep sample.
