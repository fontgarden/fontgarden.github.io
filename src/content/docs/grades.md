---
title: Glyph grades
section: system
label: must
order: 220
summary: The four-color grade that every glyph carries, and what each color permits.
callout: Quality is tracked per glyph, not per font. Each glyph in a UFO carries a mark color in its <code>lib.plist</code>, the same color Runebender shows in the glyph grid. The color is the grade. The corpus tools, the review tools and the build reports all read it.
background: [grid]
next: [outlines, dataset]
---

## The four grades

| color | meaning | use in training |
| --- | --- | --- |
| green | Finished and approved by a human. The only gold standard. | yes |
| yellow | Close to finished. Reviewed, with a known remaining issue. | by decision, logged per experiment |
| orange | Better than nothing. A machine draft or an untouched trace. | never |
| red | Empty, placeholder, or wrong. | never |

A source has mixed quality. A whole-font grade would hide this, so there is none.

## Who sets the grade

- A human sets green. A tool may never promote a glyph to green.
- A tool that drafts a glyph sets orange on what it wrote.
- A human reviewing a draft moves it to yellow or green, or leaves it orange with a note.
- Imported masters from released OFL fonts enter as yellow. They are trusted as designer work but not graded by us.

## Where the grade lives

The UFO `public.markColor` key in each glyph's `lib`. Runebender reads and writes it. Scripts read it with any UFO library. The reference values:

| color | markColor |
| --- | --- |
| green | `0,1,0,1` |
| yellow | `1,1,0,1` |
| orange | `1,0.5,0,1` |
| red | `1,0,0,1` |

Projects may use nearby values. The corpus tools classify by hue, not by exact match.

## Reports

`make scoreboard` writes `documentation/scoreboard.md`, a count of glyphs per color per master. The number of green glyphs is the measure of a family's progress. A family can enter the catalog with yellow glyphs. It cannot enter with orange or red glyphs in its declared character set.

## Debt

An unfinished second master often holds copies of the first master's outlines that have not yet been changed. These are red. Marking them honestly matters: a corpus built from a Bold master with unbolded copies teaches the model that bolding changes nothing. This defect was found in an early Virtua Grotesk corpus and is the reason the grade system exists.
