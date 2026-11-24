---
title: Contributions
section: contributing
order: 510
summary: The procedure for a contribution of drawings, corrections or code.
introduction: "A contribution is a set of drawings or corrections on the grid. A maintainer grades it and merges it into a source repository. A family has no credit line, and the collection does not accept completed fonts. This chapter is the checklist for the contributor and for the maintainer."
background: [sources, structure, grades, proposals]
---

## Types of contribution

- New glyphs for an existing style, drawn on the grid.
- Corrections to purple drafts, which move them toward green.
- A new style: a core set of glyphs on the grid, drawn by hand or traced from a specimen that is free to use.
- Script extension: Arabic, Hebrew or another script consistent with an existing style.
- Code: tools and checks, in [fgtools](https://github.com/fontgarden/fgtools).

A completed font from a different system is not a contribution. The designer cannot grade its glyphs, and its structure does not pass the checks.

## Checklist before a pull request

1. Every coordinate is even. `fgtools lint-glifs` reports no fault.
2. The masters are compatible. The compatibility check of Runebender lists nothing.
3. Every glyph that a model, an agent or the tracer drafted is purple. You do not set green on a contour glyph.
4. `make check-changes` and `make test` pass.
5. You ran `make diff` and looked at the rendered glyphs.
6. Drafts and corrections are in separate commits.
7. Your name is in `CONTRIBUTORS.txt`.

## Steps of the maintainer

1. Builds again and runs the checks at the revision of the pull request.
2. Reviews the proof for faults of shape and spacing that the checks do not find.
3. Grades each glyph in Runebender.
4. Merges. `make status` then gives the new counts.

## A new style

A new style starts from the project template. See [New font project](/docs/start/). Its design rules, with the grid and the stroke targets, are in `CONTEXT.md`. The core set is graded before a model drafts from it. The maintainers decide when a style has enough green glyphs to enter the corpus and when its fonts are released.

## Removal

A contributor can ask the maintainers to remove a name from `CONTRIBUTORS.txt`. Merged drawings keep the OFL and stay in the collection. Samples in a published corpus stay in that corpus. See [Post-authorship and open weights](/docs/culture/).
