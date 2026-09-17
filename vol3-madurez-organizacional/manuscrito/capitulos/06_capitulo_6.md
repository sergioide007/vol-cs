# Capítulo 6: Plantillas para Proyectos con Multiagentes que Operan como Equipos de Desarrollo: Sprints, Ceremonias, Demos y el ROI que los Ejecutivos Esperan

> *Un equipo de agentes sin cadencia no es un equipo: es un caos con buena ortografía.*

---

**El hilo que conecta este capítulo con el enjambre hidrológico del Capítulo 3.** Aquel caso mostraba control bajo incertidumbre en su forma más extrema: minutos para decidir, vidas de por medio, un Agente Crítico que existía únicamente para evitar que un plan incongruente llegara a tiempo cero. Este capítulo aplica el mismo principio a una escala distinta y una cadencia mucho más lenta, semanas en vez de horas, pero la pregunta de fondo no cambia: ¿cómo se gobierna un sistema que produce resultados bajo condiciones que nadie puede predecir por completo? Donde el Capítulo 3 resolvía la incertidumbre con una capa de verificación síncrona, aquí se resuelve con cadencia, la misma apuesta de la ingeniería ágil desde hace dos décadas: no eliminar la incertidumbre, sino exponerla en intervalos regulares y baratos de corregir. Los Capítulos 4 y 5, entre uno y otro, ya prepararon el terreno: defender la arquitectura ante un comité (Cap. 4) y encontrar sus fallas antes de que las encuentre otro (Cap. 5) son, ambos, ejercicios de gobernanza bajo la misma incertidumbre estructural. Este capítulo le da a esa gobernanza un ritmo operativo.

## Sección 1: La Tesis Central: Por Qué el Ágil es la Arquitectura de Coordinación del Enjambre

Existe una tensión estructural en los sistemas multiagente que la mayoría de los frameworks técnicos ignoran: la diferencia entre un conjunto de agentes que ejecutan tareas y un **equipo de agentes que produce valor de forma sostenible**. La distinción no es semántica. Un conjunto de agentes puede procesar tickets; solo un equipo puede aprender, adaptarse y mejorar iterativamente su forma de trabajar.

Dingsøyr et al. (2023), en su estudio comparativo sobre escalado ágil en *IEEE Software* (Q2, IF 4.8), documentaron que los equipos de desarrollo de software que operan bajo cadencias explícitas (sprints, ceremonias, retrospectivas) producen software de mayor calidad medible (defect density 23% menor, deployment frequency 2.1× mayor) que los equipos sin cadencia, incluso controlando por experiencia y tamaño del equipo. La razón: la cadencia impone **observabilidad sobre el proceso**, no solo sobre el producto.

Esta lógica se traslada íntegramente a los sistemas multiagente. Un enjambre sin cadencia produce resultados, pero no produce evidencia sobre cómo produce esos resultados, qué tan confiablemente los produce, ni qué se puede mejorar. Sin esa evidencia, no hay gobernanza posible. Y sin gobernanza, no hay adopción ejecutiva sostenida.

La metodología ágil (específicamente Scrum (Schwaber & Sutherland, 2020, Scrum Guide)) no es, en este contexto, una elección cultural trasplantada al mundo de la IA. Es una **arquitectura de coordinación** con tres propiedades que resultan directamente aplicables al enjambre:

1. **Acotamiento de alcance**: el sprint delimita lo que el enjambre debe resolver en N días. Sin este acotamiento, un enjambre tiende a expandir su scope indefinidamente (el equivalente agéntico del scope creep).

2. **Cierre de ciclo de retroalimentación**: la demo y la retrospectiva crean un mecanismo de aprendizaje explícito. El enjambre no solo procesa; también reflexiona sobre su propio procesamiento.

3. **Rendición de cuentas en lenguaje de negocio**: el cuadro POI→ROI conecta cada entregable técnico con su valor para el negocio. El ejecutivo no inspecciona el código; inspecciona la trayectoria entre lo prometido y lo entregado.

---

## Sección 2: Los Roles Agénticos del Equipo Scrum

La asignación de roles Scrum a los agentes no es arbitraria. Cada rol en el equipo Scrum existe para cubrir una función específica en el ciclo de entrega; la pregunta es qué capacidades de IA modelan mejor cada una.

**Agente Product Owner (APO).**

El Product Owner en Scrum es el custodio del valor: define el backlog, prioriza, y representa los intereses del stakeholder. El APO es un agente con tres capacidades específicas:

1. **Ingesta y análisis de señales de negocio**: lee métricas de producto (conversión, retención, NPS), feedback de usuarios (Intercom, Zendesk tickets, App Store reviews), y cambios regulatorios. Traduce esas señales en User Stories con criterios de aceptación explícitos.

