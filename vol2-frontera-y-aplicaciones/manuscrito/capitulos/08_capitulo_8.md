# Capítulo 8: La herramienta de agentes y multiagentes de Google para aprender idiomas, su arquitectura por dentro

> *Aprender un idioma con IA no es traducir más rápido; es conversar con un tutor que nunca se cansa ni se impacienta.*

## De la traducción al tutor conversacional: un cambio de naturaleza

Las herramientas de Google Labs para el aprendizaje de idiomas (entre las que destacan iniciativas como Speak con Gemini e integraciones de Google Translate con tutorías conversacionales) plantean una discontinuidad de diseño que exige análisis arquitectónico. La traducción automática clásica resolvía un problema puntual: convertir texto de una lengua A a una lengua B con la mayor fidelidad posible. Un tutor de idiomas basado en agentes resuelve algo estructuralmente diferente: **sostener una conversación pedagógica adaptada al nivel del aprendiz, en tiempo real, con memoria del historial de aprendizaje y ajuste dinámico de dificultad**.

La diferencia es de naturaleza, no de grado. Donde la traducción es una función pura (dado un texto, produce un texto), el tutor es un sistema con estado, memoria, objetivos pedagógicos y mecanismos de adaptación. Vygotsky (1978), cuya teoría de la Zona de Desarrollo Próximo (*ZPD*) sigue siendo el marco pedagógico más influyente en la enseñanza de lenguas, establece que el aprendizaje óptimo ocurre en el espacio entre lo que el aprendiz puede hacer de manera autónoma y lo que puede hacer con la asistencia de un guía competente. Un tutor agéntico, si está bien diseñado, opera precisamente en esa zona: siempre exigiendo un poco más de lo que el aprendiz puede hacer solo, nunca tanto que lo desmotive.

## La arquitectura, hasta donde se deja ver: cuatro agentes especializados

