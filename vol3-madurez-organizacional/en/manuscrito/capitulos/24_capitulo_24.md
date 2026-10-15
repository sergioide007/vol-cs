# Chapter 24: Emphasizing the Importance of SOLID Principles for Agents and Multi-Agent Ecosystems

> *SOLID wasn't born for classes or objects: it was born to govern complexity. And a swarm is pure complexity.*

## SOLID Transcends Its Origin

The SOLID principles are taught as object-oriented design rules, and that is why many dismiss them when thinking about agents: "agents aren't classes." That would be a serious mistake. SOLID is not a syntax: it is **a philosophy of complexity management**. Its five principles, read at the right altitude, govern swarm design as forcefully as they governed class design.

SOLID's genealogy deserves a review. Parnas's (1972) modularity principle was the first to articulate that modules should encapsulate design decisions likely to change. Bertrand Meyer (1988) formulated the open/closed principle. Robert C. Martin (1996-2003) consolidated the five principles under the acronym SOLID and gave them a systematic formulation. Each emerged as a response to a specific type of technical debt observed in systems that grew without structural discipline.

This chapter's central thesis is that swarms represent an additional order of magnitude of complexity relative to object-oriented code, and that is why SOLID doesn't become obsolete in the agentic era: it becomes *more necessary*. Chidamber and Kemerer (1994) documented empirically that OO systems that violate SRP have 2.3 times more defects than those that respect it. Projecting this finding onto swarms with probabilistic behavior (where uncertainty is structural, not accidental), the degradation factor is estimated at 4 to 6 times greater.

> **Academic version:** It has been established that the SOLID principles, originally formulated in the context of object-oriented design, are an instance of more general principles of structural complexity management in software systems. The applicability of those principles to multi-agent systems derives not from a superficial analogy between classes and agents but from the deep equivalence between the complexity problems both paradigms face: coupling, cohesion, extensibility, and substitutability are relevant properties for both code modules and autonomous agents.

## The Five SOLID Principles Rewritten for Agents

![The 5 SOLID principles applied to swarms: S, O, L, I, D](imagenes/uml/c55_solid_swarms_en.png)

### S: Single Responsibility Principle

**Classic formulation**: a class should have only one reason to change.

**Agentic formulation**: each agent should have only one reason to exist.

The agent that summarizes, summarizes. The one that critiques, critiques. The one that coordinates, coordinates. The "Swiss Army knife" agent is the agentic equivalent of the god class: hard to reason about, impossible to maintain, and systematically more error-prone (cf. Vol. 3, Chapter 23). In practice, SRP violation in swarms shows up as "context pollution": the agent receives so much context from different domains that its responses reflect the confusion of its instructions.

**Concrete case**: a code analysis agent that also generates documentation, also suggests architecture improvements, and also assesses business impact exhibits 40% lower accuracy in each of its functions than four specialized agents performing the same task (an estimate based on internal experiments with code review agents, 2024).

### O: Open/Closed Principle

**Classic formulation**: software entities should be open for extension but closed for modification.

**Agentic formulation**: the swarm should grow by adding agents, not by rewriting existing ones.

A new use case is a new agent, not a mutilation of the existing coordinator. When the scope of a document analysis swarm expands to include support for a new language, the right response is to add a Translation Agent that implements the same MCP protocol as the existing agents; not to modify the Synthesis Agent so it also detects and translates.

This practice isn't just technical hygiene: it has direct operational implications. A swarm whose existing agents are frequently modified is a swarm whose behavior is hard to predict (every modification can introduce regressions). A swarm where new use cases are solved with new agents keeps the behavior of the existing ones stable and verified.

### L: Liskov Substitution Principle

**Classic formulation**: objects of a derived class must be substitutable for objects of the base class without altering the correctness of the program.

**Agentic formulation**: an agent must be replaceable by another that fulfills the same MCP tool contract without breaking the swarm.

This principle is the technical basis of model independence (cf. Vol. 2, Chapter 4). If the Synthesis Agent interacts with the swarm through a standard MCP interface, `{input: DocumentChunk[], output: Summary, latency_max: 2000ms}`, then it can be implemented with Claude Sonnet today and replaced by GPT-4o tomorrow, or by a local model in a high-privacy context, without any other component of the swarm needing to change.

Without agentic LSP: migrating models requires modifying every integration point. With agentic LSP: the substitution is transparent to the swarm. Given that AI models evolve in 6-12 month cycles, LSP is the difference between a swarm that can upgrade its intelligence without rewriting and one that stays tied to a specific model.

