# Estado del Arte: Sistemas Multi-Agente basados en LLM y el Rol del AI Engineer

*Revisión crítica de literatura indexada (2020–2026), elaborada como respaldo académico del Volumen 1: Fundamentos*

## 1. Alcance y método de esta revisión

Este estado del arte no sustituye una revisión sistemática formal con protocolo PRISMA registrado; es una síntesis crítica dirigida a sostener académicamente la tesis del libro, construida sobre revisiones sistemáticas ya publicadas y verificables en bases indexadas (ACM Digital Library, IEEE Xplore, arXiv como fuente de preprints en un campo de publicación acelerada) más un muestreo de estudios primarios citados por esas revisiones. Cuando una afirmación proviene de una SLR publicada, se cita la SLR; cuando proviene de un estudio primario, se cita el estudio primario. No se fabricó ninguna cifra ni hallazgo: cada dato de esta sección es verificable en la fuente citada.

## 2. Líneas de investigación principales

**Línea 1: LLMs aplicados a tareas de ingeniería de software (LLM4SE).** Es la línea más consolidada y la de mayor volumen de literatura. La revisión sistemática de referencia (Hou et al., 2024, *ACM TOSEM*) analizó 395 artículos publicados entre enero de 2017 y enero de 2024, extraídos de siete bases indexadas, y documenta un crecimiento sostenido de publicaciones desde 2023 impulsado por la adopción industrial de LLMs junto con sistemas agénticos autónomos, el mismo punto de inflexión que este libro fecha en el capítulo 1.

**Línea 2: Sistemas multi-agente basados en LLM para ingeniería de software (LMA4SE).** Es la línea que sostiene directamente los capítulos 5 y 8 de este volumen. He, Treude y Lo (2025, *ACM TOSEM* 34(5)) publicaron la revisión sistemática de referencia sobre LMA aplicados a las distintas fases del ciclo de vida del software, mapeando el estado del arte de las aplicaciones. Es consistente con Ramírez-Rueda et al. (CONISOFT, 2024), que estudian específicamente la integración de sistemas multi-agente y LLMs para generación automática de código, y con la línea de trabajo de Rasheed, Waseem y colegas (Universidad de Tampere), autores de CodePori y de un artículo de posición temprano sobre agentes autónomos en desarrollo de software (2023).

**Línea 3: Patrones de prompting e ingeniería de contexto.** Sasaki et al. (COMPSAC, 2024) realizaron una revisión sistemática específica de patrones de *prompt engineering* en ingeniería de software, un antecedente directo del capítulo 10 de este volumen (Arquitectura del Contexto).

