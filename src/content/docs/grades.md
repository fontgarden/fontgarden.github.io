---
title: Glyph grades
section: system
label: must
order: 230
summary: The mark color of each glyph, which records its state and whether it can train a model.
callout: Quality is tracked for each glyph, not for each font. Each glyph in a UFO has a mark color, the same color that Runebender shows in the glyph grid. Purple is a draft that the designer has not reviewed. Red, orange and yellow are the designer's grades. Green is approved. The tools and the reports read the color.
background: [grid, structure]
next: [proposals, learning, dataset]
---

## The grades

| color | meaning | trains |
| --- | --- | --- |
| purple | A draft by a model, an agent or the tracer. The designer has not reviewed it. | no |
| red | Broken. The glyph can be replaced. | no |
| orange | Better, but not good enough. Edit it and keep the useful construction. | no |
| yellow | Close. Edit it without a new drawing. A glyph can stay yellow for a long time. | no |
| green | Approved as close to final. The contours are frozen. | yes |

Two more colors mark composites in Virtua Grotesk. Blue is a composite that needs diagnosis. Pink is a composite that needs small edits. Neither is a reference.

A source has mixed quality. A grade for the whole font would hide this, so there is none.

## Who sets what

- The designer grades contour glyphs. Only the designer moves a contour glyph to red, orange, yellow or green.
- A tool or an agent that draws or traces a glyph marks it purple.
- An agent can mark a composite green when all its parts are green and `fgtools check-design --ready` lists it.
- An agent does not change the contours of a green glyph, and does not change a component donor that a green glyph uses.

`fgtools check-changes` enforces these rules on a set of source changes. It fails when a green glyph changed, or when a glyph with changed contours is not purple.

## Only green trains

Training data comes from green glyphs only. If drafts trained the next model, the model would learn its own errors. Only green glyphs are references for a new drawing.

## Where the grade is stored

The grade is the UFO `public.markColor` key in the `lib` of each glyph. Runebender reads and writes it. The reference values:

| color | markColor |
| --- | --- |
| green | `0,1,0,1` |
| yellow | `1,1,0,1` |
| orange | `1,0.5,0,1` |
| red | `1,0,0,1` |
| purple | `0.54,0.44,0.88,1` |

`CONTEXT.md` of each project lists every value that its sources use for a color, with the policy of the color. The tools read the colors from that file.

## Reports

`make status` writes `STATUS.md`, a count of glyphs for each color, master and script. The number of green glyphs is the measure of progress. The release target is every glyph green in every master.

`fgtools corrections` lists the reviews of purple drafts from the Git history. See [Corrections and drafting evaluation](/docs/learning/).

## Bold debt

A heavier master that is not complete usually holds copies of the outlines of the base master. These copies are red. An early Virtua corpus contained a Bold master in which 37 percent of the glyphs were such copies. As a result, a third of the pair training taught the model that a Bold is the same as a Regular. A plain baseline found the fault. The loss curve did not. The corpus builder now also drops a pair whose mean point movement is less than 8 units.
