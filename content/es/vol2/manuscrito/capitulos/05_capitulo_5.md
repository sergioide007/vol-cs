# Capítulo 5: Una nueva variable en la fórmula de la confianza, aplicada a agentes y multiagentes de IA

> *La confianza no se declara; se calibra. Y con agentes, hay que recalibrarla todos los días.*

## La fórmula clásica: un andamiaje insuficiente

La confianza, en su formulación canónica, se entiende como el cociente entre el producto de credibilidad, fiabilidad e intimidad, y la orientación al interés propio. Dicha fórmula (sistematizada por Maister, Green y Galford (2000)) fue concebida para relaciones entre personas. No obstante, cuando uno de los actores de la relación es un agente probabilístico, la ecuación experimenta una tensión que sus autores nunca anticiparon: ¿cómo se otorga confianza a una entidad que exhibe competencia demostrable pero comportamiento no determinista, que carece de interés propio pero tampoco asume responsabilidad, y que resulta fiable en promedio estadístico aunque impredecible en el caso concreto?

De esta tensión se colige que la fórmula original constituye un punto de partida válido, mas no suficiente. Su insuficiencia no radica en un defecto conceptual, sino en que fue diseñada en un mundo donde todos los actores de confianza son agentes morales capaces de asumir consecuencias. Los sistemas de IA no lo son, y ese hecho cambia los cimientos del problema.

## La variable que faltaba: verificabilidad como eje articulador

Ante esta laguna, ha de incorporarse una variable que la fórmula humana daba por supuesta y que, en el contexto agéntico, adquiere carácter crítico: la **verificabilidad**. Con un colaborador humano, la confianza se construye (en parte) sobre la base de una reputación acumulada y relaciones de accountability establecidas. Con un agente, la reputación importa menos que la capacidad de *examinar cada resultado producido*. Un agente cuyas salidas no pueden verificarse no resulta confiable, por elevado que sea el índice de sus aciertos; inversamente, un agente cuya producción puede auditarse de manera barata y rápida puede ganarse la confianza operativa aunque incurra en errores periódicos, puesto que el fallo resulta detectable antes de que cause daño.

Bajo este marco, la verificabilidad cumple una función análoga a la de la intimidad en la fórmula original: permite que el acto de confiar no sea un salto en el vacío, sino una apuesta informada y revisable. La diferencia fundamental reside en el mecanismo: donde la intimidad apela a la historia compartida y el conocimiento recíproco, la verificabilidad apela a la observabilidad de outputs y a la trazabilidad de procesos. Lee y See (2004) establecen que la confianza apropiada en la automatización requiere precisamente esta clase de calibración observable (ni exceso de confianza ni rechazo injustificado), un equilibrio que solo la verificabilidad hace posible.

## La ecuación reescrita: una formulación para sistemas agénticos

A partir de los argumentos expuestos, la fórmula de la confianza aplicada a agentes puede reformularse del siguiente modo:

> **Confianza agéntica ≈ (Competencia × Verificabilidad × Trazabilidad) ÷ Costo del error**