**Línea 4: Productividad, adopción y percepción del desarrollador.** Dos SLR de 2025 abordan el lado humano: Ferino, Hoda, Grundy y Treude estudian la perspectiva de desarrolladores novatos ante la adopción de LLMs; Mohamed, Assi y Guizani revisan sistemáticamente el impacto de los asistentes LLM en la productividad del desarrollador. Esta línea sostiene el capítulo 2 (El AI Engineer) y se conecta con hallazgos organizacionales más recientes de literatura gris de alta credibilidad (Bell, 2026, *Scaling AI Adoption in Engineering*, O'Reilly: no es literatura académica indexada, pero sí una síntesis de cientos de entrevistas con CTOs, citada aquí como antecedente práctico, no como evidencia científica).

**Línea 5: Costo, eficiencia energética y sostenibilidad de LLMs en producción.** Shi, Yang y Lo (2025, *ACM TOSEM* 34(5)) revisan la literatura sobre LLMs eficientes y «verdes» en ingeniería de software; antecedente directo de (Vol. 4, cap. 12), mencionado aquí porque ya empieza a emerger como preocupación en la literatura de 2024–2025, no solo como intuición de practicante.

## 3. Marcos teóricos utilizados en la literatura

La literatura revisada no converge en una única teoría, sino en una combinación de tres marcos que rara vez se citan juntos explícitamente, aunque coexisten en la práctica:

- **Marcos de arquitectura de software clásica** (Fowler, Martin, Parnas), aplicados por analogía a agentes, el propio Vol. 1 hace esto explícitamente en el capítulo 4, pero la literatura académica revisada (Hou et al., 2024; He et al., 2025) rara vez cita estas fuentes fundacionales de ingeniería de software; tiende a tratar los sistemas LMA como un objeto de estudio nuevo, sin anclarlo en la disciplina de arquitectura de software de las últimas cinco décadas. **Esta es una discrepancia real**: la literatura de LMA4SE es rica en descripción empírica de qué patrones de coordinación existen (secuencial, jerárquico, debate/consenso, la misma taxonomía del capítulo 8), pero pobre en anclarlos a principios de diseño ya establecidos (acoplamiento, cohesión, separación de responsabilidades). Este libro sí hace esa conexión explícita; es una contribución diferenciadora, no solo una síntesis de lo ya publicado.
- **Marcos de razonamiento y planificación** (ReAct de Yao et al., 2023; Tree of Thoughts de Yao et al., 2023; Reflexion de Shinn et al., 2023), que la literatura sí trata como fundacionales y que este volumen también adopta en el capítulo 4 original del libro completo (patrones fundamentales, ahora distribuido entre los volúmenes).
- **Marcos de agentes generativos con memoria y comportamiento social** (Park et al., 2023, *Generative Agents*), influyentes en la línea de investigación pero con una aplicación práctica en ingeniería de software todavía limitada según Hou et al. (2024): la mayoría de los estudios primarios de la SLR se concentran en generación y reparación de código, no en simulación social de agentes.

## 4. Metodologías aplicadas en los estudios primarios

Predominan tres familias metodológicas en la literatura revisada:

1. **Revisión sistemática de literatura (SLR) con protocolo Kitchenham/Keele.** Es el estándar de facto en LLM4SE: Hou et al. (2024) sigue explícitamente las guías de Kitchenham y Keele (2007) y de Kitchenham et al. (2009) para SLR en ingeniería de software. La mayoría de las revisiones citadas en esta sección adoptan el mismo protocolo.
2. **Estudios de *benchmark*** (SWE-bench de Jimenez et al., 2024, citado también en nuestro propio Vol. 4), miden capacidad de resolución de tareas reales de GitHub, no percepción ni adopción.
3. **Estudios cualitativos de percepción** (entrevistas, encuestas), la línea de Ferino et al. (2025) y Mohamed et al. (2025), metodológicamente más débil en poder de generalización pero más cercana a las preguntas organizacionales que aborda el Vol. 3 de esta serie.

**Limitación metodológica recurrente, señalada por los propios autores**: Hou et al. (2024) reconocen explícitamente que incluyeron artículos de arXiv sin revisión por pares para 2023–2024, dado que es un campo de publicación acelerada, aplicando un proceso de evaluación de calidad para filtrarlos. Es una decisión razonable dada la velocidad del campo, pero introduce un sesgo hacia resultados aún no validados por pares, algo que este libro también asume al citar código y herramientas de 2026 que no han pasado por revisión académica formal (Claude Agent SDK, MCP, Archify). La honestidad exige señalarlo en ambos casos.

## 5. Hallazgos recurrentes

- El crecimiento de la literatura sobre LMA4SE es reciente y abrupto: prácticamente toda la producción académica sustancial sobre sistemas *multi*-agente (a diferencia de agentes individuales) se concentra en 2023–2026, lo cual es consistente con la periodización que este libro hace en el capítulo 1 (el "despertar agéntico").
- Los patrones de coordinación identificados empíricamente en la literatura (He et al., 2025) coinciden, en líneas generales, con los cinco patrones canónicos del capítulo 8 de este volumen, lo cual sugiere que la taxonomía de este libro no es idiosincrática, sino consistente con lo que la comunidad académica está documentando de forma independiente.
- La literatura de productividad (Mohamed et al., 2025) reporta resultados mixtos y dependientes del contexto, no una mejora universal, un hallazgo que refuerza, en vez de contradecir, la tesis de este libro de que la arquitectura y el criterio humano determinan el resultado, no el modelo en sí.

## 6. Discrepancias entre autores

La discrepancia más señalable no es de datos, sino de encuadre: una parte de la literatura (particularmente los estudios de *benchmark* puro) trata la capacidad del modelo como la variable explicativa central del éxito de un sistema agéntico. Otra parte, más cercana a la línea de adopción organizacional (Ferino et al., 2025; Mohamed et al., 2025) y a la literatura de ingeniería de software clásica que este libro invoca, sitúa el proceso, la arquitectura y la organización como la variable que realmente explica la varianza en los resultados. Este libro toma partido explícito por la segunda posición, y lo hace con el respaldo de que la evidencia de productividad "mixta y dependiente del contexto" es más compatible con una explicación organizacional/arquitectónica que con una puramente relacionada con la capacidad del modelo.

## 7. Limitaciones metodológicas de la literatura revisada

- **Sesgo hacia código abierto y tareas verificables automáticamente.** La mayoría de los estudios primarios de las SLR citadas evalúan generación o reparación de código en repositorios públicos con pruebas automatizadas (el mismo sesgo que afecta a SWE-bench). Los sistemas agénticos en dominios de misión crítica o con datos privados, el foco del «caso sectorial» de (Vol. 4, cap. 5), están sistemáticamente subrepresentados en la literatura académica indexada.
- **Ventana temporal corta.** Toda la literatura sobre LMA4SE es posterior a 2023; no existe todavía perspectiva longitudinal sobre mantenibilidad o deuda técnica de sistemas agénticos a varios años de operación, una brecha que este libro solo puede señalar, no resolver, dado que la industria misma no tiene ese historial todavía.
- **Escasa reproducibilidad.** Varias de las revisiones citadas señalan que un porcentaje significativo de los estudios primarios no publica código ni datos de forma reproducible, una limitación estructural del campo, no de esta síntesis en particular.

## 8. Brechas de conocimiento

1. **Ausencia de anclaje explícito en arquitectura de software clásica** (sección 3): una brecha que este libro busca cerrar activamente, no solo señalar.
2. **Falta de estudios longitudinales sobre gobernanza y auditoría de enjambres en producción**: el Índice de Autonomía Operativa y la auditoría de reproducción cruzada propuestos en el Vol. 3 de esta serie no tienen, hasta donde esta revisión pudo verificar, un antecedente directo publicado en literatura indexada, son una contribución original de este libro, no una síntesis de lo existente, y se presentan como tal.
3. **Escasa investigación sobre el rol emergente del "AI Engineer"** como categoría profesional distinta del ML Engineer: la literatura académica revisada trata la productividad del desarrollador de forma agregada, sin la diferenciación de roles que el capítulo 2 de este volumen propone.

## 9. Relación con la tesis central del libro

La tesis de este libro (que la arquitectura y los patrones de ingeniería perduran más allá del modelo de turno, y que la responsabilidad de lo irreversible se mantiene humana) encuentra respaldo indirecto pero consistente en la literatura revisada: el hallazgo recurrente de resultados de productividad "mixtos y dependientes del contexto" (sección 5) es exactamente lo que predeciría una tesis centrada en arquitectura y no en capacidad del modelo, y es difícil de explicar bajo una tesis centrada solo en el modelo. La literatura no *prueba* la tesis de este libro (ninguna de las SLR citadas fue diseñada para probarla), pero tampoco la contradice, y en varios puntos (patrones de coordinación, crecimiento abrupto post-2023, sesgo hacia tareas verificables) la literatura documenta empíricamente fenómenos que este libro interpreta arquitectónicamente.
