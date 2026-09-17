# Cuaderno de lectura crítica

_Para qué sirve este cuaderno: este es el volumen más heterogéneo de la serie —conviven en él ingeniería, análisis de industria y geopolítica—, y por eso es también el que más exige del lector. El cuaderno ofrece una rúbrica adaptada a esa mezcla, una plantilla de reseña y preguntas de discusión para los 32 capítulos._

## 1. Rúbrica para evaluar este volumen

| Criterio | La pregunta que usted debe poder responder | Señal de debilidad |
|---|---|---|
| Claridad del propósito | ¿Sé si este capítulo habla de ingeniería, de industria o de geopolítica, y a quién le sirve? | El capítulo cambia de registro sin avisar |
| Solidez de la evidencia | ¿El dato del mercado o del organismo citado es rastreable a una fuente primaria? | Cifra atribuida a «un informe» o a prensa secundaria |
| Frontera hecho/hipótesis | ¿Puedo distinguir lo que el autor documenta de lo que proyecta? | La proyección se presenta con el mismo tono que el hecho |
| Aplicabilidad | ¿Puedo convertir esto en una variable que mi organización modele? | Describe un país o una industria sin traducirlo a decisión |
| Vigencia | ¿Sé cuándo caduca y con qué lo verifico? | No se fecha el dato |
| Reconocimiento de límites | ¿El capítulo admite que su caso no es generalizable? | Se extrapola un ecosistema concreto a todo el sector |
| Utilidad como manual | ¿Puedo volver a este capítulo por país o por tema y encontrar la variable que busco? | El capítulo no tiene índice local ni tabla resumen |

**Aviso metodológico para el lector.** Este volumen mezcla, a propósito, razonamiento arquitectónico con análisis geopolítico que la literatura académica mantiene en silos disciplinarios distintos (lo señala el propio Estado del arte). Esa mezcla es su aportación y su riesgo: critíquela explícitamente, porque el autor la defiende como tesis, no como descuido.

## 2. Plantilla para redactar una crítica

1. **Clasifique el capítulo:** ¿ingeniería, industria, geopolítica o mixto?
2. **Tesis en una frase:** «Este capítulo sostiene que ___ y lo justifica con ___».
3. **Evidencia:** identifique el dato verificable y la proyección; no los trate igual.
4. **Hueco o sesgo:** ¿qué jurisprudencia, mercado o escenario alternativo falta?
5. **Veredicto con destinatario:** «le sirve a ___ para decidir ___ ; no debe usarse para ___ porque ___».

## 3. Preguntas de discusión por capítulo

### Bloque A — Ingeniería de frontera (caps. 1–14)

**Capítulo 1. Seguridad para agentes de IA.**
1. El capítulo sostiene que la amenaza interna es probabilística y que por eso el perímetro clásico no basta. ¿Qué control de su sistema asume todavía que la entrada es confiable?
2. Elija uno de los diez riesgos de OWASP LLM y localícelo en su arquitectura: ¿qué evidencia demuestra que está mitigado y no solo documentado en una política?

**Capítulo 2. Transformar intuiciones en sistemas.**
1. El capítulo describe una cadena que va del hallazgo casual al patrón canónico. ¿Qué intuición valiosa de su equipo sigue sin formalizar y qué coste tiene esa demora?
2. Crítica: ¿la defensa del explorador resiste la disciplina de una organización con auditoría y plazos, o el capítulo infravalora ese conflicto?

**Capítulo 3. Dónde buscar los eventos que dejan huella.**
1. ¿Qué conferencia o evento cambiaría de verdad una decisión técnica suya este año, y qué haría después para que no se quede en asistencia?
2. Crítica: ¿la taxonomía de eventos envejece rápido? ¿Sigue siendo útil cuando los nombres concretos caduquen?

**Capítulo 4. Programación reactiva multiagéntica.**
1. ¿Dónde tiene hoy acoplamiento sincrónico entre agentes, y qué latencia o fragilidad introduce?
2. El capítulo propone idempotencia, cola de mensajes muertos y límite de saltos. ¿Cuál de los tres falta en su sistema y cómo lo detectaría en producción?

**Capítulo 5. La nueva variable de la confianza.**
1. Complete la ecuación de confianza con la variable de verificabilidad, aplicada a su dominio: ¿cómo se mide concretamente?
2. ¿Su organización concede autonomía por convicción o por evidencia acumulada? ¿Qué evidencia tendría que existir para subir un nivel?

**Capítulo 6. Extensiones del pensamiento.**
1. Distinga una extensión de una sustitución en las herramientas que usa hoy. ¿Qué habilidad del equipo se está atrofiando mientras el agente la cubre?
2. Crítica: ¿es posible diseñar para la extensión y no para la dependencia cuando el proveedor optimiza exactamente lo contrario?

