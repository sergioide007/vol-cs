# Guía de producción editorial — serie «Código Sintético»

Documento para el autor/editor. Explica cómo generar las ediciones listas para
publicar y por qué los archivos salen con las medidas que salen.

## 1. Qué genera `tools/build_editions.sh`

Por cada volumen crea cuatro archivos en `dist/<volumen>/`:

| Archivo | Para qué sirve | Destino |
|---|---|---|
| `<vol>--interior-6x9--sin-caratula.pdf` | **Archivo de imprenta sin carátula** (texto del libro). Es el que se sube como «manuscrito»/«interior». | KDP (tapa blanda y dura), Lulu, IngramSpark |
| `<vol>--epub--con-portada.epub` | EPUB3 reflowable con cubierta embebida | KDP Kindle, Lulu (ebook), Apple Books, Kobo, Google Play |
| `<vol>--epub--sin-portada.epub` | EPUB3 sin cubierta embebida (manuscrito) | Plataformas que exigen el texto sin cubierta |
| `<vol>--lectura-6x9--con-portada.pdf` | PDF de difusión directa (portada + interior) | Web propia, prensa, lectores |

Además escribe `dist/BUILD-REPORT.md` con paginación, tamaño de página, lomo,
fuentes incrustadas y avisos de desbordes.

## 2. Páginas preliminares de cada volumen

Cada volumen incluye, en este orden:

| Pieza | Archivo fuente | Dónde aparece |
|---|---|---|
| Portada (cubierta delantera) | `front-matter/01_cubierta_delantera.png` | PDF de lectura (p. 1) y cubierta embebida del EPUB con portada |
| Portadilla (página de título interior) | generada desde `metadata_es.yaml` | PDF interior (p. 1), sin numerar |
| Hoja de créditos | `front-matter/03_hoja_creditos.md` | tras la portadilla, sin numerar |
| Dedicatoria | `front-matter/02b_dedicatoria.md` | tras los créditos, sin numerar |
| Sinopsis (texto de contracubierta y ficha de tienda) | `front-matter/01b_sinopsis.md` + campo `description` de `metadata_es.yaml` | interior (tras la dedicatoria) y metadatos del EPUB |
| Prólogo | `front-matter/02c_prologo.md` | tras la sinopsis, sin numerar |
| Guía de lectura, nota de vigencia, cuaderno crítico, glosario, índice rápido | `04b/04c/05/06/07` | cuerpo preliminar, con folios en el índice |
| Índice generado por el compositor | automático (`--toc`) | con folios reales |

`02_portadilla.md` y `04_tabla_contenido.md` son índices de trabajo del
manuscrito y **no se componen** (evitan duplicar la portadilla y el índice).

## 3. Ejecución

```bash
bash tools/build_editions.sh                 # los cuatro volúmenes
bash tools/build_editions.sh vol1-fundamentos
```

Requisitos (ya instalados en este entorno):

```bash
sudo apt-get install -y pandoc texlive-xetex texlive-latex-recommended \
  texlive-latex-extra texlive-lang-spanish texlive-fonts-recommended \
  fonts-texgyre fonts-dejavu fonts-liberation poppler-utils
```

## 3. Formato y márgenes (lo importante para la imprenta)

El formato final (*trim*) es **6 × 9 pulgadas (15,24 × 22,86 cm)**, pero la
**caja de texto es menor que el trim** porque hay que respetar los márgenes:
la encuadernación, el lomo y la guillotina necesitan espacio libre.

| Parámetro | Valor aplicado |
|---|---|
| Trim | 6,00 × 9,00 in |
| Margen interior (lomo / *gutter*) | **0,875 in** (2,22 cm) |
| Margen exterior | **0,625 in** (1,59 cm) |
| Margen superior | **0,75 in** (1,91 cm) |
| Margen inferior | **0,75 in** (1,91 cm) |
| **Caja de texto** | **4,5 × 7,5 in (11,43 × 19,05 cm)** |
| Sangrado (*bleed*) | no se usa (ningún elemento llega al borde) |

**Por qué estos valores son válidos en las dos plataformas y las dos
encuadernaciones:**

