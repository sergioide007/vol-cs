# Chapter 9: The Coverage Week: Working with Claude on a Real Project

## The Starting Point: A Tuesday with a Deadline

On Tuesday I got the message no engineer wants to receive in the middle of a sprint: "Quality review next week. Coverage has to be above 80% and issues at zero. All the issues."

The project was a legacy inventory and payments management system: Spring Boot 3.2 on the backend, Angular 17 on the frontend, PostgreSQL as the database. Four years of code, three teams that had rotated through, and a history of "we'll fix it later" that nobody had honored. The JaCoCo report said 38%. There were 23 open issues in the tracker, most of them validation errors nobody could close because the code had no tests, and any change could break something without anyone knowing.

I had four and a half days.

This chapter is the diary of that week: every command, every prompt, what worked and what didn't, and what it cost in tokens. By Friday evening, coverage was at 82.3% and the issue tracker was at zero. What follows is exactly how we got there.

> **Cost note:** the API prices are those in Appendix B, with its cutoff date. This chapter doesn't repeat them: it reads them from there, and having a single place to update prices is what keeps this chapter and the appendix from contradicting each other in the third edition. This week's calculations also apply to the consumer subscription, which offers a monthly ceiling instead of a per-call cost: convenient for daily work, but without the granularity of knowing what you spent on what. That granularity is what the CIU metric from Chapter 1 demands.

## 9.1 Before Generating a Single Test: Reading the Terrain

The first mistake most teams make when AI enters the scene is to use it immediately, without understanding the problem. The model knows nothing about your project; what you don't give it in context, it invents. And an invented test that passes is not a test: it is technical debt disguised as a green metric.

Diagnosis first, generation later.

**► TECHNICAL TRACK: Initial Diagnosis with JaCoCo**

```bash
# 1. Generate the coverage report
mvn clean verify -pl backend

# The report ends up at:
#   backend/target/site/jacoco/index.html
#
# What to look for in the report:
#   - "Missed Branches" column: the uncovered if/switch statements
#   - Classes with 0% coverage: the ones never touched
#   - Packages with coverage < 40%: refactoring candidates

# 2. Export the summary to CSV to read it in Claude
mvn jacoco:report
cat backend/target/site/jacoco/jacoco.csv | head -50
```

With the report in hand, the picture was clear: the `application/` package (business services) had 12% coverage because nobody had written a single unit test for the services. The `domain/` package had 0%. The `api/` package (controllers) had 67% thanks to some integration tests from the previous year that someone had left half finished.

The distribution of the problem determines the distribution of the effort.

## 9.2 The Project's CLAUDE.md: The Anchor That Makes It Possible

Chapter 6 explained that CLAUDE.md is the operational equivalent of your agent's stable context: what you don't have to repeat in every prompt because the model already knows it. For a week of intense work, that file isn't a convenience; it is the difference between tests that fit your architecture and tests you have to throw away because they used the wrong dependencies.

This was the CLAUDE.md I created first thing Monday, before sending the first prompt:

**► TECHNICAL TRACK: CLAUDE.md for a Spring Boot / Angular Project**

```markdown
# PayTrack — Project context for Claude

## Tech stack
- **Backend:** Java 17, Spring Boot 3.2, JPA/Hibernate 6, PostgreSQL 15
- **Frontend:** Angular 17, TypeScript 5.2, Jest 29, Angular Testing Library
- **Backend tests:** JUnit 5, Mockito 5, Testcontainers 1.19
- **Coverage:** JaCoCo 0.8.11; merge threshold: 80%
- **Build:** Maven 3.9; `mvn test` for unit tests, `mvn verify` for integration

## Package structure (backend)
src/main/java/com/company/paytrack/
├── domain/        # Entities and value objects — NO Spring dependencies
├── application/   # Application services — pure business logic
├── infrastructure/# JPA repositories, Kafka clients, S3
└── api/           # REST controllers and DTOs — input validation

## Test conventions you MUST follow
- Class name: `ClassUnderTestTest.java` (unit), `*IT.java` (integration)
- One @Test per observable behavior, NOT per public method
- Mockito: only for dependencies external to the class under test
- Testcontainers: ONLY when the test verifies real DB behavior
- NEVER use Thread.sleep() — use CompletableFuture.get(timeout) or Awaitility
- AssertJ for assertions (already on the classpath), NOT JUnit Assertions directly
- Angular: do NOT use `any` in spec TypeScript; always type

## Forbidden antipatterns
- A test that never fails (no meaningful assertThat or verify)
- @Disabled without a ticket number in the comment: @Disabled("PAYTRACK-1234")
- Mocking the class under test (a test double of itself)
- Hardcoding localhost or ports in integration tests — use @DynamicPropertySource

## Key commands
mvn jacoco:report                           # generates target/site/jacoco/index.html
mvn test -Dtest=PaymentServiceTest          # runs a single backend test
ng test --include='**/payment*' --watch=false  # runs filtered Angular specs
```

