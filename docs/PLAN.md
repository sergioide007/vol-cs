# Plan de migración — Código Sintético a Docs-as-Code (Open Access)

Probado sobre una copia de tu repo: migración de carpetas, 51 tests (el único que falla,
`test_pdf_index_before_and_after`, también falla en tu original en un entorno sin TeX completo),
lint ES/EN, build real de Vol. 1 EN (190 págs., 2 EPUB + 2 PDF), sitio Starlight de 277 páginas
con 40 517 enlaces internos y todas las citas `#ref-*` resueltas.

## 0. Hallazgos del análisis (léelos primero)

| # | Hallazgo | Acción |
|---|---|---|
| 1 | **`.git/config` contiene un token personal de GitHub (`ghp_…`) en la URL del remoto.** Viaja dentro del .zip. | Revócalo hoy (GitHub → Settings → Developer settings → Tokens) y usa `git remote set-url origin https://github.com/sergioide007/vol-cs.git` o SSH. No lo vuelvas a incrustar. |
| 2 | El build solo compila **español** (`metadata_es.yaml`, `lang=es`, `toc-title=Índice` fijos). El EN nunca se ha compuesto. | `tools/build_editions.sh` parcheado: `LANG_CODE=es|en`. |
| 3 | `rights:` dice «Todos los derechos reservados» en los 8 YAML: contradice el acceso abierto. | Elegir licencia (§5) y cambiar `rights` + `LICENSE`. |
| 4 | Hay ~110 MB de PDF/EPUB (`dist/`, `*/output/`) versionados; el pack de git pesa 107 MB. | Salen del árbol (`.gitignore`); opcional reescribir historial con `git filter-repo`. |
| 5 | El lint tiene **30 errores C2** (referencias «sin verificar»: 15 en Vol. 2, 6 en Vol. 3, 6 en Vol. 4, 3 en Vol. 1). Tu CI actual ya fallaría. | Para un libro público de ciencia conviene resolverlos; el deploy no queda bloqueado hasta que pongas `LINT_BLOCKING=true`. |
| 6 | EN: 6 imágenes siguen con texto en español (`*_es.png` en `en/…/imagenes`) y no hay cubierta EN (se reutiliza la ES). | Traducir esos diagramas y la cubierta antes del release EN. |
| 7 | La hoja de créditos publica tu domicilio personal. | El domicilio se declara a la BNP; en el libro puedes usar una dirección postal/correo público. Se controla en `legal/registry.yaml`. |

## 1. Estructura del repositorio

```
vol-cs/
├─ content/                    ← ÚNICA fuente del texto (Pandoc y web leen de aquí)
│  ├─ es/vol1 … vol4/
│  │  ├─ front-matter/  (metadata_es.yaml, 01b_sinopsis.md … 08_apendice_b_precios.md, 01_cubierta_delantera.png)
│  │  ├─ manuscrito/{capitulos/, imagenes/}   ← imágenes junto al texto, con sufijo _es/_en
│  │  ├─ estado-del-arte/   └─ referencias/ (referencias.md, .bib)
│  └─ en/vol1 … vol4/        (misma forma, metadata_en.yaml)
├─ web/                        ← Astro Starlight (no contiene texto: se genera con tools/web_sync.py)
├─ tools/                      ← scripts: build_editions.sh, lint_manuscript.py, validate_editions.py,
│  │                             web_sync.py, render_legal.py, vols.json (registro de volúmenes)
│  ├─ latex/ (header-interior.tex, cover-page.tex, covers/)   ├─ lua/ (filtros Pandoc)
│  ├─ epub.css                ├─ covers/ (cubiertas)           └─ skills/, test_*.py
├─ legal/                      ← registry.yaml (ISBN, Depósito Legal) + plantillas de ficha técnica ES/EN
├─ docs/                       ← PLAN.md, INFORME_EDITORIAL.md, README-build.md
├─ .github/workflows/deploy.yml
├─ LICENSE (texto, CC) · LICENSE-CODE (MIT: tools/, web/, ejemplos de código)
└─ dist/ (ignorado)            ← dist/<lang>/<volN-slug>/…  y  dist/covers/
```

Decisiones: (a) **se mueve, no se reescribe**: dentro de cada volumen se conserva `manuscrito/capitulos|imagenes`,
así Pandoc, `resource-path` y las rutas de imágenes de los capítulos no cambian; (b) las plantillas LaTeX/Lua/CSS
siguen en `tools/` porque son compartidas por los 8 builds; (c) assets junto al volumen e idioma porque los
diagramas están traducidos; (d) `vols.json` mapea `vol1` ↔ `vol1-fundamentos` para nombres de archivo y cubiertas.

