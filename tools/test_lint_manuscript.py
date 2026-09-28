#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Regresión de `lint_manuscript.py`: funciones puras e invariantes del informe.

Las pruebas no fijan cifras del manuscrito (cambian conforme se corrige): lo que
verifican son las reglas de detección y la coherencia del informe, de modo que
un hallazgo nuevo no pueda entrar por una puerta mal cerrada.
"""
from pathlib import Path
import importlib.util
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    'lint_manuscript', ROOT / 'tools/lint_manuscript.py')
lint = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(lint)


class ParagraphsTest(unittest.TestCase):
    def test_splits_on_blank_lines_keeping_line_numbers(self):
        self.assertEqual([(1, 'uno'), (3, 'dos'), (5, 'tres')],
                         list(lint.paragraphs('uno\n\ndos\n\ntres')))

    def test_ignores_fenced_code(self):
        found = [p for _, p in lint.paragraphs('antes\n\n```python\nx = 50 %\n```\n\ndespues')]
        self.assertEqual(['antes', 'despues'], found)

    def test_ignores_tables_and_indented_code(self):
        text = 'antes\n\n| a | b |\n|---|---|\n| 50 % | x |\n\n    code = 1\n\ndespues'
        self.assertEqual(['antes', 'despues'], [p for _, p in lint.paragraphs(text)])


class PatternTest(unittest.TestCase):
    def test_ref_reads_single_and_range(self):
        for text, expected in [
                ('véase el cap. 37 del volumen', [37]),
                ('los capítulos 64–65 son esto', [64, 65]),
                ('según caps. 16-21', [16, 21]),
                ('capítulo 1 (Vol. 4)', [1])]:
            found = [int(n) for m in lint.REF.finditer(text) for n in m.groups() if n]
            self.assertEqual(expected, found, text)

    def test_figure_needs_a_unit(self):
        self.assertTrue(lint.FIGURE.search('baja un 40 % el coste'))
        self.assertTrue(lint.FIGURE.search('tarda 600 ms en decidir'))
        self.assertTrue(lint.FIGURE.search('cuesta $5 por millón'))
        # Un número suelto no es una afirmación cuantitativa.
        self.assertIsNone(lint.FIGURE.search('el capítulo 12 explica el patrón'))
        self.assertIsNone(lint.FIGURE.search('3 x 4 es el tamaño de la matriz'))

    def test_pending_does_not_match_spanish_word(self):
        self.assertIsNone(lint.PENDING.search('el agente todo lo automatiza'))
        self.assertTrue(lint.PENDING.search('[ISBN PENDIENTE]'))
        self.assertTrue(lint.PENDING.search('TODO: revisar'))

    def test_legacy_part_reads_roman_and_range(self):
        match = lint.LEGACY_PART.search('### Parte IV: Patrones de escala (caps. 22–40)')
        self.assertEqual('IV', match.group(1))
        self.assertIsNone(lint.LEGACY_PART.search('## Parte final del recorrido'))

    def test_model_id(self):
        found = lint.MODEL_ID.search('model="claude-opus-4-8"')
        self.assertEqual('claude-opus-4-8', found.group(0))
        self.assertIsNone(lint.MODEL_ID.search('un modelo de lenguaje cualquiera'))


class AllowlistTest(unittest.TestCase):
    def test_prefix_and_exact(self):
        self.assertTrue(lint.allowed_model('claude-opus-4-8', ['claude-opus-*']))
        self.assertFalse(lint.allowed_model('claude-sonnet-4-6', ['claude-opus-*']))
        self.assertTrue(lint.allowed_model('gpt-4o', ['gpt-4o']))
class ManuscriptInvariantsTest(unittest.TestCase):
    """Propiedades que deben cumplirse siempre, passen o no los checks."""

    @classmethod
    def setUpClass(cls):
        cls.vols = lint.volumes()
        cls.findings = []

        def add(check, severity, item, line, message, detail=None):
            where = getattr(item, 'path', item)
            volume = getattr(item, 'volume', None)
            cls.findings.append({'check': check, 'severity': severity,
                                 'file': lint.relative(where), 'line': line,
                                 'message': message,
                                 'volume': volume.number if volume else None,
                                 'detail': detail or {}})

        appendices = lint.find_appendices(cls.vols)
        lint.check_c1_crossrefs(cls.vols, add)
        lint.check_c2_references(cls.vols, add)
        lint.check_c3_figures(cls.vols, add)
        lint.check_c4_placeholders(cls.vols, appendices, add)
        lint.check_c5_legacy_numbering(cls.vols, add)
        lint.check_c6_models(cls.vols, add)
        lint.check_c7_budget(cls.vols, add)
        lint.check_c8_anchors(cls.vols, add)
        lint.check_image_folders(cls.vols, add)

    def test_series_shape(self):
        self.assertEqual(4, len(self.vols))
        self.assertEqual(80, sum(v.count for v in self.vols))
        for volume in self.vols:
            self.assertEqual(sorted(volume.by_number), list(range(1, volume.count + 1)),
                             f'el Vol. {volume.number} tiene huecos en su numeración')

    def test_findings_are_well_formed(self):
        for finding in self.findings:
            self.assertTrue((ROOT / finding['file']).exists(), finding['file'])
            self.assertGreaterEqual(finding['line'], 1, finding)
            self.assertIn(finding['severity'], ('error', 'aviso'), finding)
            self.assertTrue(finding['message'].strip(), finding)

    def test_no_duplicate_findings(self):
        seen = {(f['check'], f['file'], f['line'], f['message']) for f in self.findings}
        self.assertEqual(len(seen), len(self.findings))

    def test_unverified_entries_are_reported_once(self):
        for volume in self.vols:
            blocks = re.split(r'(?m)^###\s*\{#ref-', volume.references())
            expected = sum(1 for body in blocks[1:] if lint.UNVERIFIED.search(body))
            reported = len([f for f in self.findings if f['check'] == 'C2'
                            and f['file'] == lint.relative(volume.references_path)])
            self.assertEqual(expected, reported, f'Vol. {volume.number}')

    def test_legacy_ranges_exceed_every_volume(self):
        """C5 solo se dispara con rangos que ningún volumen puede alojar."""
        ceiling = max(v.count for v in self.vols)
        for finding in self.findings:
            if finding['check'] != 'C5' or 'last' not in finding['detail']:
                continue
            self.assertGreater(int(finding['detail']['last']), ceiling, finding)

    def test_crossrefs_never_silently_ignored(self):
        """Toda remisión a un número inexistente en su tomo produce un hallazgo.

        Replica la resolución de `check_c1_crossrefs`: si la expresión trae
        «(Vol. N…)», el número se juzga contra ese volumen, no contra el local.
        """
        for volume in self.vols:
            for item in volume.manuscript_files():
                for match in lint.REF.finditer(item.text):
                    numbers = [int(n) for n in match.groups() if n]
                    context = item.text[max(0, match.start() - 60):match.start()]
                    labelled = lint.VOL_LABEL.search(context)
                    target = int(labelled.group(1)) if labelled else volume.number
                    counts = {v.number: v.count for v in self.vols}
                    if not any(n > counts.get(target, 0) for n in numbers):
                        continue
                    line = item.text.count('\n', 0, match.start()) + 1
                    hit = [f for f in self.findings if f['check'] == 'C1'
                           and f['file'] == lint.relative(item.path) and f['line'] == line]
                    self.assertTrue(hit, f'{lint.relative(item.path)}:{line} sin reportar')

    def test_report_renders(self):
        report = lint.render(self.vols, self.findings, {c for c, _, _ in lint.CHECKS})
        self.assertIn('| C1 | remisiones cruzadas |', report)
        self.assertIn('## C5 · numeración antigua', report)


if __name__ == '__main__':
    unittest.main()
