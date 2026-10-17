# Chapter 10: Managing AI Expectations and Timelines

> *AI did not eliminate the uncertainty in timelines; it moved it from execution to verification.*

## AI Redefines Time Management; It Does Not Abolish It

The author holds that AI completely redefines how software development timelines are managed. The critical nuance is not that it eliminates the uncertainty, but that it **displaces** it. Before code assistants became widespread, the uncertain part was how long it would take to write the code; now the code appears in minutes (sometimes seconds), but what is genuinely uncertain is how long it will take to *verify that the code is correct, secure, and appropriate for the specific context of the problem*. Expectation management therefore has to be thoroughly relearned: the bottleneck migrated from the keyboard to judgment.

This migration is not a metaphor; it can be measured empirically. Peng et al. (2023, arXiv:2302.06590), in GitHub's study with 95 professional developers, documented that the speed of generating new code increases by 55% with AI assistance. What the same study points out, and what is often left out of executive presentations, is that **the time to review and verify AI-generated code did not shrink proportionally**: developers who used Copilot reported spending more relative time on the critical review phase for generated code than for manually written code, precisely because the assistance increased the volume of code produced per unit of time.

## The Mirage of Speed: Why Fast Generation Doesn't Mean Fast Delivery

There is a dangerous expectation (frequently voiced in management meetings) that is worth taking apart with data: "if AI generates code instantly, projects will be instant." The claim is false, and its falsity is not trivial.

In a complex, changing environment (like the one the author describes in his reflections on programming in contexts of high organizational volatility), the speed of generation doesn't determine the speed of delivery, for three structural reasons:

**First reason: the complexity of the context isn't generated.** A code agent can generate a function in seconds. Without human intervention, it can't understand the implicit constraints of the legacy payment system that function will be integrated into, the compliance policies that affect it, the quirks of the team that will maintain it, or the history of architectural decisions that make certain seemingly correct implementations unviable.

**Second reason: debt is generated quickly, too.** Vaithilingam et al. (2022), in an experimental study of participants using GitHub Copilot published at CHI 2022, found that participants with AI assistance completed more tasks but introduced more bugs into the generated code than participants without assistance (an effect the authors attribute to the lower friction of generation, which inhibits spontaneous verification). Technical debt builds up at the speed of generation if there are no explicit countermeasures.

**Third reason: integration is the real bottleneck.** Generating code is only one part of the delivery process. Integration with the existing system, regression testing, code review, the deployment process, and validation of behavior in production remain operations with minimum durations that the speed of generation does not compress.

## Empirical Evidence: The New Time Curves

The following table summarizes the available data on the impact of AI on the different phases of the development cycle:

| Phase | Before AI | With AI assistants (2024) | Change factor | Source |
|------|----------------|-----------------------------|------------------|--------|
| Generating new code | Days to weeks | Hours to days | 4–10x faster | Peng et al. 2023 |
| Review and verification | Proportional to the code | **Dominates the schedule** | No significant change | Vaithilingam et al. 2022 |
| Integration with the system | Moderate | Critical (no implicit context) | Variable (sometimes slower) | McKinsey 2023 |
| Regression detection | Depends on the test suite | High with evals; low without | Bimodal | Liu et al. 2024 |
| Post-deployment maintenance | High | **High** (debt builds up fast) | No improvement without investment in evals | Jimenez et al. 2024 |

The lesson that emerges from this table is clear: AI flattens the generation curve dramatically, but **it does not flatten the verification, integration, and maintenance curves**. Whoever plans while ignoring these three factors promises deadlines they won't be able to meet, with the difference that now the failure arrives sooner and with a larger volume of committed code.

## A Planning Model for AI-Assisted Projects

Adapting agile planning methods to the context of agentic AI requires revisiting three established conventions:

**1. Story points no longer measure the same thing.** In classic agile estimation, a story point captures the complexity *of implementation*. With AI, implementation is faster; what takes time is verification. Teams that adopt AI without recalibrating their story points experience what might be called "velocity inflation": velocity goes up without value delivery rising in the same proportion.

A practical recalibration is to break the story point into two components: *generation complexity* (how hard it is to describe the problem correctly to the agent) and *verification complexity* (how hard it is to check that the generated solution is correct). In systems with high verification complexity (security, compliance, critical business logic), AI reduces the first but not the second.

**2. The Definition of Done must include verification criteria for generated output.** An increment produced with AI assistance isn't "done" until it has passed a set of explicit checks that go beyond "it compiles and the existing tests pass." The agentic DoD includes: behavioral tests on the identified edge cases, a security review of the generated code, validation of consistency with the system's context, and an assessment of the technical debt introduced.

