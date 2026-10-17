# Capítulo 30: Cursor, Windsurf y Zed

> *Cuando la extensión no alcanza, se reescribe el huésped.*

## La decisión de romper con VSCode

Instalar una extensión en VSCode tiene un techo. El modelo vive en la extensión, pero el editor no sabe nada de él: la paleta de comandos, el explorador de archivos, el flujo de edición, todo fue diseñado antes de que los LLMs existieran. En algún momento, varios equipos llegaron a la misma conclusión: para construir el editor del futuro, había que construir el editor entero.

Cursor, Windsurf y Zed son las tres respuestas más influyentes a esa conclusión. Las tres eligieron caminos distintos.

## Cursor: el fork que reescribió las reglas

Cursor (cursor.sh) es un fork de VSCode construido por Cursor Inc. Mantiene la compatibilidad total con extensiones y atajos de VSCode (el programador que migra no pierde nada) pero añade tres capas que no son posibles en una extensión:

### Tab: completado predictivo de ediciones

Cursor «Tab» no completa la línea actual: predice la **siguiente edición del archivo** (incluyendo borrados, refactorizaciones locales y cambios multilinea) y la sugiere con un solo teclado. No es autocompletado; es edición predictiva. La diferencia es arquitectónica: Cursor entrena modelos propios sobre patrones de edición, no solo de texto.

### Composer: el agente de cambios multiarchivo

Composer es la respuesta de Cursor a Cline (Vol. 2, cap. 29). Recibe una instrucción en lenguaje natural y genera un plan de cambios que puede abarcar docenas de archivos. A diferencia de Cline, Composer no ejecuta comandos de shell de forma autónoma por defecto, propone los cambios y el programador los aprueba o descarta archivo por archivo.

### Contexto semántico global

Cursor indexa el repositorio y mantiene un grafo semántico de relaciones entre símbolos. Cuando el programador abre el chat con `Ctrl+K`, el contexto incluye automáticamente los archivos relevantes, sin que el programador tenga que especificarlos. Este indexado ocurre localmente; Cursor no envía el código fuente completo a servidores externos.

![Diagrama 30.1: Lo que gana un fork respecto a una extensión](imagenes/capitulo77/diagrama77_ides_es.png)

*Diagrama 30.1: Lo que gana un fork respecto a una extensión.*

## Windsurf: la apuesta de Codeium por la «fluidez»

Codeium comenzó como un plugin de autocompletado para VSCode. En 2024 anunció Windsurf: un IDE propio (también fork de VSCode) construido alrededor de un concepto que llaman **Cascade**.

### Cascade: el agente de flujo

Cascade se diferencia de Composer en su modelo de interacción. Donde Cursor propone cambios paso a paso, Cascade describe su plan en lenguaje natural, ejecuta una secuencia de acciones y presenta el resultado final, manteniendo al programador informado del proceso sin interrumpirlo en cada paso. Codeium lo llama «flow state»: el programador permanece en el estado de concentración mientras el agente trabaja en paralelo.

Windsurf además integra herramientas de búsqueda web y terminal nativas, lo que le da una arquitectura de agente similar a Cline pero con el IDE como capa de presentación unificada.

### Supermaven integrado

Codeium adquirió Supermaven (conocido por su contexto de un millón de tokens para autocompletado) e integró su motor en Windsurf. El resultado es un completado de código con contexto de repositorio completo, sin los límites de ventana que afectan a otras soluciones.

## Zed: el editor nuevo, no el fork

Zed toma una decisión diferente: en lugar de partir de VSCode, construyó un editor desde cero en Rust, optimizado para velocidad y colaboración en tiempo real. La IA no se añadió después, fue parte del diseño desde el inicio.

### El modelo de integración de Zed

Zed integra LLMs directamente en el editor sin capa de extensión intermedia. El modelo ve el contexto del archivo activo, los errores del LSP y el historial de cambios recientes como parte de su contexto nativo. La latencia es notablemente menor que la de extensiones equivalentes porque no hay serialización entre el editor y el modelo.

| IDE | Base | Agente principal | Punto fuerte |
|---|---|---|---|
| Cursor | VSCode fork | Composer | Compatibilidad VSCode + Tab predictivo |
| Windsurf | VSCode fork | Cascade | Flujo continuo sin interrupciones |
| Zed | Nativo (Rust) | Integración directa | Velocidad y colaboración |

*Tabla 30.1: Comparación de los tres IDEs nativos de IA.*

## El dilema del ecosistema de extensiones

El mayor costo de abandonar VSCode es invisible: el ecosistema. Decenas de miles de extensiones (linters, runners de test, integraciones CI, temas) funcionan en VSCode porque son el estándar de facto. Cursor y Windsurf mitigan esto al mantener compatibilidad con la API de extensiones de VSCode. Zed construye su propio ecosistema, más pequeño, pero más rápido.

Para un equipo que evalúa el salto, la pregunta es «¿cuánto del ecosistema de herramientas de mi equipo sobrevive el cambio?», no «¿cuál IA es mejor?». La respuesta guía la decisión más que cualquier benchmark de generación de código.

