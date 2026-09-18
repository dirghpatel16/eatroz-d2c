#!/usr/bin/env node

/**
 * Eatroz / Open-Source UI Extraction Toolkit
 * Multi-Viewport High-DPI Capture
 * Captures full-page Desktop (1440px), Tablet (768px), and Mobile (390px) screenshots.
 * 100% Free & Open Source.
 */

import { chromium } from "@playwright/test";
import fs from "fs";
import path from "path";

const VIEWPORTS = [
  { name: "desktop_1440px", width: 1440, height: 900, scale: 2 },
  { name: "tablet_768px", width: 768, height: 1024, scale: 2 },
  { name: "mobile_390px", width: 390, height: 844, scale: 3 },
];

export async function captureViewports(targetUrl, outputDir = "./extracted-screenshots") {
  console.log(`\n======================================================`);
  console.log(`📸 Capturing Multi-Viewport Screenshots for: ${targetUrl}`);
  console.log(`📁 Saving to: ${outputDir}`);
  console.log(`======================================================\n`);

  if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir, { recursive: true });
  }

  const browser = await chromium.launch({ headless: true });

  try {
    for (const vp of VIEWPORTS) {
      console.log(`📷 Capturing ${vp.name} (${vp.width}x${vp.height} @ ${vp.scale}x DPI)...`);
      const context = await browser.newContext({
        viewport: { width: vp.width, height: vp.height },
        deviceScaleFactor: vp.scale,
        userAgent:
          vp.width < 768
            ? "Mozilla/5.0 (iPhone; CPU iPhone OS 17_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Mobile/15E148 Safari/604.1"
            : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
      });

      const page = await context.newPage();
      await page.goto(targetUrl, { waitUntil: "domcontentloaded", timeout: 30000 });
      await page.waitForTimeout(2000);

      const filePath = path.join(outputDir, `${vp.name}.png`);
      await page.screenshot({ path: filePath, fullPage: true });
      console.log(`✅ Saved: ${filePath}`);

      await context.close();
    }

    console.log(`\n🎉 Multi-viewport capture complete!\n`);
  } catch (error) {
    console.error(`❌ Capture error:`, error);
  } finally {
    await browser.close();
  }
}

// CLI entrypoint
if (process.argv[1] && process.argv[1].endsWith("capture-viewports.mjs")) {
  const target = process.argv[2] || "http://localhost:3000";
  const output = process.argv[3] || "./extracted-screenshots";
  captureViewports(target, output);
}
