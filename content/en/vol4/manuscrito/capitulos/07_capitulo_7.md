# Chapter 7: Event-Driven Architecture, Kafka as the Nervous System

## From Calls to Events

Everything built so far connects agents through calls: the orchestrator invokes, waits, and composes (Chapter 8). That model is correct inside a pipeline; it falls short when agents must integrate at the scale of the *whole system*: dozens of services, teams, and rhythms. For that, the industry converged a decade ago on event-driven architecture: services don't call each other; they **publish facts** ("PR 482 was opened," "ticket 1043 changed to urgent") to an immutable, ordered log, and whoever needs to react subscribes. The log as source of truth, not as a byproduct, is the central idea Kleppmann (2017) places at the heart of data-intensive systems, and the temporal decoupling it offers is the most effective tool against the coupling that ruins microservice architectures ([Newman, 2021](#ref-newman2021)). Apache Kafka is its dominant implementation (Apache Software Foundation, n.d.); the principles hold for any equivalent broker.

For the Synthetic Enterprise, the event model isn't a refinement: it solves four problems the call model can't solve well:

1. **Temporal decoupling.** The reviewer agent takes two minutes; the service that published "PR opened" doesn't wait and doesn't know a reviewer exists. Spikes are absorbed in the log, not in timeouts.
2. **Fault tolerance with honest retry.** If the agent fails midway through a task, the event stays in the log: another consumer picks it up. Lost calls, by contrast, get lost along with their context.
3. **Replay: the unexpected gift for evals.** A retained log is an evaluation set that writes itself (Chapter 13): replay last week's real events against the candidate version of the agent and compare results with the production version, without touching production. No call-based system offers this for free.
4. **Structural audit.** The immutable record of what happened and what each agent did (the requirement of Chapters 14 and 19) stops being a separate component: it is the transport medium itself.

## The CDC → Agent → Consumers Flow

Event-driven architecture draws a clear sequence in time: changes occur in source systems (a database, a form, an API), are captured as events in the log, and the agents consume them when their turn comes. The dimension that matters is time: how long each step takes, how they decouple, where latency arises.

> **Design Justification: Sequence Diagram for Interaction Modeling**
>
> In event-driven architecture, what's critical is the *temporal order of events* and the *decoupling in time* between publisher and consumer. A sequence diagram reveals exactly that: who publishes, when, who consumes, with what latency.
>
> A component diagram would show where services live; a class diagram would show their internals. Here we need to see the *flow of an event through the system over time*, the dimension that explains backpressure, decoupling, and how a slow agent does NOT block the publishers.
>
> The sequence diagram reappears in this book in **Chapter 3** (the AI Gateway, which is also a temporal flow), where time and accumulated cost are the central message.

![Diagram 7.1: CDC → Enriching Agent → Consumers flow: event-driven architecture over time](imagenes/uml/diagrama17_secuencia_en.png)

Note the fundamental property the diagram reveals: the agent does NOT block the source system. A change occurs, is published, and the normal business flow continues. For example, if the agent takes two minutes, hundreds of other changes will already have happened in the log. Temporal decoupling is what makes it an architecture of scale.

**► TECHNICAL TRACK: Agents as Citizens of the Log**

