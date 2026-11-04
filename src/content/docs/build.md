---
title: Build the fonts
section: production
label: learn
order: 310
summary: How the compiled fonts are produced from the sources.
callout: Every project builds the same way. A fresh clone, a virtual environment, and <code>make build</code> must produce the fonts in <code>fonts/</code>. If a build needs any other step, the project is not ready.
background: [tools, upstream]
next: [qa]
---

## The build

```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
make build
```

`make build` runs `build.sh`, which:

1. Removes the previous `fonts/` output and intermediate files.
2. Runs the gftools builder on `sources/config.yaml`. The builder calls fontmake to compile the designspace into a variable font and the named instances into static TTFs.
3. Runs any project fix-up scripts on the compiled fonts, for example to set name table entries.
4. Lists the files written to `fonts/variable` and `fonts/ttf`.

## config.yaml

The gftools builder recipe. A minimal file:

```yaml
sources:
  - Family.designspace
familyName: Family
buildVariable: true
buildStatic: true
buildOTF: false
buildWebfont: false
```

The recipe describes how to build. The designspace and the UFOs remain the only sources of truth for the outlines and metrics.

## Alternative compiler

Projects also provide `make build-fontc`, which runs the same sources through `fontc`, the Rust compiler. Use it to confirm that the sources do not depend on fontmake-specific behavior. The catalog ships the fontmake build until the two produce equivalent output.

## Snapshots

`build.sh` records a snapshot of the source state it built from. This lets a proof or a report be matched to the exact source revision. Do not edit sources between a build and the review of its output.

## What not to do

- Do not edit a compiled font with a table editor and commit it.
- Do not build from instance UFOs that were generated earlier.
- Do not put generated intermediate files inside `sources`.
