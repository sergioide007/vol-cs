# Capítulo 3: Multiagentes de IA ante El Niño

> *No basta con predecir el desastre; hay que orquestar la respuesta antes de que el agua llegue.*

---

## Sección 1: La Anatomía del Problema: Más Allá de la Meteorología

El fenómeno de El Niño (y su variante costera, El Niño Costero, que golpea con particular violencia el litoral peruano) es, ante todo, un sistema complejo. No un evento singular, sino una cadena de causalidades entrelazadas: anomalías térmicas superficiales en el océano Pacífico central y oriental que, semanas después, se traducen en lluvias torrenciales, desbordamientos de ríos, huaicos, pérdida de cosechas y colapso de infraestructura sanitaria. El evento de 2017 generó daños estimados en más de 3,100 millones de dólares solo en Perú ([CENEPRED, 2017](#ref-cenepred2017)), cifra que el de 2023 amenazó con superar.

Ahora bien, el problema técnico de fondo no radica en la escasez de datos. Los satélites Sentinel-3 y GOES-East de la NASA/ESA, las más de 300 boyas oceanográficas del sistema Argo, las estaciones hidrometeorológicas del SENAMHI y los modelos de circulación oceánica del IGP producen, en conjunto, terabytes de información por hora. La fractura se produce en otro nivel: entre quien sabe, quien decide y quien actúa. Entre el científico que detecta la anomalía SST (sea surface temperature) en el Niño 3.4, el funcionario que debe decretar la alerta temprana, el alcalde que gestiona la evacuación y el logístico que mueve los recursos. Cada actor habita un silo institucional distinto, opera con un vocabulario técnico diferente y tiene incentivos que rara vez se alinean en tiempo real.

Cabe puntualizar que este problema es, en esencia, un problema de orquestación distribuida bajo incertidumbre. Y la orquestación distribuida bajo incertidumbre es, precisamente, el dominio para el que los sistemas multiagente fueron concebidos.

Rolnick et al. (2022), en su revisión exhaustiva publicada en *ACM Computing Surveys* (probablemente el artículo más citado de la intersección entre machine learning y cambio climático (más de 2,000 citas a la fecha de esta edición)), identificaron la coordinación inter-institucional como el cuello de botella principal en la respuesta a desastres climáticos, por encima incluso de la precisión predictiva. Dicho de otro modo: tener el modelo correcto no sirve si la cadena de decisión está rota.

| Dimensión del problema | Evidencia documentada | Implicación arquitectónica |
|------------------------|----------------------|---------------------------|
| Latencia de alerta | El Niño 2017: tiempo promedio entre detección SENAMHI y alerta INDECI: 72 horas | Necesitamos agentes que publiquen eventos en tiempo real, no informes periódicos |
| Fragmentación de datos | IGP, ANA, SENAMHI usan formatos incompatibles (NetCDF vs CSV vs APIs REST propias) | Capa de normalización obligatoria (agentes de percepción) |
| Toma de decisiones | COEN, COER y COEL toman decisiones en reuniones presenciales con datos de ayer | Capa de síntesis y recomendación con trazabilidad |
| Coordinación regional | Perú, Ecuador y Colombia gestionan la misma cuenca hidrográfica de forma desconectada | Federación de enjambres nacionales con interoperabilidad |

---

## Sección 2: Estado del Arte: IA Predictiva Aplicada a Fenómenos Climáticos

La predicción numérica del tiempo ha sido, durante décadas, el dominio exclusivo de modelos de circulación general (GCM) ejecutados en supercomputadoras de alta capacidad. Lo que ocurrió entre 2022 y 2024 alteró ese paradigma de forma estructural: los modelos basados en aprendizaje profundo comenzaron a superar a los GCM en precisión y en velocidad por márgenes que los investigadores del ECMWF describieron como "sorprendentes".

**FourCastNet** ([Pathak et al., 2022](#ref-generic2022kurth)): desarrollado por NVIDIA, este modelo de redes neuronales entrenado sobre datos del ERA5 (ECMWF Reanalysis v5) genera predicciones globales de hasta 7 días con una velocidad 45,000 veces superior a los modelos numéricos tradicionales, manteniendo una habilidad comparable. El umbral fue decisivo: por primera vez, la predicción meteorológica podía ejecutarse en dispositivos de borde, no solo en centros de cómputo de alta gama.

**Pangu-Weather** ([Bi et al., 2022](#ref-generic2023bi)), publicado en *Nature* (revista Nature, factor de impacto 64.8), representó el siguiente escalón. Mediante una arquitectura Transformer tridimensional entrenada sobre 39 años de datos del ERA5, Pangu-Weather superó al sistema de predicción del ECMWF en el 75% de las variables evaluadas a un horizonte de 5 días. A título ilustrativo: su predicción de la trayectoria del huracán Dora (2023) fue más precisa que la de cualquier modelo operacional existente.

**GraphCast** ([Lam et al., 2022](#ref-generic2023lam)), publicado en *Science* (otro Q1 indiscutible, IF 56.9), empujó el límite aún más lejos. Entrenado sobre la misma base ERA5 pero con una arquitectura de grafo espaciotemporal, GraphCast superó al ECMWF en el 90.3% de las 1,380 variables evaluadas a 10 días de predicción, reduciendo el tiempo de cómputo de horas a menos de un minuto. Su predicción del ciclón Freddy (2023) (el más largo de la historia registrada) fue el ejemplo más dramático de transferencia de capacidad predictiva a dominios extremos.

A tenor de lo expuesto, la conclusión para un arquitecto de sistemas es inequívoca: **la precisión predictiva está resuelta, o en vías de resolverse**. El déficit no está en el modelo; está en la cadena de uso de ese modelo. Ninguno de estos tres sistemas (FourCastNet, Pangu-Weather, GraphCast) viene con un mecanismo de coordinación institucional incluido. Producen números; no coordinan evacuaciones.

Irrgang et al. (2021), en *Nature Machine Intelligence*, introducen el concepto de "neural Earth system modelling": integrar IA en los flujos de trabajo de ciencias de la Tierra no como sustituto de los modelos físicos, sino como complemento. Lo relevante para este capítulo: los autores documentan que la principal barrera para la adopción es organizacional, no técnica (los datos existen, los modelos existen, pero los pipelines de integración inter-agencia no). Esta es exactamente la brecha que un sistema multiagente puede cerrar.

---

## Sección 3: Arquitectura Técnica Expandida: Las Cuatro Capas en Detalle

**► PISTA TÉCNICA**

La Figura 3.1 resume la arquitectura completa antes de entrar al detalle de cada capa: los datos crudos entran por abajo, atraviesan percepción y razonamiento especializado, se sintetizan en la capa de orquestación y llegan al humano ya convertidos en una recomendación trazable, nunca en una orden.

![Diagrama 3.1: Arquitectura de 4 capas: Percepción → Razonamiento → Orquestación → Gobernanza](imagenes/uml/c23_architecture_layers.png)

Obsérvese que las flechas entre capas son bidireccionales solo entre Orquestación y Gobernanza: el humano puede rechazar una recomendación y forzar una nueva síntesis, pero nunca escribe directamente en la capa de razonamiento. Esa asimetría es deliberada, es el mecanismo que impide que la supervisión humana se convierta en un cuello de botella operativo sin dejar de ser, a la vez, la autoridad final.

### Capa 1: Percepción: Normalizar la Realidad Heterogénea

Los agentes de percepción son los traductores del sistema. Su función es transformar datos crudos y heterogéneos en un formato semántico compartido, no razonar. En términos técnicos, implementan el patrón **Anti-Corruption Layer** ([Fowler, 2003](#ref-fowler2003)) aplicado a datos climáticos.

Cada agente de percepción se conecta a una fuente específica mediante el Model Context Protocol (MCP, Anthropic 2024), que garantiza que el agente nunca maneja credenciales de acceso directamente (estas son mediadas por el servidor MCP con autenticación OAuth2 y registro de auditoría). Los formatos ingeridos incluyen:

- **NetCDF** (SENAMHI, IGP): archivos de variables climáticas multidimensionales con coordenadas espacio-temporales. El agente de percepción los convierte a JSON geoespacial normalizado con timestamps UTC.
- **CSV y XLSX** (ANA, INDECI): archivos de estaciones hidrometeorológicas. El agente los homologa al esquema de events internos del bus de mensajes.
- **APIs REST** (NASA EOSDIS, ESA Copernicus): respuestas JSON con imágenes satelitales y datos de nivel del mar. El agente las normaliza y georeferencia.
- **Streams MQTT** (sensores IoT de caudal en cuencas): mensajes de baja latencia que el agente convierte a eventos Kafka con metadata de calidad de señal.

El principio rector: **un único contrato de datos interno**. Todo lo que entra al bus de eventos tiene el mismo esquema, independientemente de la fuente original.

### Capa 2: Razonamiento Especializado: Los Expertos Sintéticos

En esta capa residen cuatro agentes especializados, cada uno entrenado (mediante fine-tuning o system prompting de alta especificidad) en un dominio distinto:

**Agente Hidrológico.** Su dominio es el ciclo del agua: caudales, umbrales de desbordamiento, modelos de cuencas. Consume los eventos del agente de percepción para SENAMHI y ANA, ejecuta cálculos de tiempo de concentración de cuencas (fórmula de Kirpich: `Tc = 0.0195 × (L³/H)^0.385` donde L es la longitud del cauce en metros y H es la diferencia de elevación), y publica eventos como `"Río Rímac: caudal 95th percentile en 18h, confianza: 0.87"`.

**Agente Epidemiológico.** Activa tras una alerta hidrológica. Los brotes de dengue, leptospirosis y cólera que siguen a inundaciones siguen patrones documentados (OPS/OMS, series históricas 2000-2023). Este agente cruza los mapas de inundación proyectados con los registros de vectores activos (Aedes aegypti, criaderos) y publica alertas de riesgo sanitario geolocalizado con horizonte de 15 días.

**Agente Logístico.** Su función es optimizar rutas de auxilio bajo la restricción de infraestructura degradada. Implementa una variante del Vehicle Routing Problem con Time Windows (VRPTW), resuelto con algoritmos metaheurísticos (Simulated Annealing para instancias <200 nodos, escalando a Tabu Search para instancias mayores). Publica el plan óptimo de distribución de agua potable, comida y medicamentos hacia las zonas de impacto proyectado.

**Agente Agrícola.** Estima pérdidas de campaña cruzando proyecciones de inundación con el mapa de cultivos en producción (datos MIDAGRI). Sus salidas alimentan tanto el plan logístico (qué zonas necesitarán soporte alimentario) como la valoración de daños para la declaratoria de emergencia.

### Capa 3: Orquestación y Consenso: Donde el Enjambre Decide

Un bus de eventos Apache Kafka actúa como sistema nervioso. Cada agente de la Capa 2 es un consumidor y un productor: lee eventos del bus, procesa en su dominio y publica sus conclusiones como nuevos eventos. El **Agente Coordinador** agrega estas conclusiones aplicando un esquema de ponderación basado en incertidumbre (los eventos con mayor confidence score tienen mayor peso en la recomendación final).

Críticamente, existe un **Agente Crítico** cuya función es adversarial: su único trabajo es identificar inconsistencias entre las conclusiones de los agentes especializados. ¿El agente hidrológico proyecta desbordamiento en 18 horas pero el agente logístico planifica rutas por esa misma zona? El Agente Crítico detecta la contradicción y publica un evento de conflicto que obliga a renegociación. Este mecanismo implementa, en el dominio del software, el principio popperiano de falsabilidad: una conclusión vale por las refutaciones que sobrevivió (cf. Cap. 25).

### Capa 4: Gobernanza Humana: La Máquina Sustenta, el Humano Firma

Ningún agente del sistema emite órdenes de evacuación. La Capa 4 materializa el principio de **Human-in-the-Loop** en su forma más estricta: el enjambre entrega recomendaciones, no decisiones. Cada recomendación viene acompañada de:

1. Nivel de confianza agregado (escala 0–1, calibrado mediante *reliability diagrams* sobre el historial de predicciones).
2. Cadena de evidencia trazable: qué datos originaron qué conclusión en qué agente.
3. Escenarios alternativos: la recomendación de mayor confianza + las dos alternativas de menor costo si la principal falla.

Los tomadores de decisión en el COEN (Centro de Operaciones de Emergencia Nacional) interactúan con un dashboard que muestra estas recomendaciones en lenguaje natural, con mapas interactivos y la trazabilidad completa accesible con un clic. El funcionario firma la evacuación; el sistema la preparó.

---

## Sección 4: Perspectiva Senior Engineer y QA: Confiabilidad del Sistema Bajo Presión

**► PISTA TÉCNICA**


Un sistema de gestión de desastres que falla durante el desastre es, en el mejor de los casos, inútil; en el peor, contraproducente. La confiabilidad no es una característica opcional: es la característica central.

**Validación por backtesting histórico.** La estrategia de testing más robusta disponible para este tipo de sistema es ejecutarlo contra datos históricos de eventos pasados (El Niño 1997-1998, El Niño Costero 2017) y medir si sus recomendaciones habrían sido las correctas. Las métricas relevantes no son las de un clasificador genérico: son el **Brier Score** (calibración de probabilidades), la **Resolución** (capacidad de discriminar entre eventos) y el **Reliability Diagram** (¿cuando el agente dice "90% de probabilidad", acierta el 90% de las veces?). Un agente hidrológico con un Brier Score superior a 0.25 en eventos históricos no debe ser desplegado en producción.

**Redundancia y fail-safe.** La arquitectura implementa redundancia en la Capa 1 (tres agentes de percepción por fuente crítica, consenso 2-de-3), y *graceful degradation* en la Capa 2: si el agente epidemiológico no responde en 30 segundos, el Coordinador continúa con las conclusiones de los tres agentes restantes y etiqueta la recomendación final con "Análisis epidemiológico no disponible, confianza reducida".

**Monitoreo de latencia end-to-end.** La promesa del sistema es reducir el tiempo entre detección de anomalía y recomendación oficial de alerta de 72 horas (status quo 2024) a 6 horas. Esta promesa requiere Service Level Objectives (SLOs) explícitos en cada capa: `P99 de latencia Capa 1 < 5min`, `P99 Capa 2 < 15min`, `síntesis Capa 3 < 5min`. Si algún SLO se viola, el sistema alerta al equipo de operaciones antes de que el incidente se propague.

**Testing de inyección adversarial.** Los datos meteorológicos pueden ser adulterados (un sensor defectuoso, un dato transmitido con error de unidades, o, en escenarios más sofisticados, manipulación intencionada). El pipeline de ingesta implementa detección de anomalías estadísticas (z-score > 3.5 para variables históricamente estables) antes de que los datos lleguen al bus de eventos. Un agente de percepción que detecta un dato fuera de rango lo marca como `confidence: 0.0` y lo publica de todas formas (para registro de auditoría) pero no lo incluye en el cálculo de síntesis.

---

## Sección 5: Perspectiva Ejecutiva: ROI, Presupuesto y Ciclo de Vida

**■ PISTA EJECUTIVA**


Para el Director Ejecutivo del INDECI o el Ministro de Economía que debe aprobar el presupuesto, el argumento técnico es insuficiente. Lo que importa es la ecuación de valor: ¿cuánto cuesta este sistema frente a cuánto ahorra?

**El costo de no actuar** no es hipotético. El Niño Costero 2017 generó daños cuantificados en USD 3,100 millones según la CEPAL (2017). El tiempo de respuesta promedio del COEN tardó 72 horas desde la detección de la anomalía hasta la primera orden de evacuación oficial. En ese período, la mayoría de los daños ya eran inevitables.

Un análisis conservador: reducir el tiempo de respuesta de 72 a 6 horas permitiría evacuar preventivamente el 40% de las zonas de alto impacto antes del pico (estimación basada en tiempos de transporte documentados por INDECI, 2018). Sobre USD 3,100M de daños, eso representa un ahorro potencial de USD 620M por evento severo.

**TCO del sistema (Total Cost of Ownership, horizonte 5 años):**

| Componente | Año 1 (Implementación) | Año 2-5 (Operación) |
|------------|----------------------|---------------------|
| Infraestructura cloud (Kafka, K8s, modelos) | USD 180,000 | USD 60,000/año |
| Integración APIs SENAMHI/IGP/ANA | USD 120,000 | USD 20,000/año |
| Fine-tuning modelos especializados | USD 80,000 | USD 30,000/año (actualización) |
| Capacitación COEN/COER | USD 40,000 | USD 15,000/año |
| **Total** | **USD 420,000** | **USD 125,000/año** |

TCO a 5 años: USD 920,000. Ahorro potencial por un evento severo: USD 620M. Ratio ROI: **673:1**.

Esto no es utopía: es ingeniería de valor. El argumento ante el comité presupuestario es "queremos reducir el costo esperado de El Niño severo en USD 620M con una inversión de USD 920K a 5 años", no "queremos hacer IA".

**Roadmap ejecutivo:**
- **Fase 0 (Meses 1-3)**: Diagnóstico de APIs y formatos de datos de SENAMHI, IGP, ANA. Definición de SLOs.
- **Fase 1 (Meses 4-9)**: PoC con Agente Hidrológico + Agente Coordinador. Validación con datos históricos.
- **Fase 2 (Meses 10-18)**: Despliegue piloto regional (cuencas Chira-Piura, Huallaga). Integración con COEN.
- **Fase 3 (Meses 19-30)**: Expansión nacional + interoperabilidad con Ecuador y Colombia.

---

## Sección 6: Caso Transfronterizo: El Canal de Panamá y el Racionamiento Hídrico

**■ PISTA EJECUTIVA**

El mismo problema de fondo (orquestación distribuida bajo incertidumbre climática) no es exclusivo de la gestión de desastres. Aparece, con otro disfraz, en cualquier infraestructura crítica que dependa de un recurso hídrico compartido. El caso del Canal de Panamá en 2026 lo ilustra con una nitidez poco frecuente, porque ocurre en tiempo real mientras se escribe este capítulo.

El Canal opera con dos represas (Gatún y Alhajuela) cuyo nivel determina cuántos buques pueden transitar por día y con qué calado máximo. Cada tránsito consume varios millones de galones de agua dulce, el mismo recurso que abastece a la mitad de la población panameña. En agosto de 2026, las lluvias en la cuenca cayeron un 34% por debajo del promedio histórico y el lago Gatún se ubicó apenas por debajo de su promedio de cinco años para esa fecha ([Autoridad del Canal de Panamá, agosto 2026](#ref-acp2026)). La NOAA estimó en ese mismo periodo una probabilidad del 81% de que El Niño alcance categoría "muy fuerte" hacia fines de 2026 ([NOAA Climate Prediction Center, 2026](#ref-noaa2026)). La respuesta de la ACP fue reducir los tránsitos diarios de 36 a 34 a partir del 3 de septiembre, y a 32 a partir del 15 (ACP, 2026), una restricción todavía leve comparada con la crisis de 2023-2024, cuando el nivel del lago obligó a recortar de 38 tránsitos diarios a apenas 18, con pérdidas que arrastraron cadenas de suministro globales durante meses.

Lo relevante para este capítulo es que **la arquitectura de cuatro capas descrita en la Sección 3 se traslada casi sin modificaciones**:

- **Percepción.** Los mismos agentes que normalizan NetCDF y streams MQTT en la cuenca peruana pueden ingerir la telemetría de nivel de Gatún y Alhajuela, los pronósticos ENSO de la NOAA y la cola de reservas de tránsito de las navieras, homologando todo a un esquema común vía MCP.
- **Razonamiento especializado.** Un **Agente Hidrológico** (idéntico en función al de la Sección 3, reentrenado sobre la cuenca del Canal) proyecta la trayectoria del nivel del lago a 30 y 90 días. Junto a él opera un **Agente de Programación de Tránsitos**, que resuelve una variante distinta al VRPTW de la Sección 3: un problema de *bin packing* con restricción de presupuesto hídrico, donde cada franja diaria tiene un volumen de agua disponible y cada buque reservado consume una porción de ese volumen según su calado y el número de esclusajes simultáneos que admite.
- **Orquestación y consenso.** Aquí aparece la pieza que de verdad importa: un **Agente Crítico** que compara la proyección hidrológica con el calendario de reservas ya confirmadas. Si el agente hidrológico revisa a la baja su proyección de nivel (como ocurrió varias veces durante 2023) y el calendario de tránsitos todavía asume la disponibilidad anterior, el Agente Crítico levanta el mismo tipo de conflicto temporal que vimos en el Ejercicio 3.1, obligando a renegociar la asignación de franjas antes de que la escasez se vuelva una crisis operativa anunciada con pocos días de margen.
- **Gobernanza humana.** La ACP firma la restricción; el sistema le entrega la recomendación con el nivel de confianza del pronóstico y el costo de oportunidad de cada escenario (ingresos por peajes perdidos frente a riesgo de desabasto).

El patrón que emerge (llamémoslo **Racionamiento Adaptativo bajo Incertidumbre Hidroclimática**) es portable a cualquier infraestructura que reparta un recurso escaso entre demandantes con distinto poder de pago y distinta urgencia: una represa hidroeléctrica, una red de riego agrícola, un acuífero compartido entre municipios. La lección de ingeniería es la misma que cierra la Sección 5: el valor no está en predecir mejor el clima (eso ya lo resuelven GraphCast y Pangu-Weather), está en tener la arquitectura de orquestación y gobernanza que convierte esa predicción en una decisión defendible antes de que el recurso se agote.

Y aquí conviene ser explícitos sobre algo que este libro sostiene desde el primer capítulo: esta arquitectura mantiene su valor con independencia de qué modelo específico razona en la Capa 2. Si mañana un modelo nuevo (sea de OpenAI, Anthropic o cualquier otro proveedor) resulta más barato o más preciso en pronóstico hidrológico, se sustituye el agente correspondiente sin tocar el resto del sistema, siempre que se haya respetado el principio de **Backend Agnóstico** (cf. Vol. 2). La ventaja competitiva depende de haber construido el arnés que permite adoptar ese modelo el mismo día que sale, sin reescribir la orquestación; perseguir el modelo de la semana rinde mucho menos que eso.

---

## Versión académica ampliada

> *La presente sección ofrece una reformulación de los conceptos centrales del capítulo con densidad académica superior, orientada a audiencias de investigación o presentaciones ante comités técnicos de alto nivel.*

El fenómeno ENSO (El Niño–Southern Oscillation) constituye, desde una perspectiva de sistemas complejos, un atractor caótico de baja dimensión cuya dinámica emergente ha sido caracterizada mediante técnicas de reducción dimensional (Empirical Orthogonal Functions, EOF) sobre datos satelitales de temperatura superficial del mar (SST). La transición de arquitecturas de predicción puramente numéricas hacia híbridos neuro-físicos, tal como documentan Irrgang et al. (2021) en *Nature Machine Intelligence*, introduce una disrupción metodológica: los modelos de aprendizaje profundo no sustituyen la física del sistema, sino que aprenden las residuales que el modelo físico no captura, comprimiendo así el espacio de error de manera sustancialmente más eficiente.

En el plano de la ingeniería de sistemas multi-agente aplicada a la gestión de desastres, la arquitectura propuesta en este capítulo se inscribe en el paradigma de los Sistemas Multi-Agente Heterogéneos (HMADS, por su acrónimo inglés), donde la heterogeneidad de los agentes (dominios epistémicos distintos, vocabularios técnicos diferenciados, horizontes temporales de razonamiento divergentes) no constituye una limitación sino el fundamento de la riqueza computacional del enjambre. El consenso emergente entre agentes heterogéneos bajo un protocolo de ponderación por incertidumbre (Bayesian Model Averaging, BMA) produce estimaciones calibradas de naturaleza superior a cualquier agente individual, fenómeno documentado en la literatura de *ensemble learning* desde los trabajos seminales de Breiman (1996) y formalizado para sistemas multi-agente por Wooldridge & Jennings (1995) en *The Knowledge Engineering Review*.

---

## Lo esencial del capítulo 3

- El Niño es un problema de **orquestación distribuida bajo incertidumbre**, no de escasez de datos.
- Los modelos FourCastNet, Pangu-Weather y GraphCast han resuelto la predicción a corto plazo: el déficit está en la cadena institucional de decisión, no en la ciencia.
- La arquitectura de cuatro capas (Percepción → Razonamiento → Orquestación → Gobernanza) separa dominios de responsabilidad sin acoplamiento directo entre ellos.
- El **Agente Crítico** adversarial es la pieza más importante del diseño: una recomendación vale por cuántas refutaciones sobrevivió.
- El humano firma la evacuación; el sistema la sustenta con trazabilidad y cadena de evidencia.
- El ROI conservador es 673:1 respecto al TCO a 5 años para un evento severo.
- La interoperabilidad regional (Perú, Ecuador, Colombia, Chile) convierte enjambres nacionales en una confederación transfronteriza.
- La confiabilidad se valida con backtesting histórico sobre El Niño 1997-98 y 2017, no solo con pruebas sintéticas.
- La misma arquitectura de cuatro capas, sin modificarla, resuelve el racionamiento hídrico del Canal de Panamá bajo El Niño 2026: lo que se reutiliza es el patrón; el modelo que razona dentro de él es intercambiable.

---

## Ejercicio resuelto 3.1: Diseña el Agente Crítico

**Enunciado.** El Agente Hidrológico publica el evento: `{"rio": "Piura", "desbordamiento_prob": 0.91, "horizonte_horas": 20, "confianza": 0.88}`. Simultáneamente, el Agente Logístico publica: `{"ruta_principal": "Carretera Piura-Paita", "tiempo_evacuacion_estimado": 26, "estado_ruta": "transitable"}`. El Agente Crítico debe detectar el conflicto. ¿Qué lógica implementa y qué publica?

**Solución.**

El Agente Crítico implementa una **comprobación de consistencia temporal**: si `desbordamiento_prob > 0.85` y `horizonte_horas < tiempo_evacuacion_estimado`, el plan logístico propuesto es físicamente incoherente (la evacuación llegaría después del desbordamiento).

```python
def detectar_conflicto(evento_hidrologico, evento_logistico):
    umbral_prob = 0.85
    margen_seguridad_horas = 4  # buffer operacional mínimo
    
    if (evento_hidrologico["desbordamiento_prob"] > umbral_prob and
        evento_hidrologico["horizonte_horas"] < 
        (evento_logistico["tiempo_evacuacion_estimado"] + margen_seguridad_horas)):
        
        return {
            "tipo": "CONFLICTO_TEMPORAL",
            "descripcion": "El horizonte de desbordamiento (20h) es menor al tiempo de evacuación (26h + 4h margen = 30h)",
            "agentes_involucrados": ["hidrologico", "logistico"],
            "accion_sugerida": "Buscar ruta de evacuación alternativa O reducir horizonte de acción",
            "prioridad": "CRITICA",
            "timestamp": "2025-01-15T03:45:00Z"
        }
```

El Coordinador recibe este evento de conflicto, suspende la recomendación de evacuación vía Carretera Piura-Paita, y solicita al Agente Logístico un plan alternativo con rutas que puedan completarse en menos de 16 horas. Solo cuando el Agente Crítico no detecte conflictos en la nueva propuesta, la recomendación sube a la Capa 4.

**La lección**: el Agente Crítico no hace más lento al sistema; hace más confiable al sistema. Un plan incongruente que llega al COEN a tiempo cero es más dañino que un plan correcto que llega una hora después.

---
