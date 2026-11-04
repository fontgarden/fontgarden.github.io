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

export const collections = { docs };
