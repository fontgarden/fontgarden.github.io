---
title: Proofs and media
section: production
label: learn
order: 330
summary: The print proof, the print specimen, the technical images and the marketing media of a font, and the one layout system that makes them.
callout: A project made from the template renders its proof, its specimen and its marketing media with three commands. Every picture is laid out on the lattice of the typeface, and a checker verifies each layout before DesignBot draws it. No rendered file is tracked in Git.
background: [build, qa]
next: [learning]
---

This chapter is a specification. The column State says what is built. Where it says "planned", the chapter is correct and the tool is not finished.

## The outputs

| Output | Reader | Command | State |
| --- | --- | --- | --- |
| Print proof | The designer, to find faults | `make proof`, which runs `fgtools media --proof` | Built, 10 kinds of page |
| Print specimen | A reader, on paper | `make specimen`, which runs `fgtools media --specimen` | Built |
| Marketing media | The public, on social platforms | `make media`, which runs `fgtools media` | Built, 9 formats |
| Technical images | A reader of a README or an article | The format `glyph` of the media | Built, 1 format |
| All of them | GitHub Pages | `make site`, which runs the three commands and then `fgtools site` | Built |

DesignBot draws all of them. A glyph looks the same in the proof, in the specimen and in a video.

## The layout system

A layout is not drawn by hand. It is placed on the lattice of the typeface, with the numbers of the `[layout]` block of `CONTEXT.md` of the project.

| Rule | Value in a font with an em of 1024 units |
| --- | --- |
| The module is the large step of the design grid | 64 pixels |
| Every position is a multiple of the unit | 8 pixels |
| The live area of a canvas is a whole number of modules; the margin is the rest | 1080 x 1350 has 16 x 20 modules |
| The text area is the live area less one module on each side, inside the safe area of the platform | 14 x 18 modules |
| Type sizes double | 32, 64, 128, 256, 512, 1024, and 24 for labels. The print page has one size more, 16 pixels, which is 8 points on paper. |
| The cap top of a line stands on a module line, and its start on a column line | |
| A text is chosen to fit its measure. The size never changes to make a text fit. | A word at 256 pixels fills 99% of the measure |
| One label size, one line weight, two inks and one accent | |

At an em of 1024 pixels, 1 pixel is 1 unit of the font. The grid of such a picture is the grid of the drawing.

### The parts

| Part | Place | Work |
| --- | --- | --- |
| Lattice | `fgtools/media_layout.py` | Gives each canvas its live area and its text area |
| Typesetter | `fgtools/media_layout.py` | Measures text in the font with HarfBuzz, fits a word to a measure, breaks a paragraph into lines |
| Format | `fgtools/media_formats/`, one Python file for each. The pages of the print proof are in its folder `proofs/`. | Places type, rules and paths on the lattice. It never names a pixel. |
| Checker | `fgtools/media_layout.py` | Finds a size that is not on the scale, a position off the unit, ink outside the text area, and more than two weights or three sizes in a picture |
| Plotter | `fgtools/media_plotter.rs` | DesignBot draws the checked layout. It decides nothing. |

A layout with a fault is not written. The command names each fault and stops with an error.

## Where each part is

| Part | Place | Changes for each font |
| --- | --- | --- |
| The layout system, the default formats, the canvases, the word lists | fgtools | No |
| The numbers of the lattice | `CONTEXT.md` of the project, the `[layout]` block | Yes |
| The brand: the colors and the texts | `documentation/media/brand.toml` | Yes |
| The caption, the alternative text and the canvases of a format | `documentation/media/formats.toml`, optional | Yes |
| The texts of the print proof | `sources/proof-samples.toml`, optional. The web proof uses the same file. | Yes |
| A layout that only this font has | A Python file in `documentation/media/images/`, `carousels/` or `videos/`, optional. The folder says what the format makes. | Yes |
| The rendered files | `output/media/` and `output/specimen/`, which Git ignores | Not tracked |

A new project has `brand.toml` only, and gets every default format. An improvement of a default format reaches every font with the next version of fgtools. To change a layout for one font, `fgtools media --copy` with the name of the format copies the default script into the project.

A font at the start of its design has few glyphs, and the formats use what it has. A text with a character that the font does not have is left out, and a font that can set no word shows the letters that exist. A picture never shows a system font.

## The canvases

| Canvas | Size | Text area in modules | Use |
| --- | --- | --- | --- |
| `portrait` | 1080 x 1350 | 14 x 18 | Feed image and carousel on Instagram, LinkedIn, X and Mastodon. The page of a LinkedIn document. |
| `vertical` | 1080 x 1920 | 11 x 14 | Instagram Reel and Story, and TikTok |
| `landscape` | 1920 x 1080 | 26 x 14 | Video and wide image on X, LinkedIn and Mastodon |
| `square` | 1080 x 1080 | 14 x 14 | A page or a profile that needs a square |
| `card` | 1200 x 630 | 16 x 6 | The link preview |
| `page` | 1684 x 1190, written at half size | 22 x 14 | The page of the print specimen: A4 landscape, dark ink on a light ground |

The platforms change their safe areas each year, so they are data in `fgtools/media_canvases.toml`. `fgtools media --lattice` draws the lattice and the text area on every picture.

## The formats

