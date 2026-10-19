#!/usr/bin/env bash
# Aplica las 6 imágenes EN: renombra las referencias _es -> _en en los capítulos EN del Vol. 4
# y elimina las copias en español que estaban dentro de content/en/.
# Uso (desde la raíz del repo, tras copiar encima el contenido de este paquete):  bash scripts/apply-en-images.sh
set -euo pipefail
V=content/en/vol4/manuscrito
fix() { sed -i "s#$2_es\.png#$2_en.png#g" "$V/capitulos/$1"; }
fix 01_capitulo_1.md imagenes/capitulo10/diagrama10_1
fix 04_capitulo_4.md imagenes/capitulo13/diagrama13_1
fix 05_capitulo_5.md imagenes/capitulo14/denuncias_extorsion
fix 06_capitulo_6.md imagenes/capitulo15/diagrama15_1
fix 07_capitulo_7.md imagenes/capitulo17/diagrama17_2_arquitectura_hibrida
fix 07_capitulo_7.md imagenes/uml/diagrama17_secuencia
for f in capitulo10/diagrama10_1 capitulo13/diagrama13_1 capitulo14/denuncias_extorsion capitulo15/diagrama15_1 capitulo17/diagrama17_2_arquitectura_hibrida uml/diagrama17_secuencia; do
  git rm -q "$V/imagenes/${f}_es.png" 2>/dev/null || rm -f "$V/imagenes/${f}_es.png"
done
echo "Pendientes con _es en EN: $(grep -rl _es.png $V/capitulos | wc -l) archivos"
