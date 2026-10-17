# Chapter 15: RACI and Eisenhower with Agents

> *Delegating to an agent without defining who answers for it also delegates accountability. And accountability cannot be delegated.*

## The Problem of Diffuse Responsibility in Human-Agent Teams

When an agile team brings in AI agents, an old question comes back in new clothes: who is responsible for what the agent produces? Without a structured answer, the swarm becomes a space where accountability evaporates ("the AI did it") and answering for outcomes becomes materially impossible. The phenomenon isn't unique to AI; the agile movement identified early on that self-organization without clarity of roles produces organizational ambiguity, not productive autonomy ([Schwaber & Sutherland, 2020](#ref-scrumguide2020)). What is new is that agents intensify the dynamic: they are actors with agency but without moral subjectivity, able to execute but unable to answer.

Given all this, the classic tools of organizational clarity (the RACI matrix and the Eisenhower matrix) are not only still valid in the agentic context: they become more indispensable than ever. Their value lies not in the formality they impose but in the clarity they produce: knowing who does what, who answers for what, and which priorities govern delegation decisions.

## RACI with Agents: The Rule of Non-Delegable Accountability

![RACI matrix: an agent can be R or C, but never A (Accountable is always human)](imagenes/uml/c42_raci_matrix_en.png)

The RACI matrix distinguishes four fundamental roles: Responsible (R, who executes), Accountable (A, who answers), Consulted (C, who contributes knowledge), and Informed (I, who receives the result). When introducing agents, a sharp, non-negotiable distinction is in order: **an agent can be Responsible or Consulted, but never Accountable**. The A (accountability) cannot be delegated to a machine, because it requires the ability to bear consequences, and an agent cannot bear them under any legal, ethical, or organizational framework in force.

| RACI role | Can an agent hold it? | Rationale |
|--------------|----------------------------|-----------------------------------------------------------|
| Responsible (R) | Yes | Executes the task with demonstrable competence |
| Accountable (A) | No | Bears consequences, always human |
| Consulted (C) | Yes | Contributes specialized analysis without being the final decision-maker |
| Informed (I) | Yes | Receives the result as part of the process chain |

This simple rule governs the entire integration. Violating it at any point creates an accountability vacuum that sooner or later an agent failure will expose in the worst possible way: when it has already caused harm and no one can be named as responsible. The European Union's Artificial Intelligence Act ([EU AI Act, 2024](#ref-aiact2024)) is explicit on this point: high-risk AI systems must have an identified human operator responsible for them.

## RACI at Scale: When the Responsible Party Is a Swarm

The previous rule assumes the Responsible (R) is an identifiable actor: a person, or a single agent with a name and an owner. That assumption breaks when the "agent" executing the task is actually an orchestrator that dispatched between 20 and 96 subagents in parallel (Vol. 4, Chapter 5, Case 7), the pattern both Claude Code and GPT-6 Astra now document in real production. Splitting the A among 96 workers is not an option (it has already been established that the A is non-delegable), but it is not reasonable to require a human to approve each of the 96 outputs individually either: that defeats the reason for parallelizing in the first place.

The resolution is to break the Responsible into two levels, not one:

| Level | Who | RACI role | Traceability mechanism |
|---|---|---|---|
| R-orchestrator | The manager agent that decomposes the task and aggregates results (just one, always named) | Responsible for the final aggregation | Dependency registry from Vol. 4, Chapter 5, Case 8 |
| R-worker | Each of the N dispatched subagents | Responsible for its individual subtask | Trace inherited from the R-orchestrator; needs no human owner of its own |
| A (human) | The registered agent's owner (Chapter 6, Case 6 of Vol. 4) | Approves the aggregation policy and any irreversible actions that result from it | Review by statistically significant sampling, not exhaustive |

The human control point does not move down to the individual worker (that would be unsustainable beyond a dozen agents); it moves to the orchestrator's **aggregation policy**: how it combines 96 partial results into a single conclusion, and what threshold of disagreement among workers triggers a human review before acting. This is, in essence, the same Critic Agent from Chapter 3 of this volume, generalized from a disagreement between two agents to a statistical disagreement among dozens.

## Eisenhower with Agents: What to Delegate and What to Keep

The Eisenhower matrix (classifying tasks by urgency and importance) takes on a new strategic dimension when the potential executor is a swarm of agents. The delegation criterion works as follows:

