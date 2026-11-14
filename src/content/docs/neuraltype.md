---
title: The NeuralType format
section: introduction
label: start
order: 30
summary: A short description of the .ntf font format and how the collection relates to it.
callout: NeuralType (.ntf) is a font format in which the font file is a small neural network. The network computes each letterform from the character, its context and a set of continuous parameters. The specification and the Rust engine are at <a href="https://github.com/eliheuer/post-opentype">github.com/eliheuer/post-opentype</a>, under Apache-2.0 or MIT.
background: [collection]
next: [tools, grid]
---

## A font as a function

Any font system can be written as a function. Text and context go in. Shapes and positions come out.

```
shapes, positions = f(text, context, parameters)
```

OpenType approximates this function with a table of fixed outlines and a rule system (`cmap`, `GSUB`, `GPOS`) that selects among them. Every form the font can produce must be drawn in advance. For connected scripts the approximation is coarse. Arabic gets four joining classes where the written tradition has a continuum, and Nastaliq's context-dependent stacking defeats the model almost entirely.

A `.ntf` file stores the function directly, as the weights of a small network. The engine evaluates the network for each glyph when the text changes, then traces the result into bezier outlines. Contextual forms are generated, not enumerated. Elongation (kashida) is a scalar input, not a glyph. Any learned axis, such as weight or slope, works the same way.

## The file

A v0 file has four parts:

| part | content |
| --- | --- |
| 1 | magic bytes `NTF0` |
| 2 | header length, 32-bit little-endian |
| 3 | JSON header: format, script, style, alphabet, layer sizes, padded to a 4-byte boundary |
| 4 | the weights, layer by layer |

There is no table graph and no rule bytecode. A renderer can map the file into memory and read the weights in place.

## The engine

The engine is written in Rust on Linebender libraries and compiles to WASM for the browser. It runs four stages: shape (determine joining forms), generate (one model pass per form), layout, and trace. Output is deterministic in the current models.

## Current models

| model | source | parameters | file |
| --- | --- | --- | --- |
| square Kufic | hand-written training grids | 53,600 | 215 KB at f32 |
| Nastaliq | distilled from Gulzar, an OFL Nastaliq font, shaped with HarfRust | 1,357,995 | 1.38 MB at int8 |

The Nastaliq model predicts a signed-distance field per cluster plus its position, and scored an IoU of 0.945 on held-out strings. Three attempts to improve it by making it larger failed. The posts [NeuralType](https://elih.net/blog/neuraltype/) and [Nastaliq Distilled](https://elih.net/blog/nastaliq-distilled/) have live demos and the full record.

## Relation to the collection

The collection's masters are UFO sources compiled to OpenType. They are also the training material for the models. A `.ntf` font is a second output of the same sources. The grid and grade rules in this guide exist so that the sources can serve both purposes. A font designed for NeuralType from the start, rather than distilled from an OpenType font, needs an editor for designing and training neural fonts. That editor is the next step for Runebender.