2. **Priorización por valor esperado**: implementa un algoritmo de priorización basado en WSJF (Weighted Shortest Job First, Scaled Agile Framework), considerando impacto esperado, urgencia relativa, reducción de riesgo y costo de oportunidad.

3. **Defensa del backlog**: cuando los agentes desarrolladores solicitan dividir una historia o simplificar la solución, el APO evalúa si la simplificación compromete el valor para el usuario final. No todo "más simple" es mejor para el negocio.

**Agentes Desarrolladores Especializados.**

A diferencia de los desarrolladores humanos (que son generalistas con especialidades), los agentes desarrolladores en un enjambre son **especialistas puros**:

- Agente Backend: implementa lógica de negocio, APIs, integración con servicios.
- Agente Frontend: genera código de interfaz, componentes, interacciones.
- Agente Infraestructura: gestiona Terraform, pipelines de CI/CD, configuración de Kubernetes.
- Agente de Documentación: mantiene la documentación técnica sincronizada con el código (docstrings, READMEs, ADRs).

Cada uno toma una User Story del backlog, la divide en tareas técnicas, las implementa, y la somete al **Agente Revisor** antes de marcarla como Done.

**Agente Revisor (Peer Review).**

Este agente implementa el proceso de revisión de código de forma nativa. Su checklist no es arbitrario; está basado en los criterios de calidad del equipo (definición de Done), los patrones arquitectónicos del proyecto (puede leer el CLAUDE.md o el ADR), y las reglas de linting/seguridad establecidas. Un incremento no es Done hasta que el Agente Revisor lo aprueba. Si lo rechaza, publica feedback específico y la historia vuelve al agente desarrollador.

**Agente Scrum Master (ASM).**

El Scrum Master en el marco ágil es el guardián del proceso, no del contenido. El ASM implementa:

- Detección de bloqueos: si un agente lleva más de 30 minutos sin publicar eventos, el ASM lo detecta como potencialmente bloqueado y escala al Coordinador.
- Moderación de ceremonias: genera la agenda del Daily, recopila los eventos del día anterior, y produce el informe de burndown en tiempo real.
- Métricas del proceso: calcula velocity sprint-over-sprint, lead time por historia, y tiempo de espera entre etapas.

---

## Sección 3: La Plantilla de Cadencia: Sprint Configurado para un Enjambre

![Sprint cadence: Planning → Daily → Demo → Retro → Quarterly Closing](imagenes/uml/c26_sprint_roles.png)

### Sprint Planning (Duración: 90 min → 15 min con enjambre)

El enjambre reduce el tiempo de Planning de 90 minutos (estándar para equipo de 5-7 humanos) a 15 minutos porque el trabajo de preparación ya está hecho:

- El APO ha priorizado el backlog y añadido criterios de aceptación detallados antes de la ceremonia.
- El Agente de Estimación ha calculado story points usando referencia histórica de velocidad del enjambre.
- Los agentes desarrolladores han revisado las historias del tope del backlog y marcado dependencias técnicas.

La ceremonia de Planning, en consecuencia, no es un ejercicio de estimación y negociación: es una **verificación de comprensión compartida** y el momento de formalizar el Sprint Goal.

```yaml
# Plantilla de Sprint Goal estructurado
sprint_goal:
  numero: 47
  fechas: "2025-01-20 / 2025-02-03"
  objetivo: "Habilitar checkout multi-moneda para usuarios LATAM"
  success_metrics:
    - metric: "conversion_rate_latam"
      baseline: 2.3%
      target: 3.1%
      medicion: "GA4 + BigQuery, día 3 post-deploy"
  historias_comprometidas:
    - id: "US-234"
      titulo: "Selector de moneda en carrito"
      story_points: 5
      agente_asignado: "agente_frontend_01"
    - id: "US-235"
      titulo: "Integración Stripe multi-currency"
      story_points: 8
      agente_asignado: "agente_backend_02"
  riesgos_identificados:
    - "API de Stripe multi-currency en beta → plan de rollback a moneda única"
```

### Daily Standup (Eliminado como ceremonia → Sustituido por Dashboard Continuo)

El Daily Standup existe en Scrum para sincronizar un equipo humano que trabaja en intervalos discontinuos. Los agentes publican eventos continuamente. En consecuencia, el Daily se transforma en un **dashboard de estado en tiempo real** que el equipo humano revisa en 5 minutos:

