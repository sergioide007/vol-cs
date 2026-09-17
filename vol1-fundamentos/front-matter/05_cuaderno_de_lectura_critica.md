# Cuaderno de lectura crítica

_Para qué sirve este cuaderno: un libro técnico se entiende mejor cuando el lector discute con él. Este cuaderno ofrece tres instrumentos: una rúbrica para evaluar el volumen con criterios explícitos, una plantilla para redactar una crítica fundamentada, y preguntas de discusión por capítulo que convierten cada idea en una decisión que usted puede tomar o rechazar con razones._

## 1. Rúbrica para evaluar este volumen

Use esta tabla para construir una crítica propia. No se trata de puntuar por gusto, sino de poder justificar el juicio con evidencia del propio texto.

| Criterio | La pregunta que usted debe poder responder | Señal de debilidad |
|---|---|---|
| Claridad del propósito | ¿Puedo enunciar en una frase qué problema resuelve el capítulo y a quién le sirve? | El capítulo mezcla audiencias o promete más de lo que entrega |
| Solidez de la evidencia | ¿Cada afirmación cuantitativa tiene fuente verificable o es una estimación del autor? | Cifras sin fuente o con fuente no cotejable |
| Trazabilidad | ¿Puedo llegar del concepto a su implementación (código, tabla, protocolo) sin saltos? | Se pasa del principio a la conclusión sin el paso intermedio |
| Aplicabilidad | ¿Puedo tomar una decisión concreta mañana con lo que el capítulo dice? | Todo queda en «depende» sin criterio de decisión |
| Vigencia | ¿Sé qué parte del capítulo caduca con el próximo release y cómo verificarlo? | Se presentan precios, versiones o modelos como si fueran estables |
| Reconocimiento de límites | ¿El capítulo dice cuándo **no** aplica su recomendación? | Se presenta una solución como universal |
| Utilidad como manual | ¿Puedo volver al capítulo buscando una cosa concreta y encontrarla rápido? | Falta la tabla de decisión, el índice local o el ejercicio resuelto |

**Cómo se usa en la práctica.** Elija tres capítulos, aplique la rúbrica y escriba un juicio de una página. Si su veredicto es «me gustó» o «no me gustó» sin poder señalar la fila de la tabla que lo sostiene, la crítica todavía no está lista.

## 2. Plantilla para redactar una crítica

1. **Resumen en una frase.** «Este capítulo sostiene que ___ y lo justifica con ___».
2. **Tesis del autor.** Enúnciela con sus palabras, sin ironía. Si no puede, todavía no la entendió.
3. **Evidencia a favor.** La pieza del propio capítulo que mejor sostiene la tesis (tabla, caso, ejercicio resuelto, cita indexada).
4. **Evidencia en contra o hueco.** Lo que el capítulo no cubre, lo que generaliza de más, lo que depende de un contexto distinto al suyo.
5. **Veredicto con destinatario.** No «es bueno» o «es malo», sino «le sirve a ___ para ___ , y falla para ___ porque ___».

**Regla de oro.** Critique la afirmación, no el tema. «Los agentes autónomos son peligrosos» no es una crítica; «el capítulo afirma que el nivel 4 de autonomía se justifica solo si el nivel 3 opera bien, pero no ofrece criterio para medir *opera bien*» sí lo es.

## 3. Preguntas de discusión por capítulo

Las preguntas están ordenadas para llevarlo de la comprensión a la crítica y de ahí a la decisión. No todas tienen respuesta en el texto: las que no la tienen son, precisamente, el espacio donde su criterio importa.

### Capítulo 1. El despertar agéntico

1. El capítulo clasifica los sistemas en un espectro de autonomía (niveles 0 a 4). ¿Su organización usa la palabra «agente» con esa misma precisión, o llama agente a lo que aquí es un *workflow*? ¿Qué decisión concreta (presupuesto, pruebas, permisos, quién responde) cambia al reclasificar?
2. El nivel de autonomía se elige por la estructura de la tarea, no por la ambición del equipo. Busque un caso de su entorno que hoy opere un nivel por encima de lo que la tarea exige. ¿Qué coste paga por ese exceso y quién lo asume?
3. Crítica al capítulo: ¿basta la taxonomía propuesta para decidir el nivel, o falta una dimensión (costo del error, reversibilidad, exigencia regulatoria) que usted consideraría indispensable?

### Capítulo 2. El AI Engineer

1. De las siete competencias núcleo, ¿cuál no se puede comprar y solo se adquiere con práctica deliberada? ¿Qué evidencia verificable exigiría usted en una contratación para comprobarla en una hora?
2. El capítulo sostiene «demostrar, no acumular». ¿Qué tres piezas presentaría usted hoy? Si no puede, ¿qué le falta y en cuánto tiempo lo consigue?
3. El capítulo afirma que la competencia 7 (orquestación) sin las otras seis «es la receta del incendio distribuido». ¿Está de acuerdo con ese orden de dependencias? ¿Qué contraejemplo conoce?

### Capítulo 3. Platform Engineering en la era agéntica

1. ¿Cuántos equipos de su organización consumen hoy modelos con claves de API propias, fuera de cualquier inventario central? ¿Cuál es el riesgo y quién lo está asumiendo sin saberlo?
2. El AI Gateway centraliza presupuesto, cuotas y auditoría. ¿Qué se pierde al centralizar (autonomía, velocidad, experimentación) y con qué criterio decide el capítulo que la pérdida vale la pena?
3. Crítica al capítulo: ¿es realista exigir un gateway único en una organización con silos fuertes? ¿Qué mínimo viable de gobernanza propone usted si la centralización completa no es viable?

### Capítulo 4. Fundamentos técnicos del agente moderno

