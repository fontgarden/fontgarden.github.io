---
title: Proposals and grading
section: system
order: 240
summary: The rules for the work of a model, an agent and the designer on one glyph.
introduction: Each output of a model or an agent is a draft. A draft is purple, and it gets a commit before the designer edits it. The designer reviews, corrects and grades the draft. Only the designer approves a contour glyph. This chapter gives the rules and the work sequence.
background: [grades]
next: [learning, build, dataset]
---

## Rules

1. A model or an agent drafts only the glyphs that the designer names, in the masters that the designer names.
2. A draft is a Runebender proposal, or a glyph in the source with a purple mark.
3. Commit the draft before the designer edits it. The Git history then holds the two versions.
4. The designer corrects the draft on the 2-unit grid and grades it: red, orange, yellow or green.
5. A green contour glyph is frozen. A change to a component donor also changes each glyph that uses it. Thus the donor of a green glyph is also frozen.

A request to clean a glyph is a request for the smallest change to the current drawing. Usually that change is an edit of the handles. It is not a new design.

## Work sequence of an agent

1. `make queue` lists the glyphs in sequence, with the glyph that most composites need first. The designer names the glyphs.
2. The agent drafts the glyphs, runs `make check-design` for them and corrects the results.
3. The agent runs `make check-changes` and `make diff`. It reports each changed glyph, word or table that the edit does not explain.
4. The agent renders the same text in the font and in the reference fonts, with Runebender or `make proof-web`.
5. The designer reviews and grades.
6. When the designer asks, the agent runs `fgtools corrections` and proposes a change for each open correction. See [Corrections and drafting evaluation](/docs/learning/).

The reference fonts do not control the design. Use them to compare visual weight, the distances between letters and the consistency of the outlines.

## Source edits by an agent

- Edit GLIF XML and plists in the style of the existing files. Do not save a full UFO with a font library, because that operation writes each file again.
- Add a new glyph to `contents.plist` and to `public.glyphOrder` of each master.
- Keep the contours, points and components compatible in each master.

## Task contracts

A long task without supervision has a contract in `.agents/tasks/`. The contract gives the goal, the acceptance checks, the constraints and the form of the report. Run a contract in a different checkout, on its own branch. The template has three contracts: specimen intake, glyph drafts and accented letters.

## Proposals in Runebender

- **Bolden** moves the points of the base master to draft the heavier master, in batches of 20 glyphs.
- **Draft with Virtua** draws a brush sketch again with the conventions of the collection. It uses the green glyphs of the source as references.
- **Trace Image** runs img2bez on a raster image and gives the result as a proposal.
- **The Graph** is a node editor with Font, Model, Master, Bolden, Compare and Install nodes.

The designer installs or discards each proposal. A coding agent with an MCP connection can read a glyph, measure it, render a proof and propose an edit.

The Weight debt block of Runebender gives each installed draft the purple mark. In Runebender, only green glyphs are frozen references. Red is the only grade that permits the replacement of a full outline.

## Commit of a draft before the grade

The difference between a purple draft and the outline of the designer shows the location and the size of the error of the method. This record exists only when the draft has a commit before the review starts. `fgtools corrections` reads the two commits.

## Stages of automation

A tool gets more automation in stages:

1. A new operation gives suggestions only.
2. The project measures the acceptance rate of the operation in graded sessions.
3. When the acceptance rate of a category stays above approximately 90 percent, the tool can apply that category automatically.

An automatic result is still purple, and the designer still grades it.
