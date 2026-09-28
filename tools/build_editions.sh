#!/usr/bin/env bash
# ===========================================================================
# Código Sintético — generación profesional de ediciones
#
# Produce, por cada volumen, cuatro archivos en dist/<volumen>/:
#   1) <vol>--epub--con-portada.epub      Tiendas digitales (KDP/Kindle, Lulu,
#                                         Apple Books, Kobo, Google Play)
#   2) <vol>--epub--sin-portada.epub      Manuscrito EPUB sin cubierta embebida
#   3) <vol>--interior-6x9--sin-caratula.pdf
#                                         Archivo de imprenta para KDP y Lulu
#                                         (tapa blanda y tapa dura)
#   4) <vol>--lectura-6x9--con-portada.pdf
#                                         PDF de difusión directa, con portada
#
# FORMATO Y MÁRGENES (6 x 9 pulgadas = 15,24 x 22,86 cm)
#   La caja de texto es menor que el trim porque hay que respetar márgenes:
#     interior (lomo) 0,875"  ·  exterior 0,625"  ·  superior 0,75"  ·  inferior 0,75"
#     caja de texto resultante: 4,5" x 7,5"  (11,43 x 19,05 cm)
#   Verificación contra las especificaciones vigentes:
#     · KDP tapa blanda: exterior/superior/inferior >= 0,25"; interior (gutter)
#       >= 0,375" (24-150 pág.), 0,5" (151-300), 0,625" (301-500),
#       0,75" (501-700), 0,875" (701-828).  -> cumplimos con holgura.
#     · KDP tapa dura 6x9: 75-550 páginas; márgenes >= 0,5" por lado.
#     · Lulu: mínimo 0,5" en todos los lados; interior recomendado >= 0,75".
#   Con estos valores el mismo PDF sirve para KDP y Lulu, tapa blanda y dura.
#
# Uso:
#   bash tools/build_editions.sh                 # todos los volúmenes
#   bash tools/build_editions.sh vol1-fundamentos
# ===========================================================================
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TOOLS="$ROOT/tools"
DIST="$ROOT/dist"
COVERS="$DIST/covers"
WORK="${TMPDIR:-/tmp}/codigo-sintetico-build"
mkdir -p "$DIST" "$WORK"

PANDOC="${PANDOC:-pandoc}"
PDF_ENGINE="${PDF_ENGINE:-xelatex}"
COVER_DPI="${COVER_DPI:-300}"      # resolución de la cubierta para el EPUB

# --- Parámetros de imprenta ------------------------------------------------
TRIM_W_IN="${TRIM_W_IN:-6}"
TRIM_H_IN="${TRIM_H_IN:-9}"
M_INSIDE="${M_INSIDE:-0.875}"
M_OUTSIDE="${M_OUTSIDE:-0.625}"
M_TOP="${M_TOP:-0.75}"
M_BOTTOM="${M_BOTTOM:-0.75}"
FONTSIZE="${FONTSIZE:-11pt}"
MAINFONT="${MAINFONT:-TeX Gyre Pagella}"
MONOFONT="${MONOFONT:-DejaVu Sans Mono}"
LINESTRETCH="${LINESTRETCH:-1.06}"

REPORT="$DIST/BUILD-REPORT.md"

log()  { printf '\033[1;34m▸\033[0m %s\n' "$*"; }
ok()   { printf '\033[1;32m✔\033[0m %s\n' "$*"; }
warn() { printf '\033[1;33m!\033[0m %s\n' "$*"; }
die()  { printf '\033[1;31m✘\033[0m %s\n' "$*" >&2; exit 1; }

require_tools() {
  local missing=()
  for t in "$PANDOC" "$PDF_ENGINE" pdfinfo pdfunite pdffonts pdftoppm python3; do
    command -v "$t" >/dev/null 2>&1 || missing+=("$t")
  done
  if [ "${#missing[@]}" -gt 0 ]; then
    die "Faltan herramientas: ${missing[*]}. Instale pandoc, texlive-xetex, poppler-utils, python3-pil."
  fi
}

# Lee un campo escalar de metadata_es.yaml (title, subtitle, author, date...)
meta_field() {
  local file="$1" key="$2"
  awk -v k="$key" '
    $0 ~ "^" k ":" {
      sub("^" k ":[[:space:]]*", "")
      gsub(/^"|"[[:space:]]*$/, "")
      print
      exit
    }' "$file"
}

