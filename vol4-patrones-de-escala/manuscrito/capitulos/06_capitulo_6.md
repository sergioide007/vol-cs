# Capítulo 6: Arquitectura limpia para sistemas agénticos

## El modelo es un detalle

*Clean Architecture* organiza el software en anillos concéntricos (entidades, casos de uso, adaptadores de interfaz, frameworks) gobernados por una única regla: **las dependencias apuntan hacia adentro**; nada en un anillo interior sabe que los anillos exteriores existen ([Martin, 2017](#ref-martin2017)). Su frase más citada es también la más incomprendida: «la base de datos es un detalle». No significa que la base de datos no importe; significa que las reglas de negocio no deben depender de ella.

La traducción a la era agéntica es inmediata y, para muchos equipos, incómoda: **el modelo de lenguaje es un detalle**. El proveedor, el identificador del modelo, el SDK: todo eso vive en el anillo exterior, junto a la base de datos y el framework web. Lo que vive adentro es la *política*: qué significa revisar código en su organización, qué invariantes de dominio no se negocian (capítulo 6), qué contrato cumple cada rol (capítulo 5). Un sistema agéntico bien diseñado puede cambiar de proveedor en una tarde porque ningún caso de uso importa `anthropic` ni `openai`: importa un **puerto**.

> **Justificación de diseño: diagrama de clases para modelado estructural**
>
> Clean Architecture es una *estructura de dependencias*: qué clases habitan cada anillo, cuál es la jerarquía (entidades → casos de uso → adaptadores), cuál es el flujo de la regla de dependencia. Un diagrama de clases con sus anillos concéntricos revela exactamente eso: la topología estática donde viven los objetos y cómo se relacionan.
>
> Un diagrama de componentes mostraría dónde viven los servicios en el servidor; un diagrama de secuencias mostraría un flujo ejecutado. Aquí necesitamos ver *la estructura de capas y dependencias*, el esqueleto que nunca cambia en tiempo de ejecución.
>
> El diagrama de clases reaparece en este libro en el **Capítulo 5** (La Empresa Sintética), en el **Capítulo 6** (DDD y agregados), donde nuevamente usamos clases para mostrar relaciones estructurales que gobiernan el sistema.

![Diagrama 6.1: Arquitectura Limpia (diagrama de clases con anillos concéntricos)](imagenes/capitulo15/diagrama15_1_es.png)

Obsérvese qué quedó en el centro: los prompts maestros y los contextos de dominio son **reglas de negocio expresadas en prosa**: pertenecen al núcleo, se versionan con él y no saben qué modelo las ejecutará. El lector atento reconocerá que el AIGateway del capítulo 3 ya era esta idea en miniatura: un puerto con tres adaptadores. Este capítulo la formaliza.

**► PISTA TÉCNICA: El puerto LLM en Java**

```java
// Ejemplo 6.1 (Java 17+, Spring Boot): el puerto y su caso de uso.
// El núcleo define QUÉ necesita; el anillo exterior decide CÓMO.

// ── Anillo interior: el puerto (no conoce a ningún proveedor) ──
public interface LlmPort {
    LlmResult complete(String system, String user, TaskTier tier);
}

public enum TaskTier { FAST, BALANCED, QUALITY }

public record LlmResult(String text, int inputTokens,
                        int outputTokens, String modelUsed) {}

// ── Caso de uso: política pura, testeable sin red ──
@Service
public class RevisarCodigoUseCase {

    private final LlmPort llm;                 // inyección del puerto
    private final ContextoDominio contexto;    // capítulo 6
    private final RegistroCostos costos;       // capítulo 11

    public RevisarCodigoUseCase(LlmPort llm, ContextoDominio contexto,
                                RegistroCostos costos) {
        this.llm = llm;
        this.contexto = contexto;
        this.costos = costos;
    }

    public Revision ejecutar(String diff) {
        var resultado = llm.complete(
            contexto.promptMaestro("reviewer"),     // capítulo 5
            "Revisa este diff:\n" + diff,
            TaskTier.BALANCED                        // política, no modelo
        );
        costos.registrar("code-review", resultado);
        return Revision.desdeJson(resultado.text()); // contrato verificable
    }
}

// ── Anillo exterior: el adaptador (lo único que conoce el SDK) ──
@Component
public class AnthropicAdapter implements LlmPort {

    private final AnthropicClient client = AnthropicOkHttpClient.fromEnv();
    private final ModelRegistry registry;   // tier -> model id, en config

    public AnthropicAdapter(ModelRegistry registry) {
        this.registry = registry;
    }

    @Override
    public LlmResult complete(String system, String user, TaskTier tier) {
        var params = MessageCreateParams.builder()
                .model(registry.modelFor(tier))   // nunca cableado
                .maxTokens(4096L)
                .systemOfTextBlockParams(java.util.List.of(
                        TextBlockParam.builder().text(system).build()))
                .addUserMessage(user)
                .build();
        var response = client.messages().create(params);
        var text = response.content().stream()
                .flatMap(b -> b.text().stream())
                .map(t -> t.text())
                .reduce("", String::concat);
        return new LlmResult(text,
                (int) response.usage().inputTokens(),
                (int) response.usage().outputTokens(),
                response.model().toString());
    }
}
```

Tres dividendos paga esta estructura, y todos son los de siempre ([Martin, 2017](#ref-martin2017)). **Testeabilidad:** el caso de uso se prueba con un `LlmPort` falso que devuelve respuestas fijas, sin red, sin costo, en milisegundos; los evals (capítulo 13) prueban el adaptador real, cada capa con su instrumento. **Independencia de proveedor:** la decisión de enrutar `QUALITY` a un proveedor y `FAST` a otro vive en configuración, y la comparación entre proveedores (capítulo 3) se vuelve un experimento de una línea. **Legibilidad de la política:** un auditor (humano o regulatorio; capítulo 1 (Vol. 3)) lee el caso de uso y ve la regla de negocio sin escarbar entre detalles de SDK.

Igualmente, la versión Node.js/TypeScript del mismo puerto, para el lector del otro ecosistema:

```typescript
// Ejemplo 6.2 (TypeScript / Node 20+): mismo puerto, otro idioma.
import Anthropic from "@anthropic-ai/sdk";

export type TaskTier = "fast" | "balanced" | "quality";

export interface LlmResult {
  text: string;
  inputTokens: number;
  outputTokens: number;
  modelUsed: string;
}

export interface LlmPort {
  complete(system: string, user: string, tier: TaskTier): Promise<LlmResult>;
}

export class AnthropicAdapter implements LlmPort {
  private client = new Anthropic(); // ANTHROPIC_API_KEY del entorno
  constructor(private registry: Record<TaskTier, string>) {}

  async complete(system: string, user: string,
                 tier: TaskTier): Promise<LlmResult> {
    const r = await this.client.messages.create({
      model: this.registry[tier],
      max_tokens: 4096,
      system,
      messages: [{ role: "user", content: user }],
    });
    const text = r.content
      .filter((b): b is Anthropic.TextBlock => b.type === "text")
      .map((b) => b.text).join("");
    return { text, inputTokens: r.usage.input_tokens,
             outputTokens: r.usage.output_tokens, modelUsed: r.model };
  }
}
```

## Rigor técnico avanzado: Value Objects y el patrón hexagonal completo

El código anterior oculta una decisión de diseño que separa los sistemas agénticos de producción de los prototipos. Observese que en lugar de pasar parámetros primitivos sueltos (`system: String, user: String, tier: TaskTier`), la versión de producción empaqueta la solicitud en un **objeto de valor** (`InferenciaRequest`). La diferencia parece trivial en una llamada; a escala de cien agentes interactuando durante años, es la diferencia entre un sistema mantenible y un cementerio de deuda técnica.

La arquitectura hexagonal completa, elevada al rigor de Dominio-Driven Design ([Evans, 2003](#ref-evans2003)), organiza el sistema en tres capas concéntricas, cada una con una responsabilidad única y un conjunto de tipos que la caracterizan:

![Diagrama 6.2: Arquitectura Hexagonal con DDD: Núcleo del Dominio, Capas de Aplicación e Infraestructura (diagrama de clases de arquitectura avanzada)](imagenes/capitulo16/diagrama6_ddd_es.png)

Las decisiones arquitectónicas que el diagrama codifica explican por qué cada componente merece estar ahí:

**Agrupación en capas del hexágono.** El paquete central (`Núcleo del Dominio`) contiene interfaces de puerto, tipos de valor y enumeraciones: el contrato que ningún detalle externo negocia. El paquete intermedio (`Capa de Aplicación`) tiene casos de uso que coreografían el flujo de negocio, inyectando el puerto en su constructor. El paquete exterior (`Infraestructura`) implementa los adaptadores que hablan a los SDKs externos. La regla de dependencia, nuevamente: **las dependencias siempre apuntan hacia adentro; el núcleo no conoce la infraestructura**. Esto no es cosmética; es el fundamento de la testeabilidad sin red, de la independencia de proveedor y de la auditabilidad (capítulo 1 (Vol. 3)).

**Encapsulamiento mediante Objetos de Valor.** Un objeto de valor (Value Object en DDD) es un objeto sin identidad única que encapsula un concepto del dominio. `InferenciaRequest` no tiene un ID de base de datos; lo que lo define es su estructura (`promptSistema`, `promptUsuario`, `escalafon`). El dividendo: futuras configuraciones (temperatura del modelo, límite de tokens, seed para reproducibilidad) se añaden a `InferenciaRequest` sin que el puerto cambie de firma. Los métodos del puert siguen siendo los mismos; la interfaz es estable. En sistemas sin Value Objects, cada nueva necesidad demanda una nueva firma de función, un nuevo adaptador, nuevas pruebas. Con ellos, el contrato es inmutable desde afuera.

**Erradicación de la obsesión por primitivos.** En el dominio de los agentes de IA, los tokens no son un `int` cualquiera: son dinero, son cuota, son gobernanza. La clase especializada `ConsumoTokens` encapsula esa semántica: no solo almacena el número, sino que puede calcular el costo estimado (`calcularCostoEstimado()`), validar que no excede presupuesto y generar eventos de alerta. Un auditor o un ingeniero leyendo `resultado.metatasa.calcularCostoEstimado()` entiende de inmediato que está tocando un concepto crítico. Un auditor leyendo `resultado.outputTokens * 0.00003` (multiplicación mágica) tiene que escarbar.

**Acoplamiento débil mediante discontinuidad en las flechas.** Las flechas discontinuas (`..>`) en el diagrama indican dependencias de uso temporal: instanciación, lectura, invocación de métodos. Las flechas sólidas (`-->`) indican composición estructural: propiedades que viven dentro de un objeto. El patrón es: `ReviewCodeUseCase` depende continuamente de `LlmPort` (composición: lo posee como campo) pero depende discontinuamente de `InferenciaRequest` (lo construye y lo pasa, pero no lo posee). Esa distinción permite cambiar cómo se construyen las solicitudes sin que el caso de uso cambie.

![Diagrama 6.3: Grafo de objetos en tiempo de ejecución, instancias en memoria del caso de uso, el contexto y el registro de costos operando juntos](imagenes/capitulo16/objeto_runtime_ddd_es.png)

El diagrama 6.3 completa el cuadro: cómo lucen los objetos **en la memoria del servidor en tiempo de ejecución**. El `ReviewCodeUseCase` instanciado posee referencias a tres servicios (el puerto, el contexto, el ledger de costos). Cada objeto, a su vez, mantiene su estado: `AgentDomainContext` sabe el repositorio en el que trabaja; `AgentExecutionSession` rastrea en qué paso de la tarea está el agente y cuántos tokens ha consumido hasta ahora. Es el esqueleto en memoria que explica cómo se gobiernan las transacciones economicas y técnicas durante una ejecución real. Sin ese diagrama, el código es una serie de inyecciones mágicas; con él, la topología es clara.

**► PISTA TÉCNICA: El patrón Value Object en Java, paso a paso**

```java
// En el núcleo del dominio: los tipos de valor sin contrapartida en BD
public record ConsumoTokens(
    int tokensEntrada, 
    int tokensSalida
) {
    // Invariante: ambos deben ser no negativos
    public ConsumoTokens {
        if (tokensEntrada < 0 || tokensSalida < 0)
            throw new IllegalArgumentException("Tokens negativos no válidos");
    }
    
    // La lógica de negocio vive dentro del Value Object
    public BigDecimal calcularCostoEstimado(
            BigDecimal precioEntrada,  // $0.003 por 1K tokens de entrada
            BigDecimal precioSalida) {  // $0.015 por 1K tokens de salida
        return precioEntrada.multiply(
            BigDecimal.valueOf(tokensEntrada).divide(
                BigDecimal.valueOf(1000)))
        .add(precioSalida.multiply(
            BigDecimal.valueOf(tokensSalida).divide(
                BigDecimal.valueOf(1000))));
    }
}

public record InferenciaRequest(
    Prompt promptSistema,
    Prompt promptUsuario,
    TaskTier escalafon
) {
    // Constructor validador (Java 16+)
    public InferenciaRequest {
        Objects.requireNonNull(promptSistema, "Sistema no puede ser nulo");
        Objects.requireNonNull(promptUsuario, "Usuario no puede ser nulo");
        Objects.requireNonNull(escalafon, "Tier no puede ser nulo");
    }
}

public record InferenciaResponse(
    String textoGenerado,
    ConsumoTokens metatasa,
    String identificadorModelo
) {}

// En la capa de aplicación: el caso de uso que orquesta con los Value Objects
@Service
public class RevisarCodigoUseCase {
    private final LlmPort motorIA;
    private final RegistroCostos registroCostos;
    
    public InformeRevision ejecutar(String diff) {
        // Construcción explícita de la solicitud: el contrato es visible
        var solicitud = new InferenciaRequest(
            Prompt.del("contexto/reviewer-maestro.txt"),
            Prompt.del("diff:\n" + diff),
            TaskTier.BALANCEADO
        );
        
        var respuesta = motorIA.generarCompletado(solicitud);
        
        // El costo se calcula con semántica de dominio, no con números sueltos
        BigDecimal costo = respuesta.metatasa()
            .calcularCostoEstimado(
                BigDecimal.valueOf(0.003),  // precio entrada
                BigDecimal.valueOf(0.015)   // precio salida
            );
        
        registroCostos.registrar("code-review", costo, respuesta.identificadorModelo());
        
        return InformeRevision.desdeJson(respuesta.textoGenerado());
    }
}
```

La inversión de esta estructura se ve en el tiempo de mantenimiento. Cuando el proveedor cambia de precio (ocurre cada trimestre), solo `calcularCostoEstimado()` en `ConsumoTokens` se modifica: un método, un lugar. Cuando la política de negocio decide limitar el consumo por agente, la validación se añade a `ConsumoTokens` en el constructor: el invariante de dominio protege todas las instancias, automáticamente. Cuando un auditor de compliance debe verificar que cada llamada al LLM registra su costo, una auditoría de tipos (`grep "registroCostos.registrar"`) es suficiente: el flujo es explícito.

## Caso de estudio: la migración Java → Node como prueba de la arquitectura

*(Relato en primera persona de un caso real que el autor lideró en un procesador de pagos a gran escala; por confidencialidad se omiten el nombre de la organización y de sus clientes.)*

Una de las migraciones que más recuerdo fue la más enredada, no la más grande. Eran miles de líneas de Java heredado, tocadas por equipo tras equipo durante años: código de «tócame y me desarmo» (o peor, «mejor ni me toques»). Y no era un juguete: era un procesador de pagos a gran escala, donde una hora de caída se cuenta en millones de transacciones fallidas, en caos operativo y en la reputación de toda la organización; muchos millones de dólares dependían de que no me equivocara.

Y aun así, ninguna inmensidad le gana a un buen análisis y a un diseño con buenas prácticas. Yo ya había leído a Robert C. Martin, a Martin Fowler y a la Banda de los Cuatro con sus veintitrés patrones, y lo llevaba tan dentro que me dije: si esto es cierto, lo aplico y funciona. Lo apliqué. Y funcionó.

No traduje el enredo: lo desarmé primero. Y no bastó un solo patrón (pocas veces basta uno): combiné tres. Con Chain of Responsibility, Strategy y Template Method convertí aquella maraña de `if` anidados en piezas con una sola responsabilidad cada una. El resultado fue una tasa de error de cero, mientras varias migraciones vecinas terminaban en rollback. Hasta ese momento, nadie daba fe de que se pudiera hacer así.

Cuento esto porque encierra la lección de todo el capítulo; el resto de esta sección la generaliza en un procedimiento que cualquiera puede repetir.

Un equipo debe migrar un backend Spring Boot a Node.js/TypeScript: controladores REST, servicios, autenticación, mensajería WebSocket, jobs por lotes. Decide hacerlo asistido por agentes, y la primera lección llega antes del primer prompt: **la calidad de la migración la decide la arquitectura de partida, no el modelo**. Donde el código original tenía puertos y casos de uso limpios, el agente traduce política (interfaces, contratos, tipos) y el resultado compila y pasa los tests de caracterización a la primera en una fracción dominante de los módulos. Donde la lógica de negocio estaba enredada con el framework, el agente traduce *el enredo*, fielmente, a velocidad industrial: deuda técnica con sintaxis nueva.

El procedimiento que funcionó, convertido en regla: primero **analizar, entender y apropiarse** del código original (qué hace, qué tipos maneja, qué invariantes protege) y solo después traducir, verificando el mapeo de tipos entre ecosistemas en cada frontera (el `BigDecimal` que se convierte en `number` de coma flotante es el clásico bug silencioso de seis meses). En términos de este libro: la migración es un skill de transformación (capítulo 7, patrón 3) cuyo paso «verifica equivalencia» son los tests de caracterización, y la arquitectura limpia es lo que hace que ese skill tenga fronteras donde apoyarse. La conclusión ejecutiva del caso invierte la pregunta habitual: antes de presupuestar «migrar con IA», presupueste «limpiar las fronteras para que la IA pueda migrar».

## Ejercicio resuelto 6.1: detecte las violaciones de la regla de dependencia

**Enunciado.** Este caso de uso fue escrito por un agente sin contexto arquitectónico. Señale las violaciones de la regla de dependencia y corríjalas.

```java
@Service
public class TriarTicketUseCase {
    public Triage ejecutar(String ticket) {
        var client = AnthropicOkHttpClient.fromEnv();              // (1)
        var params = MessageCreateParams.builder()
                .model(Model.CLAUDE_SONNET_4_6)                    // (2)
                .maxTokens(1024L)
                .addUserMessage("Clasifica: " + ticket)            // (3)
                .build();
        var r = client.messages().create(params);
        kafkaTemplate.send("triage-done", r.toString());           // (4)
        return null;
    }
}
```

**Solución comentada.** (1) El caso de uso construye el cliente del SDK: el anillo interior fabricando un detalle del exterior; se sustituye por el puerto `LlmPort` inyectado. (2) El identificador del modelo cableado en la política: la decisión correcta del núcleo es un *tier* (`FAST`); el mapeo tier→modelo vive en configuración del anillo exterior. (3) El prompt improvisado en una concatenación: el rol de triaje tiene un prompt maestro versionado (capítulo 5) que pertenece al dominio; la ausencia de contrato de salida hace, además, inverificable el resultado. (4) La publicación directa a Kafka: otro detalle del exterior dentro del núcleo; se invierte con un puerto `EventPublisherPort`, que es, justamente, el puente hacia el capítulo siguiente. La versión corregida tiene cuatro líneas de política y cero imports de infraestructura: ese es el test visual de un caso de uso limpio.

## Lo esencial del capítulo 6

- La regla de dependencia ([Martin, 2017](#ref-martin2017)) aplicada a agentes: **el modelo es un detalle**; proveedor y SDK viven en el anillo exterior.
- Los prompts maestros y los contextos de dominio son reglas de negocio en prosa: pertenecen al núcleo y se versionan con él.
- Puerto + adaptadores = testeabilidad sin red, independencia de proveedor y política legible.
- **Rigor técnico con Value Objects ([Evans, 2003](#ref-evans2003)):** encapsular conceptos de dominio (tokens, costos, prompts) en tipos que expresan semántica, no solo datos. Un `ConsumoTokens` que calcula costos es mejor que un `int` que se multiplica mágicamente en un rincón.
- Agrupación en capas del hexágono: el núcleo (puertos e interfaces) jamás depende de la infraestructura (adaptadores). Esa dirección de dependencia es el eje sobre el que gira la mantenibilidad a largo plazo.
- En migraciones asistidas por agentes, la arquitectura de partida decide la calidad del resultado: limpiar fronteras antes de migrar.
- Test visual del caso de uso limpio: cero imports de infraestructura; Value Objects que validan sus propios invariantes en el constructor.
- El grafo de objetos en tiempo de ejecución revela cómo el sistema toma decisiones económicas y técnicas durante una tarea real; sin él, la gobernanza es invisible.

---
