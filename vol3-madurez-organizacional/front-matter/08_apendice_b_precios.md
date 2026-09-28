# Apéndice B: precios de referencia y cómo calcular el coste de un pipeline

> **Fecha de corte: 28 de septiembre de 2026.** Los precios de los proveedores de
> modelos cambian varias veces al año. Este apéndice es el único lugar de la
> serie donde se escriben cifras de precio: si el lector encuentra un importe
> distinto en otro capítulo, es un error editorial. Para los valores vigentes,
> consulte la página oficial de precios del proveedor.

## B.1. Por qué este apéndice existe

Dos capítulos remiten a él: el capítulo 5 del Vol. 1, para calcular el coste de
un pipeline de clasificación y redacción, y el capítulo 9 del Vol. 4, para
contar el gasto de una semana de trabajo con un asistente. Ninguno de los dos
puede hacerlo sin una tabla común, y una tabla repetida en dos capítulos
terminaría discrepando en la tercera edición.

El capítulo 3 del Vol. 3 lo menciona como ejemplo de la obsolescencia del
conocimiento: los modelos nombrados aquí tendrán sucesores en meses, y lo que
no caduca son los principios para diseñar, evaluar y controlar.

## B.2. Precios por millón de tokens (USD)

| Modelo | Entrada | Salida | Nota |
|---|---:|---:|---|
| Opus 4.8 | 5,00 | 25,00 | Modelo de máxima capacidad para razonamiento largo |
| Sonnet 4.6 | 3,00 | 15,00 | Equilibrio coste/capacidad; el más usado en producción |
| Haiku 4.5 | 1,00 | 5,00 | Tareas acotadas, clasificación y extracción |

Precios por millón de tokens (MTok), en dólares, tal como constan en la línea 13
del capítulo 9 del Vol. 4. Un pipeline que consume 2 MTok de entrada y 0,5 MTok
de salida con Sonnet 4.6 cuesta `2 × 3,00 + 0,5 × 15,00 = 13,50 USD` por
ejecución; el mismo trabajo con Haiku 4.5 cuesta `2 × 1,00 + 0,5 × 5,00 = 4,50`.

La elección no es solo de precio. Sonnet 4.6 y Opus 4.8 se reservan para tareas
donde un error se paga caro; Haiku 4.5 cubre clasificación, extracción y
filtrado, donde el volumen domina el resultado. Sustituir el modelo de una etapa
sin cambiar su contrato es la operación más barata disponible.

## B.3. Suscripciones frente a API

| Modalidad | Precio | Adecuada para |
|---|---:|---|
| Claude Pro | 20 USD/mes | Trabajo diario sin desglose de gasto |
| API por token | según B.2 | Procesos automatizados y coste por etapa |

La suscripción ofrece un techo mensual conocido y un desglose desconocido. Cuando
hace falta saber cuánto costó cada llamada —que es exactamente lo que exige la
métrica CIU del capítulo 1 del Vol. 4— la API es la única de las dos que
responde.

## B.4. Factores que multiplican el precio base

Cuatro multiplicadores explican por qué la factura real supera la estimación:

1. **Longitud de salida.** La salida se factura más cara que la entrada en
   todos los modelos de la tabla. Un agente que repite el contexto en cada paso
   multiplica la entrada, no la salida.
2. **Caché de lectura.** Los prefijos de sistema repetidos entre llamadas
   admiten caché y se cobran a precio reducido. Un orquestador con un prompt
   maestro estable debe diseñar para aprovecharlo.
3. **API batch.** Las tareas no urgentes se envían por la vía de lote, a mitad
   de precio. Es la palanca del capítulo 5 del Vol. 1: clasificar y redactar
   tickets por la noche no necesita la latencia de la respuesta inmediata.
4. **Reintentos.** Un circuit breaker mal calibrado reintenta llamadas que ya
   estaban condenadas a fallar.

## B.5. La fórmula

```
coste_ejecución = (tokens_entrada / 1e6) × precio_entrada
                + (tokens_salida  / 1e6) × precio_salida

coste_mensual   = coste_ejecución × ejecuciones_al_mes

coste_real      = coste_mensual × factor_cache × factor_lote

CIU             = coste_total_del_pipeline / funcionalidades_validadas
```

`factor_cache` y `factor_lote` son fracciones entre 0 y 1 que reducen el gasto
cuando el prefijo de sistema se sirve desde caché o cuando la tarea se envía por
la vía de lote; valen 1 cuando no se aplica ninguna optimización. La cuarta línea
es la que convierte el gasto en una métrica de ingeniería: el CIU del Vol. 4 se
expresa en dólares por funcionalidad que llega a producción, que es la única
cifra comparable entre proveedores, entre modelos y entre trimestres.

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