## La relación con el paradigma multi-agente

Estos IDEs no son agentes en el sentido del capítulo 8, son **entornos de ejecución** para agentes. Cursor Composer y Cascade son orquestadores locales que coordinan cambios en el repositorio. La siguiente frontera (ya visible en 2025) es conectarlos con pipelines de CI/CD y agentes externos vía MCP, convirtiendo el IDE en un nodo más del enjambre multi-agente.

## La perspectiva ejecutiva: el IDE como decisión de plataforma

**■ PISTA EJECUTIVA**


La adopción de un IDE nativo de IA no es una decisión individual del desarrollador, es una decisión de plataforma con implicaciones de seguridad, licenciamiento, vendor lock-in y productividad medible que corresponde al liderazgo técnico y al C-suite evaluar con el mismo rigor que cualquier otra decisión de infraestructura.

**Seguridad y confidencialidad del código fuente.** Cursor y Windsurf, en su configuración por defecto, envían fragmentos del código fuente a APIs externas para el indexado semántico y la generación de sugerencias. Para empresas en sectores regulados (finanzas, salud, defensa) o que trabajan con código fuente que constituye ventaja competitiva, esta configuración no es aceptable sin un análisis explícito de los términos de datos de los proveedores. Cursor ofrece un modo "Privacy Mode" que desactiva el almacenamiento remoto del código, y tanto Cursor como Windsurf tienen acuerdos empresariales con compromisos de privacidad más estrictos. Zed, al procesar todo localmente, evita esa cuestión por arquitectura.

**Vendor lock-in y portabilidad.** Cursor y Windsurf, al mantener compatibilidad con la API de extensiones de VSCode, minimizan el riesgo de lock-in en el ecosistema de herramientas: las extensiones del equipo (linters, runners de test, integraciones CI) continúan funcionando. Zed, con su propio ecosistema de extensiones, introduce un riesgo de portabilidad que debe evaluarse contra sus ventajas de velocidad. La pregunta práctica para el CTO: "¿si mañana este proveedor sube el precio 3x o es adquirido, cuánto cuesta migrar?"

**Métricas de productividad y justificación del costo.** Los IDEs nativos de IA tienen costos de suscripción ($20–40/mes por desarrollador para Cursor y Windsurf en planes pro). Para un equipo de 10 desarrolladores, el costo anual es $2.400–$4.800. La justificación económica requiere demostrar un multiplicador de productividad de al menos 1.5x en las tareas del equipo, umbral alcanzable según la evidencia de Peng et al. (2023). La recomendación operacional es medir antes de adoptar masivamente: un piloto de 4 semanas con 3–5 desarrolladores en un proyecto representativo, midiendo velocity de sprint antes y después, produce la evidencia necesaria para la decisión.

**El IDE como nodo del enjambre multi-agente.** La frontera estratégica más relevante (ya visible en 2025) es la integración de estos IDEs con pipelines de CI/CD y agentes externos vía MCP. Un Cursor Composer o Cascade que puede no solo proponer cambios en el repositorio sino también disparar un agente de revisión de seguridad, ejecutar los tests de integración y publicar el resultado en el sistema de gestión de proyectos convierte el IDE en un nodo activo del enjambre organizacional, no solo una herramienta individual de productividad.

## Benchmarks comparativos y estado de la investigación

La comparación rigurosa de IDEs nativos de IA es metodológicamente compleja porque las diferencias de productividad dependen fuertemente del tipo de tarea, el stack tecnológico y las preferencias individuales del desarrollador. El benchmark SWE-bench ([Jimenez et al., 2024](#ref-jimenez2024)), publicado como parte de la investigación del Princeton NLP Group, evalúa la capacidad de sistemas de agentes para resolver issues reales de GitHub en repositorios de producción, la métrica de evaluación más cercana al trabajo real de un desarrollador. Los modelos que alimentan Cursor Composer (Claude Sonnet, GPT-4o) muestran tasas de resolución del 12–49% en SWE-bench, dependiendo de la variante del benchmark, rangos que, traducidos a productividad de equipo, equivalen a acelerar entre uno y cuatro sprints de trabajo de ingeniería por trimestre.

## Lo esencial del capítulo 30

- Cursor (fork de VSCode) añade Tab predictivo, Composer multiarchivo e indexado semántico local.
- Windsurf (Codeium) apuesta por el flujo continuo con Cascade y contexto de repositorio completo vía Supermaven.
- Zed construye un editor nativo desde cero en Rust, con IA integrada a bajo nivel.
- El criterio de elección real es la compatibilidad con el ecosistema de herramientas del equipo, no qué IA es "mejor".
- Perspectiva ejecutiva: adopción de IDE nativo de IA es decisión de plataforma; requiere evaluación de seguridad, vendor lock-in y piloto de productividad medida antes de adopción masiva.
- SWE-bench ([Jimenez et al., 2024](#ref-jimenez2024)) es el benchmark de mayor validez ecológica para comparar agentes de código en tareas reales.
