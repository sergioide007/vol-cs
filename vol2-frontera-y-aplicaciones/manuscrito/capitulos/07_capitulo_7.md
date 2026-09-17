# Capítulo 7: Novedades de hace un año que aún pueden seguir expandiéndose, IA generativa y la nube

> *En la IA, una novedad de hace un año no está obsoleta: está, casi siempre, infrautilizada.*

## El mito de la obsolescencia acelerada

Existe una creencia extendida y, en última instancia, costosa: que en el dominio de la inteligencia artificial, lo que fue anunciado hace doce meses ha quedado superado y ya no merece atención. La realidad documentada es, sin embargo, considerablemente más matizada. El autor, al revisar novedades de IA generativa en plataformas de nube como Azure de hace un año, ilustra un principio que la literatura de adopción de tecnología conoce bien: la mayoría de las capacidades anunciadas **se anuncian mucho antes de ser explotadas**.

Rogers (2003), en su influyente análisis de la difusión de las innovaciones, identificó que el tiempo entre la adopción de los primeros usuarios (*innovators*) y la mayoría tardía (*late majority*) puede abarcar años, incluso décadas. En el caso de la IA generativa, esta curva se comprime, pero no desaparece. La brecha entre lo que una plataforma *puede* hacer y lo que las organizaciones *efectivamente* hacen con ella es sistemática, persistente y, para el observador estratégico, una oportunidad continua. Mirar atrás un año no es ejercicio de nostalgia: es descubrir potencial sin reclamar que los competidores tampoco han explotado todavía.

## Por qué las capacidades quedan infrautilizadas: tres causas entrelazadas

La persistencia de esta brecha requiere explicación. Tres causas se entrelazan de forma que cada una refuerza a las otras:

**Primera causa: la velocidad del anuncio supera la velocidad de la adopción.** Azure, Google Cloud y AWS publican actualizaciones con frecuencia semanal. El ritmo de integración organizacional es inherentemente más lento: requiere evaluación, prototipos, aprobaciones de seguridad, adaptación de procesos y formación de equipos. La distancia entre el anuncio y la integración real se mide no en semanas sino en trimestres.

**Segunda causa: falta el conocimiento arquitectónico para ensamblar las piezas.** Disponer de una capacidad no equivale a saber encajarla en un sistema existente. Azure AI Foundry, por ejemplo, ofrece capacidades de orquestación de agentes, fine-tuning, embeddings, guardrails y evaluación integrada. La organización que no tiene un arquitecto que entienda cómo estas piezas se relacionan entre sí y con su infraestructura existente las tendrá disponibles y sin usar, año tras año.

**Tercera causa: el cambio organizacional es el cuello de botella real.** Una capacidad técnica solo rinde cuando los procesos, roles e incentivos de la organización se adaptan a ella. Implementar un agente de síntesis de documentos no tiene valor si el proceso organizacional no incluye el paso de consultar al agente. La tecnología es la parte rápida; la organización, la parte lenta.

## El método del "reexamen deliberado": explotar lo maduro antes de adoptar lo nuevo

De esta diagnosis emerge una práctica valiosa que pocos cultivan con disciplina: el **reexamen deliberado** de novedades pasadas. La práctica consiste en revisar periódicamente (cada doce a dieciocho meses) el catálogo de capacidades que la organización tiene disponibles y pagadas, formulando la pregunta: *¿qué de esto, ya maduro y estabilizado, seguimos sin aprovechar?*

La distinción entre capacidad *disponible* y capacidad *explotada* es, en el ecosistema de la nube, una fuente constante de valor latente. Microsoft, en su Pulse of the Profession (2023), reporta que las organizaciones explotan, en promedio, menos del 40% de las capacidades de IA que han contratado. El 60% restante representa cómputo pagado pero no utilizado (en el mejor de los casos) o, más frecuentemente, oportunidades perdidas de mejora competitiva.

A esto se añade un argumento de madurez tecnológica: lo anunciado hace un año es más estable, mejor documentado y menos propenso a cambios incompatibles que lo anunciado la semana pasada. La organización que adopta lo *últimísimo* paga el costo de ser beta-tester involuntario de tecnología que aún no ha madurado. La que adopta lo *maduro* construye sobre fundamentos sólidos.

## Aplicación concreta al ecosistema agéntico de Azure

Esta lógica es especialmente potente en el dominio de los agentes. Capacidades como Azure AI Agent Service (que permite construir agentes con acceso a herramientas, memoria persistente y orquestación multiagente), disponibles desde principios de 2024, permanecen sin explotar en un porcentaje significativo de las organizaciones que ya pagan la suscripción. El PromptFlow de Azure AI Studio, con sus capacidades de evaluación y testing de flujos agénticos, es otro ejemplo: anunciado, disponible, y subutilizado de manera sistemática.

El arquitecto estratégico, antes de justificar presupuesto para el próximo lanzamiento de OpenAI o Anthropic, audita lo que ya posee. Con frecuencia descubre que el enjambre que necesita podía haberse construido hace seis meses con las piezas que ya estaban disponibles y pagadas, y que la brecha era de conocimiento arquitectónico y voluntad organizacional, no tecnológica.

