---
title: Build the fonts
section: production
label: learn
order: 310
summary: How the compiled fonts are produced from the sources.
callout: Every repository builds the same way. A fresh clone, <code>make setup</code> and <code>make build</code> produce the fonts in <code>fonts/</code>. The compiler is fontc, through the gftools builder.
background: [tools, sources]
next: [qa]
---

## The build

```
make setup
make build
```

`make build` runs `fgtools build`, which does these steps:

1. It removes the previous fonts directory.
2. It copies the sources to a temporary directory. The copy has one glyph order in all masters.
3. It runs the gftools builder on `sources/config.yaml`, with fontc as the compiler.
4. It writes the fonts to `fonts/variable` and `fonts/ttf`.

A project can add its own corrections after this step. Virtua Grotesk has `scripts/build.sh`, which runs `fgtools build` and then `scripts/fix_gf_metadata.py`.

A plain `gftools builder sources/config.yaml`, as the Google Fonts packager runs it, builds the same fonts with fontmake.

## config.yaml

`config.yaml` is the recipe of the gftools builder. A minimal file:

```yaml
sources:
  - Style.designspace
familyName: Style
buildVariable: true
buildStatic: true
buildOTF: false
buildWebfont: false
```

The file must be valid strictyaml. Write instance coordinates in block style, not as `{wght: 400}`.

The recipe describes how to build. The designspace and the UFOs are the only sources of truth for the outlines and the metrics. A project with one master names its UFO in `sources` and sets `buildVariable: false`.

## Features and anchors

OpenType features are in the UFO `features.fea`. A variable font uses one feature file for all masters. An anchor that moves between masters is written with a variable value, for example `(wght=400:360 wght=700:400)`.

Glyphs that the fonts do not export are listed in `public.skipExportGlyphs`, in the lib of each UFO and of the designspace. Do not list a glyph that another glyph uses as a component.

## Compare two builds

`make diff` builds the sources of `main` and of the working tree, and compares the two builds with diffenator3. The HTML reports are in `out/diff/`. The exit status is 1 when a glyph image or a word image differs.

Run it after each source edit. Every changed glyph, word, table or language result must be one that the edit explains.

## What not to do

- Do not edit a compiled font with a table editor and commit it.
- Do not build from instance UFOs that were generated earlier.
- Do not put generated intermediate files in `sources`.
- Do not edit the sources between a build and the review of its output.
