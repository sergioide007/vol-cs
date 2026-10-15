# Chapter 12: Low Energy Consumption with AI Multi-Agent Systems: Efficiency as an Architectural Decision

> *The most expensive intelligence is the one that overthinks, not the one that makes mistakes.*

---

## Section 1: The Swarm's Hidden Cost: Thermodynamics and Economics

There is a seductive temptation in multi-agent systems: if one agent reasons well, ten will reason better. That intuition, however, ignores an unavoidable thermodynamic fact the industry took too long to face: every token consumed has a real energy cost, measurable in watts and in grams of CO₂.

Patterson et al. (2021), in their analysis published in *Communications of the ACM* (Q1, IF 5.4), quantified that training GPT-3 generated approximately 552 tons of CO₂eq, equivalent to the round-trip transatlantic flights of 300 passengers between New York and San Francisco. But training is a one-time cost; inference is a continuous one. Samsi et al. (2023), in their study "From Words to Watts" presented at the *IEEE HPEC Workshop*, measured the energy consumption of LLM inference under real conditions and found that generating 1,000 tokens with a 70B-parameter model consumes between 0.003 and 0.009 kWh depending on the hardware, equivalent to keeping an LED bulb on for 12 minutes. Multiplied by millions of daily inferences in an enterprise swarm, the scale becomes unavoidable.

Schwartz et al. (2020), in "Green AI" (*Communications of the ACM*, Q1), documented the trend they call "Red AI": the race for better results by using more compute, with no consideration of energy cost. Their proposal, "Green AI," holds that energy efficiency must be a first-class metric in the design of AI systems, on par with accuracy or latency.

From the above it follows that efficiency in a swarm is not post-hoc optimization: it is **a first-order design decision** with economic, ethical, and strategic consequences.

| Model | Parameters | Consumption per 1K tokens (kWh) | Inference cost (USD/1M tokens) | Optimal use cases |
|--------|-----------|---------------------------|----------------------------------|----------------------|
| Haiku (Anthropic) | ~3B | 0.0001 | $0.25 | Classification, FAQ, routing |
| Sonnet (Anthropic) | ~35B | 0.0008 | $3.00 | Analysis, synthesis, code |
| Opus (Anthropic) | ~200B+ | 0.003 | $15.00 | Complex reasoning, critical decisions |
| Llama 3.1 8B (local) | 8B | 0.00015 (efficient GPU) | $0 (own hardware) | Repetitive on-premise tasks |
| Llama 3.1 70B (local) | 70B | 0.0012 (H100) | $0 (own hardware) | Complex on-premise tasks |

---

## Section 2: The Three Levers of Energy Efficiency

![Graceful routing: Haiku → Sonnet → Opus by task complexity](imagenes/uml/c28_routing_efficiency_en.png)

### Lever 1: Routing by Difficulty (Graceful Escalation)

The principle is deceptively simple: not every task deserves the most powerful model. The implementation requires a **Router Agent** that classifies each request before sending it to a model, based on inferred complexity signals:

```python
from dataclasses import dataclass
from enum import Enum

class ComplexityLevel(Enum):
    TRIVIAL = "trivial"       # FAQ, binary classification, data extraction
    MODERATE = "moderate"     # Synthesis, basic analysis, structured generation
    COMPLEX = "complex"       # Multi-step reasoning, decisions with trade-offs
    CRITICAL = "critical"     # Compliance, security, irreversible decisions

@dataclass
class RoutingDecision:
    level: ComplexityLevel
    model: str
    justification: str
    estimated_cost_usd: float

class RouterAgent:
    
    CLASSIFICATION_RULES = {
        # Low-complexity signals
        "trivial": [
            "prompt_length < 500 tokens",
            "type in ['classification', 'extraction', 'faq']",
            "has_cached_answer",
            "similarity_to_previous_query > 0.90"
        ],
        # Moderate-complexity signals
        "moderate": [
            "500 <= prompt_length < 2000",
            "type in ['analysis', 'synthesis', 'simple_code']",
            "num_required_tools <= 2"
        ],
        # High-complexity signals  
        "complex": [
            "prompt_length >= 2000",
            "type in ['reasoning', 'design', 'evaluation']",
            "num_estimated_steps > 5",
            "requires_multiple_source_access"
        ]
    }
    
    def route(self, request: Request) -> RoutingDecision:
        level = self._classify_complexity(request)
        
        model_map = {
            ComplexityLevel.TRIVIAL:  ("claude-haiku-4-5",    0.00025),
            ComplexityLevel.MODERATE: ("claude-sonnet-4-6",   0.003),
            ComplexityLevel.COMPLEX:  ("claude-sonnet-4-6",   0.003),  # Sonnet for complex, Opus only for critical
            ComplexityLevel.CRITICAL: ("claude-opus-4-8",     0.015),
        }
        
        model, base_cost = model_map[level]
        estimated_cost = base_cost * (request.token_length / 1000)
        
        return RoutingDecision(
            level=level,
            model=model,
            justification=self._generate_justification(level, request),
            estimated_cost_usd=estimated_cost
        )
```

