# Capítulo 10: La Arquitectura del Contexto

## El corpus de instrucciones también es código

Los capítulos anteriores de esta parte construyeron las piezas del sistema agéntico: el agente (capítulo 4), los roles (capítulo 5), las fronteras de dominio (capítulo 6), los skills (capítulo 7), la orquestación (capítulo 8) y las herramientas (capítulo 9). Falta la pieza que casi nadie diseña y que, sin embargo, gobierna a todas: el **corpus de instrucciones** que el equipo le da a la IA para que entienda *qué* hace el sistema y *cómo* debe proceder. Hoy ese corpus tiene mil nombres y ninguna arquitectura (`CLAUDE.md`, `AGENTS.md`, `ADR.md`, `spec.md`, `.cursorrules`, `copilot-instructions.md`, una docena de READMEs con reglas) y vive disperso en carpetas o suelto en la raíz, creciendo por acreción.

El capítulo 4 dejó sentada la tesis que ahora cobra su consecuencia más amplia: los artefactos de la era agéntica son *texto leído por un intérprete falible*, y eso es lo que siempre fue el código. Si el corpus de instrucciones es texto que un intérprete ejecuta, entonces **el corpus de instrucciones es código**, y merece la misma arquitectura que cualquier otro código. Hoy no la tiene. Lo que en un proyecto pequeño es un único archivo legible se convierte, cuando el equipo crece, en un monolito de miles de líneas donde nadie sabe ya si *ya se le dijo* a la IA que vigile cierto error, si esa regla sigue vigente o si contradice otra escrita tres meses atrás por alguien que ya no está. El que hace el onboarding del proyecto, humano o agente, hereda la peor de las deudas: la que no se ve hasta que se la pisa.

