# Glosario operativo del Volumen 1

_Definiciones breves, ancladas al capítulo donde el término se desarrolla. Cuando un término tiene acepciones distintas según el volumen de la serie, se indica. El glosario no sustituye al capítulo: sirve para desambiguar una palabra a mitad de la lectura y para fijar el vocabulario común del equipo._

| Término | Definición operativa | Capítulo |
|---|---|---|
| **Agente** | Sistema que decide el flujo de sus propios pasos en función del estado de la tarea, no solo el contenido de su salida. Se distingue del *workflow* por quién decide el control. | 1, 4 |
| **Workflow (cadena fija)** | Secuencia de pasos predefinida; el modelo rellena contenido, no decide el camino. Se presupuesta, prueba y gobierna distinto que un agente. | 1 |
| **Espectro de autonomía** | Escala de niveles 0 a 4 que clasifica un sistema según cuánto decide por sí mismo. Se elige por la estructura de la tarea, no por la ambición del equipo. | 1 |
| **Arnés (*harness*)** | Conjunto de controles deterministas alrededor del modelo: presupuesto de iteraciones, herramientas permitidas, validación de salida, corte de bucle. Es lo que hace que un agente de laboratorio sobreviva en producción. | 4 |
| **ReAct** | Patrón de razonamiento-acción-observación que alterna pensamiento y uso de herramientas hasta cumplir el objetivo. Base de la familia de patrones de razonamiento. | 4 |
| **Ventana de contexto** | Espacio finito de tokens disponible en una llamada. No es memoria: se vacía al terminar la interacción si nada la persiste. | 4, 10 |
| **Memoria del agente** | Estado que sobrevive a la llamada y se recupera por algún mecanismo explícito (almacén, resumen, índice). Tiene ciclo de vida observable. | 10 |
| **Herramienta (*tool*)** | Capacidad expuesta al agente con nombre, descripción y esquema de entrada. La descripción sugiere su uso; el servidor lo impone. | 4, 9 |
| **Skill** | Unidad de conocimiento procedimental con divulgación progresiva: descripción siempre disponible, contenido cargado cuando la tarea lo requiere. | 7 |
| **Divulgación progresiva** | Estrategia de contexto por la que solo se carga el detalle necesario en el momento necesario, para no degradar rendimiento ni costo. | 7 |
| **Empresa Sintética** | Especialización de agentes en roles con responsabilidades acotadas, análoga a una organización, para reducir la entropía de un agente monolítico. | 5 |
| **Prompt maestro** | Instrucción única reutilizada por varios agentes; aplica DRY a los prompts. Introduce acoplamiento que debe gestionarse. | 5 |
| **Contexto delimitado (*bounded context*)** | Frontera de dominio dentro de la cual un modelo y un lenguaje tienen significado único. Actúa como sistema inmunológico frente a la entropía del modelo. | 6 |
| **Invariante de dominio** | Condición que debe cumplirse siempre en un agregado. Un agente puede violarla sin que un verificador la detecte si el invariante no está explicitado. | 6 |
| **Patrón de orquestación** | Forma canónica de coordinar varios agentes: pipeline, fan-out, *council*, jerárquico y *self-reflection loop*. Cada uno exige su propia política de degradación. | 8 |
| **Degradación** | Operar con calidad o cobertura reducidas pero explícitas, en lugar de fallar. Debe ser visible al consumidor; degradar en silencio es mentir con infraestructura. | 3, 8 |
| **MCP (Model Context Protocol)** | Protocolo que reduce la integración de M×N a M+N entre aplicaciones y sistemas, sobre JSON-RPC. Expone *tools*, *resources* y *prompts*. | 9 |
| **AI Gateway** | Componente de plataforma que centraliza el acceso a modelos: claves, cuotas, presupuesto, caché, auditoría y enrutamiento. | 3 |
| **Corpus de instrucciones** | Conjunto versionado de archivos (`.md`) que gobierna el comportamiento de los agentes. Se trata como código: se revisa, versiona y prueba. | 10 |
| **Regla de dependencia (en contexto)** | Las instrucciones deben depender hacia lo estable, no hacia lo cambiante, igual que en arquitectura limpia. | 10 |
| **Verificador determinista** | Comprobación no probabilística (test, esquema, lint) que valida la salida de un agente. Segunda capa de defensa junto al contexto en el prompt. | 6 |
| **Eval** | Prueba reproducible de calidad de un comportamiento probabilístico; sustituye al test unitario donde el resultado no es binario. | 2, 4 |
