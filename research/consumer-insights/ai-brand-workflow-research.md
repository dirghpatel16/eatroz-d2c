# AI Brand-Building Workflow Research — Campaign Visuals, Landing Pages, Codex

Date: 15-16 Sep 2026. Direct follow-up to `brand-research-batch-us-sleep-and-ai-workflow.md` (which covered general Claude Design brand-system workflows) — this pass targets the three specific angles asked for: AI-generated campaign visuals pre-launch, building a branded (not generic) landing page, and building with Codex specifically. Two of three planned videos analyzed via the Gemini pipeline; the third (a "build a brand in 14 minutes" video) hit the Gemini API's daily free-tier request cap (20/day on `gemini-3.6-flash` — the same key used all session) and wasn't retried, per the standing instruction to keep usage economical. Two videos is enough real signal for what follows.

---

## Building a branded (not generic) landing page with Claude Code

Video: "How to Build Landing Pages With Claude Code (No Coding)" ([youtube.com/watch?v=j9pqqLHQ2XQ](https://www.youtube.com/watch?v=j9pqqLHQ2XQ))

**The actual workflow, in order:**
1. VS Code + Claude Code extension, Opus 4.6, **Extended Thinking OFF** for this kind of task (worth noting — thinking mode isn't automatically better for design generation).
2. Load a **design Skill** before generating anything — either Anthropic's own public `frontend-design` skill, or a custom one with hardcoded brand rules (exact hex colors, exact font pairing, explicit layout principles). This is the single most load-bearing step for avoiding a generic result — **we already have the equivalent of this**, `DESIGN.md`, and it should be fed into any landing-page generation the same way.
3. **Give it a real reference URL to emulate**, not just a text description — "feeding a live, successful reference landing page URL into the prompt forces Claude to match proven spacing, hero height, card grid layouts, and visual hierarchy." Concretely actionable for `/design-html`: pick a real, well-built wellness/supplement landing page (Ritual's or Seed's, per our own research) as an explicit reference anchor in the prompt, not just describe the vibe.
4. Iterate locally via `file://` preview, then publish via GitHub + Cloudflare Pages (free, instant public URL) — a real, concrete, low-cost path to an actual live URL once a page is built, worth keeping in mind for when Eatroz's site is ready to go beyond local preview.

**The real prompt template used** (adapted structure, directly reusable):
```
Use the [Brand] Design skill. Build me a landing page for [product].
Use [reference URL] as the starting point for design, branding, layout.
Product details: [name, price, tagline]
Context: [paste real product content/copy]
```

**What actually separates "branded" from "generic AI slop," per this video, stated explicitly:** hardcoded CSS color variables (not "pick something nice"), named exact typography pairs, explicit design principles stated as rules ("minimal borders, high contrast"), and a real reference anchor. All four of these already exist in `DESIGN.md` — the gap isn't the system, it's that `/design-html` hasn't been run with an explicit reference-site anchor yet (Ritual or Seed would be the obvious pick, per our earlier research).

## Building with Codex specifically — how its design process actually differs from Claude's

Video: "Codex: Build Stunning Frontends with AI" ([youtube.com/watch?v=XEGLQ59fYwY](https://www.youtube.com/watch?v=XEGLQ59fYwY))

**The real, structural difference, not just a vibe difference:**

| | Codex | Claude (chat-based) |
|---|---|---|
| Execution | Runs the page in a live browser itself | Outputs code for the user to run |
| Visual verification | **Takes its own screenshots** across desktop/mobile, compares against the design goal, self-corrects | Needs the user to look and report back |
| Debugging | Uses browser dev tools autonomously to fix layout bugs | Relies on the user pasting errors/screenshots back |

**Workflow shown:** sketch (even a literal whiteboard photo) → upload as a multimodal input alongside a text prompt → Codex identifies what it needs (e.g., picks `Three.js` for a 3D element on its own) → generates → **screenshots its own output at multiple viewport sizes and iterates without being asked to.**

**Direct implication for our Claude+Codex team pipeline (the one we designed two sessions ago):** this changes the division of labor I originally proposed. I assumed Codex's role would be text-based review only (`codex exec` reading `DESIGN.md` and critiquing). But Codex can apparently **visually self-verify against a design reference autonomously** — meaning a stronger version of the pipeline is: Codex builds the actual `/design-html` implementation and self-checks it against a screenshot of the approved direction, rather than only reviewing something I already built. Worth trying directly next time we build the website, not just theorizing about it.

---

## Net changes to the plan, from this research

1. **`/design-html` should be run with an explicit reference-site anchor** (Ritual or Seed, per prior research) in the prompt, not just `DESIGN.md`'s tokens alone — this video's "reference URL" technique is a concrete, low-effort upgrade to how we were going to do it.
2. **Reconsider Codex's role in the team pipeline** — it may be capable of more than independent critique; its visual self-correction loop suggests it could co-build the website, not just review it.
3. **A real, free path to a live public URL exists** (GitHub + Cloudflare Pages) for whenever a working page needs to go beyond local preview — noted for when that's actually needed, not urgent now.

---

## Addendum — 2 Instagram reels, analyzed via the same Gemini pipeline

User shared 3 Instagram links. Instagram video isn't natively fetchable by Gemini's URL-resolution the way YouTube is (`yt-video-ask`'s direct-URL approach failed with an API error on the first attempt) — fixed by downloading via `yt-dlp` (which does support Instagram) and uploading the file directly to Gemini's File API, then running the same audio+visual analysis. One of the three links (a static post, not a reel) was confirmed on the first pass to be unrelated engagement-bait content, not analyzed further.

### Reel 1 — "Chompa" brand-build case study (branding agency reel)
A full 8-week brand-build process, shown step by step with real on-screen deliverables at each stage — the closest real-world analog to what we're doing for Eatroz, worth using as a structural template:

- **Week 1 — Discovery:** four core questions (What are your products? Who is it for? Why should they care? Who are you competing with?) plus a brand-personality slider exercise (Feminine↔Masculine, Playful↔Serious, Economical↔Expensive, etc.) — a concrete, reusable tool for pinning down Eatroz's own personality more precisely than prose alone.
- **Week 3 — Strategy:** a full deliverable set shown on-screen — Company Profile, Archetype (they used "Expert + Entertainer"), Positioning Statement (What/Who/Where/Why), Mission, Purpose, Manifesto, two named Buyer Personas with demographics, and a Brand Venn Diagram (Audience × Product × Story × Personality → "Your Brand"). **Eatroz has positioning and audience defined in prose across several files, but not consolidated into this single-page format** — worth doing as a `eatroz-brand-strategist` exercise, since it would surface gaps fast.
- **Moodboards + naming, done together, 3 directions each:** each visual direction shipped with matched name candidates (e.g., "The Showstopper" direction → Nutfetti/Chompa/Snacklet), not chosen separately — a useful process note for any future naming work if the Troz conflict forces a rename.
- **Week 5 — Logo concepts:** 3 genuinely distinct directions (warm/nostalgic, bold/whimsical, edgy/stretched), then **Week 7 combined the winning wordmark from one concept with the color palette from another** rather than picking a single concept wholesale — a real, reusable technique: synthesis across shortlisted directions, not forced single-choice.
- **Week 8 — Delivery:** a complete brand book (logo variations, color system, typography — three distinct type roles named: header/product-name face, body-copy face, claims/secondary-info face — icons, art direction, ad mockups across print/outdoor/digital, website design, vector source files). This maps closely onto what `DESIGN.md` + the brand-team skills already cover, but confirms the real deliverable list a "complete brand" needs — our packaging spec and copy skills are two pieces of this; a formal brand-book document consolidating everything is not yet one of our artifacts.

### Reel 2 — "Luxury AI Ad" demo (Vaseline, AI-generated product video)
Less directly relevant to brand-building, but genuinely useful for eventual campaign-visual work: shows a single static product photo transformed into a 7-shot, ~9-second "luxury" product video via an AI video-generation prompt (the reel displays its own generation prompt on-screen as part of the hook). **Real, named tells for spotting (and avoiding) AI-video artifacts, worth knowing before Eatroz ever produces its own AI ad creative:** text on labels going slightly soft/wavy under macro close-up, lighting reflections with "mathematically perfect" uniformity lacking real environmental bounce, liquid/gel surfaces staying rigid instead of showing natural physical dynamics, and camera movement that's unnaturally steady without the micro-vibration real macro rigs have. If Eatroz ever generates AI product video, these are the specific things to check for and smooth over before publishing — the difference between looking premium and looking obviously synthetic is in these details, not the overall concept.
