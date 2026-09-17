# Cuaderno de lectura crítica

_Para qué sirve este cuaderno: este volumen hace afirmaciones cuantificables —costos, percentiles, ahorros— y por tanto es el más fácil de auditar y, si se lee mal, el más fácil de malinterpretar. El cuaderno ofrece una rúbrica orientada a verificar números, una plantilla de reseña y preguntas para los 13 capítulos y el Epílogo._

## 1. Rúbrica para evaluar este volumen

| Criterio | La pregunta que usted debe poder responder | Señal de debilidad |
|---|---|---|
| Recalculabilidad | ¿Puedo rehacer el cálculo del capítulo con mis propios datos? | La cifra aparece sin fórmula ni supuestos |
| Supuestos declarados | ¿El capítulo dice qué asume (volumen, precio, latencia)? | Resultado sin condiciones de contorno |
| Distinción método/dato | ¿Sé qué parte es método duradero y qué parte es cifra caduca? | Se presenta el dato como si fuera el método |
| Reproducibilidad | ¿La práctica descrita (semana del coverage, playbook) puede replicarse paso a paso? | Falta el paso, el comando o el criterio de éxito |
| Honestidad del ahorro | ¿El ahorro está medido o proyectado? | Se promete ahorro sin línea base |
| Reconocimiento de límites | ¿El capítulo dice en qué escala o equipo NO funciona? | Se prescribe para cualquier tamaño de equipo |
| Utilidad como manual | ¿Puedo consultar el capítulo por síntoma (alerta, incidente) y encontrar la sección? | El capítulo solo se entiende leído entero |

**Prueba de fuego para este volumen.** Tome un capítulo con números (1, 2, 11, 12 o 13), reproduzca su cálculo con sus propios datos y compárelo. Si el orden de magnitud se sostiene, el capítulo cumple; si no, la diferencia le enseña más que el capítulo mismo, y esa es precisamente la crítica que vale la pena escribir.

## 2. Plantilla para redactar una crítica

1. **Unidad de análisis:** ¿el capítulo habla de una tarea, un equipo, un servicio o una organización?
2. **Tesis y cifra:** «Este capítulo sostiene que ___ y lo cuantifica en ___ bajo los supuestos ___».
3. **Verificación:** recalcule o al menos identifique la línea base. ¿Coincide?
4. **Límite de aplicación:** ¿a partir de qué volumen, tamaño de equipo o tipo de carga deja de valer?
5. **Veredicto con destinatario:** «le sirve a ___ que opera a escala ___ ; no aplica a ___ porque ___».

## 3. Preguntas de discusión por capítulo

**Capítulo 1. El silencioso Token-Burn.**
1. Calcule su propio Costo por Iteración Útil (CIU) con los datos de su gateway o de su factura. ¿Cuál de las cinco causas del capítulo explica la mayor parte de su gasto?
2. Crítica: ¿la métrica CIU es accionable sin un registro por tarea, o exige una instrumentación que muchos equipos no tienen?

**Capítulo 2. Estimaciones probabilísticas.**
1. ¿Qué distribución real tienen las iteraciones por tarea en su equipo? Si no hay datos, ¿qué impide instrumentarlo esta semana?
2. Crítica: ¿leer percentiles en lugar de medias cambia de verdad una decisión, o el capítulo sobreestima el efecto de esa lectura?

**Capítulo 3. Testing de sistemas agénticos.**
1. ¿Qué comportamiento de su agente está hoy «probado» por una sola ejecución exitosa? Eso no es una prueba.
2. Crítica: ¿el TDD propuesto para sistemas no deterministas es trasladable a dominios donde el éxito es difuso (resúmenes, clasificaciones blandas)?

**Capítulo 4. Seguridad en el stack agéntico.**
1. De los nuevos vectores de ataque del capítulo, ¿cuál no está cubierto por ningún control de su sistema?
2. Crítica: ¿los cinco principios de seguridad agéntica son verificables por un tercero o requieren confiar en el autor del sistema?

**Capítulo 5. El playbook del orquestador.**
1. De los diez casos, ¿cuál es el más cercano al suyo y qué paso del playbook no podría ejecutar hoy?
2. Crítica: ¿la promesa de que los tres primeros casos «fallan barato» se sostiene en su contexto, o hay costes ocultos de reputación o de datos?