**Urgent + Not important → Delegate to the swarm.** These are the tasks that consume time without demanding deep judgment: email triage, generating routine reports, updating documentation, monitoring alerts. The agent is faster, more consistent, and cheaper in this quadrant.

**Important + Not urgent → Human, with agentic support.** Strategy, product architecture, hiring decisions, the roadmap vision: these belong to human judgment. The agent can research, synthesize options, and prepare the analysis; the decision remains human.

**Urgent + Important → Human with real-time agentic assistance.** A production crisis, a critical negotiation, a regulatory decision under time pressure: urgency doesn't transfer responsibility to the agent. The swarm speeds up the diagnosis; the human decides.

**Not urgent + Not important → Candidates for elimination.** If a task has neither urgency nor importance, the right question is whether it should be done at all, not who does it (human or agent).

The frequent mistake is to delegate to the agent what is *important* merely because it is also *urgent*. That is where the judgment no model provides gets lost, and the agent's speed turns into speed toward the wrong result.

## The Agility Paradox: More Clarity, Not Less

There is a tempting misunderstanding: since agile values self-organization, defining formal roles would seem to contradict it. That intuition is wrong. Self-organization works when the actors share an implicit understanding of purpose and limits; agents don't share that understanding. Hence, paradoxically, **a team with agents needs more explicit clarity about roles than a purely human one**, not less. RACI and Eisenhower are, in this context, the scaffolding that keeps agility from degenerating into ambiguity.

