# Chapter 10: Context Architecture

## The Instruction Corpus Is Code

The preceding chapters of this volume engineered the discrete subsystems of an agentic architecture: the autonomous agent (Chapter 4), specialized domain roles (Chapter 5), domain boundaries (Chapter 6), executable skills (Chapter 7), multi-agent orchestration (Chapter 8), and typed tools (Chapter 9). What remains is the single component that few teams deliberately architect, yet which ultimately governs everything else: the **instruction corpus** that engineering provides to foundation models so they comprehend *what* the system does and *how* to execute within it. Today, that corpus goes by a thousand names and zero architecture (`CLAUDE.md`, `AGENTS.md`, `ADR.md`, `spec.md`, `.cursorrules`, `copilot-instructions.md`, and dozens of disparate README files) scattered across nested folders or dumped into repository roots, growing unchecked by accretion.

Chapter 4 established the foundational thesis that now reaches its broadest operational conclusion: agentic artifacts are *structured text evaluated by a fallible interpreter*, which is what software source code has always been. If an instruction corpus is text executed by a runtime interpreter, then **the instruction corpus is source code**, and demands the identical architectural discipline applied to any mission-critical codebase. Today, it lacks that discipline. What begins in an early prototype as a clean, readable 50-line file metastasizes, as teams scale, into a 4,000-line monolithic markdown document where no one knows whether the AI was already instructed to avoid a specific defect, whether that rule remains active, or whether it directly contradicts a directive committed three months earlier by an engineer who has since resigned. Incoming developers and autonomous agents alike inherit the most insidious category of technical debt: invisible debt that detonates only upon contact.

