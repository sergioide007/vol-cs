# Capítulo 6: DDD como sistema inmunológico

## Por qué la IA sin dominio genera entropía

Un modelo de lenguaje, por naturaleza estadística, tiende a producir la solución más *promedio* para un problema dado: la continuación más probable según su corpus de entrenamiento. En el desarrollo de software, la solución «más promedio» rara vez refleja las reglas de negocio específicas de su dominio. Y cuando el modelo no dispone de la información necesaria, no se detiene: genera contenido plausible y sin fundamento, el fenómeno de alucinación, sistematizado en la literatura como uno de los retos centrales de la generación con LLMs [Ji et al., 2023](#ref-ji2023). La crítica académica temprana lo formuló sin anestesia: un modelo de lenguaje es, en ausencia de anclaje, un repetidor estocástico de formas lingüísticas sin compromiso con la verdad [Bender et al., 2021](#ref-bender2021). Se puede discutir el alcance de esa crítica; su consecuencia técnica resulta ineludible: **el anclaje (grounding) no es opcional en producción**.

El **Domain-Driven Design** ([Evans, 2003](#ref-evans2003)) es la metodología que establece un *lenguaje ubicuo* (un vocabulario compartido entre el negocio y el código) y unas fronteras explícitas (los *bounded contexts*) dentro de las cuales ese vocabulario tiene un significado preciso. Escrito veinte años antes de los LLMs, el DDD resulta ser exactamente el artefacto que un agente necesita: una ontología del negocio, legible por máquina, que separa lo válido de lo inválido.

Cuando un agente conoce el contexto acotado del dominio, puede distinguir entre:

- una *transferencia bancaria* (que implica reglas de validación de saldo, verificación KYC, límites regulatorios), y
- un simple movimiento de números en una base de datos.

Sin ese contexto, el agente produce lo segundo: rápido, barato y potencialmente ilegal. Por eso llamamos al DDD el **sistema inmunológico** de la Empresa Sintética: no acelera al agente; le impide generar tejido dañino a velocidad industrial.

## El diagrama de clases: estructura de un agregado en DDD

> **Justificación de diseño: diagrama de clases para modelado estructural**
>
> En DDD, lo que interesa es la *estructura estática del dominio*: qué entidades existen, cuáles son raíces de agregados, qué invariantes gobiernan sus relaciones. Un diagrama de clases revela exactamente eso: jerarquía, responsabilidades, límites de consistencia. 
>
> Un diagrama de estados mostraría *cuándo* cambia un agregado; un componente mostraría *dónde* vive en el sistema. Aquí necesitamos ver *qué* es un agregado y *quién* es su raíz, el punto único de entrada para todos los cambios del dominio.
>
> En este libro reaparece el diagrama de clases en el **Capítulo 5** (roles de agentes), en el **Capítulo 6 (Vol. 4)** (Clean Architecture y puertos), donde nuevamente usamos clases para mostrar estructuras que no cambian en el tiempo, solo en la composición.

![Diagrama 6.1: Estructura de un Agregado en DDD: Entidad Raíz, sub-entidades y eventos de dominio](imagenes/uml/diagrama6_ddd_es.png)

**► PISTA TÉCNICA: Alimentando el bounded context al agente**

```python
# Ejemplo 6.1: Inyectando el contexto de dominio como "sistema inmunológico".
# El domain context actúa como guardarraíl semántico: invariantes, lenguaje
# ubicuo y anti-patrones, en texto plano versionado junto al código.

DOMAIN_CONTEXT_FINTECH = """
BOUNDED CONTEXT: Transferencias Bancarias — Reglas de Negocio OBLIGATORIAS

INVARIANTES (nunca violar):
1. Una transferencia solo puede crearse si saldo_disponible >= monto + comisión
2. El monto máximo por transferencia es PEN 50,000 (verificar con ConfigService)
3. Transferencias > PEN 10,000 requieren verificación KYC del receptor
4. El estado de una transferencia es inmutable una vez en estado PROCESANDO

LENGUAJE UBICUO:
- "Cuenta" = entidad con IBAN, saldo_disponible, saldo_en_transito, estado
- "Transferencia" = agregado raíz con id_unico, origen, destino, monto, comision, estado
- "Comisión" = calculada por CommissionService según tipo de cuenta y monto
- "Disponible" = saldo total - saldo_en_transito (NO usar saldo total directamente)

CONTEXTOS EXTERNOS (no implementar aquí):
- Autenticación -> AuthContext
- Notificaciones -> NotificationContext
- Reportes regulatorios -> ComplianceContext

ANTI-PATTERNS PROHIBIDOS:
- No acceder a la base de datos directamente (usar repositorios)
- No exponer entidades de dominio en la API (usar DTOs)
- No manejar notificaciones dentro de este contexto
"""

import anthropic

client = anthropic.Anthropic()

def code_with_domain_guard(tarea_tecnica: str) -> str:
    """Genera código con el bounded context inyectado como guardarraíl."""
    response = client.messages.create(
        model="claude-opus-4-8",
        max_tokens=4096,
        system=f"""Eres un senior engineer especializado en DDD y arquitectura hexagonal.

CONTEXTO DE DOMINIO OBLIGATORIO — lee y respeta estas reglas antes de escribir código:
{DOMAIN_CONTEXT_FINTECH}

INSTRUCCIÓN: Genera código que respete ESTRICTAMENTE el bounded context definido.
Si la tarea viola algún invariante, DETENTE y explica qué invariante se viola y por qué.""",
        messages=[{"role": "user", "content": tarea_tecnica}],
    )
    return next(b.text for b in response.content if b.type == "text")
```

Tres prácticas convierten este patrón en infraestructura:

1. **El contexto de dominio vive en el repositorio**, junto al código que gobierna (`domain/CONTEXT.md`), y se revisa en los mismos *pull requests*. Un contexto desactualizado es peor que ninguno: da confianza falsa.
2. **El contexto es un prefijo estable y cacheable.** Las APIs modernas permiten cachear el prefijo del prompt; un contexto de dominio extenso que se reutiliza en cada llamada cuesta una fracción del precio normal a partir de la segunda invocación (véase el capítulo 1 (Vol. 4)). La arquitectura correcta (contexto estable primero, tarea variable al final) es a la vez la más barata y la más fiable, una coincidencia afortunada que conviene explotar.
3. **Cada invariante tiene un test.** El contexto le dice al agente qué no debe violar; el test verifica que no lo violó. El capítulo 3 (Vol. 4) cierra ese bucle.

### Del documento al guardarraíl ejecutable

El paso de madurez siguiente es derivar verificadores automáticos del propio contexto: si el invariante 1 dice que toda transferencia exige saldo suficiente, un verificador estático puede buscar las rutas de código que crean transferencias y comprobar que todas pasan por la validación. El agente revisor del capítulo 5 (`reviewer`) recibe el contexto de dominio en su prompt y el verificador corre en el CI: dos capas inmunológicas, una probabilística y una determinista. La defensa en profundidad no es desconfianza en el modelo; es ingeniería.

**■ PISTA EJECUTIVA**

La pregunta ejecutiva sobre el DDD agéntico es de inversión: documentar los bounded contexts de un sistema legado cuesta semanas de trabajo de las personas más ocupadas de la organización. La respuesta corta: ese documento es ahora un *activo de producción*, no documentación. Se inyecta en cada llamada de cada agente que toca el dominio, multiplica la tasa de código válido a la primera y reduce el retrabajo que hoy consume a esas mismas personas. Las organizaciones que ya practicaban DDD parten con ventaja estructural en la era agéntica; las que no, tienen en la adopción de agentes el incentivo económico que faltaba para pagar esa deuda de modelado.

## Ejercicio resuelto 6.1: escriba el bounded context de un inventario

**Enunciado.** Redacte el contexto de dominio (formato del ejemplo 6.1) para el inventario de un e-commerce con esta regla de negocio: «no se puede vender lo que no está físicamente disponible, y lo reservado por un carrito activo no está disponible».

**Solución comentada.**

```text
BOUNDED CONTEXT: Inventario — Reglas de Negocio OBLIGATORIAS

INVARIANTES (nunca violar):
1. disponible = stock_fisico - reservado; NUNCA vender si disponible < cantidad
2. Una reserva expira a los 30 minutos y devuelve su cantidad a disponible
3. stock_fisico solo cambia por recepción, venta confirmada o ajuste auditado
4. Ningún ajuste manual sin id_auditoria

LENGUAJE UBICUO:
- "Disponible" = stock_fisico - reservado (NUNCA usar stock_fisico a secas)
- "Reserva" = cantidad bloqueada por un carrito activo, con expiración
- "Ajuste" = corrección auditada de stock_fisico (merma, conteo, daño)

CONTEXTOS EXTERNOS (no implementar aquí):
- Precios y promociones -> PricingContext
- Pagos -> PaymentContext

ANTI-PATTERNS PROHIBIDOS:
- No leer stock_fisico para decidir una venta (usar disponible)
- No crear reservas sin expiración
```

Los aciertos a verificar contra su propia solución: (1) la regla del enunciado se descompuso en **invariantes atómicos y verificables**: cada uno puede convertirse en un test (capítulo 3 (Vol. 4)); (2) el término trampa (`stock_fisico` vs. `disponible`) quedó definido en el lenguaje ubicuo **y además prohibido** en los anti-patterns, la redundancia deliberada es defensa en profundidad contra el modelo «promedio» que usaría el campo obvio; (3) la expiración de reservas, que el enunciado no mencionaba pero la regla implica, está explícita: escribir el contexto es la actividad que *descubre* estas reglas tácitas, y ese descubrimiento es la mitad del valor del ejercicio.

## Lo esencial del capítulo 6

- El modelo genera la solución «promedio»; su dominio nunca es promedio. Sin anclaje, alucina con fluidez ([Ji et al., 2023](#ref-ji2023); [Bender et al., 2021](#ref-bender2021)).
- El DDD ([Evans, 2003](#ref-evans2003)) es la ontología legible por máquina que el agente necesita: invariantes, lenguaje ubicuo, fronteras.
- El contexto vive en el repositorio, es prefijo cacheable (≈10 % del costo) y cada invariante tiene su test: tres prácticas, un sistema inmunológico.
- Dos capas de defensa: el contexto en el prompt (probabilística) y los verificadores en CI (determinista).

## Preguntas para discusión

1. ¿Existe en su organización un documento de dominio que un agente pudiera consumir hoy? Si no, ¿quién es la persona que tiene ese conocimiento en la cabeza, y qué pasa si renuncia?
2. ¿Qué invariante de su negocio, violado por código generado a velocidad industrial, causaría el incidente más caro? ¿Está escrito en algún lugar que una máquina pueda leer?
