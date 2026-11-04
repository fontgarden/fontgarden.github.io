// Section and label vocabulary for the documentation. The structure is
// adapted from the Google Fonts Guide (googlefonts.github.io/gf-guide,
// Apache-2.0).

export const SECTIONS: Record<string, { title: string; description: string }> = {
  introduction: {
    title: 'Introduction: the basics',
    description:
      'The concepts, tools and knowledge you need before you work on a Font Garden project.',
  },
  sources: {
    title: 'The source repository: project files',
    description:
      'The required layout of a font project on GitHub, so that builds, checks and training all read the same files.',
  },
  system: {
    title: 'The design system: grid and grades',
    description:
      'The rules that make a source usable as training data: the power-of-two grid, the glyph grades and the outline conventions.',
  },
  production: {
    title: 'Production: building and testing fonts',
    description:
      'How to build OpenType fonts from the sources, check them and proof them.',
  },
  data: {
    title: 'Training data and models',
    description:
      'How graded sources become a corpus, and how the open-weight models are released.',
  },
  catalog: {
    title: 'The catalog: publishing on font.garden',
    description:
      'The process for adding a family to the Font Garden catalog.',
  },
};

export const LABELS: Record<string, { text: string; color: string; meaning: string }> = {
  start: { text: 'start', color: 'blue', meaning: 'Read first if you are new to the project.' },
  must: { text: 'must→', color: 'green', meaning: 'A requirement. Every family in the catalog follows it.' },
  learn: { text: 'learn', color: 'yellow', meaning: 'Background and reference material.' },
  team: { text: 'team', color: 'brown', meaning: 'Process notes for people who publish families.' },
  nerd: { text: 'nerd', color: 'purple', meaning: 'Technical detail on the data and the models.' },
  templ: { text: 'templ', color: 'grey', meaning: 'A template you can copy into your repository.' },
};
