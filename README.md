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
