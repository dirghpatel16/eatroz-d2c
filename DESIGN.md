# Design System — Eatroz

Built via `/design-consultation`, 15 Sep 2026. Formalizes and extends `eatroz-brand-design-system.md` (the founders' locked positioning/palette/type call) with the technical layer needed to actually build the pitch deck, packaging, and website off one system. Grounded in `brand-competitive-visual-research.md` (15-brand India+US competitive research) and a "design outside voices" pass (Codex + an independent Claude subagent each proposed a direction; synthesis below).

## Product Context
- **What this is:** Eatroz — a D2C magnesium gummy supplement brand (India launch first). The brand spans packaging, a pitch deck, and an upcoming website.
- **Who it's for:** 18-35, premium "India-1" income bracket, D2C-literate, price-tolerant at ₹899-999/pack but skeptical of unproven wellness claims.
- **Space/industry:** Indian wellness/supplement D2C, competing directly with Man Matters and Be Bodywise (magnesium gummies), and against Bubble Me (magnesium-led, no gummy SKU yet).
- **Project type:** Brand system spanning physical packaging + marketing site + pitch deck (not a software app — spacing/layout/motion sections below are written for the website).

## Aesthetic Direction
- **Direction:** Botanical Clinical — "a quiet mineral laboratory brought into a warm Indian home." Calm, evidentiary, warm — not sterile, not a wellness-spa pastel cliché.
- **Decoration level:** Intentional. A single recurring diagrammatic motif (the tree-ring/mineral cross-section) carries real information; no decorative pattern-filling.
- **Mood:** Confident and precise, never hype. The brand's whole differentiator is naming exact chemical forms and stating "0% Magnesium Oxide" where competitors hide it — the aesthetic should look like it has nothing to hide, not like it's trying to look "natural."
- **Reference points:** Ritual and Seed (US) — made transparency a *structural* design principle, not a marketing line. Cymbiotika — proof that publishing real lab data (COAs) is a legitimate premium trust mechanic, not just a claim. The Whole Truth (India, ₹2000 Cr) — transparency as literal headline, not footnote. Deliberately avoiding: Man Matters/Be Bodywise's single-saturated-hero-color register, Moon Juice/Olly's whimsical hand-drawn mark, and Goli's candy-color saturation (documented consumer backlash — real Reddit complaint that it "hurts to see").

### Outside-voices synthesis (how this direction was chosen)
Codex (read-only pass over the repo) recommended keeping the locked warm sage/terracotta/Fraunces direction and sharpening it toward proof — concrete layout ideas below are largely Codex's. An independent Claude subagent pushed back harder, arguing sage+Fraunces+soft-serif is becoming its own "coastal-wellness" cliché by 2026 and proposed a colder, forensic "Assay Report" register (near-black ground primary, oxide-red, a technical monospace leading the hierarchy instead of serif). **Decision:** rejected the full cold-register pivot — this is a *sleep* product, and evening-ritual warmth is load-bearing to the positioning ("Sleepmaxxing, done properly"), so a lab-instrument-cold register would undercut it to chase a differentiation that suits a biohacker/productivity brand more than a wind-down one. Took the subagent's sharpest idea in modified form: a technical monospace as a secondary "evidence voice" for data only (dosage, %RDA, chemical forms), inside the warm palette rather than replacing it. Both voices and the competitive research independently converged on one thing, now locked below as the signature device: the ring motif must become functional (a real %RDA data-dial), not decorative.

## Signature Device — The Ring Dial
This is the single most important new decision from today's research, cited independently by the competitive research, Codex, and the subagent (Seed's "dot" precedent: a logo mark re-engineered to function as a data lens across the whole brand).

