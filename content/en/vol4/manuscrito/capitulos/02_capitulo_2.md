# Chapter 2: Probabilistic Estimation in Agentic Systems

## The End of Person-Hours

Estimating in story points or person-hours presupposes a roughly linear production model: more engineers for more time produces more software. That model was demolished half a century ago ("adding manpower to a late project makes it later," Brooks's Law, 1975), and it is doubly unsuited to agentic systems, where the bottleneck is validation, not writing code, and where effort variance is structural.

We propose adopting **Monte Carlo simulation** as the estimation methodology, for two reasons:

1. **Uncertainty in agentic systems is inherent, not correctable.** An agent can solve a task in 3 iterations or in 30, depending on the ambiguity of the initial prompt, the quality of the context, and the emergent complexity of integration. That variance doesn't disappear with the team's experience: it is a property of the system, as it is of network traffic or the demand for a service.
2. **Monte Carlo turns uncertainty from an enemy into data.** Instead of fighting it with falsely precise estimates ("this takes 8 hours"), it quantifies it: "with 85% confidence, this will cost less than X dollars and finish in under Y minutes." Management can budget percentiles; it can't budget wishes.

The method is the standard in the disciplines that manage uncertainty seriously (finance, reliability engineering, quantitative project management), and its application to software has a tradition: software economics itself was born modeling cost as a function of uncertain variables ([Boehm, 1981](#ref-boehm1981)).

**► TECHNICAL TRACK: Monte Carlo Estimator for Agentic Pipelines**

```python
# Example 2.1: Monte Carlo estimator for agentic pipelines.
# Each task is modeled with a triangular distribution (minimum, mode, maximum)
# of tokens, calibrated with historical data from the CIUTracker (Chapter 11),
# plus a log-normal retry factor.

import numpy as np

def estimate_agent_pipeline(
    tasks: list[dict],
    num_simulations: int = 10_000,
    target_percentile: int = 85,
    cost_per_token: float = 9e-6,    # USD/token average of the model mix
    tokens_per_second: float = 150,  # typical output speed
) -> dict:
    """
    Estimates the cost and time of an agentic pipeline via Monte Carlo.

    Args:
        tasks: list of dicts with 'name', 'tokens_min', 'tokens_mode',
               'tokens_max' (calibrate with your own historical data).
        num_simulations: more simulations = a more stable tail.
        target_percentile: 85 = conservative, 50 = neutral.
        cost_per_token: derive from the pipeline's real model mix.
    """
    costs, times = [], []

    for _ in range(num_simulations):
        sim_cost, sim_time = 0.0, 0.0
        for task in tasks:
            tokens = np.random.triangular(
                left=task["tokens_min"],
                mode=task["tokens_mode"],
                right=task["tokens_max"],
            )
            # Retries: log-normal — most tasks don't retry,
            # a few retry a lot. The heavy tail is the realistic part.
            retry_factor = np.random.lognormal(mean=0, sigma=0.3)
            actual_tokens = tokens * retry_factor

            sim_cost += actual_tokens * cost_per_token
            sim_time += actual_tokens / tokens_per_second
        costs.append(sim_cost)
        times.append(sim_time / 60)  # minutes

    costs, times = np.array(costs), np.array(times)
    p = target_percentile

    return {
        "cost_usd": {
            "p50": round(float(np.percentile(costs, 50)), 4),
            "p85": round(float(np.percentile(costs, 85)), 4),
            "p95": round(float(np.percentile(costs, 95)), 4),
            "mean": round(float(costs.mean()), 4),
            "std_dev": round(float(costs.std()), 4),
        },
        "time_minutes": {
            "p50": round(float(np.percentile(times, 50)), 1),
            "p85": round(float(np.percentile(times, 85)), 1),
            "p95": round(float(np.percentile(times, 95)), 1),
        },
        "recommendation": {
            "budget_usd": round(float(np.percentile(costs, p)), 4),
            "estimated_time_min": round(float(np.percentile(times, p)), 1),
            "confidence": f"{p}%",
            "interpretation": (
                f"With {p}% confidence, the pipeline will cost less than "
                f"${np.percentile(costs, p):.4f} USD and finish in under "
                f"{np.percentile(times, p):.1f} minutes."
            ),
        },
    }


# Usage example: automated code review pipeline
code_review_pipeline = [
    {"name": "Initial analysis",      "tokens_min": 500,
     "tokens_mode": 1500, "tokens_max": 4000},
    {"name": "Security review",       "tokens_min": 800,
     "tokens_mode": 2000, "tokens_max": 6000},
    {"name": "Architecture review",   "tokens_min": 1000,
     "tokens_mode": 3000, "tokens_max": 8000},
    {"name": "Final synthesis",       "tokens_min": 300,
     "tokens_mode": 1000, "tokens_max": 2500},
]

estimate = estimate_agent_pipeline(code_review_pipeline,
                                   target_percentile=85)
print(estimate["recommendation"]["interpretation"])
```

### From Estimation to Operation: The Complete Loop

The estimator above is worth nothing with invented parameters, and worth gold with measured ones. The complete maturity loop ties together the pieces of the book:

1. The **AIGateway** (Chapter 3) records tokens and cost for every real call.
2. The **CIUTracker** (Chapter 11) aggregates them by feature and by team.
3. The historical distributions calibrate this chapter's **Monte Carlo estimator**.
4. The estimates feed the **budgets** of the agentic loops (Chapter 4) and the alert thresholds.
5. Deviations between what was estimated and what was observed refine the distributions and, when systematic, give away a regime change: a new model, a context that grew, an orchestration pattern that no longer pays for itself.

**■ EXECUTIVE TRACK**

The conversation this chapter changes is the one in the planning committee. The question "how much will it cost?" now has an honest answer of three numbers (p50, p85, p95) instead of a single figure everyone knows is false. The operational recommendation: **budget at p85 and celebrate at p50**. Teams that budget at the mean live in chronic cost overrun half the time, not from poor execution but from arithmetic: in heavy-tailed distributions, the mean sits well below what reality delivers with uncomfortable frequency. The variance of agentic work is not a defect to hide: it is data to manage, and the organizations that manage it make better portfolio decisions than those that deny it.

## Worked Exercise 2.1: Read the Percentiles Like an Executive

**Problem.** The estimator returns, for a new pipeline: cost p50 = $0.9, p85 = $2.1, p95 = $4.8 per run; expected volume: 2,000 runs/month. The director asks: "how much budget do I request?" Three analysts answer: A: "$1,800/month (2,000 × p50)"; B: "$4,200/month (2,000 × p85)"; C: "$2,200/month (2,000 × the simulated mean, $1.1)". Who is right and why aren't the others?

**Annotated solution.** **C** is closest, with a nuance that matters. The error of A and B is the same: applying a percentile *per run* to an *aggregate*. The individual p85 is not the month's p85: with 2,000 independent runs, the law of large numbers narrows the distribution of the total around 2,000 × the **mean**, and the mean ($1.1) exceeds the p50 ($0.9) precisely because of the heavy tail of retries. A systematically budgets short (it confuses median with mean in a skewed distribution: the arithmetic error of the chapter); B pays an absurd insurance premium (the "bad case" doesn't happen 2,000 times in a row). The complete professional answer: **2,000 × mean + a margin for the uncertainty of the aggregate** (simulate the monthly sum and take its p85, which will be much closer to the mean than the individual p85) **plus** the regime caveat: if volume, model, or context change, the distributions are recalibrated (step 5 of the maturity loop). Individual percentiles serve a different decision: budgeting *one* critical task, setting timeouts, and sizing alerts; confusing the two uses is the most common mistake when adopting Monte Carlo.

## Key Takeaways from Chapter 2

- The variance of agentic work is structural, not correctable: it is quantified, not denied ([Brooks, 1975](#ref-brooks1975); [Boehm, 1981](#ref-boehm1981)).
- Monte Carlo with a triangular distribution + a log-normal retry factor: simple, calibratable with the gateway's data.
- Budget at p85, celebrate at p50, for individual tasks; for aggregates, simulate the sum: percentiles don't multiply.
- The estimator is worth what its parameters are worth: the loop gateway → CIU → distributions → budgets → deviations is the complete system.
- Systematic deviations are not noise: they give away a regime change (a new model, a grown context, a pattern that stopped paying).

## Discussion Questions

1. What real distribution do iterations per task have on your team? If there's no data, what keeps you from instrumenting the gateway this week?
2. Which decisions in your organization are made today on point estimates that should be made on percentiles?