---

## Perspectiva técnica avanzada

**► PISTA TÉCNICA**


### Auditoría de capacidades: el inventario de lo posible frente a lo usado

Desde la perspectiva del **Arquitecto Senior**, la auditoría de capacidades debe ser un proceso formal, con artefactos documentados y frecuencia establecida. El siguiente patrón implementa un inventario de capacidades de nube que compara el estado contratado con el estado utilizado:

```python
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

class AdoptionStage(Enum):
    ANNOUNCED     = "announced"     # Disponible del proveedor
    EVALUATED     = "evaluated"     # Probado en POC
    PILOTED       = "piloted"       # En producción piloto
    DEPLOYED      = "deployed"      # En producción plena
    RETIRED       = "retired"       # Obsoleto o reemplazado

class TechReadiness(Enum):
    ALPHA   = "alpha"    # <6 meses desde GA
    BETA    = "beta"     # 6-12 meses desde GA
    MATURE  = "mature"   # >12 meses desde GA — candidato al reexamen

@dataclass
class CloudCapability:
    id:              str
    name:            str
    provider:        str             # "azure", "aws", "gcp"
    announced_date:  datetime
    our_stage:       AdoptionStage
    monthly_cost_usd: float
    readiness:       TechReadiness

    @property
    def months_since_announcement(self) -> float:
        delta = datetime.utcnow() - self.announced_date
        return delta.days / 30.0

    @property
    def is_underused(self) -> bool:
        """
        Candidato al reexamen deliberado:
        disponible y pagado pero no desplegado,
        con más de 12 meses desde el anuncio.
        """
        return (
            self.readiness == TechReadiness.MATURE
            and self.our_stage in (AdoptionStage.ANNOUNCED, AdoptionStage.EVALUATED)
            and self.monthly_cost_usd > 0
        )


class CapabilityAuditAgent:
    """
    Agente que ejecuta el reexamen deliberado de capacidades de nube.
    Identifica potencial maduro sin reclamar y estima el valor perdido.
    """
    def __init__(self, capabilities: list[CloudCapability]):
        self._caps = capabilities

    def underused_report(self) -> dict:
        underused = [c for c in self._caps if c.is_underused]
        monthly_waste = sum(c.monthly_cost_usd for c in underused)
        return {
            "underused_count": len(underused),
            "monthly_cost_usd": round(monthly_waste, 2),
            "annual_opportunity_usd": round(monthly_waste * 12, 2),
            "items": [
                {
                    "name":    c.name,
                    "stage":   c.our_stage.value,
                    "months":  round(c.months_since_announcement, 1),
                    "cost_pm": c.monthly_cost_usd,
                }
                for c in underused
            ],
        }

    def reexamination_candidates(self) -> list[CloudCapability]:
        """Ordena por potencial de valor: más madura y más cara primero."""
        return sorted(
            [c for c in self._caps if c.is_underused],
            key=lambda c: (c.months_since_announcement, c.monthly_cost_usd),
            reverse=True,
        )
```

### Infrastructure-as-Code para la gestión de capacidades de Azure AI

El **Ingeniero Senior** implementa la gestión de capacidades de Azure AI como código, garantizando que el inventario de capacidades contratadas sea un artefacto versionado y auditable:

```python
# Ejemplo de configuración declarativa de capacidades Azure AI
# — compatible con Bicep/Terraform como metadatos de coste y adopción

AZURE_AI_CAPABILITIES = [
    CloudCapability(
        id="azure-ai-agent-service",
        name="Azure AI Agent Service",
        provider="azure",
        announced_date=datetime(2024, 1, 15),
        our_stage=AdoptionStage.EVALUATED,      # pagado, evaluado, sin desplegar
        monthly_cost_usd=450.0,
        readiness=TechReadiness.MATURE,
    ),
    CloudCapability(
        id="azure-promptflow",
        name="Azure PromptFlow (evaluación agéntica)",
        provider="azure",
        announced_date=datetime(2023, 11, 1),
        our_stage=AdoptionStage.ANNOUNCED,      # ni siquiera evaluado
        monthly_cost_usd=120.0,
        readiness=TechReadiness.MATURE,
    ),
    CloudCapability(
        id="azure-content-safety",
        name="Azure Content Safety (guardrails)",
        provider="azure",
        announced_date=datetime(2023, 8, 1),
        our_stage=AdoptionStage.DEPLOYED,       # en producción — bien aprovechado
        monthly_cost_usd=80.0,
        readiness=TechReadiness.MATURE,
    ),
]
```

### Estrategia de QA: testing del proceso de adopción

El **QA Senior** diseña pruebas que validan no solo la funcionalidad de las capacidades adoptadas, sino la coherencia del proceso de adopción: que las capacidades maduras en stage ANNOUNCED tengan un plan de evaluación y que ninguna capacidad esté marcada como DEPLOYED sin tener tests de integración asociados.

