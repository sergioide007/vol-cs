# Capítulo 23: Taiwan: el nudo geopolítico que mueve cada enjambre de agentes en el planeta

> *Quien controla los semiconductores de punta controla qué agentes se ejecutan y cuáles no. Taiwan no es un país; es una bisagra.*

## La aritmética que nadie quiere enunciar

Existe un dato que la industria de la inteligencia artificial omite sistemáticamente en sus narrativas de progreso: el 92 % de los semiconductores lógicos fabricados en nodos de 7 nm o inferiores (los únicos capaces de ejecutar modelos de lenguaje de gran escala a velocidad y escala comerciales) provienen de un único territorio de 36 000 km². Esa cifra, documentada por el Semiconductor Industry Association (2024), no es una curiosidad estadística: es la restricción de diseño más severa del ecosistema agéntico global, anterior a cualquier decisión de arquitectura o elección de framework.

En consecuencia, cada GPU NVIDIA H100 que ejecuta un agente de LangGraph en São Paulo, cada acelerador AMD MI300X que respalda un enjambre de AutoGen en Berlín y cada chip Apple M3 Ultra que corre un orquestador local en Tokio comparte un origen común: las fábricas de Taiwan Semiconductor Manufacturing Company (TSMC). Entender Taiwan no es, por tanto, un ejercicio de geopolítica superficial; es una condición previa para entender la economía real de los sistemas multiagente.

## La cadena técnica: del silicio al token generado

Para comprender la posición de Taiwan en la cadena de valor agéntica, conviene trazar el recorrido completo desde el material bruto hasta la inferencia distribuida.

El proceso fotolitográfico de TSMC a 3 nm (nodo N3E, introducido en 2023) permite integrar hasta 292 millones de transistores por milímetro cuadrado (TSMC, *Technology Report Q3-2024*). Esta densidad es condición necesaria para que un transformer de 70 000 millones de parámetros quepa en cuatro chips y no en cien. Sin esa densidad, la latencia de inferencia escalaría en un orden de magnitud, haciendo económicamente inviables los enjambres de agentes que demandan respuestas en ciclos de 200 ms o menos.

| Nodo tecnológico | Transistores/mm² | Chip representativo | Agente beneficiado |
|-----------------|-----------------|--------------------|--------------------|
| 5 nm (N5, 2020) | 173 M | A14 Bionic, H100 SXM | GPT-4, Claude 3 |
| 3 nm (N3E, 2023) | 292 M | A17 Pro, M3 Ultra | Gemini 1.5, LLaMA 3 |
| 2 nm (N2, 2025) | ~380 M (est.) | B1 series (Apple) | Próxima gen. de enjambres |
| 1.4 nm (A14, 2027) | proyección | desconocido | IA agéntica autónoma |

