# Validación de las ediciones — 25 de septiembre de 2026 (4.ª pasada)

Estado: **construcción completa y validada por herramientas; pendiente de
aprobación editorial (revisión visual) y de datos de publicación (ISBN, cubierta)**.

Esta pasada incorpora, después del prólogo de cada volumen, el **Prefacio**,
junto con la portadilla, la hoja de créditos, la dedicatoria y la sinopsis.
El orden preliminar impreso es: Prólogo → Prefacio → Guía de lectura.

Resultados de `tools/validate_editions.py` (detalle en `dist/PREFLIGHT.json`):

| Volumen | Páginas | 6×9 | Fuentes | EPUBCheck | Glifos ausentes | Texto fuera de caja | Overfull hbox |
|---|---:|:-:|:-:|:-:|:-:|:-:|---:|
| 1 — Fundamentos | 174 | ✔ | ✔ | 2/2 | 0 | 0 | 0 |
| 2 — Frontera y aplicaciones | 342 | ✔ | ✔ | 2/2 | 0 | 0 | 2 |
| 3 — Madurez organizacional | 300 | ✔ | ✔ | 2/2 | 0 | 0 | 2 |
| 4 — Patrones de escala | 268 | ✔ | ✔ | 2/2 | 0 | 0 | 1 |

- EPUBCheck 4.2.6: los **8 EPUB** pasan con 0 errores, 0 avisos (3.2). El error
  inicial RSC-005 (el `id` de la portada derivaba de `01_cubierta_delantera.png`
  y empezaba por dígito) se corrigió pasando a pandoc una copia `cover.png`.
- Glifos ausentes: **0**. Los subíndices, ►, ✗ usan DejaVu Sans; `～ 👍 👎`
  tienen equivalentes de impresión solo en el PDF (el EPUB conserva el carácter).
- Texto fuera de la caja de texto (medido con `pdftotext -bbox` sobre el PDF):
  **0 páginas afectadas en la serie**. Las 4 incidencias previas (vol2 p. 92,
  vol3 pp. 144/163/273) se corrigieron en el manuscrito y se verificaron.
- Los 5 avisos `Overfull hbox` restantes (0 / 2 / 2 / 1) son residuos de
  **0,14 a 1,21 pt** (≤0,42 mm) en la hoja de créditos, una cabecera de sección
  y celdas ya partidas: invisibles y sin riesgo de corte; la medición horizontal
  real es la que acredita que no hay tinta fuera de caja.
- Los identificadores EPUB usan UUID deterministas provisionales
  (`urn:uuid:…`); cuando existan ISBN reales deben sustituirlos en
  `metadata_es.yaml` de cada volumen (cada edición necesita el suyo).

## Herramientas añadidas esta pasada

- `tools/validate_editions.py` — validación reproducible (tamaño de página,
  fuentes incrustadas, glifos, ajuste horizontal por `pdftotext -bbox`,
  EPUBCheck por archivo). Uso: `python3 tools/validate_editions.py`
  (opcional `--vol volX-…` para un solo volumen). Devuelve código de salida
  distinto de 0 si algo falla.
- `tools/lua/print-breaks.lua` — cortes tipográficos solo para el PDF
  (celdas de tabla: primera palabra separable, `/` y `→` rompibles,
  camelCase rompible). El texto del EPUB queda intacto (verificado).
- `tools/lua/fix-ids.lua` se descartó: la causa real era el nombre de archivo
  de portada, corregida en `build_editions.sh`.

## Pendientes para publicación (requieren datos o decisión humana)

- **ISBN reales** en los 4 `metadata_es.yaml` (ahora con UUID provisional).
- **Cubierta de imprenta** (contracubierta + lomo + portada con sangrado):
  depende de la plantilla del proveedor (KDP/Lulu) y del papel elegido;
  el lomo es ≈ páginas × 0,002252" (blanco) o × 0,0025" (crema). El PDF
  «lectura» con portada no es un archivo de cubierta de imprenta.
- **Revisión visual** en pantalla o prueba impresa: composición de páginas,
  imágenes reducidas, índice y folios. Las herramientas no la sustituyen.
- Prueba de impresión y aprobación del proveedor antes de publicar.

