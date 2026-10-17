# Chapter 3: Testing Agentic Systems

## The TDD of Artificial Intelligence

Testing LLM-based systems introduces a new epistemological problem: the output is not deterministic. Two runs of the same agent with the same input can produce different outputs, both correct. Traditional testing frameworks, designed to verify exact equality (`assertEqual`), break in this context.

The solution is to replace exact assertions with *criteria-based evaluations*, what the community calls **evals**. An eval defines what properties an acceptable output must have and measures, over a set of cases, what fraction of outputs meet them. The mental shift for a classic engineer: stop asking "is it equal to what was expected?" and start asking "does it meet the criteria, at what rate, and does that rate improve or worsen with each change?"

The agentic testing pyramid has three levels, from cheapest to most expensive:

1. **Deterministic assertions on properties.** The JSON parses against the schema; the code compiles; the generated code's tests pass; the response doesn't exceed N words; it contains no credentials. Everything verifiable with code is verified with code: it is free and doesn't hallucinate.
2. **LLM-as-judge.** One model evaluates another's output against explicit criteria. The empirical validation of the pattern is solid: well-instructed LLM judges reach more than 80% agreement with human evaluators, the same level of agreement humans have with each other ([Zheng et al., 2023](#ref-zheng2023)). With two caveats the same study documents and every harness must mitigate: position bias (preferring the first option presented; mitigated by evaluating in both orders) and verbosity bias (preferring longer answers; mitigated by instructing against it explicitly).
3. **Sampled human evaluation.** Expensive and slow; reserved for periodically calibrating the automatic judges and for high-risk cases.

