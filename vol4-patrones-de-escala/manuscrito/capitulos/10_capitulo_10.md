# Capítulo 10: La evolución de las arquitecturas: del contexto al enjambre

---

## Sección 1: La Línea del Tiempo: Cómo Llegamos Aquí

Entre 2017 y el hoy, la industria de la IA vivió una transición tan profunda que corre el riesgo de parecer trivial, como si fuera un simple cambio de herramientas. No es así. Lo que ocurrió fue una reorientación fundamental de *dónde vive la inteligencia* en una arquitectura de software.

Vaswani et al. (2017) publicaron "Attention is All You Need", el paper que redefinió cómo las máquinas procesan lenguaje. Los Transformers no eran simplemente más veloces; eran arquitecturalmente distintos: podían procesar secuencias en paralelo, no en serie, lo que abrió la puerta a modelos que crecían exponencialmente en capacidad. Dos años después, GPT-2 demostró que esa capacidad traducía en comprensión del lenguaje natural a escala nunca vista. La industria del software observaba, incrédula, cómo una red neuronal podía escribir código, explicar conceptos técnicos y generar narrativas coherentes.

Ahora bien, algo faltaba. Los modelos de 2023 sabían mucho, pero no sabían nada del ahora. Entrenados en datos congelados en el tiempo (abril 2023 para GPT-3.5, abril 2024 para GPT-4), un modelo de lenguaje era como un jurista que leyó todos los libros de leyes hace diez años: experto en principios, ciego frente a las nuevas regulaciones. Entonces surgió RAG (Retrieval-Augmented Generation): la idea de conectar el modelo a un repositorio de información externa, actualizable en tiempo real. Si el modelo era el jurista, RAG era el jurista con internet y una biblioteca de precedentes al lado.

Paralelamente (y esto es determinante para entender qué viene después) los sistemas de software en producción enfrentaban un dilema que RAG no resolvía. Cuando un modelo genera un análisis, un resumen o una explicación, está leyendo. Cuando debe decidir, escribir, ejecutar una acción o coordinar con otros servicios, RAG se queda corto. Era el síntoma de un problema arquitectónico más profundo: hemos construido máquinas que comprenden, pero no hemos diseñado aún cómo las hacemos *actuar* sin romper todos nuestros sistemas.

La respuesta llegó en capas, cada una resolviendo lo que la anterior dejaba sin responder.

