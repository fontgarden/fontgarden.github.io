#!/usr/bin/env python3
"""Import the variable font of a font project into the font index.

    python3 scripts/import_font.py --project DIR --slug NAME
    python3 scripts/import_font.py --all --projects PARENT
    python3 scripts/import_font.py --check --projects PARENT

DIR is a checkout of a Font.Garden font project. The script reads the one
variable font in DIR/fonts/variable and DIR/OFL.txt. It writes:

- public/fonts/NAME/NAME.woff2   the font that the pages load
- public/fonts/NAME/NAME-index.woff2   the small font of the index list
- public/fonts/NAME/NAME.zip     the download: the TTF, the WOFF2 and OFL.txt
- public/fonts/NAME/NAME.png     the picture of a link to the specimen page
- src/data/fonts/NAME.json       the facts that the specimen page shows

--all imports each font that has an entry in src/content/fonts. The project
of a font is PARENT/NAME. --check writes nothing. It fails when the facts of
a font name a revision that is not the current revision of its project.

The script needs fontTools, brotli and Pillow. The Python of a font project
has them: DIR/.venv/bin/python.
"""
import argparse
import json
import re
import subprocess
import sys
import unicodedata
import zipfile
from pathlib import Path

from fontTools import subset
from fontTools import unicodedata as ftunicodedata
from fontTools.ttLib import TTFont
from PIL import Image, ImageDraw, ImageFont

SITE = Path(__file__).resolve().parent.parent
ENTRIES = SITE / 'src/content/fonts'
FACTS = SITE / 'src/data/fonts'
# The picture of a link: the size of the Open Graph image, in the site colors.
PREVIEW_SIZE = (1200, 630)
PREVIEW_MARGIN = 64
PREVIEW_PAPER = '#10120f'
PREVIEW_INK = '#ececea'
# A script is in the list of a font when the font has this many characters of it.
MINIMUM_SCRIPT_CHARACTERS = 20
AXIS_NAMES = {
    'wght': 'Weight',
    'wdth': 'Width',
    'opsz': 'Optical size',
    'slnt': 'Slant',
    'ital': 'Italic',
    'GRAD': 'Grade',
}
# The features that the specimen page shows with a sample. Each other
# feature is for shaping, and the page gives only its tag.
FEATURE_NAMES = {
    'kern': 'Kerning',
    'liga': 'Standard ligatures',
    'dlig': 'Discretionary ligatures',
    'tnum': 'Tabular figures',
    'pnum': 'Proportional figures',
    'lnum': 'Lining figures',
    'onum': 'Oldstyle figures',
    'zero': 'Slashed zero',
    'frac': 'Fractions',
    'sups': 'Superiors',
    'subs': 'Inferiors',
    'ordn': 'Ordinals',
    'case': 'Case-sensitive forms',
    'smcp': 'Small capitals',
    'c2sc': 'Small capitals from capitals',
    'salt': 'Stylistic alternates',
    **{f'ss{n:02d}': f'Stylistic set {n}' for n in range(1, 21)},
}
# The sample of a feature that has no direct list of input characters.
FIXED_FEATURE_SAMPLES = {
    'kern': 'AVATAR Type Wave',
    'frac': '1/2 3/4 5/8',
}
# The characters of the small font that the index list loads: the alphabet
# of the panel. The importer adds the characters of the name of the font.
INDEX_CHARACTERS = (
    'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789 '
)
# The largest number of characters or ligatures in a sample.
FEATURE_SAMPLE_ITEMS = 16


def number(value):
    """Write 400.0 as 400."""
    return int(value) if float(value).is_integer() else round(value, 2)


def character_groups(codepoints):
    """Group the characters by script, then figures, marks and symbols."""
    scripts = {}
    figures, marks, symbols = [], [], []
    for codepoint in sorted(codepoints):
        character = chr(codepoint)
        category = unicodedata.category(character)
        if category[0] in 'ZC':
            continue
        entry = [codepoint, unicodedata.name(character, '')]
        script = ftunicodedata.script(character)
        if category[0] == 'M':
            marks.append(entry)
        elif category[0] == 'N' and script in ('Zyyy', 'Zinh'):
            figures.append(entry)
        elif script in ('Zyyy', 'Zinh', 'Zzzz'):
            symbols.append(entry)
        else:
            scripts.setdefault(script, []).append(entry)

    groups, supported = [], []
    for tag, entries in sorted(scripts.items(), key=lambda item: -len(item[1])):
        name = ftunicodedata.script_name(tag).replace('_', ' ')
        if len(entries) < MINIMUM_SCRIPT_CHARACTERS:
            symbols.extend(entries)
            continue
        supported.append({'tag': tag, 'name': name, 'count': len(entries)})
        groups.append({'name': name, 'tag': tag, 'characters': entries})
    symbols.sort()
    for name, entries in (
        ('Figures', figures),
        ('Punctuation and symbols', symbols),
        ('Marks', marks),
    ):
        if entries:
            groups.append({'name': name, 'tag': None, 'characters': entries})
    return supported, groups