- The tree-ring/mineral-cross-section "O" is not decoration — it is Eatroz's data instrument.
- **Primary use:** a concentric filled-arc ring showing elemental magnesium dose as %RDA (like a progress ring) — on packaging, on the product page hero, and anywhere the wordmark's "O" appears at sufficient size.
- **Secondary uses:** the same ring device as a batch/freshness or test-verification seal; as a loading/progress indicator on the website if one is ever needed.
- **Construction:** fine near-black (`--ink`) concentric line rings on `--sage`/`--canvas`, with exactly one ring segment or the center fill rendered in `--terracotta` to show the filled proportion. The %RDA number sits at the center in the monospace data face, tabular-nums.
- **Never:** purely decorative use once the brand has a real product page — if a ring appears, it should be doing data work, not just echoing the logo.

## Proof & Trust Conventions (non-negotiable — carried forward from `eatroz-brand-design-system.md` §5, plus one new addition)
- State exact chemical forms (glycinate, citrate, malate, taurate) — never just "Magnesium."
- Explicit **"0% Magnesium Oxide"** on front/immediate sub-headline.
- Exact %RDA per serving on-pack and on the product page, not buried.
- **New, from Reddit research 15 Sep 2026:** a genuine tamper-evident seal (induction seal under the cap, or proper shrink band) — never a peelable holographic sticker. Real, named consumer complaints against Man Matters/Be Bodywise call their holographic seal out as reading fake ("always looks like someone has peeled off"). This is a documented, exploitable trust gap, not a design nicety — spec it directly to Softpills.
- No delivery-tech brand name (e.g. "MagnaSorb") until Softpills confirms what's actually licensable.
- No specific manufacturing/facility claims until independently verified.

