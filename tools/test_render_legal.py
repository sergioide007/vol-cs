#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Regresión de `render_legal.py`: ISBN, Depósito Legal, edición y coherencia de autores."""
import copy
import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('render_legal', ROOT / 'tools/render_legal.py')
rl = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(rl)


class IsbnTest(unittest.TestCase):
    def test_real_isbns_of_book_one_are_valid(self):
        """Los dos ISBN que la BNP asignó al libro 1 deben pasar el dígito de control."""
        self.assertTrue(rl.isbn13_ok('978-612-03-2931-3'))
        self.assertTrue(rl.isbn13_ok('978-612-03-2914-6'))

    def test_wrong_check_digit_or_shape_fails(self):
        self.assertFalse(rl.isbn13_ok('978-612-03-2914-7'))
        self.assertFalse(rl.isbn13_ok('612-03-2914-6'))
        self.assertFalse(rl.isbn13_ok('PENDIENTE'))


class RegistryTest(unittest.TestCase):
    def setUp(self):
        self.reg, self.site = rl.load()

    def test_inline_maps_keep_empty_values(self):
        ids = self.reg['volumes']['vol1']['es']
        self.assertEqual('', ids['kdp'])
        self.assertEqual('1', ids['edition'])

    def test_shipped_registry_is_consistent(self):
        """El registro tal como se entrega no tiene errores (solo PENDIENTE, que es otra cosa)."""
        hard = [e for e in rl.validate(self.reg, self.site) if not e.startswith('AVISO')]
        self.assertEqual([], hard)

    def test_duplicate_isbn_is_reported(self):
        reg = copy.deepcopy(self.reg)
        reg['volumes']['vol1']['es']['isbn_epub'] = '978-612-03-2914-6'
        reg['volumes']['vol2']['es']['isbn_epub'] = '978-612-03-2914-6'
        self.assertTrue(any('repetido' in e for e in rl.validate(reg, self.site)))

    def test_bad_deposito_legal_and_date_are_reported(self):
        reg = copy.deepcopy(self.reg)
        reg['volumes']['vol1']['es'].update(deposito_legal='9631', edition_date='2026-13')
        errors = ' | '.join(rl.validate(reg, self.site))
        self.assertIn('AAAA-NNNNN', errors)
        self.assertIn('AAAA-MM', errors)

    def test_cover_and_registry_authors_must_match(self):
        reg = copy.deepcopy(self.reg)
        reg['authors'] = 'Solo Uno'
        self.assertTrue(any('cubierta acredita' in e for e in rl.validate(reg, self.site)))

    def test_site_must_come_from_web_config(self):
        reg = copy.deepcopy(self.reg)
        reg['site'] = 'otro.example.org'
        self.assertTrue(any('site.config.json' in e for e in rl.validate(reg, self.site)))


class EditionTest(unittest.TestCase):
    def test_month_and_year_are_required_by_the_bnp(self):
        ids = {'edition': '1', 'edition_date': '2026-10'}
        self.assertEqual('Primera edición digital · octubre de 2026', rl.edition_line('es', ids))
        self.assertEqual('First digital edition · October 2026', rl.edition_line('en', ids))
        self.assertIn('PENDIENTE', rl.edition_line('es', {'edition': '1', 'edition_date': 'PENDIENTE'}))

    def test_rendered_credits_carry_every_bnp_field(self):
        reg, site = rl.load()
        reg['volumes']['vol1']['es'].update(edition_date='2026-10', deposito_legal='2026-12345',
                                            isbn_epub='978-612-03-2914-6', isbn_pdf='978-612-03-2931-3')
        reg['publisher_address'] = 'Calle Falsa 123, Lima'
        ctx = rl.context(reg, site, 'vol1', 'es', reg['volumes']['vol1']['es'])
        text = (ROOT / 'legal/ficha-tecnica.es.md.tpl').read_text(encoding='utf-8')
        import re
        text = re.sub(r'\{\{(\w+)\}\}', lambda m: str(ctx.get(m.group(1), m.group(0))), text)
        for needle in ('Código Sintético', 'Primera edición digital · octubre de 2026', 'Sergio Perez Ruiz',
                       'Calle Falsa 123', 'Hecho el Depósito Legal en la Biblioteca Nacional del Perú N.º 2026-12345',
                       '978-612-03-2914-6', '978-612-03-2931-3'):
            self.assertIn(needle, text)
        self.assertNotIn('Impresor', text)          # e-book: impresor y tiraje no son obligatorios
        self.assertEqual([], re.findall(r'\{\{\w+\}\}', text))


if __name__ == '__main__':
    unittest.main()
