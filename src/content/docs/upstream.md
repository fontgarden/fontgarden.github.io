---
title: Source repository structure
section: sources
label: must
order: 110
summary: The required directory layout of a Font Garden font project.
callout: Every family in the catalog follows one repository layout. The layout lets the build, the checks and the corpus tools find the sources without per-project configuration. The reference example is the <a href="https://github.com/eliheuer/virtua-grotesk">Virtua Grotesk</a> repository.
background: [hosting, tools]
next: [readmefile, license-file, grid]
---

## The essentials

```
├── AUTHORS.txt
├── CONTRIBUTORS.txt
├── OFL.txt
├── README.md
├── Makefile
├── build.sh
├── requirements.txt
├── documentation
│   ├── README.md
│   └── proofs
├── fonts
│   ├── ttf
│   └── variable
└── sources
    ├── Family.designspace
    ├── Family-Regular.ufo
    ├── Family-Bold.ufo
    └── config.yaml
```

## sources

The `sources` directory holds the canonical UFO masters and one designspace file. Build systems read the designspace and the UFO masters directly. Nothing else in the repository is a source of truth for the outlines.

- One UFO per master. Names follow the pattern `Family-Style.ufo`.
- One designspace file that lists the masters, the axes and the named instances.
- `config.yaml` is a build recipe for gftools. It describes how to build and is not a replacement for the designspace.
- Old or superseded material goes in `sources/archive`. The build ignores it.

Generated intermediate files, such as instance UFOs, must be written outside the source tree.

## fonts

Compiled fonts. `fonts/variable` holds the variable font. `fonts/ttf` holds the static instances. These directories are rebuilt from scratch by the build and are never edited by hand.

## documentation

Human-readable material about the family: proofs, design notes, grade reports and the images used in the README. A `documentation/README.md` lists what is there.

## Top-level files

- `README.md`: see [README file](/docs/readmefile/).
- `OFL.txt`, `AUTHORS.txt`, `CONTRIBUTORS.txt`: see [License files](/docs/license-file/).
- `Makefile`: the entry point for every workflow. `make help` lists the targets. At minimum a project provides `build`, `qa` and `proof`.
- `build.sh` and `requirements.txt`: the reproducible build. See [Build the fonts](/docs/build/).

## Design documentation

Families that are part of the training corpus also carry a `design` directory with the written design system of the family: grid and metrics, weight and spacing, construction of recurring shapes, per-script notes, and a record of human corrections. This material is read by people and by the model tooling. Its structure is described in [Outline conventions](/docs/outlines/).
