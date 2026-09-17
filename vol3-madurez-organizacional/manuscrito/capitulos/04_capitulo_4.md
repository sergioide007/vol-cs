# Capítulo 4: Cómo Defender una Arquitectura de Multiagentes ante un Comité: Viabilidad, Costos, Benchmarking y la Parte Agéntica de la Crítica Constructiva

> *Una arquitectura no se aprueba por ser elegante, sino por ser defendible bajo presión.*

---

## Sección 1: Lo que el Comité Compra en Realidad

Existe un malentendido estructural que reaparece en casi todas las presentaciones de arquitecturas de IA ante comités ejecutivos o comités de arquitectura empresarial: el presentador habla de tecnología; el comité decide sobre otra cosa. Cuando un director de tecnología escucha "arquitectura multiagente con orquestación por eventos", lo que procesa no es el detalle técnico. Lo que procesa es: ¿qué pasa si falla?, ¿cuánto cuesta si escala?, ¿quién tiene la culpa si el sistema alucina?

Bass, Clements y Kazman (2022), en la cuarta edición de *Software Architecture in Practice* (referencia canónica del campo, con más de 15,000 citas acumuladas en Google Scholar), formulan una taxonomía de atributos de calidad que los tomadores de decisión evalúan implícitamente: disponibilidad, modificabilidad, seguridad, rendimiento y, sobre todo, **mantenibilidad y trazabilidad**. Un comité no compra tokens; compra certidumbre sobre esos cinco atributos.

La primera maniobra estratégica, en consecuencia, consiste en **traducir cada decisión técnica a la moneda de los tres R del comité**: Riesgo, Retorno y Reversibilidad. No "usamos Kafka para desacoplar los agentes temporalmente", sino "si un agente falla, el resto del sistema no se detiene (eso es lo que Kafka nos da)". No "fine-tuneamos el modelo en datos propios", sino "el modelo no puede revelar información de otros clientes porque nunca los ve (ese es el boundary)".

| Decisión técnica | Traducción al idioma del comité |
|-----------------|--------------------------------|
| Arquitectura hexagonal con puertos | Si el modelo de IA mejora, lo cambiamos sin tocar el núcleo de negocio. Tiempo de migración: días, no meses. |
| MCP para acceso a APIs externas | El agente nunca maneja credenciales. Si el agente es comprometido, no tiene llaves. |
| Kafka como bus de eventos | Falla un agente: los demás siguen. No hay punto único de falla. |
| Evaluadores (LLM-judges) | Antes de que una respuesta llegue al usuario, es verificada por una segunda capa. El humano solo ve salidas validadas. |
| Graceful degradation | Si la IA está indisponible, el sistema vuelve al flujo manual. No caemos; bajamos. |

---

## Sección 2: El Método ATAM Aplicado a Sistemas Multiagente

