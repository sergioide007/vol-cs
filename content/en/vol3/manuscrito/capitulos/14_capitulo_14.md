# Chapter 14: Katas for AI Agents Competing for a Prize of Their Own

> *A kata is not designed so the agent gets it right, but to reveal how it reasons when it might get it wrong.*

## The Kata as a Test Bench for Reasoning Under Constraints

In the software craftsmanship tradition, a *kata* is a repeatable exercise designed not to produce a useful result but to **sharpen the performer's technique**. Dave Thomas, co-author of *The Pragmatic Programmer*, popularized the concept for code: small, well-defined problems solved over and over under different constraints until the solution becomes natural and instinctive. The kata doesn't train the solution; it trains the solver.

Carried over to the domain of AI agents, the kata takes on a radically different meaning: **it doesn't train the agent** (the model is already trained and its weights don't change during the test), but **reveals the architecture of its reasoning under constraints**. That is extraordinarily valuable, because what an agent does under constraint (of time, tools, format, or cost) exposes the core of its reasoning process in a way unconstrained tasks do not.

Inspired by software architecture gatherings like the ones the author mentions (where figures such as Sam Newman, author of *Building Microservices*, moderate debates among architects about the same design decisions), you can imagine an equivalent format for agents: different agents attack the same architectural problem, and a mixed panel of human and synthetic evaluators judges not only the result but the path, the trade-offs made explicit, and the coherence of the justification.

## Existing Competitions: SWE-bench, AgentBench, and WebArena as Formal Katas

Academia has already produced a set of benchmarks that work, in practice, as formal katas for agents: well-defined problems with explicit constraints, verifiable success criteria, and a standardized evaluation panel. Analyzing them reveals which capabilities are really hard for current agents.

**SWE-bench** (Jimenez et al., 2024, ICLR 2024): perhaps the most revealing benchmark published so far. Framed as "can language models resolve real GitHub issues?", it consists of 2,294 tasks drawn from real Python code repositories, where the agent must modify the source code to fix a bug or implement a feature, passing the issue's tests. In early 2024, the best models resolved under 5% of the tasks; by the end of 2024, the best multi-agent systems (Claude 3.5 Sonnet with code editing tools) reached 49%. The jump from 5% to 49% in twelve months is the strongest empirical evidence available for the value of multi-agent architecture over the isolated model.

**AgentBench** (Liu et al., 2024, ICLR 2024): evaluates agents in eight distinct interactive environments (web browsing, operating system use, databases, games, and more) that require taking sequential actions with real consequences in the environment. The benchmark revealed that models' capability in interactive environments is significantly lower than on question-answering tasks: the best models reached ~70-80% on static QA and only 40-50% on interactive agentic tasks, a 30% gap that captures exactly the difference between knowing and acting.

**WebArena** (Zhou et al., 2024, ICLR 2024): evaluates agents' ability to complete tasks in realistic web environments (buying a product, making a reservation, interacting with simulated social networks) through real user interfaces. The difficulty of navigating interfaces designed for humans, not for agents, produced initial success rates of only 14-18% for the best models. The benchmark is a particularly demanding kata because the adversarial environment (designed without the agent's perspective in mind) has no shortcuts.

These three benchmarks are, in essence, formalized katas the scientific community uses to calibrate the state of the art. Teams that adopt them internally (adapted to their specific domains) get a precise sensor for the real capability of their systems, far more honest than synthetic benchmarks.

## The Provocative Twist: The Agent Competes for Its Own Prize

Here lies the chapter's boldest idea, the one that deserves to be examined with technical precision before being accepted or rejected. What happens if the contest's incentive is made explicit to the agents themselves as part of their objective function, not as a metaphor but as a design parameter?

This is not about anthropomorphizing ambition or attributing motivations to the agent that it doesn't have. It is something more precise and more interesting: designing **objective functions in which each agent maximizes an explicit reward** that depends on its performance relative to other agents attacking the same problem. Competition structured this way brings out behaviors that pure cooperation tends to suppress.