With that file in the repository, every interaction with Claude Code automatically inherits the conventions. If you send a prompt without mentioning Mockito or AssertJ, the model uses them anyway because CLAUDE.md already established them as the project standard.

## 9.3 The Economic Strategy: The Right Model for Each Task

One of the costliest mistakes I can make in a week of intense work with AI is to use the most expensive model for everything. Opus reasons like a senior architect, but if I use it to generate the test for a getter, I'm paying $25/MTok for something Haiku solves just as well at $5/MTok. The difference isn't only in price: it is in speed and in where it makes sense to invest the model's cognitive attention.

The rule I apply: **the most expensive model at the start of each decision, the cheapest for executing what has already been decided.**

| Task | Model | Why | Approximate cost |
|---|---|---|---|
| Analyze architecture and generate the test plan | Sonnet | Understands relationships between layers | $3/$15 MTok |
| Decide Mockito vs Testcontainers in a complex case | Opus | Deep trade-off reasoning | $5/$25 MTok |
| Generate 200 service unit tests | Haiku | Predictable boilerplate, clear pattern | $1/$5 MTok |
| Debug why a generated test fails | Haiku | The error is already bounded | $1/$5 MTok |
| Refactor legacy code to make it testable | Sonnet | Requires understanding the domain | $3/$15 MTok |
| Mass generation of Angular/Jest specs | Haiku | Component structure is repetitive | $1/$5 MTok |

The entire week, with 180 tests generated, cost $4.07 on the API. The alternative would have been to use Sonnet for everything: the same week would have cost roughly $24, the equivalent of a month of Claude Pro. With the tiered strategy, I ended up within the budget of a single working day of cloud work.

**GitHub Copilot as an alternative.** If you already have access to Copilot ($10–19/month), it offers inline autocomplete that is useful for the simplest boilerplate. However, it doesn't have Opus's reasoning ability for architectural decisions, nor can it hold the context of a full project CLAUDE.md in every suggestion. The two approaches aren't mutually exclusive: Copilot as a typing copilot + Claude for the decisions that matter.

![Diagram 9.1: Weekly decision flow by model, from diagnosis to PR](imagenes/uml/c21_1_activity_sprint_en.png)

## 9.4 Monday and Tuesday: Mapping and Design with Sonnet

On Monday I didn't write a single test. I spent it understanding the problem and building the plan with Sonnet.

The prompt I sent was:

```
Attached are the JaCoCo report CSV and the project's package structure.
CLAUDE.md is in the repository. I need to get from 38% to 80%
coverage before Friday.

Generate an attack plan by layer:
1. Which classes to prioritize (highest coverage impact vs. effort)
2. What type of test corresponds to each layer (unit, integration, e2e)
3. Which dependencies I need to mock vs. the ones that are better tested
   with Testcontainers
4. Approximately how many tests I need per package to move the needle

Don't generate code yet. Just the plan.
```

Sonnet returned a structured plan built from four hours' worth of project context. The central point it identified, and that I had underestimated: the `application/` package had 12 service classes with an average of 8 public methods each, and nearly all the business branches (validations, currency conversions, payment states) were in that package. Reaching 80% depended almost entirely on covering that package.

The resulting plan:

| Package | Tests needed | Recommended model | Coverage impact |
|---|---|---|---|
| `domain/` | 40 tests | Haiku | +8% |
| `application/` | 95 tests | Haiku (with 3 Opus cases) | +28% |
| `infrastructure/` | 20 tests (Testcontainers) | Haiku | +8% |
| `api/` (extend the existing ones) | 15 tests | Haiku | +8% |
| Angular (`src/app/`) | 48 Jest specs | Haiku | independent JS coverage |

