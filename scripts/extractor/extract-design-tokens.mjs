#!/usr/bin/env node

/**
 * Eatroz / Open-Source UI Extraction Toolkit
 * Automated Design Token & Style Extractor
 * Uses local Playwright to extract computed styles, colors, typography, and spacing.
 * 100% Free & Open Source.
 */

import { chromium } from "@playwright/test";
import fs from "fs";
import path from "path";

// Helper to convert rgb/rgba to hex
function rgbToHex(rgbStr) {
  if (!rgbStr || rgbStr === "transparent" || rgbStr === "rgba(0, 0, 0, 0)") return null;
  const match = rgbStr.match(/rgba?\((\d+),\s*(\d+),\s*(\d+)(?:,\s*([\d.]+))?\)/);
  if (!match) return rgbStr;
  const r = parseInt(match[1]).toString(16).padStart(2, "0");
  const g = parseInt(match[2]).toString(16).padStart(2, "0");
  const b = parseInt(match[3]).toString(16).padStart(2, "0");
  if (match[4] !== undefined && parseFloat(match[4]) < 1) {
    const a = Math.round(parseFloat(match[4]) * 255).toString(16).padStart(2, "0");
    return `#${r}${g}${b}${a}`.toUpperCase();
  }
  return `#${r}${g}${b}`.toUpperCase();
}

