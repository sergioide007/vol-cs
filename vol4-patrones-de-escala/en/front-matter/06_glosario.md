# Operational Glossary: Volume 4

*Operational vocabulary for runtime operations, systems scale, and token economics. Metric terms are defined with their concrete formulas or operational calculation rules, because in this volume the mathematical definition is what imparts engineering utility.*

| Term | Operational Definition | Chapter |
|---|---|---|
| **Token-Burn** | Wasteful token consumption yielding zero business value: unproductive loops, redundant retries, and context bloat that fail to advance task completion. | 1 |
| **CIU (Cost per Useful Iteration)** | Total gross cost divided by the count of iterations that yielded an accepted, validated output. Transforms raw spend into a unit-economic metric with a value-based denominator. | 1, 11 |
| **Probabilistic Estimation** | Project estimation modeled as a probability distribution (percentiles like $p_{50}, p_{90}, p_{99}$) rather than arithmetic means, accounting for the heavy-tailed nature of agentic execution. | 2 |
| **Non-Deterministic Testing** | Automated verification of behaviors that do not produce byte-for-byte identical outputs: evaluated against invariant properties, statistical thresholds, and test matrices rather than exact string equality. | 3 |
| **Indirect Prompt Injection** | Adversarial instruction embedded within untrusted external data retrieved by an agent (web pages, files, database records) rather than supplied directly in user input. | 4 |
| **Dependency Rule** | In Clean Architecture, source code dependencies must point inward toward high-level business entities; foundation models and external APIs are low-level swappable infrastructure details. | 6 |
| **Value Object / Hexagonal Ports** | Domain-Driven Design and Clean Architecture constructs that insulate core domain logic from infrastructure details, applied here to agentic tool boundaries and payloads. | 6 |
| **Event-Driven Architecture / Kafka** | Distributed architectural pattern where decoupled agents react to asynchronous event streams rather than blocking RPCs; the distributed append-only log serves as immutable source of truth. | 7 |
| **CDC (Change Data Capture)** | Streaming database state modifications into real-time event logs, establishing the streaming pipeline: CDC → Agent Worker → Downstream Consumers. | 7 |
| **Backpressure (Event Consumption)** | Flow control mechanism where downstream agent consumers dynamically pace event ingestion to prevent memory or compute exhaustion. | 7 |
| **Four Golden Signals** | Canonical service telemetry (latency, traffic, errors, saturation) unified in this volume with synthetic agentic performance indicators. | 8 |
| **DLQ (Dead-Letter Queue)** | Destination message broker holding events that fail processing after $N$ retry cycles; weekly DLQ audits directly seed automated regression evaluation suites. | 7, 8 |
| **LLMOps** | Operational discipline managing foundation model systems: prompt versioning, continuous evaluation benchmarks, distributed tracing, and spend governance—tailored for lean engineering teams. | 8 |
| **Semantic Drift** | Subtle, gradual deviation of multi-agent outputs away from foundational system objectives over time, completely undetected by classical HTTP status checks. | 11 |
| **Spurious Consensus** | Artificial agreement among interacting agents arising not from empirical evidence, but from shared systemic biases or circular context poisoning. | 11 |
| **Synthetic Incentives** | Algorithmic reward and scoring signals engineered to break agent swarms out of analysis paralysis; carries the known risk of proxy gaming. | 11 |
| **Agentic Edge Computing** | Executing agent logic directly on client devices or localized edge hardware to satisfy latency, data sovereignty, or energy efficiency constraints. | 12 |
| **CAPEX vs. OPEX** | Capital allocation decision weighing upfront hardware infrastructure investments against variable API consumption; applied here to long-term compute efficiency. | 12 |
| **Agentic Disaster Recovery (DR)** | Business continuity engineering and recovery drills for AI systems; must restore **distributed cognitive state** and memory hierarchies rather than merely reviving containers. | 13 |
| **Distributed Cognitive State** | Ephemeral memory, session context, active reasoning traces, and registered tool state distributed across an agent swarm; an asset unaddressed by traditional DR. | 13 |
| **RTO / RPO (Agentic)** | Recovery Time Objective and Recovery Point Objective; in agentic architectures, both must be explicitly defined and measured for cognitive memory graphs. | 13 |
| **Recovery Drill** | End-to-end rehearsal of disaster recovery procedures under simulated catastrophic failure. Without live drills, a DR plan is merely an unproven hypothesis. | 13 |
| **Graceful Degradation** | Architectural capability to operate under explicitly declared degraded states when upstream dependencies or model endpoints fail, rather than suffering total collapse. | 10 |
