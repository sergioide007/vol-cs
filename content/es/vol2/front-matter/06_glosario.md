# Glosario operativo del Volumen 2

_Definiciones breves de los términos que este volumen introduce o usa con un sentido propio. El bloque A es vocabulario de ingeniería; el bloque C, vocabulario de análisis geopolítico y regulatorio. Separarlos evita el error más común al leer este volumen: tratar un término de política como si fuera una decisión de arquitectura._

## A. Ingeniería de frontera

| Término | Definición operativa | Capítulo |
|---|---|---|
| **Amenaza interna probabilística** | El riesgo no está solo fuera del sistema: el propio modelo puede producir la acción dañina sin atacante externo. Invalida la defensa basada solo en perímetro. | 1 |
| **OWASP LLM Top 10** | Lista de referencia de las diez clases de riesgo más relevantes en aplicaciones con LLM. Marco de priorización, no certificación. | 1 |
| **Inyección de prompt (directa/indirecta)** | Instrucción maliciosa que llega al modelo por la entrada del usuario o por un contenido que el agente lee (herramienta, documento, web). | 1 |
| **Confused Deputy** | Escenario en que un componente con permisos elevados actúa en nombre de otro sin verificar la autoridad real de la petición. | 1 |
| **Verificabilidad** | Grado en que el resultado de un agente puede comprobarse de forma independiente. Es la variable que el capítulo añade a la ecuación clásica de confianza. | 5 |
| **Confianza graduada** | Sustituir el binario «confío / no confío» por un espectro ligado al riesgo y a la evidencia acumulada. | 5 |
| **Modelo Actor / ReactiveX** | Bases formales del paradigma reactivo: unidades que se comunican por mensajes y operadores que componen flujos de eventos. | 4 |
| **Backpressure** | Mecanismo por el que un consumidor lento frena al productor rápido en lugar de acumular trabajo sin límite. | 4 |
| **Dead Letter Queue (DLQ)** | Cola donde se depositan los eventos que no pudieron procesarse tras N reintentos, para inspección sin detener el flujo. | 4 |
| **Tormenta de eventos** | Bucle de propagación en el que un evento genera reacciones que generan a su vez el mismo evento. Se contiene con idempotencia, DLQ y límite de saltos. | 4 |
| **Arquitectura híbrida** | Combinación deliberada de componentes cloud y on-premise/edge; su riesgo no es la mezcla sino la «costura» entre ambos. | 12 |
| **Latencia de feedback** | Tiempo entre una acción y la señal que permite aprender de ella. Determina la velocidad real de mejora de un equipo. | 26 |
| **Deuda técnica agéntica** | Deuda específica de los sistemas con agentes: contexto no gobernado, evals ausentes, permisos implícitos, patrones sin política de fallo. | 13 |
| **Atrofia cognitiva** | Pérdida de una habilidad humana por delegarla por completo en el agente en lugar de usarlo como extensión. | 6 |
| **Patrón Soporte-Evaluación** | Separar en dos agentes (o dos roles) la función de ayudar de la de juzgar, para evitar que quien asiste se evalúe a sí mismo. | 8 |

## B. Industria

| Término | Definición operativa | Capítulo |
|---|---|---|
| **Difusión espaciotemporal** | Familia de modelos generativos de vídeo que tratan el tiempo como una dimensión más de la difusión. | 16 |
| **MARL (Multi-Agent Reinforcement Learning)** | Aprendizaje por refuerzo con varios agentes que aprenden simultáneamente en un entorno compartido. | 28 |
| **Licensing proactivo** | Estrategia de licenciar datos de entrenamiento antes de que una disputa legal lo imponga. | 15, 16 |

## C. Geopolítica, regulación y ecosistemas

| Término | Definición operativa | Capítulo |
|---|---|---|
| **AI Act** | Reglamento europeo que clasifica sistemas de IA por nivel de riesgo y obliga según esa clase. Regulación como plano de construcción técnico. | 19 |
| **GPAI** | Modelo de propósito general (General Purpose AI); categoría regulada con obligaciones propias de documentación de datos. | 16, 19 |
| **GDPR / PIPL** | Marcos de protección de datos europeo y chino respectivamente. Determinam qué datos pueden centralizarse y con qué fricción. | 17, 20 |
| **Compliance-by-Design** | Incorporar el cumplimiento normativo en la arquitectura, no como auditoría posterior. | 19 |
| **NIST AI RMF** | Marco de gestión de riesgo de IA del instituto estadounidense de estándares. | 18 |
| **Constitutional AI / RLHF** | Enfoques de alineación: reglas explícitas que guían al modelo, y aprendizaje a partir de retroalimentación humana. | 18 |
| **MoE (Mixture of Experts)** | Arquitectura que activa solo una fracción de parámetros por token, reduciendo el cómputo efectivo. | 17 |
| **MLA (Multi-Head Latent Attention)** | Variante de atención que comprime la caché KV y reduce memoria de activaciones. | 17 |
| **GRPO** | Algoritmo de optimización de política relativa por grupo; permite entrenar razonamiento sin ajuste supervisado previo. | 17 |
| **Soberanía tecnológica** | Capacidad de un país de sostener su stack de IA sin depender de proveedores sujetos a otra jurisdicción. | 22, 24 |
| **Cuello de botella de la cadena de suministro** | Punto único (p. ej. litografía de ASML) del que depende toda la producción aguas abajo. | 23, 24 |
| **Modelo de madurez (ciudad agéntica)** | Escala de etapas que describe cuánto de la operación de una ciudad se coordina con enjambres gobernados. | 11 |