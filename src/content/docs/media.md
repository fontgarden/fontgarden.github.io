---
title: Proofs and media
section: production
label: learn
order: 330
summary: The print proof, the technical images and the marketing media of a font, and how one system renders all of them.
callout: A project made from the template renders its proof and its marketing media with two commands. The parts that are the same for every font are in DesignBot and fgtools. The parts that give a font its own style are a small folder in the project. No rendered file is tracked in Git.
background: [build, qa]
next: [learning]
---

This chapter is a specification. The column State says what is built. Where it says "planned", the chapter is correct and the tool is not finished.

## Three kinds of output

| Kind | Reader | Same for every font | Made by | State |
| --- | --- | --- | --- | --- |
| Print proof | The designer, on paper | Yes | `make proof`, which runs `designbot proof` | Built |
| Technical images | A reader of a README or an article | Yes | DesignBot, from the font file | Planned |
| Marketing media | The public, on social platforms | No: one style for each font | `make media`, which runs `fgtools media` | Built, 7 formats |

DesignBot draws all three. A glyph looks the same in the proof, in a README image and in a video.

## The print proof

`make proof` writes `output/proof/proof.pdf`. DesignBot reads everything from the font file: the axes, the instances, the character set, the features and the metrics. A project holds no proof code.

| Page | State |
| --- | --- |
| Cover with the facts of the font, character set, waterfall | Built |
| Text at reading sizes, with leading and tracking | Built |
| Spacing, figures, accents, kerning | Built |
| Weight waterfall, interpolation | Built |
| Arabic: character set, joining, marks, running text | Built |
| Vertical metrics, drawn from the outlines | Planned |
| OpenType features, off and on | Planned |
| Hebrew pages | Planned |
| Glyphs under review, in a block of text beside a reference font | Planned |
| The same text in the font and in a reference font, in two colors | Planned |

## The marketing media

### Terms

| Term | Meaning |
| --- | --- |
| Canvas | One size of picture or video that the platforms accept, with its safe area. The same for every font. |
| Format | One kind of picture, for example a specimen poster. A DesignBot script that holds the layout. |
| Brand | The colors and the texts of one font. |
| Instance | One format with one set of values, for example the glyph detail of the letter a. |
| Render | One instance on one canvas: one file, with a record. |
| Post | One or more renders with a caption, alternative text and a link, for one platform. |
| Campaign | A group of posts with one purpose, for example a release. |

### Where each part is

| Part | Place | Changes for each font |
| --- | --- | --- |
| The canvases and their safe areas | fgtools, `fgtools/media_canvases.toml` | No |
| The runner, the checks and the review page | fgtools, the command `fgtools media` | No |
| The values that each script gets: canvas, font, metrics, brand | fgtools, the module `brief` | No |
| The brand: the colors and the texts | The project, `documentation/media/brand.toml` | Yes |
| The formats: the canvases, words, caption and alternative text of each | The project, `documentation/media/formats.toml` | Yes |
| The format scripts | The project, `documentation/media/images/`, `carousels/` and `videos/`, one file for each format. The folder says what the format makes. | Yes |
| The rendered files | `output/media/`, which Git ignores | Not tracked |

A new project starts with the format scripts of the template. The designer changes the brand first, and then the scripts.

### The canvases

| Canvas | Size | Use | Safe area: top, right, bottom, left |
| --- | --- | --- | --- |
| `portrait` | 1080 x 1350 | Feed image and carousel on Instagram, LinkedIn, X and Mastodon. The page of a LinkedIn document. | 0, 40, 0, 40 |
| `vertical` | 1080 x 1920 | Instagram Reel and Story, and TikTok | 270, 195, 672, 120 |
| `landscape` | 1920 x 1080 | Video and wide image on X, LinkedIn and Mastodon | 54, 96, 54, 96 |
| `square` | 1080 x 1080 | A page or a profile that needs a square | 54, 54, 54, 54 |
| `card` | 1200 x 630 | The link preview | 15, 0, 15, 0 |

