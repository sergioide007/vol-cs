# Capítulo 1: Ética y alineación en producción

## El problema de la alineación a escala

Un agente que toma buenas decisiones en el 99 % de los casos pero falla catastróficamente en el 1 % restante no es un sistema de producción seguro si ese 1 % implica transferencias financieras incorrectas, datos médicos comprometidos o código de seguridad defectuoso. La estadística agrava la intuición: un sistema que ejecuta mil acciones diarias con un 1 % de fallo grave produce diez incidentes graves al día. En consecuencia, la escala convierte los casos límite en rutina.

La **alineación**, asegurar que los objetivos efectivos del sistema coinciden con los de sus operadores humanos, es el desafío central de la era agéntica, y su formulación técnica es anterior a los LLMs: Amodei et al. (2016) catalogaron los problemas concretos (efectos secundarios negativos, *reward hacking*, supervisión escalable, exploración segura, robustez al cambio de distribución) que hoy reaparecen, uno a uno, en los agentes de producción. Un agente que aprende a pasar los evals sin resolver la tarea está haciendo *reward hacking* de manual; un agente que funciona en staging y falla en producción sufre el cambio de distribución de siempre.

La respuesta de la industria combina cuatro capas, ninguna suficiente por sí sola:

1. **Alineación en el entrenamiento.** Las técnicas que convirtieron modelos de lenguaje en asistentes utilizables: el ajuste por retroalimentación humana (RLHF; [Ouyang et al., 2022](#ref-ouyang2022); [Bai et al., 2022b](#ref-bai2022)) y la **IA constitucional**, donde el modelo se entrena para criticarse y corregirse contra un conjunto explícito de principios (una constitución) reduciendo la dependencia de la supervisión humana caso a caso ([Bai et al., 2022a](#ref-bai2022a)). Esta capa la aporta el proveedor del modelo; el AI Engineer la hereda, no la controla.
2. **Diseño constitucional del sistema.** La versión operativa de lo anterior, que sí está en manos del ingeniero: definir explícitamente qué puede y qué no puede hacer cada agente, permisos, herramientas, presupuestos, invariantes de dominio (capítulos 6 y 14).
3. **Supervisión humana en decisiones de alto impacto.** Automatizar la propuesta, exigir aprobación humana para la ejecución irreversible.
4. **Monitoreo de deriva.** Los modelos cambian: el proveedor los actualiza, el contexto evoluciona, los usuarios encuentran caminos nuevos. El comportamiento correcto de ayer no garantiza el de mañana; la suite de evals (capítulo 13) corriendo continuamente es el detector.

**► PISTA TÉCNICA: Supervisión humana para acciones críticas**

```python
# Ejemplo 1.1: Human-in-the-loop para acciones irreversibles.
# El agente propone; el humano aprueba; el sistema registra todo.

import time
from datetime import datetime

import anthropic

client = anthropic.Anthropic()

ACCIONES_CRITICAS = {
    "eliminar_base_de_datos",
    "desplegar_a_produccion",
    "modificar_permisos_usuarios",
    "cancelar_contratos",
    "enviar_comunicacion_masiva",
}

def ejecutar_con_guardia_humana(accion: str, parametros: dict,
                                agente_id: str) -> dict:
    """
    Para acciones irreversibles o de alto impacto, solicita aprobación
    humana antes de ejecutar. La lista de acciones críticas es política
    de la organización, vive en configuración versionada, y NINGÚN
    agente puede modificarla.
    """
    if accion in ACCIONES_CRITICAS:
        # Descripción legible de la acción propuesta (modelo económico)
        descripcion = client.messages.create(
            model="claude-haiku-4-5",
            max_tokens=200,
            messages=[{
                "role": "user",
                "content": (
                    "Describe en 2 oraciones qué hará esta acción y su "
                    f"impacto: {accion}({parametros})"
                ),
            }],
        )
        descripcion_texto = next(
            b.text for b in descripcion.content if b.type == "text"
        )

        solicitud_id = f"approval-{agente_id}-{int(time.time())}"
        approval_queue.push({
            "id": solicitud_id,
            "accion": accion,
            "parametros": parametros,
            "agente": agente_id,
            "descripcion_legible": descripcion_texto,
            "timestamp": datetime.now().isoformat(),
            "estado": "PENDIENTE_APROBACION",
        })
        return {
            "estado": "ESPERANDO_APROBACION",
            "solicitud_id": solicitud_id,
            "mensaje": (
                f"Acción '{accion}' requiere aprobación humana. "
                f"ID: {solicitud_id}"
            ),
        }

    # Acciones no críticas se ejecutan directamente (con auditoría)
    return ejecutar_accion(accion, parametros)
```

El detalle de gobierno que el código no muestra: la cola de aprobaciones necesita un acuerdo de nivel de servicio. Si las aprobaciones tardan días, los equipos encontrarán formas de rodear el control, y el control que se rodea es peor que ninguno, porque da seguridad falsa. Aprobar debe ser fácil; solo ejecutar sin aprobar debe ser imposible.

## El contexto regulatorio: de virtud a obligación

Lo que este libro ha presentado como buena ingeniería (trazabilidad, supervisión humana, gestión de riesgos, documentación) está dejando de ser opcional. El **Reglamento de Inteligencia Artificial de la Unión Europea** ([Unión Europea, 2024](#ref-aiact2024)), primer marco integral del mundo, clasifica los sistemas por riesgo e impone a los de alto riesgo obligaciones de gestión de riesgos, gobernanza de datos, documentación técnica, registro de eventos, transparencia y vigilancia humana, con aplicación escalonada desde 2025 y sanciones proporcionales a la facturación global. En Estados Unidos, el **AI Risk Management Framework** del NIST (2023) ofrece el estándar voluntario de referencia, organizado en cuatro funciones (gobernar, mapear, medir, gestionar) que encajan una a una con las prácticas de este libro. Para el lector latinoamericano: varios países de la región tienen proyectos legislativos inspirados en el modelo europeo; construir hoy con esos estándares es asegurar el producto contra el marco que viene.

La lectura estratégica: **el costo de cumplir es marginal para quien ya construyó con disciplina, y es un rediseño completo para quien no**. La auditoría del capítulo 14, los evals del capítulo 13 y el gateway del capítulo 3 son, además de buena ingeniería, la infraestructura de cumplimiento.

## La dimensión ambiental

La honestidad intelectual obliga a incluir un costo que no aparece en la factura de la API: el energético. El entrenamiento de modelos grandes tiene una huella de carbono sustancial y medible ([Strubell et al., 2019](#ref-strubell2019); [Patterson et al., 2021](#ref-patterson2021)), y aunque la inferencia individual es órdenes de magnitud más barata, la inferencia *a escala de industria* domina ya el costo energético total del ciclo de vida de los modelos. Las palancas del AI Engineer son las mismas del capítulo 11 (el modelo adecuado a la tarea, caché, lotes, menos iteraciones desperdiciadas): la eficiencia económica y la ambiental, afortunadamente, apuntan en la misma dirección.

**■ PISTA EJECUTIVA**

La ética agéntica, en la práctica directiva, se reduce a tres preguntas con dueño:

1. **¿Quién responde por la acción del agente?** La respuesta legal y organizacional es siempre: una persona. Los agentes no tienen responsabilidad; la delegan hacia arriba. Cada agente en producción necesita un propietario humano nombrado, como cada servicio necesita un *on-call*.
2. **¿Qué decisiones nunca se delegan?** La lista de acciones de aprobación obligatoria es una decisión de directorio, no de sprint.
3. **¿Cómo sabemos que sigue alineado?** Deriva de comportamiento, evals continuos, auditoría muestreada. Además, «funcionaba cuando lo lanzamos» no es una respuesta; es la primera línea del informe del incidente.

---

## Sesgo algorítmico y equidad distribucional

La dimensión del sesgo en sistemas agénticos permanece, en la práctica, sistemáticamente subgobernada en relación con su consecuencia operativa y legal, brecha que deviene litigiosa tan pronto el sistema opera a escala poblacional. Diecinueve fuentes distintas de sesgo a lo largo del pipeline de aprendizaje automático fueron catalogadas por Mehrabi et al. (2021) en el estudio más exhaustivo del campo hasta la fecha, y su taxonomía se mapea con perturbadora precisión sobre la arquitectura multi-etapa descrita en este libro: el modelo base hereda los sesgos incrustados en los corpus de preentrenamiento; la generación aumentada por recuperación (RAG) amplifica los sesgos de la colección documental indexada, un RAG de información sanitaria entrenado predominantemente sobre literatura clínica anglosajona occidental es, estructuralmente, un amplificador de disparidades en salud; el juez evaluador (capítulo 13) puede reproducir los sesgos del agente que evalúa si ambos derivan de la misma familia de modelos; y la propia especificación de tarea puede activar preferencias latentes del modelo que ninguna auditoría de prompts revelaría sin pruebas estratificadas por subgrupos demográficos.

Conviene enfatizar (y la literatura empírica es categórica en este punto) que no existe un criterio de equidad universalmente correcto. La equidad individual (entradas similares producen salidas similares para individuos similares), la equidad de grupo en sus múltiples formulaciones (paridad demográfica, igualdad de *odds*, calibración intragrupal) y la equidad contrafáctica (los resultados serían idénticos en mundos donde los atributos protegidos difieren) optimizan valores distintos y parcialmente incompatibles entre sí. Como demostrara Chouldechova (2017) en el contexto de herramientas de predicción de reincidencia, y como formalizaran los teoremas de imposibilidad de Kleinberg et al. (2016) en términos generales, satisfacer simultáneamente más de uno de estos criterios resulta demostrablemente imposible cuando las tasas base difieren entre grupos. En consecuencia, la elección del criterio no es una decisión técnica delegable a un ingeniero individual: es una declaración de valores que porta peso ético, exposición legal y la firma organizacional de quien la adoptó, de forma explícita o por omisión estructural.

Para los sistemas clasificados como de alto riesgo bajo la Ley de IA de la UE ([Unión Europea, 2024](#ref-aiact2024)) (y, con mayor amplitud, para todo agente cuya salida afecte materialmente el acceso de individuos a empleo, crédito, servicios sanitarios, vivienda o servicios esenciales) un **protocolo de auditoría de sesgo** es simultáneamente una obligación regulatoria y una práctica de ingeniería defensiva. Su contenido mínimo: (a) declaración explícita del criterio de equidad adoptado, con justificación documentada de por qué ese criterio resulta apropiado para ese caso de uso concreto; (b) conjunto de evaluación estratificado construido para garantizar representación estadísticamente adecuada de los subgrupos protegidos, requisito que no puede satisfacerse mediante la partición del conjunto de prueba estándar, que típicamente infrarrrepresenta a las minorías por construcción; (c) medición del criterio seleccionado en *cada* actualización del modelo, cambio de prompt y revisión del contexto de dominio que llegue a producción, dado que las propiedades de equidad no se transfieren automáticamente entre versiones del modelo ni siquiera del mismo proveedor; y (d) reconocimiento documentado del sesgo residual y el razonamiento organizacional para su aceptación, puesto que la equidad perfecta es teóricamente inalcanzable y la ausencia de documentación constituye, en varias jurisdicciones, una exposición legal independiente.

**► PISTA TÉCNICA: Auditoría de sesgo estratificada, criterio de igualdad de odds**

```python
# Ejemplo 1.2: Evaluación de equidad estratificada — criterio equalized odds.
# Ejecutar en cada actualización del modelo y en cada cambio sustantivo de prompt.
# «Equalized odds» exige emparejar tanto FPR como FNR entre grupos;
# otros criterios (paridad demográfica, calibración) difieren algorítmicamente.
# Documente la elección: el código impone lo que la política organizacional declara.

from dataclasses import dataclass
from typing import Dict, List

@dataclass
class MedicionGrupo:
    grupo: str
    n: int
    tasa_aprobacion: float
    fpr: float   # tasa de falsos positivos: P(ŷ=1 | y=0, grupo)
    fnr: float   # tasa de falsos negativos: P(ŷ=0 | y=1, grupo)

class AuditorEquidad:
    """
    Auditoría equalized-odds para decisiones agénticas que afectan grupos protegidos.
    Umbral de despliegue: disparidad de FPR o FNR > 5 pp activa revisión humana
    obligatoria antes del despliegue, con independencia de la precisión agregada.
    Este umbral es decisión de política organizacional, no parámetro del modelo.
    """

    UMBRAL_DESPLIEGUE = 0.05  # brecha de 5 puntos porcentuales activa revisión

    def auditar(self, casos_por_grupo: Dict[str, List[dict]]) -> Dict:
        """
        Args:
            casos_por_grupo: {etiqueta_grupo: [{"prediccion": bool, "verdad": bool}]}
        Returns: informe de auditoría con métricas por grupo y puerta de despliegue.
        """
        mediciones: List[MedicionGrupo] = []

        for grupo, casos in casos_por_grupo.items():
            vp = sum(1 for c in casos if c["prediccion"] and c["verdad"])
            fp = sum(1 for c in casos if c["prediccion"] and not c["verdad"])
            fn = sum(1 for c in casos if not c["prediccion"] and c["verdad"])
            vn = sum(1 for c in casos if not c["prediccion"] and not c["verdad"])

            mediciones.append(MedicionGrupo(
                grupo=grupo,
                n=len(casos),
                tasa_aprobacion=(vp + vn) / len(casos) if casos else 0.0,
                fpr=fp / (fp + vn) if (fp + vn) > 0 else 0.0,
                fnr=fn / (fn + vp) if (fn + vp) > 0 else 0.0,
            ))

        brecha_fpr = max(m.fpr for m in mediciones) - min(m.fpr for m in mediciones)
        brecha_fnr = max(m.fnr for m in mediciones) - min(m.fnr for m in mediciones)
        puerta_ok = brecha_fpr <= self.UMBRAL_DESPLIEGUE and brecha_fnr <= self.UMBRAL_DESPLIEGUE

        return {
            "criterio": "equalized_odds",
            "justificacion_criterio": "[DOCUMENTAR: especifique por qué este criterio aplica aquí]",
            "por_grupo": [
                {"grupo": m.grupo, "n": m.n,
                 "tasa_aprobacion": round(m.tasa_aprobacion, 3),
                 "fpr": round(m.fpr, 3),
                 "fnr": round(m.fnr, 3)}
                for m in mediciones
            ],
            "max_disparidad_fpr": round(brecha_fpr, 3),
            "max_disparidad_fnr": round(brecha_fnr, 3),
            "puerta_despliegue_superada": puerta_ok,
            "accion_si_bloqueado": "revision_humana_obligatoria_antes_del_despliegue",
            "documentacion_requerida": True,  # Siempre: ningún sistema desplegado está libre de sesgo.
        }
```

**■ PISTA EJECUTIVA: El sesgo como categoría de riesgo estratégico**

Tres categorías de exposición distintas se materializan cuando el sesgo en un agente de producción pasa desapercibido hasta que un tercero externo lo descubre, encuadre que merece escrutinio, porque el descubrimiento externo es siempre la trayectoria de los sistemas no auditados. **Exposición legal** bajo la doctrina del impacto dispar, aplicable a las leyes de empleo, vivienda y crédito en múltiples jurisdicciones, complementada por las obligaciones del artículo 9 (gestión de riesgos) y el artículo 10 (gobernanza de datos) de la Ley de IA de la UE para sistemas de alto riesgo, con multas de hasta 30 millones de euros o el 6 % de la facturación anual global. **Exposición reputacional**: el sesgo algorítmico documentado genera cobertura mediática y atención regulatoria sostenidas que ningún presupuesto de comunicaciones recupera con rapidez, y que tiende a aflorar en momentos de estrés operativo, precisamente cuando la organización dispone de menor capacidad de respuesta. **Exposición operativa**: un agente sesgado optimiza el objetivo incorrecto a escala, y su corrección exige no solo un ajuste del modelo sino una auditoría retroactiva de todas las decisiones tomadas durante el período sesgado, un alcance que crece linealmente con el tiempo y logarítmicamente con el retraso en la detección. La auditoría estratificada descrita arriba cuesta céntimos por ejecución en la API batch y horas de analista por trimestre. Cada una de las tres categorías anteriores cuesta órdenes de magnitud más. La estructura de costos es inequívoca; la única variable es el momento en que se asume.

---

## Transparencia, explicabilidad y derecho a la impugnación

La explicabilidad en el aprendizaje automático ha madurado hasta constituir una subdisciplina bien estructurada, cuyos conceptos, taxonomías y problemas abiertos fueron cartografiados de forma exhaustiva por Arrieta et al. (2020) en un artículo de referencia del campo, distinguiendo la interpretabilidad intrínseca (el modelo es comprensible por diseño: árboles de decisión, modelos lineales, reglas explícitas) de la explicabilidad post-hoc (el modelo es una caja negra; se aplican mecanismos de atribución separados tras la predicción: LIME, SHAP, explicaciones contrafácticas). El contexto agéntico, sin embargo, desplaza sustancialmente el desafío: la unidad de explicación es ahora una trayectoria multi-etapa de razonamiento, selección de herramientas, recuperación de datos externos y decisiones intermedias (cualquiera de las cuales puede haber influido decisivamente en el resultado final), ya no una única salida del modelo. Ese desplazamiento porta consecuencia regulatoria directa, porque ni el derecho a la explicación del artículo 86 de la Ley de IA de la UE ni el derecho a revisión humana del artículo 22 del RGPD eximen a las arquitecturas multi-etapa complejas; la obligación escala con el impacto de la decisión, no con la simplicidad del sistema.

La respuesta estructural disponible en un sistema agéntico bien instrumentado es la traza distribuida (capítulo 18). Una traza producida por un bucle ReAct correctamente atribuido contiene, en cada nodo de procesamiento: el identificador de versión del prompt del sistema; los documentos recuperados con sus puntuaciones de relevancia y marcas de tiempo; el razonamiento del modelo en cadena de pensamiento (cuando el modo de reflexión está habilitado); la selección de herramienta, su entrada y su resultado; y la lógica de transición que conduce al paso siguiente. Ese registro constituye, operativamente, una explicación de la trayectoria decisional: no de las matrices de pesos internas del modelo (que permanecen opacas), sino del proceso de decisión, que es precisamente el nivel de transparencia que los marcos regulatorios exigen y que los individuos afectados pueden impugnar con sentido. En consecuencia, la infraestructura de explicabilidad no es una capacidad separada que construir desde cero: es la infraestructura de observabilidad del capítulo 18, leída bajo un objetivo regulatorio distinto.

Dos brechas técnicas permanecen abiertas que la práctica honesta debe reconocer. **La atribución de contexto** (determinar qué fragmento de un contexto largo y multi-componente (el prompt del sistema, el primer documento recuperado, un turno previo de conversación) influyó más en una salida concreta del modelo) es un problema de investigación activo; los métodos de atribución por perturbación y los de desenrollado de atención presentan modos de fallo documentados en contextos largos y conversaciones multi-turno ([Jain & Wallace, 2019](#ref-jainwallace2019)), y el campo de la interpretabilidad agéntica se encuentra en estadio inicial ([Conmy et al., 2023](#ref-conmy2023); [Elhage et al., 2021](#ref-elhage2021)). **Los contrafácticos de trayectoria** (reconstruir qué habría decidido el agente si una entrada intermedia específica hubiera diferido) son tratables para clasificadores simples e intratables en la práctica para pipelines multi-etapa estocásticos en el momento de escritura. La postura práctica del ingeniero en el ínterin es maximizar la trazabilidad por construcción, minimizar la opacidad en el tratamiento de datos, y construir la vía de impugnación como proceso organizacional: un propietario humano nombrado (capítulos 14 y 19) que pueda revisar la traza y trasladarla en lenguaje llano al individuo afectado. La arquitectura que este libro construye no aguarda a que la investigación en interpretabilidad madure; proporciona la trazabilidad estructural que hace posible la impugnación ahora.

---

## El panorama regulatorio global: construir una sola vez para el estándar más exigente

La geografía regulatoria de la inteligencia artificial atravesó una transición estructural en el período 2023-2026, desplazándose de directrices voluntarias a obligaciones vinculantes con sanciones económicas sustanciales y, en determinadas jurisdicciones, remisión penal. Comprender esa transición no es un ejercicio de cumplimiento delegable al departamento jurídico: es una restricción de diseño de producto que determina qué decisiones arquitectónicas son reversibles y cuáles no.

Tres capas de gobernanza requieren atención operativa de la dirección de ingeniería. A nivel **internacional**, la norma ISO/IEC 42001:2023 (el primer estándar formal de sistema de gestión para la inteligencia artificial) impone un ciclo planificar-hacer-verificar-actuar estructuralmente idéntico al de ISO 9001 (calidad) e ISO 27001 (seguridad de la información): identificación de riesgos, controles de tratamiento documentados, auditoría interna y revisión por la dirección. Su adopción sigue siendo formalmente voluntaria, pero es exigida de manera creciente en los contratos de aprovisionamiento empresarial y en los procesos de diligencia debida de la cadena de suministro; un equipo que ya opera un sistema de gestión integrado puede extenderlo al cumplimiento en IA con un esfuerzo incremental considerablemente menor que uno que parte de cero.

A nivel **supranacional**, la Ley de IA de la UE (Reglamento 2024/1689) establece el estándar vinculante más exigente para las organizaciones que operan en mercados europeos o desarrollan sistemas utilizados en ellos. Su árbol de clasificación de riesgos genera tres nodos decisionales para el ingeniero: prácticas **prohibidas** (manipulación subliminal, puntuación social de ciudadanos, identificación biométrica remota en tiempo real en espacios públicos), que no requieren deliberación, siendo la infracción objeto de remisión penal y multas de hasta 35 millones de euros o el 7 % de la facturación anual global; sistemas de **alto riesgo** (IA en selección de personal, evaluación crediticia, suscripción de seguros, evaluación educativa, servicios esenciales, aplicación de la ley, gestión de infraestructuras críticas), que activan el paquete completo de cumplimiento: evaluación de conformidad, documentación técnica, registro de eventos, divulgaciones de transparencia, supervisión humana e inscripción en la base de datos de la UE; y sistemas de **riesgo limitado y mínimo**: sujetos únicamente a las obligaciones de transparencia del artículo 52. Para la mayoría de las herramientas internas de desarrollo, la clasificación es limitada o mínima; para los productos que inciden en cualquiera de los dominios de alto riesgo en mercados de estados miembros de la UE, las obligaciones se aplican desde agosto de 2026.

En **Estados Unidos**, el mosaico sectorial persiste. Las directrices de la FTC sobre prácticas comerciales habilitadas por IA, la asistencia técnica de la EEOC sobre el uso de procedimientos automatizados de selección por parte de empleadores, la guía de gestión de riesgo de modelos SR 11-7 de la OCC (aplicable a modelos de IA en banca) y el marco en evolución de la FDA para el *Software as a Medical Device* habilitado por IA imponen obligaciones específicas de dominio que se superponen al Marco de Gestión de Riesgos de IA del NIST 1.0 (2023, con Perfil de IA Generativa en 2024). El ciclo Gobernar-Mapear-Medir-Gestionar del NIST RMF ofrece la capa de integración federal más coherente, y sus cuatro funciones se corresponden con notable precisión con las prácticas de este libro: Gobernar equivale al registro de agentes, la política de acciones críticas y la gobernanza del presupuesto del capítulo 3; Mapear equivale al modelo de amenazas del capítulo 14; Medir equivale a la suite de evals y el CIU de los capítulos 11 y 13; Gestionar equivale al bucle de MLOps del capítulo 18 y al plan de respuesta a incidentes implícito en el log de auditoría del capítulo 14.

La síntesis que la práctica de ingeniería debe interiorizar: **construir una sola vez para las obligaciones de alto riesgo de la Ley de IA de la UE**: trazabilidad completa, supervisión humana de las decisiones irreversibles, auditoría de sesgo documentada, explicaciones impugnables y propietario humano nombrado por cada agente en producción. Esa arquitectura satisface el NIST RMF, la ISO 42001 y todos los marcos sectoriales vigentes en el momento de escritura, dado que estos marcos son subconjuntos propios de las obligaciones europeas en su carga de cumplimiento. La vía inversa (construir para el estándar mínimo aplicable y actualizar cuando la expansión hacia dominios regulados o mercados europeos requiera cumplimiento) reproduce en la capa de gobernanza la misma dinámica económica que la deuda técnica del capítulo 11: coste diferido, agravado y liquidado en el momento de mayor presión operativa y reputacional.

## Lo esencial del capítulo 1

- A escala, los casos límite se convierten en rutina: un 1 % de fallo grave sobre mil acciones diarias produce diez incidentes graves al día.
- Los problemas de alineación tenían nombre antes de los LLMs: *reward hacking*, supervisión escalable, cambio de distribución (Amodei et al., 2016). La IA constitucional y el RLHF abordan la capa del modelo; las capas del sistema y del humano siguen siendo responsabilidad del ingeniero (Bai et al., 2022a, 2022b; [Ouyang et al., 2022](#ref-ouyang2022)).
- Cuatro capas de alineación, ninguna suficiente por sí sola: alineación del modelo en el entrenamiento, diseño constitucional del sistema, supervisión humana de lo irreversible, y monitoreo continuo de la deriva mediante la suite de evals.
- El sesgo algorítmico opera en cada capa del pipeline agéntico, corpus de preentrenamiento, índice de recuperación, modelo juez, especificación de tarea. No existe un criterio de equidad universalmente correcto; la elección es una declaración de valores con peso legal ([Mehrabi et al., 2021](#ref-mehrabi2021); [Chouldechova, 2017](#ref-chouldechova2017)). La auditoría estratificada en cada actualización del modelo constituye la práctica mínima defendible.
- La explicabilidad para agentes multi-etapa se logra a través de la traza, no de los pesos: las trazas bien instrumentadas (capítulo 18) satisfacen el derecho regulatorio a la explicación sin aguardar a que la investigación en interpretabilidad madure ([Arrieta et al., 2020](#ref-arrieta2020); [Conmy et al., 2023](#ref-conmy2023)).
- Tres capas de gobernanza requieren atención operativa: ISO/IEC 42001:2023 (internacional, voluntaria pero exigida contractualmente), Ley de IA UE 2024/1689 (supranacional, vinculante desde agosto de 2026 para alto riesgo) y NIST AI RMF (federal estadounidense, voluntario pero estructuralmente completo).
- Construir una sola vez para el estándar más exigente: las obligaciones de alto riesgo de la Ley de IA de la UE (trazabilidad, supervisión humana, auditoría de sesgo, explicaciones impugnables, propietario nombrado por agente) satisfacen por derivación estructural todos los marcos menores.
- Un control que se elude es peor que ninguno. Aprobar debe ser sin fricciones; ejecutar sin aprobación, arquitectónicamente imposible.

---