And a cross-cutting rule taken from agent evaluation research: **every eval reports cost in addition to quality** ([Kapoor et al., 2024](#ref-kapoor2024)). A change that raises the success rate from 88% to 91% by tripling the tokens is not an improvement; it is a business decision someone must make with both numbers in front of them.

**► TECHNICAL TRACK: Evaluation Framework with LLM-as-judge**

```python
# Example 3.1: Eval with criteria + LLM-as-judge, with structured output.
# The judge returns JSON validated against a schema: no regex, no surprises.

import json
import anthropic

client = anthropic.Anthropic()

JUDGE_SCHEMA = {
    "type": "object",
    "properties": {
        "evaluations": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "criterion": {"type": "string"},
                    "score": {"type": "number"},
                    "evidence": {"type": "string"},
                },
                "required": ["criterion", "score", "evidence"],
                "additionalProperties": False,
            },
        },
        "global_score": {"type": "number"},
        "verdict": {"type": "string", "enum": ["PASS", "FAIL"]},
        "main_reason": {"type": "string"},
    },
    "required": ["evaluations", "global_score", "verdict",
                 "main_reason"],
    "additionalProperties": False,
}

def eval_with_criteria(
    agent_output: str,
    criteria: list[str],
    pass_threshold: float = 0.7,
) -> dict:
    """
    Evaluates an agent's output using another LLM as the judge.
    Built-in mitigations: explicit criteria, mandatory textual evidence,
    an anti-verbosity instruction, structured output.
    """
    criteria_fmt = "\n".join(f"{i+1}. {c}" for i, c in enumerate(criteria))

    judgment = client.messages.create(
        model="claude-opus-4-8",
        max_tokens=2048,
        system="""You are an objective technical evaluator. You evaluate whether
        an output meets a list of criteria. For each criterion:
        - Assign a score from 0.0 (does not meet) to 1.0 (meets perfectly)
        - Quote the textual evidence from the output that justifies the score
        - Be strict: 0.7+ only if the criterion is clearly met
        - Do NOT reward length: a concise response that meets the
          criterion scores the same or better than a long one.""",
        messages=[{
            "role": "user",
            "content": (
                f"OUTPUT TO EVALUATE:\n{agent_output}\n\n"
                f"EVALUATION CRITERIA:\n{criteria_fmt}\n\n"
                f"PASS THRESHOLD: {pass_threshold}"
            ),
        }],
        output_config={"format": {"type": "json_schema",
                                  "schema": JUDGE_SCHEMA}},
    )

    result = json.loads(
        next(b.text for b in judgment.content if b.type == "text")
    )
    result["passed"] = result["global_score"] >= pass_threshold
    return result


# Regression suite for the Chapter 5 code review agent:
def test_code_review_agent():
    vulnerable_code = '''
def login(username, password):
    query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
    return db.execute(query)
    '''

    agent_output = run_agent("reviewer",
                             f"Review this code:\n{vulnerable_code}")

    criteria = [
        "Identifies the SQL injection vulnerability present in the code",
        "Mentions that interpolating strings into SQL queries is dangerous",
        "Suggests prepared statements or parameterized queries as the fix",
        "Assigns high or critical severity to the finding",
        "The report is actionable: it says what to change and where",
    ]

    result = eval_with_criteria(agent_output["output"], criteria,
                                pass_threshold=0.75)

    assert result["passed"], (
        f"The code review agent failed the evaluation.\n"
        f"Score: {result['global_score']}\n"
        f"Reason: {result['main_reason']}"
    )
    return result
```

### From the One-Off Eval to the Regression Suite

An isolated eval is an anecdote; a suite is engineering. The practices that separate the two:

- **A versioned case set.** Dozens to hundreds of representative inputs (including the hard cases that have already failed in production, which are the most valuable) in the repository, next to the code.
- **Running in CI.** Every change of prompt, model, or tool runs the suite. Changing a prompt without running the evals is as professional as changing code without running the tests.
- **Metrics with thresholds.** Success rate, average cost per case, p95 latency. The build fails if quality drops or cost spikes.
- **In batch and at half price.** Eval suites are the perfect use case for batch APIs: asynchronous, massive, at a 50% discount.
- **Periodic judge calibration.** A monthly sample evaluated by humans, compared against the judge, maintains confidence in the system ([Zheng et al., 2023](#ref-zheng2023)).

**■ EXECUTIVE TRACK**

The right executive question about any agentic system in production is "**how would we know if it got worse?**", not "how good is it?" Without an eval suite, the real answer is "from customer complaints": a monitoring system with an unacceptable reputational cost. The eval suite is to the agentic system what the test suite is to classic software: the condition of possibility for safe change. Budgeting for it isn't optional; it is the difference between operating a system and praying to it.

## Worked Exercise 3.1: The Onboarding Agent's Criteria

**Problem.** Write the evaluation criteria for the Chapter 5 onboarding agent (it answers new engineers' questions from internal documentation, with citations). Cover the three levels of the pyramid and point out which criterion is the hardest to word well.

**Annotated solution.** **Level 1 (deterministic):** every response contains at least one citation in `[SOURCE n]` format; every cited `n` exists in the retrieved sources; the response doesn't exceed 400 words; zero credentials or secrets in the text. **Level 2 (LLM-as-judge):** "every technical claim is backed by the cited source" (the judge verifies claim by claim against the fragment); "if the sources don't contain the answer, the agent says so and suggests whom to ask"; "the tone is that of a mentor, not a manual." **Level 3 (human, sampled):** would the response really have unblocked a new engineer? The hardest criterion is the second one at level 2, the **honest "I don't know"**, because it requires test cases whose answer *is not* in the corpus, and the temptation to measure only what the system knows how to answer is precisely how eval suites become decorative. A derived rule of thumb: at least 20% of the case set must be deliberately unanswerable, and the metric for that subset (correct abstention rate) is reported separately.

## Key Takeaways from Chapter 3

- Nondeterministic output breaks `assertEqual`: you evaluate with criteria and rates, not exact equality.
- Three-level pyramid: deterministic assertions (free), LLM-as-judge (valid and cheap, with known, mitigable biases; [Zheng et al., 2023](#ref-zheng2023)), sampled humans (calibration).
- Every eval reports cost alongside quality ([Kapoor et al., 2024](#ref-kapoor2024)): +3 points for 3× tokens is a business decision, not an improvement.
- The suite lives in the repository, runs in CI, fails the build, and feeds on real production failures.
- Changing a prompt without running the evals is a direct commit to main.

---
