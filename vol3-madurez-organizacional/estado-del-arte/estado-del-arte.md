# Estado del Arte: Gobernanza, Rendición de Cuentas y Supervisión Humana en Sistemas de IA Autónomos

*Revisión crítica de literatura indexada (2019–2026), elaborada como respaldo académico del Volumen 3: Madurez Organizacional*

## 1. Líneas de investigación principales

**Línea 1: Gobernanza de IA como campo consolidado.** La revisión sistemática de Batool, Zowghi y Bano (2023/2024, arXiv:2401.10896) es la referencia más citada del campo de *Responsible AI Governance*; establece que, aunque existen numerosos principios y marcos de gobernanza, persiste una falta de alineación entre esos principios y su implementación real en modelos organizacionales de liderazgo y toma de decisiones, el mismo vacío que el capítulo 20 de este volumen intenta cerrar con un protocolo operativo, no solo declarativo.

**Línea 2: Marcos normativos y de riesgo.** Convergen aquí el NIST AI Risk Management Framework (2023), la norma ISO/IEC 42001 (2023) y el EU AI Act, todos citados de forma recurrente como los tres marcos estructurales de referencia (Floridi & Cowls, 2019; Mittelstadt, 2019; OECD, 2022, según la síntesis de "The Governance Inversion Hypothesis", 2026). Es notable que la literatura reciente empieza a documentar una tensión que este libro también aborda: los marcos normativos avanzan más lento que la capacidad técnica de los sistemas que buscan regular (Anderljung et al., 2023, citado en la SLR sobre cumplimiento en sectores críticos).

**Línea 3: Rendición de cuentas (*accountability*) y responsabilidad distribuida.** Es la línea directamente conectada con el capítulo 15 de este volumen (RACI con agentes). La literatura reciente sobre responsabilidad legal y organizacional en sistemas autónomos (análisis comparativo de regulación y marcos de gobernanza basados en riesgo, 2026) señala explícitamente que los métodos actuales para asignar responsabilidad entre los distintos roles de un sistema de IA siguen siendo fragmentarios, y que la falta de claridad se agrava en sistemas complejos multi-componente (Stahl, 2023; Yazdanpanah et al., 2023), exactamente el problema que el "RACI a escala" de este libro busca resolver con una regla operativa concreta, no solo con un llamado a mayor claridad.

**Línea 4: Gobernanza de IA agéntica en operaciones empresariales.** Una revisión sistemática de 2025 sobre el auge de la IA agéntica en operaciones empresariales documenta ahorros de costos y mayor eficiencia operativa reportados por organizaciones adoptantes, junto con preocupaciones recurrentes sobre rendición de cuentas ética, seguridad de datos y su efecto en el empleo humano (Chan et al., 2023, citado en esa SLR). La misma revisión destaca que la IA agéntica ha ganado tracción particular en entornos de alto riesgo como salud y finanzas (Gridach et al., 2025), dominios estructuralmente análogos al "caso sectorial" que cierra el capítulo 5 del Vol. 4 de esta serie.

## 2. Marcos teóricos utilizados

La literatura de gobernanza de IA no parte de una teoría única, sino que importa marcos de tres tradiciones distintas: **ética aplicada** (los principios de Floridi & Cowls, con su síntesis de "AI4People"), **teoría organizacional clásica de burocracia** (Bovens & Zouridis, 2002, "From Street-Level to System-Level Bureaucracies", un antecedente directo (aunque anterior a los LLMs) de la pregunta de qué ocurre con la discrecionalidad humana cuando un sistema de información automatiza decisiones), y **gestión de riesgo** (los marcos NIST/ISO ya mencionados). Este volumen adopta implícitamente una síntesis de las tres, pero lo hace de forma más operacional que la mayoría de la literatura revisada: donde los marcos académicos declaran principios (transparencia, explicabilidad, supervisión humana), el capítulo 20 de este libro los convierte en un umbral numérico (el Índice de Autonomía Operativa) y un protocolo de auditoría ejecutable.

## 3. Metodologías aplicadas

Predominan las revisiones sistemáticas de literatura con protocolo explícito (varias de las citadas siguen PRISMA o variantes de Kitchenham), meta-análisis de marcos de política pública (Kluge Correa et al., analizando 200 políticas y guías éticas globales para identificar 17 principios prevalentes), y estudios de caso sectoriales (salud, finanzas, sector público). Es notablemente escasa la investigación empírica que mida cuantitativamente el nivel de autonomía real de un sistema en producción, la mayoría de la literatura trabaja con categorías cualitativas (alto/bajo riesgo, supervisado/no supervisado), no con un índice continuo comparable al propuesto en este volumen.

