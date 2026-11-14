---
title: Post-authorship and open weights
section: introduction
label: start
order: 10
summary: The position the collection takes on authorship, licensing and provenance.
callout: Font Garden is one authorless collection. There are no families signed by a designer, no reserved font names and no scraped training data. Fonts are OFL. Model weights are open. Every sample in the corpus can be traced to a source file, a revision and a grade. This chapter explains the position and what it means for a contributor.
next: [collection, neuraltype]
---

## One collection, no authors

Most type is published as families by named designers. A font AI trained on such a catalog learns the drawing habits of hundreds of people and spends its capacity reconciling them. Normalizing the fonts afterward removes information.

Font Garden takes a different approach. A small team draws a core set by hand on one grid system, local models draft the rest in the same conventions, and a person grades every glyph. The result is an open font library held to one standard, in which every glyph is also clean training data.

Nobody signs a glyph. The drawings and the corrections are the expert data, and they belong to the collection. This follows the authorless commons of the International Typographic Style, in which the system matters more than the hand that executed it. The practice is described in the posts [Diffuse Value Capture](https://elih.net/blog/diffuse-value-capture/) and [Local AI in Runebender](https://elih.net/blog/local-ai-in-runebender/).

## Three rules

1. Fonts are published under the [SIL Open Font License 1.1](https://openfontlicense.org) without a Reserved Font Name. The OFL FAQ states that a font made by a model trained on OFL sources is a derivative work and stays under the OFL. The collection accepts this.
2. Model weights are published under Apache-2.0. Tools and engines are published under Apache-2.0 or MIT. Both are permissive licenses, like the OFL without its reserved name clause.
3. Training targets come only from the collection's own sources. A foreign font may be an input to a tool, for example as a reference raster. It is never a training target. Compiled fonts are never used as sources. See [The collection is the dataset](/docs/dataset/).

## Why provenance matters

Models trained on scraped fonts cannot say where a shape came from. The collection can. Each sample records the repository, the revision, the glyph name, the master and the grade. The corpus manifest is public. A project that already trained on scraped data cannot adopt this position later, so it is a durable difference rather than a marketing claim.

## What this means for a contributor

- Your drawings become part of the collection under the OFL, with your name in `CONTRIBUTORS.txt` and, if you hold copyright, in `AUTHORS.txt`. There is no per-family credit.
- Everything you draw on the grid is training data. If you do not want your work used this way, do not contribute it. There is no separate opt-out.
- You keep your copyright. The OFL requires attribution and forbids selling the font by itself. It does not transfer ownership.
