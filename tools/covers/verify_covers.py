#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifica las cubiertas compuestas: mide el PDF ya generado.

No confía en los cálculos de tools/covers/make_styles.py: rasteriza la cubierta
a 300 ppp y comprueba sobre los píxeles reales que

  1. la página mide 6x9 pulg. (432 x 648 bp);
  2. el nombre de un solo autor del arte ya no está (no queda tinta en la zona
     del parche fuera de la leyenda nueva);
  3. la leyenda de los dos coautores está centrada, con la altura de mayúscula
     y el ancho previstos, dentro del área segura de KDP/Lulu (>= 0,25 pulg. de
     margen) y con el color de acento del volumen;
  4. el parche no deja costura visible (la fila anterior al parche y su primera
     fila tienen casi el mismo color);
  5. en el volumen 2 se ven las reglas laterales con su color.

Uso:
  python3 tools/covers/verify_covers.py --dir /ruta/a/cubiertas  # <vol>.pdf
  python3 tools/covers/verify_covers.py                          # dist/....pdf
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from inspect_covers import (ROOT, accent_colour, load_rows, median,  # noqa: E402
                            row_background, row_ink, row_runs,
                            runs_from_bools)

STYLES = json.loads((Path(__file__).resolve().parent / "cover-styles.json")
                    .read_text(encoding="utf-8"))["volumenes"]
DPI = 300
PX_PER_BP = DPI / 72.0
PAGE_W_BP, PAGE_H_BP = 432.0, 648.0
SAFE_MARGIN_BP = 18.0        # 0,25 pulg., mínimo de KDP y Lulu
INK_MIN_PX = 8               # píxeles de tinta por fila para contar como texto
RULE_RUN_MIN_BP = 12.0       # un tramo más largo que esto es regla, no letra
TOL_BP = 1.2                 # tolerancia de medidas tipográficas (bp)
TOL_COLOUR = 26              # tolerancia por canal de color
SEAM_TOL = 4.0               # diferencia de brillo admisible en la costura


def render_page(pdf: Path, work: Path, page: int = 1) -> Path:
    """Rasteriza una página del PDF a 300 ppp."""
    out = work / "page"
    subprocess.run(["pdftoppm", "-r", str(DPI), "-png", "-singlefile",
                    "-f", str(page), "-l", str(page), str(pdf), str(out)],
                   check=True)
    return out.with_suffix(".png")


def page_size_bp(pdf: Path) -> tuple[float, float]:
    txt = subprocess.run(["pdfinfo", str(pdf)], capture_output=True,
                         text=True, check=True).stdout
    for line in txt.splitlines():
        if line.startswith("Page size:"):
            nums = [float(t) for t in line.split()
                    if t.replace(".", "", 1).isdigit()]
            if len(nums) >= 2:
                return nums[0], nums[1]
    return 0.0, 0.0


def median_colour(rows, y: int, x0: int, x1: int, bg) -> tuple[int, int, int]:
    """Color mediano de los píxeles de tinta de un tramo de la fila."""
    row = rows[y]
    r0, g0, b0 = bg
    px = []
    for x in range(x0, x1 + 1):
        i = x * 3
        p = (row[i], row[i + 1], row[i + 2])
        if max(abs(p[0] - r0), abs(p[1] - g0), abs(p[2] - b0)) > 24:
            px.append(p)
    if not px:
        return (0, 0, 0)
    return tuple(median([p[c] for p in px]) for c in range(3))