Sixteen percentage points were already mine on Tuesday before writing a line of code, because the plan was well founded.

## 9.5 Wednesday: The Hard Cases with Opus

Most of the week's 180 tests I generated with Haiku. But there were three services I couldn't hand to Haiku without first making an architectural decision:

- `PaymentService`: processes distributed transactions with double entry (debit + credit) under a JPA transaction that also publishes an event to Kafka.
- `ReconciliationService`: reads results from an external bank's API, reconciles them against the DB, and raises alarms.
- `InventoryService`: manages stock with optimistic locking and has three variants of a replenishment algorithm.

For these three, I used Opus with the following prompt:

**► TECHNICAL TRACK: Prompt for a Test Architecture Decision with Opus**

```
Context: PayTrack project (CLAUDE.md attached).

Class under analysis: PaymentService.java (attached).
Dependencies: PaymentRepository (JPA), EventPublisher (Kafka), CurrencyConverter.

The class has a distributed transaction: if the Kafka event fails
after JPA has committed, the state is left inconsistent.

Specific question: should I test PaymentService with:
  (a) Mockito for everything (fast, isolated),
  (b) Testcontainers with PostgreSQL + Kafka in a container (slow, realistic), or
  (c) A hybrid: Mockito for the happy path + Testcontainers only for
      the Kafka failure case?

Consider CI pipeline speed, confidence in the test, and
maintenance complexity. Justify with concrete trade-offs,
not generalities. At the end, give me the seed code for the
option you recommend.
```

Opus chose option (c) and justified it precisely: the happy path with Mockito is enough because the business logic (computing the debit/credit) doesn't depend on the infrastructure; the Kafka failure case, by contrast, requires Testcontainers because Spring's transactional behavior (rollback vs. the outbox pattern) only emerges with a real DB. Without Testcontainers for that specific case, the test would always pass, even if the system produced inconsistent states in production.

The seed code Opus returned:

**► TECHNICAL TRACK: Hybrid Mockito + Testcontainers Test for a Transactional Service**

```java
// PaymentServiceTest.java — Happy path with Mockito (Haiku can expand this)
@ExtendWith(MockitoExtension.class)
class PaymentServiceTest {

    @Mock PaymentRepository paymentRepository;
    @Mock EventPublisher eventPublisher;
    @Mock CurrencyConverter currencyConverter;

    @InjectMocks PaymentService paymentService;

    @Test
    void processPayment_withValidData_shouldSaveAndPublishEvent() {
        // Arrange
        var request = new PaymentRequest("ACC-001", "ACC-002",
                                         new BigDecimal("500.00"), "USD");
        var savedPayment = Payment.builder()
                .id(UUID.randomUUID()).status(PaymentStatus.PENDING).build();

        given(currencyConverter.convert(any(), eq("USD"), eq("PEN")))
                .willReturn(new BigDecimal("1875.00"));
        given(paymentRepository.save(any(Payment.class))).willReturn(savedPayment);

        // Act
        var result = paymentService.processPayment(request);

        // Assert
        assertThat(result.status()).isEqualTo(PaymentStatus.PENDING);
        then(eventPublisher).should().publish(any(PaymentCreatedEvent.class));
        then(paymentRepository).should().save(argThat(p ->
                p.getAmount().compareTo(new BigDecimal("1875.00")) == 0));
    }

    @Test
    void processPayment_withNegativeAmount_shouldThrowException() {
        var request = new PaymentRequest("ACC-001", "ACC-002",
                                         new BigDecimal("-10.00"), "USD");

        assertThatThrownBy(() -> paymentService.processPayment(request))
                .isInstanceOf(InvalidAmountException.class)
                .hasMessageContaining("negative amount");
    }
}

// PaymentServiceKafkaIT.java — Kafka failure case (Testcontainers)
@SpringBootTest
@Testcontainers
class PaymentServiceKafkaIT {

    @Container
    static PostgreSQLContainer<?> postgres =
            new PostgreSQLContainer<>("postgres:15-alpine");

    @Container
    static KafkaContainer kafka =
            new KafkaContainer(DockerImageName.parse("confluentinc/cp-kafka:7.4.0"));

    @DynamicPropertySource
    static void configureProperties(DynamicPropertyRegistry registry) {
        registry.add("spring.datasource.url", postgres::getJdbcUrl);
        registry.add("spring.datasource.username", postgres::getUsername);
        registry.add("spring.datasource.password", postgres::getPassword);
        registry.add("spring.kafka.bootstrap-servers", kafka::getBootstrapServers);
    }

    @Autowired PaymentService paymentService;
    @Autowired PaymentRepository paymentRepository;

    @Test
    void processPayment_whenKafkaFails_shouldRollBackJPA() {
        // This test verifies that if Kafka rejects the event,
        // the JPA transaction is rolled back and no orphan payment remains.

        // Disconnect Kafka to simulate a network failure
        kafka.stop();

        var request = new PaymentRequest("ACC-001", "ACC-002",
                                         new BigDecimal("100.00"), "USD");

        assertThatThrownBy(() -> paymentService.processPayment(request))
                .isInstanceOf(EventPublicationException.class);

        // Verify that the payment did not remain in the DB (successful rollback)
        assertThat(paymentRepository.findAll()).isEmpty();
    }
}
```