No platform of this list publishes its safe area. The values are from current guides, checked in November 2026. The platforms change these values each year, so they are data in one file, and `fgtools media --safe-areas` draws them on every picture.

### The formats

One format gives many posts, because one value changes between instances.

| Series | Format | Kind | Value that changes | State |
| --- | --- | --- | --- | --- |
| Release | `release`: name, version and facts from the font file | Image | Version | Built |
| Release | `link-card`: the picture of a link | Image | Title | Built |
| Release | Release notes: the glyphs that a version adds | Carousel | Version | Planned |
| Glyphs | `specimen-poster`: words from the lightest to the heaviest weight | Image | Words | Built |
| Glyphs | `glyph-detail`: one glyph on the grid with the metrics | Carousel | Glyph | Built |
| Glyphs | `character-set`: one page for each group of characters | Carousel | Group | Built |
| Glyphs | Annotated glyph: numbered features of the design on one glyph | Image | Glyph | Planned |
| Glyphs | Similar characters, for example I, l and 1 | Image | Set | Planned |
| Axis | `weight-axis`: one word across the weight axis | Video | Word | Built |
| Axis | Weight numbers: each value set in its own weight | Image | Range | Planned |
| Axis | Wave: rows of a word, each row later on the axis | Video | Word, script | Planned |
| Axis | Masters: the outlines of two masters with lines between matching points | Image or video | Glyph | Planned |
| Scripts | `scripts`: one line in each script of the font | Carousel | Lines | Built |
| Scripts | Language sample | Carousel | Language | Planned |
| Process | Before and after: one glyph at two commits | Video | Glyph, commits | Planned |
| Process | Progress: the review state of the glyph set | Image | Date | Planned |
| Use | Installation and CSS | Image | Text | Planned |

### One render

A render is one file in `output/media/<folder>/<format>/`, named `<family>_<format>_<canvas>` with its extension. The folder is `images`, `carousels` or `videos`, as in the sources. An image is a PNG. A carousel is numbered PNG pages and one PDF, which is the document post of LinkedIn. A video is an MP4: H.264, 30 frames in a second, with a silent audio track.

Beside each render is a JSON record: the format, the canvas, the size, the caption, the alternative text and the commit of the sources. `output/media/index.html` shows every render on one page for review.

### Stages

| Stage | What happens | State |
| --- | --- | --- |
| 1. Render | `make media` renders each format on each of its canvases | Built |
| 2. Check | Automatic checks of each render | Partly built |
| 3. Review | The designer reads the review page and approves renders | Page built, approval planned |
| 4. Publish | CI renders the proof and the media, `fgtools site` collects them into `output/site/`, and CI publishes that folder on GitHub Pages. A README shows pictures from there. Turn Pages on once in the settings of the repository, with the source "GitHub Actions". | Built |
| 5. Compose | Posts get their renders, caption, alternative text and link for each platform | Planned |
| 6. Export | A file for a scheduling tool, or a call to the platform | Planned |
| 7. Record | The address of each post, so that no post repeats and results can be compared | Planned |

### Checks

| Check | State |
| --- | --- |
| The font has a glyph for each character of the brand texts. DesignBot draws a missing glyph with a system font, and a picture of another font is worse than no picture. | Built |
| A format that needs a weight axis is not rendered for a font with one weight | Built |
| The safe area can be drawn on each picture | Built |
| No system font for text that a script writes itself | Planned, in DesignBot |
| Text inside the safe area and inside its box | Planned |
| Contrast of the colors of the brand | Planned |
| A loop is seamless, and it has no more than three flashes in a second | Planned |
| Size, codec, duration and file size against the limits of each platform | Planned |
| Alternative text and caption present, and inside the limit of each platform | Planned |
| The same sources give the same file | Planned |

### What a person decides

- The words and the glyphs to show.
- The approval of each render.
- The text of each caption. Alternative text for an image of text states the words, the typeface and the weight.
- The date of a release, and whether a draft glyph can be shown in public.
- Photographs of the font in use, with their credits.

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

Animated WebP and APNG are not accepted by any platform. Mastodon encodes video at a low bit rate that damages thin strokes, so a still image is better there.
