# Capítulo 20: DevSecOps y Permisos para Agentes

> *Un permiso bien diseñado no frena al agente: lo encauza. La diferencia entre una valla y una jaula es el criterio con que fue construida.*

## DevSecOps no es un obstáculo, es un contrato

Para muchos desarrolladores, los permisos y roles de DevSecOps se perciben como fricción: una valla que ralentiza el progreso. Conviene revisar esa percepción, y hacerlo con rigor: la valla de permisos no existe para estorbar, sino para **codificar la confianza en forma de contrato verificable**. Cuando se incluye a los agentes en el flujo de DevSecOps, esta valla deja de ser un detalle operativo y se convierte en la línea de defensa central, puesto que un agente con permisos excesivos es cualitativamente más peligroso que un humano con los mismos permisos (cf. cap. 29).

La razón de esta asimetría es estructural: el humano que abusa de sus privilegios actúa con intención, velocidad humana y un registro cognitivo de consecuencias. El agente que desborda sus límites actúa sin intención pero a velocidad de máquina, replicando el error miles de veces antes de que cualquier sistema de monitorización alcance a registrar la anomalía. He aquí, por tanto, la primera lección: la disciplina de DevSecOps no se relaja en la era agéntica; se intensifica.

> **Versión académica:** La incorporación de sistemas de IA agénticos en los flujos de integración y entrega continua (CI/CD) introduce vectores de riesgo cualitativamente distintos de los asociados a actores humanos. La velocidad de actuación de un agente comprometido o mal configurado excede en varios órdenes de magnitud la capacidad de respuesta de los mecanismos de control tradicionales, lo que eleva el requisito de contención a un rango de criticidad superior.

## Por qué la valla está bien: tres fundamentos inviolables

Tres razones justifican el rigor de permisos y roles, y todas ellas se intensifican cuando los actores son agentes:

- **Contención del daño.** El principio de privilegio mínimo (*least privilege*) limita el radio de explosión de cualquier error, humano o agéntico. Un agente que solo puede leer no puede escribir ni borrar; un agente que solo puede escribir en un directorio específico no puede comprometer el sistema de archivos completo. La superficie de ataque potencial se expresa mediante: `superficie = n_agentes × permisos_promedio × tiempo_de_vida_del_permiso`. Reducir cualquiera de los tres factores reduce el riesgo de manera multiplicativa.
- **Trazabilidad.** Los roles definen quién (o qué agente) puede hacer qué, haciendo auditable cada acción. En un sistema sin roles definidos, una anomalía descubierta en los logs puede no tener origen atribuible; en un sistema con roles bien diseñados, cada acción lleva la firma del agente que la ejecutó, el rol que la autorizó y el momento en que ocurrió. Esta trazabilidad no es un lujo burocrático: es el fundamento de la forensia digital en sistemas agénticos.
- **Reversibilidad.** Una arquitectura de permisos clara permite revocar el acceso de un agente comprometido sin desmontar todo el sistema. Si las credenciales son de corta vida y revocables centralmente, neutralizar a un agente comprometido es una operación de segundos; si las credenciales son permanentes y distribuidas, es una operación de días.

## El modelo de confianza cero aplicado a agentes

El marco de referencia más adecuado para comprender los permisos agénticos es la *Zero Trust Architecture* (ZTA), formalizada por el NIST en la publicación especial 800-207 (Stafford, 2020). El principio rector es deceptivamente simple: "nunca confiar, siempre verificar" (*never trust, always verify*). Aplicado a agentes, este principio se reinterpreta con matices importantes.

En la arquitectura de confianza cero para enjambres, resulta significativo distinguir dos componentes funcionales. El **Policy Decision Point** (PDP) evalúa si una solicitud de acceso es legítima, considerando la identidad del agente, el recurso solicitado, el contexto de la tarea y el estado del sistema. El **Policy Enforcement Point** (PEP) intercepta cada solicitud del agente y la remite al PDP antes de permitir o denegar la acción. En un enjambre bien diseñado, ningún agente accede directamente a ningún recurso: toda acción pasa por este ciclo de decisión.

La diferencia con los sistemas de permisos clásicos es sustancial. En los sistemas RBAC (*Role-Based Access Control*) tradicionales, el rol se asigna al usuario una vez y permanece hasta que un administrador lo revoca. En los sistemas ABAC (*Attribute-Based Access Control*), el acceso se evalúa en función de atributos del sujeto, el recurso y el entorno. Para agentes, el modelo más adecuado es PBAC (*Policy-Based Access Control*): el acceso se decide mediante políticas expresadas como reglas condicionales que tienen en cuenta el riesgo de la acción concreta, no solo la identidad del agente.

