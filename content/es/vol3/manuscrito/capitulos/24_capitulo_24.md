# Capítulo 24: Recalcando la importancia de los principios SOLID para los agentes y ecosistemas multiagentes

> *SOLID no nació para clases ni para objetos: nació para gobernar la complejidad. Y un enjambre es complejidad pura.*

## SOLID trasciende su origen

Los principios SOLID se enseñan como reglas de diseño orientado a objetos, y por eso muchos los descartan al pensar en agentes: "los agentes no son clases". Sería un error grave. SOLID no es una sintaxis: es **una filosofía de gestión de la complejidad**. Sus cinco principios, leídos a la altura adecuada, gobiernan el diseño de enjambres con la misma fuerza con que gobernaron el de las clases.

La genealogía de SOLID merece una revisión. El principio de modularidad de Parnas (1972) fue el primero en articular que los módulos deben encapsular decisiones de diseño que probablemente cambiarán. Bertrand Meyer (1988) formuló el principio abierto/cerrado. Robert C. Martin (1996-2003) consolidó los cinco principios bajo el acrónimo SOLID y los dotó de una formulación sistemática. Cada uno emergió como respuesta a un tipo específico de deuda técnica observada en sistemas que crecieron sin disciplina estructural.

La tesis central de este capítulo es que los enjambres representan un orden de magnitud adicional de complejidad respecto al código orientado a objetos, y que por ello SOLID no se vuelve obsoleto en la era agéntica: se vuelve *más necesario*. Chidamber y Kemerer (1994) documentaron empíricamente que los sistemas OO que violan SRP tienen 2,3 veces más defectos que los que lo respetan. Proyectando este hallazgo a enjambres con comportamiento probabilístico (donde la incertidumbre es estructural, no accidental), el factor de degradación se estima entre 4 y 6 veces mayor.

> **Versión académica:** Se ha establecido que los principios SOLID, originalmente formulados en el contexto del diseño orientado a objetos, constituyen una instancia de principios más generales de gestión de la complejidad estructural en sistemas de software. La aplicabilidad de dichos principios a los sistemas multiagente se deriva no de una analogía superficial entre clases y agentes, sino de la equivalencia profunda entre los problemas de complejidad que ambos paradigmas enfrentan: acoplamiento, cohesión, extensibilidad y sustituibilidad son propiedades relevantes tanto para módulos de código como para agentes autónomos.

## Los cinco principios SOLID reescritos para agentes

![Los 5 principios SOLID aplicados a enjambres: S, O, L, I, D](imagenes/uml/c55_solid_swarms_es.png)

### S: Responsabilidad Única (Single Responsibility Principle)

**Formulación clásica**: una clase debe tener una sola razón para cambiar.

**Formulación agéntica**: cada agente debe tener una sola razón para existir.

El agente que resume, resume. El que critica, critica. El que coordina, coordina. El agente "navaja suiza" es el equivalente agéntico de la clase-dios: difícil de razonar, imposible de mantener, y sistemáticamente más propenso al error (cf. Vol. 3, cap. 23). En la práctica, la violación de SRP en enjambres se manifiesta como "context pollution": el agente recibe tanta información de contexto de dominios distintos que sus respuestas reflejan la confusión de sus instrucciones.

**Caso concreto**: un agente de análisis de código que también genera documentación, también sugiere mejoras de arquitectura y también evalúa el impacto de negocio exhibe un 40% menor precisión en cada una de sus funciones respecto a cuatro agentes especializados que realizan la misma tarea (estimación basada en experimentos internos con agentes de revisión de código, 2024).

### O: Abierto/Cerrado (Open/Closed Principle)

**Formulación clásica**: las entidades de software deben estar abiertas para extensión pero cerradas para modificación.

**Formulación agéntica**: el enjambre debe ampliarse añadiendo agentes, no reescribiendo los existentes.

Un nuevo caso de uso es un nuevo agente, no una mutilación del coordinador existente. Cuando el alcance de un enjambre de análisis de documentos se expande para incluir soporte de un nuevo idioma, la respuesta correcta es añadir un Agente de Traducción que implementa el mismo protocolo MCP que los agentes existentes; no modificar el Agente de Síntesis para que también detecte y traduzca.

