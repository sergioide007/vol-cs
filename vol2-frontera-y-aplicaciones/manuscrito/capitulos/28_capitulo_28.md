# Capítulo 28: El fútbol y los multiagentes, donde emerge el futuro táctico

> *En el fútbol, 11 jugadores son 11 agentes. La táctica es emergencia agéntica; el entrenador, el orquestador.*

## El partido como sistema multiagente: formalización teórica

Conviene precisar qué se entiende aquí por "sistema multiagente" antes de aplicar el término al fútbol, porque la conexión no es metafórica: es estructural. Un sistema multiagente, en la definición canónica de Wooldridge y Jennings (1995), es un sistema compuesto por múltiples agentes autónomos que perciben su entorno, razonan sobre sus percepciones y actúan de forma coordinada (o competitiva) para alcanzar objetivos individuales o colectivos. Un partido de fútbol satisface cada uno de esos criterios con una precisión que la mayoría de los sistemas de software artificiales no alcanza.

Cada jugador es un agente que: (a) percibe el entorno (posición del balón, posiciones de compañeros y rivales, estado del marcador, tiempo restante); (b) mantiene un modelo interno del mundo (expectativas sobre el comportamiento del entrenador rival, conocimiento de las fortalezas de sus compañeros, comprensión de las restricciones del sistema táctico); (c) toma decisiones en tiempo real bajo presión temporal severa (la ventana de decisión de un jugador de élite se mide en fracción de segundo *[orden de magnitud]: el análisis con tracking optical recoge muestras a alta frecuencia precisamente porque el humano no alcanza a processar cada cuadro, pero la magnitud de la decisión no se cita aquí porque depende del sport, la posición y el nivel; midasela en su propio equipo]*); y (d) coordina con otros agentes del mismo equipo a través de protocolos implícitos, el lenguaje táctico compartido que define qué hace el extremo izquierdo cuando el pivote recibe con presión desde atrás.

Esta formalización no es trivial. Implica que las herramientas teóricas desarrolladas para sistemas multiagente artificiales (teoría de juegos, protocolos de consenso, MARL) son *directamente aplicables* al análisis y optimización táctica del fútbol, no como analogías sino como marcos formales.

## La capa de datos: del evento al tracking biomecánico

El análisis de fútbol ha atravesado tres generaciones de datos que corresponden, no casualmente, a las tres generaciones del análisis multiagente.

**Primera generación: datos de evento.** Hasta aproximadamente 2012, el análisis estándar se basaba en datos de evento: pases completados, tiros a puerta, distancias recorridas, faltas cometidas. Estos datos capturan *qué* ocurrió, no *cómo* ni *por qué*. Son equivalentes al nivel de log de aplicación en sistemas de software: útiles para diagnóstico post-mortem, insuficientes para inferencia causal.

**Segunda generación: tracking 2D.** Entre 2012 y 2020, ligas de élite (en particular la Premier League, la Bundesliga y la Serie A) comenzaron a desplegar sistemas de tracking óptico que registran la posición de cada jugador y del balón a 25 frames por segundo. La empresa Tracab (ChyronHego), Second Spectrum y Stats Perform lideran este segmento. Con datos de tracking 2D, es posible computar métricas que los datos de evento no pueden capturar: velocidad de presión, espacio disponible en el momento del pase, cobertura defensiva en función de la posición de todos los jugadores simultáneamente. El dataset público más utilizado en investigación académica, el publicado por Pappalardo et al. (2019) en *Scientific Data* de la editorial Nature: proporciona eventos espaciotemporales de cinco ligas europeas y ha sido descargado más de 50.000 veces desde su publicación.

**Tercera generación: tracking biomecánico y multimodal.** En 2023-2025, un número reducido de clubes (entre los que se documentan Liverpool FC, Manchester City y Bayern Munich) ha comenzado a experimentar con sistemas que combinan tracking óptico con datos biomecánicos de GPS avanzado y acelerómetros corporales. Con estos datos, la unidad de análisis deja de ser la posición en el campo y pasa a ser el *estado fisiológico y cognitivo del agente*: nivel de fatiga muscular, patrón de aceleración/desaceleración, respuesta a estímulos visuales. La consecuencia analítica es sustancial: es posible predecir cuándo un agente está cognitivamente sobrecargado antes de que su rendimiento visible degrade.

