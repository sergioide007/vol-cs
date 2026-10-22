#!/usr/bin/env python3
"""Genera la web de publicación por volúmenes (hub + una página por volumen e idioma).

    python3 tools/render_info_site.py --info ../info-codigo-sintetico-main --out dist/info-site

Fuente única: legal/registry.yaml (vía render_legal.public_json). Nada se escribe a mano:
 · ISBN y Depósito Legal aparecen solo cuando ya están en el registro (si no, «en trámite»);
 · los botones de compra aparecen solo cuando hay enlace (kdp / google_play / lulu);
 · el CSS es el del libro 1 (se extrae de su index.html) para que el diseño sea el mismo;
 · el libro 1 se conserva intacto en /libro-1/ (solo se ajustan rutas y URL canónica).
Salida: index.html (ES), en/index.html, vol1..4/, en/vol1..4/, libro-1/, assets/.
"""
import argparse
import html
import importlib.util
import json
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('rl', ROOT / 'tools/render_legal.py')
rl = importlib.util.module_from_spec(spec)
spec.loader.exec_module(rl)

T = {
    'es': dict(lang='es', locale='es_PE', hub_h='Serie «Código Sintético»', hub_sub='Cuatro volúmenes sobre arquitectura, economía y criterio de ingeniería para sistemas multiagente.',
               read='Leer en línea (gratis)', soon='En trámite de registro', open_vol='Ver el volumen', ficha='Ficha técnica editorial',
               title='Título', authors='Autores', publisher='Autor-editor', place='Lugar de edición', edition='Edición', contact='Contacto y licencias',
               dl='Depósito Legal', dl_pending='en trámite en la Biblioteca Nacional del Perú (SIRNADEL)', isbn='ISBN', isbn_pending='en trámite (Agencia Peruana del ISBN)',
               lic='Licencia', buy='Ediciones empaquetadas', buy_none='Las ediciones empaquetadas estarán disponibles al completar el registro legal.',
               other='English edition', other_url='en/', book1='El libro de entrada (volumen único, 2026)', back='Todos los volúmenes',
               fmt={'epub': 'EPUB', 'pdf': 'PDF', 'print': 'Impreso'}, store={'kdp': 'Amazon KDP', 'google_play': 'Google Play Books', 'lulu': 'Lulu'},
               ed_word='Edición {n} · {when}', legal_note='Este sitio informa la edición digital; la lectura en línea es gratuita.'),
    'en': dict(lang='en', locale='en_US', hub_h='“Synthetic Code” series', hub_sub='Four volumes on architecture, economics and engineering judgment for multi-agent systems.',
               read='Read online (free)', soon='Legal registration in progress', open_vol='View volume', ficha='Publishing details',
               title='Title', authors='Authors', publisher='Author-publisher', place='Place of publication', edition='Edition', contact='Contact and licensing',
               dl='Legal deposit', dl_pending='in progress at the National Library of Peru (SIRNADEL)', isbn='ISBN', isbn_pending='in progress (Peruvian ISBN Agency)',
               lic='License', buy='Packaged editions', buy_none='Packaged editions will be available once legal registration is complete.',
               other='Edición en español', other_url='../', book1='The companion book (single volume, 2026, Spanish)', back='All volumes',
               fmt={'epub': 'EPUB', 'pdf': 'PDF', 'print': 'Print'}, store={'kdp': 'Amazon KDP', 'google_play': 'Google Play Books', 'lulu': 'Lulu'},
               ed_word='Edition {n} · {when}', legal_note='This site describes the digital edition; online reading is free.'),
}
e = html.escape


def head(t, title, desc, url, css, extra=''):
    return (f'<!DOCTYPE html>\n<html lang="{t["lang"]}">\n<head>\n<meta charset="utf-8">\n'
            '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
            f'<title>{e(title)}</title>\n<meta name="description" content="{e(desc)}">\n'
            f'<link rel="canonical" href="{url}">\n<meta property="og:title" content="{e(title)}">\n'
            f'<meta property="og:locale" content="{t["locale"]}">\n{extra}<style>\n{css}\n</style>\n</head>\n<body>\n')


def top(t, prefix, other):
    return (f'<header class="top"><div class="wrap"><a class="brand" href="{prefix}">Código <span>Sintético</span></a>'
            f'<nav><a href="{other}">{t["other"]}</a></nav></div></header>\n<main>\n')


FOOT = '</main>\n<footer><div class="wrap"><p>{p} · {a} · Lima, Perú</p><p>{n}</p></div></footer>\n</body>\n</html>\n'


def when_text(lang, d):
    return rl.edition_line(lang, {'edition': str(d['edition']), 'edition_date': d['edition_date'] or ''}).split('·')[-1].strip() \
        if d['edition_date'] else None