# Título de la serie/volumen que corre en las páginas pares (verso)
running_title() {
  case "$1" in
    vol1-fundamentos)             echo "Código Sintético · Fundamentos" ;;
    vol2-frontera-y-aplicaciones) echo "Código Sintético · Frontera y Aplicaciones" ;;
    vol3-madurez-organizacional)  echo "Código Sintético · Madurez Organizacional" ;;
    vol4-patrones-de-escala)      echo "Código Sintético · Patrones de Escala" ;;
    *)                            echo "Código Sintético" ;;
  esac
}

volumes() {
  if [ "$#" -gt 0 ]; then
    printf '%s\n' "$@"
  else
    find "$ROOT" -mindepth 1 -maxdepth 1 -type d -name 'vol[1-4]-*' -printf '%f\n' | LC_ALL=C sort
  fi
}

# Lista ordenada de archivos que forman el cuerpo del libro
body_files() {
  local d="$1"
  printf '%s\n' \
    "$d/front-matter/03_hoja_creditos.md" \
    "$d/front-matter/02b_dedicatoria.md" \
    "$d/front-matter/01b_sinopsis.md" \
    "$d/front-matter/02c_prologo.md" \
    "$d/front-matter/02d_prefacio.md" \
    "$d/front-matter/04b_guia_de_lectura.md" \
    "$d/front-matter/04c_nota_vigencia.md" \
    "$d/front-matter/05_cuaderno_de_lectura_critica.md" \
    "$d/front-matter/06_glosario.md" \
    "$d/front-matter/07_indice_de_consulta_rapida.md"
  find "$d/manuscrito/capitulos" -maxdepth 1 -name '*.md' -printf '%p\n' | LC_ALL=C sort
  # El apéndice B va después del cuerpo y antes de las referencias: los capítulos
  # lo citan y el lector debe encontrarlo sin pasar por la bibliografía.
  [ -f "$d/front-matter/08_apendice_b_precios.md" ] \
    && printf '%s\n' "$d/front-matter/08_apendice_b_precios.md"
  printf '%s\n' \
    "$d/estado-del-arte/estado-del-arte.md" \
    "$d/referencias/referencias.md"
}

# --- Cifras normativas ------------------------------------------------------
# Mínimo de margen interior (gutter) exigido por KDP según la paginación.
kdp_gutter_min() {
  local p="$1"
  if   [ "$p" -le 150 ]; then echo "0.375"
  elif [ "$p" -le 300 ]; then echo "0.5"
  elif [ "$p" -le 500 ]; then echo "0.625"
  elif [ "$p" -le 700 ]; then echo "0.75"
  else                        echo "0.875"
  fi
}

# Margen interior que usamos: el mayor entre el estándar profesional (0,875")
# y el mínimo de KDP para la paginación real (así el archivo nunca se rechaza).
gutter_for_pages() {
  local p="$1" kdp
  kdp="$(kdp_gutter_min "$p")"
  awk -v a="$M_INSIDE" -v b="$kdp" 'BEGIN { print (a+0 >= b+0) ? a : b }'
}

spine_width()       { awk -v p="$1" 'BEGIN { printf "%.3f", p * 0.002252 }'; }  # papel blanco
spine_width_cream() { awk -v p="$1" 'BEGIN { printf "%.3f", p * 0.0025   }'; }  # papel crema