**Capítulo 7. Novedades de hace un año que aún se expanden.**
1. ¿Qué capacidad ya madura de su stack infrautiliza por ir detrás de la novedad?
2. Aplique el «reexamen deliberado» a un servicio propio: ¿qué mejoraría sin adoptar nada nuevo?

**Capítulo 8. Tutor de idiomas: arquitectura por dentro.**
1. El patrón Soporte-Evaluación separa a quien ayuda de quien juzga. ¿Dónde mezcla su sistema esas dos funciones en un mismo agente?
2. Crítica: ¿la arquitectura descrita es replicable sin el mismo volumen de datos y de usuarios que la sostiene?

**Capítulo 9. El cierre de conexiones aplicado a agentes.**
1. ¿Qué recurso abre un agente en su sistema y podría no cerrar: conexión, sesión, contexto, archivo, suscripción?
2. Crítica: la tesis es que «la abundancia anestesia la disciplina». ¿Tiene un contraejemplo en su equipo?

**Capítulo 10. Enseñar IA con multiagentes.**
1. ¿Qué salvaguarda del capítulo considera irrenunciable y quién la verifica en la práctica?
2. Crítica: ¿el capítulo aporta evidencia empírica suficiente o apela a plausibilidad pedagógica?

**Capítulo 11. Ciudades inteligentes.**
1. ¿Algún proyecto suyo se presenta como «inteligente» sin haber definido antes la forma nativa de su enjambre? ¿Qué falta?
2. Crítica: ¿el modelo de madurez urbano es trasladable a otros dominios o es específico de la ciudad?

**Capítulo 12. Arquitecturas híbridas.**
1. ¿Qué parte determinista debe sostener a la probabilística en su sistema, y está diseñada para eso?
2. Justifique la hibridación ante un CFO: ¿qué coste de «costura» está dispuesto a pagar y por cuánto tiempo?

**Capítulo 13. ¿Funcionalidad o estructura?**
1. ¿Qué deuda técnica específicamente agéntica reconoce en su sistema (la del capítulo, no la clásica)?
2. Crítica: ¿«la estructura gana a largo plazo» es una afirmación falsable? ¿Qué evidencia la respalda dentro del capítulo?

**Capítulo 14. La vigencia de los libros que debes leer.**
1. ¿Qué clásico le falta leer para no quedar atrapado en lo nuevo? ¿Qué le impediría entender de su propio sistema?
2. Crítica: ¿el criterio de «dieta híbrida» es aplicable a un equipo entero o solo a una persona?

### Bloque B — Industrias (caps. 15–16 y 28–32)

**Capítulo 15. Música en multiagentes.**
1. ¿Qué demanda la especialización por género musical y cómo se traduce en una decisión de arquitectura concreta?
2. Crítica: ¿el modelo de negocio creativo del capítulo resuelve el problema de propiedad intelectual o solo lo aplaza?

**Capítulo 16. Vídeo en multiagentes.**
1. ¿Por qué el vídeo fuerza una arquitectura distribuida y qué límite físico —no comercial— lo impone?
2. Crítica: ¿la gobernanza china descrita es replicable en su jurisdicción o es un caso único presentado como modelo?

**Capítulo 28. El fútbol y los multiagentes.**
1. ¿Qué laboratorio de decisión bajo incertidumbre distribuida tiene usted más cerca que el fútbol?
2. Crítica: ¿el aprendizaje por refuerzo multiagente está maduro para decidir en producción, o el capítulo promete más de lo que la evidencia sostiene?

**Capítulo 29. Cline y Continue.**
1. ¿Qué agente integrado en el IDE usa ya y qué le falta para no salir del editor?
2. Crítica: ¿los benchmarks y validaciones de impacto citados miden lo que el lector necesita decidir?

**Capítulo 30. Cursor, Windsurf y Zed.**
1. ¿Su elección de IDE es una decisión de plataforma o un gusto personal disfrazado de decisión técnica?
2. Crítica: ¿el dilema del ecosistema de extensiones está resuelto o el capítulo lo deja abierto sin advertirlo?

**Capítulo 31. Grok, Cody y Amazon Q.**
1. ¿Cuál es el criterio de selección que de verdad importa en su contexto y está escrito en algún sitio?
2. Crítica: ¿un mapa del ecosistema de herramientas puede sobrevivir más de un año? ¿Cómo debería consumirse este capítulo?

**Capítulo 32. Móvil, videojuegos 3D y realidad virtual.**
1. ¿Qué restricción física de su dominio cambia la arquitectura respecto a un sistema de agentes «de servidor»?
2. Crítica: ¿los tres dominios comparten base suficiente para unirlos en un mismo capítulo, o habría ganado el lector separándolos?

