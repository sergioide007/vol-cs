# Índice de consulta rápida: problema → dónde acudir

_Sección de apoyo. Este volumen es de frontera: sirve para ampliar el mapa, no para resolver un bucle de agente. La tabla distingue los dos usos y evita que el lector busque aquí lo que está en el Vol. 1 o el Vol. 4._

## 1. Si su problema es técnico…

| Si usted necesita… | Acuda a | Nota |
|---|---|---|
| Endurecer un agente frente a ataques | Cap. 1 (OWASP LLM, cuatro superficies, defensa en capas) | Ejercicio resuelto 1.1 |
| Decidir cuánta autonomía conceder y con qué justificación | Cap. 5 (verificabilidad y confianza graduada) | Complementa Vol. 1, cap. 1 |
| Diseñar agentes que reaccionan en lugar de esperar | Cap. 4 (bus de eventos, backpressure, tormentas) | Complementa Vol. 4, cap. 7 |
| Evitar que un enjambre se caiga por bucles de eventos | Cap. 4 (idempotencia, DLQ, límite de saltos) | — |
| Diseñar una arquitectura cloud + edge/on-premise | Cap. 12 (dimensiones de hibridación, costura) | Complementa Vol. 4, cap. 7 |
| Decidir entre añadir funcionalidad o preservar estructura | Cap. 13 (deuda técnica agéntica, curva de inversión) | Complementa Vol. 4, cap. 6 |
| Enseñar un procedimiento a un agente educador | Caps. 8 y 10 (patrón Soporte-Evaluación, salvaguardas) | — |
| Ver qué se está atrofiando en el equipo por delegar | Cap. 6 (extensión frente a dependencia) | — |

## 2. Si su problema es de decisión estratégica…

| Si usted necesita… | Acuda a | Pregunta que responde |
|---|---|---|
| Evaluar dependencia de un proveedor o país | Caps. 17, 22, 23, 24 | ¿Qué variable de mi arquitectura depende de un tercero? |
| Cumplir la regulación más exigente a la que podría enfrentarse | Cap. 19 (AI Act, compliance-by-design) | ¿Diseño una vez para el estándar más duro? |
| Situar su organización en el mapa global de talento y cómputo | Caps. 20, 21, 25, 26, 27 | ¿Dónde está mi ventaja real y dónde mi brecha? |
| Elegir herramientas de IDE y agentes de desarrollo | Caps. 29, 30, 31 | ¿Es decisión de plataforma o de gusto? |
| Medir el impacto de una inversión en agentes | Caps. 26 y 13 | ¿Cuál es mi latencia de feedback y mi deuda? |
| Explicar a un comité por qué la estructura importa más que la velocidad | Cap. 13 | ¿Cuál es el coste de la trampa de la velocidad agéntica? |

## 3. Frontera entre volúmenes

Si lo que busca es **construir** (agentes, herramientas, contexto, orquestación), está en el Vol. 1. Si es **operar y escalar** (coste, testing, DR, métricas, observabilidad), está en el Vol. 4. Si es **organizar y gobernar** (roles, ética, comités, equipos), está en el Vol. 3. Este volumen responde a **dónde está el campo y hacia dónde va**, no a cómo montar el sistema: para eso, use la Guía de lectura y el mapa de prerrequisitos.

## 4. Advertencia de uso

Los capítulos 15 a 32 contienen análisis fechados. Antes de usar cualquiera de sus cifras o comparativas en una decisión, aplique la **Nota sobre vigencia tecnológica** de este volumen: feche el dato, verifique en la fuente primaria y separe la proyección del hecho.