| Agente | Última actividad | Estado | Bloqueado | Próximo evento esperado |
|--------|-----------------|--------|-----------|------------------------|
| APO | Refinó US-236 (09:45) | Activo | No | Revisión de criterios US-237 (11:00) |
| Dev Backend | Commit US-235 al 60% (10:30) | En progreso | No | PR listo (15:00 est.) |
| Dev Frontend | US-234 en revisión (10:15) | Esperando | Revisor |, |
| Revisor | Revisando US-234 (10:20) | Activo | No | Feedback en <20 min |
| Scrum Master |, | Monitor | No | Burndown update (11:00) |

### Sprint Demo (Duración: 30 min para stakeholders)

Las demos ocurren entre agentes revisores antes de llegar a los stakeholders humanos. Un incremento solo es presentable si:

1. El Agente Revisor lo aprobó (calidad técnica).
2. Los criterios de aceptación del APO se verificaron automáticamente.
3. Los tests de aceptación (escritos por el APO como Given-When-Then) pasan en el entorno de staging.

La demo para stakeholders humanos, entonces, no es un "¿funciona?". Es un "esto funciona, estos son los números, este es el impacto esperado". El tiempo de validación técnica ya está absorbido.

### Retrospectiva (30 min al cierre del sprint)

El ASM genera el informe de retrospectiva con datos del sprint: velocity, lead time, tasa de rechazo del Revisor, bloqueeos detectados. El equipo humano (tech lead + PO) revisa el informe y toma decisiones de mejora de proceso. Tres preguntas:

1. ¿Qué patrones de bloqueo se repitieron más de dos veces? → Investigar causa raíz.
2. ¿Qué historias tomaron más del doble de su estimación? → Revisar criterio de estimación.
3. ¿El Sprint Goal se logró? → Conectar con métricas de negocio del cuadro POI→ROI.

---

## Sección 4: DORA Metrics Aplicadas al Enjambre: El Lenguaje que el CTO Entiende

**■ PISTA EJECUTIVA**


Las DORA metrics (Forsgren, Humble & Kim, 2018, *Accelerate: The Science of Lean Software and DevOps*) son el estándar industrial para medir el rendimiento de la entrega de software. Cuatro métricas, ampliamente adoptadas por la industria desde el State of DevOps Report 2023 (Google Cloud/DORA):

| Métrica DORA | Definición | Elite performer | Enjambre multiagente (benchmark 2024) |
|-------------|-----------|-----------------|---------------------------------------|
| Deployment Frequency | ¿Con qué frecuencia se despliega a producción? | Múltiples veces al día | 8–15 deploys/día (tasks menores) |
| Lead Time for Changes | ¿Cuánto tarda un commit en llegar a producción? | <1 hora | 22–45 minutos (con CI/CD integrado) |
| Change Failure Rate | ¿Qué % de deploys causan un incidente? | <5% | 3–5% (comparado con 15–25% en equipos humanos medianos) |
| Time to Restore Service | Si hay un incidente, ¿cuánto tarda en resolverse? | <1 hora | 18–35 minutos (con Agente de Diagnóstico integrado) |

La capacidad de presentar métricas DORA actualizadas ante el CTO transforma la conversación de "¿cómo va el proyecto?" a "estamos en el cuartil elite en deployment frequency y lead time, con change failure rate 40% por debajo del benchmark de nuestra industria".

---

## Sección 5: Del POI al ROI: El Cuadro que los Ejecutivos Esperan

**■ PISTA EJECUTIVA**


El cierre trimestral (Quarterly Closing) es donde el enjambre rinde cuentas en el lenguaje del negocio. El cuadro POI→ROI conecta cada Promised Outcome Indicator con su Return on Investment medido:

| Sprint | POI (prometido) | KPI de medición | ROI esperado | ROI medido | Delta |
|--------|----------------|-----------------|-------------|------------|-------|
| S-45 | Reducir tiempo de onboarding de 72h a 24h | TTFV (Time to First Value) | $120K/año ahorro CS | $134K/año | +11.7% |
| S-46 | Habilitar checkout en 3 idiomas | Tasa de conversión LATAM | +$280K/año revenue | +$312K/año | +11.4% |
| S-47 | Multi-currency LATAM | Revenue LATAM | +$220K/año revenue | En progreso |, |

Este cuadro responde a la pregunta que todo CFO hace en la revisión trimestral: "¿Qué valor entregó el equipo de IA en los últimos 90 días, en dinero?" No en features. En dinero.

**Versión académica ampliada:**

