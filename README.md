# Font.Garden Website

The [font.garden](https://font.garden) website — a single-page landing site for
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

- `src/pages/index.astro` — the landing page (the whole site)
- `src/layouts/Layout.astro` — html/head shell
- `src/styles/global.css` — Tailwind directives, `@font-face`, base styles
- `src/styles/fonts/` — woff2 fonts used by the site (refreshed by `~/Desktop/rebuild-virtua.sh`)
- `public/` — static assets served as-is (favicon, CNAME)