## La arquitectura técnica: MARL en el campo de juego

**► PISTA TÉCNICA**


### Agentes de visión: tracking en tiempo real

La primera capa del sistema de análisis agéntico es el *agente de visión*: un modelo de visión computacional que, a partir del flujo de video o de sensores de tracking, extrae la posición y el estado de cada jugador en tiempo real. En implementaciones de producción (como las desplegadas por Stats Perform en la Premier League) este agente procesa 25 frames por segundo con latencia inferior a 40 milisegundos, lo que permite análisis verdaderamente en tiempo real durante el partido.

La complejidad técnica no está en la detección de jugadores (un modelo YOLO o similar puede hacer eso) sino en la *identificación persistente*: mantener la identidad del jugador #7 a través de oclusiones, colisiones visuales entre jugadores y cambios de cámara. Esa persistencia de identidad es el problema de tracking multi-objeto (MOT), y su resolución es el prerrequisito para cualquier análisis táctico significativo.

### Agentes de decisión: razonamiento sobre espacio y posesión

Sobre los datos de tracking, una segunda capa de agentes razona sobre conceptos tácticos de nivel superior: espacio, presión, líneas de pase disponibles, zonas de cobertura defensiva. El trabajo seminal de Fernández y Bornn (2018), *Wide Open Spaces: A statistical technique for measuring space creation in professional soccer*, formaliza la noción de "espacio de influencia" de cada jugador como una función de su posición, velocidad y la posición de todos los demás agentes en el campo. Esta métrica (denominada PITCH control en la literatura) permite cuantificar en tiempo real qué fracción del campo controla cada equipo, y cómo cambia esa distribución con cada movimiento.

La extensión agéntica de este trabajo consiste en convertir el cálculo de PITCH control en un agente reactivo que actualiza su estado en cada frame: el *agente de control espacial* que produce, en tiempo real, un mapa de calor de influencia táctica. Combinado con el *agente de presión* (que cuantifica cuánto tiempo tiene el poseedor del balón antes de ser presionado, basándose en las velocidades y posiciones de los defensores) estos agentes producen una descripción cuantitativa del estado táctico del partido que ningún analista humano puede computar en tiempo real.

### El agente de valoración de acciones: más allá del gol

La métrica más poderosa del análisis multiagente de fútbol es la *valoración de acciones*: cuánto valor añade o resta cada acción individual a la probabilidad de marcar gol. El paper de Decroos et al. (2019), *Actions Speak Louder Than Goals: Valuing Player Actions in Soccer* (publicado en KDD 2019, la conferencia más selectiva de minería de datos), introduce el framework VAEP (Valuing Actions by Estimating Probabilities) que cuantifica el valor de cualquier acción (no solo goles y asistencias) en términos de cambio en la probabilidad de marcar o encajar.

La arquitectura del sistema VAEP es multiagente en su estructura: un agente de contexto extrae características del estado del juego antes y después de cada acción; un agente de valoración computa el cambio en probabilidad de gol; un agente de atribución asigna ese cambio al jugador que realizó la acción. La composición de estos agentes produce una descripción cuantitativa de *quién contribuyó qué y cuándo*, con precisión que ningún sistema de estadísticas convencional puede replicar.

## Casos documentados: clubes que ya despliegan multiagentes

### Liverpool FC: el departamento de investigación como ventaja competitiva

Liverpool FC ha construido a lo largo de la última década un departamento de investigación y análisis que, en la industria del fútbol, es reconocido como la referencia en aplicación de ciencia de datos a decisiones deportivas. El trabajo de Ian Graham (matemático con doctorado en física computacional de Cambridge) como Director of Research del club entre 2012 y 2022 estableció una metodología basada en modelos probabilísticos para evaluación de jugadores, análisis táctico y preparación de rivales.

El sistema de análisis de Liverpool no es multiagente en el sentido técnico estricto de un pipeline de agentes de software. Es multiagente en el sentido organizacional: múltiples agentes analíticos humanos y algorítmicos que operan sobre datos compartidos, producen análisis independientes y los sintetizan en recomendaciones al cuerpo técnico. La separación entre el agente de análisis táctico (que analiza patrones de juego del rival) y el agente de valoración de jugadores (que evalúa el mercado de transferencias) (con síntesis realizada por un orquestador humano) es estructuralmente idéntica al patrón de arquitectura multiagente descrito en el capítulo 8.

