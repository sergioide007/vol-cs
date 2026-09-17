# Validación de las ediciones — corrección del índice (17 de septiembre de 2026)

## Incidencia corregida

Se eliminaron las filas sin título (puntos y folios) que aparecían debajo de
«Referencias». Los encabezados vacíos `### {#ref-…}` se convierten en anclas
sin encabezado mediante `/workspaces/vol-cs/tools/lua/reference-anchors.lua`.
La entrada «Referencias» permanece como última entrada del índice.
No se modificó el contenido bibliográfico en esta corrección.

## Resultados sobre las ediciones reconstruidas

Construcción completa: código de salida **0**, 16 entregables regenerados.

| Volumen | Páginas interior / lectura | Filas vacías (ambos PDF) | EPUBCheck | Glifos ausentes | Texto fuera de caja horizontal | Overfull hbox |
|---|---:|---:|---:|---:|---:|---:|
| 1 — Fundamentos | 160 / 161 | 0 | 2/2 | 0 | 0 | 0 |
| 2 — Frontera y aplicaciones | 334 / 335 | 0 | 2/2 | 0 | 0 | 2 |
| 3 — Madurez organizacional | 292 / 293 | 0 | 2/2 | 0 | 0 | 3 |
| 4 — Patrones de escala | 260 / 261 | 0 | 2/2 | 0 | 0 | 1 |

- Índices LaTeX: ninguna entrada vacía; terminan en «Referencias».
- Los ocho PDF no contienen líneas formadas exclusivamente por puntos y folios.
- Los cuatro interiores mantienen 432 × 648 pt y fuentes incrustadas.
- Los ocho EPUB pasan EPUBCheck. Se comprobaron 56/73/72/44 anclas
  bibliográficas por volumen y 118/71/85/57 enlaces de citas por variante EPUB:
  todos tienen destino existente.
- Las anclas con tildes se codifican en LaTeX; los destinos
  `ref-ramuxedrez-rueda2024` y `ref-muxe1rquez0000` se confirmaron con `pdfinfo -dests`.
- Cuatro pruebas de regresión pasan, incluida una compilación PDF que reproduce
  la fila vacía sin filtro y comprueba su desaparición con el filtro.
- Preflight actualizado en `/workspaces/vol-cs/dist/PREFLIGHT.json`.
  **Su salida es 1**, no 0: permanece estricto ante los seis avisos Overfull hbox
  (0,137–1,212 pt), aunque no se detectan palabras fuera de la caja horizontal.
- El log del volumen 4 también contiene tres avisos Overfull vbox; el preflight
  actual no valida desbordes verticales. Requieren revisión visual y no quedan
  certificados por el resultado horizontal.

## Reproducción

```bash
python3 /workspaces/vol-cs/tools/test_reference_anchors.py
bash /workspaces/vol-cs/tools/build_editions.sh
python3 /workspaces/vol-cs/tools/validate_editions.py
```

El validador ahora detecta filas de puntos y folios sin título y devuelve
salida no nula si aparecen.

## Pendientes ajenos a esta corrección

- Depuración y comprobación documental de la bibliografía: hay residuos de
  BibTeX y referencias provisionales. La corrección del índice no los resuelve.
- Revisión visual, especialmente composición vertical, y prueba de impresión.
- ISBN reales por edición; los identificadores EPUB siguen siendo UUID provisionales.
- Cubierta de imprenta según proveedor y papel. Recalcular el lomo con los
  nuevos recuentos: 160/334/292/260 páginas.

La incidencia de las filas vacías está cerrada; esto no constituye aprobación
editorial integral ni autorización de imprenta.
