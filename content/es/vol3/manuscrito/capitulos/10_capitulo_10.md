# Capítulo 10: Gestión de expectativas y tiempos de la IA

> *La IA no eliminó la incertidumbre de los plazos; la trasladó de la ejecución a la verificación.*

## La IA redefine la gestión del tiempo, no la abole

El autor sostiene que la IA redefine por completo la gestión de los tiempos del desarrollo de software. El matiz crítico no radica en eliminarla, sino en **desplazarla**. Antes de la generalización de los asistentes de código, lo incierto era cuánto tardaría escribir el código; ahora, el código aparece en minutos (en ocasiones, en segundos), pero lo genuinamente incierto es cuánto tardará *verificar que ese código es correcto, seguro y adecuado para el contexto específico del problema*. La gestión de expectativas, por tanto, debe reeducarse a fondo: el cuello de botella migró del teclado al criterio.

Esta migración no es metafórica; es empíricamente medible. Peng et al. (2023, arXiv:2302.06590), en el estudio de GitHub con 95 desarrolladores profesionales, documentaron que la velocidad de generación de código nuevo aumenta un 55% con asistencia de IA. Lo que el mismo estudio señala, y que con frecuencia se omite en las presentaciones ejecutivas, es que **el tiempo de revisión y verificación del código generado por IA no se redujo proporcionalmente**: los desarrolladores que usaron Copilot reportaron dedicar más tiempo relativo a la fase de revisión crítica del código generado que al código escrito manualmente, precisamente porque la asistencia aumentó el volumen de código producido por unidad de tiempo.

## El espejismo de la velocidad: por qué la generación rápida no implica entrega rápida

Existe una expectativa peligrosa (y frecuentemente articulada en reuniones de dirección) que conviene desmontar con datos: "si la IA genera código instantáneamente, los proyectos serán instantáneos". La afirmación es falsa, y su falsedad no es trivial.

En un entorno complejo y cambiante (como el que el autor describe en sus reflexiones sobre programación en contextos de alta volatilidad organizacional) la velocidad de generación no determina la velocidad de entrega por tres razones estructurales:

**Primera razón: la complejidad del contexto no se genera.** Un agente de código puede generar una función en segundos. No puede, sin intervención humana, comprender las restricciones implícitas del sistema de pagos legacy al que esa función se integrará, las políticas de compliance que la afectan, las peculiaridades del equipo que la mantendrá o el historial de decisiones arquitectónicas que hacen inviables ciertas implementaciones aparentemente correctas.

**Segunda razón: la deuda también se genera rápido.** Vaithilingam et al. (2022), en un estudio experimental con participantes usando GitHub Copilot publicado en CHI 2022, encontraron que los participantes con asistencia de IA completaron más tareas pero introdujeron más bugs en el código generado que los participantes sin asistencia (un efecto que los autores atribuyen a la menor fricción de generación, que inhibe la verificación espontánea). La deuda técnica se acumula a la velocidad de la generación si no hay contramedidas explícitas.

**Tercera razón: la integración es el cuello de botella real.** Generar código es solo una parte del proceso de entrega. La integración con el sistema existente, las pruebas de regresión, la revisión de código, el proceso de despliegue y la validación de comportamiento en producción siguen siendo operaciones con tiempos mínimos que la velocidad de generación no comprime.

## Evidencia empírica: las nuevas curvas de tiempo

La siguiente tabla sintetiza los datos disponibles sobre el impacto de la IA en las distintas fases del ciclo de desarrollo:

| Fase | Antes de la IA | Con asistentes de IA (2024) | Factor de cambio | Fuente |
|------|----------------|-----------------------------|------------------|--------|
| Generación de código nuevo | Días a semanas | Horas a días | 4–10x más rápido | Peng et al. 2023 |
| Revisión y verificación | Proporcional al código | **Domina el cronograma** | Sin cambio significativo | Vaithilingam et al. 2022 |
| Integración con sistema | Moderada | Crítica (sin contexto implícito) | Variable (a veces más lenta) | McKinsey 2023 |
| Detección de regresiones | Depende del test suite | Alta si hay evals; baja si no | Bimodal | Liu et al. 2024 |
| Mantenimiento post-despliegue | Alto | **Alto** (la deuda se acumula rápido) | Sin mejora sin inversión en evals | Jimenez et al. 2024 |

