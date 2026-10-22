#!/usr/bin/env python3
"""Capa legal de la serie: una sola fuente (legal/registry.yaml) para todo lo que
exigen la BNP (Depósito Legal, ISBN) y las plataformas.

    python3 tools/render_legal.py                 # escribe 03_hoja_creditos.md de cada volumen/idioma
    python3 tools/render_legal.py --strict        # además FALLA si hay PENDIENTE o datos inválidos (releases)
    python3 tools/render_legal.py --check         # solo valida, no escribe nada
    python3 tools/render_legal.py --meta es vol1 epub OUT.yaml
                                                  # overlay de metadatos de Pandoc (ISBN, autores, derechos)
    python3 tools/render_legal.py --public OUT.json
                                                  # datos públicos por volumen para la web (sin datos personales)

Validaciones (siempre se informan; con --strict son errores):
  · marcadores PENDIENTE sin resolver;
  · ISBN-13 con dígito de control correcto, sin repetirse entre formatos/volúmenes/idiomas;
  · Depósito Legal con forma AAAA-NNNNN, y fecha de edición AAAA-MM (la BNP exige mes y año);
  · autores del registro = autores de la leyenda de cubierta (tools/covers/cover-design.json);
  · dominio del sitio = web/site.config.json.
Un lector YAML propio (el registro es plano) evita depender de PyYAML.
"""
import argparse
import json
import re
import sys
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
LEGAL = ROOT / 'legal'
VOLS = json.loads((ROOT / 'tools' / 'vols.json').read_text(encoding='utf-8'))

MONTHS = {
    'es': 'enero febrero marzo abril mayo junio julio agosto septiembre octubre noviembre diciembre'.split(),
    'en': 'January February March April May June July August September October November December'.split(),
}
ORDINALS = {
    'es': {1: 'Primera', 2: 'Segunda', 3: 'Tercera', 4: 'Cuarta', 5: 'Quinta'},
    'en': {1: 'First', 2: 'Second', 3: 'Third', 4: 'Fourth', 5: 'Fifth'},
}
# (clave en el registro, etiqueta de la tabla, formato corto)
FORMATS = (('isbn_epub', 'EPUB', 'epub'),
           ('isbn_pdf', 'PDF', 'pdf'),
           ('isbn_print', {'es': 'Impreso (bajo demanda)', 'en': 'Print (on demand)'}, 'print'))


# --------------------------------------------------------------------------- registro
def parse_registry(text):
    data = {}
    stack = [(-1, data)]
    for raw in text.splitlines():
        if raw.lstrip().startswith('#'):
            continue
        line = re.sub(r'\s+#\s.*$', '', raw).rstrip()
        if not line.strip():
            continue
        indent = len(line) - len(line.lstrip())
        key, _, val = line.strip().partition(':')
        val = val.strip()
        while stack and stack[-1][0] >= indent:
            stack.pop()
        parent = stack[-1][1]
        if val == '':
            parent[key] = {}
            stack.append((indent, parent[key]))
        elif val.startswith('{'):
            parent[key] = {k.strip(): v.strip().strip('"') for k, v in
                           (kv.split(':', 1) for kv in re.split(r',\s*(?=\w+\s*:)', val.strip('{} ')))}
        else:
            parent[key] = val.strip('"')
    return data


def load():
    reg = parse_registry((LEGAL / 'registry.yaml').read_text(encoding='utf-8'))
    site = json.loads((ROOT / 'web' / 'site.config.json').read_text(encoding='utf-8'))
    return reg, site


def meta(path, key):
    m = re.search(rf'^\s*{key}:\s*"?([^"\n]+?)"?\s*$', path.read_text(encoding='utf-8'), re.M)
    return m.group(1).strip() if m else ''


# --------------------------------------------------------------------------- ISBN y fechas
def isbn13_ok(value):
    digits = re.sub(r'[\s-]', '', value)
    if not re.fullmatch(r'97[89]\d{10}', digits):
        return False
    total = sum(int(d) * (1 if i % 2 == 0 else 3) for i, d in enumerate(digits[:12]))
    return (10 - total % 10) % 10 == int(digits[12])


def is_set(value):
    return bool(value) and not str(value).startswith('PENDIENTE') and value != 'NO'


def edition_line(lang, ids):
    n = int(ids.get('edition', '1') or 1)
    ordinal = ORDINALS[lang].get(n, str(n))
    noun = {'es': 'edición digital', 'en': 'digital edition'}[lang]
    when = ids.get('edition_date', '')
    if re.fullmatch(r'\d{4}-(0[1-9]|1[0-2])', when):
        y, m = when.split('-')
        month = MONTHS[lang][int(m) - 1]
        when = f'{month} de {y}' if lang == 'es' else f'{month} {y}'
    else:
        when = 'PENDIENTE (mes y año)' if lang == 'es' else 'PENDIENTE (month and year)'
    return f'{ordinal} {noun} · {when}'


