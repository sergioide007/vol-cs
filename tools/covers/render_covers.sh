#!/usr/bin/env bash
# ===========================================================================
# Código Sintético — renderiza las páginas de cubierta 6x9 (432 x 648 bp)
#
# Por cada volumen produce, en el directorio indicado:
#   <volumen>.pdf                 página de cubierta (arte + leyenda vectorial)
#   <volumen>-cover-300ppp.jpg    la misma cubierta a 300 ppp, para el EPUB
#   <volumen>/                    archivos auxiliares de LaTeX
#
# La cubierta se compone sobre el arte original (que acredita a un solo autor):
# tools/latex/cover-page.tex + tools/latex/covers/<volumen>.tex (constantes
# medidas del arte por tools/covers/make_styles.py).
#
# Uso:
#   bash tools/covers/render_covers.sh --out dist/covers
#   bash tools/covers/render_covers.sh --out dist/covers vol1-fundamentos
# ===========================================================================
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
OUT=""
SLUGS=()
EPUB_DPI="${EPUB_DPI:-300}"

while [ $# -gt 0 ]; do
  case "$1" in
    --out) OUT="$2"; shift 2 ;;
    --dpi) EPUB_DPI="$2"; shift 2 ;;
    -h|--help) sed -n '2,20p' "${BASH_SOURCE[0]}"; exit 0 ;;
    *) SLUGS+=("$1"); shift ;;
  esac
done

if [ -z "$OUT" ]; then
  echo "Falta --out DIR" >&2
  exit 2
fi
if [ "${#SLUGS[@]}" -eq 0 ]; then
  mapfile -t SLUGS < <(find "$ROOT" -mindepth 1 -maxdepth 1 -type d \
    -name 'vol[1-4]-*' -printf '%f\n' | LC_ALL=C sort)
fi

mkdir -p "$OUT"
fail=0
for slug in "${SLUGS[@]}"; do
  art="$ROOT/$slug/front-matter/01_cubierta_delantera.png"
  style="$ROOT/tools/latex/covers/$slug"
  work="$OUT/$slug"
  if [ ! -f "$art" ]; then
    echo "! $slug: falta el arte $art" >&2
    fail=1; continue
  fi
  if [ ! -f "$style.tex" ]; then
    echo "! $slug: falta el estilo $style.tex (ejecute tools/covers/make_styles.py)" >&2
    fail=1; continue
  fi

  rm -rf "$work"; mkdir -p "$work"
  sed -e "s|@COVER@|$art|g" -e "s|@STYLE@|$style|g" \
      "$ROOT/tools/latex/cover-page.tex" > "$work/cover-page.tex"
  if ! ( cd "$work" && xelatex -interaction=nonstopmode -halt-on-error \
         cover-page.tex >"$work/xelatex.log" 2>&1 ); then
    echo "! $slug: falló xelatex" >&2
    tail -25 "$work/xelatex.log" >&2
    fail=1; continue
  fi
  cp "$work/cover-page.pdf" "$OUT/$slug.pdf"

  # Cubierta para el EPUB: la misma página rasterizada a 300 ppp (1800 x 2700,
  # muy por encima del mínimo de KDP) y guardada como JPEG para no inflar el
  # archivo del libro.
  if command -v pdftoppm >/dev/null 2>&1; then
    pdftoppm -r "$EPUB_DPI" -png -singlefile "$OUT/$slug.pdf" "$work/epub-cover"
    python3 - "$work/epub-cover.png" "$OUT/$slug-cover-${EPUB_DPI}ppp.jpg" <<'PY'
import sys
from pathlib import Path
from PIL import Image
src, dst = sys.argv[1], sys.argv[2]
im = Image.open(src).convert("RGB")
im.save(dst, "JPEG", quality=88, optimize=True)
print(f"  cubierta EPUB {im.size[0]}x{im.size[1]} px "
      f"({im.size[0] / 6:.0f} ppp) -> {Path(dst).name} "
      f"{Path(dst).stat().st_size // 1024} KB")
PY
  fi
  echo "✔ $slug → $OUT/$slug.pdf"
done

exit "$fail"
