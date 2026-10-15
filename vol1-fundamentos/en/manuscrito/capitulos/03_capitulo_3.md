# Chapter 3: Platform Engineering in the Agentic Era

## The Platform as an Internal Product

*Platform engineering* is the software discipline that constructs paved roads for development teams across an enterprise. It is not raw infrastructure: it is the architectural abstraction layer that transforms complex distributed operations (deploying a containerized service, provisioning a database cluster, configuring end-to-end distributed tracing) into single-click workflows or declarative natural language commands.

The guiding operational framework is *Team Topologies* [Skelton & Pais, 2019](#ref-skeltonpais2019): organizational team structures must be engineered deliberately to minimize the extraneous cognitive load placed upon stream-aligned delivery teams. The platform team exists exclusively to absorb that cognitive load, managing the internal developer platform (IDP) as a true product—with explicit internal users, product roadmaps, and adoption telemetry.

In the agentic era, platform engineering acquires an urgent mandate: **exposing foundation model capabilities as first-class primitives of the internal platform**. If every product squad independently provisions proprietary API keys, selects disparate models, invents custom spend throttles, and implements isolated security policies, the enterprise accumulates as many systemic single points of failure—architectural, financial, and regulatory—as it has engineering teams.

**► TECHNICAL TRACK: Architecture of an Enterprise AI Platform**

> **Architectural Justification: Sequence Diagrams for Interaction Modeling**
>
> An AI Gateway is, above all, a temporal flow: an incoming inference payload arrives, traverses discrete processing layers (input sanitization, semantic routing, model execution, audit persistence), and completes with an incurred financial cost. What governs system health is the *chronological order* of these operations: what latency each layer adds, how much compute each consumes, and where invariant validation checks must fire prior to external egress.
>
> A component diagram merely illustrates where the gateway sits within a static network topology; a class diagram illustrates internal object composition. Here, system design demands the *temporal execution sequence*—the ordered chain of policy decisions and capital expenditures that dictate whether a request is executed or rejected.
>
> This sequence modeling reappears in **Volume 4, Chapter 7** (the Change Data Capture → Agent Worker → Downstream Consumers streaming pipeline), where asynchronous time decoupling again represents the core architectural invariant.

![Diagram 3.1: Internal AI Developer Platform (AI-IDP), Request Flow Through the Gateway](imagenes/capitulo03/diagrama3_1_en.png)

## The AI Gateway: The Most Mission-Critical Component

The AI Gateway serves as the centralized, unified ingress point for all foundation model interactions across the enterprise. Its non-negotiable operational responsibilities: task-complexity dynamic routing, team-level cost accounting, automated budget enforcement with deterministic cutoffs, tamper-evident audit logging, and automated cross-provider fallback logic.

```python
# Example 3.1: Minimum Viable AI Gateway
# Centralizes routing, cost tracking, and team-level budgets.
#
# PRICING NOTE: Rates reflect Anthropic public documentation at publication (2026).
# Model pricing and identifiers evolve; verify active schedules at
# https://platform.claude.com/docs before deploying to production. The PATTERN endures.

import time
from dataclasses import dataclass, field
from typing import Optional

import anthropic

@dataclass
class ModelConfig:
    model_id: str
    cost_per_million_input: float   # USD per 1M input tokens
    cost_per_million_output: float  # USD per 1M output tokens
    max_context_tokens: int
    latency_tier: str               # "fast" | "balanced" | "quality"

MODEL_REGISTRY = {
    "quality": ModelConfig(
        model_id="claude-opus-4-8",
        cost_per_million_input=5.00,
        cost_per_million_output=25.00,
        max_context_tokens=1_000_000,
        latency_tier="quality",
    ),
    "balanced": ModelConfig(
        model_id="claude-sonnet-4-6",
        cost_per_million_input=3.00,
        cost_per_million_output=15.00,
        max_context_tokens=1_000_000,
        latency_tier="balanced",
    ),
    "fast": ModelConfig(
        model_id="claude-haiku-4-5",
        cost_per_million_input=1.00,
        cost_per_million_output=5.00,
        max_context_tokens=200_000,
        latency_tier="fast",
    ),
}

class BudgetExceededError(Exception):
    pass

class AIGateway:
    """
    Centralized enterprise access gateway for foundation models.
    Enforces: routing, cost accounting, budget guardrails, and audit logging.
    """

    def __init__(self, team_id: str, budget_usd_monthly: float):
        self.client = anthropic.Anthropic()  # Reads ANTHROPIC_API_KEY from environment
        self.team_id = team_id
        self.budget_usd_monthly = budget_usd_monthly
        self.cost_this_month = 0.0
        self.request_log: list[dict] = []

    def _select_model(self, task_complexity: str,
                      force_model: Optional[str] = None) -> ModelConfig:
        """Automated model selection governed by declared task complexity."""
        if force_model:
            return MODEL_REGISTRY[force_model]
        # Complexity-based routing: simple tasks must not incur premium inference rates
        routing = {
            "simple": "fast",       # Classification, extraction, short summarization
            "moderate": "balanced", # Code generation, technical analysis, QA
            "complex": "quality",   # System architecture, multi-step deductive reasoning
        }
        return MODEL_REGISTRY[routing.get(task_complexity, "balanced")]

    def _calculate_cost(self, model: ModelConfig,
                        input_tokens: int, output_tokens: int) -> float:
        return (
            (input_tokens / 1_000_000) * model.cost_per_million_input
            + (output_tokens / 1_000_000) * model.cost_per_million_output
        )

    def complete(
        self,
        messages: list,
        system: str = "",
        task_complexity: str = "moderate",
        force_model: Optional[str] = None,
        max_tokens: int = 2048,
    ) -> dict:
        model_config = self._select_model(task_complexity, force_model)

        # Enforce budget guardrails BEFORE dispatching inference
        if self.cost_this_month >= self.budget_usd_monthly * 0.95:
            raise BudgetExceededError(
                f"Team {self.team_id}: 95% of monthly budget consumed. "
                f"Current spend: ${self.cost_this_month:.2f} / "
                f"${self.budget_usd_monthly:.2f}"
            )

        start_time = time.time()
        response = self.client.messages.create(
            model=model_config.model_id,
            max_tokens=max_tokens,
            system=system,
            messages=messages,
        )
        latency_ms = (time.time() - start_time) * 1000

        cost = self._calculate_cost(
            model_config,
            response.usage.input_tokens,
            response.usage.output_tokens,
        )
        self.cost_this_month += cost

        # Structured audit log: every request persisted for compliance analysis
        self.request_log.append({
            "team": self.team_id,
            "model": model_config.model_id,
            "complexity": task_complexity,
            "input_tokens": response.usage.input_tokens,
            "output_tokens": response.usage.output_tokens,
            "cost_usd": cost,
            "latency_ms": round(latency_ms),
            "timestamp": time.time(),
        })

        text = next(b.text for b in response.content if b.type == "text")
        return {
            "content": text,
            "model_used": model_config.model_id,
            "cost_usd": cost,
            "tokens": {
                "input": response.usage.input_tokens,
                "output": response.usage.output_tokens,
            },
        }


# Canonical usage across an engineering team:
# gateway = AIGateway(team_id="backend-platform", budget_usd_monthly=500.0)
# result = gateway.complete(
#     system="You are an expert systems code reviewer.",
#     messages=[{"role": "user", "content": f"Review this pull request:\n\n{code}"}],
#     task_complexity="moderate",  # Gateway dynamically selects the balanced tier
# )
# print(f"Operation unit cost: ${result['cost_usd']:.4f}")
```

### Multi-Provider Gateway Architecture

A production gateway rarely couples to a single vendor. The fortunate architectural reality is that the three dominant frontier APIs share identical conceptual mechanics (role-based message payloads, JSON schema tool definitions, token usage accounting in responses), keeping the translation layer remarkably thin:

```python
# Example 3.2: Minimal adapters for Claude, OpenAI, and Gemini.
# Each provider maintains its official SDK; the internal contract is unified.
# Verify active models and pricing in each provider's official documentation.

class ClaudeAdapter:
    def __init__(self):
        import anthropic
        self.client = anthropic.Anthropic()

    def complete(self, system: str, user: str, model: str, max_tokens: int) -> str:
        resp = self.client.messages.create(
            model=model, max_tokens=max_tokens,
            system=system, messages=[{"role": "user", "content": user}],
        )
        return next(b.text for b in resp.content if b.type == "text")

class OpenAIAdapter:
    def __init__(self):
        from openai import OpenAI
        self.client = OpenAI()  # Reads OPENAI_API_KEY from environment

    def complete(self, system: str, user: str, model: str, max_tokens: int) -> str:
        resp = self.client.chat.completions.create(
            model=model, max_completion_tokens=max_tokens,
            messages=[{"role": "system", "content": system},
                      {"role": "user", "content": user}],
        )
        return resp.choices[0].message.content

class GeminiAdapter:
    def __init__(self):
        from google import genai
        self.client = genai.Client()  # Reads GEMINI_API_KEY from environment

    def complete(self, system: str, user: str, model: str, max_tokens: int) -> str:
        resp = self.client.models.generate_content(
            model=model, contents=user,
            config={"system_instruction": system,
                    "max_output_tokens": max_tokens},
        )
        return resp.text
```

The decision of when to route to each provider is a business and technical judgment, not dogma: it must be driven by internal automated evaluation suites (Volume 4, Chapter 3) executed against your proprietary workloads, reviewed quarterly as price-performance frontiers shift multiple times per year.

**■ EXECUTIVE TRACK: The Capital ROI of Agentic Platform Engineering**

A centralized platform engineering team of four to six engineers delivering an enterprise AI-IDP directly matches the delivery velocity of fifty to one hundred product engineers. The capital allocation thesis mirrors cloud infrastructure: rather than requiring each product squad to configure bespoke servers, the platform abstracts distributed complexity. In the agentic era, the "server" is inference access, and "configuration" encompasses automated model routing, token economics, regression evals, and data governance.

Also, risk mitigation often outweighs raw productivity gains: without a centralized gateway, the enterprise maintains zero inventory of AI interactions—leaving leadership incapable of demonstrating to internal auditors or statutory regulators what proprietary data was transmitted to which external vendor. The NIST AI Risk Management Framework (2023) and the European Union AI Act [European Union, 2024](#ref-eu2024) converge on the same operational mandate: end-to-end traceability. The internal platform is the single architectural locus where compliance traceability is implemented once and inherited universally across all product lines.

**Core Telemetry for Benchmarking an AI Platform:**

| Operational Metric | Pre-Platform Baseline | Post-Platform Target (6 Months) |
|---|---|---|
| AI feature integration lead time | 2–3 weeks | 2–3 days |
| Cost visibility per LLM invocation | Zero visibility | Fully visible and < $0.01 on simple tasks |
| % of requests routed to cost-optimal tier | 0% (Manual developer selection) | > 80% (Automated gateway routing) |
| Production hallucination incidents | Unmeasured | Quantified with explicit error budgets |
| Automated agent regression eval coverage | 0% | > 70% of core production flows |

## Worked Exercise 3.1: Add Project-Level Budget Throttling to the Gateway

**Problem Statement.** The `AIGateway` in Example 3.1 tracks budgets at the team level. Finance mandates tracking spend **per project** within each team under a revised operational policy: upon exhausting allocated budget, the gateway must not reject requests with a hard error, but rather gracefully degrade execution to the economy model tier while raising an alert. Implement the minimal architectural changes.

**Walkthrough Solution.** Three concise modifications. First, `complete()` accepts a `project_id` argument and the budget registry transitions from an isolated scalar to a typed dictionary `{project_id: ProjectBudget}`; the structured audit log already captures all necessary metadata to retroactively reconstruct project-level expenditures—the direct dividend of rigorous logging from Day One. Second, the threshold exhaustion policy is formalized as an explicit enumeration (`HARD_STOP`, the existing default, or `DEGRADE`, the new policy), because implicit runtime fallback behavior is an incident waiting to occur. Third, under `DEGRADE`, `_select_model` forcibly overrides routing to the `fast` tier and injects `"degraded": True` into the return payload: downstream consumer services **must explicitly know** they received degraded output. Silently degrading execution quality is lying with infrastructure. The senior engineering nuance: operational degradation is instrumented as a metric; if a project spends 30% of the month degraded, the issue is not budget limits, but flawed probabilistic estimation (Volume 4, Chapter 2) or runaway Token-Burn (Volume 4, Chapter 1).

## Chapter 3 Takeaways

- The internal platform is a managed product [Skelton & Pais, 2019](#ref-skeltonpais2019); in the agentic era, it exposes AI primitives as first-class architectural capabilities.
- The AI Gateway is the critical component: complexity-based routing, unit cost accounting, budget cutoffs, immutable audit logs, and provider failover.
- Without a gateway there is no inventory; without an inventory there is zero defensibility before compliance auditors ([NIST, 2023](#ref-nist2023); [European Union, 2024](#ref-eu2024)).
- Dominant foundation model APIs share identical conceptual abstractions: multi-provider adapters are thin, and routing policies are calibrated quarterly via internal evals.
- A platform team of 4–6 engineers acts as a force multiplier for 50–100 product developers: the economics of cloud infrastructure, applied to cognitive compute.

## Discussion Questions

1. How many engineering teams across your enterprise invoke foundation models using uninventoried, personal API keys today?
2. If an AI provider doubled prices or suffered an extended regional outage tomorrow, how many hours would your architecture require to redirect production traffic to an alternative model?
3. Who is the designated internal Product Owner of your company's AI platform? If the answer is "no one," what production failure will occur before that ownership is assigned?

---