| Modelo | Granularidad | Dinamismo | Adecuación para agentes |
|--------|-------------|-----------|------------------------|
| RBAC | Por rol | Baja (cambio manual) | Insuficiente |
| ABAC | Por atributo | Media (evaluación en tiempo real) | Adecuada |
| PBAC | Por política | Alta (reglas condicionales dinámicas) | Óptima |
| ZTA/JIT | Por acción y tiempo | Máxima (just-in-time, efímero) | Excelente |

## El ciclo de vida del permiso agéntico

Una de las contribuciones más importantes que DevSecOps puede aportar a la arquitectura de enjambres es la conceptualización del permiso agéntico como un ciclo de vida, no como un estado binario (tiene/no tiene). El ciclo comprende cinco fases que deben implementarse explícitamente en la infraestructura:

1. **Solicitud**: el agente declara qué necesita hacer y por qué, expresado en lenguaje de política formal. El PDP recibe esta solicitud junto con el contexto de la tarea en curso.
2. **Evaluación de riesgo**: el PDP computa un score de riesgo basado en quién solicita, qué solicita, sobre qué recurso, en qué contexto y en qué momento del flujo de trabajo. Esta evaluación puede incorporar modelos de riesgo probabilístico.
3. **Otorgamiento temporal** (*just-in-time access*): si el PDP aprueba, el permiso se otorga con una vida útil mínima (típicamente el tiempo estimado para completar la tarea más un margen de seguridad del 20%). Expirado ese tiempo, el permiso se revoca automáticamente, sin necesidad de acción humana.
4. **Ejecución monitorizada**: durante la ventana de permiso activo, el PEP registra cada uso del permiso con timestamp, resultado y cualquier anomalía de patrón (por ejemplo: el agente que solicitó permiso de lectura intentó una escritura).
5. **Revocación y auditoría**: al expirar o revocarse el permiso, el registro queda inmutable en el log de auditoría. Cualquier desviación del comportamiento esperado genera una alerta y, dependiendo del nivel de criticidad, puede provocar la cuarentena inmediata del agente.

## Cómo mejorar DevSecOps para la era agéntica

Los modelos de permisos clásicos fueron diseñados para humanos, cuyo comportamiento es relativamente estable y cuya velocidad de acción es predecible. Los agentes imponen tres evoluciones estructurales necesarias, no opcionales:

**Primera evolución: permisos dinámicos y de corta vida.** En lugar de conceder a un agente acceso permanente a una base de datos, se le otorga acceso exactamente cuando lo necesita, por el tiempo mínimo necesario, y se revoca automáticamente. Esta práctica (denominada *just-in-time access* (JIT)) reduce la ventana de exposición de semanas o meses a minutos. Rababah et al. (2024) demuestran que la implementación de JIT en sistemas de IA agénticos reduce el impacto potencial de compromisos en un 73% respecto a los modelos de acceso permanente.

**Segunda evolución: permisos contextuales.** El mismo agente puede merecer más o menos acceso según el riesgo de la tarea concreta. Un agente de síntesis de informes necesita permisos de lectura amplia pero ningún permiso de escritura; ese mismo agente ejecutando una tarea de corrección de datos necesita permisos de escritura acotados a registros específicos. La política es "este agente, cuando ejecuta la tarea Y sobre el recurso Z, tiene acceso A", no "este agente tiene acceso X".

**Tercera evolución: mediación obligatoria.** El agente nunca posee la credencial directamente. En cambio, la solicita a un guardián de secretos (*secrets manager*) que decide si otorgarla, registra el otorgamiento y la revoca cuando expira. Herramientas como HashiCorp Vault o AWS Secrets Manager implementan este patrón. Si el agente es comprometido, el atacante obtiene el agente pero no las credenciales; si las credenciales estuvieran en el agente, el compromiso del agente equivaldría al compromiso de todos los sistemas a los que accede.

## Métricas de madurez DevSecOps para enjambres

Un modelo de madurez de cinco niveles permite a las organizaciones situar su práctica actual y definir una hoja de ruta hacia la gestión óptima de permisos agénticos:

