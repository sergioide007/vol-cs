# Chapter 7: Skill Engineering: Teaching Procedures to Autonomous Agents

## Skills: The Procedural Knowledge of the Agent

If autonomous agents function as the specialized workers of the Synthetic Enterprise, **skills** represent their standard operating procedures: packaged, deterministic workflows that an agent invokes consistently and reproducibly. The paradigm resolves an acute problem in context architecture: specialized operational procedures cannot reside permanently within the global system prompt (which would bloat prompt token count, inflating inference costs and triggering context degradation [Liu et al., 2024](#ref-liu2024)), nor can they be improvised stochastically on every task. A skill represents the optimal equilibrium: a modular unit of procedural knowledge governed by **progressive disclosure**, where a lightweight semantic description is permanently resident in the tool index, while the full operational instructions are loaded dynamically only when triggered by user intent.

Within platforms such as Claude Code and modern agent runtimes, a skill is a structured Markdown artifact defining:

1. **Activation Trigger** (When to execute, determined by semantic intent matching)
2. **Execution Protocol** (What step-by-step procedure to execute)
3. **Tool Registry** (The minimal necessary effector tools exposed)
4. **Output Schema** (The machine-readable contract returned)

This architecture transcends individual vendors: Google and OpenAI deploy analogous mechanisms for packaged execution runtimes and tool bundles. The foundational invariant the AI Engineer must master is architectural: **procedural engineering knowledge is version-controlled in the repository and loaded on demand**.

The canonical anatomy of a production-grade skill:

```markdown
---
name: domain-review
description: |
  Audits synthetic code to verify compliance with the domain bounded context.
  TRIGGER when: user requests domain logic review, mentions DDD, bounded context,
  or following code generation for core business logic.
  DO NOT TRIGGER for: infrastructure code, frontend UI styling, simple unit tests.
tools:
  - Read
  - Grep
  - Bash
---

# Skill: Domain Review

## Objective
Verify that synthesized code complies with declared Bounded Contexts and
violates zero core domain invariants.

## Execution Protocol

### Step 1: Discover the Bounded Context
- Locate the domain context file: `grep -r "BOUNDED CONTEXT" docs/ domain/`
- Fallback: if absent, infer a baseline specification from discovered domain entities

### Step 2: Static Anti-Pattern Analysis
Audit the codebase for these specific architectural anti-patterns:
- Direct database access from domain entities: `grep -r "db\." domain/`
- Domain entities leaked directly into API controllers: verify presence of DTOs
- Business validation logic inside repository implementations: enforce CRUD boundaries

### Step 3: Invariant Verification
For every business invariant declared within the domain context:
- Trace where the rule is implemented in source code
- Verify the presence of an automated unit test covering that rule
- Flag as "Missing Coverage" if no automated assertion exists

### Step 4: Output Synthesis
Emit the findings adhering strictly to this schema:
- VERDICT: [1 line: PASS / FAIL + total violation count]
- CRITICAL VIOLATIONS: [breached domain invariants]
- WARNINGS: [discovered architectural anti-patterns]
- REQUIRED REMEDIATIONS: [ordered list of required code modifications]
```

The skill above represents the **operational execution of Chapter 6**: the domain context establishes business invariants; the skill formalizes the procedural algorithm to audit them. This synthesis—static domain knowledge files combined with dynamic execution procedures—characterizes mature context engineering.

## The Five Canonical Skill Patterns

```
Pattern 1: ANALYSIS SKILL
─────────────────────────
Purpose:    Deep structural inspection of existing repository artifacts
Trigger:    "analyze", "audit", "review", "what does X do?"
Pipeline:   Read -> Grep -> Semantic Analysis -> Structured Report
Examples:   security-review, domain-review, performance-audit

Pattern 2: GENERATION SKILL
───────────────────────────
Purpose:    Synthesizing greenfield artifacts adhering to architectural templates
Trigger:    "create", "generate", "scaffold", "implement X"
Pipeline:   Ingest Template -> Adapt to Context -> Write Artifact -> Verify
Examples:   generate-api-endpoint, scaffold-domain-entity, create-test-suite

Pattern 3: TRANSFORMATION SKILL
───────────────────────────────
Purpose:    Refactoring an artifact from Format A to Format B
Trigger:    "migrate", "convert", "refactor to X"
Pipeline:   Read -> AST/Structure Analysis -> Transform -> Assert Parity
Examples:   refactor-to-ddd, migrate-to-typescript, convert-to-async

Pattern 4: ORCHESTRATION SKILL
──────────────────────────────
Purpose:    Coordinating multiple specialized agents or toolchains in sequence
Trigger:    "deploy", "full pipeline", "end-to-end promotion"
Pipeline:   Plan -> Dispatch Sub-Agents -> Consolidate Results -> Synthesize
Examples:   full-deploy-pipeline, code-review-council, onboard-new-service

Pattern 5: VALIDATION SKILL
───────────────────────────
Purpose:    Formally asserting that contracts and invariants remain intact
Trigger:    "verify", "validate", "is this correct?", pre-merge/pre-deploy
Pipeline:   Define Invariants -> Execute Assertions -> Emit Go/No-Go
Examples:   verify-api-contracts, validate-domain-invariants, pre-deploy-check
```

**► TECHNICAL TRACK: Authoring a Production Skill**

```bash
# Directory hierarchy for version-controlled agent skills
mkdir -p .claude/skills

# Reference implementation: Automated Token Cost Audit Skill
cat > .claude/skills/cost-audit.md << 'EOF'
---
name: cost-audit
description: |
  Audits foundation model API invocations in code and estimates monthly spend.
  TRIGGER when: user inquires about costs, mentions Token-Burn, requests
  inference spend optimization, or prior to production deployment.
tools:
  - Grep
  - Read
  - Bash
---

# Skill: Cost Audit

## Objective
Detect all foundation model API invocations across the codebase and model
expected monthly spend based on projected volume.

## Protocol

1. Discover all model inference invocations across source files:
   `grep -rn "messages.create\|chat.completions\|generate_content" --include="*.py" .`

2. For each discovered invocation point:
   - Identify the target model ID
   - Estimate baseline input tokens (system instructions + typical context)
   - Estimate maximum output tokens (configured `max_tokens`)
   - Calculate unit cost per request against the local pricing schedule

3. Model monthly transaction volume based on:
   - Synchronous HTTP endpoints: inspect access logs or document conservative estimates
   - Asynchronous batch workers: read scheduler crontab configuration
   - Internal CLI tools: query active developer headcount

4. Emit output matrix: Function | Target Model | Tokens/Call | Cost/Call | Projected Monthly Cost

## Pricing Schedule
DO NOT utilize memorized or hallucinated pricing: parse the versioned
`config/llm_pricing.json` file in the repository (calibrated quarterly
by the platform team). If absent, halt and instruct the user to seed it
from the provider's official pricing page.
EOF
```

The concluding directive of this skill—forbidding memorized rates and mandating a versioned configuration file—enforces a fundamental engineering invariant: **skills must never contain volatile, time-sensitive data**. They encapsulate enduring *procedures* that query transient *data* from versioned configuration files. A skill hardcoding 2026 model pricing will hallucinate obsolete figures in 2028.

**■ EXECUTIVE TRACK**

Skills represent the definitive solution to an existential executive challenge: "How do we prevent institutional knowledge from vanishing when senior engineers depart?". The classical solution—confluence wikis and markdown docs—fails systematically because static text is never executed, drifting quietly into obsolescence. A skill is documentation that **executes**: when an operational procedure drifts, the skill fails with an automated error, forcing immediate remediation. An enterprise skill library represents institutional know-how compiled into an executable digital asset: discoverable, versioned, and instantly transferable to incoming human developers and autonomous agents alike.

## Clean Skills: Architecture and the Pull Request Review Checklist

Applying Synthetic Clean Code (Chapter 4) to skill engineering yields two concrete mechanisms. The first is the **Canonical Skill Template**, the procedural counterpart to Chapter 5's Master System Prompt: every skill in the enterprise originates from the identical structural schema (frontmatter with positive/negative triggers, single-sentence objective, ordered numbered protocol, deterministic output schema), ensuring that reviewing a peer's skill is as effortless as reviewing your own.

The second is the **Skill Pull Request Review Checklist**, enforcing the principle that skills are production source code subjected to mandatory peer review:

1. **Unambiguous Name and Explicit Triggers.** Does the identifier describe the action (`cost-audit`, never `utils`)? Does the description codify when to trigger **and when NOT to trigger**? Negative triggers eliminate false activations, the most pervasive operational defect.
2. **Single Responsibility Principle (SRP).** Does it encapsulate exactly ONE procedure? A skill that analyzes "and opportunistically fixes" represents two skills poorly coupled.
3. **Zero Hardcoded Volatile Data.** Are version tags, model IDs, pricing rates, or changing endpoints present? They must be externalized to versioned config files.
4. **Principle of Least Privilege (Minimal Tools).** Is the `tools` array strictly bounded? An audit or analysis skill must never hold write permissions to the filesystem or shell.
5. **Machine-Verifiable Output Contract.** Does the output schema allow automated eval assertions (Volume 4, Chapter 3)?
6. **Automated Test Coverage.** Does the pull request include at least one reproducible test scenario with expected input and assertion output?

Six inspection questions, two minutes per review: the difference between an enterprise skill platform and a disorganized drawer of personal prompts.

## Worked Exercise 7.1: Architect a Pre-Deployment Validation Skill

**Problem Statement.** Instantiate Pattern 5 (Validation) to author a `pre-deploy-check` skill that audits three deployment preconditions prior to production release: automated test suite passes, zero plaintext secrets in source files, and CHANGELOG.md is updated with the current release version. Apply the review checklist.

**Walkthrough Solution.**

```markdown
---
name: pre-deploy-check
description: |
  Audits production deployment prerequisites: test suite, secrets, changelog.
  TRIGGER when: user requests deployment, mentions release, or pre-deploy checks.
  DO NOT TRIGGER for: local development builds, sandbox, or staging deployments.
tools:
  - Bash
  - Grep
  - Read
---

# Skill: Pre-Deploy Check

## Objective
Emit a machine-verifiable Go/No-Go decision before triggering production release.

## Protocol
1. Test Suite: Execute project test runner (`npm test` or `pytest -q`);
   capture exit code.
2. Secret Scanning: `grep -rEn "(api[_-]?key|secret|password)\s*[:=]\s*['\"]"`
   across source directories, ignoring mock tests and documentation examples.
3. Release Changelog: Verify that CHANGELOG.md includes an entry matching
   the current version tag in the project manifest.

## Output Report (Strictly Formatted Contract)
- VERDICT: GO | NO-GO
- CHECKS: [test_suite: PASS / FAIL] [secrets_scan: CLEAN / FINDINGS] [changelog: VALID / MISSING]
- BLOCKERS: [list of blocking issues, empty if VERDICT is GO]
```

Audit against the review checklist: (1) explicit positive and negative triggers; (2) strictly single responsibility: *validates*, never automatically mutates or deploys (production release is a high-consequence action governed by human approval, Volume 3, Chapter 1); (3) zero hardcoded tool versions; (4) constrained to read-only tooling (`Bash`, `Grep`, `Read`) without write effectors; (5) the `VERDICT/CHECKS/BLOCKERS` contract is trivially verified via automated regex assertions; (6) minimal test fixture: executing the skill against a test repository containing a planted credential must reliably emit `NO-GO` with the file path cited.

## Chapter 7 Takeaways

- A skill = version-controlled procedural knowledge operating under progressive disclosure: lightweight triggers in index, deep protocols loaded on demand.
- Five canonical patterns: Analysis, Generation, Transformation, Orchestration, and Validation. Instantiate patterns; do not improvise from scratch.
- Skills must never contain perishable data: enduring procedures querying versioned configuration files.
- Enforce the 6-point Skill Review Checklist across every pull request; treat skills as production software.
- A skill is executable documentation: when an engineering practice decays, the skill breaks with an automated alert, forcing immediate remediation.

---
