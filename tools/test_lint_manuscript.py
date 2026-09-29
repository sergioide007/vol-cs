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

    def test_table_row_does_not_merge_with_long_paragraph(self):
        """Regresión: con dos líneas de prosa delante, la tabla se fusionaba."""
        text = 'linea uno\nlinea dos\n| a | 50 % |\n| b | 60 % |\n\ndespues'
        self.assertEqual(['linea uno\nlinea dos', 'despues'],
                         [p for _, p in lint.paragraphs(text)])

    def test_indented_code_does_not_merge_with_long_paragraph(self):
        text = 'linea uno\nlinea dos\n    code = 50 %\n\ndespues'
        self.assertEqual(['linea uno\nlinea dos', 'despues'],
                         [p for _, p in lint.paragraphs(text)])

    def test_bullet_opens_its_own_unit(self):
        """Regresión del Vol. 2 cap. 9: la viñeta se fundía con la prosa."""
        text = ('Prosa que ocupa\nuna línea y media.\n'
                '- Viñeta con su propia cifra del 40 %.\n'
                '- Otra viñeta.\n')
        self.assertEqual(
            ['Prosa que ocupa\nuna línea y media.',
             '- Viñeta con su propia cifra del 40 %.',
             '- Otra viñeta.'],
            [p for _, p in lint.paragraphs(text)])

    def test_quote_continuation_is_a_single_unit(self):
        text = '> primera línea de la cita\n> segunda línea de la cita\n\notro'
        self.assertEqual(['> primera línea de la cita\n> segunda línea de la cita',
                          'otro'],
                         [p for _, p in lint.paragraphs(text)])

    def test_unit_reports_its_containing_heading(self):
        found = list(lint.prose_units('## Lo esencial del capítulo 3\n\n- Viñeta.\n'))
        self.assertEqual([(3, '- Viñeta.', '## Lo esencial del capítulo 3')], found)


class UnitKindTest(unittest.TestCase):
    def test_is_item_distinguishes_bullet_and_quote_from_prose(self):
        for text in ('- viñeta', '* viñeta', '1. paso', '12) paso', '> cita'):
            self.assertTrue(lint.is_item(text), text)
        for text in ('prosa normal', '# Encabezado', '| a | b |'):
            self.assertFalse(lint.is_item(text), text)

    def test_summary_heading_marks_restatement_blocks(self):
        for text in ('## Lo esencial del capítulo 9', '### Resumen',
                     '## 5. Conclusiones', '## Cierre del volumen',
                     '## Síntesis', '### Puntos clave'):
            self.assertTrue(lint.SUMMARY_HEADING.match(text), text)
        for text in ('## Las cinco causas principales del Token-Burn',
                     '## Lo que sigue', '## Taxonomía de conferencias'):
            self.assertFalse(lint.SUMMARY_HEADING.match(text), text)


class MaskCodeTest(unittest.TestCase):
    def test_preserves_line_numbers(self):
        text = 'antes\n\n```python\nx = 1\ny = 2\n```\n\ndespues'
        self.assertEqual(text.count('\n'), lint.mask_code(text).count('\n'))

    def test_preserves_offsets(self):
        """Sin esto, el número de línea de C6 apunta a la línea equivocada."""
        text = 'antes\n\n```py\nclaude-sonnet\n```\n\nfin claude-sonnet\n'
        masked = lint.mask_code(text)
        self.assertEqual(len(text), len(masked))
        self.assertEqual(text.index('fin claude'), masked.index('fin claude'))

    def test_keeps_prose_and_drops_code(self):
        text = 'antes claude-sonnet\n\n```\nclaude-haiku\n```\n\ndespues claude-opus'
        masked = lint.mask_code(text)
        self.assertIn('antes claude-sonnet', masked)
        self.assertIn('despues claude-opus', masked)
        self.assertNotIn('claude-haiku', masked)

    def test_unclosed_fence_masks_to_end(self):
        self.assertNotIn('claude-opus', lint.mask_code('```\nclaude-opus\n'))


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

    def test_pending_only_counts_marker_forms(self):
        """«TODO» en mayúsculas para enfatizar es castellano, no trabajo pendiente."""
        self.assertIsNone(lint.PENDING.search('**Costo si TODO en cloud**: ~$12/día'))
        self.assertIsNone(lint.PENDING.search('# Este es el esqueleto de TODO agente'))
        self.assertTrue(lint.PENDING.search('[TODO] revisar el apéndice'))
        self.assertTrue(lint.PENDING.search('TODO: reescribir la sección'))

    def test_c4_ignores_pending_inside_code(self):
        """Un enum llamado PENDIENTE en un ejemplo de Java no es un hueco."""
        code = '```java\nvar pago = Pago.builder().estado(EstadoPago.PENDIENTE).build();\n```\n'
        self.assertIsNone(lint.PENDING.search(lint.mask_code(code)))

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
class GluedTest(unittest.TestCase):
    """C12 solo marca lo que queda tras enmascarar codigo y comillas."""

    def setUp(self):
        self.pat = lint.re.compile(lint.GLUED)

    def test_identifier_in_backticks_is_masked(self):
        text = 'usa `maxIterations` en el bucle'
        self.assertIsNone(self.pat.search(lint.mask_inline_code(text)))

    def test_identifier_in_block_is_masked(self):
        text = '```python\nwhile promptSistema():\n    pass\n```'
        self.assertIsNone(self.pat.search(lint.mask_inline_code(text)))

    def test_glued_word_in_prose_is_caught(self):
        self.assertIsNotNone(self.pat.search('el metodo comoHipotesis'))

    def test_masking_preserves_length_and_newlines(self):
        text = 'antes `codigo` despues\n```\nx = 1\n```\nfin'
        masked = lint.mask_inline_code(text)
        self.assertEqual(len(text), len(masked))
        self.assertEqual(text.count('\n'), masked.count('\n'))


