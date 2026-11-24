import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';
import { SECTIONS } from './lib/docs';

const docs = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/docs' }),
  schema: z.object({
    title: z.string(),
    section: z.enum(Object.keys(SECTIONS) as [string, ...string[]]),
    order: z.number(),
    summary: z.string().optional(),
    introduction: z.string().optional(),
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

// One entry per model. The file name is the slug. Each model page has
// the same parts, in the sequence of these fields.
const models = defineCollection({
  loader: glob({ pattern: '*.yaml', base: './src/content/models' }),
  schema: z.object({
    order: z.number().int(),
    name: z.string(),
    type: z.string(),
    status: z.string(),
    summary: z.string(),
    tasks: z.string(),
    architecture: z.string(),
    parameters: z.string(),
    trainingData: z.string(),
    training: z.string().optional(),
    evaluation: z.string(),
    file: z.string(),
    license: z.string(),
    location: z.string(),
    locationUrl: z.string().url().optional(),
  }),
});

export const collections = { docs, fonts, models };
