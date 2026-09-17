# Capítulo 14: Katas de agentes de IA concursando para obtener ellos mismos un premio

> *La kata no se diseña para que el agente acierte, sino para revelar cómo razona cuando podría equivocarse.*

## La kata como banco de pruebas del razonamiento bajo restricciones

En la tradición del software artesanal, una *kata* es un ejercicio repetible diseñado no para producir un resultado útil sino para **perfeccionar la técnica del ejecutante**. Dave Thomas, co-autor del *Pragmatic Programmer*, popularizó el concepto aplicado al código: pequeños problemas bien definidos que se resuelven repetidamente con distintas restricciones, hasta que la solución se vuelve natural e instintiva. La kata no entrena la solución; entrena al solucionador.

Trasladada al dominio de los agentes de IA, la kata adquiere un matiz radicalmente diferente que conviene precisar desde el inicio: **no entrena al agente**: el modelo ya está entrenado; sus pesos no cambian durante la kata, , sino que **revela la arquitectura de su razonamiento bajo restricciones**. Esto es extraordinariamente valioso, porque lo que un agente hace bajo restricción (de tiempo, de herramientas, de formato, de costo) expone el núcleo de su proceso de razonamiento de una forma que las tareas sin restricción no permiten.

Inspirado en encuentros de arquitectura de software como los que el autor menciona (donde figuras como Sam Newman, autor de *Building Microservices*, moderan debates entre arquitectos sobre las mismas decisiones de diseño) puede imaginarse un formato equivalente para agentes: distintos agentes atacan el mismo problema arquitectónico, y un panel mixto de evaluadores humanos y sintéticos juzga no solo el resultado sino el camino, los trade-offs explicitados y la coherencia de la justificación.

## Las competiciones existentes: SWE-bench, AgentBench y WebArena como katas formales

La academia ha producido ya un conjunto de benchmarks que funcionan, en la práctica, como katas formales para agentes: problemas bien definidos, con restricciones explícitas, criterios de éxito verificables y un panel de evaluación estandarizado. Su análisis revela qué capacidades son realmente difíciles para los agentes actuales.

**SWE-bench** (Jimenez et al., 2024, ICLR 2024): quizás el benchmark más revelador publicado hasta la fecha. Presentado como "¿pueden los modelos de lenguaje resolver issues reales de GitHub?", el benchmark consiste en 2,294 tareas extraídas de repositorios de código Python reales, donde el agente debe modificar el código fuente para resolver un bug o implementar una feature, pasando los tests de la issue. A principios de 2024, los mejores modelos resolvían menos del 5% de las tareas; a finales de 2024, los mejores sistemas multiagente (Claude 3.5 Sonnet con herramientas de edición de código) alcanzaron el 49%. El salto de 5% a 49% en doce meses es la evidencia empírica más contundente disponible del valor de la arquitectura multiagente sobre el modelo aislado.

**AgentBench** (Liu et al., 2024, ICLR 2024): evalúa agentes en ocho entornos interactivos distintos (navegación web, uso de sistemas operativos, bases de datos, juegos, etc.) que requieren tomar acciones secuenciales con consecuencias reales en el entorno. El benchmark reveló que la capacidad de los modelos en entornos interactivos es significativamente menor que en tareas de pregunta-respuesta: los mejores modelos alcanzaban ~70-80% en QA estática y solo 40-50% en tareas agénticas interactivas, una brecha del 30% que captura exactamente la diferencia entre saber y actuar.

**WebArena** (Zhou et al., 2024, ICLR 2024): evalúa la capacidad de agentes para completar tareas en entornos web realistas (comprar un producto, hacer una reserva, interactuar con redes sociales simuladas) con interfaces reales de usuario. La complejidad de navegar interfaces diseñadas para humanos, no para agentes, produjo tasas de éxito iniciales de solo 14-18% para los mejores modelos. El benchmark es una kata particularmente exigente porque el entorno adversarial (diseñado sin considerar la perspectiva del agente) no tiene atajos.

Estos tres benchmarks son, en esencia, katas formalizadas que la comunidad científica usa para calibrar el estado del arte. Los equipos que los adoptan internamente (adaptados a sus dominios específicos) obtienen un sensor preciso de la capacidad real de sus sistemas, mucho más honesto que los benchmarks sintéticos.

## El giro provocador: el agente compite por su propio premio

Aquí reside la idea más audaz del capítulo, la que merece ser examinada con precisión técnica antes de aceptarse o rechazarse. ¿Qué ocurre si el incentivo del concurso se hace explícito para los propios agentes como parte de su función objetivo, no como metáfora sino como parámetro de diseño?

No se trata de antropomorfizar la ambición ni de atribuir al agente motivaciones que no tiene. Se trata de algo más preciso y más interesante: diseñar **funciones objetivo donde cada agente maximiza una recompensa explícita** que depende de su desempeño relativo al de otros agentes atacando el mismo problema. La competencia, así estructurada, hace emerger comportamientos que la cooperación pura tiende a suprimir.