## Typography
- **Display/Hero:** Fraunces (soft optical size), weight 600-700 for headlines, 400 italic for the ritual/emotional line ("Sleepmaxxing, done properly."). Carries the warmth and the brand's one moment of softness.
- **Body:** Inter — tight tracking, used for all paragraph copy and UI labels.
- **UI/Labels:** Inter, uppercase, letter-spacing .04-.09em for kickers/eyebrows (matches the deck's existing `.kicker` convention).
- **Data/Tables (new):** IBM Plex Mono or JetBrains Mono, tabular-nums — the "evidence voice." Use ONLY for dosage numbers, %RDA, chemical-form labels, prices, and the ring-dial center label. Never for headlines or body copy — this is a deliberate, bounded departure from the locked Fraunces+Inter-only rule in `eatroz-brand-design-system.md`, scoped narrowly so it reads as "proof," not as a third competing voice.
- **Loading:** Google Fonts CDN (`fonts.googleapis.com`) — Fraunces and Inter already loaded this way in `deck/index.html`; add Plex Mono/JetBrains Mono the same way.
- **Scale** (rem, 16px base):
  | Step | Size | Use |
  |---|---|---|
  | display-xl | clamp(2.8rem, 8vw, 5.6rem) | Cover/hero wordmark |
  | display-lg | clamp(1.9rem, 4vw, 2.6rem) | Section titles |
  | display-md | 1.5rem | Card/subsection titles |
  | body-lg | 1.1rem | Lede paragraphs |
  | body | 1rem | Default body copy |
  | body-sm | .82rem | Secondary/caption text |
  | data-lg | 2.2rem | Ring-dial center number, big stats |
  | data | .82rem tabular | Table rows, dosage labels |
  | label | .68-.72rem, uppercase, tracked | Kickers, eyebrows |

## Color
- **Approach:** Restrained — one accent (terracotta), color is rare and meaningful, never scattered.
- **Primary surface:** `#E7ECE3` (sage) — pack background, primary page surface.
- **Canvas:** `#F7F5F0` (warm off-white) — negative space, secondary surface.
- **Accent:** `#C1552F` (terracotta) — appears once per composition as a strong block (spine, ring segment, CTA), never as flooded color. Deep variant `#8F3F22` for hover/pressed states.
- **Ink:** `#1C1B18` (near-black) — all type, line-art motif.
- **Ink-soft:** `#55524A` — secondary/muted text.
- **Stone:** `#D8D2C4` — dividers, table borders. Supporting neutral, never a second hero color.
- **Semantic** (new, needed for the website forms/states — chosen to sit inside the existing palette rather than import generic red/green/amber):
  - Success: `#5C7A54` (a desaturated moss, sage's darker cousin)
  - Warning: `#B8863B` (muted amber, warmer than terracotta so it doesn't collide with the brand accent)
  - Error: `#A3382A` (deeper, cooler red than terracotta — visually distinct so error states never read as "brand accent")
  - Info: `#55524A` (same as ink-soft)
- **Dark mode:** already implemented and shipping in `deck/index.html` — reuse exactly, do not reinvent:
  - `--sage: #2B3128; --sage-deep: #4C5A44; --terracotta: #E6835A; --terracotta-deep: #B85A34;`
  - `--canvas: #1C1B18; --ink: #F3EFE6; --ink-soft: #B7B0A0;`
  - `--stone: #47433a; --surface: #242320; --line: #3c3830;`
  - Strategy: swap, don't just darken — sage becomes a true dark olive ground, ink flips to warm cream text, terracotta brightens (`#E6835A`) to hold contrast against the dark ground.

## Spacing
- **Base unit:** 8px.
- **Density:** Spacious/comfortable — generous negative space is part of the "calm, not sterile" mood; matches the deck's existing clamp()-based padding.
- **Scale:** 2xs(4) xs(8) sm(12) md(16) lg(24) xl(32) 2xl(48) 3xl(64) 4xl(96)

## Layout
- **Approach:** Hybrid — creative-editorial for hero/marketing moments (asymmetric, poster-style first viewport, left-anchored copy with a right-weighted ring/object, per Codex's proposal), grid-disciplined for proof/data sections (the "apothecary grid" pattern from Be Bodywise's research finding — a repeatable, tabular layout for dosage/facts, direct web equivalent of the deck's existing `.facts` component).
- **Grid:** 12-column desktop, single-column stack under 760px.
- **Max content width:** 1240px (matches `deck/index.html`'s `.slide-inner` for visual continuity between deck and website).
- **Border radius:** Deliberately near-zero. The deck already uses sharp-edged bordered cards (1-1.5px solid borders, no rounding) as part of the clinical-not-cutesy register — continue this on the website. Scale: sm(2px) md(4px) lg(6px) full(9999px, dots/badges only). This is a real departure from most DTC sites' rounded-everything default — worth keeping deliberately, not softening later "to look more modern."

## Motion
- **Approach:** Minimal-functional. The brand's confidence comes from restraint, not choreography — motion should aid comprehension (the ring dial filling in on scroll/load is the one deliberate animated moment worth having), never decorate.
- **Easing:** enter(ease-out) exit(ease-in) move(ease-in-out)
- **Duration:** micro(80ms) short(200ms) medium(350ms) — no "long" tier; nothing on this brand should take longer than 350ms to resolve.

## Decisions Log
| Date | Decision | Rationale |
|---|---|---|
| 15 Sep 2026 | DESIGN.md created via `/design-consultation` | Formalizes `eatroz-brand-design-system.md`, adds technical layer (spacing/layout/motion/dark-mode tokens already proven in `deck/index.html`) |
| 15 Sep 2026 | Ring motif upgraded from decorative to functional (%RDA data-dial) | Independently proposed by competitive research, Codex, and an independent Claude subagent — three-way convergence treated as a strong signal |
| 15 Sep 2026 | Added IBM Plex Mono/JetBrains Mono as a bounded "evidence voice" for data only | Synthesis of the subagent's monospace-forward proposal, scoped narrowly to avoid diluting Fraunces+Inter as the primary voice |
| 15 Sep 2026 | Added tamper-evident seal requirement to Proof & Trust Conventions | Real Reddit complaints found Man Matters/Be Bodywise's holographic peel-seal reads as fake to Indian consumers — documented, exploitable trust gap |
| 15 Sep 2026 | Rejected full "cold/forensic" register pivot proposed by outside-voices subagent | This is a sleep product — evening-ritual warmth is load-bearing to "Sleepmaxxing, done properly"; kept sage/terracotta/Fraunces as primary |
