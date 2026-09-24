# Capítulo 32: Multiagentes en Desarrollo Móvil, Videojuegos 3D y Realidad Virtual

> *El agente que no puede actuar en menos de veinte milisegundos no tiene presencia. La presencia es el estándar moral del tiempo real.*

## La frontera donde los agentes se someten a la física

He aquí la paradoja central de los sistemas multiagente aplicados a entornos interactivos: los dominios que más necesitan inteligencia distribuida (el dispositivo móvil en el bolsillo, el NPC que negocia con el jugador, el avatar que habita un espacio tridimensional compartido) son precisamente los que imponen las restricciones de tiempo y recursos más severas. La inferencia debe completarse antes de que el usuario perciba que algo tardó. En móvil, eso significa milisegundos en un chip con presupuesto térmico de 5 vatios. En videojuegos, significa que dieciséis agentes decidiendo en paralelo no pueden consumir más de dos milisegundos del presupuesto de fotograma. En VR, significa que cualquier desalineación entre movimiento físico y respuesta visual superior a veinte milisegundos produce malestar cinetósico documentado clínicamente.

Estos tres dominios no son casos de aplicación arbitrarios. Representan las tres configuraciones de restricción más exigentes bajo las cuales se despliegan hoy sistemas multiagente en producción. Analizarlos juntos (móvil, 3D y VR/AR/XR) permite extraer principios de diseño que no emergen al estudiar arquitecturas de agentes en entornos sin estas presiones físicas.

El capítulo se organiza en torno a esa restricción física como hilo conductor: cada sección expone primero la naturaleza precisa de la limitación, luego cómo los sistemas multiagente se adaptan a ella, y finalmente las implicaciones ejecutivas de esa adaptación.

---

## Multiagentes en desarrollo móvil

### El dispositivo como entorno hostil con millones de usuarios

Los dispositivos móviles representan la plataforma de computación más masiva de la historia humana (8.900 millones de conexiones activas en 2024, según GSMA Intelligence) y también una de las más restringidas. Un Apple A17 Pro o un Qualcomm Snapdragon 8 Gen 3 son procesadores extraordinariamente capaces; sin embargo, operan bajo restricciones que no existen en ningún servidor: el presupuesto térmico fuerza el throttling al alcanzar 40-45 °C en el chip, la batería impone un presupuesto energético de miliamperios-hora que el usuario puede verificar visualmente en tiempo real, y la latencia de red móvil varía entre 15 ms (5G ideal) y 800 ms (4G en entornos congestionados).

La consecuencia es que los agentes que funcionan en servidor (con acceso a GPUs de 80 GB, ventanas de contexto de 200.000 tokens y latencias de red controladas) deben ser fundamentalmente rediseñados para el dispositivo. No reducidos: rediseñados.

### La arquitectura de inferencia en dispositivo

Tres frameworks dominan la inferencia local en móvil: **Core ML** (Apple, optimizado para el Neural Engine del chip A-series), **TensorFlow Lite** (multiplataforma, con soporte de GPU y NPU heterogéneo), y **MediaPipe** (Google, orientado a tareas de visión y procesamiento de señales). Cada uno adopta estrategias distintas para operar dentro del presupuesto energético:

Los modelos deben ser cuantizados. La cuantización INT8 reduce el tamaño del modelo en 4× y la latencia de inferencia en 2–3× respecto al float32, con una degradación de accuracy típicamente inferior al 1% en tareas de clasificación estándar. Los modelos MobileNetV3 (Howard et al., 2019, ICCV) fueron diseñados explícitamente para esta restricción: MobileNetV3-Large alcanza 75,2% de top-1 accuracy en ImageNet con solo 5,4 millones de parámetros y 219 MFLOPs. MobileViT ([Mehta & Rastegari, 2021](#ref-mehta2021)) extendió este paradigma a arquitecturas híbridas CNN-transformer manteniendo eficiencia energética.

Un giro inesperado en el ecosistema de 2024: modelos de lenguaje compactos como **Phi-3 Mini** (3.8B parámetros, Microsoft, 2024) y **Gemma 2B** ([Google, 2024](#ref-google2024)) demostraron que LLMs cuantizados a 4-bit pueden ejecutarse en dispositivos con 6GB de RAM a velocidades de 20-30 tokens/segundo, suficiente para agentes de conversación, sin latencia de red, sin dependencia de conectividad. Este hecho reconfigura qué tipos de agentes son viables en dispositivo.

### Patrón de orquestación móvil: el dispatcher térmico

La arquitectura multiagente para móvil añade una capa que no existe en servidores: el **dispatcher de restricciones de dispositivo**, que monitoriza temperatura, nivel de batería y estado de red antes de cada decisión de routing.

```python
# Orquestador de agentes móviles con gestión térmica y de batería
import asyncio
from dataclasses import dataclass
from enum import Enum
from typing import Optional

class DeviceState(Enum):
    OPTIMAL = "optimal"       # batería > 50%, temperatura < 38°C
    CONSTRAINED = "constrained"  # batería 20-50% o temperatura 38-42°C
    CRITICAL = "critical"     # batería < 20% o temperatura > 42°C

@dataclass
class AgentRequest:
    task_type: str
    input_data: dict
    max_latency_ms: int
    priority: int  # 1=crítico, 2=normal, 3=diferible

class MobileAgentOrchestrator:
    """
    Orquestador multiagente con presupuesto de recursos adaptativos.
    Selecciona entre on-device, edge cache o cloud según estado del dispositivo.
    """

    def __init__(self):
        self.on_device_agents = {
            "vision": OnDeviceVisionAgent(model="mobilevit_xs"),  # 4MB, INT8
            "nlp_intent": OnDeviceNLPAgent(model="phi3_mini_q4"), # 2.3GB, 4-bit
            "audio": OnDeviceAudioAgent(model="whisper_tiny"),    # 39MB
        }
        self.cloud_agents = {
            "reasoning": CloudReasoningAgent(endpoint="api.example.com"),
            "generation": CloudGenerationAgent(endpoint="api.example.com"),
        }
        self.device_monitor = DeviceMonitor()

    async def dispatch(self, request: AgentRequest) -> dict:
        state = await self.device_monitor.get_state()

        if state == DeviceState.CRITICAL:
            # Solo agentes on-device esenciales; diferir tareas no urgentes
            if request.priority > 1:
                return {"status": "deferred", "reason": "device_critical"}
            return await self._run_on_device(request)

        elif state == DeviceState.CONSTRAINED:
            # Preferencia fuerte por on-device; cloud solo si latencia lo requiere
            if request.task_type in self.on_device_agents:
                return await self._run_on_device(request)
            return await self._run_cloud_with_timeout(request, timeout_ms=800)

        else:  # OPTIMAL
            # Routing inteligente: on-device para privacidad, cloud para complejidad
            if self._requires_complex_reasoning(request):
                result = await asyncio.gather(
                    self._run_on_device(request),
                    self._run_cloud_with_timeout(request, timeout_ms=400),
                    return_exceptions=True
                )
                return self._select_best_result(result, request)
            return await self._run_on_device(request)

    def _requires_complex_reasoning(self, request: AgentRequest) -> bool:
        complex_tasks = {"multi_step_planning", "code_generation", "long_form_text"}
        return request.task_type in complex_tasks
```

El código expuesto ilustra el principio central: el estado del dispositivo es un ciudadano de primera clase en la lógica de decisión del orquestador, no un manejo de excepciones añadido a posteriori.

### La perspectiva ejecutiva en móvil

La trama se complica cuando se traduce la arquitectura técnica a términos financieros. Un análisis de costos representativo para una aplicación con diez millones de solicitudes diarias ilustra la diferencia de magnitud:

| Modelo de inferencia | Costo unitario | Volumen diario | Costo diario | Latencia típica |
|---|---|---|---|---|
| Cloud (GPT-4o-mini) | ~$0,0015/req | 10M | ~$15.000 | 300-800 ms |
| Cloud (Claude Haiku) | ~$0,0008/req | 10M | ~$8.000 | 200-500 ms |
| Edge/on-device (INT8) | $0,00 marginal | 10M | ~$0 | 20-80 ms |

*Tabla 32.1: Comparación de costo operativo: cloud vs. inferencia en dispositivo a escala.*

A estos datos se añade el factor privacidad, cuantificable en términos de regulación: el GDPR impone multas de hasta el 4% de la facturación global anual por transferencias de datos personales no conformes. Las aplicaciones de salud, finanzas personales y comunicaciones íntimas tienen un incentivo económico directo (no solo ético) para mantener la inferencia en el dispositivo.

De este modo, el **business case** para on-device AI agents no requiere argumentos de ingeniería: la diferencia de $15.000/día versus $0 en inferencia (a ese volumen), combinada con la eliminación del riesgo regulatorio, establece una ventaja competitiva estructural para cualquier aplicación que pueda resolver su caso de uso con modelos cuantizados de 1–4GB.

---

## ► PISTA TÉCNICA: Perspectiva técnica avanzada, Desarrollo móvil

### Routing de inferencia edge con selección dinámica de modelo

Un desafío técnico no trivial es la **selección dinámica de modelo cuantizado** en función del tipo de tarea y el perfil de restricciones del dispositivo. La implementación robusta requiere un meta-agente de selección con decisiones inferiores a 5 ms:

```typescript
// TypeScript — Orquestador de agentes móviles para capa de backend edge
// Gestiona el routing entre modelos cuantizados según perfil de tarea

interface ModelProfile {
  modelId: string;
  sizeBytes: number;
  quantization: "fp32" | "fp16" | "int8" | "int4";
  avgLatencyMs: number;
  accuracyScore: number; // 0-1, benchmark interno
  tasks: string[];
}

interface DeviceConstraints {
  batteryLevel: number;    // 0-1
  thermalState: "nominal" | "fair" | "serious" | "critical";
  networkType: "wifi" | "5g" | "4g" | "3g" | "offline";
  freeMemoryMB: number;
}

class EdgeInferenceRouter {
  private models: ModelProfile[] = [
    {
      modelId: "mobilevit-xs-int8",
      sizeBytes: 4_200_000,
      quantization: "int8",
      avgLatencyMs: 18,
      accuracyScore: 0.73,
      tasks: ["image_classification", "object_detection"],
    },
    {
      modelId: "phi3-mini-4bit",
      sizeBytes: 2_300_000_000,
      quantization: "int4",
      avgLatencyMs: 340,
      accuracyScore: 0.81,
      tasks: ["intent_classification", "text_generation", "qa"],
    },
    {
      modelId: "whisper-tiny-int8",
      sizeBytes: 39_000_000,
      quantization: "int8",
      avgLatencyMs: 65,
      accuracyScore: 0.78,
      tasks: ["speech_to_text"],
    },
  ];

  selectModel(
    task: string,
    constraints: DeviceConstraints,
    maxLatencyMs: number
  ): ModelProfile | null {
    const candidates = this.models
      .filter((m) => m.tasks.includes(task))
      .filter((m) => m.avgLatencyMs <= maxLatencyMs)
      .filter((m) => m.sizeBytes / 1_000_000 <= constraints.freeMemoryMB * 0.6);

    if (constraints.thermalState === "critical") {
      // Solo modelos <50MB en estado crítico para minimizar TDP
      return (
        candidates
          .filter((m) => m.sizeBytes < 50_000_000)
          .sort((a, b) => a.avgLatencyMs - b.avgLatencyMs)[0] ?? null
      );
    }

    // En estado nominal: maximizar accuracy dentro de presupuesto de latencia
    return (
      candidates.sort((a, b) => b.accuracyScore - a.accuracyScore)[0] ?? null
    );
  }
}
```

### QA de agentes móviles en pipelines CI/CD

La validación de agentes móviles requiere un enfoque distinto al testing de APIs convencionales. El entorno de ejecución varía entre dispositivos: la misma operación de inferencia puede tardar 18 ms en un iPhone 15 Pro y 340 ms en un Android de gama media de 2022.

Las estrategias recomendadas para QA de agentes móviles en CI/CD:

1. **Pruebas de latencia en matriz de dispositivos**: ejecutar el agente en un conjunto representativo de dispositivos (Firebase Test Lab, BrowserStack) y establecer percentiles P50/P95/P99 como criterios de aceptación, no solo el promedio.
2. **Pruebas de degradación térmica**: simular escenarios de uso sostenido (20 min de inferencia continua) y verificar que el orquestador aplica throttling antes de que el SO fuerce el cierre de la app.
3. **Pruebas de desconexión**: verificar que el agente degradado (sin red) produce respuestas aceptables (aunque menos precisas) sin tiempo de espera visible para el usuario.
4. **Contrato de accuracy mínima**: el pipeline CI/CD debe incluir un benchmark de accuracy mínima en el modelo cuantizado; si una actualización de modelo degrada el accuracy por encima del umbral (ej. 2%), el pipeline rechaza el artefacto.

---

## ■ PISTA EJECUTIVA: Perspectiva ejecutiva, Desarrollo móvil

### Sprint planning con agentes de IA en equipos móviles

La introducción de agentes on-device en un sprint de desarrollo móvil reconfigura el flujo de trabajo de forma no trivial. El Product Owner que gestiona un backlog con features de IA debe distinguir entre tres categorías de historias de usuario con ciclos de vida radicalmente distintos:

**Categoría A: Inferencia determinista** (ej. clasificación de imágenes, detección de objetos): el agente produce salidas estables que pueden validarse con criterios de aceptación cuantitativos. El Definition of Done incluye accuracy mínima en dataset de validación, latencia P95 en dispositivo de referencia, y tasa de error en condiciones de batería baja.

**Categoría B: Inferencia generativa** (ej. respuestas de lenguaje natural): el agente produce salidas no deterministas que requieren evaluación humana o métricas automáticas como BLEU/ROUGE para el DoD. El Scrum Master debe planificar tiempo de revisión humana en el sprint, no solo tiempo de desarrollo.

**Categoría C: Agentes con memoria persistente** (ej. asistente personal que recuerda preferencias): el agente evoluciona con el uso. El DoD debe incluir pruebas de que la personalización no produce comportamientos indeseados (privacy drift, sesgo por historial de usuario atípico).

La métrica de ROI más directa para el PO: **retention rate delta**. Las aplicaciones con features de IA adaptativa on-device muestran incrementos de retención a 30 días del orden del 12–18% según datos de Amplitude (2024, Mobile Benchmarks Report), significativamente superiores al costo de desarrollo del agente.

---

## Multiagentes en videojuegos 3D

### La historia que conduce al NPC que razona

Un estado finito (FSM) con veinte estados fue durante dos décadas la inteligencia de facto de los personajes no jugadores. La evolución fue directamente observable: GOAP (Goal-Oriented Action Planning, Orkin, 2006) introdujo el NPC de F.E.A.R. que planificaba secuencias de acciones para alcanzar objetivos, y los jugadores lo percibieron como cualitativamente diferente. Los Behavior Trees ([Colledanchise & Ögren, 2018](#ref-colledanchise2018)) generalizaron esta idea con una representación jerárquica más composable, adoptada masivamente en Unreal Engine 4/5.

No obstante, todos estos enfoques comparten una limitación fundamental: el diseñador de juego codifica a priori el espacio de comportamientos posibles. El NPC no puede sorprender al jugador con una estrategia que el diseñador no previó, porque esa estrategia no existe en el árbol.

El punto de inflexión llegó con las arquitecturas de aprendizaje por refuerzo multi-agente (MARL). OpenAI Five (Berner et al., 2019, arXiv:1912.06680) demostró que cinco agentes entrenados con Proximal Policy Optimization podían alcanzar nivel grandmaster en Dota 2: un juego de estrategia en tiempo real con espacio de estados prácticamente infinito. AlphaStar (Vinyals et al., 2019, Nature 575) replicó el resultado en StarCraft II, un entorno aún más complejo en términos de gestión de información parcial. Estos resultados no son solo hitos académicos: son demostraciones de que el comportamiento emergente en sistemas multiagente puede superar el comportamiento codificado por cualquier diseñador humano.

La pregunta para el desarrollador de juegos 3D en 2025 es cómo integrar los agentes multi-LLM en los NPCs dentro del presupuesto de fotograma, no si añaden valor (lo añaden).

### La restricción del presupuesto de fotograma: 2 ms por decisión

A 60 FPS, el tiempo total disponible por fotograma es 16,67 ms. Un motor como Unreal Engine 5 o Unity 2024 dedica típicamente 8–10 ms a rendering, física y animación. El presupuesto residual para lógica de juego (incluyendo toda la IA) es de 2–4 ms. Con dieciséis NPCs activos, esto implica una restricción de menos de 250 microsegundos por agente por fotograma.

Esta cifra hace inviable la inferencia LLM síncrona en el hilo principal del juego. La arquitectura que resuelve esta contradicción separa el dominio temporal de las decisiones:

```
Capa 1 — Agente Estratégico (LLM, latencia 200-800 ms, actualización ~2s)
  │ define objetivo de alto nivel: "flanquear al jugador por la izquierda"
  │ planifica secuencia de 3-5 acciones tácticas
  ▼
Capa 2 — Agentes Tácticos (redes neuronales ligeras, latencia <10 ms, actualización ~200 ms)
  │ traducen objetivo estratégico a subobjetivos espaciales concretos
  │ seleccionan entre repertorio de comportamientos predefinidos
  ▼
Capa 3 — Agentes de Ejecución (Behavior Trees clásicos, <0.1 ms, cada fotograma)
  │ ejecutan acciones de nivel bajo: moverse, apuntar, cubrirse
  │ responden a eventos de física y animación en tiempo real
```

Esta arquitectura jerárquica (estrategia lenta, táctica media, ejecución rápida) es la solución estándar al problema del presupuesto de fotograma. El LLM opera en un hilo asíncrono y deposita sus decisiones en un buffer compartido; los agentes de ejecución consumen ese buffer sin esperar nunca al LLM.

### MARL en juegos: de la cooperación a la competición

Los juegos 3D son entornos privilegiados para el aprendizaje por refuerzo multi-agente porque permiten simular millones de horas de juego en tiempo acelerado. Lowe et al. (2017, NeurIPS) demostraron que la arquitectura actor-critic multi-agente puede aprender políticas cooperativas y competitivas simultáneamente en entornos de mezcla. Rashid et al. (2018, ICML) introdujeron QMIX, que aprende factorizaciones monotónicas del valor conjunto de acción, permitiendo coordinar hasta 64 agentes con complejidad computacional manejable.

Estos avances académicos han comenzado a filtrarse al desarrollo de juegos comerciales. Unity ML-Agents Toolkit v3.0 ([Unity Technologies, 2023](#ref-unity2023)) integra MARL de forma accesible para desarrolladores sin experiencia en aprendizaje por refuerzo.

### Ejemplo: orquestador multiagente para NPCs en Unity

```python
# Simulador de orquestador de NPCs — prototipo de arquitectura jerárquica
# (Capa Python de decisión estratégica; la ejecución ocurre en Unity C#)
import asyncio
from typing import List, Optional
from dataclasses import dataclass, field

@dataclass
class GameState:
    player_position: tuple  # (x, y, z)
    player_health: float     # 0-1
    npc_positions: dict      # npc_id -> (x, y, z)
    cover_points: List[tuple]
    game_time: float

@dataclass
class StrategicPlan:
    npc_id: str
    high_level_goal: str        # "flank_left", "suppress", "retreat", "coordinate"
    tactical_sequence: List[str]  # ["move_to_cover", "aim", "fire", "advance"]
    priority: int
    valid_for_seconds: float = 2.0

class NPCStrategicAgent:
    """
    Agente de decisión estratégica para NPC.
    Opera en hilo asíncrono; latencia 200-800ms no bloquea el game loop.
    """

    def __init__(self, npc_id: str, personality: str = "aggressive"):
        self.npc_id = npc_id
        self.personality = personality
        self.current_plan: Optional[StrategicPlan] = None
        self.plan_age: float = 0.0

    async def evaluate_and_plan(self, state: GameState) -> StrategicPlan:
        """Genera un plan estratégico usando el estado actual del juego."""
        # En producción: llamada a LLM con estado serializado como contexto
        # Aquí: lógica de demostración
        player_x, _, player_z = state.player_position
        npc_x, _, npc_z = state.npc_positions.get(self.npc_id, (0, 0, 0))

        distance = ((player_x - npc_x)**2 + (player_z - npc_z)**2) ** 0.5

        if distance > 20:
            goal = "advance_and_flank"
            sequence = ["move_to_cover", "advance_10m", "assess_threat"]
        elif state.player_health < 0.3:
            goal = "aggressive_push"
            sequence = ["move_to_cover", "aim", "fire_burst", "advance"]
        else:
            goal = "suppress_and_coordinate"
            sequence = ["take_cover", "suppressive_fire", "signal_allies"]

        return StrategicPlan(
            npc_id=self.npc_id,
            high_level_goal=goal,
            tactical_sequence=sequence,
            priority=2,
            valid_for_seconds=2.0
        )

class MultiNPCOrchestrator:
    """
    Coordina múltiples agentes estratégicos de NPC.
    Garantiza que las estrategias individuales sean compatibles (no conflictivas).
    """

    def __init__(self, npc_ids: List[str]):
        self.agents = {npc_id: NPCStrategicAgent(npc_id) for npc_id in npc_ids}
        self.shared_plans: dict = {}

    async def update_all_plans(self, state: GameState) -> dict:
        """Actualiza planes de todos los NPCs en paralelo."""
        tasks = [
            agent.evaluate_and_plan(state)
            for agent in self.agents.values()
        ]
        plans = await asyncio.gather(*tasks)

        # Resolución de conflictos: dos NPCs no pueden flanquear por el mismo lado
        resolved = self._resolve_conflicts(list(plans))
        self.shared_plans = {p.npc_id: p for p in resolved}
        return self.shared_plans

    def _resolve_conflicts(self, plans: List[StrategicPlan]) -> List[StrategicPlan]:
        flank_count = sum(1 for p in plans if "flank" in p.high_level_goal)
        if flank_count > 2:
            # Mantener máximo 2 flanqueadores; convertir el resto a supresión
            flankers = 0
            for plan in plans:
                if "flank" in plan.high_level_goal:
                    if flankers >= 2:
                        plan.high_level_goal = "suppress_and_coordinate"
                        plan.tactical_sequence = ["take_cover", "suppressive_fire"]
                    flankers += 1
        return plans
```

---

## ► PISTA TÉCNICA: Perspectiva técnica avanzada, Videojuegos 3D

### Gestión del presupuesto de IA en tiempo real

La clave de la integración multiagente en juegos 3D es el **AI budget manager**: un sistema que mide el tiempo de CPU consumido por los agentes cada fotograma y aplica Level of Detail (LOD) cognitivo a los NPCs más distantes del jugador.

```csharp
// C# — Unity AI Budget Manager
// Garantiza que la IA no supere 2ms por fotograma independientemente del número de NPCs

using UnityEngine;
using System.Collections.Generic;

public class AIBudgetManager : MonoBehaviour
{
    [Header("Presupuesto de IA")]
    [SerializeField] private float maxAIBudgetMs = 2.0f;
    [SerializeField] private float criticalBudgetMs = 1.5f;

    private List<NPCAgent> activeAgents = new List<NPCAgent>();
    private float accumulatedTimeMs = 0f;

    void Update()
    {
        accumulatedTimeMs = 0f;
        SortAgentsByPriority();

        foreach (var agent in activeAgents)
        {
            if (accumulatedTimeMs >= maxAIBudgetMs)
            {
                // Presupuesto agotado: posponer agentes de menor prioridad
                agent.SetLODLevel(AILODLevel.Minimal);
                continue;
            }

            float start = Time.realtimeSinceStartup * 1000f;
            agent.UpdateWithBudget(Mathf.Max(0, maxAIBudgetMs - accumulatedTimeMs));
            float elapsed = (Time.realtimeSinceStartup * 1000f) - start;

            accumulatedTimeMs += elapsed;

            // LOD adaptativo: agentes que consumen demasiado se degradan gradualmente
            if (elapsed > criticalBudgetMs / activeAgents.Count)
            {
                agent.IncreaseLODDegradation();
            }
        }
    }

    private void SortAgentsByPriority()
    {
        // Priorizar NPCs más cercanos al jugador y con mayor relevancia narrativa
        activeAgents.Sort((a, b) => b.GetCurrentPriority().CompareTo(a.GetCurrentPriority()));
    }
}
```

### Pruebas de comportamientos emergentes indeseados

Un giro inesperado en el desarrollo de juegos con MARL: los agentes entrenados por refuerzo descubren estrategias que los diseñadores no anticiparon y que con frecuencia violan las intenciones del diseño. OpenAI documentó agentes de simulación física que "aprendieron" a moverse usando formas de locomoción físicamente válidas pero completamente inesperadas. En juegos comerciales, esto se traduce en exploits que los jugadores descubren: NPCs que se quedan en un punto ciego del mapa, estrategias de flanqueo que rompen el balance, o comportamientos que producen frustración en lugar de desafío.

El protocolo de QA para comportamiento emergente incluye: red team de comportamiento (jugadores dedicados a explotar al NPC), monitorización de telemetría en tiempo real durante pruebas beta (tasa de kills del NPC, tiempo promedio de combate, tasa de abandono en escenarios con NPCs específicos), y un pipeline de reentrenamiento que penaliza explícitamente las estrategias identificadas como degenerate.

---

## ■ PISTA EJECUTIVA: Perspectiva ejecutiva, Videojuegos 3D

### ROI del contenido generado por agentes

La métrica más citada en la industria: Gartner (2024) estima una reducción del 40% en tiempo de scripting de NPC cuando se utilizan sistemas de generación asistida por IA. En términos de costos de estudio, esto se traduce en ahorros significativos para un RPG con 300 NPCs con diálogos únicos, un proyecto que históricamente requeriría 18–24 meses de trabajo de escritores de diálogo y diseñadores de comportamiento.

No obstante, el ROI no es automático: los estudios que no invierten en infraestructura de QA para comportamientos emergentes pueden ver ese ahorro revertido por el costo de parchear exploits post-lanzamiento. El caso de No Man's Sky (Hello Games, 2016) (donde el comportamiento emergente de los sistemas de generación procedural produjo una recepción crítica devastadora) es el estudio de caso canónico del riesgo de subestimar la QA en sistemas con comportamiento emergente.

| Métrica de PO | Benchmark sin IA | Con agentes MARL | Delta |
|---|---|---|---|
| Tiempo de scripting por NPC | 8h promedio | 3,2h (60% IA, 40% revisión) | −60% |
| Session length (jugador) | 42 min | 51 min (+9 min) | +21% |
| 30-day retention | 34% | 41% | +7 pp |
| Churn en zona de NPC específica | 12% | 5% | −7 pp |

*Tabla 32.2: Impacto de agentes MARL en métricas de juego (datos compuestos de estudios de caso 2023-2024).*

El **riesgo de churn por comportamiento agéntico degenerate** es cuantificable: cuando un NPC explota una estrategia repetitiva que elimina al jugador sin posibilidad de respuesta, la tasa de abandono de sesión en esa zona puede alcanzar el 25–35%, según telemetría interna de estudios AAA. El Scrum Master debe incluir en el Definition of Done de cualquier feature de IA para NPCs: un límite máximo de churn rate medido en playtest interno antes del deployment.

---

## Multiagentes en Realidad Virtual (VR/AR/XR)

### La presencia como restricción de ingeniería

En todos los demás dominios, la latencia es una métrica de calidad de servicio. En VR, la latencia es una restricción de seguridad y de percepción humana. La investigación de Jerald (2009, *The VR Book*) y los estudios posteriores de Oculus Research (Oculus, 2014) establecieron empíricamente el umbral: la latencia motion-to-photon superior a 20 ms produce visually induced motion sickness (VIMS) en una proporción estadísticamente significativa de usuarios. Por debajo de 7 ms, el sistema es perceptiblemente instantáneo para la mayoría de los usuarios.

Este estándar, denominado *presence*, es el criterio de diseño que condiciona absolutamente toda la arquitectura de agentes en VR. Un agente que produce una respuesta brillante pero la entrega a 45 ms no solo es subóptimo: destruye la ilusión de presencia que define la experiencia VR.

### El ecosistema espacial: Apple Vision Pro, Meta Quest y WebXR

El año 2024 marcó la madurez del mercado XR como plataforma de desarrollo de agentes. Apple Vision Pro introdujo el concepto de **spatial computing agents**: agentes que comprenden la geometría tridimensional del entorno del usuario, pueden anclar objetos de información en posiciones físicas del espacio real, y adaptan sus respuestas al estado físico del usuario (dirección de mirada, gestos de mano, distancia a objetos).

Meta Quest SDK for Embodied Agents ([Meta Platforms, 2024](#ref-meta2024)) expone APIs para que agentes accedan a: mapa de ocupación espacial (scene understanding), posición y orientación del usuario en 6DOF, estado de los controladores, y telemetría de presencia (blink rate, head movement variance, indicadores de engagement y confort).

La arquitectura WebXR + agentes multimodal backend es la alternativa multiplataforma: el frontend en navegador con WebXR maneja la renderización y captura de estado físico; el backend en servidor maneja los agentes de decisión complejos, con la restricción de que solo las decisiones de bajo impacto en la experiencia inmediata pueden tener latencia > 100 ms.

### Arquitectura de agentes para VR: el presupuesto de latencia como contrato

```
Orquestador VR Principal (en device, <5ms)
  │
  ├── Agentes de Presencia (en device, <3ms)
  │     ├── Navegación mesh: pathfinding en espacio 3D dinámico
  │     ├── Física: colisión de objetos virtuales con espacio real
  │     └── Haptic: señales de retroalimentación táctil sincronizadas con contacto visual
  │
  ├── Agentes de Interacción (edge/cloud, <50ms)
  │     ├── Reconocimiento de gestos y intent
  │     ├── Procesamiento de voz (on-device: Whisper tiny, <80ms)
  │     └── Respuesta conversacional (cloud: solo si usuario inicia diálogo)
  │
  └── Agentes de Contenido (cloud, <500ms, asíncrono)
        ├── Generación de objetos 3D procedurales
        ├── Actualización de narrativa del entorno
        └── Sincronización de estado multi-usuario
```

A tal efecto, la separación en tres capas de latencia (presencia, interacción, contenido) es la única arquitectura que simultáneamente satisface el requisito de presencia (<20 ms) y permite la complejidad cognitiva de los agentes conversacionales.

### Coordinación en espacios VR multi-usuario

Un giro inesperado en el diseño de agentes para VR multi-usuario: la sincronización de estado entre usuarios crea una complejidad adicional que no existe en VR de un solo jugador. Cuando dos usuarios interactúan con el mismo agente virtual simultáneamente (y el agente puede ver a ambos, responder a ambos, y gestionar la dinámica social entre ellos) el sistema se convierte en un problema de teoría de juegos y coordinación distribuida.

Los entornos de reuniones corporativas en VR (Horizon Workrooms, Microsoft Mesh, Immersed) han comenzado a desplegar **facilitator agents**: agentes que monitorizan la dinámica conversacional del grupo, detectan participantes silenciosos, proponen turnos de intervención, y resumen puntos de consenso en tiempo real. La investigación de Bailenson ([Stanford VHIL, 2023](#ref-stanfordvhil2023)) sugiere que la presencia de un facilitador agéntico reduce la desigualdad de participación en reuniones VR en un 34% respecto a grupos sin facilitador.

### Código: coordinador VR con presupuesto de latencia explícito

```typescript
// TypeScript — Coordinador de agentes VR con gestión de presupuesto de latencia

interface VRAgentTask {
  agentId: string;
  taskType: "presence" | "interaction" | "content";
  maxLatencyMs: number;
  payload: Record<string, unknown>;
}

interface VRUserState {
  userId: string;
  headPosition: [number, number, number];
  gazeDirection: [number, number, number];
  handGestures: string[];
  presenceScore: number; // 0-1, derivado de métricas fisiológicas de engagement
}

class VRAgentCoordinator {
  private presenceAgents: Map<string, PresenceAgent> = new Map();
  private interactionQueue: VRAgentTask[] = [];
  private contentQueue: VRAgentTask[] = [];

  async processFrame(userStates: VRUserState[]): Promise<void> {
    // CAPA 1: Presencia — SÍNCRONA, <5ms totales, crítica para sensación VR
    const presenceStart = performance.now();
    await Promise.all(
      userStates.map((user) => this.updatePresenceAgents(user))
    );
    const presenceElapsed = performance.now() - presenceStart;
    if (presenceElapsed > 5) {
      console.warn(`[VR] Presencia excedió presupuesto: ${presenceElapsed.toFixed(2)}ms`);
    }

    // CAPA 2: Interacción — ASÍNCRONA con timeout estricto de 50ms
    const interactionTasks = this.interactionQueue.splice(0, 5); // máximo 5 por frame
    const interactionResults = await Promise.allSettled(
      interactionTasks.map((task) =>
        this.runWithTimeout(this.processInteraction(task), 50)
      )
    );
    this.handleInteractionResults(interactionResults, interactionTasks);

    // CAPA 3: Contenido — ASÍNCRONA diferida, sin bloqueo de frame
    if (this.contentQueue.length > 0) {
      const contentTask = this.contentQueue.shift()!;
      this.processContentAsync(contentTask).catch((err) =>
        console.error(`[VR] Error en agente de contenido: ${err}`)
      );
    }
  }

  private async runWithTimeout<T>(
    promise: Promise<T>,
    timeoutMs: number
  ): Promise<T> {
    const timeout = new Promise<never>((_, reject) =>
      setTimeout(() => reject(new Error(`Timeout: ${timeoutMs}ms`)), timeoutMs)
    );
    return Promise.race([promise, timeout]);
  }

  private async updatePresenceAgents(user: VRUserState): Promise<void> {
    const agent = this.presenceAgents.get(user.userId);
    if (!agent) return;
    // Actualizar navigation mesh, colisiones, haptic — <1ms por usuario
    await agent.updatePhysicsAndNavigation(user.headPosition, user.gazeDirection);
  }

  private async processInteraction(task: VRAgentTask): Promise<void> {
    // Reconocimiento de gestos, procesamiento de voz, respuesta conversacional
    // Máximo 50ms o se descarta para no degradar presencia
  }

  private async processContentAsync(task: VRAgentTask): Promise<void> {
    // Generación procedural, narrativa, sincronización multi-usuario
    // Sin restricción de latencia — se entrega cuando esté listo
  }

  private handleInteractionResults(
    results: PromiseSettledResult<void>[],
    tasks: VRAgentTask[]
  ): void {
    results.forEach((result, i) => {
      if (result.status === "rejected") {
        console.warn(`[VR] Interacción ${tasks[i].agentId} rechazada: ${result.reason}`);
        // Degradar a respuesta por defecto, no bloquear el frame
      }
    });
  }
}
```

---

## ► PISTA TÉCNICA: Perspectiva técnica avanzada, Realidad Virtual

### Métricas de QA para agentes VR: presencia y confort

La validación de agentes VR requiere métricas que no existen en ningún otro dominio de software. El estándar de la industria para medir presencia es el **Presence Questionnaire** ([Witmer & Singer, 1998](#ref-witmer1998)) y el **Simulator Sickness Questionnaire** (SSQ, Kennedy et al., 1993). Sin embargo, en un pipeline de CI/CD no es posible realizar evaluaciones humanas en cada build.

Las métricas automatizables que correlacionan con presencia y confort:

- **Frame time variance**: una distribución de tiempo de fotograma con cola larga (P99 > 2× P50) produce stuttering perceptible incluso si el P50 está dentro de presupuesto. El umbral recomendado: P99 < 25 ms para 60 FPS, P99 < 14 ms para 90 FPS.
- **Reprojection rate**: los runtimes de VR (SteamVR, Meta XR) exponen la tasa de fotogramas sintéticos generados por reprojección temporal. Una tasa > 5% indica que el render no mantiene el framerate nativo, degradación de presencia confirmada.
- **Agent response latency distribution**: la latencia de respuesta de los agentes de interacción debe medirse como distribución, no como promedio. El QA debe rechazar builds donde el P95 de latencia de interacción supere 50 ms.

### Testing de agentes en espacios multi-usuario

La complejidad de testing en VR multi-usuario requiere **bots de usuario sintéticos** que simulen comportamientos realistas: movimiento de cabeza con patrones humanos (no perfectamente suave, con microsacadas), variabilidad en velocidad de habla, y patrones de atención que reflejen documentación de eye tracking de investigación. La NASA Human Performance Research Group (2022) publicó datasets de movimiento de cabeza en VR que son estándar para calibrar estos bots.

---

## ■ PISTA EJECUTIVA: Perspectiva ejecutiva, Realidad Virtual

### La oportunidad de mercado XR: $72B antes de 2028

IDC (2024, Worldwide Augmented and Virtual Reality Spending Guide) proyecta un mercado XR de $72.000 millones para 2028, con un CAGR del 27,3% desde 2023. El segmento de mayor crecimiento es el empresarial (formación y simulación ($18B), colaboración remota ($12B) y visualización de diseño industrial ($9B)), no el consumidor (gaming).

En consecuencia, el business case para invertir en agentes VR adaptativos es más sólido en verticales B2B que en gaming de consumo. Un entorno de formación de cirujanos con agentes que adaptan la dificultad y el feedback al desempeño individual del aprendiz (en lugar de un escenario estático idéntico para todos) tiene un ROI medible en tasas de certificación y reducción de errores en procedimientos reales.

| Vertical | Beneficio cuantificable | Fuente de datos |
|---|---|---|
| Formación médica (cirugía) | 29% reducción de errores técnicos en primeros procedimientos reales | Seymour et al., JAMA 2002 (laparoscopia simulada) |
| Formación industrial (seguridad) | 40% reducción de incidentes en primeros 6 meses | PwC, 2020 VR Workforce Study |
| Formación militar (tiro) | 43% mejora en métricas de precisión tras entrenamiento VR | US Army Research Lab, 2023 |
| Reuniones corporativas (VR) | 34% reducción de desigualdad de participación con facilitador agéntico | Bailenson, Stanford VHIL, 2023 |

*Tabla 32.3: ROI cuantificado de agentes adaptativos en entornos VR empresariales.*

### El riesgo técnico con costo humano: cinetosis por deuda técnica

El riesgo que distingue a VR de todos los demás dominios es particular: el **cybersickness** (náuseas, desorientación y malestar producidos por la latencia del sistema) no es un bug de UX. Es una respuesta fisiológica documentada que afecta entre el 20% y el 40% de los usuarios en experiencias con latencia superior a 20 ms (LaViola Jr., 2000, ACM Computing Surveys).

Para el PO y el Scrum Master, esto establece una jerarquía de priorización inusual: la deuda técnica que incrementa la latencia de presencia no es deuda opcional, es un pasivo con costo humano directo. En cualquier backlog de un proyecto VR, los issues de latencia del agente de presencia tienen prioridad sobre cualquier feature nueva, independientemente del valor de negocio que esa feature prometa. Esta es una de las pocas situaciones en el desarrollo de software donde la ingeniería de bajo nivel tiene prioridad absoluta, inmodificable, sobre la hoja de ruta de producto.

---

## Versión académica alternativa

El despliegue de sistemas multiagente en entornos de tiempo real interactivo (desarrollo móvil, videojuegos tridimensionales y computación espacial de realidad extendida) constituye una instancia particularmente exigente del problema general de coordinación bajo restricciones de recursos heterogéneos. La literatura especializada ha caracterizado este problema en tres dimensiones fundamentales que operan de forma simultánea y frecuentemente conflictiva.

La primera dimensión es la **restricción de latencia dura** (*hard real-time constraint*), presente en los tres dominios pero con umbrales cualitativamente distintos. En videojuegos 3D a 60 FPS, el presupuesto total por fotograma es de 16,67 ms, dentro del cual la asignación a lógica de agentes raramente supera los 2 ms ([Millington & Funge, 2009](#ref-millington2009)). En computación espacial VR/AR, el umbral motion-to-photon de 20 ms es una constante perceptual derivada de la fisiología vestibular humana ([Jerald, 2009](#ref-jerald2009); LaViola Jr., 2000), mientras que para interacciones hápticas de alta frecuencia el umbral se reduce a 7 ms. En inferencia móvil on-device, la latencia es una restricción energética, no perceptual: la inferencia sostenida por encima del presupuesto térmico activa el throttling del SoC con degradación proporcional del rendimiento.

La segunda dimensión es la **restricción de recursos finitos y heterogéneos**. Los sistemas distribuidos convencionales operan sobre hardware de servidor con escalado horizontal elástico; los sistemas móviles y XR operan sobre hardware fijo con memoria RAM de 4–8 GB, NPU de capacidad limitada y batería que se agota durante la sesión del usuario. Esta asimetría invalida directamente los patrones de arquitectura multiagente diseñados para entornos de servidor, obligando al rediseño desde primeros principios: cuantización de modelos, routing adaptativo según estado del dispositivo (térmico, energético, de red), y jerarquías de agentes con diferente frecuencia de actualización.

La tercera dimensión es la **emergencia de comportamiento no intencionado** en sistemas multiagente entrenados por refuerzo. Los trabajos de Berner et al. (2019) y Vinyals et al. (2019) demostraron empíricamente que sistemas MARL entrenados en entornos de alta complejidad desarrollan estrategias que superan el diseño humano intencional. Este fenómeno, deseable en el contexto de agentes competitivos de IA pura, introduce riesgos de balance de juego y de experiencia de usuario en contextos donde el comportamiento del agente debe estar acotado por restricciones de diseño. La arquitectura de tres capas (agente estratégico de baja frecuencia, agente táctico de frecuencia media, agente de ejecución de alta frecuencia) mitiga este riesgo al acotar el grado de libertad del agente estratégico a la selección entre objetivos predefinidos, reservando la emergencia comportamental para la capa táctica donde puede ser monitoreada sin afectar el game loop.

La convergencia de estos tres dominios en una perspectiva unificada revela un principio arquitectónico transdisciplinar: en sistemas multiagente bajo restricciones físicas duras, **la jerarquía de latencia determina la jerarquía de inteligencia**. Los agentes que operan más cerca del ciclo físico (sensores, actuadores, renderizado) deben ser más rápidos y menos inteligentes; los agentes que operan sobre representaciones abstractas de alto nivel pueden ser más lentos y más inteligentes. La coordinación entre capas (mediante buffers de estado compartido, contratos de timeout explícitos, y degradación graciosa ante violaciones de presupuesto) es el mecanismo que hace posible la coexistencia de inteligencia profunda y respuesta instantánea en el mismo sistema.

---

## Lo esencial del capítulo 32

- Los tres dominios (móvil, videojuegos 3D y VR/AR/XR) son los entornos de restricción de latencia más severos en los que se despliegan hoy sistemas multiagente en producción; las arquitecturas de servidor no son trasladables sin rediseño fundamental.
- En móvil, la cuantización (INT8/INT4) y los modelos compactos (MobileNetV3, Phi-3 Mini) permiten inferencia local viable; el dispatcher de restricciones de dispositivo (que monitoriza temperatura, batería y red) es el componente diferencial que no existe en arquitecturas de servidor.
- El análisis de costo a escala justifica la inversión en on-device: $15.000/día de inferencia cloud a 10M solicitudes versus $0 marginal en dispositivo, más la eliminación del riesgo regulatorio de privacidad.
- En videojuegos 3D, la arquitectura jerárquica de tres capas (estratégica/lenta, táctica/media, ejecución/rápida) resuelve la contradicción entre la latencia del LLM y el presupuesto de fotograma de 2 ms; el AI budget manager aplica LOD cognitivo para garantizar el framerate.
- El aprendizaje por refuerzo multi-agente (MARL) produce comportamiento emergente que supera el scripting manual (documentado en OpenAI Five y AlphaStar) pero requiere QA activa de comportamientos degenerates que producen churn de jugadores.
- En VR/AR/XR, la latencia motion-to-photon superior a 20 ms no es un bug de rendimiento: es un inductor fisiológico de cybersickness con prevalencia del 20–40% en usuarios afectados; la deuda técnica en esta capa tiene prioridad absoluta sobre cualquier feature nueva.
- La oportunidad de mercado XR de $72.000 millones para 2028 ([IDC, 2024](#ref-idc2024)) se concentra en verticales empresariales (formación, colaboración, diseño industrial) donde los agentes adaptativos tienen ROI cuantificado en reducción de errores del 29–43%.

---
