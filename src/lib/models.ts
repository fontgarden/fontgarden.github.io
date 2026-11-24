// The models of the site: the entries of src/content/models, in sequence.
import { getCollection, type CollectionEntry } from 'astro:content';

export type Model = CollectionEntry<'models'>;

export async function loadModels(): Promise<Model[]> {
  const models = await getCollection('models');
  return models.sort((a, b) => a.data.order - b.data.order);
}
