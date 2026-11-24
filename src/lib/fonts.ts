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
    indexWoff2: string;
    indexWoff2Bytes: number;
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

// The rule of one font. The index list uses the small font, which has
// only the alphabet and the name. The specimen page uses the full font.
export function fontFaceCss(font: IndexFont, file = font.facts.files.woff2): string {
  const axis = (tag: string) => font.facts.axes.find((a) => a.tag === tag);
  const weight = axis('wght');
  const width = axis('wdth');
  return [
    '@font-face {',
    `font-family: '${font.cssFamily}';`,
    `src: url('${file}') format('woff2');`,
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
// of Human Rights. A font shows the scripts that it has. Each text is
// the text of the UDHR in Unicode project (github.com/eric-muller/udhr),
// without change. Hindi has a space before the danda in that source.
export const SCRIPT_SAMPLES: Record<string, { lang: string; dir: 'ltr' | 'rtl'; text: string }> = {
  Latn: {
    lang: 'en',
    dir: 'ltr',
    text: 'All human beings are born free and equal in dignity and rights. They are endowed with reason and conscience and should act towards one another in a spirit of brotherhood.',
  },
  Arab: {
    lang: 'ar',
    dir: 'rtl',
    text: 'يولد جميع الناس أحرارًا متساوين في الكرامة والحقوق. وقد وهبوا عقلاً وضميرًا وعليهم أن يعامل بعضهم بعضًا بروح الإخاء.',
  },
  Hebr: {
    lang: 'he',
    dir: 'rtl',
    text: 'כל בני אדם נולדו בני חורין ושווים בערכם ובזכויותיהם. כולם חוננו בתבונה ובמצפון, לפיכך חובה עליהם לנהוג איש ברעהו ברוח של אחוה.',
  },
  Cyrl: {
    lang: 'ru',
    dir: 'ltr',
    text: 'Все люди рождаются свободными и равными в своем достоинстве и правах. Они наделены разумом и совестью и должны поступать в отношении друг друга в духе братства.',
  },
  Grek: {
    lang: 'el',
    dir: 'ltr',
    text: 'Όλοι οι άνθρωποι γεννιούνται ελεύθεροι και ίσοι στην αξιοπρέπεια και τα δικαιώματα. Είναι προικισμένοι με λογική και συνείδηση, και οφείλουν να συμπεριφέρονται μεταξύ τους με πνεύμα αδελφοσύνης.',
  },
  Armn: {
    lang: 'hy',
    dir: 'ltr',
    text: 'Բոլոր մարդիկ ծնվում են ազատ ու հավասար իրենց արժանապատվությամբ ու իրավունքներով։ Նրանք ունեն բանականություն ու խիղճ և միմյանց պետք է եղբայրաբար վերաբերվեն։',
  },
  Geor: {
    lang: 'ka',
    dir: 'ltr',
    text: 'ყოველი ადამიანი იბადება თავისუფალი და თანასწორი თავისი ღირსებითა და უფლებებით. მათ მინიჭებული აქვთ გონება და სინდისი და ერთმანეთის მიმართ უნდა ექცეოდნენ ძმობის სულისკვეთებით.',
  },
  Deva: {
    lang: 'hi',
    dir: 'ltr',
    text: 'सभी मनुष्यों को गौरव और अधिकारों के मामले में जन्मजात स्वतन्त्रता और समानता प्राप्त है । उन्हें बुद्धि और अन्तरात्मा की देन प्राप्त है और परस्पर उन्हें भाईचारे के भाव से बर्ताव करना चाहिए ।',
  },
  Beng: {
    lang: 'bn',
    dir: 'ltr',
    text: 'সমস্ত মানুষ স্বাধীনভাবে সমান মর্যাদা এবং অধিকার নিয়ে জন্মগ্রহণ করে। তাঁদের বিবেক এবং বুদ্ধি আছে; সুতরাং সকলেরই একে অপরের প্রতি ভ্রাতৃত্বসুলভ মনোভাব নিয়ে আচরণ করা উচিত।',
  },
  Taml: {
    lang: 'ta',
    dir: 'ltr',
    text: 'மனிதப் பிறிவியினர் சகலரும் சுதந்திரமாகவே பிறக்கின்றனர்; அவர்கள் மதிப்பிலும், உரிமைகளிலும் சமமானவர்கள், அவர்கள் நியாயத்தையும் மனச்சாட்சியையும் இயற்பண்பாகப் பெற்றவர்கள். அவர்கள் ஒருவருடனொருவர் சகோதர உணர்வுப் பாங்கில் நடந்துகொள்ளல் வேண்டும்.',
  },
  Hang: {
    lang: 'ko',
    dir: 'ltr',
    text: '모든 인간은 태어날 때부터 자유로우며 그 존엄과 권리에 있어 동등하다. 인간은 천부적으로 이성과 양심을 부여받았으며 서로 형제애의 정신으로 행동하여야 한다.',
  },
};

// The first sentence of a sample, for the tester. The sentence ends at a
// full stop, a danda or an Armenian full stop.
export function firstSentence(text: string): string {
  return /^.*?[.।։](?=\s|$)/u.exec(text)?.[0] ?? text;
}

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
