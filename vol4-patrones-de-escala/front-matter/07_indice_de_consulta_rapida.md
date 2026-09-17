# Índice de consulta rápida: problema → dónde acudir

_Sección de apoyo. Este volumen está pensado para consultarse por síntoma: «me cuesta demasiado», «no sé si funciona», «se cayó y no sé por qué», «no sé cuánto tarda esto». La tabla traduce cada síntoma a un capítulo y una sección._

## 1. Por síntoma

| Síntoma o pregunta | Acuda a | Apoyo directo |
|---|---|---|
| «El gasto de tokens subió sin que el valor suba» | Cap. 1 (las cinco causas del Token-Burn; métrica CIU) | Ej. resuelto 1.1 (audite este pipeline) |
| «No sé cuánto tarda una tarea de este tipo» | Cap. 2 (estimación por percentiles) | Ej. resuelto 2.1 (lea los percentiles como un directivo) |
| «El agente funciona en pruebas y falla de forma intermitente» | Cap. 3 (testing no determinista) | Ej. resuelto 3.1 (criterios evaluables) |
| «Me preocupa que un contenido externo manipule al agente» | Cap. 4 (vectores de ataque, cinco principios) | Ej. resuelto 4.1 (anatomía de un ataque indirecto) |
| «Quiero poner un caso de uso en marcha sin jugármela» | Cap. 5 (playbook de casos; empiece por los tres que fallan barato) | Casos 1–3 |
| «Quiero cambiar de modelo sin reescribir el sistema» | Cap. 6 (arquitectura limpia; el modelo es un detalle) | Ej. resuelto 6.1 (violaciones de la regla de dependencia) |
| «Necesito que el sistema reaccione a datos que cambian» | Cap. 7 (event-driven, CDC, backpressure) | Ej. resuelto 7.1 (topics del triaje) |
| «No veo lo que pasa dentro del sistema» | Cap. 8 (señales doradas + señales sintéticas, LLMOps) | Ej. resuelto 8.1 (las alertas del pipeline) |
| «Me piden subir la cobertura y no tengo tiempo» | Cap. 9 (la semana del coverage, paso a paso) | Ej. resuelto 9.1 |
| «No sé qué arquitectura toca: RAG, MCP, orquestación o enjambre» | Cap. 10 (línea del tiempo y degradación elegante) | Ej. resueltos 10.1 y 10.2 |
| «Las métricas clásicas no capturan lo que veo» | Cap. 11 (deriva semántica, bucles, consenso falso) | Ej. resuelto 11.1 |
| «Quiero reducir coste energético o llevarlo al dispositivo» | Cap. 12 (tres palancas, edge, CAPEX/OPEX) | Ej. resuelto 12.1 |
| «Se cayó producción y no sé cómo recuperar la memoria del sistema» | Cap. 13 (DR agéntico, estado cognitivo distribuido) | Protocolos y configuraciones de referencia |
| «Quiero el resumen ejecutivo de todo el libro» | Epílogo de la serie | «Lo esencial del recorrido completo» |

## 2. Índice de ejercicios resueltos del volumen

| Ejercicio | Qué entrena | Capítulo |
|---|---|---|
| Ej. resuelto 1.1 | Auditar un pipeline y calcular su CIU | 1 |
| Ej. resuelto 2.1 | Leer percentiles como un directivo | 2 |
| Ej. resuelto 3.1 | Definir criterios evaluables para un agente | 3 |
| Ej. resuelto 4.1 | Anatomía de un ataque indirecto | 4 |
| Ej. resuelto 6.1 | Detectar violaciones de la regla de dependencia | 6 |
| Ej. resuelto 7.1 | Diseñar los *topics* de un triaje de tickets | 7 |
| Ej. resuelto 8.1 | Definir las alertas del pipeline de revisión | 8 |
| Ej. resuelto 9.1 | Replicar la semana del coverage en dos horas | 9 |
| Ej. resueltos 10.1 y 10.2 | Rediseñar de RAG a orquestación; integrar *quantum* con degradación | 10 |
| Ej. resuelto 11.1 | Detectar deriva semántica antes del comité | 11 |
| Ej. resuelto 12.1 | Estrategia de eficiencia para un enjambre financiero | 12 |

## 3. Frontera con los otros volúmenes

Si su problema es **qué construir y con qué fundamentos**, vaya al Vol. 1. Si es **seguridad, industria o contexto global**, al Vol. 2. Si es **organización, gobierno, roles o ética**, al Vol. 3. Este volumen responde a **cómo operar, medir, defender y recuperar** un sistema ya concebido.

## 4. Advertencia de uso

Todas las cifras de este volumen (precios, ahorros, latencias, costos de infraestructura) deben recalcularse con sus propios datos antes de tomar una decisión. Aplique la **Nota sobre vigencia tecnológica**: el método perdura, la cifra no. Y recuerde la regla del propio libro: degradar en silencio es mentir con infraestructura; citar una cifra caducada como si fuera actual es la misma falta, en forma editorial.