That seed code was the mold. Haiku extended it with twelve more variants on Wednesday afternoon, because the pattern was already established.

## 9.6 Thursday and Friday: Mass Execution with Haiku

With Sonnet's plan and Opus's molds, Thursday was pure volume. Haiku is fast, cheap, and, when it has a good CLAUDE.md and a reference example in the prompt, it produces tests that pass without modification in most cases.

The workflow I repeated for each service:

**► TECHNICAL TRACK: Mass Generation Prompt with Haiku**

```
[Project CLAUDE.md in the session context]

Class to test: InventoryService.java (attached)
Already-approved reference test: InventoryServiceTest_reference.java (attached)

Generate JUnit 5 tests for the following methods that have 0 coverage:
- adjustStock(String skuId, int quantity, AdjustmentType type)
- calculateReplenishment(String skuId) — has three branches (FIFO, LIFO, AVERAGE)
- transferBetweenWarehouses(String source, String destination, int quantity)

Follow the reference test's pattern:
- One @Test per behavior, named given_When_Then
- AssertJ for assertions
- Mockito for InventoryRepository and WarehouseRepository
- No business logic in the test: only arrange, act, and verify

Also generate the concurrency edge case for adjustStock
when two threads try to adjust the same SKU simultaneously
(use Awaitility, not Thread.sleep).
```

The result arrived in seconds: 12 tests for `InventoryService`, all with descriptive names, no circular dependencies, with the concurrency case included using `Awaitility` just as I asked.

For Angular the flow was equivalent, but in TypeScript with Jest:

**► TECHNICAL TRACK: Angular Component Test Generated by Haiku**

