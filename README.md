# Font.Garden Website

The [font.garden](https://font.garden) website — the landing page and documentation for
Font Garden and the NeuralType (`.ntf`) font format. Built with
[Astro](https://astro.build) and Tailwind CSS, deployed to GitHub Pages on
every push to `main`.

## Develop

```
pnpm install
pnpm dev
```

## Build

```
pnpm build
pnpm preview
```

## Structure

- `src/pages/index.astro` — the landing page
- `src/pages/docs/` — the documentation index and chapter template
- `src/content/docs/*.md` — one Markdown file per guide chapter; frontmatter sets
  section, label, order, callout, background and next reading
- `src/content.config.ts`, `src/lib/docs.ts` — chapter schema, section and label vocabulary
- `src/layouts/DocsLayout.astro`, `src/styles/docs.css` — documentation shell and styles,
  adapted from the Google Fonts Guide (Apache-2.0)
- `src/layouts/Layout.astro` — html/head shell
- `src/styles/global.css` — Tailwind directives, `@font-face`, base styles
- `src/styles/fonts/` — woff2 fonts used by the site (refreshed by `~/Desktop/rebuild-virtua.sh`)
- `public/` — static assets served as-is (favicon, CNAME)

## Keep the guide current

The guide describes the Font.Garden system: the project template
(`fontgarden/font-project-template`), the tools (`fontgarden/fontgarden-tools`),
the QA profile (`fontgarden/fontspector-fontgarden`), the tracing tools
(`img2glyph`, `img2bez`, `img2ufo`) and the reference project
(`eliheuer/virtua-grotesk`). Those repositories are the source of the facts.

When a command, a rule, a grade or the layout changes in one of them, update
the chapter that describes it in the same session:

| change | chapter |
| --- | --- |
| a `fgtools` command or a make target | `fgtools.md`, and `build.md` or `qa.md` |
| the template or `fgtools customize` | `start.md`, `sources.md` |
| the specimen intake or the tracing tools | `specimen.md`, `tools.md` |
| mark colors and their policy | `grades.md`, `proposals.md` |
| corrections or the drafting evaluation | `learning.md` |
| a Fontspector check of the profile | `qa.md` |

`scripts/check_guide.py` compares the guide with checkouts of those
repositories. It fails when a chapter names an `fgtools` command or a `make`
target that does not exist, and when a command or a template target has no
chapter. CI runs it on each push and each Monday.

```
python3 scripts/check_guide.py --tools ~/GH/fontgarden/fontgarden-tools \
  --template ~/GH/fontgarden/font-project-template --reference ~/GH/repos/virtua-grotesk
```

Run it and `pnpm build` before a commit. A push to `main` publishes the site.
