---
title: Setting up a working environment
section: introduction
label: start
order: 30
summary: The editor, build tools and checkers used on Font Garden projects, and how to install them.
callout: Font Garden projects use a small set of tools. Most are standard in open font production. One, the Runebender web editor, is specific to this system. Install them in the order given below.
background: [culture]
next: [hosting, upstream]
---

## Required tools

| tool | purpose | install |
| --- | --- | --- |
| git and a GitHub account | version control and hosting | [git-scm.com](https://git-scm.com) |
| Python 3.11 or later | runs the build and check scripts | [python.org](https://python.org) |
| gftools and fontmake | compile UFO and designspace sources to TTF | `pip install -r requirements.txt` in a project |
| fontspector | runs the font checks | [fontspector](https://github.com/fonttools/fontspector), a Rust binary |
| Runebender | the font editor | see below |

Each project repository carries a `requirements.txt` that pins the Python tools. Create a virtual environment in the project and install from that file. Do not install the tools globally.

```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Runebender

Runebender is the editor used on all Font Garden families. It reads and writes UFO and designspace files directly. It is part of the [Linebender](https://linebender.org) project.

The web editor runs from a local workspace server. Start it with the path of a designspace or UFO:

```
runebender-serve sources/Family.designspace --open
```

The editor opens in your browser at `localhost:8765`. Edits you make in the browser save back to the source files on disk when you press Cmd+S. Edits that other tools make on disk reload in the browser.

Runebender shows the per-glyph mark color that this system uses as a grade. See [Glyph grades](/docs/grades/).

## Optional tools

- `fontc`, the Rust compiler from Google Fonts. Projects provide a `build-fontc.sh` as an alternative to the Python build.
- `diffenator3` and its `diff3proof` renderer, for browser proofs and comparisons between builds.
- `designbot`, the Font Garden proof generator. `designbot proof <font.ttf>` writes a multi-page PDF proof from a compiled font.

## Fontbakery

Earlier Google Fonts documentation refers to Fontbakery. Font Garden projects use fontspector, which replaced it. Do not add Fontbakery to a project.
