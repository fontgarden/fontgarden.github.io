import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';
import { LABELS, SECTIONS } from './lib/docs';

const docs = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/docs' }),
  schema: z.object({
    title: z.string(),
    section: z.enum(Object.keys(SECTIONS) as [string, ...string[]]),
    label: z.enum(Object.keys(LABELS) as [string, ...string[]]),
    order: z.number(),
    summary: z.string().optional(),
    callout: z.string().optional(),
    background: z.array(z.string()).default([]),
    next: z.array(z.string()).default([]),
  }),
});

// One entry per font of the FTGD-100 index. The file name is the slug.
// scripts/import_font.py writes the measured facts to src/data/fonts.
const fonts = defineCollection({
  loader: glob({ pattern: '*.yaml', base: './src/content/fonts' }),
  schema: z.object({
    number: z.number().int().min(0).max(99),
    name: z.string(),
    classification: z.string(),
    status: z.string(),
    repository: z.string().url(),
    summary: z.string(),
  }),
});

export const collections = { docs, fonts };
