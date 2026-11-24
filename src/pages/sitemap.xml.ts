// The sitemap: the address of each page of the site.
import type { APIRoute } from 'astro';
import { getCollection } from 'astro:content';
import { loadFonts } from '../lib/fonts';
import { loadModels } from '../lib/models';

export const GET: APIRoute = async ({ site }) => {
  const docs = await getCollection('docs');
  const fonts = await loadFonts();
  const models = await loadModels();
  const paths = [
    '/',
    '/fonts/',
    ...fonts.map((font) => `/fonts/${font.slug}/`),
    '/models/',
    ...models.map((model) => `/models/${model.id}/`),
    '/docs/',
    ...docs.map((doc) => `/docs/${doc.id}/`),
    '/about/',
  ];
  const urls = paths.map((path) => `  <url><loc>${new URL(path, site)}</loc></url>`);
  const xml = [
    '<?xml version="1.0" encoding="UTF-8"?>',
    '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ...urls,
    '</urlset>',
    '',
  ].join('\n');
  return new Response(xml, { headers: { 'Content-Type': 'application/xml' } });
};