def features(font, table):
    if table not in font:
        return []
    records = font[table].table.FeatureList.FeatureRecord
    return sorted({record.FeatureTag for record in records})


def feature_samples(font):
    """Give a sample text for each feature that the specimen page shows.

    The sample comes from the font: the input characters of the single
    substitutions and the ligatures of the feature.
    """
    cmap = font.getBestCmap()
    character = {}
    for codepoint, glyph in sorted(cmap.items()):
        # A mark alone is not a clear sample.
        if unicodedata.category(chr(codepoint))[0] != 'M':
            character.setdefault(glyph, chr(codepoint))
    inputs = {}
    if 'GSUB' in font:
        table = font['GSUB'].table
        for record in table.FeatureList.FeatureRecord:
            items = inputs.setdefault(record.FeatureTag, [])
            for index in record.Feature.LookupListIndex:
                for subtable in table.LookupList.Lookup[index].SubTable:
                    subtable = getattr(subtable, 'ExtSubTable', subtable)
                    for glyph in getattr(subtable, 'mapping', {}):
                        if isinstance(subtable.mapping[glyph], str):
                            items.append([glyph])
                    for first, ligatures in getattr(subtable, 'ligatures', {}).items():
                        items.extend([first, *ligature.Component] for ligature in ligatures)
    present = set(inputs) | set(features(font, 'GPOS'))
    samples = []
    for tag, name in FEATURE_NAMES.items():
        if tag not in present:
            continue
        fixed = FIXED_FEATURE_SAMPLES.get(tag)
        if fixed:
            text = fixed if all(ord(c) in cmap for c in fixed if c != ' ') else ''
        else:
            texts = []
            for glyphs in inputs.get(tag, []):
                if all(glyph in character for glyph in glyphs):
                    item = ''.join(character[glyph] for glyph in glyphs)
                    if item not in texts:
                        texts.append(item)
            texts = texts[:FEATURE_SAMPLE_ITEMS]
            text = (' ' if any(len(item) > 1 for item in texts) else '').join(texts)
        if text:
            samples.append({'tag': tag, 'name': name, 'sample': text})
    return samples


def write_index_font(source, target, family):
    """Write the small font of the index list: the alphabet and the name.

    The index list shows each font at its default style, with kerning.
    """
    options = subset.Options()
    options.flavor = 'woff2'
    options.layout_features = ['kern', 'mark', 'mkmk', 'ccmp']
    options.name_IDs = [1, 2, 16, 17]
    options.notdef_outline = True
    options.drop_tables += ['meta']
    font = TTFont(source)
    subsetter = subset.Subsetter(options)
    subsetter.populate(text=INDEX_CHARACTERS + family)
    subsetter.subset(font)
    font.flavor = 'woff2'
    font.save(target)


def revision(project):
    result = subprocess.run(
        ['git', '-C', str(project), 'log', '-1', '--format=%h %cs'],
        capture_output=True, text=True, check=False,
    )
    parts = result.stdout.split()
    return {'commit': parts[0], 'date': parts[1]} if len(parts) == 2 else None


def entry_field(slug, field):
    """Read one field of the entry of a font. The entry can be missing."""
    entry = ENTRIES / f'{slug}.yaml'
    if not entry.exists():
        return None
    match = re.search(rf'^{field}:\s*(.+)$', entry.read_text(), re.M)
    return match.group(1).strip() if match else None


def write_preview(source, target, slug, family, lines):
    """Draw the picture of a link: the name of the font, in the font."""
    width, height = PREVIEW_SIZE
    measure = width - 2 * PREVIEW_MARGIN
    image = Image.new('RGB', PREVIEW_SIZE, PREVIEW_PAPER)
    draw = ImageDraw.Draw(image)
    label = ImageFont.truetype(str(source), 32)
    number = entry_field(slug, 'number')
    top = f'FTGD-{int(number):02d}' if number is not None else 'FTGD-100'
    draw.text((PREVIEW_MARGIN, PREVIEW_MARGIN), top, font=label, fill=PREVIEW_INK)
    site = 'Font.Garden'
    draw.text((width - PREVIEW_MARGIN - draw.textlength(site, font=label), PREVIEW_MARGIN),
              site, font=label, fill=PREVIEW_INK)
    # The name is as wide as the measure, and not taller than a third of the picture.
    trial = ImageFont.truetype(str(source), 100)
    size = min(100 * measure / draw.textlength(family, font=trial), height / 3)
    draw.text((PREVIEW_MARGIN, height / 2), family, font=ImageFont.truetype(str(source), size),
              fill=PREVIEW_INK, anchor='lm')
    y = height - PREVIEW_MARGIN
    for line in reversed(lines):
        draw.text((PREVIEW_MARGIN, y), line, font=label, fill=PREVIEW_INK, anchor='ls')
        y -= 44
    image.save(target, optimize=True)


def slugs():
    return sorted(path.stem for path in ENTRIES.glob('*.yaml'))


