#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Deriva de la medición del arte las constantes tipográficas de cada cubierta.

Entrada : tools/covers/cover-design.json (decisiones editoriales)
          tools/covers/inspect_covers.py  (medición del arte original)
Salidas : tools/covers/cover-styles.json   (cifras, para auditar)
          tools/latex/covers/<volumen>.tex (constantes que consume la plantilla)

Cómo se calcula cada cosa
-------------------------
El arte original trae el nombre de UN autor en la franja inferior, compuesto en
una sans geométrica (familia ITC Avant Garde). La leyenda nueva debe parecer
nativa, así que se copian del arte: altura de mayúscula, línea base, color de
acento y espaciado entre letras.

1. Altura de mayúscula: medida en el arte (cap_px). Pasa a puntos de página
   multiplicando por la escala del arte: 432 bp / 1024 px (página 6x9 pulg.).
2. Cuerpo tipográfico: TeX Gyre Adventor tiene cap/em = 0,735 (medido con las
   sondas tools/covers/probe*.tex), así que cuerpo = cap_bp / 0,735.
3. Espaciado entre letras: se compara el ancho de tinta de la primera palabra
   del arte ("SERGIO"/"Sergio") con el que da Adventor sin espaciado extra; la
   diferencia, repartida entre los huecos de esa palabra, es el espaciado que
   traía el arte. En fontspec, LetterSpace suma 0,27 x cuerpo x valor al ancho
   de una cadena de ~33 caracteres, es decir 0,27/32 del cuerpo por hueco (ley
   verificada a 16 y 32 bp con LetterSpace 10 y 20); de ahí el valor que se
   emite, calculado sobre los huecos de la leyenda completa.
4. Ancho de la leyenda: ancho natural (medido en las sondas) + espaciado x
   huecos. Si excede el máximo seguro de la página (384 bp = 0,89 del ancho, o
   sea 24 bp = 0,33 pulg. de margen por lado), se reduce todo proporcionalmente
   (cuerpo y espaciado) para respetar el área segura de KDP/Lulu.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from inspect_covers import ROOT, analyse  # noqa: E402

DESIGN = Path(__file__).resolve().parent / "cover-design.json"
STYLES_JSON = Path(__file__).resolve().parent / "cover-styles.json"
LATEX_DIR = ROOT / "tools" / "latex" / "covers"

TRIM_W_BP = 432.0            # 6 pulgadas en big points
ART_PX_W = 1024.0
S_PX_TO_BP = TRIM_W_BP / ART_PX_W

# Métricas de TeX Gyre Adventor Bold medidas con tools/covers/probe2..4.tex
# (anchos de tinta, en múltiplos del cuerpo tipográfico, con LetterSpace=0).
ADVENTOR = {
    "cap_per_em": 0.735,
    "ink_per_em": {
        "SERGIO": 3.465,        # 55.44 bp / 16 bp
        "Sergio": 2.910,        # 46.56 bp / 16 bp
        "upper_legend": 16.83,  # 269.28 bp / 16 bp
        "title_legend": 15.60,  # 249.60 bp / 16 bp
    },
    # Δancho_total = 0.27 × cuerpo × LetterSpace (43.2 bp con cuerpo 16 y LS 10)
    "letterspace_factor": 0.27,
}

LEGEND_MAX_WIDTH_BP = 384.0   # ancho máximo de la leyenda (área segura KDP/Lulu)
RULE_GAP_BP = 8.0             # aire entre la leyenda y las reglas laterales
RULE_MIN_LEN_BP = 30.0        # longitud mínima de cada regla (si no, no se lee)
FONT_FILE = "texgyreadventor-bold.otf"   # familia Avant Garde, la del arte


