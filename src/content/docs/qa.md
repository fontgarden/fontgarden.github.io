---
title: Quality assurance
section: production
label: learn
order: 320
summary: The checks and proofs that run on the sources and on every build.
callout: Four kinds of review run on every style. Checks of the sources, checks of the compiled fonts with Fontspector, a comparison of builds with diffenator3, and proofs that a person reads. Automated checks do not see a wrong shape, so a person looks at every proof.
background: [build, grades]
next: [learning, dataset]
---

## Checks of the sources

These commands read the UFO masters. They do not need a build.

| command | use |
| --- | --- |
| `make check-design GLYPHS="n a"` | Compares glyphs with the grid and the stroke targets in `context.md`. |
| `make check-changes` | Compares the sources with `main`. It fails when a green glyph changed, or when a glyph with changed contours is not purple. |
| `make check-accents` | Lists the accented letters whose mark is not where the other accented letters predict, or not where the anchors of its parts are. |
| `make accent-proofs` | Draws each accented letter beside the reference fonts and measures it against them. |
| `make lint` | Finds structural faults in the GLIF files, differences between the masters and faults of the curves. |
| `make test` | Checks the repository layout and the references in the documents. |

The design checks are a filter. They do not measure quality. On 2026-11-10 they passed 50 of the 72 glyphs that are green in both masters of Virtua Grotesk. Thus a finding is a reason to look, not an error.

## Accented letters

An accented letter is a composite of a base letter and a mark. `fgtools check-accents` fits one anchor for each base and one for each mark to all accented letters of a master, with medians. It lists each letter whose mark is not at the fitted position, and each letter whose mark is not where the `top` or `bottom` anchors of its parts are.

`fgtools evaluate-accent-placement` measures the method on compiled fonts, where the positions of the designer are known. On the 9 families of the reference fonts, 2162 marks, on 2026-11-14:

| method | top marks within 0.8% of the em |
| --- | ---: |
| from the outlines only | 33% |
| outlines, with the constant of each mark from the other letters | 67% |
| from the anchors that the other accented letters imply | 99% |

The third method needs another mark on the same base and another base with the same mark. It predicts 86% of the marks. Bottom marks are harder: an ogonek joins a stroke and is not centered.

A listed letter is a reason to look. A mark on the stem of L is correct, and is not where the centered marks predict.

### Build the accented letters

Two commands write the accented letters, and both change nothing without `--write`:

1. `fgtools place-anchors` adds the `top`, `bottom`, `_top` and `_bottom` anchors that are missing. An anchor that is in the sources does not change. Green glyphs are left out without `--include-green`.
2. `fgtools build-accented-letters` adds each accented letter of a set that is not in the sources, as a purple composite at the offset that the anchors give, in every master. The default set is the 145 accented letters of the Google Fonts Latin Core glyph set. The command lists the letters that it does not build: a letter with two marks, the caron of d, t, l and L, and the comma accent of g.

A trial on Virtua Grotesk on 2026-11-15 removed all 145 accented letters from a copy of both masters and built them again. With the anchors of the designer in place, 96% of the composites were within 8 units of the position of the designer. With the anchors also removed, 60% were within 8 units and 80% within 20 units.

### Review the accented letters

`make accent-proofs` draws one row for each accented letter: the project in the first column, then the same character in each family of the reference fonts, at the weight of the master and at one x-height or cap height. It writes the sheets and `review.json` to `out/accent-proofs/`. Two numbers describe a mark: its `position` (the center of the mark as a share of the width of the base letter) and its `gap` (the distance from the base letter as a share of the x-height). A letter gets a finding when a number is outside the range of the reference fonts by more than 0.04, or when `check-accents` lists it. The letters with findings are on the first sheets.

An agent that can read images then reviews every letter with the skill `accent-review`, and gives each one a verdict: `correct`, `fault` or `designer`. The agent corrects a purple letter with a fault and reports the others. The task contract is `.agents/tasks/accented-letters.md` of the project. A verdict is not approval: the designer grades the letters.

## Fontspector

[Fontspector](https://github.com/fonttools/fontspector) runs checks on the compiled fonts. It replaced Fontbakery. The collection uses the Font.Garden profile, which includes the Google Fonts profile and adds four requirements:

| check | requirement |
| --- | --- |
| `fontgarden/unitsperem` | The em is 1024 units. |
| `fontgarden/grid` | Every master of a variable font has its on-curve points and advance widths on the 2-unit grid. |
| `fontgarden/license` | The font has the SIL Open Font License 1.1. |
| `opentype/vendor_id` | The vendor ID is `FTGD`. |

Each repository provides three targets:

- `make qa` works offline. It leaves out the checks in `[qa.exclude]` of `context.md`. Each exclusion has a reason.
- `make qa-full` runs all checks, with the network checks. A style must pass this before a release.
- `make qa-package PACKAGE=<directory>` checks an assembled google/fonts package.

An exclusion is known development debt. Do not add an exclusion to hide a new failure. Reports go to `out/qa/`. A FAIL gives a failing exit status. A WARN needs review.

The profile is also a Rust plugin for Fontspector: [fontspector-fontgarden](https://github.com/fontgarden/fontspector-fontgarden). It has no release yet.

## Comparison of builds

`make diff` compares the build of the working tree with the build of `main`. See [Build the fonts](/docs/build/). An agent runs it after each source edit and reports each change that the edit does not explain.

## Proofs

`make proof-web` builds the fonts and serves them beside the fonts in `reference-fonts/`, in a browser, at one em size and weight. It has four modes: Compare, Toggle between two builds, Waterfall, and Text. If a reference font does not have a glyph, the proof shows the missing code points. It does not use a fallback font.

The samples are live browser text for Latin, Hebrew and Arabic. `sources/proof-samples.toml` adds samples for a project. Runebender reads the same file: its proof view and the Proof section of the right panel offer the samples of the script of the current glyph, drawn from the live outline while you edit. In Runebender, a sample text can contain `{glyph}`, the current glyph; the web proof shows it as written. Browser rendering is not release QA.

## Connected scripts

Arabic and Hebrew need real shaping for a review. Render test lines with a shaping engine, not with a glyph viewer. Keep a reference renderer built on HarfBuzz and FreeType beside the renderer of the project. Then a fault of the font can be told from a fault of the renderer.

## After a source edit

1. Run `make check-changes` and `make check-design` for the edited glyphs.
2. Run `make build`.
3. Run `make diff`.
4. Look at the rendered glyphs in words, beside the reference fonts.

Command success is not visual review. The designer gives the verdict on drawings.
