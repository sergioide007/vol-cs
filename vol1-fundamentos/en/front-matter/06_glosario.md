# Volume 1 Operational Glossary

*Concise definitions anchored to the chapter where each concept is developed. When a term takes on distinct nuances across different volumes of the series, it is noted. This glossary does not substitute for the chapters; it resolves ambiguities mid-reading and establishes a shared baseline vocabulary for your engineering team.*

| Term | Operational Definition | Chapter |
|---|---|---|
| **Agent** | A software system that governs the control flow of its own steps based on task state, not merely the content of its textual output. Distinguished from a *workflow* by who owns control flow decisions. | 1, 4 |
| **Workflow (Fixed Chain)** | A predefined sequence of execution steps; the language model synthesizes content but does not determine the path. Budgeted, tested, and governed differently than an autonomous agent. | 1 |
| **Autonomy Spectrum** | A formal scale of levels (0 to 4) classifying a system by how much decision authority it exercises autonomously. Selected based on task structure, never organizational ambition. | 1 |
| **Harness** | The suite of deterministic runtime controls surrounding the model: iteration budgets, authorized tools, output schema validators, and loop breakers. The critical layer that allows an experimental agent to survive in production. | 4 |
| **ReAct** | A reasoning-action-observation loop alternating cognitive deliberation with tool execution until an objective is met. Foundational baseline for the family of agent reasoning patterns. | 4 |
| **Context Window** | The finite token capacity available in a single inference call. It is not persistent memory: it purges completely upon turn completion unless backed by an external persistence layer. | 4, 10 |
| **Agent Memory** | Persistent state that outlives an individual inference call, retrieved via explicit mechanisms (key-value stores, vector indexes, episodic summaries). Governed by an observable lifecycle. | 10 |
| **Tool** | A capability exposed to an agent with an explicit name, description, and input schema. The description guides invocation; the host server strictly enforces authorization and execution boundaries. | 4, 9 |
| **Skill** | A discrete unit of procedural knowledge with progressive disclosure: metadata is always accessible, while detailed operational instructions load only when task context demands it. | 7 |
| **Progressive Disclosure** | A context optimization pattern ensuring only essential operational detail is injected into the prompt at any given step, minimizing latency, token cost, and model degradation. | 7 |
| **Synthetic Enterprise** | The organizational pattern of decomposing complex workflows into specialized agent roles with strict contracts, counteracting the entropy of monolithic "god agents." | 5 |
| **Master Prompt** | A single, authoritative prompt template reused across multiple agents, applying DRY to prompt engineering. Introduces architectural coupling that must be actively governed. | 5 |
| **Bounded Context** | A domain boundary within which an architectural model and ubiquitous language maintain unambiguous meaning. Serves as an immune system against semantic drift. | 6 |
| **Domain Invariant** | A business rule that must hold true across every state transition in an aggregate. An agent can violate it without detection unless explicit deterministic validators enforce it. | 6 |
| **Orchestration Pattern** | A canonical topology for coordinating multiple agents: pipeline, fan-out, council, hierarchical delegator, or self-reflection loop. Each mandates its own graceful degradation policy. | 8 |
| **Graceful Degradation** | The disciplined operational posture of serving reduced but explicitly declared quality or coverage rather than suffering hard failure. Degrading silently is lying with infrastructure. | 3, 8 |
| **Model Context Protocol (MCP)** | An open standard converting $M \times N$ custom integrations into an $M + N$ architecture over JSON-RPC, exposing standardized tools, resources, and prompts. | 9 |
| **AI Gateway** | A core platform infrastructure component centralizing model routing, API key management, quota allocations, rate limiting, semantic caching, and audit logging. | 3 |
| **Instruction Corpus** | The version-controlled repository of Markdown specification files governing agent behavior. Managed with the same rigor as source code: reviewed, tested, and audited. | 10 |
| **Dependency Rule (in Context)** | The architectural principle dictating that instructions must depend inward toward stable abstractions rather than volatile details, mirroring Clean Architecture. | 10 |
| **Deterministic Verifier** | A non-probabilistic gate (unit test, schema validator, linter) verifying agent output. The second line of defense complementing prompt context. | 6 |
| **Eval** | An automated, reproducible benchmark measuring probabilistic behavior against verifiable rubrics; replaces binary unit tests where outcomes are non-deterministic. | 2, 4 |