| Nivel | Denominación | Criterios clave | Indicadores |
|-------|-------------|-----------------|-------------|
| 1 | Inicial | Permisos manuales, sin política formal | Tiempo de revocación > 24h |
| 2 | Repetible | RBAC implementado, revisiones periódicas | Permisos revisados trimestralmente |
| 3 | Definido | ABAC/PBAC, JIT para agentes críticos | Permisos efímeros en >50% de accesos |
| 4 | Gestionado | ZTA completa, PDP/PEP para todos los agentes | Detección de anomalías < 5 min |
| 5 | Optimizando | ML en evaluación de riesgo, auto-ajuste de políticas | Falsos positivos < 0.1% |

La mayoría de organizaciones que despliegan enjambres en 2024-2025 operan en el nivel 1 o 2. Rahman et al. (2023) documentan en su revisión sistemática de DevSecOps que solo el 12% de organizaciones con prácticas DevSecOps maduras han extendido esas prácticas a sus sistemas de IA, lo que representa una brecha de seguridad sistémica de considerable magnitud.

## Un índice cuantificable de autonomía

Los niveles de autonomía del capítulo 1 (Vol. 1) son cualitativos: dicen si un sistema opera en Nivel 0 a 4, no cuánta autonomía real ejerce dentro de ese nivel. Para que un comité de arquitectura pueda fijar un umbral objetivo (y no una impresión) este libro propone el **Índice de Autonomía Operativa (IAO)**, ponderado por el riesgo de cada acción según la escala verde/amarillo/rojo ya introducida:

$$\text{IAO} = \frac{\sum (\text{acciones autónomas} \times \text{peso de riesgo})}{\sum (\text{acciones totales} \times \text{peso de riesgo})}$$

donde los pesos $1 / 3 / 10$ corresponden a los niveles verde/amarillo/rojo.

Ponderar por riesgo, y no solo contar acciones, evita el falso positivo más común de este tipo de métricas: un agente que ejecuta miles de acciones verdes sin supervisión pero jamás toca una acción roja sin aprobación puede reportar un 95 % de "autonomía" que no dice nada sobre lo que de verdad importa. El IAO exige que la autonomía se demuestre donde el daño potencial es alto, no donde es barato.

El IAO por sí solo premiaría a un sistema temerario, así que se acompaña de un segundo término, la **tasa de reversión con daño** (τ): la fracción de acciones autónomas que tuvo que revertirse *y* causó un efecto medible antes de revertirse (a diferencia de una reversión limpia, sin consecuencia). El **IAO ajustado** es:

$$\text{IAO}_{\text{ajustado}} = \text{IAO} \times (1 - \tau)$$

**Cómo se usa como gate de promoción entre entornos.** El registro de dependencias del Vol. 4 (capítulo 5, caso 8) ya exige evidencia para ascender de un entorno a otro; el IAO ajustado es esa evidencia expresada en un número:

| Entorno | IAO ajustado mínimo para permanecer | τ máximo tolerado |
|---|---|---|
| Desarrollo | Sin umbral, entorno de exploración | Sin umbral |
| Stage | 0.30 | 5 % |
| QA | 0.50 | 2 % |
| Producción | El valor que QA sostuvo durante al menos dos semanas, nunca superior | 0.5 % |

Estos valores son un punto de partida razonable, no una ley física: cada organización debe calibrarlos con su propio historial de incidentes, pero **debe fijarlos por escrito antes del primer ascenso a producción**, no negociarlos incidente a incidente.

## Auditoría agnóstica del modelo

Medir la autonomía resuelve *cuánto* decide el sistema solo; no resuelve si esa medición sigue siendo válida cuando el modelo detrás del agente cambia (de Claude a GPT-6 Astra, de un proveedor cerrado a Kimi K2.6 en producción propia), que es precisamente el escenario que el Backend Agnóstico (Vol. 2) da por hecho que ocurrirá. Una auditoría de permisos que solo verificó el comportamiento de un modelo no dice nada sobre el comportamiento del siguiente.

La respuesta es lo que este libro llama **auditoría de reproducción cruzada**: en lugar de auditar el modelo, se audita la traza de decisión capturada por el arnés (entrada, contexto, acción tomada, nivel de riesgo asignado, intervención humana si la hubo, el mismo esquema de *spans* de OpenTelemetry del capítulo 11 del Vol. 4), y esa traza se reproduce contra un segundo proveedor sin decirle cuál fue la decisión original. El criterio de aprobación exige que **ambos respeten el mismo cerco de permisos**, no que coincidan en la acción (divergencias razonables son esperables y hasta deseables): si la traza original fue clasificada verde, el segundo proveedor no debe escalarla a una acción roja no autorizada, y viceversa.

**Protocolo mínimo de la auditoría:**

