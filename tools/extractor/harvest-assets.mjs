#!/usr/bin/env node

/**
 * Eatroz / Open-Source UI Extraction Toolkit
 * Asset Harvester: Downloads SVGs, Web Fonts (.woff2), and Product Images.
 * 100% Free & Open Source.
 */

import { chromium } from "@playwright/test";
import fs from "fs";
import path from "path";
import https from "https";
import http from "http";

function downloadFile(url, dest) {
  return new Promise((resolve, reject) => {
    const client = url.startsWith("https") ? https : http;
    const req = client.get(
      url,
      {
        headers: {
          "User-Agent":
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
          Accept: "*/*",
        },
        timeout: 10000,
      },
      (res) => {
        if (res.statusCode >= 300 && res.statusCode < 400 && res.headers.location) {
          const redirectUrl = new URL(res.headers.location, url).href;
          downloadFile(redirectUrl, dest).then(resolve).catch(reject);
          return;
        }
        if (res.statusCode !== 200) {
          reject(new Error(`Failed with HTTP ${res.statusCode}`));
          return;
        }
        const file = fs.createWriteStream(dest);
        res.pipe(file);
        file.on("finish", () => {
          file.close();
          resolve();
        });
        file.on("error", (err) => {
          fs.unlink(dest, () => {});
          reject(err);
        });
      }
    );
    req.on("error", (err) => {
      fs.unlink(dest, () => {});
      reject(err);
    });
    req.on("timeout", () => {
      req.destroy();
      fs.unlink(dest, () => {});
      reject(new Error("Timeout"));
    });
  });
}

export async function harvestAssets(targetUrl, outputDir = "./extracted-assets") {
  console.log(`\n======================================================`);
  console.log(`📦 Harvesting Assets from: ${targetUrl}`);
  console.log(`📁 Saving to: ${outputDir}`);
  console.log(`======================================================\n`);

  const svgDir = path.join(outputDir, "svgs");
  const fontDir = path.join(outputDir, "fonts");
  const imgDir = path.join(outputDir, "images");

  [outputDir, svgDir, fontDir, imgDir].forEach((d) => {
    if (!fs.existsSync(d)) fs.mkdirSync(d, { recursive: true });
  });

  const fontUrls = new Set();

  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({
    userAgent:
      "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
  });

  const page = await context.newPage();

  page.on("response", (response) => {
    const url = response.url();
    if (url.endsWith(".woff2") || url.endsWith(".woff") || url.endsWith(".ttf")) {
      fontUrls.add(url);
    }
  });

  try {
    await page.goto(targetUrl, { waitUntil: "domcontentloaded", timeout: 30000 });
    await page.waitForTimeout(2000);

    console.log(`🎨 Extracting inline vector SVGs...`);
    const svgs = await page.evaluate(() => {
      return Array.from(document.querySelectorAll("svg")).map((svg, index) => {
        const id = svg.getAttribute("id") || svg.getAttribute("class") || `icon-${index + 1}`;
        return {
          id: id.replace(/[^a-zA-Z0-9_-]/g, "_").slice(0, 30),
          xml: svg.outerHTML,
        };
      });
    });

    svgs.forEach((item, idx) => {
      const filename = path.join(svgDir, `${idx + 1}_${item.id}.svg`);
      fs.writeFileSync(filename, item.xml, "utf-8");
    });
    console.log(`✅ Saved ${svgs.length} SVG assets to ${svgDir}`);

    console.log(`🖼️ Extracting image sources...`);
    const imgUrls = await page.evaluate(() => {
      const urls = new Set();
      document.querySelectorAll("img").forEach((img) => {
        if (img.src && !img.src.startsWith("data:")) urls.add(img.src);
      });
      return Array.from(urls);
    });

    console.log(`Found ${imgUrls.length} image resources. Downloading...`);
    let imgCount = 0;
    for (const url of imgUrls.slice(0, 15)) {
      try {
        const ext = path.extname(new URL(url).pathname) || ".webp";
        const dest = path.join(imgDir, `img_${imgCount + 1}${ext}`);
        await downloadFile(url, dest);
        imgCount++;
      } catch {
        // Skip
      }
    }
    console.log(`✅ Downloaded ${imgCount} images to ${imgDir}`);

    console.log(`🔤 Intercepted ${fontUrls.size} web fonts.`);
    let fontCount = 0;
    for (const fontUrl of fontUrls) {
      try {
        const ext = path.extname(new URL(fontUrl).pathname) || ".woff2";
        const dest = path.join(fontDir, `font_${fontCount + 1}${ext}`);
        await downloadFile(fontUrl, dest);
        fontCount++;
      } catch {
        // Skip
      }
    }
    console.log(`✅ Downloaded ${fontCount} font files to ${fontDir}`);

    console.log(`\n🎉 Asset harvesting completed successfully!\n`);
  } catch (error) {
    console.error(`❌ Asset harvest error:`, error);
  } finally {
    await browser.close();
  }
}

if (process.argv[1] && process.argv[1].endsWith("harvest-assets.mjs")) {
  const target = process.argv[2] || "http://localhost:3000";
  const output = process.argv[3] || "./extracted-assets";
  harvestAssets(target, output);
}
