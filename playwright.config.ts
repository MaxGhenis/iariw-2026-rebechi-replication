import { defineConfig } from '@playwright/test';

const port = process.env.PORT || '3000';

export default defineConfig({
  testDir: './tests',
  timeout: 60000,
  use: {
    viewport: { width: 1920, height: 1080 },
    deviceScaleFactor: 2,
  },
  webServer: {
    command: `bun run dev -- -p ${port}`,
    url: `http://localhost:${port}`,
    reuseExistingServer: true,
    timeout: 120000,
  },
});
