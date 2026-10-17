#!/usr/bin/env python3
"""Genera el contenido del sitio (Starlight) a partir de content/<lang>/<volN>/.

El Markdown de content/ es la ÚNICA fuente: Pandoc lo compone en PDF/EPUB y este
script lo adapta a la web SIN modificarlo (el resultado va a web/src/content/docs/,
que no se versiona). Qué adapta:
  · añade el frontmatter que exige Starlight (título = primer «# …», orden del menú);
  · quita ese H1 del cuerpo (Starlight ya pinta el título);
  · convierte las anclas de Pandoc «### {#ref-x}» en <a id="ref-x">;
  · reescribe las citas «(#ref-x)» -> «/<lang>/<vol>/back/<referencias>/#ref-x»
    (en el libro es un único documento; en la web, cada capítulo es una página);
  · copia las imágenes a web/public/img/<lang>/<vol>/ y reescribe sus rutas;
  · genera la portada de cada volumen y la portada de cada idioma.
Solo biblioteca estándar.
"""
import json
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WEB = ROOT / 'web'
DOCS = WEB / 'src' / 'content' / 'docs'
IMG = WEB / 'public' / 'img'
VOLS = json.loads((ROOT / 'tools' / 'vols.json').read_text(encoding='utf-8'))
SITE = json.loads((WEB / 'site.config.json').read_text(encoding='utf-8'))
LANGS = ('es', 'en')

# (archivo de origen, slug ES (referencia), slug de URL) — orden = orden del menú.
# La URL usa el MISMO slug en ES y EN: así el selector de idioma de Starlight enlaza
# página con página y no se generan páginas de «respaldo» duplicadas.
FRONT = [
    ('03_hoja_creditos', 'ficha-tecnica', 'imprint'),
    ('02b_dedicatoria', 'dedicatoria', 'dedication'),
    ('01b_sinopsis', 'sinopsis', 'synopsis'),
    ('02c_prologo', 'prologo', 'foreword'),
    ('02d_prefacio', 'prefacio', 'preface'),
    ('04b_guia_de_lectura', 'guia-de-lectura', 'reading-guide'),
    ('04c_nota_vigencia', 'nota-de-vigencia', 'currency-note'),
    ('05_cuaderno_de_lectura_critica', 'lectura-critica', 'critical-reading'),
    ('06_glosario', 'glosario', 'glossary'),
    ('07_indice_de_consulta_rapida', 'consulta-rapida', 'quick-reference'),
]
# Los dos «índices de trabajo» del manuscrito no se publican (igual que en el libro).
SKIP = {'02_portadilla', '04_tabla_contenido'}
BACK = [  # (ruta relativa al volumen, slug ES, slug EN)
    ('front-matter/08_apendice_b_precios.md', 'apendice-b', 'appendix-b'),
    ('estado-del-arte/estado-del-arte.md', 'estado-del-arte', 'state-of-the-art'),
    ('referencias/referencias.md', 'referencias', 'references'),
]
UI = {
    'es': dict(read='Empezar a leer', home_h='Volúmenes', toc='Contenido', dl='Descargas',
               dl_pdf='PDF de lectura', dl_epub='EPUB', buy='Apoyar el proyecto / ediciones empaquetadas',
               tagline='Arte de orquestar agentes de IA · acceso abierto',
               front='Preliminares', chapters='Capítulos', back='Apéndices y referencias'),
    'en': dict(read='Start reading', home_h='Volumes', toc='Contents', dl='Downloads',
               dl_pdf='Reading PDF', dl_epub='EPUB', buy='Support the project / packaged editions',
               tagline='The art of orchestrating AI agents · open access',
               front='Front matter', chapters='Chapters', back='Appendices & references',),
}
warnings = []


def warn(msg):
    warnings.append(msg)
    print('!', msg, file=sys.stderr)


def yq(s):
    return json.dumps(s, ensure_ascii=False)


def meta(path, key):
    m = re.search(rf'^{key}:\s*"?([^"\n]+?)"?\s*$', path.read_text(encoding='utf-8'), re.M)
    return m.group(1).strip() if m else ''


def split_h1(text, fallback):
    """(título, cuerpo sin el primer H1)."""
    lines = text.lstrip('\ufeff').splitlines()
    for i, line in enumerate(lines):
        if line.startswith('# '):
            return line[2:].strip(), '\n'.join(lines[:i] + lines[i + 1:]).lstrip('\n')
        if line.strip():
            break
    return fallback, text


def adapt(body, lang, vol, refs_slug):
    base = f'/{lang}/{vol}'
    # Anclas de Pandoc en la bibliografía: «### {#ref-x}» (encabezado vacío con id).
    body = re.sub(r'^#{1,6}\s*\{#(ref-[\w.:-]+)\}\s*$', r'<a id="\1"></a>', body, flags=re.M)
    # Citas internas del libro -> página de referencias.
    body = re.sub(r'\]\(#(ref-[\w.:-]+)\)', rf']({base}/back/{refs_slug}/#\1)', body)
    # Imágenes: imagenes/<carpeta>/x.png -> /img/<lang>/<vol>/<carpeta>/x.png
    body = re.sub(r'\]\((?:\./)?imagenes/', f'](/img/{lang}/{vol}/', body)
    return body


