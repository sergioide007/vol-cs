# Capítulo 8: Operar el sistema, observabilidad y MLOps para equipos pequeños

## No se gobierna lo que no se ve

Los capítulos 11 y 13 dieron las métricas (CIU, evals); este capítulo las pone a correr en producción. La disciplina madre es la ingeniería de fiabilidad: las cuatro señales doradas (latencia, tráfico, errores, saturación) como mínimo vital de cualquier servicio ([Beyer et al., 2016](#ref-beyer2016)), y los tres pilares clásicos de la observabilidad (logs, métricas y trazas) como sus instrumentos. El estándar abierto que los unifica hoy es OpenTelemetry (OpenTelemetry, s.f.), y su concepto central, la **traza distribuida**, parece diseñado para nosotros: el bucle ReAct *es* una traza; la tarea es el span raíz; cada pensamiento, llamada al modelo y ejecución de herramienta, un span hijo con duración, atributos y resultado.

A las señales doradas, el sistema agéntico añade las suyas (las **señales sintéticas**), todas derivables de la instrumentación que el libro ya construyó:

| Señal | Qué revela | De dónde sale |
|---|---|---|
| Tokens entrada/salida por tarea | Contexto inflado, verbosidad | AIGateway (cap. 3) |
| Tasa de acierto de caché | Prefijos rotos por timestamps/UUIDs | `cache_read_input_tokens` (cap. 10) |
| Iteraciones por tarea (p50/p95) | Bucles degenerados, prompts ambiguos | Bucle agéntico (cap. 4) |
| Tasa de error de herramientas | Esquemas ambiguos, sistemas caídos | Resultados `is_error` (cap. 4) |
| CIU por equipo y feature | La economía completa | CIUTracker (cap. 10) |
| Tasa de paso de evals | Deriva de calidad | Suite en CI (cap. 12) |
| Profundidad de la DLQ | Casos que el sistema no digiere | Broker (cap. 16) |

```python
# Ejemplo 8.1 (Python + OpenTelemetry): el bucle ReAct como traza.
# Cada tarea = un span raíz; cada herramienta = un span hijo.
# pip install opentelemetry-api opentelemetry-sdk

from opentelemetry import trace

tracer = trace.get_tracer("agente.revisor")

def run_agent_traced(user_input: str, max_iterations: int = 10) -> str:
    with tracer.start_as_current_span("tarea.code-review") as root:
        root.set_attribute("agent.prompt_version", "reviewer-v3")
        messages = [{"role": "user", "content": user_input}]

        for i in range(max_iterations):
            with tracer.start_as_current_span("llm.call") as span:
                response = client.messages.create(
                    model="claude-opus-4-8", max_tokens=4096,
                    tools=TOOLS, messages=messages)
                span.set_attribute("llm.model", response.model)
                span.set_attribute("llm.tokens.input",
                                   response.usage.input_tokens)
                span.set_attribute("llm.tokens.output",
                                   response.usage.output_tokens)
                span.set_attribute("llm.cache.read",
                                   response.usage.cache_read_input_tokens or 0)

            if response.stop_reason != "tool_use":
                root.set_attribute("agent.iterations", i + 1)
                return extract_text(response)

            messages.append({"role": "assistant", "content": response.content})
            results = []
            for block in response.content:
                if block.type == "tool_use":
                    with tracer.start_as_current_span(
                            f"tool.{block.name}") as tspan:
                        content, is_err = execute_tool(block.name, block.input)
                        tspan.set_attribute("tool.is_error", is_err)
                        results.append({"type": "tool_result",
                                        "tool_use_id": block.id,
                                        "content": content,
                                        "is_error": is_err})
            messages.append({"role": "user", "content": results})

        root.set_attribute("agent.budget_exhausted", True)
        return "Presupuesto de iteraciones agotado."
```

El atributo más valioso de toda la traza es el menos técnico: `agent.prompt_version`. Cuando la tasa de paso de evals caiga un martes a las 15:40, esa etiqueta dirá en segundos si fue el despliegue del prompt nuevo, una actualización silenciosa del modelo del proveedor, o un cambio en la distribución de las entradas. Sin ella, la respuesta son tres días de arqueología.

## MLOps para equipos pequeños: LLMOps sin ceremonia

La literatura de MLOps nació para equipos que entrenan modelos, con su deuda técnica oculta (el código del modelo como fracción mínima del sistema; [Sculley et al., 2015](#ref-sculley2015)) y sus rúbricas de madurez ([Breck et al., 2017](#ref-breck2017)). El equipo de este libro no entrena nada, y eso simplifica radicalmente la disciplina: su «modelo» es un compuesto de *prompt + contexto + herramientas + identificador de modelo del proveedor*. La traducción honesta de MLOps a este mundo (llámese LLMOps) cabe en cuatro prácticas que un equipo de tres personas opera sin plataforma dedicada:

1. **Versionar el compuesto, no solo el código.** Prompts maestros, contextos de dominio, skills, esquemas de herramientas e identificadores de modelo viven en Git y se etiquetan juntos: el despliegue es un *release* del compuesto. La pregunta «¿qué versión del agente respondió esto?» tiene respuesta de una palabra: la etiqueta que viaja en la traza y en los eventos (capítulo 7).
2. **Probar el compuesto en CI.** La suite de evals (capítulo 13) corre en cada cambio de cualquier pieza del compuesto. La rúbrica de Breck et al. (2017) se hereda adaptada: ¿los datos de evaluación versionados? ¿umbrales que rompen la build? ¿costo medido junto a calidad?
3. **Desplegar con canario.** El prompt nuevo atiende el 10 % del tráfico durante una ventana; el CIU y la tasa de evals del canario se comparan con el control antes de promover. En el mundo event-driven (capítulo 7) esto es un segundo grupo de consumidores leyendo el mismo log; el canario más barato jamás construido.
4. **Monitorear la deriva con los propios evals.** Una muestra diaria de tráfico real pasa por la suite; la tendencia, no el valor puntual, dispara la alerta. Los proveedores actualizan modelos: el comportamiento correcto de ayer es una hipótesis, no una garantía (capítulo 1 (Vol. 3)).

### Migraciones de agentes: el patrón Flyway/Liquibase aplicado al compuesto

Versionar con etiquetas de Git (práctica 1) basta para saber qué compuesto corrió; no basta para responder la pregunta que Flyway y Liquibase llevan veinte años resolviendo en bases de datos: ¿en qué orden exacto se aplicaron los cambios a cada entorno, y puede reconstruirse ese orden si un entorno se desincroniza? Un prompt maestro editado directamente en producción, sin pasar por dev y stage, es el equivalente agéntico de un `ALTER TABLE` ejecutado a mano contra la base de producción, justo lo que estas herramientas existen para impedir.

La adaptación es directa. Cada cambio al compuesto, prompt, esquema de herramienta, política de degradación (capítulo 5, caso 8), asignación RACI (Vol. 3, capítulo 15), se declara como una migración numerada e inmutable:

```
migraciones/
  agente_investigador/
    V001__prompt_inicial.md
    V002__anade_herramienta_busqueda_web.yaml
    V003__ajusta_politica_degradacion.yaml
    V004__actualiza_modelo_a_claude_sonnet_5.yaml
```

Tres garantías, tomadas directamente de Flyway/Liquibase, son las que de verdad importan:

1. **Checksum de migración aplicada.** Una vez que `V002` se aplicó en un entorno, su contenido queda hasheado en una tabla de historial (`agent_migrations`: agente, versión, entorno, checksum, aplicado_por, fecha). Si alguien edita `V002.yaml` después de aplicada, la siguiente ejecución falla por checksum distinto, el mismo mecanismo que impide reescribir a mano la historia de un esquema SQL en producción, aplicado ahora al historial de decisiones de un agente.
2. **Orden estricto, sin saltos.** `V004` no puede aplicarse en producción si `V003` no se aplicó antes en ese mismo entorno. Esto resuelve, en la práctica, la pregunta de promoción entre entornos del capítulo 5 (caso 8, Vol. 4): superar el umbral de IAO ajustado es necesario pero no basta; la secuencia de migraciones de stage debe ser, además, un subconjunto exacto y en el mismo orden de la que se promueve a producción.
3. **Migración de reversión emparejada.** Cada `V00N` declara su `U00N` (undo). Si el prompt de `V004` degrada la calidad medida por evals (práctica 3, canario), el rollback correcto no es editar el prompt de vuelta a mano (eso pierde la auditoría): es aplicar `U004`, registrado en la misma tabla de historial con la misma disciplina que su aplicación original.

**Qué compra esto que Git por sí solo no compra.** Un `git log` responde qué cambió; una tabla de migraciones aplicadas responde qué está vigente en cada entorno en este instante, sin necesidad de hacer *checkout* del commit correcto en cada uno, la misma pregunta que la auditoría de reproducción cruzada (Vol. 3, capítulo 20) necesita antes de replicar una traza contra un segundo proveedor: qué versión exacta del compuesto produjo esa decisión.

**■ PISTA EJECUTIVA: el stack mínimo viable para un equipo de tres**

| Capacidad | Instrumento suficiente | Costo típico |
|---|---|---|
| Trazas y métricas | OpenTelemetry + cualquier backend (hay opciones libres y gestionadas) | Horas de configuración |
| Versionado del compuesto | Git + etiquetas + PR obligatorio para `prompts/` | Cero |
| Evals en CI | El runner de CI existente + API batch a mitad de precio | Centavos por corrida |
| Canario | Un segundo grupo de consumidores o un flag de enrutamiento | Horas |
| Alertas | Umbral sobre CIU, evals y DLQ en el dashboard existente | Cero |
| Migraciones del compuesto | Tabla de historial (SQLite basta) + convención `V00N`/`U00N` en `prompts/` | Cero |

La columna de costos es el argumento: nada de esta disciplina exige plataforma nueva ni equipo dedicado. Exige decidir que el sistema agéntico es un sistema de producción, y tratarlo con la seriedad que ya se le da al resto.

## Ejercicio resuelto 8.1: las alertas del pipeline de code review

**Enunciado.** Defina las alertas mínimas del pipeline de revisión (capítulos 15 y 17): condición, umbral inicial y a quién despierta cada una.

**Solución comentada.** Cinco alertas bastan, y ninguna usa un valor absoluto arbitrario; todas comparan contra la línea base móvil de la semana anterior, porque en sistemas no deterministas el *cambio* informa y el valor absoluto miente:

1. **Calidad:** tasa de paso de la muestra diaria de evals cae > 10 puntos vs. línea base → dueño del agente (humano nombrado, capítulo 1 (Vol. 3)). Es la alerta reina; las demás suelen explicarla.
2. **Economía:** CIU del pipeline sube > 50 % vs. línea base sostenido 2 horas → mismo dueño; causa típica: contexto inflado por un cambio en el tamaño de los diffs, o caché rota por un prefijo modificado.
3. **Latencia:** p95 de `tarea.code-review` (la traza raíz) supera el doble de la línea base → guardia de plataforma; causa típica: proveedor degradado; verificar antes de tocar nada propio.
4. **Digestión:** profundidad de la DLQ > 5 mensajes/hora → revisión en el día; cada mensaje es un eval candidato.
5. **Presupuesto:** corte duro del gasto por hora (capítulo 7) → se pausa solo; la alerta informa, no pide permiso.

El error de diseño a evitar quedó fuera de la lista deliberadamente: alertar sobre tokens por llamada. Esa señal oscila con cada PR y entrena al equipo a ignorar alertas; la métrica agregada con denominador de valor (el CIU) es la que merece despertar a alguien.

## Lo esencial del capítulo 8

- Señales doradas ([Beyer et al., 2016](#ref-beyer2016)) + señales sintéticas: tokens, caché, iteraciones, errores de herramienta, CIU, evals, DLQ.
- El bucle ReAct es una traza distribuida nativa; `agent.prompt_version` en cada span convierte tres días de arqueología en una consulta.
- LLMOps sin ceremonia: versionar el compuesto, probarlo en CI, canario por grupo de consumidores, deriva vigilada por los propios evals ([Sculley et al., 2015](#ref-sculley2015); [Breck et al., 2017](#ref-breck2017)).
- Migraciones tipo Flyway/Liquibase (`V00N`/`U00N`, checksum, orden estricto por entorno) responden qué compuesto está vigente ahora mismo, no solo qué cambió, y hacen del rollback una migración de reversión auditada, no una edición manual.
- Las alertas comparan contra línea base móvil; la única alerta de valor absoluto es el corte de presupuesto, y esa no pide permiso.
- Todo el stack cabe en el presupuesto de un equipo de tres: la barrera es de decisión, no de dinero.
