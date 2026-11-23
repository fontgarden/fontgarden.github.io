---
title: Models
section: data
label: nerd
order: 420
summary: The models trained on the collection, how they run, and what is released.
callout: "The collection trains two kinds of model. Glyph language models draw outlines as token sequences and run inside Runebender. NeuralType models are fonts: the weights draw letterforms in context. Both run locally on a laptop or a gaming GPU. Weights are released under Apache-2.0. The first public release is in preparation."
background: [dataset, neuraltype]
next: [contributing]
---

## Virtua-12M

| Virtua-12M-v0.1 | |
| --- | --- |
| architecture | decoder-only transformer, 6 layers, 384 dimensions, 8 heads |
| parameters | 12.54 million |
| context | 1,368 tokens |
| vocabulary | about 1,700 tokens: commands, names, coordinates, deltas |
| tasks | weight transfer (bolden), completion, sketch to glyph |
| training | one M4 Pro laptop in 3 hours 20 minutes with MLX, or 20 minutes on an RTX 2060 SUPER |
| checkpoint | 50 MB, float32 safetensors |
| release | planned: Hugging Face `fontgarden/virtua`, Apache-2.0. Not yet uploaded. |

Weight transfer is delta prediction. Given the base master, the model predicts, one point at a time, the offset from each point to its position in the heavier master. Each delta is a small bounded move, which is what lets a small model do the job, and the point structure is preserved by construction, so the masters still interpolate. The output is a draft, marked purple. A person corrects it on the 2-unit grid.

Two implementations, MLX and PyTorch, are held to identical output by a parity script. Weights will ship as float32 so that others can continue training. The model card will record the baseline, the model score across seeds, and the corpus manifest.

## Running models

Task models run through `font-ml`, a Rust crate built on Candle with Metal or CUDA. A bolden pass takes about half a second per glyph on an M4 Pro. A model package is a directory with `config.json`, `weights.safetensors` and `vocab.txt`. Packages live in `~/Runebender/models/<kind>/<name>` and, per font, in `MyFont.models/`.

The Shapes tool trains a separate 5.5 million parameter model from scratch on a UFO of named shapes. A quick run takes about 12 minutes and a thorough run about 30 on an M4 Pro. Adding a shape to a trained base takes about 2 minutes. This is the smallest demonstration of the whole loop: draw, train, propose, grade.

Chat models are open-weight GGUF files run through `llama-server`. They answer questions about a font by calling editor tools that return measurements. A 4B model gives a correct stem width only with a tool.

## NeuralType models

A NeuralType model is distilled from a teacher. For the Nastaliq model the teacher is Gulzar shaped with HarfRust: for every one, two and three letter string, the shaper returns glyph ids, advances and offsets, and the outlines are read from the font. The student is a feed-forward network that predicts a signed-distance field for each cluster and its position. See [The NeuralType format](/docs/neuraltype/).

The next model is a font designed for NeuralType from the start, on the collection's grid, rather than distilled from an OpenType font.

## Releases

| model | task | where | license | status |
| --- | --- | --- | --- | --- |
| Virtua-12M-v0.1 | weight transfer | Hugging Face `fontgarden/virtua` | Apache-2.0 | in preparation |
| gulzar-int8.ntf | Nastaliq NeuralType font | the demo of the post [Nastaliq Distilled](https://elih.net/blog/nastaliq-distilled/) | OFL, with Gulzar's copyright notice | released |

The Virtua-12M-v0.1 upload is the next release task. Until it is done, the only public model file is the Nastaliq font. What stays private: the training code, the corpus tools and the plans. The editor, the model runtime, the sources and the released weights are public.

## Model file safety

Published model files are safetensors or GGUF, which hold numbers rather than code. Check the publisher's account name letter by letter, compare the SHA-256 checksum, and read the license field inside the file before you load it.