An agent that knows its answer will be judged against those of other agents with the same resources tends, when the system is well designed, to:
- Justify its choices more explicitly (because the evaluator can compare justifications)
- Anticipate objections to its solution (because another agent will raise them)
- Refine the solution beyond the first acceptable draft (because "acceptable" isn't enough to win)
- Be more precise in the claims it makes (because wrong claims are more visible in a comparison)

These behaviors emerge not from the explicit instruction "be more careful" but from the competitive structure of the objective function. Controlled rivalry is, paradoxically, a more effective engine of quality than a direct quality instruction, precisely because it works on incentives instead of instructions.

## Objective Function Theory in Competitive Agents: The Technical Foundation

The theoretical foundation for competitive agent katas lies in the literature on multi-agent systems with mixed objective functions (cooperative and competitive). In the formalism of game theory, a swarm in which agents maximize individual objective functions in a shared environment is a **zero-sum** or **variable-sum game**, depending on the structure of the rewards.

For a well-designed agentic kata, the objective function has three components:

```
R_agent(i) = w₁ · Q_result(i) + w₂ · Q_reasoning(i) + w₃ · Q_efficiency(i)
             - w₄ · Hallucination_penalty(i)
             + w₅ · First_place_bonus
```

Where:
- **Q_result**: quality of the final result (deterministic if there is ground truth, model-based if not)
- **Q_reasoning**: quality of the exhibited reasoning process (judged by an LLM or a human)
- **Q_efficiency**: inversely proportional to the tokens, time, or tool calls used
- **Hallucination_penalty**: cost for incorrect or fabricated claims that are detected
- **First_place_bonus**: a relative incentive for beating the competitors in the specific scenario

The weights w₁-w₅ are not fixed; they vary with the kata's objective. An efficiency-oriented kata assigns a high weight to w₃; a kata oriented to reasoning quality assigns a high weight to w₂. Varying the weights across different katas of the same problem reveals dimensions of agentic behavior that no kata with fixed weights can capture.

## Anatomy of a Complete Agentic Kata

A well-structured agentic kata has five elements that can't be omitted without degrading its diagnostic value:

| Element | Function | Quality criterion |
|----------|---------|---------------------|
| **Constrained problem statement** | Defines the problem with explicit limits (latency, cost, consistency, available tools) | Minimal ambiguity; verifiable constraints |
| **Heterogeneous competitors** | Different agents with different base models, strategies, or configurations | Enough diversity for qualitatively different approaches to emerge |
| **Mixed judging panel** | Human evaluators + an evaluator agent with explicit criteria | Criteria agreed before the kata; disagreements documented |
| **Explicit objective function** | The reward each agent maximizes, with weights known to all participants | Transparency: all agents know the criteria before starting |
| **Structured retrospective** | Analysis of *why* the winning solution won, not just *what* won | Extraction of generalizable patterns, not just celebration of the result |

The structured retrospective is the most frequently omitted element and the most valuable. Without it, the kata produces a ranking but no learning. With it, the kata produces a catalog of patterns the team can reuse in real systems.

## Designing Internal Evaluations: A Technical Guide for Teams

**► TECHNICAL TRACK**


Transposing competitive katas to the organizational context requires adapting the academic elements to the team's needs and constraints. A minimal technical guide for implementing the first internal kata:

**Step 1: Choose the problem domain**: pick a real problem from the production system where there is genuine ambiguity about the best solution. Architectural design problems are especially suitable because they have multiple defensible solutions with different trade-offs.

**Step 2: Define operational constraints**: state explicitly which tools each agent has available, what the token or time budget is, and which system constraints must be respected. The constraints make the kata; without them, it's just an LLM query.

**Step 3: Configure the competitors**: deploy three to five agent instances with different configurations (different base models, different system prompts, different tools, different temperatures). Diversity of configuration produces diversity of approaches.

**Step 4: Explicit evaluation criteria**: agree before the kata on how each dimension of the objective function will be evaluated. Without prior agreement, the retrospective turns into a debate about the criteria instead of the results.

**Step 5: Retrospective with pattern extraction**: don't just discuss which agent won; extract the generalizable patterns of the winning solution and the avoidable errors of the losing ones. Document the patterns as team knowledge (cf. Chapter 31).

## Why the Agentic Kata Educates Its Designers

The least obvious and highest-impact benefit of the agentic kata is its formative value: beyond evaluating agents, it **educates the engineers and architects who design them**. This educational effect is qualitatively different from reading a paper or attending a conference.

Watching five agents attack the same architectural problem (some choosing strong consistency, some availability, some a hybrid) illuminates the trade-offs with a clarity no theoretical treatise matches. The trade-offs stop being academic abstractions and become observable differences in behavior: the agent that chose strong consistency fails the low-latency task; the one that chose availability produces inconsistent results in the network partition scenario. The kata turns the trade-offs of the CAP theorem ([Brewer, 2000](#ref-brewer2000)) into observable behavior.

The biggest beneficiary of the kata is not the winning agent; it is the team that designed it, ran it, and analyzed the results. The kata is, ultimately, a learning device for its creators. The agent's prize is, in the end, the learning of the human who watches it.

## The Agentic Hackathon as an Executive Program

**■ EXECUTIVE TRACK**


The agentic kata, scaled to the organizational level, becomes the agentic hackathon: a one- to three-day event where teams of engineers design, implement, and compete with swarms of agents to solve a real business problem. Unlike the classic hackathon (where working software is built in record time), the agentic hackathon produces two outputs at once: a potentially deployable agentic system and a catalog of patterns learned during the competition.

Organizations that ran agentic hackathons in 2023-2024 (Amazon, Google, Salesforce, and numerous mid-sized fintech companies) report three consistent benefits: a faster learning cycle in the domain of agentic AI, identification of internal talent with swarm design abilities that weren't visible in everyday work, and the generation of at least one or two architecture patterns directly applicable to production systems.

**Alternative version (higher academic density):**

The design of competitive exercises for generative artificial intelligence agent systems is an evaluation methodology that surpasses conventional static benchmarks in information density for at least three reasons. First, tasks with explicit constraints induce adaptive behaviors that unconstrained tasks don't activate, revealing dimensions of the agent's reasoning space that stay hidden under standard conditions. Second, the relative comparison between agents with different configurations on the same problem produces a contrastive signal with a high signal-to-noise ratio compared with absolute evaluation systems, where the problem's variance factors are mixed with the agent's variance factors. Third, the structured post-competition retrospective turns the evaluating panel's implicit knowledge into explicit, documented knowledge transferable to the organizational team.

## Key Takeaways from Chapter 14

- The agentic kata doesn't train the agent (whose weights don't change): it reveals the architecture of its reasoning under constraints.
- SWE-bench ([Jimenez et al., 2024](#ref-jimenez2024)): from 5% to 49% resolution of real GitHub issues in 12 months (empirical evidence of the value of multi-agent architecture).
- AgentBench ([Liu et al., 2024](#ref-liu2024)): a 30% gap between performance on static QA (~75%) and on interactive agentic tasks (~45%); it measures the difference between knowing and acting.
- WebArena ([Zhou et al., 2024](#ref-generic2024zhou)): a 14-18% success rate in real web environments; interfaces designed for humans are adversarial katas for agents.
- The competitive objective function (R = w₁·Q_result + w₂·Q_reasoning - w₄·Hallucination_penalty + w₅·Bonus) brings out justification, anticipation of objections, and precision without direct instruction.
- The kata has five elements that can't be omitted: a constrained problem statement, heterogeneous competitors, a mixed judging panel, an explicit objective function, and a structured retrospective.
- The biggest beneficiary of the kata is the team that designed it, not the winning agent: it turns abstract trade-offs into observable behavior.
