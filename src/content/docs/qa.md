---
title: Quality assurance
section: production
label: learn
order: 320
summary: The checks and proofs that run on the sources and on every build.
callout: Four kinds of review run on every style. Checks of the sources, checks of the compiled fonts with Fontspector, a comparison of builds with diffenator3, and proofs that a person reads. Automated checks do not see a wrong shape, so a person looks at every proof.
background: [build, grades]
next: [learning, dataset]
---

## Checks of the sources

These commands read the UFO masters. They do not need a build.

| command | use |
| --- | --- |
| `make check-design GLYPHS="n a"` | Compares glyphs with the grid and the stroke targets in `sources/design.toml`. |
| `make check-changes` | Compares the sources with `main`. It fails when a green glyph changed, or when a glyph with changed contours is not purple. |
| `make lint` | Finds structural faults in the GLIF files, differences between the masters and faults of the curves. |
| `make test` | Checks the repository layout and the references in the documents. |

The design checks are a filter. They do not measure quality. On 2026-11-10 they passed 50 of the 72 glyphs that are green in both masters of Virtua Grotesk. Thus a finding is a reason to look, not an error.

## Fontspector

[Fontspector](https://github.com/fonttools/fontspector) runs checks on the compiled fonts. It replaced Fontbakery. The collection uses the Font.Garden profile, which includes the Google Fonts profile and adds four requirements:

| check | requirement |
| --- | --- |
| `fontgarden/unitsperem` | The em is 1024 units. |
| `fontgarden/grid` | Every master of a variable font has its on-curve points and advance widths on the 2-unit grid. |
| `fontgarden/license` | The font has the SIL Open Font License 1.1. |
| `opentype/vendor_id` | The vendor ID is `FTGD`. |

Each repository provides three targets:

- `make qa` works offline. It leaves out the checks in `[qa.exclude]` of `sources/design.toml`. Each exclusion has a reason.
- `make qa-full` runs all checks, with the network checks. A style must pass this before a release.
- `make qa-package PACKAGE=<directory>` checks an assembled google/fonts package.

An exclusion is known development debt. Do not add an exclusion to hide a new failure. Reports go to `out/qa/`. A FAIL gives a failing exit status. A WARN needs review.

The profile is also a Rust plugin for Fontspector: [fontspector-fontgarden](https://github.com/fontgarden/fontspector-fontgarden). It has no release yet.

## Comparison of builds

`make diff` compares the build of the working tree with the build of `main`. See [Build the fonts](/docs/build/). An agent runs it after each source edit and reports each change that the edit does not explain.

## Proofs

`make proof-web` builds the fonts and serves them beside the fonts in `reference-fonts/`, in a browser, at one em size and weight. It has four modes: Compare, Toggle between two builds, Waterfall, and Text. If a reference font does not have a glyph, the proof shows the missing code points. It does not use a fallback font.

The samples are live browser text for Latin, Hebrew and Arabic. `sources/proof-samples.toml` adds samples for a project. Browser rendering is not release QA.

## Connected scripts

Arabic and Hebrew need real shaping for a review. Render test lines with a shaping engine, not with a glyph viewer. Keep a reference renderer built on HarfBuzz and FreeType beside the renderer of the project. Then a fault of the font can be told from a fault of the renderer.

## After a source edit

1. Run `make check-changes` and `make check-design` for the edited glyphs.
2. Run `make build`.
3. Run `make diff`.
4. Look at the rendered glyphs in words, beside the reference fonts.

Command success is not visual review. The designer gives the verdict on drawings.
