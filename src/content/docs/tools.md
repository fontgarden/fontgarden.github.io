---
title: Setting up a working environment
section: introduction
label: start
order: 40
summary: The editor, the source tools, the compiler and the checkers used on the collection, and how to install them.
callout: The collection is made with a small set of tools. Most are written in Rust and published under Apache-2.0 or MIT. One command, <code>make setup</code>, installs the tools that a source repository needs, at pinned versions. Models run locally.
background: [collection]
next: [start, fgtools, hosting]
---

## Required tools

| tool | purpose | install |
| --- | --- | --- |
| git and a GitHub account | version control and hosting | [git-scm.com](https://git-scm.com) |
| Python 3.13 or later | runs fgtools and gftools | [python.org](https://python.org) |
| fgtools | status, design checks, build, QA, build comparison, web proof, drafting evaluation | `make setup` |
| fontc 2.0.1 | compiles the sources | `make setup` |
| Fontspector 1.9.0 | checks the compiled fonts | `make setup` |
| Runebender | the font editor, also used by the design checks for measurement | [github.com/fontgarden/runebender](https://github.com/fontgarden/runebender) |
| Rust | builds the tracing tools and diffenator3 | [rustup.rs](https://rustup.rs) |

## make setup

In a source repository, `make setup` does three things:

1. It creates the virtual environment `.venv`.
2. It installs the pinned `requirements.txt`. This includes [fontgarden-tools](https://github.com/fontgarden/fontgarden-tools), pinned to a commit, and gftools.
3. It runs `fgtools install-tools`. This installs the fontc and Fontspector release binaries into `.venv/bin`, after a check of their SHA-256 checksums.

Do not install the tools globally. `requirements.in` lists the direct dependencies. See [The fgtools command](/docs/fgtools/).

## Runebender

Runebender is the editor used on the collection. It reads and writes UFO and designspace sources directly. It is part of the [Linebender](https://linebender.org) project.

Runebender shows the mark color of each glyph, which this system uses as a grade. It labels each measurement with its decomposition into powers of two. See [Glyph grades](/docs/grades/) and [The dyadic grid](/docs/grid/).

`make runebender` opens the sources of a project in the Runebender web editor. Edits to the source files load again in the browser.

`fgtools check-design` uses the Runebender binary for measurement. If the binary is not on `PATH`, set `RUNEBENDER` to its path.

Coding agents connect to the editor through MCP. An agent can read, measure, proof and propose. See [Proposals and grading](/docs/proposals/).

## Tools for a specimen image

These three tools turn a specimen image into purple drafts. See [From a specimen image to drafts](/docs/specimen/).

```
cargo install --git https://github.com/fontgarden/img2glyph
cargo install --git https://github.com/fontgarden/img2bez img2bez
cargo install --git https://github.com/fontgarden/img2ufo
```

- `img2glyph` divides a specimen image into one crop for each glyph.
- `img2bez` traces a raster into cubic outlines on the grid.
- `img2ufo` traces the labeled crops and writes them into a UFO, with placement, spacing and metrics.

## Reference fonts

One shared collection of OFL fonts serves every comparison and measurement: the accent placement evaluation, proofs and checks. It is not a source of outlines.

```
export FONTGARDEN_REFERENCE_FONTS=~/GH/fontgarden/reference-fonts
fgtools fetch-reference-fonts
```

The command downloads the trusted families from [google/fonts](https://github.com/google/fonts). Each family goes to its own folder with its `OFL.txt`. The list is `fontgarden/reference_fonts.toml` in fontgarden-tools, with the reason for each family. The designer decides which families it holds. The first list has 9: Source Sans 3, Source Serif 4, IBM Plex Sans, Inter, Roboto, Noto Sans, Fira Sans, Work Sans and EB Garamond. Commands that take reference fonts use the collection by default.

### Reference fonts of a project

Each font has its own references. A project names them in `sources/design.toml`, each with the reason that it is a reference:

```
[reference_fonts.families]
heebo = "A Hebrew extension of Roboto: a plain sans for text."
notosanshebrew = "A Hebrew sans with full coverage of the marks."
```

A key is a directory name of google/fonts under `ofl/`, so the upstream of a family is `https://github.com/google/fonts/tree/main/ofl/<name>`. `make reference-fonts` copies the upright fonts and the `OFL.txt` of each family into `reference-fonts/<name>/` of the project. Git ignores that folder. A family comes from the first place that has it:

1. the shared collection of `FONTGARDEN_REFERENCE_FONTS`;
2. a local clone of google/fonts that `FONTGARDEN_GOOGLE_FONTS` names;
3. a download from GitHub.

`make proof-web` and the proof view of Runebender read `reference-fonts/`. Runebender shows the families that cover the glyph, so a Hebrew glyph is shown beside the Hebrew references.

## Optional tools

- `diffenator3`, for `make diff`, which compares two builds.
- `designbot`, the Rust graphics library used for specimens and proof sheets.
- `font-ml`, which runs the task models locally.

## Fontbakery and fontmake

Earlier Google Fonts documentation refers to Fontbakery. Fontspector replaced it. Do not add Fontbakery to a repository.

The fonts are built with fontc, the Rust compiler of Google Fonts that replaces fontmake. `fgtools build --compiler fontmake` builds with fontmake, and `fgtools diff --fontmake` compares the two compilers.