## 4. Hallazgos recurrentes

- Consenso amplio en que la rendición de cuentas es un concepto multidimensional que ya no puede reducirse a lo legal, sino que debe abarcar supervisión organizacional, transparencia y gestión de riesgo a lo largo de todo el ciclo de vida del sistema (Novelli et al., 2024; Stahl, 2023).
- Consenso en que la ética por sí sola, sin verificación técnica y alineación de seguridad, es insuficiente como base de gobernanza, un giro que la literatura de 2024–2025 marca explícitamente como más reciente que el enfoque puramente declarativo de años anteriores.
- Tensión documentada entre innovación y cumplimiento en sectores críticos: las organizaciones reportan operar en un "corredor de cumplimiento" simultáneamente restrictivo y mal definido (Wang & Wu, 2024).

## 5. Discrepancias entre autores

La discrepancia más relevante para este volumen es de nivel de abstracción: una parte de la literatura (los marcos normativos: NIST, ISO, EU AI Act) opera al nivel de principios generales aplicables a cualquier sistema de IA; otra parte, más reciente y todavía minoritaria, empieza a reconocer que los sistemas de razonamiento de gran escala (LRMs/LLMs agénticos) son "infraestructuras de decisión socio-técnicas" que requieren gestión por nivel de riesgo, no como software convencional. Este libro se alinea explícitamente con la segunda posición, y va un paso más allá de lo que la literatura revisada ofrece: mientras la literatura académica se detiene en el diagnóstico ("se necesita gestión diferenciada por riesgo"), este volumen entrega el mecanismo (la tabla de pesos verde/amarillo/rojo del IAO).

## 6. Limitaciones metodológicas de la literatura revisada

- **Predominio de estudios de política y no de ingeniería.** La mayor parte de la literatura de gobernanza de IA proviene de escuelas de políticas públicas, derecho y ética aplicada, no de ingeniería de software; esto explica por qué son fuertes en taxonomía de principios y débiles en mecanismos operativos verificables, precisamente el vacío que este volumen, escrito desde la ingeniería, busca llenar.
- **Escasa validación empírica de los marcos propuestos.** Varias SLR citadas señalan que los marcos de gobernanza revisados rara vez incluyen evidencia de implementación exitosa medida, más allá de estudios de caso puntuales y no comparables entre sí.
- **Sesgo geográfico e institucional.** La literatura de políticas está dominada por marcos de EU, EE. UU. y organismos multilaterales (OCDE); la revisión de Frost et al. sobre la estrategia nacional de IA de Canadá es una de las pocas referencias con foco explícito fuera de esos tres polos, y ninguna de las fuentes revisadas aquí aborda con profundidad comparable a América Latina: una brecha que el capítulo sobre El Niño/Canal de Panamá y los casos de Sber (Rusia) y Doraleh (Yibuti) de este libro parcialmente compensan, aunque no sustituyen investigación académica formal sobre la región.

## 7. Brechas de conocimiento

1. **Ausencia de métricas cuantitativas de autonomía comparables entre organizaciones**: el IAO de este libro es, hasta donde esta revisión pudo verificar, una propuesta original sin antecedente directo publicado en la literatura indexada revisada.
2. **Falta de protocolos de auditoría que sean agnósticos del proveedor del modelo**: toda la literatura de auditoría de IA revisada asume un sistema con un modelo fijo; ninguna aborda explícitamente qué ocurre con la validez de una auditoría cuando el modelo subyacente cambia, el problema exacto que la auditoría de reproducción cruzada del capítulo 20 resuelve.
3. **Escasa investigación sobre RACI u otros marcos de asignación de responsabilidad humana específicamente adaptados a enjambres de decenas de agentes**: la literatura de responsabilidad distribuida es rica en principios, pero no en mecanismos de escala.

## 8. Relación con la tesis central del libro

La tesis de este volumen (que la gobernanza debe expresarse en mecanismos verificables y no solo en principios declarados, y que esa gobernanza debe sobrevivir al cambio de proveedor de modelo) encuentra en la literatura un diagnóstico convergente (la brecha entre principios y mecanismos operativos, sección 1 y 5) pero no una solución ya publicada. Esto posiciona las contribuciones originales de este volumen (el IAO y la auditoría de reproducción cruzada) no como una síntesis de lo existente, sino como una respuesta directa a una brecha que la propia literatura académica reconoce y no ha cerrado todavía.
