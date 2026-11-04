---
title: The power-of-two grid
section: system
label: must
order: 210
summary: The unit system that makes Font Garden sources readable as training data.
callout: Families in the Font Garden catalog are drawn on a power-of-two grid. The em is 1024 units. New geometry sits on multiples of 8. The source floor is 2. This chapter gives the rules and the reason for them. The machine-readable version of the rules for a family lives in its <code>design/system/contract.json</code>.
background: [neuraltype, upstream]
next: [grades, outlines]
---

## Metrics

The reference values, from Virtua Grotesk:

| metric | value |
| --- | --- |
| em (unitsPerEm) | 1024 |
| cap height and ascender | 768 |
| x-height | 576 |
| descender | -256 |

A new family may choose other vertical metrics, but each must be a sum of few powers of two, and the em must be 1024. Drawing metrics are distinct from the line-box and clipping metrics in `fontinfo.plist`.

## Grid levels

- **8 units.** New machine-drawn geometry, handles, advance widths and sidebearings sit on the 8-unit grid. Kerning values are multiples of 8.
- **2 units.** The source floor. No coordinate in a source master is odd.
- **Off-grid human corrections.** A human may place a point off the 8-grid to make an optical correction. Such points are protected. Never snap an inherited human drawing to pass a check meant for new drafts.

Check source masters on their own lattice. Interpolated instances and the quadratic curves of a compiled TrueType font do not stay on the lattice, and their values are never a reason to move a source point.

## Why powers of two

A coordinate on this grid is a short sum of powers of two. The number of terms in that sum, its popcount, tells a model something about the point without any extra label:

- A coordinate such as 512 (one term) or 520 = 512 + 8 (two terms) is default grid geometry.
- A coordinate such as 98 = 64 + 32 + 2 (three terms) marks a place where the designer made an optical correction, for example the compensation on the round side of an `o`.

The grid is therefore self-labeling. The default structure and the deliberate departures from it are both visible in the numbers. A model trained on many such sources learns where optical corrections happen and how large they are. This is the central idea of the system: the catalog is the dataset, and the grid is what makes the dataset legible.

Two consequences follow:

1. High popcount is not a fault. Do not round a measurement to lower its count.
2. Grid membership describes positions. Popcount describes measurements. Keep the two ideas separate when you review a glyph.

## Sidebearings and counters

Sidebearings are the hard constraint. They stay on the 8-grid because kerning is in multiples of 8. When a target width forces the geometry off the grid, change the counter or the advance, not the sidebearing.

Worked example from the capital O of Virtua Grotesk. A counter of 512 and a side of 108 give a width of 728. Half of 728 is 364, which is not a multiple of 8, so the glyph cannot have both sidebearings on the 8-grid and a centered counter. The wrong fix is a sidebearing of 44. The right fix is a sidebearing of 48 and a counter of 520, which gives a width of 736 and a center at 416. The side of 108 is the stroke weight and stays as it is.

## Priority

Curve quality comes before grid tidiness. A smooth, continuous curve with an untidy popcount is correct. A curve bent to hit round numbers is a defect. See [Outline conventions](/docs/outlines/).

## Checking

Each project provides `make lint-grid`, which checks the source outlines against the grid rules, and `make grid-qa`, which writes a per-glyph report with grades and popcounts.
