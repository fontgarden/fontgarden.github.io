---
title: The fgtools command
section: production
label: learn
order: 305
summary: The shared command of the Font.Garden source tools, and the make targets that call it.
callout: The tools of all Font.Garden fonts are in one Python package, <a href="https://github.com/fontgarden/fontgarden-tools">fontgarden-tools</a>, with one command, <code>fgtools</code>. A source repository pins the package to a commit and calls it from its Makefile. Change a general tool in the package, not in a font repository.
background: [tools, sources]
next: [build, qa]
---

## How a project is found

A project is a directory that contains `sources/config.yaml`. The command uses the current directory or the nearest parent with that file. The masters are the `<source>` elements of the designspace, or the single UFO that `config.yaml` names.

The tools do not change the UFO sources, with one exception: `fgtools customize` renames a new project.

## Commands

| command | make target | use |
| --- | --- | --- |
| `fgtools status` | `make status` | Writes `STATUS.md` from the mark colors. |
| `fgtools queue` | `make queue` | Ranks the glyphs that most composites wait on. |
| `fgtools check-design` | `make check-design` | Checks glyphs against the grid and the stroke targets. `--ready` lists the composites that can be green. |
| `fgtools check-accents` | `make check-accents` | Lists the accented letters whose mark is not where the other accented letters predict. |
| `fgtools evaluate-accent-placement` | | Tests the accent placement methods on compiled fonts. |
| `fgtools check-changes` | `make check-changes` | Compares the sources with a base revision. |
| `fgtools lint-glifs`, `lint-curves` | `make lint` | Structural faults and curve faults. |
| `fgtools build` | `make build` | Builds the fonts with the gftools builder and fontc. |
| `fgtools diff` | `make diff` | Compares two builds with diffenator3. |
| `fgtools qa` | `make qa`, `make qa-full`, `make qa-package` | Runs Fontspector with the Font.Garden profile. |
| `fgtools proof-web` | `make proof-web` | Serves the font beside the reference fonts in a browser. |
| `fgtools corrections` | `make corrections` | Lists the reviews of purple drafts from the Git history. |
| `fgtools evaluate-drafting` | | Tests a drafting method on held-out green glyphs. |
| `fgtools customize` | `make customize` | Renames a project made from the template. |
| `fgtools install-tools` | `make setup` | Installs the pinned fontc and Fontspector binaries. |

`fgtools COMMAND --help` lists the arguments of a command. The full reference is the [README of fontgarden-tools](https://github.com/fontgarden/fontgarden-tools#commands).

## The pin

`requirements.txt` of a source repository pins fontgarden-tools to a commit. To use a newer version, change the commit in `requirements.in` and `requirements.txt`, then run `make setup`.

## A change to a tool

1. Make the change in fontgarden-tools, with a test.
2. Run the tests of the package. To run them on a real project too, set `FONTGARDEN_TEST_PROJECT` to its root.
3. Update the pin in each font repository that needs the change.
4. Update the chapter of this guide that describes the command.
