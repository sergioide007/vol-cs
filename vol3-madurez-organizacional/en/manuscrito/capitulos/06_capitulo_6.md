# Chapter 6: Templates for Multi-Agent Projects That Operate as Development Teams: Sprints, Ceremonies, Demos, and the ROI Executives Expect

> *A team of agents without a cadence is not a team: it is chaos with good spelling.*

---

**The thread connecting this chapter to the hydrological swarm of Chapter 3.** That case showed control under uncertainty in its most extreme form: minutes to decide, lives at stake, and a Critic Agent that existed solely to keep an incoherent plan from arriving at time zero. This chapter applies the same principle at a different scale and a much slower cadence, weeks instead of hours, but the underlying question doesn't change: how do you govern a system that produces results under conditions no one can fully predict? Where Chapter 3 resolved uncertainty with a synchronous verification layer, here it is resolved with cadence, the same bet agile engineering has made for two decades: not to eliminate uncertainty, but to expose it at regular intervals that are cheap to correct. Chapters 4 and 5, between the two, already prepared the ground: defending the architecture before a committee (Chapter 4) and finding its flaws before someone else does (Chapter 5) are both exercises in governance under the same structural uncertainty. This chapter gives that governance an operating rhythm.

## Section 1: The Central Thesis: Why Agile Is the Swarm's Coordination Architecture

There is a structural tension in multi-agent systems that most technical frameworks ignore: the difference between a set of agents that execute tasks and a **team of agents that produces value sustainably**. The distinction is not semantic. A set of agents can process tickets; only a team can learn, adapt, and iteratively improve the way it works.

Dingsøyr et al. (2023), in their comparative study on agile scaling in *IEEE Software* (Q2, IF 4.8), documented that software development teams operating under explicit cadences (sprints, ceremonies, retrospectives) produce software of measurably higher quality (23% lower defect density, 2.1× higher deployment frequency) than teams without a cadence, even controlling for experience and team size. The reason: cadence imposes **observability over the process**, not just over the product.

This logic carries over entirely to multi-agent systems. A swarm without a cadence produces results, but it produces no evidence about how it produces them, how reliably it produces them, or what could be improved. Without that evidence, there is no possible governance. And without governance, there is no sustained executive adoption.

Agile methodology (specifically Scrum (Schwaber & Sutherland, 2020, Scrum Guide)) is not, in this context, a cultural choice transplanted into the world of AI. It is a **coordination architecture** with three properties that apply directly to the swarm:

1. **Scope bounding**: the sprint delimits what the swarm must resolve in N days. Without this bounding, a swarm tends to expand its scope indefinitely (the agentic equivalent of scope creep).

2. **Closing the feedback loop**: the demo and the retrospective create an explicit learning mechanism. The swarm doesn't just process; it also reflects on its own processing.

3. **Accountability in business language**: the POI→ROI table connects each technical deliverable to its value for the business. The executive doesn't inspect the code; they inspect the trajectory between what was promised and what was delivered.

---

## Section 2: The Agentic Roles of the Scrum Team

Assigning Scrum roles to agents is not arbitrary. Each role on the Scrum team exists to cover a specific function in the delivery cycle; the question is which AI capabilities model each one best.

**Product Owner Agent (APO).**

The Product Owner in Scrum is the custodian of value: it defines the backlog, prioritizes, and represents the stakeholder's interests. The APO is an agent with three specific capabilities:

1. **Ingesting and analyzing business signals**: it reads product metrics (conversion, retention, NPS), user feedback (Intercom, Zendesk tickets, App Store reviews), and regulatory changes. It translates those signals into User Stories with explicit acceptance criteria.

2. **Prioritization by expected value**: it implements a prioritization algorithm based on WSJF (Weighted Shortest Job First, Scaled Agile Framework), considering expected impact, relative urgency, risk reduction, and opportunity cost.

3. **Defending the backlog**: when the developer agents ask to split a story or simplify the solution, the APO evaluates whether the simplification compromises value for the end user. Not everything "simpler" is better for the business.

**Specialized Developer Agents.**

Unlike human developers (who are generalists with specialties), developer agents in a swarm are **pure specialists**:

- Backend Agent: implements business logic, APIs, and service integration.
- Frontend Agent: generates interface code, components, and interactions.
- Infrastructure Agent: manages Terraform, CI/CD pipelines, and Kubernetes configuration.
- Documentation Agent: keeps technical documentation in sync with the code (docstrings, READMEs, ADRs).

Each takes a User Story from the backlog, splits it into technical tasks, implements them, and submits the work to the **Reviewer Agent** before marking it Done.

**Reviewer Agent (Peer Review).**

This agent implements the code review process natively. Its checklist is not arbitrary; it is based on the team's quality criteria (the definition of Done), the project's architectural patterns (it can read CLAUDE.md or the ADR), and the established linting and security rules. An increment is not Done until the Reviewer Agent approves it. If it rejects it, it publishes specific feedback and the story goes back to the developer agent.

**Scrum Master Agent (ASM).**

The Scrum Master in the agile framework is the guardian of the process, not the content. The ASM implements:

- Blocker detection: if an agent goes more than 30 minutes without publishing events, the ASM flags it as potentially blocked and escalates to the Coordinator.
- Ceremony moderation: it generates the Daily agenda, gathers the previous day's events, and produces the real-time burndown report.
- Process metrics: it calculates sprint-over-sprint velocity, lead time per story, and wait time between stages.

---

## Section 3: The Cadence Template: A Sprint Configured for a Swarm

![Sprint cadence: Planning → Daily → Demo → Retro → Quarterly Closing](imagenes/uml/c26_sprint_roles_en.png)

### Sprint Planning (Duration: 90 min → 15 min with a swarm)

The swarm cuts Planning time from 90 minutes (standard for a team of 5-7 humans) to 15 minutes because the preparation work is already done:

- The APO has prioritized the backlog and added detailed acceptance criteria before the ceremony.
- The Estimation Agent has calculated story points using the swarm's historical velocity as a reference.
- The developer agents have reviewed the stories at the top of the backlog and flagged technical dependencies.

The Planning ceremony, then, is not an exercise in estimation and negotiation: it is a **check for shared understanding** and the moment to formalize the Sprint Goal.

```yaml
# Structured Sprint Goal template
sprint_goal:
  number: 47
  dates: "2025-01-20 / 2025-02-03"
  objective: "Enable multi-currency checkout for LATAM users"
  success_metrics:
    - metric: "conversion_rate_latam"
      baseline: 2.3%
      target: 3.1%
      measurement: "GA4 + BigQuery, day 3 post-deploy"
  committed_stories:
    - id: "US-234"
      title: "Currency selector in cart"
      story_points: 5
      assigned_agent: "frontend_agent_01"
    - id: "US-235"
      title: "Stripe multi-currency integration"
      story_points: 8
      assigned_agent: "backend_agent_02"
  identified_risks:
    - "Stripe multi-currency API in beta → rollback plan to single currency"
```

### Daily Standup (Eliminated as a ceremony → Replaced by a Continuous Dashboard)

The Daily Standup exists in Scrum to synchronize a human team working in discontinuous intervals. Agents publish events continuously. The Daily therefore turns into a **real-time status dashboard** that the human team reviews in 5 minutes:

| Agent | Last activity | Status | Blocked | Next expected event |
|--------|-----------------|--------|-----------|------------------------|
| APO | Refined US-236 (09:45) | Active | No | Review of US-237 criteria (11:00) |
| Dev Backend | Committed US-235 at 60% (10:30) | In progress | No | PR ready (15:00 est.) |
| Dev Frontend | US-234 in review (10:15) | Waiting | Reviewer |, |
| Reviewer | Reviewing US-234 (10:20) | Active | No | Feedback in <20 min |
| Scrum Master |, | Monitor | No | Burndown update (11:00) |

### Sprint Demo (Duration: 30 min for stakeholders)

Demos happen between reviewer agents before they reach human stakeholders. An increment is only presentable if:

1. The Reviewer Agent approved it (technical quality).
2. The APO's acceptance criteria were verified automatically.
3. The acceptance tests (written by the APO as Given-When-Then) pass in the staging environment.

The demo for human stakeholders, then, is not a "does it work?" It is "this works, here are the numbers, this is the expected impact." The technical validation time has already been absorbed.

### Retrospective (30 min at the close of the sprint)

The ASM generates the retrospective report with sprint data: velocity, lead time, the Reviewer's rejection rate, and detected blockers. The human team (tech lead + PO) reviews the report and makes process improvement decisions. Three questions:

1. Which blocking patterns repeated more than twice? → Investigate the root cause.
2. Which stories took more than double their estimate? → Review the estimation criteria.
3. Was the Sprint Goal achieved? → Connect to the business metrics in the POI→ROI table.

---

## Section 4: DORA Metrics Applied to the Swarm: The Language the CTO Understands

**■ EXECUTIVE TRACK**


DORA metrics (Forsgren, Humble & Kim, 2018, *Accelerate: The Science of Lean Software and DevOps*) are the industry standard for measuring software delivery performance. Four metrics, widely adopted across the industry since the State of DevOps Report 2023 (Google Cloud/DORA):

| DORA metric | Definition | Elite performer | Multi-agent swarm (2024 benchmark) |
|-------------|-----------|-----------------|---------------------------------------|
| Deployment Frequency | How often do you deploy to production? | Multiple times a day | 8–15 deploys/day (minor tasks) |
| Lead Time for Changes | How long does it take a commit to reach production? | <1 hour | 22–45 minutes (with integrated CI/CD) |
| Change Failure Rate | What % of deploys cause an incident? | <5% | 3–5% (vs. 15–25% on mid-sized human teams) |
| Time to Restore Service | If there is an incident, how long does it take to resolve? | <1 hour | 18–35 minutes (with an integrated Diagnostic Agent) |

Being able to present up-to-date DORA metrics to the CTO changes the conversation from "how is the project going?" to "we're in the elite quartile on deployment frequency and lead time, with a change failure rate 40% below our industry's benchmark."