1. El capítulo distingue ventana de contexto de memoria. En su equipo, ¿hay decisiones de diseño que confunden ambas? ¿Qué fallo concreto produce esa confusión en producción?
2. El arnés es el sistema de control alrededor del modelo. Separe su sistema en dos columnas: lo que es determinista y lo que queda al criterio del modelo. ¿Puede justificar cada elemento de la segunda columna?
3. El capítulo presenta ReAct y su familia de variantes. ¿Qué patrón usa hoy y por qué ese y no otro? ¿Qué evidencia le haría cambiarlo?
4. Crítica al capítulo: es el más denso del volumen y agrupa temas que otros libros tratan por separado. ¿La unidad argumental que el autor defiende como razón para no dividirlo se sostiene, o el lector paga un coste de densidad evitable?

### Capítulo 5. La Empresa Sintética

1. ¿Qué ventaja obtiene al especializar sus agentes en roles y qué coste de coordinación paga por ello? ¿Cómo lo mide hoy?
2. El prompt maestro aplica DRY a las instrucciones. ¿Qué riesgo de acoplamiento introduce un prompt maestro único y cómo lo mitigaría?
3. Crítica al capítulo: ¿la metáfora de la «empresa» ilumina o confunde? ¿Qué se gana y qué se pierde al tratar un enjambre como organigrama?

### Capítulo 6. DDD como sistema inmunológico

1. ¿Existe en su organización un documento de dominio que un agente pudiera consumir hoy? Si no, ¿quién tiene ese conocimiento en la cabeza y qué pasa el día que se va?
2. Identifique un invariante de su dominio que un agente podría violar sin que ningún verificador determinista lo detecte. ¿Qué capa debería atraparlo?
3. Crítica al capítulo: ¿el vocabulario de DDD (agregado, contexto delimitado, lenguaje ubicuo) explica bien el problema a un equipo sin cultura de diseño orientado a objetos, o se convierte en barrera de entrada?

### Capítulo 7. Creación de skills

1. ¿Qué procedimiento de su equipo vive solo en la cabeza de una persona? Conviértalo en skill: ¿cuál es el disparador, qué salida produce y cómo sabría si funcionó?
2. El capítulo insiste en la divulgación progresiva: la descripción está siempre disponible y el contenido se carga solo cuando hace falta. ¿Qué falla cuando la descripción es ambigua?
3. Crítica al capítulo: la checklist de revisión de skills, ¿es verificable por alguien que no escribió el skill, o exige el mismo contexto que el autor?

### Capítulo 8. Patrones de orquestación multi-agente

1. De los cinco patrones canónicos, ¿cuál fallaría peor en su dominio y por qué? ¿Qué lo haría fallar: latencia, costo, consistencia o la naturaleza del error?
2. El capítulo exige una política de degradación distinta por patrón. ¿Su sistema distingue «degradar» de «fallar»? ¿Qué evidencia tiene de que la degradación queda documentada y no silenciosa?
3. Revisión crítica: de los cuatro anti-patrones de orquestación que el capítulo describe, ¿reconoce alguno en su arquitectura actual? ¿Cuál y con qué consecuencia observable?

### Capítulo 9. MCP: el protocolo que une el mundo agéntico

1. De los diez sistemas internos más consultados por sus equipos (tickets, métricas, documentación, CRM…), ¿cuántos son hoy accesibles para un agente de forma gobernada?
2. Puntúe sus cinco servidores MCP más usados con el protocolo de admisión del capítulo (mantenimiento, seguridad del esquema, versionado, trazabilidad, degradación). ¿Alguno quedaría por debajo del umbral y qué haría al respecto?
3. Crítica al capítulo: ¿el umbral «menos de 4 no se admite, sin excepción de urgencia» es realista en una organización con presión de negocio, o es un ideal que nadie cumple y por tanto no gobierna nada?

### Capítulo 10. La Arquitectura del Contexto

1. El corpus de instrucciones también es código: ¿quién lo revisa, quién lo versiona y quién lo prueba en su equipo?
2. La regla de dependencia aplicada a los archivos `.md`: ¿su corpus de prompts depende hacia arriba (hacia lo estable) o hacia abajo (hacia lo cambiante)? Dé un ejemplo concreto.
3. Crítica al capítulo: ¿la analogía «el corpus de instrucciones es código» se sostiene hasta el final, o hay prácticas del código (tests, tipado, cobertura) sin equivalente razonable en un corpus en lenguaje natural?

## 4. Autoevaluación de comprensión

Marque lo que puede hacer **sin volver al texto**; lo que no marque es su lista de relectura.

- [ ] Explicar la diferencia entre *workflow* y agente con un ejemplo propio.
- [ ] Enunciar las siete competencias del AI Engineer sin leerlas.
- [ ] Justificar por qué el gateway es el componente más crítico de la plataforma.
- [ ] Dibujar el ciclo ReAct y señalar dónde entra el arnés.
- [ ] Distinguir contexto de memoria en un caso real.
- [ ] Nombrar los cinco patrones de orquestación y el fallo típico de cada uno.
- [ ] Aplicar el protocolo de admisión de MCP a un servidor concreto.
- [ ] Decir qué parte de su corpus de instrucciones es dependiente y cuál estable.

## 5. Cómo citar y discutir este volumen

Al citar, distinga siempre tres cosas: el **principio** (invariante y probablemente duradero), la **implementación** (atada a una herramienta o versión) y el **dato** (cifra o precio, con fecha de caducidad). Una crítica honesta de este volumen separa las tres: se puede estar de acuerdo con el principio, en desacuerdo con la implementación y dudar del dato, sin contradicción. Esa distinción es, en sí misma, la competencia que el libro quiere enseñar.
