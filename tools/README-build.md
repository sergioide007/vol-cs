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
| Prólogo | `front-matter/02c_prologo.md` | tras la sinopsis, con folio propio en el índice |
| Prefacio | `front-matter/02d_prefacio.md` | tras el prólogo, con folio propio en el índice |
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

## 4. Formato y márgenes (lo importante para la imprenta)

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

## 5. Decisiones editoriales de la maquetación

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

## 6. Lo que falta antes de subir a las plataformas

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

## 7. Estructura de los archivos de apoyo

```
tools/
├─ build_editions.sh          Script principal (pandoc + XeLaTeX + poppler)
├─ epub.css                   Hoja de estilo del EPUB
├─ latex/
│  ├─ header-interior.tex     Cabeceras, folios, código, tablas, viudas
│  └─ cover-page.tex          Página de portada 6×9 para el PDF de lectura
└─ lua/
│  ├─ table-widths.lua        Ancho de columnas: evita desbordes de tabla
│  ├─ print-breaks.lua        Puntos de corte en celdas largas (solo PDF)
│  └─ reference-anchors.lua   Oculta del índice las anclas bibliográficas
├─ skill_cliches.py           Detector de clichés de IA (solo lectura)
├─ skill_aplicar.py           Aplicador del mapa curado (idempotente)
├─ lint_manuscript.py         Auditoría del manuscrito (9 comprobaciones)
├─ test_lint_manuscript.py    Regresión de la auditoría
├─ model-allowlist.txt        Familias de modelo admitidas en el cuerpo (C6)
└─ skills/anti-cliches-ia/
   └─ SKILL.md                Criterio editorial: qué es cliché y qué no
```

## 8. Integración continua

`.github/workflows/manuscrito.yml` ejecuta dos puertas independientes en cada
pull request:

- **manuscrito**: regresión de las herramientas, `lint_manuscript.py` (falla si
  queda algún error) y publicación del resumen de `dist/AUDIT.md` en la página
  de la ejecución.
- **ediciones**: `build_editions.sh`, `validate_editions.py` y la regresión de
  las anclas bibliográficas, con los PDF y EPUB adjuntos como artefacto.

## 9. Auditoría del manuscrito (`lint_manuscript.py`)

`validate_editions.py` comprueba que el PDF esté bien maquetado. No comprueba que
el libro se contradiga a sí mismo. Para eso está `lint_manuscript.py`, que lee el
manuscrito y falla igual que el validador:

```bash
python3 tools/lint_manuscript.py                    # informe + exit 1 si hay errores
python3 tools/lint_manuscript.py --vol vol4-patrones-de-escala
python3 tools/lint_manuscript.py --only C1 C3       # una familia de checks
python3 tools/lint_manuscript.py --quiet            # solo el resumen por stderr
```

Escribe `dist/AUDIT.md` (informe legible) y `dist/AUDIT.json` (para máquinas). Los
**errores** bloquean la composición; los **avisos** son el trabajo pendiente
registrado, no un defecto.

| ID | Qué comprueba | Severidad |
|---|---|---|
| C1 | Remisión cruzada a un capítulo que no existe, o sin etiqueta de volumen | error / aviso |
| C2 | Entrada bibliográfica que se declara no verificada | error |
| C3 | Párrafo con cifras sin marca `[D]` dato, `[E]` estimación, `[I]` ilustrativa | aviso |
| C4 | Apéndice citado que no existe, marcador `PENDIENTE`/`TODO` | error / aviso |
| C5 | Restos de la numeración global antigua («Parte IV», «caps. 76–79») | error |
| C6 | Identificador de modelo literal fuera de `tools/model-allowlist.txt` | aviso |
| C7 | Capítulo fuera del presupuesto de palabras (1.600–4.500) | aviso |
| C8 | Ancla `#ref-` sin entrada, o entrada nunca citada | error / aviso |
| C9 | Carpeta de imágenes que conserva la numeración antigua | aviso |
| C11 | Año de la cita distinto del año de la entrada | error |
| C12 | Palabra pegada a un identificador, fuera de código y comillas | aviso |
| C13 | Carácter no representable en las fuentes del libro (CJK) | error |
| C14 | Mayúscula en medio de palabra, fuera de código y comillas | aviso |
| C15 | Mención «Apellido (año)» en la prosa sin entrada en la bibliografía del volumen | aviso |

**C15, la comprobación que faltaba.** El libro cita obras clásicas dentro de la
frase («Cunningham (1992) articuló la metáfora de la deuda técnica») en lugar de
enlazarlas. Si el apellido no aparece en la bibliografía de ese volumen, el
lector no puede localizar la obra: la cita es irresoluble. Se busca el apellido
en el texto de la bibliografía y no en las anclas, porque lo que el lector
necesita es encontrar la obra, no adivinar el ancla. Se informa una vez por
apellido y archivo: una sola ficha resuelve todas las menciones.

No cuenta como cita el año que cierra un rótulo en negrita, ni la norma con su
año («Ley de Seguridad de Datos (2021)»), ni los lugares, herramientas, modelos
y fenómenos que llevan año sin ser fuentes (`MENTION_OK`). Las instituciones y
las revistas **sí** se informan: citar «la revisión sistemática de Frontiers
(2026)» sin autor ni título es una atribución que el lector no puede seguir.

**C6 y el apéndice B.** Los precios y los nombres de modelo viven solo en
`front-matter/08_apendice_b_precios.md`, con su fecha de corte. `model-allowlist.txt`
declara qué familias se aceptan en el cuerpo del texto; por eso el apéndice se
puede actualizar sin reescribir capítulos.

**Presupuesto de palabras** (C7): se cuentan las palabras de prosa, sin contar los
bloques de código. Es un aviso, no un error: un capítulo corto puede ser
deliberado, y uno largo, un problema de estructura.

**Regresión**: `python3 tools/test_lint_manuscript.py` verifica las reglas de
detección y comprueba que toda remisión a un número inexistente produce un
hallazgo.

## 10. Pasador anti-clichés de IA

Antes de componer, la prosa de los cuatro volúmenes pasa por el skill
`tools/skills/anti-cliches-ia/SKILL.md`, que elimina el metadiscurso enfático
(«Merece énfasis que…», «Conviene señalar…», «Cabe destacar…») y los tics de
escritura tipo Wikipedia, **sin tocar tablas, código, fórmulas ni citas**.

```bash
python3 tools/skill_cliches.py --detall   # inventario (no modifica nada)
python3 tools/skill_aplicar.py --check     # simulación: cuántas sustituciones faltan
python3 tools/skill_aplicar.py             # aplica el mapa curado
```

El aplicador es **idempotente**: si la versión nueva ya está en el archivo,
cuenta la sustitución como hecha en lugar de fallar. Si una frase no se
encuentra ni en su forma antigua ni en la nueva, la reporta y aborta para que
el editor la revise a mano.
