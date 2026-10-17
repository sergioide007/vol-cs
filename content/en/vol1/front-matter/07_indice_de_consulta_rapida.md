# Quick Reference Index: Problem → Direct Solution

*Operational navigation aid. When you need to resolve an immediate production defect rather than reading sequentially, this index routes you directly to the relevant section. References marked "Ex. X.Y" point to fully worked code exercises.*

## 1. By Symptom or Objective

| If You Need To… | Go To | Immediate Support |
|---|---|---|
| Determine whether your system is an agent or a fixed workflow | Ch. 1, "What Is, Formally, an Agent?" | Ex. 1.1 (Autonomy Spectrum) |
| Define the AI Engineer hiring profile and interview rubrics | Ch. 2, "The Seven Core Competencies" | Ex. 2.1 (Eight-Week Transition Curriculum) |
| Centralize API keys, token quotas, and model auditing | Ch. 3, "The AI Gateway" | Ex. 3.1 (Per-Project Circuit Breaker) |
| Prevent infinite loops and cap per-task token expenditure | Ch. 4, "Resilience in Production: The Harness as Control System" | Ex. 4.1 (Design the Production Harness) |
| Design tools an agent cannot misuse or hallucinate parameters for | Ch. 4, "Actionable Error Design"; Ch. 9, "Clean MCP Tools" | Ex. 4.2, Ex. 9.1 |
| Divide work among multiple specialized agents without chaos | Ch. 5, "Applying Specialization to Code" | Ex. 5.1 (Ticket Triage Pipeline) |
| Prevent AI from silently violating business domain invariants | Ch. 6, "Class Diagrams: Domain Aggregates in DDD" | Ex. 6.1 (Bounded Context Implementation) |
| Codify an engineering SOP into an executable agent skill | Ch. 7, "The Five Skill Patterns" | Ex. 7.1 (Pre-Deploy Validation Skill) |
| Select an orchestration topology and graceful degradation policy | Ch. 8, "The Five Canonical Patterns" | Ex. 8.1 (Select the Topology) |
| Connect agents to enterprise backends under strict governance | Ch. 9, "Catalog Admission Protocol" | Ex. 9.1 (Deploying a Fourth MCP Tool) |
| Structure and version the instruction corpus in Git | Ch. 10 ("The Architecture of Context") | — |
| Decouple deterministic infrastructure from probabilistic inference | Ch. 4 (Harness) and Ch. 6 (Deterministic Verifiers) | Ex. 4.1, Ex. 6.1 |
| Understand technical shelf life and deprecation risks | Note on Technological Shelf Life | — |

## 2. Index of Worked Exercises in This Volume

| Exercise | Core Competency Trained | Chapter |
|---|---|---|
| Ex. 1.1 | Classifying systems across the Autonomy Spectrum | 1 |
| Ex. 2.1 | Designing an eight-week engineer conversion program | 2 |
| Ex. 3.1 | Implementing per-project budget cutoffs in an AI Gateway | 3 |
| Ex. 4.1 | Engineering a production-grade defensive harness | 4 |
| Ex. 4.2 | Building two typed tools, a budget limit, and actionable errors | 4 |
| Ex. 5.1 | Architecting a multi-agent ticket triage pipeline | 5 |
| Ex. 6.1 | Implementing an inventory domain aggregate and bounded context | 6 |
| Ex. 7.1 | Authoring a pre-deploy validation skill with progressive disclosure | 7 |
| Ex. 8.1 | Selecting the optimal orchestration topology under risk constraints | 8 |
| Ex. 9.1 | Extending an MCP server with a fourth auditable tool | 9 |

## 3. What to Do If Your Issue Is Not Addressed Here

This volume focuses on foundational principles and core architecture. If your operational bottleneck concerns **scale and runtime economics** (cost per task, CIU metrics, agentic testing pyramids, disaster recovery), consult Volume 4. If it relates to **agentic cybersecurity, critical industries, or geopolitics**, see Volume 2. If it concerns **enterprise governance, team topologies, or organizational maturity**, consult Volume 3. The Series Map in the Reading Guide clarifies cross-volume dependencies.
