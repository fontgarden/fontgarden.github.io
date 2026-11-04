---
title: README file
section: sources
label: templ
order: 120
summary: What the README of a font project must contain, with a template.
callout: The README is the first thing a visitor reads. It names the family, shows it, states the license, and tells a developer how to build it. Copy the template below into a new project and replace the bracketed parts.
background: [upstream]
next: [license-file]
---

## Required contents

1. The family name and one sentence that describes the design.
2. A specimen image. Store it in `documentation/readme-images`.
3. The supported scripts and the axes of the variable font.
4. The license, with a link to `OFL.txt`.
5. Build instructions that work from a fresh clone.
6. How to report a problem or contribute.

## Template

````markdown
# [Family Name]

[One sentence on the design: style, intended use, scripts.]

![Specimen](documentation/readme-images/specimen.png)

## Coverage

- Scripts: [Latin, Arabic, Hebrew]
- Axes: [Weight 400 to 700]
- Styles: [Regular, Medium, Bold]

## Build

```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
make build
```

The compiled fonts are written to `fonts/`.

## Checks

```
make qa
```

Runs fontspector against the compiled fonts.

## Contributing

Open an issue to report a problem. Open a pull request against `main`
for a change. See `CONTRIBUTORS.txt`.

## License

This Font Software is licensed under the SIL Open Font License,
Version 1.1. See [OFL.txt](OFL.txt).
````