def derive(meas: dict, design: dict) -> dict:
    """Combina medición y diseño y devuelve las constantes de un volumen."""
    fw = meas["first_word"]
    cap_px = meas["cap_px"]
    cap_bp = cap_px * S_PX_TO_BP
    size = cap_bp / ADVENTOR["cap_per_em"]

    # Espaciado del arte: ancho de la primera palabra medido en el arte frente
    # al que daría Adventor sin espaciado extra, repartido entre los huecos.
    ratio_art = fw["width_px"] / cap_px
    ratio_nat = ADVENTOR["ink_per_em"][design["source_word"]] / ADVENTOR["cap_per_em"]
    gaps_word = fw["letters"] - 1
    extra_cap_per_gap = (ratio_art - ratio_nat) / gaps_word
    extra_gap_bp = extra_cap_per_gap * cap_bp

    legend = design["legend"]
    key = "upper_legend" if design["case"] == "upper" else "title_legend"
    gaps = len(legend) - 1
    natural_bp = ADVENTOR["ink_per_em"][key] * size
    total_bp = natural_bp + extra_gap_bp * gaps

    # LetterSpace: la ley es Δancho = 0,27 × cuerpo × LetterSpace para una
    # cadena de 33 caracteres, o sea que cada hueco recibe 0,27/32 del cuerpo.
    # Como el ancho crece proporcionalmente al cuerpo, el valor no cambia si
    # luego se reduce todo para respetar el área segura.
    letterspace = (extra_gap_bp * gaps
                   / (ADVENTOR["letterspace_factor"] * size))

    # Presupuesto de ancho: si el volumen lleva reglas laterales hay que dejarles
    # sitio para que se lean como reglas y no como guiones.
    reserve = 2 * RULE_GAP_BP + (2 * RULE_MIN_LEN_BP if design["rules"] else 0.0)
    budget = LEGEND_MAX_WIDTH_BP - reserve
    scale = min(1.0, budget / total_bp)

    size_final = size * scale
    legend_bp = total_bp * scale
    rule_len_bp = max(0.0, (LEGEND_MAX_WIDTH_BP - legend_bp) / 2 - RULE_GAP_BP) \
        if design["rules"] else 0.0
    line_bp = legend_bp + 2 * RULE_GAP_BP + 2 * rule_len_bp

    patch_top = meas["bottom_patch"]["patch_top"]
    baseline_row = meas["baseline_row"]
    art_h = meas["size"][1]

    out = {
        "legend": legend,
        "case": design["case"],
        "rules": design["rules"],
        "cap_px": cap_px,
        "cap_bp": round(cap_bp, 3),
        "size_bp": round(size_final, 3),
        "size_bp_unscaled": round(size, 3),
        "letterspace": round(letterspace, 4),
        "scale": round(scale, 4),
        "legend_width_bp": round(legend_bp, 2),
        "line_width_bp": round(line_bp, 2),
        "margin_bp": round((TRIM_W_BP - line_bp) / 2, 2),
        "ink": meas["accent"]["hex"],
        "ink_rgb": meas["accent"]["rgb"],
        "baseline_px": baseline_row,
        "baseline_bp": round((art_h - baseline_row - 1) * S_PX_TO_BP, 3),
        "patch_top_px": patch_top,
        "patch_height_bp": round((art_h - patch_top) * S_PX_TO_BP, 3),
        "source_bottom_px": meas["quiet_band"][1],
        "patch_stretch": meas["bottom_patch"]["stretch"],
        # Constantes de reglas: se emiten siempre (0 si el volumen no las lleva)
        # para que la plantilla pueda calcular sin condicionales.
        "rules_ink": None,
        "rule_height_bp": 0.0,
        "rule_depth_bp": 0.0,
        "rule_len_bp": round(rule_len_bp, 3),
        "rule_gap_bp": RULE_GAP_BP,
    }
    if design["rules"]:
        rule_rows = sorted({r["y"] for r in meas["side_rules"]})
        top_bp = (baseline_row + 1 - rule_rows[0]) * S_PX_TO_BP * scale
        bottom_bp = (baseline_row - rule_rows[-1]) * S_PX_TO_BP * scale
        # Color de las reglas: núcleos medidos del arte (ver inspect_covers).
        rules_ink = meas.get("side_rules_ink") or {"hex": meas["side_rules"][0]["hex"]}
        out["rules_ink"] = rules_ink["hex"]
        out["rule_height_bp"] = round(top_bp, 3)
        out["rule_depth_bp"] = round(-bottom_bp, 3)
        out["rule_gap_bp"] = RULE_GAP_BP
    return out