Y aquí está el giro que eleva el problema de incomodidad a defecto medible: **el monolito de contexto no solo cansa al humano; degrada al modelo**. La evidencia es la misma que el capítulo 4 usó para la ventana de contexto: el rendimiento de los modelos cae cuando la información relevante está enterrada en el medio de un contexto largo, con la conocida curva en U [Liu et al., 2024](#ref-liu2024). Un archivo de reglas de cinco mil líneas es, literalmente, enterrar. La instrucción crítica que en un archivo de cincuenta líneas el modelo respeta, en uno de cinco mil la pierde, no por desobediencia, sino por física del contexto. El corpus inflado es, además, la **causa número uno del Token-Burn** que el capítulo 1 (Vol. 4) cuantifica: si cada invocación arrastra el monolito entero «por contexto», se paga el prefijo completo en cada iteración. Organizar el corpus para cargar solo el dominio relevante no es higiene estética: es la cura simultánea de un problema de calidad y de un problema de costo.

## La regla de dependencia aplicada a los archivos `.md`

La solución no hay que inventarla: lleva décadas escrita. Parnas (1972) enseñó que un sistema se descompone en módulos ocultando dentro de cada uno las decisiones que pueden cambiar; Evans (2003) dio a esos módulos una frontera con sentido de negocio, el *bounded context*; Martin (2017) los ordenó con una regla única, las dependencias apuntan hacia adentro; y Conway (1968) advirtió que la estructura del artefacto terminará reflejando la del equipo, lo queramos o no. **La Arquitectura del Contexto** es, sencillamente, aplicar esas cuatro lecciones al corpus de instrucciones en lugar de al código fuente.

En la práctica, tres capas:

- **El núcleo (reglas transversales).** Lo que vale para todo el sistema y rara vez cambia: el lenguaje ubicuo, los invariantes de seguridad (capítulo 4 (Vol. 4)), las convenciones de estilo, la política de acciones irreversibles. Es pequeño, estable y se lee entero. Es el anillo interior: ningún dominio lo modifica, todos lo respetan.
- **Los dominios (bounded contexts).** Una carpeta por dominio de negocio (`facturacion/`, `inventario/`, `identidad/`), y dentro, solo las reglas, especificaciones y decisiones (ADRs) de *ese* dominio. La información se oculta donde pertenece [Parnas, 1972](#ref-parnas1972): quien trabaja en facturación no carga ni lee las reglas de inventario. La frontera del archivo es la frontera del dominio.
- **El manifiesto (el gateway).** Un único índice en la raíz que no contiene reglas, sino el mapa: qué dominios existen, qué archivo gobierna cada uno y a quién pertenece. Es el equivalente, en la capa de conocimiento, del AI Gateway del capítulo 3: el punto de entrada que enruta. Un agente que llega a implementar un *feature* lee primero el manifiesto, descubre qué dominio toca y carga *solo* ese contexto.

```
contexto/
├── MANIFIESTO.md            # el gateway: mapa de dominios y dueños. NO contiene reglas.
├── nucleo/                  # anillo interior: transversal y estable
│   ├── lenguaje-ubicuo.md
│   ├── seguridad.md         # invariantes no negociables (cap. 14)
│   └── estilo.md
├── facturacion/             # bounded context (cap. 6)
│   ├── reglas.md            # invariantes del dominio
│   ├── spec.md              # qué hace, no cómo
│   └── decisiones/          # ADRs locales al dominio
│       └── 2026-03-tarifas.md
├── inventario/
│   └── reglas.md
└── prompts-maestros/        # casos de uso de negocio, activables (cap. 5 y 7)
    ├── alta-de-cliente.md
    └── conciliacion-mensual.md
```

La regla de dependencia se respeta tal cual: los dominios dependen del núcleo, nunca al revés; ningún dominio importa a otro (si dos dominios necesitan compartir una regla, esa regla pertenece al núcleo, no a un dominio que el otro espía). Y el manifiesto, como todo buen *gateway*, no sabe nada de las reglas que enruta: solo dónde viven. Quien haya leído el capítulo 6 reconocerá que esto no es más que DDD (el mismo que actúa de sistema inmunológico para el código generado) aplicado un nivel más arriba: a las instrucciones que generan ese código.

## Agentes guardianes y prompts maestros

La estructura de archivos es la mitad del patrón; la otra mitad es quién la cuida y cómo se activa. Aquí el volumen se cierra sobre sí mismo.

**Un agente guardián por dominio.** Cada *bounded context* tiene un skill especialista (capítulo 7) cuyo único trabajo es velar por la coherencia de *su* carpeta: detectar reglas duplicadas, contradictorias u obsoletas, y rechazar en revisión cualquier cambio que viole los invariantes del núcleo. Es el patrón council del capítulo 8 puesto al servicio del conocimiento: el guardián de facturación no opina sobre inventario, y por eso opina bien sobre facturación. Cuando una regla nueva llega por *pull request* (porque el corpus se versiona y se revisa como código, no se edita a mano en producción), el guardián del dominio afectado es el primer revisor.

**Un orquestador en el gateway.** Sobre los guardianes vive un orquestador (capítulo 8, patrón jerárquico) que habita el dominio del manifiesto. No conoce las reglas de cada dominio, ni debe; conoce el mapa. Ante una petición de negocio («implementa el descuento por volumen»), lee el manifiesto, identifica que toca `facturacion/`, delega en su guardián y carga solo ese contexto. El orquestador es a los dominios de conocimiento lo que el AI Gateway (capítulo 3) es a los proveedores de modelo: sabe a quién llamar sin saber cómo hace su trabajo el llamado.

**La carpeta de prompts maestros.** Por último, los casos de uso que el negocio pide repetidamente no se reescriben cada vez: viven versionados en `prompts-maestros/`, cada uno como una plantilla que el capítulo 5 ya describió (una estructura, muchos parámetros) y que activa un flujo completo con todo su contexto acotado. «Alta de cliente» o «conciliación mensual» dejan de ser instrucciones improvisadas en un chat y se vuelven artefactos de ingeniería: con dueño, con historial y con la suite de evals (capítulo 3 (Vol. 4)) que certifica que siguen funcionando cuando el modelo o las reglas cambian.

## Caso de estudio: el onboarding que dejó de leer miles de líneas

*(Escenario ilustrativo compuesto, fiel a un patrón recurrente.)*

Un equipo de plataforma acumuló, en dieciocho meses, un `CLAUDE.md` de casi cuatro mil líneas: reglas de seis dominios, decisiones fosilizadas, tres convenciones de nombres que se contradecían y un par de instrucciones que apuntaban a un servicio ya apagado. Cada ingeniero nuevo (y cada agente) lo cargaba entero. Los síntomas eran los del capítulo 1 (Vol. 4) y los del capítulo 4 a la vez: el costo por iteración subía sin que la calidad lo hiciera, y el agente «olvidaba» reglas que estaban escritas, pero enterradas en la línea 2.700.

La refactorización no tocó una sola línea de código de producto: reorganizó el corpus según la Arquitectura del Contexto. Lo transversal y vigente subió al núcleo; cada dominio recibió su carpeta; las decisiones muertas se archivaron con fecha en lugar de borrarse (la regla del Boy Scout del capítulo 4, aplicada al conocimiento); y un manifiesto de treinta líneas reemplazó al portón de cuatro mil. El resultado, medido con la propia instrumentación del equipo: el onboarding dejó de ser «lee todo y reza» y pasó a «el agente carga el dominio del feature»; el contexto medio por invocación cayó de miles a cientos de líneas, con su ahorro directo de tokens (capítulo 1 (Vol. 4)); y la pregunta que abría este capítulo (*¿ya se le dijo a la IA que vigile este error?*) pasó de ser una arqueología de media hora a un `grep` en una carpeta.

## Límites y buenas prácticas

La honestidad que el libro exige obliga al reverso. **Esta arquitectura no es gratis ni siempre conviene.** Para un proyecto pequeño o en sus primeras semanas, un único archivo legible es superior: imponerle bounded contexts a un sistema que cabe en una cabeza es la sobre-ingeniería que el capítulo 4 advierte: la *god class* tiene un gemelo opuesto, igual de dañino, en la fragmentación prematura. El patrón se justifica cuando el corpus deja de caber en una lectura, cuando varios equipos lo editan en paralelo, o cuando el costo del contexto inflado empieza a doler en la factura. Tres buenas prácticas gobiernan su adopción:

- **El manifiesto nunca contiene reglas, solo el mapa.** En cuanto el gateway empieza a acumular lógica, deja de ser un gateway y se vuelve un segundo monolito. Si crece, es señal de que falta un dominio.
- **Una regla, un dueño, un lugar.** Lo único peor que una regla enterrada es la misma regla escrita en dos dominios con dos redacciones distintas. La fuente de verdad es única (DRY, capítulo 4); lo compartido sube al núcleo.
- **El corpus se versiona y se revisa como código.** Un cambio de regla sin revisión es un *commit* directo a la rama principal (capítulo 4); el guardián del dominio es su primer revisor y la suite de evals (capítulo 3 (Vol. 4)), su prueba de regresión.

Como en todo este volumen, el principio es lo estable y la herramienta lo efímero: los nombres de archivo de hoy (`CLAUDE.md`, `AGENTS.md`) cambiarán; la idea de que el corpus de instrucciones es arquitectura, y que se gobierna con fronteras, dueños y una regla de dependencia, sobrevivirá a todos ellos.

## Memoria del Agente: el Ciclo de Vida Observable

La Arquitectura del Contexto se completa cuando el agente mismo se vuelve observable. A través de toda su ejecución, un agente recorre estados (inactivo, procesando, aguardando, completado) cada transición es un evento que el equipo debe poder monitorear, testear y corregir. Comprender estos estados no es un lujo de observabilidad; es el fundamento de la ingeniería: no puedes reparar o optimizar lo que no ves.

> **Justificación de diseño: diagrama de estados para comportamiento dinámico**
>
> El ciclo de vida del agente es un proceso que cambia en el tiempo: nace inactivo, se activa, herramientas la bloquean, se completa o falla. Un diagrama de estados captura exactamente ese *cambio temporal*: transiciones claras, eventos que las disparan, los tiempos en los que el agente puede ser monitoreado o interrumpida.
>
> Un diagrama de clases mostraría qué objetos existen; una secuencia mostraría quién llama a quién. Aquí necesitamos el *qué pasa en el tiempo*, la dimensión que importa para observabilidad, optimización y debugging.
>
> El diagrama de estados reaparece más adelante en el **Capítulo 7 (Vol. 4)** (cuando el agente aguarda un evento en el log), donde de nuevo el tiempo y la transición son lo que interesa.

![Diagrama 10.1: Ciclo de vida del Agente: máquina de estados con transiciones observables](imagenes/uml/diagrama10_estado_es.png)

Cada estado tiene una instrumentación natural:
- **Inactivo → Activo:** el agente recibió un prompt. Registra marca de tiempo, costo inicial.
- **Activo → LlamadaHerramienta:** LLM propuso una herramienta. Registra cuál y parámetros.
- **LlamadaHerramienta → Aguardando:** la herramienta se envió. Comienza medición de latencia.
- **Aguardando → Activo:** resultado disponible. Latencia registrada, siguiente iteración.
- **Activo → Completado:** respuesta final sin herramientas. Ciclo cerrado, costo registrado.
- **Activo/Aguardando → Error:** invariante violada, timeout agotado. Clave para patrones de fallo.

La observabilidad en tiempo de ejecución (capítulo 8 (Vol. 4)) recolecta estas transiciones. Los evals (capítulo 3 (Vol. 4)) verifican que el agente no queda atrapado en un estado, p.ej. Aguardando > N segundos sugiere herramienta lenta o agente bloqueada. El *gateway* (capítulo 3) usa estos estados para tomar decisiones: si el agente entra en Error, escala humana; si Completado dentro del presupuesto, registra éxito.

## Lo esencial del capítulo 10

- El corpus de instrucciones (los `*.md` que la IA lee para saber qué y cómo) es código: texto leído por un intérprete falible, y merece arquitectura.
- El monolito de contexto degrada al modelo (la información enterrada se usa peor; [Liu et al., 2024](#ref-liu2024)) y es la causa #1 de Token-Burn (capítulo 1 (Vol. 4)). Es un defecto medible, no una incomodidad.
- La Arquitectura del Contexto aplica gigantes conocidos a los archivos: ocultación de información [Parnas, 1972](#ref-parnas1972), bounded contexts ([Evans, 2003](#ref-evans2003)), regla de dependencia [Martin, 2017](#ref-martin2017), ley de Conway (1968). Tres capas: núcleo, dominios, manifiesto-gateway.
- Un guardián especialista por dominio (capítulo 7), un orquestador en el gateway que enruta sin conocer las reglas (capítulos 3 y 8), y `prompts-maestros/` versionados como casos de uso de negocio (capítulo 5).
- No siempre conviene: en proyectos pequeños un solo archivo gana. El patrón se justifica cuando el corpus no cabe en una lectura, varios equipos lo editan o el contexto inflado duele en la factura.
