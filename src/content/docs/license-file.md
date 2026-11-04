---
title: License files
section: sources
label: templ
order: 130
summary: The OFL, AUTHORS and CONTRIBUTORS files, and the licenses used for code and models.
callout: Three plain text files at the top of the repository record who made the family and under what terms it is released. They are required for the catalog and for inclusion in a training corpus.
background: [culture, upstream]
next: [grid]
---

## OFL.txt

The full text of the SIL Open Font License 1.1, preceded by the copyright notice. Get the text from [openfontlicense.org](https://openfontlicense.org). The first lines look like this:

```
Copyright 2026 The [Family] Project Authors (https://github.com/[owner]/[repo])

This Font Software is licensed under the SIL Open Font License, Version 1.1.
This license is copied below, and is also available with a FAQ at:
https://openfontlicense.org
```

Do not add a Reserved Font Name. See [Open fonts and open weights](/docs/culture/).

The same copyright line goes into the UFO `fontinfo.plist` fields `copyright`, `openTypeNameLicense` and `openTypeNameLicenseURL`, so the compiled fonts carry it.

## AUTHORS.txt

The copyright holders, one per line, with an email or URL.

```
# This is the official list of project authors for copyright purposes.
# This file is distinct from the CONTRIBUTORS.txt file.

Eli Heuer <eli@elih.net>
```

## CONTRIBUTORS.txt

Everyone who contributed work, whether or not they hold copyright.

```
# This is the list of people who have contributed to this project,
# whether or not they hold copyright. See AUTHORS.txt for copyright holders.

Eli Heuer <eli@elih.net>
```

## Code and models

Scripts in a font repository are covered by the OFL together with the fonts unless a separate license file says otherwise. Stand-alone tools and engines use Apache-2.0 or MIT. The NeuralType engine is dual-licensed under both. Released model weights use Apache-2.0.
