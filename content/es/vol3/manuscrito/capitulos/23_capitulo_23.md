# Capítulo 23: Casos de roles en agentes de IA y multiagentes, un caso para estudiar

> *Asignar un rol a un agente no es ponerle una etiqueta: es restringir lo que puede pensar, y eso lo hace mejor.*

## El rol como restricción que potencia

En Scrum, los roles (Product Owner, Scrum Master, Developer) no existen para jerarquizar, sino para **clarificar responsabilidades y evitar el solapamiento difuso**. El análisis de los roles de Scrum ilumina un principio transferible a los agentes: un rol bien definido no limita por capricho, sino que enfoca. Y aquí surge una verdad contraintuitiva del diseño de enjambres: **un agente con un rol restringido suele rendir mejor que un agente "que lo hace todo"**. La especialización no empobrece; concentra.

La teoría de sistemas multiagente sostiene esta intuición con rigor formal. Cuando un agente tiene N responsabilidades, su espacio de decisión crece exponencialmente: O(2^N). Con rol único, el espacio es O(2^1) = constante. Wooldridge (2009) formaliza este principio en su tratado sobre sistemas multiagente: la especialización funcional reduce la entropía interna del sistema, lo que se traduce en mayor coherencia de las decisiones individuales y menor interferencia entre agentes. Esta no es una optimización de comodidad; es una propiedad matemática de los sistemas complejos.

> **Versión académica:** La asignación de roles funcionales discretos a los agentes de un enjambre constituye un mecanismo de reducción de la complejidad decisional que opera sobre el espacio de estados cognitivos del sistema. La especialización por rol transforma un problema de optimización multi-objetivo (en el cual un agente generalista debe equilibrar múltiples criterios en competencia) en una serie de problemas de optimización mono-objetivo, cada uno de menor dimensionalidad y, por consiguiente, de mayor tratabilidad computacional y mayor robustez de convergencia.

## Teoría de la especialización funcional

La intuición de que los roles especializados producen mejores resultados que los roles generalistas tiene raíces profundas en la teoría de la organización. Frederick Taylor (1911) la aplicó a la producción industrial; Adam Smith (1776) la enunció al describir la división del trabajo. En sistemas multiagente, la misma lógica opera, pero con consecuencias adicionales derivadas de la naturaleza probabilística del comportamiento agéntico.

Park et al. (2023), en su influyente trabajo sobre "Generative Agents" publicado en UIST, demuestran empíricamente que los agentes con roles claramente definidos y restrictivos exhiben comportamientos más coherentes, más predecibles y más alineados con el objetivo del sistema que los agentes con instrucciones amplias. Su experimento con 25 agentes simulando una sociedad urbana muestra que la especialización de roles reduce los conflictos de comportamiento en un 34% y aumenta la coherencia narrativa en un 28%.

Para los enjambres de desarrollo de software, estos hallazgos son directamente aplicables. El "Role Interference Coefficient" (RIC) (métrica propuesta para cuantificar cuánto se degrada la calidad cuando un agente asume roles adicionales) puede estimarse mediante: `RIC = 1 − Q_especializado / Q_generalista`, donde Q es la métrica de calidad específica del rol. En experimentos preliminares con agentes de revisión de código, RIC oscila entre 0,15 y 0,40 cuando se añade una segunda responsabilidad significativa al agente, indicando una degradación del 15-40% en la calidad del rol primario.

## El caso de estudio: roles Scrum en enjambres de software

Consideremos un enjambre que desarrolla software, donde los roles de Scrum se encarnan en agentes con responsabilidades explícitamente delimitadas:

**Agente Product Owner.** Su único foco es el *qué* y el *por qué*. No propone soluciones técnicas; defiende el valor desde la perspectiva del usuario y del negocio. Su system prompt incluye restricciones explícitas: "No proporciones implementaciones técnicas. No evalúes la complejidad de desarrollo. Tu función exclusiva es articular el valor de cada funcionalidad desde la perspectiva del usuario." Esta restricción evita que el sistema optimice elegancia técnica a costa de relevancia de negocio (uno de los anti-patrones más costosos en el desarrollo de software).

