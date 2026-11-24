---
title: The NeuralType format
section: introduction
order: 30
summary: A short description of the .ntf font format and its relation to the collection.
introduction: NeuralType (.ntf) is a font format in which the font file is a small neural network. The network calculates each letterform from the character, its context and a set of continuous parameters. The specification and the Rust engine are at <a href="https://github.com/eliheuer/post-opentype">github.com/eliheuer/post-opentype</a>, with the Apache-2.0 or MIT license.
background: [collection]
next: [tools, grid]
---

## A font as a function

A font system is a function. The inputs are text, context and parameters. The outputs are shapes and positions.

```
shapes, positions = f(text, context, parameters)
```

OpenType approximates this function with a table of fixed outlines and a set of rules (`cmap`, `GSUB`, `GPOS`) that select outlines. A designer must draw each form of the font before use. For connected scripts the approximation has low precision. Arabic has four joining classes in OpenType, and the written tradition has a continuous range of forms. The Nastaliq style puts letters at heights that change with the context, and the rule system does not describe this well.

A `.ntf` file holds the function as the weights of a small network. The engine evaluates the network for each glyph when the text changes. Then it traces the result into Bézier outlines. The network generates the contextual forms, so the file has no list of them. Elongation (kashida) is a scalar input and not a glyph. A learned axis, for example weight or slope, is also an input.

## File structure

A file of version 0 has four parts:

| part | content |
| --- | --- |
| 1 | the magic bytes `NTF0` |
| 2 | the header length, as a 32-bit little-endian number |
| 3 | the JSON header: format, script, style, alphabet and layer sizes, with padding to a 4-byte boundary |
| 4 | the weights, layer by layer |

The file has no graph of tables and no rule bytecode. A renderer can map the file into memory and read the weights there.

## Engine

The engine is in Rust, on Linebender libraries. It compiles to WASM for the browser. It has four stages:

1. Shape: find the joining forms.
2. Generate: evaluate the model one time for each form.
3. Layout.
4. Trace.

The output of the current models is deterministic.

## Current models

| model | source | parameters | file |
| --- | --- | --- | --- |
| square Kufic | training grids written by hand | 53,600 | 215 KB at f32 |
| Nastaliq | distilled from Gulzar, an OFL Nastaliq font, with shaping by HarfRust | 1,357,995 | 1.38 MB at int8 |

For each cluster, the Nastaliq model predicts a signed-distance field and a position. Its IoU on held-out strings is 0.945. Three larger versions of the model did not give a better result. The posts [NeuralType](https://elih.net/blog/neuraltype/) and [Nastaliq Distilled](https://elih.net/blog/nastaliq-distilled/) have demonstrations and the full record.

## Relation to the collection

The masters of the collection are UFO sources, and the build compiles them to OpenType. The masters are also the training data of the models. A `.ntf` font is a second output of the same sources. The grid rules and the grade rules of this guide make the sources correct for both outputs.

The Nastaliq model is a distillation of an OpenType font. A font that starts as a NeuralType design needs an editor in which a designer can design and train a neural font. That editor is the next stage of Runebender.
