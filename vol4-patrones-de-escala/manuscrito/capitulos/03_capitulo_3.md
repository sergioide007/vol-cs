# Capítulo 3: Testing de sistemas agénticos

## El TDD de la inteligencia artificial

El testing de sistemas basados en LLMs introduce un problema epistemológico nuevo: la salida no es determinista. Dos ejecuciones del mismo agente con la misma entrada pueden producir salidas diferentes, ambas correctas. Los frameworks de testing tradicionales, diseñados para verificar igualdad exacta (`assertEqual`), se rompen en este contexto.

La solución es reemplazar las aserciones exactas por *evaluaciones basadas en criterios*, lo que la comunidad llama **evals**. Un eval define qué propiedades debe tener una salida aceptable y mide, sobre un conjunto de casos, qué fracción de las salidas las cumple. El cambio mental para un ingeniero clásico: deja de preguntarse «¿es igual a lo esperado?» y empieza a preguntarse «¿cumple los criterios, con qué tasa, y esa tasa mejora o empeora con cada cambio?».

La pirámide de testing agéntico tiene tres niveles, del más barato al más caro:

1. **Aserciones deterministas sobre propiedades.** El JSON parsea contra el esquema; el código compila; los tests del código generado pasan; la respuesta no excede N palabras; no contiene credenciales. Todo lo verificable con código se verifica con código: es gratis y no alucina.
2. **LLM-as-judge.** Un modelo evalúa la salida de otro contra criterios explícitos. La validación empírica del patrón es sólida: jueces LLM bien instruidos alcanzan más del 80 % de acuerdo con evaluadores humanos, el mismo nivel de acuerdo que los humanos tienen entre sí ([Zheng et al., 2023](#ref-zheng2023)). Con dos salvedades que el mismo estudio documenta y todo arnés debe mitigar: sesgo de posición (preferir la primera opción presentada; se mitiga evaluando en ambos órdenes) y sesgo de verbosidad (preferir respuestas largas; se mitiga instruyéndolo explícitamente).
3. **Evaluación humana muestreada.** Cara y lenta; se reserva para calibrar periódicamente a los jueces automáticos y para los casos de alto riesgo.

Y una regla transversal tomada de la investigación en evaluación de agentes: **todo eval reporta costo además de calidad** ([Kapoor et al., 2024](#ref-kapoor2024)). Un cambio que sube la tasa de éxito del 88 % al 91 % triplicando los tokens no es una mejora; es una decisión de negocio que alguien debe tomar con los dos números delante.

**► PISTA TÉCNICA: Framework de evaluación con LLM-as-judge**

```python
# Ejemplo 3.1: Eval con criterios + LLM-as-judge, con salida estructurada.
# El juez devuelve JSON validado contra esquema: sin regex, sin sorpresas.

import json
import anthropic

client = anthropic.Anthropic()

JUDGE_SCHEMA = {
    "type": "object",
    "properties": {
        "evaluaciones": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "criterio": {"type": "string"},
                    "score": {"type": "number"},
                    "evidencia": {"type": "string"},
                },
                "required": ["criterio", "score", "evidencia"],
                "additionalProperties": False,
            },
        },
        "score_global": {"type": "number"},
        "veredicto": {"type": "string", "enum": ["PASS", "FAIL"]},
        "razon_principal": {"type": "string"},
    },
    "required": ["evaluaciones", "score_global", "veredicto",
                 "razon_principal"],
    "additionalProperties": False,
}

def eval_con_criterios(
    output_agente: str,
    criterios: list[str],
    umbral_aprobacion: float = 0.7,
) -> dict:
    """
    Evalúa la salida de un agente usando otro LLM como juez.
    Mitigaciones incorporadas: criterios explícitos, evidencia textual
    obligatoria, instrucción anti-verbosidad, salida estructurada.
    """
    criterios_fmt = "\n".join(f"{i+1}. {c}" for i, c in enumerate(criterios))

    juicio = client.messages.create(
        model="claude-opus-4-8",
        max_tokens=2048,
        system="""Eres un evaluador técnico objetivo. Evalúas si un output
        cumple una lista de criterios. Para cada criterio:
        - Asigna un score de 0.0 (no cumple) a 1.0 (cumple perfectamente)
        - Cita la evidencia textual del output que justifica el score
        - Sé estricto: 0.7+ solo si el criterio se cumple claramente
        - NO premies la longitud: una respuesta concisa que cumple el
          criterio puntúa igual o mejor que una larga.""",
        messages=[{
            "role": "user",
            "content": (
                f"OUTPUT A EVALUAR:\n{output_agente}\n\n"
                f"CRITERIOS DE EVALUACIÓN:\n{criterios_fmt}\n\n"
                f"UMBRAL DE APROBACIÓN: {umbral_aprobacion}"
            ),
        }],
        output_config={"format": {"type": "json_schema",
                                  "schema": JUDGE_SCHEMA}},
    )

    resultado = json.loads(
        next(b.text for b in juicio.content if b.type == "text")
    )
    resultado["aprobado"] = resultado["score_global"] >= umbral_aprobacion
    return resultado


# Suite de regresión para el agente de code review del capítulo 5:
def test_code_review_agent():
    codigo_vulnerable = '''
def login(username, password):
    query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
    return db.execute(query)
    '''

    output_agente = run_agent("reviewer",
                              f"Revisa este código:\n{codigo_vulnerable}")

    criterios = [
        "Identifica la vulnerabilidad de SQL injection presente en el código",
        "Menciona que interpolar strings en queries SQL es peligroso",
        "Sugiere prepared statements o queries parametrizadas como solución",
        "Asigna severidad alta o crítica al hallazgo",
        "El reporte es accionable: indica qué cambiar y dónde",
    ]

    resultado = eval_con_criterios(output_agente["output"], criterios,
                                   umbral_aprobacion=0.75)

    assert resultado["aprobado"], (
        f"El agente de code review falló la evaluación.\n"
        f"Score: {resultado['score_global']}\n"
        f"Razón: {resultado['razon_principal']}"
    )
    return resultado
```

### Del eval puntual a la suite de regresión

Un eval aislado es una anécdota; una suite es ingeniería. Las prácticas que separan ambas:

- **Conjunto de casos versionado.** Decenas a cientos de entradas representativas (incluidos los casos difíciles que ya fallaron en producción, que son los más valiosos) en el repositorio, junto al código.
- **Ejecución en CI.** Cada cambio de prompt, modelo o herramienta corre la suite. Cambiar un prompt sin correr los evals es tan profesional como cambiar código sin correr los tests.
- **Métricas con umbrales.** Tasa de éxito, costo medio por caso, latencia p95. La build falla si la calidad cae o el costo se dispara.
- **En lote y a mitad de precio.** Las suites de evals son el caso de uso perfecto de las APIs batch: asíncronas, masivas, con 50 % de descuento.
- **Calibración periódica del juez.** Una muestra mensual evaluada por humanos, comparada con el juez, mantiene la confianza en el sistema ([Zheng et al., 2023](#ref-zheng2023)).

**■ PISTA EJECUTIVA**

La pregunta directiva correcta sobre cualquier sistema agéntico en producción es «**¿cómo sabríamos si empeora?**», no «¿qué tan bueno es?». Sin suite de evals, la respuesta real es «por las quejas de los clientes»: un sistema de monitoreo con un costo reputacional inaceptable. La suite de evals es al sistema agéntico lo que la suite de tests al software clásico: la condición de posibilidad del cambio seguro. Presupuestarla no es opcional; es la diferencia entre operar un sistema y rezarle.

## Ejercicio resuelto 3.1: los criterios del agente de onboarding

**Enunciado.** Escriba los criterios de evaluación para el agente de onboarding del capítulo 5 (responde preguntas de ingenieros nuevos desde documentación interna, con citas). Cubra los tres niveles de la pirámide y señale qué criterio es el más difícil de redactar bien.

**Solución comentada.** **Nivel 1 (determinista):** toda respuesta contiene al menos una cita en formato `[FUENTE n]`; cada `n` citado existe en las fuentes recuperadas; la respuesta no excede 400 palabras; cero credenciales o secretos en el texto. **Nivel 2 (LLM-as-judge):** «cada afirmación técnica está respaldada por la fuente citada» (el juez verifica afirmación por afirmación contra el fragmento); «si las fuentes no contienen la respuesta, el agente lo declara y sugiere a quién preguntar»; «el tono es de mentor, no de manual». **Nivel 3 (humano, muestreado):** ¿la respuesta habría desbloqueado realmente a un ingeniero nuevo? El criterio más difícil es el segundo del nivel 2, el **«no sé» honesto**, porque exige casos de prueba cuya respuesta *no está* en el corpus, y la tentación de medir solo lo que el sistema sabe responder es justo como las suites de evals se vuelven decorativas. Regla práctica derivada: al menos un 20 % del conjunto de casos debe ser irrespondible a propósito, y la métrica de ese subconjunto (tasa de abstención correcta) se reporta por separado.

## Lo esencial del capítulo 3

- La salida no determinista rompe el `assertEqual`: se evalúa con criterios y tasas, no con igualdad exacta.
- Pirámide de tres niveles: aserciones deterministas (gratis), LLM-as-judge (válido y barato, con sesgos conocidos y mitigables; [Zheng et al., 2023](#ref-zheng2023)), humanos muestreados (calibración).
- Todo eval reporta costo junto a calidad ([Kapoor et al., 2024](#ref-kapoor2024)): +3 puntos por 3× tokens es una decisión de negocio, no una mejora.
- La suite vive en el repositorio, corre en CI, falla la build, y se nutre de los fallos reales de producción.
- Cambiar un prompt sin correr los evals es un commit directo a main.

---
