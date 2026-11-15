---
title: The dyadic grid
section: system
label: must
order: 210
summary: The dyadic self-labeling grid system that every source in the collection is drawn on.
callout: "Every source in the collection is drawn on a dyadic self-labeling grid system, nested grids built on powers of two. The em is 1024 units. Structural points sit on the 8-unit grid. Optical corrections drop to the 2-unit subgrid. Measurements are labeled by popcount. The grids record most of the drawing intent automatically, so the sources are labeled training data without extra work. This chapter is the specification. The reasoning is in <a href=\"https://elih.net/blog/virtua-grotesk/\">Virtua Grotesk: Grid Systems for Dataset Engineering</a>."
background: [neuraltype, sources]
next: [structure, grades]
---

## The em

The em is 1024 units, 2 to the tenth power. The industry default of 1000 is PostScript's coordinate system and reads as a percentage of the body, but it fails two requirements of the pipeline.

1. **Normalize exactly.** Dividing a coordinate by the em must give a number the machine holds exactly, and the proportions of the design must land on whole coordinates. A fraction is exact only when its denominator is a power of two. A 96-unit stem over 1024 is 0.09375, exact. Over 1000 it is 0.096, which has no finite binary form.
2. **Close under the operations.** Halving, subdividing and interpolating must land back on the grid. 1024 halves ten times down to 1. 1000 stops after three: 500, 250, 125. Nine sixteenths of the em is 576 on 1024 and 562.5 on 1000, and font coordinates are integers.

## Vertical metrics

The reference values, from Virtua Grotesk:

| metric | value | fraction of the em |
| --- | --- | --- |
| cap height and ascender | 768 | 3/4 |
| x-height | 576 | 9/16 |
| descender | -256 | 1/4 |

A new style may choose other metrics, but each must be a dyadic fraction of the em. Drawing metrics are distinct from the line-box and clipping metrics in `fontinfo.plist`.

## The positional hierarchy

Two grids classify point positions.

- **The 2-unit grid is the law.** Every coordinate in a source master is even. The tokenizer has one token per 2-unit position, and the round trip from UFO to tokens and back is exact only because the sources and the codec share this grid. Odd coordinates and floats are rejected, not rounded.
- **The 8-unit grid is the structural default.** New points, handles, advance widths, sidebearings and kerning values sit on it. Machine drafts land on it. In the human-drawn sources about 85 percent of points are on it.
- **A point on the 2-unit grid but off the 8-unit grid records a fine optical correction.** Such points are made by a person and are protected. Never snap an inherited human drawing to pass a check meant for new drafts.

Check the masters on their own lattice. Interpolated instances and the quadratic curves of a compiled TrueType font do not stay on the lattice, and their values are never a reason to move a source point.

## The measurement hierarchy

Every integer is a unique sum of distinct powers of two. The number of terms is its popcount. The collection uses popcount to label handle lengths, stems, counters and other structural spans.

| popcount | example | meaning |
| --- | --- | --- |
| 1 | 64, 128, 256 | a pure power, the default |
| 2 | 96 = 64 + 32 | a short sum |
| 3 | 104 = 64 + 32 + 8 | a finer adjustment |
| 4 or more | 23 = 16 + 4 + 2 + 1 | a long decomposition, usually an optical correction |

The count is descriptive. A 64-unit stem is too light and 128 too heavy, so the Regular stem of Virtua is 96 = 64 + 32. Where 96 is too light the design uses 112 = 64 + 32 + 16. Both are valid. A high popcount marks a place where the designer made a specific decision, and that mark is teaching signal. Runebender labels each measurement with its decomposition and colors it by popcount. The colors identify the count. They do not indicate errors.

Grid membership describes positions. Popcount describes measurements. Keep the two ideas separate when you review a glyph, and never round a measurement to lower its count.

## Interpolation

Stems and other structural spans in corresponding masters differ by a value that halves cleanly. Virtua's Regular stem is 96 and its Bold stem is 192; the difference of 96 splits evenly, so the half-weight stem is 144 and every quarter lands on the 8-unit grid. Endpoints of 90 and 180 would not close this way. When you set the spans of a new master, choose values whose differences are themselves on the grid.

## Spacing

Sidebearings and kerning default to the 8-unit grid, because kerning is done in multiples of 8. Of Virtua Regular's 84 kerning pairs, all but two sit on it; the two exceptions use the 2-unit grid for a finer optical adjustment. The sidebearing is the hard constraint. When a target width forces the geometry off the grid, change the counter or the advance, not the sidebearing. A counter of 520 = 512 + 8 is correct. A sidebearing of 44 is not.

## Priority

Curve quality comes before grid tidiness. A smooth, continuous curve with an untidy popcount is correct. A curve bent to hit round numbers is a defect. See [Outline structure](/docs/structure/).

## Checking

- `make check-design` checks glyphs against the 2-unit grid and the stroke targets, and reports the points that are off the 8-unit grid.
- `fgtools report-grid-levels` counts the points at each level of the grid, by script and mark color, with the advances and kerning values off the 8-unit grid.
- `make check-changes` lists, for each changed purple draft, the new points that are off the 8-unit grid. A point that the base revision has is not new. A new point off that grid needs a reason: a stroke value of the designer, or a derived point.
- `make qa` runs the Fontspector check `fontgarden/grid` on the compiled variable font: every master has its on-curve points and advance widths on the 2-unit grid.
- `sources/design.toml` holds the grid values and the stroke targets of a style. The tools read it. People edit it.
