#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Auditoría del manuscrito: remisiones, cifras, bibliografía y presupuesto.

Complementa a `validate_editions.py`, que solo mira la maquetación. Aquí se
mira el texto: si el manuscrito se contradice, promete apéndices que no
existen o afirma cifras sin origen declarado, esto falla igual que un glifo
ausente en el PDF.

Ocho comprobaciones (C1..C8), documentadas en `PLAN_DE_TRABAJO.md`:

  C1  Remisión cruzada a un capítulo que no existe en el volumen citado, o
      remisión sin etiqueta de volumen cuando el número solo existe en otro.
  C2  Entrada bibliográfica sin verificar («as cited in the manuscript»,
      «no verificado», «not fully verified»).
  C3  Párrafo con cifras sin marca de origen ([D] dato, [E] estimación,
      [I] ilustrativa) ni cita a la bibliografía.
  C4  Referencia a un apéndice inexistente o marcador «PENDIENTE».
  C5  Restos de la numeración antigua por partes (Parte IV, «caps. 76–79»).
      Nota: el total de 80 capítulos sí es correcto y no se reporta.
  C6  Identificador de modelo literal fuera de `tools/model-allowlist.txt`.
  C7  Capítulo fuera del presupuesto de palabras (aviso, no error).
  C8  Ancla `#ref-` usada sin entrada, o entrada de bibliografía nunca usada.
  C9  Carpeta de imágenes que conserva la numeración global antigua.
  C11 Año de la cita en el texto distinto del año de la entrada.

Uso:
    python3 tools/lint_manuscript.py                     # informe + exit 1 si hay errores
    python3 tools/lint_manuscript.py --vol vol4-patrones-de-escala
    python3 tools/lint_manuscript.py --only C1 C3
    python3 tools/lint_manuscript.py --no-json

