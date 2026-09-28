u# Validación de las ediciones — 28 de septiembre de 2026 (5.ª pasada)

Estado: **construcción completa y validada por herramientas; pendiente de
aprobación editorial (revisión visual) y de datos de publicación (ISBN, cubierta)**.

Esta pasada añade el **Apéndice B** (precios de referencia) a los cuatro volúmenes
y corrige la numeración heredada del Epílogo y de 34 remisiones cruzadas. El
Apéndice B se compone después del cuerpo y antes de la bibliografía, y es la
única fuente de precios e identificadores de modelo de la serie.

Resultados de `tools/validate_editions.py` (detalle en `dist/PREFLIGHT.json`):

| Volumen | Páginas | 6×9 | Fuentes | EPUBCheck | Glifos ausentes | Texto fuera de caja | Overfull hbox |
|---|---:|:-:|:-:|:-:|:-:|:-:|---:|
| 1 — Fundamentos | 178 | ✔ | ✔ | 2/2 | 0 | 0 | 0 |
| 2 — Frontera y aplicaciones | 346 | ✔ | ✔ | 2/2 | 0 | 0 | 2 |
| 3 — Madurez organizacional | 306 | ✔ | ✔ | 2/2 | 0 | 0 | 2 |
| 4 — Patrones de escala | 270 | ✔ | ✔ | 2/2 | 0 | 0 | 1 |

Las cuatro páginas suben por el Apéndice B (+4, +4, +6 y +2 respecto a la
4.ª pasada). Los cinco `Overfull \hbox` son los mismos de la pasada anterior:
residuos de 0,14 a 1,21 pt, invisibles y sin riesgo de corte.

La auditoría del **manuscrito** (no de la maquetación) la produce
`tools/lint_manuscript.py` y vive en `dist/AUDIT.md`. En esta pasada quedan
**0 errores de C1** (remisiones cruzadas), **0 de C4** (apéndices inexistentes),
**0 de C5** (numeración antigua) y **0 de C8** (anclas rotas). Sigue pendiente la
bibliografía sin verificar (C2), que requiere verificación documental fuente por
fuente y no puede cerrarse con herramientas.

## Pasada anterior (25 de septiembre de 2026)

Resultados de `tools/validate_editions.py`:

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

