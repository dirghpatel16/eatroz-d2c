#!/usr/bin/env node

/**
 * Eatroz / Open-Source UI Extraction Toolkit
 * Master Orchestrator: Runs Token Extraction, Asset Harvesting, Viewport Capture, and Figma Export.
 * 100% Free, Local, and Open Source.
 */

import path from "path";
import { extractDesignTokens } from "./extract-design-tokens.mjs";
import { harvestAssets } from "./harvest-assets.mjs";
import { captureViewports } from "./capture-viewports.mjs";
import { exportWebToFigma } from "./web-to-figma.mjs";

async function main() {
  const target = process.argv[2] || "http://localhost:3000";
  const outputRoot = process.argv[3] || "./extracted-output";

  console.log(`\n================================================================`);
  console.log(`🚀 RUNNING COMPLETE 100% FREE UI EXTRACTION SUITE`);
  console.log(`🎯 Target: ${target}`);
  console.log(`📂 Output Root: ${outputRoot}`);
  console.log(`================================================================\n`);

  try {
    console.log(`\n[STEP 1/4] Extracting Design Tokens & CSS Variables...`);
    await extractDesignTokens(target, path.join(outputRoot, "tokens"));

    console.log(`\n[STEP 2/4] Harvesting Vector SVGs, Web Fonts, and Images...`);
    await harvestAssets(target, path.join(outputRoot, "assets"));

    console.log(`\n[STEP 3/4] Capturing Multi-Viewport High-DPI Screenshots...`);
    await captureViewports(target, path.join(outputRoot, "screenshots"));

    console.log(`\n[STEP 4/4] Exporting DOM to Figma Layer Tree...`);
    await exportWebToFigma(target, path.join(outputRoot, "figma"));

    console.log(`\n================================================================`);
    console.log(`🎉 ALL EXTRACTION TASKS COMPLETED SUCCESSFULLY (100% FREE)!`);
    console.log(`📁 All assets, tokens, screenshots, and Figma files saved in:`);
    console.log(`   👉 ${path.resolve(outputRoot)}`);
    console.log(`================================================================\n`);
  } catch (err) {
    console.error(`❌ Orchestrator error:`, err);
    process.exit(1);
  }
}

main();
