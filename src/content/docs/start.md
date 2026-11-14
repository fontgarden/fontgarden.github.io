---
title: Start a font project
section: sources
label: templ
order: 105
summary: How to start a source repository from the project template, by hand or with a coding agent and a specimen image.
callout: A new font starts from the <a href="https://github.com/fontgarden/font-project-template">Font.Garden project template</a>. The template is a source repository in the Google Fonts layout, with the Font.Garden tools, QA and agent instructions. It holds a starter font with two glyphs. This chapter is the entry point for a new project.
background: [tools]
next: [specimen, sources]
---

## Start by hand

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

The agent needs `img2glyph`, `img2bez` and `img2ufo` on `PATH`. See [Setting up a working environment](/docs/tools/).

The result is a project with one purple draft for each glyph of the specimen, a built font and a QA report. The designer then grades the drafts. See [From a specimen image to drafts](/docs/specimen/).

## What the designer supplies

Only the designer can give these facts:

- the family name. A traced font does not get the name of the original typeface.
- the origin of the specimen, and that the design is free to use.
- the design decisions: which specimen, the metric targets and the style.

## What the template gives

| part | content |
| --- | --- |
| `sources/` | a starter UFO, `config.yaml`, `design.toml` and `held-out-glyphs.toml` |
| `Makefile` | the commands, each of which calls `fgtools` |
| `AGENTS.md`, `.agents/` | the rules, the skills and the task contracts for coding agents |
| `documentation/` | the build and QA guide, the learning loop and the Google Fonts release notes |
| `tests/`, `.github/workflows/` | the layout test, the reference test and the CI build |

## After the start

The work loop is the same for every project: choose glyphs, draft, check, compare builds, review, grade and learn from the corrections. See [Proposals and grading](/docs/proposals/) and [Corrections and drafting evaluation](/docs/learning/).
