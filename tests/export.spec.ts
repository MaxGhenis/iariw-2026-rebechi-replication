import { test } from '@playwright/test';
import * as fs from 'fs';

const SLIDE_COUNT = 24;

test('export all slides as PNGs', async ({ page }) => {
  test.setTimeout(300000);
  fs.mkdirSync('export', { recursive: true });
  for (let i = 0; i < SLIDE_COUNT; i++) {
    await page.goto(`http://localhost:3000/?slide=${i}`);
    await page.waitForLoadState('networkidle');
    // Let images and fonts settle
    await page.waitForTimeout(400);
    const n = String(i + 1).padStart(2, '0');
    await page.screenshot({ path: `export/slide-${n}.png` });
  }
});