**3. The retrospective must track the ratio between generation and verification.** The most useful indicator for calibrating AI adoption on an agile team is the time spent verifying per hour of assisted generation. A ratio above 3:1 suggests the task specification given to the agent is deficient; a ratio below 0.5:1 suggests verification is insufficient and debt is silently accumulating.

## The CI/CD Pipeline for AI-Generated Code: What to Add

**► TECHNICAL TRACK**


Conventional continuous integration and deployment pipelines need to be extended when the code is partially or entirely generated by AI assistants. The minimum extensions required are:

- **Reinforced static analysis**: static tools should be configured with stricter rules for AI-generated code, where patterns of logical copy-paste and unnecessary dependencies are more frequent.
- **Mutation testing**: verifies that the existing tests are capable of detecting bugs in the generated code, not just in manually written code.
- **Authorship tracking**: marking what percentage of the code in each PR was generated by AI makes it possible to calibrate the level of review needed and to build historical data on bug rates by the origin of the code.
- **Automated behavior evals**: for critical functions, an evaluator agent (cf. Chapter 32, eval design) verifies that the generated behavior is consistent with the business specifications, not just with the unit tests.

## Quantified ROI: When and How Much AI Saves

**■ EXECUTIVE TRACK**


The most frequent executive question (and the worst answered) is: "how much ROI do we get from AI in software development?" The right answer depends on two variables that simplistic analyses ignore: the nature of the tasks (high vs. low verifiability) and the team's maturity in using AI tools.

McKinsey Global Institute's analysis (2023) estimates that generative AI can automate the equivalent of 60-70% of the time spent on documentation, test generation, and boilerplate code. For architectural design, resolving complex bugs in legacy systems, and product decision-making, the percentage of automation falls to 10-20%.

The most honest ROI model is therefore **bimodal**:

| Type of task | Share automatable | Typical ROI (6 months) | Necessary condition |
|---------------|-------------------------|---------------------|---------------------|
| Boilerplate, docs, unit tests | 60–70% | 3–5x | Teams with good specs |
| Design, complex debugging, decisions | 10–20% | 1.2–1.5x | Only with seniors who have judgment |
| Integration and verification | 5–15% | 0.8–1.1x | Requires prior investment in evals |

The third type (integration and verification) can have an ROI below 1 in the short term if no investment is made in evaluating the generated code. This is the unspoken risk of rushed implementations.

## Managing the Stakeholder: Pedagogy as an Executive Competency

**■ EXECUTIVE TRACK**


Expectation management therefore becomes, above all, an exercise in executive pedagogy. The leader must translate the complexity of the generation/verification asymmetry into language a nontechnical stakeholder can understand and act on.

Three messages are essential and non-negotiable. First, **generation is cheap, but correction is expensive** (the cost of an error in AI-generated, unverified code is comparable to that of code written under time pressure, and in some cases higher). Second, **speed without verification is debt disguised as progress** (an increment delivered in days that introduces bugs into production has no positive ROI). Third, **the value is not in producing more code, but in producing the right code** (lines of code generated per sprint is a process indicator, not a measure of business value).

Whoever communicates these three messages clearly and consistently doesn't just govern expectations: they turn AI adoption into a real competitive advantage instead of a marketing pressure.

**Alternative version (higher academic density):**

Managing time expectations in software development projects with generative artificial intelligence assistance is a strategic communication problem. It involves translating technical asymmetries (specifically, the divergence between the reduction in code generation times and the absence of an equivalent reduction in verification and validation times) into cognitive frameworks accessible to organizational actors with different levels of technical literacy. The available empirical evidence ([Peng et al., 2023](#ref-peng2023); [Vaithilingam et al., 2022](#ref-vaithilingam2022)) suggests that the lack of this translation is the primary factor in the gap between the declared expectations of AI productivity and the results measured in real projects.

## Key Takeaways from Chapter 10

- AI moves the uncertainty in timelines from generation to verification; the bottleneck migrated from the keyboard to judgment.
- Peng et al. (2023): +55% in code generation speed, with no proportional reduction in verification time.
- Vaithilingam et al. (2022): more tasks completed with AI, but more bugs introduced (the lower friction of generation inhibits spontaneous verification).
- Story points should be broken into generation complexity and verification complexity; AI reduces the first, not the second.
- The agentic DoD includes edge cases, a security review, consistency with the system's context, and an assessment of debt.
- CI/CD for AI code extends the pipeline with reinforced static analysis, mutation testing, authorship tracking, and automated behavior evals.
- ROI is bimodal: 3–5x on boilerplate/docs/tests; 0.8–1.1x on integration and verification without prior investment in evals.
- Managing stakeholders is pedagogy: generation is cheap, correction is expensive; speed without verification is disguised debt.
