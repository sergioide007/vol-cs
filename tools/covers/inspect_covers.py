#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Analiza las cubiertas PNG de la serie «Código Sintético».

Motivo: las cubiertas originales (generadas por IA, 1024 x 1536 px) traen el
nombre de un solo autor en la franja inferior. Para acreditar a los dos
coautores hay que borrar esa línea y dibujar la leyenda nueva. Este script mide
la geometría exacta de esa franja para que las constantes que usan
tools/latex/cover-page.tex y tools/covers/make_styles.py no sean inventadas:

  * filas con tinta de la línea de autoría y su extensión horizontal,
  * color de la tinta y color de acento de cada volumen,
  * altura de mayúscula y línea base,
  * franja "quieta" (sin tinta) por encima, que es la que se copia y estira
    para tapar el nombre viejo, junto con su uniformidad (si el fondo es plano,
    el estiramiento no deja costura visible),
  * primera palabra del nombre ("SERGIO"/"Sergio") y su ancho, que es lo que
    permite deducir el espaciado entre letras que traía el arte.
  * reglas laterales (vol. 2), que hay que volver a dibujar porque el parche
    las tapa.

Uso:
  python3 tools/covers/inspect_covers.py            # informe legible
  python3 tools/covers/inspect_covers.py --json     # mismas cifras en JSON
  python3 tools/covers/inspect_covers.py --vol vol1-fundamentos
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
COVER_REL = Path("front-matter") / "01_cubierta_delantera.png"

# Franja inferior que se analiza (por debajo de esta fila ya no hay arte, solo
# fondo: el nombre de autoría vive hacia el final de la cubierta).
BOTTOM_FROM = 1200
INK_DELTA = 24      # distancia mínima al fondo de la fila para contar como tinta
RULE_MIN_LEN = 100  # tramo horizontal de esta longitud = regla, no glifo
WORD_GAP_FACTOR = 1.8   # un hueco > 1,8 x la mediana separa palabras, no letras