```python
def test_mature_undeployed_capabilities_have_eval_plan(audit: CapabilityAuditAgent) -> None:
    """Toda capacidad madura no desplegada debe tener un plan de evaluación."""
    candidates = audit.reexamination_candidates()
    for cap in candidates:
        assert cap.our_stage != AdoptionStage.ANNOUNCED, (
            f"Capacidad '{cap.name}' lleva {cap.months_since_announcement:.0f} meses "
            f"disponible y sigue en stage ANNOUNCED. Requiere plan de evaluación."
        )

def test_no_deployed_capability_without_integration_tests(caps: list) -> None:
    deployed = [c for c in caps if c.our_stage == AdoptionStage.DEPLOYED]
    for cap in deployed:
        # En un sistema real, verificaría la existencia de tests en el repositorio
        assert cap.id in CAPABILITIES_WITH_TESTS, \
            f"Capacidad desplegada '{cap.name}' carece de tests de integración."
```

---

## Perspectiva ejecutiva

**■ PISTA EJECUTIVA**


### Visión del Product Owner: el reexamen como acelerador del roadmap

El **Product Owner** enfrenta una presión constante: justificar la adopción de nuevas capacidades mientras gestiona el backlog de las ya contratadas. El reexamen deliberado ofrece una respuesta directa a esta tensión: antes de proponer una nueva partida presupuestaria para la última capacidad de IA, el P.O. debe presentar un análisis de las capacidades ya contratadas y subutilizadas.

El argumento es financieramente contundente: si la organización paga mensualmente por capacidades que no usa, el primer paso para generar valor es desplegar lo que ya tiene, no contratar más. Este enfoque también mejora la credibilidad del P.O. ante el CFO: demuestra que el equipo de producto gestiona el gasto de IA con disciplina, no solo persiguiendo la última novedad.

**Template de decisión de adopción para el P.O.**:

| Capacidad candidata         | ¿Ya la tenemos? | Stage actual    | Costo mensual | Acción recomendada         |
|-----------------------------|-----------------|-----------------|---------------|----------------------------|
| Azure AI Agent Service      | Sí              | Evaluado        | $450          | Desplegar antes de licitar |
| Nuevo modelo GPT-5o         | No              | -               | TBD           | Esperar a auditar primero  |
| Azure PromptFlow            | Sí              | Anunciado       | $120          | Evaluar este trimestre     |

### Visión del Scrum Master: la auditoría de capacidades como ítem de backlog trimestral

El **Scrum Master** institucionaliza la auditoría de capacidades como un ítem fijo del backlog al inicio de cada trimestre (no de cada sprint, para evitar que se convierta en ruido). La sesión de auditoría, de no más de 2 horas, produce una lista priorizada de capacidades maduras para reexamen, que alimenta el planning del siguiente trimestre.

El Scrum Master actúa aquí como guardián del principio: evita que el equipo caiga en el antipatrón del *novelty chasing* (la persecución perpetua de lo últimísimo) que es una forma de procrastinación tecnológica. La disciplina de explotar lo maduro antes de adoptar lo nuevo es, paradójicamente, la que produce innovación más sostenible: las capacidades están estables, los equipos las entienden, y el valor llega antes.

---

## Versión académica alternativa (mayor densidad formal)

> La brecha sistemática entre la disponibilidad de una capacidad tecnológica y su adopción efectiva ha sido estudiada extensamente en la literatura de sistemas de información. El modelo de Venkatesh et al. (2003), conocido como UTAUT (*Unified Theory of Acceptance and Use of Technology*), identifica cuatro determinantes principales de la adopción: expectativa de rendimiento, expectativa de esfuerzo, influencia social y condiciones facilitadoras. En el contexto de la IA generativa en la nube, el tercer y cuarto determinantes son los que mayor fricción generan: la influencia social opera a través de la presión hacia lo nuevo (*novelty bias*) en lugar de hacia lo maduro, y las condiciones facilitadoras (conocimiento arquitectónico, procesos adaptados, incentivos) son precisamente las que la velocidad de los anuncios no puede proveer. El reexamen deliberado propuesto en este capítulo puede entenderse, en el marco UTAUT, como una intervención sobre el cuarto determinante: la creación de condiciones facilitadoras para la explotación de capacidades cuya expectativa de rendimiento ya ha sido validada por el mercado, pero cuyas condiciones de adopción no han sido todavía construidas por la organización.

---

## Lo esencial del capítulo 7

- En la IA generativa en la nube, lo de hace un año no está obsoleto: está, en la mayoría de las organizaciones, infrautilizado y ya pagado.
- La brecha entre lo posible y lo usado nace de tres causas entrelazadas: velocidad de anuncio mayor que la de adopción, falta de conocimiento arquitectónico y lentitud del cambio organizacional.
- El reexamen deliberado (auditoría periódica de capacidades maduras disponibles) es la práctica que convierte la brecha en oportunidad.
- Azure AI Agent Service, PromptFlow y similares son ejemplos de capacidades maduras frecuentemente infrautilizadas en organizaciones que ya las pagan.
- El P.O. presenta la auditoría de capacidades antes de solicitar nuevas partidas presupuestarias; el Scrum Master la institucionaliza como ítem trimestral del backlog.
- Explotar lo maduro antes de adoptar lo nuevo produce innovación más sostenible: los fundamentos son sólidos y el valor llega antes.