### Bloque C — Geopolítica y ecosistemas (caps. 17–27)

**Capítulo 17. China en la era multiagente.**
1. ¿Qué variable de su arquitectura depende hoy de decisiones chinas: costo, disponibilidad de chips, pesos abiertos, jurisdicción de datos?
2. Crítica: el capítulo pasa de dato verificable a proyección. ¿Dónde está exactamente la frontera y la traspasa en algún punto sin avisar?

**Capítulo 18. USA en agentes de IA.**
1. ¿Qué primitiva de la que depende su sistema nació en EE. UU. y qué riesgo implica depender de su estándar?
2. Después de leer sobre Constitutional AI y RLHF, ¿qué cambiaría en su forma de especificar la alineación de un agente?

**Capítulo 19. Europa en agentes de IA.**
1. ¿Su producto cumple el estándar más exigente al que podría enfrentarse, o solo el de su mercado actual?
2. Crítica: ¿el coste del cumplimiento es inversión, como afirma el capítulo, o hay escenarios donde es puro coste sin retorno?

**Capítulo 20. América Latina y África en multiagentes.**
1. ¿Qué vertical local suyo es ventaja competitiva real y no copia de un producto global?
2. Crítica: ¿el «salto posible» depende de condiciones que el capítulo afirma pero no demuestra?

**Capítulo 21. Australia: laboratorio geopolítico de confianza.**
1. ¿Qué papel juega la confianza como infraestructura en su organización y cómo la contabiliza?
2. Crítica: ¿es exportable el modelo australiano o depende de escala y geografía que el lector no tiene?

**Capítulo 22. Rusia: cuando las sanciones redefinen la arquitectura.**
1. ¿Qué enseña la restricción de cómputo sobre la eficiencia de su propio stack?
2. Crítica: ¿se puede analizar soberanía tecnológica sin tomar posición política? ¿El capítulo lo consigue?

**Capítulo 23. Taiwán: el nudo geopolítico.**
1. ¿Cuál es su plan concreto ante una disrupción de la cadena de silicio, y está escrito o solo intuido?
2. Crítica: ¿el capítulo modela el riesgo (con escenarios y probabilidades) o solo lo describe?

**Capítulo 24. Países Bajos: cuando la infraestructura es el arma.**
1. ¿Qué infraestructura de la que depende usted es un cuello de botella ajeno que no controla?
2. Crítica: ¿la lectura de ASML y del intercambio de Ámsterdam como «arma» es analítica o retórica?

**Capítulo 25. Japón: la fábrica del futuro.**
1. ¿Qué tarea de su operación está lista para pasar de automatización a autonomía, y qué la retiene?
2. Crítica: ¿la economía de escala agéntica se sostiene con los datos que el capítulo aporta?

**Capítulo 26. Melbourne: donde la experimentación redefinió el modelo.**
1. ¿Cómo mide la latencia de feedback en su equipo y qué decisiones cambia ese número?
2. Crítica: ¿el «modelo Melbourne» es replicable o es una serie de coincidencias bien narradas?

**Capítulo 27. Universidades: la próxima generación.**
1. ¿Qué debería enseñarse primero en su organización y en qué orden, según su propio cuello de botella?
2. Crítica: ¿el currículo propuesto forma para la industria o para la investigación? ¿A quién sirve cada uno?

## 4. Autoevaluación de comprensión

Marque lo que puede explicar **sin volver al texto**; lo que no marque es su lista de relectura.

- [ ] Diferenciar hecho verificable de proyección en un capítulo geopolítico.
- [ ] Explicar por qué la amenaza de un agente es interna y probabilística.
- [ ] Enunciar la variable que completa la ecuación de confianza.
- [ ] Nombrar las tres contramedidas estructurales frente a tormentas de eventos.
- [ ] Decir qué distingue una arquitectura híbrida de una puramente cloud.
- [ ] Explicar por qué el vídeo y el fútbol fuerzan arquitecturas multiagente distintas de un chatbot.
- [ ] Traducir un análisis de país en una variable que su organización deba modelar.
- [ ] Indicar qué parte de este volumen caduca y con qué la verificaría.

## 5. Cómo citar y discutir este volumen

Este volumen contiene tres tipos de afirmación que **no deben citarse igual**: el **principio de ingeniería** (por ejemplo, que la confianza es graduada), el **dato** (cifras de mercado, de coste, de norma) y la **proyección geopolítica**. Al citar, feche el dato, marque la proyección como hipótesis del autor y conserve el principio. Un lector que aplica esa separación puede usar el volumen durante años aunque las cifras y los mapas cambien: es exactamente la distinción que exige el Estado del arte de esta serie.
