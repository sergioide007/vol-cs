#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Detector de clichés de IA y escritura tipo Wikipedia (solo prosa).
Uso: python3 tools/skill_cliches.py [--reporte archivo]
Protege: bloques de código cercados, líneas de tabla (|), sangrías de código,
y código en línea (`...`). NO modifica nada: solo reporta.
"""
import re, sys, pathlib

PATRONES = {
    "AI": [
        r"no es solo[^.]{0,60}es que",
        r"en la era (digital|ag[eé]tica|de la IA|de los agentes)",
        r"ha llegado para quedarse",
        r"cabe destacar que",
        r"es importante destacar que",
        r"es fundamental (entender|comprender|recordar|señalar)",
        r"en [úu]ltima instancia,",
        r"no cabe duda de que",
        r"revolucion(a|ario|ar|ario)",
        r"potenciar",
        r"desbloquear",
        r"empoderar",
        r"jugar un papel (clave|fundamental|importante)",
        r"desempe[ñn]a un papel (clave|fundamental|importante|destacado)",
        r"Imagina (esto|que|un escenario)",
        r"[¿?]Alguna vez te has preguntado",
        r"Hablemos de",
        r"Es hora de",
        r"El futuro (es|lleg[oó]|pertenace|pertenece)",
        r"panorama actual",
        r"mundo (actual|de hoy|moderno|en el que vivimos)",
        r"a medida que (la IA|los agentes|la tecnolog[íi]a|avanza)",
        r"la clave est[áa] en",
        r"m[áa]s all[áa] de (lo )?(obvio|aparente)",
        r"en resumen,",
        r"en definitiva,",
        r"cambio de juego",
        r"game.changer",
        r"[Rr][áa]pida?mente y (de manera )?escalab",
        r"robusto y escalable",
        r"innovador(a|as|o|os)?\b",
        r"de vanguardia",
        r"sin precedentes",
        r"un mundo cada vez m[áa]s",
        r"abr[aá] camino para",
        r"estamos (viviendo|frente a|ante) (un|una)",
        r"es importante (notar|recordar|señalar|mencionar|tener en cuenta)",
        r"es (imprescindible|indispensable) (notar|recordar|señalar|mencionar)",
        r"nunca (olvidemos|dejemos de)",
        r"recuerda que",
        r"no (te )?preocupes",
        r"(sumérjete|adéntrate|adentrate) en",
        r"aprovecha (el poder|la potencia|el potencial)",
        r"el poder de (la|los|el) (IA|inteligencia artificial)",
        r"impulsad[oa]s? por (la|el) (IA|inteligencia artificial)",
        r"en (este|el) (punto|momento) es (importante|fundamental|clave)",
        r"para (concluir|cerrar)( esta| este)?",
        r"esperamos que (este|hayas|vaya)",
        r"vamos a (ver|analizar|examinar|explorar|mirar)",
        r"¡(vamos|listos|prepárate| prepárate|atentos)!",
        r"definir el panorama",
        r"elevar (el listón|la vara)",
        r"pioner[oa]|pionero",
        r"sin (duda|ninguna duda)",
        r"es inevitable (no|ignorar|omitir|dejar de lado)",
        r"no (podemos|puede) (dejar de|ignorar)",
        r"cada vez m[aá]s (inteligente|potente|sofisticad[oa])",
        r"la (nueva|revolucionaria) (era|generación) de",
        r"en (resumen|síntesis|sumario)",
        r"para (resumir|concluir)",
        r"a modo de (resumen|síntesis|conclusión)",
        r"la (clave|respuesta) (es|está)",
        r"no (se trata|va) de .{0,40}sino (de )?",
        r"¿(te has preguntado|cuál es|sabes qué|alguna vez)",
        r"imagine (un|una) (escenario|mundo|caso)",
        r"hagamos un ejercicio",
        r"(practiquemos|veamos|miremos|exploremos)",
        r"(demos|hagamos) un paso",
        r"antes de empezar",
        r"al final del (capítulo|libro|texto|volumen)",
        r"comenzaremos (por|con)",
        r"el viaje",

    ],
    "WIKI": [
        r"se caracteriza por",
        r"se define como",
        r"constituye un[a]?",
        r"comprende un[a]?",
        r"denominad[oa] tambi[ée]n",
        r"tambi[ée]n conocid[oa] como",
        r"no obstante,",
        r"en este sentido,",
        r"dicho lo cual,",
        r"a continuaci[óo]n se (presenta|muestra|describe|detalla)",
        r"se muestra en la (figura|tabla)",
        r"v[ée]ase tambi[ée]n",
        r"es un (concepto|t[ée]rmino|enfoque|marco) que",
        r"se trata de un",
        r"a saber,",
        r"por consiguiente,",
        r"en consecuencia,",
        r"asimismo,",
        r"cabe se[ñn]alar que",
        r"como se (ha|puede) (mencionado|observado|se[ñn]alado|visto)",
        r"anteriormente",
        r"ulteriormente",
        r"dicho/a/ello anteriormente",
        r"se refiere a",
        r"se suele (utilizar|usar|considerar|llamar)",
        r"por lo general,",
        r"en la mayor[ií]a de los casos",
        r"puede considerarse",
        r"de acuerdo con",
        r"a lo largo de (este|el|la)",
        r"en relaci[óo]n con",
        r"en este (trabajo|documento|texto|cap[ií]tulo)",
        r"el objetivo de (este|el) (cap[ií]tulo|trabajo|documento)",
        r"cabe mencionar",
        r"es de ([áa]mbito|inter[ée]s|relevancia)",
        r"amplia (aplicabilidad|utilidad)",
        r"multifac[eé]tico",
        r"se procede a",
        r"se analiza",
        r"se describe",
        r"se expone",
        r"ello es,",
        r"dado que",
        r"dada la (importancia|complejidad)",
        r"debido a que",
        r"en efecto,",
        r"cuya (naturaleza|complejidad) (es|de)",
    ],
    "EMOJI": [
        r"[\U0001F300-\U0001FAFF\u2600-\u27BF\uFE0F]",
    ],
}

PROSA_EXCL = ("```", "~~~")


def lineas_de_prosa(texto):
    """Yield (número_de_línea, línea) solo de prosa (sin código ni tablas)."""
    en_fence = False
    for i, linea in enumerate(texto.splitlines(), 1):
        s = linea.lstrip()
        if s.startswith(PROSA_EXCL):
            en_fence = not en_fence
            continue
        if en_fence:
            continue
        if s.startswith("|"):          # tabla
            continue
        if linea.startswith(("    ", "\t")):  # bloque de código sangrado
            continue
        limpia = re.sub(r"`[^`]*`", "", linea)  # código en línea
        yield i, limpia


def escanear(ruta: pathlib.Path):
    hits = []
    texto = ruta.read_text(encoding="utf-8")
    for i, linea in lineas_de_prosa(texto):
        for cat, pats in PATRONES.items():
            for p in pats:
                for m in re.finditer(p, linea, re.I):
                    hits.append((str(ruta), i, cat, p, m.group(0),
                                 " ".join(linea.split())[:160]))
    return hits


def main():
    raiz = pathlib.Path(__file__).resolve().parent.parent
    salidas = []
    for globo in ("vol*/manuscrito/capitulos/*.md",
                  "vol*/front-matter/*.md",
                  "vol*/estado-del-arte/*.md",
                  "vol*/referencias/*.md"):
        salidas += sorted(raiz.glob(globo))
    total = []
    for f in salidas:
        total += escanear(f)
    # resumen por patrón
    detalle = "--detall" in sys.argv
    por_patron = {}
    for ruta, i, cat, p, m, linea in total:
        por_patron.setdefault((cat, p), []).append((ruta, i, m, linea))
    out = []
    for (cat, p), hs in sorted(por_patron.items(), key=lambda x: -len(x[1])):
        out.append(f"[{cat}] {len(hs):4d}  {p}")
        ver = hs if detalle else hs[:3]
        for ruta, i, m, linea in ver:
            out.append(f"          {ruta}:{i}  «{m}»")
            if detalle:
                out.append(f"                      {linea}")
    out.append(f"TOTAL_HITS {len(total)}")
    texto = "\n".join(out) + "\n"
    if "--reporte" in sys.argv:
        pathlib.Path(sys.argv[sys.argv.index("--reporte") + 1]).write_text(
            texto, encoding="utf-8")
    print(texto, end="")
    return 0

if __name__ == "__main__":
    sys.exit(main())