def check(projects):
    """Compare the revision in the facts of each font with its project."""
    faults = []
    for slug in slugs():
        facts = FACTS / f'{slug}.json'
        if not facts.exists():
            faults.append(f'{slug}: no facts file')
            continue
        recorded = json.loads(facts.read_text())['revision']
        current = revision(projects / slug)
        if current is None:
            faults.append(f'{slug}: {projects / slug} is not a Git checkout')
        elif recorded != current:
            faults.append(f'{slug}: imported at {recorded and recorded["commit"]}, '
                          f'the project is at {current["commit"]}')
    if faults:
        sys.exit('\n'.join(faults))
    print(f'The facts of {len(slugs())} fonts name the current revision of their project.')


def main():
    parser = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    parser.add_argument('--project', type=Path)
    parser.add_argument('--slug')
    parser.add_argument('--all', action='store_true')
    parser.add_argument('--check', action='store_true')
    parser.add_argument('--projects', type=Path)
    args = parser.parse_args()
    if args.check or args.all:
        if not args.projects:
            parser.error('--all and --check need --projects')
        if args.check:
            check(args.projects)
        else:
            for slug in slugs():
                import_font(args.projects / slug, slug)
    elif args.project and args.slug:
        import_font(args.project, args.slug)
    else:
        parser.error('give --project and --slug, or --all, or --check')


def import_font(project, slug):
    candidates = sorted((project / 'fonts/variable').glob('*.ttf'))
    if len(candidates) != 1:
        sys.exit(f'{project}/fonts/variable must hold one TTF, found {len(candidates)}')
    source = candidates[0]
    license_file = project / 'OFL.txt'
    if not license_file.exists():
        sys.exit(f'{license_file} does not exist')

    font = TTFont(source)
    names = font['name']
    os2 = font['OS/2']
    supported, groups = character_groups(font.getBestCmap())

    axes, instances = [], []
    if 'fvar' in font:
        for axis in font['fvar'].axes:
            axes.append({
                'tag': axis.axisTag,
                'name': AXIS_NAMES.get(axis.axisTag, names.getDebugName(axis.axisNameID)),
                'min': number(axis.minValue),
                'default': number(axis.defaultValue),
                'max': number(axis.maxValue),
            })
        for instance in font['fvar'].instances:
            instances.append({
                'name': names.getDebugName(instance.subfamilyNameID),
                'coordinates': {tag: number(v) for tag, v in instance.coordinates.items()},
            })

    public = SITE / 'public/fonts' / slug
    public.mkdir(parents=True, exist_ok=True)
    woff2 = public / f'{slug}.woff2'
    font.flavor = 'woff2'
    font.save(woff2)

    archive = public / f'{slug}.zip'
    with zipfile.ZipFile(archive, 'w', zipfile.ZIP_DEFLATED) as bundle:
        bundle.write(source, source.name)
        bundle.write(woff2, source.with_suffix('.woff2').name)
        bundle.write(license_file, 'OFL.txt')

    family = names.getDebugName(16) or names.getDebugName(1)
    index_woff2 = public / f'{slug}-index.woff2'
    write_index_font(source, index_woff2, family)
    write_preview(source, public / f'{slug}.png', slug, family, [
        ', '.join(script['name'] for script in supported),
        ', '.join(f"{axis['name']} {axis['min']} to {axis['max']}" for axis in axes),
    ])

    data = {
        'family': family,
        'version': names.getDebugName(5).split(';')[0].replace('Version ', ''),
        'copyright': license_file.read_text().splitlines()[0].strip(),
        'license': 'SIL Open Font License 1.1',
        'licenseUrl': 'https://openfontlicense.org',
        'revision': revision(project),
        'unitsPerEm': font['head'].unitsPerEm,
        'metrics': {
            'ascender': font['hhea'].ascent,
            'capHeight': os2.sCapHeight,
            'xHeight': os2.sxHeight,
            'descender': font['hhea'].descent,
        },
        'glyphCount': font['maxp'].numGlyphs,
        'characterCount': sum(len(group['characters']) for group in groups),
        'axes': axes,
        'instances': instances,
        'scripts': supported,
        'features': {'GSUB': features(font, 'GSUB'), 'GPOS': features(font, 'GPOS')},
        'featureSamples': feature_samples(font),
        'files': {
            'woff2': f'/fonts/{slug}/{woff2.name}',
            'woff2Bytes': woff2.stat().st_size,
            'indexWoff2': f'/fonts/{slug}/{index_woff2.name}',
            'indexWoff2Bytes': index_woff2.stat().st_size,
            'download': f'/fonts/{slug}/{archive.name}',
            'preview': f'/fonts/{slug}/{slug}.png',
            'downloadBytes': archive.stat().st_size,
            'fontFile': source.name,
            'webFontFile': source.with_suffix('.woff2').name,
        },
        'groups': groups,
    }
    target = FACTS / f'{slug}.json'
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(data, ensure_ascii=False, separators=(',', ':')) + '\n')
    print(f'{data["family"]} {data["version"]}: {data["characterCount"]} characters, '
          f'{len(axes)} axes, {woff2.stat().st_size} bytes of WOFF2')


if __name__ == '__main__':
    main()