> La aplicación del marco Scrum a sistemas multi-agente puede formalizarse como un problema de coordinación bajo la teoría de juegos cooperativos ([Osborne & Rubinstein, 1994](#ref-osbornerubinstein1994)), donde el Sprint Goal opera como un **punto focal** ([Schelling, 1960](#ref-schelling1960)) que reduce la ambigüedad sobre el comportamiento esperado de cada agente sin necesidad de comunicación explícita exhaustiva. Las ceremonias, a su vez, pueden modelarse como mecanismos de revelación de información ([Myerson, 1979](#ref-myerson1979)): el Daily Dashboard revela el estado de cada agente sobre el espacio de búsqueda del sprint; la Retrospectiva es un mecanismo de actualización de creencias colectiva sobre la función de producción del enjambre. Bajo esta formalización, la cadencia ágil es un protocolo de coordinación con propiedades matemáticas analizables, no una convención organizacional: minimiza la entropía colectiva del proceso de entrega bajo una restricción de transparencia informacional.

---

## Lo esencial del capítulo 6

- La metodología ágil es la **arquitectura de coordinación** del enjambre, no un adorno cultural.
- Los cuatro roles agénticos (APO, Developers, Reviewer, Scrum Master) cubren funciones distintas del ciclo Scrum con capacidades específicas de IA.
- El Sprint Planning se reduce de 90 a 15 minutos porque el APO prepara el trabajo previo; el Daily se sustituye por un dashboard en tiempo real.
- Las **demos entre Agentes Revisores** materializan el peer review de forma nativa, el incremento es Demo-Ready solo si pasa la revisión del agente.
- Las **métricas DORA** conectan el rendimiento del enjambre con el lenguaje que el CTO comprende.
- El cuadro **POI→ROI trimestral** conecta cada entregable con su valor en dinero, el lenguaje que el CFO exige.
- La cadencia impone observabilidad, y la observabilidad hace posible la gobernanza.

---

## Ejercicio resuelto 6.1: Diseña el Quarterly Closing del enjambre

**Enunciado.** Tu enjambre completó el Q1 (Enero–Marzo 2025). Se comprometieron los siguientes POIs: (1) Reducir churn de clientes 10%, (2) Habilitar integraciones con 3 ERPs principales, (3) Reducir TTFV de 5 días a 2 días. Tienes los siguientes datos: Churn redujo 7.3%, ERP integrados: 2 de 3 (el tercero atrasado 3 semanas), TTFV actual: 2.4 días. Diseña la presentación del Quarterly Closing.

**Solución.**

## Q1 2025: Quarterly Closing: Resumen Ejecutivo

### POI 1: Churn -10% → Logrado parcialmente: -7.3%
**Impacto ROI**: $-180K proyectados vs. $-131.4K reales (-27% del objetivo)
**Análisis**: El segmento SMB redujo churn -11.2% (superó objetivo);  
el segmento Enterprise se retrasó (-3.1%). Causa raíz: el feature de  
"Customer Success Alerts" priorizó SMB por volumen de tickets.  
**Q2 action**: Dedicar 30% de capacidad del enjambre a Enterprise CS.

### POI 2: 3 ERPs integrados → Logrado 2/3 (66%)  
**Impacto ROI**: $+340K proyectados vs. $+226K reales  
**Análisis**: SAP y Oracle integrados y en producción. NetSuite  
retrasado 3 semanas por incompatibilidad de API v2 → v3.  
**ETA NetSuite**: Semana 2 de Q2. No requiere recursos adicionales.  
**Q2 commitment**: NetSuite completo + ERP adicional regional.

### POI 3: TTFV 5 días → 2 días → Logrado al 80%: 2.4 días  
**Impacto ROI**: $+95K/año (vs. $+118K proyectados)  
**Análisis**: Onboarding automatizado redujo de 5 a 3.1 días en S45.  
Optimización adicional en S46-47 bajó a 2.4 días. Brecha restante:  
paso de verificación manual de documentos (0.4 días).  
**Q2 action**: Automatizar verificación de documentos con visión computacional.

### Resumen ejecutivo Q1
| Indicador | Objetivo | Real | % cumplimiento |
|-----------|---------|------|----------------|
| Revenue impacto | $+$638K | $+$452K | 71% |
| Capacidad enjambre utilizada | 100% | 94% | 94% |
| Deployment frequency | 8/día | 11/día | 138% |
| Change failure rate | <8% | 4.3% | Elite |

> **Veredicto Q1**: 71% de impacto de revenue prometido. 2 de 3 POIs logrados. Rendimiento técnico DORA en cuartil Elite. Q2 ajusta prioridades basado en gaps identificados.

Este formato responde la pregunta ejecutiva antes de que se formule: "¿Qué logramos, qué faltó, por qué faltó, y qué haremos diferente?"

---
