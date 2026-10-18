#!/usr/bin/env python3
"""Genera miniaturas WebP ligeras de las portadas para la landing (Core Web Vitals).

Uso:
  python3 tools/make_cover_thumbs.py <repo-vol-cs> <carpeta-salida>
Lee   <repo-vol-cs>/content/{es,en}/volN/front-matter/01_cubierta_delantera.png
Crea  <carpeta-salida>/volN-es.webp y volN-en.webp  (240×360, ~10-20 KB c/u)
Si falta la portada EN, omite ese archivo (y la landing usará la ES).
"""
import sys
from pathlib import Path
from PIL import Image

src, out = Path(sys.argv[1]), Path(sys.argv[2])
out.mkdir(parents=True, exist_ok=True)
for lang in ('es', 'en'):
    for n in range(1, 5):
        p = src / 'content' / lang / f'vol{n}' / 'front-matter' / '01_cubierta_delantera.png'
        if not p.exists():
            print(f'· falta {p}')
            continue
        im = Image.open(p).convert('RGB')
        im.thumbnail((240, 360), Image.LANCZOS)
        dst = out / f'vol{n}-{lang}.webp'
        im.save(dst, 'WEBP', quality=80, method=6)
        print(f'{dst}  {im.size}  {dst.stat().st_size // 1024} KB')
