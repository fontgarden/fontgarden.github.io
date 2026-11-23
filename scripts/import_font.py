#!/usr/bin/env python3
"""Import the variable font of a font project into the font index.

    python3 scripts/import_font.py --project DIR --slug NAME

DIR is a checkout of a Font.Garden font project. The script reads the one
variable font in DIR/fonts/variable and DIR/OFL.txt. It writes:

- public/fonts/NAME/NAME.woff2   the font that the pages load
- public/fonts/NAME/NAME.zip     the download: the TTF and OFL.txt
- src/data/fonts/NAME.json       the facts that the specimen page shows

The script needs fontTools and brotli. The Python of a font project has
both: DIR/.venv/bin/python.
"""
import argparse
import json
import subprocess
import sys
import unicodedata
import zipfile
from pathlib import Path

from fontTools import unicodedata as ftunicodedata
from fontTools.ttLib import TTFont

SITE = Path(__file__).resolve().parent.parent
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


def revision(project):
    result = subprocess.run(
        ['git', '-C', str(project), 'log', '-1', '--format=%h %cs'],
        capture_output=True, text=True, check=False,
    )
    parts = result.stdout.split()
    return {'commit': parts[0], 'date': parts[1]} if len(parts) == 2 else None


def main():
    parser = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    parser.add_argument('--project', type=Path, required=True)
    parser.add_argument('--slug', required=True)
    args = parser.parse_args()

    candidates = sorted((args.project / 'fonts/variable').glob('*.ttf'))
    if len(candidates) != 1:
        sys.exit(f'{args.project}/fonts/variable must hold one TTF, found {len(candidates)}')
    source = candidates[0]
    license_file = args.project / 'OFL.txt'
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

    public = SITE / 'public/fonts' / args.slug
    public.mkdir(parents=True, exist_ok=True)
    woff2 = public / f'{args.slug}.woff2'
    font.flavor = 'woff2'
    font.save(woff2)

    archive = public / f'{args.slug}.zip'
    with zipfile.ZipFile(archive, 'w', zipfile.ZIP_DEFLATED) as bundle:
        bundle.write(source, source.name)
        bundle.write(license_file, 'OFL.txt')

    data = {
        'family': names.getDebugName(16) or names.getDebugName(1),
        'version': names.getDebugName(5).split(';')[0].replace('Version ', ''),
        'copyright': license_file.read_text().splitlines()[0].strip(),
        'license': 'SIL Open Font License 1.1',
        'licenseUrl': 'https://openfontlicense.org',
        'revision': revision(args.project),
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
        'files': {
            'woff2': f'/fonts/{args.slug}/{woff2.name}',
            'woff2Bytes': woff2.stat().st_size,
            'download': f'/fonts/{args.slug}/{archive.name}',
            'downloadBytes': archive.stat().st_size,
            'fontFile': source.name,
        },
        'groups': groups,
    }
    target = SITE / 'src/data/fonts' / f'{args.slug}.json'
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(data, ensure_ascii=False, separators=(',', ':')) + '\n')
    print(f'{data["family"]} {data["version"]}: {data["characterCount"]} characters, '
          f'{len(axes)} axes, {woff2.stat().st_size} bytes of WOFF2')


if __name__ == '__main__':
    main()