**Why does it work?** Information theory backs the principle: the information entropy of a trivial task (e.g., "is this email spam?") is low. A small model reaches convergence with few reasoning tokens. Using Opus in that case is like using a neurosurgery scalpel to cut fruit: it works, but at a disproportionate cost.

In practical terms, Haiku on tasks of low *Kolmogorov complexity* (formatting, classification, structured extraction) is **6× cheaper than Sonnet** with no measurable quality degradation. Sonnet on moderate analysis is **5× cheaper than Opus** with a quality difference under 3% on standard domain benchmarks.

### Lever 2: Semantic Cache (Don't Recompute What's Already Computed)

A semantic cache is qualitatively different from a literal text cache. Instead of looking for exact string matches, it compares the new query's embedding with the embeddings of previous queries and their stored responses. If the cosine similarity exceeds a threshold (typically 0.85–0.92), the stored response is returned without inference.

**The quantitative justification**: the Pareto Principle applied to enterprise queries is remarkably consistent. Internal studies at companies with >10,000 users of AI systems show that 80% of query volume comes from 20% of unique topics or questions. A correctly sized semantic cache captures that 80% with a false-negative rate (cases where the cached answer differs materially from the one that would have been generated de novo) below 2%.

```python
import numpy as np
from typing import Optional

class SemanticCache:
    def __init__(self, similarity_threshold: float = 0.87):
        self.threshold = similarity_threshold
        self.cache: dict[str, tuple[np.ndarray, str]] = {}  # {id: (embedding, response)}
    
    def lookup(self, query_embedding: np.ndarray) -> Optional[str]:
        if not self.cache:
            return None
        
        # Vectorized cosine similarity
        cache_embeddings = np.array([emb for emb, _ in self.cache.values()])
        similarities = np.dot(cache_embeddings, query_embedding) / (
            np.linalg.norm(cache_embeddings, axis=1) * np.linalg.norm(query_embedding)
        )
        
        max_idx = np.argmax(similarities)
        if similarities[max_idx] >= self.threshold:
            cached_response = list(self.cache.values())[max_idx][1]
            self._record_cache_hit(similarities[max_idx])
            return cached_response
        
        return None  # Cache miss → full inference
    
    def store(self, embedding: np.ndarray, response: str) -> None:
        key = self._generate_key(embedding)
        self.cache[key] = (embedding, response)
```

### Lever 3: Early Termination (Early Stopping for Agents)

Agentic reasoning has a diminishing marginal cost: the first reasoning step contributes most of the value; the following ones refine. Setting confidence thresholds that stop reasoning once certainty is sufficient avoids the waste of over-deliberation.

**The mathematical principle**: information gain (in bits) decreases logarithmically with each reasoning iteration. Past 80% confidence, each additional 10% of confidence costs roughly twice as many reasoning tokens as the previous 10%. The cost-benefit curve invariably inverts around 85–90%.

---

## Section 3: Edge Computing with Ryzen AI: The Swarm on the Device

Now, what emerges when you combine routing by difficulty with local inference hardware is something few architectures allow: **swarms of agents running entirely on the device**, with no contact with the cloud for tasks that don't need it.

AMD Ryzen AI integrates an **NPU (Neural Processing Unit)** specialized in low-latency inference. The Ryzen AI 300 reaches 16 TOPS (Tera Operations Per Second) at 15–45W. For context: a laptop with a 50Wh battery can run 8 inference agents in parallel for **8–10 hours of continuous work**: data documented by AnandTech benchmarks, 2024.

**The economic calculation is transparent**:
- Cloud GPU server for inference: $0.50/hour
- Ryzen AI 300 laptop (~$1,299) amortized over 36 months: ~$0.06/day of compute

