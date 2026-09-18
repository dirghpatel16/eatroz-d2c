#!/usr/bin/env node

/**
 * 100% Free AI Screenshot-to-Code Cloner
 * Takes a website screenshot and uses free-tier vision AI (Gemini 2.5 Flash)
 * to generate clean React + Tailwind CSS code.
 */

import fs from "fs";
import path from "path";
import https from "https";

function loadEnvKey() {
  if (process.env.GEMINI_API_KEY) return process.env.GEMINI_API_KEY;
  const secretsPath = path.join(process.env.HOME || "", ".config", "secrets.env");
  if (fs.existsSync(secretsPath)) {
    const lines = fs.readFileSync(secretsPath, "utf-8").split("\n");
    for (const line of lines) {
      const match = line.match(/^\s*GEMINI_API_KEY=["']?([^"'\s]+)["']?/);
      if (match) return match[1];
    }
  }
  return null;
}

export async function cloneScreenshotToCode(imagePath, outputPath, options = {}) {
  const apiKey = loadEnvKey();

  if (!fs.existsSync(imagePath)) {
    throw new Error(`Screenshot file not found: ${imagePath}`);
  }

  console.log(`\n======================================================`);
  console.log(`🤖 AI Screenshot-to-Code Cloner`);
  console.log(`📸 Input Image: ${imagePath}`);
  console.log(`📁 Output Path: ${outputPath}`);
  console.log(`======================================================\n`);

  const imgData = fs.readFileSync(imagePath);
  const base64Img = imgData.toString("base64");
  const ext = path.extname(imagePath).toLowerCase();
  const mimeType = ext === ".png" ? "image/png" : ext === ".webp" ? "image/webp" : "image/jpeg";

  const prompt = `You are a world-class frontend engineer specializing in React, Next.js, and Tailwind CSS.
Look at this website screenshot and reverse-engineer it into a clean, modern, responsive React component.
Requirements:
1. Use semantic HTML (header, main, section, nav, footer, button, etc.).
2. Use modern Tailwind CSS classes for layout, typography, colors, padding, and subtle animations.
3. Match the visual hierarchy, font weights, and spacing as closely as possible.
4. If there are SVG icons or logos in the image, represent them with clean inline SVGs or Lucide-style vectors.
5. Return ONLY the complete, production-ready React component code inside a single tsx codeblock. No conversational preamble.`;

  if (!apiKey) {
    console.log(`ℹ️ No GEMINI_API_KEY found. Checking local Ollama at http://localhost:11434...`);
    try {
      const ollamaRes = await fetch("http://localhost:11434/api/generate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          model: "llava",
          prompt,
          images: [base64Img],
          stream: false,
        }),
      });
      if (ollamaRes.ok) {
        const json = await ollamaRes.json();
        const text = json.response || "";
        const codeMatch = text.match(/```(?:tsx|jsx|javascript|typescript)?\s*([\s\S]*?)```/);
        const finalCode = codeMatch ? codeMatch[1].trim() : text.trim();
        fs.writeFileSync(outputPath, finalCode, "utf-8");
        console.log(`✅ Generated via local Ollama (100% free & offline): ${outputPath}`);
        return finalCode;
      }
    } catch {
      // Ollama not running
    }

    const dir = path.dirname(outputPath);
    if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });

    const bundlePath = outputPath.replace(/\.[^.]+$/, ".bundle.json");
    fs.writeFileSync(
      bundlePath,
      JSON.stringify(
        {
          instruction: prompt,
          imageMime: mimeType,
          imageBase64Length: base64Img.length,
          targetScreenshot: path.resolve(imagePath),
        },
        null,
        2
      )
    );
    console.log(`✅ Prepared 100% free AI cloner bundle: ${bundlePath}`);
    console.log(`👉 Feed ${imagePath} with the prompt into any free AI model (Claude, ChatGPT, Gemini, or Ollama) or set GEMINI_API_KEY for instant terminal generation.`);
    return;
  }

  const payload = JSON.stringify({
    contents: [
      {
        parts: [
          { text: prompt },
          {
            inline_data: {
              mime_type: mimeType,
              data: base64Img,
            },
          },
        ],
      },
    ],
    generationConfig: {
      temperature: 0.2,
      maxOutputTokens: 8192,
    },
  });

  console.log(`⏳ Sending image to Gemini 2.5 Flash Vision...`);

  return new Promise((resolve, reject) => {
    const req = https.request(
      `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key=${apiKey}`,
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Content-Length": Buffer.byteLength(payload),
        },
      },
      (res) => {
        let raw = "";
        res.on("data", (chunk) => (raw += chunk));
        res.on("end", () => {
          if (res.statusCode !== 200) {
            return reject(new Error(`API Error ${res.statusCode}: ${raw}`));
          }
          try {
            const data = JSON.parse(raw);
            const text = data.candidates?.[0]?.content?.parts?.[0]?.text || "";
            const codeMatch = text.match(/```(?:tsx|jsx|javascript|typescript)?\s*([\s\S]*?)```/);
            const finalCode = codeMatch ? codeMatch[1].trim() : text.trim();

            const dir = path.dirname(outputPath);
            if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });

            fs.writeFileSync(outputPath, finalCode, "utf-8");
            console.log(`✅ Code successfully generated and saved to: ${outputPath}`);
            resolve(finalCode);
          } catch (err) {
            reject(err);
          }
        });
      }
    );

    req.on("error", reject);
    req.write(payload);
    req.end();
  });
}

if (process.argv[1] && process.argv[1].endsWith("screenshot-to-code.mjs")) {
  const image = process.argv[2];
  const output = process.argv[3] || "./ClonedComponent.tsx";

  if (!image) {
    console.error("Usage: node screenshot-to-code.mjs <screenshot.png> [output.tsx]");
    process.exit(1);
  }

  cloneScreenshotToCode(image, output).catch((err) => {
    console.error("❌ Cloning failed:", err.message);
    process.exit(1);
  });
}