# --- Composición del PDF interior (sin carátula) ---------------------------
build_interior_pdf() {
  local d="$1" out="$2" tmp="$3" inside="$4"
  local hdr="$tmp/header-interior.tex"
  sed -e "s|@RUNNING-TITLE@|$(running_title "$(basename "$d")")|g" \
      -e "s|@GRAPHICSPATH@|$d/manuscrito/|g" \
      "$TOOLS/latex/header-interior.tex" > "$hdr"

  # La hoja de créditos va antes del índice y sin numerar (orden editorial).
  "$PANDOC" "$d/front-matter/03_hoja_creditos.md" -t latex -o "$tmp/creditos.tex"

  mapfile -t files < <(body_files "$d" | tail -n +2)

  "$PANDOC" "${files[@]}" \
    --from=markdown+smart+pipe_tables \
    --to=latex --standalone \
    --output="$tmp/main.tex" \
    --metadata-file="$d/front-matter/metadata_es.yaml" \
    --toc --toc-depth=2 \
    --include-in-header="$hdr" \
    --include-before-body="$tmp/creditos.tex" \
    --lua-filter="$TOOLS/lua/table-widths.lua" \
    --lua-filter="$TOOLS/lua/reference-anchors.lua" \
    --lua-filter="$TOOLS/lua/print-breaks.lua" \
    --resource-path="$d/manuscrito:$d/manuscrito/capitulos:$d" \
    -V documentclass=book \
    -V classoption=twoside -V classoption=openright \
    -V fontsize="$FONTSIZE" \
    -V mainfont="$MAINFONT" -V monofont="$MONOFONT" \
    -V indent=true -V linestretch="$LINESTRETCH" \
    -V geometry:paperwidth="${TRIM_W_IN}in" \
    -V geometry:paperheight="${TRIM_H_IN}in" \
    -V geometry:inner="${inside}in" \
    -V geometry:outer="${M_OUTSIDE}in" \
    -V geometry:top="${M_TOP}in" \
    -V geometry:bottom="${M_BOTTOM}in" \
    -V toc-title="Índice" \
    2> "$tmp/pandoc-latex.log" \
    || { tail -30 "$tmp/pandoc-latex.log"; die "pandoc falló al generar el LaTeX de $d"; }

  # Tres pasadas de XeLaTeX: índice con folios reales, referencias internas
  # de las citas (anclas #ref-*) y cabeceras definitivas.
  local pass
  for pass in 1 2 3; do
    ( cd "$tmp" && xelatex -interaction=nonstopmode -halt-on-error main.tex </dev/null >/dev/null 2>&1 ) \
      || { echo "--- últimas líneas de main.log ---"; tail -40 "$tmp/main.log"; die "XeLaTeX falló en la pasada $pass de $d"; }
  done

  cp "$tmp/main.pdf" "$out"
}

# --- Composición del EPUB ---------------------------------------------------
build_epub() {
  local d="$1" out="$2" tmp="$3" cover="$4"
  mapfile -t files < <(body_files "$d")
  local args=( "${files[@]}"
    --from=markdown+smart+pipe_tables
    --to=epub3
    --output="$out"
    --metadata-file="$d/front-matter/metadata_es.yaml"
    --toc --toc-depth=2
    --css="$TOOLS/epub.css"
    --lua-filter="$TOOLS/lua/table-widths.lua"
    --lua-filter="$TOOLS/lua/reference-anchors.lua"
    --resource-path="$d/manuscrito:$d/manuscrito/capitulos:$d"
    --split-level=1
    -V lang=es )

  if [ -n "$cover" ]; then
    # La cubierta es la compuesta por tools/covers/render_covers.sh (arte
    # original + leyenda con los dos coautores), no el PNG del arte. El id XML
    # del item de portada lo deriva pandoc del nombre del archivo; se copia con
    # un nombre que empiece por letra para que EPUBCheck no lo rechace
    # (RSC-005: un nombre XML no puede empezar por dígito).
    cp "$cover" "$tmp/cubierta.jpg"
    args+=( --epub-cover-image="$tmp/cubierta.jpg" )
  fi

  "$PANDOC" "${args[@]}" 2> "$tmp/epub.log" \
    || { tail -20 "$tmp/epub.log"; die "pandoc falló al generar el EPUB de $d"; }
}

# --- Cubiertas compuestas ---------------------------------------------------
# El arte de las portadas acredita a un solo autor. tools/covers/ mide ese arte
# (altura de mayúscula, línea base, espaciado, color de acento, franja limpia)
# y compone una leyenda vectorial con los dos coautores sobre un parche de la
# propia ilustración. Por cada volumen produce:
#   dist/covers/<vol>.pdf                   cubierta 6x9 (432 x 648 bp)
#   dist/covers/<vol>-cover-300ppp.jpg      la misma, para el EPUB
build_covers() {
  local work="$WORK/covers"
  mkdir -p "$work" "$COVERS"
  python3 "$TOOLS/covers/make_styles.py" >"$work/styles.log" 2>&1 \
    || { tail -20 "$work/styles.log"; die "Falló la medición del arte de cubiertas"; }
  bash "$TOOLS/covers/render_covers.sh" --out "$COVERS" --dpi "$COVER_DPI" "$@" \
    >"$work/render.log" 2>&1 \
    || { tail -30 "$work/render.log"; die "Falló la composición de cubiertas"; }
}

# Leyenda de autoría decidida para un volumen (de la medición, no a mano)
legend_of() {
  python3 -c 'import json,sys
d = json.load(open(sys.argv[1], encoding="utf-8"))["volumenes"]
print(d[sys.argv[2]]["legend"])' "$TOOLS/covers/cover-styles.json" "$1"
}

