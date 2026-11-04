---
title: Quality assurance
section: production
label: learn
order: 320
summary: The checks and proofs that run on every build.
callout: Three kinds of review run on every family. Automated checks with fontspector, printed and browser proofs, and the grid and grade reports. The first two are standard in open font production. The third is specific to this system.
background: [build, grades]
next: [dataset, publishing]
---

## fontspector

[fontspector](https://github.com/fonttools/fontspector) runs profile-based checks on compiled fonts. It replaced Fontbakery. Each project provides two targets:

- `make qa` runs the development profile. It carries a documented list of excluded checks, for problems that are known and accepted while a family is in progress. The exclusions are listed in `documentation/qa.md`.
- `make qa-full` runs the complete profile with no exclusions. A family must pass this before it enters the catalog.

Read failures in full. A check that fails on every glyph usually points at one source problem, not many.

## Proofs

`make proof` builds the fonts and writes a PDF proof to `documentation/proofs/proof.pdf` with `designbot proof`. The proof introspects the font: axes, instances, character set, metrics and features. It needs no per-project configuration.

`make review` writes a browser proof with `diff3proof` to `out/review`. Use it to compare two builds or to inspect shaping of connected scripts.

Proofs are committed to `documentation/proofs` when a release is tagged, so that a reviewer can see what was shipped without building.

## Grid and grade reports

- `make lint-grid` checks source coordinates against the grid rules in [The power-of-two grid](/docs/grid/).
- `make grid-qa` writes a per-glyph report with the grade, the grid conformance and the popcounts.
- `make scoreboard` updates the color inventory in `documentation/scoreboard.md`.

These reports are inputs to the corpus. A glyph that fails them is excluded from training regardless of its color.

## Connected scripts

Arabic and Hebrew need real shaping to review. Render test lines with a shaping engine, not with a glyph viewer. Projects with these scripts provide a target such as `make qa-hebrew` that renders a fixed text in each weight and checks mark attachment.

## Local review

Before you open a pull request, run in this order: `make build`, `make qa`, `make proof`. Look at the proof. Automated checks do not see a wrong shape.
