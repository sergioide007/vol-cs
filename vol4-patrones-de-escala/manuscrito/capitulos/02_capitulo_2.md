# Capítulo 2: Estimaciones probabilísticas en sistemas agénticos

## El fin de las horas-persona

La estimación en puntos de historia u horas-persona presupone un modelo de producción aproximadamente lineal: más ingenieros por más tiempo produce más software. Ese modelo fue demolido hace medio siglo («añadir personal a un proyecto retrasado lo retrasa más», la Ley de Brooks, 1975), y resulta doblemente inadecuado para los sistemas agénticos, donde el cuello de botella es la validación, no la escritura de código, y donde la varianza del esfuerzo es estructural.

Proponemos adoptar la **simulación de Monte Carlo** como metodología de estimación, por dos razones:

1. **La incertidumbre en sistemas agénticos es inherente, no corregible.** Un agente puede resolver una tarea en 3 iteraciones o en 30, dependiendo de la ambigüedad del prompt inicial, la calidad del contexto y la complejidad emergente de la integración. Esa varianza no desaparece con la experiencia del equipo: es una propiedad del sistema, como lo es del tráfico de red o de la demanda de un servicio.
2. **Monte Carlo convierte la incertidumbre de enemiga en dato.** En lugar de combatirla con estimaciones falsamente precisas («esto tarda 8 horas»), la cuantifica: «con 85 % de confianza, esto costará menos de X dólares y completará en menos de Y minutos». La dirección puede presupuestar percentiles; no puede presupuestar deseos.