A este respecto, el packaging avanzado resulta tan determinante como la litografía. La tecnología CoWoS (*Chip-on-Wafer-on-Substrate*) de TSMC, que apila chips lógicos con memoria HBM3e en un único substrato, es la razón por la cual un H100 SXM5 puede mover 3,35 terabytes de datos por segundo entre sus núcleos de cómputo y su memoria. Sin CoWoS, el cuello de botella de memoria limitaría la longitud de contexto procesable a una fracción de los 128 k tokens que hoy soportan modelos como Gemini 1.5 Pro ([Google DeepMind, 2024](#ref-googledeepmind2024)).

La capacidad de Taiwán no se agota en NVIDIA: El segundo actor fundamental es MediaTek, cuyo chip Dimensity 9300 incorpora la unidad de procesamiento neuronal (NPU) de mayor throughput del segmento móvil (87 TOPS, 2024). Estos chips son los nodos de inferencia local que permitirán que enjambres livianos ejecuten agentes de bajo coste directamente en dispositivos del borde, el escenario que el capítulo 12 denominó arquitectura híbrida.

## ITRI y la investigación aplicada: el ecosistema invisible

Detrás de TSMC opera un tejido de investigación que raramente aparece en los artículos de prensa occidental. El Industrial Technology Research Institute (ITRI), fundado en 1973, ha patentado más de 32 000 tecnologías, muchas de ellas directamente aplicables a sistemas agénticos: procesadores neuromórficos de ultra-bajo consumo, memorias resistivas (RRAM) para inferencia en el borde, y protocolos de interconexión die-to-die (el estándar UCIe) que permiten construir chiplets heterogéneos para cargas de trabajo de IA distribuida.

No obstante, el ecosistema taiwanese no se limita al hardware. Empresas como Asus, Acer y Quanta llevan décadas integrando subsistemas de cómputo en forma de servidores de alto rendimiento. Quanta Cloud Technology (QCT) ensambla los servidores DGX de NVIDIA (la unidad atómica de la mayoría de enjambres empresariales) con integración vertical desde la placa madre hasta el sistema de refrigeración líquida. La arquitectura de un enjambre que corre en AWS, Azure o GCP depende, en el nivel físico, de estos sistemas.

## La dimensión ejecutiva: riesgo de cadena de suministro como variable de arquitectura

**■ PISTA EJECUTIVA**


Para el ejecutivo tecnológico o el Product Owner de una plataforma agéntica, Taiwan plantea un problema de riesgo que no puede resolverse con redundancia de software. En el escenario hipotético de una interrupción severa en el Estrecho de Taiwan (escenario que think tanks como RAND Corporation (*Implications of Taiwan Strait Conflict*, 2023) y el CNAS han modelado), la producción global de semiconductores de punta caería entre un 37 % y un 42 % en los primeros 12 meses, según estimaciones del Boston Consulting Group (2021). No existe hoy ninguna alternativa a escala: Intel Foundry Services (IFS) opera en 18 nm en volumen; Samsung en 3 nm pero con rendimientos inferiores al 60 %; SMIC (China) está limitado a 7 nm por restricciones de acceso a equipos EUV de ASML.

La implicación arquitectónica directa para quienes diseñan sistemas agénticos es triple. Primero, la dependencia de inferencia en GPU cloud (H100, A100) debe coexistir con estrategias de inferencia cuantizada en hardware commodity, tal como argumenta el enfoque de cuantización a 4 bits documentado por Dettmers et al. (*QLoRA*, NeurIPS 2023). Segundo, los enjambres deben ser arquitectónicamente agnósticos al acelerador: el protocolo MCP (*Model Context Protocol*, Anthropic 2024) y el estándar OpenAI Agents SDK separan el orquestador del runtime de inferencia, permitiendo sustituir un backend CUDA por ROCm de AMD o SYCL de Intel sin refactorización mayor. Tercero, el plan de continuidad operacional de cualquier producto agéntico de misión crítica debe incluir un escenario de degradación graceful a modelos más pequeños (3B–7B parámetros) que puedan ejecutarse en hardware menos especializado.

> **Visión general:** La configuración geopolítica de la cadena de suministro de semiconductores de avanzada generación impone restricciones no derivables de principios puramente tecnológicos sobre la arquitectura de sistemas de inteligencia artificial distribuida. Dado que la concentración de capacidad de fabricación en nodos sub-7 nm permanece localizada en un único actor (TSMC, con una cuota de mercado del 92 % en dicho segmento según datos del Semiconductor Industry Association (2024)) los sistemas agénticos que dependen de la inferencia en aceleradores de alto rendimiento están expuestos a riesgos de discontinuidad de suministro cuya materialización escapa al control de los arquitectos de software. En consecuencia, el diseño de enjambres resilientes exige incorporar estrategias de degradación graceful y agnósticismo de backend como restricciones de primer orden, no como optimizaciones diferibles.

## Taiwan como árbitro silencioso de la carrera agéntica

Un giro inesperado para quienes mapean la competencia entre USA y China en IA agéntica (cf. Vol. 2, caps. 17 y 18) es que Taiwan sirve a ambos lados simultáneamente. TSMC fabrica chips diseñados por NVIDIA (empresa plenamente estadounidense) y también fabrica chips diseñados por HiSilicon (Huawei), aunque con las restricciones derivadas de los controles de exportación de 2022-2023. De facto, Taiwan es el proveedor de capacidad de cómputo de ambos competidores.

Esta posición de neutralidad técnica resulta, paradójicamente, más poderosa que la de cualquier actor que solo compite en modelos. Anthropic puede diseñar Claude 4; OpenAI puede diseñar GPT-5; DeepSeek puede diseñar R2. Todos dependerán de que TSMC ejecute sus órdenes de fabricación en el momento preciso y con los rendimientos requeridos. En esa dependencia radica la palanca silenciosa de Taiwan sobre la evolución del ecosistema agéntico global.

## Lo esencial del capítulo 23

- Taiwan produce el 92 % de los semiconductores de punta global; sin esos chips, ningún enjambre de agentes a escala es posible.
- CoWoS y HBM3e (tecnologías de packaging propias de TSMC) son tan determinantes como el nodo litográfico para el rendimiento de los modelos.
- MediaTek y QCT extienden la influencia taiwanese desde los nodos de borde hasta los servidores de inferencia en data center.
- El riesgo geopolítico del Estrecho de Taiwan es una variable de arquitectura: los enjambres deben diseñarse agnósticos al acelerador y con degradación graceful documentada.
- Taiwan sirve simultáneamente a USA y China, lo que lo convierte en árbitro técnico de la carrera agéntica, no en un simple proveedor.
