# Glosario operativo del Volumen 4

_Vocabulario de operación, escala y economía. Los términos de métricas se definen con la fórmula o el criterio de cálculo, porque en este volumen la definición es la que hace útil la métrica._

| Término | Definición operativa | Capítulo |
|---|---|---|
| **Token-Burn** | Gasto de tokens que no produce valor: iteraciones, reintentos y contexto inflado que no mueven la aguja del resultado. | 1 |
| **CIU (Costo por Iteración Útil)** | Costo total dividido entre las iteraciones que produjeron un resultado aceptado. Convierte el gasto en una cifra con denominador de valor. | 1, 11 |
| **Estimación probabilística** | Estimar por distribución (percentiles) en lugar de por media, porque el trabajo con agentes tiene cola larga. | 2 |
| **Testing no determinista** | Verificar un comportamiento que no produce siempre el mismo resultado: se prueba por propiedades, umbrales y conjuntos de casos, no por igualdad exacta. | 3 |
| **Ataque indirecto (prompt injection)** | Instrucción maliciosa introducida en contenido que el agente lee, no en la petición del usuario. | 4 |
| **Regla de dependencia** | En arquitectura limpia, las dependencias apuntan hacia el núcleo (dominio); el modelo y la infraestructura son detalles reemplazables. | 6 |
| **Value Object / arquitectura hexagonal** | Piezas de la arquitectura limpia que aíslan el dominio de los detalles de infraestructura; aplicadas aquí a sistemas con agentes. | 6 |
| **Event-driven / Kafka** | Arquitectura en la que los componentes reaccionan a eventos en lugar de llamarse directamente; el log es la fuente de verdad. | 7 |
| **CDC (Change Data Capture)** | Captura de cambios de una base de datos como flujo de eventos, base del flujo CDC → agente → consumidores. | 7 |
| **Backpressure (en consumo de eventos)** | El consumidor regula su ritmo para no saturarse, en lugar de acumular mensajes sin límite. | 7 |
| **Señales doradas** | Cuatro métricas clásicas de servicio (latencia, tráfico, errores, saturación) que este volumen combina con señales sintéticas de agentes. | 8 |
| **DLQ (cola de mensajes muertos)** | Destino de los eventos no procesables tras N reintentos; su revisión semanal alimenta las evaluaciones del sistema. | 7, 8 |
| **LLMOps** | Operación de sistemas con modelos: versionado de prompts, evaluaciones, observabilidad y control de costo, sin el aparato de MLOps clásico cuando el equipo es pequeño. | 8 |
| **Deriva semántica** | Cambio gradual del significado de las respuestas del enjambre respecto al objetivo, que ninguna métrica clásica detecta. | 11 |
| **Consenso falso** | Acuerdo entre agentes que no nace de la evidencia sino de compartir el mismo sesgo o contexto. | 11 |
| **Incentivos sintéticos** | Señales que el capítulo propone para que el enjambre salga de la parálisis; tienen el riesgo de ser optimizadas como cualquier métrica. | 11 |
| **Edge computing agéntico** | Ejecución del agente en el dispositivo o en el borde, por latencia, privacidad o costo energético. | 12 |
| **CAPEX vs. OPEX** | Decidir entre invertir en capacidad propia (hardware) o pagar por consumo; el capítulo lo aplica a la eficiencia energética. | 12 |
| **DR (Disaster Recovery)** | Plan y práctica de recuperación ante desastres. En su versión agéntica debe recuperar **estado cognitivo distribuido**, no solo servicios. | 13 |
| **Estado cognitivo distribuido** | Memoria, contexto y decisiones repartidas entre agentes y subsistemas; activo que el DR tradicional no contempla. | 13 |
| **RTO / RPO** | Tiempo objetivo de recuperación y punto objetivo de recuperación de datos; en sistemas agénticos deben definirse también para la memoria. | 13 |
| **Ensayo de recuperación** | Prueba real de restauración. Sin ensayo, un plan de DR es una hipótesis, no una capacidad. | 13 |
| **Graceful degradation** | Operar con capacidades reducidas y declaradas cuando una pieza no está disponible, en lugar de fallar. | 10 |