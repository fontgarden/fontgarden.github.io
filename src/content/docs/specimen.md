---
title: From a specimen image to drafts
section: sources
label: learn
order: 107
summary: The intake pipeline that turns a raster specimen into purple drafts in a UFO.
callout: The intake pipeline turns an image of a type specimen into one traced glyph for each glyph of the specimen. Each trace is a purple draft. The result is the start of the design work, not a finished font. The task contract is <code>.agents/tasks/specimen-intake.md</code> in the project template.
background: [start, tools]
next: [grades, proposals]
---

## The pipeline

| step | tool | result |
| --- | --- | --- |
| 1. Segment | `img2glyph process` | one crop for each glyph, and a manifest |
| 2. Label | an agent or a person | `sources/specimen/labels.json`, one Unicode value for each crop |
| 3. Measure | an agent or a person | cap height, x-height, ascender and descender, in pixels |
| 4. Trace and place | `img2ufo`, which uses `img2bez` | purple glyphs in the UFO, on the baseline, with first spacing |
| 5. Build and check | `fgtools lint-glifs`, `make test` | fonts and a QA report |
| 6. Render and compare | a line of text in the built font | a list of placement faults and shape faults |

## Rules of the intake

- Trace only from raster images. Do not copy or convert outlines from a digital font file.
- Do not give the font the name of the original typeface.
- Do not correct the shape of a glyph in this task. A traced glyph is a draft, and the designer grades it.
- Do not push or publish. The origin of the specimen decides whether the font can be published. That decision is the designer's.

## What img2ufo does

- It marks each trace purple, `0.54,0.44,0.88,1`.
- On a later run, it replaces only purple and red glyphs. Graded glyphs stay.
- It snaps points and advance widths to the grid, and sets the em to 1024 units.
- It removes contours from scan dust: a contour with fewer than 3 points, or smaller than 2 percent of the em.
- It sets the vendor ID `FTGD` and the vertical metrics.
- With `--worklist`, it writes the list of glyphs of the Google Fonts Latin Core set that are still missing.

## Image resolution

A glyph of about 500 pixels gives a clean trace. A glyph of about 100 pixels gives an uneven one. Report a low resolution. Do not enlarge the image to hide it.

## Acceptance

- `sources/specimen/` holds the image and `labels.json`, and `documentation/google-fonts.md` states the origin of the specimen.
- Every glyph of the specimen is in the UFO with its Unicode value, and is purple.
- The vertical metrics come from the specimen, snapped to the 8-unit grid.
- `fgtools lint-glifs` reports no structural fault, `make build` succeeds, and `make test` passes.
- `make status` is run.

## Known limits

- Dust that touches the edge of a glyph stays in the trace.
- Some glyphs are placed too high or too low, and the first spacing is loose.
- The pipeline stops at purple drafts. Accented letters have their own task contract. See [Quality assurance](/docs/qa/). Other composites, kerning and the release do not have task contracts yet.
