---
title: The catalog is the dataset
section: data
label: nerd
order: 410
summary: How graded, on-grid sources become a training corpus, and how models are released.
callout: Font Garden does not scrape fonts. The catalog families, drawn on the grid and graded per glyph, are the training data. This chapter describes how a source becomes a corpus and what the released models are. The training code and the corpus tools are not public.
background: [grid, grades, culture]
next: [publishing]
---

## Why generated data

Models trained on found fonts learn the habits of hundreds of designers: different point structures, curve conventions, contour directions and unit systems. Capacity goes into coping with that noise, and outputs inherit it.

The alternative is to fix the representation first and then produce data for it. On the power-of-two grid, an outline is a short sequence over a small vocabulary. Every sample carries its own labels: the grade, the master, the position on the weight axis, and the popcount pattern that marks optical corrections. Validity is checkable by machine. Outputs are edit-ready UFO outlines by construction.

## From source to corpus

1. The corpus builder reads a family's designspace and UFO masters from its repository at a tagged revision.
2. Each glyph is filtered by grade. Green is always included. Yellow is included by a per-experiment decision that is logged. Orange and red are never included.
3. Glyphs that fail `lint-grid` are excluded.
4. Masters are amplified by grid-snapped interpolation along the designspace axes, and by pairing weights for the bolding task.
5. The result is tokenized. The reference tokenizer round-trips every outline exactly.

The provenance of every sample is recorded: repository, revision, glyph name, master and grade.

## Tasks

In order of value against difficulty:

1. Glyph completion from a partial outline.
2. Weight extension: drafting a Bold from a Regular.
3. Diacritic and script extension.
4. Style-conditioned generation.

## Baselines

Every model result is compared with a plain baseline on the same held-out glyphs. For weight extension the baseline is the mean per-point delta between masters. A model ships only if it beats the baseline. This rule caught the unbolded-copy defect described in [Glyph grades](/docs/grades/), which a loss curve alone did not show.

## Released models

| model | task | weights | license |
| --- | --- | --- | --- |
| Virtua-12M-v0.1 | completion and weight extension on the Virtua grid | float32, Hugging Face `fontgarden/virtua` | Apache-2.0 |

Weights ship as float32 so that others can continue training. The model card records the baseline and the model score.

## Known limits

- A model trained on few families draws in those families' style. More seed families on the grid is the fix, and the reason the catalog grows.
- Optical corrections live in small offsets. A grid that is too coarse removes them. The 8-unit grid with a 2-unit floor is the current compromise.
