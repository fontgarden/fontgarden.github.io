---
title: Licenses
section: sources
order: 130
summary: The OFL, AUTHORS and CONTRIBUTORS files, and the licenses for code, models and the outputs of models.
introduction: Three text files at the root of each source repository record the contributors and the license of the fonts. The copyright holder is the project and not a designer. You can copy the templates of this chapter without change.
background: [culture, sources]
next: [grid]
---

## OFL.txt

`OFL.txt` has the copyright notice, then the full text of the SIL Open Font License 1.1. Get the text from [openfontlicense.org](https://openfontlicense.org). These are the first lines:

```
Copyright 2026 The Font Garden Project Authors (https://github.com/fontgarden)

This Font Software is licensed under the SIL Open Font License, Version 1.1.
This license is copied below, and is also available with a FAQ at:
https://openfontlicense.org
```

Do not add a Reserved Font Name. The modification terms of the OFL still require a new name for a changed font. The collection does not add the second restriction of a Reserved Font Name. As a result, the terms for derived fonts and for the outputs of models are short.

Put the same copyright line into the fields `copyright`, `openTypeNameLicense` and `openTypeNameLicenseURL` of `fontinfo.plist` in the UFO. The compiled fonts then contain it.

## AUTHORS.txt

`AUTHORS.txt` lists the copyright holders. Each line has one name and an email address or a URL.

```
# This is the official list of project authors for copyright purposes.
# This file is distinct from the CONTRIBUTORS.txt file.

Eli Heuer <eli@elih.net>
```

## CONTRIBUTORS.txt

`CONTRIBUTORS.txt` lists each person who contributed drawings, corrections or code. A person in this list can hold copyright or not. This list is the only credit for a person in the collection.

```
# This is the list of people who have contributed to this project,
# whether or not they hold copyright. See AUTHORS.txt for copyright holders.

Eli Heuer <eli@elih.net>
```

## Code, models and outputs

| item | license |
| --- | --- |
| scripts in a source repository | OFL, as for the fonts, unless a file gives a different license |
| Runebender, font-ml, img2bez, DesignBot, the NeuralType engine | Apache-2.0 or MIT |
| released model weights | Apache-2.0 |
| fonts that a model made, when the model trained on the collection | OFL |

The last line follows question 1.25 of the OFL FAQ, version 1.1-update7. A font from a model that trained on OFL sources is a derivative work, and it keeps the OFL. The FAQ does not make a statement about the weights. For a model that trained only on the sources of the collection, the copyright holder is the project. The project selects Apache-2.0 for the weights.

## Fonts of other parties

A font of another party can go into a repository only as a reference, in the `reference-fonts` directory that Git ignores. Its license must permit that use. Most foundry licenses do not permit training on the font software, on rendered glyphs or on outlines. The collection does not use a font of another party as a training target, so that term does not apply. The license must still permit the use as a reference. If you are not sure about a license, use a font with the OFL or CC0.