def check_volume(slug: str, pdf: Path, work: Path) -> list[tuple[str, bool, str]]:
    """Comprueba una cubierta y devuelve [(nombre, ok, detalle)]."""
    st = STYLES[slug]
    png = render_page(pdf, work)
    w, h, rows, _mode, _dpi = load_rows(png)
    results: list[tuple[str, bool, str]] = []

    def check(name: str, ok: bool, detail: str = "") -> None:
        results.append((name, ok, detail))

    # 1) tamaño de página
    pw, ph = page_size_bp(pdf)
    check("página 432×648 bp",
          abs(pw - PAGE_W_BP) < 0.5 and abs(ph - PAGE_H_BP) < 0.5,
          f"{pw:g} × {ph:g} bp")

    # 2) filas de referencia (todo en píxeles de la página a 300 ppp)
    patch_top = int(round((h - 1) - st["patch_height_bp"] * PX_PER_BP))
    patch_top = max(0, min(h - 1, patch_top))
    baseline_row = int(round((h - 1) - st["baseline_bp"] * PX_PER_BP))

    inked = []
    for y in range(patch_top, h):
        bg = row_background(rows[y])
        n, x0, x1, _ = row_ink(rows[y], bg)
        inked.append((y, n, x0, x1, bg))

    strong = runs_from_bools([r[1] >= INK_MIN_PX for r in inked], patch_top,
                             merge_gap=4)
    band = strong[-1] if strong else None
    check("leyenda presente en la franja inferior", band is not None,
          f"filas {band}" if band else "sin tinta")

    if not band:
        return results

    by_y = {r[0]: r for r in inked}
    band_rows = [y for y in range(band[0], band[1] + 1) if by_y[y][1] > 0]

    # 3) extensión de la leyenda, distinguiendo glifos de reglas: un tramo de
    #    más de 12 bp no es una letra, es una regla lateral.
    glyph_x: list[int] = []
    rule_runs: dict[int, list[tuple[int, int]]] = {}
    for y in band_rows:
        rs = row_runs(rows[y], by_y[y][4])
        for x0, x1 in rs:
            if (x1 - x0 + 1) / PX_PER_BP >= RULE_RUN_MIN_BP:
                rule_runs.setdefault(y, []).append((x0, x1))
            else:
                glyph_x += [x0, x1]
    if not glyph_x:
        check("glifos de la leyenda", False, "no se detectan letras")
        return results
    x_min, x_max = min(glyph_x), max(glyph_x)

    cap_px = baseline_row - band[0] + 1
    cap_bp = cap_px / PX_PER_BP
    cap_expected = st["cap_bp"] * st["scale"]
    check("altura de mayúscula", abs(cap_bp - cap_expected) <= TOL_BP,
          f"medida {cap_bp:.2f} bp · prevista {cap_expected:.2f} bp")

    width_bp = (x_max - x_min + 1) / PX_PER_BP
    check("ancho de la leyenda",
          abs(width_bp - st["legend_width_bp"]) <= TOL_BP * 2,
          f"medido {width_bp:.2f} bp · previsto {st['legend_width_bp']:.2f} bp")

    off_bp = ((x_min + x_max + 1) / 2.0 - w / 2.0) / PX_PER_BP
    check("leyenda centrada", abs(off_bp) <= 1.5, f"desvío {off_bp:+.2f} bp")

    # La línea completa (leyenda + reglas + aire) debe caber en el área segura.
    line_x0 = min([x_min] + [a for rs in rule_runs.values() for a, _ in rs])
    line_x1 = max([x_max] + [b for rs in rule_runs.values() for _, b in rs])
    left_bp = line_x0 / PX_PER_BP
    right_bp = (w - 1 - line_x1) / PX_PER_BP
    check(f"dentro del área segura (≥ {SAFE_MARGIN_BP:g} bp)",
          left_bp >= SAFE_MARGIN_BP and right_bp >= SAFE_MARGIN_BP,
          f"márgenes {left_bp:.1f} / {right_bp:.1f} bp")

    # 4) colores (núcleo de los glifos: el píxel más alejado del fondo por fila)
    rgb, spread = accent_colour(rows, band[0], band[1])
    want = st["ink_rgb"]
    check("color de acento",
          all(abs(rgb[c] - want[c]) <= TOL_COLOUR for c in range(3)),
          f"#{rgb[0]:02X}{rgb[1]:02X}{rgb[2]:02X} vs {st['ink']}")

    # 5) el nombre viejo no debe quedar: fuera de la leyenda (y de las reglas)
    #    la franja del parche tiene que estar limpia. Se exige el mismo mínimo
    #    de píxeles que para detectar texto, para no contar el degradado, y se
    #    salta la fila del borde (mezcla arte/parche; en el vol. 2 cae sobre la
    #    regla de la propia ilustración).
    stray = [y for y, n, _x0, _x1, _bg in inked
             if n >= INK_MIN_PX and y > patch_top + 1
             and not (band[0] - 6 <= y <= band[1] + 8)]
    check("sin restos del nombre anterior", not stray,
          f"{len(stray)} filas con tinta fuera de la leyenda"
          + (f" (p. ej. {stray[:6]})" if stray else ""))

    # 6) el parche tiene que ser continuo: ningún salto brusco de brillo entre
    #    filas consecutivas (un resto del nombre viejo o un borde de costura
    #    daría un salto grande).
    jumps = []
    prev = None
    for y in range(patch_top + 1, h):
        if band[0] - 6 <= y <= band[1] + 8:
            prev = None
            continue
        mean = sum(row_background(rows[y])) / 3.0
        if prev is not None:
            jumps.append(abs(mean - prev))
        prev = mean
    check("parche sin saltos de brillo", max(jumps) <= SEAM_TOL,
          f"salto máximo {max(jumps):.2f}/255 (≤ {SEAM_TOL:g})")

    # 7) reglas laterales (volumen 2)
    if st["rules"]:
        check("reglas laterales dibujadas", len(rule_runs) >= 2,
              f"{len(rule_runs)} filas con regla")
        if rule_runs:
            y = sorted(rule_runs)[len(rule_runs) // 2]
            x0, x1 = max(rule_runs[y], key=lambda r: r[1] - r[0])
            len_bp = (x1 - x0 + 1) / PX_PER_BP
            check("longitud de las reglas",
                  abs(len_bp - st["rule_len_bp"]) <= TOL_BP * 2,
                  f"medida {len_bp:.2f} bp · prevista {st['rule_len_bp']:.2f} bp")
            mid = (x0 + x1) // 2
            rgb = median_colour(rows, y, mid - 3, mid + 3, row_background(rows[y]))
            want = [int(st["rules_ink"].lstrip("#")[i:i + 2], 16) for i in (0, 2, 4)]
            check("color de las reglas",
                  all(abs(rgb[c] - want[c]) <= TOL_COLOUR for c in range(3)),
                  f"#{rgb[0]:02X}{rgb[1]:02X}{rgb[2]:02X} vs {st['rules_ink']}")
    return results


def main() -> int:
    ap = argparse.ArgumentParser(description="Verifica las cubiertas compuestas.")
    ap.add_argument("--dir", help="carpeta con <volumen>.pdf (por defecto, dist/)")
    ap.add_argument("--vol", nargs="*", help="volúmenes a comprobar")
    args = ap.parse_args()

    import tempfile
    work_root = Path(tempfile.mkdtemp(prefix="cover-verify-"))
    slugs = args.vol or sorted(STYLES)
    failures = 0

    for slug in slugs:
        if args.dir:
            pdf = Path(args.dir) / f"{slug}.pdf"
        else:
            pdf = (ROOT / "dist" / slug /
                   f"{slug}--lectura-6x9--con-portada.pdf")
        print(f"\n=== {slug}")
        if not pdf.is_file():
            print(f"  ✘ no existe {pdf}")
            failures += 1
            continue
        work = work_root / slug
        work.mkdir(parents=True, exist_ok=True)
        for name, ok, detail in check_volume(slug, pdf, work):
            print(f"  {'✔' if ok else '✘'} {name}"
                  + (f" — {detail}" if detail else ""))
            failures += 0 if ok else 1

    print(f"\n{'OK: todas las comprobaciones pasan' if not failures else f'{failures} comprobaciones fallidas'}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