This paradox has been documented in the literature on work teams in highly automated environments: introducing autonomous systems requires explicit roles, not reduced ones ([Grote, 2012](#ref-grote2012)). Teams that assume "the AI will organize itself" reproduce, on the agentic plane, the same mistake as teams that confuse self-organization with the absence of structure.

---

## Advanced Technical Perspective

**► TECHNICAL TRACK**


### RACI as an Authorization Pattern in Code

From the **Senior Architect's** viewpoint, the RACI matrix is not just an organizational governance artifact: it can and should be implemented as an authorization pattern in the swarm's code. Every action an agent attempts to execute should pass through a **RACIAuthorizationGate** that checks whether the agent has the right role for that action in that context:

```python
from enum import Enum
from dataclasses import dataclass
from typing import Callable, Any

class RACIRole(Enum):
    RESPONSIBLE  = "R"   # Can execute
    ACCOUNTABLE  = "A"   # Never assigned to agents
    CONSULTED    = "C"   # Can provide analysis, not execute the final action
    INFORMED     = "I"   # Receives notification

@dataclass
class AgentPermission:
    agent_id:     str
    action_type:  str
    role:         RACIRole

    def can_execute(self) -> bool:
        """Only R can execute directly."""
        return self.role == RACIRole.RESPONSIBLE

    def can_consult(self) -> bool:
        return self.role in (RACIRole.RESPONSIBLE, RACIRole.CONSULTED)

class RACIAuthorizationError(PermissionError):
    pass


class RACIGate:
    """
    Verifies the agent has the right role before executing.
    If the role is A, it raises an error — accountability is always human.
    """
    def __init__(self, permissions: list[AgentPermission]):
        self._registry: dict[tuple, RACIRole] = {
            (p.agent_id, p.action_type): p.role
            for p in permissions
        }

    def authorize(self, agent_id: str, action_type: str, fn: Callable, *args: Any) -> Any:
        role = self._registry.get((agent_id, action_type))
        if role is None:
            raise RACIAuthorizationError(
                f"Agent '{agent_id}' has no role defined for action '{action_type}'"
            )
        if role == RACIRole.ACCOUNTABLE:
            raise RACIAuthorizationError(
                "RACI violation: no agent may hold the Accountable role. "
                "Assign this action to a human."
            )
        if not AgentPermission(agent_id, action_type, role).can_execute():
            raise RACIAuthorizationError(
                f"Agent '{agent_id}' has role {role.value} for '{action_type}': "
                f"not authorized for direct execution."
            )
        return fn(*args)
```

This implementation makes the RACI rule enforced by the system, not just by people, eliminating the risk of accidental violations.

### Eisenhower as a Task Priority Router in the Swarm

The **Senior Engineer** can implement the Eisenhower logic as a router that assigns incoming tasks to the appropriate executor:

```python
from dataclasses import dataclass

@dataclass
class Task:
    id:          str
    description: str
    urgent:      bool
    important:   bool

def eisenhower_router(task: Task) -> str:
    """
    Returns the recommended executor:
      'swarm'          → autonomous agent
      'human+swarm'    → human with agentic support
      'human_led'      → human leads, agent assists
      'eliminate'      → candidate for elimination
    """
    if task.urgent and not task.important:
        return "swarm"
    elif task.important and not task.urgent:
        return "human+swarm"
    elif task.urgent and task.important:
        return "human_led"
    else:
        return "eliminate"
```

### QA Strategy: Testing Role Boundaries

The **Senior QA** designs tests that verify agents don't exceed their assigned roles, especially that no agent performs Accountable actions:

```python
import pytest

def test_agent_cannot_hold_accountable_role(raci_gate):
    with pytest.raises(RACIAuthorizationError, match="Accountable"):
        perm = AgentPermission("agent-x", "approve_deployment", RACIRole.ACCOUNTABLE)
        raci_gate.authorize("agent-x", "approve_deployment", lambda: None)

def test_agent_with_responsible_role_can_execute(raci_gate):
    result = raci_gate.authorize("agent-draft", "generate_document", lambda: "OK")
    assert result == "OK"

def test_task_routing_urgent_not_important():
    task = Task("t1", "Alert triage", urgent=True, important=False)
    assert eisenhower_router(task) == "swarm"
```

---

## Executive Perspective

**■ EXECUTIVE TRACK**


### The Product Owner's View: RACI in the Backlog

The **Product Owner** builds RACI assignment into the product epics that involve agents. For every epic with an agentic component, the backlog includes an explicit task: *"Define and validate the RACI matrix for the [domain name] swarm."* That task is completed before the swarm's first user story enters a sprint.

The risk of skipping this step is concrete: when the first agent failure happens (and it will), the team will lose valuable sprint time debating who should have reviewed what. Clarity beforehand turns the failure into learning; ambiguity turns it into conflict.

**P.O. health indicator**: the percentage of user stories with an agentic component that have their RACI defined before entering a sprint. The target is 100%.

### The Scrum Master's View: Eisenhower in Sprint Planning

The **Scrum Master** facilitates, at the start of each sprint, a quick review (no more than 15 minutes) of the backlog filtered through Eisenhower. For each agentic item in the sprint, the team answers: *"Is this the right quadrant? Are we assigning this to the right executor?"*

This practice prevents one of the most common antipatterns on teams adopting AI: delegating important-urgent tasks to the agent under sprint pressure, then discovering at review that the result is unacceptable because it required human judgment. The cost of that antipattern, measured in rework and lost trust, far exceeds the cost of the 15 minutes of preventive review.

---

## Alternative Academic Version (Higher Formal Density)

> Applying responsibility assignment frameworks (such as RACI) to complex socio-technical systems is supported by the theory of High Reliability Organizations (HRO), developed by Weick and Sutcliffe (2007). According to this framework, organizations operating in high-consequence environments achieve their reliability not by eliminating uncertainty but by extreme clarification of the response patterns to it. Introducing AI agents into agile teams constitutes, in HRO terms, a new source of systemic uncertainty whose management requires precisely the explicit statement of the accountability patterns that informal self-organization cannot provide. Not delegating the Accountable role to artificial systems is therefore not an arbitrary restriction but the coherent application of the HRO principle of distributed situational awareness: someone in the system must be able to recognize when the agent's behavior has deviated from what is expected and to act accordingly, and that capacity requires moral subjectivity.

---

## Key Takeaways from Chapter 15

- With agents, responsibility tends to blur ("the AI did it"); clarity of roles becomes structurally indispensable.
- The cardinal RACI rule: an agent can be Responsible or Consulted, but never Accountable; accountability cannot be delegated to a machine.
- Eisenhower guides what to delegate: urgent-not-important to the swarm; important to human judgment, even under pressure of urgency.
- The most frequent Eisenhower violation on agile teams: delegating what is important because it is also urgent.
- Implementing RACI as an authorization pattern in code turns the organizational rule into a constraint enforced by the system.
- A team with agents needs more explicit clarity about roles, not less: self-organization presupposes a shared understanding that agents lack.
- The Scrum Master facilitates the Eisenhower review at the start of the sprint to avoid the antipattern of delegating the urgent-important to the swarm.
- When the Responsible party is a swarm of dozens of subagents, the human A moves from approving every output to approving the orchestrator's aggregation policy and the threshold that triggers review.