La lección que emerge de esta tabla es nítida: la IA aplana la curva de generación de forma dramática, pero **no aplana las curvas de verificación, integración y mantenimiento**. Quien planifica ignorando estos tres factores promete plazos que no podrá cumplir, con la diferencia de que ahora el incumplimiento llega antes y con mayor volumen de código comprometido.

## Modelo de planificación para proyectos con asistencia de IA

La adaptación de los métodos de planificación ágil al contexto de IA agéntica requiere revisar tres convenciones establecidas:

**1. Los story points ya no miden lo mismo.** En la estimación ágil clásica, un story point captura la complejidad *de implementación*. Con IA, la implementación es más rápida; lo que demora es la verificación. Los equipos que adoptan IA sin recalibrar sus story points experimentan lo que podría denominarse la "inflación de velocidad": la velocity aumenta sin que la entrega de valor lo haga en la misma proporción.

Una recalibración práctica consiste en descomponer el story point en dos componentes: *complejidad de generación* (qué tan difícil es describir correctamente el problema al agente) y *complejidad de verificación* (qué tan difícil es comprobar que la solución generada es correcta). En sistemas con alta complejidad de verificación (dominio de seguridad, compliance, lógica de negocio crítica), la IA reduce el primero pero no el segundo.

**2. El Definition of Done debe incluir criterios de verificación de salida generada.** Un incremento producido con asistencia de IA no está "hecho" hasta que ha pasado por un conjunto de verificaciones explícitas que van más allá de "compila y pasan los tests existentes". El DoD agéntico incluye: pruebas de comportamiento en los casos límite identificados, revisión de seguridad del código generado, validación de consistencia con el contexto del sistema y evaluación de la deuda técnica introducida.

**3. La retrospectiva debe rastrear la proporción entre generación y verificación.** El indicador más útil para calibrar la adopción de IA en un equipo ágil es el tiempo dedicado a verificar por cada hora de generación asistida. Un ratio mayor de 3:1 sugiere que la especificación de las tareas al agente es deficiente; un ratio menor de 0.5:1 sugiere que la verificación es insuficiente y la deuda se acumula silenciosamente.

## El pipeline CI/CD para código generado por IA: qué añadir

**► PISTA TÉCNICA**


Los pipelines de integración y despliegue continuo convencionales deben extenderse cuando el código es generado parcial o totalmente por asistentes de IA. Las extensiones mínimas necesarias son:

- **Análisis estático reforzado**: las herramientas estáticas deben configurarse con reglas más estrictas para código generado por IA, donde los patrones de copy-paste lógico y las dependencias innecesarias son más frecuentes.
- **Pruebas de mutación**: verifican que las pruebas existentes son capaces de detectar bugs en el código generado, no solo en el código escrito manualmente.
- **Rastreo de autoría**: marcar qué porcentaje del código en cada PR fue generado por IA permite calibrar el nivel de revisión necesario y construir datos históricos sobre la tasa de bugs por origen del código.
- **Eval automatizado de comportamiento**: para funciones críticas, un agente evaluador (cf. cap. 32, diseño de evals) verifica que el comportamiento generado es consistente con las especificaciones de negocio, no solo con los tests unitarios.

## ROI cuantificado: cuándo y cuánto ahorra la IA

**■ PISTA EJECUTIVA**


La pregunta ejecutiva más frecuente (y la más mal respondida) es: "¿cuánto ROI obtenemos de la IA en desarrollo de software?". La respuesta correcta depende de dos variables que los análisis simplistas ignoran: la naturaleza de las tareas (alta vs. baja verificabilidad) y la madurez del equipo en el uso de herramientas de IA.

