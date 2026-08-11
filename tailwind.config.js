/** @type {import('tailwindcss').Config} */
export default {
  content: ['./src/**/*.{astro,html,js,jsx,md,mdx,svelte,ts,tsx,vue}'],
  theme: {
    extend: {
      colors: {
        ink: 'var(--color-ink)',
        paper: 'var(--color-paper)',
        muted: 'var(--color-muted)',
        rule: 'var(--color-rule)',
        accent: '#FF4E00',
      },
      fontSize: {
        small: ['var(--text-small)', { lineHeight: '1.5' }],
        h1: ['var(--text-h1)', { lineHeight: '1.25' }],
      },
      fontFamily: {
        grotesk: ['Virtua Grotesk', 'system-ui', 'sans-serif'],
      },
    },
  },
  plugins: [],
};