def vol_page(t, lang, vol, d, pub, base, site, css):
    lang_prefix = '' if lang == 'es' else 'en/'
    url = f'{base}/{lang_prefix}{vol}/'
    names = ', '.join(pub['authors'])
    isbn_rows = ''.join(f'<div><dt>{t["isbn"]} ({t["fmt"][k]})</dt><dd>{e(v)}</dd></div>' for k, v in d['isbn'].items()) \
        or f'<div><dt>{t["isbn"]}</dt><dd>{t["isbn_pending"]}</dd></div>'
    dl = (f'Hecho el Depósito Legal en la Biblioteca Nacional del Perú N.º {d["deposito_legal"]}'
          if d['deposito_legal'] else t['dl_pending'])
    when = when_text(lang, d)
    ed = t['ed_word'].format(n=d['edition'], when=when) if when else t['soon']
    stores = ''.join(f'<a class="btn primary" href="{e(u)}" rel="noopener">{t["store"][k]}</a>' for k, u in d['links'].items())
    buy = f'<div class="btns">{stores}</div>' if stores else f'<p class="note">{t["buy_none"]}</p>'
    reader = f'{site}/{lang}/{vol}/'
    sub = d['title']
    ld = {'@context': 'https://schema.org', '@type': 'Book', 'name': f'{rl.VOLS["series"][lang]}: {sub}', 'inLanguage': lang,
          'author': [{'@type': 'Person', 'name': a} for a in pub['authors']], 'publisher': {'@type': 'Person', 'name': pub['publisher']},
          'bookEdition': str(d['edition']), 'url': url, 'license': pub['license']['url'],
          'image': f'{base}/assets/covers/{lang}-{vol}.jpg'}
    if d['edition_date']:
        ld['datePublished'] = d['edition_date']
    ld['workExample'] = [{'@type': 'Book', 'bookFormat': 'https://schema.org/EBook', 'isbn': v,
                          'encodingFormat': {'epub': 'application/epub+zip', 'pdf': 'application/pdf'}.get(k, 'Paperback')}
                         for k, v in d['isbn'].items()]
    out = head(t, f'{rl.VOLS["series"][lang]} · {sub}', t['hub_sub'], url, css,
               f'<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>\n')
    out += top(t, '/' if lang == 'es' else '/en/', f'/en/{vol}/' if lang == 'es' else f'/{vol}/')
    out += (f'<div class="hero"><div class="wrap"><div><div class="eyebrow">{e(rl.VOLS["series"][lang])} · {vol.upper().replace("VOL","Vol. ")}</div>'
            f'<h1>{e(sub)}</h1><p class="author">{e(names)}</p><div class="btns"><a class="btn primary" href="{reader}">{t["read"]}</a></div></div>'
            f'<div class="cover"><img src="/assets/covers/{lang}-{vol}.jpg" alt="{e(sub)}" width="600" height="900"></div></div></div>\n'
            f'<section id="ficha" class="alt"><div class="wrap"><h2>{t["ficha"]}</h2><div class="data"><div class="card"><dl>'
            f'<div><dt>{t["title"]}</dt><dd>{e(rl.VOLS["series"][lang])}: {e(sub)}</dd></div>'
            f'<div><dt>{t["authors"]}</dt><dd>{e(names)}</dd></div><div><dt>{t["publisher"]}</dt><dd>{e(pub["publisher"])}</dd></div>'
            f'<div><dt>{t["place"]}</dt><dd>Lima, Perú</dd></div><div><dt>{t["edition"]}</dt><dd>{e(ed)}</dd></div></dl></div>'
            f'<div class="card"><dl>{isbn_rows}<div><dt>{t["dl"]}</dt><dd>{e(dl)}</dd></div>'
            f'<div><dt>{t["lic"]}</dt><dd><a href="{pub["license"]["url"]}">{e(pub["license"]["name"])}</a></dd></div></dl></div></div>'
            f'<p class="note">{t["legal_note"]}</p></div></section>\n'
            f'<section id="comprar"><div class="wrap"><h2>{t["buy"]}</h2>{buy}</div></section>\n')
    return out + FOOT.format(p=e(rl.VOLS['series'][lang]), a=e(pub['publisher']), n=t['legal_note'])