Un agente que sabe que su respuesta será juzgada contra la de otros agentes con los mismos recursos tiende, cuando el sistema está bien diseñado, a:
- Justificar más explícitamente sus elecciones (porque el evaluador puede comparar justificaciones)
- Anticipar objeciones a su solución (porque otro agente las formulará)
- Refinar la solución más allá del primer borrador aceptable (porque "aceptable" no es suficiente para ganar)
- Ser más preciso en las afirmaciones que hace (porque las afirmaciones erróneas son más visibles en comparación)

Estos comportamientos emergen no de la instrucción explícita "sé más cuidadoso", sino de la estructura competitiva de la función objetivo. La rivalidad controlada es, paradójicamente, un motor de calidad más eficaz que la instrucción directa de calidad, precisamente porque opera sobre los incentivos en lugar de sobre las instrucciones.

## Teoría de funciones objetivo en agentes competitivos: el fundamento técnico

El fundamento teórico de las katas competitivas para agentes reside en la literatura sobre sistemas multiagente con funciones objetivo mixtas (cooperativas y competitivas). En el formalismo de la teoría de juegos, un enjambre donde los agentes maximizan funciones objetivo individuales en un entorno compartido es un **juego de suma cero** o **suma variable** según la estructura de las recompensas.

Para una kata agéntica bien diseñada, la función objetivo tiene tres componentes:

```
R_agente(i) = w₁ · Q_resultado(i) + w₂ · Q_razonamiento(i) + w₃ · Q_eficiencia(i)
             - w₄ · Penalización_alucinaciones(i)
             + w₅ · Bonus_primer_lugar
```

Donde:
- **Q_resultado**: calidad del resultado final (determinista si hay ground truth, por modelo si no la hay)
- **Q_razonamiento**: calidad del proceso de razonamiento exhibido (evaluado por juez LLM o humano)
- **Q_eficiencia**: inversamente proporcional a los tokens, tiempo o llamadas a herramientas utilizados
- **Penalización_alucinaciones**: coste por afirmaciones incorrectas o fabricadas detectadas
- **Bonus_primer_lugar**: incentivo relativo por superar a los competidores en el escenario específico

Los pesos w₁-w₅ no son fijos; varían según el objetivo de la kata. Una kata orientada a eficiencia asigna peso alto a w₃; una kata orientada a calidad de razonamiento asigna peso alto a w₂. La variación de los pesos entre distintas katas del mismo problema revela dimensiones del comportamiento agéntico que ninguna kata con pesos fijos puede capturar.

## Anatomía de una kata agéntica completa

Una kata agéntica bien estructurada tiene cinco elementos que no pueden omitirse sin degradar su valor diagnóstico:

| Elemento | Función | Criterio de calidad |
|----------|---------|---------------------|
| **Enunciado restringido** | Define el problema con límites explícitos (latencia, costo, consistencia, herramientas disponibles) | Ambigüedad mínima; restricciones verificables |
| **Competidores heterogéneos** | Distintos agentes con distintos modelos base, estrategias o configuraciones | Suficiente diversidad para que emerjan enfoques cualitativamente distintos |
| **Panel juez mixto** | Evaluadores humanos + agente evaluador con criterios explícitos | Criterios acordados antes de la kata; desacuerdos documentados |
| **Función objetivo explícita** | La recompensa que cada agente maximiza, con pesos conocidos por todos los participantes | Transparencia: todos los agentes conocen los criterios antes de comenzar |
| **Retrospectiva estructurada** | Análisis de *por qué* ganó la solución ganadora, no solo *qué* ganó | Extracto de patrones generalizables, no solo celebración del resultado |

La retrospectiva estructurada es el elemento más frecuentemente omitido y el más valioso. Sin ella, la kata produce un ranking pero no un aprendizaje. Con ella, la kata produce un catálogo de patrones que el equipo puede reutilizar en sistemas reales.

## Diseño de evaluaciones internas: guía técnica para equipos

**► PISTA TÉCNICA**


La transposición de las katas competitivas al contexto organizacional requiere adaptar los elementos académicos a las necesidades y restricciones del equipo. Una guía técnica mínima para implementar la primera kata interna:

**Paso 1: Selección del dominio problema**: elegir un problema real del sistema en producción donde existe ambigüedad genuina sobre cuál es la mejor solución. Los problemas de diseño arquitectónico son especialmente adecuados porque tienen múltiples soluciones defensibles con trade-offs distintos.

**Paso 2: Definición de restricciones operacionales**: especificar explícitamente qué herramientas tiene disponibles cada agente, cuál es el presupuesto en tokens o en tiempo, y qué restricciones del sistema deben respetarse. Las restricciones hacen la kata; sin ellas, es solo una consulta al LLM.

**Paso 3: Configuración de los competidores**: desplegar entre tres y cinco instancias de agente con distintas configuraciones (modelos base distintos, system prompts distintos, herramientas distintas, temperaturas distintas). La diversidad de configuración es la que produce diversidad de enfoques.