def write(path, title, body, order=None, extra=''):
    path.parent.mkdir(parents=True, exist_ok=True)
    fm = ['---', f'title: {yq(title)}']
    if order is not None:
        fm += ['sidebar:', f'  order: {order}']
    if extra:
        fm.append(extra.rstrip())
    fm.append('---\n')
    path.write_text('\n'.join(fm) + '\n' + body.rstrip() + '\n', encoding='utf-8')


def sync_volume(lang, vol):
    src = ROOT / 'content' / lang / vol
    if not src.is_dir():
        return None
    ui = UI[lang]
    i = 1  # slug de URL común a ambos idiomas
    refs_slug = BACK[2][1 + i]
    out = DOCS / lang / vol
    first_chapter = None

    for n, (stem, *slugs) in enumerate(FRONT):
        f = src / 'front-matter' / f'{stem}.md'
        if f.exists():
            title, body = split_h1(f.read_text(encoding='utf-8'), stem)
            write(out / 'front' / f'{slugs[i]}.md', title, adapt(body, lang, vol, refs_slug), n)
    known = {s for s, *_ in FRONT} | SKIP | {'08_apendice_b_precios'}
    for f in sorted((src / 'front-matter').glob('*.md')):
        if f.stem not in known:
            warn(f'{lang}/{vol}: front-matter/{f.name} no está en el mapa de web_sync (no se publica)')

    for f in sorted((src / 'manuscrito' / 'capitulos').glob('*.md')):
        num = f.stem.split('_')[0]
        title, body = split_h1(f.read_text(encoding='utf-8'), f.stem)
        write(out / 'chapters' / f'{num}.md', title, adapt(body, lang, vol, refs_slug), int(num))
        first_chapter = first_chapter or f'/{lang}/{vol}/chapters/{num}/'

    for n, (rel, *slugs) in enumerate(BACK):
        f = src / rel
        if f.exists():
            title, body = split_h1(f.read_text(encoding='utf-8'), rel)
            write(out / 'back' / f'{slugs[i]}.md', title, adapt(body, lang, vol, refs_slug), n)

    # Imágenes (y portada; la EN reutiliza el arte ES hasta tener el propio)
    img_src = src / 'manuscrito' / 'imagenes'
    if img_src.is_dir():
        shutil.copytree(img_src, IMG / lang / vol, dirs_exist_ok=True)
    cover = next((p for p in (src / 'front-matter' / '01_cubierta_delantera.png',
                              ROOT / 'content' / 'es' / vol / 'front-matter' / '01_cubierta_delantera.png')
                  if p.exists()), None)
    if cover:
        (IMG / lang / vol).mkdir(parents=True, exist_ok=True)
        shutil.copy(cover, IMG / lang / vol / 'cover.png')

    # Portada del volumen
    md = src / 'front-matter' / f'metadata_{lang}.yaml'
    title = f"{VOLS['series'][lang]} — {VOLS['titles'][lang][vol]}"
    subtitle = meta(md, 'subtitle') if md.exists() else ''
    slug = VOLS['slugs'][vol]
    rel = f"{SITE['repo']}/releases/latest/download"
    parts = [f'![{title}](/img/{lang}/{vol}/cover.png)\n', f'*{subtitle}*\n' if subtitle else '']
    if first_chapter:
        parts.append(f'<p><a class="cs-btn" href="{first_chapter}">{ui["read"]} →</a></p>\n')
    if SITE.get('downloadsFromReleases'):
        parts.append(f'**{ui["dl"]}:** [{ui["dl_pdf"]}]({rel}/{slug}--{lang}--lectura-6x9--con-portada.pdf) · '
                     f'[{ui["dl_epub"]}]({rel}/{slug}--{lang}--epub--con-portada.epub)\n')
    if not str(SITE['buyUrl']).startswith('PENDIENTE'):
        parts.append(f'<p><a class="cs-btn cs-btn-alt" href="{SITE["buyUrl"]}" rel="noopener">{ui["buy"]}</a></p>\n')
    write(out / 'index.md', title, '\n'.join(parts), 0,
          extra='description: ' + yq(subtitle or title))
    return title, subtitle, f'/{lang}/{vol}/'


def sync_lang_home(lang, cards):
    ui = UI[lang]
    lis = '\n'.join(f'<li><a href="{url}"><strong>{t}</strong></a><br/><small>{s}</small></li>'
                    for t, s, url in cards)
    body = f'<ul class="cs-vols">\n{lis}\n</ul>\n'
    write(DOCS / lang / 'index.md', VOLS['series'][lang], f'{ui["tagline"]}\n\n## {ui["home_h"]}\n\n{body}',
          extra='template: doc\ndescription: ' + yq(ui['tagline']))


def main():
    if DOCS.exists():
        shutil.rmtree(DOCS)
    if IMG.exists():
        shutil.rmtree(IMG)
    for lang in LANGS:
        cards = [c for c in (sync_volume(lang, v) for v in VOLS['slugs']) if c]
        if cards:
            sync_lang_home(lang, cards)
    pages = sum(1 for _ in DOCS.rglob('*.md'))
    print(f'web_sync: {pages} páginas, {len(warnings)} avisos')


if __name__ == '__main__':
    main()