def median(values) -> int:
    values = sorted(values)
    return values[len(values) // 2]


def load_rows(path: Path):
    """Devuelve (ancho, alto, filas) con cada fila como bytes RGB.

    Se lee de golpe con tobytes() y se trocea por filas: es mucho más rápido
    que recorrer la imagen píxel a píxel con PixelAccess.
    """
    im = Image.open(path)
    rgb = im.convert("RGB")
    w, h = rgb.size
    raw = rgb.tobytes()
    stride = w * 3
    rows = [raw[y * stride:(y + 1) * stride] for y in range(h)]
    return w, h, rows, im.mode, im.info.get("dpi")


def row_background(row: bytes) -> tuple[int, int, int]:
    """Fondo de la fila = mediana por canal (la tinta ocupa < 50 % del ancho)."""
    return tuple(median(row[c::3]) for c in range(3))


def row_ink(row: bytes, bg: tuple[int, int, int]):
    """(nº de píxeles de tinta, x_min, x_max, color medio de la tinta)."""
    n = 0
    x_min = x_max = None
    acc = [0, 0, 0]
    r0, g0, b0 = bg
    for i in range(0, len(row), 3):
        r, g, b = row[i], row[i + 1], row[i + 2]
        if max(abs(r - r0), abs(g - g0), abs(b - b0)) > INK_DELTA:
            n += 1
            x = i // 3
            if x_min is None:
                x_min = x
            x_max = x
            acc[0] += r
            acc[1] += g
            acc[2] += b
    if not n:
        return 0, None, None, None
    return n, x_min, x_max, tuple(round(c / n) for c in acc)


def runs_from_bools(flags: list[bool], offset: int, merge_gap: int = 0):
    """Agrupa índices True consecutivos -> [[inicio, fin]] en filas reales.

    `merge_gap` une tramos separados por pocas filas: en el volumen 3 el
    descendente de la «g» de «Sergio» queda 1 fila por debajo del cuerpo de
    las letras y, sin unir, se interpretaría como dos bandas distintas.
    """
    runs, start = [], None
    for i, flag in enumerate(flags):
        if flag and start is None:
            start = i
        elif not flag and start is not None:
            runs.append([offset + start, offset + i - 1])
            start = None
    if start is not None:
        runs.append([offset + start, offset + len(flags) - 1])
    merged: list[list[int]] = []
    for run in runs:
        if merged and run[0] - merged[-1][1] - 1 <= merge_gap:
            merged[-1][1] = run[1]
        else:
            merged.append(run)
    return merged


def row_runs(row: bytes, bg, min_len: int = 3):
    """Tramos horizontales de tinta de una fila (para separar texto de reglas)."""
    runs, start = [], None
    width = len(row) // 3
    r0, g0, b0 = bg
    for x in range(width):
        i = x * 3
        r, g, b = row[i], row[i + 1], row[i + 2]
        ink = max(abs(r - r0), abs(g - g0), abs(b - b0)) > INK_DELTA
        if ink and start is None:
            start = x
        elif not ink and start is not None:
            if x - start >= min_len:
                runs.append([start, x - 1])
            start = None
    if start is not None and width - start >= min_len:
        runs.append([start, width - 1])
    return runs


def row_colour_masks(row: bytes, bg, min_dist: int):
    """Itera los píxeles que distan `min_dist` o más del fondo de la fila."""
    r0, g0, b0 = bg
    for i in range(0, len(row), 3):
        r, g, b = row[i], row[i + 1], row[i + 2]
        if max(abs(r - r0), abs(g - g0), abs(b - b0)) >= min_dist:
            yield i // 3, (r, g, b)


def dominant_ink_colour(rows, y0: int, y1: int, min_dist: int = 90):
    """Color más frecuente entre los píxeles de tinta 'llenos' de la banda."""
    counts: dict[tuple[int, int, int], int] = {}
    for row in rows[y0:y1 + 1]:
        bg = row_background(row)
        for _x, p in row_colour_masks(row, bg, min_dist):
            counts[p] = counts.get(p, 0) + 1
    if not counts:
        return (255, 255, 255), 0
    colour = max(counts, key=lambda c: counts[c])
    return colour, counts[colour]


def accent_colour(rows, y0: int, y1: int):
    """Color de acento estimado con el píxel más alejado del fondo en cada fila.

    Es más fiable que el color de moda cuando el trazo es fino o el texto va
    muy espaciado (pocos píxeles superan un umbral alto): en cada fila se toma
    el píxel más alejado del fondo y se combinan por mediana por canal.
    """
    samples = []
    for row in rows[y0:y1 + 1]:
        bg = row_background(row)
        r0, g0, b0 = bg
        best, best_d = None, -1
        for i in range(0, len(row), 3):
            p = (row[i], row[i + 1], row[i + 2])
            d = max(abs(p[0] - r0), abs(p[1] - g0), abs(p[2] - b0))
            if d > best_d:
                best, best_d = p, d
        if best and best_d > 0:
            samples.append(best)
    if not samples:
        return (255, 255, 255), 0
    med = [median([s[c] for s in samples]) for c in range(3)]
    spread = max(max(abs(s[c] - med[c]) for c in range(3)) for s in samples)
    return tuple(med), spread


def rule_clusters(rules: list[dict]) -> list[list[dict]]:
    """Agrupa los tramos largos en reglas.

    Una regla es un trazo fino que ocupa varias filas: filas contiguas (o casi)
    cuyos tramos se solapan horizontalmente. Cada regla del arte sale así como un
    grupo, no como una fila suelta.
    """
    clusters: list[list[dict]] = []
    for r in sorted(rules, key=lambda r: (r["y"], r["x0"])):
        for c in clusters:
            last = c[-1]
            overlap = min(last["x1"], r["x1"]) - max(last["x0"], r["x0"]) + 1
            shortest = min(last["x1"] - last["x0"], r["x1"] - r["x0"]) + 1
            if r["y"] - last["y"] <= 2 and overlap >= 0.5 * shortest:
                c.append(r)
                break
        else:
            clusters.append([r])
    return clusters


def rule_core_colour(rows, cluster: list[dict]):
    """Color de la tinta de una regla: el píxel de núcleo.

    El trazo del arte es fino (≈3 px) y está suavizado: solo la fila central
    tiene cobertura total. La mediana de todas las filas mezclaría los bordes
    translúcidos y devolvería un color más oscuro que la tinta real, así que se
    toma el píxel más alejado del fondo (el centro del trazo), como en
    accent_colour.
    """
    x0 = min(r["x0"] for r in cluster)
    x1 = max(r["x1"] for r in cluster)
    best, best_d = (0, 0, 0), -1
    for r in cluster:
        row = rows[r["y"]]
        r0, g0, b0 = r["bg"]
        for x in range(x0, x1 + 1):
            i = x * 3
            p = (row[i], row[i + 1], row[i + 2])
            d = max(abs(p[0] - r0), abs(p[1] - g0), abs(p[2] - b0))
            if d > best_d:
                best, best_d = p, d
    return best


def first_word(detail: dict, width: int):
    """Primera palabra del nombre de autoría y su ancho de tinta.

    Se proyectan sobre las columnas los tramos de tinta de cuerpo de letra
    (los tramos largos, o sea las reglas laterales del vol. 2, se descartan) y
    se corta en el primer hueco claramente mayor que el espaciado interletra:
    el espacio entre palabras mide ~2-3 veces más que el hueco entre letras.
    """
    cols = [False] * width
    for runs in detail.values():
        for x0, x1 in runs:
            if x1 - x0 < RULE_MIN_LEN:
                for x in range(x0, x1 + 1):
                    cols[x] = True
    groups = runs_from_bools(cols, 0)
    if len(groups) < 2:
        return None
    gaps = [groups[i + 1][0] - groups[i][1] - 1 for i in range(len(groups) - 1)]
    word_gap = WORD_GAP_FACTOR * median(gaps)
    # La primera palabra termina en el primer hueco ancho (espacio entre
    # palabras); los huecos de dentro son los interletras.
    last = len(groups) - 1
    for i, gap in enumerate(gaps):
        if gap > word_gap:
            last = i
            break
    word = [groups[0][0], groups[last][1]]
    return {"x0": word[0], "x1": word[1], "width_px": word[1] - word[0] + 1,
            "letters": last + 1, "groups_total": len(groups),
            "median_gap_px": median(gaps),
            "word_gap_px": min((g for g in gaps if g > word_gap), default=None)}


def analyse(path: Path) -> dict:
    width, height, rows, mode, dpi = load_rows(path)

    band_rows = []
    for y in range(BOTTOM_FROM, height):
        bg = row_background(rows[y])
        n, x0, x1, ink = row_ink(rows[y], bg)
        band_rows.append({"y": y, "bg": bg, "ink": n, "x0": x0, "x1": x1,
                          "ink_colour": ink})

    inked = runs_from_bools([r["ink"] > 0 for r in band_rows], BOTTOM_FROM)
    strong = runs_from_bools([r["ink"] >= 8 for r in band_rows], BOTTOM_FROM,
                             merge_gap=4)
    author = strong[-1] if strong else None
    by_y = {r["y"]: r for r in band_rows}

    quiet = None
    if author:
        y = author[0] - 1
        while y >= BOTTOM_FROM and by_y[y]["ink"] == 0:
            y -= 1
        if y + 1 <= author[0] - 1:
            quiet = (y + 1, author[0] - 1)

    info = {
        "volume": path.parents[1].name,
        "file": str(path),
        "size": [width, height],
        "mode": mode,
        "dpi": dpi,
        "author_band": list(author) if author else None,
        "author_extent": None,
        "author_ink": None,
        "accent": None,
        "first_word": None,
        "author_runs_by_row": None,
        "side_rules": None,
        "glyph_extent": None,
        "quiet_band": list(quiet) if quiet else None,
        "quiet_uniformity": None,
        "max_row_ink": None,
        "baseline_row": None,
        "cap_px": None,
        "ink_runs": [list(r) for r in inked],
        "strong_runs": [list(r) for r in strong],
        "bottom_patch": None,
    }

    if author:
        band = [r for r in band_rows if author[0] <= r["y"] <= author[1]]
        info["author_extent"] = [min(r["x0"] for r in band), max(r["x1"] for r in band)]
        colour, freq = dominant_ink_colour(rows, author[0], author[1])
        info["author_ink"] = {
            "rgb": list(colour),
            "hex": "#%02X%02X%02X" % colour,
            "px": freq,
        }
        acc, spread = accent_colour(rows, author[0], author[1])
        info["accent"] = {
            "rgb": list(acc),
            "hex": "#%02X%02X%02X" % acc,
            "spread": spread,
        }
        rules = []
        glyph_x: list[int] = []
        detail = {}
        for r in band:
            y = r["y"]
            rs = row_runs(rows[y], r["bg"])
            detail[str(y)] = rs
            for x0, x1 in rs:
                if x1 - x0 >= RULE_MIN_LEN:
                    # Color real de la regla: el trazo es fino (≈3 px en el arte),
                    # así que la mediana de la fila mezcla los bordes suavizados y
                    # oscurece el color. Se toma el píxel de núcleo, el más alejado
                    # del fondo de esa fila (el centro del trazo).
                    row = rows[y]
                    rgb = max(((row[x * 3], row[x * 3 + 1], row[x * 3 + 2])
                               for x in range(x0, x1 + 1)),
                              key=lambda p: max(abs(p[k] - r["bg"][k])
                                                for k in range(3)))
                    rules.append({"y": y, "x0": x0, "x1": x1, "rgb": list(rgb),
                                  "hex": "#%02X%02X%02X" % rgb})
                else:
                    glyph_x += [x0, x1]
        info["author_runs_by_row"] = detail
        info["side_rules"] = rules
        if rules:
            # Color único de las reglas: mediana por canal de los núcleos.
            med_rgb = tuple(median([r["rgb"][k] for r in rules]) for k in range(3))
            info["side_rules_ink"] = {"rgb": list(med_rgb),
                                      "hex": "#%02X%02X%02X" % med_rgb}
        else:
            info["side_rules_ink"] = None
        info["glyph_extent"] = [min(glyph_x), max(glyph_x)] if glyph_x else None
        info["first_word"] = first_word(detail, width)

        # Altura de mayúscula y línea base: la línea base es la última fila con
        # tinta "de cuerpo" (los descendentes —la «g» de «Sergio» en el vol. 3—
        # tienen muchas menos muestras que el resto de la banda).
        counts = [r["ink"] for r in band]
        max_ink = max(counts) if counts else 0
        rows_over = [r["y"] for r in band if r["ink"] >= max_ink * 0.25]
        baseline = max(rows_over) if rows_over else author[1]
        info["max_row_ink"] = max_ink
        info["baseline_row"] = baseline
        info["cap_px"] = baseline - author[0] + 1

    if quiet:
        q0, q1 = quiet
        means = [sum(by_y[y]["bg"]) / 3.0 for y in range(q0, q1 + 1)]
        info["quiet_uniformity"] = {
            "rows": q1 - q0 + 1,
            "mean_brightness": round(sum(means) / len(means), 2),
            "spread": round(max(means) - min(means), 2),
        }
        patch_rows = height - q0
        source_rows = q1 - q0 + 1
        info["bottom_patch"] = {
            "patch_top": q0,
            "patch_rows": patch_rows,
            "source_rows": source_rows,
            "stretch": round(patch_rows / source_rows, 3),
        }
    return info


def report(data: dict) -> str:
    out = [f"### {data['volume']}"]
    out.append(f"- archivo: `{data['file']}`")
    out.append(f"- tamaño: {data['size'][0]} × {data['size'][1]} px · modo {data['mode']} · "
               f"dpi declarados: {data['dpi'] or 'ninguno'} · "
               f"resolución real a 6×9 in: {data['size'][0] / 6:.0f} ppi")
    out.append(f"- bandas con tinta en la franja inferior (y ≥ {BOTTOM_FROM}): "
               f"{data['strong_runs']}")
    if data["author_band"]:
        g = data["glyph_extent"]
        width_px = (g[1] - g[0] + 1) if g else 0
        out.append(f"- línea de autoría: filas {data['author_band']} · "
                   f"ancho del texto x {g} ({width_px} px) · "
                   f"tinta {data['author_ink']['hex']} "
                   f"({data['author_ink']['px']} px de núcleo) · "
                   f"acento {data['accent']['hex']}")
        if data["side_rules"]:
            ys = sorted({r["y"] for r in data["side_rules"]})
            left = [r for r in data["side_rules"] if r["x0"] < 512]
            right = [r for r in data["side_rules"] if r["x0"] >= 512]
            fmt = lambda rs: f"x {min(r['x0'] for r in rs)}–{max(r['x1'] for r in rs)}"
            out.append(f"- reglas laterales: filas {ys[0]}–{ys[-1]} · "
                       f"izquierda {fmt(left) if left else '—'} · "
                       f"derecha {fmt(right) if right else '—'} · "
                       f"color {data['side_rules_ink']['hex']} "
                       f"(núcleos de {len(data['side_rules'])} filas)")
        out.append(f"- altura de mayúscula: {data['cap_px']} px · línea base fila "
                   f"{data['baseline_row']} (banda hasta {data['author_band'][1]})")
        fw = data.get("first_word")
        if fw:
            out.append(f"- primera palabra: x {fw['x0']}–{fw['x1']} "
                       f"({fw['width_px']} px, {fw['letters']} letras) · "
                       f"hueco mediano entre letras {fw['median_gap_px']} px · "
                       f"grupos totales {fw['groups_total']} → "
                       f"ancho/mayúscula = {fw['width_px'] / data['cap_px']:.3f}")
    u, p = data["quiet_uniformity"], data["bottom_patch"]
    if u:
        out.append(f"- franja quieta encima: filas {data['quiet_band']} · {u['rows']} filas · "
                   f"brillo medio {u['mean_brightness']} · variación vertical "
                   f"{u['spread']}/255 ({u['spread'] / 255 * 100:.1f} %)")
        out.append(f"- parche inferior: tapa desde y={p['patch_top']} hasta el borde "
                   f"({p['patch_rows']} filas) copiando {p['source_rows']} filas "
                   f"→ estiramiento ×{p['stretch']}")
    out.append("")
    return "\n".join(out)


def main() -> int:
    ap = argparse.ArgumentParser(description="Analiza las cubiertas PNG de la serie.")
    ap.add_argument("--json", action="store_true", help="salida JSON")
    ap.add_argument("--vol", nargs="*", help="volúmenes a analizar (por defecto, todos)")
    args = ap.parse_args()

    dirs = args.vol or sorted(
        d.name for d in (ROOT / "content" / "es").iterdir() if d.is_dir() and d.name.startswith("vol")
    )
    data = []
    for name in dirs:
        cover = ROOT / "content" / "es" / name.split("-")[0] / COVER_REL
        if not cover.is_file():
            print(f"! sin cubierta: {cover}", file=sys.stderr)
            continue
        data.append(analyse(cover))

    if args.json:
        print(json.dumps(data, indent=2, ensure_ascii=False))
    else:
        print("\n".join(report(d) for d in data))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
