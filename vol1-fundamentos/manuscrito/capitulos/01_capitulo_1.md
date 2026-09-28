# Capítulo 1: El despertar agéntico

## La transición del desarrollador tradicional al orquestador de agentes

Durante cuatro décadas, la productividad de un desarrollador de software se midió en líneas de código por hora, tickets cerrados por sprint y *pull requests* integrados por semana. Era una métrica industrial aplicada a un trabajo intelectual, y funcionaba a duras penas: la velocidad de producción de código tenía un tope físico, el de la escritura humana.

Esa limitación desapareció.

La secuencia es reconstruible con precisión a partir de la literatura. En 2017, la arquitectura Transformer estableció el sustrato técnico de todo lo que vino después [Vaswani et al., 2017](#ref-vaswani2017). En 2020, los modelos de lenguaje de gran escala demostraron que podían realizar tareas nuevas a partir de unos pocos ejemplos en el contexto, sin reentrenamiento [Brown et al., 2020](#ref-brown2020). En 2021, un modelo especializado resolvió problemas de programación descritos en lenguaje natural con una tasa de éxito que sorprendió a sus propios autores, quienes acompañaron el resultado con una discusión explícita de sus riesgos [Chen et al., 2021](#ref-chen2021). En 2022, el ajuste con retroalimentación humana convirtió esos modelos en asistentes capaces de seguir instrucciones [Ouyang et al., 2022](#ref-ouyang2022), y se documentó que ciertas capacidades (aritmética en varios pasos, razonamiento encadenado) emergen de forma abrupta con la escala [Wei, Tay, et al., 2022](#ref-wei2022).

En 2023 llegó la síntesis decisiva: los modelos aprendieron a *actuar*. Aprendieron a alternar razonamiento con uso de herramientas externas ([Yao, Zhao, et al., 2023](#ref-yaoreact2023); [Schick et al., 2023](#ref-schick2023)) y a poblar entornos simulados con comportamientos sociales creíbles [Park et al., 2023](#ref-park2023). Entre 2023 y 2024, los marcos multi-agente demostraron que varios modelos coordinados superan a uno solo en tareas de ingeniería de software ([Qian et al., 2024](#ref-qian2024); [Hong et al., 2024](#ref-hong2024); [Wu et al., 2024](#ref-wu2024)). Y hacia 2025–2026, los primeros sistemas multi-agente con supervisión humana intermitente alcanzaron entornos de producción empresarial; los proveedores empezaron a publicar guías de arquitectura específicas para construirlos [Anthropic, 2024](#ref-anthropic2024).

El desarrollador cuya única ventaja competitiva es escribir sintaxis correcta enfrenta hoy la situación del operador de telégrafo ante la conmutación automática: su destreza no desapareció, pero dejó de ser el cuello de botella que justificaba su precio. La historia de la ingeniería es, en buena parte, la historia de profesiones que ascendieron en la cadena de abstracción o quedaron fuera de ella.

**► PISTA TÉCNICA**

## Qué es, formalmente, un agente

La teoría de agentes autónomos es muy anterior a los LLMs. La *Distributed Artificial Intelligence* (DAI) establece que un sistema es inteligente en proporción a la calidad de las interacciones entre sus componentes, no a la capacidad de cada componente aislado ([Ferber, 1999](#ref-ferber1999)). La definición clásica de Wooldridge (2009) describe al agente como una entidad computacional situada en un entorno, capaz de acción autónoma para alcanzar sus objetivos de diseño. Un agente, en el sentido técnico formal:

- **Percibe** su entorno a través de sensores. En los agentes LLM: el contexto de la conversación, los mensajes del usuario, los resultados de las herramientas que invoca.
- **Razona** sobre ese entorno usando un modelo interno del mundo. En los agentes LLM: el conocimiento paramétrico del modelo más el contexto inyectado.
- **Actúa** sobre el entorno mediante efectores. En los agentes LLM: llamadas a funciones, herramientas, APIs, sistemas de archivos.
- **Aprende** de los resultados para refinar su comportamiento futuro. En los agentes LLM actuales, este aprendizaje ocurre *dentro de la sesión* (vía contexto y memoria externa), no en los pesos del modelo.

![Diagrama 1.1: Ciclo de un agente autónomo](imagenes/capitulo01/diagrama1_1_es.png)

Esta definición tiene una consecuencia práctica inmediata: **un chatbot no es un agente**. Un chatbot percibe y razona, pero no actúa sobre el mundo ni cierra el ciclo observando las consecuencias de sus acciones. La frontera entre ambos no es el modelo subyacente, que puede ser el mismo, sino la arquitectura que lo rodea. Anthropic (2024) propone una distinción operativa que adoptaremos en todo el libro: los **flujos de trabajo** (*workflows*) son sistemas donde el código del desarrollador orquesta los pasos y el LLM ejecuta tareas dentro de un guion predefinido; los **agentes** son sistemas donde el propio modelo decide dinámicamente su trayectoria: qué herramienta usar, cuándo iterar, cuándo detenerse. La misma fuente ofrece el consejo de ingeniería más valioso y menos seguido del campo: empiece por el patrón más simple que resuelva el problema, y escale a agente solo cuando la tarea lo justifique.

### Reactivo y proactivo: las dos mitades de la agencia

La teoría clásica descompone la agencia en dos propiedades en tensión [Wooldridge, 2009](#ref-wooldridge2009). Un agente es **reactivo** cuando percibe los cambios de su entorno y responde a ellos a tiempo: el bug que aparece, el test que se rompe, el mensaje del usuario que corrige el rumbo. Y es **proactivo** cuando no se limita a responder, sino que toma la iniciativa dirigida por un objetivo: descompone la meta, planifica y persigue el plan aunque nadie lo empuje en cada paso. La distinción no es nueva ni exclusiva de los LLMs: refleja la frontera entre los *agentes de reflejo simple* y los *agentes basados en objetivos* de la teoría clásica [Russell & Norvig, 2020](#ref-russellnorvig2020).

La tensión es real y define el diseño. Un agente **puramente reactivo**, de estímulo y respuesta, sin objetivo propio, nunca emprende nada por sí mismo: es rápido y robusto, pero no resuelve una tarea de varios pasos. Un agente **puramente proactivo**, que ejecuta su plan sin volver a mirar el mundo, actúa sobre un entorno que ya cambió y persigue, ciego, un objetivo que dejó de tener sentido. La buena ingeniería agéntica vive en el equilibrio, y ese equilibrio ya tiene nombre: es lo que el patrón ReAct (capítulo 4) hace explícito al **intercalar** observación (la mitad reactiva) y razonamiento dirigido a la meta (la mitad proactiva), ciclo a ciclo. Un agente que solo reacciona es un disparador glorificado; uno que solo planifica es un guion que ignora la realidad. El agente útil alterna las dos mitades bajo un presupuesto. Conviene no confundir esta *reactividad del agente* con la *reactividad de los sistemas* (backpressure, flujos, Mono/Flux), que gobierna la infraestructura sobre la que el agente corre: son ideas distintas con el mismo nombre, y la segunda se trata en el capítulo 7 (Vol. 4).

La frontera viva de la industria empuja justamente hacia la mitad proactiva. Lo que en 2024–2025 los equipos de Silicon Valley empezaron a llamar **agentes ambientales** (*ambient agents*) no es una categoría nueva de agente. Son sistemas que corren en segundo plano, se disparan con eventos en lugar de con un *prompt*, y solo reclaman al humano cuando detectan algo que merece su atención [Chase, 2025](#ref-chase2025): el agente proactivo llevado a su consecuencia operativa, montado sobre la arquitectura orientada a eventos del capítulo 7 (Vol. 4). La promesa es seductora («guarda tu atención para cuando de verdad importe»), y por eso exige el escrutinio más frío: cada grado de proactividad que el sistema gana es un grado de control que el humano cede, y con él, más superficie de riesgo [Mitchell et al., 2025](#ref-mitchell2025). El capítulo 2 (Vol. 3) retoma esta frontera no como una promesa de marketing, sino como un problema de ingeniería con su propio criterio de diseño, y como el terreno donde los agentes dejan de asistir y empiezan a anticipar.

### El espectro de autonomía

Conviene pensar la agencia como un espectro y no como una categoría binaria:

| Nivel | Sistema | Quién decide el flujo | Ejemplo |
|---|---|---|---|
| 0 | Llamada única | El desarrollador | Clasificar un correo |
| 1 | Cadena (*workflow*) | El desarrollador | Pipeline extracción → validación → resumen |
| 2 | Enrutador | El modelo elige entre rutas fijas | Triaje de tickets a especialistas |
| 3 | Agente con herramientas | El modelo, dentro de un presupuesto | Depurar un test que falla |
| 4 | Sistema multi-agente | Un orquestador + agentes especializados | Desarrollar una funcionalidad completa |

Cada nivel hacia abajo en la tabla aumenta la capacidad y, simultáneamente, la varianza del comportamiento, el costo por tarea y la superficie de fallo. La tesis económica de esta obra (que desarrollaremos en el Vol. 4, al medir el costo por iteración útil) es que el nivel correcto es el **mínimo** que resuelve el problema, no el máximo que la tecnología permite.

**■ PISTA EJECUTIVA**

Para un director de ingeniería, la transición agéntica tiene una traducción directa al estado de resultados: el costo marginal de *escribir* una unidad de software ha colapsado, pero se ha desplazado hacia la *validación y el gobierno* de lo escrito. La evidencia cuantitativa disponible es consistente: la asistencia de IA acelera de forma medible la tarea de programar ([Peng et al., 2023](#ref-peng2023); [Ziegler et al., 2024](#ref-ziegler2024)), pero los benchmarks de tareas reales muestran el límite con la misma claridad: cuando se evaluó a los mejores modelos de 2023–2024 sobre incidencias reales de GitHub, resolvían sin ayuda solo una fracción pequeña de ellas [Jimenez et al., 2024](#ref-jimenez2024). La brecha entre «escribe código plausible» y «resuelve problemas de producción de extremo a extremo» es el espacio donde su organización gana o pierde dinero.

El error estratégico más común del período 2025–2026 es optimizar la primera dimensión (contratar menos desarrolladores porque «la IA escribe el código») mientras se ignora la segunda (quién valida que el código es correcto, seguro y alineado con el negocio). Las organizaciones que ganan en la era agéntica no son las que eliminan ingenieros: son las que **reentrenan a sus ingenieros para gobernar agentes**.

Tres preguntas para su próximo comité de dirección:

1. ¿Sabemos cuánto gastamos hoy, al mes, en tokens de modelos de lenguaje, y quién lo gasta? (Si la respuesta es no, el capítulo 1 (Vol. 4) es para usted.)
2. ¿Qué porcentaje del código generado por IA llega a producción sin retrabajo humano? (Si nadie lo mide, la cifra de productividad que le reportan es una ilusión.)
3. ¿Tenemos un plan de formación para convertir ingenieros senior en orquestadores de agentes, o asumimos que ocurrirá solo? (El capítulo 2 propone uno.)

## Ejercicio resuelto 1.1: ubique cada sistema en el espectro de autonomía

**Enunciado.** Clasifique estos cuatro sistemas en el espectro de autonomía (niveles 0 a 4) y justifique: (a) un servicio que resume cada ticket entrante en una línea; (b) un asistente que, ante un bug reportado, busca en el código, reproduce el fallo y propone un parche; (c) un flujo que extrae datos de facturas, los valida contra reglas y los carga al ERP; (d) un sistema donde un coordinador reparte una migración entre agentes de análisis, conversión y prueba.

**Solución comentada.** (a) **Nivel 0**: una llamada por ticket, sin decisiones de flujo; cualquier nivel superior sería costo sin retorno. (b) **Nivel 3**: el modelo decide qué archivos leer, cuándo ejecutar tests y cuándo detenerse; exige presupuesto de iteraciones y herramientas de solo lectura más una de propuesta de parche, nunca de escritura directa. (c) **Nivel 1**: los pasos son fijos y conocidos; la tentación común es llamarlo «agente» en la presentación interna, pero es un *workflow*, y esa precisión importa: se presupuesta, se prueba y se gobierna distinto. (d) **Nivel 4**: descomposición dinámica multi-dominio; solo se justifica si (b) ya opera bien, porque hereda todos sus requisitos y añade coordinación. La lección transversal: el nivel se elige por la **estructura de la tarea**, no por la ambición del equipo.

## Lo esencial del capítulo 1

- La secuencia 2017–2026 es reconstruible con literatura: Transformer → few-shot → código → instrucciones → herramientas → multi-agente ([Vaswani et al., 2017](#ref-vaswani2017); [Brown et al., 2020](#ref-brown2020); [Chen et al., 2021](#ref-chen2021); [Ouyang et al., 2022](#ref-ouyang2022); [Yao, Zhao, et al., 2023](#ref-yaoreact2023)).
- Un agente percibe, razona, actúa y aprende [Wooldridge, 2009](#ref-wooldridge2009); un chatbot no actúa: la diferencia es la arquitectura, no el modelo.
- La agencia es reactiva (responde a tiempo a los cambios) y proactiva (toma la iniciativa hacia un objetivo); ReAct equilibra ambas intercalando observación y razonamiento ([Wooldridge, 2009](#ref-wooldridge2009); [Russell & Norvig, 2020](#ref-russellnorvig2020)).
- Workflows (el código decide) vs. agentes (el modelo decide): empiece por el patrón más simple que resuelva el problema [Anthropic, 2024a](#ref-anthropic2024).
- El nivel de autonomía correcto es el mínimo que resuelve la tarea; cada nivel añade varianza, costo y superficie de fallo.
- El costo se desplazó de escribir a validar: las organizaciones ganadoras reentrenan ingenieros para gobernar agentes.

---