**Migración** (rama nueva, árbol limpio): `bash scripts/migrate-layout.sh` (admite `DRY=1`), luego copia
`tools/`, `web/`, `legal/`, `.github/`, `.gitignore`, `LICENSE*` del kit encima y ejecuta
`python3 -m unittest discover -s tools -p 'test_lint*.py'`.

## 2. Motor web: Astro Starlight (no Docusaurus)

Razones: i18n nativo por carpeta (`es/`, `en/`) con selector que enlaza página↔página; búsqueda Pagefind
por idioma sin servicio externo; build estático rápido (277 páginas en ~16 s); Markdown sin MDX
(tu texto tiene `<`, `{`, `[D]`…, que romperían MDX en Docusaurus); menú por volumen autogenerado.
Config: `web/astro.config.mjs`. Datos de negocio (URL de compra, precio, licencia): `web/site.config.json`.

`tools/web_sync.py` adapta sin tocar tu fuente: añade frontmatter (título = primer `#`), convierte `### {#ref-x}`
en `<a id>`, redirige `(#ref-x)` → página de referencias del volumen y reescribe rutas de imágenes.
URLs: `/es/vol1/chapters/01/`, `/en/vol1/back/references/#ref-brown2020` (slug común en ambos idiomas).

**Dominio**: en tu DNS crea `CNAME codigosintetico → sergioide007.github.io`; en el repo, Settings → Pages →
Source: *GitHub Actions* y Custom domain `codigosintetico.specsolid.com` (+ *Enforce HTTPS*).

## 3. Pipeline (`.github/workflows/deploy.yml`)

| Evento | Qué hace |
|---|---|
| PR | tests + lint + compila el sitio (sin publicar) |
| push a `main` | lo anterior + **despliega el sitio** |
| tag `vX.Y.Z` | además compila **PDF+EPUB de los 4 volúmenes en ES y EN** (matriz por idioma, valida con epubcheck) y crea el **Release** |
| manual | compila las ediciones sin Release |

Release: se adjuntan PDF de lectura y EPUB con portada (16 archivos + `SHA256SUMS.txt`). Los PDF de imprenta
(KDP) y EPUB sin portada quedan como artefacto del workflow (30 días). El Release nace **en borrador**; para
publicarlo automáticamente define la variable de repo `RELEASE_PUBLIC=true`.
En tags el build **falla si quedan ISBN/Depósito Legal en `PENDIENTE`** (`render_legal.py --strict`).

## 4. Ficha técnica y aviso legal

- `legal/registry.yaml` guarda ISBN por formato (EPUB, PDF, impreso) y Depósito Legal por volumen e idioma;
  `tools/render_legal.py` regenera `03_hoja_creditos.md` en ES y EN (plantillas `legal/ficha-tecnica.*.md.tpl`).
- Aviso del pie de la web: `web/src/legal.mjs` (ES/EN). El botón de apoyo/compra aparece cuando
  `buyUrl` en `site.config.json` deja de ser `PENDIENTE_URL_COMPRA`.
- BNP (verificado en gob.pe): el Depósito Legal se pide **antes de publicar** en SIRNADEL, es gratuito, y para
  e-books no se exige imprenta ni tiraje; la entrega digital se hace desde SIRNADEL y el certificado llega en
  hasta 20 días hábiles. El ISBN lo asigna la BNP al editor; cada formato/idioma necesita el suyo. La web no lleva ISBN.
  Confirma en SIRNADEL si las ediciones web+EPUB+PDF cuentan como una o varias publicaciones.

## 5. Decisiones que te tocan a ti

1. **Licencia.** Dejé CC BY-NC-SA 4.0 (texto) + MIT (código) como borrador: el «NC» protege la venta del formato
   empaquetado, pero su alcance es discutido. Alternativas: CC BY-NC-ND (sin derivadas) o CC BY (máxima apertura, pero
   cualquiera podría vender tu libro). Consúltalo con un abogado; esto no es asesoría legal. Descarga el texto
   legal completo de creativecommons.org y reemplaza `LICENSE`.
2. **Release público = descarga gratis.** Si el PDF/EPUB está en un Release público, nadie necesita pagar los 9.99 USD
   por *ese* archivo. Coherente con acceso abierto; el valor de pago queda en Kindle/impresión (con ISBN), bundles,
   cubiertas, soporte. Si prefieres no regalar el archivo, deja el Release en borrador y sube los archivos a tu tienda.
3. Activar `downloadsFromReleases` en `site.config.json` solo cuando el primer Release esté publicado (si no, 404).