**Capítulo 6. Arquitectura limpia para sistemas agénticos.**
1. El capítulo sostiene que «el modelo es un detalle». ¿Podría cambiar de proveedor de modelo sin tocar la lógica de negocio? ¿Qué se lo impide?
2. Crítica: ¿la regla de dependencia aplicada a agentes es la misma de la arquitectura limpia clásica o introduce una excepción que el capítulo no admite?

**Capítulo 7. Arquitectura event-driven.**
1. ¿Dónde sigue usando llamadas sincrónicas donde un evento sería más robusto? ¿Qué le impide migrar?
2. En el caso del sincronizador por lotes: ¿la arquitectura híbrida cloud/on-premise descrita encaja con su realidad o añade una costura que no puede mantener?

**Capítulo 8. Operar el sistema, observabilidad y MLOps.**
1. De las señales que el capítulo propone, ¿cuál falta en su tablero y qué incidente ya le costó por no verla?
2. Crítica: ¿el enfoque «sin ceremonia» para equipos pequeños sigue siendo suficiente cuando el sistema pasa de tres a diez servicios?

**Capítulo 9. La semana del coverage.**
1. Replique el ejercicio resuelto 9.1 con su propio proyecto. ¿Su calibración de tokens por punto de cobertura coincide con la del autor?
2. Crítica: ¿el ahorro de la semana (de ~$26 a $4.04) es reproducible con su volumen, o depende de condiciones (tamaño del proyecto, calidad del `CLAUDE.md`) que el capítulo no aísla?

**Capítulo 10. La evolución de las arquitecturas.**
1. ¿En qué punto de la línea del tiempo del capítulo está su sistema: RAG, MCP, orquestación o enjambre? ¿Qué le falta para avanzar sin saltarse un paso?
2. Crítica: ¿la sección sobre computación cuántica permite una decisión hoy o es prospectiva que el lector todavía no puede usar?

**Capítulo 11. Más métricas de KPI.**
1. ¿Qué fenómeno de enjambre (deriva semántica, bucle improductivo, consenso falso) podría estar ocurriendo ya en su sistema sin que nadie lo mida?
2. Crítica: ¿los incentivos sintéticos propuestos mejoran el resultado o enseñan al enjambre a optimizar el incentivo?

**Capítulo 12. Bajo consumo de energía.**
1. ¿Cuál de las tres palancas de eficiencia energética tiene mayor margen en su caso, y cómo lo mediría?
2. Crítica: ¿la decisión CAPEX/OPEX descrita se sostiene con supuestos de precios que son volátiles?

**Capítulo 13. Recuperación ante desastres con multi-agentes.**
1. ¿Qué activo de su sistema (memoria, estado cognitivo distribuido, herramientas) no está cubierto por su plan de continuidad actual?
2. ¿Ha ejecutado un ensayo de recuperación real en el último año? Si no, su plan es una hipótesis.
3. Crítica: ¿el análisis de costos por arquitectura y estrategia permite decidir, o solo comparar órdenes de magnitud?

**Epílogo de la serie.**
1. De los invariantes de producción que resume el Epílogo, ¿cuál falta hoy en su sistema y qué lo hace evidente?
2. Crítica: el Epílogo afirma que el coste real de la adopción no es el token sino la deuda de verificación acumulada. ¿Tiene datos de su organización que confirmen o refuten esa tesis?

## 4. Autoevaluación de comprensión

Marque lo que puede hacer **sin volver al texto**; lo que no marque es su lista de relectura.

- [ ] Calcular el Costo por Iteración Útil con mis propios datos.
- [ ] Nombrar las cinco causas principales del Token-Burn.
- [ ] Explicar por qué una media no sirve para estimar tareas agénticas.
- [ ] Diseñar una prueba para un comportamiento no determinista.
- [ ] Enunciar los cinco principios de seguridad agéntica.
- [ ] Decir qué señales mínimas necesita un tablero de enjambre.
- [ ] Repetir la secuencia diagnóstico → plan → arquitectura → generación → auditoría de la semana del coverage.
- [ ] Explicar qué hace distinto al DR agéntico frente al DR tradicional.

## 5. Cómo citar y discutir este volumen

Este volumen contiene tres tipos de afirmación: el **método** (cómo se calcula, cómo se instrumenta), el **orden de magnitud** (una cifra representativa con supuestos) y la **configuración concreta** (versiones y herramientas). Cite el método sin fecha; feche el orden de magnitud y recalcule; trate la configuración como punto de partida verificable. El Estado del arte de la serie es explícito en que las herramientas de 2026 citadas no han pasado por revisión académica formal: esa honestidad se corresponde con una lectura igualmente honesta por parte del lector.