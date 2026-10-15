# Chapter 5: The Orchestrator's Playbook: Complete Use Cases

This chapter grounds everything so far in six complete systems. The first three (continuous code review, onboarding assistance, and automatic documentation) offer the best value-to-risk ratio for a first serious adoption, and they share a deliberate property: **they fail cheaply**. A bad review gets ignored; a bad onboarding answer gets corrected by asking a colleague; bad documentation gets regenerated. The next three (customer support, assisted research, and the enterprise agent platform) raise the stakes: they touch external users, business decisions, and the entire organization, and they demand the maturity the first three build. For each case: the problem, the architecture, the essential code or design, and the metrics to govern it.

## Case 1: A Continuous Code Review System

**Context.** A team of fifteen engineers with three to five *pull requests* a day. The first review feedback takes hours, blocking delivery; human reviewers burn their attention on mechanical problems (style, obvious mistakes, catalog vulnerabilities) instead of on design.

**Agentic solution.** A pipeline (Chapter 8, pattern 1) triggered by every PR: the reviewer agent analyzes the diff with the domain context (Chapter 6) injected; the security agent, on an economy model, sweeps the OWASP catalog; a synthesizer posts a single, structured comment, with confidence declared per finding. Low-confidence findings are flagged as such rather than omitted (Chapter 5).

![Diagram 5.1: Automated code review pipeline](imagenes/capitulo14/diagrama14_1_en.png)

**The decisive design point:** the system *comments*, it doesn't *block*. The human decides. This keeps the system in the "fails cheaply" category and builds the team's trust with evidence: the fraction of useful comments is measured with reactions (👍/👎) that feed the eval suite (Chapter 13).

