# Appendix B: Reference Pricing and Pipeline Cost Accounting

> **Cutoff Date: September 28, 2026.** Source: Official Anthropic documentation
> ("Models overview" and "Pricing"). Vendor pricing adjusts periodically.
> This appendix is the sole repository across the entire series where explicit
> pricing figures are recorded: if a reader encounters a conflicting rate in
> another chapter, it represents an editorial defect. Always consult official
> vendor documentation for real-time rates.

## B.1. Architectural Rationale for This Appendix

Two chapters cross-reference this appendix directly: Chapter 5 of Volume 1, to calculate the cost profile of an agentic ticket triage and synthesis pipeline, and Chapter 9 of Volume 4, to audit the expenses of a one-week engineering sprint utilizing an autonomous coding agent. Neither chapter can establish its economic proofs without a unified reference baseline, and duplicate pricing tables across volumes would inevitably drift out of synchronization across printings.

Also, Chapter 3 of Volume 3 references this appendix as a case study in technical half-life: the specific models listed here will be superseded within months, whereas the principles governing architectural design, evaluation pyramids, and defensive cost controls remain invariant.

## B.2. Pricing per Million Tokens (USD)

| Model | Input | Output | Primary Operational Use Case |
|---|---:|---:|---|
| Fable 5.1 | 10.00 | 50.00 | High-complexity reasoning and long-horizon autonomous planning |
| Opus 5.5 | 4.00 | 20.00 | Deep cognitive synthesis and knowledge work; default recommendation |
| Sonnet 5 | 2.00 | 10.00 | Optimal Pareto frontier of execution speed, capability, and cost |
| Haiku 4.5 | 1.00 | 5.00 | Ultra-fast classification, high-volume extraction, and shallow filtering |

Legacy models, retained for backwards compatibility: Opus 4.8, 4.7, 4.6, 4.5, and 4.1 ($5.00 / $25.00); Sonnet 4.6, 4.5, and 4 ($3.00 / $15.00); and Haiku 3.5 ($0.80 / $4.00).

An agentic pipeline processing 2 MTok input and 0.5 MTok output with **Sonnet 5** costs `2 × $2.00 + 0.5 × $10.00 = $9.00 USD` per run. The identical workload dispatched to **Haiku 4.5** costs `2 × $1.00 + 0.5 × $5.00 = $4.50`, while executing via **Opus 5.5** totals `2 × $4.00 + 0.5 × $20.00 = $18.00`.

Model selection is an economic and architectural trade-off, not merely a price comparison. Sonnet 5 and Opus 5.5 are reserved for stages where error blast radiuses carry severe financial or operational penalties. Haiku 4.5 handles deterministic classification, extraction, and pre-filtering, where raw request volume dictates total expenditure. Hot-swapping the underlying model at an individual pipeline stage without altering its tool contract represents the highest-leverage optimization available.

> **Tokenizer Variance Warning:** Claude 4.7 and later models utilize an updated
> tokenizer that yields approximately **30% more tokens** for identical input text;
> Sonnet 4.6 and earlier utilize the previous vocabulary. Comparing gross per-token
> pricing across model generations without adjusting for tokenizer density leads to
> flawed financial projections.

## B.3. Consumer Subscriptions vs. Direct API Access

| Billing Model | Rate Structure | Architectural Fit |
|---|---:|---|
| Consumer Subscription | Fixed monthly fee | Daily interactive workflows lacking programmatic telemetry |
| Pay-Per-Token API | Usage-based (per B.2) | Automated pipelines, CI/CD gates, and per-step accounting |

Consumer flat-rate subscriptions provide an explicit financial ceiling at the expense of zero visibility into per-task economics. When production engineering requires attributing costs to specific microservice steps—as mandated by the Iteration Cost per Unit (CIU) metric in Volume 4, Chapter 1—direct API access is the sole viable mechanism.

## B.4. The Three Multipliers Governing Real Production Invoices

1. **Prompt Cache Reads (Hits and Refreshes):** Invoiced at **0.1×** base input pricing: for Sonnet 5, $0.20 per MTok rather than $2.00. This is the single highest-leverage lever in agentic systems, yet the most frequently overlooked.
2. **Prompt Cache Writes:** Billed at a premium over base input: 1.25× for a 5-minute time-to-live (TTL) window and 2.0× for a 1-hour window. Amortization succeeds only when prompt prefixes are reused across multiple consecutive invocations; a stable master prompt capitalizes on this, whereas volatile prompts destroy efficiency.
3. **Batch API Ingestion:** Asynchronous, non-real-time tasks dispatched via batch endpoints receive an immediate 50% discount. This underpins the overnight batch architecture in Volume 1, Chapter 5: classifying and drafting responses for thousands of backlogged tickets overnight does not require sub-second interactive latency.

Prompt caching and batch discounts **compound multiplicatively**, and order of operations is vital: the cache prefix is primed first, and subsequent batch requests reuse the cached context.

## B.5. The Production Cost Accounting Formula

```
execution_cost   = (input_tokens  / 1e6) * input_price
                 + (output_tokens / 1e6) * output_price

optimized_cost   = execution_cost * cache_factor * batch_factor

CIU              = total_pipeline_cost / verified_features_shipped
```

Here, `cache_factor` and `batch_factor` are fractional multipliers between 0 and 1. An architecture that pairs prompt cache reads (0.1×) with batch processing (0.5×) reduces its compute expenditure by a factor of **0.05**—slashing operating costs by two full orders of magnitude without altering business logic. The third equation operationalizes raw spending into an engineering metric: the CIU metric from Volume 4 measures dollars expended per unit of verified business value delivered to production—the only figure comparable across model providers, architectural versions, and fiscal quarters.

## B.6. Maintenance and Audit Governance

This file serves as the single source of truth for pricing metrics across the four-volume series. The repository linter (`tools/lint_manuscript.py`) validates two invariants:

- **C4:** Any cited appendix must exist physically in the repository. If a chapter references "as detailed in Appendix B" and this file is missing, the build process halts.
- **C6:** No literal foundation model identifier may appear in manuscript prose outside the approved allowlist in `tools/model-allowlist.txt`. Concrete version strings are confined to this reference table; prose discusses model tiers (e.g., "the frontier reasoning model"), preserving technical shelf life.

When market pricing shifts, edit this matrix, update the cutoff date, record the adjustment in `INFORME_EDITORIAL.md`, and verify the two pipeline chapters that reference it. This twenty-minute maintenance workflow guarantees architectural integrity without requiring structural rewrites.