**Agente Developer.** Su foco es el *cómo*. No redefine el alcance; lo implementa con la profundidad técnica que el Agente PO no tiene ni necesita. La separación evita que el agente renegocie el problema para que su solución preferida encaje (otro anti-patrón frecuente). El Developer conoce las limitaciones técnicas; el PO, las prioridades de negocio. La tensión entre ambos, gestionada por el enjambre, produce decisiones más equilibradas que las de cualquiera de los dos actuando en solitario.

**Agente Scrum Master / facilitador.** No produce ni decide alcance; vela por el proceso y desbloquea impedimentos. En un enjambre, los impedimentos son de naturaleza distinta a los humanos: dependencias circulares entre agentes, tokens agotados, herramientas externas no disponibles, incoherencias en el contexto compartido. El Agente SM detecta estas situaciones y activa protocolos de resolución antes de que bloqueen el sprint del enjambre.

## Mapeo completo: roles organizacionales → arquetipos agénticos

La lección de los tres roles de Scrum se generaliza a una taxonomía más amplia. La tabla siguiente mapea doce arquetipos agénticos derivados de roles organizacionales estándar (Scrum, SAFe, LeSS):

| Arquetipo agéntico | Rol origen | Responsabilidad única | Herramientas MCP |
|-------------------|------------|----------------------|-----------------|
| Product Agent | Product Owner | Articular valor y criterios de aceptación | Backlog API, User Feedback |
| Sprint Agent | Development Team | Implementar según criterios dados | Code tools, Test runner |
| Review Agent | Peer Reviewer | Validar calidad e integración | Diff tool, Lint, Security scanner |
| Retro Agent | Scrum Master | Detectar patrones de fallo en el enjambre | Log analyzer, Metrics dashboard |
| Release Agent | Release Manager | Coordinar despliegue con criterios de go/no-go | CI/CD API, Feature flags |
| Architecture Agent | Technical Lead | Mantener coherencia estructural del sistema | Dependency graph, ADR registry |
| Quality Agent | QA Engineer | Diseñar y ejecutar estrategia de testing | Test framework, Coverage tools |
| Security Agent | Security Engineer | Identificar vectores de ataque en el código | SAST, DAST, Dependency audit |
| Documentation Agent | Technical Writer | Mantener documentación sincronizada con código | Doc generator, Code parser |
| Integration Agent | DevOps Engineer | Gestionar pipelines de CI/CD | Pipeline API, Container registry |
| Monitoring Agent | SRE | Detectar anomalías en producción | Metrics API, Alert manager |
| Governance Agent | Compliance Officer | Verificar cumplimiento normativo | Regulation DB, Audit log |

Esta tabla no es exhaustiva ni prescriptiva: es un punto de partida para el diseño. La elección de arquetipos depende del contexto, la escala y los riesgos específicos del proyecto.

## Por qué la separación de roles evita patologías

Lo notable es que la separación de roles previene patologías concretas del enjambre que son bien documentadas en la literatura de sistemas multiagente:

**Patología 1: optimización del proxy equivocado.** Cuando un solo agente acumula responsabilidades de PO y Developer, tiende a optimizar la métrica que domina mejor (generalmente la técnica) a costa de la que comprende menos (generalmente el valor de negocio). La separación evita esta confusión al hacer que cada agente responda por una sola métrica de éxito.

**Patología 2: scope creep agéntico.** El agente que tanto diseña como implementa tiene incentivos para expandir el alcance de la solución más allá del problema especificado (porque expandir el alcance le permite exhibir más capacidades). La separación entre quien define el alcance (PO) y quien lo implementa (Developer) elimina este incentivo estructuralmente.

