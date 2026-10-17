#!/usr/bin/env python3
"""Rellena la hoja de créditos de cada volumen/idioma desde legal/registry.yaml.

    python3 tools/render_legal.py            # escribe content/<lang>/<volN>/front-matter/03_hoja_creditos.md
    python3 tools/render_legal.py --strict   # además, falla si queda algún «PENDIENTE» (usar en releases)

Un pequeño lector YAML propio (el registro es plano) evita depender de PyYAML.
"""
import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEGAL = ROOT / 'legal'
VOLS = json.loads((ROOT / 'tools' / 'vols.json').read_text(encoding='utf-8'))


def parse_registry(text):
    data, stack = {}, [(-1, {})]
    stack[0] = (-1, data)
    for raw in text.splitlines():
        line = raw.split(' #')[0].rstrip() if not raw.lstrip().startswith('#') else ''
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
                           (kv.split(':', 1) for kv in val.strip('{} ').split(','))}
        else:
            parent[key] = val.strip('"')
    return data


def meta(path, key):
    m = re.search(rf'^{key}:\s*"?([^"\n]+?)"?\s*$', path.read_text(encoding='utf-8'), re.M)
    return m.group(1).strip() if m else ''


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--strict', action='store_true')
    args = ap.parse_args()
    reg = parse_registry((LEGAL / 'registry.yaml').read_text(encoding='utf-8'))
    base = {k: v for k, v in reg.items() if k != 'volumes'}
    pending = []
    for vol, langs in reg['volumes'].items():
        for lang, ids in langs.items():
            fm = ROOT / 'content' / lang / vol / 'front-matter'
            if not fm.is_dir():
                continue
            md = fm / f'metadata_{lang}.yaml'
            subtitle = meta(md, 'subtitle')
            short_title = subtitle.split('—')[0].strip()
            ctx = dict(base, **ids, vol=vol, n=vol[-1], series=VOLS['series'][lang],
                       title=VOLS['series'][lang], subtitle=subtitle or short_title)
            text = (LEGAL / f'ficha-tecnica.{lang}.md.tpl').read_text(encoding='utf-8')
            text = re.sub(r'\{\{(\w+)\}\}', lambda m: str(ctx.get(m.group(1), m.group(0))), text)
            (fm / '03_hoja_creditos.md').write_text(text, encoding='utf-8')
            pending += [f'{lang}/{vol}: {m}' for m in re.findall(r'PENDIENTE\w*', text)]
    print(f'render_legal: {len(pending)} marcadores PENDIENTE', file=sys.stderr)
    if args.strict and pending:
        print('\n'.join(sorted(set(pending))), file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