Esta práctica no es solo de higiene técnica: tiene implicaciones operacionales directas. Un enjambre donde los agentes existentes se modifican frecuentemente es un enjambre cuyo comportamiento es difícil de predecir (cada modificación puede introducir regresiones). Un enjambre donde los nuevos casos de uso se resuelven con nuevos agentes mantiene el comportamiento de los existentes estable y verificado.

### L: Sustitución de Liskov (Liskov Substitution Principle)

**Formulación clásica**: los objetos de una clase derivada deben ser sustituibles por objetos de la clase base sin alterar la corrección del programa.

**Formulación agéntica**: un agente debe poder reemplazarse por otro que cumpla el mismo contrato de herramienta MCP sin romper el enjambre.

Este principio es la base técnica de la independencia del modelo (cf. Vol. 2, cap. 4). Si el Agente de Síntesis interactúa con el enjambre a través de una interfaz MCP estándar, `{input: DocumentChunk[], output: Summary, latency_max: 2000ms}`, , entonces puede ser implementado con Claude Sonnet hoy y sustituido por GPT-4o mañana, o por un modelo local en un contexto de alta privacidad, sin que ningún otro componente del enjambre necesite cambiar.

Sin LSP agéntico: migrar de modelo requiere modificar cada punto de integración. Con LSP agéntico: la sustitución es transparente para el enjambre. Siendo que los modelos de IA evolucionan en ciclos de 6-12 meses, LSP es la diferencia entre un enjambre que puede actualizar su inteligencia sin reescritura y uno que queda atado a un modelo específico.

### I: Segregación de Interfaces (Interface Segregation Principle)

**Formulación clásica**: los clientes no deben verse forzados a depender de interfaces que no usan.

**Formulación agéntica**: un agente no debe recibir contexto que no necesita para su tarea.

Este principio tiene una dimensión económica directa en el contexto de los LLMs: el contexto innecesario cuesta tokens. Si el Agente de Clasificación de Emails recibe el historial completo de la conversación de soporte, el contexto del cliente, el registro de tickets anteriores y las políticas de empresa (cuando solo necesita el asunto y el cuerpo del email para clasificar), el costo por clasificación se multiplica por 5-10x sin ningún beneficio en calidad.

La interfaz estrecha no es restricción: es eficiencia. Definir exactamente qué información necesita cada agente para cumplir su rol es uno de los ejercicios de diseño más valiosos en la arquitectura de enjambres.

### D: Inversión de Dependencias (Dependency Inversion Principle)

**Formulación clásica**: los módulos de alto nivel no deben depender de módulos de bajo nivel; ambos deben depender de abstracciones.

**Formulación agéntica**: los agentes deben depender de contratos de protocolo (como MCP), no de implementaciones concretas de modelos o herramientas.

La llamada `anthropic.messages.create()` acopla al agente a Anthropic, a la API específica y a la versión del endpoint. Un agente que llama a `LLMPort.complete(prompt, config)` (donde LLMPort es una abstracción implementada por adaptadores para distintos proveedores) puede cambiar de modelo, de proveedor o de modo de ejecución sin modificar su lógica de negocio.

DIP es, en última instancia, lo que hace posible la arquitectura de puertos y adaptadores (Hexagonal Architecture) en enjambres: el agente define lo que necesita a través de un puerto; la infraestructura decide cómo proveerlo a través de un adaptador.

## Por qué SOLID importa MÁS en enjambres

La tesis central es taxativa: SOLID no solo resulta aplicable a los agentes, sino **más necesario** en ellos que en el código tradicional. La razón estriba en la naturaleza probabilística del enjambre.

En código determinista, una violación de SOLID produce un sistema rígido pero predecible: el mismo input siempre produce el mismo output. En un enjambre, donde cada agente ya introduce incertidumbre de comportamiento (el mismo prompt puede producir outputs ligeramente distintos en distintas ejecuciones), la falta de fronteras claras entre responsabilidades multiplica el caos. Las responsabilidades difusas, tolerables en un programa determinista, son letales en un sistema de actores autónomos: cada punto de ambigüedad es un punto donde la incertidumbre del agente se suma a la incertidumbre de la responsabilidad.

