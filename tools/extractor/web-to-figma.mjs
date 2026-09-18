#!/usr/bin/env node

/**
 * Eatroz / Open-Source UI Extraction Toolkit
 * Web-to-Figma JSON Generator
 * Converts live web DOM elements to Figma-compatible node structures.
 * 100% Free & Open Source (Compatible with free Figma JSON import plugins).
 */

import { chromium } from "@playwright/test";
import fs from "fs";
import path from "path";

export async function exportWebToFigma(targetUrl, outputDir = "./extracted-figma") {
  console.log(`\n======================================================`);
  console.log(`🎨 Exporting Web DOM to Figma Layers for: ${targetUrl}`);
  console.log(`📁 Output Directory: ${outputDir}`);
  console.log(`======================================================\n`);

  if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir, { recursive: true });
  }

  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({
    viewport: { width: 1440, height: 900 },
  });
  const page = await context.newPage();

  try {
    await page.goto(targetUrl, { waitUntil: "domcontentloaded", timeout: 30000 });
    await page.waitForTimeout(1500);

    const figmaTree = await page.evaluate(() => {
      function rgbToFigmaColor(rgbStr) {
        if (!rgbStr || rgbStr === "transparent" || rgbStr === "rgba(0, 0, 0, 0)") return null;
        const match = rgbStr.match(/rgba?\((\d+),\s*(\d+),\s*(\d+)(?:,\s*([\d.]+))?\)/);
        if (!match) return null;
        return {
          r: parseInt(match[1]) / 255,
          g: parseInt(match[2]) / 255,
          b: parseInt(match[3]) / 255,
          a: match[4] !== undefined ? parseFloat(match[4]) : 1,
        };
      }

      function domNodeToFigma(el, depth = 0) {
        if (depth > 6) return null;
        const rect = el.getBoundingClientRect();
        if (rect.width === 0 || rect.height === 0) return null;

        const style = window.getComputedStyle(el);
        if (style.display === "none" || style.visibility === "hidden") return null;

        const isText = el.childNodes.length === 1 && el.childNodes[0].nodeType === Node.TEXT_NODE;
        const bgColor = rgbToFigmaColor(style.backgroundColor);
        const textColor = rgbToFigmaColor(style.color);

        const classStr = typeof el.className === "string" ? el.className : el.className?.baseVal || "";
        const classSelector = classStr.trim() ? `.${classStr.trim().split(/\s+/)[0]}` : "";

        const node = {
          name: el.tagName.toLowerCase() + (el.id ? `#${el.id}` : classSelector),
          type: isText ? "TEXT" : "FRAME",
          x: Math.round(rect.x),
          y: Math.round(rect.y),
          width: Math.round(rect.width),
          height: Math.round(rect.height),
          fills: bgColor ? [{ type: "SOLID", color: { r: bgColor.r, g: bgColor.g, b: bgColor.b }, opacity: bgColor.a }] : [],
          strokes: [],
          cornerRadius: parseFloat(style.borderRadius) || 0,
        };

        if (isText) {
          node.characters = el.textContent.trim();
          node.fontSize = parseFloat(style.fontSize) || 16;
          node.fontFamily = style.fontFamily.split(",")[0].replace(/['"]/g, "").trim();
          node.fontWeight = parseInt(style.fontWeight) || 400;
          if (textColor) {
            node.fills = [{ type: "SOLID", color: { r: textColor.r, g: textColor.g, b: textColor.b }, opacity: textColor.a }];
          }
        } else {
          if (style.display === "flex") {
            node.layoutMode = style.flexDirection.includes("column") ? "VERTICAL" : "HORIZONTAL";
            node.itemSpacing = parseFloat(style.gap) || 0;
            node.paddingTop = parseFloat(style.paddingTop) || 0;
            node.paddingBottom = parseFloat(style.paddingBottom) || 0;
            node.paddingLeft = parseFloat(style.paddingLeft) || 0;
            node.paddingRight = parseFloat(style.paddingRight) || 0;
          }

          const children = [];
          for (const child of Array.from(el.children)) {
            const childNode = domNodeToFigma(child, depth + 1);
            if (childNode) children.push(childNode);
          }
          node.children = children;
        }

        return node;
      }

      return domNodeToFigma(document.body);
    });

    const outputPath = path.join(outputDir, "figma-layers.json");
    fs.writeFileSync(outputPath, JSON.stringify(figmaTree, null, 2), "utf-8");
    console.log(`✅ Saved Figma Node Tree: ${outputPath}`);

    const readmeContent = `# Free Web-to-Figma Import Guide

This directory contains \`figma-layers.json\`, a structured Figma node tree extracted from **${targetUrl}**.

## How to Import into Figma for 100% Free:
1. Open Figma and create a new design file.
2. In Plugins, search for **"Open HTML to Figma"** (open-source) or the free tier of **"HTML to Design"**.
3. Select "Import JSON" and choose \`figma-layers.json\`.
4. All frames, typography layers, text nodes, and flex Auto-Layouts will be imported as native, editable Figma vectors!
`;
    fs.writeFileSync(path.join(outputDir, "README.md"), readmeContent, "utf-8");
    console.log(`✅ Saved Free Import Guide: ${path.join(outputDir, "README.md")}`);

    console.log(`\n🎉 Web-to-Figma extraction complete!\n`);
  } catch (error) {
    console.error(`❌ Figma export error:`, error);
  } finally {
    await browser.close();
  }
}

if (process.argv[1] && process.argv[1].endsWith("web-to-figma.mjs")) {
  const target = process.argv[2] || "http://localhost:3000";
  const output = process.argv[3] || "./extracted-figma";
  exportWebToFigma(target, output);
}
