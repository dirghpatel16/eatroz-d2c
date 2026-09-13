# Research Tooling Reference — for Claude Code and Codex

*Written 12 Sep 2026. Companion to `HANDOFF.md` — read that first for project context. This file is specifically about what research tooling was used, what's genuinely free, what actually works when tested (not just in theory), and what still needs the user's action. Keep this updated as tools are added or tested.*

---

## Already installed, zero setup, works in either tool

These are plain files on this machine's PATH — any shell-capable agent (Claude Code or Codex CLI) can call them directly, right now, with no configuration.

| Tool | Path | What it does | Cost |
|---|---|---|---|
| `yt-transcript` | `~/.local/bin/yt-transcript` | Verbatim YouTube captions (yt-dlp), falls back to local Whisper if no captions | Free |
| `yt-video-ask` | `~/.local/bin/yt-video-ask` | Sends a YouTube URL + question to **Gemini**, which reads audio AND visuals (slides, on-screen text, charts) — the single highest-value tool used in this project | Free tier of Gemini API (`GEMINI_API_KEY` in `~/.config/secrets.env`) |
| `make-pdf` | `~/.claude/skills/gstack/make-pdf/dist/pdf` | Renders markdown → publication-quality PDF (cover page, TOC, page numbers) | Free, local binary |

Usage:
```bash
yt-transcript <URL>
yt-video-ask <URL> "targeted question about the video"
~/.claude/skills/gstack/make-pdf/dist/pdf generate --cover --toc input.md output.pdf
```
If `make-pdf` ever isn't reachable from a given environment, `pandoc file.md -o file.pdf` is the portable fallback.

---

## Free, public, no login — usable right now, but with real limits (tested, not assumed)

| Tool | What it's good for | Actual tested limitation |
|---|---|---|
| **Zauba Corp** (zaubacorp.com) | Looking up an Indian company's legal entity name, CIN, registered address, incorporation date, authorized/paid-up capital | Direct page fetch returned **HTTP 403** when tried directly — go through a web search first to land on the right company page via a search snippet, rather than fetching the URL directly. Financial filings shown are often **stale** (tested: only showed data through FY23 for a company whose FY25 revenue was needed) — do not rely on this for current-year revenue, only for entity identity and older filings. |
| **Google Patents** (patents.google.com) | Free, no login, useful for a partial global trademark/IP pre-check | Not tested in this project yet — worth trying before assuming it works smoothly |
| **WIPO Global Brand Database** (branddb.wipo.int) | International trademark search | **Tested and blocked** — the search results page sits behind an interactive CAPTCHA (an "altcha-widget" challenge) that cannot be automated by either Claude or Codex. A human has to open it in a real browser and click through. Don't attempt to automate this again — it's a confirmed dead end for agent access. |
| **AmbitionBox** (ambitionbox.com) | Real, India-specific, often company-specific salary data (better than generic aggregators like Payscale for this use case) | Not yet tested for scraping resistance in this project — try a direct fetch first |
| **Meta Ad Library** (facebook.com/ads/library) | Manually browsable, no login, for viewing any brand's current live ad creative | **This is the correct tool, confirmed — not a fallback.** See the resolved finding below; the API cannot do what we need here. |
| **India's official trademark portal** (tmrsearch.ipindia.gov.in) | The actual authoritative India trademark search | **Confirmed blocked for agent use** — now requires OTP login to a real email/mobile number. Neither Claude nor Codex should attempt this; it needs the user directly. |

---

## Free tier, but requires the user to sign up (5 minutes each, no card needed for the ones marked so)

| Service | Free tier | Sign-up | What it unlocks |
|---|---|---|---|
| **Composio** | Free tier for individual use; the Exa-backed web search toolkit didn't need extra OAuth once connected in this project | composio.dev → create an MCP connection, get the MCP server URL/key | `COMPOSIO_SEARCH_WEB` (dated, citation-backed search — much better than plain web search for grading claims), `COMPOSIO_SEARCH_FETCH_URL_CONTENT` (full clean page text) |
| **Tavily** | 1,000 free API calls/month, no card required | tavily.com → dashboard gives an API key immediately | A second, independent search backend — genuinely useful for cross-checking a claim Composio/Exa returned, since they sometimes disagree |
| ~~**Meta for Developers**~~ | — | **Dead end — see the resolved finding below. Do not pursue this for Indian commercial-ad monitoring.** | — |

**Once these keys exist, here's how they get wired in (this session's plan, not yet executed — waiting on the user to grab the keys):**
- **Claude Code:** MCP servers are added via the `claude mcp add` command or a plugin's marketplace entry; config lives in `~/.claude.json` under `mcpServers`. Current entries there: `stitch`, `composio`, `ruflo`.
- **Codex CLI:** MCP servers go in `~/.codex/config.toml` under `[mcp_servers.<name>]` blocks (command/args/env). A `config.toml` already exists there (600 permissions, not read/exposed in this process) — new entries should be **appended**, not replacing anything already configured.

---

## Not free — skip, or use the free consumer version instead

| Service | Why skipped | Free alternative |
|---|---|---|
| Perplexity Sonar **API** | Paid, no free API tier | The regular perplexity.ai web chat has a free tier — usable manually for a one-off second opinion, just not scriptable |
| Tofler (deep financials) | Paid tier needed for anything beyond basic lookup | Zauba Corp's free tier for entity/CIN identity; accept that recent-year revenue verification for private Indian companies is genuinely hard to get for free |
| CMIE Consumer Pyramid Household Survey | Enterprise-priced | The already-cited secondary sources (NFHS, ICMR-INDIAB, Redseer press summaries) are the free substitute — lower resolution, but real |

---

