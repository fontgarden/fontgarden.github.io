#!/usr/bin/env python3
"""Tests of scripts/import_font.py.

    python3 -m unittest scripts/test_import_font.py

Each test builds a small font in a temporary folder. No test reads a font
project or writes to the website.
"""
import json
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path
from unittest import mock

from fontTools.feaLib.builder import addOpenTypeFeaturesFromString
from fontTools.fontBuilder import FontBuilder
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.ttLib import TTFont

sys.path.insert(0, str(Path(__file__).resolve().parent))
import import_font  # noqa: E402

CHARACTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789/'
FEATURES = """
feature liga { sub f i by f_i; } liga;
feature tnum { sub one by one.tf; sub two by two.tf; } tnum;
feature kern { pos A V -80; } kern;
"""


def square():
    pen = TTGlyphPen(None)
    pen.moveTo((50, 0))
    pen.lineTo((50, 700))
    pen.lineTo((450, 700))
    pen.lineTo((450, 0))
    pen.closePath()
    return pen.glyph()


def build_font(path, family='Test Sans'):
    """Write a font with the Latin alphabet, the figures and three features."""
    cmap = {ord(character): f'u{ord(character):04X}' for character in CHARACTERS}
    cmap.update({ord('f'): 'f', ord('i'): 'i', ord('1'): 'one', ord('2'): 'two',
                 ord('A'): 'A', ord('V'): 'V', ord(' '): 'space'})
    glyphs = ['.notdef', *dict.fromkeys(cmap.values()), 'f_i', 'one.tf', 'two.tf']
    builder = FontBuilder(1000, isTTF=True)
    builder.setupGlyphOrder(glyphs)
    builder.setupCharacterMap(cmap)
    builder.setupGlyf({name: square() for name in glyphs})
    builder.setupHorizontalMetrics({name: (500, 50) for name in glyphs})
    builder.setupHorizontalHeader(ascent=800, descent=-200)
    builder.setupNameTable({'familyName': family, 'styleName': 'Regular',
                            'version': 'Version 2.500;test'})
    builder.setupOS2(sCapHeight=700, sxHeight=500)
    builder.setupPost()
    addOpenTypeFeaturesFromString(builder.font, FEATURES)
    builder.save(path)


def build_project(root, family='Test Sans'):
    project = root / 'test-sans'
    (project / 'fonts/variable').mkdir(parents=True)
    build_font(project / 'fonts/variable/TestSans[wght].ttf', family)
    (project / 'OFL.txt').write_text('Copyright 2026 The Test Sans Project Authors\n\nLicense text\n')
    return project


class NumberTest(unittest.TestCase):
    def test_whole_number_has_no_fraction(self):
        self.assertEqual(import_font.number(400.0), 400)
        self.assertIsInstance(import_font.number(400.0), int)

    def test_fraction_has_two_places(self):
        self.assertEqual(import_font.number(62.456), 62.46)


class CharacterGroupsTest(unittest.TestCase):
    def test_groups_by_script_then_figures_symbols_and_marks(self):
        codepoints = [*range(ord('a'), ord('z') + 1), ord('1'), ord('+'), 0x0301, ord(' ')]
        supported, groups = import_font.character_groups(codepoints)
        self.assertEqual([script['tag'] for script in supported], ['Latn'])
        self.assertEqual(supported[0]['count'], 26)
        self.assertEqual([group['name'] for group in groups],
                         ['Latin', 'Figures', 'Punctuation and symbols', 'Marks'])

    def test_space_is_in_no_group(self):
        _, groups = import_font.character_groups([ord(' ')])
        self.assertEqual(groups, [])

    def test_script_with_few_characters_goes_to_symbols(self):
        supported, groups = import_font.character_groups([0x03A9, ord('+')])
        self.assertEqual(supported, [])
        self.assertEqual([entry[0] for entry in groups[0]['characters']], [ord('+'), 0x03A9])