**2024 trae MCP (Model Context Protocol)** ([Anthropic, Cline, 2024](#ref-clineanthropic2024)): una abstracción limpia que deja que el modelo acceda a herramientas (APIs, bases de datos, sistemas de archivos) de forma segura, sin hardcodear ningún detalle dentro del prompt. Donde RAG era lectura, MCP era lectura *y* escritura bajo guardianes. Un modelo con MCP puede decir "quiero saber el estado del proyecto en Jira", el protocolo traduce eso en una llamada autenticada y deja que el modelo siga su razonamiento. Crucial: el modelo nunca maneja credenciales ni entiende la topología del sistema; solo entiende qué pueden hacer las herramientas y cómo pedirlas.

Pero MCP seguía siendo reactivo. El modelo respondía a una entrada, accedía a herramientas, devolvía un resultado. Los primeros agentes (frameworks como ReAct, LangChain, Autogen) añadieron la pieza que faltaba: **el ciclo**. El agente no genera una respuesta y termina; genera un paso, lo evalúa, decide si necesita más información o más acciones, y repite. Es la diferencia entre "un modelo que responde preguntas" y "una máquina que resuelve problemas".

Lo que ocurre en 2025 es donde la historia se vuelve incómoda. Cuando agentes individuales funcionan, el siguiente paso natural es escalable: ¿qué pasa si en lugar de un agente resolver un ticket, tenemos cinco agentes especializados atacando partes distintas del mismo problema? ¿Qué pasa si el agente A publica un evento, el agente B lo ve y actúa en consecuencia, y el agente C valida el resultado? Ahí emergen las orquestaciones: pipelines donde múltiples agentes colaboran, se comunican por eventos (el capítulo 7 que ya viste, Kafka como sistema nervioso, pero escalado), y producen resultados que ninguno de ellos podría generar solo.

En los sistemas multiagentes opera la emergencia, no la coordinación programada. Sistemas donde decenas de agentes especializados interactúan bajo reglas simples y los patrones de colaboración emergen. Las ciudades inteligentes, los mercados financieros de trading de alta frecuencia, las cadenas de suministro adaptativas: todos operan bajo este principio. El software deja de ser un artefacto estático que respondemos y se convierte en un organismo que anticipa, aprende y se reconfigura.

| Año | Evento | Qué Cambió | Por Qué Importa |
|-----|--------|-----------|-----------------|
| 2017 | Transformers (Vaswani et al.) | Arquitectura base para LLMs | Paralelismo, escala exponencial de capacidad |
| 2019 | GPT-2 (escala de parámetros) | Comprensión del lenguaje natural a escala | La IA deja de ser clasificación; es generación |
| 2023 | RAG emergente | Conexión modelo ↔ datos externos | Supera límite de fecha de corte; información actualizable |
| 2023-2024 | Prompt injection, adversarial attacks | Crisis de seguridad | Los modelos solos son peligrosos si pueden actuar sin control |
| 2024 | MCP (Model Context Protocol) | Acceso seguro a herramientas/APIs | Guardianes de permisos; modelo nunca maneja credenciales |
| 2024 | Frameworks de agentes (ReAct, LangChain) | Ciclo cerrado: reflexión + acción + evaluación | Modelos que resuelven, no solo responden |
| 2024-2025 | BigData + vectores = Memory at Scale | Recuperación masiva de contexto histórico | Agentes con memoria corporativa de años, no minutos |
| 2023-2024 | NVIDIA NIM (Inference Microservices) | Inferencia optimizada, cloud-native, APIs estándar | Latencia predecible, escalabilidad, compliance on-prem |
| 2024-2025 | NVIDIA NIM Operator (Kubernetes) | Orquestación declarativa de pipelines multi-servicio | Auto-escalado por GPU metrics, rolling upgrades sin downtime, GitOps-friendly |
| 2025 | Orquestaciones (Kafka + Agentes) | Múltiples agentes coordinados por eventos | Desacoplamiento temporal; escalabilidad a cientos de agentes |
| 2025-2026 | Sistemas multiagentes | Emergencia sin programación explícita | Adaptabilidad, anticipación, aprendizaje colectivo |
| 2027+ | Sistemas urbanos adaptativos, AI plataformas | Gobernanza de ciudades y economías digitales | IA como infraestructura crítica, no herramienta |

---

## Sección 2: RAG: El Punto de Inflexión

Para el ejecutivo que encarga sistemas de IA, RAG es simple: **es llevar un modelo de lenguaje a datos que actualmente no conoce**. La metáfora es tan común que se vuelve invisible: un jurista (el modelo) con internet (el retriever) y una biblioteca (la base de vectores) al lado. Correcto, pero insuficiente para entender por qué RAG llegó a ser el patrón dominante y, al mismo tiempo, por qué era apenas el principio.

Repasemos qué ocurría antes. GPT-3.5 fue entrenado en datos hasta abril de 2023. Si en mayo de 2023 tu empresa lanzaba un producto nuevo, el modelo no lo conocía. Si tu equipo legal publicaba una política interna el jueves, el modelo seguía ignorándola el viernes. El entrenamiento ocurría en ciclos de meses, a costo descomunal ([Anthropic, 2024](#ref-anthropic2024); [Kaplan et al., 2020](#ref-kaplan2020)), y cada paso de aprendizaje requería recompilar cientos de miles de parámetros. Era como estar condenado a reescribir toda tu filosofía cada vez que aprendías una canción nueva.

RAG trastocó eso. En lugar de entrenar, *recuperas*. Antes de que el modelo genere su respuesta, consultas una base de datos (tradicional o vectorial; cap. 11 profundizó en por qué los vectores) y le entregas fragmentos contextuales relevantes en su prompt de sistema. El modelo ve contexto fresco, produce una respuesta más precisa, y lo hace en milisegundos, sin reentrenamiento, sin esperar ciclos de batch. Para un ejecutivo: RAG significa **"mis sistemas de IA nunca están desactualizados"**.

Pero aquí llega la complicación. RAG resuelve el problema de *acceso a datos*; no resuelve el problema de *verdad*. Cuando construyes una base de vectores desde documentos corporativos, heredes sus sesgos, sus omisiones, sus contradicciones. Si tu documentación dice que la política A aplica a clientes en Perú y la documentación de Cumplimiento dice que no, RAG recupera ambas y el modelo genera una respuesta que contiene las dos verdades contradictorias. El problema es ahora visible (es progreso) pero sigue siendo un problema. Esto propulsa la necesidad del capítulo 13: evaluadores (LLM-judges, evals deterministas) que verifiquen que la salida del modelo es coherente con las políticas de la empresa, no solo con el promedio de internet.

La carga de mantenimiento de RAG es también infravalorada. Una base de vectores no es "set and forget". Cambia la terminología corporativa, el modelo empieza a recuperar fragmentos con vocabulario desfasado. Se publican nuevas políticas, hay que reembeber (reextraract vectores) desde cero. A escala de BigData (donde "millones de documentos" es la norma, no la excepción), esto demanda infraestructura. Pipelines que detecten cambios en los repositorios fuente, ETLs que actualicen los vectores, evaluadores que verifiquen coherencia. El patrón de "construye un RAG rápido" desmorona cuando observas que, en realidad, estás construyendo un **pipeline de datos continuo con costos de operación indefinida**.

Entonces, ¿cuándo es RAG la respuesta correcta? No siempre. Algunos casos de uso:

**RAG es tu herramienta cuando:**
- Tienes datos corporativos frecuentemente actualizados (documentación de producto, regulaciones, base de conocimiento de soporte).
- La precisión mejora materialmente con contexto reciente (vs. contexto de entrenamiento del modelo).
- Puedes mantener la calidad de los fragmentos recuperados (metadata limpia, sin duplicación, sin contradicciones).
- La latencia de recuperación (consulta vectorial + lectura de BD) cabe en tu presupuesto de tiempo de respuesta.

**RAG es un costo oculto cuando:**
- Usas RAG para "mejorar un modelo débil" en lugar de usar un modelo más capaz. (El capítulo 3 mostró: a veces, Opus cuesta lo mismo que Haiku + RAG.)
- Recuperas cientos de fragmentos en paralelo porque "más contexto es mejor contexto". (No lo es. Dilución. Cap. 11 lo cuantifica.)
- Tu fuente de datos cambia tan rápido que los vectores envejecen más rápido de lo que los reembebes.

El giro que ocurre en 2024-2025, y que conecta RAG con lo que viene después, es este: **RAG asume que el modelo solo necesita leer**. Pero en la mayoría de los sistemas de IA en producción, el modelo también necesita escribir, ejecutar acciones, validar decisiones. Ah está el acoplamiento. Un modelo que dice "necesito ver la especificación del proyecto en Jira" (lectura, RAG lo resuelve) es distinto de un modelo que dice "necesito actualizar el estado del proyecto en Jira a 'en revisión', pero solo si dos miembros del equipo lo aprobaron primero" (lectura + escritura + decisión + validación). Para esto, RAG ya no es suficiente.

| Caso de Uso | Necesidad Primaria | Herramienta | Por Qué | Costo Estimado |
|-------------|------------------|-----------|--------|----------------|
| "¿Cuándo se lanza el producto X?" | Lectura de datos actualizado | RAG | Modelo + retriever, sin ciclos de acción | Bajo (contexto + inferencia) |
| "Genera un resumen de los últimos PRs" | Lectura + síntesis | RAG | El modelo integra multiples fuentes | Bajo-Medio (volumen de contexto) |
| "Crea un ticket en Jira con estos datos" | Lectura + escritura + API auth | MCP | Guardianes de permisos; modelo no maneja credenciales | Bajo (1-2 llamadas) |
| "¿Es seguro deployar? Si no, alerta al oncall" | Lectura + decisión + acción secundaria | MCP + Evaluador | MCP para acceso seguro; evaluador para validar decisión | Bajo-Medio (decisión binaria) |
| "Cierra todos los tickets de un cliente que churnó" | Lectura + decisión + múltiples escrituras | Agente (ciclo) | Itera: recupera tickets, valida estado, ejecuta, verifica | Medio (iteraciones desconocidas a priori) |
| "Orquesta 5 agentes para procesar una solicitud de auditoría" | Coordinación + escalabilidad | Orquestación (Kafka + Agentes) | Eventos desacoplan a los agentes; cada uno es independiente | Medio-Alto (volumen de eventos) |
| "Que 50 agentes de risk management detecten fraude en paralelo" | Emergencia + anticipación | Multiagentes (sin coreografía) | Reglas locales + comunicación = patrones emergentes | Alto (complejidad + observabilidad) |
| "Procesa 500K embeddings diarios, <100ms latencia, compliance on-prem" | Escalabilidad + control | NVIDIA NIM on-premises | APIs estándar, hardware optimizado, no egreso de datos | Medio (operación + H100s) |
| NIM Pipeline: embed + rerank + LLM, auto-escala P99 | Orquestación declarativa | NIM Operator en K8s | NIMService + NIMPipeline CRDs; HPA por métricas GPU | Medio-Alto (K8s + GPU) |

---

## Sección 3: De MCP a Orquestaciones: La Capa de Coordinación

Cuando preguntabas a un modelo si era seguro deployar cierto código, RAG te daba contexto: "Aquí están los últimos commits, el historial de issues, la documentación." Generaba un análisis. Punto. Ahora, si el modelo dice "No es seguro; necesito que alguien revise los cambios en AWS", ¿qué ocurre? El modelo termina su generación y tú, manualmente, creas un ticket de soporte. RAG no contempla acciones.

MCP ([Anthropic, 2024](#ref-anthropic2024)) resuelve eso con una idea deceptivamente simple: **dadle al modelo herramientas, pero sin que maneje ni credenciales ni topología del sistema**. En lugar de:

```
Modelo → ["Quiero leer archivos", "Quiero escribir en BD"]  
         ↓ (Modelo obtiene credenciales)  
         Caos de seguridad
```

Ocurre:

```
Modelo → ["Quiero invocar `get_aws_compliance_status`"]  
         ↓ (Servidor traduce a llamada autenticada)  
         Modelo ve respuesta, prosigue razonamiento
```

El protocolo no es magia; es disciplina. El modelo declara qué necesita hacer, el servidor valida permisos, ejecuta bajo guardianes (rate limits, auditabilidad), devuelve resultado. Es el patrón hexagonal del capítulo 6, escalado. Este cambio ocurrió en paralelo con LangGraph ([LangChain, 2024](#ref-langchain2024)), que formalizó cómo orquestar agentes con estado: no solo llamadas aisladas, sino máquinas de estado dirigidas por decisiones del modelo.

Aquí viene lo que está acalorando a Silicon Valley. En 2025, la pregunta dejó de ser "¿cómo hago que un agente resuelva un ticket?" para convertirse en "¿cómo coordino 50 agentes en paralelo resolviendo distintos aspectos del mismo ticket?". Manning Publications publicó "AI Agents in Action" (2025), que captura el patrón emergente: agentes especializados, cada uno con un rol (recuperación de contexto, validación, ejecución, auditoría), comunicándose por eventos. No por RPC. Por eventos.

Aquí entra Kafka (que ya viste en el capítulo 7, pero ahora escala). Un agente genera un evento ("Ticket 4521 clasificado como HIGH PRIORITY"). Otro agente subscrito a ese evento actúa ("Verificar si hay precedentes de tickets similares en el último mes"). Un tercero publica un resultado ("Se encontraron 3 precedentes; recomendación es escalar a nivel 2"). El cuarto, un evaluador, valida coherencia ("¿El escalado es consistente con las políticas de SLA?"). Ninguno espera a ninguno. El sistema es desacoplado temporalmente. A escala de mensajes, BigData deja de ser "millones de registros en una BD" para convertirse en "millones de eventos en un stream", y los agentes leen historia, toman decisiones, publican eventos nuevos.

El costo de esto, a nivel USA, lo ve claramente Anthropic (2025): **usar múltiples agentes coordinados consume 15 veces más tokens que un agente único haciendo lo mismo**. Pero la varianza disminuye 80%. Es decir: pagas más dinero, ganas previsibilidad y escalabilidad. Para sistemas financieros (JPMorgan está experimentando con IA agéntica en el trading; [Bloomberg lo reporta en enero 2025](#ref-bloomberg2025)), esa tradeoff es aceptable. Para un startup que procesa 10 tickets/día, es prohibitivo.

Las orquestaciones, entonces, no son "más agentes = mejor solución". Son decisiones de escala. Cuándo la complejidad de un problema requiere división de trabajo, y cuándo esa división justifica los tokens (y la latencia) adicionales.

---

## Sección 4: Sistemas Multiagentes y el Horizonte Disruptivo

Cuando múltiples agentes colaboran bajo un esquema de orquestación, ocurre algo extraño: patrones emergen sin estar programados.

Considera un sistema de trading de alta frecuencia basado en agentes. Diez agentes especializados:
- Agente A: Recupera noticias financieras en tiempo real
- Agente B: Analiza impacto regulatorio
- Agente C: Valida señales técnicas en gráficos
- Agentes D-G: Ejecutores (buy/sell órdenes con límites de capital y risk)
- Agente H: Monitor de correlación (detecta si múltiples agentes están apostando lo mismo)
- Agente I: Auditor (registra cada transacción, flags si hay anomalías)
- Agente J: Aprendiz (actualiza modelos de decisión basado en outcomes históricos)

Ninguno tiene instrucción explícita "coordina con los otros". Sin embargo, cuando A publica un evento ("nueva regulación sobre cryptos"), B lo ve, ejecuta análisis, publica evento. C ve el análisis de B, valida contra gráficos, publica confianza. D ve los eventos de B y C, suma información, decide compra. H ve que D está apostando fuerte, verifica correlación con otros traders (agentes), alerta si hay concentración de riesgo. J registra el resultado de la decisión de D: ¿funcionó? ¿Por qué? 

**Esto es emergencia**: el comportamiento colectivo no es la suma de comportamientos individuales. Es un producto de las interacciones locales bajo reglas simples.

DeepSeek (empresa de investigación en IA, China) publicó en 2024 arquitecturas MoE (Mixture of Experts) que encapsulan exactamente esto: en lugar de un modelo monolítico, múltiples expertos (pequeños transformers especializados) se activan de forma selectiva según la entrada. Es multiagentes *dentro del modelo*. La industria occidental está replicando el patrón: Anthropic publica sobre "constitutional AI at scale" (aplicar valores corporativos en sistemas distribuidos); OpenAI experimenta con razonamiento profundo (o1-mini, diciembre 2024) donde el modelo reserva "tokens de pensamiento" para reflexión interna antes de generar. Es el patrón de agentes que reflexionan antes de actuar.

Las ciudades inteligentes son el canvas más visible de esto. Singapur (proyecto "Smart Nation", desde 2014, ahora con IA agéntica en 2025) opera con agentes especializados para tráfico, energía, residuos, salud pública. No hay "controlador central"; cada subsistema es un equipo de agentes que se comunica por API y eventos. Una fuga de gas se detecta (sensor → agente de monitoreo → evento), el evento dispara alertas de salud (agentes sanitarios), ajustes de flujo de aire (agentes HVAC), y notificación a vecinos (agentes de comunicación). Todo sin intervención humana, bajo reglas. Es multiagentes aplicado a infraestructura urbana.

Lo que está de moda en USA no es tanto multiagentes (concepto viejo; Sharon Goldwater, Bonabeau, los años 90) sino **multiagentes con evaluación y adaptación integradas**. Guardrails AI (startup 2023, bien financiada) ofrece frameworks donde cada agente tiene guardianes locales (no confundamos con el patrón 16: guardianes en el anillo exterior, aquí guardianes en cada agente). Anthropic publica sobre "evaluación en bucle cerrado": el agente decide, el evaluador valida, el evaluador retroalimenta al agente, el agente actualiza su estrategia de decisión. Es RL (reinforcement learning) distribuido sin necesidad de reentrenamiento central.

Aquí el costo disruptivo: un sistema multiagente con 50 agentes, cada uno con evaluador integrado, en un día procesa millones de eventos, millones de inferencias. La factura de tokens es orden de magnitud superior a cualquier cosa que haya visto antes. Bloomberg, JPMorgan, Palantir: todos están optimizando "costo de IA agéntica a escala". La respuesta emergente es usar modelos pequeños (Haiku, Sonnet) como agentes individuales, reservar modelos grandes (Opus, o1) solo para decisiones críticas. Es la tiering del capítulo 3, escalada a orquestaciones.

Adaptadores de modelos (patrón arquitectónico, 2025): porque cambiar de Sonnet a Opus en producción sin reescribir es crítico, algunos equipos construyen "adaptadores de modelos", essencialmente puertos que abstraen qué LLM ejecuta cada agente. Es el patrón hexagonal, pero aplicado a la selección de modelos en tiempo de ejecución. Esto está experimentándose en equipos de Stripe, Anthropic internamente, y startups de fintech.

La conclusión: los sistemas multiagentes no son futuros. Están operando hoy en finanzas, logística, ciudades. Lo disruptivo es hacer que sean económicamente viables (reducir tokens sin perder calidad) y auditables (cada decisión rastreable). Los próximos 18 meses definirán si la industria logra ambos.

---

## Sección 5: Usar Modelos como Experto: Ecosistema, Arquitectura y Computación Cuántica

Hasta aquí hemos tratado los agentes, las orquestaciones, la evaluación. Hay un nivel anterior que determina todo lo demás: **cómo usas el modelo mismo**. No es trivial. La diferencia entre un equipo que gasta $100,000/mes en llamadas a APIs y un equipo que obtiene 10× mejor resultado gastando $10,000 es arquitectura.

Cuando un ingeniero llama a `claude.messages.create()` dentro de un loop, está usando el modelo como utilidad: entrada → salida → fin. Es correcto para prototipos. Inaceptable en producción. A escala, debes tratar el modelo como un **componente arquitectónico que vive en un ecosistema**, donde decisiones sobre batching, caching, routing y adaptación de capacidades no son "optimizaciones opcionales"; son la frontera entre viabilidad económica e insolvencia.

**Ecosistema de Modelos: Batching, Caching, Routing**

Comencemos por los invisibles. Cuando tu agente publica un evento ("Necesito analizar 5,000 invoices para compliance"), una arquitectura ingenua hace 5,000 llamadas secuenciales a la API. Esperas 2 horas. Pagas $150. Una arquitectura madura hace batching: agrupa los 5,000 invoices, los envía en un único request (o pocos requests en paralelo), espera 30 minutos, paga $45. La diferencia: el modelo procesa el lote en caché de contexto, no en 5,000 inferencias aisladas.

Anthropic publicó en enero 2025 su prompt caching: tu sistema guarda el prompt maestro ("eres un revisor de compliance, aquí están las 500 políticas relevantes") una sola vez. Las siguientes 999 llamadas reutilizan ese prompt, pagando 90% menos por esos tokens. Es transparente para el usuario (la API maneja). Profundo para quien diseña: ahora tu agente de compliance cuesta 1/10 si diseñas el batching.

El routing es igualmente crítico. ¿Todos los problemas requieren Opus? No. Una pregunta FAQ: Haiku. Una decisión de fusión: Opus. Un análisis de código que cabe en 100K tokens: Sonnet con prompt caching. Si tu orquestación inteligentemente rutea cada tarea al modelo correcto (basado en complejidad, costo, latencia requerida), tu costo operativo se divide por tres. El patrón: **Model Adapter** no es cosmética. Es el puerto donde vive la decisión de enrutamiento.

**NVIDIA NIM: Microservicios Optimizados para Inferencia a Escala**

Ahora bien, una vez que has diseñado el batching, el caching y el routing, el siguiente desafío es **dónde hospedas** esa lógica. Las API directas a Anthropic, OpenAI o Google funcionan para prototipos. Para producción a escala (cientos de millones de inferencias, latencia <100ms, disponibilidad 99.99%), necesitas infraestructura. Aquí entra NVIDIA NIM (NVIDIA Inference Microservices), lanzado en 2023-2024.

**¿Qué es NIM?** Una plataforma cloud-native que empaqueta modelos de IA optimizados (no solo LLMs; también visión, audio, embedding) con infraestructura de despliegue listo para producción. El valor no está en "correr un modelo"; está en "correr un modelo a escala sin optimizar infraestructura tú mismo".

Los componentes clave:

1. **Inference engines optimizados por hardware:** NIM no llama a una API remota. Hospedas contenedores en tu infraestructura (cloud público, on-premises, edge). NVIDIA maneja la optimización: cuantización automática (FP8, INT8 para modelos sin pérdida, velocidad +2-3×), compilación específica para GPU (NVIDIA H100, H200, L40, RTX 6000), kernel kernels optimizados. Para un modelo que en CPU toma 500ms/inferencia, NVIDIA NIM en GPU optimizado toma 50ms.

2. **APIs estándar por dominio:** Lugar de que cada modelo tenga su propia API, NIM expone interfaces estandarizadas. LLM chat endpoint sigue OpenAI spec. Embedding endpoint sigue formato estándar. Visión sigue OpenAI Vision API. Developer que conoce una API, conoce todas. Cambiar de modelo (digamos, de Llama 405B a Mistral 8×22B) requiere cambiar una variable de configuración, no reescribir código cliente.

3. **Despliegue flexible:** Alojamiento en la nube (mediante NVIDIA API Catalog, que es managed). On-premises (descargás contenedor, lo corres en tu cluster de GPUs, tú lo mantienes). Hybrid: parte crítica corre en tu DC, fallback a cloud si tu infrastructure cae.

4. **Soporte empresarial:** SLAs, actualizaciones de seguridad, corrección de errores. Para equipos de 50+ ingenieros usando IA en producción, el costo del soporte se amortiza rápidamente en "tiempo no gastado debuggueando CUDA".

**Cómo entra NIM en tu ecosistema de modelos:**

Supongamos que tu orquestación que vimos antes (batching, caching, routing) vive en Kubernetes. Antes, cada decisión de routing era "¿llamamos a Anthropic API o Azure OpenAI?" Ahora es:

```
Tarea "clasificación de documento"
  ↓ (Router)
  ¿Complejidad baja (FAQ)? → Haiku en NIM local (on-prem, <50ms latency)
  ¿Complejidad media? → Sonnet en NIM cloud-managed (NVIDIA API Catalog, <200ms)
  ¿Complejidad alta? → Opus en API Anthropic directo (confiabilidad máxima, latencia aceptada)
```

El beneficio: **latencia predecible**. RAG local cuesta 50ms retrieval + 100ms LLM (vía API remota) = 150ms en caída promedio. Con NIM local, retrieval 50ms + Haiku en GPU 30ms = 80ms. Para un sistema que procesa 1,000 documentos/hora, eso es 1.4 minutos de ahorro de latencia acumulada por hora. A escala de datacenter, es significativo.

**Cuándo NIM es tu herramienta:**
- Inferencia >100K/día. En ese nivel, la infraestructura propia se paga.
- Latencia <100ms es crítico (trading, diagnóstico médico, control de robots).
- Compliance: modelos sensibles nunca deben salir de tu red (healthcare HIPAA, finanzas PCI-DSS).
- Mezcla de modelos abiertos + cerrados. NIM hospeda open-source (Llama, Mistral, Code Llama) y, vía integración, acceso a modelos proprietarios.

**NIM en RTX PCs: El Puente Desarrollo → Producción (2024)**

Hay un uso intermedio de NIM que merece mención: **desarrollo local en workstations RTX**. 

Los equipos de ingeniería con pipelines RAG complejos enfrentan este dilema: desarrollar contra APIs remotas (Anthropic, OpenAI) es costoso durante experimentación (1,000 iteraciones = miles en bills). Pero descargar Llama 70B localmente requiere A100s ($16K/GPU).

NIM en RTX PCs (serie 50, Blackwell) cierra esa brecha. Con Podman en WSL2, un ingeniero en una workstation (RTX 6000 Ada, ~$7K) ejecuta:

```bash
podman pull nvcr.io/nim/meta/llama-70b-instruct
podman run --gpus all -p 8000:8000 nvcr.io/nim/meta/llama-70b-instruct
```

Resultado: servidor OpenAI-compatible en localhost:8000. Zero API calls. Integra con LangChain, CrewAI, FlowiseAI, VS Code AI Toolkit: misma interfaz que usará en producción con NIM en Kubernetes.

**Por qué importa:**
- Desarrollo offline (sin internet, vuelos, entornos sensibles)
- Cost: $0 por iteración (vs. $1-10 por call API durante experimentación)
- Unified experience: código que corre localmente corre igual en K8s producción
- Testing RAG pipelines: embedding + reranking + LLM locales, mismo día de escritura

**El patrón:**
1. Ingeniero escribe pipeline RAG contra NIM local en su RTX PC
2. Tests llegan al 95% de precisión
3. Commit a main
4. CI/CD deploya a NIM Operator en K8s (100 líneas de YAML)
5. Zero code changes. Solo infraestructura cambia.

Esto es **escalabilidad horizontal sin refactor**. Y es posible gracias a que NIM expone interfaces estándar (OpenAI spec) en ambos contextos.

**Cuándo NIM no es tu herramienta:**
- <10K inferencias/día. Overhead de operación (monitoreo, actualizaciones, disaster recovery) no se amortiza.
- Latencia flexible (reporte batch que se ejecuta overnight es OK).
- Single model, single use case. La simplicidad de "lanzo una API y olvido" supera el ahorro de latencia.
- Infraestructura legacy sin Kubernetes (pero nota: RTX local sigue siendo viable incluso sin K8s)

**Tabla de costos: API Directo vs. NIM Local vs. NIM K8s**

| Escenario | Herramienta | Costo Inicial | Costo/Inf. | Latencia | Ideal Para |
|-----------|-------------|---------------|------------|----------|-----------|
| Prototipado (≤100 inf/día) | Claude API Directo | $0 | $0.003–0.02 | 500ms+ | Startups, MVP rápido |
| Desarrollo (1K–10K inf/día) | NIM local en RTX PC | $7K (GPU) | $0 | 50–100ms | Equipos de ingeniería |
| MVP producción (10K–100K) | NIM en NVIDIA API Catalog | $0–500 (créditos) | $0.001–0.005 | 100–200ms | Startups con SLA moderado |
| Empresarial (100K–1M inf/día) | NIM Operator en K8s · on-prem | $50K–200K (GPUs) | $0.0001–0.001 | 30–50ms | Finanzas, healthcare |
| Máxima (>1M inf/día) | Multi-región NIM + DGX Cloud | $200K+ | $0.00001–0.0005 | 10–30ms | JPMorgan, Stripe-scale |

**NIM es la respuesta a "¿cómo monetizo escalabilidad en inferencia?"** Para equipos que ya tienen batching, caching, routing en lugar, NIM es el "dónde", la capa de hospedaje que hace todo eso viable a escala sin comprometer latencia o compliance.

**NIM Operator: Orquestación Declarativa de Inferencia en Kubernetes (2024-2025)**

El siguiente punto es determinante. Hemos hablado de batching, caching, routing, y NIM como infraestructura. Pero ¿cómo orquestan equipos de 50+ ingenieros no 1 sino 10 servicios de NIM simultáneamente? ¿Cómo hacen rolling upgrades sin downtime? ¿Cómo auto-escalan basado no solo en CPU sino en métricas de inferencia (KVCache, cola de requests)?

La respuesta es **NIM Operator** ([NVIDIA, 2024](#ref-nvidia2024)): una extensión Kubernetes que trata pipelines completos de inferencia como ciudadanos de primer orden. 

El patrón es declarativo, GitOps-friendly:

```yaml
apiVersion: apps.nvidia.com/v1alpha1
kind: NIMPipeline
metadata:
  name: rag-pipeline-prod
spec:
  services:
    - name: embedding-service
      model: nvidia/NV-Embed-QA-004
      replicas: 3
      resources:
        gpu: 1
    - name: llm-service
      model: meta/llama-70b-instruct
      replicas: 2
      resources:
        gpu: 4
    - name: reranker-service
      model: nvidia/nv-rerank-qa-mixedbread-v1
      replicas: 2
      resources:
        gpu: 1
  autoscaling:
    metrics:
      - type: GPU_MEMORY
        target: 80
      - type: QUEUE_LENGTH
        target: 500
      - type: REQUEST_LATENCY_P99
        target: 500ms
```

Esto no es YAML por YAML. Es arquitectura. Qué ocurre bajo el capó:

1. **NIMService CRD** (Custom Resource Definition): Cada servicio individual (embedding, LLM, reranking) es un NIMService. Lifecycle management, health checks, rolling upgrades.

2. **NIMPipeline CRD**: Orquesta múltiples NIMServices como una unidad coherente. Una RAG pipeline de verdad: cuando llega una query, el embedding-service procesa, pasa resultado a reranker-service, éste valida relevancia, luego pasa al llm-service. Todo declarado una vez, orquestado por Kubernetes automáticamente.

3. **Auto-escalado inteligente**: No es CPU. Es **métricas de inferencia**:
   - KVCache utilization (cuánta memoria tiene usado la ventana de contexto del modelo)
   - Queue length (cuántos requests esperan)
   - P99 latency (¿estamos violando SLA?)
   
   Si KVCache sube a 85%, agrega pod. Si latency P99 baja a <200ms, reduce. Todo dinámico.

4. **Pre-cacheo de modelos**: El operador distribuye modelos grandes (Llama 70B = 140GB) a persistent volumes en los nodos. Cuando un pod nuevo se crea, no descarga 140GB de internet; lo monta local. Escalado 10× más rápido.

5. **Rolling upgrades sin downtime**: Cambiar de Llama 70B a Llama 405B? En el YAML cambias el `model:` field. El operador:
   - Crea pods nuevos con el modelo nuevo
   - Drena requests de los pods viejos (con timeout)
   - Mata los viejos
   - Zero downtime, completamente automático

Esto es **Capítulo 6** (hexagonal, guardianes) escalado. Pero en lugar de guardianes en el anillo exterior, son **guardianes en infraestructura**. El modelo no sabe que está siendo auto-escalado, reemplazado, o monitoreado. El operador lo maneja.

El costo: un NIMPipeline con 3 servicios, auto-escalado a 10 pods, procesa 100K requests/día. Tú defines SLA (P99 <500ms, GPU memory <80%). El cluster se autoadapta. No necesitas oncall revisando utilización a las 3am.

¿Dónde entra esto en tu orquestación de agentes? Precisamente aquí: si cada agente especializado (recuperación, análisis, validación, ejecución) corre como un NIMService dentro de un NIMPipeline, tu orquestación de 50 agentes no es caos. Es un YAML, versionado en Git, auditado, reproducible.

**Conclusión arquitectónica**: Kubernetes sin NIM Operator requiere escribir controllers personalizados (meses de trabajo). NIM Operator es el atajoversus that generalizes el patrón. Es lo que Kafka fue a Zookeeper: abstracción que simplifica lo inmanejable.

**Fine-tuning vs. Contexto: La Decisión que Importa**

Ahora toca una decisión arquitectónica que paraliza a los equipos. Tienes datos internos (10 millones de ejemplos de tickets resueltos). ¿Fine-tuneas un modelo, o construyes RAG?

Fine-tuning cuesta: $5,000-$50,000 en tokens, 1-2 semanas de turnaround, requiere mantener versiones del modelo (si tus políticas cambian, ¿reentrenarás?). El dividendo: el modelo "entiende" tu dominio; pregunta específica, respuesta matizada.

RAG cuesta: $500-$2,000 en infraestructura, reembed cada vez que tus datos cambian (automático si el pipeline es bueno), zero wait time.

**La respuesta correcta es contextual, no binaria.** MIT CSAIL ([Grupo de Learning and Intelligent Systems, 2025](#ref-lis2025)) publicó un marco: fine-tuning es óptimo cuando (a) tienes >10M ejemplos de alta calidad, (b) el patrón es estable (cambia <5% anualmente), (c) latencia es crítica (necesitas <100ms, RAG agrega 50ms de retrieval). Para la mayoría de casos corporativos, RAG gana. Pero hay una tercera vía que Stanford está explorando (lab de Perdomo-Ortiz en Google Quantum AI, 2024-2025): **knowledge distillation en tiempo de ejecución**. Tienes un modelo grande (Opus) que "sabe" tu dominio. Destila continuamente ese conocimiento en un modelo más pequeño (Haiku), que se actualiza sin reentrenamiento explícito. El resultado: Haiku con conocimiento Opus, costo Haiku.

**Arquitectura de Modelos: Capas de IA vs. Infraestructura Tradicional**

Aquí viene el giro. Los equipos construyen sistemas donde "el modelo es un servicio más", como la BD, como Kafka. Correcto en abstracto; peligroso en concreto. Un modelo no es una BD. No garantiza consistencia, no tiene ACID, no es determinista. Inyectarlo en arquitecturas tradiciones sin capas de aislamiento = deuda técnica.

La respuesta: **capas de IA como infraestructura de primer orden**. Harvard ([Grupo de Systems Security, 2025](#ref-syssec2025)) ha documentado patrones: la capa de IA no habita donde la lógica de negocio crítica. Habita en una frontera (como en Capítulo 6, el anillo exterior). Entre esa capa de IA y el núcleo, van evaluadores, validadores, guardianes. El modelo genera; el evaluador valida; si falla, el sistema degrada gracefully (vuelve a un comportamiento conocido, no cae).

En orquestaciones, esto se intensifica. Cincuenta agentes, cada uno llamando modelos, cada uno posiblemente alucinando. Sin capas de aislamiento explícitas, una alucinación en un agente propaga como incendio (otras agentes leen su evento, lo asumen correcto, construyen sobre él). Con capas: cada evento publicado por un agente tiene un sello de "confidence" y "audited flag". Los agentes consumidores pueden decidir "confío en este evento solo si fue auditado."

**Computación Cuántica: De la Teoría a la Producción (2025-2030)**

Ahora el futuro próximo. En 2024-2025, computación cuántica y IA agéntica parecen mundos distintos. No lo son. Hay una intersección específica que importa, y está más cerca de lo que parece.

**Primero, esclarecimiento teórico.** La computación cuántica aprovecha los principios de la mecánica cuántica para realizar cálculos complejos que son imposibles para computadoras clásicas. En lugar de bits (0 o 1), usa cúbits que pueden existir en superposición de ambos estados simultáneamente. Esta propiedad, junto con entrelazamiento cuántico, permite explorar espacios de soluciones exponencialmente más rápido. Pero aquí el mito: "quantum va a ejecutar prompts directamente". Incorrecto. Es que ciertos problemas que los agentes resuelven (optimización combinatoria, muestreo probabilístico, búsqueda en bases masivas) tienen ventajas potenciales si accedes a hardware cuántico.

**La historia acelerada.** Richard Feynman reconoció el potencial en 1981. David Deutsch presentó la computadora cuántica universal en 1985. Peter Shor desarrolló su algoritmo en 1994 (factorización eficiente, amenaza real a criptografía). En 2001, D-Wave lanza la primera computadora cuántica comercial. En 2019, Google anuncia "supremacía cuántica" (Sycamore completó un cálculo específico más rápido que cualquier supercomputadora). En 2024, Google Willow reclama qubits lógicos con tasas de error <1%, un salto desde ~10% hace dos años. IBM Quantum publicó estrategias de mitigación de errores que hacen viable usar ~100 qubits para problemas reales.

**Casos reales operacionales hoy (2024-2025):**

**Google** usa computación cuántica para desarrollar nuevos materiales para baterías (potencial: aumentar significativamente capacidad de almacenamiento de energía). El algoritmo explora el espacio de configuraciones moleculares de forma exponencialmente más rápida que heurísticas clásicas.

**IBM**, en colaboración con BASF, usa computación cuántica para diseñar nuevos catalizadores que podrían transformar la industria química. En junio 2023, IBM y Samsung anunciaron una colaboración para desarrollar computadoras cuánticas de próxima generación. El roadmap de IBM apunta a 100,000 qubits en un computador cuántico-céntrico para 2033 (ambición explícita).

**JPMorgan Chase** desarrolla nuevos algoritmos para optimización de carteras de inversión. El problema: con 1,000 activos, hay 2^1000 permutaciones. Un solver clásico toma meses; un solver cuántico podría hacerlo en horas.

**Volkswagen** optimiza sus rutas de transporte (VRP: Vehicle Routing Problem). Tienen cientos de puntos de entrega. Quantum routing reduce costos y mejora eficiencia.

**Pfizer** usa computación cuántica para descubrimiento de nuevos medicamentos (simulación molecular para acelerar desarrollo de tratamientos).

**Goldman Sachs** desarrolla nuevos modelos de riesgo (quantum advantage en evaluación de carteras).

**Maersk** optimiza planificación de cadenas de suministro (problema combinatorio masivo; quantum reduce tiempos de entrega).

**Novartis** desarrolla modelos de diagnóstico más precisos (simulación molecular, pattern recognition).

Estos no son proyectos piloto. Son operaciones reales (muchas con publicaciones verificables). Lo que falta: scaling (pasar de 100 qubits lógicos a 10,000), estabilidad (mantener coherencia más tiempo), y educación en equipos de ingeniería.

**Dónde entra tu agente en contacto con quantum (Escenarios Reales)**

1. **Optimización combinatoria a escala:** Tu agente observa: "Este es un problema de routing con 500+ puntos." Puerta arquitectónica: ¿Existe solver cuántico disponible? SÍ → Delega a Amazon Braket (timeout: 2 minutos). NO → Fallback a heurística clásica (timeout: 30 minutos). Resultado se ingiere al agente; sigue razonamiento.

2. **Muestreo probabilístico:** Tu modelo generativo necesita escenarios posibles para evaluación de riesgo (finanzas). Un muestreador cuántico genera escenarios que cubren el espacio de probabilidad uniformemente. Papers de Harvard ([Aspuru-Guzik lab, 2024](#ref-aspuru2024)) y Rigetti muestran esto funcional con ~500 qubits. Aún no en producción general, pero prototipada en labs de fintech.

3. **Búsqueda en bases vectoriales masivas:** Tu agente recupera de 10 millones de vectores el más similar a la query. El algoritmo de Grover (cuántica teórica, 1996) ofrece √N aceleración. Para 10M vectores, eso es 100× en teoría. En práctica, overheads reducen a ~3-5×. IonQ está prototipando esto con empresas de fintech (2025).

**Pioneros y Liderazgo Académico**

Los fundadores teóricos siguen activos. **Isaac Chuang (MIT)**, considerado uno de los padres fundadores de la computación cuántica, realiza contribuciones fundamentales en desarrollo de algoritmos cuánticos y corrección de errores. **John Preskill (Caltech)**, físico teórico, realiza importantes contribuciones a la comprensión de los fundamentos. **Scott Aaronson (Universidad de Texas en Austin)**, teórico de computación cuántica, ha clarificado los límites de qué es posible vs. imposible en quantum. **Hartmut Häfele y su grupo (Google AI)** avanzan en arquitecturas de hardware.

Pero hay un movimiento emergente: **Alejandro Perdomo-Ortiz**, ahora en Google Quantum AI (antes Stanford), lidera investigación en quantum machine learning aplicado a problemas reales. Su grupo publica regularmente sobre quantum-classical hybrids.

En Latinoamérica emerge talento. **Fernando Pastawski (Argentina, 40 años)**, físico teórico en CONICET, trabaja en algoritmos cuánticos para simulación de sistemas complejos. **Cecilia Vergara (México, 37 años)**, ingeniera en LNCC Brasil, desarrolla hardware cuántico (diseño y construcción de qubits superconductores). **Felipe Carillo (Colombia, 35 años)**, matemático en IMEC Brasil, contribuye en teoría de complejidad de algoritmos cuánticos. **Mariana Weiss (Brasil, 32 años)**, física en IFSC, estudia fundamentals (decoherencia cuántica). **Diego Ortiz (Chile, 29 años)**, ingeniero en Universidad de Chile, desarrolla software para programación de computadoras cuánticas.

**En Perú**, la escena es emergente pero prometedora. **Pontificia Universidad Católica del Perú (PUCP)** ofrece cursos introductorios. El **Grupo de Investigación en Física Computacional de PUCP**, dirigido por Dr. Jorge Luis Peralta, muestra interés explícito en computación cuántica. **Universidad Nacional de Ingeniería (UNI)** integra quantum en currículo. **Universidad Norbert Wiener** cuenta con docentes que han realizado estudios relacionados. Esta infraestructura formativa resulta estratégica: la próxima década demandará ingenieros con formación combinada en computación cuántica, IA y arquitecturas agénticas.

**Realidad Operacional 2026: Quantum no es "silver bullet"**

Amazon Braket ofrece acceso híbrido (clásico + cuántico en el mismo job). Tu agente puede correr lógica clásica, detectar que necesita optimización combinatoria, delegarla a un solver cuántico vía Braket, resumir con lógica clásica. Microsoft Azure Quantum hace similar. Esto es arquitectura híbrida, y existe hoy.

¿Pero por qué no todos lo usan? **Costo, latencia variable, y falta de benchmarks fiables.** Un problema de routing en Braket cuesta ~$10-50 USD por invocación (dependiendo de complexity). Una heurística clásica cuesta $0.01. Quantum es 1,000× más caro. Vale la pena solo si: (a) solución clásica toma horas y quantum toma minutos (ganancia >10×), O (b) necesitas calidad de solución que clásico NO alcanza (pharma, materiales).

El costo de error cuántico sigue siendo alto. Google Willow alcanzó <1% error en qubits lógicos (monumental). Pero para un cálculo que requiere 10,000 puertas cuánticas, incluso 0.1% error por puerta se magnifica. NISQ (Noisy Intermediate-Scale Quantum) era el término de 2019-2024; ahora es "post-NISQ" pero sin garantía de productividad.

**La brújula arquitectónica correcta:**

El modelo maestro es graceful degradation. No construyes sistemas que **dependen** de quantum. Construyes sistemas que **se aceleran con** quantum si está disponible. Es como Redis en arquitecturas clásicas: si está ahí, úsalo; si no, la lógica sigue funcionando. Así es quantum: complemento, no revolución.

**Horizonte Realista 2026-2030**

El consenso académico internacional (Stanford, MIT, Caltech, plus universidades latinoamericanas emergentes):

- 2026-2027: Quantum operacional en finanzas (portfolio optimization), logística (VRP), farmacia (molecular simulation)
- 2027-2028: Desarrollo de estándares y protocolos cloud-quantum (interoperabilidad between IBM, Google, Microsoft, Amazon)
- 2028-2030: Educación masiva (generación de ingenieros quantum-native emerja de universidades que HOY están instalando labs)
- 2030+: Quantum-AI hybrid como infraestructura crítica (no excepcional)

Perú no está afuera. PUCP, UNI, Norbert Wiener están posicionándose. En 5-10 años, equipos de Silicon Valley pueden estar escalando talento desde Latinoamérica en quantum + IA.

**Conclusión: Usar Modelos como Experto en la Era Quantum-Agentic**

Entonces, ¿cómo integro esto en mi orquestación hoy?

No lo haces completamente. Hoy, 2026, es temprano. Pero diseñas con opción. Architecto para tres capas: (1) Lógica clásica + modelos (la base), (2) Quantum como acelerador selectivo (si está disponible), (3) Evaluadores aislados en frontera (validan todo, confían en nada). Este es el patrón industrial que JPMorgan, Google, Volkswagen, Maersk ya están implementando.

Usar modelos como experto no es sólo "llamar Opus en lugar de Haiku". Es entender:
- El ecosistema (batching, caching, routing)
- La arquitectura (capas de IA aisladas, evaluadores en frontera)
- El horizonte próximo (computación cuántica como acelerador selectivo)
- El talento emergente (Latinoamérica producirá ingenieros quantum-agentic en 3-5 años)

El equipo que domina estos cuatro niveles corre 10× más eficiente y está preparado para lo que viene. Y si eres de Perú, Latinoamérica, o emerging markets: la curva de talento es tu ventaja. No necesitas 20 años de quantum legacy; puedes aprender quantum-native.

---

## Lo esencial del capítulo 10

- **RAG** resuelve acceso a datos actualizado; es lectura pura. Costo oculto: mantenimiento perpetuo.
- **MCP** añade acceso seguro a herramientas. El modelo no maneja credenciales; el protocolo interpone guardianes.
- **Agentes** traen el ciclo cerrado: reflexión + acción + evaluación. Útil cuando no sabes a priori qué pasos son necesarios.
- **Orquestaciones** coordinan múltiples agentes por eventos. Consumo: 15× tokens vs. agente único; varianza: −80%.
- **Multiagentes** produce emergencia: patrones sin programación explícita. Operativo en finanzas, logística, ciudades hoy.
- **Adaptadores de modelos** (2025): abstraer qué LLM ejecuta cada agente para cambiar sin reescribir.
- **NVIDIA NIM**: Microservicios cloud-native para inferencia optimizada. APIs estándar por dominio, latencia predecible, compliance-ready. Rentable en >100K inferencias/día.
- **NVIDIA NIM Operator**: Patrón Kubernetes declarativo (CRDs: NIMService, NIMPipeline) para orquestar multi-service inference. Auto-escalado por métricas de GPU (KVCache, latency P99). Zero-downtime rolling upgrades.
- **Costo crítico**: BigData + evaluadores distribuidos = factura de tokens de orden de magnitud superior. La optimización es el reto 2025-2026.
- La línea de evolución no es "RAG es obsoleto → MCP es obsoleto → Agentes es lo final". Es **acumulativa**: cada nivel resuelve una limitación de lo anterior, coexisten en arquitecturas maduras.
- **Computación cuántica** es acelerador selectivo (3 casos: optimización, muestreo, búsqueda) para 2026-2030, no revolución.
- **Talento latinoamericano** está posicionándose: Perú (PUCP, UNI), Argentina, Brasil, Chile, Colombia emergen en quantum + IA simultáneamente.

---

## Ejercicio Resuelto 10.1: Rediseña tu Sistema (de RAG a Orquestación)

**Enunciado.** Tu equipo opera un RAG para atender tickets de soporte (1,000 tickets/mes). La métrica de éxito es: "ticket cerrado en menos de 2 horas". Hoy, el RAG genera una sugerencia de solución con 78% de precisión. Los tickets que el RAG falla los revisa un humano, que toma 30 minutos. Presupuesto mensual: $2,000 USD.

**Propuesta 1 (Status quo RAG):**
- Costo: ~$450 (inferencia Sonnet) + $500 (infraestructura vectorial) = $950
- Tiempo de ciclo: 5 minutos (modelo) + 30 minutos (humano cuando falla) = 35 min promedio
- SLA: 78% en <2h (cuando el modelo funciona); 22% falla

**Propuesta 2 (Agente + Evaluador):**
- Agente 1: Recupera contexto (MCP → Jira, Slack, docs)
- Agente 2: Genera solución candidata
- Evaluador: Valida coherencia y SLA compliance
- Si falla evaluador, publica evento → humano interviene
- Costo: ~$800 (agentes + evaluador, más tokens de ciclo)
- Tiempo de ciclo: 8 minutos (iteraciones del agente) + 15 minutos (humano, raro)
- SLA: 95% en <2h

**Propuesta 3 (Orquestación ligera):**
- 3 agentes paralelos: (1) Recupera contexto, (2) Analiza patrón de ticket, (3) Genera solución
- Event bus los coordina: cuando los tres publican resultados, un síntesís compone respuesta
- Evaluador valida
- Humano solo interviene si evaluador pita
- Costo: ~$1,200 (3 agentes + síntesis + evaluador)
- Tiempo de ciclo: 6 minutos (paralelo) + 10 minutos (humano, muy raro, <5% de tickets)
- SLA: 98% en <1h

**Tu decisión:**
1. ¿Cuál eliges y por qué? (Pista: no es la más barata.)
2. ¿En qué punto cambiarías de Propuesta 1 a Propuesta 2? ¿Cuál es la métrica clave?
3. Propuesta 3 tiene SLA mejor pero costo 25% más alto. ¿Hay un piso debajo del cual no baja? (Pista: sí, y es el costo de un humano full-time.)

**Solución comentada:**
- La respuesta depende de tu SLA. Si es "cerrado en 2h", Propuesta 1 deja afuera 22% de tickets. Propuesta 2 deja fuera 5%, pero pagás $250 más. Propuesta 3 sale de lo económico solo si tienes >5,000 tickets/mes (ahí la eficiencia paralela amortiza).
- La métrica de cambio: cuando el costo de humanos revisando fallos de RAG (22% × 30 min × salario) supera el costo diferencial de Propuesta 2. En USA, eso ocurre cuando pasás 2,500 tickets/mes.
- El piso: un humano full-time en soporte cuesta ~$5,000-6,000 USD/mes. Si tu orquestación cuesta eso, ya no añade valor económico. La arquitectura debe generar throughput (más tickets/mes) o calidad (menos escaladas humanas) para justificarse.

---

## Ejercicio Resuelto 10.2: Integrar Quantum Hoy (Graceful Degradation)

**Enunciado.** Tu sistema de logística procesa rutas de entrega. Hoy usas simulated annealing (clásico) que toma 30 minutos por ruta óptima y cuesta $0.50. Un solver cuántico en Amazon Braket podría hacerlo en 2 minutos, pero cuesta $40. ¿Cuándo haces el switch?

**Solución:**
El switch no es automático. Necesitas un gate:

```
Si (problema.puntos > 200 AND problema.complejidad > 0.7) {
  Intent: Intenta Braket (timeout: 2 min, presupuesto: $40)
  Si resultado óptimo: úsalo (5× ganancia, $40 se amortiza en urgencia)
  Si timeout: fallback a simulated annealing
} Else {
  Usa simulated annealing (costo: $0.50, tiempo: 30 min)
}
```

El criterio: **quantum solo cuando el problema es lo suficientemente difícil Y el ahorro de tiempo es crítico para SLA**. Para la mayoría de rutas diarias (50-100 puntos), simulated annealing está bien. Para rutas de emergencia (250+ puntos, debe estar resuelta en 30 minutos), quantum paga su prima.

Esto es graceful degradation: quantum es opcional, mejora cuando puede, el sistema sobrevive sin ella.

---
