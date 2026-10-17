# Chapter 8: Operating the System: Observability and MLOps for Small Teams

## You Can't Govern What You Can't See

Chapters 11 and 13 gave the metrics (CIU, evals); this chapter puts them to work in production. The parent discipline is reliability engineering: the four golden signals (latency, traffic, errors, saturation) as the vital minimum of any service ([Beyer et al., 2016](#ref-beyer2016)), and the three classic pillars of observability (logs, metrics, and traces) as its instruments. The open standard that unifies them today is OpenTelemetry (OpenTelemetry, n.d.), and its central concept, the **distributed trace**, seems designed for us: the ReAct loop *is* a trace; the task is the root span; each thought, model call, and tool execution is a child span with duration, attributes, and result.

To the golden signals, the agentic system adds its own (the **synthetic signals**), all derivable from the instrumentation the book has already built:

| Signal | What it reveals | Where it comes from |
|---|---|---|
| Input/output tokens per task | Inflated context, verbosity | AIGateway (Ch. 3) |
| Cache hit rate | Prefixes broken by timestamps/UUIDs | `cache_read_input_tokens` (Ch. 10) |
| Iterations per task (p50/p95) | Degenerate loops, ambiguous prompts | Agentic loop (Ch. 4) |
| Tool error rate | Ambiguous schemas, downed systems | `is_error` results (Ch. 4) |
| CIU per team and feature | The complete economics | CIUTracker (Ch. 10) |
| Eval pass rate | Quality drift | Suite in CI (Ch. 12) |
| DLQ depth | Cases the system can't digest | Broker (Ch. 16) |

```python
# Example 8.1 (Python + OpenTelemetry): the ReAct loop as a trace.
# Each task = a root span; each tool = a child span.
# pip install opentelemetry-api opentelemetry-sdk

from opentelemetry import trace

tracer = trace.get_tracer("agent.reviewer")

def run_agent_traced(user_input: str, max_iterations: int = 10) -> str:
    with tracer.start_as_current_span("task.code-review") as root:
        root.set_attribute("agent.prompt_version", "reviewer-v3")
        messages = [{"role": "user", "content": user_input}]

        for i in range(max_iterations):
            with tracer.start_as_current_span("llm.call") as span:
                response = client.messages.create(
                    model="claude-opus-4-8", max_tokens=4096,
                    tools=TOOLS, messages=messages)
                span.set_attribute("llm.model", response.model)
                span.set_attribute("llm.tokens.input",
                                   response.usage.input_tokens)
                span.set_attribute("llm.tokens.output",
                                   response.usage.output_tokens)
                span.set_attribute("llm.cache.read",
                                   response.usage.cache_read_input_tokens or 0)

            if response.stop_reason != "tool_use":
                root.set_attribute("agent.iterations", i + 1)
                return extract_text(response)

            messages.append({"role": "assistant", "content": response.content})
            results = []
            for block in response.content:
                if block.type == "tool_use":
                    with tracer.start_as_current_span(
                            f"tool.{block.name}") as tspan:
                        content, is_err = execute_tool(block.name, block.input)
                        tspan.set_attribute("tool.is_error", is_err)
                        results.append({"type": "tool_result",
                                        "tool_use_id": block.id,
                                        "content": content,
                                        "is_error": is_err})
            messages.append({"role": "user", "content": results})

        root.set_attribute("agent.budget_exhausted", True)
        return "Iteration budget exhausted."
```

The most valuable attribute in the whole trace is the least technical one: `agent.prompt_version`. When the eval pass rate drops on a Tuesday at 3:40 p.m., that tag will tell you in seconds whether it was the new prompt's deployment, a silent update to the provider's model, or a shift in the distribution of inputs. Without it, the answer is three days of archaeology.

## MLOps for Small Teams: LLMOps Without Ceremony

The MLOps literature was born for teams that train models, with their hidden technical debt (the model code as a minimal fraction of the system; [Sculley et al., 2015](#ref-sculley2015)) and their maturity rubrics ([Breck et al., 2017](#ref-breck2017)). This book's team trains nothing, and that radically simplifies the discipline: its "model" is a composite of *prompt + context + tools + the provider's model identifier*. The honest translation of MLOps to this world (call it LLMOps) fits in four practices a team of three can operate without a dedicated platform:

1. **Version the composite, not just the code.** Master prompts, domain contexts, skills, tool schemas, and model identifiers live in Git and are tagged together: deployment is a *release* of the composite. The question "which version of the agent answered this?" has a one-word answer: the tag that travels in the trace and in the events (Chapter 7).
2. **Test the composite in CI.** The eval suite (Chapter 13) runs on every change to any piece of the composite. The rubric from Breck et al. (2017) is inherited, adapted: is the evaluation data versioned? thresholds that break the build? cost measured alongside quality?
3. **Deploy with a canary.** The new prompt serves 10% of traffic during a window; the canary's CIU and eval rate are compared with the control before promoting. In the event-driven world (Chapter 7) this is a second consumer group reading the same log; the cheapest canary ever built.
4. **Monitor drift with your own evals.** A daily sample of real traffic goes through the suite; the trend, not the point value, triggers the alert. Providers update models: yesterday's correct behavior is a hypothesis, not a guarantee (Chapter 1 (Vol. 3)).

### Agent Migrations: The Flyway/Liquibase Pattern Applied to the Composite

Versioning with Git tags (practice 1) is enough to know which composite ran; it isn't enough to answer the question Flyway and Liquibase have been solving in databases for twenty years: in exactly what order were the changes applied to each environment, and can that order be reconstructed if an environment falls out of sync? A master prompt edited directly in production, without passing through dev and stage, is the agentic equivalent of an `ALTER TABLE` run by hand against the production database, precisely what these tools exist to prevent.

The adaptation is direct. Every change to the composite (prompt, tool schema, degradation policy (Chapter 5, Case 8), RACI assignment (Vol. 3, Chapter 15)) is declared as a numbered, immutable migration:

```
migrations/
  researcher_agent/
    V001__initial_prompt.md
    V002__adds_web_search_tool.yaml
    V003__tunes_degradation_policy.yaml
    V004__updates_model_to_claude_sonnet_5.yaml
```

Three guarantees, taken directly from Flyway/Liquibase, are the ones that truly matter:

1. **Checksum of an applied migration.** Once `V002` has been applied in an environment, its content is hashed in a history table (`agent_migrations`: agent, version, environment, checksum, applied_by, date). If someone edits `V002.yaml` after it was applied, the next run fails with a different checksum, the same mechanism that prevents hand-rewriting the history of a SQL schema in production, now applied to the history of an agent's decisions.
2. **Strict order, no skips.** `V004` can't be applied in production if `V003` wasn't applied earlier in that same environment. In practice this resolves the environment promotion question from Chapter 5 (Case 8, Vol. 4): clearing the adjusted OAI threshold is necessary but not sufficient; the sequence of migrations in stage must also be an exact subset, in the same order, of what is promoted to production.
3. **Paired reversal migration.** Each `V00N` declares its `U00N` (undo). If `V004`'s prompt degrades the quality measured by evals (practice 3, canary), the correct rollback is not editing the prompt back by hand (that loses the audit): it is applying `U004`, recorded in the same history table with the same discipline as its original application.

**What this buys that Git alone doesn't.** A `git log` answers what changed; a table of applied migrations answers what is in force in each environment at this instant, with no need to *check out* the right commit in each one, the same question the cross-reproduction audit (Vol. 3, Chapter 20) needs answered before replaying a trace against a second provider: which exact version of the composite produced that decision.

**■ EXECUTIVE TRACK: The Minimum Viable Stack for a Team of Three**

| Capability | Sufficient instrument | Typical cost |
|---|---|---|
| Traces and metrics | OpenTelemetry + any backend (free and managed options exist) | Hours of setup |
| Composite versioning | Git + tags + mandatory PR for `prompts/` | Zero |
| Evals in CI | The existing CI runner + batch API at half price | Cents per run |
| Canary | A second consumer group or a routing flag | Hours |
| Alerts | Threshold on CIU, evals, and DLQ in the existing dashboard | Zero |
| Composite migrations | History table (SQLite is enough) + `V00N`/`U00N` convention in `prompts/` | Zero |

The cost column is the argument: none of this discipline demands a new platform or a dedicated team. It demands deciding that the agentic system is a production system, and treating it with the seriousness already given to the rest.

## Worked Exercise 8.1: The Code Review Pipeline's Alerts

**Problem.** Define the review pipeline's minimum alerts (Chapters 15 and 17): condition, initial threshold, and whom each one wakes up.

**Annotated solution.** Five alerts are enough, and none uses an arbitrary absolute value; all compare against the moving baseline of the previous week, because in nondeterministic systems the *change* informs and the absolute value lies:

1. **Quality:** pass rate of the daily eval sample drops > 10 points vs. baseline → the agent's owner (named human, Chapter 1 (Vol. 3)). It is the queen alert; the others usually explain it.
2. **Economics:** pipeline CIU rises > 50% vs. baseline sustained for 2 hours → same owner; typical cause: context inflated by a change in diff size, or a cache broken by a modified prefix.
3. **Latency:** p95 of `task.code-review` (the root trace) exceeds double the baseline → platform on-call; typical cause: a degraded provider; verify before touching anything of your own.
4. **Digestion:** DLQ depth > 5 messages/hour → same-day review; each message is a candidate eval.
5. **Budget:** hard cutoff of hourly spend (Chapter 7) → it pauses itself; the alert informs, it doesn't ask permission.

The design mistake to avoid was deliberately left off the list: alerting on tokens per call. That signal oscillates with every PR and trains the team to ignore alerts; the aggregate metric with a value denominator (the CIU) is the one that deserves to wake someone.

## Key Takeaways from Chapter 8

- Golden signals ([Beyer et al., 2016](#ref-beyer2016)) + synthetic signals: tokens, cache, iterations, tool errors, CIU, evals, DLQ.
- The ReAct loop is a native distributed trace; `agent.prompt_version` on every span turns three days of archaeology into a query.
- LLMOps without ceremony: version the composite, test it in CI, canary via consumer group, drift watched by your own evals ([Sculley et al., 2015](#ref-sculley2015); [Breck et al., 2017](#ref-breck2017)).
- Flyway/Liquibase-style migrations (`V00N`/`U00N`, checksum, strict order per environment) answer what composite is in force right now, not just what changed, and make rollback an audited reversal migration, not a manual edit.
- Alerts compare against a moving baseline; the only absolute-value alert is the budget cutoff, and that one doesn't ask permission.
- The whole stack fits within the budget of a team of three: the barrier is one of decision, not money.