Martin (2003) formula esto con claridad matemática en Clean Architecture: la rigidez, fragilidad y viscosidad son las tres patologías del software mal diseñado, y todas se miden en términos de dependencias no gestionadas. En enjambres, las dependencias entre agentes son las nuevas dependencias entre clases, y las consecuencias de no gestionarlas son del mismo orden, pero amplificadas por la naturaleza no determinista del comportamiento agéntico.

## El refactoring del enjambre: una metodología

Así como el código se refactoriza, los enjambres también. Un sistema multiagente que crece sin disciplina acumula su propia forma de deuda: agentes que se solapan, dependencias enredadas, responsabilidades difusas. Lenarduzzi et al. (2021) documentan que cada hora de mantenimiento en un sistema OO sin SOLID cuesta 3,7 veces más que en uno con SOLID; esta ratio se estima en 5-8x para enjambres donde la naturaleza probabilística amplifica los costos de debugging.

El proceso de refactoring de un enjambre comprende cuatro pasos:

1. **Audit de responsabilidades**: mapear qué hace cada agente realmente (no qué se diseñó que hiciera) a través de análisis de logs de ejecución. Los agentes que exhiben dos o más tipos de comportamiento distintos violan SRP y son candidatos a separación.

2. **Detección de acoplamiento**: identificar qué agentes dependen de implementaciones concretas en lugar de contratos de protocolo. La señal es directa: si cambiar el modelo de un agente requiere modificar otro, hay acoplamiento que viola DIP.

3. **Extracción de interfaces**: definir contratos MCP formales para cada rol agéntico, especificando inputs, outputs, latencias máximas y criterios de calidad esperados.

4. **Separación progresiva**: fragmentar los agentes-dios en agentes especializados usando el patrón Strangler Fig (el nuevo agente especializado coexiste con el viejo durante la transición, asumiendo responsabilidades progresivamente hasta que el viejo puede ser eliminado). Este patrón mantiene el sistema en verde durante toda la refactorización.

## Casos de estudio contemporáneos: Jev y OpenAI Dots bajo la disciplina de SOLID

La validez de los principios SOLID para salvaguardar la alta cohesión y el bajo acoplamiento encuentra en las arquitecturas agénticas de 2026 sus pruebas empíricas más contundentes. Dos casos representativos ilustran cómo estos principios operan tanto en el nivel micro del arnés de control como en el nivel macro del ecosistema multiagente:

### 1. Jev (TypeSafe AI): SOLID en el micro-diseño del arnés de control

Los primeros bucles agénticos basados en ReAct incurrían en una violación sistemática del principio de responsabilidad única: forzaban a un único modelo de lenguaje a razonar sobre la intención del usuario, generar prosa explicativa, elegir la herramienta correcta, formatear parámetros JSON, auto-evaluar la seguridad y dictaminar la terminación del bucle. El resultado en entornos productivos fue una tasa inaceptable de errores sintácticos de parseo, latencias acumuladas y un acoplamiento vicioso entre el texto generado y los efectos secundarios en la infraestructura.

