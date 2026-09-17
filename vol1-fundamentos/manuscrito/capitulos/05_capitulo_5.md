# Capítulo 5: La Empresa Sintética

## Aplicando la especialización al código

Frederick Winslow Taylor revolucionó la manufactura a principios del siglo XX con un principio devastadoramente simple: la especialización sistemática del trabajo aumenta la productividad más que cualquier otro factor. Un trabajador que hace una sola tarea con excelencia supera en rendimiento a diez que hacen diez tareas con mediocridad.

La misma lógica aplica a los sistemas de agentes, y aquí la intuición taylorista tiene respaldo experimental moderno. Un agente de propósito general, que planifica, escribe, revisa y despliega simultáneamente, comete más errores, consume más tokens y produce salidas de menor calidad que un sistema donde cada agente tiene un rol definido y restringido. Los marcos que organizaron agentes como una empresa de software lo demostraron de forma independiente: ChatDev estructura el desarrollo como una cadena de fases (diseño, codificación, prueba) atendidas por agentes especializados que dialogan entre sí [Qian et al., 2024](#ref-qian2024); MetaGPT codifica procedimientos operativos estándar (los SOP de una consultora) en el flujo de comunicación entre agentes con roles de gerente de producto, arquitecto e ingeniero, y con ello reduce drásticamente las alucinaciones en cascada [Hong et al., 2024](#ref-hong2024); y AutoGen generalizó el patrón de conversación entre agentes como primitiva de programación [Wu et al., 2024](#ref-wu2024).

Este es el principio de la **Empresa Sintética**: la organización de agentes en roles especializados, con interfaces de comunicación explícitas entre ellos, refleja la estructura de una empresa de software bien organizada.

La **Ley de Conway** da el marco formal: «cualquier organización que diseñe un sistema producirá un diseño cuya estructura es una copia de la estructura de comunicación de la organización» [Conway, 1968](#ref-conway1968). Aplicada a agentes, la lectura es literal: si sus agentes no tienen protocolos de comunicación claros (quién habla con quién, con qué formato, con qué autoridad), el sistema resultante será tan caótico como una empresa sin organigrama. La novedad histórica es que, por primera vez, el arquitecto diseña *las dos cosas a la vez*: la organización y el sistema son el mismo artefacto.

> **Justificación de diseño: diagrama de clases para modelado estructural**
>
> La Empresa Sintética es ante todo una *estructura*: qué roles existen, cuál es la jerarquía, qué contratos cada rol cumple. Un diagrama de clases (con sus herencias y relaciones) revela exactamente eso: quién reporta a quién, quién es especialista de qué, dónde están los límites de responsabilidad.
>
> Un diagrama de secuencia mostraría cómo interactúan en tiempo de ejecución; un componente mostraría dónde viven en el servidor. Aquí necesitamos ver *la estructura estática del organigrama*, la topología que gobierna todo lo demás.
>
> El diagrama de clases reaparece en este libro en el **Capítulo 6** (DDD y agregados), en el **Capítulo 6 (Vol. 4)** (Clean Architecture y puertos), donde nuevamente usamos clases para mostrar relaciones estructurales que no cambian en el tiempo.

![Diagrama 5.1: La Empresa Sintética: estructura organizacional de agentes (diagrama de clases)](imagenes/capitulo05/diagrama5_1_es.png)

**► PISTA TÉCNICA: Implementando la Empresa Sintética**

```python
# Ejemplo 5.1: Orquestador básico de la Empresa Sintética.
# Roles especializados con modelos de costo distinto por rol:
# el planner usa el modelo más capaz; los analistas, modelos más económicos.

import anthropic

client = anthropic.Anthropic()

AGENT_ROLES = {
    "planner": {
        "model": "claude-opus-4-8",       # razonamiento de arquitectura
        "system": """Eres el CTO de un equipo de ingeniería.
        Recibes un objetivo de negocio y lo descompones en tareas técnicas concretas.
        Output: JSON con lista de tareas, cada una con: descripción, agente responsable,
        criterios de aceptación, y estimado de complejidad (low/medium/high).""",
    },
    "coder": {
        "model": "claude-sonnet-4-6",     # generación de código, balanceado
        "system": """Eres un senior engineer. Implementas código limpio, testeable y
        siguiendo los principios SOLID. Solo produces código, no explicaciones largas.
        Si necesitas aclaración sobre la tarea, pregunta en una sola línea antes de codificar.""",
    },
    "reviewer": {
        "model": "claude-sonnet-4-6",
        "system": """Eres un tech lead experto en code review. Evalúas código en 4 dimensiones:
        1. Correctitud (¿hace lo que debe hacer?), 2. Seguridad (OWASP Top 10),
        3. Mantenibilidad (SOLID, DDD), 4. Performance (complejidad algorítmica).
        Reporta TODOS los hallazgos, incluidos los de severidad baja, con tu nivel
        de confianza en cada uno: un filtro posterior decidirá qué se corrige.
        Output: JSON con score 0-10 por dimensión y lista de cambios requeridos.""",
    },
    "security": {
        "model": "claude-haiku-4-5",      # análisis de patrones, económico
        "system": """Eres un experto en seguridad de aplicaciones. Analiza código buscando
        las vulnerabilidades más comunes: SQL injection, XSS, SSRF, deserialización insegura,
        credenciales en el código, path traversal. Output: JSON con vulnerabilidades,
        severidad (critical/high/medium/low), y remediación sugerida.""",
    },
}

def run_agent(role: str, task: str, context: str = "") -> dict:
    """Ejecuta un agente especializado con su configuración predefinida."""
    config = AGENT_ROLES[role]
    content = f"{context}\n\nTarea: {task}" if context else task

    response = client.messages.create(
        model=config["model"],
        max_tokens=4096,
        system=config["system"],
        messages=[{"role": "user", "content": content}],
    )
    text = next(b.text for b in response.content if b.type == "text")
    return {
        "role": role,
        "output": text,
        "tokens_used": response.usage.input_tokens + response.usage.output_tokens,
        "model": config["model"],
    }

def synthetic_company_pipeline(objetivo: str) -> dict:
    """
    Pipeline de la Empresa Sintética:
    Planner -> Coder -> (Reviewer + Security) -> métricas.
    """
    total_tokens = 0

    plan = run_agent("planner", objetivo)
    total_tokens += plan["tokens_used"]

    code = run_agent("coder", plan["output"],
                     context=f"Plan técnico:\n{plan['output']}")
    total_tokens += code["tokens_used"]

    # Review y Security son independientes: en producción, ejecútelos en
    # paralelo (asyncio / ThreadPoolExecutor). Aquí secuencial por claridad.
    review = run_agent("reviewer", code["output"], context="Código a revisar:")
    total_tokens += review["tokens_used"]

    security_audit = run_agent("security", code["output"],
                               context="Código a auditar:")
    total_tokens += security_audit["tokens_used"]

    return {
        "plan": plan["output"],
        "codigo": code["output"],
        "review": review["output"],
        "security": security_audit["output"],
        "metricas": {
            "total_tokens": total_tokens,
            # El costo real se calcula por modelo y por dirección
            # (input/output); véase el AIGateway del capítulo 3.
        },
    }
```

Obsérvese la decisión económica embebida en la tabla de roles: el planificador usa el modelo más capaz porque sus errores se propagan a todo el pipeline; el auditor de seguridad usa el más económico porque su tarea es de reconocimiento de patrones sobre un texto acotado. Asignar modelo por rol, y no «el mejor modelo para todo», es la primera optimización de costos de cualquier sistema multi-agente, y por sí sola suele reducir la factura a la mitad.

### La instrucción del revisor: una lección de evaluación

El prompt del rol `reviewer` incluye una línea que merece explicación: «Reporta TODOS los hallazgos [...] un filtro posterior decidirá». Los modelos recientes siguen las instrucciones de severidad con tanta literalidad que un prompt del tipo «reporta solo problemas graves» deprime la cobertura: el modelo encuentra el defecto y decide no reportarlo por no parecerle suficientemente grave. La práctica robusta es separar **detección** (exhaustiva, con confianza declarada) de **filtrado** (un paso posterior, humano o automático). Es el mismo principio de los sistemas de detección clásicos: nunca mezclar el sensor con el umbral.

## El prompt maestro: DRY aplicado a las instrucciones

Si observa los cuatro prompts de sistema del ejemplo 5.1, verá repetición estructural: todos definen un rol, un alcance, unas reglas y un formato de salida. Esa estructura repetida es una *plantilla* pidiendo a gritos ser extraída, el principio DRY del Código Limpio Sintético (capítulo 4). Llamamos **prompt maestro** a esa plantilla versionada de la que derivan todos los prompts de rol de la organización:

```python
# Ejemplo 5.2: Prompt maestro — una sola estructura, muchos roles.
# La plantilla se versiona en el repositorio (prompts/master_v3.md) y
# cada rol es un conjunto de parámetros, no un texto artesanal.

MASTER_PROMPT = """Eres {rol}, parte de un equipo de agentes especializados.

ALCANCE — tu única responsabilidad:
{alcance}

REGLAS — en orden de prioridad; ante conflicto, gana la primera:
{reglas}

FUERA DE ALCANCE — si la tarea cae aquí, decláralo y detente:
{fuera_de_alcance}

FORMATO DE SALIDA — exactamente esto, sin texto adicional:
{formato_salida}
"""

ROL_REVIEWER = {
    "rol": "un tech lead experto en code review",
    "alcance": "evaluar código en correctitud, seguridad (OWASP Top 10), "
               "mantenibilidad (SOLID, DDD) y performance",
    "reglas": "1. Reporta TODOS los hallazgos con confianza declarada.\n"
              "2. Cita la línea exacta de cada hallazgo.\n"
              "3. No propongas refactorings fuera del diff revisado.",
    "fuera_de_alcance": "decidir si el PR se aprueba (lo decide un humano); "
                        "modificar el código",
    "formato_salida": 'JSON: {"hallazgos": [{"linea": int, "dimension": str, '
                      '"severidad": str, "confianza": float, "detalle": str}]}',
}

def system_prompt(rol_config: dict) -> str:
    return MASTER_PROMPT.format(**rol_config)
```

La anatomía (rol, alcance, reglas priorizadas, fuera de alcance, formato) no es arbitraria: cada bloque neutraliza un modo de fallo conocido. El **alcance** combate la deriva de responsabilidad (la god class agéntica); las **reglas priorizadas** resuelven los conflictos de instrucciones que los modelos, ante ambigüedad, resuelven de forma impredecible; el **fuera de alcance** explícito es la diferencia entre un agente que escala lo que no le corresponde y uno que improvisa; y el **formato de salida** convierte la integración con el siguiente eslabón en un contrato verificable (capítulo 3 (Vol. 4)). Los beneficios operativos son los de siempre con DRY: una mejora en la plantilla se propaga a todos los roles, un eval de regresión cubre la estructura común, y el diff de un *pull request* sobre `prompts/` muestra exactamente qué cambió en el comportamiento del sistema.

> **Nota editorial: alcance del caso de estudio.** El caso que sigue es un escenario compuesto, construido para ilustrar el proceso de refactorización rol por rol, no una auditoría de una empresa real ni un estudio longitudinal. La sección "Estado del Arte" de este volumen documenta que no existe todavía perspectiva longitudinal publicada sobre sistemas agénticos en producción a varios años.

## Caso de estudio: refactorizar un agente monolítico a Empresa Sintética

*(Caso compuesto ilustrativo: condensa un patrón de refactorización recurrente; las cifras indican orden de magnitud.)*

**Situación inicial.** Un equipo construyó «Dev-Bot»: un único agente con un prompt de sistema de 4.000 palabras que planifica, codifica, revisa su propio código y escribe la documentación. En la demo funcionaba; tres meses después, el equipo observa: tasa de código aceptado a la primera en torno al 40 %, costo por funcionalidad errático (el CIU del capítulo 1 (Vol. 4) oscila 10×), y cada ajuste del prompt para arreglar un comportamiento rompe otro: el síntoma inequívoco de una god class [Martin, 2009](#ref-martin2009), solo que escrita en prosa.

**El refactoring, en cuatro pasos disciplinados** (comportamiento verificado con evals antes y después de cada paso, como manda Fowler, 2018):

1. **Caracterización.** Antes de tocar nada, el equipo construye una suite de 40 evals con casos reales de los últimos tres meses (capítulo 3 (Vol. 4)). Es el equivalente de los *characterization tests*: sin ellos, «refactorizar» un prompt es adivinar.
2. **Extracción del primer rol.** El revisor se separa a un agente propio con el prompt maestro anterior. Hallazgo típico: el monolito «se aprobaba a sí mismo», el sesgo de autocomplacencia que el patrón evaluador-generador del capítulo 8 existe para romper. La tasa de defectos detectados sube de inmediato.
3. **Extracción del planificador y contratos JSON.** El plan deja de ser un párrafo libre y pasa a ser una lista de tareas con criterios de aceptación (formato de salida del prompt maestro). El codificador recibe tareas acotadas; el contexto por llamada baja, y con él, el costo y el efecto *lost in the middle* [Liu et al., 2024](#ref-liu2024).
4. **Asignación de modelo por rol.** Planificador en el modelo premium; codificador en el balanceado; barrido de seguridad en el económico (ejemplo 5.1). El CIU se estabiliza y cae en torno al 40 % respecto al monolito.

**Resultado.** Mismo proveedor, mismos modelos, ninguna técnica exótica: solo SRP, DRY, contratos y tests aplicados a prosa. La lección del caso es la tesis del capítulo: la calidad de un sistema multi-agente es, ante todo, una propiedad de su *diseño organizacional*, no del modelo de turno.

## Ejercicio resuelto 5.1: diseñe el pipeline de triaje de tickets

**Enunciado.** Una empresa recibe 500 tickets de soporte diarios. Diseñe una Empresa Sintética mínima que clasifique cada ticket (facturación/técnico/ventas), extraiga los datos estructurados y redacte un borrador de respuesta que un humano aprueba. Asigne modelo por rol y justifique.

**Solución comentada.** Tres roles bastan; la tentación de añadir un cuarto «coordinador» viola el árbol de decisión del capítulo 8 (los pasos son conocidos: es un *pipeline*, no necesita orquestador razonante):

| Rol | Tarea | Modelo | Justificación |
|---|---|---|---|
| Clasificador | Categoría + urgencia + idioma | Económico (`claude-haiku-4-5`) | Clasificación cerrada de texto corto: la gama económica rinde igual aquí; a 500/día, la diferencia de precio financia el resto del pipeline |
| Extractor | JSON con cliente, producto, problema | Económico, con salida estructurada | Extracción contra esquema: verificable en el nivel 1 de la pirámide de testing |
| Redactor | Borrador de respuesta con tono de marca | Balanceado (`claude-sonnet-4-6`) | Único rol donde la calidad de prosa importa; recibe SOLO el JSON del extractor, no el ticket crudo: menos tokens y menos inyección indirecta (capítulo 4 (Vol. 4)) |

Los detalles que separan la solución profesional de la ingenua: (1) el redactor consume el JSON del extractor, contrato explícito, contexto mínimo; (2) el humano aprueba el borrador, el sistema «falla barato» (capítulo 5 (Vol. 4)); (3) los tres prompts derivan del prompt maestro; y (4) el lote nocturno de tickets no urgentes va por la API batch a mitad de precio (capítulo 1 (Vol. 4)). Costo estimado del pipeline completo: calcúlelo con el apéndice B: es un ejercicio dentro del ejercicio, y la respuesta sorprende por lo baja.

## Lo esencial del capítulo 5

- Especialización vence a generalismo, con evidencia: ChatDev, MetaGPT y AutoGen ([Qian et al., 2024](#ref-qian2024); [Hong et al., 2024](#ref-hong2024); [Wu et al., 2024](#ref-wu2024)).
- La Ley de Conway (1968) ahora se diseña: organización y sistema son el mismo artefacto.
- Modelo por rol = primera optimización de costos; suele recortar la factura a la mitad.
- Detección separada de filtrado en los revisores: el sensor nunca decide el umbral.
- El prompt maestro (rol, alcance, reglas priorizadas, fuera de alcance, formato) es DRY aplicado a instrucciones: una plantilla versionada, muchos roles parametrizados.

**■ PISTA EJECUTIVA**

La Empresa Sintética no elimina la organización humana: la *refleja y la amplifica*. Cada equipo humano pasa de ejecutar tareas a gobernar una célula de agentes que las ejecuta. Las preguntas de diseño organizacional que esto abre (¿quién es responsable cuando el agente falla?, ¿cómo se mide a un ingeniero que orquesta?) se desarrollan en los capítulos 19 y 20. El dato para la decisión de hoy: el patrón de roles especializados no es una preferencia estética; es el patrón con mejor evidencia publicada de reducción de errores en cascada [Hong et al., 2024](#ref-hong2024) y mejora de factualidad [Du et al., 2023](#ref-du2023), y su costo adicional es cuantificable y gobernable.

---
