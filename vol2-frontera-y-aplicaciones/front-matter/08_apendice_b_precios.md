# Apéndice B: precios de referencia y cómo calcular el coste de un pipeline

> **Fecha de corte: 28 de septiembre de 2026.** Fuente: documentación oficial de
> Anthropic (páginas «Models overview» y «Pricing»). Los precios de los
> proveedores cambian varias veces al año. Este apéndice es el único lugar de la
> serie donde se escriben cifras de precio: si el lector encuentra un importe
> distinto en otro capítulo, es un error editorial. Para los valores vigentes,
> consulte la página oficial de precios.

## B.1. Por qué este apéndice existe

Dos capítulos remiten a él: el capítulo 5 del Vol. 1, para calcular el coste de
un pipeline de clasificación y redacción, y el capítulo 9 del Vol. 4, para
contar el gasto de una semana de trabajo con un asistente. Ninguno de los dos
puede hacerlo sin una tabla común, y una tabla repetida en dos capítulos
terminaría discrepando en la tercera edición.

El capítulo 3 del Vol. 3 lo menciona como ejemplo de la obsolescencia del
conocimiento: los modelos nombrados aquí tendrán sucesores en meses, y lo que no
caduca son los principios para diseñar, evaluar y controlar.

## B.2. Precios por millón de tokens (USD)

| Modelo | Entrada | Salida | Para qué |
|---|---:|---:|---|
| Fable 5.1 | 10,00 | 50,00 | Razonamiento exigente y trabajo agéntico de horizonte largo |
| Opus 5.5 | 4,00 | 20,00 | Razonamiento largo y trabajo de conocimiento; recomendado por defecto |
| Sonnet 5 | 2,00 | 10,00 | Mejor combinación de velocidad e inteligencia |
| Haiku 4.5 | 1,00 | 5,00 | El más rápido, con inteligencia casi de frontera |

Modelos anteriores, todavía disponibles: Opus 4.8, 4.7, 4.6, 4.5 y 4.1 (5,00 /
25,00), Sonnet 4.6, 4.5 y 4 (3,00 / 15,00) y Haiku 3.5 (0,80 / 4,00).

Un pipeline que consume 2 MTok de entrada y 0,5 MTok de salida con **Sonnet 5**
cuesta `2 × 2,00 + 0,5 × 10,00 = 9,00 USD` por ejecución. El mismo trabajo con
**Haiku 4.5** cuesta `2 × 1,00 + 0,5 × 5,00 = 4,50`, y con **Opus 5.5**,
`2 × 4,00 + 0,5 × 20,00 = 18,00`.

La elección no es solo de precio. Sonnet 5 y Opus 5.5 se reservan para tareas
donde un error se paga caro; Haiku 4.5 cubre clasificación, extracción y
filtrado, donde el volumen domina el resultado. Sustituir el modelo de una etapa
sin cambiar su contrato es la operación más barata disponible.

> **Advertencia de tokenizer.** Los modelos Claude 4.7 y posteriores usan un
> tokenizador más nuevo que produce aproximadamente un **30 % más de tokens**
> para el mismo texto; Sonnet 4.6 y anteriores usan el anterior. Comparar coste
> entre familias sin tener en cuenta este factor lleva a conclusiones
> equivocadas: no basta con comparar los precios por MTok.

## B.3. Suscripciones frente a API

| Modalidad | Precio | Adecuada para |
|---|---:|---|
| Suscripción de consumo | cuota mensual fija | Trabajo diario sin desglose de gasto |
| API por token | según B.2 | Procesos automatizados y coste por etapa |

La suscripción ofrece un techo mensual conocido y un desglose desconocido. Cuando
hace falta saber cuánto costó cada llamada —que es exactamente lo que exige la
métrica CIU del capítulo 1 del Vol. 4— la API es la única de las dos que
responde.

## B.4. Los tres multiplicadores que explican la factura real

1. **Caché de lectura (aciertos y refrescos).** Se factura al **0,1×** del precio
   base: con Sonnet 5, 0,20 USD por MTok en lugar de 2,00. Es la palanca más
   potente y la más ignorada.
2. **Escritura de caché.** Cuesta más que el precio base: 1,25× la entrada para
   la ventana de 5 minutos y 2× para la de 1 hora. Solo compensa si el prefijo
   se reutiliza muchas veces; un orquestador con un prompt maestro corto y
   estable la aprovecha, uno que cambia en cada llamada, no.
3. **API batch.** Las tareas no urgentes se envían por la vía de lote, a mitad
   de precio. Es lo que permite el lote nocturno del capítulo 5 del Vol. 1:
   clasificar y redactar tickets por la noche no necesita la latencia de la
   respuesta inmediata.

Los descuentos de caché y de lote **se acumulan**, y el orden importa: primero se
escribe la caché y después se envía el lote que la reutiliza.

## B.5. La fórmula

```
coste_ejecucion  = (tokens_entrada / 1e6) * precio_entrada
                 + (tokens_salida  / 1e6) * precio_salida

coste_optimizado = coste_ejecucion * factor_cache * factor_lote

CIU              = coste_total_del_pipeline / funcionalidades_validadas
```

`factor_cache` y `factor_lote` son fracciones entre 0 y 1. Un sistema que
aprovecha la caché de lectura (0,1×) y envía por lote (0,5×) multiplica su
gasto por **0,05**: una reducción de dos órdenes de magnitud sin tocar la
arquitectura. La tercera línea es la que convierte el gasto en una métrica de
ingeniería: el CIU del Vol. 4 se expresa en dólares por funcionalidad que llega
a producción, la única cifra comparable entre proveedores, entre modelos y
entre trimestres.

## B.6. Cómo mantener este apéndice

Este archivo es la única fuente de precios de la serie. El linter
`tools/lint_manuscript.py` comprueba dos cosas:

- **C4**: que todo apéndice citado exista de verdad. Si un capítulo dice «como
  ve el apéndice B» y este archivo falta, la composición falla.
- **C6**: que ningún identificador de modelo aparezca escrito en el cuerpo del
  texto fuera de la lista blanca `tools/model-allowlist.txt`. Los nombres viven
  aquí; en los capítulos se habla de familias («el modelo de gama alta»), no de
  versiones concretas.

Cuando cambien los precios, se edita esta tabla, se actualiza la fecha de corte,
se registra el cambio en `INFORME_EDITORIAL.md` y se revisan los dos capítulos
que la calculan. Es una operación de veinte minutos, y evita que el libro tenga
que reimprimirse.