def hub_page(t, lang, pub, base, site, css):
    cards = ''
    for vol, langs in pub['volumes'].items():
        d = langs[lang]
        cards += (f'<div class="card"><img src="/assets/covers/{lang}-{vol}.jpg" alt="" width="300" height="450" style="width:100%;height:auto;border-radius:10px">'
                  f'<h3>{vol.upper().replace("VOL", "Vol. ")} · {e(d["title"])}</h3>'
                  f'<p>{"ISBN: " + ", ".join(d["isbn"].values()) if d["isbn"] else t["soon"]}</p>'
                  f'<p><a href="{vol}/">{t["open_vol"]} →</a></p></div>')
    book1 = f'<p class="note"><a href="/libro-1/">{t["book1"]}</a> · <a href="{site}/{lang}/">{t["read"]}</a></p>'
    url = f'{base}/' + ('' if lang == 'es' else 'en/')
    out = head(t, t['hub_h'], t['hub_sub'], url, css)
    out += top(t, '/' if lang == 'es' else '/en/', '/en/' if lang == 'es' else '/')
    out += (f'<div class="hero"><div class="wrap"><div><div class="eyebrow">{", ".join(pub["authors"])}</div><h1>{t["hub_h"]}</h1>'
            f'<p class="sub">{t["hub_sub"]}</p></div></div></div>\n<section><div class="wrap"><h2>{t["back"]}</h2>'
            f'<div class="grid">{cards}</div>{book1}</div></section>\n')
    return out + FOOT.format(p=e(rl.VOLS['series'][lang]), a=e(pub['publisher']), n=t['legal_note'])


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--info', required=True, help='carpeta del repo info-codigo-sintetico (libro 1)')
    ap.add_argument('--out', default=str(ROOT / 'dist/info-site'))
    ap.add_argument('--base', default='https://info-codigo-sintetico.specsolid.com')
    ap.add_argument('--covers', default=str(ROOT / 'dist'), help='dist/ con <lang>/covers/*-cover-300ppp.jpg')
    args = ap.parse_args()
    info, out, base = Path(args.info), Path(args.out), args.base.rstrip('/')
    reg, site_cfg = rl.load()
    pub = rl.public_json(reg, site_cfg)
    site = site_cfg['url'].rstrip('/')
    src = (info / 'index.html').read_text(encoding='utf-8')
    css = re.search(r'<style>(.*?)</style>', src, re.S).group(1).strip()
    css += '\n.cover img{width:100%;height:auto;border-radius:12px}\nh3{margin:.6em 0 .2em;font-size:1.05rem}'

    if out.exists():
        shutil.rmtree(out)
    (out / 'assets/covers').mkdir(parents=True)
    # Libro 1 intacto: solo se reubican rutas y URL canónica.
    b1 = out / 'libro-1'
    b1.mkdir()
    page = src.replace('href="assets/', 'href="../assets/').replace('src="assets/', 'src="../assets/')
    page = page.replace('rel="canonical" href="https://info-codigo-sintetico.specsolid.com/"',
                        f'rel="canonical" href="{base}/libro-1/"')
    (b1 / 'index.html').write_text(page, encoding='utf-8')
    shutil.copytree(info / 'assets', out / 'assets', dirs_exist_ok=True)
    for name in ('CNAME', '.nojekyll'):
        if (info / name).exists():
            shutil.copy(info / name, out / name)

    try:
        from PIL import Image
    except ImportError:
        Image = None
    for lang in ('es', 'en'):
        for vol, slug in rl.VOLS['slugs'].items():
            jpg = Path(args.covers) / lang / 'covers' / f'{slug}-cover-300ppp.jpg'
            dst = out / 'assets/covers' / f'{lang}-{vol}.jpg'
            if jpg.is_file() and Image:
                Image.open(jpg).convert('RGB').resize((600, 900)).save(dst, 'JPEG', quality=84, optimize=True)
    n = 0
    for lang in ('es', 'en'):
        t, root = T[lang], out if lang == 'es' else out / 'en'
        root.mkdir(exist_ok=True)
        (root / 'index.html').write_text(hub_page(t, lang, pub, base, site, css), encoding='utf-8')
        for vol, langs in pub['volumes'].items():
            (root / vol).mkdir(exist_ok=True)
            (root / vol / 'index.html').write_text(vol_page(t, lang, vol, langs[lang], pub, base, site, css), encoding='utf-8')
            n += 1
    (out / 'robots.txt').write_text(f'User-agent: *\nAllow: /\nSitemap: {base}/sitemap.xml\n', encoding='utf-8')
    urls = [f'{base}/', f'{base}/en/', f'{base}/libro-1/'] + [f'{base}/{p}{v}/' for p in ('', 'en/') for v in pub['volumes']]
    (out / 'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
                                     + ''.join(f'<url><loc>{u}</loc></url>\n' for u in urls) + '</urlset>\n', encoding='utf-8')
    print(f'{n} páginas de volumen + 2 hubs + libro-1 → {out}')


if __name__ == '__main__':
    main()
