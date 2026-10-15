# Chapter 30: Cursor, Windsurf, and Zed

> *When an extension isn't enough, you rewrite the host.*

## The Decision to Break with VS Code

Installing an extension in VS Code has a ceiling. The model lives in the extension, but the editor knows nothing about it: the command palette, the file explorer, the editing flow were all designed before LLMs existed. At some point, several teams reached the same conclusion: to build the editor of the future, they had to build the whole editor.

Cursor, Windsurf, and Zed are the three most influential answers to that conclusion. Each took a different path.

## Cursor: The Fork That Rewrote the Rules

Cursor (cursor.sh) is a fork of VS Code built by Cursor Inc. It keeps full compatibility with VS Code extensions and shortcuts (a programmer who switches loses nothing), but it adds three layers that aren't possible in an extension:

### Tab: Predictive Edit Completion

Cursor's "Tab" doesn't complete the current line. It predicts the **next edit in the file** (including deletions, local refactorings, and multiline changes) and suggests it with a single keystroke. This is not autocomplete; it is predictive editing. The difference is architectural: Cursor trains its own models on editing patterns, not just on text.

### Composer: The Multi-File Change Agent

Composer is Cursor's answer to Cline (Vol. 2, Chapter 29). It takes an instruction in natural language and generates a plan of changes that can span dozens of files. Unlike Cline, Composer does not run shell commands autonomously by default. It proposes the changes, and the programmer approves or discards them file by file.

### Global Semantic Context

Cursor indexes the repository and maintains a semantic graph of relationships between symbols. When the programmer opens the chat with `Ctrl+K`, the context automatically includes the relevant files, without the programmer having to specify them. This indexing happens locally; Cursor does not send the full source code to external servers.

![Diagram 30.1: What a Fork Gains over an Extension](imagenes/capitulo77/diagrama77_ides_en.png)

*Diagram 30.1: What a fork gains over an extension.*

## Windsurf: Codeium's Bet on "Flow"

Codeium started as an autocomplete plugin for VS Code. In 2024 it announced Windsurf: its own IDE (also a fork of VS Code) built around a concept it calls **Cascade**.

### Cascade: The Flow Agent

Cascade differs from Composer in its interaction model. Where Cursor proposes changes step by step, Cascade describes its plan in natural language, carries out a sequence of actions, and presents the final result, keeping the programmer informed without interrupting at every step. Codeium calls this "flow state": the programmer stays in a state of concentration while the agent works in parallel.

Windsurf also has native web search and terminal tools, which gives it an agent architecture similar to Cline's, with the IDE as the unified presentation layer.

### Supermaven Built In

Codeium acquired Supermaven (known for its one-million-token context for autocomplete) and built its engine into Windsurf. The result is code completion with full-repository context, without the window limits that affect other solutions.

## Zed: A New Editor, Not a Fork

Zed makes a different choice. Instead of starting from VS Code, it built an editor from scratch in Rust, optimized for speed and real-time collaboration. AI was not added afterward; it was part of the design from the start.

### Zed's Integration Model

Zed integrates LLMs directly into the editor with no extension layer in between. The model sees the active file's context, the LSP errors, and the history of recent changes as part of its native context. Latency is noticeably lower than with equivalent extensions because there is no serialization between the editor and the model.

| IDE | Base | Main agent | Strength |
|---|---|---|---|
| Cursor | VS Code fork | Composer | VS Code compatibility + predictive Tab |
| Windsurf | VS Code fork | Cascade | Continuous flow without interruptions |
| Zed | Native (Rust) | Direct integration | Speed and collaboration |

*Table 30.1: Comparison of the three AI-native IDEs.*

## The Extension Ecosystem Dilemma

The biggest cost of leaving VS Code is invisible: the ecosystem. Tens of thousands of extensions (linters, test runners, CI integrations, themes) work in VS Code because it is the de facto standard. Cursor and Windsurf soften this by staying compatible with the VS Code extension API. Zed is building its own ecosystem, smaller but faster.