---

## Section 5: From POI to ROI: The Table Executives Expect

**■ EXECUTIVE TRACK**


The Quarterly Closing is where the swarm reports in the language of the business. The POI→ROI table connects each Promised Outcome Indicator to its measured Return on Investment:

| Sprint | POI (promised) | Measurement KPI | Expected ROI | Measured ROI | Delta |
|--------|----------------|-----------------|-------------|------------|-------|
| S-45 | Cut onboarding time from 72h to 24h | TTFV (Time to First Value) | $120K/year CS savings | $134K/year | +11.7% |
| S-46 | Enable checkout in 3 languages | LATAM conversion rate | +$280K/year revenue | +$312K/year | +11.4% |
| S-47 | Multi-currency LATAM | LATAM revenue | +$220K/year revenue | In progress |, |

This table answers the question every CFO asks at the quarterly review: "What value did the AI team deliver in the last 90 days, in money?" Not in features. In money.

**Expanded academic version:**

> Applying the Scrum framework to multi-agent systems can be formalized as a coordination problem under cooperative game theory ([Osborne & Rubinstein, 1994](#ref-osbornerubinstein1994)), where the Sprint Goal operates as a **focal point** ([Schelling, 1960](#ref-schelling1960)) that reduces ambiguity about each agent's expected behavior without the need for exhaustive explicit communication. The ceremonies, in turn, can be modeled as information revelation mechanisms ([Myerson, 1979](#ref-myerson1979)): the Daily Dashboard reveals each agent's state over the sprint's search space; the Retrospective is a mechanism for collective belief updating about the swarm's production function. Under this formalization, the agile cadence is a coordination protocol with analyzable mathematical properties, not an organizational convention: it minimizes the collective entropy of the delivery process under a constraint of informational transparency.

---

## Key Takeaways from Chapter 6

- Agile methodology is the swarm's **coordination architecture**, not a cultural ornament.
- The four agentic roles (APO, Developers, Reviewer, Scrum Master) cover distinct functions of the Scrum cycle with specific AI capabilities.
- Sprint Planning shrinks from 90 to 15 minutes because the APO prepares the work beforehand; the Daily is replaced by a real-time dashboard.
- **Demos between Reviewer Agents** build peer review in natively: an increment is Demo-Ready only if it passes the agent's review.
- **DORA metrics** connect the swarm's performance to the language the CTO understands.
- The quarterly **POI→ROI table** connects each deliverable to its value in money, the language the CFO demands.
- Cadence imposes observability, and observability makes governance possible.

---

## Worked Exercise 6.1: Design the Swarm's Quarterly Closing

**Problem.** Your swarm completed Q1 (January–March 2025). The following POIs were committed: (1) Reduce customer churn by 10%, (2) Enable integrations with 3 major ERPs, (3) Cut TTFV from 5 days to 2 days. You have the following data: churn fell 7.3%, ERPs integrated: 2 of 3 (the third running 3 weeks late), current TTFV: 2.4 days. Design the Quarterly Closing presentation.

**Solution.**

## Q1 2025: Quarterly Closing: Executive Summary

### POI 1: Churn -10% → Partially achieved: -7.3%
**ROI impact**: $-180K projected vs. $-131.4K actual (-27% of target)
**Analysis**: The SMB segment cut churn by -11.2% (beat the target);  
the Enterprise segment lagged (-3.1%). Root cause: the  
"Customer Success Alerts" feature prioritized SMB because of ticket volume.  
**Q2 action**: Dedicate 30% of the swarm's capacity to Enterprise CS.

### POI 2: 3 ERPs integrated → Achieved 2/3 (66%)  
**ROI impact**: $+340K projected vs. $+226K actual  
**Analysis**: SAP and Oracle integrated and in production. NetSuite  
delayed 3 weeks by an API v2 → v3 incompatibility.  
**NetSuite ETA**: Week 2 of Q2. No additional resources required.  
**Q2 commitment**: NetSuite complete + an additional regional ERP.

### POI 3: TTFV 5 days → 2 days → Achieved at 80%: 2.4 days  
**ROI impact**: $+95K/year (vs. $+118K projected)  
**Analysis**: Automated onboarding cut it from 5 to 3.1 days in S45.  
Further optimization in S46-47 brought it down to 2.4 days. Remaining gap:  
the manual document verification step (0.4 days).  
**Q2 action**: Automate document verification with computer vision.

### Q1 Executive Summary
| Indicator | Target | Actual | % achieved |
|-----------|---------|------|----------------|
| Revenue impact | $+$638K | $+$452K | 71% |
| Swarm capacity used | 100% | 94% | 94% |
| Deployment frequency | 8/day | 11/day | 138% |
| Change failure rate | <8% | 4.3% | Elite |

> **Q1 Verdict**: 71% of the promised revenue impact. 2 of 3 POIs achieved. DORA technical performance in the Elite quartile. Q2 adjusts priorities based on the gaps identified.

This format answers the executive question before it is asked: "What did we achieve, what fell short, why did it fall short, and what will we do differently?"

---
