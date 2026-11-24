// The FTGD-100 font index: the entries of src/content/fonts joined with
// the facts that scripts/import_font.py writes to src/data/fonts.
import { getCollection } from 'astro:content';

export const INDEX_SIZE = 100;

export interface Axis {
  tag: string;
  name: string;
  min: number;
  default: number;
  max: number;
}

export interface FontFacts {
  family: string;
  version: string;
  copyright: string;
  license: string;
  licenseUrl: string;
  revision: { commit: string; date: string } | null;
  unitsPerEm: number;
  metrics: { ascender: number; capHeight: number; xHeight: number; descender: number };
  glyphCount: number;
  characterCount: number;
  axes: Axis[];
  instances: { name: string; coordinates: Record<string, number> }[];
  scripts: { tag: string; name: string; count: number }[];
  features: { GSUB: string[]; GPOS: string[] };
  featureSamples: { tag: string; name: string; sample: string }[];
  files: {
    woff2: string;
    woff2Bytes: number;
    download: string;
    preview: string;
    downloadBytes: number;
    fontFile: string;
    webFontFile: string;
  };
  groups: { name: string; tag: string | null; characters: [number, string][] }[];
}

export interface IndexFont {
  slug: string;
  number: number;
  label: string;
  name: string;
  classification: string;
  status: string;
  repository: string;
  summary: string;
  cssFamily: string;
  facts: FontFacts;
}

const facts = import.meta.glob<FontFacts>('../data/fonts/*.json', {
  eager: true,
  import: 'default',
});

export const numberLabel = (number: number) => String(number).padStart(2, '0');

export async function loadFonts(): Promise<IndexFont[]> {
  const entries = await getCollection('fonts');
  const fonts = entries.map((entry) => {
    const data = facts[`../data/fonts/${entry.id}.json`];
    if (!data) {
      throw new Error(
        `No facts for ${entry.id}. Run scripts/import_font.py --slug ${entry.id}.`
      );
    }
    return {
      slug: entry.id,
      ...entry.data,
      label: numberLabel(entry.data.number),
      // The family name in CSS. Each font of the index has its own, so
      // that a specimen never falls back to the font of the site text.
      cssFamily: `FTGD ${numberLabel(entry.data.number)}`,
      facts: data,
    };
  });
  fonts.sort((a, b) => a.number - b.number);
  fonts.forEach((font, i) => {
    if (i > 0 && fonts[i - 1].number === font.number) {
      throw new Error(`Two fonts have the number ${font.label}.`);
    }
  });
  return fonts;
}

export function fontFaceCss(font: IndexFont): string {
  const axis = (tag: string) => font.facts.axes.find((a) => a.tag === tag);
  const weight = axis('wght');
  const width = axis('wdth');
  return [
    '@font-face {',
    `font-family: '${font.cssFamily}';`,
    `src: url('${font.facts.files.woff2}') format('woff2');`,
    weight ? `font-weight: ${weight.min} ${weight.max};` : '',
    width ? `font-stretch: ${width.min}% ${width.max}%;` : '',
    'font-display: swap;',
    '}',
  ].join('');
}

// The CSS that a person copies to use the font on a website. The file
// is the WOFF2 of the download, next to the style sheet.
export function usageCss(font: IndexFont): string {
  const axis = (tag: string) => font.facts.axes.find((a) => a.tag === tag);
  const weight = axis('wght');
  const width = axis('wdth');
  return [
    '@font-face {',
    `  font-family: '${font.facts.family}';`,
    `  src: url('${font.facts.files.webFontFile}') format('woff2');`,
    weight ? `  font-weight: ${weight.min} ${weight.max};` : '',
    width ? `  font-stretch: ${width.min}% ${width.max}%;` : '',
    '  font-display: swap;',
    '}',
    '',
    'body {',
    `  font-family: '${font.facts.family}', sans-serif;`,
    '}',
  ]
    .filter((line, i, lines) => line !== '' || lines[i - 1] === '}')
    .join('\n');
}

export const axisRange = (axis: Axis) => `${axis.name} ${axis.min} to ${axis.max}`;

export function variationSettings(coordinates: Record<string, number>): string {
  return Object.entries(coordinates)
    .map(([tag, value]) => `'${tag}' ${value}`)
    .join(', ');
}

export function fileSize(bytes: number): string {
  return `${Math.round(bytes / 1000)} kB`;
}

// The same text for each font: Article 1 of the Universal Declaration
// of Human Rights. A font shows the scripts that it has.
export const SCRIPT_SAMPLES: Record<string, { lang: string; dir: 'ltr' | 'rtl'; text: string }> = {
  Latn: {
    lang: 'en',
    dir: 'ltr',
    text: 'All human beings are born free and equal in dignity and rights. They are endowed with reason and conscience and should act towards one another in a spirit of brotherhood.',
  },
  Arab: {
    lang: 'ar',
    dir: 'rtl',
    text: 'يولد جميع الناس أحراراً متساوين في الكرامة والحقوق. وقد وهبوا عقلاً وضميراً وعليهم أن يعامل بعضهم بعضاً بروح الإخاء.',
  },
  Hebr: {
    lang: 'he',
    dir: 'rtl',
    text: 'כל בני אדם נולדו בני חורין ושווים בערכם ובזכויותיהם. כולם חוננו בתבונה ובמצפון, לפיכך חובה עליהם לנהוג איש ברעהו ברוח של אחוה.',
  },
};

// Articles 1 to 3, for the text sizes.
export const TEXT_SAMPLE = [
  SCRIPT_SAMPLES.Latn.text,
  'Everyone is entitled to all the rights and freedoms set forth in this Declaration, without distinction of any kind, such as race, colour, sex, language, religion, political or other opinion, national or social origin, property, birth or other status.',
  'Everyone has the right to life, liberty and security of person.',
];

export const ALPHABET_SAMPLE = [
  'ABCDEFGHIJKLMNOPQRSTUVWXYZ',
  'abcdefghijklmnopqrstuvwxyz',
  '0123456789',
];