1. Muestrear trazas de producción estratificadas por color de riesgo (más peso a amarillo y rojo, donde el costo de una discrepancia es mayor).
2. Reproducir cada traza contra al menos un proveedor alternativo al que opera en producción, en un entorno aislado sin efectos secundarios reales.
3. Registrar tres resultados posibles por traza: concordancia de clasificación de riesgo, discrepancia dentro de tolerancia (ambos permanecen en el mismo nivel de aprobación requerido), o discrepancia de gobernanza (un proveedor habría actuado sin la aprobación que el otro sí exige).
4. Solo el tercer caso es un hallazgo de auditoría; los dos primeros son evidencia de portabilidad saludable.

Una organización que aprueba este protocolo trimestralmente no solo cumple con la letra del EU AI Act sobre trazabilidad (capítulo 15); demuestra en la práctica que su arquitectura, y no su proveedor de modelo, es la que sostiene la gobernanza, el compromiso de fondo de este libro entero.



![Autonomía graduada: permisos por daño potencial - riesgo bajo, medio y alto](imagenes/uml/c51_graduated_autonomy_es.png)

La trama se complica cuando se reconoce que el rigor excesivo también tiene un costo. Una valla demasiado rígida convierte al agente en inútil: si toda acción requiere aprobación humana previa, se pierde exactamente la autonomía que justificaba el agente. El arte de DevSecOps en la era agéntica consiste en **graduar los permisos según el daño potencial**: libertad amplia donde el error es barato y reversible, control estricto donde es caro e irreversible.

Esta gradación puede formalizarse en tres niveles operativos. El nivel **verde** permite acción autónoma donde el daño potencial es bajo y reversible (leer un documento, generar un borrador). El nivel **amarillo** permite la acción pero con registro reforzado y notificación, cuando el daño potencial es medio (enviar un email, modificar una base de datos de prueba). El nivel **rojo** bloquea la acción hasta aprobación humana explícita, cuando el daño potencial es alto e irreversible (ejecutar código en producción, transferir fondos).

La valla, bien diseñada, no es lo opuesto a la autonomía: es lo que la hace operativamente segura.

## Perspectiva ejecutiva: el costo de la permisividad

**■ PISTA EJECUTIVA**


El argumento definitivo para invertir en gobernanza de permisos agénticos es económico. Una brecha de seguridad causada por un agente con privilegios excesivos tiene un costo medio de $4.35 millones de dólares en todos los sectores, elevándose a $9.44 millones en el sector financiero ([IBM Security, 2023](#ref-ibmsecurity2023)). Este costo incluye detección y contención, recuperación de sistemas, notificación regulatoria, honorarios legales y daño reputacional.

El retorno sobre la inversión en Zero Trust para sistemas agénticos es igualmente claro: las organizaciones que implementan ZTA completa reportan una reducción del 37% en el tiempo de contención de incidentes y una reducción del 50% en el alcance del daño cuando un incidente ocurre ([Gartner, 2024](#ref-gartner2024)). Para un enjambre de 20 agentes en producción durante 12 meses, la inversión en una arquitectura de permisos madura (estimada en 3-4 semanas de trabajo de arquitectura de seguridad) tiene un ROI potencial de 12-15x considerando el costo evitado de un incidente de seguridad de mediana gravedad.

## Lo esencial del capítulo 20

- La valla de permisos de DevSecOps codifica confianza en un contrato verificable; con agentes, es la defensa central porque su velocidad de acción supera la capacidad humana de monitorización.
- Los modelos de permisos evolucionan de RBAC a PBAC/ZTA: dinámicos, contextuales, con mediación obligatoria y ciclo de vida explícito.
- El modelo de madurez de 5 niveles permite localizar la práctica actual; la mayoría de organizaciones está en nivel 1-2 en 2024-2025.
- La gradación por daño potencial (verde/amarillo/rojo) resuelve el falso dilema jaula-vs-anarquía: libertad donde el error es reversible, control donde es irreversible.
- El ROI de invertir en gobernanza de permisos agénticos es de 12-15x considerando el costo evitado de incidentes.
- El Índice de Autonomía Operativa (IAO), ponderado por riesgo y ajustado por reversiones con daño, convierte el ascenso entre entornos en un umbral numérico fijado por escrito, no en una negociación caso a caso.
- La auditoría de reproducción cruzada verifica que el cerco de permisos se sostiene al cambiar de proveedor de modelo: el hallazgo que importa es la discrepancia de gobernanza, no la discrepancia de respuesta.
