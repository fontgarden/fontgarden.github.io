// The sitemap: the address of each page of the site.
import type { APIRoute } from 'astro';
import { getCollection } from 'astro:content';
import { loadFonts } from '../lib/fonts';

export const GET: APIRoute = async ({ site }) => {
  const docs = await getCollection('docs');
  const fonts = await loadFonts();
  const paths = [
    '/',
    '/fonts/',
    ...fonts.map((font) => `/fonts/${font.slug}/`),
    '/docs/',
    ...docs.map((doc) => `/docs/${doc.id}/`),
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