| Format | Kind | What it shows | State |
| --- | --- | --- | --- |
| `words` | Image | One word for each weight at 256 pixels. Each word fills the measure. | Built |
| `weights` | Image | One text at each weight, from the lightest to the heaviest | Built |
| `text` | Image | The line of the brand at 64 pixels and the description of the font at 32 pixels | Built |
| `scripts` | Image | One word in each script of the font | Built |
| `release` | Image | The name, and the facts of the font from the font file | Built |
| `link-card` | Image | The picture of a link | Built |
| `glyph` | Carousel | One glyph on the grid of its design, with the points of the drawing and the metrics | Built |
| `characters` | Carousel | The characters in cells of two modules, one group for each page | Built |
| `weight-axis` | Video | One text across the weight axis. A square moves on a line, a whole number of units in each frame. | Built |
| Features: the changed glyph in ink inside a gray word | Image | | Planned |
| Similar characters, for example I, l and 1 | Image | | Planned |
| Masters: the outlines of two masters with lines between matching points | Image or video | | Planned |
| Before and after: one glyph at two commits | Video | | Planned |

## The print proof

The print proof is for the designer. The shared fgtools generator uses the page formats below.

Virtua Grotesk adds a project-specific Print Proof for reading. Each named weight has one page per script. The upper half sets a passage without diacritics and the lower half repeats the same words with the same line breaks. Arabic uses vowel marks, Hebrew uses vowel points, and the Latin sample uses English words that can take accents, such as “café” and “résumé”. Read across the two sizes to check weight and down the page to check mark placement. The Full Proof opens with these pages and continues with detailed checks.

| Page | What it shows |
| --- | --- |
| Facts | The format `release` |
| Character set | Every encoded character, one in each module |
| Sizes | One line at 128, 64, 32, 16 and 8 points, for each script and each master |
| Reading | A text at 8 on 12 points and at 16 on 24 points, for each script and each master |
| Spacing | Each letter between two straight and two round control letters |
| Kerning and figures | Pairs, words, default and tabular figures |
| Diacritics | Each letter with a mark beside its base letter |
| Weights and interpolation | The format `weights`, and the glyphs of the brand at 11 steps of the axis |
| Lines | The short samples of fgtools and of the project |
| Arabic joining and Arabic marks | Each letter in its four forms, and each vowel mark on 12 letters |

A sample line that mixes a script from the left with a script from the right is left out: DesignBot sets a line in one direction.

The print specimen is the formats `release`, `text`, `words`, `weights`, `scripts`, `glyph` and `characters` on the `page` canvas, as one PDF.

## A part only

Each of the three commands makes all of its outputs, or the part that you name.

| Wanted | Command |
| --- | --- |
| The names of the formats, the canvases and the pages | `make formats` |
| Some pages of the print proof | `make proof PAGE="spacing kerning"` |
| Some pages of the print specimen | `make specimen PAGE=words` |
| One kind of media: `images`, `carousels` or `videos` | `make media FORMAT=videos` |
| Some formats | `make media FORMAT="words glyph"` |
| One format on one canvas | `make media FORMAT=weight-axis CANVAS=landscape` |
| The technical image | `make media FORMAT=glyph` |
| The pictures with the lattice drawn on them | `make media LATTICE=1` |
| A copy of a default format, to change it for this font | `make copy-format FORMAT=words` |

A part of the proof or of the specimen is written to the file of the whole one. Each `make` target builds the fonts first. `.venv/bin/fgtools media` with the same names renders the fonts that exist, without a build.

The last line of each command is `Open:` and the file to look at: the review page of the media, the PDF of the proof or the specimen, a picture or the diff report. Most terminals open the link with a Command-click.

## One render

A render is one file in `output/media/<folder>/<format>/`, named `<family>_<format>_<canvas>` with its extension. The folder is `images`, `carousels` or `videos`. An image is a PNG. A carousel is numbered PNG pages and one PDF, which is the document post of LinkedIn. A video is an MP4: H.264, 30 frames in a second, with a silent audio track.

Beside each render is a JSON record: the format, the canvas, the size, the caption, the alternative text and the commit of the sources. `output/media/index.html` shows every render on one page for review.

## Stages

| Stage | What happens | State |
| --- | --- | --- |
| 1. Compose | Each format places its elements on the lattice of each canvas | Built |
| 2. Check | The checker verifies each layout against the rules | Built |
| 3. Plot | DesignBot draws the layouts | Built |
| 4. Review | The designer reads the review page | Page built, approval planned |
| 5. Publish | CI runs `make site`: it renders the proof, the specimen and the media, `fgtools site` collects them into `output/site/`, and CI publishes that folder on GitHub Pages. Turn Pages on once in the settings of the repository, with the source "GitHub Actions". | Built |
| 6. Post | Posts with a caption, alternative text and a link for each platform, and a record of what was posted | Planned |

## What a person decides

- The words of the brand, and the glyphs to show.
- The approval of each render.
- The text of each caption. Alternative text for an image of text states the words, the typeface and the weight.
- The date of a release, and whether a draft glyph can be shown in public.

## Platforms

Each platform encodes a file again. The export for a platform follows from the canvas.

| Placement | Canvas | Export |
| --- | --- | --- |
| Instagram and TikTok picture | `portrait` | JPEG, sRGB, under 8 MB. Instagram accepts 20 pictures in a carousel. |
| LinkedIn, X, Mastodon image | `portrait` or `landscape` | PNG under 5 MB |
| LinkedIn document | `portrait` | PDF |
| Link preview | `card` | PNG or JPEG under 600 KB |
| Instagram Reel and Story, TikTok | `vertical` | MP4, 3 seconds or longer. A Reel can be posted again on TikTok without a change. |
| Video on X and LinkedIn | `landscape` | MP4 |

Mastodon encodes video at a low bit rate that damages thin strokes, so a still image is better there.

Virtua Grotesk’s `make twitter-animation` renders clean, red-grid and CRT versions. The specimen index lists all three under Twitter Animations. Its DesignBot script uses `renderer.set_crt(true)` for the CRT export.
