# Cuaderno de lectura crítica

_Para qué sirve este cuaderno: este volumen hace afirmaciones sobre organizaciones, equipos y personas. Son afirmaciones más fáciles de discutir que las técnicas y, por eso, más fáciles de discutir mal. El cuaderno ofrece una rúbrica adecuada a ese tipo de afirmación, una plantilla de reseña y preguntas para los 25 capítulos._

## 1. Rúbrica para evaluar este volumen

| Criterio | La pregunta que usted debe poder responder | Señal de debilidad |
|---|---|---|
| Claridad de la audiencia | ¿Sé desde qué rol habla el capítulo (CTO, tech lead, PO, QA)? | Habla a todos a la vez y no sirve a ninguno |
| Traducibilidad a decisión | ¿Puedo convertirlo en una decisión con responsable y fecha? | Queda en buena intención sin mecanismo |
| Base empírica | ¿La afirmación sobre equipos se apoya en datos, en un caso o solo en analogía? | Analogía presentada como evidencia |
| Reconocimiento de contexto | ¿El capítulo dice en qué tipo de organización no aplica? | Se prescribe para toda organización |
| Riesgo de métrica | ¿Advierte de cómo la métrica puede pervertirse? | Convierte el indicador en objetivo |
| Vigencia normativa | ¿Sé qué parte depende de una regulación que puede cambiar? | Se cita la norma sin versión ni fecha |
| Utilidad como manual | ¿Puedo volver al capítulo por rol o por problema y encontrar la plantilla? | Falta la plantilla o la tabla de decisión |

**Advertencia que el propio volumen formula y que procede aplicar aquí.** Una práctica organizativa no se copia: se adapta. Al reseñar un capítulo de este tipo, la pregunta central no es «¿es verdad?» sino «¿en qué organización es verdad y en cuál produce el efecto contrario?».

## 2. Plantilla para redactar una crítica

1. **Rol del capítulo:** ¿a quién le habla y qué decisión le pide?
2. **Tesis en una frase:** «Este capítulo sostiene que ___ y lo justifica con ___».
3. **Tipo de evidencia:** dato, caso documentado, analogía o experiencia del autor. Nómbrelo.
4. **Contexto faltante:** ¿qué tipo de organización haría fracasar esta práctica?
5. **Veredicto con destinatario:** «le sirve a ___ en organizaciones ___ ; es contraproducente en ___ porque ___».

## 3. Preguntas de discusión por capítulo

### Gobierno y ética

**Capítulo 1. Ética y alineación en producción.**
1. ¿Qué obligación regulatoria de las que el capítulo cita ya aplica a su producto y no está en su backlog con responsable y fecha?
2. Crítica: ¿«construir una sola vez para el estándar más exigente» es siempre racional, o hay escenarios donde es coste puro sin mercado que lo pague?

**Capítulo 20. DevSecOps y permisos para agentes.**
1. ¿Qué permiso de agente existe hoy en su sistema sin haber pasado por revisión de seguridad? ¿Quién lo aprobó y con qué criterio?
2. Crítica: ¿el índice cuantificable de autonomía es interpretable sin arbitrariedad en los pesos, o dos equipos obtendrían números distintos del mismo sistema?

**Capítulo 21. Cada línea de código como responsabilidad.**
1. ¿Quién firma hoy una línea de código generada por un agente en su equipo, y qué significa esa firma en la práctica?
2. Crítica: ¿la taxonomía de responsabilidad agéntica es jurídicamente operativa o se queda en marco conceptual?

**Capítulo 15. RACI y Eisenhower con agentes.**
1. Cuando decide un agente, ¿quién es *accountable* en su organización? Si la respuesta es «el agente», ahí está el problema.
2. Crítica: ¿RACI aplicado a enjambres aclara la responsabilidad o la diluye detrás de una tabla más?

### Rol y competencia profesional

**Capítulo 2. El futuro, el Ingeniero Orquestador.**
1. De las cinco competencias del orquestador, ¿cuál falta más en su equipo y cómo la desarrollaría con un plan concreto?
2. Crítica: ¿el «nuevo contrato social de la ingeniería» es una descripción de lo que está pasando o un deseo del autor?

**Capítulo 8. Convertirte en maestro de agentes.**
1. ¿En qué nivel del modelo de madurez agéntica está usted y qué evidencia verificable lo demuestra?
2. Crítica: ¿el nivel 4 (diseñar evaluaciones propias) es alcanzable sin un equipo de plataforma detrás?

**Capítulo 9. Seis casos de liderazgo técnico.**
1. ¿Qué riesgo técnico de su equipo no está traducido al idioma del negocio, y a quién le corresponde traducirlo?
2. Crítica: ¿el coste del liderazgo técnico débil está cuantificado con rigor o estimado con plausibilidad?

**Capítulo 10. Gestión de expectativas y tiempos de la IA.**
1. ¿Qué expectativa de plazo debe corregir hoy, y con qué dato de su propio equipo la corrige?
2. Crítica: ¿las «nuevas curvas de tiempo» se sostienen con evidencia reproducible o con anécdota bien contada?

**Capítulo 13. El síntoma del programador cansado.**
1. ¿Qué señal de degradación contextual muestra su enjambre (repite, olvida, se contradice) y cómo la instrumentaría?
2. Crítica: ¿la analogía con la neurociencia de la fatiga aporta poder explicativo o solo retórica?

### Práctica de equipo

**Capítulo 6. Plantillas para proyectos con multiagentes como equipos.**
1. ¿Qué ceremonia de su equipo sobrevive hoy sin propósito claro, y qué la reemplazaría si el enjambre asumiera su función?
2. Crítica: ¿tratar el ágil como «arquitectura de coordinación» del enjambre es una metáfora útil o una analogía forzada?