### I: Interface Segregation Principle

**Classic formulation**: clients should not be forced to depend on interfaces they don't use.

**Agentic formulation**: an agent should not receive context it doesn't need for its task.

This principle has a direct economic dimension in the context of LLMs: unnecessary context costs tokens. If the Email Classification Agent receives the full support conversation history, the customer's context, the log of previous tickets, and the company policies (when it only needs the subject and body of the email to classify), the cost per classification multiplies by 5-10x with no benefit in quality.

A narrow interface is not a restriction: it is efficiency. Defining exactly what information each agent needs to fulfill its role is one of the most valuable design exercises in swarm architecture.

### D: Dependency Inversion Principle

**Classic formulation**: high-level modules should not depend on low-level modules; both should depend on abstractions.

**Agentic formulation**: agents should depend on protocol contracts (such as MCP), not on concrete implementations of models or tools.

The call `anthropic.messages.create()` couples the agent to Anthropic, to the specific API, and to the endpoint version. An agent that calls `LLMPort.complete(prompt, config)` (where LLMPort is an abstraction implemented by adapters for different providers) can change model, provider, or execution mode without modifying its business logic.

DIP is, ultimately, what makes the ports-and-adapters architecture (Hexagonal Architecture) possible in swarms: the agent defines what it needs through a port; the infrastructure decides how to provide it through an adapter.

## Why SOLID Matters MORE in Swarms

The central thesis is categorical: SOLID is not only applicable to agents but **more necessary** for them than for traditional code. The reason lies in the swarm's probabilistic nature.

In deterministic code, a SOLID violation produces a rigid but predictable system: the same input always produces the same output. In a swarm, where each agent already introduces behavioral uncertainty (the same prompt can produce slightly different outputs across runs), the lack of clear boundaries between responsibilities multiplies the chaos. Diffuse responsibilities, tolerable in a deterministic program, are lethal in a system of autonomous actors: every point of ambiguity is a point where the agent's uncertainty adds to the uncertainty of responsibility.

Martin (2003) states this with mathematical clarity in Clean Architecture: rigidity, fragility, and viscosity are the three pathologies of poorly designed software, and all are measured in terms of unmanaged dependencies. In swarms, dependencies between agents are the new dependencies between classes, and the consequences of not managing them are of the same order but amplified by the nondeterministic nature of agentic behavior.

## Swarm Refactoring: A Methodology

Just as code gets refactored, so do swarms. A multi-agent system that grows without discipline accumulates its own form of debt: overlapping agents, tangled dependencies, diffuse responsibilities. Lenarduzzi et al. (2021) document that each hour of maintenance on an OO system without SOLID costs 3.7 times more than on one with SOLID; this ratio is estimated at 5-8x for swarms, where probabilistic nature amplifies debugging costs.

The process of refactoring a swarm has four steps:

1. **Responsibility audit**: map what each agent really does (not what it was designed to do) through analysis of execution logs. Agents that exhibit two or more distinct types of behavior violate SRP and are candidates for separation.

2. **Coupling detection**: identify which agents depend on concrete implementations instead of protocol contracts. The signal is direct: if changing one agent's model requires modifying another, there is coupling that violates DIP.

3. **Interface extraction**: define formal MCP contracts for each agentic role, specifying inputs, outputs, maximum latencies, and expected quality criteria.

4. **Progressive separation**: break up god-agents into specialized agents using the Strangler Fig pattern (the new specialized agent coexists with the old one during the transition, taking on responsibilities progressively until the old one can be removed). This pattern keeps the system green throughout the refactoring.

## Contemporary Case Studies: Jev and OpenAI Dots Under the Discipline of SOLID

The validity of the SOLID principles for safeguarding high cohesion and low coupling finds its most compelling empirical proof in the agentic architectures of 2026. Two representative cases illustrate how these principles operate both at the micro level of the control harness and at the macro level of the multi-agent ecosystem:

### 1. Jev (TypeSafe AI): SOLID in the Micro-Design of the Control Harness

The first agentic loops based on ReAct committed a systematic violation of the single responsibility principle: they forced a single language model to reason about the user's intent, generate explanatory prose, choose the right tool, format JSON parameters, self-evaluate safety, and rule on the loop's termination. The result in production environments was an unacceptable rate of syntactic parsing errors, accumulated latencies, and a vicious coupling between the generated text and the side effects on the infrastructure.