For a team weighing the jump, the question is "how much of my team's tooling ecosystem survives the switch?", not "which AI is better?" The answer drives the decision more than any code generation benchmark.

## The Relationship to the Multi-Agent Paradigm

These IDEs are not agents in the sense of Chapter 8. They are **execution environments** for agents. Cursor Composer and Cascade are local orchestrators that coordinate changes across the repository. The next frontier (already visible in 2025) is connecting them to CI/CD pipelines and external agents through MCP, making the IDE one more node in the multi-agent swarm.

## The Executive View: The IDE as a Platform Decision

**■ EXECUTIVE TRACK**


Adopting an AI-native IDE is not an individual developer's decision. It is a platform decision, with implications for security, licensing, vendor lock-in, and measurable productivity, and technical leadership and the C-suite should evaluate it with the same rigor as any other infrastructure decision.

**Security and source code confidentiality.** By default, Cursor and Windsurf send fragments of source code to external APIs for semantic indexing and for generating suggestions. For companies in regulated sectors (finance, healthcare, defense), or whose source code is a competitive advantage, this configuration is not acceptable without an explicit review of the providers' data terms. Cursor offers a "Privacy Mode" that turns off remote storage of the code, and both Cursor and Windsurf have enterprise agreements with stricter privacy commitments. Zed, which processes everything locally, avoids the issue by architecture.

**Vendor lock-in and portability.** Because Cursor and Windsurf stay compatible with the VS Code extension API, they minimize lock-in risk in the tooling ecosystem: the team's extensions (linters, test runners, CI integrations) keep working. Zed, with its own extension ecosystem, introduces a portability risk that has to be weighed against its speed advantages. The practical question for the CTO is: "if this vendor raises the price 3x tomorrow or is acquired, what does it cost to migrate?"

**Productivity metrics and cost justification.** AI-native IDEs carry subscription costs ($20–40 per developer per month for Cursor and Windsurf on pro plans). For a team of 10 developers, that comes to $2,400–$4,800 a year. The business case requires showing a productivity multiplier of at least 1.5x on the team's tasks, a threshold that is reachable according to the evidence in Peng et al. (2023). The operational recommendation is to measure before adopting widely: a 4-week pilot with 3–5 developers on a representative project, measuring sprint velocity before and after, produces the evidence needed for the decision.

**The IDE as a node in the multi-agent swarm.** The most relevant strategic frontier (already visible in 2025) is the integration of these IDEs with CI/CD pipelines and external agents through MCP. A Cursor Composer or Cascade that can not only propose changes in the repository but also trigger a security review agent, run the integration tests, and post the result to the project management system turns the IDE into an active node of the organizational swarm, not just an individual productivity tool.

## Comparative Benchmarks and the State of the Research

A rigorous comparison of AI-native IDEs is methodologically complex because productivity differences depend heavily on the type of task, the technology stack, and the individual developer's preferences. The SWE-bench benchmark ([Jimenez et al., 2024](#ref-jimenez2024)), published as part of research by the Princeton NLP Group, evaluates how well agent systems resolve real GitHub issues in production repositories, the evaluation metric closest to a developer's actual work. The models that power Cursor Composer (Claude Sonnet, GPT-4o) show resolution rates of 12–49% on SWE-bench, depending on the benchmark variant. Translated into team productivity, those ranges are equivalent to speeding up between one and four sprints of engineering work per quarter.

## Key Takeaways from Chapter 30

- Cursor (a fork of VS Code) adds predictive Tab, multi-file Composer, and local semantic indexing.
- Windsurf (Codeium) bets on continuous flow with Cascade and full-repository context through Supermaven.
- Zed builds a native editor from scratch in Rust, with AI integrated at a low level.
- The real selection criterion is compatibility with the team's tooling ecosystem, not which AI is "better."
- Executive view: adopting an AI-native IDE is a platform decision; it calls for a security review, an assessment of vendor lock-in, and a measured productivity pilot before wide adoption.
- SWE-bench ([Jimenez et al., 2024](#ref-jimenez2024)) is the benchmark with the greatest ecological validity for comparing coding agents on real tasks.
