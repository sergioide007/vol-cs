# Capítulo 29: Cline y Continue

> *La extensión más poderosa no es la que hace más cosas: es la que desaparece cuando no hace falta y actúa cuando sí.*

## El territorio: agentes que se quedan en VSCode

Mientras una parte del ecosistema decidía construir IDEs completos (Vol. 2, caps. 30 y 31), otra parte apostó por algo distinto: llevar la agencia completa al interior de VSCode sin romper el flujo del programador. Cline y Continue son los dos exponentes más influyentes de esa apuesta. No compiten entre sí (resuelven necesidades adyacentes) y juntos definen los extremos del espectro entre *autonomía* y *contexto*.

## Cline: el agente autónomo

Cline (anteriormente conocido como Claude Dev) nació de una premisa radical: si un modelo como Claude puede razonar sobre código, ¿por qué limitarlo a responder preguntas en un chat? La respuesta fue convertirlo en un agente completo dentro de VSCode.

### Lo que Cline puede hacer

En una sola instrucción, Cline puede:

- Leer el árbol de archivos del proyecto y comprender su arquitectura
- Editar varios archivos de forma coordinada
- Ejecutar comandos en la terminal integrada y leer su salida
- Navegar páginas web para buscar documentación o errores
- Llamar servidores MCP (cap. 9) para interactuar con servicios externos

Todo esto ocurre en un **bucle autónomo** que solo interrumpe cuando detecta una acción irreversible (borrar un archivo, ejecutar un comando destructivo) o cuando el modelo necesita aclaración. El programador supervisa, no microgestiona.

### Arquitectura de Cline

Cline es open-source (licencia MIT) y modelado sobre el Agent SDK de Anthropic, aunque acepta cualquier proveedor compatible con la API de OpenAI. Su diseño separa el **núcleo de razonamiento** (el modelo LLM, intercambiable) del **conjunto de herramientas** (sistema de archivos, terminal, navegador), unidos por una interfaz normalizada. Esta separación permite cambiar de Claude a GPT-4o o a un modelo local sin tocar la lógica de agente.

![Diagrama 29.1: Arquitectura de Cline](imagenes/capitulo76/diagrama76_vscode_extension_es.png)

*Diagrama 29.1: Arquitectura de Cline: el modelo es intercambiable, las herramientas son estables.*

### El patrón de confirmación humana

Cline implementa un patrón que los capítulos anteriores describen teóricamente: **acción autónoma con puntos de control humano**. Antes de ejecutar un comando de shell o de modificar un archivo crítico, pide confirmación. Esta granularidad es configurable: el programador puede autorizar categorías completas (p. ej., «editar archivos .ts sin preguntar») y reservar la confirmación para operaciones de mayor riesgo.

## Continue: el asistente contextual

Continue (continue.dev) parte de una filosofía diferente. En lugar de autonomía, apuesta por **profundidad de contexto**. Su premisa: el mayor obstáculo del programador no es la escritura de código, es que el modelo no sabe qué hace el resto del repositorio cuando sugiere un cambio.

### Indexación del repositorio

Continue indexa el repositorio completo al arrancar y mantiene ese índice actualizado. Cuando el programador pide «refactoriza esta función para que sea coherente con el patrón del módulo de autenticación», Continue recupera los archivos relevantes del índice y los incluye en el contexto antes de enviarlo al modelo. El resultado es una IA que *conoce la base de código*, no solo el archivo abierto.

### Privacidad y modelos locales

Continue soporta modelos locales a través de Ollama: el código nunca sale del equipo. Esto lo convierte en la opción natural para equipos con restricciones de privacidad (bancos, salud, defensa) donde enviar código a una API externa no es aceptable.

| Dimensión | Cline | Continue |
|---|---|---|
| Modelo de uso | Agente autónomo | Asistente contextual |
| Autonomía | Alta | Media |
| Privacidad | API externa (configurable) | Local posible |
| Punto fuerte | Tareas complejas end-to-end | Coherencia con el repo |
| Integración multi-agente | MCP nativo | RAG del repositorio |

*Tabla 29.1: Comparación de posicionamiento.*

## La conexión con el paradigma multi-agente

Ninguno de los dos es una isla. Cline puede actuar como **orquestador local** (invoca servidores MCP, delega subtareas a agentes especializados, y devuelve el resultado al programador) conectando el IDE con el ecosistema agentico descrito en los capítulos anteriores. Continue, por su parte, actúa como **capa de recuperación de contexto** (RAG aplicado al código): recupera el conocimiento relevante antes de que cualquier agente tome una decisión sobre el repositorio.

