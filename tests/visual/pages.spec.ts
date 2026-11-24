// Screenshot tests: each page, complete, at a desktop and a phone width.
// A test fails when a page differs from its stored picture.
//
//   pnpm test:visual:update     store the pictures, before a change
//   pnpm test:visual            compare the pages with the stored pictures
//
// Git ignores the pictures, and the tests do not run in CI: text has other
// pixels on another system, and the pictures are 13 MB.
import { expect, test, type Page } from '@playwright/test';

const PAGES: [name: string, path: string][] = [
  ['home', '/'],
  ['font-index', '/fonts/'],
  ['specimen', '/fonts/virtua-grotesk/'],
  ['guide-index', '/docs/'],
  ['guide-chapter', '/docs/font-index/'],
  ['not-found', '/404.html'],
];

const settle = async (page: Page) => {
  await page.evaluate(() => document.fonts.ready);
  await page.waitForLoadState('networkidle');
};

for (const [name, path] of PAGES) {
  test(name, async ({ page }) => {
    await page.goto(path);
    await settle(page);
    await expect(page).toHaveScreenshot(`${name}.png`, {
      fullPage: true,
      // The date of the last change is not a fact of the layout.
      mask: [page.locator('.chapter-source time')],
    });
  });
}

test('font-index-selection', async ({ page, isMobile }, testInfo) => {
  await page.goto('/fonts/');
  await settle(page);
  const row = page.locator('a[data-font="virtua-grotesk"]');
  // A desktop shows the specimen in the panel. A phone shows it below the row.
  if (testInfo.project.name === 'phone') await row.click();
  else await row.hover();
  await settle(page);
  await expect(page).toHaveScreenshot('font-index-selection.png');
});
