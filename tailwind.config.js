/** @type {import('tailwindcss').Config} */
export default {
  content: ['./src/**/*.{astro,html,js,jsx,md,mdx,svelte,ts,tsx,vue}'],
  theme: {
    extend: {
      colors: {
        accent: '#FF4E00',
      },
      fontFamily: {
        grotesk: ['Virtua Grotesk', 'system-ui', 'sans-serif'],
      },
    },
  },
  plugins: [],
};
