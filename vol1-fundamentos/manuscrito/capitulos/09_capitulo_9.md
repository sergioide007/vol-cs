# Capítulo 9: MCP: el protocolo que une el mundo agéntico

## El USB-C de la inteligencia artificial

El **Model Context Protocol** (MCP) es el estándar abierto, publicado por Anthropic a finales de 2024, que define cómo los agentes de IA se conectan con el mundo exterior: bases de datos, APIs, sistemas de archivos, servicios internos [Anthropic, 2024b](#ref-anthropic2024). Es, en esencia, el contrato de integración de la era agéntica, y su adopción desbordó rápidamente a su creador: durante 2025, los principales proveedores y herramientas del ecosistema anunciaron soporte para el protocolo, convirtiéndolo en el candidato más sólido a estándar de facto.

El problema que resuelve es el clásico M×N: antes de MCP, conectar M aplicaciones de IA con N sistemas externos exigía M×N integraciones a medida, con formatos propietarios incompatibles. MCP lo reduce a M+N: cada aplicación implementa el protocolo una vez (como *cliente*) y cada sistema lo implementa una vez (como *servidor*). Es la misma economía que estandarizó los puertos físicos (de ahí el apodo de «USB-C de la IA») y, antes, la que hizo de HTTP el idioma de la web.

Técnicamente, MCP es un protocolo basado en JSON-RPC 2.0 que expone tres primitivas:

- **Tools** (herramientas): funciones que el agente puede invocar: consultar una base de datos, crear un ticket, ejecutar una búsqueda.
- **Resources** (recursos): contenido que el agente puede leer: archivos, registros, documentación.
- **Prompts** (plantillas): instrucciones parametrizables que el servidor ofrece al cliente.

> **Justificación de diseño: diagrama de componentes para arquitectura del sistema**
>
> MCP es ante todo un *ecosistema modular*: múltiples clientes (aplicaciones de IA) que se conectan con múltiples servidores (sistemas externos) a través de un protocolo estándar. Un diagrama de componentes revela exactamente eso: las cajas (aplicación, servidor MCP), los puertos (Tools, Resources, Prompts), las conexiones desacopladas.
>
> Un diagrama de clases mostraría la estructura interna de un cliente o servidor; un diagrama de secuencias mostraría un flujo específico de interacción. Aquí necesitamos ver *la arquitectura modular del ecosistema*, cómo se conectan los piezas sin conocer detalles de la otra.
>
> El diagrama de componentes reaparece en este libro en el **Capítulo 8** (topologías multi-agente), donde nuevamente usamos componentes para mostrar cómo se conectan múltiples módulos especializados.

![Diagrama 9.1: Ecosistema MCP (diagrama de componentes)](imagenes/capitulo09/diagrama9_1_es.png)

**► PISTA TÉCNICA: Construyendo un MCP server de producción**

```python
# mcp_server_empresa.py
# MCP Server que expone herramientas del sistema interno al agente.
# Requiere: pip install mcp

import asyncio
import json

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

server = Server("sistema-empresa-v1")

# Definición de herramientas: la descripción ES el prompt del agente
@server.list_tools()
async def list_tools():
    return [
        Tool(
            name="consultar_estado_ticket",
            description="""Consulta el estado de un ticket en el sistema de gestión de proyectos.
            USAR cuando el usuario pregunta sobre el estado de una tarea, issue, o ticket.
            Retorna: estado actual, asignado, última actualización, y bloqueos si existen.""",
            inputSchema={
                "type": "object",
                "properties": {
                    "ticket_id": {
                        "type": "string",
                        "description": "ID del ticket (formato: PROJ-123)",
                    }
                },
                "required": ["ticket_id"],
            },
        ),
        Tool(
            name="ejecutar_query_db",
            description="""Ejecuta una query de SOLO LECTURA en la base de datos.
            SOLO permite SELECT. Rechaza automáticamente INSERT, UPDATE, DELETE, DROP.
            USAR para: verificar datos, auditar estado, depurar problemas de producción.
            NO USAR para: modificar datos (usar la API REST para eso).""",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Query SQL de solo lectura (SELECT)",
                    },
                    "database": {
                        "type": "string",
                        "enum": ["produccion", "staging", "analytics"],
                        "description": "Ambiente de base de datos",
                    },
                },
                "required": ["query", "database"],
            },
        ),
        Tool(
            name="obtener_metricas_sistema",
            description="""Obtiene métricas de performance del sistema en tiempo real.
            Incluye: latencia de endpoints, tasa de errores, uso de CPU/memoria,
            y alertas activas. USAR para diagnóstico de incidentes o revisiones de salud.""",
            inputSchema={
                "type": "object",
                "properties": {
                    "servicio": {
                        "type": "string",
                        "description": "Nombre del servicio (ej: 'api-gateway')",
                    },
                    "ventana_minutos": {
                        "type": "integer",
                        "description": "Ventana de tiempo en minutos (default: 15)",
                        "default": 15,
                    },
                },
                "required": ["servicio"],
            },
        ),
    ]

@server.call_tool()
async def call_tool(name: str, arguments: dict):

    if name == "consultar_estado_ticket":
        ticket_id = arguments["ticket_id"]
        # Integración real con Jira/Linear/etc.
        ticket_data = await ticket_service.get(ticket_id)
        return [TextContent(
            type="text",
            text=json.dumps({
                "id": ticket_id,
                "estado": ticket_data.status,
                "asignado": ticket_data.assignee,
                "ultima_actualizacion": ticket_data.updated_at.isoformat(),
                "bloqueadores": ticket_data.blockers or [],
            }, indent=2, ensure_ascii=False),
        )]

    elif name == "ejecutar_query_db":
        query = arguments["query"].strip()

        # Guardarraíl de seguridad: solo SELECT, y validado en el SERVIDOR.
        # Nunca confíe en que el modelo respetará la descripción de la
        # herramienta: la descripción guía, el servidor impone.
        if not query.upper().startswith("SELECT") or ";" in query.rstrip(";"):
            return [TextContent(
                type="text",
                text="ERROR: Solo se permite una única query SELECT. "
                     "Para modificar datos, usa la API REST del sistema.",
            )]

        database = arguments["database"]
        # Defensa adicional: usuario de BD de solo lectura + timeout
        results = await db_service.execute_readonly(query, database)
        return [TextContent(type="text",
                            text=json.dumps(results, indent=2, default=str))]

    elif name == "obtener_metricas_sistema":
        servicio = arguments["servicio"]
        ventana = arguments.get("ventana_minutos", 15)
        metricas = await metrics_service.get(servicio, ventana)
        return [TextContent(type="text", text=json.dumps(metricas, indent=2))]

async def main():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream,
                         server.create_initialization_options())

if __name__ == "__main__":
    asyncio.run(main())
```

**Registro del MCP server en Claude Code:**

```json
// .mcp.json (configuración del proyecto)
{
  "mcpServers": {
    "sistema-empresa": {
      "command": "python",
      "args": ["mcp_server_empresa.py"],
      "env": {
        "DB_CONNECTION_STRING": "${DB_CONNECTION_STRING}",
        "TICKET_API_KEY": "${TICKET_API_KEY}"
      }
    }
  }
}
```

### La seguridad de MCP es la seguridad de su organización

Un servidor MCP es, por definición, un puente entre un modelo probabilístico y sus sistemas reales. Cuatro reglas no negociables, que anticipan el capítulo 4 (Vol. 4):

1. **El servidor impone, la descripción sugiere.** Toda validación (solo lectura, límites, permisos) vive en el código del servidor. La descripción de la herramienta es un prompt, y los prompts se pueden manipular [Greshake et al., 2023](#ref-greshake2023).
2. **Mínimo privilegio por construcción.** La herramienta de consulta usa un usuario de base de datos de solo lectura; la credencial con permisos de escritura ni siquiera existe en ese proceso.
3. **Los resultados de las herramientas son entrada no confiable.** Lo que vuelve de un sistema externo (una página web, un ticket escrito por un tercero) puede contener instrucciones inyectadas dirigidas al modelo. El capítulo 4 (Vol. 4) desarrolla el ataque y las defensas.
4. **Servidores de terceros se auditan como dependencias.** Instalar un MCP server es conceder a su agente las capacidades de ese servidor; la cadena de suministro de servidores MCP merece el mismo escrutinio que la de paquetes de software.

**■ PISTA EJECUTIVA**

Para la dirección de tecnología, MCP convierte una pregunta recurrente («¿integramos la IA con el sistema X?») en una decisión de catálogo: ¿existe ya un servidor MCP para X, lo construimos, o esperamos? La recomendación estratégica es tratar los servidores MCP como **productos de plataforma** (capítulo 3): un catálogo interno, con propietarios, niveles de servicio y revisión de seguridad, del que todos los equipos consumen. La alternativa (cada equipo improvisando sus integraciones) reconstruye exactamente el problema M×N que el protocolo vino a eliminar.

## Herramientas MCP limpias

Las cuatro reglas de seguridad anteriores tienen su contraparte de diseño en el Código Limpio Sintético (capítulo 4), porque un servidor MCP es, ante todo, una **interfaz pública**: y las interfaces públicas se diseñan para sus consumidores, que aquí son dos: el modelo (que lee las descripciones) y el ingeniero (que mantiene el servidor):

- **Nombres que se autoinvocan.** `consultar_estado_ticket` se elige correctamente entre veinte herramientas; `query_v2` exige que el modelo adivine. En catálogos grandes, la calidad de los nombres es la diferencia entre un agente preciso y uno errático.
- **Una herramienta, una acción.** La tentación de un `ejecutar_operacion(tipo, parametros)` genérico viola SRP y, peor, destruye la capacidad del arnés de aplicar permisos por acción: no se puede dar «solo lectura» a una herramienta que hace de todo.
- **Errores para el modelo, no para el log.** «ERROR: Solo se permite una única query SELECT. Para modificar datos, usa la API REST», el mensaje del ejemplo, enseña al modelo el camino correcto en la misma respuesta. Un `400 Bad Request` lo deja reintentando a ciegas, quemando presupuesto.
- **El esquema es el contrato.** Tipos estrictos, `enum` donde el dominio es cerrado, `required` mínimo: cada grado de libertad innecesario en el esquema es una forma nueva de invocación incorrecta que tendrá que depurar.

## Ejercicio resuelto 9.1: añada la cuarta herramienta

**Enunciado.** Añada al servidor del ejemplo una herramienta `crear_ticket` que permita al agente abrir tickets de incidencia. Diseñe sus guardarraíles: ¿qué puede salir mal y cómo lo impide el servidor?

**Solución comentada.** La definición sigue la plantilla de las anteriores; lo interesante son los guardarraíles, porque esta es la primera herramienta **de escritura** del servidor:

```python
Tool(
    name="crear_ticket",
    description="""Crea un ticket de incidencia en el sistema de gestión.
    USAR cuando el usuario reporte un problema reproducible y pida registrarlo.
    NO USAR para: consultas (usar consultar_estado_ticket), ni para crear
    más de un ticket por incidencia.""",
    inputSchema={
        "type": "object",
        "properties": {
            "titulo": {"type": "string", "maxLength": 120},
            "descripcion": {"type": "string", "maxLength": 4000},
            "severidad": {"type": "string",
                          "enum": ["low", "medium", "high"]},
        },
        "required": ["titulo", "descripcion", "severidad"],
    },
)
```

Y en el manejador, las defensas que el esquema no puede expresar: (1) **idempotencia**: un hash de `titulo+descripcion` con ventana de 10 minutos rechaza duplicados, porque un agente en bucle de reintentos puede crear cincuenta tickets idénticos (el Token-Burn tiene primos); (2) **límite de tasa por sesión**: N tickets por hora por agente, presupuesto como control de seguridad (capítulo 4 (Vol. 4)); (3) **severidad `critical` excluida del enum**: escalar a crítico exige un humano: es la política de acciones de alto impacto del capítulo 1 (Vol. 3) aplicada en el lugar correcto, el servidor; (4) **autoría trazada**: el ticket registra que lo creó un agente, con el id de sesión: auditoría total. Obsérvese que ninguna de las cuatro defensas vive en el prompt: la descripción *sugiere* el buen uso; el servidor lo *impone*.

## El protocolo de admisión al catálogo

La pregunta de discusión con la que suele cerrarse esta conversación (¿con qué criterios entra un servidor MCP al catálogo?) no debería quedar abierta en una organización que ya opera en producción. Este libro propone un protocolo de puntuación, verificable en una revisión de una hora, que unifica las reglas de seguridad y de diseño ya vistas en este capítulo con el registro de dependencias y el presupuesto de degradación del Vol. 4 (capítulo 5, caso 8):

| Criterio | 0 puntos | 1 punto | 2 puntos |
|---|---|---|---|
| Mantenimiento | Sin dueño identificable | Mantenedor individual | Organización o proveedor con incentivo de largo plazo (capítulo 2) |
| Seguridad del esquema | Sin guardarraíles en el servidor | Guardarraíles parciales | Las cuatro defensas de este capítulo: idempotencia, límite de tasa, exclusión de acciones críticas del enum, autoría trazada |
| Versionado del contrato | Sin versión declarada | Versión sin política de deprecación | Semver explícito + ventana de deprecación documentada + contrato dirigido por el consumidor (Vol. 4, caso 8) |
| Trazabilidad | Sin registro | Log propio no estandarizado | Traza compatible con el esquema OpenTelemetry (Vol. 4, capítulo 11) |
| Plan de degradación | Sin plan | Solo falla dura | Modo degradado documentado y probado en stage (Vol. 4, caso 8) |

**Umbrales de decisión:** 7 a 10 puntos admite el servidor sin reservas; 4 a 6 lo admite únicamente en modo *shadow* de solo lectura en QA (la misma tabla de entornos del Vol. 4, caso 8) hasta elevar el puntaje; menos de 4 no se admite al catálogo, sin excepción de urgencia, la excepción de urgencia es, precisamente, cómo se acumula la deuda de gobernanza que el capítulo 1 (Vol. 4) (Vol. 3) mide en dólares.

**Versionado del contrato, en concreto.** Un esquema de versionado semántico específico para herramientas MCP evita la ambigüedad de «actualizamos el servidor» sin más contexto: **MAJOR** cuando se elimina una herramienta o se rompe su `inputSchema` (exige mínimo 90 días con ambas versiones activas en paralelo); **MINOR** cuando se añade una herramienta o un campo opcional (retrocompatible, sin ventana obligatoria); **PATCH** cuando solo cambia la redacción de una descripción para mejorar la invocación del modelo (capítulo 2, prompt de la herramienta). El equipo consumidor, no el equipo dueño del servidor, decide cuándo migrar de una versión MAJOR a la siguiente, el mismo principio de autonomía del consumidor que sostienen los contratos dirigidos por el consumidor.

Un catálogo que aplica este protocolo de forma consistente convierte «¿integramos la IA con el sistema X?» en un número reproducible, no en una negociación distinta cada vez que un equipo lo pregunta.



- MCP reduce la integración de M×N a M+N: cada aplicación y cada sistema implementan el protocolo una vez [Anthropic, 2024b](#ref-anthropic2024).
- Tres primitivas: tools (acciones), resources (lecturas), prompts (plantillas), sobre JSON-RPC 2.0.
- El servidor impone, la descripción sugiere; los resultados de herramientas son entrada no confiable [Greshake et al., 2023](#ref-greshake2023).
- Herramientas limpias: nombres autoinvocables, una acción por herramienta, errores que enseñan, esquemas estrictos.
- Los servidores MCP se gestionan como productos de plataforma: catálogo, dueños, revisión de seguridad.
- El protocolo de admisión al catálogo puntúa mantenimiento, seguridad del esquema, versionado, trazabilidad y plan de degradación (0-10); por debajo de 4 no se admite, sin excepción de urgencia.

## Preguntas para discusión

1. De los diez sistemas internos más consultados por sus equipos (tickets, métricas, documentación, CRM…), ¿cuántos son hoy accesibles para un agente de forma gobernada?
2. ¿Quién aprueba, en su organización, que un nuevo servidor MCP entre al catálogo? El protocolo de admisión de este capítulo da una respuesta reproducible: ¿su organización podría puntuar hoy sus cinco servidores MCP más usados contra esa tabla?

---