- *KDP tapa blanda*: exige mínimo 0,25 in en exterior/superior/inferior y un
  interior (*gutter*) que crece con la paginación: 0,375 in (24–150 págs.),
  0,5 in (151–300), 0,625 in (301–500), 0,75 in (501–700), 0,875 in (701–828).
  Con 0,875 in de lomo cumplimos hasta 828 páginas.
- *KDP tapa dura*: formato 6 × 9 admitido entre **75 y 550 páginas**; exige al
  menos 0,5 in de margen en todos los lados. Cumplimos con holgura.
- *Lulu*: mínimo 0,5 in en todos los lados. Cumplimos.

> El script comprueba la paginación real y, si un volumen exigiera más lomo del
> aplicado, **recompone el PDF automáticamente** con el margen que KDP pide.

## 4. Decisiones editoriales de la maquetación

1. **Índice generado por el compositor.** Se usa el índice automático con
   folios reales; el archivo `04_tabla_contenido.md` es un índice de trabajo del
   manuscrito y **no se incluye** en el libro (evita duplicar el índice).
   El filtro `reference-anchors.lua` convierte los encabezados bibliográficos
   vacíos `### {#ref-…}` en anclas sin encabezado: conserva los enlaces de las
   citas, pero evita las filas de puntos y folios bajo «Referencias».
   Prueba de regresión: `python3 tools/test_reference_anchors.py`.
2. **Portadilla desde metadatos.** La portada interior se genera con los datos de
   `metadata_es.yaml` (título, subtítulo, autor, año); no se usa
   `02_portadilla.md` para no duplicarla.
3. **Hoja de créditos antes del índice**, sin numerar: es el orden editorial
   correcto y lo permite `--include-before-body`.
4. **Márgenes espejados** (`twoside` + `openright`): el lomo alterna de lado en
   páginas pares e impares, obligatorio en encuadernación.
5. **Folio al margen exterior** y títulos corrientes (serie en páginas pares,
   capítulo en impares); aperturas de capítulo sin cabecera.
6. **Tipografía de libro**: TeX Gyre Pagella (11 pt) para el texto y DejaVu Sans
   Mono para el código, con cuerpo reducido y corte de línea para que el código
   no desborde la caja.
7. **Tablas ajustadas** mediante un filtro Lua que reparte el ancho entre
   columnas y permite el ajuste de línea.
8. **Imágenes**: se reducen si exceden la caja, nunca se amplían ni se deforman.
9. **EPUB sin fuentes incrustadas**: máxima compatibilidad con lectores; el
   usuario elige su tipografía.

## 5. Lo que falta antes de subir a las plataformas

- **ISBN**: los cuatro `metadata_es.yaml` llevan `PENDIENTE-ISBN-VOLx-ES`.
  Cada edición (EPUB y PDF, en su caso) requiere su propio ISBN.
- **Cubierta de imprenta (contracubierta + lomo + portada)**: el archivo de
  portada suelto sirve para el PDF de lectura y el EPUB, pero KDP y Lulu piden
  un PDF de cubierta de una sola página con sangrado y lomo exacto. Ancho de
  lomo = *páginas × 0,002252 in* (papel blanco) o *× 0,0025 in* (papel crema);
  use la calculadora de cubierta de la plataforma y su generador de plantillas
  para colocar el código de barras del ISBN.
- **Revisión de prueba**: descargar la prueba de KDP (*previewer*) o el
  *proof* impreso y comprobar el lomo adoptado antes de publicar.
- **Avisos `Overfull hbox`**: el informe indica cuántas líneas desbordan la caja.
  Unas pocas con tablas muy anchas son tolerables; si el número es alto,
  conviene partir esas tablas o reducir columnas en el manuscrito.

## 6. Estructura de los archivos de apoyo

```
tools/
├─ build_editions.sh          Script principal (pandoc + XeLaTeX + poppler)
├─ epub.css                   Hoja de estilo del EPUB
├─ latex/
│  ├─ header-interior.tex     Cabeceras, folios, código, tablas, viudas
│  └─ cover-page.tex          Página de portada 6×9 para el PDF de lectura
└─ lua/
   └─ table-widths.lua        Ancho de columnas: evita desbordes de tabla
```
