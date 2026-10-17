# State of the Art: Governance, Accountability, and Human Oversight in Autonomous AI Systems

*Critical review of indexed literature (2019–2026), prepared as academic support for Volume 3: Organizational Maturity*

## 1. Main Research Lines

**Line 1: AI governance as an established field.** The systematic review by Batool, Zowghi, and Bano (2023/2024, arXiv:2401.10896) is the most-cited reference in the field of *Responsible AI Governance*. It finds that although many principles and governance frameworks exist, there is still a gap between those principles and how they are actually implemented in organizational models of leadership and decision-making. That is the same gap Chapter 20 of this volume tries to close with an operational protocol, not just a declarative one.

**Line 2: Regulatory and risk frameworks.** Here the NIST AI Risk Management Framework (2023), ISO/IEC 42001 (2023), and the EU AI Act converge, and all three are cited again and again as the structural reference frameworks (Floridi & Cowls, 2019; Mittelstadt, 2019; OECD, 2022, according to the synthesis in "The Governance Inversion Hypothesis," 2026). Notably, recent literature is starting to document a tension this book also takes up: regulatory frameworks move more slowly than the technical capability of the systems they aim to regulate (Anderljung et al., 2023, cited in the systematic literature review on compliance in critical sectors).

**Line 3: Accountability and distributed responsibility.** This is the line most directly connected to Chapter 15 of this volume (RACI with agents). Recent literature on legal and organizational responsibility in autonomous systems (a 2026 comparative analysis of regulation and risk-based governance frameworks) states explicitly that current methods for assigning responsibility among the different roles in an AI system remain fragmentary, and that the lack of clarity gets worse in complex multi-component systems (Stahl, 2023; Yazdanpanah et al., 2023). This is exactly the problem the "RACI at scale" in this book tries to solve with a concrete operating rule, not just a call for greater clarity.

**Line 4: Governance of agentic AI in enterprise operations.** A 2025 systematic review of the rise of agentic AI in enterprise operations documents the cost savings and greater operational efficiency that adopting organizations report, along with recurring concerns about ethical accountability, data security, and the effect on human employment (Chan et al., 2023, cited in that review). The same review notes that agentic AI has gained particular traction in high-risk settings such as healthcare and finance (Gridach et al., 2025), domains structurally similar to the "sector case" that closes Chapter 5 of Vol. 4 of this series.

## 2. Theoretical Frameworks Used

The AI governance literature does not start from a single theory. It imports frameworks from three different traditions: **applied ethics** (the principles of Floridi & Cowls, with their "AI4People" synthesis), **classical organizational theory of bureaucracy** (Bovens & Zouridis, 2002, "From Street-Level to System-Level Bureaucracies," a direct antecedent, though it predates LLMs, of the question of what happens to human discretion when an information system automates decisions), and **risk management** (the NIST and ISO frameworks mentioned above). This volume implicitly adopts a synthesis of the three, but in a more operational way than most of the literature reviewed: where the academic frameworks state principles (transparency, explainability, human oversight), Chapter 20 of this book turns them into a numerical threshold (the Operational Autonomy Index) and an executable audit protocol.

## 3. Methodologies Applied

Systematic literature reviews with an explicit protocol predominate (several of those cited follow PRISMA or variants of Kitchenham), along with meta-analyses of public policy frameworks (Kluge Correa et al., who analyzed 200 global policies and ethics guidelines to identify 17 prevalent principles) and sector case studies (healthcare, finance, the public sector). Empirical research that quantitatively measures the actual level of autonomy of a system in production is notably scarce. Most of the literature works with qualitative categories (high/low risk, supervised/unsupervised), not with a continuous index comparable to the one proposed in this volume.

## 4. Recurring Findings

- Broad consensus that accountability is a multidimensional concept that can no longer be reduced to the legal sphere and must cover organizational oversight, transparency, and risk management across the system's entire life cycle (Novelli et al., 2024; Stahl, 2023).
- Consensus that ethics alone, without technical verification and safety alignment, is not enough as a basis for governance, a shift the 2024–2025 literature explicitly marks as more recent than the purely declarative approach of earlier years.
- A documented tension between innovation and compliance in critical sectors: organizations report operating in a "compliance corridor" that is both restrictive and poorly defined (Wang & Wu, 2024).

## 5. Disagreements Among Authors

The disagreement most relevant to this volume is one of level of abstraction. One part of the literature (the regulatory frameworks: NIST, ISO, the EU AI Act) works at the level of general principles that apply to any AI system. Another part, more recent and still a minority, is beginning to recognize that large-scale reasoning systems (LRMs and agentic LLMs) are "socio-technical decision infrastructures" that need to be managed by risk level and not treated as conventional software. This book explicitly sides with the second position and goes a step beyond what the reviewed literature offers: while the academic literature stops at the diagnosis ("differentiated risk-based management is needed"), this volume supplies the mechanism (the OAI's green/yellow/red weight table).

## 6. Methodological Limitations of the Literature Reviewed

- **A predominance of policy studies over engineering studies.** Most of the AI governance literature comes from schools of public policy, law, and applied ethics, not from software engineering. That explains why it is strong on taxonomies of principles and weak on verifiable operating mechanisms, precisely the gap this volume, written from engineering, aims to fill.
- **Little empirical validation of the proposed frameworks.** Several of the systematic reviews cited point out that the governance frameworks reviewed rarely include evidence of successful, measured implementation beyond isolated case studies that can't be compared with one another.
- **Geographic and institutional bias.** The policy literature is dominated by frameworks from the EU, the US, and multilateral bodies (the OECD). Frost et al.'s review of Canada's national AI strategy is one of the few references with an explicit focus outside those three poles, and none of the sources reviewed here addresses Latin America in comparable depth. The chapter on El Niño and the Panama Canal, and this book's cases on Sber (Russia) and Doraleh (Djibouti), partly make up for this gap, though they do not replace formal academic research on the region.

## 7. Knowledge Gaps

1. **No quantitative autonomy metrics that can be compared across organizations**: as far as this review could verify, this book's OAI is an original proposal with no direct antecedent published in the indexed literature reviewed.
2. **No audit protocols that are agnostic to the model provider**: all the AI audit literature reviewed assumes a system with a fixed model, and none explicitly addresses what happens to the validity of an audit when the underlying model changes, the exact problem that the cross-reproduction audit in Chapter 20 solves.
3. **Little research on RACI or other human responsibility assignment frameworks specifically adapted to swarms of dozens of agents**: the distributed responsibility literature is rich in principles but not in mechanisms that scale.

## 8. Relationship to the Book's Central Thesis

This volume's thesis is that governance must be expressed in verifiable mechanisms and not only in declared principles, and that this governance must survive a change of model provider. In the literature it finds a convergent diagnosis (the gap between principles and operating mechanisms, Sections 1 and 5) but no published solution. That positions this volume's original contributions (the OAI and the cross-reproduction audit) not as a synthesis of what already exists, but as a direct answer to a gap the academic literature itself acknowledges and has not yet closed.
