// The sections of the guide, in the sequence of the guide index.
import { execFileSync } from 'node:child_process';

export const SECTIONS: Record<string, { title: string; description: string }> = {
  introduction: {
    title: 'Introduction',
    description:
      'The collection, its position on authorship and licenses, the NeuralType format and the tools.',
  },
  sources: {
    title: 'Sources',
    description:
      'The source repository of a font: how to start one, its layout, its license files and its use of GitHub.',
  },
  system: {
    title: 'Design rules',
    description:
      'The rules for each source: the grid, the outline structure, the grade of each glyph and the review of drafts.',
  },
  production: {
    title: 'Production',
    description:
      'The build of the fonts, the checks, the proofs, the media and the font index of this website.',
  },
  data: {
    title: 'Data and models',
    description:
      'The training corpus that the graded sources give, the models and the releases.',
  },
  contributing: {
    title: 'Contributions',
    description: 'The procedure for a contribution of drawings, corrections or code.',
  },
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
