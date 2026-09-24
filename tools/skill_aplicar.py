#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Aplica el skill anti-cliches-ia: sustituciones curadas una a una.

Reglas duras:
  * solo prosa; nunca tablas (|), codigo cercado/sangrado, formulas ni citas
  * cada patron original debe aparecer EXACTAMENTE una vez
  * modo --check: no escribe, solo informa
"""
import argparse
import pathlib
import re
import sys

RAIZ = pathlib.Path(__file__).resolve().parent.parent

# (archivo, original, nuevo)
MAPA = [
    # --- Vol 1 -------------------------------------------------------------
    ("vol1-fundamentos/estado-del-arte/estado-del-arte.md",
     "**Esta es una discrepancia real que vale la pena señalar**:",
     "**Esta es una discrepancia real**:"),
    ("vol1-fundamentos/manuscrito/capitulos/02_capitulo_2.md",
     "esto separa lo que vale la pena adoptar hoy de lo que vale la pena solo vigilar",
     "esto separa lo que conviene adoptar hoy de lo que conviene solo vigilar"),

    # --- Vol 2 -------------------------------------------------------------
    ("vol2-frontera-y-aplicaciones/manuscrito/capitulos/06_capitulo_6.md",
     "Merece énfasis particular un error conceptual que se desliza con facilidad "
     "en la adopción de agentes: confundir la extensión del pensamiento con su sustitución.",
     "Un error conceptual se desliza con facilidad en la adopción de agentes: "
     "confundir la extensión del pensamiento con su sustitución."),
    ("vol2-frontera-y-aplicaciones/manuscrito/capitulos/07_capitulo_7.md",
     "Existe una creencia extendida y, en última instancia, costosa:",
     "Existe una creencia extendida y costosa:"),

    ("vol2-frontera-y-aplicaciones/manuscrito/capitulos/12_capitulo_12.md",
     "Merece énfasis que la decisión de dónde va cada agente es **arquitectónica, no accidental**.",
     "La decisión de dónde va cada agente es **arquitectónica, no accidental**."),
    ("vol2-frontera-y-aplicaciones/manuscrito/capitulos/13_capitulo_13.md",
     "En la era de los agentes, este dilema no se ha resuelto; se ha **intensificado**.",
     "En los sistemas con agentes, este dilema no se ha resuelto; se ha **intensificado**."),
    ("vol2-frontera-y-aplicaciones/manuscrito/capitulos/13_capitulo_13.md",
     "Robert C. Martin lo formuló con una claridad que conviene recordar:",
     "Robert C. Martin lo formuló con precisión:"),
    ("vol2-frontera-y-aplicaciones/manuscrito/capitulos/17_capitulo_17.md",
     "Merece énfasis que China posee una ventaja estructural en datos",
     "China posee una ventaja estructural en datos"),
    ("vol2-frontera-y-aplicaciones/manuscrito/capitulos/18_capitulo_18.md",
     "La inversión que sustenta todo esto es de magnitud sin precedentes:",
     "La inversión que sustenta todo esto es de magnitud extraordinaria:"),
    ("vol2-frontera-y-aplicaciones/manuscrito/capitulos/17_capitulo_17.md",
     "La última pregunta merece énfasis especial:",
     "La última pregunta es la decisiva:"),
    ("vol2-frontera-y-aplicaciones/manuscrito/capitulos/18_capitulo_18.md",
     "Merece énfasis que existe una tensión real, aunque no fatal, en el ecosistema "
     "americano de IA agéntica.",
     "Existe una tensión real, aunque no fatal, en el ecosistema americano de IA agéntica."),
    ("vol2-frontera-y-aplicaciones/manuscrito/capitulos/19_capitulo_19.md",
     "Merece énfasis que la intersección entre GDPR (Reglamento 2016/679) y AI Act crea "
     "un espacio técnico que Europa domina por necesidad",
     "La intersección entre GDPR (Reglamento 2016/679) y AI Act crea un espacio técnico "
     "que Europa domina por necesidad"),
    ("vol2-frontera-y-aplicaciones/manuscrito/capitulos/21_capitulo_21.md",
     "Merece énfasis que Australia fue uno de los primeros países",
     "Australia fue uno de los primeros países"),
    ("vol2-frontera-y-aplicaciones/manuscrito/capitulos/22_capitulo_22.md",
     "Conviene señalar que el relato dominante sobre Rusia en inteligencia artificial "
     "oscila entre dos polos igualmente distorsionados",
     "El relato dominante sobre Rusia en inteligencia artificial oscila entre dos polos "
     "igualmente distorsionados"),
    ("vol2-frontera-y-aplicaciones/manuscrito/capitulos/22_capitulo_22.md",
     "Merece énfasis que estos números no son comparables directamente",
     "Estos números no son comparables directamente"),
    ("vol2-frontera-y-aplicaciones/manuscrito/capitulos/23_capitulo_23.md",
     "No obstante, conviene señalar que el ecosistema taiwanese no se limita al hardware.",
     "No obstante, el ecosistema taiwanese no se limita al hardware."),
    ("vol2-frontera-y-aplicaciones/manuscrito/capitulos/25_capitulo_25.md",
     "Cabe precisar la arquitectura: no es centralizada.",
     "La arquitectura no es centralizada."),
    ("vol2-frontera-y-aplicaciones/manuscrito/capitulos/26_capitulo_26.md",
     "Merece énfasis una divergencia fundamental en estrategia de innovación.",
     "Hay una divergencia fundamental en estrategia de innovación."),
    ("vol2-frontera-y-aplicaciones/manuscrito/capitulos/32_capitulo_32.md",
     "Merece énfasis que la validación de agentes móviles requiere un enfoque distinto "
     "al testing de APIs convencionales.",
     "La validación de agentes móviles requiere un enfoque distinto al testing de APIs "
     "convencionales."),
    ("vol2-frontera-y-aplicaciones/manuscrito/capitulos/32_capitulo_32.md",
     "No obstante, merece énfasis que el ROI no es automático:",
     "No obstante, el ROI no es automático:"),
    ("vol2-frontera-y-aplicaciones/manuscrito/capitulos/32_capitulo_32.md",
     "Merece énfasis particular el riesgo que distingue a VR de todos los demás dominios:",
     "El riesgo que distingue a VR de todos los demás dominios es particular:"),

    # --- Vol 3 -------------------------------------------------------------
    ("vol3-madurez-organizacional/manuscrito/capitulos/01_capitulo_1.md",
     "Conviene enfatizar (y la literatura empírica es categórica en este punto) que "
     "no existe un criterio de equidad universalmente correcto.",
     "No existe un criterio de equidad universalmente correcto; la literatura empírica "
     "es categórica en este punto."),
    ("vol3-madurez-organizacional/manuscrito/capitulos/09_capitulo_9.md",
     "Merece énfasis un argumento que con frecuencia se omite en las discusiones sobre IA:",
     "Las discusiones sobre IA suelen omitir un argumento:"),
    ("vol3-madurez-organizacional/manuscrito/capitulos/20_capitulo_20.md",
     "Cabe precisar que este ciclo comprende cinco fases que deben implementarse "
     "explícitamente en la infraestructura:",
     "El ciclo comprende cinco fases que deben implementarse explícitamente "
     "en la infraestructura:"),
    ("vol3-madurez-organizacional/manuscrito/capitulos/21_capitulo_21.md",
     "Importa destacar que esta transformación del rol tiene implicaciones directas "
     "para la evaluación del rendimiento.",
     "Esta transformación del rol tiene implicaciones directas para la evaluación "
     "del rendimiento."),

    # --- Vol 4 -------------------------------------------------------------
    ("vol4-patrones-de-escala/estado-del-arte/estado-del-arte.md",
     "una distinción de capas que vale la pena señalar como límite explícito del "
     "alcance de este volumen.",
     "una distinción de capas que delimita el alcance de este volumen."),
    ("vol4-patrones-de-escala/manuscrito/capitulos/02_capitulo_2.md",
     "# Capítulo 2: Estimaciones probabilísticas en la era de la IA",
     "# Capítulo 2: Estimaciones probabilísticas en sistemas agénticos"),
    ("vol4-patrones-de-escala/front-matter/04_tabla_contenido.md",
     "**Capítulo 2: Estimaciones probabilísticas en la era de la IA**",
     "**Capítulo 2: Estimaciones probabilísticas en sistemas agénticos**"),
    ("vol4-patrones-de-escala/manuscrito/capitulos/10_capitulo_10.md",
     "insuficiente para entender por qué RAG fue revolucionario y, al mismo tiempo,",
     "insuficiente para entender por qué RAG llegó a ser el patrón dominante y, "
     "al mismo tiempo,"),
    ("vol4-patrones-de-escala/manuscrito/capitulos/10_capitulo_10.md",
     "Peter Shor desarrolló su algoritmo innovador en 1994",
     "Peter Shor desarrolló su algoritmo en 1994"),
    ("vol4-patrones-de-escala/manuscrito/capitulos/10_capitulo_10.md",
     "diseñar nuevos catalizadores que podrían revolucionar la industria química",
     "diseñar nuevos catalizadores que podrían transformar la industria química"),
    ("vol4-patrones-de-escala/manuscrito/capitulos/10_capitulo_10.md",
     "En síntesis: **NIM es la respuesta a",
     "**NIM es la respuesta a"),
    ("vol4-patrones-de-escala/manuscrito/capitulos/99_epilogo_serie.md",
     "Merece énfasis este hecho: ninguno de esos capítulos fue ornamental.",
     "Ninguno de esos capítulos fue ornamental."),
    ("vol4-patrones-de-escala/manuscrito/capitulos/99_epilogo_serie.md",
     "Cabe destacar que este hecho no es anecdótico; es metodológico.",
     "El hecho no es anecdótico; es metodológico."),
    ("vol4-patrones-de-escala/manuscrito/capitulos/99_epilogo_serie.md",
     "El viaje concluyó donde muchos practitioners lo inician:",
     "El recorrido termina donde muchos profesionales lo empiezan:"),

    # --- Tercera pasada: residuos confirmados en contexto ------------------
    # "recuerda que" como metadiscurso (el resto de la frase ya es directa)
    ("vol4-patrones-de-escala/manuscrito/capitulos/01_capitulo_1.md",
     "esta sección recuerda que bajo esa línea hay una segunda factura",
     "esa línea esconde una segunda factura"),
    # "El viaje completo" como titulo de sección (viaje = cliché de cierre)
    ("vol4-patrones-de-escala/manuscrito/capitulos/99_epilogo_serie.md",
     "## 1. El viaje completo: síntesis por partes",
     "## 1. El recorrido completo: síntesis por partes"),

    # --- Metadiscurso "Nótese que" (2a pasada) ---------------------------
    ("vol1-fundamentos/manuscrito/capitulos/07_capitulo_7.md",
     "Nótese que el skill anterior es la **operacionalización del capítulo 6**:",
     "El skill anterior es la **operacionalización del capítulo 6**:"),
    ("vol2-frontera-y-aplicaciones/manuscrito/capitulos/02_capitulo_2.md",
     "Nótese que el patrón produce valor precisamente porque",
     "El patrón produce valor precisamente porque"),
    ("vol3-madurez-organizacional/manuscrito/capitulos/22_capitulo_22.md",
     "Nótese que el primer MVP a menudo **no contiene agente alguno**:",
     "El primer MVP a menudo **no contiene agente alguno**:"),

    # --- Residuos de segunda pasada --------------------------------------
    ("vol3-madurez-organizacional/manuscrito/capitulos/09_capitulo_9.md",
     "En síntesis, lo que distingue al líder técnico no cambia con la IA:",
     "Lo que distingue al líder técnico no cambia con la IA:"),
    ("vol3-madurez-organizacional/manuscrito/capitulos/11_capitulo_11.md",
     "este dilema se presenta con una velocidad sin precedentes:",
     "este dilema se presenta con una velocidad inédita en este sector:"),
    ("vol4-patrones-de-escala/manuscrito/capitulos/01_capitulo_1.md",
     "No obstante, la honestidad obliga al reverso:",
     "La honestidad obliga, sin embargo, al reverso:"),
    ("vol1-fundamentos/estado-del-arte/estado-del-arte.md",
     "mapeando el panorama actual de aplicaciones",
     "mapeando el estado del arte de las aplicaciones"),
    ("vol4-patrones-de-escala/manuscrito/capitulos/99_epilogo_serie.md",
     "El viaje concluyó donde muchos practitioners lo inician:",
     "El recorrido termina donde muchos profesionales lo empiezan:"),

    # --- Cuarta pasada: "la clave es que" como muletilla -------------------
    ("vol2-frontera-y-aplicaciones/manuscrito/capitulos/12_capitulo_12.md",
     "La clave es que estos ejes son **independientes**:",
     "Estos ejes son **independientes**:"),
    ("vol3-madurez-organizacional/manuscrito/capitulos/16_capitulo_16.md",
     "La clave es que el agente *prepara* los datos; el Scrum Master *facilita* la conversación sobre ellos",
     "El agente *prepara* los datos; el Scrum Master *facilita* la conversación sobre ellos"),
    # "pionera" enHypérbole sobre un paper real -> se deja solo el dato
    ("vol2-frontera-y-aplicaciones/manuscrito/capitulos/19_capitulo_19.md",
     "La arquitectura pionera documentada por Bonawitz et al.",
     "La arquitectura documentada por Bonawitz et al."),
]

FENCE = re.compile(r"^\s*(```|~~~|```)")


def lineas_editables(lineas):
    """True = prosa editable; False = tabla, código cercado o sangrado."""
    flags = []
    dentro = False
    for l in lineas:
        if FENCE.match(l):
            dentro = not dentro
            flags.append(False)
            continue
        protegido = (dentro
                     or l.startswith("|")
                     or l.startswith("    ")
                     or l.startswith("\t"))
        flags.append(not protegido)
    return flags


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true",
                    help="informa sin escribir")
    args = ap.parse_args()

    aplicados = 0
    omitidos = []
    problemas = []
    ya_aplicados = []

    por_archivo = {}
    for arch, orig, nuevo in MAPA:
        por_archivo.setdefault(arch, []).append((orig, nuevo))

    for arch, pares in por_archivo.items():
        ruta = RAIZ / arch
        if not ruta.exists():
            problemas.append(f"archivo inexistente: {arch}")
            continue
        texto = ruta.read_text(encoding="utf-8")
        lineas = texto.splitlines(keepends=True)
        editable = lineas_editables(lineas)
        cambios = False

        for orig, nuevo in pares:
            # el patron debe vivir en una linea de prosa
            candidatas = [i for i, l in enumerate(lineas)
                          if orig in l and editable[i]]
            if len(candidatas) > 1:
                problemas.append(
                    f"{arch}: {len(candidatas)} coincidencias de «{orig[:45]}»")
                continue
            if not candidatas:
                # idempotencia: si la version nueva ya esta, el trabajo esta hecho
                ya = [i for i, l in enumerate(lineas)
                      if nuevo in l and editable[i]]
                if len(ya) == 1:
                    ya_aplicados.append(f"{arch}: {nuevo[:45]}")
                    continue
                omitidos.append(f"{arch}: {orig[:45]}")
                continue
            i = candidatas[0]
            if "`" in lineas[i].split(orig)[0].split("`")[-1]:
                problemas.append(f"{arch}: dentro de codigo en linea")
                continue
            lineas[i] = lineas[i].replace(orig, nuevo, 1)
            cambios = True
            aplicados += 1

        if cambios and not args.check:
            ruta.write_text("".join(lineas), encoding="utf-8")

    modo = "SIMULACION" if args.check else "APLICADO"
    print(f"[{modo}] {aplicados}/{len(MAPA)} sustituciones; "
          f"{len(ya_aplicados)} ya aplicadas; "
          f"{len(omitidos)} sin coincidencia; {len(problemas)} problemas")
    for p in problemas:
        print("  ! " + p)
    for o in omitidos:
        print("  ? " + o)
    if omitidos and not args.check:
        print("ABORTA: el mapa no es reproducible sobre el estado actual.")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())


