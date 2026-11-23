#!/usr/bin/env python3
"""Check the built site in dist/.

    pnpm build
    python3 scripts/check_site.py

The check fails when:

- a link or a file reference in a page names a path that the site does not have
- a link names a part of a page (#name) that the page does not have
- the sitemap names a page that the site does not have
- a font of the index has no facts file, font file, download or link picture
- a page has no title, no description or no canonical link
"""
import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlparse

SITE = Path(__file__).resolve().parent.parent
DIST = SITE / 'dist'
ORIGIN = 'https://font.garden'
REFERENCE = re.compile(r'\s(?:href|src)="([^"]*)"')
IDENTIFIER = re.compile(r'\sid="([^"]*)"')
REQUIRED = {
    'a title': re.compile(r'<title>[^<]+</title>'),
    'a description': re.compile(r'<meta name="description" content="[^"]+"'),
    'a canonical link': re.compile(r'<link rel="canonical" href="[^"]+"'),
}


def resolve(path):
    """Give the file that the server sends for a path of the site."""
    target = DIST / unquote(path).lstrip('/')
    if target.is_dir():
        target = target / 'index.html'
    return target if target.is_file() else None


def main():
    if not DIST.is_dir():
        sys.exit('dist/ does not exist. Run pnpm build first.')
    pages = sorted(DIST.rglob('*.html'))
    identifiers = {page: set(IDENTIFIER.findall(page.read_text())) for page in pages}
    faults = []

    for page in pages:
        name = page.relative_to(DIST)
        text = page.read_text()
        for label, pattern in REQUIRED.items():
            if label == 'a canonical link' and name.name == '404.html':
                continue
            if not pattern.search(text):
                faults.append(f'{name}: the page does not have {label}')
        for reference in sorted(set(REFERENCE.findall(text))):
            url = urlparse(reference.replace('&amp;', '&'))
            if url.scheme in ('http', 'https') and f'{url.scheme}://{url.netloc}' != ORIGIN:
                continue
            if url.scheme not in ('', 'http', 'https'):
                continue
            if url.path and not url.path.startswith('/'):
                faults.append(f'{name}: {reference} is not a path from the site root')
                continue
            target = resolve(url.path) if url.path else page
            if target is None:
                faults.append(f'{name}: {reference} does not exist')
            elif url.fragment and target in identifiers and url.fragment not in identifiers[target]:
                faults.append(f'{name}: {reference} names a part that the page does not have')

    sitemap = DIST / 'sitemap.xml'
    if not sitemap.is_file():
        faults.append('sitemap.xml does not exist')
    else:
        for location in re.findall(r'<loc>([^<]+)</loc>', sitemap.read_text()):
            if resolve(urlparse(location).path) is None:
                faults.append(f'sitemap.xml: {location} does not exist')

    entries = sorted((SITE / 'src/content/fonts').glob('*.yaml'))
    for entry in entries:
        slug = entry.stem
        facts = SITE / 'src/data/fonts' / f'{slug}.json'
        if not facts.is_file():
            faults.append(f'{slug}: no facts file. Run scripts/import_font.py.')
            continue
        files = json.loads(facts.read_text())['files']
        for key in ('woff2', 'download', 'preview'):
            if key not in files or resolve(files[key]) is None:
                faults.append(f'{slug}: the {key} file does not exist')
        if resolve(f'/fonts/{slug}/') is None:
            faults.append(f'{slug}: no specimen page')

    if faults:
        sys.exit('\n'.join(faults))
    print(f'{len(pages)} pages and {len(entries)} fonts have no fault.')


if __name__ == '__main__':
    main()
