# Open-Source AI Web Cloners & Code Generation Suite (100% Free)

This directory contains standalone, 100% free local tools and guides for reverse-engineering websites, converting screenshots to code, and transforming extracted HTML/DOM structures into React + Tailwind CSS components.

---

## 🛠️ Included Local Cloner Tools

### 1. HTML-to-React Component Converter (`html-to-react.mjs`)
Converts raw HTML snippets or extracted DOM nodes into modular React JSX components with proper JSX attributes (`className`, `htmlFor`, `tabIndex`, viewBox, camelCase SVG attributes).
```bash
node tools/cloners/html-to-react.mjs <input.html> [output.tsx]
```
* **Cost:** $0.00 (Zero dependencies, pure AST replacement).
* **Speed:** Instant (< 50ms).

### 2. AI Screenshot-to-Code Cloner (`screenshot-to-code.mjs`)
Takes full-page or component screenshots and generates clean, responsive React + Tailwind CSS components.
```bash
node tools/cloners/screenshot-to-code.mjs <screenshot.png> [output.tsx]
```
* **Modes Supported:**
  - **Local Ollama (Offline & Free):** Automatically detects `http://localhost:11434` with vision models (e.g. `llava`).
  - **Free Gemini API:** If `GEMINI_API_KEY` is set in environment or `~/.config/secrets.env`, uses Google's free Gemini 2.5 Flash tier.
  - **Zero-Key Cloner Bundle:** If no key is set, automatically generates an AI prompt bundle JSON linking the high-DPI screenshot, ready to feed into any free web chat (ChatGPT, Claude.ai, or Gemini).

---

## 🌐 Top Open-Source AI Cloners on GitHub (Zero-Cost Setup)

### 1. `abi/screenshot-to-code` (~60,000 ⭐)
* **GitHub:** [https://github.com/abi/screenshot-to-code](https://github.com/abi/screenshot-to-code)
* **What it does:** Web app + backend that converts screenshots, mockups, or screen recordings into clean Tailwind CSS + React / Vue / HTML code.
* **Quick Clone & Run:**
```bash
git clone https://github.com/abi/screenshot-to-code.git
cd screenshot-to-code/backend
# Works with Ollama, Claude, or OpenAI API keys
```

### 2. `codingstark-dev/decant` (Rust Web Scraper)
* **GitHub:** [https://github.com/codingstark-dev/decant](https://github.com/codingstark-dev/decant)
* **What it does:** Clones the entire visual layer of any website (all CSS, fonts, SVG graphics, and responsive layouts) and rewrites all asset paths so the site renders completely offline.

### 3. `BuilderIO/figma-html` (DOM to Figma Core)
* **GitHub:** [https://github.com/BuilderIO/figma-html](https://github.com/BuilderIO/figma-html)
* **What it does:** The open-source engine powering HTML-to-Figma conversions, converting CSS flexbox rules to Figma auto-layout.

### 4. `open-htmltofigma` (Free Figma Plugin)
* **GitHub:** [https://github.com/kevicebryan/open-htmltofigma](https://github.com/kevicebryan/open-htmltofigma)
* **What it does:** Open-source Figma plugin that takes the `figma-layers.json` exported by our `web-to-figma.mjs` script and imports it directly into Figma frames without any paid subscription.