## PROVEN IN PRODUCTION: the Composio + Tavily combo, used together, is the real 10x upgrade

*Not theoretical anymore — this was actually used for a real, high-stakes research task (13 Sep 2026: responding to an internal founder meeting, verifying five brand names, finding an unlisted competitor, and pinning down a load-bearing product-feasibility claim). Recording what actually worked so it's used this way by default going forward, in either Claude Code or Codex.*

- **Composio's `COMPOSIO_SEARCH_WEB`** (Exa-backed) is what surfaced the single most important finding of that session — AG1 CEO Kat Cole's on-record "you can't put AG1, as it is, in a gummy" quote, with full context (15-gummy figure, the "Essentials" simplification, still needing 8 gummies) — from a citation trail of dated LinkedIn posts a plain search would likely have missed or under-sourced. It also found BiteBella (a real, reviewed, live competitor the founders didn't know existed) directly from a garbled brand-name guess ("Belly Bite or Bite Belly"), and pulled genuinely current (2026) LinkedIn commentary from Indian D2C operators on exactly the topics being researched — this is the single best source type for "what does someone actually building this right now think" that nothing else in this toolset replicates.
- **`COMPOSIO_SEARCH_FETCH_URL_CONTENT`** pulled a competitor's full live site (BiteBella) in one call — pricing, review counts, founder bios, customer testimonials verbatim — turning a "go look at their website" task into one tool call.
- **Tavily's `tvly` CLI is the better choice specifically for Reddit** — confirmed again in this session (see the corrected finding below the domain-availability section) and used again productively here for cross-checking claims Composio's Exa backend didn't independently confirm.
- **Direct verification beats trusting either tool's synthesis.** The transcript this research responded to claimed five brand names had "domains and trademarks available." A live `curl`/RDAP check (not a search tool at all) found four of the five were actually registered. **Lesson: for anything with a concrete, checkable state (domain availability, a specific fact, a claimed data point), verify directly — a search tool's synthesized answer is not a substitute for checking the actual thing.** This is the same discipline that caught the Sanode "20 countries" fabrication earlier in this project — it's a repeatable pattern, not a one-off catch.

## RESOLVED: Meta Ad Library API is a dead end for Indian commercial-ad monitoring — use the website instead

*This was genuinely uncertain earlier in this project (two blog sources disagreed on whether commercial-brand monitoring was even a valid use case). It's now resolved with a live app-creation attempt plus Meta's own official documentation at facebook.com/ads/library/api — not another blog. Don't re-litigate this.*

**The Ad Library API's data scope, verbatim from Meta's own page, covers only:**
1. Ads about social issues, elections, or politics — worldwide, past 7 years
2. Ads of *any* type — but only if delivered to the **UK or EU**

**It does not cover ordinary commercial ads delivered to India, or anywhere outside UK/EU, unless they're political/social-issue ads.** Man Matters, Plix, OZiva, Bodywise, Kapiva — none of their ordinary product-marketing ads qualify. This makes the entire developer-app route (app type, use case, identity verification — all the things debated earlier in this project) moot: no configuration of the app changes the underlying data scope.

**Confirmed live, not just from docs:** a fresh Meta developer app (type: Business, correctly configured) was created and its "Available products" list checked directly — there is no "Ads Library API" product to add at all. Access to `ads_archive` is a direct Graph API call, not a product you set up, and it's gated by the scope limits above regardless.

**Meta's own page states the correct tool for our actual need, verbatim:** *"To search for all ads currently running across Meta technologies, please use the Ad Library"* (the regular website, not the API).

**Conclusion — don't build the API integration. Use facebook.com/ads/library manually** (or scripted browser automation against the public website, if scheduled monitoring is wanted later) for tracking Man Matters/Plix/OZiva/etc. ad creative. It needs no signup, no ID verification, no app — and it's the tool Meta itself points to for this exact use case.

## The honest state of "10x research," as actually tested in this project

Three of the free-tier tools were tried live during this session and all three hit real, worth-knowing limits — recorded here so the next session doesn't re-discover the same walls:
1. **Zauba Corp free tier ≠ current-year financials.** It's excellent for confirming a company's legal identity (which matters — several Indian brands trade under a different registered name than their consumer brand name, e.g. Wellbeing Nutrition = Nutritionalab Private Limited) but the free public view lags well behind the most recent filing year. Treat it as an identity/older-filing tool, not a live-revenue tool.
2. **WIPO's Global Brand Database is CAPTCHA-gated and cannot be automated.** Don't retry this with a different URL pattern or user-agent — it's a deliberate bot-block, not a fixable request issue. Trademark clearance searches need a human in a real browser, full stop — this applies to India's own portal too (OTP-gated).
3. **Meta's Ad Library API doesn't cover Indian commercial ads at all** — confirmed via a live app-creation attempt plus Meta's own docs (full detail above). Don't build a Meta developer-app integration for this; the plain website already does the job for free.

**Both Composio and Tavily are now live and confirmed working in this project — in Claude Code and in Codex CLI.** Composio registered cleanly with Bearer-token auth (`COMPOSIO_API_KEY` env var, not a raw value in Codex's config.toml); Tavily is fully OAuth-authenticated in Codex and was already separately authenticated in Claude Code (`tvly auth` confirmed the same key predates this session). Both keys live only in `~/.config/secrets.env` (owner-read-only). This is genuinely the highest-leverage upgrade from this whole list — everything else here is either a confirmed dead end (Zauba beyond identity lookup, WIPO, Meta Ad Library API) or free-and-already-working with zero setup (AmbitionBox, Google Patents, the website version of Meta's Ad Library). Don't spend more time chasing paid tiers (Tofler, Perplexity API, CMIE) unless a specific research question genuinely can't be answered any other way.
