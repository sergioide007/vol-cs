#!/usr/bin/env python3
"""Paridad ES/EN de dist/ y manifiesto de entrega.

    python3 tools/check_parity.py            # falla (exit 1) si algún idioma no tiene los mismos documentos
    python3 tools/check_parity.py --no-write # solo comprueba

Por cada volumen y cada idioma deben existir los cuatro documentos de la serie:
  interior-6x9--sin-caratula.pdf · lectura-6x9--con-portada.pdf · epub--con-portada.epub · epub--sin-portada.epub
Escribe dist/MANIFEST.json y dist/MANIFEST.md (tamaño, SHA-256, páginas y estado legal de cada archivo).
"""
import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / 'dist'
VOLS = json.loads((ROOT / 'tools/vols.json').read_text(encoding='utf-8'))
LANGS = ('es', 'en')
KINDS = ('interior-6x9--sin-caratula.pdf', 'lectura-6x9--con-portada.pdf',
         'epub--con-portada.epub', 'epub--sin-portada.epub')
PAGE_TOLERANCE = 0.30        # ES y EN pueden diferir en extensión, no en un tercio del libro


def sha256(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for block in iter(lambda: f.read(1 << 20), b''):
            h.update(block)
    return h.hexdigest()


def pages(path):
    out = subprocess.run(['pdfinfo', str(path)], capture_output=True, text=True).stdout
    m = re.search(r'^Pages:\s+(\d+)', out, re.M)
    return int(m.group(1)) if m else None


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--no-write', action='store_true')
    args = ap.parse_args()
    problems, manifest = [], {}
    legal = {}
    try:
        legal = json.loads(subprocess.check_output(
            ['python3', str(ROOT / 'tools/render_legal.py'), '--public', '/dev/stdout'], text=True))['volumes']
    except Exception:      # el manifiesto sigue siendo útil sin el estado legal
        pass
    for vol, slug in VOLS['slugs'].items():
        manifest[slug] = {}
        for lang in LANGS:
            row = manifest[slug][lang] = {}
            for kind in KINDS:
                f = DIST / lang / slug / f'{slug}--{lang}--{kind}'
                if not f.is_file() or f.stat().st_size == 0:
                    problems.append(f'falta {f.relative_to(ROOT)}')
                    continue
                row[f.name] = {'bytes': f.stat().st_size, 'sha256': sha256(f),
                               **({'pages': pages(f)} if f.suffix == '.pdf' else {})}
            row['_legal'] = legal.get(vol, {}).get(lang, {})
        a, b = [next((v.get('pages') for k, v in manifest[slug][l].items()
                      if k.endswith('interior-6x9--sin-caratula.pdf')), None) for l in LANGS]
        if a and b and abs(a - b) / max(a, b) > PAGE_TOLERANCE:
            problems.append(f'{slug}: ES {a} págs. vs EN {b} págs. (diferencia > {PAGE_TOLERANCE:.0%})')
    for lang in LANGS:
        for vol, slug in VOLS['slugs'].items():
            cover = DIST / lang / 'covers' / f'{slug}.pdf'
            if not cover.is_file():
                problems.append(f'falta la cubierta {cover.relative_to(ROOT)}')
    if not args.no_write:
        DIST.mkdir(exist_ok=True)
        (DIST / 'MANIFEST.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        lines = ['# Manifiesto de ediciones', '', '| Volumen | Idioma | Archivo | Págs. | MB | SHA-256 |', '|---|---|---|---|---|---|']
        for slug, langs in manifest.items():
            for lang, files in langs.items():
                for name, info in files.items():
                    if name == '_legal':
                        continue
                    lines.append(f"| {slug} | {lang} | `{name.split('--', 2)[2]}` | {info.get('pages', '—')} | "
                                 f"{info['bytes'] / 1e6:.1f} | `{info['sha256'][:12]}…` |")
        (DIST / 'MANIFEST.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')
    for p in problems:
        print('✘', p)
    n = sum(1 for s in manifest.values() for l in s.values() for k in l if k != '_legal')
    print(f'paridad: {n}/{len(VOLS["slugs"]) * len(LANGS) * len(KINDS)} documentos · {len(problems)} problemas')
    return 1 if problems else 0


if __name__ == '__main__':
    raise SystemExit(main())
