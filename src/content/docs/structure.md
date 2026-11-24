---
title: Outline structure
section: system
order: 220
summary: The rules for points, contours, components and masters that each outline in the collection obeys.
introduction: "The shape of an outline is not sufficient for a source. The point structure must also be correct. An outline has a small number of points, at the structural features of the shape, with handles on the axes. These rules apply to each contour in the collection, from a person or from a model. They are stricter than usual practice, because the corpus builder rejects each outline that breaks them."
background: [grid]
next: [grades, proposals]
---

## Sequence of priorities

1. Curve continuity. A smooth join stays smooth. The tangents at a smooth point are collinear.
2. Master compatibility. Each master has the same contours, in the same sequence, with the same points of the same types.
3. Grid level. Each coordinate is even. New points are on the 8-unit grid.
4. Popcount. A low popcount is not a goal. See [The dyadic grid](/docs/grid/).

When two of these rules conflict, the rule with the lower number has priority.

## Points

- Put points only at structural features: extrema, corners and inflections.
- Each extremum has an on-curve point.
- Handles are on an axis. Make a handle exactly horizontal or vertical when its angle is less than 6 units from that axis. An off-axis handle is permitted only where the curve has no tangent on an axis. The structure checks count the off-axis handles.
- Use few points. The compiled `beh` of IBM Plex Arabic has 95 points, and its source has approximately 20. The number of the source is the target.
- Use only cubic curves. The compiler converts them.
- Do not put a second point at the position where a contour closes.

## Contours

- Each contour is closed. An open contour is a drawing error.
- Outer contours are counter-clockwise and inner contours are clockwise. This is the PostScript convention of UFO sources, and it makes each counter a hole.
- Each contour starts at the same point in each master. Use the lowest on-curve point at the left, if possible.
- A graded glyph has no overlap of contours. Remove the overlap in the source and not in the build. The corpus builder decomposes composites and removes overlap. It reports a glyph that this operation changes.
- Construct chamfers and corner cuts on the grid. Do not fit them to a curve. The chamfers of Virtua Grotesk are 16 units.

## Components and anchors

- A diacritic or a repeated part is a component with an anchor. It is not a copy of contours. A base glyph has anchors with the name of a position (`top`, `bottom`). A mark glyph has the related anchor with an underscore (`_top`).
- Do not scale or rotate a component in a source master. Draw a different glyph.
- For a large glyph set, a script calculates the anchors from the outlines during the build. Manual anchors on hundreds of glyphs take approximately one week, and each revision of an outline makes them incorrect.
- Combining marks are not letterforms. The corpus builder removes them. They still obey each rule of this chapter.

## Masters

- A style has two or more masters on a weight axis. The Regular master is the base. Each glyph in each other master is point-compatible with the base.
- A model draft of a heavier master moves the points of the base. It does not change the point structure, so the masters still interpolate.
- The deltas between masters are on the 8-unit grid where the design permits. For the Bold drafts of a machine, Virtua Grotesk adds 48 units to each side of a stem and 72 units to a bar.
- An incomplete master can hold copies of the base outlines. Each copy must be red. See [Glyph grades](/docs/grades/).

## Sources and compiled fonts

The corpus builder reads UFO masters at a named revision. It does not read a compiled font. Compiled outlines have more points than their sources, and they contain conversion artifacts. A model that trains on them learns to draw outlines with too many points.

## Names

Glyph names follow the convention of Google Fonts and Glyphs. A script has a suffix (`-ar`, `-hb`), and a position has a suffix (`.init`, `.medi`, `.fina`). Each encoded glyph has its Unicode value in the UFO.

## Checks

The compatibility check of Runebender lists the glyphs that do not interpolate, with the reason for each. `img2bez structure-compare` renders a font, traces the result and compares the structure: point counts, lines and curves, and on-axis handles. Its list starts with the largest difference. The automatic checks of [Quality assurance](/docs/qa/) do the other checks.
