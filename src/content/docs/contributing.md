---
title: Contributing to the collection
section: contributing
label: team
order: 510
summary: How drawings, corrections and code enter the collection.
callout: Contributions are drawings and corrections on the grid, graded by a maintainer and merged into a source repository. There is no credit for each family and no submission of finished fonts. This chapter is the checklist for a contributor and for the maintainer who merges.
background: [sources, structure, grades, proposals]
---

## What a contribution is

- New glyphs for an existing style, drawn on the grid.
- Corrections to purple drafts, which move them toward green.
- A new style: a core set of glyphs on the grid, drawn by hand or traced from a specimen that is free to use.
- Script extension: Arabic, Hebrew or another script consistent with an existing style.
- Code: tools and checks, in [fontgarden-tools](https://github.com/fontgarden/fontgarden-tools).

A finished font from outside the system is not a contribution. It cannot be graded, and its structure does not pass the checks.

## Before you open a pull request

1. Every coordinate is even. `make lint` reports no fault.
2. The masters are compatible. The compatibility check of Runebender lists nothing.
3. Every glyph that a model, an agent or the tracer drafted is purple. You do not set green on a contour glyph.
4. `make check-changes`, `make build`, `make qa` and `make test` pass.
5. You ran `make diff` and looked at the rendered glyphs.
6. Drafts and corrections are in separate commits.
7. Your name is in `CONTRIBUTORS.txt`.

## What the maintainer does

1. Builds again and runs the checks at the revision of the pull request.
2. Reviews the proof for faults of shape and spacing that the checks do not find.
3. Grades each glyph in Runebender.
4. Merges. `make status` then gives the new counts.

## A new style

A new style starts from the project template. See [Start a font project](/docs/start/). Its metrics and grid rules are in `sources/design.toml`, and its written design system is in `documentation/design/`. The core set is graded before a model drafts from it. The maintainers decide when a style has enough green glyphs to enter the corpus and when its fonts are released.

## Removal

A contributor can ask for their name to be removed from `CONTRIBUTORS.txt`. Drawings already merged under the OFL stay in the collection, and samples already in a published corpus stay in it. See [Post-authorship and open weights](/docs/culture/).
