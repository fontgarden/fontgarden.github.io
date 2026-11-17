---
title: The fgtools command
section: production
label: learn
order: 305
summary: The shared command of the Font.Garden source tools, and the make targets that call it.
callout: The tools of all Font.Garden fonts are in one Python package, <a href="https://github.com/fontgarden/fgtools">fgtools</a>, with one command, <code>fgtools</code>. A source repository pins the package to a commit and calls it from its Makefile. Change a general tool in the package, not in a font repository.
background: [tools, sources]
next: [build, qa]
---

## How a project is found

A project is a directory that contains `sources/config.yaml`. The command uses the current directory or the nearest parent with that file. The masters are the `<source>` elements of the designspace, or the single UFO that `config.yaml` names.

Most tools only read the UFO sources. Four commands change them, and say so: `fgtools edit`, `fgtools place-anchors --write`, `fgtools build-accented-letters --write` and `fgtools customize`.

## Commands

| command | make target | use |
| --- | --- | --- |
| `fgtools status` | `make status` | Writes `STATUS.md` from the mark colors. |
| `fgtools queue` | `make queue` | Ranks the glyphs that most composites wait on. |
| `fgtools check-design` | `make check-design` | Checks glyphs against the grid and the stroke targets. `--ready` lists the composites that can be green. |
| `fgtools report-grid-levels` | | Counts the points on the 8-unit grid, on the 2-unit grid only, and off both, by script and mark color. |
| `fgtools check-accents` | | Lists the accented letters whose mark is not where the other accented letters predict. |
| `fgtools place-anchors` | | Adds the accent anchors that are missing on the base letters and the marks. Writes only with `--write`. |
| `fgtools build-accented-letters` | | Adds the accented letters of a set as purple composites. Writes only with `--write`. |
| `fgtools render-accent-proofs` | | Draws each accented letter beside the reference fonts and measures it against them. |
| `fgtools evaluate-accent-placement` | | Tests the accent placement methods on compiled fonts. |
| `fgtools check-changes` | `make check-changes` | Compares the sources with a base revision. |
| `fgtools lint-glifs`, `lint-curves` | | Structural faults and curve faults. |
| `fgtools build` | `make build` | Builds the fonts with the gftools builder and fontc. |
| `fgtools diff` | `make diff` | Compares two builds with diffenator3. |
| `fgtools qa` | `make qa`, `make test` | Runs Fontspector with the Font.Garden profile. |
| `fgtools render` | | Draws glyphs large in one picture: the change, the filled glyph, its points, other glyphs of the project and the reference fonts. An agent reads the picture before and after every edit. |
| `fgtools edit` | | Changes a glyph with a calculated operation: an edge moved to a coordinate, the sidebearings, or a mirrored copy of a donor. It marks the glyph purple and refuses a green glyph. |
| `fgtools check-repository` | `make test` | Checks that every tracked file has a place in the layout, that no document names a file or a `make` target that does not exist, and that a `## Contents` chapter lists the chapters of its document. |
| `fgtools proof-web` | `make proof-web` | Serves the font beside the reference fonts in a browser. |
| `fgtools draft-weights` | | Drafts the masters of more weights, for example Thin and Black, from two masters and the stroke targets in `CONTEXT.md`. Writes to `output/weights/`. |
| `fgtools corrections` | | Lists the reviews of purple drafts from the Git history. |
| `fgtools evaluate-drafting` | | Tests a drafting method on held-out green glyphs. |
| `fgtools fetch-reference-fonts` | | Downloads the shared OFL reference fonts from Google Fonts. |
| `fgtools customize` | `make customize` | Renames a project made from the template. |
| `fgtools install-tools` | `make setup` | Installs the pinned fontc and Fontspector binaries. |

`fgtools COMMAND --help` lists the arguments of a command. The full reference is the [README of fgtools](https://github.com/fontgarden/fgtools#commands).

## The pin

`requirements.txt` of a source repository pins fgtools to a commit. To use a newer version, change the commit in `requirements.in` and `requirements.txt`, then run `make setup`.

## A change to a tool

1. Make the change in fgtools, with a test.
2. Run the tests of the package. To run them on a real project too, set `FONTGARDEN_TEST_PROJECT` to its root.
3. Update the pin in each font repository that needs the change.
4. Update the chapter of this guide that describes the command.
