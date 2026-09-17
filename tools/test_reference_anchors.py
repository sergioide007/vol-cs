#!/usr/bin/env python3
"""Regresión de las anclas bibliográficas: stdlib y pandoc."""
from pathlib import Path
import json
import re
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
FILTER = ROOT / 'tools/lua/reference-anchors.lua'


def convert(text, target, filtered=True):
    args = ['pandoc', '-f', 'markdown', '-t', target]
    if filtered:
        args += ['--lua-filter', str(FILTER)]
    return subprocess.check_output(args, input=text, text=True)


class ReferenceAnchorsTest(unittest.TestCase):
    def test_only_empty_reference_headers_change(self):
        text = '# Referencias\n\n### {#ref-example}\n\nTexto.\n\n### Título {#ref-named}\n\n### {#other}\n'
        blocks = json.loads(convert(text, 'json'))['blocks']
        self.assertEqual(blocks[0]['t'], 'Header')
        self.assertEqual(blocks[1]['t'], 'Plain')
        span = blocks[1]['c'][0]
        self.assertEqual(span['t'], 'Span')
        self.assertEqual(span['c'][0][0], 'ref-example')
        self.assertEqual(blocks[3]['t'], 'Header')
        self.assertEqual(blocks[4]['t'], 'Header')

    def test_links_and_targets_survive(self):
        text = '[Cita](#ref-example)\n\n### {#ref-example}\n\nAutor (2026). Obra.\n'
        latex = convert(text, 'latex')
        self.assertIn('hyperlink{ref-example}', latex)
        self.assertIn('hypertarget{ref-example}', latex)
        self.assertNotIn('subsection', latex)
        self.assertNotIn('addcontentsline', latex)
        html = convert(text, 'html')
        self.assertIn('href="#ref-example"', html)
        self.assertIn('id="ref-example"', html)
        self.assertNotIn('<h3', html)

    def test_pdf_index_before_and_after(self):
        text = '# Referencias\n\n### {#ref-example}\n\nAutor (2026). Obra.\n'
        with tempfile.TemporaryDirectory() as tmp:
            for filtered in (False, True):
                pdf = Path(tmp) / ('filtered.pdf' if filtered else 'original.pdf')
                # Incluye H3 para reproducir el encabezado bibliográfico vacío.
                args = ['pandoc', '-f', 'markdown', '--toc', '--toc-depth=3',
                        '-V', 'documentclass=book', '--pdf-engine=xelatex', '-o', str(pdf)]
                if filtered:
                    args += ['--lua-filter', str(FILTER)]
                subprocess.run(args, input=text, text=True, check=True,
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                output = subprocess.check_output(['pdftotext', '-layout', str(pdf), '-'], text=True)
                empty = re.findall(r'^\s*(?:\.\s*){3,}\d+\s*$', output, re.M)
                self.assertEqual(bool(empty), not filtered)
                self.assertIn('Referencias', output)

    def test_all_bibliographies(self):
        for path in sorted(ROOT.glob('vol[1-4]-*/referencias/referencias.md')):
            with self.subTest(volume=path.parts[-3]):
                source = path.read_text()
                original = json.loads(convert(source, 'json', False))['blocks']
                result = json.loads(convert(source, 'json'))['blocks']
                anchors = [b for b in original if b['t'] == 'Header'
                           and b['c'][1][0].startswith('ref-') and not b['c'][2]]
                self.assertTrue(anchors)
                self.assertEqual(len(original), len(result))
                for before, after in zip(original, result):
                    if before in anchors:
                        self.assertEqual(after['t'], 'Plain')
                        self.assertEqual(after['c'][0]['c'][0], before['c'][1])
                    else:
                        self.assertEqual(before, after)


if __name__ == '__main__':
    unittest.main()
