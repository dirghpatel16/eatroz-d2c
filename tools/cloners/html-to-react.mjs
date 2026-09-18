#!/usr/bin/env node

/**
 * 100% Free HTML-to-React/Tailwind Component Cloner
 * Parses extracted HTML/DOM elements and converts them into modular React JSX components
 * using Tailwind CSS styling tokens.
 */

import fs from "fs";
import path from "path";

export function htmlToReactComponent(htmlContent, componentName = "ExtractedComponent") {
  // Clean comments and doctypes
  let cleaned = htmlContent
    .replace(/<!--[\s\S]*?-->/g, "")
    .replace(/<!DOCTYPE.*?>/gi, "");

  // Convert HTML attributes to JSX equivalents
  cleaned = cleaned
    .replace(/\bclass="/g, 'className="')
    .replace(/\bfor="/g, 'htmlFor="')
    .replace(/\btabindex="/g, 'tabIndex="')
    .replace(/\bautocomplete="/g, 'autoComplete="')
    .replace(/\bviewbox="/gi, 'viewBox="')
    .replace(/\bstrokewidth="/gi, 'strokeWidth="')
    .replace(/\bstrokelinecap="/gi, 'strokeLinecap="')
    .replace(/\bstrokelinejoin="/gi, 'strokeLinejoin="')
    .replace(/\bfillrule="/gi, 'fillRule="')
    .replace(/\bcliprule="/gi, 'clipRule="');

  // Self-close void tags (img, input, br, hr)
  cleaned = cleaned
    .replace(/<(img|input|br|hr)([^>]*?)(?<!\/)>/gi, "<$1$2 />");

  const componentCode = `import React from "react";

export function ${componentName}() {
  return (
    <div className="${componentName.toLowerCase()}-wrapper w-full">
      ${cleaned.trim()}
    </div>
  );
}

export default ${componentName};
`;

  return componentCode;
}

if (process.argv[1] && process.argv[1].endsWith("html-to-react.mjs")) {
  const inputFile = process.argv[2];
  const outputFile = process.argv[3] || "./ExtractedComponent.tsx";

  if (!inputFile || !fs.existsSync(inputFile)) {
    console.error("Usage: node html-to-react.mjs <input.html> [output.tsx]");
    process.exit(1);
  }

  const html = fs.readFileSync(inputFile, "utf-8");
  const compName = path.basename(outputFile, path.extname(outputFile));
  const jsx = htmlToReactComponent(html, compName);

  fs.writeFileSync(outputFile, jsx, "utf-8");
  console.log(`✅ Converted ${inputFile} -> ${outputFile}`);
}