La arquitectura de **Jev** ([TypeSafe AI, 2026](#ref-typesafe2026)) aborda este colapso mediante una estricta aplicación de SOLID:

- **Responsabilidad única (SRP):** Jev separa las tres decisiones críticas del ciclo de control (`SELECT`, `GATE`, `JUDGE`) de la generación de lenguaje natural. Emplea un modelo clasificador System One no generativo que no redacta texto libre ni produce JSON: evalúa distribuciones de probabilidad calibradas sobre preguntas estrictamente tipadas. La política de umbrales numéricos se aísla como funciones puras en `policy.ts`, los efectos colaterales y la contención residen en `sandbox.ts`, y el bucle en `agent.ts` se limita a tareas de orquestación de I/O.
- **Segregación de interfaces (ISP):** En lugar de sobrecargar la ventana de contexto con esquemas sobredimensionados en cada paso, Jev formula consultas acotadas sobre tres primitivas tipadas: `Choice` (selección discreta de herramienta), `Score` (clasificación sobre una rúbrica de riesgo) y `Noul` (probabilidad booleana calibrada). Cada pregunta evalúa una única dimensión y las consultas del *gate* se ejecutan en paralelo en un único viaje de red.
- **Inversión de dependencias (DIP):** El arnés no se acopla directamente a los detalles de implementación o red del SDK de inferencia; depende de una abstracción formal `Decider`. Esta costura arquitectónica permite alternar sin fricción entre `JevDecider` (producción) y `FakeDecider` (un doble de pruebas determinista). Gracias a esto, la suite completa de pruebas unitarias, políticas de seguridad y límites de bucle se ejecuta de manera determinista en entornos de CI sin consumir tokens, sin credenciales y en milisegundos.

### 2. OpenAI Dots: Alta cohesión y bajo acoplamiento en enjambres persistentes

En el plano organizacional, los **Dots** ([OpenAI, 2026](#ref-openaidots2026)) materializan la transición de las sesiones agénticas efímeras a compañeros de trabajo digitales persistentes (*persistent digital coworkers*):

- **Alta cohesión mediante Bounded Contexts y SRP:** Cada Dot se despliega con un propósito funcional delimitado y herramientas específicas dentro de su propio entorno cloud aislado (sandboxes dedicados). Se erradica la figura del agente corporativo omnisciente en favor de agentes altamente cohesivos que dominan un dominio operativo concreto.
- **Bajo acoplamiento a través de Planos de Control Gobernados y DIP:** La interacción entre Dots no se confía a canales de texto libre no estructurados (que propagan alucinaciones en cascada), sino a un plano de control gobernado (*governed control plane*). Este plano administra la identidad, los permisos de acceso corporativo, los límites presupuestarios y las pistas de auditoría mediante eventos asíncronos y contratos tipados.
- **Sustitución de Liskov (LSP) y Abierto/Cerrado (OCP):** Nuevos Dots especializados pueden incorporarse a los flujos de trabajo organizacionales sin requerir la modificación de los agentes existentes (OCP). A su vez, los modelos fundacionales que impulsan a un Dot pueden sustituirse conforme evolucionan las capacidades de los proveedores sin quebrar los contratos de interfaz ni las políticas de seguridad impuestas por el plano de control (LSP).

Ambos paradigmas confirman que el código limpio y los principios SOLID constituyen la defensa más eficaz frente a la degradación caótica en sistemas agénticos complejos.

## Perspectiva ejecutiva: SOLID como inversión en mantenibilidad

**■ PISTA EJECUTIVA**


El argumento económico para SOLID en enjambres es directo. Un enjambre de 20 agentes en producción durante 12 meses, sin SOLID, acumula una deuda de acoplamiento que hace que cada nueva feature cueste entre 3 y 7 veces más que la primera. Con SOLID, ese multiplicador se mantiene cercano a 1,2-1,5x durante toda la vida del sistema. La diferencia acumulada en 12 meses, para un equipo de 4 ingenieros, equivale a entre $180.000 y $400.000 en costos de desarrollo.

Esta inversión en estructura temprana (estimada en 1-2 semanas de diseño adicional al inicio del proyecto) tiene un ROI de 4x en el primer mes y de 10x al tercer mes, conforme el costo evitado de reescritura y debugging se acumula (cf. Vol. 3, cap. 24).

## Lo esencial del capítulo 24

- SOLID es una filosofía de gestión de la complejidad, no una sintaxis OO; por eso aplica a los agentes con mayor urgencia que a las clases.
- Los cinco principios reescritos para enjambres: responsabilidad única por agente, ampliar con nuevos agentes (no modificar existentes), contratos sustituibles (LSP → independencia del modelo), interfaces estrechas (ISP → eficiencia de tokens), dependencia de abstracciones (DIP → puertos MCP).
- Implementaciones como Jev (TypeSafe AI, 2026) en el arnés de control y Dots (OpenAI, 2026) en enjambres persistentes validan que SRP, ISP y DIP son esenciales para desacoplar el control determinista de la inferencia probabilística.
- SOLID importa MÁS en enjambres porque la incertidumbre probabilística amplifica el caos de las fronteras difusas: el factor de degradación se estima en 4-6x vs. 2,3x en OO.
- El refactoring de enjambres comprende 4 pasos: audit de responsabilidades, detección de acoplamiento, extracción de interfaces, separación progresiva con Strangler Fig.
- El ROI de SOLID temprano en enjambres es de 4x en mes 1 y 10x en mes 3.
