// Section and label vocabulary for the documentation. The structure is
// adapted from the Google Fonts Guide (googlefonts.github.io/gf-guide,
// Apache-2.0).

import { execFileSync } from 'node:child_process';

export const SECTIONS: Record<string, { title: string; description: string }> = {
  introduction: {
    title: 'Introduction: the basics',
    description:
      'What the collection is, the position it takes on authorship and licensing, the font format it is built toward, and the tools.',
  },
  sources: {
    title: 'Sources: the files of the collection',
    description:
      'The source tree, the license files and the hosting practice that the build, the checks and the corpus tools depend on.',
  },
  system: {
    title: 'Engineering rules: grid, structure and grades',
    description:
      'The requirements every source in the collection meets. They are stricter than ordinary font production because every glyph is also training data.',
  },
  production: {
    title: 'Production: building and testing',
    description:
      'How the OpenType fonts are compiled from the sources, checked and proofed.',
  },
  data: {
    title: 'Data and models',
    description:
      'How graded sources become a corpus, how the models are trained and evaluated, and what is released.',
  },
  contributing: {
    title: 'Contributing',
    description:
      'How drawings and corrections enter the collection.',
  },
};

export const LABELS: Record<string, { text: string; color: string; meaning: string }> = {
  start: { text: 'start', color: 'blue', meaning: 'Read first if you are new to the project.' },
  must: { text: 'must→', color: 'green', meaning: 'A requirement. Every source in the collection follows it.' },
  learn: { text: 'learn', color: 'yellow', meaning: 'Background and reference material.' },
  team: { text: 'team', color: 'brown', meaning: 'Process notes for people who grade and merge work.' },
  nerd: { text: 'nerd', color: 'purple', meaning: 'Technical detail on the data and the models.' },
  templ: { text: 'templ', color: 'grey', meaning: 'A template you can copy.' },
};

export const REPOSITORY = 'https://github.com/fontgarden/fontgarden.github.io';

// The date of the last commit that changed a file, as 2026-11-24. The
// value is null when Git does not have the history of the file.
export function lastChanged(file: string): string | null {
  try {
    const date = execFileSync('git', ['log', '-1', '--format=%cs', '--', file], {
      encoding: 'utf8',
    }).trim();
    return date || null;
  } catch {
    return null;
  }
}

// The chapters in the sequence of the guide index: by section, then by
// the order number of the chapter.
export function inGuideSequence<T extends { data: { section: string; order: number } }>(
  chapters: T[]
): T[] {
  const sections = Object.keys(SECTIONS);
  return [...chapters].sort(
    (a, b) =>
      sections.indexOf(a.data.section) - sections.indexOf(b.data.section) ||
      a.data.order - b.data.order
  );
}
