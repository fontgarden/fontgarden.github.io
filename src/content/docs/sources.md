---
title: Source repository structure
section: sources
order: 120
summary: The mandatory layout of a source repository in the collection.
introduction: "Each source repository in the collection has the same layout. As a result, the build, the checks and the corpus builder find the sources without a configuration for each repository. A new repository starts from the <a href=\"https://github.com/fontgarden/font-project-template\">project template</a>. The reference project is <a href=\"https://github.com/eliheuer/virtua-grotesk\">Virtua Grotesk</a>."
background: [hosting, start]
next: [licenses, grid]
---

## Layout

```
├── AGENTS.md
├── AUTHORS.txt
├── CONTRIBUTORS.txt
├── OFL.txt
├── README.md
├── CONTEXT.md
├── STATUS.md
├── WORKLOG.md
├── Makefile
├── requirements.in
├── requirements.txt
├── .mcp.json
├── .agents
│   └── tasks
├── documentation
│   ├── google-fonts.md
│   └── media
│       └── brand.toml
├── fonts
│   ├── ttf
│   └── variable
├── sources
│   ├── Style.designspace
│   ├── Style-Regular.ufo
│   ├── Style-Bold.ufo
│   ├── config.yaml
│   ├── held-out-glyphs.toml
│   └── specimen
```

The layout is the layout of the Google Fonts project template, with the Font.Garden files. The tools are not in the repository. They are in [fgtools](https://github.com/fontgarden/fgtools). A Python file in `sources/` holds only the code of one font.

## sources

| path | content |
| --- | --- |
| `Style-Master.ufo` | One UFO for each master. |
| `Style.designspace` | The masters, the axes and the named instances. A project with one master has no designspace. |
| `config.yaml` | The recipe of the gftools builder. A project is a directory that contains this file. |
| `held-out-glyphs.toml` | The cases of the drafting evaluation. |
| `proof-samples.toml` | Optional. Text samples for the web proof and for the proof view and the Proof section of Runebender. |
| `specimen/` | Optional. The specimen image and `labels.json`, for a font traced from a specimen. |

Only drawn `<source>` masters are training data. Instances are not. Generated files go to `output/`, which Git ignores.

Files that people edit use TOML with comments. JSON is only for data that a program writes. `config.yaml` is YAML because gftools requires it.

## CONTEXT.md

`CONTEXT.md` is the one design file of a project. It starts with a description of the font, a table of contents and the chapter "The idea". That chapter gives the purpose and the precedents of the design. Text about the design in a README, a specimen or an article comes from there. The chapters after that hold the numbered design rules of the style. Below a rule, a `toml` code block holds the values that the tools check for that rule:

````markdown
R1. Every point is on the 2-unit grid. Structural points are on the 8-unit grid.

```toml
[grid]
source = 2
machine_draft = 8
```
````

- Agents and people read the whole file. Runebender gives it to its agents.
- `fgtools` reads only the `toml` blocks, as one TOML document: the grid, the stroke targets, the weights, the mark colors, the reference fonts, the QA exclusions and the start date of the corrections list.
- A design value is stated only in this file.

## documentation

`documentation/google-fonts.md` is the one document of the release: the project facts, the QA, the package and, for a traced font, the origin of the specimen. The folder also holds the Google Fonts article and, in `media/`, the brand and the formats of the marketing media. See [Proofs and media](/docs/media/). A project has no other documents. The design is in `CONTEXT.md`, and the work procedure is in `AGENTS.md`.

## Agent files

`AGENTS.md` gives the rules for coding agents, as short bullets. `.mcp.json` starts the MCP server of Runebender for an agent. `WORKLOG.md` is the record of work for all agents. `.agents/tasks/` holds task contracts for long and unattended tasks. Each contract gives a goal, acceptance checks, constraints and the form of the report.

## Excluded files

The repository holds sources, tests and maintained documents. It does not hold records of work.

- No handoffs, receipts, reports, plans, audits or dated documents. `WORKLOG.md` is the one record of work, with short entries and the newest entry first. Each agent reads it at the start of work and adds an entry at the end.
- A tracked file has at most 500 KB. A specimen scan in `sources/specimen/` can be larger.

`fgtools check-repository` enforces these rules, and `make test` runs it in CI. Each tracked file must have a place in the layout, which is the same for every Font.Garden project and is in fgtools. The command also fails when a document names a file or a `make` target that does not exist. When a document has a chapter `## Contents`, the command fails when that chapter and the `##` chapters of the document differ. A Python file in `sources/` is optional. It holds only the code of one font, for example the Fontspector checks of that font.

## Top-level files

- `README.md` states what the style is and gives the commands.
- `make status` writes `STATUS.md` from the mark colors.
- `OFL.txt`, `AUTHORS.txt`, `CONTRIBUTORS.txt`: see [Licenses](/docs/licenses/).
- `Makefile` is the entry point for every workflow. `make help` lists the targets. Each target calls `fgtools`.
- `requirements.txt` pins every Python dependency, with fgtools pinned to a commit.
