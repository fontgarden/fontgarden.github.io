---
title: The NeuralType format
section: introduction
label: start
order: 20
summary: A short description of the .ntf font format and how it relates to the OpenType fonts in the catalog.
callout: NeuralType (.ntf) is a font format in which the font file is a small neural network. The network computes each letterform from the character, its context and a set of continuous parameters. This chapter is a summary. The specification and the Rust engine are at <a href="https://github.com/eliheuer/post-opentype">github.com/eliheuer/post-opentype</a>.
background: [culture]
next: [tools, grid]
---

## A font as a function

Any font system can be written as a function. Text and context go in. Shapes and positions come out.

```
glyph = F(character, context, parameters)
```

OpenType approximates this function with a table of fixed outlines and a rule system (`cmap`, `GSUB`, `GPOS`) that selects among them. Every form the font can produce must be drawn in advance.

A `.ntf` file stores the function directly, as the weights of a small network. The engine evaluates the network for each glyph when the text changes, then traces the result into bezier outlines. Contextual forms are generated, not enumerated. Elongation (kashida) is a scalar input, not a separate glyph. Any learned axis, such as weight or slope, works the same way.

## The file

A v0 file has three parts:

| offset | content |
| --- | --- |
| 0 | magic `NTF0` |
| 4 | header length as a 32-bit little-endian integer |
| 8 | JSON header, padded so the weights start on a 4-byte boundary |
| 8 + header | raw little-endian float weights, layer by layer |

The header names the format version, the script, the style, the supported alphabet and the layer sizes. There is no table graph and no rule bytecode.

## Current models

Two public demonstrations exist, both with live text input:

- A square Kufic font of 53,600 weights in a 215 KB file. Described in [NeuralType: A Post-OpenType Font Format](https://elih.net/blog/neuraltype/).
- A Nastaliq font distilled from Gulzar, an OFL Nastaliq font, into 1.36 million parameters. With 8-bit weights the file is 1.38 MB. Described in [Nastaliq Distilled](https://elih.net/blog/nastaliq-distilled/).

## Relation to the OpenType catalog

The families in the catalog are drawn as UFO sources and compiled to OpenType. They are also the training material for the models. A `.ntf` font is a second output of the same sources. The grid and grade rules in this guide exist so that the sources can serve both purposes.