# --- Portada suelta (6x9) para el PDF de lectura ----------------------------
make_cover_pdf() {
  local slug="$1" out="$2"
  local cover="$COVERS/$slug.pdf"
  [ -f "$cover" ] || die "No hay cubierta compuesta para $slug: $cover"
  cp "$cover" "$out"
}

# --- Verificación de un PDF ya compuesto ------------------------------------
verify_pdf() {
  local pdf="$1"
  PDF_PAGES=$(pdfinfo "$pdf" | awk '/^Pages:/{print $2}')
  PDF_SIZE=$(pdfinfo "$pdf"  | awk -F': *' '/^Page size/{print $2}')
  PDF_EMB_TOTAL=$(pdffonts "$pdf" | tail -n +3 | grep -c . || true)
  PDF_EMB_OK=$(pdffonts "$pdf" | tail -n +3 | awk 'NF>=6 && $(NF-4)=="yes" {n++} END {print n+0}')
}

# --- Programa principal -----------------------------------------------------
require_tools

{
  echo "# Informe de construcción — Serie «Código Sintético»"
  echo
  echo "Generado: $(date -u '+%Y-%m-%d %H:%M UTC')"
  echo
  echo "## Parámetros de imprenta aplicados (6 × 9 pulgadas)"
  echo
  echo "| Concepto | Valor |"
  echo "|---|---|"
  printf '| Trim (formato final) | %s × %s in (15,24 × 22,86 cm) |\n' "$TRIM_W_IN" "$TRIM_H_IN"
  printf '| Margen interior (lomo/gutter) | %s in |\n' "$M_INSIDE"
  printf '| Margen exterior | %s in |\n' "$M_OUTSIDE"
  printf '| Margen superior | %s in |\n' "$M_TOP"
  printf '| Margen inferior | %s in |\n' "$M_BOTTOM"
  printf '| Caja de texto resultante | %s × %s in |\n' \
    "$(awk -v w="$TRIM_W_IN" -v i="$M_INSIDE" -v o="$M_OUTSIDE" 'BEGIN{printf "%.4f", w-i-o}')" \
    "$(awk -v h="$TRIM_H_IN" -v t="$M_TOP" -v b="$M_BOTTOM" 'BEGIN{printf "%.4f", h-t-b}')"
  printf '| Cuerpo / interlineado | %s / %s |\n' "$FONTSIZE" "$LINESTRETCH"
  printf '| Tipografías | %s (texto) · %s (código) |\n' "$MAINFONT" "$MONOFONT"
  echo
  echo "_Motivo de estos márgenes: la caja de texto debe ser menor que el trim"
  echo "para que la encuadernación, el lomo y la guillotina no corten texto._"
  echo "Los valores superan el mínimo de KDP (0,25\" exterior; 0,375\"–0,875\""
  echo "interior según paginación) y el de Lulu (0,5\" en todos los lados)."
  echo
  echo "## Volúmenes"
} > "$REPORT"

failures=0

mapfile -t slugs < <(volumes "$@")

# Cubiertas: se componen antes del bucle porque el EPUB con portada y el PDF de
# lectura las necesitan. Solo se procesan los volúmenes que existen en disco.
cover_slugs=()
for slug in "${slugs[@]}"; do
  [ -d "$ROOT/$slug" ] && cover_slugs+=("$slug")
done
if [ "${#cover_slugs[@]}" -gt 0 ]; then
  log "Componiendo cubiertas (arte original + leyenda de autoría) …"
  build_covers "${cover_slugs[@]}"
  ok "cubiertas 6x9 y para EPUB en $COVERS"
fi