### StatsBomb: la empresa que convirtió los datos en conocimiento agéntico

StatsBomb (fundada en 2012 por Ted Knutson) ha construido la base de datos de eventos de fútbol de mayor resolución disponible públicamente. El modelo de datos de StatsBomb captura no solo el tipo de evento (pase, disparo, tackle) sino su contexto táctico: parte del cuerpo utilizada, posición 3D del balón en el momento del impacto, indicador de presión sobre el poseedor, patrón de movimiento previo al pase. Esta granularidad transforma cada evento en un vector de estado que puede alimentar directamente un modelo MARL.

La investigación académica que ha utilizado datos de StatsBomb incluye trabajos publicados en KDD, NeurIPS workshops de sports analytics y la MIT Sloan Sports Analytics Conference. El acceso público a datos de la Copa del Mundo femenina y competiciones de selecciones nacionales ha permitido a investigadores de múltiples universidades desarrollar y comparar modelos de análisis táctico de forma reproducible, un estándar de rigor que el análisis de fútbol tradicional nunca había alcanzado.

### Bayern Munich: gemelo digital de la táctica

Bayern Munich, en colaboración con tecnología de SAP, ha desarrollado un sistema de análisis táctico que los propios materiales del club denominan "digital twin of tactics": una representación computacional del sistema táctico del equipo que permite simular cómo respondería el sistema a variaciones, nuevas posiciones iniciales, sustituciones, cambios de formación del rival. Esta simulación es, en esencia, un sistema multiagente: cada jugador es representado por un agente con un modelo de comportamiento aprendido de datos históricos, y la táctica emerge de la interacción de esos agentes en la simulación.

## Multi-Agent Reinforcement Learning (MARL): el estado de la investigación

El estado del arte en MARL aplicado a deportes colectivos fue establecido de forma definitiva por el trabajo de Vinyals et al. (2019), *Grandmaster Level in StarCraft II Using Multi-Agent Reinforcement Learning* (publicado en *Nature*, volumen 575), donde una arquitectura multiagente basada en aprendizaje por refuerzo alcanzó nivel de grandmaster en StarCraft II (un juego estratégico de información imperfecta con dinámica de equipos) sin heurísticas diseñadas por expertos. Las lecciones de ese trabajo son directamente transferibles al análisis de fútbol: los desafíos de coordinación entre unidades, exploración del espacio de estrategias y generalización a rivales no vistos durante el entrenamiento son estructuralmente equivalentes en ambos dominios.

El framework QMIX de Rashid et al. (2018) (publicado en *ICML 2018*) establece cómo factorizar el Q-valor de un enjambre en Q-valores individuales de forma que la política centralizada sea consistente con la ejecución descentralizada. Esta arquitectura (denominada CTDE, Centralized Training with Decentralized Execution) es directamente relevante para el análisis de fútbol: el modelo se entrena con acceso a todos los datos (tracking completo de todos los jugadores), pero en tiempo de inferencia cada agente decide basándose solo en su observación local.

El trabajo de Lowe et al. (2017), *Multi-Agent Actor-Critic for Mixed Cooperative-Competitive Environments* (NeurIPS 2017), extiende el actor-critic clásico a entornos con agentes que son simultáneamente cooperativos (con compañeros) y competitivos (con rivales), exactamente la dinámica de un partido de fútbol. Los gradientes de política aprendidos en ese framework capturan el equilibrio entre maximizar el beneficio individual del agente y contribuir al éxito colectivo del equipo, lo que en fútbol se manifiesta como la tensión entre el jugador que busca la gloria individual del gol y el que hace el pase al compañero mejor posicionado.

## La perspectiva ejecutiva: valorización de jugadores y gestión de riesgo

**■ PISTA EJECUTIVA**


Desde la perspectiva del liderazgo organizacional, el análisis multiagente de fútbol tiene implicaciones de negocio cuantificables que van más allá de la mejora del rendimiento deportivo.

