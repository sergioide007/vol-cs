# Capítulo 9: El cierre de conexiones también aplica a los agentes y multiagentes de IA: una visión crítica

> *Lo que no se cierra, se acumula; y lo que se acumula, en alta concurrencia, te derriba.*

## Una regla que la IA no deroga, sino que amplifica

En el desarrollo de sistemas de alta concurrencia, una regla es sagrada y tiene décadas de validación empírica en incidentes de producción: toda conexión que se abre debe cerrarse. La fuga de conexiones (ese descuido aparentemente menor, ese error que en el entorno de desarrollo nunca se manifiesta) ha derribado sistemas enteros bajo carga. Kleppmann (2017), en su análisis de los sistemas de datos distribuidos, identifica la gestión inadecuada de recursos como una de las causas más frecuentes de fallos en producción bajo carga alta.

Lo que el autor reivindica en este capítulo es que **la era agéntica no deroga esta regla, sino que la amplifica en proporción al número de agentes en el enjambre**. Un enjambre de cien agentes que cada uno abre dos conexiones concurrentes a modelos, herramientas, bases de datos y APIs está gestionando potencialmente doscientas conexiones simultáneas. Si el protocolo de cierre no es disciplinado, el problema de fuga que en un servidor monolítico podía tolerarse horas se manifiesta en minutos bajo carga de producción.

No resulta ocioso señalar que este principio se aplica con igual fuerza a recursos de naturaleza diversa: conexiones de red TCP, sesiones HTTP, handles de archivos, locks de base de datos, canales gRPC, streams de eventos y (lo que es nuevo en el ecosistema agéntico) sesiones de modelo LLM, contextos de razonamiento y conexiones MCP.

## El nuevo rostro del problema: cuatro formas específicamente agénticas

Lo que en un servidor monolítico era una fuga de conexiones a la base de datos adopta, en un sistema multiagente, formas nuevas y más sutiles que requieren identificación específica:

**Sesiones de modelo sin liberar.** Cada llamada a un LLM vía API consume cuota de tokens, latencia de inicio de sesión y, en algunos proveedores, recursos de estado de conversación. Un agente que no gestiona explícitamente el ciclo de vida de sus sesiones (especialmente en arquitecturas de streaming de largo plazo) agota la cuota disponible antes de que la carga real lo justifique.

**Contextos que no se purgan.** La memoria de un agente, si nunca se limita o se cierra, crece hasta degradar el razonamiento por dilución de contexto relevante (cf. Liu et al., 2024, "Lost in the Middle"). El agente con un contexto de 200.000 tokens donde los primeros 180.000 son historia irrelevante no razona peor por falta de información, sino por exceso de ella.

**Herramientas con estado abierto.** Un agente que abre una conexión vía MCP (a una base de datos, a un servicio externo, a un sistema de archivos) y no la cierra al terminar su tarea deja recursos colgando en el otro extremo. A escala de enjambre, esto produce agotamiento de pools de conexión en los servicios conectados.

**Bucles que no terminan.** El equivalente agéntico de la conexión no cerrada: un agente que no decide cuándo ha terminado su tarea entra en un bucle de razonamiento infinito que consume tokens, tiempo y dinero sin converger a un resultado. Este problema es especialmente insidioso porque no produce un error explícito: el agente sigue "pensando" indefinidamente.

## La crítica central: la abundancia anestesia la disciplina

He aquí la visión crítica que este capítulo propone con franqueza. En la era de la nube escalable y de los modelos de pago por uso, la abundancia aparente de recursos **anestesia la disciplina de cierre**. Como "siempre hay más cómputo", como los tokens son baratos y como la nube escala automáticamente, la tentación es no preocuparse por cerrar, no purgar, no terminar. Esta laxitud es una deuda que la cuenta de la nube cobra puntualmente al final de cada mes, y que bajo el pico de carga se convierte en una deuda de disponibilidad: el sistema se derrumba precisamente cuando más se lo necesita.

La crítica del autor a las malas prácticas de cierre (documentadas en sus experiencias con sistemas de alta concurrencia) no ha perdido vigencia con la llegada de los agentes. La ha potenciado. El poder de los agentes no exime del rigor en la gestión de recursos; lo exige con más urgencia, porque la escala del problema se ha multiplicado.