def authors_of(reg):
    return [a.strip() for a in reg.get('authors', '').split(';') if a.strip()]


def cite_authors(names, lang):
    joiner = {'es': ' y ', 'en': ' & '}[lang]
    return joiner.join(names) if len(names) <= 2 else ', '.join(names[:-1]) + joiner + names[-1]


# --------------------------------------------------------------------------- render
def context(reg, site, vol, lang, ids):
    base = {k: v for k, v in reg.items() if k != 'volumes'}
    fm = ROOT / 'content' / lang / vol / 'front-matter'
    subtitle = meta(fm / f'metadata_{lang}.yaml', 'subtitle')
    names = authors_of(reg)
    rows = []
    for key, label, _ in FORMATS:
        value = ids.get(key, 'NO')
        if value != 'NO':
            rows.append(f"| {label if isinstance(label, str) else label[lang]} | {value} |")
    pid = reg.get('publisher_id', '')
    id_label = {'es': 'Documento de identidad', 'en': 'ID number'}[lang]
    ctx = dict(base, **ids, vol=vol, n=vol[-1], series=VOLS['series'][lang],
               title=VOLS['series'][lang], subtitle=subtitle or VOLS['titles'][lang][vol],
               site=urlparse(site['url']).netloc,
               authors=', '.join(names), authors_cite=cite_authors(names, lang),
               author_label=({'es': 'Autores', 'en': 'Authors'} if len(names) > 1
                             else {'es': 'Autor', 'en': 'Author'})[lang],
               publisher_id_line=(f' — {id_label}: {pid}' if pid else ''),
               edition_line=edition_line(lang, ids), isbn_rows='\n'.join(rows),
               edition_year=(ids.get('edition_date', '')[:4] if is_set(ids.get('edition_date', ''))
                             else 'PENDIENTE (mes y año)' if lang == 'es' else 'PENDIENTE (month and year)'))
    if ids.get('isbn_print', 'NO') != 'NO':
        ctx['print_block'] = ({'es': '**Impresor:** ', 'en': '**Printer:** '}[lang] + reg.get('printer', 'PENDIENTE') +
                              {'es': '\\\n**Tiraje:** impresión bajo demanda (según pedidos).\n\n',
                               'en': '\\\n**Print run:** print on demand (per order).\n\n'}[lang])
        ctx['print_note'] = {'es': ' y, bajo demanda, impresa', 'en': ' and, on demand, in print'}[lang]
    else:
        ctx['print_block'], ctx['print_note'] = '', ''
    return ctx


def render_all(reg, site, write):
    problems, pending = [], []
    for vol, langs in reg['volumes'].items():
        for lang, ids in langs.items():
            fm = ROOT / 'content' / lang / vol / 'front-matter'
            if not fm.is_dir():
                continue
            ctx = context(reg, site, vol, lang, ids)
            text = (LEGAL / f'ficha-tecnica.{lang}.md.tpl').read_text(encoding='utf-8')
            text = re.sub(r'\{\{(\w+)\}\}', lambda m: str(ctx.get(m.group(1), m.group(0))), text)
            if write:
                (fm / '03_hoja_creditos.md').write_text(text, encoding='utf-8')
            pending += [f'{lang}/{vol}: {m}' for m in re.findall(r'PENDIENTE\w*', text)]
            problems += [f'{lang}/{vol}: placeholder sin resolver {m}' for m in re.findall(r'\{\{\w+\}\}', text)]
    return pending, problems


