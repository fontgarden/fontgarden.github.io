---
title: Corrections and drafting evaluation
section: system
order: 250
summary: The procedure that makes a system change from each correction, and the evaluation of drafting methods.
introduction: "The corrections of the designer must improve the system. The record of a correction is the Git history and not a file. Each correction becomes a rule, a check, a test case or a glyph record. A fixed evaluation compares drafting methods with approved drawings, so the scores of different dates are comparable."
background: [grades, proposals]
next: [qa, dataset]
---

## Work sequence

1. **Choose.** `make queue` ranks the glyphs that most composites wait on. The designer names the glyphs.
2. **Draft.** An agent or a model drafts the glyph, with a purple mark. Where an edit is a calculation, the agent uses `fgtools edit`, which calculates the points. When the designer gives a picture of another font as an example, the agent first measures it with `fgtools measure-picture` and draws to the ratios. The draft is committed before the designer edits it.
3. **Look and measure.** `fgtools render` draws the glyph large: the change, the filled glyph, its points, the donors and the reference fonts. Below the glyph, it shows the glyph in a block of text, sharp and blurred, adjacent to the same block in a reference font. In the blurred block, a glyph that is too heavy is a dark area. The agent reads this picture before and after every edit. `make check-design` compares the draft with the targets in `CONTEXT.md`. A pass removes clear faults. It is not an approval.
4. **Second review.** A second agent gets only the picture, `CONTEXT.md` and the glyph names. It gives each glyph the verdict `pass`, or `fault` with the rule number. The first agent corrects the faults before the designer sees the draft.
5. **Review.** The designer compares the glyph with the reference fonts, then grades it. The review commit changes the purple mark to red, orange, yellow or green.
6. **Learn.** `fgtools corrections` lists the open corrections. Each one becomes a change to the system.

## Git history as the record

The draft commit and the review commit are the record of a decision. Do not copy drafts or corrections into files. Do not add reports. `WORKLOG.md` holds short entries about the work. It does not hold drafts or corrections.

`fgtools corrections` reads the history. It finds each review of a purple draft and compares the draft with the first green version of the glyph. Until the glyph is green, it uses the latest version that is not purple. If the two differ, the review is a correction.

A correction is open until a tracked file or a later commit message cites the hash of its review commit. `[corrections] start` in `CONTEXT.md` gives the first date that the list includes.

## Changes from a correction

| the correction shows | change |
| --- | --- |
| a mistake that a script can find | a value in `CONTEXT.md`, or a check in the tools |
| a mistake that repeats | a rule entry in the design documents |
| a decision that a drafting method has to learn | a case in `sources/held-out-glyphs.toml` |
| a fault of one glyph only | one line in the record of the glyph |

The designer approves or rejects each change. One correction is not a rule. When the same mistake occurs again, add the glyph and the commit to the existing entry.

## Measures of improvement

The summary of `fgtools corrections` gives these numbers for each month:

- the grades that the designer gave
- the drafts that reached green without a change
- the drafts that the designer corrected
- the mean overlap of the drafts with the version of the designer

When the system improves, the grades become better, more drafts get green without a change and the overlap increases.

## Drafting evaluation

`fgtools evaluate-drafting` tests a drafting method (an agent, a model or a script) on green glyphs that the method has not seen. The glyphs are in `sources/held-out-glyphs.toml`, in four tasks:

| task | the method gets | the method must |
| --- | --- | --- |
| redraw | the sources without the glyph | draw the glyph in every master |
| bold | the green Regular, without the Bold | draw the Bold |
| repair | the glyph with some points moved | move the points back |
| relatives | green glyphs of the same construction | draw the glyph from them |

1. `fgtools evaluate-drafting prepare TASK RUN` copies the sources to `RUN/sources`, sets the task and writes the brief `TASK.md`.
2. The method edits only `RUN/sources`. If a method reads the project sources or the Git history, its score is not valid.
3. `fgtools evaluate-drafting score RUN` gives the overlap with the approved drawing, the distance from it, the master compatibility and the grid result.
4. `fgtools evaluate-drafting compare RUN RUN` compares two runs of one task.

A method is useful only if its score is better than the baselines. In Virtua Grotesk on 2026-11-12, a Regular copied into the Bold scored a mean overlap of 0.585. The moved glyphs of the repair task, without a repair, scored 0.962.

## Agent harnesses

`fgtools evaluate-drafting run TASK RUN --harness NAME` prepares a run and starts a coding agent in it without a person. It records the time, the exit status and the cost, and it scores the result. `fgtools evaluate-drafting table RUN ...` prints one line for each run.

The harnesses are Claude Code, Codex and OMP. Each harness runs with its permission checks on. The agent can edit files in the run folder and run `fgtools`, and nothing else. A test of the package fails if a harness turns the permission checks off.

## Limits

Evaluation scores and model scores do not approve a glyph. Keep the glyphs of one construction, and the masters of one glyph, on the same side of a division into training and evaluation data.