**Typical results of the pattern** (ranges observed in deployments of the pattern; exact values depend on the team and the repository): first feedback in minutes instead of hours; early detection of a substantial fraction of mechanical defects before human review; cost per PR of cents: compute it with your own CIUTracker and compare it with the cost of an hour of a senior engineer. Public evidence on AI assistance in development tasks supports the direction of the effect ([Peng et al., 2023](#ref-peng2023); [Ziegler et al., 2024](#ref-ziegler2024)); the magnitude on *your* team will be told by your instrumentation, not by this book.

## Case 2: A Technical Onboarding Assistant

**Problem.** A new engineer takes weeks to become productive, and during that time consumes the team's most expensive resource: the attention of the seniors, answering questions whose answer is already written (in the wiki, in the ADRs, in the commits) but can't be found.

**Solution.** A RAG agent ([Lewis et al., 2020](#ref-lewis2020)) with read-only access to: internal documentation, commit history, resolved tickets, and code. It answers with citations to its sources (the grounding that mitigates hallucination; [Ji et al., 2023](#ref-ji2023)) and, when it doesn't know, says so and suggests whom to ask.

```python
# Example 5.1: Onboarding agent with RAG.
# Key to the design: it answers ONLY from the retrieved documents,
# cites its sources, and declares when it doesn't know.

import anthropic

client = anthropic.Anthropic()

def onboarding_agent(question: str, engineer_context: dict,
                     vector_store) -> str:
    docs = vector_store.search(question, top_k=5)
    sources = "\n\n".join(
        f"[SOURCE {i+1}: {d['path']}]\n{d['content']}"
        for i, d in enumerate(docs)
    )

    response = client.messages.create(
        model="claude-opus-4-8",
        max_tokens=2048,
        system=f"""You are the technical mentor of {engineer_context['name']},
        who joined the team {engineer_context['days_at_company']} days ago.
        Their background: {engineer_context['background']}.

        RULES:
        1. Answer ONLY with information from the sources provided.
        2. Cite the source of every claim: [SOURCE n].
        3. If the sources don't contain the answer, say so explicitly
           and suggest whom to ask. NEVER invent information
           about the system.""",
        messages=[{
            "role": "user",
            "content": f"{question}\n\nRelevant internal sources:\n{sources}",
        }],
    )
    return next(b.text for b in response.content if b.type == "text")
```

**Governance metrics:** fraction of questions answered with a verifiable citation; "I don't know" rate (an honest "I don't know" is a success of the system, not a failure); senior hours freed per week, measured by a short survey.

## Case 3: Technical Documentation That Doesn't Go Stale

**Problem.** Documentation is always out of date, because maintaining it competes with shipping features, and always loses.

**Solution.** A generation skill (Chapter 7, pattern 2) run in CI after every merge to the main branch: it detects the modified files, regenerates the documentation for the affected public interfaces, and opens a documentation PR a human approves in seconds. The processing is asynchronous: a perfect candidate for the batch API at half price (Chapter 11).

```bash
# .claude/skills/auto-docs.md (excerpt of the procedure)
### Process
1. `git diff HEAD~1 HEAD --name-only` -> changed files
2. For each modified Python/TypeScript file:
   a. Read the current file
   b. Identify new or modified public functions/classes
   c. Generate docstring + usage example
   d. Update the corresponding docs/ file
3. Open a PR with the docs/ changes (never a direct commit to main)
```

**The detail that matters:** the agent opens a PR; it doesn't write straight to the main branch. The cost of human approval is seconds; the value (that no agent error reaches the canonical documentation without human eyes) is the principle of Chapters 14 and 19 applied to an everyday case.

## Case 4: Customer Support with Honest Escalation

**Problem.** A support team handles queries where 60–70% are repetitive (order status, configuration, billing) and the rest require human judgment. The previous generation's chatbots failed because of a design flaw: they didn't know how not to know.

**Architecture.** An economy router classifies each query into three routes. *Green route:* queries resolved with read-only tools (order status via API, help articles via RAG with citations): the agent responds directly. *Yellow route:* the agent drafts a proposed response a human approves with one click, the Case 3 pattern applied to customers. *Red route:* immediate escalation to a human with the context already gathered and summarized, and the agent's contribution is that the customer doesn't repeat their story. The design rule that governs everything: **when in doubt about the route, take the most conservative one**. The router's confidence threshold is versioned configuration, not the model's judgment.

**The metrics that matter**, and the ones that mislead: the automatic resolution rate is the vanity metric; it rises easily by *making the system worse* (safe but useless answers). The honest ones: reopen rate by route (did the green answer actually resolve it?), correct escalation rate (sampled by humans: was the red route really red?), and satisfaction measured by route, never aggregated. Cost per query (cents on the green route) is compared against the human channel's cost *only* for the queries the human no longer handles; comparing overall averages is creative accounting.

**Why this case is fourth and not first:** it touches customers. It demands the mature eval suite (Chapter 13), the guardrails of Chapter 4 (the support channel is a direct-injection surface by definition), and a critical actions policy (Chapter 1 (Vol. 3)): the support agent *proposes* refunds; it never executes them.

## Case 5: The Research Agent with Citations or Silence

**Problem.** Technical and product decisions that require synthesizing scattered sources (documentation, comparisons, literature, internal discussions) consume days of the organization's most expensive people, and the result usually lives in a chat thread nobody finds again.

**Architecture.** A three-phase pipeline with an explicit budget per phase. *Collection:* parallel search (fan-out, Chapter 8) over internal (RAG) and external (web search with tools) sources, with limits on sources and tokens. *Synthesis:* the top-tier model produces a structured report in which **every claim carries its source**: the onboarding rule (Case 2) elevated to a deliverable. *Contrast:* a second agent (the adversary of the council pattern) actively looks for evidence against the first's conclusions and appends the tensions found. This third phase, which almost everyone omits because of cost, is what separates a useful report from a dangerous one: the practice of refutation with evidence (understanding the thesis before rebutting it, backing each refutation with proof) applied by design (see "Author's Public Work").

**The metrics:** fraction of claims with a verifiable source (audited by sampling); hallucination rate detected in the contrast (if it is sustainedly zero, the adversary isn't working); expert time saved, measured by survey; and the hard budget limit per report: research is the use case with the highest Token-Burn risk in the catalog, because "searching a little more" always seems justified.

## Case 6: The Enterprise Agent Platform

**Problem.** After Cases 1 through 5, the organization has half a dozen agents in production, and each one was born with its own infrastructure. The problem is no longer building agents: it is that twenty teams can build them without repeating the mistakes the first five already paid for.

**Architecture.** This case doesn't add an agent: it adds the **internal product** that contains them all, and it is the culmination of the entire book. Its components are the earlier chapters turned into a service: the multi-provider gateway with budgets (Chapter 3) as the single door; the MCP server catalog with owners and security review (Chapter 9); the library of versioned skills and master prompts (Chapters 5 and 7); the eval harness as a CI service (Chapter 13); observability with traces and synthetic signals (Chapter 8); and the agent registry with a named human owner, a list of critical actions, and audit (Chapters 14 and 19). The platform team operates it as a product: with a roadmap, internal users, and adoption metrics ([Skelton & Pais, 2019](#ref-skeltonpais2019)).

**The metric that sums them all up:** the time from "a team has an idea for an agent" to "that agent operates in governed production": with inventory, budget, evals, and an owner. Without a platform it is measured in months and governance is optional; with one, in days and governance is the path of least resistance. That investment, making the right thing the easy thing, is the operational definition of a mature platform, and the end state this playbook leads to.

## Case 7: Multi-Provider Swarm Parallelism

### The Problem This Case Introduces

Cases 1 through 6 assume one agent, or a small, homogeneous group, is enough. Past a certain volume (processing thousands of tickets, refactoring an entire monorepo, researching dozens of sources in parallel) the constraint stops being the model and becomes how many agents a single orchestrator can coordinate without losing consistency. This case documents how the four most relevant providers solve that problem today, with each one's real syntax, so that the decision about which swarm to couple to is an engineering decision and not a brand preference.

### Common Architecture, Different Syntax

All four converge on the same pattern: an orchestrator decomposes the task, hands independent subtasks to workers that run in parallel, and a synthesis phase gathers the results, the same *fan-out/gather* from Chapter 8, now exposed as an SDK primitive instead of a hand-drawn pattern. The Agnostic Backend principle (Vol. 2) demands treating that primitive as interchangeable:

- **Claude (Agent SDK / Claude Code).** The *Task tool* dispatches subagents from a conversation; each runs in its own context and, if it touches files, in its own *git worktree* to avoid write collisions. For swarms that exceed what a single conversation can coordinate turn by turn, the SDK exposes a *Workflow tool*: Claude writes the orchestration script in code and hands it to a runtime that executes it in the background, with three primitives: `agent()` for an individual worker, `parallel()` as a synchronization barrier, and `pipeline()` for chaining results without a barrier.

```javascript
// Conceptual excerpt of an Agent SDK workflow
const findings = await parallel([
  agent('researcher-A', { source: 'internal-docs' }),
  agent('researcher-B', { source: 'web-search' }),
  agent('researcher-C', { source: 'github-issues' }),
]);
const report = await agent('synthesis', { inputs: findings });
```

- **OpenAI (Agents SDK).** The coordination primitive is the **handoff**: one agent hands control to another, treating it almost like one more tool, with no central hierarchical dispatcher. For truly parallel work, the SDK runs agents or tool calls in parallel and aggregates the results; *guardrails* (input and output validations) also run in parallel with the main call, to fail fast without penalizing the happy path's latency.

```python
from agents import Agent, handoff

triage = Agent(
    name="Triage",
    handoffs=[handoff(researcher_a), handoff(researcher_b)],
)
```

- **Google (Agent Development Kit).** It is the most explicit of the four: `ParallelAgent` runs sub-agents in isolated branches (with no shared memory between them during execution), and each writes its result to a session state key (`output_key`) that a final agent, normally a `SequentialAgent`, reads to synthesize. Dispatch to a sub-agent is a typed function call (`transfer_to_agent`), which makes coordination failures appear in the trace as ordinary *tool-calling* failures, auditable on the same dashboard that audits any other tool.

```python
from google.adk.agents import ParallelAgent, SequentialAgent

collection = ParallelAgent(
    name="collection",
    sub_agents=[researcher_a, researcher_b, researcher_c],
)
pipeline = SequentialAgent(sub_agents=[collection, synthesis])
```

- **Kimi K2.6 (Moonshot AI, open source).** It is the most aggressive on scale and the most relevant to the Agnostic Backend on price: its *Agent Swarm* mode dispatches up to 300 specialized subagents and chains up to 4,000 tool steps in a single autonomous run, at a fraction of the per-token cost of the other three (Moonshot reports execution time reductions of up to 80% versus a single agent). It doesn't expose a `ParallelAgent` class of its own: parallelization happens inside the tool call, the model returns several entries in the same `tool_calls` array when it detects independent subtasks, and the client executes them and responds in the same turn.

### The Table an Architecture Committee Needs to See

| Provider | Parallelism primitive | Documented ceiling | Isolation between workers | Relative cost |
|---|---|---|---|---|
| Claude (Agent SDK) | `parallel()` / `pipeline()` in the Workflow tool; Task tool for in-conversation subagents | Dozens, bounded by task design, not by the SDK | Own context; optional git worktree | High (frontier) |
| OpenAI (Agents SDK) | Handoffs + parallel execution of agents and tools | No published hard limit | Own session per agent | High (frontier) |
| Google (ADK) | `ParallelAgent` with `output_key` + synthesis `SequentialAgent` | No published hard limit | Isolated branches, no shared memory | Medium-high |
| Kimi K2.6 (Moonshot) | Agent Swarm inside `tool_calls` | 300 subagents / 4,000 steps (documented) | Per specialized subagent | Low (open source) |

### Why This Reinforces the Agnostic Backend and Doesn't Contradict It

No provider invented the pattern: all four implement the same orchestrator-worker pairing that Chapter 8 described before a single line of SDK existed for it. What changes between rows of the table is the dispatch syntax and the scale ceiling, not the underlying architecture. A well-designed multi-provider gateway (Chapter 3) doesn't adopt a swarm SDK as a platform decision: it exposes an internal interface of "dispatch N independent subtasks and synthesize" and translates that interface to the SDK currently in force. When the successor
 of Kimi K2.6 or Astra's successor publishes a ceiling of a thousand subagents, the change is absorbed in that translation layer, without touching the code that orchestrates the business.

### Astra as a Case Study of the Upper Limit

GPT-6 Astra ([OpenAI, September 2026](#ref-openai2026sept)) doesn't introduce a new SDK primitive (it uses the same Agents SDK described above), but it is the most-cited field test of how far the pattern scales: independent evaluators document runs of 20 to 96 subagents coordinated by a single manager agent, applied to maintenance tasks (labeling data, reading logs, debugging deployments, keeping pipelines saturated) at a measured cost under six dollars per compute hour. This automates precisely the portion of the AI Engineer's work (Chapter 2) that that chapter already identified as lowest in added value: the routine supervision of runs. It leaves intact the portion Chapter 2 requires to remain human: architectural judgment, verification of the irreversible, and responsibility for the signature. The Platform Engineer (Chapter 3) covers different ground from Astra's: deciding where a swarm of 96 agents is allowed to act without synchronous supervision, and where not.

## Case 8: Promotion Between Environments and Dependencies Between Teams and Third Parties

### The Problem This Case Introduces

The seven previous cases describe architecture within an environment. In practice, every agent is born in development, goes through stage, sometimes through QA as a separate environment, and only at the end reaches production, and at each jump the credentials, the token budget, the tolerable failure surface, and above all which MCP servers from other teams or third parties it has access to all change. An agent that in development calls the Payments team's billing MCP server without friction can't inherit that access in production without Payments knowing, approving it, and assigning it its own error budget. This is the case where most of this book's incidents start: not from a poor agent design, but from an environment jump nobody modeled.

### The Environment as an Autonomy Parameter, Not Just a Configuration One

What usually varies between environments (URLs, keys, rate limits) still varies here, but a dimension is added that almost no team versions explicitly: the **autonomy ceiling** permitted by the levels framework of Chapter 1. The same agent can operate at Level 3 (tools, with a budget) in development and be restricted to Level 1 (fixed chain, reviewed) in production until it accumulates enough evidence.

| Environment | Autonomy ceiling | Access to third-party MCP | Who approves the promotion |
|---|---|---|---|
| Development | Level 3–4 (agent with tools or multi-agent) | Sandboxes or contract *mocks*, never the real service | The team itself |
| Stage | Level 2–3 | Replica of the real service with synthetic data | The team, with platform review |
| QA | Level 2 | Real third-party service, in *shadow* mode (read-only, no writes) | Platform + the owner of the depended-on service |
| Production | The level the QA evidence supports, never more | Real service, with budget and scope signed by the owning team | Architecture committee or its delegate (Chapter 6) |

Promotion from one environment to another is not just another *deploy*: it is a request for autonomy that must present its own evidence, with the same rigor Chapter 6 requires for the eval harness.

### Dependencies Between Teams: The Versioned MCP Contract

The MCP server catalog with owners (Chapter 9, revisited in Case 6) resolves who is responsible for each tool, but it doesn't resolve what happens when that owner changes the shape of their tool. The answer, taken from a discipline already mature in REST APIs, is consumer-driven contract testing (popularized by tools such as Pact): each team that consumes another's MCP server publishes, alongside its own agent, an executable contract of what it expects to receive. The owning team's pipeline runs those contracts before every change; if another team's contract breaks, CI/CD blocks it before it reaches stage, not after the consuming agent fails in production with nobody understanding why.

### Dependencies with External Third Parties: The Same Principle, with Less Control

When the MCP server belongs not to another internal team but to an external provider (a bank, a payment gateway, a government API like those in the sector case), the executable contract is rarely negotiable. What is negotiable is the **degradation budget**: defining in advance what the agent does when the third party changes without notice, responds slower than expected, or goes down outright (read-only mode, retry queue with backoff, or immediate escalation to a human) and testing that degraded mode in stage with the same rigor as the happy path. A swarm of 96 coordinated agents (Case 7) that depends on a third party with no degraded mode is not a resilient swarm: it is a single external API with a damage multiplier.

### The Registry of Dependencies, Not Just of Agents

The agent registry with a named human owner (Chapter 6, Case 6) extends here to a **dependency registry**: for each agent in production, which internal and external MCP servers it consumes, at what autonomy level, and what degraded mode it has if each one fails. When the Payments team announces it is retiring a version of its MCP server, this registry is what makes it possible to answer in minutes "these three agents from these two teams depend on it" instead of finding out through a production incident.

In sum, the nine cases form a deliberate ladder. The first three teach the basic capabilities with bounded risk: agents that *read* (Case 1), that *answer* from internal knowledge (Case 2), that *write* with human approval (Case 3). The next five compose them at scale: toward the customer (Case 4), toward decisions (Case 5), toward the entire organization (Case 6), toward the parallelism ceiling each provider allows today (Case 7), toward the crossing of environments and teams that decides whether everything above survives production (Case 8), and toward the unattended or remote operation that frees the human from the desk without freeing them from responsibility (Case 9). Each rung reuses the infrastructure of the previous one (gateway, evals, audit) and produces the CIU data to decide whether the next rung is worth its cost. Skipping rungs is possible; paying for them twice is the usual result.

## Case 9: Background Agents at Scale and Remote Orchestration

### The Problem This Case Introduces

The eight previous cases assume someone is at the screen directing the agent. Beyond a certain organizational scale, that assumption breaks: the task is too big for an interactive session (thousands of migrations in a twenty-million-line monorepo) or the responsible engineer simply isn't at their computer when the agent needs a decision. This case documents how two real solutions, of different natures, solve each half of the problem.

### Spotify: The Background Agent as a Staff Worker, Not a Copilot

Spotify runs a coding agent built on the Claude Agent SDK that runs in the background, not in an interactive session: it receives a migration task (updating a dependency, propagating an API change across thousands of services), executes it without synchronous supervision, and opens a *pull request* for human review. The figure that makes the scale tangible: more than 650 PRs generated by this agent are merged to production every month, on a codebase of more than twenty million lines (Spotify Engineering, 2026). The prompts that direct the agent live versioned in Git (the same migrations pattern from Chapter 8 applied to the source, not just to the application history), and a Slack bot triggers one-off tasks for cases that don't merit a scheduled run.

What makes this case transferable, beyond the figure, is the architecture: the background agent doesn't replace the fan-out pattern of Chapter 8 (Vol. 1), it deploys it at the scale of an entire engineering organization. Every PR it produces is, in effect, an anonymous worker of an implicit swarm, with the same traceability aspect requirement from Chapter 8: without a record of which versioned prompt produced each PR, that volume would be impossible to audit when something goes wrong.

### Remote Orchestration: The Same Pattern, with the Human on the Move

The second problem (the engineer who needs to step in but isn't at their desk) is solved by a different capability: remote control of a Claude Code session from the phone (`claude --remote-control`, in preview since February 2026), which generates a QR code or link to continue the session from the mobile app or the browser. The session keeps running on the engineer's local machine (the file system, MCP servers, and tools never leave it); the phone is just the interface for approving actions, queuing tasks, or redirecting the work midway.

### Minimal Guide to Trying It

1. Start a Claude Code session on the work machine with the remote control flag enabled.
2. Scan the generated QR code from the Claude mobile app.
3. Define in advance which actions require explicit approval from the phone (the permissions fence from Chapter 20, Vol. 3, applies equally from a cell phone as from a keyboard).
4. Use the task queue to leave work prepared that the agent runs as soon as compute budget frees up, with no need for the engineer to be present at the start.

### Why These Two Cases Are the Same Architecture, Not Two Different Tools

Spotify's background agent removes the human from the synchronous loop for low-risk, high-volume tasks; remote control keeps the human in the loop but decouples them from a fixed desk. Both are variations of the same principle from Chapter 5, Case 8: the autonomy ceiling is not a property of the agent, it is an architectural decision about when and from where human supervision is exercised.

## Case 10 (Sector-Specific): Bounded Agents in a Mission-Critical System

The nine previous cases are horizontal: they apply to almost any software organization. The chapter closes with a *vertical* case (a mission-critical system in a regulated, high-risk domain) because it teaches a lesson the horizontal ones can't: in these systems, the right question is "where should there *not* be one, and how narrow must it be where there is?", not "where do I put an agent?" The example, based on an architecture the author designed and published (see "Author's Public Work"), is a platform for reporting extortion complaints that integrates citizens, police, prosecutors, and even data capture by IoT and drones.

![Diagram 5.2: Architecture of an extortion complaint system, the overwhelming majority is conventional engineering (PCI environment with MFA, microservices by domain, integration with State APIs, distributed security with anonymity, encryption, and audit); the agentic contribution is deliberately narrow (figure published by the author).](imagenes/capitulo14/denuncias_extorsion_es.png)

### The First Thing the Diagram Teaches Is How Much Is *Not* AI

The PCI environment with multi-factor authentication, the load balancer and API versioning, the microservices separated by domain (registration, analysis, query, case management, notifications), the REST integration with the APIs of the Ministry of the Interior, the National Police, and the Prosecutor's Office, and the distributed security layer (complainant anonymity, encryption in transit and at rest, access logging, audit, and monitoring) are classic engineering, and must stay that way. In a system where a failure puts a person's physical safety at risk, determinism is not a style preference: it is a safety requirement. The rule from Chapter 1 (Vol. 3) (the agent proposes, the human approves the irreversible) hardens here into a design principle: no action with legal or security consequences hangs on a probabilistic decision.

### Where the Agent Fits, Then, and Why So Narrow

Three points, all read-only or supervised drafting, none of autonomous action. The first is the **analysis microservice**: it classifies and prioritizes incoming complaints (urgency, pattern of recidivism, link to open cases) so a human analyst handles first what matters most; it is triage, Case 4 elevated to a domain where being wrong is expensive, and that is why its output is a *priority recommendation with its evidence*, never an automatic filing. The second is **anonymity as assisted redaction**: a bounded agent detects and masks information that could identify the victim before the complaint circulates among agencies, with human review of the low-confidence fraction (the Case 3 pattern). The third is the **enrichment of IoT and drone data**: classifying and summarizing the telemetry and evidence stream for the control panel, the *CDC → enriching agent → consumers* pattern Chapter 7 formalizes, operating on the stream without touching the source databases (structural least privilege, Chapter 4).

### The Lesson That Generalizes

In high-risk domains, the agent's value lies not in automating the decision but in *sharpening human attention toward it*: prioritizing, masking, summarizing, enriching. The system stays deterministic in its backbone; the agent lives at its margins, where an error translates into "a human looks at something in a different order," not "a complaint gets lost." Designing this way is not technological timidity: it is the literal application of the security principles (Chapter 4) and the critical actions policy (Chapter 1 (Vol. 3)) to a domain that doesn't forgive. The complete playbook, then, is not a list of places to put agents; it is the criterion for deciding how narrow each one must be; and in the systems that matter most, the right answer is usually "narrower than enthusiasm suggests."

## Key Takeaways from Chapter 5

- Start with what fails cheaply: a review that comments, onboarding that cites, documentation that proposes PRs.
- The advanced cases demand the maturity of the basic ones: support with three routes and conservative doubt; research with citations and an adversary; a platform as a product.
- Vanity metrics (automatic resolution, volume generated) rise while making the system worse; honest ones have a value denominator and are measured by route.
- The agent proposes; the human approves the irreversible. In all six cases, without exception.
- The platform makes governance the path of least resistance: that is the playbook's final goal.
- In mission-critical domains the agent lives at the margins (prioritizing, masking, summarizing, enriching), not in the deterministic backbone: it sharpens human attention, it doesn't replace the decision.
- Claude, OpenAI, Google, and Kimi implement the same orchestrator-worker pattern with different syntax (Task tool/Workflow, handoffs, ParallelAgent, Agent Swarm): the multi-provider gateway translates, the business isn't rewritten.
- The environment doesn't just change credentials: it changes the permitted autonomy ceiling. Promoting from stage to production is a request for autonomy with evidence, not just another deploy.
- Dependencies between teams are governed with consumer-driven contracts; dependencies with external third parties, with a degradation budget tested in stage. Both are registered alongside the agent that uses them, not just the agent.
- A background agent with no interactive session (Spotify) and a remote session controlled from the phone are the same architectural decision seen from two angles: where and when human supervision is exercised, not whether it exists.