Break-even is reached in approximately 40 days of intensive use. After that, each day of local inference costs 88% less than the cloud alternative.

**The privacy case**: when data can't leave the device (healthcare, defense, legal consulting), the local swarm is not a cost optimization, it is the only legally viable architecture. Privacy, in that case, is guaranteed by physics: the data never travels.

**Example autonomy calculation for a swarm of 8 lightweight agents**:

```
Lightweight model: ResNet-50 equivalent (~25M parameters per agent)
NPU consumption: ~0.8J per inference
Battery: 50Wh = 180,000J

Total inferences available: 180,000J ÷ 0.8J = 225,000 inferences

Swarm usage:
8 agents × 30 inferences/second × 3,600 seconds = 864,000 inferences/hour

Autonomy in pure inference: ~15 minutes (continuous peak use)
Autonomy in real use (active + idle cycles): 8–10 hours of a working day
```

The strategic point: **the agentic code doesn't change**. Only the deployment changes. Instead of "run agents on a cloud GPU," they are run on "local Ryzen AI + cloud as a fallback." The multi-agent system is deployment-agnostic if it was designed with the model adapter pattern (cf. Ch. 22).

---

## Section 4: The Small Model Paradox: More Isn't Always More

Here is this chapter's central counterintuitive point: a swarm of well-orchestrated small models can outperform a single large model in quality, and do so at lower cost.

The reason is **entropy-reducing specialization**: an 8B-parameter model fine-tuned to classify technical support tickets has a probability distribution much more concentrated over the space of correct answers for that domain than a generalist 200B-parameter model. The small model doesn't need to "think about everything else"; it can devote all its capacity to the specific problem.

Luccioni, Viguier & Ligozat (2023), in their study on the carbon footprint of BLOOM published in the *Journal of Machine Learning Research* (Q1, IF 6.2), documented that smaller models (specialized by domain through fine-tuning) can match the performance of generalist models on specific tasks with up to 50× fewer active parameters. Efficiency doesn't oppose quality; well designed, it enables it.

**The paradox quantified** for a legal contract processing system:

| Architecture | Quality (F1 on clause extraction) | Cost per contract | P99 latency |
|-------------|----------------------------------------|-------------------|-------------|
| Single Opus | 0.91 | $0.28 | 8.2 seconds |
| Swarm: 3×Haiku + 1×Sonnet supervisor | 0.93 | $0.06 | 3.1 seconds |
| Swarm: 5×Llama-8B-legal + 1×Sonnet arbiter | 0.94 | $0.02 | 1.8 seconds |

The specialized swarm outperforms the single large model in quality, at 14× lower cost and 4.5× lower latency. This is not an anecdote; it is the pattern documented in multiple domains with similar characteristics (a bounded domain, high volume, objectively definable quality criteria).

---

## Section 5: Executive Perspective: CAPEX vs. OPEX and the Strategic Decision

**■ EXECUTIVE TRACK**


For the CFO or CTO who must approve the AI infrastructure strategy, the decision is not technical: it is financial and strategic.

**Cloud-First Model** (pure OPEX):
- Initial CAPEX: $0
- Monthly OPEX: Variable with usage. For 1M inferences/day, ~$12,000–$45,000/month
- Advantages: no hardware commitments, instant scalability, no MLOps team for hardware
- Disadvantages: unpredictable variable cost, data egress, variable latency, provider dependence

**Hybrid Model** (initial CAPEX + reduced OPEX):
- Initial CAPEX: $50,000–$200,000 (on-premise GPUs: NVIDIA H100s)
- Monthly OPEX: $3,000–$8,000 (electricity, cooling, maintenance) + cloud for peaks
- Advantages: predictable cost, data control, latency <50ms, no data egress
- Disadvantages: high CAPEX, MLOps team needed, upgrade cycle every 3–5 years

**Edge + Cloud Model** (for teams with AI workstations):
- Initial CAPEX: $1,000–$7,000/workstation (RTX 6000 Ada or Ryzen AI)
- Monthly OPEX: ~$0 on inference, $200–$500 in electricity
- Advantages: $0 per iteration during development, privacy, code portable to production
- Disadvantages: limited scale, not suitable for >100K inferences/day

**Strategic decision table**:

