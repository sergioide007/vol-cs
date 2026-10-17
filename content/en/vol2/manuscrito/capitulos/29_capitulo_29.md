# Chapter 29: Cline and Continue

> *The most powerful extension is not the one that does the most. It is the one that disappears when it isn't needed and acts when it is.*

## The Territory: Agents That Stay in VS Code

While one part of the ecosystem decided to build entire IDEs (Vol. 2, Chapters 30 and 31), another part bet on something different: bringing full agency inside VS Code without breaking the programmer's flow. Cline and Continue are the two most influential examples of that bet. They don't compete with each other (they solve adjacent needs), and together they mark the two ends of the spectrum between *autonomy* and *context*.

## Cline: The Autonomous Agent

Cline (formerly known as Claude Dev) started from a radical premise: if a model like Claude can reason about code, why limit it to answering questions in a chat window? The answer was to make it a full agent inside VS Code.

### What Cline Can Do

From a single instruction, Cline can:

- Read the project's file tree and understand its architecture
- Edit several files in a coordinated way
- Run commands in the integrated terminal and read their output
- Browse web pages to look up documentation or errors
- Call MCP servers (Chapter 9) to interact with external services

All of this happens in an **autonomous loop** that interrupts only when it detects an irreversible action (deleting a file, running a destructive command) or when the model needs clarification. The programmer supervises rather than micromanaging.

### Cline's Architecture

Cline is open source (MIT license) and modeled on Anthropic's Agent SDK, although it accepts any provider compatible with the OpenAI API. Its design separates the **reasoning core** (the LLM, which is interchangeable) from the **toolset** (file system, terminal, browser), joined by a normalized interface. That separation makes it possible to switch from Claude to GPT-4o or to a local model without touching the agent logic.

![Diagram 29.1: Cline's Architecture](imagenes/capitulo76/diagrama76_vscode_extension_en.png)

*Diagram 29.1: Cline's architecture: the model is interchangeable, and the tools are stable.*

### The Human Confirmation Pattern

Cline implements a pattern that earlier chapters describe in theory: **autonomous action with human checkpoints**. Before running a shell command or modifying a critical file, it asks for confirmation. The granularity is configurable: the programmer can approve whole categories (for example, "edit .ts files without asking") and save confirmation for higher-risk operations.

## Continue: The Contextual Assistant

Continue (continue.dev) starts from a different philosophy. Instead of autonomy, it bets on **depth of context**. Its premise is that the programmer's biggest obstacle is not writing code but the fact that the model doesn't know what the rest of the repository does when it suggests a change.

### Repository Indexing

Continue indexes the entire repository at startup and keeps that index up to date. When the programmer asks, "refactor this function to be consistent with the authentication module's pattern," Continue pulls the relevant files from the index and includes them in the context before sending it to the model. The result is an AI that *knows the codebase*, not just the open file.

### Privacy and Local Models

Continue supports local models through Ollama, so the code never leaves the machine. That makes it the natural choice for teams with privacy constraints (banking, healthcare, defense) where sending code to an external API is not acceptable.

| Dimension | Cline | Continue |
|---|---|---|
| Usage model | Autonomous agent | Contextual assistant |
| Autonomy | High | Medium |
| Privacy | External API (configurable) | Local possible |
| Strength | Complex end-to-end tasks | Consistency with the repo |
| Multi-agent integration | Native MCP | Repository RAG |

*Table 29.1: Positioning comparison.*

## The Connection to the Multi-Agent Paradigm

Neither tool is an island. Cline can act as a **local orchestrator** (it invokes MCP servers, delegates subtasks to specialized agents, and returns the result to the programmer), linking the IDE with the agentic ecosystem described in earlier chapters. Continue acts as a **context retrieval layer** (RAG applied to code): it retrieves the relevant knowledge before any agent makes a decision about the repository.

Used together, with Continue as the knowledge layer and Cline as the executor, they form a two-layer system that embodies the principle from Chapter 8: separate *knowing* from *doing*.

## The Executive View: IDE Agents as a Measurable Productivity Lever

**■ EXECUTIVE TRACK**


From the standpoint of product leadership and engineering team management, bringing agents into the IDE is not a tooling upgrade; it changes the production model for software. The implications for product owners, scrum masters, and software architects deserve to be spelled out.

**Impact on team velocity.** Data published by GitHub in the *Copilot Impact Report 2023* (for an assistant less autonomous than Cline) documents a 55% reduction in the time needed to complete standard programming tasks. For agents that can act autonomously, like Cline, the multiplier is larger on tasks that are complex and repeatable: dependency migrations, test generation, and refactorings with a well-defined pattern. The gain is not linear; the tasks that benefit most are exactly the ones that used to eat the most time in sprints.

**Implications for the Definition of Done.** When an autonomous agent can generate, run, and fix tests in a loop, the DoD of a user story has to be updated. The criterion "all tests pass" becomes "all tests pass *and were reviewed by the programmer*," not simply written and run by the agent. This distinction (human review of the quality of the tests, not just of their result) matters operationally for teams that use Cline as an executor.

**The risk of accelerated technical debt.** The same mechanism that speeds up code production can speed up the buildup of technical debt if no explicit review policy is in place. An agent that produces 200 lines of code in 5 minutes can produce 200 lines with excessive coupling, missing abstractions, and low-quality tests in the same time. The answer is not to limit the agent but to set stricter code review criteria for agent-generated code, putting architecture ahead of functionality in code review.

**Continue as an onboarding accelerator.** One executive use of Continue that doesn't get enough attention is onboarding new engineers to large codebases. A new engineer who can ask conversational questions about a 500,000-line repository ("how is the retry pattern implemented in the payments module?", "what does this service do when the external provider returns a 429?") shortens their onboarding curve from weeks to days. In this context, the ROI of Continue can be measured directly in onboarding hours saved.

## Benchmarks and Impact Validation

The research of Peng et al. (2023), *The Impact of AI on Developer Productivity: Evidence from GitHub Copilot* (published as a working paper of the National Bureau of Economic Research), provides empirical evidence that LLM-based code assistants speed up task completion by 55.8% in randomized controlled experiments. It is the most methodologically rigorous study available on the impact of coding agents, and its method can be applied to evaluating Cline and Continue in production.

For software architects weighing whether to adopt these tools, the Peng et al. method offers an evaluation framework: measure task time on a representative set of the team's tasks, with and without the assistant, using random assignment. The number that comes out of that experiment is worth more than any benchmark published by the tool vendors themselves.

## Key Takeaways from Chapter 29

- Cline is an open-source autonomous agent for VS Code: it edits, executes, browses, and calls MCP tools in a supervised loop.
- Continue is a contextual assistant that indexes the whole repository and can run with local models.
- Both are model-provider agnostic.
- Cline as a local orchestrator plus Continue as the RAG layer form a two-layer system of agency and contextual intelligence.
- Executive view: the DoD has to be updated when an agent generates code, and Continue speeds up onboarding of new engineers to large codebases.
- The empirical evidence (Peng et al., 2023, NBER) documents a 55% speedup on programming tasks with code assistants, the most rigorous benchmark available.
