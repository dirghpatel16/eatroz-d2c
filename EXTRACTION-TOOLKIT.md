# Eatroz 100% Free UI & Design Extraction Toolkit

An enterprise-grade, local, and **100% free** web UI extraction pipeline built directly into this repository. No subscriptions, no paid APIs, no rate limits.

---

## 🛠️ Quick Commands

Run any of the following commands from the `website/` directory:

```bash
# 1. Complete Full Extraction (Tokens + Assets + Screenshots + Figma)
npm run extract:all <target_url>

# 2. Extract Design Tokens & CSS Variables Only
npm run extract:tokens <target_url>

# 3. Harvest All SVGs, Web Fonts (.woff2), and Product Images
npm run extract:assets <target_url>

# 4. Capture Multi-Viewport High-DPI Screenshots (Desktop, Tablet, Mobile)
npm run extract:screens <target_url>

# 5. Export DOM to Editable Figma Layers JSON
npm run extract:figma <target_url>
```

---

## 📁 What Each Tool Extracts

### 1. Design Token & Style Extractor (`extract-design-tokens.mjs`)
- Runs local Playwright headless Chromium.
- Crawls every visible element in the DOM and extracts computed styles.
- **Outputs:**
  - `design-tokens.json`: All background colors, text colors, and border colors sorted by frequency; typography scales (H1–H6, body, weights); spacing steps; border-radii; and CSS variables.
  - `tokens.css`: Standard CSS Custom Properties (`--color-bg-1`, `--color-text-1`, etc.) ready to paste into `globals.css`.
  - `tailwind.tokens.js`: Ready-to-use Tailwind theme configuration extension.

### 2. Asset Harvester (`harvest-assets.mjs`)
- Intercepts network responses and downloads:
  - **Inline & Linked Vector SVGs** (saved as individual `.svg` files).
  - **Original Web Fonts** (`.woff2`, `.woff`, `.ttf` files downloaded directly).
  - **High-Res Product Images** (`.webp`, `.png`, `.jpg`).

### 3. Multi-Viewport Capture (`capture-viewports.mjs`)
- Renders and screenshots full-page layouts at three viewports:
  - **Desktop:** `1440x900` @ 2x DPI
  - **Tablet:** `768x1024` @ 2x DPI
  - **Mobile:** `390x844` @ 3x Retina DPI
- Ideal for pixel-perfect design comparisons or feeding into vision models.

### 4. Free Web-to-Figma Exporter (`web-to-figma.mjs`)
- Recursively converts DOM nodes, bounding rects, background fills, font styles, and flexbox AutoLayout settings into Figma-compatible JSON (`figma-layers.json`).
- **How to Import into Figma for $0:**
  1. In Figma, open any file.
  2. Open the free community plugin **"Open HTML to Figma"** (open-source) or the free tier of **"HTML to Design"**.
  3. Select "Import JSON" and choose `figma-layers.json`.
  4. All frames, typography, and vector layers will be created natively in your Figma canvas!

---

## 🤖 Free MCP Server Configuration (Playwright MCP)

To give an AI agent (in Claude Desktop, Cursor, or Antigravity) direct, automated browser control and extraction capabilities without paid services:

1. Open your AI client configuration:
   - **Claude Desktop:** `~/Library/Application Support/Claude/claude_desktop_config.json`
   - **Cursor:** `.cursor/mcp.json`
2. Add the Playwright MCP server:

```json
{
  "mcpServers": {
    "playwright": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-playwright"]
    }
  }
}
```

3. Ask your agent:
   > *"Navigate to the target website, extract its design tokens, and generate a Next.js component matching its layout."*

---

## 🔒 100% Free Guarantee
- Uses local **Playwright** (`1.63.0`) already installed in your dev dependencies.
- Zero paid scraping APIs.
- Zero Figma subscription requirements.
- Unlimited local runs.