**Valorización de mercado.** Los modelos de valoración de acciones (VAEP, Expected Threat, Expected Goals) han transformado el mercado de transferencias. Un club que puede cuantificar con precisión el valor real de un jugador (separando la contribución individual del sistema táctico en el que opera) posee ventaja de información en las negociaciones de transferencia. El retorno de inversión de estas capacidades analíticas ha sido documentado: los clubes que adoptaron analytics de datos avanzados antes de 2015 mostraron un rendimiento de mercado de transferencias sistemáticamente superior al promedio de su liga durante el período 2015-2022 (análisis documentado por la empresa 21st Club).

**Gestión de riesgo de lesiones.** Los datos biomecánicos de alta frecuencia permiten identificar patrones de fatiga muscular que preceden las lesiones musculares en 3-7 días. Un sistema de agentes que monitorea el estado fisiológico de cada jugador y genera alertas preventivas no solo reduce el riesgo de lesión, reduce el riesgo de ausencia de un activo valorado en decenas de millones de euros en el momento crítico de la temporada. Este es el caso de uso donde el ROI del analytics de fútbol avanzado es más directamente cuantificable.

**Preparación táctica como ventaja asimétrica.** Un equipo con capacidad de simular 10.000 variaciones de la táctica del rival en 24 horas (basándose en datos de tracking y modelos multiagente de los jugadores rivales) llega a cada partido con una preparación táctica que el equipo rival, sin esas capacidades, no puede igualar. Esta asimetría de preparación, multiplicada sobre una temporada de 38 partidos, produce diferencias acumuladas de rendimiento que se traducen en posiciones de tabla. En la Premier League, la diferencia entre clasificar para Champions League y no hacerlo equivale a ingresos adicionales de 50-100 millones de euros por temporada.

## El fútbol como laboratorio de decisión bajo incertidumbre distribuida

La dimensión más profunda de la conexión entre fútbol y multiagentes trasciende el análisis deportivo: el fútbol es el laboratorio más accesible, más observado y más documentado para el estudio de la *toma de decisiones distribuida bajo incertidumbre severa con restricciones temporales extremas*.

Las organizaciones empresariales enfrentan exactamente la misma estructura de problema: múltiples actores con información parcial, que deben coordinarse para alcanzar un objetivo colectivo, en un entorno dinámico donde el adversario también se adapta, con ventanas de decisión que no permiten análisis exhaustivo. Las empresas que estudian el fútbol como modelo de coordinación distribuida (no como entretenimiento, sino como sistema formal) obtienen insights transferibles a diseño organizacional, gestión de crisis y arquitecturas de decisión.

Equipos de consultoría estratégica han comenzado a usar análisis de partidos de fútbol como metodología de diagnóstico organizacional: la forma en que un equipo de fútbol responde a la pérdida del balón (presión inmediata vs. repliegue ordenado) es estructuralmente análoga a la forma en que una organización responde a una crisis de mercado. Los patrones son formalmente equivalentes. Los aprendizajes son transferibles.

## Lo esencial del capítulo 28

- Un partido de fútbol satisface la definición formal de sistema multiagente: 11 agentes autónomos por equipo que perciben, razonan y coordinan bajo protocolos implícitos en tiempo real.
- La generación de datos de tracking 2D y biomecánico ha convertido el campo de juego en el entorno multiagente más rico en datos del mundo, con 25 frames/segundo de estado completo del sistema.
- Los frameworks MARL (QMIX, MADDPG) y los modelos de valoración de acciones (VAEP) son directamente aplicables al análisis táctico; la investigación académica en KDD, NeurIPS y *Nature* valida esa aplicabilidad.
- Liverpool, StatsBomb y Bayern Munich representan casos documentados de implementación de análisis agéntico: separación de responsabilidades entre agentes especializados, síntesis orquestada, retroalimentación continua.
- La perspectiva ejecutiva: valorización de mercado, gestión de riesgo de lesiones y preparación táctica son los tres dominios donde el ROI del análisis multiagente de fútbol es más directamente cuantificable.
- El fútbol es el laboratorio más accesible para el estudio de coordinación distribuida bajo incertidumbre, con transferencia directa a diseño organizacional y arquitecturas de decisión empresarial.
