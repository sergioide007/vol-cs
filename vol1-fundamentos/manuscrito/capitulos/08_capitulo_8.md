# Capítulo 8: Patrones de orquestación multi-agente

## La arquitectura de la inteligencia distribuida

El sistema multi-agente es la culminación de todo lo anterior: múltiples agentes especializados, coordinados por un orquestador, producen resultados que ninguno podría producir individualmente. Wooldridge (2009) identifica las propiedades emergentes de los sistemas multi-agente: comportamientos que surgen de la interacción y que no estaban programados explícitamente en ningún agente individual. En ingeniería de software, las propiedades emergentes que buscamos son calidad, resiliencia y cobertura de perspectivas; las que debemos evitar son los bucles de acuerdo mutuo, la amplificación de errores y el costo descontrolado.

Antes de los patrones, la advertencia que la evidencia obliga a dar: **más agentes no es automáticamente mejor**. La evaluación rigurosa de agentes muestra que gran parte de las ganancias reportadas en benchmarks provienen de comparaciones sin control de costo, y que sistemas simples con presupuesto equivalente igualan a menudo a arquitecturas complejas [Kapoor et al., 2024](#ref-kapoor2024). La misma cautela aparece en la guía de ingeniería de Anthropic (2024): el éxito en producción no consiste en construir el sistema más sofisticado, sino el *adecuado*. Cada patrón siguiente se presenta, por eso, con su perfil de costo y su criterio de uso, y el capítulo 3 (Vol. 4) da las herramientas para verificar, con evals propios, que la complejidad adicional paga su precio.

## Los cinco patrones canónicos de orquestación

> **Justificación de diseño: Diagrama de componentes para la arquitectura del sistema**
>
> Una topología multi-agente es ante todo *cómo interactúan los módulos especializados*: quién habla con quién, cómo se conectan, dónde está el flujo. Un diagrama de componentes (con sus puertos y dependencias) muestra exactamente eso: la topología arquitectónica del sistema.
>
> Un diagrama de clases mostraría la estructura interna de un agente; un diagrama de estados mostraría cómo uno cambia en el tiempo. Aquí necesitamos ver *la conexión entre múltiples agentes*, el patrón de integración que gobernará toda su coordinación.
>
> En este libro reaparece el diagrama de componentes en el **Capítulo 9** (el ecosistema MCP), donde nuevamente el patrón de módulos especializados es lo que interesa.

![Diagrama 8.1.1: Patrón 1: Pipeline (diagrama de componentes)](imagenes/capitulo08/diagrama8_1_1_es.png)

**Pipeline (cadena).** Uso ideal: flujos predecibles con dependencias lineales. Ventaja: simple, auditable, fácil de depurar; cada eslabón puede validarse antes de pasar al siguiente. Desventaja: lento (secuencial) y un fallo detiene todo. Ejemplo: especificación → implementación → revisión → documentación. Es el patrón con mejor relación calidad/complejidad y debe ser la opción por defecto.

![Diagrama 8.1.2: Patrón 2: Fan-out paralelo](imagenes/capitulo08/diagrama8_1_2_es.png)

**Fan-out paralelo (seccionado).** Uso ideal: tareas independientes que pueden ejecutarse simultáneamente. Ventaja: reduce el tiempo total de forma proporcional al paralelismo disponible. Desventaja: exige una fase de fusión (*merge*) que es, ella misma, una tarea de razonamiento; los resultados parciales pueden ser inconsistentes entre sí. Ejemplo: generar frontend, backend y tests en paralelo a partir de un contrato de API común, el contrato previo es lo que hace al patrón viable.

![Diagrama 8.1.3: Patrón 3: Debate y consenso (council)](imagenes/capitulo08/diagrama8_1_3_es.png)

**Debate y consenso (council).** Uso ideal: decisiones de alto impacto y evaluación de artefactos críticos. Varios agentes con perspectivas distintas opinan; un sintetizador decide. Su fundamento empírico es directo: el debate entre múltiples instancias mejora la factualidad y el razonamiento respecto al agente único [Du et al., 2023](#ref-du2023). Desventaja: multiplica el costo por el número de consejeros; reservarlo para decisiones cuyo costo de error supere con holgura el costo del debate.

![Diagrama 8.1.4: Patrón 4: Jerárquico (Empresa Sintética)](imagenes/capitulo08/diagrama8_1_4_es.png)

**Jerárquico (orquestador-trabajadores).** Uso ideal: proyectos complejos con múltiples dominios. Un orquestador descompone, delega a especialistas y sintetiza. Ventaja: escala naturalmente y refleja la organización real [Conway, 1968](#ref-conway1968). Desventaja: la coordinación añade latencia y tokens; el orquestador es un punto único de fallo de razonamiento. Es el patrón de ChatDev y MetaGPT ([Qian et al., 2024](#ref-qian2024); [Hong et al., 2024](#ref-hong2024)).

![Diagrama 8.1.5: Patrón 5: Self-reflection loop](imagenes/capitulo08/diagrama8_1_5_es.png)

**Self-reflection loop (evaluador-optimizador).** Uso ideal: cuando la calidad es crítica y **verificable automáticamente**: tests que pasan, esquemas que validan, criterios formales. Un generador produce; un evaluador critica; el generador corrige. Fundamento: Self-Refine [Madaan et al., 2023](#ref-madaan2023) y Reflexion [Shinn et al., 2023](#ref-shinn2023). Desventaja: sin criterio de parada degenera en bucle infinito; sin señal de calidad objetiva degenera en autocomplacencia: el modelo aprueba su propia salida. Regla práctica: máximo de iteraciones explícito y evaluador distinto del generador.

**► PISTA TÉCNICA: Implementación del patrón council**

```python
# Ejemplo 8.1: Council pattern para revisión arquitectónica.
# Tres consejeros especializados opinan en paralelo; un sintetizador decide.
# Fundamento: el debate multi-agente mejora la factualidad [Du et al., 2023](#ref-du2023).

import anthropic

client = anthropic.Anthropic()

COUNSELORS = {
    "scalability": """Eres un arquitecto especializado en escalabilidad y
    sistemas distribuidos. Evalúas desde: carga, latencia, disponibilidad
    y operabilidad a escala. Sé conciso: máximo 300 palabras.
    Argumenta con datos y mecanismos, no con opiniones.""",
    "developer_experience": """Eres un arquitecto especializado en developer
    experience y simplicidad operacional. Evalúas desde: velocidad de onboarding,
    facilidad de depuración, costo de mantenimiento y deuda técnica.
    Defiendes la tecnología aburrida y el principio YAGNI. Máximo 300 palabras.""",
    "economics": """Eres un arquitecto especializado en economía de sistemas.
    Evalúas TCO (costo total de propiedad), costos operacionales, impacto en
    velocidad de entrega y ROI de decisiones técnicas. Piensas en términos
    de Boehm (economía del software) y métricas DORA. Máximo 300 palabras.""",
}

def consult(role_system: str, problema: str) -> dict:
    resp = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        system=role_system,
        messages=[{"role": "user",
                   "content": f"Evalúa desde tu especialidad: {problema}"}],
    )
    return {
        "text": next(b.text for b in resp.content if b.type == "text"),
        "tokens": resp.usage.input_tokens + resp.usage.output_tokens,
    }

def architecture_council(problema_arquitectonico: str) -> dict:
    """
    Patrón Council: 3 perspectivas especializadas debaten una decisión
    de arquitectura; el modelo más capaz sintetiza el veredicto final.
    En producción, las tres consultas se lanzan en paralelo.
    """
    views = {name: consult(system, problema_arquitectonico)
             for name, system in COUNSELORS.items()}

    synthesis = client.messages.create(
        model="claude-opus-4-8",   # el modelo más capaz para la síntesis
        max_tokens=2048,
        system="""Eres el arquitecto jefe que debe tomar una DECISIÓN FINAL
        basada en los argumentos de tres consejeros especializados. Tu output:

        1. DECISIÓN: [una línea clara y sin ambigüedad]
        2. RAZÓN PRINCIPAL: [el argumento que inclina la balanza]
        3. CONDICIONES: [3 condiciones que harían cambiar esta decisión]
        4. PRIMER PASO: [la acción concreta a tomar esta semana]
        5. RIESGO PRINCIPAL: [lo que puede salir mal y cómo mitigarlo]

        No resumas los argumentos. Ve directo a la decisión.""",
        messages=[{
            "role": "user",
            "content": (
                f"Problema: {problema_arquitectonico}\n\n"
                f"ESCALABILIDAD:\n{views['scalability']['text']}\n\n"
                f"DEVELOPER EXPERIENCE:\n{views['developer_experience']['text']}\n\n"
                f"ECONOMÍA:\n{views['economics']['text']}\n\nToma tu decisión."
            ),
        }],
    )

    total_tokens = (sum(v["tokens"] for v in views.values())
                    + synthesis.usage.input_tokens
                    + synthesis.usage.output_tokens)

    return {
        "decision": next(b.text for b in synthesis.content if b.type == "text"),
        "perspectives": {k: v["text"] for k, v in views.items()},
        "meta": {
            "total_tokens": total_tokens,
            "agentes_consultados": len(COUNSELORS) + 1,
            "patron": "Council (debate + síntesis)",
        },
    }


# Ejemplo de uso:
# resultado = architecture_council(
#     "Tenemos un monolito Django de 5 años con 50K usuarios activos. "
#     "El equipo propone migrarlo a microservicios para 'escalar mejor'. "
#     "¿Es la decisión correcta ahora?"
# )
# print(resultado["decision"])
# Output esperado: una recomendación clara, no un "depende".
```

### Cómo elegir patrón: el árbol de decisión

1. ¿La tarea cabe en una sola llamada bien diseñada? → **No orqueste.** (La opción que los entusiastas olvidan.)
2. ¿Los pasos son conocidos de antemano? → **Pipeline.**
3. ¿Las subtareas son independientes entre sí? → **Fan-out** con contrato previo.
4. ¿La salida es verificable automáticamente? → **Self-reflection loop** con presupuesto.
5. ¿La decisión es cara de revertir y admite perspectivas? → **Council.**
6. ¿El problema exige descomposición dinámica de varios dominios? → **Jerárquico**. Y prepare la observabilidad del capítulo 1 (Vol. 4), porque la necesitará.

**■ PISTA EJECUTIVA**

La lección directiva de este capítulo cabe en una frase: **la arquitectura multi-agente es una decisión de inversión, no de moda**. Cada patrón compra una propiedad (velocidad, robustez, cobertura de perspectivas) a un precio medible en tokens y en complejidad operativa. Exija a su equipo lo que exigiría ante cualquier inversión: la comparación contra la alternativa simple, con costo total y métricas de calidad en la misma tabla [Kapoor et al., 2024](#ref-kapoor2024). Cuando el equipo proponga un council de cinco agentes, la pregunta correcta es «¿qué obtuvimos respecto a un solo agente bien instruido, y cuánto nos costó?», no «¿funciona?» (casi todo funciona en la demo).

## El ciclo de vida del agente como máquina de estados: rigor técnico de producción

Antes de describir cómo los orquestadores coordi coordinan múltiples agentes, es esencial entender cómo un agente individual transiciona entre estados. En producción, ese ciclo es un autómata finito determinista, no un diagrama conceptual: cada transición es observable, auditable y fallible de forma predecible. Esta es la diferencia entre un prototipo que funciona en la demo y un sistema agéntico que funciona en producción a escala.

En primer lugar, el ciclo del agente tiene exactamente cinco estados bien definidos: **Inactivo** (aguardando tarea), **Planificación** (decomposición y selección de herramientas), **Ejecución** (invocación de herramientas y APIs), **Evaluación** (validación de resultados y decisión de reintento), y **Completado** o **Fallido** (terminal). Cada transición es gatillada por un evento observable: recepción de tarea, plan seleccionado, observación registrada, presupuesto agotado.

![Diagrama 8.2: Ciclo de vida del agente como máquina de estados, del Inactivo al Completado, con reintentos y paradas de seguridad](imagenes/uml/8_state_agent_es.png)

A continuación, la estructura del ciclo revela cuatro decisiones críticas que cualquier implementación debe resolver:

**La representación del estado es política de negocio.** El diagrama distingue entre transiciones que pertenecen al dominio («reintento requerido», «éxito») y transiciones que pertenecen a la infraestructura («presupuesto excedido», «error»). Esa distinción es lo que permite un log de auditoría que un humano o un auditor regulatorio pueden leer sin escarbar en code. El registro del evento debe incluir: timestamp, agente_id, estado_anterior, estado_nuevo, razón (contrato verificable), y tokens consumidos hasta ese punto.

**La contrapresión previene cascadas.** Cuando el agente entra en la fase de Ejecución, no todas las herramientas pueden ser invocadas. El servidor MCP (capítulo 9) que le brinda acceso a las herramientas debe ser capaz de rechazarlas si violarían presupuesto, permisos o invariantes de dominio (capítulo 6). Ese rechazo es una transición de **Ejecución → Evaluación** con razón «herramienta rechazada por guardarraíles». El modelo, al recibirlo, debe saber que ese es un NO definitivo, no una opinión.

**Primero, la observación cierra el bucle.** Cuando una herramienta falla (la API externa está caída, el resultado es inválido), la transición natural es **Ejecución → Evaluación**. El evaluador, en Evaluación, debe decidir: ¿reintento? (la red se recupera), ¿cambiar de herramienta? (la especificación era ambigua), ¿terminal? (presupuesto agotado). Sin una observación clara de por qué falló, esa decisión es adivinanza. De ahí que el contrato de la herramienta (capítulo 4) incluya la estructura del error: `{ "is_error": true, "reason": "external_api_timeout", "recovery_hint": "retry in 30 seconds" }`.

Finalmente, el presupuesto no es una sugerencia.  Cuando el agente ha consumido N iteraciones, o M tokens, o el tiempo T ha transcurrido, la máquina de estados salta a **Evaluación → Fallido** automáticamente, sin pedir permiso. La gobernanza (capítulo 1 (Vol. 4)) inyecta este límite en la máquina misma, no como una validación de aplicación: si el contador alcanza el tope, la transición no es posible.

**► PISTA TÉCNICA: Máquina de estados en TypeScript con presupuesto integrado**

```typescript
// agent-state-machine.ts
// Implementación de la máquina de estados del agente con auditabilidad incorporada.
// La política de presupuesto vive en el estado, no en el resto del código.

enum AgentState {
  IDLE = "IDLE",
  PLANNING = "PLANNING",
  EXECUTING = "EXECUTING",
  EVALUATING = "EVALUATING",
  COMPLETED = "COMPLETED",
  FAILED = "FAILED",
}

interface StateTransition {
  timestamp: Date;
  fromState: AgentState;
  toState: AgentState;
  reason: string;
  tokensConsumedTotal: number;
  agentId: string;
}

interface AgentBudget {
  maxIterations: number;
  maxTokens: number;
  maxTimeMs: number;
  currentIterations: number;
  currentTokens: number;
  startTimeMs: number;
}

class AgentStateMachine {
  private state: AgentState = AgentState.IDLE;
  private transitions: StateTransition[] = [];
  private budget: AgentBudget;
  private llmPort: LlmPort; // del capítulo 6 (Vol. 4)

  constructor(
    agentId: string,
    maxIterations: number = 10,
    maxTokens: number = 100000,
    maxTimeMs: number = 300000 // 5 minutos
  ) {
    this.budget = {
      maxIterations,
      maxTokens,
      maxTimeMs,
      currentIterations: 0,
      currentTokens: 0,
      startTimeMs: Date.now(),
    };
  }

  // Transición: solo si es válida según presupuesto
  private canTransitionTo(nextState: AgentState): boolean {
    const elapsed = Date.now() - this.budget.startTimeMs;
    if (elapsed > this.budget.maxTimeMs) return false;
    if (this.budget.currentIterations >= this.budget.maxIterations)
      return false;
    if (this.budget.currentTokens >= this.budget.maxTokens) return false;
    return true;
  }

  async executeTask(input: string): Promise<string> {
    // Transición: IDLE → PLANNING
    this._transition(AgentState.PLANNING, "task.received");

    const plan = await this.llmPort.complete(
      "Planifica la tarea...",
      input,
      "BALANCED"
    );
    this.budget.currentTokens += plan.inputTokens + plan.outputTokens;

    while (true) {
      this.budget.currentIterations++;

      // Guardarraíles: ¿se puede seguir?
      if (!this.canTransitionTo(AgentState.EXECUTING)) {
        this._transition(
          AgentState.EVALUATING,
          "budget.exhausted"
        );
        break;
      }

      // Transición: PLANNING → EXECUTING
      this._transition(AgentState.EXECUTING, "plan.selected");

      const toolResult = await this.executeTool(plan);
      this.budget.currentTokens += toolResult.tokensUsed;

      // Transición: EXECUTING → EVALUATING
      this._transition(
        AgentState.EVALUATING,
        "observation.received"
      );

      // Evaluación: ¿reintentamos?
      if (toolResult.isError) {
        if (this.budget.currentIterations < this.budget.maxIterations) {
          // Reintento: EVALUATING → PLANNING
          this._transition(AgentState.PLANNING, "retry.required");
          continue;
        } else {
          // Presupuesto agotado: EVALUATING → FAILED
          this._transition(AgentState.FAILED, "max.iterations.reached");
          break;
        }
      } else {
        // Éxito: EVALUATING → COMPLETED
        this._transition(AgentState.COMPLETED, "success");
        return toolResult.content;
      }
    }

    // Si llegamos aquí, fue un fallo
    throw new Error(
      `Agent failed: ${this.state}. ` +
      `Iterations: ${this.budget.currentIterations}/${this.budget.maxIterations}, ` +
      `Tokens: ${this.budget.currentTokens}/${this.budget.maxTokens}`
    );
  }

  private _transition(
    nextState: AgentState,
    reason: string
  ): void {
    const transition: StateTransition = {
      timestamp: new Date(),
      fromState: this.state,
      toState: nextState,
      reason,
      tokensConsumedTotal: this.budget.currentTokens,
      agentId: this.constructor.name,
    };

    // Log estructurado: auditoría inmediata
    console.log(
      JSON.stringify(transition, null, 2)
    );
    this.transitions.push(transition);

    this.state = nextState;
  }

  // Recurso para auditoría: el historial de transiciones
  getAuditTrail(): StateTransition[] {
    return [...this.transitions];
  }
}
```

La virtud de este diseño es que el presupuesto no es un comentario en el código: es una estructura que la máquina de estados consulta en cada iteración, automáticamente. Un agente que excede presupuesto no «continúa por error»; no puede transicionar, punto. Esa restricción vive cerca del estado, donde pertenece.

## Arquitectura empresarial de agentes: la plataforma de producción

Cuando múltiples agentes especializados deben orquestar flujos complejos en una organización (decenas de equipos, latencias variables, gobernanza de IA, auditoría regulatoria) el diseño no puede ser ad-hoc. Emerge una necesidad arquitectónica clara: una **plataforma de agentes** que separe preocupaciones en capas lógicas, cada una con su responsabilidad única, su contrato explícito y su mecanismo de observabilidad.

![Diagrama 8.3: Arquitectura de Plataformas Agénticas de Producción: Las cuatro capas de la orquestación empresarial (Abstracción de Modelos, Núcleo de Ejecución, Eventos y Evaluación, Observabilidad Transversal)](imagenes/publicados/arquitectura_agentica_enterprise.png)

La arquitectura que el diagrama revela es una evolución natural de los cinco patrones que presentamos en la primera sección, y de la máquina de estados que acaba de describirse. Primero, organiza explícitamente la división de responsabilidades:

**Capa de Abstracción de Modelos (AI Gateway).** Aquí reside toda la lógica que media entre los agentes y los proveedores de LLMs externos. El gateway cumple cuatro funciones simultáneamente: (1) **resiliencia**, encolando solicitudes fallidas para reintento automático; (2) **caché de prefijos**, reutilizando fragmentos de contexto estables a costo reducido; (3) **control de cuotas**, bloqueando nuevas llamadas si se alcanzó el presupuesto de tokens o dinero; (4) **polimorfismo de modelos**, enrutando solicitudes al modelo más económico o más capaz según el tier de tarea (capítulo 3). El axioma arquitectónico que gobierna esta capa es: **el agente nunca debe "saber" quién responde sus preguntas**.

A continuación, el Núcleo de Ejecución del Agente (Orquestador + MCP). Aquí vive la máquina de estados que ya describimos, el bucle ReAct (capítulo 4) y la capacidad de delegación a especialistas. El Orquestador es el corazón: recibe una tarea, descompone si es necesario (patrón jerárquico del capítulo 8), delega a especialistas y sintetiza. El Servidor MCP es el sistema nervioso: expone las herramientas que los agentes pueden invocar, validando permisos, esquemas y rechazando operaciones que violarían invariantes del dominio (capítulo 6). Juntos, son el lugar donde vive la **política de negocio pura**, sin detalles de infraestructura.

Además, el Ecosistema de Eventos y Evaluación Continua. Cuando un agente completa una tarea, no desaparece en silencio. Publica un evento en Kafka: quién ejecutó qué, con qué costo, con qué resultado. Ese evento fluye hacia dos destinos: (1) consumidores de negocio que actúan sobre el resultado (el siguiente paso en un pipeline); (2) el Eval Harness, que analiza si la respuesta cumple umbrales de calidad, detecta alucinaciones, y si encuentra problemas, publica a la DLQ para revisión humana. El patrón es: **la evaluación es continua, no posterior**; si el agente degrada, lo sabemos en minutos, no en la próxima auditoría trimestral.

Finalmente, la Capa de Telemetría Transversal (Observabilidad). Cada paso (cada transición de estado, cada llamada al modelo, cada invocación de herramienta) genera spans que OpenTelemetry (capítulo 8 (Vol. 4)) agrega en trazas distribuidas. La razón: cuando un cliente reporta «mi solicitud tardó 5 minutos», necesitamos saber en segundos si fue el agente, el modelo, la base de datos remota, o una combinación. Esa traza es la única fuente de verdad para el debugging en producción.

**► PISTA TÉCNICA: Cómo las capas se comunican sin acoplamiento**

```java
// PlatformAgentOrchestrator.java
// El orquestador de la plataforma: cómo coordina las capas sin conocer
// sus internales. Los puertos (interfaces) son el único contrato.

@Service
public class PlatformAgentOrchestrator {
    
    private final LlmPort llmGateway;              // Capa de Abstracción
    private final MCP_ServerPort toolExecutor;     // Núcleo
    private final EventBusPort eventPublisher;     // Eventos
    private final EvalHarnessPort evaluator;       // Evaluación
    private final ObservabilityPort tracer;        // Telemetría
    
    @Transactional
    public AgentResult executeTask(TaskRequest task) {
        // Crear traza raíz para esta tarea
        Span rootSpan = tracer.startSpan("agent.task", 
            task.agentId, task.taskId);
        
        try {
            // PASO 1: Planificación (máquina de estados: PLANNING)
            rootSpan.addEvent("state.planning");
            Plan plan = generatePlan(task);
            
            // PASO 2: Ejecución (máquina de estados: EXECUTING)
            rootSpan.addEvent("state.executing");
            Result result = executeWithRetries(plan, rootSpan);
            
            // PASO 3: Publicar evento (desacoplamiento)
            eventPublisher.publish(new AgentExecutedEvent(
                taskId: task.taskId,
                agentId: task.agentId,
                result: result,
                tokensUsed: result.tokenMetrics,
                timestamp: Instant.now()
            ));
            
            // PASO 4: Evaluación asíncrona
            evaluator.asyncEval(result, task.agentId);
            
            rootSpan.addEvent("state.completed");
            return result;
            
        } catch (Exception e) {
            rootSpan.recordException(e);
            rootSpan.addEvent("state.failed");
            
            // Publicar a DLQ para revisión
            eventPublisher.publishToDLQ(new AgentFailedEvent(
                taskId: task.taskId,
                error: e.getMessage(),
                context: task
            ));
            throw e;
        } finally {
            rootSpan.end();
        }
    }
    
    private Result executeWithRetries(Plan plan, Span span) {
        int attempt = 0;
        while (attempt < MAX_ATTEMPTS) {
            try {
                // El gateway abstrae los reintentos internos y la caché
                LlmResponse response = llmGateway.complete(
                    plan.systemPrompt,
                    plan.userPrompt,
                    plan.tier
                );
                
                if (response.requiresToolUse()) {
                    // El MCP Server valida y ejecuta herramientas
                    ToolResult toolResult = toolExecutor.executeTool(
                        response.toolName,
                        response.toolInput,
                        plan.domainContext  // Invariantes del dominio
                    );
                    
                    span.addEvent("tool.executed", 
                        Map.of("tool", response.toolName,
                               "success", !toolResult.isError));
                    
                    // El resultado vuelve al agente (máquina de estados)
                    plan = plan.withObservation(toolResult);
                } else {
                    // El agente alcanzó conclusión
                    return new Result(response.text, response.tokens);
                }
                
                attempt++;
            } catch (RateLimitException e) {
                // El gateway maneja el rate limiting
                span.addEvent("rate_limit", 
                    Map.of("retry_after_ms", e.retryAfterMs));
                Thread.sleep(e.retryAfterMs);
                attempt++;
            }
        }
        
        throw new BudgetExhaustedException(
            "Max attempts reached for task " + plan.taskId);
    }
}
```

El poder de esta estructura es que cada capa puede evolucionarse sin tocar las otras. Si mañana decides cambiar de Kafka a Pulsar, el Orquestador no se entera: solo usa el EventBusPort. Si Claude lanza un modelo nuevo, el Gateway se configura sin recompilar el Orquestador. Si el Eval Harness necesita añadir una nueva métrica de calidad, la DLQ la captura y alimenta el aprendizaje. La **extensibilidad nace del desacoplamiento**.

## Orquestadores limpios: los cuatro anti-patrones

El orquestador es a la Empresa Sintética lo que la raíz de composición es a un sistema con inyección de dependencias: el único lugar donde se decide quién habla con quién. El Código Limpio Sintético (capítulo 4) identifica sus cuatro degeneraciones recurrentes:

1. **El dios-orquestador.** El orquestador que, además de coordinar, opina, corrige y reescribe los resultados de sus especialistas. Es la god class otra vez: cuando el sintetizador del council empieza a «mejorar» el código del coder, hay dos roles mal mezclados, y un eval que ya no sabe a quién atribuir los fallos. Regla: el orquestador decide y compone; no produce contenido de dominio.
2. **Los agentes charlatanes.** Eslabones que se pasan el contexto completo unos a otros «por si acaso». Cada salto duplica tokens y degrada la señal [Liu et al., 2024](#ref-liu2024). Regla: entre agentes viajan **contratos** (el JSON del prompt maestro, capítulo 5), no transcripciones.
3. **El bucle de cortesía.** Dos agentes que se validan mutuamente hasta el límite de presupuesto («buen punto», «de acuerdo contigo»). Es el modo de fallo conocido del debate sin estructura: el consenso prematuro. Regla: los debates tienen rondas fijas, roles adversariales explícitos y un sintetizador con autoridad para cerrar [Du et al., 2023](#ref-du2023).
4. **La jerarquía infinita.** Orquestadores que delegan en orquestadores que delegan. Cada nivel añade latencia, costo y un punto de fallo de razonamiento; la evidencia de los marcos publicados es consistente en que un solo nivel de delegación captura casi todo el valor ([Qian et al., 2024](#ref-qian2024); [Hong et al., 2024](#ref-hong2024)). Regla: un nivel de profundidad salvo justificación medida.

## AOP para agentes: propagación de errores como aspecto transversal

Los cinco patrones y los cuatro anti-patrones anteriores comparten un punto ciego: ninguno dice qué hace el sistema cuando un eslabón del pipeline, una rama del fan-out o un consejero del council simplemente falla. Sin un diseño deliberado, cada agente termina reimplementando su propio *try/except*, su propio reintento, su propio formato de log, y cuando el orquestador crece hacia los enjambres de 20 a 96 agentes del capítulo 5 (Vol. 4), esa duplicación se convierte en el mayor foco de inconsistencia del sistema: un mismo tipo de fallo se registra distinto según quién lo capturó primero.

La Programación Orientada a Aspectos (AOP), formalizada por Kiczales et al. (1997) para separar *cross-cutting concerns* (logging, seguridad, transacciones) de la lógica de negocio en sistemas empresariales, encuentra en la orquestación de agentes un caso de uso casi de manual: interceptar cada llamada a herramienta o invocación de agente con un comportamiento común, sin que el agente mismo necesite saber que ese comportamiento existe.

**Los tres aspectos mínimos que todo orquestador de producción necesita:**

1. **Aspecto de captura.** Envuelve cada llamada y normaliza cualquier excepción a un tipo común (`AgentError`) con metadata: qué agente, qué herramienta, qué intento, qué patrón de los cinco anteriores estaba en curso.
2. **Aspecto de propagación.** Decide si el error sube al llamador sin modificar (falla dura), se convierte en una entrada degradada para el sintetizador (falla suave), o dispara un reintento con backoff, la misma taxonomía del presupuesto de degradación del capítulo 5 del Vol. 4, caso 8.
3. **Aspecto de trazabilidad.** Adjunta el error a la traza OpenTelemetry (capítulo 1 (Vol. 4), Vol. 4) con el mismo esquema que una ejecución exitosa, para que la auditoría de reproducción cruzada (Vol. 3, capítulo 20) pueda comparar fallos entre proveedores con el mismo rigor con que compara éxitos.

```python
def con_aspecto_de_errores(politica_degradacion):
    """Decorador que separa el manejo de errores de la lógica del agente."""
    def decorador(func_agente):
        @functools.wraps(func_agente)
        async def envoltura(*args, **kwargs):
            intento = 0
            while True:
                try:
                    resultado = await func_agente(*args, **kwargs)
                    registrar_traza(func_agente.__name__, "exito", intento)
                    return resultado
                except Exception as e:
                    error = AgentError.desde(e, agente=func_agente.__name__, intento=intento)
                    registrar_traza(func_agente.__name__, "error", intento, error)
                    accion = politica_degradacion.decidir(error, intento)
                    if accion == "reintentar":
                        intento += 1
                        await asyncio.sleep(backoff(intento))
                        continue
                    if accion == "degradar":
                        return ResultadoDegradado(motivo=error)
                    raise error  # falla dura: sube tal cual al orquestador
        return envoltura
    return decorador

@con_aspecto_de_errores(politica_degradacion=POLITICA_ESTANDAR)
async def agente_investigador(consulta):
    ...
```

El decorador es agnóstico del framework: el mismo aspecto envuelve una llamada al Task tool de Claude, un handoff de OpenAI Agents SDK, o un nodo de un `ParallelAgent` de Google ADK (capítulo 5, Vol. 4), la lógica de negocio del agente no cambia una línea al migrar de proveedor, que es, otra vez, el Backend Agnóstico sostenido a nivel de código, no solo de arquitectura.

**La política de degradación no es una sola: cada patrón exige una por defecto distinta.** El pipeline, por diseño, detiene todo ante una falla dura (esa rigidez es su ventaja documentada más arriba). El fan-out debe degradar en lugar de fallar: perder una fuente no debería cancelar la síntesis, siempre que el hueco quede documentado. El council debe hacer visible la degradación al sintetizador («2 de 3 consejeros respondieron»), nunca silenciarla como si el quórum completo hubiera opinado. El jerárquico debe propagar la falla del trabajador como un `AgentError` estructurado, no como una excepción cruda, para que el orquestador decida con la misma información que tendría un humano. El self-reflection loop debe fallar cerrado: si el evaluador mismo falla, la salida por defecto es "no aprobado", nunca "aprobado por ausencia de objeción", el mismo principio de la valla de permisos del capítulo 2 (Vol. 3).

**Por qué esto es el camino hacia la fluidez, no un costo adicional.** Un enjambre que maneja sus errores de forma transversal e inconsistente no es lento porque el modelo sea lento: es lento porque cada incidente exige que un ingeniero rastree manualmente en qué capa se perdió el error. La velocidad que hoy asociamos con GPT-6 Astra (corridas de decenas de agentes sostenidas durante horas) depende tanto del aspecto de errores como del modelo detrás: sin captura y propagación uniformes, un enjambre de esa escala simplemente no sobrevive lo suficiente para completar la tarea. La excelencia técnica y la velocidad de negocio, en este caso, son la misma disciplina de ingeniería vista desde dos ángulos.



*(Caso compuesto ilustrativo; cifras de orden de magnitud, calculadas con los precios del apéndice B.)*

Una organización debe decidir si migra su monolito a microservicios, la pregunta del ejemplo 8.1. El arquitecto ejecuta el council tres veces para verificar estabilidad de la recomendación (una práctica barata que casi nadie usa: tres ejecuciones siguen costando centavos).

**La traza, condensada.** El consejero de escalabilidad cuantifica: el monolito sirve 50.000 usuarios con p95 estable; el cuello real es la base de datos, no el código. El de developer experience advierte: el equipo de doce personas no tiene experiencia operando sistemas distribuidos; la migración consumiría dos trimestres de su capacidad. El económico calcula el costo de oportunidad contra el backlog actual. El sintetizador produce: **DECISIÓN: no migrar ahora; extraer únicamente el módulo de reportes** (la fuente real de presión), con tres condiciones medibles que reabrirían la decisión y un primer paso para la semana.

**La cuenta.** Cuatro llamadas (tres consejeros en el modelo balanceado, síntesis en el premium), unos 18.000 tokens en total por ejecución: del orden de **15 a 20 centavos de dólar por corrida**, menos de un dólar por las tres. El contraste pedagógico: la alternativa humana (tres arquitectos senior, una reunión de dos horas) cuesta tres órdenes de magnitud más, y no deja traza estructurada. El council no reemplaza esa conversación humana: la **prepara**, entregando a los humanos un mapa de argumentos con sus tensiones ya explícitas. Ahí está su ROI real, y por eso el patrón se reserva para decisiones caras de revertir: en una decisión trivial, ni siquiera 20 centavos se justifican frente a una llamada simple.

## Ejercicio resuelto 8.1: elija el patrón

**Enunciado.** Para cada escenario, elija el patrón de orquestación y justifique: (a) traducir 2.000 descripciones de producto a tres idiomas; (b) decidir el esquema de particionado de una base de datos que costará semanas revertir; (c) generar una función con sus tests hasta que la suite pase.

**Solución comentada.**

- **(a) Ninguno: o fan-out trivial.** Son 6.000 tareas independientes y verificables por separado: una llamada bien diseñada por unidad, ejecutada por la API batch a mitad de precio (capítulo 1 (Vol. 4)). Quien proponga aquí un sistema multi-agente está comprando complejidad sin propiedad alguna a cambio: la primera rama del árbol de decisión existe precisamente para este caso.
- **(b) Council.** Decisión cara de revertir, con perspectivas legítimamente en tensión (rendimiento, operación, costo) y sin verificador automático posible. El debate estructurado mejora la factualidad de la recomendación [Du et al., 2023](#ref-du2023) y el costo del patrón es despreciable frente al costo del error: el caso de estudio anterior es esta misma situación.
- **(c) Self-reflection loop.** Existe una señal de éxito objetiva y automática (la suite pasa), que es el requisito del patrón ([Shinn et al., 2023](#ref-shinn2023); [Madaan et al., 2023](#ref-madaan2023)). Con presupuesto: máximo N iteraciones, y el evaluador es el test runner, determinista, no otro LLM opinando.

El meta-aprendizaje del ejercicio: la pregunta nunca es «¿qué patrón es mejor?» sino «¿qué propiedad necesito comprar y cuál es la señal de calidad disponible?». Verificabilidad automática → bucle; tensión de perspectivas → council; independencia → lote; pasos conocidos → pipeline.

## Lo esencial del capítulo 8

- Más agentes no es mejor: sin control de costo, las comparaciones son marketing [Kapoor et al., 2024](#ref-kapoor2024). El patrón correcto es el mínimo que compra la propiedad necesaria.
- Cinco patrones canónicos: pipeline (defecto), fan-out (independencia + contrato), council (decisiones caras), jerárquico (descomposición dinámica), self-reflection (señal verificable + presupuesto).
- **Máquina de estados de producción:** el ciclo del agente (Inactivo → Planificación → Ejecución → Evaluación → Completado/Fallido) no es conceptual; es un autómata observable, auditable y con guardarraíles de presupuesto integrados en la estructura, no como validaciones posteriores.
- **Presupuesto como política codificada:** transiciones bloqueadas, no sugerencias ignoradas. Si maxIterations se alcanza, la máquina salta a Fallido sin pedir permiso.
- **Arquitectura empresarial de cuatro capas:** (1) Abstracción de Modelos (gateway con resiliencia y caché), (2) Núcleo de Ejecución (orquestador + MCP), (3) Eventos y Evaluación Continua (Kafka + Eval Harness), (4) Observabilidad Transversal (trazas distribuidas). El desacoplamiento entre capas es el axioma: cambiar un proveedor de LLM no debe recompilar el orquestador.
- Cuatro anti-patrones: dios-orquestador, agentes charlatanes, bucle de cortesía, jerarquía infinita.
- Entre agentes viajan contratos, no transcripciones.
- AOP separa el manejo de errores de la lógica de negocio en tres aspectos (captura, propagación, trazabilidad); cada uno de los cinco patrones exige una política de degradación por defecto distinta, y esa uniformidad (no un modelo más rápido) es lo que sostiene un enjambre a la escala de Astra.
- El council prepara la decisión humana con argumentos trazables por centavos; no la sustituye.
- **Auditoría estructurada:** cada transición de estado, cada evento, cada herramienta invocada registra quién, cuándo, costo y resultado. La DLQ captura los fallos; la traza los explica. Esa es la base de compliance, debugging y evaluación post-incidente.

---