La Architecture Tradeoff Analysis Method (ATAM), desarrollada en el Software Engineering Institute de Carnegie Mellon ([Kazman, Klein & Clements, 2000](#ref-kazman2000)), es el marco más riguroso disponible para evaluar decisiones arquitectónicas antes del deployment. Fue diseñada para sistemas críticos de misión (defensa, aviación, telecomunicaciones) y su aplicación a sistemas multiagente de IA resulta tanto pertinente como reveladora.

El proceso ATAM se estructura en cuatro pasos que, adaptados al contexto agéntico, producen el artefacto más valioso que cualquier arquitecto puede llevar a un comité: **un mapa completo de tradeoffs con su costo explícito**.

**Paso 1: Presentar el driver arquitectónico.** ¿Cuál es el atributo de calidad que más importa? Para un sistema de soporte al cliente con IA, es probablemente disponibilidad y latencia. Para un sistema de compliance financiero, es auditoría y trazabilidad. Para un sistema de gobernanza de desastres (Cap. 23), es confiabilidad y tiempo de respuesta. El error frecuente: no jerarquizar, y presentar "queremos que sea rápido, seguro, escalable y barato" (que es decir nada).

**Paso 2: Identificar los escenarios de atributo de calidad.** Un escenario de atributo de calidad tiene la forma: "Bajo condición X, el sistema debe hacer Y en Z tiempo/costo/probabilidad". Ejemplos:
- "Cuando el tráfico se triplica en 30 minutos (pico de ventas), el agente de clasificación debe mantener latencia P99 < 2 segundos."
- "Cuando el modelo de IA produce una respuesta que viola la política de privacidad, el evaluador debe detectarla y descartarla antes de que llegue al usuario en el 99.5% de los casos."
- "Si el servicio de inferencia falla, el sistema debe degradar a respuestas pre-computadas en menos de 5 segundos."

**Paso 3: Mapear los riesgos y sensibilidades arquitectónicas.** Cada decisión de diseño tiene un punto de sensibilidad (cambio pequeño = impacto grande) y puntos de tradeoff (ganar en un atributo = perder en otro). La tabla ATAM hace esto explícito. Para el comité, esta tabla es invaluable: demuestra que el arquitecto ha pensado en los fallos, no solo en el camino feliz.

| Decisión de diseño | Riesgo | Beneficio | Tradeoff |
|-------------------|--------|-----------|----------|
| Modelos en la nube (vs. on-premise) | Latencia variable, egreso de datos sensibles | Sin CAPEX de GPU, actualizaciones automáticas | Latencia P99 aumenta 80ms vs. on-premise |
| Fine-tuning vs. RAG | Fine-tuning: costo inicial alto, rigidez | Fine-tuning: latencia <50ms, sin overhead retrieval | RAG más flexible pero +50ms latencia retrieval |
| Un orquestador central vs. coreografía por eventos | Orquestador: punto único de falla | Coreografía: resiliencia por diseño | Coreografía = mayor complejidad de debugging |
| Evaluador humano-en-el-loop vs. automático | Humano: lento, no escala | Automático: <1ms latencia | Automático: 2-5% de falsos negativos iniciales |

**Paso 4: Presentar el análisis de riesgo.** El comité recibe tres columnas: Riesgo identificado, Probabilidad (estimada con historial de incidentes en sistemas análogos), y Plan de mitigación. Este paso convierte la presentación en una conversación de gestión de riesgos (el lenguaje nativo del comité).

---

## Sección 3: El Panel de Agentes Críticos: Estresar la Propuesta Antes de la Sala

He aquí la innovación que diferencia esta aproximación de la preparación convencional. En lugar de ensayar la presentación frente a un colega complaciente, se despliega un **panel de agentes críticos sintéticos** (cada uno encarnando un arquetipo del comité) que someten la propuesta a interrogatorio antes de que la presente un humano con poder de veto.

Los arquetipos del panel:

**Agente CFO.** Su preocupación central: TCO a 3 años y punto de equilibrio. Preguntas típicas: "¿Cuándo el costo de los tokens supera el ahorro en trabajo manual?", "¿Qué ocurre con el costo si el volumen se triplica?", "¿Hay costos ocultos en el operación (monitoreo, actualizaciones de modelos, retraining)?". Su función es encontrar el escenario económico donde la propuesta se quiebra.

**Agente de Seguridad.** Busca superficies de ataque que el arquitecto no mencionó: "¿Qué impide una inyección de prompt desde los datos de entrada?", "¿Cómo auditamos las decisiones del agente para cumplimiento regulatorio?", "¿Dónde viven las credenciales de las APIs externas?", "¿Qué ocurre si el modelo alucinan y la salida se persiste en la base de datos?"

**Agente Escéptico Tecnológico.** Cuestiona la madurez: "¿Esto está en producción en empresas de nuestro sector y tamaño?", "¿Qué pasa cuando el proveedor del modelo cambia sus precios o depreca la API?", "¿En cuántos meses podemos revertir si no funciona?", "¿Cuál es el riesgo de vendor lock-in?"

**Agente de Negocio.** Exige impacto cuantificado: "¿Cuántos tickets por mes resuelve sin humanos?", "¿Cuál es el CSAT esperado vs. el actual?", "¿En qué mejora específicamente la experiencia del cliente?", "¿Cómo medimos el éxito en los primeros 90 días?"

**El proceso**: el arquitecto presenta la propuesta; los cuatro agentes generan objeciones simultáneamente; el arquitecto las responde; los agentes escalan si la respuesta es insuficiente. La sesión termina cuando los cuatro agentes clasifican la propuesta como "defendible" (no perfecta, sino defendible).

Lo que emerge de este proceso no es una propuesta pulida que oculta los riesgos. Es una propuesta honesta que muestra los riesgos *y sus mitigaciones*. Esa honestidad es, paradójicamente, lo más persuasivo que puede llevar un arquitecto a una sala.

---

## Sección 4: Benchmarking Honesto: Comparar para Convencer, No para Impresionar

**► PISTA TÉCNICA**


El benchmarking no es vanidad técnica. Es la herramienta retórica más poderosa ante un comité porque convierte intuiciones en argumentos cuantificados y comparaciones en decisiones. Pero el benchmarking deshonesto (que solo muestra los escenarios donde el sistema gana) destruye la credibilidad en el momento en que el comité hace la pregunta que el presentador omitió.

**Principio de benchmarking honesto**: mostrar los tres escenarios (en el que el sistema gana, en el que empata, y en el que pierde), con la condición de cada uno.

Ejemplo para un sistema multiagente de soporte al cliente:

| Métrica | Sistema actual (humanos) | Agente IA | Orquestación multiagente | Cuándo multiagente pierde |
|---------|--------------------------|-----------|--------------------------|--------------------------|
| Tickets resueltos/hora | 12 | 45 | 78 | Nunca en volumen puro |
| Costo por ticket | $8.50 | $1.20 | $2.10 | En volumen <200 tickets/día |
| Satisfacción cliente (CSAT) | 4.2/5 | 3.8/5 | 4.4/5 | En tickets complejos emocionales |
| Tiempo de primera respuesta | 8 min | 12 seg | 8 seg | Nunca en velocidad |
| Tasa de escalada a humano | 35% | 28% | 9% | Nunca en autonomía |
| Precisión en temas regulatorios | 94% | 72% | 91% | En dominios no entrenados |

La columna "cuándo pierde" es la más importante. Un comité que ve esa columna confía en las otras. Un comité que no la ve sospecha de las otras.

**Benchmarking de arquitectura vs. línea base y vs. alternativas:**

No comparar solo contra "el sistema actual". Comparar contra: (a) el sistema actual, (b) la alternativa monolítica (un único agente grande), y (c) la arquitectura propuesta. Esto demuestra que la decisión de multiagentes fue considerada frente a la alternativa más simple, y fue elegida por razones específicas, no por moda.

---

## Sección 5: La Narrativa de Control: Cómo Cerrar la Defensa

Una defensa arquitectónica exitosa no cierra con "y en conclusión, es la mejor solución". Cierra con una **narrativa de control**: el sistema es gobernable, reversible, y mejora mediblemente.

Los tres compromisos que el comité necesita escuchar (y que el arquitecto debe poder sostener con evidencia):

1. **Trazabilidad total.** "Cada decisión del agente es registrada con su input, su razonamiento, su output, y el tiempo. Si algo falla, sabemos exactamente qué pasó, en qué agente, con qué datos, a qué hora. No es una caja negra; es un sistema con logs estructurados y auditabilidad completa."

2. **Reversibilidad diseñada.** "Si el sistema no rinde como prometido en los primeros 90 días, tenemos un plan de rollback explícito: los flujos manuales siguen existiendo en paralelo durante los primeros 6 meses. El switch es operacional, no arquitectónico."

3. **Mejora medible.** "En el mes 1, midamos X. En el mes 3, midamos Y. En el mes 6, decidimos si expandir o no. No les pedimos un cheque en blanco; les pedimos 90 días de datos."

La narrativa de control es, en esencia, el reconocimiento de que la IA es probabilística y el sistema que la contiene debe ser determinístico en su gobernanza. El comité no compra la IA; compra el sistema que la gobierna.

---

## Versión académica ampliada

> *Reformulación de los conceptos centrales con densidad académica superior.*

La evaluación de arquitecturas de software en contextos de alta incertidumbre (como los sistemas multi-agente de inteligencia artificial) puede encuadrarse dentro del paradigma de la toma de decisiones bajo ambigüedad epistémica, formalizado por Ellsberg (1961) y aplicado al dominio de sistemas de información por Peppard & Ward (2004) en *Strategic Planning for Information Systems*. Desde esta perspectiva, los atributos de calidad arquitectónica son construcciones socio-técnicas que emergen de la negociación entre stakeholders con modelos mentales divergentes y horizontes temporales distintos, no propiedades objetivas del sistema.

El método ATAM (Architecture Tradeoff Analysis Method), tal como fue formulado por Kazman et al. (2000) en su Technical Report del SEI, opera precisamente en este espacio de negociación: sus escenarios de atributos de calidad son instrumentos de elicitación que fuerzan la articulación explícita de las asunciones implícitas que cada stakeholder mantiene sobre el sistema. En el contexto específico de sistemas multi-agente, esta función de elicitación resulta especialmente valiosa, dado que la naturaleza emergente del comportamiento del enjambre, cuya caracterización formal fue establecida por Bonabeau, Dorigo & Theraulaz (1999) en *Swarm Intelligence: From Natural to Artificial Systems*, introduce una clase de incertidumbre aleatoria (no reducible por más información) que los marcos de evaluación tradicionales no contemplaban.

---

## Lo esencial del capítulo 4

- El comité no compra tecnología; compra los tres R: **Riesgo, Retorno y Reversibilidad**.
- Cada decisión técnica debe traducirse al idioma del comité antes de entrar a la sala.
- El método **ATAM** aplicado a sistemas multiagente produce el artefacto más valioso: un mapa completo de tradeoffs con costo explícito.
- Un **panel de cuatro agentes críticos** (CFO, Seguridad, Escéptico, Negocio) estresa la propuesta antes de que lo haga un humano con veto.
- El benchmarking honesto muestra el escenario donde el sistema pierde: esa columna construye credibilidad en las otras.
- La narrativa de cierre es una **narrativa de control**: trazabilidad, reversibilidad, mejora medible en 90 días.
- La IA es probabilística; el sistema que la gobierna debe ser determinístico en su auditabilidad.

---

## Ejercicio resuelto 4.1: Traduce un riesgo técnico al idioma del CFO

**Enunciado.** El CFO del comité pregunta: "Escuché que estos sistemas de IA 'alucinan'. ¿Qué significa eso para nosotros si un agente alucinada y ese error llega a un cliente?"

**Respuesta del arquitecto (traducción al idioma del CFO):**

"Una alucinación es cuando el modelo genera información que parece correcta pero no lo es. Sin controles, ese error llegaría al cliente. **Con nuestra arquitectura, hay tres capas antes de que eso ocurra:**

Primero, el modelo tiene un evaluador automático (LLM-judge) que compara su respuesta con las políticas de la empresa. Si la respuesta viola alguna política, es descartada y se genera una alternativa. Ese evaluador captura aproximadamente el 97% de las alucinaciones en dominios bien definidos.

Segundo, si la confianza del modelo está por debajo del 0.80 (lo cual indica incertidumbre alta), el sistema escala automáticamente a un agente humano. El cliente no ve la alucinación; ve una respuesta 'transfiriéndote con un especialista'.

Tercero, toda respuesta es registrada. Si una alucinación pasa los dos filtros anteriores y llega al cliente, podemos rastrear exactamente qué prompt la provocó, en qué contexto, y corregir el evaluador para que no vuelva a ocurrir.

El costo esperado de una alucinación que llegue al cliente en nuestro sistema: un ticket de soporte manual (que ya tiene hoy). La diferencia es que ahora sabemos exactamente qué ocurrió y podemos evitar que se repita."

Esta respuesta no prometió perfección (imposible). Prometió gobernanza medible y mejora continua. Eso es lo que un CFO puede aprobar.

---
