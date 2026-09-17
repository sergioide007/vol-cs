# Capítulo 7: Creación de skills, enseñar procedimientos a los agentes

## Skills: el conocimiento procedimental del agente

Si los agentes son los trabajadores de la Empresa Sintética, los **skills** son sus especializaciones: procedimientos empaquetados que el agente puede invocar de forma consistente y reproducible. La idea responde a un problema real de ingeniería de contexto: las instrucciones especializadas no pueden vivir todas en el prompt de sistema (lo inflarían hasta degradar el rendimiento y el costo; [Liu et al., 2024](#ref-liu2024)), pero tampoco pueden improvisarse en cada tarea. Un skill es la solución intermedia: una unidad de conocimiento procedimental con **divulgación progresiva**, donde su descripción breve está siempre disponible y su contenido completo se carga solo cuando la tarea lo requiere.

En Claude Code y en la plataforma de agentes de Anthropic, un skill es un archivo Markdown estructurado que define:

1. **Cuándo activarse** (el disparador, basado en la intención del usuario)
2. **Qué hacer** (el procedimiento, paso a paso)
3. **Qué herramientas usar** (el arsenal disponible)
4. **Qué salida producir** (el formato del resultado)

El concepto trasciende a un proveedor: OpenAI y Google ofrecen mecanismos análogos de instrucciones empaquetadas y herramientas predefinidas. Lo que el AI Engineer debe dominar es el principio, no la sintaxis: **el conocimiento procedimental del equipo se versiona en el repositorio y se carga bajo demanda**.

La anatomía de un skill bien diseñado:

```markdown
---
name: domain-review
description: |
  Revisa que el código generado respeta el bounded context del dominio.
  ACTIVAR cuando: el usuario pide revisar código de dominio, menciona DDD,
  bounded context, o cuando se acaba de generar lógica de negocio.
  NO ACTIVAR para: código de infraestructura, UI, tests unitarios simples.
tools:
  - Read
  - Grep
  - Bash
---

# Skill: Domain Review

## Objetivo
Verificar que el código respeta los bounded contexts definidos y no viola
invariantes de dominio.

## Protocolo de Ejecución

### Paso 1: Identificar el Bounded Context
- Buscar el archivo de contexto: `grep -r "BOUNDED CONTEXT" docs/ domain/`
- Si no existe: crear uno básico basado en las entidades encontradas

### Paso 2: Análisis de Violaciones
Buscar estos anti-patterns específicos:
- Acceso directo a DB desde capa de dominio: `grep -r "db\." domain/`
- Entidades expuestas en controllers: verificar que usan DTOs
- Lógica de negocio en repositorios: verificar que solo hacen CRUD

### Paso 3: Verificar Invariantes
Para cada invariante listado en el contexto de dominio:
- Encontrar dónde se implementa en el código
- Verificar que existe un test que lo cubre
- Marcar como "sin cobertura" si no hay test

### Paso 4: Reporte
Producir reporte en este formato:
- RESUMEN: [1 línea: pass/fail + número de violaciones]
- VIOLACIONES CRÍTICAS: [invariantes rotos]
- ADVERTENCIAS: [anti-patterns encontrados]
- ACCIONES REQUERIDAS: [lista numerada de cambios]
```

Nótese que el skill anterior es la **operacionalización del capítulo 6**: el contexto de dominio define las reglas; el skill define el procedimiento para auditarlas. Esa composición, documentos de conocimiento más procedimientos que los consumen, es la forma madura de la ingeniería de contexto.

## Los cinco patrones de skill más valiosos

```
Patrón 1: SKILL DE ANÁLISIS
────────────────────────────
Propósito:  Inspección profunda de artefactos existentes
Disparador: "analiza", "revisa", "audita", "¿qué hace X?"
Estructura: Read -> Grep -> Análisis -> Reporte estructurado
Ejemplos:   security-review, domain-review, performance-audit

Patrón 2: SKILL DE GENERACIÓN
──────────────────────────────
Propósito:  Crear artefactos nuevos siguiendo plantillas
Disparador: "crea", "genera", "scaffoldea", "implementa X"
Estructura: Lee plantillas -> Adapta al contexto -> Escribe -> Valida
Ejemplos:   generate-api-endpoint, scaffold-domain-entity, create-test-suite

Patrón 3: SKILL DE TRANSFORMACIÓN
───────────────────────────────────
Propósito:  Convertir un artefacto del formato A al formato B
Disparador: "migra", "convierte", "refactoriza a X"
Estructura: Lee -> Analiza estructura -> Transforma -> Verifica equivalencia
Ejemplos:   refactor-to-ddd, migrate-to-typescript, convert-to-async

Patrón 4: SKILL DE ORQUESTACIÓN
─────────────────────────────────
Propósito:  Coordinar múltiples agentes o herramientas en secuencia
Disparador: "despliega", "pipeline completo", "proceso de inicio a fin"
Estructura: Plan -> Lanza sub-agentes -> Recoge resultados -> Sintetiza
Ejemplos:   full-deploy-pipeline, code-review-council, onboard-new-service

Patrón 5: SKILL DE VALIDACIÓN
──────────────────────────────
Propósito:  Verificar que invariantes y contratos se cumplen
Disparador: "verifica", "valida", "¿está correcto?", antes de merge/deploy
Estructura: Define criterios -> Ejecuta checks -> Produce go/no-go
Ejemplos:   verify-api-contracts, validate-domain-invariants, pre-deploy-check
```

**► PISTA TÉCNICA: Creando su primer skill**

```bash
# Estructura de directorios para skills en un proyecto Claude Code
mkdir -p .claude/skills

# Skill de ejemplo: auditor de costos de tokens
cat > .claude/skills/cost-audit.md << 'EOF'
---
name: cost-audit
description: |
  Audita el uso de tokens en el código y estima costos mensuales.
  ACTIVAR cuando: el usuario pregunta sobre costos, menciona token-burn,
  quiere optimizar el gasto en IA, o antes de lanzar a producción.
tools:
  - Grep
  - Read
  - Bash
---

# Cost Audit Skill

## Objetivo
Identificar llamadas a APIs de LLM en el código y estimar su costo mensual
basado en el uso esperado.

## Proceso

1. Encontrar todas las llamadas a APIs de modelos:
   `grep -rn "messages.create\|chat.completions\|generate_content" --include="*.py" .`

2. Para cada llamada encontrada:
   - Identificar el modelo usado
   - Estimar tokens de entrada (system prompt + contexto típico)
   - Estimar tokens de salida (max_tokens configurado)
   - Calcular costo por llamada según la tabla de precios local

3. Estimar volumen mensual basado en:
   - Endpoints HTTP: revisar logs o asumir un volumen conservador documentado
   - Jobs batch: leer configuración del scheduler
   - Llamadas síncronas: contar por usuario activo

4. Producir tabla: Función | Modelo | Tokens/call | Costo/call | Costo/mes

## Tabla de precios
NO uses precios memorizados: lee el archivo `config/precios_llm.json`
del repositorio (actualizado trimestralmente por el equipo de plataforma)
y, si no existe, indica al usuario que debe crearlo desde la documentación
oficial del proveedor.
EOF
```

El detalle final del skill, prohibir precios memorizados y exigir un archivo de configuración versionado, ilustra un principio general: **los skills no deben contener datos perecederos**. Contienen procedimientos (estables) que leen datos (volátiles) de fuentes versionadas. Un skill con precios incrustados de 2026 seguirá susurrando esos precios en 2028.

**■ PISTA EJECUTIVA**

Los skills son la respuesta a una pregunta que toda dirección de ingeniería se hace: «¿cómo evitamos que el conocimiento de nuestros mejores ingenieros viva solo en sus cabezas?». La respuesta clásica, la documentación, fracasa porque la documentación no se ejecuta y, por tanto, se desactualiza sin que nadie lo note. Un skill es documentación que **se ejecuta**: cuando el procedimiento queda obsoleto, el skill falla de forma visible y alguien lo arregla. La biblioteca de skills de una organización es, literalmente, su know-how operativo convertido en activo digital: inventariable, versionable y transferible al siguiente empleado o al siguiente agente.

## Skills limpios: plantillas y la checklist de revisión

El Código Limpio Sintético (capítulo 4) aplicado a los skills produce dos artefactos concretos. El primero es la **plantilla de skill**, el equivalente del prompt maestro del capítulo 5 para conocimiento procedimental: todo skill de la organización nace de la misma estructura (frontmatter con disparadores positivos y negativos, objetivo en una frase, protocolo numerado, formato de reporte), de modo que leer un skill ajeno cuesta lo mismo que leer el propio. Los cinco patrones de este capítulo son, precisamente, cinco plantillas: el equipo no redacta skills desde cero, instancia el patrón que corresponde.

El segundo es la **checklist de revisión de skills**, porque un skill entra al repositorio por *pull request* como cualquier código:

1. **Nombre y disparador.** ¿El nombre dice qué hace (`cost-audit`, no `utils`)? ¿La descripción dice cuándo activarse **y cuándo no**? El disparador negativo evita activaciones falsas, el error más común.
2. **Responsabilidad única.** ¿Encapsula UN procedimiento? Un skill que analiza «y de paso corrige» son dos skills mal mezclados.
3. **Sin datos perecederos.** ¿Precios, versiones, URLs cambiantes? Van a configuración versionada, no al skill.
4. **Herramientas mínimas.** ¿La lista `tools` es la mínima necesaria? Un skill de análisis no necesita permisos de escritura (mínimo privilegio, capítulo 4 (Vol. 4)).
5. **Salida verificable.** ¿El formato de reporte permite un eval automático (capítulo 3 (Vol. 4))?
6. **Probado.** ¿Existe al menos un caso de prueba con entrada y salida esperada en la suite?

Seis preguntas, dos minutos por revisión: la diferencia entre una biblioteca de skills y un cajón de prompts sueltos.

## Ejercicio resuelto 7.1: un skill de validación pre-deploy

**Enunciado.** Instancie el patrón 5 (validación) en un skill `pre-deploy-check` que verifique, antes de cada despliegue: que los tests pasan, que no hay credenciales en el código y que el CHANGELOG fue actualizado. Aplique la checklist anterior.

**Solución comentada.**

```markdown
---
name: pre-deploy-check
description: |
  Verifica condiciones de despliegue: tests, credenciales, changelog.
  ACTIVAR cuando: el usuario pida desplegar, mencione release o pre-deploy.
  NO ACTIVAR para: despliegues a entornos locales o de experimentación.
tools:
  - Bash
  - Grep
  - Read
---

# Pre-Deploy Check

## Objetivo
Producir un go/no-go verificable antes de desplegar a producción.

## Protocolo
1. Tests: ejecutar la suite (`npm test` o `pytest -q` según el proyecto);
   capturar el código de salida.
2. Credenciales: `grep -rEn "(api[_-]?key|secret|password)\s*[:=]\s*['\"]"`
   sobre el código fuente, excluyendo tests y ejemplos documentados.
3. Changelog: verificar que CHANGELOG.md tiene una entrada cuya versión
   coincide con la del manifiesto del proyecto.

## Reporte (formato fijo, evaluable)
- VEREDICTO: GO | NO-GO
- CHECKS: [tests: pass/fail] [credenciales: limpio/hallazgos] [changelog: ok/falta]
- BLOQUEANTES: [lista, vacía si GO]
```

Contra la checklist: (1) nombre y disparadores (incluido el negativo) explícitos; (2) una sola responsabilidad: *valida*, no corrige ni despliega (corregir sería otro skill; desplegar, una acción crítica con guardia humana, capítulo 1 (Vol. 3)); (3) sin datos perecederos, los comandos de test se detectan del proyecto, no se fijan versiones; (4) tres herramientas de solo lectura y ejecución acotada, sin permisos de escritura; (5) el formato `VEREDICTO/CHECKS/BLOQUEANTES` es trivialmente evaluable por una aserción determinista; (6) el caso de prueba mínimo: un repositorio de juguete con una credencial plantada debe producir `NO-GO` con el hallazgo listado.

## Lo esencial del capítulo 7

- Un skill = conocimiento procedimental versionado con divulgación progresiva: descripción siempre visible, contenido bajo demanda.
- Cinco patrones-plantilla: análisis, generación, transformación, orquestación, validación. Se instancian, no se improvisan.
- Los skills no contienen datos perecederos: procedimientos estables que leen configuración versionada.
- Checklist de revisión de seis puntos en cada PR de skill, es código, y se revisa como código.
- Un skill es documentación que se ejecuta: cuando queda obsoleto, falla visiblemente y alguien lo arregla.

---