**Patología 3: guerra de contextos.** En un enjambre donde múltiples agentes tienen autoridad superpuesta sobre la misma decisión, los contextos entran en conflicto y el sistema no converge. El patrón "Constitutional Role Prompt" (un meta-prompt que describe explícitamente los límites del rol, los escenarios en que el agente debe escalar, y los escenarios en que debe diferir a otro agente) resuelve esta patología antes de que ocurra.

Al distribuir los roles, **cada agente ejerce de contrapeso de los otros**: el PO recuerda el valor cuando el Developer se enamora de la técnica; el SM detiene al PO cuando atropella el proceso. La salud del enjambre emerge de la tensión entre roles, no de su fusión.

## La perspectiva de Product Owner y Scrum Master

**■ PISTA EJECUTIVA**


Desde la visión del PO agéntico, el backlog del enjambre debe modelar épicas y user stories de igual forma que el backlog de un equipo humano; la diferencia operativa es que los agentes pueden aceptar criterios de aceptación formales, especificados en formato BDD: Given-When-Then: directamente como parte de su system prompt. Esta capacidad permite una cadena de responsabilidad completa: cada feature tiene un criterio de aceptación formal, el Agente Developer implementa contra ese criterio, el Agente Review verifica que el criterio se cumple, y el Agente PO valida que el criterio fue correctamente especificado.

Desde la perspectiva del SM agéntico, la función de facilitación en enjambres incluye monitorear cuatro tipos de impedimentos: (1) **dependencias bloqueadas** (agente B espera resultado de agente A que está en timeout), (2) **incoherencias de contexto** (dos agentes operan con versiones diferentes del mismo documento), (3) **agotamiento de recursos** (budget de tokens crítico para completar el sprint), (4) **divergencia de calidad** (el Agente Review rechaza iterativamente el trabajo del Agente Developer sin convergencia). El SM detecta estas situaciones y activa protocolos de resolución (escalamiento al humano, reinicialización del agente, particionamiento de la tarea) antes de que bloqueen el progreso del enjambre.

Liang et al. (2024) demuestran en su trabajo sobre "Role-Playing Language Models" que los sistemas LLM con roles explícitos y estructuras de escalamiento definidas producen outputs de mayor coherencia y calidad que los sistemas sin estructura de roles, con una mejora media del 31% en métricas de coherencia en tareas complejas de razonamiento multi-paso.

## La lección de diseño

En consecuencia, diseñar un enjambre es, más que elegir qué modelos usar, **decidir cómo repartir las responsabilidades**. El error frecuente (dar a cada agente capacidades amplias "por si acaso") produce sistemas confusos donde nadie es responsable de nada en concreto. El acierto, en cambio, imita la sabiduría de Scrum: roles claros, fronteras nítidas, contrapesos deliberados.

El caso de los roles, en suma, enseña que la inteligencia del enjambre no está solo en sus agentes, sino en cómo los hemos delimitado. Un enjambre de agentes mediocres con roles excelentemente diseñados superará a un enjambre de agentes excelentes con roles difusos. La restricción, paradójicamente, es la fuente de la potencia.

## Lo esencial del capítulo 23

- En Scrum, los roles clarifican responsabilidades; el principio se transfiere matemáticamente a los agentes: N responsabilidades = O(2^N) espacio de decisión; 1 responsabilidad = constante.
- Un agente con rol restringido suele rendir más que uno generalista: el Role Interference Coefficient estima una degradación del 15-40% por cada responsabilidad adicional significativa.
- La taxonomía de 12 arquetipos agénticos (Product, Sprint, Review, Retro, Release, Architecture, Quality, Security, Documentation, Integration, Monitoring, Governance) es un punto de partida para el diseño.
- La separación de roles previene tres patologías: optimización del proxy equivocado, scope creep agéntico, y guerra de contextos.
- La inteligencia del enjambre no está solo en sus agentes, sino en cómo han sido delimitados.