# --------------------------------------------------------------------------- validación
def validate(reg, site):
    errors, seen = [], {}
    for vol, langs in reg['volumes'].items():
        for lang, ids in langs.items():
            where = f'{lang}/{vol}'
            for key, _, _ in FORMATS:
                v = ids.get(key, 'NO')
                if not is_set(v):
                    continue
                if not isbn13_ok(v):
                    errors.append(f'{where}: {key} «{v}» no es un ISBN-13 válido (dígito de control)')
                elif not v.replace('-', '').startswith('978612'):
                    errors.append(f'AVISO {where}: {key} «{v}» no lleva el prefijo peruano 978-612')
                if v in seen:
                    errors.append(f'{where}: {key} «{v}» repetido en {seen[v]} (un ISBN por formato/edición/idioma)')
                seen[v] = f'{where}.{key}'
            dl = ids.get('deposito_legal', '')
            if is_set(dl) and not re.fullmatch(r'20\d{2}-\d{3,6}', dl):
                errors.append(f'{where}: deposito_legal «{dl}» debe tener la forma AAAA-NNNNN')
            ed = ids.get('edition_date', '')
            if is_set(ed) and not re.fullmatch(r'\d{4}-(0[1-9]|1[0-2])', ed):
                errors.append(f'{where}: edition_date «{ed}» debe ser AAAA-MM')
    design = json.loads((ROOT / 'tools' / 'covers' / 'cover-design.json').read_text(encoding='utf-8'))['legends']
    names = {a.casefold() for a in authors_of(reg)}
    for slug, leg in design.items():
        legend = leg if isinstance(leg, str) else leg.get('legend', '')
        on_cover = {a.strip().casefold() for a in legend.split('·') if a.strip()}
        if on_cover != names:
            errors.append(f'{slug}: la cubierta acredita «{legend}» pero el registro dice «{reg.get("authors")}»')
    if 'site' in reg and reg['site'] != urlparse(site['url']).netloc:
        errors.append(f'registry.site «{reg["site"]}» ≠ web/site.config.json «{urlparse(site["url"]).netloc}» '
                      '(elimina `site` del registro: se toma de la configuración web)')
    return errors


# --------------------------------------------------------------------------- salidas
def write_meta(reg, lang, vol, fmt, out):
    ids = reg['volumes'][vol][lang]
    year = ids.get('edition_date', '')[:4] if is_set(ids.get('edition_date', '')) else ''
    lines = ['---', 'author:'] + [f'  - "{a}"' for a in authors_of(reg)]
    lines.append('toc-title: "' + {'es': 'Índice', 'en': 'Contents'}[lang] + '"')   # en el YAML, no en argv: inmune a la locale
    lines.append(f'rights: "© {year} {reg["publisher"]}. {reg["license_name"]}."'.replace('©  ', '© '))
    if year:
        lines.append(f'date: "{ids["edition_date"]}"')
    key = {'epub': 'isbn_epub', 'pdf': 'isbn_pdf', 'print': 'isbn_print'}[fmt]
    if is_set(ids.get(key, '')):
        uuid = meta(ROOT / 'content' / lang / vol / 'front-matter' / f'metadata_{lang}.yaml', 'text')
        lines += ['identifier:', '  - scheme: ISBN', f'    text: "{ids[key]}"']
        if uuid:
            lines += ['  - scheme: UUID', f'    text: "{uuid}"']
    lines.append('---')
    Path(out).write_text('\n'.join(lines) + '\n', encoding='utf-8')


def public_json(reg, site):
    """Solo datos que ya son públicos en el libro: sin DNI ni domicilio."""
    out = {'publisher': reg['publisher'], 'site': site['url'], 'authors': authors_of(reg),
           'license': {'name': reg['license_name'], 'url': reg['license_url']}, 'volumes': {}}
    for vol, langs in reg['volumes'].items():
        out['volumes'][vol] = {}
        for lang, ids in langs.items():
            out['volumes'][vol][lang] = {
                'slug': VOLS['slugs'][vol], 'title': VOLS['titles'][lang][vol],
                'edition': int(ids.get('edition', 1)),
                'edition_date': ids['edition_date'] if is_set(ids.get('edition_date')) else None,
                'isbn': {f: ids[k] for k, _, f in FORMATS if is_set(ids.get(k, ''))},
                'deposito_legal': ids['deposito_legal'] if is_set(ids.get('deposito_legal', '')) else None,
                'links': {k: ids[k] for k in ('kdp', 'google_play', 'lulu') if ids.get(k)},
            }
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--strict', action='store_true')
    ap.add_argument('--check', action='store_true')
    ap.add_argument('--meta', nargs=4, metavar=('LANG', 'VOL', 'FORMAT', 'OUT'))
    ap.add_argument('--public', metavar='OUT.json')
    args = ap.parse_args()
    reg, site = load()

    if args.meta:
        lang, vol, fmt, out = args.meta
        write_meta(reg, lang, vol, fmt, out)
        return
    if args.public:
        Path(args.public).write_text(json.dumps(public_json(reg, site), ensure_ascii=False, indent=2) + '\n',
                                     encoding='utf-8')
        return

    pending, problems = render_all(reg, site, write=not args.check)
    issues = validate(reg, site) + problems
    hard = [i for i in issues if not i.startswith('AVISO')]
    print(f'render_legal: {len(pending)} marcadores PENDIENTE · {len(hard)} errores · '
          f'{len(issues) - len(hard)} avisos', file=sys.stderr)
    for i in issues:
        print(f'  ! {i}', file=sys.stderr)
    if args.strict and (pending or hard):
        print('\n'.join(sorted(set(pending))), file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
