# Free MCP Server Setup Guide for AI Agents

This directory provides the configuration to run **Playwright MCP** and **Chrome DevTools MCP** for 100% free, agentic website extraction and UI reverse-engineering.

---

## 1. What These MCP Servers Do
- **`playwright-mcp`**: Enables your AI agent (in Claude Desktop, Cursor, Windsurf, or Antigravity) to navigate to live websites, click tabs, scroll, capture full-page screenshots, snapshot accessibility DOM trees, and extract computed styles directly.
- **`chrome-devtools-mcp`**: Connects directly to Google Chrome via DevTools protocol to inspect live CSS properties, extract `.woff2` font files, inspect network traffic, and capture layout metrics.

---

## 2. Configuration for AI Clients

### For Claude Desktop (`~/Library/Application Support/Claude/claude_desktop_config.json`)
Add the following under `"mcpServers"`:

```json
{
  "mcpServers": {
    "puppeteer": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-puppeteer"]
    },
    "playwright": {
      "command": "npx",
      "args": ["-y", "@executeautomation/playwright-mcp-server"]
    },
    "fetch": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-fetch"]
    }
  }
}
```

---

## 3. How to Use with AI Agents
Once configured, you can simply ask your AI agent:
- *"Navigate to https://seed.com, take a full page screenshot, and extract all color variables."*
- *"Inspect the hero capsule element on https://seed.com and give me its computed CSS styles and font sizes."*
- *"Reverse-engineer the layout of this page and generate a React + Tailwind component."*

**Cost: $0.00 (Zero API subscriptions, runs completely locally on your machine).**