for slug in "${slugs[@]}"; do
  d="$ROOT/$slug"
  [ -d "$d" ] || { warn "Directorio no encontrado: $slug (se omite)"; continue; }

  log "Componiendo $slug …"
  tmp="$WORK/$slug"
  rm -rf "$tmp"; mkdir -p "$tmp"
  out="$DIST/$slug"; mkdir -p "$out"

  interior="$out/${slug}--interior-6x9--sin-caratula.pdf"
  epub_cover="$out/${slug}--epub--con-portada.epub"
  epub_plain="$out/${slug}--epub--sin-portada.epub"
  reading="$out/${slug}--lectura-6x9--con-portada.pdf"

  # 1) PDF interior (el archivo que se sube a KDP y Lulu)
  inside_used="$M_INSIDE"
  build_interior_pdf "$d" "$interior" "$tmp" "$inside_used"
  pages=$(pdfinfo "$interior" | awk '/^Pages:/{print $2}')

  # Si por paginación KDP exigiera más lomo del que usamos, se recompone.
  need="$(gutter_for_pages "$pages")"
  if awk -v a="$inside_used" -v b="$need" 'BEGIN{exit !(b+0 > a+0)}'; then
    warn "$slug: $pages págs. exigen lomo $need\" (KDP); se recompone."
    inside_used="$need"
    build_interior_pdf "$d" "$interior" "$tmp" "$inside_used"
    pages=$(pdfinfo "$interior" | awk '/^Pages:/{print $2}')
  fi
  verify_pdf "$interior"

  # 2) EPUB con y sin portada
  build_epub "$d" "$epub_cover" "$tmp" "$COVERS/$slug-cover-${COVER_DPI}ppp.jpg"
  build_epub "$d" "$epub_plain" "$tmp" ""

  # 3) PDF de lectura: portada compuesta 6x9 + interior
  make_cover_pdf "$slug" "$tmp/cover-6x9.pdf"
  pdfunite "$tmp/cover-6x9.pdf" "$interior" "$reading"

  # --- Métricas y avisos ----------------------------------------------------
  overfull=$(grep -c 'Overfull \\hbox' "$tmp/main.log" 2>/dev/null || true)
  misses=$(grep -ci 'could not fetch\|no such file' "$tmp/pandoc-latex.log" 2>/dev/null || true)
  kdp_min=$(kdp_gutter_min "$pages")
  hc_ok="sí"
  [ "$pages" -ge 75 ] && [ "$pages" -le 550 ] || hc_ok="no (KDP tapa dura admite 75–550 págs.)"

  log "$slug: $pages páginas · $PDF_SIZE · caja $(awk -v w="$TRIM_W_IN" -v i="$inside_used" -v o="$M_OUTSIDE" 'BEGIN{printf "%.4f", w-i-o}') × $(awk -v h="$TRIM_H_IN" -v t="$M_TOP" -v b="$M_BOTTOM" 'BEGIN{printf "%.4f", h-t-b}') in"
  [ "$overfull" = "0" ] || warn "$slug: $overfull líneas desbordadas (Overfull \\hbox) — revisar tablas/código anchos."
  [ "$misses" = "0" ]   || warn "$slug: $misses recursos no encontrados (imágenes)."
  [ "$PDF_EMB_TOTAL" = "$PDF_EMB_OK" ] || warn "$slug: fuentes no incrustadas ($PDF_EMB_OK/$PDF_EMB_TOTAL)."

  {
    echo
    printf '### %s\n\n' "$slug"
    echo "| Dato | Valor |"
    echo "|---|---|"
    printf '| Páginas del interior | %s |\n' "$pages"
    printf '| Tamaño de página | %s (= 6 × 9 in) |\n' "$PDF_SIZE"
    printf '| Caja de texto | %s × %s in |\n' \
      "$(awk -v w="$TRIM_W_IN" -v i="$inside_used" -v o="$M_OUTSIDE" 'BEGIN{printf "%.4f", w-i-o}')" \
      "$(awk -v h="$TRIM_H_IN" -v t="$M_TOP" -v b="$M_BOTTOM" 'BEGIN{printf "%.4f", h-t-b}')"
    printf '| Lomo aplicado / mínimo KDP para %s págs. | %s in / %s in |\n' "$pages" "$inside_used" "$kdp_min"
    printf '| Elegible para tapa dura KDP (75–550 págs.) | %s |\n' "$hc_ok"
    printf '| Lomo de cubierta (papel blanco / crema) | %s in / %s in |\n' "$(spine_width "$pages")" "$(spine_width_cream "$pages")"
    printf '| Fuentes incrustadas | %s/%s |\n' "$PDF_EMB_OK" "$PDF_EMB_TOTAL"
    printf '| Cubierta compuesta | `dist/covers/%s.pdf` + `%s-cover-%sppp.jpg` |\n' \
      "$slug" "$slug" "$COVER_DPI"
    printf '| Leyenda de autoría de la cubierta | %s |\n' "$(legend_of "$slug")"
    printf '| Líneas desbordadas (Overfull hbox) | %s |\n' "$overfull"
    printf '| Recursos no encontrados | %s |\n' "$misses"
    echo
    echo "**Archivos generados**"
    echo
    for f in "$out"/*; do
      printf -- '- `%s` (%s)\n' "$(basename "$f")" "$(du -h "$f" | cut -f1)"
    done
  } >> "$REPORT"

  ok "$slug completado → dist/$slug/"
done

echo
ok "Informe: dist/BUILD-REPORT.md"