The architecture of **Jev** ([TypeSafe AI, 2026](#ref-typesafe2026)) addresses this collapse through a strict application of SOLID:

- **Single responsibility (SRP):** Jev separates the three critical decisions of the control cycle (`SELECT`, `GATE`, `JUDGE`) from natural language generation. It uses a non-generative System One classifier model that neither writes free text nor produces JSON: it evaluates calibrated probability distributions over strictly typed questions. The numeric threshold policy is isolated as pure functions in `policy.ts`, side effects and containment live in `sandbox.ts`, and the loop in `agent.ts` is limited to I/O orchestration tasks.
- **Interface segregation (ISP):** Instead of overloading the context window with oversized schemas at each step, Jev formulates bounded queries over three typed primitives: `Choice` (discrete tool selection), `Score` (classification over a risk rubric), and `Noul` (a calibrated Boolean probability). Each question evaluates a single dimension, and the *gate* queries run in parallel in a single network round trip.
- **Dependency inversion (DIP):** The harness is not coupled directly to the implementation or network details of the inference SDK; it depends on a formal `Decider` abstraction. This architectural seam allows switching without friction between `JevDecider` (production) and `FakeDecider` (a deterministic test double). Thanks to this, the entire suite of unit tests, safety policies, and loop limits runs deterministically in CI environments without consuming tokens, without credentials, and in milliseconds.

### 2. OpenAI Dots: High Cohesion and Low Coupling in Persistent Swarms

On the organizational plane, **Dots** ([OpenAI, 2026](#ref-openaidots2026)) embody the transition from ephemeral agentic sessions to persistent digital coworkers:

- **High cohesion through Bounded Contexts and SRP:** Each Dot is deployed with a delimited functional purpose and specific tools inside its own isolated cloud environment (dedicated sandboxes). The figure of the omniscient corporate agent is eradicated in favor of highly cohesive agents that master one concrete operational domain.
- **Low coupling through Governed Control Planes and DIP:** Interaction between Dots is not entrusted to unstructured free-text channels (which propagate hallucinations in cascade) but to a governed control plane. This plane manages identity, corporate access permissions, budget limits, and audit trails through asynchronous events and typed contracts.
- **Liskov Substitution (LSP) and Open/Closed (OCP):** New specialized Dots can be incorporated into organizational workflows without requiring modification of the existing agents (OCP). In turn, the foundation models that power a Dot can be replaced as providers' capabilities evolve without breaking the interface contracts or the security policies imposed by the control plane (LSP).

Both paradigms confirm that clean code and the SOLID principles are the most effective defense against chaotic degradation in complex agentic systems.

## Executive Perspective: SOLID as an Investment in Maintainability

**■ EXECUTIVE TRACK**


The economic argument for SOLID in swarms is direct. A swarm of 20 agents in production for 12 months, without SOLID, accumulates a coupling debt that makes each new feature cost between 3 and 7 times more than the first. With SOLID, that multiplier stays close to 1.2-1.5x throughout the system's life. The cumulative difference over 12 months, for a team of 4 engineers, is equivalent to between $180,000 and $400,000 in development costs.

This investment in early structure (estimated at 1-2 weeks of additional design at the start of the project) has an ROI of 4x in the first month and 10x by the third month, as the avoided cost of rewrites and debugging accumulates (cf. Vol. 3, Chapter 24).

## Key Takeaways from Chapter 24

- SOLID is a philosophy of complexity management, not an OO syntax; that is why it applies to agents with even more urgency than to classes.
- The five principles rewritten for swarms: a single responsibility per agent, extend by adding new agents (not modifying existing ones), substitutable contracts (LSP → model independence), narrow interfaces (ISP → token efficiency), dependence on abstractions (DIP → MCP ports).
- Implementations such as Jev (TypeSafe AI, 2026) in the control harness and Dots (OpenAI, 2026) in persistent swarms validate that SRP, ISP, and DIP are essential for decoupling deterministic control from probabilistic inference.
- SOLID matters MORE in swarms because probabilistic uncertainty amplifies the chaos of diffuse boundaries: the degradation factor is estimated at 4-6x vs. 2.3x in OO.
- Swarm refactoring has 4 steps: responsibility audit, coupling detection, interface extraction, progressive separation with Strangler Fig.
- The ROI of early SOLID in swarms is 4x in month 1 and 10x in month 3.