**Paso 4: Criterios de evaluación explícitos**: acordar antes de la kata cómo se evalúa cada dimensión de la función objetivo. Sin acuerdo previo, la retrospectiva se convierte en debate sobre los criterios en lugar de sobre los resultados.

**Paso 5: Retrospectiva con extracción de patrones**: no solo discutir qué agente ganó sino extraer los patrones generalizables de la solución ganadora y los errores evitables de las soluciones perdedoras. Los patrones se documentan como conocimiento del equipo (cf. cap. 31).

## Por qué la kata agéntica educa a sus diseñadores

Conviene subrayar el beneficio menos evidente y de mayor impacto de la kata agéntica: no solo evalúa agentes, **educa a los ingenieros y arquitectos que los diseñan**. Este efecto educativo es cualitativamente diferente al de leer un paper o asistir a una conferencia.

Observar a cinco agentes atacando el mismo problema arquitectónico (algunos eligiendo consistencia fuerte, otros disponibilidad, otros un híbrido) ilumina los trade-offs con una claridad que ningún tratado teórico iguala. Los trade-offs dejan de ser abstracciones académicas y se convierten en diferencias observables de comportamiento: el agente que eligió consistencia fuerte falla en la tarea de baja latencia; el que eligió disponibilidad produce resultados inconsistentes en el escenario de partición de red. La kata convierte los trade-offs del teorema CAP ([Brewer, 2000](#ref-brewer2000)) en comportamiento observable.

El mayor beneficiario de la kata no es el agente ganador; es el equipo que la diseñó, la ejecutó y analizó los resultados. La kata es, en última instancia, un dispositivo de aprendizaje para sus creadores. El premio del agente es, en última instancia, el aprendizaje del humano que lo observa.

## El hackathon agéntico como programa ejecutivo

**■ PISTA EJECUTIVA**


La kata agéntica, escalada al nivel organizacional, se convierte en el hackathon agéntico: un evento de uno a tres días donde equipos de ingenieros diseñan, implementan y compiten con enjambres de agentes para resolver un problema de negocio real. A diferencia del hackathon clásico (donde se construye software funcionando en tiempo récord), el hackathon agéntico produce dos outputs simultáneos: un sistema agéntico potencialmente desplegable y un catálogo de patrones aprendidos durante el proceso de competencia.

Las organizaciones que han implementado hackathons agénticos en 2023-2024 (Amazon, Google, Salesforce y numerosas empresas medianas del sector fintech) reportan tres beneficios consistentes: aceleración del ciclo de aprendizaje en el dominio de la IA agéntica, identificación de talento interno con capacidades de diseño de enjambres que no eran visibles en el trabajo cotidiano, y generación de al menos uno o dos patrones de arquitectura directamente aplicables a sistemas en producción.

**Versión alternativa (mayor densidad académica):**

El diseño de ejercicios competitivos para sistemas de agentes de inteligencia artificial generativa constituye una metodología de evaluación que supera en densidad informacional a los benchmarks estáticos convencionales por al menos tres razones. Primera, las tareas con restricciones explícitas inducen comportamientos adaptativos que las tareas sin restricción no activan, revelando dimensiones del espacio de razonamiento del agente que permanecen ocultas en condiciones estándar. Segunda, la comparación relativa entre agentes con distintas configuraciones sobre el mismo problema produce una señal contrastiva de alta relación señal-ruido respecto de los sistemas de evaluación absolutos, donde los factores de varianza del problema se mezclan con los factores de varianza del agente. Tercera, la retrospectiva estructurada post-competencia convierte el conocimiento implícito del panel evaluador en conocimiento explícito documentado y transferible al equipo organizacional.

## Lo esencial del capítulo 14

- La kata agéntica no entrena al agente (cuyos pesos no cambian): revela la arquitectura de su razonamiento bajo restricciones.
- SWE-bench ([Jimenez et al., 2024](#ref-jimenez2024)): de 5% a 49% de tasa de resolución de issues reales de GitHub en 12 meses (evidencia empírica del valor de la arquitectura multiagente).
- AgentBench ([Liu et al., 2024](#ref-liu2024)): brecha del 30% entre desempeño en QA estática (~75%) y en tareas agénticas interactivas (~45%); mide la diferencia entre saber y actuar.
- WebArena ([Zhou et al., 2024](#ref-generic2024zhou)): 14-18% de tasa de éxito en entornos web reales; las interfaces diseñadas para humanos son katas adversariales para agentes.
- La función objetivo competitiva (R = w₁·Q_resultado + w₂·Q_razonamiento - w₄·Penalización_alucinaciones + w₅·Bonus) hace emerger justificación, anticipación de objeciones y precisión sin instrucción directa.
- La kata tiene cinco elementos no omitibles: enunciado restringido, competidores heterogéneos, panel juez mixto, función objetivo explícita y retrospectiva estructurada.
- El mayor beneficiario de la kata es el equipo que la diseñó, no el agente ganador: convierte trade-offs abstractos en comportamiento observable.
