# Capítulo 15: RACI y Eisenhower con Agentes

> *Delegar en un agente sin definir quién responde es delegar también la rendición de cuentas. Y eso no se delega.*

## El problema de la responsabilidad difusa en equipos humano-agente

Cuando un equipo ágil incorpora agentes de IA, resurge una pregunta antigua con ropaje nuevo: ¿quién es responsable de lo que produce el agente? Sin una respuesta estructurada, el enjambre deviene un espacio donde la accountability se evapora ("lo hizo la IA") y la rendición de cuentas se vuelve materialmente imposible. Este fenómeno no es exclusivo de la IA; el movimiento ágil ya identificó tempranamente que la autoorganización sin claridad de roles produce ambigüedad organizativa, no autonomía productiva ([Schwaber & Sutherland, 2020](#ref-scrumguide2020)). La novedad radica en que los agentes intensifican esta dinámica: son actores con agencia sin subjetividad moral, capaces de ejecutar pero incapaces de responder.

A tenor de lo señalado, las herramientas clásicas de claridad organizacional (la matriz RACI y la matriz de Eisenhower) no solo siguen vigentes en el contexto agéntico: se vuelven más indispensables que nunca. Su valor no reside en la formalidad que imponen, sino en la claridad que producen: saber quién hace qué, quién responde por qué, y qué prioridades gobiernan las decisiones de delegación.

## RACI con agentes: la regla de la accountability indelegable

![Matriz RACI: Agente puede ser R o C, pero nunca A (Accountable siempre humano)](imagenes/uml/c42_raci_matrix_es.png)

La matriz RACI distingue cuatro roles fundamentales: Responsable (R, quien ejecuta), Aprobador (A, quien responde), Consultado (C, quien aporta conocimiento) e Informado (I, quien recibe el resultado). Al introducir agentes, conviene establecer una distinción tajante y no negociable: **un agente puede ser Responsable o Consultado, pero jamás Aprobador**. La A (accountability) es indelegable a una máquina, porque exige la capacidad de asumir consecuencias, y un agente no puede asumirlas en ningún marco legal, ético u organizacional vigente.

| Rol RACI     | ¿Puede asumirlo un agente? | Fundamento                                                |
|--------------|----------------------------|-----------------------------------------------------------|
| Responsable (R) | Sí                      | Ejecuta la tarea con competencia demostrable              |
| Aprobador (A)   | No                      | Asume consecuencias, siempre humano                      |
| Consultado (C)  | Sí                      | Aporta análisis especializado sin ser el decisor final    |
| Informado (I)   | Sí                      | Recibe el resultado como parte de la cadena de proceso    |

Esta regla simple gobierna la integración completa. Viola haberla en cualquier punto es crear un vacío de accountability que, tarde o temprano, un fallo del agente pondrá en evidencia de la peor manera posible: cuando ya ha causado daño y nadie puede ser señalado como responsable. El Reglamento de Inteligencia Artificial de la Unión Europea ([EU AI Act, 2024](#ref-aiact2024)) es explícito al respecto: los sistemas de IA de alto riesgo deben tener identificado un operador humano responsable.

## RACI a escala: cuando el Responsable es un enjambre

La regla anterior asume que el Responsable (R) es un actor identificable: una persona, o un agente único con un nombre y un dueño. Esa asunción se rompe cuando el "agente" que ejecuta la tarea es en realidad un orquestador que despachó entre 20 y 96 subagentes en paralelo (Vol. 4, capítulo 5, caso 7), el patrón que hoy documentan tanto Claude Code como GPT-6 Astra en producción real. Repartir la A entre 96 trabajadores no es una opción (ya se estableció que la A es indelegable), pero tampoco es razonable exigir que un humano apruebe individualmente cada una de las 96 salidas: eso anula el motivo por el que se paralelizó en primer lugar.

La resolución es declinar el Responsable en dos niveles, no en uno:

| Nivel | Quién | Rol RACI | Mecanismo de trazabilidad |
|---|---|---|---|
| R-orquestador | El agente gestor que descompone la tarea y agrega resultados (uno solo, siempre nombrado) | Responsable de la agregación final | Registro de dependencias del Vol. 4, capítulo 5, caso 8 |
| R-trabajador | Cada uno de los N subagentes despachados | Responsable de su subtarea individual | Traza heredada del R-orquestador; no requiere dueño humano propio |
| A (humano) | El dueño del agente registrado (capítulo 6, caso 6 del Vol. 4) | Aprueba la política de agregación y las acciones irreversibles que de ella resulten | Revisión por muestreo estadísticamente significativo, no exhaustiva |

El punto de control humano no se mueve al nivel del trabajador individual (eso sería insostenible a partir de la decena de agentes); se mueve a la **política de agregación** del orquestador: cómo combina 96 resultados parciales en una sola conclusión, y qué umbral de discrepancia entre trabajadores dispara una revisión humana antes de actuar. Esto es, en esencia, el mismo Agente Crítico del capítulo 3 de este volumen, generalizado de un desacuerdo entre dos agentes a un desacuerdo estadístico entre decenas.



La matriz de Eisenhower (clasificación de tareas por urgencia e importancia) adquiere una dimensión estratégica nueva cuando el executor potencial es un enjambre de agentes. El criterio de delegación se articula de la siguiente manera:

**Urgente + No importante → Delegar al enjambre.** Estas son las tareas que consumen tiempo sin exigir juicio profundo: triage de correos, generación de reportes rutinarios, actualización de documentación, monitoreo de alertas. El agente es más veloz, más consistente y menos costoso en este cuadrante.

**Importante + No urgente → Humano, con soporte agéntico.** La estrategia, la arquitectura de producto, las decisiones de contratación, la visión del roadmap: estas pertenecen al criterio humano. El agente puede investigar, sintetizar opciones y preparar el análisis; la decisión permanece humana.

**Urgente + Importante → Humano con asistencia agéntica en tiempo real.** Una crisis de producción, una negociación crítica, una decisión regulatoria bajo presión temporal: la urgencia no transfiere la responsabilidad al agente. El enjambre acelera el diagnóstico; el humano decide.

**No urgente + No importante → Candidatos a eliminación.** Si una tarea no tiene urgencia ni importancia, la pregunta correcta es si debe hacerse, no quién la hace (humano o agente).

El error frecuente es delegar al agente lo *importante* por el mero hecho de que también es *urgente*. Ahí se pierde el juicio que ningún modelo aporta, y la velocidad del agente se convierte en velocidad hacia el resultado equivocado.

## La paradoja de la agilidad: más claridad, no menos

Existe un malentendido tentador: dado que lo ágil valora la autoorganización, definir roles formales parecería contradecirlo. Esta intuición es incorrecta. La autoorganización funciona cuando los actores comparten un entendimiento implícito del propósito y los límites; los agentes no comparten ese entendimiento. De ahí que, paradójicamente, **un equipo con agentes necesite más claridad explícita de roles que uno puramente humano**, no menos. RACI y Eisenhower son, en este contexto, los andamios que permiten que la agilidad no degenere en ambigüedad.

Esta paradoja ha sido documentada en la literatura sobre equipos de trabajo en entornos de alta automatización: la introducción de sistemas autónomos requiere roles explicitados, no roles reducidos ([Grote, 2012](#ref-grote2012)). Los equipos que asumen que "la IA se organizará sola" reproducen en el plano agéntico el mismo error que los equipos que confunden autoorganización con ausencia de estructura.

---

## Perspectiva técnica avanzada

**► PISTA TÉCNICA**


### RACI como patrón de autorización en código

Desde la óptica del **Arquitecto Senior**, la matriz RACI no es solo un artefacto de gobernanza organizacional: puede y debe implementarse como un patrón de autorización en el código del enjambre. Cada acción que un agente intenta ejecutar debe pasar por un **RACIAuthorizationGate** que verifique si el agente tiene el rol adecuado para esa acción en ese contexto:

```python
from enum import Enum
from dataclasses import dataclass
from typing import Callable, Any

class RACIRole(Enum):
    RESPONSIBLE  = "R"   # Puede ejecutar
    ACCOUNTABLE  = "A"   # Jamás asignado a agentes
    CONSULTED    = "C"   # Puede proveer análisis, no ejecutar acción final
    INFORMED     = "I"   # Recibe notificación

@dataclass
class AgentPermission:
    agent_id:     str
    action_type:  str
    role:         RACIRole

    def can_execute(self) -> bool:
        """Solo R puede ejecutar directamente."""
        return self.role == RACIRole.RESPONSIBLE

    def can_consult(self) -> bool:
        return self.role in (RACIRole.RESPONSIBLE, RACIRole.CONSULTED)

class RACIAuthorizationError(PermissionError):
    pass


class RACIGate:
    """
    Verifica que el agente tenga el rol correcto antes de ejecutar.
    Si el rol es A, lanza error — la accountability es siempre humana.
    """
    def __init__(self, permissions: list[AgentPermission]):
        self._registry: dict[tuple, RACIRole] = {
            (p.agent_id, p.action_type): p.role
            for p in permissions
        }

    def authorize(self, agent_id: str, action_type: str, fn: Callable, *args: Any) -> Any:
        role = self._registry.get((agent_id, action_type))
        if role is None:
            raise RACIAuthorizationError(
                f"Agente '{agent_id}' sin rol definido para acción '{action_type}'"
            )
        if role == RACIRole.ACCOUNTABLE:
            raise RACIAuthorizationError(
                "Violación RACI: ningún agente puede tener rol Accountable. "
                "Asigne esta acción a un humano."
            )
        if not AgentPermission(agent_id, action_type, role).can_execute():
            raise RACIAuthorizationError(
                f"Agente '{agent_id}' tiene rol {role.value} para '{action_type}': "
                f"no autorizado para ejecución directa."
            )
        return fn(*args)
```

Esta implementación hace que la regla RACI sea ejecutada por el sistema, no solo por las personas, eliminando el riesgo de violaciones accidentales.

### Eisenhower como enrutador de prioridad de tareas en el enjambre

El **Ingeniero Senior** puede implementar la lógica de Eisenhower como un enrutador que asigna tareas entrantes al executor apropiado:

```python
from dataclasses import dataclass

@dataclass
class Task:
    id:          str
    description: str
    urgent:      bool
    important:   bool

def eisenhower_router(task: Task) -> str:
    """
    Retorna el executor recomendado:
      'swarm'          → agente autónomo
      'human+swarm'    → humano con soporte agéntico
      'human_led'      → humano lidera, agente asiste
      'eliminate'      → candidata a eliminación
    """
    if task.urgent and not task.important:
        return "swarm"
    elif task.important and not task.urgent:
        return "human+swarm"
    elif task.urgent and task.important:
        return "human_led"
    else:
        return "eliminate"
```

### Estrategia de QA: testing de límites de rol

El **QA Senior** diseña pruebas que verifican que los agentes no excedan sus roles asignados, especialmente que ningún agente ejecute acciones de Aprobador:

```python
import pytest

def test_agent_cannot_hold_accountable_role(raci_gate):
    with pytest.raises(RACIAuthorizationError, match="Accountable"):
        perm = AgentPermission("agent-x", "approve_deployment", RACIRole.ACCOUNTABLE)
        raci_gate.authorize("agent-x", "approve_deployment", lambda: None)

def test_agent_with_responsible_role_can_execute(raci_gate):
    result = raci_gate.authorize("agent-draft", "generate_document", lambda: "OK")
    assert result == "OK"

def test_task_routing_urgent_not_important():
    task = Task("t1", "Triage de alertas", urgent=True, important=False)
    assert eisenhower_router(task) == "swarm"
```

---

## Perspectiva ejecutiva

**■ PISTA EJECUTIVA**


### Visión del Product Owner: RACI en el backlog

El **Product Owner** incorpora la asignación RACI en las épicas del producto que involucran agentes. Para cada épica con componente agéntico, el backlog incluye una tarea explícita: *"Definir y validar matriz RACI para el enjambre de [nombre del dominio]."* Esta tarea se completa antes de que la primer historia de usuario del enjambre entre en sprint.

El riesgo de omitir este paso es concreto: cuando ocurra el primer fallo del agente (y ocurrirá), el equipo perderá tiempo valioso de sprint debatiendo quién debería haber revisado qué. La claridad previa convierte el fallo en aprendizaje; la ambigüedad lo convierte en conflicto.

**Indicador de salud del P.O.**: el porcentaje de historias de usuario con componente agéntico que tienen su RACI definido antes de entrar en sprint. El objetivo es 100%.

### Visión del Scrum Master: Eisenhower en la planificación del sprint

El **Scrum Master** facilita al inicio de cada sprint una revisión rápida (no más de 15 minutos) del backlog filtrado por Eisenhower. Para cada ítem agéntico del sprint, el equipo responde: *"¿Es este el cuadrante correcto? ¿Estamos asignando esto al executor adecuado?"*

Esta práctica previene uno de los antipatrones más comunes en equipos que adoptan IA: delegar al agente tareas importantes-urgentes por la presión del sprint, y descubrir en la revisión que el resultado no es aceptable porque exigía criterio humano. El coste de ese antipatrón, medido en retrabajo y confianza perdida, supera con creces el coste de los 15 minutos de revisión preventiva.

---

## Versión académica alternativa (mayor densidad formal)

> La aplicación de marcos de asignación de responsabilidades (como RACI) a sistemas socio-técnicos complejos está respaldada por la teoría de la organización de alta fiabilidad (*High Reliability Organization*, HRO), desarrollada por Weick y Sutcliffe (2007). Según este marco, las organizaciones que operan en entornos de alta consecuencia logran su fiabilidad no mediante la eliminación de la incertidumbre, sino mediante una clarificación extrema de los patrones de respuesta ante la misma. La introducción de agentes de IA en equipos ágiles constituye, en términos HRO, una fuente de incertidumbre sistémica nueva cuya gestión requiere precisamente la explicitación de los patrones de accountability que la autoorganización informal no puede proveer. La no delegación del rol Accountable a sistemas artificiales no es, por tanto, una restricción arbitraria, sino la aplicación coherente del principio HRO de conciencia situacional distribuida: alguien en el sistema debe tener la capacidad de reconocer cuándo el comportamiento del agente se ha desviado de lo esperado y de actuar en consecuencia; esa capacidad requiere subjetividad moral.

---

## Lo esencial del capítulo 15

- Con agentes, la responsabilidad tiende a difuminarse ("lo hizo la IA"); la claridad de roles se vuelve estructuralmente indispensable.
- Regla RACI cardinal: un agente puede ser Responsable o Consultado, pero jamás Aprobador; la accountability es indelegable a una máquina.
- Eisenhower guía qué delegar: urgente-no-importante al enjambre; importante al criterio humano, incluso bajo presión de urgencia.
- La violación del Eisenhower más frecuente en equipos ágiles: delegar lo importante por ser también urgente.
- La implementación de RACI como patrón de autorización en código convierte la regla organizacional en restricción ejecutada por el sistema.
- Un equipo con agentes necesita más claridad explícita de roles, no menos: la autoorganización presupone entendimiento compartido que los agentes no tienen.
- El Scrum Master facilita la revisión de Eisenhower al inicio del sprint para evitar el antipatrón de la delegación urgente-importante al enjambre.
- Cuando el Responsable es un enjambre de decenas de subagentes, la A humana se mueve de aprobar cada salida a aprobar la política de agregación del orquestador y el umbral que dispara revisión.
