---
title: Training data
section: data
order: 410
summary: The procedure that makes a training corpus from graded sources on the grid.
introduction: Font.Garden does not collect fonts for training. The training data is the masters of the collection, which are on the grid and have a grade for each glyph. This chapter describes the procedure from a source to a corpus. The training code and the corpus tools are private. The corpus manifest and the evaluation numbers are public.
background: [grid, grades, culture]
next: [models]
---

## Reasons for designed data

A model that trains on fonts from many designers gets many conventions: different point structures, curve conventions, contour directions and unit systems. The model uses capacity for these differences, and its outputs contain them. A model that trains on one design system can be small. Virtua-12M has 12.54 million parameters and a checkpoint of 50 MB.

The first pretraining of Virtua used 28,770 pairs of Regular and Bold glyphs, traced from compiled Google Fonts files. The project stopped this method for two reasons:

- Compiled outlines have more points than their sources. The model learned to draw outlines with too many points.
- The designs had no relation to each other. The model used capacity for their differences.

The corpus now contains only original work on the dyadic grid.

## Token sequence of a glyph

A glyph is an ordered list of drawing commands, and a transformer predicts sequences. A codec converts each UFO outline into tokens, and tokens into an outline. The conversion in both directions is exact, because the sources and the codec use the same 2-unit grid.

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
| conditions | the glyph name `N_*`, the code point `U_*`, the weight `W400` to `W700`, `ADV` |
| coordinates | one token for each 2-unit position from -512 to 1280, 897 tokens |
| deltas | one token for each 2-unit offset from -384 to 384, 385 tokens, for weight transfer |

The codec rejects a value that is out of range. It does not clip the value. Each glyph has approximately 90 tokens.

## Procedure from source to corpus

1. The corpus builder reads the designspace and the UFO masters of a style at a tagged revision. It reads only the `<source>` masters that a person drew. Instances are not training data.
2. The builder selects glyphs by grade. Only green glyphs go into the corpus. Purple drafts and red, orange and yellow glyphs do not.
3. The builder removes each glyph that fails the grid check or the structure checks. It decomposes composites and removes overlap. It removes combining marks.
4. The builder makes pairs for weight transfer from the point-compatible glyphs of the base master and the heaviest master. It removes a pair when the mean point movement is less than 8 units. Such a pair is Bold debt. See [Glyph grades](/docs/grades/).
5. The builder interpolates the masters at dyadic weights from the base-2 van der Corput sequence, and it puts each result on the grid. As a result, each build of the corpus gives the same bits.
6. The builder removes the held-out evaluation glyphs before step 5. Thus no interpolation puts them into the training data.

Each sample has a record of its origin: repository, revision, glyph name, master and grade. Each model release includes the manifest.

## Data checklist

Before each training run, a person approves these items:

- The data comes from sources and not from compiled fonts. The record gives the upstream repository and the commit.
- Each glyph has no overlap, and each composite was decomposed first.
- The outlines have few points, only cubic curves, and closed contours with the correct direction.
- A person examined the grid conformance in review UFOs in Runebender.
- Each source has a confirmed license and its attribution.
- The advance widths are the real values, and the sidebearings are in the usual range.
- The data contains only letterforms.
- An automatic QA report is attached.

## Evaluation rules

1. Hold out glyphs that the model does not train on. This includes glyphs from interpolation.
2. Compare the model with a simple baseline. For weight transfer, the baseline moves each base point by the mean delta from Regular to Bold. A model release is permitted only when the model has a better score than the baseline.
3. Do more than one run with different seeds, and publish the mean and the standard deviation. The first result of Virtua was a coordinate error of 20.9 from one seed. The result of five seeds is 24.0 with a standard deviation of 1.6. The baseline is 31.3.
4. State the limits of the score. Coordinate error does not measure curve continuity. IoU does not measure position.

## Known limits

- A model that trained on few styles draws in those styles. The correction is more designs on the grid that a person draws.
- Optical corrections are small offsets. A grid that is too coarse removes them. The current values are an 8-unit default grid and a 2-unit minimum grid.
- Valid output for new input is the most difficult problem of neural fonts. The current method for outlines is constrained decoding, which does not permit an illegal token at any position.