```typescript
// Example 7.1 (Node.js + kafkajs): the reviewer agent as a consumer.
// The event triggers the Chapter 6 use case; the result is
// published as a new fact. Nobody calls anybody.

import { Kafka } from "kafkajs";
import { ReviewCodeUseCase } from "./domain/review-code";

const kafka = new Kafka({ clientId: "reviewer-agent",
                          brokers: [process.env.KAFKA_BROKER!] });
const consumer = kafka.consumer({ groupId: "code-review-agents" });
const producer = kafka.producer();

export async function main(useCase: ReviewCodeUseCase) {
  await consumer.connect();
  await producer.connect();
  await consumer.subscribe({ topic: "pull-requests.opened" });

  await consumer.run({
    eachMessage: async ({ message }) => {
      const event = JSON.parse(message.value!.toString());

      // Idempotency: the log delivers "at least once"; the agent
      // must tolerate duplicates (same principle as Exercise 7.1).
      if (await alreadyReviewed(event.prId, event.headSha)) return;

      const review = await useCase.execute(event.diff);

      await producer.send({
        topic: "pull-requests.reviewed",
        messages: [{
          key: String(event.prId),         // same key => same order
          value: JSON.stringify({
            prId: event.prId,
            headSha: event.headSha,
            verdict: review.verdict,
            findings: review.findings,
            costUsd: review.costUsd,        // the CIU travels with the fact
            agent: "reviewer-v3",           // prompt version: audit
          }),
        }],
      });
    },
  });
}
```

```java
// Example 7.2 (Java, Spring Kafka): the same citizen, in the other language.
@Component
public class ReviewListener {

    private final ReviewCodeUseCase useCase;
    private final KafkaTemplate<String, ReviewEvent> kafka;

    public ReviewListener(ReviewCodeUseCase useCase,
                          KafkaTemplate<String, ReviewEvent> kafka) {
        this.useCase = useCase;
        this.kafka = kafka;
    }

    @KafkaListener(topics = "pull-requests.opened",
                   groupId = "code-review-agents")
    public void onPrOpened(PrOpenedEvent event) {
        if (alreadyReviewed(event.prId(), event.headSha())) return; // idempotency
        var review = useCase.execute(event.diff());
        kafka.send("pull-requests.reviewed", String.valueOf(event.prId()),
                   ReviewEvent.of(event, review, "reviewer-v3"));
    }
}
```

Four decisions in this code are doctrine, not style. First, the **partition key** (`prId`) guarantees that events for the same PR are processed in order; global ordering doesn't exist in a partitioned log and chasing it is the rookie mistake. Second, **idempotency** in the consumer is mandatory because the log delivers "at least once"; an agent without it is the generator of the fifty duplicate tickets from Exercise 7.1. Third, the **event schema is a contract**: exactly the contract of the master prompt (Chapter 5) elevated to the boundary between services; it is governed with a schema registry and evolves in a backward-compatible way. Finally, failed events go to a **dead-letter queue** (DLQ) with their full context: the DLQ of an agentic system is pure gold, every dead message is a real hard case for the eval suite.

Lastly, a cost warning closes the technical track: decoupling makes consumption *invisible*; nobody "sees" the agent work, only the log grow. The Chapter 11 budget applies to the consumer: a spend limit per time window and a pause of the consumer group when it is exceeded. An agent subscribed to a topic with spikes is Token-Burn on self-service.

## Reactivity and Backpressure: The Agent as a Sustainable Consumer