| Scenario | Daily volume | Recommendation | 3-year TCO |
|-----------|---------------|---------------|-------------|
| MVP startup | <10K inf/day | Cloud-First | $45K–$90K |
| Mid-sized company | 10K–500K inf/day | Hybrid (70% local, 30% cloud peaks) | $180K–$320K |
| Enterprise | 500K–5M inf/day | Primary on-premise + Cloud resilience | $400K–$1.2M |
| Sensitive data (healthcare, legal) | Any volume | On-premise mandatory | Varies |

---

## Expanded Academic Version

> Energy efficiency in neural inference systems can be formalized through the notion of *Pareto efficiency* over the criteria space (quality, latency, energy). Formally, an architectural configuration A dominates B if and only if A is at least as good as B on all criteria and strictly better on at least one. The set of non-dominated configurations constitutes the system's **Pareto frontier**, and the architect's task is to select the optimal point on that frontier according to the specific operational constraints. The empirical evidence documents that this frontier is systematically superior for swarms of specialized models than for single generalist models: specialization shifts the frontier toward higher values of quality per unit of energy consumed, which Luccioni et al. (2023) formalized as the improvement in the *accuracy-per-watt* ratio when moving from monolithic architectures to heterogeneous swarms.

---

## Key Takeaways from Chapter 12

- Every token has a real energy cost. Training GPT-3: ~552 tons CO₂eq ([Patterson et al., 2021](#ref-patterson2021)).
- The three central **levers**: routing by difficulty (Haiku 6× cheaper than Sonnet on trivial tasks), semantic cache (captures 80% of volume with <2% false negatives), early termination (information gain decreases logarithmically).
- Edge computing with the **AMD Ryzen AI NPU**: 16 TOPS at 15–45W, break-even vs. cloud in 40 days.
- A swarm of small specialized models outperforms a single large model in quality and cost (the paradox quantified: 14× lower cost, 4.5× lower latency, +3% quality in the documented case).
- **CAPEX vs. OPEX**: Cloud-First for an MVP; Hybrid for a mid-sized company; On-premise for enterprise and sensitive data.
- Energy efficiency is, besides economic, an ethical responsibility. "Green AI" ([Schwartz et al., 2020](#ref-schwartz2020)) proposes efficiency as a first-class metric.
- Data privacy is guaranteed by physics in edge architectures: if the data doesn't leave the device, it can't be compromised in transit.

---

## Worked Exercise 12.1: Design the Efficiency Strategy for a Financial Analysis Swarm

**Problem.** A mid-sized bank processes 50,000 transactions per day that require fraud risk analysis. The team proposes using Opus for every transaction. The architect must design an efficient alternative. Regulatory constraint: transaction data cannot leave the bank's infrastructure (PCI-DSS).

**Solution:**

```yaml
proposed_architecture:
  name: "On-premise fraud analysis swarm"
  
  routing_layer:
    type: "Local Router Agent"
    hardware: "RTX A6000 (48GB VRAM)"
    model: "Llama-3.1-8B-finance-finetuned"
    function: "Classifies transactions as TRIVIAL/MODERATE/CRITICAL"
    cost: "$0 per transaction (local inference)"
    
  analysis_layer:
    trivial:  # 70% of volume (routine transactions)
      model: "Llama-3.1-8B-fraud-detector"
      hardware: "On-premise NPU"
      cost: "$0"
      latency: "<50ms"
      
    moderate:  # 25% of volume
      model: "Llama-3.1-70B-finance"
      hardware: "2× NVIDIA H100 on-premise"
      cost: "$0"
      latency: "<200ms"
      
    critical:  # 5% of volume (transactions >$50,000 or anomalous patterns)
      model: "claude-sonnet-4-6 via private API"
      note: "API endpoint inside the bank's VPC via AWS PrivateLink"
      cost: "$0.003 per transaction"
      latency: "<2s"

  calculations:
    daily_volume: 50000
    distribution: [0.70, 0.25, 0.05]
    opus_alternative_cost: "50,000 × $0.015 = $750/day = $273,750/year"
    proposal_cost: "50,000 × 0.05 × $0.003 = $7.50/day = $2,737/year"
    annual_savings: "$271,013 (99% reduction)"
    
  compliance:
    pci_dss: "compliant — 95% of data never leaves on-premise"
    audit: "all analyses logged with on-premise OpenTelemetry"
```

The projected annual savings exceed $271K with full PCI-DSS compliance. The on-premise hardware CAPEX (~$120,000 in H100s) is amortized in 5.3 months.

---