El análisis de McKinsey Global Institute (2023) estima que la IA generativa puede automatizar el equivalente al 60-70% del tiempo dedicado a tareas de documentación, generación de tests y código boilerplate. Para tareas de diseño arquitectónico, resolución de bugs complejos en sistemas legacy y toma de decisiones de producto, el porcentaje de automatización cae al 10-20%.

El modelo de ROI más honesto es, por tanto, **bimodal**:

| Tipo de tarea | Porcentaje automatizable | ROI típico (6 meses) | Condición necesaria |
|---------------|-------------------------|---------------------|---------------------|
| Boilerplate, docs, tests unitarios | 60–70% | 3–5x | Equipos con buenas specs |
| Diseño, debugging complejo, decisiones | 10–20% | 1.2–1.5x | Solo con seniors con criterio |
| Integración y verificación | 5–15% | 0.8–1.1x | Requiere inversión previa en evals |

El tercer tipo (integración y verificación) puede tener ROI menor a 1 en el corto plazo si no se invierte en evaluar el código generado. Este es el riesgo no articulado de las implementaciones apresuradas.

## Gestionar al stakeholder: la pedagogía como competencia ejecutiva

**■ PISTA EJECUTIVA**


En consecuencia, la gestión de expectativas se convierte, ante todo, en un ejercicio de pedagogía ejecutiva. El líder debe traducir la complejidad de la asimetría generación/verificación a un lenguaje que el stakeholder no técnico pueda entender y actuar sobre ella.

Tres mensajes resultan imprescindibles y no negociables: primero, **la generación es barata, pero la corrección es cara** (el costo del error en código generado por IA y no verificado es comparable al del código escrito bajo presión de tiempo, y en algunos casos superior); segundo, **la velocidad sin verificación es deuda disfrazada de progreso** (el incremento que se entrega en días pero introduce bugs en producción no tiene ROI positivo); tercero, **el valor no está en producir más código, sino en producir el código correcto** (la métrica de líneas de código generadas por sprint es un indicador de proceso, no de valor de negocio).

Quien comunica estos tres mensajes con claridad y sostenibilidad no solo gobierna las expectativas: convierte la adopción de IA en una ventaja competitiva real en lugar de en una presión de marketing.

**Versión alternativa (mayor densidad académica):**

La gestión de las expectativas temporales en proyectos de desarrollo de software con asistencia de inteligencia artificial generativa constituye un problema de comunicación estratégica que involucra la traducción de asimetrías técnicas (específicamente, la divergencia entre la reducción de los tiempos de generación de código y la ausencia de reducción equivalente en los tiempos de verificación y validación) a marcos cognitivos accesibles para actores organizacionales con distintos niveles de alfabetización técnica. La evidencia empírica disponible ([Peng et al., 2023](#ref-peng2023); [Vaithilingam et al., 2022](#ref-vaithilingam2022)) sugiere que la falta de esta traducción constituye el factor primario de la brecha entre las expectativas declaradas sobre la productividad de la IA y los resultados medidos en proyectos reales.

## Lo esencial del capítulo 10

- La IA desplaza la incertidumbre de los plazos de la generación a la verificación; el cuello de botella migró del teclado al criterio.
- Peng et al. (2023): +55% en velocidad de generación de código, sin reducción proporcional en tiempo de verificación.
- Vaithilingam et al. (2022): más tareas completadas con IA, pero más bugs introducidos (la menor fricción de generación inhibe la verificación espontánea).
- Los story points deben descomponerse en complejidad de generación y complejidad de verificación; la IA reduce el primero, no el segundo.
- El DoD agéntico incluye casos límite, revisión de seguridad, consistencia con el contexto del sistema y evaluación de deuda.
- El CI/CD para código IA extiende el pipeline con análisis estático reforzado, mutación, rastreo de autoría y eval automático de comportamiento.
- El ROI es bimodal: 3–5x en boilerplate/docs/tests; 0.8–1.1x en integración y verificación sin inversión previa en evals.
- Gestionar stakeholders es pedagogía: la generación es barata, la corrección es cara; la velocidad sin verificación es deuda disfrazada.