El método es el estándar en las disciplinas que gestionan incertidumbre en serio (finanzas, ingeniería de fiabilidad, gestión de proyectos cuantitativa), y su aplicación al software tiene tradición: la propia ingeniería económica del software nació modelando el costo como función de variables inciertas ([Boehm, 1981](#ref-boehm1981)).

**► PISTA TÉCNICA: Estimador Monte Carlo para pipelines agénticos**

```python
# Ejemplo 2.1: Estimador Monte Carlo para pipelines agénticos.
# Cada tarea se modela con una distribución triangular (mínimo, moda, máximo)
# de tokens, calibrada con datos históricos del CIUTracker (capítulo 11),
# más un factor log-normal de reintentos.

import numpy as np

def estimar_pipeline_agente(
    tareas: list[dict],
    num_simulaciones: int = 10_000,
    percentil_objetivo: int = 85,
    costo_por_token: float = 9e-6,   # USD/token promedio del mix de modelos
    tokens_por_segundo: float = 150,  # velocidad típica de salida
) -> dict:
    """
    Estima costo y tiempo de un pipeline agéntico vía Monte Carlo.

    Args:
        tareas: lista de dicts con 'nombre', 'tokens_min', 'tokens_mode',
                'tokens_max' (calibrar con datos históricos propios).
        num_simulaciones: más simulaciones = más estable la cola.
        percentil_objetivo: 85 = conservador, 50 = neutro.
        costo_por_token: derivar del mix real de modelos del pipeline.
    """
    costos, tiempos = [], []

    for _ in range(num_simulaciones):
        costo_sim, tiempo_sim = 0.0, 0.0
        for tarea in tareas:
            tokens = np.random.triangular(
                left=tarea["tokens_min"],
                mode=tarea["tokens_mode"],
                right=tarea["tokens_max"],
            )
            # Reintentos: log-normal — la mayoría de tareas no reintenta,
            # unas pocas reintentan mucho. La cola pesada es lo realista.
            factor_reintento = np.random.lognormal(mean=0, sigma=0.3)
            tokens_reales = tokens * factor_reintento

            costo_sim += tokens_reales * costo_por_token
            tiempo_sim += tokens_reales / tokens_por_segundo
        costos.append(costo_sim)
        tiempos.append(tiempo_sim / 60)  # minutos

    costos, tiempos = np.array(costos), np.array(tiempos)
    p = percentil_objetivo

    return {
        "costo_usd": {
            "p50": round(float(np.percentile(costos, 50)), 4),
            "p85": round(float(np.percentile(costos, 85)), 4),
            "p95": round(float(np.percentile(costos, 95)), 4),
            "media": round(float(costos.mean()), 4),
            "desviacion": round(float(costos.std()), 4),
        },
        "tiempo_minutos": {
            "p50": round(float(np.percentile(tiempos, 50)), 1),
            "p85": round(float(np.percentile(tiempos, 85)), 1),
            "p95": round(float(np.percentile(tiempos, 95)), 1),
        },
        "recomendacion": {
            "presupuesto_usd": round(float(np.percentile(costos, p)), 4),
            "tiempo_estimado_min": round(float(np.percentile(tiempos, p)), 1),
            "confianza": f"{p}%",
            "interpretacion": (
                f"Con {p}% de confianza, el pipeline costará menos de "
                f"${np.percentile(costos, p):.4f} USD y completará en menos "
                f"de {np.percentile(tiempos, p):.1f} minutos."
            ),
        },
    }


# Ejemplo de uso: pipeline de code review automatizado
pipeline_code_review = [
    {"nombre": "Análisis inicial",      "tokens_min": 500,
     "tokens_mode": 1500, "tokens_max": 4000},
    {"nombre": "Review de seguridad",   "tokens_min": 800,
     "tokens_mode": 2000, "tokens_max": 6000},
    {"nombre": "Review de arquitectura","tokens_min": 1000,
     "tokens_mode": 3000, "tokens_max": 8000},
    {"nombre": "Síntesis final",        "tokens_min": 300,
     "tokens_mode": 1000, "tokens_max": 2500},
]

estimacion = estimar_pipeline_agente(pipeline_code_review,
                                     percentil_objetivo=85)
print(estimacion["recomendacion"]["interpretacion"])
```

### De la estimación a la operación: el bucle completo

El estimador anterior no vale nada con parámetros inventados, y vale oro con parámetros medidos. El bucle de madurez completo une las piezas del libro:

1. El **AIGateway** (capítulo 3) registra tokens y costo de cada llamada real.
2. El **CIUTracker** (capítulo 11) los agrega por funcionalidad y por equipo.
3. Las distribuciones históricas calibran el **estimador Monte Carlo** de este capítulo.
4. Las estimaciones alimentan los **presupuestos** de los bucles agénticos (capítulo 4) y los umbrales de alerta.
5. Las desviaciones entre lo estimado y lo observado refinan las distribuciones, y, cuando son sistemáticas, delatan un cambio de régimen: un modelo nuevo, un contexto que creció, un patrón de orquestación que ya no paga su costo.

**■ PISTA EJECUTIVA**

La conversación que este capítulo cambia es la del comité de planificación. La pregunta «¿cuánto va a costar?» tiene a partir de ahora una respuesta honesta de tres números (p50, p85, p95) en lugar de una cifra única que todos saben falsa. La recomendación operativa: **presupueste al p85 y celebre al p50**. Los equipos que presupuestan a la media viven en sobrecosto crónico la mitad de las veces, no por mala ejecución, sino por aritmética: en distribuciones de cola pesada, la media está muy por debajo de lo que la realidad entrega con frecuencia incómoda. La varianza del trabajo agéntico no es un defecto a esconder: es un dato a gestionar, y las organizaciones que la gestionan toman mejores decisiones de cartera que las que la niegan.

## Ejercicio resuelto 2.1: lea los percentiles como un directivo

**Enunciado.** El estimador devuelve, para un pipeline nuevo: costo p50 = $0,9, p85 = $2,1, p95 = $4,8 por ejecución; volumen esperado: 2.000 ejecuciones/mes. El director pregunta: «¿cuánto presupuesto pido?». Tres analistas responden: A: «$1.800/mes (2.000 × p50)»; B: «$4.200/mes (2.000 × p85)»; C: «$2.200/mes (2.000 × la media simulada, $1,1)». ¿Quién tiene razón y por qué los otros no?

**Solución comentada.** **C** está más cerca, con un matiz que importa. El error de A y B es el mismo: aplicar un percentil *por ejecución* a un *agregado*. El p85 individual no es el p85 del mes: con 2.000 ejecuciones independientes, la ley de los grandes números estrecha la distribución del total alrededor de 2.000 × la **media**, y la media ($1,1) supera al p50 ($0,9) precisamente por la cola pesada de los reintentos. A presupuesta corto de forma sistemática (confunde mediana con media en una distribución asimétrica: el error aritmético del capítulo); B paga un seguro absurdo (el «caso malo» no ocurre 2.000 veces seguidas). La respuesta profesional completa: **2.000 × media + un margen por la incertidumbre del agregado** (simular la suma mensual y tomar su p85, que estará mucho más cerca de la media que el p85 individual) **más** la advertencia de régimen: si el volumen, el modelo o el contexto cambian, las distribuciones se recalibran (paso 5 del bucle de madurez). Los percentiles individuales sirven para otra decisión: presupuestar *una* tarea crítica, fijar timeouts y dimensionar alertas; confundir los dos usos es el error más común al adoptar Monte Carlo.

## Lo esencial del capítulo 2

- La varianza del trabajo agéntico es estructural, no corregible: se cuantifica, no se niega ([Brooks, 1975](#ref-brooks1975); [Boehm, 1981](#ref-boehm1981)).
- Monte Carlo con distribución triangular + factor log-normal de reintentos: simple, calibrable con los datos del gateway.
- Presupueste al p85, celebre al p50, para tareas individuales; para agregados, simule la suma: los percentiles no se multiplican.
- El estimador vale lo que sus parámetros: el bucle gateway → CIU → distribuciones → presupuestos → desviaciones es el sistema completo.
- Las desviaciones sistemáticas no son ruido: delatan un cambio de régimen (modelo nuevo, contexto crecido, patrón que dejó de pagar).

## Preguntas para discusión

1. ¿Qué distribución real tienen las iteraciones por tarea en su equipo? Si no hay datos, ¿qué impide instrumentar el gateway esta semana?
2. ¿Qué decisiones de su organización se toman hoy sobre estimaciones puntuales que deberían tomarse sobre percentiles?