```typescript
// payment-form.component.spec.ts — generated by Haiku, reviewed by the engineer

import { ComponentFixture, TestBed } from '@angular/core/testing';
import { ReactiveFormsModule } from '@angular/forms';
import { HttpClientTestingModule } from '@angular/common/http/testing';
import { of, throwError } from 'rxjs';

import { PaymentFormComponent } from './payment-form.component';
import { PaymentService } from '../../services/payment.service';

describe('PaymentFormComponent', () => {
  let fixture: ComponentFixture<PaymentFormComponent>;
  let component: PaymentFormComponent;
  let paymentServiceSpy: jest.Mocked<PaymentService>;

  beforeEach(async () => {
    const spy = {
      processPayment: jest.fn(),
    } as unknown as jest.Mocked<PaymentService>;

    await TestBed.configureTestingModule({
      imports: [ReactiveFormsModule, HttpClientTestingModule],
      declarations: [PaymentFormComponent],
      providers: [{ provide: PaymentService, useValue: spy }],
    }).compileComponents();

    fixture = TestBed.createComponent(PaymentFormComponent);
    component = fixture.componentInstance;
    paymentServiceSpy = TestBed.inject(PaymentService) as jest.Mocked<PaymentService>;
    fixture.detectChanges();
  });

  it('should disable the submit button when the form is invalid', () => {
    // The form starts empty, therefore invalid
    const button = fixture.nativeElement.querySelector('button[type="submit"]');
    expect(button.disabled).toBe(true);
  });

  it('should show a validation error when the amount is negative', () => {
    component.form.patchValue({ amount: -50, sourceAccount: 'ACC-001',
                                destinationAccount: 'ACC-002' });
    fixture.detectChanges();

    const errorEl = fixture.nativeElement.querySelector('[data-testid="error-amount"]');
    expect(errorEl?.textContent).toContain('The amount must be greater than zero');
  });

  it('should call paymentService.processPayment with the form data on submit', () => {
    paymentServiceSpy.processPayment.mockReturnValue(of({ id: 'PAY-001',
                                                          status: 'PENDING' }));
    component.form.patchValue({ amount: 500, sourceAccount: 'ACC-001',
                                destinationAccount: 'ACC-002', currency: 'USD' });
    fixture.detectChanges();

    component.onSubmit();

    expect(paymentServiceSpy.processPayment).toHaveBeenCalledWith({
      amount: 500, sourceAccount: 'ACC-001',
      destinationAccount: 'ACC-002', currency: 'USD',
    });
  });

  it('should show the server error message when the payment fails', () => {
    paymentServiceSpy.processPayment.mockReturnValue(
      throwError(() => ({ error: { message: 'Insufficient funds' } }))
    );
    component.form.patchValue({ amount: 9999999, sourceAccount: 'ACC-001',
                                destinationAccount: 'ACC-002', currency: 'USD' });

    component.onSubmit();
    fixture.detectChanges();

    const globalError = fixture.nativeElement
        .querySelector('[data-testid="error-global"]');
    expect(globalError?.textContent).toContain('Insufficient funds');
  });
});
```

That file arrived ready. The only thing I adjusted was the name of the `data-testid` attribute so it matched the component's real HTML, something Haiku couldn't know without the template.

![Diagram 9.2: Toolkit architecture, VS Code, Alpaquitay AI, cloud models, and local LM Studio](imagenes/uml/c21_2_component_toolkit_en.png)

## 9.7 Alpaquitay AI: The Copilot Without an API Bill

Throughout the week, every prompt I sent to Claude I sent through **Alpaquitay AI**, the VS Code extension available on the Marketplace. The reason is simple: instead of switching between the IDE and the browser (or the CLI), the context of the file I had open was sent directly as part of the prompt. I selected the service class, opened the Alpaquitay panel, and typed the prompt; the extension attached the active file to the context automatically.

**Configuring the model from VS Code:**

Inside the Alpaquitay AI panel, the `/model` command switches the model on the fly:

```
/model haiku    # for mass generation (Thursday/Friday)
/model sonnet   # for analysis and the plan (Monday)
/model opus     # for architectural decisions (Wednesday)
```

**Connecting to LM Studio for work with no API cost:**

If you want to completely eliminate token spend for the simplest tasks (exploring code, generating basic boilerplate, quick queries), Alpaquitay AI supports the OpenAI-compatible endpoint that LM Studio exposes:

```jsonc
// .vscode/settings.json (or user settings)
{
  "alpaquitay.endpoint": "http://localhost:1234/v1",
  "alpaquitay.model": "lmstudio-community/Meta-Llama-3.1-8B-Instruct-GGUF",
  "alpaquitay.useLocalModel": true
}
```

With LM Studio running and Llama 3.1 loaded, Alpaquitay redirects all requests to the local server. The cost is zero API tokens; the trade-off is speed (an 8B model on CPU is considerably slower than Haiku in the cloud) and reduced reasoning ability. For generating the test of a simple-value getter, it is enough. For `PaymentService` with distributed transactions, it is not: there it pays to go back to the cloud with Opus.

The hybrid strategy I applied during the week: LM Studio for initial exploration and trivial boilerplate; the Claude API for the tests that really mattered.

**► TECHNICAL TRACK: Verify That Alpaquitay Connects to the Local Server**

```bash
# First, verify that LM Studio is serving
curl http://localhost:1234/v1/models | jq '.data[].id'

# If the output shows the loaded model, Alpaquitay can use it.
# From the Alpaquitay AI panel in VS Code, look for the connection
# indicator in the bottom status bar; it should show the name
# of the local model, not "claude-*".
```

