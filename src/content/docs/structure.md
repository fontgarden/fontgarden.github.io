---
title: Outline structure
section: system
label: must
order: 220
summary: The point structure rules that make an outline usable as a source and as training data.
callout: "A font source's structure, not only its silhouette, is what makes it usable. An outline is like a low-polygon mesh: a small number of points at the places that matter, with handles locked to the axes. These rules apply to every contour in the collection, whether a person or a model drew it. They are stricter than common practice because the corpus builder rejects what they forbid."
background: [grid]
next: [grades, proposals]
---

## Order of priorities

1. Curve continuity. Smooth joins stay smooth. Tangents at a smooth point are colinear.
2. Master compatibility. Every master has the same contours, in the same order, with the same points of the same types.
3. Grid membership. Every coordinate is even. New points sit on the 8-unit grid.
4. Popcount. Not a goal. See [The dyadic grid](/docs/grid/).

When two of these conflict, the higher one wins.

## Points

- Points go at structural features only: extrema, corners and inflections. Nothing else.
- Every extremum has an on-curve point.
- Handles are on-axis. A handle within 6 units of horizontal or vertical is made exactly horizontal or vertical. Off-axis handles are allowed only where the curve has no axis-aligned tangent, and are counted by the structure checks.
- Point economy. The compiled IBM Plex Arabic `beh` has 95 points; its source has about 20. The source count is the target.
- Cubic curves only. The compiler converts them.
- No duplicated closing points.

## Contours

- Contours are closed. An open contour is a drawing error, not a feature.
- Winding is set so that counters cut holes: outer contours counter-clockwise, inner contours clockwise, the PostScript convention that UFO sources use.
- Each contour starts at the same logical point in every master. Prefer the lowest-left on-curve point.
- No overlapping contours in a graded glyph. Overlap is removed in the source, not at build time. The corpus builder decomposes composites and removes overlap, and a glyph that changes under that operation is flagged.
- Chamfers and corner cuts are constructed on the grid, not fitted. Virtua's chamfers are 16 units.

## Components and anchors

- Diacritics and repeated parts are components with anchors, not copied contours. Base glyphs carry anchors named by position (`top`, `bottom`). Mark glyphs carry the matching underscore anchor (`_top`).
- A component is never scaled or rotated in a source master. Draw a separate glyph instead.
- Anchors on large glyph sets are computed by a script at build time from the outline, not placed by hand. Placing anchors on hundreds of glyphs by hand is a week of work, and every outline revision breaks it.
- Combining marks are not letterforms. The corpus builder drops them. They still follow every rule above.

## Masters

- Styles are drawn as two or more masters along a weight axis. The Regular master is the base. Each glyph in every other master is point-compatible with the base.
- A model draft of a heavier master moves the base's points. It never changes the point structure, so the masters still interpolate.
- Deltas between masters sit on the 8-unit grid where the design allows. Virtua's machine lattice for Bold drafts is stems of plus 48 per side and bars of plus 72.
- A master in progress may carry unbolded copies of the base, but they must be marked red. See [Glyph grades](/docs/grades/).

## Sources, never compiled

The corpus reads UFO masters at a named revision. It never reads a compiled font. Compiled outlines carry point bloat and conversion artifacts, and training on them teaches a model to draw dense, compiled-looking outlines, the opposite of the goal.

## Naming

Glyph names follow the Google Fonts and Glyphs convention with script suffixes (`-ar`, `-hb`) and positional suffixes (`.init`, `.medi`, `.fina`). Unicode values are set in the UFO for every encoded glyph.

## Checking

Runebender's compatibility check lists the glyphs that do not interpolate and says why. `img2bez structure-compare` renders a font, traces it back and compares the structure: point counts, lines against curves, on-axis handles, ranked worst first. The automated checks in [Quality assurance](/docs/qa/) cover the rest.
