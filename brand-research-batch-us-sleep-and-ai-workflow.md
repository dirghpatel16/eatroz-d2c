# US Sleep-Brand Visual Research + AI Brand-Building Workflow

Date: 15 Sep 2026. Small, targeted addition — done inline (not via parallel subagents) after the first research pass, scoped tightly rather than padded to a round number, per explicit steer to keep usage economical without cutting quality. See `brand-competitive-visual-research.md` (first pass, 15 brands) and `brand-research-batch-india-sleep.md` (India sleep-category batch) for the rest.

---

## US Sleep Brands (visual identity)

### Beam (sleep supplement)
- Category default: sleep supplements lean earthy greens/purples/blues for "calm," rounded soft sans-serif type "like a warm hug."
- Beam's real distinct move isn't packaging — it's product *format*: turning the supplement into a bedtime-ritual object (a hot-cocoa-style mix, not a pill/gummy), making the ritual itself the differentiator rather than the graphic language.
- Source: [Sarah Sherr — visual identity for wellness brands](https://www.sarahsherrphoto.com/los-angeles-photography-insights/how-to-set-up-visual-identity-health-wellness-brands), [Splash Creative — premium supplement branding](https://splashcreative.com/how-to-make-supplement-brand-look-premium/)

### Eight Sleep (sleep tech, not supplement, but the category's most-cited brand identity)
- Current identity: monochrome black-and-white, heavy geometric serif wordmark with enlarged square serifs — reads as strength/precision, part of a deliberate pivot to a "sleep fitness" (performance, not softness) positioning.
- Earlier iteration used whites/greys with a light purple accent for calm — they moved AWAY from that toward the current cold, technical register.
- Identity concept ties to moon-phase iconography (the "8" = 8 hours) and LCD/sports-jersey visual references.
- Source: [1000logos.net](https://1000logos.net/eight-sleep-logo/), [Brand New / Under Consideration](https://www.underconsideration.com/brandnew/archives/new_logo_and_identity_for_eight_sleep_by_interesting_development.php)

### Casper (mattress, adjacent category, strong brand-consistency case study)
- Deep navy wordmark, rounded/bubbly friendly sans-serif, pastel-light color system — approachable rather than clinical.
- Cited stat: visual consistency across collateral is linked to real revenue lift (up to 23%) — a concrete argument for enforcing DESIGN.md discipline once the website ships.
- Source: [DesignRush](https://www.designrush.com/best-designs/print/casper-s-illustrated-subway-ads), [Looka — mattress logos](https://looka.com/blog/mattress-logo-design/)

**Synthesis, sleep-category-specific (cross-referencing the India batch's finding):** across both markets, sleep brands split into two lanes — "engineering/performance" (Eight Sleep's cold monochrome) or "generic soft wellness" (Beam, most Indian competitors) — and nobody has built a genuinely *calm, low-stimulation, designed-to-be-the-last-thing-you-see-before-bed* visual language. The India batch's independent finding reinforces this: **a specific, disciplined dusk/indigo hue, owned the way Sleepy Owl owns blue in Indian D2C coffee, is a real open lane nobody in either market has claimed.** Worth naming honestly even though it sits in tension with the already-locked sage/terracotta — not a recommendation to reopen that decision, but a genuine finding the founders should be aware of if this space ever gets revisited (e.g., for a night-specific sub-line or packaging variant).

---

## AI Brand-Building Workflow Research (your explicit ask: how people use Claude/Codex for full brand identity)

Real finding, not previously known to this project: **Claude Design (`claude.ai/design`)** is Anthropic's actual product for exactly this — upload brand assets once, every subsequent generation (logo system, packaging, web page, slide deck, print) inherits them automatically. Two real workflow videos analyzed via the Gemini video pipeline (audio + on-screen text, not captions):

### Video 1 — "How to Build a Complete Brand Identity Using Claude Design" ([youtube.com/watch?v=lmlw2GFjI80](https://www.youtube.com/watch?v=lmlw2GFjI80))
Workflow: draft a detailed spec prompt (deliverables, exact hex codes, type pairings, tone, explicit *exclusions* like "no calming gradients") → Claude Design "High Fidelity" prototype mode → paste prompt → ~6 minutes compiles a full multi-artboard system (cover/hero, logo + monogram + secondary lockup, color palette with usage *ratios*, typography + data panel, packaging label flats + die-lines, print/editorial piece, website hero).

**The actual prompt used in the video, worth using as a direct template for an Eatroz version:**
> "Design a complete brand identity for [brand], a [category] whose [differentiator]. The tone is [3 adjectives] — [analogy], not [cliché to avoid]. No [anti-pattern 1], no [anti-pattern 2].
> Present as a design canvas with labeled artboards: Cover — [wordmark treatment + texture + caption style] / Logo system — primary wordmark, monogram cut from [motif], secondary lockup with [tagline] / Palette — N-swatch palette with usage ratios and a one-line philosophy / Typography — display specimen + a data/ingredient panel in mono / Packaging — label flats + die-line / Print — one editorial piece / Website hero — [mood].
> Palette: [exact hex list]. Type: [display font] for display, [sans] for labels, [mono] for data/batch numbers. Motifs: [specific, named visual devices]. No [explicit exclusion, e.g. hand-drawn SVG illustration] — use [alternative]."

This maps almost exactly onto Eatroz's own locked system (sage/terracotta hexes, Fraunces + Inter + mono, the ring-motif-as-data-device) — DESIGN.md is already written in a compatible shape to become this kind of prompt directly.

### Video 2 — "How to Build a Brand Design System with AI" ([youtube.com/watch?v=MaGyfnie9WI](https://www.youtube.com/watch?v=MaGyfnie9WI))
Different entry point: a browser extension ("Branding Capture") extracts an existing reference site's CSS/colors/fonts into a `branding-kit.zip`, which Claude Design ingests directly to bootstrap a design system — then generates, off that one system: a full website, a slide deck (as a lead-magnet PDF), and a separate ad-focused landing page, all traceable back to the same tokens. Export options: PDF, PPTX, standalone HTML, or ZIP.

**Direct implication for Eatroz:** since DESIGN.md already exists with real hex/type/spacing values (not a reference site to scrape), the more relevant path is Video 1's — write one comprehensive Claude-Design prompt directly from DESIGN.md's tokens, get logo system + packaging + web hero + print piece as one coherent multi-artboard output, then hand the approved direction to `/design-html` for the real, working website (Pretext-native, not a static Claude Design mockup).

**Recommendation:** next concrete step, if you want to act on this, is trying Claude Design directly with a prompt built from DESIGN.md — likely faster and higher-fidelity than continuing to lean on the gstack `$D` tool, which is blocked on a missing OpenAI key anyway.