class FontTest(unittest.TestCase):
    """Tests that read the test font."""

    @classmethod
    def setUpClass(cls):
        cls.folder = tempfile.TemporaryDirectory()
        cls.root = Path(cls.folder.name)
        cls.project = build_project(cls.root)
        cls.source = cls.project / 'fonts/variable/TestSans[wght].ttf'

    @classmethod
    def tearDownClass(cls):
        cls.folder.cleanup()

    def test_feature_samples_come_from_the_font(self):
        samples = {sample['tag']: sample['sample']
                   for sample in import_font.feature_samples(TTFont(self.source))}
        self.assertEqual(samples, {'kern': 'AVATAR Type Wave', 'liga': 'fi', 'tnum': '12'})

    def test_feature_lists(self):
        font = TTFont(self.source)
        self.assertEqual(import_font.features(font, 'GSUB'), ['liga', 'tnum'])
        self.assertEqual(import_font.features(font, 'GPOS'), ['kern'])

    def test_index_font_has_only_the_alphabet_and_the_name(self):
        target = self.root / 'index.woff2'
        import_font.write_index_font(self.source, target, 'Test Sans')
        characters = {chr(codepoint) for codepoint in TTFont(target).getBestCmap()}
        self.assertEqual(characters, set(import_font.INDEX_CHARACTERS))
        self.assertLess(target.stat().st_size, self.source.stat().st_size)

    def test_revision_of_a_folder_without_git_is_none(self):
        with mock.patch.object(import_font.subprocess, 'run') as run:
            run.return_value.stdout = ''
            self.assertIsNone(import_font.revision(self.project))


class ImportTest(unittest.TestCase):
    """One complete import into a temporary website folder."""

    @classmethod
    def setUpClass(cls):
        cls.folder = tempfile.TemporaryDirectory()
        root = Path(cls.folder.name)
        cls.site = root / 'site'
        entries = cls.site / 'src/content/fonts'
        entries.mkdir(parents=True)
        (entries / 'test-sans.yaml').write_text('number: 7\nname: Test Sans\n')
        cls.project = build_project(root)
        cls.patches = [
            mock.patch.object(import_font, 'SITE', cls.site),
            mock.patch.object(import_font, 'ENTRIES', entries),
            mock.patch.object(import_font, 'FACTS', cls.site / 'src/data/fonts'),
            mock.patch.object(import_font, 'revision',
                              return_value={'commit': 'abc1234', 'date': '2026-01-02'}),
            mock.patch('builtins.print'),
        ]
        for patch in cls.patches:
            patch.start()
        import_font.import_font(cls.project, 'test-sans')
        cls.facts = json.loads((cls.site / 'src/data/fonts/test-sans.json').read_text())

    @classmethod
    def tearDownClass(cls):
        for patch in cls.patches:
            patch.stop()
        cls.folder.cleanup()

    def test_facts(self):
        self.assertEqual(self.facts['family'], 'Test Sans')
        self.assertEqual(self.facts['version'], '2.500')
        self.assertEqual(self.facts['copyright'], 'Copyright 2026 The Test Sans Project Authors')
        self.assertEqual(self.facts['revision'], {'commit': 'abc1234', 'date': '2026-01-02'})
        self.assertEqual(self.facts['unitsPerEm'], 1000)
        self.assertEqual(self.facts['metrics'],
                         {'ascender': 800, 'capHeight': 700, 'xHeight': 500, 'descender': -200})
        self.assertEqual(self.facts['axes'], [])
        self.assertEqual([script['tag'] for script in self.facts['scripts']], ['Latn'])
        # The space is not a character of a group.
        self.assertEqual(self.facts['characterCount'], len(CHARACTERS))

    def test_each_file_of_the_facts_exists(self):
        files = self.facts['files']
        for key in ('woff2', 'indexWoff2', 'download', 'preview'):
            path = self.site / 'public' / files[key].lstrip('/')
            self.assertTrue(path.is_file(), key)
            self.assertEqual(files[key].split('/')[1:3], ['fonts', 'test-sans'])
        self.assertEqual(files['woff2Bytes'],
                         (self.site / 'public/fonts/test-sans/test-sans.woff2').stat().st_size)

    def test_download_has_the_font_twice_and_the_license(self):
        archive = self.site / 'public/fonts/test-sans/test-sans.zip'
        with zipfile.ZipFile(archive) as bundle:
            self.assertEqual(sorted(bundle.namelist()),
                             ['OFL.txt', 'TestSans[wght].ttf', 'TestSans[wght].woff2'])

    def test_check_passes_at_the_recorded_revision(self):
        import_font.check(self.project.parent)

    def test_check_fails_at_another_revision(self):
        import_font.revision.return_value = {'commit': 'def5678', 'date': '2026-01-03'}
        try:
            with self.assertRaises(SystemExit) as failure:
                import_font.check(self.project.parent)
            self.assertIn('imported at abc1234', str(failure.exception))
        finally:
            import_font.revision.return_value = {'commit': 'abc1234', 'date': '2026-01-02'}

    def test_two_fonts_in_the_project_is_a_fault(self):
        extra = self.project / 'fonts/variable/Extra.ttf'
        extra.write_bytes(b'')
        try:
            with self.assertRaises(SystemExit):
                import_font.import_font(self.project, 'test-sans')
        finally:
            extra.unlink()


if __name__ == '__main__':
    unittest.main()
