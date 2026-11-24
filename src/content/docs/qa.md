---
title: Quality assurance
section: production
order: 320
summary: The checks and the proofs of the sources and of each build.
introduction: "Each style has four types of review: checks of the sources, checks of the compiled fonts with Fontspector, a comparison of builds with diffenator3, and proofs that a person reads. An automatic check does not find an incorrect shape, so a person examines each proof."
background: [build, grades]
next: [learning, dataset]
---

## Checks of the sources

These commands read the UFO masters. They do not need a build.

| command | use |
| --- | --- |
| `make check-design GLYPHS="n a"` | Compares glyphs with the grid and the stroke targets in `CONTEXT.md`, and their color in text with the reference fonts. |
| `make check-changes` | Compares the sources with `main`. It fails when a green glyph changed, or when a glyph with changed contours is not purple. |
| `fgtools check-accents` | Lists the accented letters whose mark is not where the other accented letters predict, or not where the anchors of its parts are. |
| `fgtools render-accent-proofs` | Draws each accented letter beside the reference fonts and measures it against them. |
| `fgtools lint-glifs`, `fgtools lint-curves` | Finds structural faults in the GLIF files, differences between the masters and faults of the curves. |
| `make test` | Builds, then runs `fgtools check-repository` and the Fontspector checks. |

The design checks are a filter. They do not measure quality. On 2026-11-10 they passed 50 of the 72 glyphs that are green in both masters of Virtua Grotesk. Thus a finding is a reason to look, not an error.

## Accented letters

An accented letter is a composite of a base letter and a mark. `fgtools check-accents` fits one anchor for each base and one for each mark to all accented letters of a master, with medians. It lists each letter whose mark is not at the fitted position. It also lists each letter whose mark is not at the `top` or `bottom` anchors of its parts.

`fgtools evaluate-accent-placement` measures the method on compiled fonts, where the positions of the designer are known. On the 9 families of the reference fonts, 2162 marks, on 2026-11-14:

| method | top marks within 0.8% of the em |
| --- | --- |
| from the outlines only | 33% |
| outlines, with the constant of each mark from the other letters | 67% |
| from the anchors that the other accented letters imply | 99% |

The third method needs another mark on the same base and another base with the same mark. It predicts 86% of the marks. Bottom marks are harder: an ogonek joins a stroke and is not centered.

A listed letter is a reason to look. A mark on the stem of L is correct, and is not where the centered marks predict.

### Build the accented letters

Two commands write the accented letters, and both change nothing without `--write`:

1. `fgtools place-anchors` adds the `top`, `bottom`, `_top` and `_bottom` anchors that are missing. An anchor that is in the sources does not change. Green glyphs are left out without `--include-green`.
2. `fgtools build-accented-letters` adds each accented letter of a set that is not in the sources. Each new letter is a purple composite at the offset that the anchors give, in each master. The default set is the 145 accented letters of the Google Fonts Latin Core glyph set. The command lists the letters that it does not build: a letter with two marks, the caron of d, t, l and L, and the comma accent of g.

A trial on Virtua Grotesk on 2026-11-15 removed all 145 accented letters from a copy of both masters and built them again. With the anchors of the designer in place, 96% of the composites were within 8 units of the position of the designer. With the anchors also removed, 60% were within 8 units and 80% within 20 units.

### Review the accented letters

`fgtools render-accent-proofs` draws one row for each accented letter. The first column is the project. The other columns are the same character in each family of the reference fonts, at the weight of the master and at one x-height or cap height. It writes the sheets and `review.json` to `output/accent-proofs/`. Two numbers describe a mark: its `position` (the center of the mark as a share of the width of the base letter) and its `gap` (the distance from the base letter as a share of the x-height). A letter gets a finding when a number is outside the range of the reference fonts by more than 0.04, or when `check-accents` lists it. The letters with findings are on the first sheets.

Then an agent that can read images compares each letter with the accent rules of `CONTEXT.md`, as the task contract `accented-letters` describes. It gives each letter a verdict: `correct`, `fault` or `designer`. The agent corrects a purple letter with a fault and reports the others. The task contract is `.agents/tasks/accented-letters.md` of the project. A verdict is not approval: the designer grades the letters.

## Fontspector