**Capítulo 7. El ecosistema de desarrollo equiparado al del negocio.**
1. ¿Dónde está su brecha de velocidades entre técnica y negocio, y qué patrón just-in-time podría cerrarla?
2. Crítica: ¿las métricas DORA aplicadas al enjambre miden lo mismo que en un equipo exclusivamente humano?

**Capítulo 22. Comenzar por MVPs.**
1. ¿Cuál es la pregunta que su MVP debe responder, y qué resultado la respondería sin ambigüedad?
2. Crítica: ¿el marco RACE añade algo a un MVP clásico bien planteado, o solo renombra pasos conocidos?

**Capítulo 23. Casos de roles en agentes de IA.**
1. ¿Qué patología concreta evita hoy la separación de roles en su enjambre? Si no evita ninguna, revise el diseño.
2. Crítica: ¿el mapeo de roles organizacionales a arquetipos agénticos es útil o antropomorfiza el sistema sin ganancia?

**Capítulo 24. SOLID para agentes y ecosistemas.**
1. ¿Qué principio SOLID falta en su enjambre y qué deuda concreta está generando su ausencia?
2. Crítica: ¿«SOLID importa más en enjambres» aporta evidencia nueva o reafirma un principio conocido?

**Capítulo 25. Rescatar la agilidad.**
1. ¿Qué ritual de su equipo mide actividad en lugar de valor? ¿Lo eliminaría o lo reemplazaría por uno que mida valor?
2. Crítica: ¿la tesis de que la agilidad «fue capturada» describe un hecho o romantiza un pasado idealizado?

### Fundamentos de decisión

**Capítulo 4. Defender una arquitectura ante un comité.**
1. ¿Qué pregunta del comité no sabría responder hoy sobre su propuesta de multiagentes?
2. Aplique el método ATAM al caso: ¿qué *trade-off* crítico no había escrito antes de leer el capítulo?

**Capítulo 11. Un llamado a reinventarse.**
1. ¿Qué supuesto cognitivo de su equipo es preciso inventariar antes de reiniciar un proyecto?
2. Crítica: ¿«optimizar no es reinventar» es una afirmación falsable o una máxima sin consecuencia operativa?

**Capítulo 12. La lucha entre agentes: el sistema vence al modelo.**
1. ¿Qué decisión suya cambió por arquitectura del sistema en lugar de por cambiar de modelo?
2. Crítica: ¿el capítulo demuestra su tesis con benchmarks o solo la ilustra con casos favorables?

**Capítulo 16. PMBOK y los nuevos avances.**
1. ¿Qué parte del PMBOK aporta memoria útil en su contexto y cuál es burocracia pura?
2. Crítica: ¿el «núcleo irreductiblemente humano» que propone el capítulo es verificable o es una declaración de fe?

**Capítulo 18. Guía para no perderse en el ecosistema.**
1. ¿Cuál es su disciplina de «no adoptar» y quién la ejerce con autoridad en su organización?
2. Crítica: ¿las tres preguntas-brújula bastan para decidir en un campo que cambia cada mes?

**Capítulo 19. Ideas para generar ingresos.**
1. ¿Cuál de los cuatro arquetipos de monetización tiene foso defensivo real en su caso, y por qué?
2. Crítica: ¿«validar barato con un MVP agéntico» funciona cuando la propuesta de valor exige precisión alta desde el inicio?

### Casos aplicados

**Capítulo 3. Multiagentes ante El Niño.**
1. ¿Qué capa de esa arquitectura de cuatro capas es trasladable a su dominio de riesgo, y cuál no?
2. Crítica: ¿el capítulo demuestra la fiabilidad del sistema bajo presión o la argumenta?

**Capítulo 5. Descubriendo los bugs del software.**
1. ¿Qué fallo de su sistema es epistemológico (no se detecta porque nadie pregunta) y no puramente técnico?
2. Crítica: ¿el ROI del bug no encontrado está cuantificado con datos o estimado por plausibilidad?

**Capítulo 14. Katas de agentes.**
1. Diseñe una kata interna: objetivo, restricción y criterio de éxito evaluable.
2. Crítica: ¿la competición mejora la competencia real o entrena a optimizar la métrica de la competición?

**Capítulo 17. Enseñanzas de agentes de IA.**
1. ¿Qué explicaría usted a un junior para probar que entendió un patrón? Escríbalo en cinco líneas.
2. Crítica: ¿el principio de Feynman es aplicable a sistemas completos o solo a conceptos aislados?

## 4. Autoevaluación de comprensión

Marque lo que puede explicar **sin volver al texto**; lo que no marque es su lista de relectura.

- [ ] Traducir un riesgo técnico al idioma de un CFO con cifras.
- [ ] Describir los niveles del modelo de madurez agéntica.
- [ ] Explicar por qué un agente no puede ser *accountable* de una decisión.
- [ ] Justificar cuándo un MVP agéntico debe frenar antes de tocar usuarios externos.
- [ ] Diferenciar optimización de reinvención.
- [ ] Decir qué mide DORA y qué NO mide en un enjambre.
- [ ] Diseñar una evaluación propia para un comportamiento probabilístico.
- [ ] Explicar por qué la separación de roles evita patologías en un enjambre.

## 5. Cómo citar y discutir este volumen

Las afirmaciones de este volumen son de tres clases: **marcos** (RACI, PMBOK, DORA, ATAM), **prácticas** (sprints con agentes, MVP agéntico, katas) y **juicios** del autor sobre el estado del sector. Los marcos se citan por su versión y su organismo; las prácticas, por el contexto en que funcionaron; los juicios, como opinión argumentada. Confundir los tres es el error que produce las malas críticas de los libros de gestión: exigir a un juicio la prueba de un dato, o tratar un marco como si fuera una ley.