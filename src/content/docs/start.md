---
title: New font project
section: sources
order: 105
summary: The procedure to start a source repository from the project template, manually or with a coding agent and a specimen image.
introduction: "A new font starts from the <a href=\"https://github.com/fontgarden/font-project-template\">Font.Garden project template</a>. The template is a source repository with the Font.Garden tools, the checks and the instructions for agents. It contains a font with two glyphs. Use this chapter first for a new project."
background: [tools]
next: [specimen, sources]
---

## Manual start

1. Create a repository from the template with "Use this template" on GitHub, or clone it into a new folder.
2. Install the tools and name the family:

   ```
   make setup
   make customize FAMILY="My Face" DESIGNER="Your Name" EMAIL=you@example.com
   ```

3. Review the staged changes with `git diff --staged`, then commit.
4. Add glyphs. Draw them in the UFO, or trace them from a specimen image.

`make customize` replaces the placeholder family name, designer and repository URL in the sources, the documents and the file names. Run it once, before the first glyph.

## Start from a specimen image with an agent

Give a coding agent (Claude Code, Codex or OMP) the image and this request. Replace the words in capital letters.

> Create a font project from https://github.com/fontgarden/font-project-template
> for the specimen image at PATH. The family name is NAME, the designer is
> DESIGNER (EMAIL). The specimen is from ORIGIN. Clone the template into a new
> local folder, run `make setup` and `make customize`, then do the task in
> `.agents/tasks/specimen-intake.md`. Do not push or publish.

The agent needs `img2glyph`, `img2bez` and `img2ufo` on `PATH`. See [Tools and installation](/docs/tools/).

The result is a project with one purple draft for each glyph of the specimen, a built font and a QA report. The designer then grades the drafts. See [Drafts from a specimen image](/docs/specimen/).

## Facts from the designer

Only the designer can give these facts:

- the family name. A traced font does not get the name of the original typeface.
- the origin of the specimen, and that the design is free to use.
- the design decisions: which specimen, the metric targets and the style.

## Contents of the template

| part | content |
| --- | --- |
| `CONTEXT.md` | the design rules of the style and the values that the tools check |
| `sources/` | a starter UFO, `config.yaml` and `held-out-glyphs.toml` |
| `Makefile` | the commands, each of which calls `fgtools` |
| `AGENTS.md`, `.agents/` | the way of work for coding agents, and the task contracts |
| `documentation/` | the Google Fonts release document |
| `.github/workflows/` | the CI build, which runs `make test` |

## Work after the start

The work loop is the same for every project: choose glyphs, draft, check, compare builds, review, grade and learn from the corrections. See [Proposals and grading](/docs/proposals/) and [Corrections and drafting evaluation](/docs/learning/).