Aunque los detalles internos de las implementaciones de Google son propietarios, los principios arquitectónicos de un tutor agéntico de idiomas son inferibles a partir de los principios de diseño de agentes ([Anthropic, 2024](#ref-anthropic2024)) y de la literatura de sistemas tutoriales inteligentes (*Intelligent Tutoring Systems*, ITS):

**Agente conversacional.** Mantiene el diálogo natural, selecciona vocabulario y estructuras gramaticales acordes con el nivel detectado del aprendiz, y produce respuestas que son lingüísticamente accesibles pero no condescendientes. Su métrica de éxito es la continuidad y la fluidez de la conversación, no la corrección de la gramática.

**Agente evaluador.** Corre en paralelo al agente conversacional, analizando las producciones del aprendiz en busca de errores (de vocabulario, gramática, pronunciación cuando hay audio, o uso contextual). Toma la decisión pedagógica de cuándo corregir y cuándo dejar pasar: corregir cada error interrumpe el flujo y desmotiva; no corregir nunca permite que los errores se fosilizan (*fossilization*, Selinker, 1972). Esta tensión, central en la pedagogía de idiomas desde hace décadas, se resuelve mediante la separación de responsabilidades entre el agente que conversa y el que evalúa.

**Agente de currículo.** Rastrea el progreso del aprendiz a lo largo del tiempo y decide qué introducir a continuación: qué estructuras gramaticales, qué campos semánticos, qué registros de lengua. Opera en el horizonte del aprendizaje, no en el de la conversación individual. Su decisión es de semanas, no de segundos.

**Memoria del aprendiz.** Persiste qué vocabulario ha sido enseñado y cuántas veces se ha activado correctamente, qué errores recurren, qué temas motivan a este usuario concreto, y qué nivel de confianza tiene en cada subdominio de la lengua. Esta memoria es lo que hace que el tutor sea *este* tutor del aprendiz, no un tutor genérico que cada día empieza desde cero.

## El principio pedagógico hecho arquitectura: SOLID aplicado a la enseñanza

Lo más notable de esta arquitectura, desde la óptica de este libro, es cómo un principio pedagógico centenario (la tensión entre fluidez y corrección en la enseñanza de idiomas) se materializa en una decisión de diseño de software: la **separación de responsabilidades** entre el agente conversacional y el agente evaluador.

Si un solo agente realizara ambas funciones, la corrección contaminaría la fluidez: el aprendiz sentiría que cada error es inmediatamente señalado, lo que produce ansiedad lingüística (*language anxiety*, Horwitz et al., 1986), uno de los predictores más robustos de dificultad en el aprendizaje de lenguas. Al separar conversación y evaluación en agentes distintos, el sistema puede ser cálido y fluido en el diálogo mientras es riguroso y sistemático en el análisis. Es el principio de Responsabilidad Única (SOLID) aplicado no al software sino a la pedagogía: una responsabilidad, un agente.

Esta transferencia del principio de diseño de software al diseño pedagógico tiene implicaciones que trascienden los idiomas: cualquier dominio donde sea necesario **equilibrar acompañamiento y exigencia** puede beneficiarse del mismo patrón.

## La lección transferible: el patrón Soporte-Evaluación

El patrón arquitectónico que subyace al tutor de Google (separar el agente que sostiene la relación del agente que evalúa el desempeño) es transferible a cualquier dominio que enfrente la misma tensión:

- **Salud**: el agente de acompañamiento emocional y el agente de evaluación de adherencia al tratamiento son roles distintos que no deben mezclarse.
- **Coaching ejecutivo**: el agente que facilita la reflexión y el agente que mide el progreso hacia los KPIs operan con lógicas distintas.
- **Atención al cliente**: el agente que gestiona la relación afectiva con el cliente y el agente que monitorea el cumplimiento de SLAs sirven a propósitos que, mezclados, se degradas mutuamente.

En cada uno de estos casos, la arquitectura de la herramienta de Google proporciona un modelo: no una aplicación directa, sino un patrón de separación que puede adaptarse al dominio específico.

---

## Perspectiva técnica avanzada

**► PISTA TÉCNICA**


### Implementación del patrón Soporte-Evaluación en TypeScript

Desde la perspectiva del **Arquitecto Senior**, el patrón se implementa como una orquestación de dos agentes con responsabilidades claramente delimitadas y un protocolo de comunicación explícito:

```typescript
// Tipos de dominio para el tutor de idiomas agéntico
interface LearnerProfile {
  userId:            string;
  targetLanguage:    string;
  nativeLanguage:    string;
  cefrLevel:         "A1" | "A2" | "B1" | "B2" | "C1" | "C2";
  sessionHistory:    ConversationTurn[];
  errorPatterns:     Record<string, number>;  // error → frecuencia
  motivationTopics:  string[];
}

interface ConversationTurn {
  role:      "user" | "tutor";
  content:   string;
  timestamp: Date;
}

interface EvaluationResult {
  errors:         LanguageError[];
  shouldCorrect:  boolean;          // decisión pedagógica del evaluador
  correctionType: "immediate" | "delayed" | "none";
  suggestedFeedback: string | null;
}

interface LanguageError {
  type:     "grammar" | "vocabulary" | "pragmatics" | "pronunciation";
  excerpt:  string;
  severity: "minor" | "moderate" | "critical";
}

// ─────────────────────────────────────────────────
// Agente Conversacional: sostiene el diálogo
// ─────────────────────────────────────────────────
class ConversationalAgent {
  constructor(
    private readonly llmFn: (prompt: string) => Promise<string>,
    private readonly profile: LearnerProfile,
  ) {}

  async respond(
    learnerInput: string,
    evaluationResult: EvaluationResult,
  ): Promise<string> {
    const corrections = evaluationResult.shouldCorrect
      ? `\nCorrection context (weave naturally, do not interrupt flow): ${evaluationResult.suggestedFeedback}`
      : "";

    const prompt = `
You are a warm, patient language tutor for a ${this.profile.cefrLevel} ${this.profile.targetLanguage} learner.
Their native language is ${this.profile.nativeLanguage}.
Conversation so far: ${JSON.stringify(this.profile.sessionHistory.slice(-6))}
Learner's latest message: "${learnerInput}"
${corrections}
Respond naturally. Keep the conversation flowing. Level vocabulary to ${this.profile.cefrLevel}.
    `.trim();

    return this.llmFn(prompt);
  }
}

// ─────────────────────────────────────────────────
// Agente Evaluador: analiza sin interrumpir el flujo
// ─────────────────────────────────────────────────
class EvaluatorAgent {
  constructor(
    private readonly llmFn: (prompt: string) => Promise<string>,
  ) {}

  async evaluate(learnerInput: string, profile: LearnerProfile): Promise<EvaluationResult> {
    const prompt = `
Analyze the following ${profile.targetLanguage} learner output (CEFR level: ${profile.cefrLevel}).
Output: "${learnerInput}"
Known recurring errors: ${JSON.stringify(profile.errorPatterns)}
Return JSON: {
  "errors": [{"type": "grammar|vocabulary|pragmatics", "excerpt": "...", "severity": "minor|moderate|critical"}],
  "shouldCorrect": true|false,
  "correctionType": "immediate|delayed|none",
  "suggestedFeedback": "..."
}
Correction policy: correct CRITICAL errors always; MODERATE errors only if recurring (>3 times); MINOR errors never during flow.
    `.trim();

    const raw = await this.llmFn(prompt);
    return JSON.parse(raw) as EvaluationResult;
  }
}

// ─────────────────────────────────────────────────
// Orquestador: coordina ambos agentes
// ─────────────────────────────────────────────────
class LanguageTutorOrchestrator {
  private conversational: ConversationalAgent;
  private evaluator:      EvaluatorAgent;

  constructor(
    llmFn: (p: string) => Promise<string>,
    private profile: LearnerProfile,
  ) {
    this.conversational = new ConversationalAgent(llmFn, profile);
    this.evaluator      = new EvaluatorAgent(llmFn);
  }

  async processInput(learnerInput: string): Promise<{
    tutorResponse:    string;
    evaluationResult: EvaluationResult;
  }> {
    // Evaluador y conversacional pueden correr en paralelo hasta cierto punto
    const evaluationResult = await this.evaluator.evaluate(learnerInput, this.profile);
    const tutorResponse    = await this.conversational.respond(learnerInput, evaluationResult);

    // Actualizar historial y patrones de error
    this.profile.sessionHistory.push(
      { role: "user",  content: learnerInput,  timestamp: new Date() },
      { role: "tutor", content: tutorResponse, timestamp: new Date() },
    );
    for (const err of evaluationResult.errors) {
      this.profile.errorPatterns[err.type] = (this.profile.errorPatterns[err.type] ?? 0) + 1;
    }

    return { tutorResponse, evaluationResult };
  }
}
```

### Agente de currículo: la Zona de Desarrollo Próximo como algoritmo

El **Ingeniero Senior** implementa el agente de currículo como un sistema de recomendación que mantiene al aprendiz en la ZPD de Vygotsky:

```typescript
class CurriculumAgent {
  /** Selecciona el próximo concepto a introducir según la ZPD del aprendiz. */
  selectNextConcept(profile: LearnerProfile): string {
    // Concepto en la ZPD: dominado al 60-80% (no demasiado fácil, no demasiado difícil)
    const mastered     = this.getMasteredConcepts(profile);    // >80% accuracy
    const inProgress   = this.getInProgressConcepts(profile);  // 60-80%
    const notStarted   = this.getNotStartedConcepts(profile);  // <60%

    // Prioriza: reforzar en-progreso antes de introducir nuevo
    if (inProgress.length > 0) return inProgress[0];
    if (notStarted.length  > 0) return notStarted[0];
    return "advanced_review";
  }

  private getMasteredConcepts(profile: LearnerProfile): string[] {
    // Implementación real consultaría la memoria persistente del aprendiz
    return [];
  }
  private getInProgressConcepts(profile: LearnerProfile): string[] { return []; }
  private getNotStartedConcepts(profile: LearnerProfile): string[] { return []; }
}
```

### Estrategia de QA: testing del patrón Soporte-Evaluación

El **QA Senior** verifica que los dos agentes no se mezclen inadecuadamente, que el conversacional no tome decisiones de evaluación y el evaluador no contamine el flujo conversacional:

```typescript
describe("Separation of Concerns: Conversational vs Evaluator", () => {
  it("evaluator does not modify the conversational response directly", async () => {
    const eval_result: EvaluationResult = {
      errors: [{ type: "grammar", excerpt: "I goed", severity: "critical" }],
      shouldCorrect: true,
      correctionType: "immediate",
      suggestedFeedback: "Try 'I went' — irregular verb.",
    };
    const response = await conversationalAgent.respond("I goed to the market", eval_result);
    // La corrección debe estar integrada fluidamente, no como interrupción brusca
    expect(response).not.toContain("ERROR:");
    expect(response).not.toContain("WRONG:");
    expect(response.toLowerCase()).toContain("went");  // corrección integrada
  });

  it("evaluator runs independently of conversational flow", async () => {
    const [evalResult] = await Promise.allSettled([
      evaluatorAgent.evaluate("I goed", mockProfile),
    ]);
    expect(evalResult.status).toBe("fulfilled");
    if (evalResult.status === "fulfilled") {
      expect(evalResult.value.errors.length).toBeGreaterThan(0);
    }
  });
});
```

---

## Perspectiva ejecutiva

**■ PISTA EJECUTIVA**


### Visión del Product Owner: el tutor de idiomas como caso de estudio de diseño centrado en el usuario

El **Product Owner** de cualquier producto con componente conversacional puede extraer del caso Google Idiomas una lección de producto que trasciende el aprendizaje de lenguas: la tensión entre **engagement** (el usuario vuelve) y **outcome** (el usuario mejora) es el núcleo del diseño de producto en educación. Un producto que maximiza el engagement sin producir outcomes es un juego; uno que produce outcomes sin engagement es un examen. El tutor agéntico bien diseñado maximiza ambos simultáneamente, precisamente porque la arquitectura de agentes separados le permite ser cálido y exigente a la vez.

**Métricas de producto para el tutor agéntico**:

| Métrica                              | Objetivo         | Señal de alerta           |
|--------------------------------------|------------------|---------------------------|
| Sesión media (minutos)               | > 12 min         | < 5 min (baja engagement) |
| Tasa de retorno semanal              | > 65%            | < 40%                     |
| Progreso CEFR por trimestre          | +0.5 nivel       | 0 niveles (no hay outcome)|
| Error recurrence rate                | Décline > 20%    | Sin cambio (no corrige)   |
| Anxiety score (encuesta mensual)     | < 3/10           | > 6/10 (evaluador invasivo)|

### Visión del Scrum Master: la arquitectura de separación como modelo de equipo

El **Scrum Master** puede usar el patrón Soporte-Evaluación del tutor de Google como metáfora pedagógica para el propio equipo: el Scrum Master actúa como el agente conversacional (sostiene la dinámica del equipo, crea el espacio psicológico seguro para que el equipo trabaje), mientras que las métricas de velocidad, calidad y deuda técnica actúan como el agente evaluador, proporcionan datos objetivos sin contaminar el clima del equipo.

La confusión entre ambos roles (cuando el Scrum Master usa las métricas para señalar fallos en lugar de para generar conversación de mejora) reproduce exactamente el antipatrón del agente conversacional que también evalúa: interrumpe el flujo, genera ansiedad y degrada la colaboración.

---

## Versión académica alternativa (mayor densidad formal)

> La separación entre el componente conversacional y el componente evaluativo en los sistemas de tutoría inteligente (ITS) ha sido estudiada extensamente en la literatura de educación asistida por computadora. VanLehn (2011), en su revisión meta-analítica de los sistemas ITS, identifica que los tutores que proveen retroalimentación correctiva de forma integrada en el flujo de la conversación (en lugar de interrumpirlo) producen mejoras de aprendizaje estadísticamente superiores (d = 0.76 frente a d = 0.40 para sistemas de retroalimentación interrumpiva). Este resultado sugiere que la separación arquitectónica propuesta es, más que una decisión de ingeniería de software, una consecuencia de la evidencia pedagógica: la retroalimentación integrada requiere que el sistema tenga la capacidad de generar una respuesta conversacional fluida *mientras* mantiene el tracking evaluativo en un componente distinto. La implementación naive (un único agente que conversa y evalúa simultáneamente) no puede producir retroalimentación integrada de calidad porque sus dos objetivos optimizan métricas incompatibles en el mismo espacio de generación de texto.

---

## Lo esencial del capítulo 8

- Un tutor de idiomas agéntico no traduce: sostiene una conversación pedagógica adaptada, con memoria persistente del aprendiz y operación en la Zona de Desarrollo Próximo de Vygotsky.
- La arquitectura separa cuatro agentes: conversacional, evaluador, de currículo y memoria del aprendiz, cada uno con una única responsabilidad.
- La separación entre conversacional y evaluador resuelve la tensión pedagógica entre fluidez y corrección: SOLID aplicado a la pedagogía, con base empírica en la investigación ITS.
- El patrón Soporte-Evaluación se transfiere a cualquier dominio que equilibre acompañamiento y exigencia: salud, coaching, atención al cliente.
- El P.O. diseña el producto midiendo tanto engagement (el usuario vuelve) como outcome (el usuario mejora), el tutor agéntico bien diseñado optimiza ambos simultáneamente.
- El Scrum Master usa el patrón como metáfora de equipo: él sostiene la dinámica; las métricas evalúan, sin mezclar ambos roles.