## 9.8 Manan-Kanchu: The Guardian of Generated Code

Generating 180 tests with AI in four days raises a legitimate question: how do I know the generated code is safe and complies with the project's policies? A test that introduces a vulnerability is worse than no test.

That is what **Manan-Kanchu** is for, the code analysis VS Code extension that the author also publishes. After each batch of generated tests, before `git add`, I scan it.

**► TECHNICAL TRACK: Using Manan-Kanchu to Audit AI-Generated Code**

```bash
# From the Manan-Kanchu panel in VS Code:
# Right-click the src/test/java folder → "Analyze with Manan-Kanchu"
#
# Or from the terminal (the extension's CLI, if installed globally):
manankanchu scan ./backend/src/test/java --report=json > scan_report.json

# Typical output the engineer checks:
# {
#   "summary": {
#     "total_files": 47,
#     "ai_detected": 42,       <- expected: we just generated with AI
#     "vulnerabilities": 0,
#     "policy_violations": 2,  <- these need attention
#     "malware_patterns": 0
#   },
#   "policy_violations": [
#     {
#       "file": "PaymentServiceTest.java",
#       "line": 34,
#       "rule": "NO_HARDCODED_SECRETS",
#       "detail": "Possible credential: 'postgres:password123' in literal"
#     },
#     {
#       "file": "ReconciliationServiceTest.java",
#       "line": 89,
#       "rule": "NO_EXTERNAL_URL",
#       "detail": "Hardcoded URL detected: 'http://api.bank.com'"
#     }
#   ]
# }
```

The two policy violations were exactly what I expected: Haiku had hardcoded Testcontainers credentials and a URL for an external service that should go in environment variables or in `@DynamicPropertySource`. I fixed them in three minutes. Without the scan, those credentials would have entered the repository.

The `ai_detected: 42` indicator is not an alarm: the code is the author's even if a tool generated it. What matters is that the engineer reviewed it, understands it, and signs off on it. Manan-Kanchu doesn't tell you "don't use AI"; it tells you "here is something to review before it reaches production."

![Diagram 9.3: Model selection sequence, from Monday's analysis to Friday's PR](imagenes/uml/c21_3_sequence_model_en.png)

## 9.9 The Five Antipatterns That Almost Cost Me the Week

This week wasn't linear. I made mistakes; some cost me hours. I record them precisely so you don't repeat them.

**Antipattern 1: Sending to Haiku without CLAUDE.md and without a reference example.**

On Wednesday afternoon, in a hurry, I sent a generation prompt to Haiku without attaching CLAUDE.md and without indicating the reference test. Haiku generated tests with JUnit 4 (`@RunWith`, `@Before`) instead of JUnit 5 (`@ExtendWith`, `@BeforeEach`), and used JUnit's `assertEquals` instead of AssertJ. I had to discard 15 tests and redo them with the right context. Cost: two hours.

**Antipattern 2: Using Opus for all the volume.**

On Tuesday, optimistic about the quality of Opus's outputs, I used it for the first twenty domain tests. The tests were perfect, but then the day's bill arrived: $8.40 from Tuesday alone. I switched to Haiku on Wednesday and the rest of the week cost $3.67 in total. Opus for the decisions, Haiku for the execution.

**Antipattern 3: Not reviewing the generated tests before running them.**

Four of Haiku's tests compiled but didn't test what their name said. For example, `shouldCalculateVolumeDiscount` had no assertion about the discount; it only verified that the method didn't throw an exception. A test without a meaningful assertion is worse than no test: it adds to coverage, gives false security, and hides bugs. I reviewed all the tests by eye before running them.

**Antipattern 4: Generating the integration tests with Haiku before having resolved the design.**

I tried asking Haiku directly for the `PaymentService` tests without going through Opus first. Haiku generated reasonable tests but chose Mockito for the Kafka failure case: a test that always passed because it mocked exactly the layer that needed to fail. It was the right decision for the happy path, not for the transactional failure case. Order matters: Opus decides, Haiku executes.

**Antipattern 5: Not running Manan-Kanchu before the first commit.**

On the first day I skipped it out of confidence. On the second day, the scan found the two policy violations I detailed earlier. If that code had reached the Git history, cleaning it up would have required a `git rebase` with history rewriting. A simple practice prevents a security incident.

