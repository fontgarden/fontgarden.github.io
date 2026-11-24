---
title: Post-authorship and open weights
section: introduction
order: 10
summary: The position of the collection on authorship, licenses and the origin of training data.
introduction: Font.Garden is one collection without named authors. No designer signs a family, no font has a Reserved Font Name, and no training data comes from fonts of other people. The fonts have the OFL and the model weights are open. Each sample of the corpus has a record of its source file, its revision and its grade.
next: [collection, neuraltype]
---

## One collection without authors

Most type foundries publish families by named designers. A model that trains on such a catalog gets outlines from hundreds of people. Each person has different drawing conventions, and the model uses capacity to learn the differences. A normalization step after the fact removes information from the outlines.

Font.Garden uses a different method. A small team draws a core set of glyphs by hand on one grid system. Local models draft the other glyphs with the same conventions. A person grades each glyph. The result is an open font library with one standard, and each approved glyph is also training data.

No person signs a glyph. The drawings and the corrections belong to the collection. This practice follows the International Typographic Style, which gave more importance to the system than to the person who drew a design. The posts [Diffuse Value Capture](https://elih.net/blog/diffuse-value-capture/) and [Local AI in Runebender](https://elih.net/blog/local-ai-in-runebender/) describe the practice.

## Three rules

1. The fonts have the [SIL Open Font License 1.1](https://openfontlicense.org), without a Reserved Font Name. The OFL FAQ states that a font from a model that trained on OFL sources is a derivative work, and that it keeps the OFL. The collection accepts this.
2. The model weights have the Apache-2.0 license. The tools and the engines have Apache-2.0 or MIT. These licenses are permissive.
3. Training targets come only from the sources of the collection. A font of another party can be an input to a tool, for example as a reference image. It is not a training target. A compiled font is not a source. See [Training data](/docs/dataset/).

## The record of origin

A model that trained on fonts from the web has no record of the origin of a shape. The collection has this record. Each sample gives the repository, the revision, the glyph name, the master and the grade. The corpus manifest is public. A project cannot add this record after it trained on fonts without one.

## Conditions for a contributor

- Your drawings become part of the collection, with the OFL. Your name goes into `CONTRIBUTORS.txt`. If you hold copyright, your name also goes into `AUTHORS.txt`. A family does not have a credit line.
- Each glyph that you draw on the grid is training data. If you do not accept this use, do not contribute the work. The collection has no opt-out for single contributions.
- You keep your copyright. The OFL requires attribution, and it does not permit the sale of the font alone. It does not transfer ownership.