export async function extractDesignTokens(targetUrl, outputDir = "./extracted-design-system") {
  console.log(`\n======================================================`);
  console.log(`🚀 Starting UI Extraction for: ${targetUrl}`);
  console.log(`📁 Output Directory: ${outputDir}`);
  console.log(`======================================================\n`);

  if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir, { recursive: true });
  }

  const browser = await chromium.launch({
    headless: true,
    args: ["--no-sandbox", "--disable-setuid-sandbox"],
  });

  const context = await browser.newContext({
    viewport: { width: 1440, height: 900 },
    userAgent:
      "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
  });

  const page = await context.newPage();

  try {
    console.log(`⏳ Navigating to ${targetUrl}...`);
    await page.goto(targetUrl, { waitUntil: "domcontentloaded", timeout: 30000 });
    // Allow any dynamic client-side animations or fonts to settle
    await page.waitForTimeout(2000);

    console.log(`🔍 Inspecting DOM styles and computed tokens...`);

    const extracted = await page.evaluate(() => {
      const colors = {
        backgrounds: {},
        text: {},
        borders: {},
      };
      const typography = {
        families: {},
        headings: {},
        body: {},
      };
      const spacing = new Set();
      const radii = new Set();
      const shadows = new Set();
      const cssVariables = {};

      // 1. Extract CSS Custom Properties from document
      for (const sheet of Array.from(document.styleSheets)) {
        try {
          for (const rule of Array.from(sheet.cssRules || [])) {
            if (rule.selectorText === ":root" || rule.selectorText === "html") {
              for (const prop of Array.from(rule.style)) {
                if (prop.startsWith("--")) {
                  cssVariables[prop] = rule.style.getPropertyValue(prop).trim();
                }
              }
            }
          }
        } catch {
          // Ignore cross-origin stylesheet errors
        }
      }

      // 2. Traverse visible DOM elements
      const elements = Array.from(document.querySelectorAll("body *"));

      elements.forEach((el) => {
        const style = window.getComputedStyle(el);
        const rect = el.getBoundingClientRect();

        // Skip non-visible elements
        if (rect.width === 0 || rect.height === 0 || style.display === "none" || style.visibility === "hidden") {
          return;
        }

        // Colors
        if (style.backgroundColor && style.backgroundColor !== "rgba(0, 0, 0, 0)") {
          colors.backgrounds[style.backgroundColor] = (colors.backgrounds[style.backgroundColor] || 0) + 1;
        }
        if (style.color) {
          colors.text[style.color] = (colors.text[style.color] || 0) + 1;
        }
        if (style.borderColor && style.borderWidth !== "0px" && style.borderStyle !== "none") {
          colors.borders[style.borderColor] = (colors.borders[style.borderColor] || 0) + 1;
        }

        // Typography
        if (style.fontFamily) {
          typography.families[style.fontFamily] = (typography.families[style.fontFamily] || 0) + 1;
        }

        const tag = el.tagName.toLowerCase();
        const textContent = el.textContent?.trim();

        if (textContent && textContent.length > 0) {
          const typeSpec = {
            fontFamily: style.fontFamily,
            fontSize: style.fontSize,
            fontWeight: style.fontWeight,
            lineHeight: style.lineHeight,
            letterSpacing: style.letterSpacing,
          };

          if (/^h[1-6]$/.test(tag)) {
            if (!typography.headings[tag]) {
              typography.headings[tag] = typeSpec;
            }
          } else if (tag === "p" || tag === "span" || tag === "div") {
            const key = `${style.fontSize}-${style.fontWeight}`;
            if (!typography.body[key]) {
              typography.body[key] = { ...typeSpec, sample: textContent.slice(0, 30) };
            }
          }
        }

        // Spacing & Layout
        ["paddingTop", "paddingRight", "paddingBottom", "paddingLeft"].forEach((prop) => {
          if (style[prop] && style[prop] !== "0px") spacing.add(style[prop]);
        });

        // Radii
        if (style.borderRadius && style.borderRadius !== "0px") {
          radii.add(style.borderRadius);
        }

        // Shadows
        if (style.boxShadow && style.boxShadow !== "none") {
          shadows.add(style.boxShadow);
        }
      });

      return {
        colors,
        typography,
        spacing: Array.from(spacing).sort((a, b) => parseFloat(a) - parseFloat(b)),
        radii: Array.from(radii),
        shadows: Array.from(shadows),
        cssVariables,
      };
    });

    // Process Colors to Hex and sort by frequency
    const processColorGroup = (group) =>
      Object.entries(group)
        .map(([rgb, count]) => ({ hex: rgbToHex(rgb), raw: rgb, count }))
        .filter((c) => c.hex)
        .sort((a, b) => b.count - a.count);

    const processedTokens = {
      meta: {
        sourceUrl: targetUrl,
        extractedAt: new Date().toISOString(),
        viewport: "1440x900",
      },
      colors: {
        backgrounds: processColorGroup(extracted.colors.backgrounds),
        text: processColorGroup(extracted.colors.text),
        borders: processColorGroup(extracted.colors.borders),
      },
      typography: {
        dominantFamilies: Object.entries(extracted.typography.families)
          .sort((a, b) => b[1] - a[1])
          .map(([fam, count]) => ({ family: fam, occurrences: count })),
        headings: extracted.typography.headings,
        bodySamples: Object.values(extracted.typography.body).slice(0, 8),
      },
      layout: {
        spacingSteps: extracted.spacing.slice(0, 16),
        borderRadii: extracted.radii,
        boxShadows: extracted.shadows,
      },
      cssVariables: extracted.cssVariables,
    };

    // 1. Write tokens JSON
    const jsonPath = path.join(outputDir, "design-tokens.json");
    fs.writeFileSync(jsonPath, JSON.stringify(processedTokens, null, 2), "utf-8");
    console.log(`✅ Exported JSON: ${jsonPath}`);

    // 2. Generate clean CSS Custom Properties
    let cssContent = `/**\n * Auto-Generated Design Tokens from ${targetUrl}\n * Extracted: ${new Date().toISOString()}\n */\n\n:root {\n`;

    // Colors
    cssContent += `  /* --- Extracted Colors --- */\n`;
    processedTokens.colors.backgrounds.slice(0, 8).forEach((c, idx) => {
      cssContent += `  --color-bg-${idx + 1}: ${c.hex};\n`;
    });
    processedTokens.colors.text.slice(0, 6).forEach((c, idx) => {
      cssContent += `  --color-text-${idx + 1}: ${c.hex};\n`;
    });
    processedTokens.colors.borders.slice(0, 4).forEach((c, idx) => {
      cssContent += `  --color-border-${idx + 1}: ${c.hex};\n`;
    });

    // Native CSS Variables if found
    if (Object.keys(processedTokens.cssVariables).length > 0) {
      cssContent += `\n  /* --- Native Site Variables --- */\n`;
      for (const [key, val] of Object.entries(processedTokens.cssVariables)) {
        cssContent += `  ${key}: ${val};\n`;
      }
    }

    cssContent += `}\n`;

    const cssPath = path.join(outputDir, "tokens.css");
    fs.writeFileSync(cssPath, cssContent, "utf-8");
    console.log(`✅ Exported CSS: ${cssPath}`);

    // 3. Generate Tailwind Config Extension
    const tailwindColors = {};
    processedTokens.colors.backgrounds.slice(0, 6).forEach((c, idx) => {
      tailwindColors[`extracted-bg-${idx + 1}`] = c.hex;
    });
    processedTokens.colors.text.slice(0, 4).forEach((c, idx) => {
      tailwindColors[`extracted-text-${idx + 1}`] = c.hex;
    });

    const tailwindConfigContent = `/**\n * Tailwind CSS theme extension\n */\nmodule.exports = {\n  theme: {\n    extend: {\n      colors: ${JSON.stringify(tailwindColors, null, 8).replace(/"([^"]+)":/g, "$1:")},\n    },\n  },\n};\n`;

    const tailwindPath = path.join(outputDir, "tailwind.tokens.js");
    fs.writeFileSync(tailwindPath, tailwindConfigContent, "utf-8");
    console.log(`✅ Exported Tailwind: ${tailwindPath}`);

    console.log(`\n🎉 Design tokens successfully extracted and exported to ${outputDir}!\n`);
  } catch (error) {
    console.error(`❌ Extraction error:`, error);
  } finally {
    await browser.close();
  }
}

// CLI entrypoint
if (process.argv[1] && process.argv[1].endsWith("extract-design-tokens.mjs")) {
  const target = process.argv[2] || "http://localhost:3000";
  const output = process.argv[3] || "./extracted-tokens";
  extractDesignTokens(target, output);
}