## El cierre como principio de diseño del enjambre

De lo expuesto se deriva que el cierre debe ser un **principio de diseño explícito del enjambre**, no una preocupación tardía que se añade cuando el sistema ya está en producción y los problemas ya han ocurrido. Cada agente del sistema debe declarar, en su especificación:

- Qué recursos abre (conexiones, sesiones, contextos, locks)
- Cuándo los cierra (al completar la tarea, al recibir señal de interrupción, al superar el timeout)
- Qué sucede si falla a mitad de camino (garantías de cierre en el caso de excepción)

Los patrones de la ingeniería de software clásica (`try-with-resources` en Java, `async with` en Python, `using` en C#) existen precisamente para garantizar que estas garantías sean declarativas y no dependan de la disciplina del programador en cada punto de uso. Deben trasladarse, con su espíritu intacto, al diseño de agentes.

---

## Perspectiva técnica avanzada

**► PISTA TÉCNICA**


### Gestión explícita del ciclo de vida de recursos en agentes Python

Desde la perspectiva del **Arquitecto Senior**, todo agente que consume recursos externos debe implementar el protocolo de gestión de ciclo de vida de manera explícita y verificable. El patrón recomendado utiliza context managers y connection pools con límites estrictos:

```python
import asyncio
import time
from contextlib import asynccontextmanager
from dataclasses import dataclass, field
from typing import AsyncIterator, Optional
import httpx


@dataclass
class AgentResourceMetrics:
    """Métricas de gestión de recursos del agente para observabilidad."""
    connections_opened:  int   = 0
    connections_closed:  int   = 0
    connections_timeout: int   = 0
    sessions_leaked:     int   = 0

    @property
    def leak_rate(self) -> float:
        if self.connections_opened == 0:
            return 0.0
        return self.sessions_leaked / self.connections_opened


class AgentResourceManager:
    """
    Gestor explícito de ciclo de vida de recursos para agentes.
    Implementa el principio de diseño del cap. 48:
    cierra todo lo que abre, incluso en caso de error.
    """
    def __init__(
        self,
        llm_timeout_s:   float = 30.0,
        tool_timeout_s:  float = 10.0,
        max_connections: int   = 20,
    ):
        self._llm_timeout  = llm_timeout_s
        self._tool_timeout = tool_timeout_s
        self.metrics       = AgentResourceMetrics()
        self._http_client: Optional[httpx.AsyncClient] = None
        self._pool_limits  = httpx.Limits(
            max_connections=max_connections,
            max_keepalive_connections=max_connections // 2,
        )

    @asynccontextmanager
    async def llm_session(self) -> AsyncIterator[httpx.AsyncClient]:
        """
        Contexto para llamadas LLM: abre, usa, cierra garantizadamente.
        Timeout obligatorio — previene bucles sin fin.
        """
        client = httpx.AsyncClient(
            timeout=self._llm_timeout,
            limits=self._pool_limits,
        )
        self.metrics.connections_opened += 1
        try:
            yield client
            self.metrics.connections_closed += 1
        except asyncio.TimeoutError:
            self.metrics.connections_timeout += 1
            raise
        except Exception:
            self.metrics.sessions_leaked += 1
            raise
        finally:
            await client.aclose()   # garantía de cierre incluso en excepción

    @asynccontextmanager
    async def tool_connection(self, tool_url: str) -> AsyncIterator[httpx.AsyncClient]:
        """Conexión a herramienta vía MCP: timeout más estricto."""
        client = httpx.AsyncClient(timeout=self._tool_timeout)
        self.metrics.connections_opened += 1
        try:
            yield client
            self.metrics.connections_closed += 1
        finally:
            await client.aclose()


class BoundedContextAgent:
    """
    Agente con contexto acotado: previene la degradación por crecimiento ilimitado.
    Implementa el principio de purga de contexto del cap. 48.
    """
    def __init__(
        self,
        max_context_tokens: int = 8_000,
        resource_manager:   Optional[AgentResourceManager] = None,
    ):
        self._max_tokens      = max_context_tokens
        self._context:        list[dict] = []
        self._resource_mgr    = resource_manager or AgentResourceManager()
        self._token_count:    int = 0

    def _estimate_tokens(self, message: dict) -> int:
        # Aproximación conservadora: 4 chars ≈ 1 token
        return len(str(message)) // 4

    def add_to_context(self, message: dict) -> None:
        estimated = self._estimate_tokens(message)
        # Si añadir el mensaje supera el límite, purgar los más antiguos
        while self._token_count + estimated > self._max_tokens and self._context:
            removed         = self._context.pop(0)
            self._token_count -= self._estimate_tokens(removed)
        self._context.append(message)
        self._token_count += estimated

    async def call_llm(self, prompt: str, llm_api_url: str) -> str:
        """Llamada LLM con gestión explícita del ciclo de vida."""
        async with self._resource_mgr.llm_session() as client:
            response = await client.post(
                llm_api_url,
                json={"messages": self._context, "prompt": prompt},
            )
            response.raise_for_status()
            return response.json()["content"]
```

### Circuit Breaker para llamadas a modelos y herramientas

El **Ingeniero Senior** implementa el patrón Circuit Breaker para prevenir que un servicio externo degradado cascade el fallo al enjambre completo:

```python
from enum import Enum

class CircuitState(Enum):
    CLOSED   = "closed"    # Normal: permite llamadas
    OPEN     = "open"      # Roto: bloquea llamadas
    HALF_OPEN = "half_open" # Prueba: permite una llamada de prueba

class AgentCircuitBreaker:
    """
    Circuit Breaker para agentes: previene la cascada de fallos.
    Estado OPEN = la conexión está "abierta" (rota) para nuevas llamadas.
    Se cierra (CLOSED) cuando el servicio se recupera.
    """
    def __init__(
        self,
        failure_threshold: int   = 5,
        recovery_timeout_s: float = 30.0,
    ):
        self.state             = CircuitState.CLOSED
        self._failure_count    = 0
        self._threshold        = failure_threshold
        self._recovery_timeout = recovery_timeout_s
        self._last_failure_time: float = 0

    async def call(self, fn, *args, **kwargs):
        if self.state == CircuitState.OPEN:
            if time.time() - self._last_failure_time >= self._recovery_timeout:
                self.state = CircuitState.HALF_OPEN
            else:
                raise RuntimeError("Circuit OPEN: llamadas bloqueadas temporalmente")

        try:
            result = await fn(*args, **kwargs)
            self._on_success()
            return result
        except Exception as e:
            self._on_failure()
            raise

    def _on_success(self) -> None:
        self._failure_count = 0
        self.state          = CircuitState.CLOSED

    def _on_failure(self) -> None:
        self._failure_count   += 1
        self._last_failure_time = time.time()
        if self._failure_count >= self._threshold:
            self.state = CircuitState.OPEN
```

### Estrategia de QA: testing de gestión de recursos

El **QA Senior** diseña pruebas que verifican que los agentes cierran todos sus recursos incluso ante excepciones, y que el circuit breaker previene cascadas de fallos:

```python
import pytest

@pytest.mark.asyncio
async def test_agent_closes_connection_on_exception(resource_manager: AgentResourceManager) -> None:
    """El recurso debe cerrarse incluso cuando el LLM lanza excepción."""
    initial_opened = resource_manager.metrics.connections_opened
    with pytest.raises(Exception):
        async with resource_manager.llm_session() as client:
            raise ValueError("Simulated LLM failure")
    # Tras la excepción, la conexión debe estar cerrada (not leaked)
    assert resource_manager.metrics.sessions_leaked == 0
    assert resource_manager.metrics.connections_opened == initial_opened + 1

@pytest.mark.asyncio
async def test_circuit_breaker_opens_after_threshold(breaker: AgentCircuitBreaker) -> None:
    """Después de N fallos, el circuit breaker debe abrir."""
    async def failing_fn():
        raise ConnectionError("Service unavailable")

    for _ in range(breaker._threshold):
        with pytest.raises(ConnectionError):
            await breaker.call(failing_fn)

    assert breaker.state == CircuitState.OPEN

@pytest.mark.asyncio
async def test_bounded_context_does_not_exceed_token_limit(agent: BoundedContextAgent) -> None:
    """El contexto del agente no debe superar el límite de tokens."""
    for i in range(100):
        agent.add_to_context({"role": "user", "content": f"Mensaje {i}" * 50})
    assert agent._token_count <= agent._max_tokens
```

---

## Perspectiva ejecutiva

**■ PISTA EJECUTIVA**


### Visión del Product Owner: el costo del descuido en la factura de la nube

El **Product Owner** tiene un interlocutor inesperado en este debate: el CFO. Las fugas de conexión en enjambres de agentes no son solo un problema de disponibilidad, son un problema de costos. Un enjambre que mantiene sesiones LLM abiertas innecesariamente, que no purga contextos cuando podría, y que no tiene timeouts configurados puede multiplicar por dos o por tres la factura de la nube en un mes de pico de carga.

El P.O. debe incluir en los criterios de aceptación de cualquier historia de usuario que involucre agentes los siguientes controles:

- Todos los recursos tienen timeout configurado explícitamente.
- El circuit breaker está habilitado para cada conexión a servicio externo.
- El leak rate del `AgentResourceMetrics` es < 0.5% en el entorno de staging bajo carga simulada.
- El contexto del agente tiene límite de tokens definido y probado.

**Regla de oro del P.O.**: si el agente no tiene timeout, no sale a producción.

### Visión del Scrum Master: la deuda técnica de los recursos no cerrados

El **Scrum Master** facilita una conversación de deuda técnica específica: el inventario de agentes en producción que no tienen gestión explícita de ciclo de vida de recursos. Esta deuda es invisible hasta el primer incidente de producción bajo carga alta, y entonces es urgente y costosa. La práctica recomendada es incluir en cada sprint al menos una historia de usuario de salud del sistema: *"Como equipo, quiero que todos los agentes de producción tengan circuit breakers y timeouts configurados, para evitar cascadas de fallos bajo pico de carga."*

El Scrum Master actúa aquí como el recordatorio institucional de que la velocidad de entrega de features no puede construirse sobre fundamentos que se derrumban bajo carga. La metáfora es precisa: construir un enjambre sin gestión de recursos es como construir un edificio sin instalaciones de plomería revisadas; todo parece bien hasta que alguien abre todos los grifos a la vez.

---

## Versión académica alternativa (mayor densidad formal)

> La gestión de recursos en sistemas concurrentes distribuidos puede analizarse a través del modelo de referencia de los sistemas de alta disponibilidad, donde el comportamiento del sistema bajo carga es la métrica crítica de calidad. Kleppmann (2017) establece que la fiabilidad de un sistema distribuido se degrada de manera no lineal cuando los recursos son gestionados de forma laxa: la fuga de conexiones no produce un fallo lineal proporcional al número de conexiones perdidas, sino un colapso súbito cuando el pool de conexiones disponibles alcanza cero. En el contexto de los enjambres multiagente, esta no-linealidad se amplifica por tres factores: (i) el número de agentes concurrentes es mayor que el de threads en un servidor tradicional; (ii) cada agente puede mantener múltiples conexiones simultáneas a diferentes servicios; y (iii) la duración de las sesiones LLM es impredecible en ausencia de timeout explícito. El circuit breaker pattern, formalizado por Nygard (2007) en *Release It!*, constituye la respuesta arquitectónica estándar a este riesgo: permite que el sistema falle rápido y de manera controlada en lugar de degradarse lentamente hasta el colapso total.

---

## Lo esencial del capítulo 9

- La regla "cierra lo que abres" no se deroga con la IA agéntica: se amplifica en proporción al número de agentes en el enjambre.
- El problema adopta cuatro formas específicamente agénticas: sesiones de modelo sin liberar, contextos que no se purgan, herramientas con estado abierto y bucles sin fin.
- La abundancia de cómputo en la nube anestesia la disciplina de cierre; la deuda se cobra bajo el pico de carga con fallos de disponibilidad y facturas inesperadas.
- El cierre debe ser un principio de diseño explícito: context managers, connection pools con límites, timeouts obligatorios y circuit breakers.
- El P.O. incorpora gestión de recursos como criterio de aceptación; si el agente no tiene timeout, no sale a producción.
- El Scrum Master facilita el inventario de deuda técnica de recursos no gestionados como parte regular del backlog.
