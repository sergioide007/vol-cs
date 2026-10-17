#!/usr/bin/env bash
# Migra el repo al layout  content/{es,en}/volN/  conservando el historial (git mv).
# Uso (desde la raíz del repo, rama limpia):   bash scripts/migrate-layout.sh
# Con DRY=1 solo imprime lo que haría.
set -euo pipefail

declare -A SLUG=( [vol1]=vol1-fundamentos [vol2]=vol2-frontera-y-aplicaciones
                  [vol3]=vol3-madurez-organizacional [vol4]=vol4-patrones-de-escala )
PARTS=(front-matter manuscrito referencias estado-del-arte)

run() { if [ "${DRY:-0}" = 1 ]; then echo "+ $*"; else "$@"; fi; }
mv_() { # git mv si el repo es git y el origen está versionado; si no, mv
  if [ -e "$1" ]; then
    mkdir -p "$(dirname "$2")"
    if [ "${DRY:-0}" != 1 ] && git ls-files --error-unmatch "$1" >/dev/null 2>&1; then
      run git mv "$1" "$2"
    else
      run mv "$1" "$2"
    fi
  fi
}

for short in vol1 vol2 vol3 vol4; do
  old="${SLUG[$short]}"
  [ -d "$old" ] || { echo "No existe $old, se omite"; continue; }
  for p in "${PARTS[@]}"; do
    mv_ "$old/$p"      "content/es/$short/$p"      # español: raíz del volumen
    mv_ "$old/en/$p"   "content/en/$short/$p"      # inglés: subcarpeta en/
  done
  # Utilidades sueltas del volumen (no son contenido)
  [ -f "$old/referencias_bib_append.py" ] && mv_ "$old/referencias_bib_append.py" "tools/legacy/$short-referencias_bib_append.py"
  # Binarios compilados: dejan de versionarse (los genera el CI)
  [ -d "$old/output" ] && { run rm -rf "$old/output"; }
  rmdir "$old/en" 2>/dev/null || true
  rmdir "$old"    2>/dev/null || true
done

# Documentos de trabajo → docs/
mkdir -p docs
mv_ INFORME_EDITORIAL.md docs/INFORME_EDITORIAL.md
mv_ tools/README-build.md docs/README-build.md
mv_ n.txt docs/notas/n.txt
# El CI antiguo (rutas viejas) lo reemplaza .github/workflows/deploy.yml
[ -f .github/workflows/manuscrito.yml ] && { git rm -q .github/workflows/manuscrito.yml 2>/dev/null || rm -f .github/workflows/manuscrito.yml; }
# Artefactos de build y de editor fuera del control de versiones
[ -d .alpaquitay ] && run git rm -r -q --cached .alpaquitay 2>/dev/null || true
[ -d dist ] && run git rm -r -q --cached dist 2>/dev/null || true
run rm -rf tools/__pycache__
echo "Layout migrado. Siguiente: aplicar tools/ y web/ del kit, y ejecutar los tests."
