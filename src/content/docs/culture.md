---
title: Open fonts and open weights
section: introduction
label: start
order: 10
summary: The licensing and provenance rules that every Font Garden project follows.
callout: Every font in the Font Garden catalog is released under the SIL Open Font License. Every model we release has open weights. Every training corpus is built from sources whose license permits it. This chapter explains why these three rules exist and what they mean for a contributor.
next: [neuraltype, tools]
---

## Three rules

1. Fonts are published under the [SIL Open Font License 1.1](https://openfontlicense.org) (OFL). Anyone can use, study, modify and redistribute them.
2. Model weights are published under an open license. The first release, Virtua-12M-v0.1, is on Hugging Face at `fontgarden/virtua` under Apache-2.0.
3. Training data comes only from sources that permit it. The default source is our own catalog, which we draw on the grid system described in this guide. OFL fonts from other authors can enter a corpus only with their license files intact and a record of where they came from.

## Why provenance matters

Most font generation models are trained on scraped data. The fonts are collected from the web, rasterized, and used without the author's knowledge. The type design community has rejected this practice.

Font Garden takes the opposite position. The dataset is published. Every sample can be traced to a source file, a license and a grade. This stance cannot be adopted later by a project that already trained on scraped data, so it is a durable difference, not a marketing claim.

## What open means for contributors

- Your source files, not only the compiled fonts, are public once a family is in the catalog. A private repository is acceptable while a project is in progress.
- You keep your copyright. The OFL requires attribution and forbids selling the font by itself. It does not transfer ownership.
- A family in the catalog is also training data. If you do not want your work used this way, do not submit it to the catalog. There is no separate opt-out.

## Reserved font names

The OFL lets an author reserve the font name. Font Garden families do not use Reserved Font Names. A fork must still change the name under the OFL's modification terms, but we do not add the extra legal restriction. This keeps derived families and model outputs simple to redistribute.
