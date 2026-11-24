---
title: The collection
section: introduction
order: 20
summary: The contents of the Font.Garden collection and the procedure that adds to it.
introduction: The collection has three parts. The first part is a set of masters, each drawn on one dyadic grid system. The second part is the models that train on the masters. The third part is the fonts that come from both. The collection becomes larger when a person draws a new design on the grid and when a person grades the drafts of a model.
background: [culture]
next: [neuraltype, tools]
---

## Contents

The first font of the collection is Virtua Grotesk, a neo-grotesk on the grid of [The dyadic grid](/docs/grid/). It has masters at four weights: Thin, Regular, Bold and Black. It has the Latin, Arabic and Hebrew scripts. Each weight has a master at the optical sizes 14 pt and 144 pt. The Thin, Black and 144 pt masters start as calculated drafts from the Regular and Bold masters. The sources and the design documentation are public at [github.com/eliheuer/virtua-grotesk](https://github.com/eliheuer/virtua-grotesk).

The first model is Virtua-12M-v0.1, a decoder-only transformer with 12.54 million parameters. Its training data is the Regular and Bold masters. It drafts a Bold from a Regular, and it draws a brush sketch again with the conventions of the collection. See [Models](/docs/models/).

The published fonts are in the index at [font.garden/fonts](/fonts/). Each font has a number and a standard specimen page. See [The font index and the specimen page](/docs/font-index/).

The plan has three more designs on the same grid: an oldstyle serif in the Plantin tradition, a monospaced font and an italic of Virtua Grotesk. Each design adds a style and more data to the corpus.

## Growth procedure

1. A person draws a core set of glyphs for a new style on the grid.
2. A model drafts the other glyphs of a master, the other masters and the other scripts. Each draft is purple.
3. A person corrects and grades each draft. Green glyphs go into the corpus.
4. The model trains again on the larger corpus.

Interpolation between masters gives a large number of samples, because each interpolation on the grid is a valid instance. Interpolation does not give new styles. New styles come only from new designs that a person draws.

## Exclusions

- The collection is not a catalog of families by named designers. See [Post-authorship and open weights](/docs/culture/).
- The collection does not train on Google Fonts or on other OFL collections. An early experiment trained on compiled fonts, and the project stopped it. Compiled outlines contain conversion artifacts, and designs without a relation to each other add noise. See [Training data](/docs/dataset/).
- The collection is not a service that makes a font from a text prompt. Generation without examples is not a goal.

## Long-term goal

The goal is a font that is a model and not a table of outlines. An OpenType font holds one fixed shape for each glyph. A neural font draws each glyph for its context. The sources of the collection have the properties that the training of such fonts needs. See [The NeuralType format](/docs/neuraltype/).
