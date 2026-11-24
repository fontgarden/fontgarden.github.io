---
title: The dyadic grid
section: system
order: 210
summary: The grid system of each source in the collection, with its units, its levels and its checks.
introduction: "Each source in the collection is on a dyadic grid system: nested grids with units that are powers of two. The em is 1024 units. Structural points are on the 8-unit grid. Optical corrections use the 2-unit grid. The popcount of a measurement is its label. The grids record most of the intent of a drawing, so the sources are labeled training data. This chapter is the specification. The post <a href=\"https://elih.net/blog/virtua-grotesk/\">Virtua Grotesk: Grid Systems for Dataset Engineering</a> gives the reasons."
background: [neuraltype, sources]
next: [structure, grades]
---

## The em

The em is 1024 units, which is 2 to the power of 10. The usual value of 1000 comes from the PostScript coordinate system. It does not meet two requirements of the data procedure.

1. **Exact normalization.** A coordinate divided by the em must be a number that a computer holds exactly. A fraction is exact in binary only when its denominator is a power of two. A stem of 96 units on an em of 1024 is 0.09375, which is exact. On an em of 1000 it is 0.096, which has no finite binary form.
2. **Results that stay on the grid.** A half, a subdivision and an interpolation must give a value on the grid. 1024 has ten halves that are whole numbers. 1000 has three: 500, 250 and 125. Nine sixteenths of the em is 576 on 1024 and 562.5 on 1000. Font coordinates are integers.

## Vertical metrics

These are the reference values, from Virtua Grotesk:

| metric | value | fraction of the em |
| --- | --- | --- |
| cap height and ascender | 768 | 3/4 |
| x-height | 576 | 9/16 |
| descender | -256 | 1/4 |

A new style can have other metrics. Each metric must be a dyadic fraction of the em. The drawing metrics are different from the line metrics and the clipping metrics in `fontinfo.plist`.

## Levels of position

Two grids classify the position of a point.

- **The 2-unit grid is mandatory.** Each coordinate in a source master is even. The tokenizer has one token for each 2-unit position. The conversion from UFO to tokens and from tokens to UFO is exact only because the sources and the codec use this grid. The tools reject odd coordinates and fractions. They do not round them.
- **The 8-unit grid is the default for structure.** New points, handles, advance widths, sidebearings and kerning values are on it. The drafts of a machine are on it. `fgtools report-grid-levels` gives the fraction of points on it for each master, script and mark color.
- **A point on the 2-unit grid that is not on the 8-unit grid records a small optical correction.** A person makes such a point. Do not move it. Do not move a point of an existing drawing by a person to pass a check for new drafts.

Do the grid checks on the masters. Interpolated instances and the quadratic curves of a compiled TrueType font are not on the grid. Their values are not a reason to move a source point.

## Levels of measurement

Each integer is one sum of different powers of two. The number of terms is its popcount. The collection uses the popcount as the label of a handle length, a stem, a counter or a different structural span.

| popcount | example | meaning |
| --- | --- | --- |
| 1 | 64, 128, 256 | one power of two, the default |
| 2 | 96 = 64 + 32 | a sum of two terms |
| 3 | 104 = 64 + 32 + 8 | a smaller adjustment |
| 4 or more | 23 = 16 + 4 + 2 + 1 | a sum of many terms, usually an optical correction |

The popcount is a description and not a limit. For Virtua Grotesk Regular, a stem of 64 units is too light and a stem of 128 is too heavy. Thus the stem is 96 = 64 + 32. Where 96 is too light, the design uses 112 = 64 + 32 + 16. Both values are correct. A high popcount shows a location where the designer made a specific decision, and a model can learn from that label. Runebender shows the terms of each measurement and gives the measurement a color for its popcount. The color identifies the popcount. It does not show an error.

Grid level describes a position. Popcount describes a measurement. Keep the two apart when you review a glyph. Do not round a measurement to get a lower popcount.

## Interpolation

A structural span has a value in each master. The difference between the values of two masters must be a number with exact halves on the grid. The Regular stem of Virtua Grotesk is 96 and the Bold stem is 192. The difference is 96, so the stem at the middle weight is 144, and each quarter step is on the 8-unit grid. Values of 90 and 180 do not have this property. When you set the spans of a new master, select values whose differences are on the grid.

## Spacing

Sidebearings and kerning values use the 8-unit grid by default, because kerning uses multiples of 8. Virtua Grotesk Regular has 131 kerning pairs, and 127 of them are on that grid. The other four use the 2-unit grid for a smaller optical adjustment.

The sidebearing has priority. When a target width does not fit the grid, change the counter or the advance, and not the sidebearing. A counter of 520 = 512 + 8 is correct. A sidebearing of 44 is not.

## Priority

Curve quality has priority over simple grid values. A smooth and continuous curve with a high popcount is correct. A curve with a bend that gives round numbers is a defect. See [Outline structure](/docs/structure/).

## Checks

- `make check-design` compares the glyphs with the 2-unit grid and the stroke targets. It reports the points that are not on the 8-unit grid.
- `fgtools report-grid-levels` counts the points at each grid level, for each script and mark color. It also counts the advances and the kerning values that are not on the 8-unit grid.
- `make check-changes` lists, for each changed purple draft, the new points that are not on the 8-unit grid. A point of the base revision is not new. A new point that is not on that grid needs a reason: a stroke value of the designer, or a derived point.
- `make test` runs the Fontspector check `fontgarden/grid` on the compiled variable font. In each master, the on-curve points and the advance widths must be on the 2-unit grid.
- `CONTEXT.md` holds the grid values and the stroke targets of a style, in `toml` blocks below its rules. The tools read the blocks. People edit them.