class GlyphsTest(unittest.TestCase):
    """C13: un caracter no representable sale como cuadrado vacio en el PDF."""

    def test_detects_cjk(self):
        self.assertTrue(lint.CJK.search('(\u751f\u6210\u5f0f)'))

    def test_ignores_latin_and_punctuation(self):
        self.assertIsNone(lint.CJK.search('Interim Measures (2023), n.o 15.'))

    def test_spanish_letters_are_not_flagged(self):
        self.assertIsNone(lint.CJK.search('a\u00f1o n\u00fa\u00f1o gu\u00edi\u00e1 ¿cu\u00e1l?'))


class CapsInWordTest(unittest.TestCase):
    """C14: una mayuscula en medio de palabra castellana."""

    def setUp(self):
        self.pat = lint.CAMEL

    def test_flags_glued_capital(self):
        self.assertIsNotNone(self.pat.search('los turnOS de palabra'))
        self.assertIsNotNone(self.pat.search('el metodo comoHipotesis'))

    def test_allows_known_terms(self):
        for term in ('arXiv:2302.06590', 'iPhone', 'eBay', 'macOS'):
            match = self.pat.search(term)
            if match:
                self.assertTrue(match.group(0).startswith(lint.CAMEL_OK), term)

    def test_ignores_code_and_backticks(self):
        self.assertIsNone(self.pat.search(lint.mask_inline_code('`maxIterations`')))

    def test_flags_symbol_in_prose_without_backticks(self):
        """Un identificador citado en prosa debe ir entrecomillado: ese es el
        defecto que C14 detecta y que la convencion del libro resuelve."""
        self.assertIsNotNone(self.pat.search(lint.mask_inline_code('el promptSistema del agente')))

    def test_plain_spanish_is_clean(self):
        self.assertIsNone(self.pat.search('los turnos de palabra se organizan bien'))


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

    def test_orphan_entries_are_detected(self):
        """C8 debe listar las entradas de la bibliografia que nadie cita.

        Esta comprobacion existe porque esa rama estuvo muerta: la condicion
        extra «'#anchor' no esta en el texto de la bibliografia» es siempre
        falsa, ya que el encabezado de la entrada es «### {#ref-slug}».
        """
        orphans = [f for f in self.findings
                   if f['check'] == 'C8' and f['severity'] == 'aviso']
        counted = 0
        for volume in self.vols:
            anchors = re.findall(r'(?m)^###\s*\{#(ref-[^}]+)\}',
                                 volume.references())
            reales = [a for a in anchors
                      if not any(f'#{a}' in c.text for c in volume.chapters)]
            counted += len(reales)
            self.assertEqual(
                len(reales), len([f for f in orphans if f['volume'] == volume.number
                                  and f['detail']['anchor'] in reales]),
                f'Vol. {volume.number}: {len(reales)} entradas sin citar')
        self.assertEqual(counted, len(orphans), 'todos los hallazgos de C8')

    def test_report_renders(self):
        """El informe lista las nueve comprobaciones aunque no tengan hallazgos.

        Una comprobación sin hallazgos no abre sección de detalle, así que la
        prueba mira la tabla resumen, que es la que siempre se compone.
        """
        selected = {c for c, _, _ in lint.CHECKS}
        report = lint.render(self.vols, self.findings, selected)
        for code, name, _ in lint.CHECKS:
            self.assertIn(f'| {code} | {name} |', report)
        # Y el detalle aparece para la comprobación que sí tiene hallazgos.
        for code, _, _ in lint.CHECKS:
            expected = any(f['check'] == code for f in self.findings)
            self.assertEqual(expected, f'## {code} ·' in report, code)

    def test_report_truncates_and_points_to_json(self):
        """El markdown se recorta; el JSON conserva la lista completa."""
        report = lint.render(self.vols, self.findings, {c for c, _, _ in lint.CHECKS})
        self.assertIn('AUDIT.json', report)


if __name__ == '__main__':
    unittest.main()
