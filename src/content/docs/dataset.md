---
title: The collection is the dataset
section: data
label: nerd
order: 410
summary: How graded, on-grid sources become a training corpus.
callout: Font Garden does not collect fonts. The collection's own masters, drawn on the grid and graded per glyph, are the training data. The dataset is engineered, not collected. This chapter describes how a source becomes a corpus. The training code and the corpus tools are private; the corpus manifest and the evaluation numbers are public.
background: [grid, grades, culture]
next: [models]
---

## Why engineered data

Models trained on found fonts learn the habits of hundreds of designers: different point structures, curve conventions, winding and unit systems. Capacity goes into coping with that noise, and outputs inherit it. Consistency is signal. A model that learns one design system can be small: Virtua-12M has 12.54 million parameters and a 50 MB checkpoint.

The first Virtua pretraining used 28,770 Regular to Bold pairs traced from Google Fonts binaries. It was retired for two reasons that both point the same way. Compiled outlines carry point bloat, so the model learned to draw dense, compiled-looking outlines. And unrelated designs made the model spend capacity absorbing accidents. The corpus is now original work on the dyadic grid only.

## Glyphs as sentences

A glyph is an ordered list of drawing commands, and a transformer predicts sequences. A codec converts each UFO outline into tokens and back. The round trip is exact because the sources and the codec share the 2-unit grid.

```
BOS N_two U_0032 W400 ADV 592
MOVE 48 0
LINE 528 0
LINE 544 16
...
CURVE 116 258 32 146 32 32
LINE 32 16
CLOSE
EOS
```

| token class | values |
| --- | --- |
| commands | `MOVE`, `LINE`, `CURVE`, `CLOSE` |
| conditioning | glyph name `N_*`, codepoint `U_*`, weight `W400` to `W700`, `ADV` |
| coordinates | one token per 2-unit position from -512 to 1280, 897 tokens |
| deltas | one token per 2-unit offset from -384 to 384, 385 tokens, used for weight transfer |

Values out of range are rejected, never clipped. Each glyph is about 90 tokens.

## From source to corpus

1. The corpus builder reads a style's designspace and UFO masters at a tagged revision. Only drawn `<source>` masters are read. Instances never train.
2. Each glyph is filtered by grade. Only green glyphs enter. Purple drafts and the grades red, orange and yellow do not enter.
3. Glyphs that fail the grid check or the structure checks are dropped. Composites are decomposed and overlap is removed. Combining marks are dropped.
4. Pairs for weight transfer are built from point-compatible glyphs of the base and the heaviest master. A pair whose mean point movement is under 8 units is dropped as Bold debt.
5. Masters are amplified by interpolation at dyadic weights from the base-2 van der Corput sequence, snapped to the grid. The corpus is therefore bit-reproducible.
6. Held-out evaluation glyphs are removed before any augmentation, so that no interpolation leaks them into training.

The provenance of every sample is recorded: repository, revision, glyph name, master and grade. The manifest is published with each model.

## The data engineering checklist

Before any training run, a person signs off on:

- Source, never compiled. Upstream repository and commit recorded.
- Overlap removed on every glyph, composites decomposed first.
- Point economy, cubics only, closed and correctly wound contours.
- Grid conformance checked visually in review UFOs in Runebender.
- License confirmed per source, attribution kept.
- Real advance widths and sane sidebearings.
- Letterforms only.
- An automated QA report attached.

## Evaluation rules

1. Hold out glyphs the model never trains on, including through interpolation.
2. Compare with a plain baseline. For weight transfer the baseline shifts each base point by the mean Regular to Bold delta. A model ships only if it beats the baseline.
3. Run several seeds and publish mean and standard deviation. The first Virtua result, a coordinate error of 20.9, was a lucky draw. Across five seeds it is 24.0 plus or minus 1.6 against a baseline of 31.3.
4. State what the score misses. Coordinate error says nothing about curve continuity. IoU says nothing about position.

## Known limits

- A model trained on few styles draws in those styles. More hand-drawn designs on the grid is the fix.
- Optical corrections live in small offsets. A grid that is too coarse removes them. The 8-unit default with a 2-unit floor is the current compromise.
- Producing valid output for unseen input is the hardest problem facing neural fonts. Constrained decoding, which forbids illegal tokens at each position, is the current answer for outlines.