def tex_for(slug: str, st: dict, art_h: int) -> str:
    """Escribe el bloque TeX con las constantes del volumen."""
    lines = [
        "% " + "-" * 74,
        f"% Estilo de cubierta — {slug}",
        "% GENERADO por tools/covers/make_styles.py: no editar a mano.",
        f"% Leyenda: {st['legend']}",
        f"% Mayúscula del arte {st['cap_px']} px → cuerpo {st['size_bp']} bp "
        f"(sin escalar {st['size_bp_unscaled']} bp, factor {st['scale']})",
        f"% Ancho de leyenda {st['legend_width_bp']} bp (máximo seguro "
        f"{LEGEND_MAX_WIDTH_BP} bp) → margen {st['margin_bp']} bp por lado",
        "% " + "-" * 74,
        f"\\def\\CoverArtPxH{{{art_h}}}",
        f"\\def\\CoverArtPxW{{{int(ART_PX_W)}}}",
        f"\\def\\CoverPatchTopPx{{{st['patch_top_px']}}}",
        f"\\def\\CoverSourceBottomPx{{{st['source_bottom_px']}}}",
        f"\\def\\CoverPatchHeightBp{{{st['patch_height_bp']}bp}}",
        # Recortes: el PNG no declara dpi, así que graphicx lo toma a 1 px = 1 bp
        # y los recortes se expresan en píxeles del arte.
        f"\\def\\CoverTrimTopBp{{{st['patch_top_px']}bp}}",
        f"\\def\\CoverTrimBottomBp{{{art_h - 1 - st['source_bottom_px']}bp}}",
        f"\\def\\CoverLegendBaselineBp{{{st['baseline_bp']}bp}}",
        f"\\def\\CoverLegendSize{{{st['size_bp']}bp}}",
        f"\\def\\CoverLegendLeading{{{round(st['size_bp'] * 1.18, 3)}bp}}",
        f"\\def\\CoverLegendInk{{{st['ink'].lstrip('#')}}}",
        f"\\def\\CoverLegendText{{{st['legend']}}}",
        f"\\def\\CoverLegendWidthBp{{{st['legend_width_bp']}bp}}",
        f"\\def\\CoverLineWidthBp{{{st['line_width_bp']}bp}}",
        f"\\def\\CoverRulesEnabled{{{1 if st['rules'] else 0}}}",
        f"\\newfontfamily\\CoverLegendFont{{{FONT_FILE}}}"
        f"[LetterSpace={st['letterspace']}]",
        # Constantes de reglas laterales: siempre presentes (a 0 si no se usan).
        f"\\def\\CoverRuleInk{{{st['rules_ink'].lstrip('#') if st['rules_ink'] else 'FFFFFF'}}}",
        f"\\def\\CoverRuleHeightBp{{{st['rule_height_bp']}bp}}",
        f"\\def\\CoverRuleDepthBp{{{st['rule_depth_bp']}bp}}",
        f"\\def\\CoverRuleLenBp{{{st['rule_len_bp']}bp}}",
        f"\\def\\CoverRuleGapBp{{{st['rule_gap_bp']}bp}}",
    ]
    return "\n".join(lines) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser(description="Genera los estilos de cubierta.")
    ap.add_argument("--vol", nargs="*", help="volúmenes (por defecto, todos)")
    ap.add_argument("--lang", choices=("es", "en"), default="es",
                    help="idioma del arte (cada idioma tiene su propia cubierta)")
    args = ap.parse_args()
    # ES conserva las rutas históricas; EN usa su propio JSON y su subcarpeta.
    global STYLES_JSON, LATEX_DIR
    if args.lang != "es":
        STYLES_JSON = STYLES_JSON.with_name(f"cover-styles.{args.lang}.json")
        LATEX_DIR = LATEX_DIR / args.lang

    design = json.loads(DESIGN.read_text(encoding="utf-8"))["legends"]
    slugs = args.vol or sorted(design)
    LATEX_DIR.mkdir(parents=True, exist_ok=True)

    styles: dict[str, dict] = {}
    print(f"{'volumen':<32}{'cap':>4}{'cuerpo':>9}{'LetterSp.':>10}"
          f"{'ancho':>8}{'factor':>8}{'margen':>8}")
    for slug in slugs:
        cover = ROOT / "content" / args.lang / slug.split("-")[0] / "front-matter" / "01_cubierta_delantera.png"
        if not cover.is_file():
            print(f"! sin cubierta: {cover}", file=sys.stderr)
            continue
        meas = analyse(cover)
        st = derive(meas, design[slug])
        styles[slug] = st
        (LATEX_DIR / f"{slug}.tex").write_text(
            tex_for(slug, st, meas["size"][1]), encoding="utf-8")
        print(f"{slug:<32}{st['cap_px']:>4}{st['size_bp']:>9.2f}"
              f"{st['letterspace']:>10.3f}{st['legend_width_bp']:>8.1f}"
              f"{st['scale']:>8.3f}{st['margin_bp']:>8.1f}")

    STYLES_JSON.write_text(
        json.dumps({
            "_lee": [
                "Cifras derivadas del arte por tools/covers/make_styles.py.",
                "Las medidas crudas están en tools/covers/inspect_covers.py;",
                "las decisiones editoriales, en cover-design.json.",
                "patch_* describen el parche que borra el nombre de un autor;",
                "size_bp/letterspace/ink/baseline_bp describen la leyenda nueva.",
            ],
            "escala_px_a_bp": S_PX_TO_BP,
            "max_ancho_leyenda_bp": LEGEND_MAX_WIDTH_BP,
            "tipografia": {"archivo": FONT_FILE, **ADVENTOR},
            "volumenes": styles,
        }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"\nEscrito {STYLES_JSON} y {LATEX_DIR}/*.tex")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