And here lies the insight that elevates this from an organizational nuisance to a quantifiable engineering defect: **a monolithic context document does not merely fatigue human engineers; it actively degrades foundation model accuracy**. The empirical mechanics mirror those detailed in Chapter 4: model recall and instruction-following degrade sharply when relevant directives are buried within the middle of extended context windows—the well-documented U-shaped attention curve [Liu et al., 2024](#ref-liu2024). A 5,000-line markdown prompt is, literally, burying signal in noise. A critical invariant that a model strictly adheres to when presented in a 50-line file is ignored in a 5,000-line document—not out of behavioral defiance, but due to the physical limits of attention mechanisms. Also, an inflated instruction corpus is the **primary driver of enterprise Token-Burn** (quantified in Volume 4, Chapter 1): if every inference call blindly drags the entire corporate rulebook along as raw context, you pay for the full prefix on every single turn. Structuring the context corpus to load strictly the relevant domain context is not aesthetic hygiene: it simultaneously resolves an acute quality defect and an escalating financial burn.

## The Dependency Rule Applied to Markdown Files

The architectural solution does not require inventing novel abstractions: it has been codified for decades. Parnas (1972) demonstrated that systems must be decomposed into modules that encapsulate design decisions subject to change; Evans (2003) grounded those modules in business domain boundaries via *Bounded Contexts*; Martin (2017) structured them via a universal Dependency Rule pointing strictly inward; and Conway (1968) proved that software architectures inevitably mirror team communication structures. **Context Architecture** is nothing more than applying these four foundational software engineering principles to the instruction corpus rather than the application source code.

In production, this translates into three decoupled layers:

- **The Core (Transversal Invariants).** Global system invariants that rarely mutate: ubiquitous language definitions, non-negotiable security guardrails (Volume 4, Chapter 4), formatting conventions, and irreversible action policies. It is compact, permanent, and read in full. It occupies the innermost architectural ring: no domain modifies it; all domains inherit it.
- **The Domains (Bounded Contexts).** A dedicated directory per business domain (`billing/`, `inventory/`, `identity/`), housing exclusively the business rules, functional specifications, and Architectural Decision Records (ADRs) pertaining to *that specific domain*. Knowledge is encapsulated strictly where it belongs [Parnas, 1972](#ref-parnas1972): an agent refactoring billing logic never loads or parses inventory rules. The directory boundary is the domain boundary.
- **The Manifest (The Gateway).** A single lightweight index in the root that contains zero rules, but rather the architectural map: which domains exist, which files govern them, and which team owns each boundary. In the knowledge layer, this represents the direct counterpart to the AI Gateway in Chapter 3: an ingress point that routes context. An agent arriving to implement a feature first reads the manifest, discovers the target domain, and pages in *exclusively* that domain context.

```
context/
├── MANIFEST.md            # The Gateway: Domain index and ownership map. Contains ZERO rules.
├── core/                  # Innermost ring: Transversal, permanent invariants
│   ├── ubiquitous-language.md
│   ├── security.md        # Non-negotiable security invariants (Vol. 4, Ch. 4)
│   └── style-guide.md
├── billing/               # Bounded Context (Ch. 6)
│   ├── rules.md           # Business invariants
│   ├── spec.md            # What the domain computes, not how
│   └── decisions/         # Local Architecture Decision Records (ADRs)
│       └── 2026-03-pricing-tiers.md
├── inventory/
│   └── rules.md
└── master-prompts/        # Reusable enterprise business workflows (Ch. 5 & 7)
    ├── customer-onboarding.md
    └── monthly-reconciliation.md
```

The Dependency Rule is enforced strictly: domains depend on the core; the core never depends on domains. Domains never import cross-domain contexts directly (if two domains require a shared invariant, that rule is promoted to the core, never spied upon across domain boundaries). And the manifest, like any robust gateway, knows zero internal domain rules: it knows strictly where they reside. Anyone who mastered Chapter 6 will recognize that this is Domain-Driven Design applied one level higher: to the instruction sets that generate the software.

## Guardian Agents and Master Prompts

The directory structure represents half the architecture; the other half is operational maintenance and runtime execution. Here, the volume completes its conceptual circle.

**A Domain Guardian Agent per Bounded Context.** Every Bounded Context is paired with a specialized review skill (Chapter 7) whose sole mandate is preserving the structural integrity of *its* directory: detecting duplicated, contradictory, or obsolete rules, and blocking in code review any pull request that breaches core invariants. This represents the Council pattern from Chapter 8 deployed in service of knowledge architecture: the billing guardian never reviews inventory rules, and therefore reviews billing rules with deep domain expertise. When an engineer or agent modifies domain rules via pull request (because the instruction corpus is versioned and code-reviewed like software, never hand-edited directly in production), the domain guardian serves as the mandatory first reviewer.

**A Gateway Orchestrator.** At the manifest layer resides a lightweight hierarchical orchestrator (Chapter 8) that navigates the repository index. It maintains zero internal knowledge of domain business logic; it reads the manifest map. When ingesting a business request ("implement enterprise volume discounts"), it parses the manifest, identifies that the task touches `billing/`, delegates execution to the billing guardian, and loads exclusively that bounded context into the prompt. The orchestrator is to domain knowledge what the AI Gateway (Chapter 3) is to foundation model providers: it routes to the optimal handler without needing to execute the work itself.

**The Master Prompts Directory.** Recurring enterprise business workflows are never improvised ad-hoc within chat interfaces: they reside versioned within `master-prompts/`, each structured as the canonical template defined in Chapter 5 (one unified structure, multiple parameterized instances). Invocations like "customer onboarding" or "monthly ledger reconciliation" cease to be prompt-engineering experiments and become hardened software assets: maintained by explicit owners, tracked across Git commit histories, and evaluated against continuous eval suites (Volume 4, Chapter 3) to assert that behavior remains invariant across model upgrades.

## Case Study: Halting the 4,000-Line Monolithic Onboarding Prompt

*(Composite reference scenario, modeled after recurring enterprise adoption engagements.)*

**Baseline State.** Over eighteen months of organic development, a platform engineering team accumulated a `CLAUDE.md` file spanning nearly 4,000 lines: unorganized rules across six disparate domains, obsolete architectural decisions, three mutually contradictory naming conventions, and lingering instructions referencing decommissioned microservices. Every incoming developer—and every autonomous agent session—loaded the entire file. The symptoms mirrored Chapter 4 and Volume 4, Chapter 1: unit cost per completed iteration climbed steadily while code quality stalled, and agents routinely hallucinated or forgot directives buried around line 2,700.

**The Architectural Refactoring.** The team touched zero lines of product application code; they refactored the instruction corpus according to Context Architecture. Transversal invariants were promoted to `core/`; each business subsystem was isolated into its own domain directory; obsolete decisions were archived with deprecation timestamps rather than deleted (the Boy Scout rule from Chapter 4, applied to documentation); and a 30-line manifest replaced the 4,000-line monolith. Measured across internal telemetry: agent onboarding transformed from "ingest everything and hope for attention" to "page in strictly the target feature domain"; average prompt token volume dropped from thousands to hundreds of lines, yielding direct token savings (Volume 4, Chapter 1); and answering "was the agent already told to catch this bug?" shifted from half an hour of prompt archaeology to a simple directory grep.

## Boundary Conditions and Operational Best Practices

Engineering integrity requires acknowledging the inverse: **Context Architecture is not free, and is not universally required.** For small greenfield repositories or early prototypes, a single, clean markdown file is superior: imposing formal bounded contexts on a codebase that fits comfortably within a single developer's head represents the exact over-engineering warned against in Chapter 4—premature abstraction is the evil twin of the god class. The pattern is justified when the instruction corpus exceeds a single sitting's cognitive capacity, when multiple teams contribute concurrently, or when context token bloat begins driving material cloud invoices. Three cardinal best practices govern adoption:

- **The Manifest Never Houses Business Rules; It Houses the Map.** The moment an index accumulates domain logic, it ceases to be a gateway and degrades into a second monolith. If the manifest expands, a bounded context is missing.
- **One Rule, One Owner, One Canonical Location.** The only thing worse than a buried rule is the identical rule duplicated across two domain files with subtly diverging text. Maintain a single source of truth (DRY, Chapter 4); promote shared invariants to the core.
- **The Corpus Is Version-Controlled and Code-Reviewed as Source.** Committing prompt modifications without peer review is pushing unreviewed code directly to production (Chapter 4); the domain guardian agent is its first reviewer, and regression eval suites (Volume 4, Chapter 3) serve as its continuous integration tests.

Throughout this volume, the underlying principles endure while tooling identifiers fluctuate: whether files are named `CLAUDE.md`, `AGENTS.md`, or future formats, the fundamental thesis that instruction sets are software architecture—governed by bounded contexts, explicit ownership, and inward dependency rules—will outlive them all.

## Agent State Memory: The Observable Runtime Lifecycle

Context Architecture reaches completion when the autonomous agent itself becomes fully observable. Throughout its execution, an agent traverses discrete lifecycle states (Idle, Processing, Awaiting Tool, Completed): every state transition represents a structured telemetry event that engineering teams must monitor, test, and govern. Runtime observability is not a luxury; it is the prerequisite of systems engineering: you cannot optimize or secure what you cannot observe.

> **Design Justification: State Diagrams for Dynamic Behavioral Modeling**
>
> An agent's execution lifecycle is a temporal process: initialized in an idle state, activated by an event, suspended while awaiting external tool execution, and terminating in success or failure. A state machine diagram captures that *temporal dynamics*: explicit transitions, triggering events, and deterministic intercept points for observability or intervention.
>
> A class diagram models static components; a sequence diagram captures point-to-point interactions. Here, systems design demands *runtime lifecycle transitions*—the operational dimension essential for distributed tracing, latency optimization, and failure diagnostics.
>
> State diagrams reappear in **Volume 4, Chapter 7** (modeling an agent awaiting streaming CDC log events), where asynchronous state transitions again represent the core architectural focus.

![Diagram 10.1: Agent Lifecycle: State Machine with Observable Transitions](imagenes/uml/diagrama10_estado_en.png)

Every lifecycle transition maps to automated instrumentation:
- **Idle → Active:** The agent ingests an incoming task prompt. Records initialization timestamp and baseline invocation budget.
- **Active → ToolCall:** The foundation model requests tool execution. Captures tool identifier and schema arguments.
- **ToolCall → Awaiting:** The tool execution payload is dispatched to the runtime. Initiates latency stopwatches.
- **Awaiting → Active:** Tool execution payload returns. Records tool latency and appends return data to the working memory trajectory.
- **Active → Completed:** The model emits a final natural language answer without requesting tools. Terminates the cycle and logs gross token spend.
- **Active/Awaiting → Error:** A domain invariant is breached, or an execution timeout fires. Critical for diagnosing distributed failure modes.

Production observability platforms (Volume 4, Chapter 8) aggregate these discrete transitions into distributed traces. Continuous eval suites (Volume 4, Chapter 3) assert that agents do not stagnate within intermediate states (e.g., lingering in `Awaiting` for $> N$ seconds exposes slow third-party microservices or deadlocked processes). The AI Gateway (Chapter 3) uses these state transitions to enforce governance policies: routing fatal error states to human operators while logging successful executions to audit ledgers.

## Chapter 10 Takeaways

- The instruction corpus (the markdown files an agent reads to comprehend rules and procedures) is source code: structured text parsed by a fallible interpreter, demanding software architecture.
- Monolithic context files degrade foundation model attention (the *lost in the middle* phenomenon; [Liu et al., 2024](#ref-liu2024)) and represent the primary driver of runaway Token-Burn (Volume 4, Chapter 1). It is a measurable defect, not aesthetic disorganization.
- Context Architecture applies established systems principles to instruction sets: Information Hiding [Parnas, 1972](#ref-parnas1972), Bounded Contexts ([Evans, 2003](#ref-evans2003)), the Dependency Rule [Martin, 2017](#ref-martin2017), and Conway's Law (1968). Structured across three layers: Core, Bounded Domains, and the Manifest Gateway.
- Deploy a domain guardian agent per bounded context (Chapter 7), a gateway orchestrator routing via the manifest (Chapters 3 & 8), and versioned `master-prompts/` representing parameterized business workflows (Chapter 5).
- Avoid premature abstraction: for lean prototypes, a single clean file is superior. Context Architecture is warranted when the corpus exceeds a single reading, multiple teams contribute concurrently, or context token bloat begins impacting cloud infrastructure invoices.

---
