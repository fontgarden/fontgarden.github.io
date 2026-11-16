---
title: Proposals and grading
section: system
label: must
order: 240
summary: How a model, an agent and a person share the work on a glyph.
callout: Every output of a model or an agent is a draft. A draft is marked purple and committed before the designer edits it. The designer reviews, corrects and grades. Only the designer approves a contour glyph. This chapter describes the rules and the work loop that they produce.
background: [grades]
next: [learning, build, dataset]
---

## The rules

1. A model or an agent drafts only the glyphs that the designer names, in the masters that the designer names.
2. A draft is a Runebender proposal, or a glyph in the source with a purple mark.
3. The draft is committed before the designer edits it, so that the Git history holds both versions.
4. The designer corrects the draft on the 2-unit grid and grades it: red, orange, yellow or green.
5. Green contour glyphs are frozen. A change to a component donor also changes every glyph that uses it, so a donor of a green glyph is frozen too.

A request to clean a glyph is the smallest change to the current drawing, usually an edit of the handles. It is not a new design.

## The work loop of an agent

1. `make queue` ranks the glyphs that most composites wait on. The designer names the glyphs.
2. The agent drafts, runs `make check-design` for the glyphs, and corrects the findings.
3. The agent runs `make check-changes` and `make diff`. It reports each changed glyph, word or table that the edit does not explain.
4. The agent renders the same text in the font and in the reference fonts, with Runebender or `make proof-web`.
5. The designer reviews and grades.
6. When the designer asks, the agent runs `fgtools corrections` and proposes a change for each open correction. See [Corrections and drafting evaluation](/docs/learning/).

The reference fonts do not dictate the design. Use them to compare visual weight, spacing and the consistency of the outlines.

## Source edits by an agent

- Edit GLIF XML and plists in the existing style. Do not save a whole UFO with a font library, because that rewrites every file.
- Register a new glyph in `contents.plist` and `public.glyphOrder` of every master.
- Keep the contours, points and components compatible in every master.

## Task contracts

Long and unattended tasks have a contract in `.agents/tasks/`: the goal, the acceptance checks, the constraints and the form of the report. Run a contract in a separate checkout, on its own branch. The template has three contracts: specimen intake, glyph drafts and the Google Fonts release.

## Proposals in Runebender

- **Bolden** moves the points of the base master to draft the heavier master, in batches of 20 glyphs.
- **Draft with Virtua** draws a brush sketch again in the conventions of the collection, with the green glyphs of the source as reference.
- **Trace Image** runs img2bez on a raster and places the result as a proposal.
- **The Graph** is a node editor with Font, Model, Master, Bolden, Compare and Install nodes.

The designer installs or discards each proposal. A coding agent connected through MCP can read a glyph, measure it, render a proof and propose an edit.

The Weight debt block of Runebender marks installed drafts purple. In the grading of Runebender, only green glyphs are frozen references, and red is the only grade that permits the replacement of a whole outline.

## Commit drafts before grading

The difference between a purple draft and the outline that the designer kept shows where the method was wrong and by how much. For that record to exist, the draft must be committed before the review starts. `fgtools corrections` reads these two commits.

## The trust ladder

A tool gets a larger role in steps. A new operation starts with suggestions. Its acceptance rate is measured over graded sessions. When acceptance in a category stays above about 90 percent, that category can be applied automatically. The result is still marked purple and still graded.