[Fontspector](https://github.com/fonttools/fontspector) runs checks on the compiled fonts. It replaced Fontbakery. The collection uses the Font.Garden profile, which includes the Google Fonts profile and adds 12 checks:

| check | requirement |
| --- | --- |
| `fontgarden/unitsperem` | The em is 1024 units. |
| `fontgarden/grid` | Every master of a variable font has its on-curve points and advance widths on the 2-unit grid. |
| `fontgarden/license` | The font has the SIL Open Font License 1.1. |
| `fontgarden/vendor_id` | The vendor ID is `FTGD`. |
| `fontgarden/visible_ink` | Every visible character has ink at every weight. |
| `fontgarden/mark_glyphs` | Combining marks have the mark class and an advance of 0. |
| `fontgarden/marks_attach` | Combining marks attach to their bases. |
| `fontgarden/stacked_marks` | Two marks above a letter keep 16 units between them. |
| `fontgarden/arabic_joins` | Arabic joining forms meet the kashida without a gap. |
| `fontgarden/hebrew_marks_clear` | Hebrew accents and meteg clear the vowel point. |
| `fontgarden/precomposed_match` | A precomposed letter has the same ink as its base and mark sequence. |
| `fontgarden/static_stat_weight` | A static font names its own weight in the STAT table. |

A check that only one font needs is in that font's repository, in `sources/fontspector_checks.py`. It is written as the checks of the profile are, and `fgtools qa` runs it with them, in the section "This font". Virtua Grotesk has five:

- Modern Hebrew is covered.
- The `a` uses one glyph at every weight.
- The `a` keeps both waist shelves and the foot flat.
- The stacked feh keeps the counter of its donor.
- Arabic vowels clear the signs that distinguish letters.

Each repository has three targets for the checks:

- `make test` runs every check: the repository check, the Google Fonts checks, the Font.Garden checks and the checks of the font. Some Google Fonts checks need the internet. CI runs it on each push.
- `make test-google-fonts` runs the Google Fonts checks only.
- `make test-fontgarden` runs the Font.Garden checks and the checks of the font only.

All three leave out the known faults in `[qa.exclude]` of `CONTEXT.md`, each with its reason, so that a FAIL is a new fault. The fonts are ready for release when the list is empty. Do not add a check to the list to hide a new fault. With `NO_BUILD=1`, a target uses the fonts in `fonts/` and does not build them first. `fgtools qa --package <directory>` runs every check, with no exclusions, on an assembled google/fonts package. Reports go to `output/qa/`. A FAIL gives a failing exit status. A WARN needs review.

Four of the checks are also in a Rust plugin for Fontspector, [fontspector-fontgarden](https://github.com/fontgarden/fontspector-fontgarden): the em, the grid, the license and the vendor ID. The plugin has no release yet.

## Comparison of builds

`make diff` compares the build of the working tree with the build of `main`. See [Font build](/docs/build/). An agent runs it after each source edit and reports each change that the edit does not explain.

## Proofs

`make proof` builds the fonts and writes the print proof to `output/proof/proof.pdf`. The proof has these pages:

- the facts of the font
- the character set
- the scale of sizes
- text at 8 and 16 points
- spacing strings
- kerning pairs and figures
- diacritics
- the weight axis
- the short lines of `sources/proof-samples.toml`
- the joining forms and the marks of the Arabic script

Each script and each master has its pages, and a font shows only the pages that it has the glyphs for. The command is `fgtools media --proof`. It uses the layout system of [Proofs and media](/docs/media/). Print the proof to judge the color of the text.

fgtools and the project template are behind Virtua Grotesk for this command. Virtua Grotesk has `make proofs`, from its own `sources/proof_review.py`. That command writes a Print Proof and a Full Proof to `output/proof/`, each also with the red grid. The command is not in fgtools at this time.

`make proof-web` builds the fonts and serves them beside the fonts in `reference-fonts/`, in a browser, at one em size and weight. It has four modes: Compare, Toggle between two builds, Waterfall, and Text. If a reference font does not have a glyph, the proof shows the missing code points. It does not use a fallback font.

The samples are live browser text for Latin, Hebrew and Arabic. `sources/proof-samples.toml` adds samples for a project. Runebender reads the same file. Its proof view and the Proof section of its right panel show the samples for the script of the current glyph. Runebender draws them from the current outline during an edit. In Runebender, a sample text can contain `{glyph}`, which is the current glyph. The web proof shows `{glyph}` as text. Browser rendering is not release QA.

## Connected scripts

Arabic and Hebrew need real shaping for a review. Render test lines with a shaping engine, not with a glyph viewer. Keep a reference renderer built on HarfBuzz and FreeType beside the renderer of the project. Then a fault of the font can be told from a fault of the renderer.

## After a source edit

1. Run `make check-changes` and `make check-design` for the edited glyphs.
2. Run `make build`.
3. Run `make diff`.
4. Look at the rendered glyphs in words, beside the reference fonts.

Command success is not visual review. The designer gives the verdict on drawings.