## 9.10 Friday Afternoon: Final Metrics

At 4:30 p.m. on Friday I ran `mvn clean verify` for the last time:

```
[INFO] Tests run: 247, Failures: 0, Errors: 0, Skipped: 0
[INFO] Overall coverage: 82.3%
[INFO]   com.company.paytrack.domain:         91.2%
[INFO]   com.company.paytrack.application:    84.7%
[INFO]   com.company.paytrack.infrastructure: 78.9%
[INFO]   com.company.paytrack.api:            76.1%
[INFO] BUILD SUCCESS
```

Angular:

```
Test Suites: 12 passed, 12 total
Tests:       61 passed, 61 total
Coverage:    86.4% statements, 79.1% branches
```

Issues: 23 → 0. The validation issues nobody could close turned out to be real bugs that the new tests detected; once detected, the fix was mechanical with Haiku because the failing test already pointed exactly at what was broken.

**Breakdown of the week's real cost:**

| Model | Input tokens | Output tokens | Cost |
|---|---|---|---|
| Sonnet 4.6 (Monday–Tuesday, design) | ~18 K | ~12 K | $0.24 |
| Opus 4.8 (Wednesday, 3 complex services) | ~22 K | ~9 K | $0.34 |
| Haiku 4.5 (Thursday–Friday, mass generation) | ~380 K | ~590 K | $3.33 |
| Haiku 4.5 (fixes and debugging) | ~30 K | ~20 K | $0.13 |
| **Total** | — | — | **$4.04** |

Four dollars for the week. The Sonnet-for-everything alternative would have cost roughly $26. The Opus-for-everything alternative, roughly $140.

Efficiency isn't a luxury when the budget is limited; it is the requirement for the tool to be sustainable in the long run.

**■ EXECUTIVE TRACK**

The coverage week is not an experiment: it is a business case. From the executive perspective, what happened is that one engineer, without hiring anyone else, covered the equivalent of four weeks of test work in five days, at an API cost lower than a cup of coffee. The real cost of the week was human review time, not tokens: each generated test required between 30 seconds and 3 minutes of review. That doesn't disappear with more AI; it is the quality guarantee. If you eliminate the review, you don't have tests: you have false metrics.

What does change with AI is the proportion: before, the bottleneck was writing; now, it is reviewing. And reviewing is a skill that scales better than typing, because a senior engineer can review four tests per minute, but can hardly write more than one.

## Key Takeaways from Chapter 9

- CLAUDE.md is not optional for intensive work: it is the prefix that turns generic prompts into code that fits your architecture without rework.
- The model tier strategy (Sonnet for design, Opus for complex decisions, Haiku for mass execution) cut the week's cost from ~$26 to $4.04 while maintaining the same output quality.
- The right order is: diagnosis → plan (Sonnet) → architecture decisions (Opus) → mass generation (Haiku) → audit (Manan-Kanchu). Skipping any step in the sequence comes back with interest.
- Alpaquitay AI as a bridge between VS Code and the models (cloud or local with LM Studio) eliminates the friction of context: the active file is always part of the prompt.
- Manan-Kanchu is the quality gate before the commit: it detects hardcoded credentials, external URLs, and vulnerabilities that models introduce into their boilerplate without intent but with consequences.
- The bottleneck shifted from writing to reviewing. Human review doesn't disappear; it concentrates.

---

## Worked Exercise 9.1: Replicate the Coverage Week in Two Hours

Take a project of your own (Spring Boot or any Java/Python backend) and apply this week's flow in miniature: a two-hour session.

1. Generate the current coverage report (`mvn jacoco:report` or your stack's equivalent).
2. Create a `CLAUDE.md` with: stack, test conventions, build commands, two forbidden antipatterns.
3. Send the report to Sonnet with the Section 9.4 prompt and ask for the attack plan.
4. Pick the service with the highest coverage impact according to the plan and send it to Haiku with the Section 9.6 prompt.
5. Run the generated test. If it fails, ask Haiku to fix the error by attaching the stack trace.
6. Record: how many tokens did you consume? How much did it move the coverage needle? How many minutes of review did each test need?

The record will give you your own calibration of speed and cost, which is more valuable than any table in this chapter.