Now, that warning opens the question that closes the chapter: what happens when the log emits faster than the agent can consume? The topic spits out thousands of events per second; the agent, tied to the latency of a model call, processes dozens. Without a mechanism that regulates the pace, the buffers fill, memory runs out, and the service goes down, and, before going down, it burns tokens on events a saturated system will end up discarding. Systems engineering's answer to this problem has a name: **backpressure**, the consumer's ability to tell the producer "slow down" instead of drowning in silence ([Bonér et al., 2014](#ref-boner2014)).

Here the distinction Chapter 1 anticipated is in order: the *reactivity of the agent* (reacting to an observation) is not the *reactivity of systems* (governing asynchronous flows with backpressure). The latter is the substrate on which the consumer agent lives, and the author developed it in earlier work with a thesis that is, word for word, this book's: **adopt reactivity selectively and in measure, not by fashion** (see "Author's Public Work"). Its lessons apply directly to the citizen of the log:

- **Backpressure isn't optional; it is the difference between degrading and crashing.** A reactive consumer limits its admission rate (`limitRate`) and its concurrency (how many events it processes in parallel) so the pace is set by the slowest link (the model), not the fastest (the broker). It is the same idea as the consumer group pause in the previous paragraph, expressed as a continuous property of the flow rather than as an emergency switch.
- **Consistency under failure is designed, not hoped for.** When a consumer updates the database and then publishes an event, a failure between the two steps leaves the system inconsistent; the Saga pattern with compensating transactions (Chapter 8) is the canonical reactive answer, and the DLQ with context is its safety net.
- **The adoption criterion is the whole book's:** *what fails if we don't use reactivity here?* For a low-volume consumer, a simple imperative loop is more readable and just as correct; full reactive programming (streams, operators, `Mono`/`Flux`) adds a cognitive load that is paid only when concurrency or latency justify it. A hybrid architecture (reactive modules where the flow demands it, imperative where it doesn't) is usually the mature decision.

The synthesis with token economics is the lesson the agent inherits from the reactive system: in reactivity, *faster is not better; sustainable is better*. An agent that consumes as fast as the log produces is not efficient: it is an incident (of saturation and of billing) waiting for its traffic peak. Backpressure is, at once, the availability guardrail of Chapter 8 and the budget guardrail of Chapter 11, written as a single property of the flow.

## Case Study: From the Batch Synchronizer to the Flow with Agentic Enrichment

*(An evolution of an architecture case previously published by the author; see "Author's Public Work." Illustrative figures.)*

![Diagram 7.3: Architecture of the synchronizer in its published form: a dual stack (Spring Boot WebFlux in Java and Node.js on Kubernetes) behind a PCI environment, with Kafka as the decoupler, Saga for distributed consistency, Circuit Breaker for resilience, and an Event Store over shared resources (Redis, PostgreSQL, MongoDB, MySQL). The original case study that germinated in this chapter (figure published by the author).](imagenes/capitulo16/sincronizador_continua_en.png)

The diagram is the case in its original form, before the simplification this chapter proposes, and it is worth reading as such: each component solves a real problem (the PCI environment isolates the sensitive data; Kafka decouples the two stacks; the Saga pattern from Chapter 8 maintains consistency across services without a distributed transaction; the Circuit Breaker cuts the cascade of failures; the Event Store keeps the history to rebuild state). But read together they also tell the other side: that resilience has an operational and cognitive price that is justified only if the batch's minutes of latency *really* hurt. The chapter doesn't discard this architecture; it uses it as an honest starting point for asking which part of its complexity is essential and which is accidental when all that's needed is for the cache to see the change in seconds.

The starting point is a classic synchronizer: a serverless function periodically queries MySQL, compares with the Redis cache, and updates the differences, batches, a one-way flow, its own audit. It works, and its author honestly documented its limits: minutes of latency between the change and its visibility, and a multi-cloud operational complexity whose monthly cost was measured in hundreds of dollars.

The event-driven evolution inverts the mechanics: the database's changes are captured as events (CDC, *change data capture*) and flow through the log; the cache is just one more consumer that updates in seconds. And here the agentic opportunity appears that the batch made unthinkable: **an enriching agent as an intermediate consumer**, which classifies each change, detects anomalies against the domain's invariants (Chapter 6), and publishes the enriched event for the cache and for the operations dashboard. The pattern is general and reusable: *CDC → economy enrichment agent → consumers*, with the agent operating on the flow without touching either the database or the cache; structural least privilege (Chapter 4) by construction.

The moral of the case, faithful to its original: the event-driven version is not "better" in the abstract; it is better *if* the minutes of latency hurt and *if* the team can operate a broker. The architecture is chosen with the decision tree and the numbers on the table (Chapter 8), not with the enthusiasm of the diagram.

## Hybrid Architecture: Agents at the Boundary Between Cloud and On-Premise

When agents must orchestrate flows involving both cloud systems (modern, scalable infrastructure) and sensitive on-premise data (customer databases, historical transaction records), an architectural challenge emerges that purely cloud or purely local architectures don't solve: how to maintain security, decoupling, and governance when the critical data never leaves the organization's perimeter, but the agents live in the cloud.

First, the guiding principle is **perimeter Zero-Trust**: no component trusts that another is "inside" or "outside" simply by its physical location. Every boundary (between the cloud and on-premise, between microservices) demands authentication, authorization, and encryption. For agents, this means that access to on-premise systems doesn't travel through the model but through a VPN (Virtual Private Network) gateway that intercepts, validates, and logs every request before allowing it.

![Diagram 7.2: Evolved Hybrid Architecture: Cloud VPC with private subnets, isolated agents, encrypted VPN tunnels to sensitive data, and an Event Bus for decoupling in time](imagenes/capitulo17/diagrama17_2_arquitectura_hibrida_en.png)

The topology the diagram encodes solves four challenges at once:

**Network isolation by layers.** The API Gateway (at the cloud's edge) is the only public entry point; it exposes only what the organization decides to expose. Behind it, a VPC (Virtual Private Cloud) groups the agentic components into private subnets where no incoming request can arrive without passing through the Gateway. After that, the VPN tunnels to on-premise are the only channels allowed for sensitive data. The consequence: even if an agent is compromised, its access to the database can't happen without crossing a specific firewall that can detect, block, and log the attempt.

**Separation of responsibilities through queues.** Agents that process sensitive data never store it in their local context; they receive it as the result of a query, process it, and publish enriched events on a bus (Kafka, or any broker). Those events travel back through the VPN with a metadata envelope that declares which agent executed which operation, when, and at what cost. Audit is built into the flow, not a separate "log system" nobody maintains.

**Granular access control in the adapters.** The agent doesn't get "database user with full access" credentials; it gets a short-lived rotating token that grants access to *exactly* the tables and operations that specific task needs. In the MCP server (Chapter 9) that exposes the tools, the validator rejects any query that isn't within that scope. The agent's state machine (Chapter 8) records every transition, including the rejected ones; that trace is the basis of any compliance audit.

**Consumer-side governance.** The consumer-side governance is non-negotiable. When an event reaches the DLQ (Dead Letter Queue) for consistency, it contains the full context: which agent attempted it, with what parameters, why it failed. An auditor or an incident responder can reproduce exactly what happened, at what step security or the invariants failed, and if necessary, recover the system without losing the audit trail.

**► TECHNICAL TRACK: Secure VPN Tunnel in TypeScript**

```typescript
// vpn-client-agent.ts
// MCP client that connects through a secure VPN tunnel to
// on-premise systems. The tunnel is the only communication channel;
// the agent shouldn't know about encryption, certificates, or the network.

import TunnelClient from "@secure-tunnel/client";
import { LlmPort } from "./types";

class SecureOnPremiseAdapter implements LlmPort {
  private tunnel: TunnelClient;
  
  constructor(
    vpnGatewayUrl: string,
    clientCertPath: string,
    clientKeyPath: string
  ) {
    // Strict certificate validation: fails if not valid
    this.tunnel = new TunnelClient({
      serverUrl: vpnGatewayUrl,
      clientCert: require("fs").readFileSync(clientCertPath),
      clientKey: require("fs").readFileSync(clientKeyPath),
      tlsValidation: "strict", // Don't allow self-signed in production
      maxRetries: 3,
      retryBackoff: 2000, // 2 seconds, exponential
    });

    // Log of established connection: auditability
    this.tunnel.on("connected", () => {
      console.log(
        JSON.stringify({
          event: "vpn_tunnel_established",
          timestamp: new Date().toISOString(),
          gateway: vpnGatewayUrl,
        })
      );
    });

    this.tunnel.on("disconnected", () => {
      console.error(
        JSON.stringify({
          event: "vpn_tunnel_disconnected",
          timestamp: new Date().toISOString(),
          action: "agent_will_fail_gracefully",
        })
      );
    });
  }

  async queryOnPremiseDatabase(
    query: string,
    timeout: number = 30000
  ): Promise<any[]> {
    if (!query.toUpperCase().startsWith("SELECT")) {
      throw new Error("Only read operations are allowed.");
    }

    try {
      // The tunnel is the only way to access the database.
      // The agent has no direct IP to on-premise.
      const result = await this.tunnel.request({
        service: "database",
        operation: "query",
        payload: { query },
        timeout,
      });

      // Every response brings its audit envelope
      console.log(
        JSON.stringify({
          event: "secure_query_executed",
          timestamp: new Date().toISOString(),
          query_checksum: hashQuery(query),
          rows_returned: result.data?.length || 0,
          execution_time_ms: result.executionTime,
          tunnel_metadata: result.tunnelMetadata, // who executed it, when
        })
      );

      return result.data;
    } catch (error) {
      // Error in the tunnel: the agent will not retry, it will fail.
      // The DLQ will capture the event for human review.
      throw new Error(
        `Secure query failed: ${error.message}. ` +
        `Tunnel may be down. Escalate to on-premise team.`
      );
    }
  }
}
```

This adapter encapsulates the tunnel's security; the agent that uses it simply calls `queryOnPremiseDatabase(query)` without knowing there is a VPN, certificates, or retransmissions. That abstraction is the Chapter 6 port applied to infrastructure.

## Worked Exercise 7.1: The Ticket Triage Topics

**Problem.** Take the triage pipeline from Exercise 7.1 (500 tickets/day) to events: define topics, partition keys, retry policy, and where the budget cuts off.

**Annotated solution.** Three topics follow the three roles (`tickets.received` → `tickets.classified` → `tickets.drafted`) and a fourth cross-cutting one: `tickets.dlq`. The partition key is `ticketId` across the whole chain: the same ticket, always in order, and parallelism is graduated with partitions (at 500/day, 3 partitions are more than enough; the right figure will be given by the latency percentile, not intuition). Retries: 3 with exponential backoff in the consumer and, when exhausted, the whole message (with the response from the model that failed) to the DLQ; weekly human review of the DLQ feeds the eval suite with the cases that teach the most. The budget cuts off at the drafting role's consumer (the only one on the balanced tier): if hourly spend exceeds the CIUTracker threshold (Chapter 11), the group pauses and alerts; the tickets wait in the log without being lost, which is exactly the difference between degrading and failing. And the final detail that connects the three parts of the book: the `tickets.drafted` topic retained for 30 days **is** the evaluation set for the next prompt change.

## Key Takeaways from Chapter 7

- Events instead of calls: the immutable log as source of truth ([Kleppmann, 2017](#ref-kleppmann2017)) decouples times, teams, and failures ([Newman, 2021](#ref-newman2021)).
- An event-driven agent is a consumer and a producer: a well-thought-out partition key, mandatory idempotency, schema as contract, DLQ with context.
- Log replay is the eval suite that writes itself; the DLQ, its chapter of hard cases.
- Decoupling hides cost: a budget and a consumer pause, or Token-Burn on self-service.
- CDC → enriching agent → consumers: the pattern that turns a batch synchronizer into a flow with intelligence, without touching the source systems.
- **Secure hybrid architecture:** agents in the cloud, sensitive data on-premise. Perimeter Zero-Trust at every boundary, VPN tunnels as the only channel to critical systems, adapters that encapsulate security so the agent knows nothing of certificates, retransmissions, or network details.
- **Audit built into the flow:** every transition, every on-premise query, every failed event records who, when, and why. The DLQ is not a dead end; it is the entry to human review and to new eval cases.
- Backpressure: the consumer sets the pace, not the broker ([Bonér et al., 2014](#ref-boner2014)). Selective reactivity, not by fashion; the criterion is "what fails if we don't use it here?" Faster is not better; sustainable is.

---