Usados juntos (Continue como capa de conocimiento, Cline como ejecutor) forman un sistema en dos capas que encarna el principio del capítulo 8: separar *el saber* del *el hacer*.

## La perspectiva ejecutiva: agentes en el IDE como palanca de productividad medible

**■ PISTA EJECUTIVA**


Desde una perspectiva de liderazgo de producto y gestión de equipos de ingeniería, la introducción de agentes en el IDE no es una actualización de herramientas, es un cambio en el modelo de producción del software. Las implicaciones para product owners, scrum masters y arquitectos de software merecen articulación explícita.

**Impacto en la velocidad del equipo.** Los datos publicados por GitHub en el *Copilot Impact Report 2023* (aunque referidos a un asistente menos autónomo que Cline) documentan una reducción del 55% en el tiempo requerido para completar tareas de programación estándar. Para agentes con capacidad de acción autónoma como Cline, el multiplicador es mayor en tareas de alta complejidad y repetibilidad: migraciones de dependencias, generación de tests, refactorizaciones con patrón bien definido. La ganancia no es lineal, las tareas que más se benefician son exactamente las que más tiempo consumían en los sprints.

**Implicaciones para la definición de "Definition of Done".** Cuando un agente autónomo puede generar, ejecutar y corregir tests en un bucle, la DoD de una historia de usuario debe actualizarse. El criterio "todos los tests pasan" se convierte en "todos los tests pasan *y fueron revisados por el programador*", no simplemente escritos y ejecutados por el agente. Esta distinción (revisión humana de la calidad de los tests, no solo de su resultado) es operacionalmente relevante para equipos que usan Cline como ejecutor.

**El riesgo de deuda técnica acelerada.** El mismo mecanismo que acelera la producción de código puede acelerar la acumulación de deuda técnica si no se establece una política de revisión explícita. Un agente que genera 200 líneas de código en 5 minutos puede generar 200 líneas de código con acoplamiento excesivo, ausencia de abstracciones adecuadas y tests de baja calidad en el mismo tiempo. La solución no es limitar el agente, es establecer criterios de revisión de código más rigurosos para código generado agénticamente, priorizando arquitectura sobre funcionalidad en el code review.

**Continue como herramienta de incorporación acelerada.** Un uso ejecutivo de Continue que no recibe suficiente atención: la incorporación de nuevos ingenieros a codebases grandes. Un ingeniero nuevo que puede hacer preguntas conversacionales sobre un repositorio de 500.000 líneas de código ("¿cómo está implementado el patrón de retry en el módulo de pagos?", "¿qué hace este servicio cuando el proveedor externo devuelve un 429?") reduce su curva de onboarding de semanas a días. El ROI de Continue en este contexto es directamente cuantificable en horas de onboarding ahorradas.

## Benchmarks y validación de impacto

La investigación de Peng et al. (2023), *The Impact of AI on Developer Productivity: Evidence from GitHub Copilot* (publicado como working paper del National Bureau of Economic Research), proporciona evidencia empírica de que los asistentes de código basados en LLM aumentan la velocidad de completar tareas en un 55.8% en experimentos controlados aleatorizados. Este es el estudio de mayor rigor metodológico disponible sobre el impacto de agentes de código, y su metodología es aplicable a la evaluación de Cline y Continue en entornos de producción.

Para arquitectos de software que evalúan la adopción de estas herramientas, la metodología de Peng et al. ofrece un framework de evaluación: medir tiempo de tarea en un conjunto representativo de tareas del equipo, con y sin el asistente, usando asignación aleatoria. El resultado numérico obtenido en ese experimento es más valioso que cualquier benchmark publicado por los propios vendedores de herramientas.

## Lo esencial del capítulo 29

- Cline es un agente autónomo open-source para VSCode: edita, ejecuta, navega y llama herramientas MCP en un bucle supervisado.
- Continue es un asistente contextual que indexa el repositorio completo y puede operar con modelos locales.
- Ambos son agnósticos al proveedor de modelo.
- Cline como orquestador local + Continue como capa RAG forman un sistema en dos capas de agencia e inteligencia contextual.
- Perspectiva ejecutiva: la DoD debe actualizarse cuando un agente genera código; Continue acelera el onboarding de nuevos ingenieros a codebases grandes.
- La evidencia empírica (Peng et al., 2023, NBER) documenta +55% de velocidad en tareas de programación con asistentes de código, el benchmark más riguroso disponible.
