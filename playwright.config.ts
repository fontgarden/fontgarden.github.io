// Screenshot tests of the built site. See tests/visual/pages.spec.ts.
import { defineConfig } from '@playwright/test';

const PORT = 4391;

export default defineConfig({
  testDir: 'tests/visual',
  snapshotPathTemplate: 'tests/visual/snapshots/{projectName}/{arg}{ext}',
  fullyParallel: true,
  reporter: [['list']],
  use: {
    baseURL: `http://localhost:${PORT}`,
    // The installed Chrome. The tests do not download a browser.
    channel: 'chrome',
    // With reduced motion the panel shows still text, so a picture does
    // not change from one run to the next.
    reducedMotion: 'reduce',
  },
  expect: {
    toHaveScreenshot: { animations: 'disabled', maxDiffPixelRatio: 0.001 },
  },
  projects: [
    { name: 'desktop', use: { viewport: { width: 1440, height: 900 } } },
    { name: 'phone', use: { viewport: { width: 390, height: 844 }, hasTouch: true } },
  ],
  webServer: {
    command: `pnpm build && pnpm preview --port ${PORT}`,
    url: `http://localhost:${PORT}/fonts/`,
    reuseExistingServer: false,
  },
});
