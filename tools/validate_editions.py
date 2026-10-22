#!/usr/bin/env python3
"""Preflight reproducible: stdlib, Poppler y EPUBCheck (sin PIL)."""
import argparse
import json
from pathlib import Path
import re
import subprocess
import tempfile
import zipfile
import html
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
# Un título de índice o de apartado no es un párrafo: por encima de esto, el
# título y el texto siguiente se fundieron en una sola línea de encabezado.
MAX_TITLE = 150


def run(*args):
    return subprocess.check_output(args, text=True, stderr=subprocess.STDOUT)


def inspect_pdf(path):
    info = run('pdfinfo', str(path))
    fonts = run('pdffonts', str(path)).splitlines()[2:]
    pages = int(re.search(r'^Pages:\s+(\d+)', info, re.M)[1])
    result = {'pages': pages, 'size_6x9': '432 x 648 pts' in info,
              'fonts_embedded': all(row.split()[-5] == 'yes' for row in fonts if row.strip())}
    # Una línea compuesta solo por líderes y folio es una entrada vacía del índice.
    text = run('pdftotext', '-layout', str(path), '-')
    result['empty_toc_entries'] = [
        {'page': number, 'line': line.strip()}
        for number, page in enumerate(text.split('\f'), 1)
        for line in page.splitlines()
        if re.fullmatch(r'\s*(?:\.\s*){3,}\d+\s*', line)
    ]
    with tempfile.TemporaryDirectory() as tmp:
        bbox = Path(tmp) / 'bbox.html'
        subprocess.run(['pdftotext', '-bbox', str(path), str(bbox)], check=True)
        tree = ET.parse(bbox)
        violations = []
        for number, page in enumerate(tree.findall('.//{*}page'), 1):
            # Physical recto: inner left; verso: inner right.
            left, right = (63, 387) if number % 2 else (45, 369)
            words = page.findall('.//{*}word')
            for word in words:
                x0, x1 = float(word.get('xMin')), float(word.get('xMax'))
                if x0 < left - 1 or x1 > right + 1:
                    violations.append({'page': number, 'text': word.text,
                                       'x0': x0, 'x1': x1})
        result['horizontal_text_violations'] = violations
    return result


def long_pdf_bookmarks(path):
    """Marcadores del PDF (panel de índice del visor) que parecen un párrafo."""
    try:
        from pypdf import PdfReader
    except ImportError:          # el validador no exige dependencias: se avisa y sigue
        return None
    found = []

    def walk(items):
        for item in items:
            if isinstance(item, list):
                walk(item)
            elif len(item.title) > MAX_TITLE:
                found.append({'chars': len(item.title), 'title': item.title[:80] + '…'})
    walk(PdfReader(str(path)).outline)
    return found


def long_epub_headings(path):
    """Encabezados h1-h6 del EPUB y entradas de su índice que parecen un párrafo."""
    found = []
    with zipfile.ZipFile(path) as z:
        for name in z.namelist():
            if not name.endswith(('.xhtml', '.ncx')) or name.endswith('cover.xhtml'):
                continue
            body = z.read(name).decode('utf-8', 'replace')
            pattern = r'<text>(.*?)</text>' if name.endswith('.ncx') \
                else r'<h[1-6][^>]*>(.*?)</h[1-6]>'
            for raw in re.findall(pattern, body, re.S):
                title = html.unescape(re.sub(r'<[^>]+>', '', raw)).strip()
                if len(title) > MAX_TITLE:
                    found.append({'file': name.split('/')[-1], 'chars': len(title),
                                  'title': title[:80] + '…'})
    return found


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--epubcheck', default='/usr/share/java/epubcheck.jar')
    parser.add_argument('--lang', choices=['es', 'en'], default='es')
    parser.add_argument('--work', type=Path, default=None)
    parser.add_argument('--vol', help='slug largo del volumen (p. ej. vol1-fundamentos)')
    args = parser.parse_args()
    dist = ROOT / 'dist' / args.lang
    if args.work is None:
        args.work = Path('/tmp/codigo-sintetico-build') / args.lang
    report = {}
    directories = sorted(dist.glob('vol[1-4]-*'))
    if args.vol:
        directories = [p for p in directories if p.name == args.vol]
    if not directories:
        parser.error('No hay volúmenes para validar')
    for directory in directories:
        print('Validando', directory.name, flush=True)
        slug = directory.name
        row = inspect_pdf(directory / f'{slug}--{args.lang}--interior-6x9--sin-caratula.pdf')
        logpath = args.work / slug / 'main.log'
        if not logpath.exists():
            logpath = directory / '.main.log'
        if logpath.exists():
            log = logpath.read_text(errors='replace')
            row['overfull_hbox'] = log.count('Overfull \\hbox')
            row['missing_glyphs'] = [line for line in log.splitlines() if 'Missing character:' in line]
        else:
            row['log_unavailable'] = True
        bookmarks = long_pdf_bookmarks(directory / f'{slug}--{args.lang}--interior-6x9--sin-caratula.pdf')
        row['long_pdf_bookmarks'] = bookmarks if bookmarks is not None else []
        row['epub_long_headings'] = {}
        row['epubs'] = {}
        for epub in sorted(directory.glob('*.epub')):
            check = subprocess.run(['java', '-jar', args.epubcheck, str(epub)],
                                   text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            (directory / (epub.stem + '--epubcheck.log')).write_text(check.stdout)
            row['epubs'][epub.name] = {'exit': check.returncode, 'output': check.stdout}
            row['epub_long_headings'][epub.name] = long_epub_headings(epub)
        report[slug] = row
    target = dist / (f'PREFLIGHT-{args.vol}.json' if args.vol else 'PREFLIGHT.json')
    target.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    for slug, row in report.items():
        print(slug, 'pages=', row['pages'], 'overfull=', row.get('overfull_hbox'),
              'glyphs=', len(row.get('missing_glyphs', [])),
              'horizontal=', len(row['horizontal_text_violations']),
              'titulos-largos=', len(row['long_pdf_bookmarks'])
              + sum(len(v) for v in row['epub_long_headings'].values()),
              'epubcheck=', [x['exit'] for x in row['epubs'].values()])
    print(target)
    return int(any(not row['size_6x9'] or not row['fonts_embedded']
                   or row.get('overfull_hbox', 0) or row.get('missing_glyphs')
                   or row.get('log_unavailable') or row['horizontal_text_violations']
                   or row['empty_toc_entries'] or row['long_pdf_bookmarks']
                   or any(row['epub_long_headings'].values())
                   or any(epub['exit'] for epub in row['epubs'].values())
                   for row in report.values()))


if __name__ == '__main__':
    raise SystemExit(main())
