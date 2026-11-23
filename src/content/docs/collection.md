---
title: The collection
section: introduction
label: start
order: 20
summary: What the Font Garden collection is today and how it grows.
callout: The collection is a set of masters drawn on one dyadic grid system, the models trained on them, and the fonts generated from both. It grows by drawing more designs on the same grid and by grading what the models draft. This chapter describes the state of the collection and the plan for it.
background: [culture]
next: [neuraltype, tools]
---

## What is in it

The seed of the collection is Virtua Grotesk, a neo-grotesk drawn on the dyadic self-labeling grid described in [The dyadic grid](/docs/grid/). It has masters at four weights, Thin, Regular, Bold and Black, with Latin, Arabic and Hebrew. Each weight has a master at the optical sizes 14 and 144 pt. The Thin, Black and 144 pt masters start as calculated drafts from the Regular and Bold masters. Its sources and design documentation are public at [github.com/eliheuer/virtua-grotesk](https://github.com/eliheuer/virtua-grotesk).

The first model, Virtua-12M-v0.1, is a 12.54 million parameter decoder-only transformer trained on the Regular and Bold masters. It drafts a Bold from a Regular and redraws a brush sketch in the collection's conventions. See [Models](/docs/models/).

The published fonts are in the index at [font.garden/fonts](/fonts/). Each font has a number and a standard specimen page. See [The font index and the specimen page](/docs/font-index/).

The next designs planned on the same grid are an oldstyle serif in the Plantin tradition, a mono, and an italic of Virtua. Each adds a style region to the collection and real data to the corpus.

## How it grows

1. A person draws a core set of glyphs for a new style on the grid.
2. A model drafts the rest: the remaining glyphs of a master, the other masters, the other scripts. Drafts are marked purple.
3. A person corrects and grades each draft. Green glyphs enter the corpus.
4. The model is retrained on the larger corpus and the next drafts are better.

Interpolation between masters gives volume, because every grid-snapped interpolation is a valid instance. Variety comes only from new hand-drawn designs. The corpus grows by drawing, not by collecting.

## What it is not

- It is not a catalog of families by named designers. See [Post-authorship and open weights](/docs/culture/).
- It is not trained on Google Fonts or other OFL collections. An early experiment did this, from compiled binaries, and was retired because compiled outlines carry conversion artifacts and unrelated designs add noise. See [The collection is the dataset](/docs/dataset/).
- It is not a text-to-font service. Zero-shot generation from a prompt is not a goal.

## The long-term aim

Fonts that are models rather than tables of outlines. An OpenType font stores one fixed shape per glyph in a box inherited from metal type. A neural font draws each glyph in context. The collection is being built so that its sources can train such fonts. See [The NeuralType format](/docs/neuraltype/).
