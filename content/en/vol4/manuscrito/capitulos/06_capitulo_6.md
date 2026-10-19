# Chapter 6: Clean Architecture for Agentic Systems

## The Model Is a Detail

*Clean Architecture* organizes software into concentric rings (entities, use cases, interface adapters, frameworks) governed by a single rule: **dependencies point inward**; nothing in an inner ring knows the outer rings exist ([Martin, 2017](#ref-martin2017)). Its most quoted phrase is also the most misunderstood: "the database is a detail." It doesn't mean the database doesn't matter; it means the business rules must not depend on it.

The translation to the agentic era is immediate and, for many teams, uncomfortable: **the language model is a detail**. The provider, the model identifier, the SDK: all of that lives in the outer ring, next to the database and the web framework. What lives inside is the *policy*: what reviewing code means in your organization, which domain invariants aren't negotiable (Chapter 6), which contract each role fulfills (Chapter 5). A well-designed agentic system can switch providers in an afternoon because no use case imports `anthropic` or `openai`: it imports a **port**.

> **Design Justification: Class Diagram for Structural Modeling**
>
> Clean Architecture is a *dependency structure*: which classes inhabit each ring, what the hierarchy is (entities → use cases → adapters), what the flow of the dependency rule is. A class diagram with its concentric rings reveals exactly that: the static topology where objects live and how they relate.
>
> A component diagram would show where services live on the server; a sequence diagram would show an executed flow. Here we need to see *the structure of layers and dependencies*, the skeleton that never changes at runtime.
>
> The class diagram reappears in this book in **Chapter 5** (The Synthetic Enterprise), in **Chapter 6** (DDD and aggregates), where we again use classes to show structural relationships that govern the system.

![Diagram 6.1: Clean Architecture (class diagram with concentric rings)](imagenes/capitulo15/diagrama15_1_en.png)

Note what ended up in the center: the master prompts and the domain contexts are **business rules expressed in prose**: they belong to the core, are versioned with it, and don't know which model will execute them. The attentive reader will recognize that the AIGateway from Chapter 3 was already this idea in miniature: a port with three adapters. This chapter formalizes it.

**► TECHNICAL TRACK: The LLM Port in Java**

```java
// Example 6.1 (Java 17+, Spring Boot): the port and its use case.
// The core defines WHAT it needs; the outer ring decides HOW.

// ── Inner ring: the port (knows no provider) ──
public interface LlmPort {
    LlmResult complete(String system, String user, TaskTier tier);
}

public enum TaskTier { FAST, BALANCED, QUALITY }

public record LlmResult(String text, int inputTokens,
                        int outputTokens, String modelUsed) {}

// ── Use case: pure policy, testable without a network ──
@Service
public class ReviewCodeUseCase {

    private final LlmPort llm;                 // port injection
    private final DomainContext context;       // Chapter 6
    private final CostLedger costs;            // Chapter 11

    public ReviewCodeUseCase(LlmPort llm, DomainContext context,
                             CostLedger costs) {
        this.llm = llm;
        this.context = context;
        this.costs = costs;
    }

    public Review execute(String diff) {
        var result = llm.complete(
            context.masterPrompt("reviewer"),       // Chapter 5
            "Review this diff:\n" + diff,
            TaskTier.BALANCED                        // policy, not model
        );
        costs.record("code-review", result);
        return Review.fromJson(result.text());      // verifiable contract
    }
}

// ── Outer ring: the adapter (the only thing that knows the SDK) ──
@Component
public class AnthropicAdapter implements LlmPort {

    private final AnthropicClient client = AnthropicOkHttpClient.fromEnv();
    private final ModelRegistry registry;   // tier -> model id, in config

    public AnthropicAdapter(ModelRegistry registry) {
        this.registry = registry;
    }

    @Override
    public LlmResult complete(String system, String user, TaskTier tier) {
        var params = MessageCreateParams.builder()
                .model(registry.modelFor(tier))   // never hard-wired
                .maxTokens(4096L)
                .systemOfTextBlockParams(java.util.List.of(
                        TextBlockParam.builder().text(system).build()))
                .addUserMessage(user)
                .build();
        var response = client.messages().create(params);
        var text = response.content().stream()
                .flatMap(b -> b.text().stream())
                .map(t -> t.text())
                .reduce("", String::concat);
        return new LlmResult(text,
                (int) response.usage().inputTokens(),
                (int) response.usage().outputTokens(),
                response.model().toString());
    }
}
```

This structure pays three dividends, and all of them are the usual ones ([Martin, 2017](#ref-martin2017)). **Testability:** the use case is tested with a fake `LlmPort` that returns fixed responses, with no network, no cost, in milliseconds; the evals (Chapter 13) test the real adapter, each layer with its own instrument. **Provider independence:** the decision to route `QUALITY` to one provider and `FAST` to another lives in configuration, and the comparison between providers (Chapter 3) becomes a one-line experiment. **Readable policy:** an auditor (human or regulatory; Chapter 1 (Vol. 3)) reads the use case and sees the business rule without digging through SDK details.

Likewise, the Node.js/TypeScript version of the same port, for readers of the other ecosystem:

```typescript
// Example 6.2 (TypeScript / Node 20+): same port, another language.
import Anthropic from "@anthropic-ai/sdk";

export type TaskTier = "fast" | "balanced" | "quality";

export interface LlmResult {
  text: string;
  inputTokens: number;
  outputTokens: number;
  modelUsed: string;
}

export interface LlmPort {
  complete(system: string, user: string, tier: TaskTier): Promise<LlmResult>;
}

export class AnthropicAdapter implements LlmPort {
  private client = new Anthropic(); // ANTHROPIC_API_KEY from the environment
  constructor(private registry: Record<TaskTier, string>) {}

  async complete(system: string, user: string,
                 tier: TaskTier): Promise<LlmResult> {
    const r = await this.client.messages.create({
      model: this.registry[tier],
      max_tokens: 4096,
      system,
      messages: [{ role: "user", content: user }],
    });
    const text = r.content
      .filter((b): b is Anthropic.TextBlock => b.type === "text")
      .map((b) => b.text).join("");
    return { text, inputTokens: r.usage.input_tokens,
             outputTokens: r.usage.output_tokens, modelUsed: r.model };
  }
}
```

## Advanced Technical Rigor: Value Objects and the Complete Hexagonal Pattern

The code above hides a design decision that separates production agentic systems from prototypes. Note that instead of passing loose primitive parameters (`system: String, user: String, tier: TaskTier`), the production version packages the request into a **value object** (`InferenceRequest`). The difference looks trivial in a single call; at the scale of a hundred agents interacting over years, it is the difference between a maintainable system and a graveyard of technical debt.

The complete hexagonal architecture, elevated to the rigor of Domain-Driven Design ([Evans, 2003](#ref-evans2003)), organizes the system into three concentric layers, each with a single responsibility and a set of types that characterize it:

![Diagram 6.2: Hexagonal Architecture with DDD: Domain Core, Application and Infrastructure Layers (advanced architecture class diagram)](imagenes/capitulo16/diagrama6_ddd_en.png)

The architectural decisions the diagram encodes explain why each component deserves to be there:

**Grouping into the hexagon's layers.** The central package (`Domain Core`) contains port interfaces, value types, and enumerations: the contract no external detail negotiates. The middle package (`Application Layer`) has use cases that choreograph the business flow, injecting the port into their constructor. The outer package (`Infrastructure`) implements the adapters that talk to the external SDKs. The dependency rule, once more: **dependencies always point inward; the core doesn't know the infrastructure**. This isn't cosmetic; it is the foundation of network-free testability, provider independence, and auditability (Chapter 1 (Vol. 3)).

**Encapsulation through Value Objects.** A value object (Value Object in DDD) is an object with no unique identity that encapsulates a domain concept. `InferenceRequest` has no database ID; what defines it is its structure (`systemPrompt`, `userPrompt`, `tier`). The dividend: future configurations (model temperature, token limit, seed for reproducibility) are added to `InferenceRequest` without the port changing its signature. The port's methods stay the same; the interface is stable. In systems without Value Objects, every new need demands a new function signature, a new adapter, new tests. With them, the contract is immutable from the outside.

**Eradicating primitive obsession.** In the AI agent domain, tokens aren't just any `int`: they are money, they are quota, they are governance. The specialized class `TokenUsage` encapsulates that semantics: it doesn't just store the number, it can compute the estimated cost (`calculateEstimatedCost()`), validate that it doesn't exceed the budget, and raise alert events. An auditor or an engineer reading `result.usage().calculateEstimatedCost()` understands immediately they are touching a critical concept. An auditor reading `result.outputTokens * 0.00003` (a magic multiplication) has to dig.

**Weak coupling through dashed arrows.** The dashed arrows (`..>`) in the diagram indicate temporary usage dependencies: instantiation, reading, method invocation. The solid arrows (`-->`) indicate structural composition: properties that live inside an object. The pattern is: `ReviewCodeUseCase` depends continuously on `LlmPort` (composition: it owns it as a field) but depends discontinuously on `InferenceRequest` (it builds it and passes it, but doesn't own it). That distinction lets you change how requests are built without the use case changing.

![Diagram 6.3: Runtime object graph, in-memory instances of the use case, the context, and the cost ledger operating together](imagenes/capitulo16/objeto_runtime_ddd_en.png)

Diagram 6.3 completes the picture: what the objects look like **in the server's memory at runtime**. The instantiated `ReviewCodeUseCase` holds references to three services (the port, the context, the cost ledger). Each object, in turn, maintains its state: `AgentDomainContext` knows the repository it is working in; `AgentExecutionSession` tracks which step of the task the agent is on and how many tokens it has consumed so far. It is the in-memory skeleton that explains how economic and technical transactions are governed during a real execution. Without that diagram, the code is a series of magic injections; with it, the topology is clear.

**► TECHNICAL TRACK: The Value Object Pattern in Java, Step by Step**

```java
// In the domain core: value types with no database counterpart
public record TokenUsage(
    int inputTokens,
    int outputTokens
) {
    // Invariant: both must be non-negative
    public TokenUsage {
        if (inputTokens < 0 || outputTokens < 0)
            throw new IllegalArgumentException("Negative tokens are not valid");
    }

    // The business logic lives inside the Value Object
    public BigDecimal calculateEstimatedCost(
            BigDecimal inputPrice,   // $0.003 per 1K input tokens
            BigDecimal outputPrice) {  // $0.015 per 1K output tokens
        return inputPrice.multiply(
            BigDecimal.valueOf(inputTokens).divide(
                BigDecimal.valueOf(1000)))
        .add(outputPrice.multiply(
            BigDecimal.valueOf(outputTokens).divide(
                BigDecimal.valueOf(1000))));
    }
}

public record InferenceRequest(
    Prompt systemPrompt,
    Prompt userPrompt,
    TaskTier tier
) {
    // Validating constructor (Java 16+)
    public InferenceRequest {
        Objects.requireNonNull(systemPrompt, "System prompt cannot be null");
        Objects.requireNonNull(userPrompt, "User prompt cannot be null");
        Objects.requireNonNull(tier, "Tier cannot be null");
    }
}

public record InferenceResponse(
    String generatedText,
    TokenUsage usage,
    String modelIdentifier
) {}

// In the application layer: the use case that orchestrates with the Value Objects
@Service
public class ReviewCodeUseCase {
    private final LlmPort aiEngine;
    private final CostLedger costLedger;

    public ReviewReport execute(String diff) {
        // Explicit construction of the request: the contract is visible
        var request = new InferenceRequest(
            Prompt.from("context/reviewer-master.txt"),
            Prompt.from("diff:\n" + diff),
            TaskTier.BALANCED
        );

        var response = aiEngine.generateCompletion(request);

        // The cost is computed with domain semantics, not with loose numbers
        BigDecimal cost = response.usage()
            .calculateEstimatedCost(
                BigDecimal.valueOf(0.003),  // input price
                BigDecimal.valueOf(0.015)   // output price
            );

        costLedger.record("code-review", cost, response.modelIdentifier());

        return ReviewReport.fromJson(response.generatedText());
    }
}
```

The payoff of this structure shows in maintenance time. When the provider changes its price (it happens every quarter), only `calculateEstimatedCost()` in `TokenUsage` is modified: one method, one place. When the business policy decides to limit consumption per agent, the validation is added to `TokenUsage` in the constructor: the domain invariant protects all instances, automatically. When a compliance auditor must verify that every LLM call records its cost, a type audit (`grep "costLedger.record"`) is enough: the flow is explicit.

## Case Study: The Java → Node Migration as a Test of the Architecture

*(A first-person account of a real case the author led at a large-scale payment processor; for confidentiality, the names of the organization and its clients are omitted.)*

One of the migrations I remember best was the most tangled, not the largest. It was thousands of lines of legacy Java, touched by team after team over the years: "touch me and I fall apart" code (or worse, "better not touch me at all"). And it was no toy: it was a large-scale payment processor, where an hour of downtime is counted in millions of failed transactions, operational chaos, and the reputation of the entire organization; many millions of dollars depended on my not making a mistake.

And yet no immensity beats good analysis and a design with good practices. I had already read Robert C. Martin, Martin Fowler, and the Gang of Four with their twenty-three patterns, and I had them so deep inside me that I told myself: if this is true, I apply it and it works. I applied it. And it worked.

I didn't translate the tangle: I untangled it first. And a single pattern wasn't enough (one is rarely enough): I combined three. With Chain of Responsibility, Strategy, and Template Method I turned that thicket of nested `if`s into pieces with a single responsibility each. The result was an error rate of zero, while several neighboring migrations ended in rollback. Until then, nobody vouched that it could be done this way.

I tell this because it holds the lesson of the whole chapter; the rest of this section generalizes it into a procedure anyone can repeat.

A team must migrate a Spring Boot backend to Node.js/TypeScript: REST controllers, services, authentication, WebSocket messaging, batch jobs. It decides to do it assisted by agents, and the first lesson arrives before the first prompt: **the quality of the migration is decided by the starting architecture, not by the model**. Where the original code had clean ports and use cases, the agent translates policy (interfaces, contracts, types) and the result compiles and passes the characterization tests on the first try in a dominant fraction of the modules. Where the business logic was entangled with the framework, the agent translates *the tangle*, faithfully, at industrial speed: technical debt with new syntax.

The procedure that worked, turned into a rule: first **analyze, understand, and take ownership** of the original code (what it does, what types it handles, what invariants it protects) and only then translate, verifying the type mapping between ecosystems at every boundary (the `BigDecimal` that becomes a floating-point `number` is the classic six-month silent bug). In this book's terms: the migration is a transformation skill (Chapter 7, pattern 3) whose "verify equivalence" step is the characterization tests, and clean architecture is what gives that skill boundaries to lean on. The case's executive conclusion inverts the usual question: before budgeting "migrate with AI," budget "clean up the boundaries so that AI can migrate."

## Worked Exercise 6.1: Spot the Dependency Rule Violations

**Problem.** This use case was written by an agent without architectural context. Point out the dependency rule violations and fix them.

```java
@Service
public class TriageTicketUseCase {
    public Triage execute(String ticket) {
        var client = AnthropicOkHttpClient.fromEnv();              // (1)
        var params = MessageCreateParams.builder()
                .model(Model.CLAUDE_SONNET_4_6)                    // (2)
                .maxTokens(1024L)
                .addUserMessage("Classify: " + ticket)             // (3)
                .build();
        var r = client.messages().create(params);
        kafkaTemplate.send("triage-done", r.toString());           // (4)
        return null;
    }
}
```

**Annotated solution.** (1) The use case builds the SDK client: the inner ring manufacturing a detail of the outer one; it is replaced by the injected `LlmPort` port. (2) The model identifier hard-wired into the policy: the core's right decision is a *tier* (`FAST`); the tier→model mapping lives in the outer ring's configuration. (3) The prompt improvised in a concatenation: the triage role has a versioned master prompt (Chapter 5) that belongs to the domain; the absence of an output contract also makes the result unverifiable. (4) The direct publication to Kafka: another detail of the outside inside the core; it is inverted with an `EventPublisherPort` port, which is, precisely, the bridge to the next chapter. The corrected version has four lines of policy and zero infrastructure imports: that is the visual test of a clean use case.

## Key Takeaways from Chapter 6

- The dependency rule ([Martin, 2017](#ref-martin2017)) applied to agents: **the model is a detail**; provider and SDK live in the outer ring.
- Master prompts and domain contexts are business rules in prose: they belong to the core and are versioned with it.
- Port + adapters = network-free testability, provider independence, and readable policy.
- **Technical rigor with Value Objects ([Evans, 2003](#ref-evans2003)):** encapsulate domain concepts (tokens, costs, prompts) in types that express semantics, not just data. A `TokenUsage` that computes costs is better than an `int` that gets magically multiplied in some corner.
- Grouping into the hexagon's layers: the core (ports and interfaces) never depends on the infrastructure (adapters). That direction of dependency is the axis on which long-term maintainability turns.
- In agent-assisted migrations, the starting architecture decides the quality of the result: clean the boundaries before migrating.
- The visual test of a clean use case: zero infrastructure imports; Value Objects that validate their own invariants in the constructor.
- The runtime object graph reveals how the system makes economic and technical decisions during a real task; without it, governance is invisible.

---
