---
title: Outline conventions
section: system
label: learn
order: 230
summary: How outlines are constructed so that masters interpolate and the model learns one way of drawing.
callout: Consistency across glyphs and families is what the models learn from. This chapter lists the drawing conventions. The written design system of a family, in its <code>design</code> directory, carries the family-specific detail.
background: [grid, grades]
next: [build]
---

## Order of priorities

1. Curve continuity. Smooth joins stay smooth. Tangents at a smooth point are colinear.
2. Master compatibility. Every master has the same contours, in the same order, with the same number of points, of the same types.
3. Grid membership. New points sit on the 8-grid; the source floor is 2.
4. Popcount. Not a goal. See [The power-of-two grid](/docs/grid/).

When two of these conflict, the higher one wins.

## Contours

- Outer contours run counter-clockwise. Inner contours run clockwise. This is the PostScript convention that UFO sources use.
- Each contour starts at the same logical point in every master. Prefer the lowest-left on-curve point.
- Cubic curves, not quadratic. The compiler converts them.
- No overlapping contours in the final source. Remove overlap at build time, not in the drawing, when a construction needs it for interpolation.
- Extrema have on-curve points.

## Components

Diacritics and repeated parts are components with anchors, not copied contours. Base glyphs carry anchors named by position (`top`, `bottom`, `ogonek`). Mark glyphs carry the matching underscore anchor (`_top`). The build composes accented glyphs from these.

A component is never scaled or rotated in a source master. Draw a separate glyph instead.

## Masters

Families are drawn as two or more masters along a weight axis. The Regular is the reference master. Each glyph in each other master must interpolate with the Regular. Runebender's compatibility check lists the glyphs that do not.

A master in progress is allowed to carry unbolded copies of the Regular, but they must be marked red. See [Glyph grades](/docs/grades/).

## The design directory

Families in the corpus document their system under `design`:

| path | content |
| --- | --- |
| `system/grid.md`, `system/contract.json` | metrics, grid rules, palette |
| `system/weight.md`, `system/spacing.md` | stem values, sidebearing logic |
| `system/interpolation.md` | source topology and master rules |
| `constructions/` | how recurring shapes are built: chamfers, turns, bowls, dots |
| `writing-systems/` | notes per script |
| `glyphs/` | named intent and exceptions for single glyphs |
| `corrections/` | human corrections and rejected examples |
| `reviews/` | current state and evidence |

This directory is read by people and by the tools that prepare model work. Write it in plain language and keep it current.