Cada término merece análisis individualizado. La **competencia** designa la capacidad demostrada del agente para ejecutar la tarea encomendada; su medición admite proxies cuantitativos: tasas de acierto en benchmarks, F1-scores sobre conjuntos de evaluación, latencia en la detección de errores. La **verificabilidad** expresa el grado en que las salidas pueden someterse a escrutinio externo sin incurrir en costos prohibitivos; en la práctica, se operacionaliza mediante agentes auditores, hashes de salida, trazas de razonamiento explícitas y mecanismos de comparación con ground-truth. La **trazabilidad** (concepto distinto, aunque relacionado) indica la posibilidad de reconstruir la cadena causal que llevó al agente a una decisión particular; técnicas como Chain-of-Thought ([Wei et al., 2022](#ref-wei2022)) y la instrumentación mediante OpenTelemetry constituyen su implementación técnica.

El denominador, **costo del error**, actúa como regulador del sistema: a mayor impacto potencial de un fallo (medido en términos financieros, reputacionales o de seguridad), mayor debe ser el nivel de verificabilidad y trazabilidad exigido antes de autorizar la acción. Se establece así un principio de proporcionalidad que ninguna fórmula binaria de confianza podría capturar.

## Confianza graduada: del binario al espectro de riesgo

Una implicación central de la formulación anterior es que, con agentes, la confianza deja de ser binaria (confío o no confío) para devenir una función continua definida sobre el espacio producto (dominio × nivel de riesgo). Se confía al agente la generación de un borrador sin supervisión; se exige verificación humana para aprobar una transferencia financiera; se requiere doble revisión para publicar código en producción sin pasar por staging. Esta gradación no constituye desconfianza: es la forma madura de relación con un colaborador probabilístico.

La analogía más precisa es la del avión autopilotado, no la del empleado en período de prueba: el sistema opera con autonomía en condiciones nominales; el piloto interviene en la maniobra de aterrizaje. La distribución de responsabilidades está calibrada en función de las consecuencias del fallo y la fiabilidad demostrada del sistema en cada subdominio, no es estática ni arbitraria. Ribeiro et al. (2016) subrayan que la confianza en modelos de machine learning exige mecanismos de explicación local (qué fundamentó *esta* decisión concreta) precisamente porque la confianza global en un modelo no garantiza su corrección en instancias individuales.

---

## Perspectiva técnica avanzada

**► PISTA TÉCNICA**


### Patrón Shadow Agent: verificabilidad como capa arquitectónica

**► PISTA TÉCNICA**


Desde la óptica del **Arquitecto de Software Senior**, la verificabilidad no emerge espontáneamente: ha de diseñarse como una capa arquitectónica explícita. El patrón recomendado es el **Shadow Agent**: un agente secundario ejecuta en paralelo al agente principal, procesa los mismos inputs, y compara su resultado con el del agente principal antes de que el output llegue al sistema downstream. Las discrepancias por encima de un umbral de tolerancia disparan un ciclo de revisión humana.

```python
from dataclasses import dataclass, field
from typing import Any, Callable, Optional
import hashlib, time

@dataclass
class TrustScore:
    competence_proxy: float   # F1 score sobre eval-set reciente [0,1]
    verifiability:    float   # 0=caja negra, 1=completamente auditable
    traceability:     float   # 0=sin reasoning, 1=CoT completo
    error_cost:       float   # 1-100: impacto normalizado del fallo

    def compute(self) -> float:
        numerator   = self.competence_proxy * self.verifiability * self.traceability
        denominator = max(self.error_cost, 0.01)
        return round(numerator / denominator, 4)

    def is_trustworthy(self, threshold: float = 0.65) -> bool:
        return self.compute() >= threshold


class TrustViolationError(RuntimeError):
    pass


class TrustGatedExecutor:
    """
    Ejecuta la acción del agente solo si supera el umbral de confianza.
    Registra el score para monitoreo continuo.
    """
    def __init__(self, trust_threshold: float = 0.65):
        self.threshold  = trust_threshold
        self._audit_log: list[dict] = []

    def execute(
        self,
        agent_fn:    Callable[[Any], Any],
        trust_score: TrustScore,
        action:      Any,
    ) -> Any:
        score   = trust_score.compute()
        ts      = time.time()
        trusty  = score >= self.threshold

        self._audit_log.append({
            "timestamp":   ts,
            "score":       score,
            "threshold":   self.threshold,
            "authorized":  trusty,
            "action_hash": hashlib.sha256(str(action).encode()).hexdigest()[:12],
        })

        if trusty:
            return agent_fn(action)
        raise TrustViolationError(
            f"Trust score {score:.3f} por debajo del umbral {self.threshold}. "
            f"Verificabilidad={trust_score.verifiability:.2f}, "
            f"Trazabilidad={trust_score.traceability:.2f}"
        )

    @property
    def override_rate(self) -> float:
        """Tasa de override: porcentaje de llamadas bloqueadas."""
        if not self._audit_log:
            return 0.0
        blocked = sum(1 for e in self._audit_log if not e["authorized"])
        return blocked / len(self._audit_log)
```

Este patrón separa la lógica de evaluación de confianza de la lógica de ejecución, cumpliendo el principio de Single Responsibility. El `TrustScore` puede actualizarse continuamente conforme el agente opera en producción, alimentado por el sistema de observabilidad.

### Trazabilidad con OpenTelemetry: la traza como artefacto de confianza

El **Ingeniero Senior** implementa la trazabilidad mediante instrumentación explícita. La traza generada permite, en auditoría posterior, reconstruir qué prompt produjo qué output, en qué momento y con qué versión del modelo:

```python
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import ConsoleSpanExporter, SimpleSpanProcessor

provider = TracerProvider()
provider.add_span_processor(
    SimpleSpanProcessor(ConsoleSpanExporter())
)
trace.set_tracer_provider(provider)
tracer = trace.get_tracer("agent.trust.tracer")

def traced_agent_call(agent_fn: Callable, prompt: str, model_version: str) -> str:
    with tracer.start_as_current_span("agent_inference") as span:
        span.set_attribute("agent.prompt_hash",
            hashlib.sha256(prompt.encode()).hexdigest()[:16])
        span.set_attribute("agent.model_version", model_version)
        span.set_attribute("agent.has_cot", "<thinking>" in prompt.lower())

        t0     = time.perf_counter()
        result = agent_fn(prompt)
        latency_ms = (time.perf_counter() - t0) * 1000

        span.set_attribute("agent.output_length",        len(result))
        span.set_attribute("agent.latency_ms",           round(latency_ms, 2))
        span.set_attribute("agent.cot_present_in_output","<thinking>" in result)
        return result
```

### Estrategia de QA: pipeline de evaluación continua de confianza

El **QA Senior** diseña un pipeline que computa el `competence_proxy` sobre un conjunto de evaluación vivo: un subconjunto de casos reales donde el ground truth es conocido. La degradación de este índice por debajo del umbral dispara una alerta de mantenimiento antes de que el impacto llegue al usuario. Se recomienda combinar evaluación automatizada con revisión humana periódica (Human-in-the-Loop evaluation, siguiendo Liang et al., 2022):

| Métrica                  | Frecuencia        | Umbral de alerta |
|--------------------------|-------------------|------------------|
| F1-score (eval-set vivo) | Cada despliegue   | < 0.80           |
| Override rate            | Diario            | > 5%             |
| Latencia de detección    | Tiempo real       | > 500 ms         |
| Discrepancia shadow      | Por inferencia    | > 15%            |

---

## Perspectiva ejecutiva

**■ PISTA EJECUTIVA**


### Visión del Product Owner: la confianza como criterio de aceptación

La confianza agéntica no es únicamente un problema de ingeniería; es también una decisión de producto. El **Product Owner** debe incorporar niveles de confianza requeridos en la Definición de Hecho (*Definition of Done*) de cada historia de usuario que involucre acción autónoma de un agente. Un ejemplo concreto:

**Historia de usuario**: *"Como usuario, quiero que el agente genere el primer borrador de mi correo de respuesta."*

**Criterio de aceptación técnico**: *"El agente debe alcanzar un trust_score ≥ 0.70 en el dominio 'redacción de correo', validado contra un eval-set de 200 ejemplos representativos, antes de operar sin revisión humana."*

Esta práctica vincula la confianza con la entrega de valor e impide que la adopción de agentes avance más rápido que la validación de su fiabilidad. El riesgo del P.O. es ceder a la presión de velocidad y desplegar agentes con trust scores no validados: los fallos subsecuentes erosionan la confianza del usuario final y generan deuda de reputación que tarda semanas en recuperarse.

### Visión del Scrum Master: override rate como métrica de salud del equipo

El **Scrum Master** introduce en las retrospectivas una métrica de equipo: la **tasa de override humano** (*human override rate*), definida como el porcentaje de acciones agénticas que fueron revertidas o corregidas por el equipo durante el sprint. Una tasa de override elevada señala calibración insuficiente del agente; una tasa de cero puede indicar complacencia peligrosa, el equipo acepta sin cuestionar, aunque el agente esté fallando en silencio.

El objetivo es una tasa baja y estable de overrides que refleje un nivel de confianza operativamente sostenible, no cero overrides. La conversación de retrospectiva es: *"¿Cuándo nos dimos cuenta del error del agente? ¿Pudimos detectarlo antes? ¿Qué mejora a la verificabilidad evitaría este override la próxima vez?"*

---

## Versión académica alternativa (mayor densidad formal)

> La introducción de la verificabilidad como constructo central en el marco de confianza agéntica puede fundamentarse en la teoría de la *accountability* distribuida ([Bovens, 2007](#ref-bovens2007)), según la cual la rendición de cuentas exige la existencia de foros capaces de examinar la conducta del actor y de imponer consecuencias en caso de desviación. En ausencia de subjetividad moral en el agente artificial, dicho examen ha de recaer sobre los artefactos observables de su comportamiento (outputs, trazas, logs). El marco propuesto operacionaliza este requisito teórico en una función computable. Desde una perspectiva bayesiana, la confianza puede entenderse como una distribución de probabilidad sobre las futuras acciones del agente, actualizada cada vez que una nueva observación verificable se incorpora al conjunto de evidencias disponibles (cf. Lee & See, 2004). La verificabilidad, en este encuadre, no es sino la tasa a la que dicha distribución puede actualizarse de forma informada, reduciendo la incertidumbre epistémica sin incurrir en costos de observación prohibitivos.

---

## Lo esencial del capítulo 5

- La fórmula clásica de la confianza (Maister et al.) es necesaria pero insuficiente para agentes probabilísticos: carece de la variable que corresponde al principal mecanismo de control disponible.
- La verificabilidad (capacidad de auditar outputs de manera barata y oportuna) reemplaza a la intimidad como cimiento de la confianza en sistemas agénticos.
- La ecuación reformulada, **Confianza agéntica ≈ (Competencia × Verificabilidad × Trazabilidad) ÷ Costo del error**, permite calibración continua y proporcional al riesgo.
- El Shadow Agent Pattern y la instrumentación con OpenTelemetry son las implementaciones técnicas principales de verificabilidad y trazabilidad, respectivamente.
- El Product Owner incorpora niveles de confianza mínimos en la Definición de Hecho; el Scrum Master monitorea la tasa de override como métrica de salud del equipo.
- La confianza graduada (no binaria) es la forma madura de relación con un colaborador probabilístico: proporcional al dominio y al coste potencial del error.
- Una override rate de cero no es éxito: es una señal de alerta de complacencia operativa.
