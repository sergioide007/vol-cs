# Volume 2 Operational Glossary

*Concise definitions of technical and geopolitical terminology introduced or specialized in this volume. Section A defines frontier systems engineering vocabulary; Section B covers vertical industry mechanics; Section C details geopolitical, regulatory, and ecosystem terms. Keeping them segregated prevents the most frequent error when reviewing this volume: treating a political constraint as if it were a purely technical software design choice.*

## A. Frontier Engineering

| Term | Operational Definition | Chapter |
|---|---|---|
| **Probabilistic Insider Threat** | The security paradigm recognizing that risk does not reside solely outside system boundaries: the foundational model itself can trigger destructive side effects without an external malicious attacker. Invalidates perimeter-only security models. | 1 |
| **OWASP Top 10 for LLMs** | The authoritative industry taxonomy categorizing the ten most critical security vulnerabilities in LLM-based applications. Serves as a risk prioritization framework, not a static compliance checklist. | 1 |
| **Prompt Injection (Direct / Indirect)** | An adversarial instruction delivered via user input (direct) or through external data retrieved by an agent (indirect: poisoned web pages, databases, or MCP tools). | 1 |
| **Confused Deputy** | An architectural failure scenario where a highly privileged component executes actions on behalf of a lower-privileged caller without validating the caller's actual authorization. | 1 |
| **Verifiability** | The degree to which an agent's reasoning trace and output can be independently asserted by deterministic code. The core variable added to classical trust calculus. | 5 |
| **Graduated Trust** | The architectural practice of replacing binary trust switches ("trusted / untrusted") with a continuous operational spectrum calibrated to task risk and verified historical performance. | 5 |
| **Actor Model / ReactiveX** | The formal foundations of reactive systems: isolated state units communicating via asynchronous messages, and declarative operators composing resilient event streams. | 4 |
| **Backpressure** | Flow-control signaling enabling a downstream consumer to throttle an upstream producer rather than buffering unbounded work in memory until failure. | 4 |
| **Dead Letter Queue (DLQ)** | An isolated storage buffer where unprocessable messages are routed after exhausting retry budgets, enabling forensic inspection without halting the live stream. | 4 |
| **Event Storm** | A cascading failure loop where an event triggers reactions that recursively republish identical events. Mitigated by idempotency keys, DLQs, and maximum hop limits. | 4 |
| **Hybrid Architecture** | The deliberate partitioning of workloads between hyperscaler cloud infrastructure and on-premise/edge compute; the primary failure surface is the integration seam between both planes. | 12 |
| **Feedback Latency** | The elapsed time between an agentic action and the arrival of a verifiable feedback signal. Dictates the upper bound on an engineering team's empirical learning velocity. | 26 |
| **Agentic Technical Debt** | The architectural debt unique to systems built on autonomous agents: unversioned prompts, missing eval suites, implicit ambient permissions, and loops lacking degradation fallbacks. | 13 |
| **Cognitive Atrophy** | The erosion of human domain expertise caused by delegating decision authority entirely to an agent rather than utilizing it as a cognitive exoskeleton. | 6 |
| **Support-Evaluation Pattern** | An architectural separation of concerns delegating helpful assistance and quality judgment to distinct agents, ensuring an assistant never evaluates its own work. | 8 |

## B. Industry

| Term | Operational Definition | Chapter |
|---|---|---|
| **Spatiotemporal Diffusion** | Generative diffusion model architectures that treat time as a coherent mathematical dimension alongside spatial video coordinates. | 16 |
| **Multi-Agent Reinforcement Learning (MARL)** | Reinforcement learning algorithms where multiple autonomous agents learn policies concurrently within a shared, evolving environment. | 28 |
| **Proactive Licensing** | The strategic legal procurement of intellectual property rights for training data prior to judicial rulings or regulatory mandates. | 15, 16 |

## C. Geopolitics, Regulation, and Tech Ecosystems

| Term | Operational Definition | Chapter |
|---|---|---|
| **EU AI Act** | Comprehensive European Union legislation classifying AI systems into tiered risk categories and enforcing binding obligations per tier. Regulation operationalized as an architectural blueprint. | 19 |
| **General Purpose AI (GPAI)** | Foundational, high-impact models subject to explicit transparency, systemic risk evaluation, and data governance disclosures under global regulatory regimes. | 16, 19 |
| **GDPR / PIPL** | European and Chinese data privacy frameworks governing permissible cross-border data transfer, retention policies, and architectural data localization constraints. | 17, 20 |
| **Compliance-by-Design** | The engineering discipline of embedding statutory compliance, data residency, and audit boundaries directly into system architecture rather than treating them as post-hoc review items. | 19 |
| **NIST AI RMF** | The National Institute of Standards and Technology's Artificial Intelligence Risk Management Framework, formalizing risk mapping, measurement, and governance. | 18 |
| **Constitutional AI / RLHF** | Alignment methodologies: explicit machine-readable principles guiding model self-correction (Constitutional AI), and preference optimization via human feedback (RLHF). | 18 |
| **Mixture of Experts (MoE)** | Model architecture dynamically routing inference tokens to a sparse subset of specialized expert parameters, drastically reducing active FLOPs per token. | 17 |
| **Multi-Head Latent Attention (MLA)** | Attention mechanism compressing key-value (KV) cache footprints into low-rank latent projections, allowing far higher concurrent serving throughput. | 17 |
| **Group Relative Policy Optimization (GRPO)** | A mathematical policy optimization algorithm enabling reasoning model training from group rewards without requiring separate critic networks. | 17 |
| **Technological Sovereignty** | A state's structural capacity to sustain its national AI stack without existential dependence on foreign vendors subject to adversarial extraterritorial jurisdiction. | 22, 24 |
| **Supply Chain Chokepoint** | A concentrated global monopoly node (e.g., ASML extreme ultraviolet photolithography) upon which all downstream advanced semiconductor manufacturing depends. | 23, 24 |
| **Agentic City Maturity Model** | A formal progression scale measuring the degree to which municipal urban operations (traffic, power, emergency logistics) are orchestrated by governed multi-agent swarms. | 11 |
