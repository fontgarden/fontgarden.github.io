#!/usr/bin/env python3
"""Compare the guide with the repositories that it describes.

    python3 scripts/check_guide.py --tools DIR --template DIR --reference DIR

DIR are checkouts of fontgarden-tools, font-project-template and the
reference project (virtua-grotesk). The check fails when:

- a chapter names an `fgtools` command that the tools do not have
- the tools have a command that no chapter names
- a chapter names a `make` target that neither Makefile has
- the template has a `make` target that no chapter names
- a link or a `background`/`next` entry names a chapter that does not exist
"""
import argparse
import re
import sys
from pathlib import Path

GUIDE = Path(__file__).resolve().parent.parent / 'src/content/docs'
# Template targets that the guide does not have to describe.
INTERNAL_TARGETS = {'help', 'venv', 'clean'}
# Only text in code marks is a command.
CODE = r'(?:`|<code>)'


def make_targets(makefile):
    return set(re.findall(r'^([a-z][a-z0-9-]*):', makefile.read_text(), re.M))


def main():
    parser = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    parser.add_argument('--tools', type=Path, required=True)
    parser.add_argument('--template', type=Path, required=True)
    parser.add_argument('--reference', type=Path, required=True)
    args = parser.parse_args()

    cli = (args.tools / 'fontgarden/cli.py').read_text()
    commands = set(re.findall(r"^    '([a-z-]+)': \(", cli, re.M))
    template_targets = make_targets(args.template / 'Makefile')
    targets = template_targets | make_targets(args.reference / 'Makefile')
    if not commands or not template_targets:
        sys.exit('No commands or no make targets found. Check the paths.')

    chapters = {path.stem: path.read_text() for path in sorted(GUIDE.glob('*.md'))}
    faults, named_commands, named_targets = [], set(), set()
    for name, text in chapters.items():
        for command in re.findall(CODE + r'fgtools ([a-z][a-z-]*)', text):
            named_commands.add(command)
            if command not in commands:
                faults.append(f'{name}.md: `fgtools {command}` is not a command of fontgarden-tools')
        # `fgtools lint-glifs`, `lint-curves`: a command named without the prefix.
        named_commands |= set(re.findall(r'`([a-z][a-z-]*)`', text)) & commands
        for target in re.findall(CODE + r'make ([a-z][a-z0-9-]*)', text):
            named_targets.add(target)
            if target not in targets:
                faults.append(f'{name}.md: `make {target}` is not a target of the template or the reference project')
        slugs = re.findall(r'\(/docs/([a-z0-9-]+)/\)', text)
        for line in re.findall(r'^(?:background|next): \[(.*)\]', text, re.M):
            slugs += [slug.strip() for slug in line.split(',') if slug.strip()]
        faults += [f'{name}.md: no chapter `{slug}`' for slug in slugs if slug not in chapters]

    faults += [f'No chapter names the command `fgtools {command}`'
               for command in sorted(commands - named_commands)]
    faults += [f'No chapter names the template target `make {target}`'
               for target in sorted(template_targets - named_targets - INTERNAL_TARGETS)]
    if faults:
        sys.exit('\n'.join(faults))
    print(f'The guide agrees with {len(commands)} commands and {len(template_targets)} template targets.')


if __name__ == '__main__':
    main()
