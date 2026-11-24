---
title: Models
section: data
order: 420
summary: The models that train on the collection, the way to run them and the releases.
introduction: "The collection trains two types of model. A glyph language model draws an outline as a sequence of tokens, and it operates in Runebender. A NeuralType model is a font: its weights draw letterforms for a context. Both types run on a laptop or on a consumer GPU. The weights have the Apache-2.0 license. The first public release is in preparation."
background: [dataset, neuraltype]
next: [contributing]
---

## Virtua-12M

| Virtua-12M-v0.1 | |
| --- | --- |
| architecture | decoder-only transformer, 6 layers, 384 dimensions, 8 heads |
| parameters | 12.54 million |
| context | 1,368 tokens |
| vocabulary | approximately 1,700 tokens: commands, names, coordinates, deltas |
| tasks | weight transfer, completion, sketch to glyph |
| training | 3 hours 20 minutes with MLX on one M4 Pro laptop, or 20 minutes on an RTX 2060 SUPER |
| checkpoint | 50 MB, float32 safetensors |
| release | planned at Hugging Face `fontgarden/virtua`, Apache-2.0. Not uploaded at this time. |

Weight transfer is the prediction of deltas. The input is the base master. For each point, the model predicts the offset to the position of that point in the heavier master. Each delta is a small move with a limit, so a small model is sufficient. The point structure does not change, so the masters still interpolate. The output is a purple draft. A person corrects it on the 2-unit grid.

The model has two implementations, in MLX and in PyTorch. A parity script makes sure that they give the same output. The weights will be float32, so that other people can continue the training. The model card will give the baseline, the score of the model for each seed and the corpus manifest.

## Local operation

`font-ml` runs the task models. It is a Rust crate on Candle, with Metal or CUDA. Weight transfer for one glyph takes approximately half a second on an M4 Pro. A model package is a directory with `config.json`, `weights.safetensors` and `vocab.txt`. The packages are in `~/Runebender/models/<kind>/<name>`. A font can have its own packages in `MyFont.models/`.

The Shapes tool trains a different model, with 5.5 million parameters, on a UFO of named shapes. It starts without pretrained weights. On an M4 Pro, a short run takes approximately 12 minutes and a full run approximately 30 minutes. The addition of one shape to a trained base takes approximately 2 minutes. This tool shows the full procedure at the smallest scale: draw, train, propose and grade.

The chat models are open-weight GGUF files that `llama-server` runs. A chat model answers a question about a font with calls to editor tools that return measurements. A model with 4 billion parameters gives a correct stem width only when it has such a tool.

## NeuralType models

A NeuralType model is a distillation of a teacher. For the Nastaliq model, the teacher is the Gulzar font with shaping by HarfRust. For each string of one, two and three letters, the shaper returns glyph IDs, advances and offsets. The outlines come from the font. The student is a feed-forward network. For each cluster, it predicts a signed-distance field and a position. See [The NeuralType format](/docs/neuraltype/).

The next model is a font that starts as a NeuralType design on the grid of the collection. It is not a distillation of an OpenType font.

## Releases

| model | task | location | license | status |
| --- | --- | --- | --- | --- |
| Virtua-12M-v0.1 | weight transfer | Hugging Face `fontgarden/virtua` | Apache-2.0 | in preparation |
| gulzar-int8.ntf | Nastaliq NeuralType font | the demonstration of the post [Nastaliq Distilled](https://elih.net/blog/nastaliq-distilled/) | OFL, with the copyright notice of Gulzar | released |

The upload of Virtua-12M-v0.1 is the next release task. Until then, the Nastaliq font is the only public model file. The training code, the corpus tools and the plans are private. The editor, the model runtime, the sources and the released weights are public.

## Safety of model files

The published model files are safetensors or GGUF. These formats hold numbers and no code. Before you load a model file, do these steps:

1. Compare each letter of the account name of the publisher with the correct name.
2. Compare the SHA-256 checksum.
3. Read the license field in the file.
