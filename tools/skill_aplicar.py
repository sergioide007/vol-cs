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

    # --- Quinta pasada: revisión lingüística integral (anti-clichés IA) ----
    ("vol1-fundamentos/manuscrito/capitulos/04_capitulo_4.md",
     "> **Antes de empezar, este es el capítulo más denso del volumen.**",
     "> **Nota de orientación: este es el capítulo más denso del volumen.**"),
    ("vol1-fundamentos/manuscrito/capitulos/06_capitulo_6.md",
     "Se puede discutir el alcance de esa crítica; no se puede ignorar su consecuencia de ingeniería: **el anclaje (grounding) no es opcional en producción**.",
     "Se puede discutir el alcance de esa crítica; su consecuencia técnica resulta ineludible: **el anclaje (grounding) no es opcional en producción**."),
    ("vol1-fundamentos/manuscrito/capitulos/08_capitulo_8.md",
     "> **Antes de empezar: este es el segundo capítulo más denso del volumen y el que más código concentra**",
     "> **Nota de orientación: este es el segundo capítulo más denso del volumen y el que más código concentra**"),
    ("vol2-frontera-y-aplicaciones/manuscrito/capitulos/02_capitulo_2.md",
     "Importa precisar el mecanismo subyacente. La emergencia conductual",
     "El mecanismo subyacente explica esta brecha: la emergencia conductual"),
    ("vol2-frontera-y-aplicaciones/manuscrito/capitulos/02_capitulo_2.md",
     "hay una cadena de transformaciones que merece ser entendida con precisión, pues gestionarla constituye una competencia organizacional de primer orden.",
     "media una cadena de transformaciones exigente, cuya gestión constituye una competencia organizacional de primer orden."),
    ("vol2-frontera-y-aplicaciones/manuscrito/capitulos/05_capitulo_5.md",
     "En este orden de ideas, la verificabilidad cumple una función estructuralmente análoga a la que la intimidad cumplía en la fórmula original:",
     "Bajo este marco, la verificabilidad cumple una función análoga a la de la intimidad en la fórmula original:"),
    ("vol2-frontera-y-aplicaciones/manuscrito/capitulos/08_capitulo_8.md",
     "marcan un cambio de paradigma que merece análisis arquitectónico detenido.",
     "plantean una discontinuidad de diseño que exige análisis arquitectónico."),
    ("vol2-frontera-y-aplicaciones/manuscrito/capitulos/09_capitulo_9.md",
     "Lo que el autor reivindica en este capítulo es que **la era agéntica no deroga esta regla, sino que la amplifica en proporción al número de agentes en el enjambre**.",
     "**La era agéntica no deroga esta regla, sino que la amplifica en proporción al número de agentes en el enjambre**."),
    ("vol2-frontera-y-aplicaciones/manuscrito/capitulos/09_capitulo_9.md",
     "No resulta ocioso señalar que este principio se aplica con igual fuerza a recursos de naturaleza diversa:",
     "Este principio se aplica con igual fuerza a recursos de diversa naturaleza:"),
    ("vol2-frontera-y-aplicaciones/manuscrito/capitulos/10_capitulo_10.md",
     "La propuesta multiagente que se describe en este capítulo intenta responder ese reto con una arquitectura pedagógica",
     "La propuesta multiagente desarrollada aquí aborda ese reto con una arquitectura pedagógica"),
    ("vol2-frontera-y-aplicaciones/manuscrito/capitulos/12_capitulo_12.md",
     "No obstante, lo híbrido tiene un costo que conviene declarar: la **complejidad de las costuras**.",
     "Lo híbrido conlleva, sin embargo, un costo arquitectónico concreto: la **complejidad de las costuras**."),
    ("vol2-frontera-y-aplicaciones/manuscrito/capitulos/13_capitulo_13.md",
     "No obstante, el dilema es en parte falso, y conviene cerrarlo con su superación. Bien entendidas, estructura y funcionalidad no se oponen: la estructura es lo que **permite sostener la velocidad de la funcionalidad** en el tiempo.",
     "El dilema es, sin embargo, en parte falso. Bien entendidas, estructura y funcionalidad no se oponen: la estructura es lo que **permite sostener la velocidad de la funcionalidad** en el tiempo."),
    ("vol2-frontera-y-aplicaciones/manuscrito/capitulos/14_capitulo_14.md",
     "Existe una paradoja que conviene enunciar sin rodeos: el profesional que *solo* estudia IA queda, tarde o temprano, atrapado en ella.",
     "Una paradoja real amenaza al especialista: el profesional que *solo* estudia IA queda, tarde o temprano, atrapado en ella."),
    ("vol2-frontera-y-aplicaciones/manuscrito/capitulos/17_capitulo_17.md",
     'Conviene precisar que la Estrategia Nacional de IA de China (publicada en 2017, revisada en 2023 como *Generative AI Interim Measures*, CACC) no habla explícitamente de "agentes". Habla de "sistemas inteligentes autónomos distribuidos".',
     'La Estrategia Nacional de IA de China (publicada en 2017, revisada en 2023 como *Generative AI Interim Measures*, CACC) no habla explícitamente de "agentes": habla de "sistemas inteligentes autónomos distribuidos".'),
    ("vol2-frontera-y-aplicaciones/manuscrito/capitulos/18_capitulo_18.md",
     "Esta distinción es fundamental para el equipo de QA del enjambre: los tests de comportamiento deben verificar propiedades emergentes del modelo, no solo la presencia de filtros de capa.",
     "Esta distinción rige el trabajo de QA del enjambre: los tests de comportamiento deben verificar propiedades emergentes del modelo, no solo la presencia de filtros de capa."),
    ("vol2-frontera-y-aplicaciones/manuscrito/capitulos/23_capitulo_23.md",
     "Dicho esto, Taiwan no fabrica solo para NVIDIA.",
     "La capacidad de Taiwán no se agota en NVIDIA:"),
    ("vol2-frontera-y-aplicaciones/manuscrito/capitulos/25_capitulo_25.md",
     "**On-Device Learning**: Conviene precisar que Japón mantiene datos de fabricación locales (secreto comercial). Con Ryzen AI en la caja de control, puedes entrenar un *agente predictive maintenance* LSTM directamente en datos de vibración en tiempo real.",
     "**On-Device Learning**: Japón mantiene sus datos de fabricación en entornos locales bajo secreto comercial. Con Ryzen AI en la caja de control, es posible entrenar un *agente predictive maintenance* LSTM directamente con datos de vibración en tiempo real."),
    ("vol2-frontera-y-aplicaciones/manuscrito/capitulos/28_capitulo_28.md",
     'Conviene precisar qué se entiende aquí por "sistema multiagente" antes de aplicar el término al fútbol, porque la conexión no es metafórica: es estructural.',
     'Definir con exactitud qué constituye un «sistema multiagente» es indispensable antes de aplicar el término al fútbol: la conexión no es metafórica, sino estructural.'),
    ("vol3-madurez-organizacional/manuscrito/capitulos/03_capitulo_3.md",
     "Cabe puntualizar que este problema es, en esencia, un problema de orquestación distribuida bajo incertidumbre. Y la orquestación distribuida bajo incertidumbre es, precisamente, el dominio para el que los sistemas multiagente fueron concebidos.",
     "En esencia, este desafío radica en la orquestación distribuida bajo incertidumbre: precisamente el dominio para el que los sistemas multiagente fueron concebidos."),
    ("vol3-madurez-organizacional/manuscrito/capitulos/03_capitulo_3.md",
     "En el plano de la ingeniería de sistemas multi-agente aplicada a la gestión de desastres, la arquitectura propuesta en este capítulo se inscribe",
     "En el plano de la ingeniería de sistemas multi-agente aplicada a la gestión de desastres, la arquitectura expuesta se inscribe"),
    ("vol3-madurez-organizacional/manuscrito/capitulos/09_capitulo_9.md",
     "El glosario operacional que el líder no puede ignorar:",
     "Glosario operacional de referencia para el liderazgo técnico:"),
    ("vol3-madurez-organizacional/manuscrito/capitulos/10_capitulo_10.md",
     "Conviene precisar el matiz crítico: no la elimina, la **desplaza**.",
     "El matiz crítico no radica en eliminarla, sino en **desplazarla**."),
    ("vol3-madurez-organizacional/manuscrito/capitulos/14_capitulo_14.md",
     "Trasladada al dominio de los agentes de IA, la kata adquiere un matiz radicalmente diferente que conviene precisar desde el inicio: **no entrena al agente**: el modelo ya está entrenado; sus pesos no cambian durante la kata, , sino que **revela la arquitectura de su razonamiento bajo restricciones**.",
     "Trasladada al dominio de los agentes de IA, la kata adquiere un sentido radicalmente diferente: **no entrena al agente** (el modelo ya está entrenado y sus pesos no cambian durante la prueba), sino que **revela la arquitectura de su razonamiento bajo restricciones**."),
    ("vol3-madurez-organizacional/manuscrito/capitulos/14_capitulo_14.md",
     "Conviene subrayar el beneficio menos evidente y de mayor impacto de la kata agéntica: no solo evalúa agentes, **educa a los ingenieros y arquitectos que los diseñan**.",
     "El beneficio menos evidente y de mayor impacto de la kata agéntica radica en su valor formativo: más allá de evaluar agentes, **educa a los ingenieros y arquitectos que los diseñan**."),
    ("vol3-madurez-organizacional/manuscrito/capitulos/16_capitulo_16.md",
     "No resulta ocioso señalar que dicha transición hacia los principios no fue arbitraria.",
     "Dicha transición hacia los principios no fue arbitraria."),
    ("vol3-madurez-organizacional/manuscrito/capitulos/18_capitulo_18.md",
     "Las tres preguntas-brújula propuestas en este capítulo pueden interpretarse como un mecanismo de restauración de la racionalidad acotada funcional:",
     "Las tres preguntas-brújula formuladas aquí pueden interpretarse como un mecanismo de restauración de la racionalidad acotada funcional:"),
    ("vol3-madurez-organizacional/manuscrito/capitulos/22_capitulo_22.md",
     'Conviene advertir una trampa específica de esta era. Como los agentes hacen que construir sea barato y rápido (un enjambre funcional puede prototipado en días en lugar de meses), la tentación de saltarse el MVP y "construirlo todo de una vez" es mayor que nunca.',
     'Existe una trampa específica en este contexto: como los agentes abaratan y aceleran el desarrollo (un enjambre funcional puede ser prototipado en días en lugar de meses), la tentación de saltarse el MVP y «construirlo todo de una vez» es mayor que nunca.'),
    ("vol3-madurez-organizacional/manuscrito/capitulos/24_capitulo_24.md",
     "Conviene subrayar una tesis fuerte: SOLID no es solo aplicable a los agentes, es **más necesario** en ellos que en el código tradicional. La razón es la naturaleza probabilística del enjambre.",
     "La tesis central es taxativa: SOLID no solo resulta aplicable a los agentes, sino **más necesario** en ellos que en el código tradicional. La razón estriba en la naturaleza probabilística del enjambre."),
    ("vol4-patrones-de-escala/manuscrito/capitulos/09_capitulo_9.md",
     "> **Una nota sobre costos antes de empezar:** los precios de la API son los del apéndice B, con su fecha de corte.",
     "> **Nota de costos:** los precios de la API son los del apéndice B, con su fecha de corte."),
    ("vol4-patrones-de-escala/manuscrito/capitulos/10_capitulo_10.md",
     "Y luego vienen los sistemas multiagentes, donde ocurre lo verdaderamente disruptivo. No es coordinación programada: es emergencia.",
     "En los sistemas multiagentes opera la emergencia, no la coordinación programada."),
    ("vol4-patrones-de-escala/manuscrito/capitulos/10_capitulo_10.md",
     "Esta infraestructura emergente es crucial: la próxima década demandará ingenieros que entiendan quantum + IA + agentes simultaneamente.",
     "Esta infraestructura formativa resulta estratégica: la próxima década demandará ingenieros con formación combinada en computación cuántica, IA y arquitecturas agénticas."),
    ("vol4-patrones-de-escala/manuscrito/capitulos/13_capitulo_13.md",
     "Este principio es fundamental para el DR híbrido: los agentes edge deben poder continuar operando y recuperar su estado de forma autónoma, sin coordinación cloud, durante el período de partición.",
     "Este principio rige el diseño del DR híbrido: los agentes edge deben poder continuar operando y recuperar su estado de forma autónoma, sin coordinación cloud, durante el período de partición."),
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