Solo biblioteca estándar. No modifica el manuscrito: informa.
"""
import argparse
import json
import re
import sys
import unicodedata
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ALLOWLIST = ROOT / 'tools' / 'model-allowlist.txt'

# Presupuesto editorial de palabras por capítulo (C7).
MIN_WORDS, MAX_WORDS = 1600, 4500

# Hallazgos por archivo que se detallan en el markdown. El JSON lleva la lista
# completa: el informe se lee en el navegador y un bloque de 259 líneas no se lee.
MAX_DETAIL_PER_FILE = 12

# Un párrafo con cifras debe medir al menos esto para entrar en el informe
# (debajo es una leyenda, una viñeta o una línea de tabla, no una afirmación).
MIN_PROSE_CHARS = 120

# Cifras que exigen origen declarado. Se excluye la «x» suelta: en un manual
# técnico aparece en productos de matrices y en enumeraciones, no como dato.
FIGURE = re.compile(
    r'\d[\d.,]*\s*(?:%|por ciento|ms|milisegundos?|GB|TB|MTok|tokens?|veces|×)|'
    r'(?<!\w)\$\s?\d|\bd[óo]lares?\b',
    re.I)

# Marcas de origen que satisfacen C3.
SOURCE = re.compile(r'\[(D|E|I)\]|#ref-|\[[^\]]*\]\(#[^)]*\)|\bhttps?://|\bdoi:')

# Entradas bibliográficas sin comprobar (C2).
UNVERIFIED = re.compile(
    r'as cited in the manuscript|no verificado|not fully verified|'
    r'por verificar', re.I)

# Marcadores de contenido pendiente (C4). «TODO» en mayúsculas: la palabra
# española «todo» no es un marcador de trabajo.
PENDING = re.compile(r'\[?\bPENDIENTE\b[^\]\n]{0,12}\]?|PENDIENTE-|\bTODO\b|\bFIXME\b')

# Identificadores de modelo literales (C6).
MODEL_ID = re.compile(
    r'\b(claude|gpt|gemini|llama|qwen|mistral|deepseek)-[a-z0-9][a-z0-9._-]*',
    re.I)

# C12: simbolo pegado a una palabra, fuera de codigo y de comillas.
#
# Se apunta a dos cosas. La primera es evitar la clase de error que se ha
# repetido al editar desde el terminal: una palabra pegada a la anterior
# («comoHipotesis»). La segunda es mas util todavia: un identificador de codigo
# citado en la prosa sin comillas inversas, que es un defecto tipografico
# distinto y igual de visible para el lector.
#
# La precision se midio antes de adoptarlo: en el manuscrito hay 449
# identificadores pegados dentro de bloques de codigo o de comillas inversas
# (legitimos) y solo 1 fuera. Por eso el patron exige estar fuera de ambos.
GLUED = (r'(?<![A-Za-z`\w\-])[a-z\u00e1\u00e9\u00ed\u00f3\u00fa\u00f1]{3,}'
         r'[A-Z\u00c1\u00c9\u00cd\u00d3\u00da\u00d1][a-z\u00e1\u00e9\u00ed\u00f3\u00fa\u00f1]{2,}(?:[a-zA-Z]*)')

# Año declarado en la entrada bibliográfica y año en la cita del texto (C11).
YEAR = re.compile(r'\b(?:19|20)\d{2}\b')
CITE = re.compile(r'\[[^\]]*?\((?:#ref-[a-z0-9-]+\)|https?://[^)]*)\]|\[[^\]]*\]\(#ref-[a-z0-9-]+\)')

# Apéndices y anexos citados (C4).
APPENDIX = re.compile(r'\bap[ée]ndice\s+([A-Z])\b|\banexo\s+([A-Z])\b', re.I)

# Remisiones: «cap. 37», «capítulo 55», «caps. 64–70», «capítulos 15 a 20».
# El lookbehind evita que una ruta como `imagenes/capitulo60/` cuente como
# remisión, y los separadores de rango no cruzan el salto de línea: un título
# «## Lo esencial del capítulo 25» seguido de una viñeta «- 100…» es una sola
# mención al capítulo 25, no un rango 25–100.
REF = re.compile(
    r'(?<![\w/])(?:cap[íi]tulos?[ \t]+|caps?\.[ \t]*)'
    r'(\d{1,3})(?:[ \t]*[–—-][ \t]*(\d{1,3}))?'
    r'(?:[ \t]+(?:a|al)[ \t]+(\d{1,3}))?', re.I)

# Etiqueta de volumen en la misma expresión: «(Vol. 4, cap. 3)».
VOL_LABEL = re.compile(r'\(\s*Vol\.\s*([1-4])', re.I)

# Remisión mal formada: un paréntesis dentro de otro, con volumen duplicado.
NESTED_REF = re.compile(
    r'\([^()]*(?:\([^()]*\)[^()]*){1,2}Vol\.\s*[1-4][^()]*\)', re.I)

# Restos de la numeración antigua (C5).
LEGACY_PART = re.compile(
    r'\bParte\s+(VIII|VII|VI|IV|V|III|II|IX|X|I)\b(?![\w])|'
    r'\b(?:cap[íi]tulos?[ \t]+|caps?\.[ \t]*)(\d{1,3})[ \t]*[–—-][ \t]*(\d{1,3})',
    re.I)
# --------------------------------------------------------------------------- #
# Utilidades
# --------------------------------------------------------------------------- #

def strip_accents(text):
    """«capítulo» -> «capitulo»: los acentos no deben decidir un diagnóstico."""
    norm = unicodedata.normalize('NFD', text)
    return ''.join(c for c in norm if unicodedata.category(c) != 'Mn')


def slug(text):
    norm = strip_accents(text.lower())
    return re.sub(r'[^a-z0-9]+', '-', norm).strip('-')


def relative(path):
    return str(path.relative_to(ROOT))


def words(text):
    """Palabras de prosa: sin contar los bloques de código."""
    return len(re.sub(r'```.*?```', ' ', text, flags=re.S).split())


def paragraphs(text):
    """Divide en párrafos, conservando la línea de inicio de cada uno.

    Se ignoran bloques de código, tablas y sangrados de código, que es donde
    viven los fragmentos de código de los capítulos: ahí una cifra no es una
    afirmación editorial.
    """
    lines = text.splitlines()
    out, buffer, start, fenced = [], [], 0, False
    for number, line in enumerate(lines, 1):
        if line.lstrip().startswith(('```', '~~~')):
            fenced = not fenced
            continue
        if fenced:
            continue
        if not line.strip():
            if buffer:
                out.append((start, '\n'.join(buffer)))
                buffer = []
            continue
        if line.startswith(('|', '    ', '\t')) or re.match(r'^\s*(?:>|[-*+]|\d+\.)\s*$', line):
            # Una viñeta suelta o una cita corta no es una afirmación: corta el
            # párrafo para no medirla dos veces, pero conserva las largas.
            if len(buffer) < 2:
                if buffer:
                    out.append((start, '\n'.join(buffer)))
                    buffer = []
                continue
        if not buffer:
            start = number
        buffer.append(line)
    if buffer:
        out.append((start, '\n'.join(buffer)))
    return out


def mask_code(text):
    """Enmascara los bloques de código conservando los saltos de línea.

    Se usa en C6: un nombre de modelo dentro de un ejemplo de código es el
    valor de una variable de ejemplo, no una afirmación sobre la vigencia del
    libro. En C1, en cambio, sí se buscan remisiones dentro del código: allí
    un comentario puede apuntar a un capítulo que ya no existe.

    Sustituye el contenido por espacios en lugar de borrarlo para que los
    números de línea del informe sigan coincidiendo con el archivo.
    """
    out, fenced = [], False
    for line in text.splitlines(keepends=True):
        if line.lstrip().startswith(('```', '~~~')):
            fenced = not fenced
            out.append(line)
        elif fenced:
            # Se conservan longitud y saltos: el desplazamiento de los
            # caracteres following debe seguir apuntando a la línea correcta.
            out.append(re.sub(r'[^\n]', ' ', line))
        else:
            out.append(line)
    return ''.join(out)


def find_appendices(volumes):
    """Apéndices y anexos que existen de verdad, por volumen."""
    found = {v.number: set() for v in volumes}
    for volume in volumes:
        for path in sorted(volume.directory.glob('front-matter/*.md')):
            text = path.read_text(encoding='utf-8')
            head = re.search(r'^#\s*(.+)$', text, re.M)
            if not head:
                continue
            title = head.group(1)
            match = re.match(r'\s*(?:ap[ée]ndice|anexo)\s+([A-Z])\b', title, re.I)
            if match:
                found[volume.number].add(match.group(1).upper())
    return found


def read_allowlist():
    if not ALLOWLIST.exists():
        return []
    return [line.strip() for line in ALLOWLIST.read_text(encoding='utf-8').splitlines()
            if line.strip() and not line.strip().startswith('#')]


def allowed_model(identifier, patterns):
    """La lista blanca se compara sin distinguir mayúsculas.

    El manuscrito escribe «GPT-4» con mayúsculas y la lista dice «gpt-*»: sin
    esta normalización, C6 marcaría como literales nombres que sí están
    admitidos, que es peor que no comprobar nada.
    """
    identifier = identifier.lower()
    for pattern in patterns:
        pattern = pattern.lower()
        if pattern.endswith('*') and identifier.startswith(pattern[:-1]):
            return True
        if identifier == pattern:
            return True
    return False
# --------------------------------------------------------------------------- #
# Descubrimiento
# --------------------------------------------------------------------------- #

class Chapter:
    def __init__(self, path, volume):
        self.path = path
        self.volume = volume
        self.text = path.read_text(encoding='utf-8')
        head = re.search(r'^#\s+(.+?)\s*$', self.text, re.M)
        self.title = head.group(1) if head else path.stem
        # El número de capítulo es el del nombre de archivo, no el del título.
        match = re.search(r'(\d+)_capitulo_?(\d*)', path.name)
        self.number = int(match.group(2)) if match and match.group(2) else None
        self.unnumbered = 'epilogo' in path.name or self.number is None
        self.words = words(self.text)
        self.filename = path.name

    @property
    def label(self):
        return f'Vol. {self.volume.number}, cap. {self.number}' if self.number \
            else f'Vol. {self.volume.number}, epílogo'


class TextFile:
    """Un archivo de texto del volumen que no es un capítulo numerado."""

    def __init__(self, path, volume):
        self.path = path
        self.volume = volume
        self.text = path.read_text(encoding='utf-8')
        self.filename = path.name


class Volume:
    def __init__(self, directory):
        self.directory = directory
        self.name = directory.name
        self.number = int(re.match(r'vol([1-4])', directory.name).group(1))
        self.chapters = [Chapter(p, self) for p in
                         sorted(directory.glob('manuscrito/capitulos/*.md'))]
        self.numbered = [c for c in self.chapters if not c.unnumbered]
        self.count = len(self.numbered)
        self.by_number = {c.number: c for c in self.numbered}

    @property
    def title(self):
        meta = self.directory / 'front-matter' / 'metadata_es.yaml'
        if meta.exists():
            line = re.search(r'^subtitle:\s*"?([^"\n]+)', meta.read_text(encoding='utf-8'), re.M)
            if line:
                return line.group(1).split('—')[0].strip()
        return self.name

    def references(self):
        path = self.references_path
        if not path.exists():
            return ''
        return path.read_text(encoding='utf-8')

    @property
    def references_path(self):
        return self.directory / 'referencias' / 'referencias.md'

    def manuscript_files(self):
        """Todo el texto que se compone en el libro, para remisiones y cifras."""
        yield from self.chapters
        for path in sorted(self.directory.glob('front-matter/*.md')):
            yield TextFile(path, self)
        state = self.directory / 'estado-del-arte' / 'estado-del-arte.md'
        if state.exists():
            yield TextFile(state, self)


def volumes():
    return [Volume(d) for d in sorted(ROOT.glob('vol[1-4]-*')) if d.is_dir()]
# --------------------------------------------------------------------------- #
# Comprobaciones
# --------------------------------------------------------------------------- #

def check_c1_crossrefs(vols, add):
    """C1: remisiones a capítulos que no existen, o sin etiqueta de volumen."""
    counts = {v.number: v.count for v in vols}
    for volume in vols:
        for item in volume.manuscript_files():
            text = item.text
            for match in REF.finditer(text):
                numbers = [int(n) for n in match.groups() if n]
                line = text.count('\n', 0, match.start()) + 1
                label = match.group(0)
                # ¿La expresión trae volumen propio? "(Vol. 4, cap. 3)"
                context = text[max(0, match.start() - 60):match.start()]
                labelled = VOL_LABEL.search(context)
                target = int(labelled.group(1)) if labelled else volume.number
                out_of_range = [n for n in numbers if n > counts.get(target, 0)]
                candidates = [v.number for v in vols if v.count >= max(numbers)]
                if out_of_range and not labelled and candidates:
                    # El número existe, pero en otro tomo: falta la etiqueta.
                    add('C1', 'aviso', item, line,
                        f'«{label}» remite al cap. {numbers[0]} sin decir de qué '
                        f'tomo: en el Vol. {volume.number} no existe; sí en '
                        f'{"el Vol. " if len(candidates) == 1 else "los Vols. "}'
                        f'{", ".join(str(c) for c in candidates)}',
                        detail={'numbers': numbers, 'candidates': candidates})
                elif out_of_range:
                    # No existe en ningún tomo: es numeración global antigua.
                    add('C1', 'error', item, line,
                        f'«{label}» usa la numeración global antigua: el cap. '
                        f'{out_of_range[0]} no existe en ningún volumen '
                        f'(máximo actual: {max(counts.values())})',
                        detail={'target': target, 'numbers': numbers})
                if labelled and re.search(r'\(\s*Vol\.\s*\d[^()]*\([^()]*\)\s*\)', context):
                    add('C1', 'aviso', item, line,
                        'remisión con paréntesis anidados: '
                        'conviene la forma «(Vol. N, cap. M)»',
                        detail={'context': context[-60:]})
            # Paréntesis anidados y volumen duplicado: «(capítulo 1 (Vol. 4), Vol. 4)».
            for match in NESTED_REF.finditer(text):
                line = text.count('\n', 0, match.start()) + 1
                add('C1', 'aviso', item, line,
                    f'remisión mal formada: «{match.group(0).strip()[:60]}» — '
                    f'la forma correcta es «(Vol. N, cap. M)»',
                    detail={'text': match.group(0)[:80]})


def check_c2_references(vols, add):
    """C2: entradas bibliográficas que se declaran no verificadas."""
    for volume in vols:
        text = volume.references()
        if not text:
            continue
        # Cada entrada es un bloque `### {#ref-slug}` seguido de su texto.
        blocks = re.split(r'(?m)^###\s*\{#(ref-[^}]+)\}', text)
        for index in range(1, len(blocks) - 1, 2):
            anchor, body = blocks[index], blocks[index + 1]
            if not UNVERIFIED.search(body):
                continue
            line = text.count('\n', 0, text.find('{#' + anchor + '}')) + 1
            label = anchor.replace('ref-', '')
            used = [c for c in volume.chapters if '#' + anchor in c.text]
            where = ', '.join(c.filename for c in used[:3]) or 'sin citarla'
            add('C2', 'error', volume.references_path, line,
                f'«{label}» se declara sin verificar ({where})',
                detail={'anchor': anchor, 'chapters': [c.filename for c in used]})
        # Entradas huérfanas: definidas y nunca citadas (C8, no C2).
        for index in range(1, len(blocks) - 1, 2):
            anchor = blocks[index]
            if f'#{anchor}' not in text and not any(
                    f'#{anchor}' in c.text for c in volume.chapters):
                line = text.count('\n', 0, text.find('{#' + anchor + '}')) + 1
                add('C8', 'aviso', volume.references_path, line,
                    f'«{anchor.replace("ref-", "")}» está en la bibliografía y no se '
                    f'cita en ningún capítulo',
                    detail={'anchor': anchor})
def check_c3_figures(vols, add):
    """C3: párrafos con cifras y sin marca de origen ([D], [E], [I] o cita)."""
    for volume in vols:
        for chapter in volume.chapters:
            for start, paragraph in paragraphs(chapter.text):
                if len(paragraph) < MIN_PROSE_CHARS:
                    continue
                match = FIGURE.search(paragraph)
                if not match:
                    continue
                if SOURCE.search(paragraph):
                    continue
                excerpt = ' '.join(paragraph.split())
                add('C3', 'aviso', chapter, start,
                    f'cifra sin origen declarado: «{match.group(0).strip()}» — '
                    f'marcar [D] dato, [E] estimación o [I] ilustrativa',
                    detail={'excerpt': excerpt[:200]})


def check_c4_placeholders(vols, appendices, add):
    """C4: apéndices citados que no existen y marcadores de contenido pendiente."""
    for volume in vols:
        available = appendices.get(volume.number, set())
        for item in volume.manuscript_files():
            text = item.text
            for match in APPENDIX.finditer(text):
                letter = (match.group(1) or match.group(2) or '').upper()
                if letter and letter not in available:
                    line = text.count('\n', 0, match.start()) + 1
                    add('C4', 'error', item, line,
                        f'se cita el apéndice {letter}, que no existe en el '
                        f'Vol. {volume.number}',
                        detail={'appendix': letter})
            for match in PENDING.finditer(text):
                line = text.count('\n', 0, match.start()) + 1
                snippet = match.group(0).strip()
                if 'Depósito Legal' in text[max(0, match.start() - 40):match.start() + 20]:
                    # Depósito legal e ISBN los tramita la editorial, no el linter.
                    continue
                add('C4', 'aviso', item, line,
                    f'marcador pendiente: «{snippet}»',
                    detail={'snippet': snippet})


def check_c5_legacy_numbering(vols, add):
    """C5: restos de la numeración global por partes (caps. 1–79).

    Solo se marca aquí lo que ningún tomo puede alojar; los rangos que sí
    existen en otro volumen los reporta C1 como «falta la etiqueta del tomo».
    """
    tomos = len(vols)
    total = sum(v.count for v in vols)
    ceiling = max(v.count for v in vols)
    for volume in vols:
        for item in volume.manuscript_files():
            text = item.text
            for match in LEGACY_PART.finditer(text):
                part, first, last = match.group(1), match.group(2), match.group(3)
                line = text.count('\n', 0, match.start()) + 1
                if part:
                    add('C5', 'error', item, line,
                        f'«Parte {part}» pertenece a la numeración antigua: la serie '
                        f'son {tomos} volúmenes de numeración propia, no siete partes',
                        detail={'part': part})
                elif int(last) > ceiling:
                    add('C5', 'error', item, line,
                        f'«{match.group(0).strip()}» usa numeración global; ningún '
                        f'volumen llega al cap. {int(last)} (la serie suma {total} '
                        f'capítulos repartidos en {tomos} tomos)',
                        detail={'first': int(first), 'last': int(last)})


def check_c6_models(vols, add):
    """C6: identificadores de modelo literales fuera de la lista blanca."""
    patterns = read_allowlist()
    for volume in vols:
        for item in volume.manuscript_files():
            for match in MODEL_ID.finditer(mask_code(item.text)):
                identifier = match.group(0)
                if allowed_model(identifier, patterns):
                    continue
                line = item.text.count('\n', 0, match.start()) + 1
                add('C6', 'aviso', item, line,
                    f'«{identifier}» está fijado en el texto: los modelos y sus '
                    f'precios cambian; consúltense en el apéndice B',
                    detail={'identifier': identifier})


def check_c7_budget(vols, add):
    """C7: capítulos fuera del presupuesto de palabras."""
    for volume in vols:
        for chapter in volume.chapters:
            if chapter.words < MIN_WORDS:
                add('C7', 'aviso', chapter, 1,
                    f'{chapter.words} palabras (mínimo {MIN_WORDS}): capítulo corto',
                    detail={'words': chapter.words, 'min': MIN_WORDS})
            elif chapter.words > MAX_WORDS:
                add('C7', 'aviso', chapter, 1,
                    f'{chapter.words} palabras (máximo {MAX_WORDS}): '
                    f'considerar dividirlo',
                    detail={'words': chapter.words, 'max': MAX_WORDS})
def check_c8_anchors(vols, add):
    """C8: anclas `#ref-` citadas que no tienen entrada en la bibliografía.

    Las entradas nunca citadas las reporta check_c2_references, que ya tiene el
    texto de la bibliografía de cada volumen abierto.
    """
    for volume in vols:
        known = set(re.findall(r'(?m)^###\s*\{#(ref-[^}]+)\}', volume.references()))
        for item in volume.manuscript_files():
            for match in re.finditer(r'#(ref-[a-z0-9_-]+)', item.text):
                anchor = match.group(1)
                if anchor in known:
                    continue
                line = item.text.count('\n', 0, match.start()) + 1
                add('C8', 'error', item, line,
                    f'«#{anchor}» no tiene entrada en la bibliografía del '
                    f'Vol. {volume.number}',
                    detail={'anchor': anchor})


def check_image_folders(vols, add):
    """Carpetas de imágenes cuyo nombre no sigue la numeración vigente.

    No rompen la composición (la ruta existe), pero delatan la numeración
    global antigua y desorientan a quien mantenga las figuras.
    """
    for volume in vols:
        images = volume.directory / 'manuscrito' / 'imagenes'
        if not images.is_dir():
            continue
        for folder in sorted(images.glob('capitulo*')):
            legacy = re.search(r'capitulo(\d+)', folder.name)
            if not legacy:
                continue
            owners = sorted({str(c.number) for c in volume.chapters
                             if folder.name in c.text})
            if legacy.group(1).lstrip('0') in {n.lstrip('0') for n in owners}:
                continue
            add('C9', 'aviso', folder, 1,
                f'`{folder.name}` guarda la numeración antigua: lo usa el '
                f'cap. {", ".join(owners) or "?"} de este volumen',
                detail={'folder': folder.name, 'chapters': owners})


def check_c11_citation_years(vols, add):
    """C11: el año de la cita en el texto no coincide con el de la entrada.

    Una cita que dice «(McKinsey, 2021)» y apunta a una entrada fechada en 2024
    no es una entrada sin verificar: es una cita que dice una cosa y remite a
    otra. Ninguna de las dos se puede arreglar maquetando, pero sí se puede
    detectar sin leerlas.
    """
    for volume in vols:
        texto = volume.references()
        if not texto:
            continue
        bloques = re.split(r'(?m)^###\s*\{#ref-([a-z0-9_-]+)\}', texto)
        anios = {}
        for i in range(1, len(bloques) - 1, 2):
            anios[bloques[i]] = {int(a) for a in re.findall(YEAR, bloques[i + 1][:400])}
        for item in volume.manuscript_files():
            for match in re.finditer(r'([^\n\n]{0,90}?)\[([^\]]*)\]\(#ref-([a-z0-9_-]+)\)',
                                     item.text):
                etiqueta, anio_texto, anchor = match.group(1), match.group(2), match.group(3)
                if anchor not in anios or not anios[anchor]:
                    continue
                citados = {int(a) for a in re.findall(YEAR, etiqueta + ' ' + anio_texto)}
                if citados and not (citados & anios[anchor]):
                    line = item.text.count('\n', 0, match.start()) + 1
                    add('C11', 'error', item, line,
                        f'la cita dice {", ".join(str(a) for a in sorted(citados))} y la '
                        f'entrada «{anchor.replace("ref-", "")}» es de '
                        f'{", ".join(str(a) for a in sorted(anios[anchor]))}',
                        detail={'anchor': anchor,
                                'texto': sorted(citados), 'entrada': sorted(anios[anchor])})


def mask_inline_code(text):
    """Enmascara bloques de codigo y comillas inversas conservando la longitud.

    Es lo que permite que C12 distinga un identificador de codigo citado en la
    prosa (que va entrecomillado) de una palabra pegada por error.
    """
    text = re.sub(r'(?ms)^(```|~~~).*?^\1',
                  lambda m: re.sub(r'[^\n]', ' ', m.group(0)), text)
    return re.sub(r'`[^`\n]*`', lambda m: re.sub(r'[^\n]', ' ', m.group(0)), text)


def check_c12_language(vols, add):
    """C12: palabra pegada a un identificador, fuera de codigo y comillas.

    Se mide sobre el texto con los bloques de codigo y las comillas inversas
    enmascarados: dentro de ellos, un identificador pegado es lo normal.
    """
    glued = re.compile(GLUED)
    for volume in vols:
        for item in volume.manuscript_files():
            if item.path.name == 'referencias.md':
                continue
            text = mask_inline_code(item.text)
            for number, line in enumerate(text.splitlines(), 1):
                stripped = line.lstrip()
                if stripped.startswith(('|', '#', '>')):
                    continue
                match = glued.search(line)
                if not match:
                    continue
                add('C12', 'aviso', item, number,
                    f'\u00ab{match.group(0)}\u00bb pegado a la palabra anterior, fuera de '
                    f'comillas inversas: si es un identificador de codigo, entrecom\u00edllalo; '
                    f'si no lo es, es un error de edici\u00f3n',
                    detail={'token': match.group(0)})


CHECKS = (
    ('C1', 'remisiones cruzadas', check_c1_crossrefs),
    ('C2', 'bibliografía sin verificar', check_c2_references),
    ('C3', 'cifras sin origen declarado', check_c3_figures),
    ('C4', 'apéndices y marcadores pendientes', check_c4_placeholders),
    ('C5', 'numeración antigua', check_c5_legacy_numbering),
    ('C6', 'modelos fijados en el texto', check_c6_models),
    ('C7', 'presupuesto de palabras', check_c7_budget),
    ('C8', 'anclas bibliográficas', check_c8_anchors),
    ('C9', 'carpetas de imágenes', check_image_folders),
    ('C11', 'año de la cita', check_c11_citation_years),
    ('C12', 'lenguaje', check_c12_language),
)


# --------------------------------------------------------------------------- #
# Informe
# --------------------------------------------------------------------------- #

def render(vols, findings, selected):
    lines = [
        '# Auditoría del manuscrito',
        '',
        f'Fecha: {date.today().isoformat()} · {len(vols)} volúmenes · '
        f'{sum(v.count for v in vols)} capítulos · '
        f'{sum(words(c.text) for v in vols for c in v.chapters):,} palabras de prosa'
        .replace(',', '.'),
        '',
        'Generado por `tools/lint_manuscript.py`. Complementa a '
        '`validate_editions.py`, que solo comprueba la maquetación. '
        'La lista completa de hallazgos está en `dist/AUDIT.json`; este '
        'informe se recorta por archivo para que se pueda leer.',
        '',
        '## Resumen por comprobación',
        '',
        '| ID | Comprobación | Errores | Avisos |',
        '|---|---|---:|---:|',
    ]
    for code, name, _ in CHECKS:
        if code not in selected:
            continue
        errors = sum(1 for f in findings if f['check'] == code and f['severity'] == 'error')
        warnings = sum(1 for f in findings if f['check'] == code and f['severity'] == 'aviso')
        lines.append(f'| {code} | {name} | {errors} | {warnings} |')

    lines += ['', '## Detalle por volumen', '',
              '| Volumen | Capítulos | Palabras | Errores | Avisos |',
              '|---|---:|---:|---:|---:|']
    for volume in vols:
        mine = [f for f in findings if f.get('volume') == volume.number]
        errors = sum(1 for f in mine if f['severity'] == 'error')
        warnings = sum(1 for f in mine if f['severity'] == 'aviso')
        lines.append(f'| {volume.number} — {volume.title} | {volume.count} | '
                     f'{sum(c.words for c in v_chapters(volume)):,} | {errors} | {warnings} |'
                     .replace(',', '.'))

    for code, name, _ in CHECKS:
        mine = [f for f in findings if f['check'] == code]
        if not mine:
            continue
        lines += ['', f'## {code} · {name} ({len(mine)})', '']
        by_file = {}
        for finding in mine:
            by_file.setdefault(finding['file'], []).append(finding)
        for path in sorted(by_file):
            shown = sorted(by_file[path], key=lambda f: f['line'])
            lines.append(f'**`{path}`**')
            lines.append('')
            for finding in shown[:MAX_DETAIL_PER_FILE]:
                mark = '✘' if finding['severity'] == 'error' else '!'
                lines.append(f'- L{finding["line"]} {mark} {finding["message"]}')
            if len(shown) > MAX_DETAIL_PER_FILE:
                lines.append(f'- … y {len(shown) - MAX_DETAIL_PER_FILE} más en '
                             f'`dist/AUDIT.json`')
            lines.append('')
    return '\n'.join(lines) + '\n'


def v_chapters(volume):
    return [c for c in volume.chapters if not c.unnumbered]
def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--vol', action='append', default=[],
                        help='restringe la auditoría a un volumen (repetible)')
    parser.add_argument('--only', nargs='+', default=None, metavar='CID',
                        help='solo estas comprobaciones (p. ej. --only C1 C3)')
    parser.add_argument('--no-json', action='store_true',
                        help='no escribir dist/AUDIT.json')
    parser.add_argument('--quiet', action='store_true',
                        help='no imprimir el informe por stdout')
    args = parser.parse_args()

    vols = volumes()
    if args.vol:
        wanted = {name for name in args.vol}
        vols = [v for v in vols if v.name in wanted or str(v.number) in wanted]
    if not vols:
        parser.error('No hay volúmenes que auditar')

    selected = {code for code, _, _ in CHECKS}
    if args.only:
        selected = {code.upper() for code in args.only}
        unknown = selected - selected.intersection({c for c, _, _ in CHECKS})
        if unknown:
            parser.error(f'Comprobación desconocida: {", ".join(sorted(unknown))}')

    findings = []

    def add(check, severity, item, line, message, detail=None):
        where = getattr(item, 'path', item)
        volume = getattr(item, 'volume', None)
        findings.append({
            'check': check,
            'severity': severity,
            'file': relative(where),
            'line': line,
            'message': message,
            'volume': volume.number if volume else None,
            'detail': detail or {},
        })

    appendices = find_appendices(vols)
    runners = {
        'C1': lambda: check_c1_crossrefs(vols, add),
        'C2': lambda: check_c2_references(vols, add),
        'C3': lambda: check_c3_figures(vols, add),
        'C4': lambda: check_c4_placeholders(vols, appendices, add),
        'C5': lambda: check_c5_legacy_numbering(vols, add),
        'C6': lambda: check_c6_models(vols, add),
        'C7': lambda: check_c7_budget(vols, add),
        'C8': lambda: check_c8_anchors(vols, add),
        'C9': lambda: check_image_folders(vols, add),
        'C11': lambda: check_c11_citation_years(vols, add),
        'C12': lambda: check_c12_language(vols, add),
    }
    for code, _, _ in CHECKS:
        if code in selected:
            runners[code]()

    findings.sort(key=lambda f: (f['check'], f['file'], f['line']))
    report = render(vols, findings, selected)

    target = ROOT / 'dist'
    target.mkdir(exist_ok=True)
    (target / 'AUDIT.md').write_text(report, encoding='utf-8')
    if not args.no_json:
        (target / 'AUDIT.json').write_text(json.dumps({
            'date': date.today().isoformat(),
            'checks': {code: name for code, name, _ in CHECKS if code in selected},
            'volumes': [{'number': v.number, 'name': v.name, 'chapters': v.count,
                         'words': sum(c.words for c in v_chapters(v))} for v in vols],
            'findings': findings,
        }, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

    if not args.quiet:
        print(report)
        print('Informe: dist/AUDIT.md', file=sys.stderr)

    errors = sum(1 for f in findings if f['severity'] == 'error')
    warnings = len(findings) - errors
    print(f'lint_manuscript: {errors} errores, {warnings} avisos', file=sys.stderr)
    return 1 if errors else 0


if __name__ == '__main__':
    raise SystemExit(main())
