# Capítulo 16: PMBOK y los nuevos avances de agentes y multiagentes de IA: visión de una simbiosis

> *El PMBOK no muere con la IA; encuentra en ella el ejecutor que sus principios siempre presupusieron.*

## El PMBOK no es burocracia: es memoria destilada

Conviene desmontar un prejuicio extendido: el PMBOK es la cristalización de décadas de aprendizaje colectivo sobre cómo no fracasar gestionando proyectos, no papeleo. Sus áreas de conocimiento (alcance, tiempo, costo, riesgo, calidad, comunicaciones, adquisiciones, recursos, interesados e integración) son, en el fondo, un mapa de los lugares donde los proyectos mueren. La séptima edición ([PMI, 2021](#ref-pmbok2021)), en particular, experimentó un giro conceptual relevante: transitó de la prescripción de procesos a la articulación de principios y a la medición de valor entregado. Este viraje aproxima el PMBOK al terreno donde la IA agéntica puede aportar de manera más directa.

No resulta ocioso señalar que dicha transición hacia los principios no fue arbitraria. La investigación de Joslin y Müller (2015) demostró que el éxito de un proyecto está más correlacionado con la gobernanza subyacente (los principios que orientan las decisiones) que con el seguimiento mecánico de procesos específicos. En este contexto, los principios del PMBOK 7 operan como invariantes estratégicas que los agentes pueden ejecutar sin necesidad de entender su justificación: la vigilancia de riesgos, la comunicación de estado, la proyección de costos, son todas tareas que un enjambre puede sostener en tiempo real.

## La simbiosis: qué aporta cada parte

La relación entre PMBOK e IA agéntica es complementaria, no competitiva. El PMBOK aporta el **marco de gobernanza**: qué vigilar, qué riesgos anticipar, cómo medir valor, cuándo escalar. Los agentes aportan la **capacidad de ejecución continua y sin fatiga**: vigilar esos riesgos en tiempo real, recalcular el cronograma ante cada cambio, mantener actualizada la documentación que ningún humano quiere mantener, sintetizar el estado del proyecto para los interesados a cualquier hora.

| Área PMBOK          | Aporte del agente agéntico                                     |
|---------------------|----------------------------------------------------------------|
| Gestión de riesgos  | Monitoreo continuo, alerta temprana, simulación Monte Carlo    |
| Gestión del tiempo  | Recálculo dinámico ante cambios, análisis de ruta crítica      |
| Gestión de costos   | Proyección en tiempo real, detección de desvíos por umbral     |
| Comunicaciones      | Síntesis automática de estado para stakeholders                |
| Calidad             | Verificación sistemática de entregables contra criterios       |
| Gestión de alcance  | Análisis de impacto de cambios y trazabilidad de requisitos    |
| Gestión de recursos | Optimización de asignación y detección de sobreasignaciones    |

El PMBOK dice *qué* gestionar; los agentes hacen posible gestionarlo *sin interrupción*. Esta división del trabajo respeta la estructura conceptual que el PMBOK ha construido durante décadas, mientras libera al gestor humano del peso de la ejecución mecánica.

## Lo que la IA no puede tomar del PMBOK: el núcleo irreductiblemente humano

Existe, no obstante, un núcleo que permanece irreductiblemente humano. La **gestión de interesados** (entender la política, la emoción y el poder que rodean a un proyecto) exige una comprensión social que ningún agente posee. Un director de proyecto experto sabe cuándo la información correcta, comunicada de la manera equivocada al interesado equivocado, convierte un aliado en un obstáculo. Los agentes pueden sintetizar información; no pueden leer la sala.

Del mismo modo, la decisión de cerrar o pivotar un proyecto (con todas sus implicaciones humanas, presupuestarias y políticas) es accountability pura (cf. Vol. 3, cap. 15): indelegable. El valor de la simbiosis correcta no consiste en entregar el PMBOK a la IA, sino en **liberar al gestor humano de lo mecánico para que se concentre en lo verdaderamente humano**: la negociación política, la decisión de propósito, el mantenimiento de la coalición de apoyo del proyecto.

## El riesgo de la automatización ciega: métricas perfectas sobre un proyecto que naufraga

Aquí se impone una advertencia técnica de primer orden. Automatizar el seguimiento de un proyecto con agentes sin comprender *por qué* el PMBOK pide ese seguimiento conduce a un antipatrón peligroso: métricas perfectas sobre un proyecto que naufraga. El agente producirá informes impecables de avance mientras el proyecto se desintegra por razones que ninguna métrica captura, falta de apoyo ejecutivo, conflictos interpersonales no resueltos, cambio no comunicado en las prioridades de negocio.

La herramienta amplifica el criterio, no lo reemplaza. Un gestor que no entiende por qué el PMBOK pide la gestión de riesgos no puede diseñar los agentes que la automaticen con sentido; solo puede automatizar el artefacto sin el principio. Y el artefacto sin el principio es documentación cara e inútil.

---

## Perspectiva técnica avanzada

**► PISTA TÉCNICA**


### Agente de gestión de riesgos: implementación del registro de riesgos vivo

Desde la óptica del **Arquitecto Senior**, la gestión de riesgos del PMBOK puede implementarse como un agente que mantiene un registro de riesgos vivo, actualizado por señales del entorno del proyecto:

```python
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from enum import Enum

class RiskLevel(Enum):
    LOW      = "low"
    MEDIUM   = "medium"
    HIGH     = "high"
    CRITICAL = "critical"

@dataclass
class Risk:
    id:          str
    description: str
    probability: float   # 0-1
    impact:      float   # 0-1 (normalizado)
    owner:       str     # siempre humano (accountability RACI)
    detected_at: datetime = field(default_factory=datetime.utcnow)
    mitigated:   bool    = False

    @property
    def score(self) -> float:
        return round(self.probability * self.impact, 3)

    @property
    def level(self) -> RiskLevel:
        if self.score >= 0.70:   return RiskLevel.CRITICAL
        if self.score >= 0.40:   return RiskLevel.HIGH
        if self.score >= 0.15:   return RiskLevel.MEDIUM
        return RiskLevel.LOW


class RiskRegistryAgent:
    """
    Agente que mantiene el registro de riesgos vivo.
    Detecta riesgos emergentes, actualiza scores y alerta al humano responsable.
    El rol Accountable (owner) siempre es humano (cf. RACI, Vol. 3, cap. 15).
    """
    def __init__(self):
        self._registry: dict[str, Risk] = {}

    def register(self, risk: Risk) -> None:
        self._registry[risk.id] = risk

    def update_score(self, risk_id: str, probability: float, impact: float) -> Risk:
        risk             = self._registry[risk_id]
        risk.probability = probability
        risk.impact      = impact
        return risk

    def critical_risks(self) -> list[Risk]:
        return [r for r in self._registry.values()
                if r.level == RiskLevel.CRITICAL and not r.mitigated]

    def generate_executive_summary(self) -> str:
        risks     = list(self._registry.values())
        critical  = [r for r in risks if r.level == RiskLevel.CRITICAL]
        high      = [r for r in risks if r.level == RiskLevel.HIGH]
        mitigated = [r for r in risks if r.mitigated]
        return (
            f"Resumen ejecutivo de riesgos — {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}\n"
            f"Total: {len(risks)} | Críticos: {len(critical)} | "
            f"Altos: {len(high)} | Mitigados: {len(mitigated)}"
        )
```

### Simulación Monte Carlo para el cronograma

El **Ingeniero Senior** implementa el análisis de ruta crítica con simulación Monte Carlo para proporcionar rangos de finalización probabilísticos, no fechas falsamente precisas:

```python
import random
from statistics import mean, stdev

def monte_carlo_schedule(
    tasks: list[dict],   # cada tarea: {name, optimistic, most_likely, pessimistic}
    iterations: int = 10_000,
) -> dict:
    """
    Simula el cronograma del proyecto usando distribución PERT.
    Retorna percentiles P50, P80, P90 de duración total.
    """
    totals = []
    for _ in range(iterations):
        total = 0
        for task in tasks:
            # Distribución PERT (beta modificada)
            opt, ml, pess = task["optimistic"], task["most_likely"], task["pessimistic"]
            mu    = (opt + 4 * ml + pess) / 6
            sigma = (pess - opt) / 6
            sample = random.gauss(mu, sigma)
            total += max(opt, min(pess, sample))
        totals.append(total)

    totals.sort()
    n = len(totals)
    return {
        "P50": round(totals[int(n * 0.50)], 1),
        "P80": round(totals[int(n * 0.80)], 1),
        "P90": round(totals[int(n * 0.90)], 1),
        "mean": round(mean(totals), 1),
        "stdev": round(stdev(totals), 2),
    }
```

### Estrategia de QA: verificación sistemática de entregables

El **QA Senior** diseña un agente que verifica cada entregable contra los criterios de calidad definidos en el plan del proyecto, generando un informe de conformidad antes de que el entregable llegue al interesado:

```python
@dataclass
class QualityCheck:
    deliverable_id:   str
    criteria:         list[str]
    verified_at:      Optional[datetime] = None
    passed:           Optional[bool]     = None
    findings:         list[str]          = field(default_factory=list)

class DeliverableQAAgent:
    def verify(self, deliverable: str, check: QualityCheck) -> QualityCheck:
        # Aquí se invocaría el LLM con los criterios como prompt de evaluación
        # El resultado es una lista de findings y un veredicto booleano
        check.verified_at = datetime.utcnow()
        # [Invocación LLM omitida para brevedad]
        return check
```

---

## Perspectiva ejecutiva

**■ PISTA EJECUTIVA**


### Visión del Product Owner: el PMBOK como backlog de gobernanza

El **Product Owner** de un proyecto con componente agéntico trata las áreas de conocimiento del PMBOK como **épicas de gobernanza** del producto. Cada área se traduce en un conjunto de historias de usuario agénticas con criterios de aceptación medibles:

- *"Como gestor de proyecto, quiero recibir diariamente un resumen ejecutivo de riesgos críticos, generado por el agente de riesgos, para poder actuar antes de que el riesgo escale."*
- *"Como patrocinador, quiero que el agente de costos genere una alerta cuando la variación presupuestaria supere el 10%, con proyección de fin de proyecto actualizada."*

La diferencia respecto al PMBOK tradicional es la frecuencia: donde antes el gestor producía estos artefactos semanalmente con esfuerzo manual considerable, ahora el agente los produce diariamente o en tiempo real, dejando al gestor libre para la gestión de interesados y la toma de decisiones de fondo.

### Visión del Scrum Master: ceremonias del PMBOK con agentes

El **Scrum Master** facilita la integración de los artefactos agénticos del PMBOK en las ceremonias existentes. El Registro de Riesgos vivo se revisa en la Daily como un ítem de agenda de 2 minutos; el resumen ejecutivo de costos se incorpora a la Sprint Review como contexto para el patrocinador; el análisis Monte Carlo del cronograma se presenta en la Sprint Planning para calibrar el alcance del sprint frente al riesgo de calendario.

El agente *prepara* los datos; el Scrum Master *facilita* la conversación sobre ellos. Confundir estos roles (dejar que el agente también "facilite" la conversación) reproduce la confusión RACI del capítulo anterior: el agente como Aprobador de la dinámica del equipo.

---

## Versión académica alternativa (mayor densidad formal)

> La viabilidad de la integración entre los marcos de gestión de proyectos y los sistemas multiagente puede examinarse a través de la lente de la teoría de sistemas adaptativos complejos ([Holland, 1992](#ref-holland1992)). En dicha teoría, los agentes del sistema responden a señales locales siguiendo reglas simples, de cuya interacción emergen comportamientos globales complejos y adaptativos. El PMBOK, en su séptima edición, provee precisamente esas reglas simples: principios de gobernanza que, cuando son ejecutados de manera distribuida por agentes especializados, producen un comportamiento sistémico equivalente al de una organización de proyecto bien gobernada. La investigación de Joslin y Müller (2015) sobre el gobierno de proyectos confirma empíricamente que la claridad de los principios de gobernanza predice el éxito del proyecto con mayor fiabilidad que la adherencia a procesos específicos, un resultado congruente con la arquitectura de principios distribuibles que aquí se propone. En suma, la simbiosis PMBOK-agentes es una convergencia estructural entre la teoría de gestión de proyectos y la arquitectura de sistemas multiagente, no una adaptación superficial.

---

## Lo esencial del capítulo 16

- El PMBOK 7, centrado en principios y valor, se aproxima al terreno donde la IA agéntica puede ejecutar de forma más directa y continua.
- La simbiosis es complementaria: el PMBOK aporta gobernanza y criterios; los agentes aportan ejecución continua, monitoreo en tiempo real y síntesis automática.
- El Registro de Riesgos vivo, la simulación Monte Carlo del cronograma y la verificación sistemática de entregables son los primeros tres patrones de implementación.
- La gestión de interesados y la decisión de cerrar o pivotar el proyecto permanecen irreductiblemente humanas: exigen subjetividad moral y accountability.
- Automatizar sin comprender los principios subyacentes produce métricas perfectas sobre un proyecto que naufraga.
- El Product Owner trata las áreas del PMBOK como épicas de gobernanza con historias de usuario agénticas medibles; el Scrum Master integra los artefactos agénticos en las ceremonias existentes.
