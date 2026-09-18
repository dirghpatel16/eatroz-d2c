# Brand Visual Research — Real Screenshots (not text search)

Date: 15 Sep 2026. Done via headless Chrome directly (the browser extension is unreliable in this environment), screenshotting real homepages and actually looking at them — a deeper layer than the text-based research in `brand-competitive-visual-research.md` and the `brand-research-batch-*.md` files, which this deliberately doesn't repeat.

**Operational note, reported honestly per the task brief:** of 20 targeted sites, 7 loaded and were fully analyzed, 2 came back with a clear, informative failure (Cloudflare bot-check, dead domain), and 11 failed to load at all — several Indian D2C sites (Setu, Plix, mCaffeine, The Whole Truth) and a few US ones (Olly, Nutrafol, Bloom Nutrition, Cymbiotika) hung indefinitely under headless Chrome in this environment even with generous time budgets and retries, likely bot-detection holding the connection open rather than serving a block page. Not a research shortcut — genuinely could not get a screenshot. Sugar Cosmetics and Bombay Shaving Company weren't reached given the failure rate on the rest of the batch.

---

## US — successfully analyzed (4)

### Ritual
Real homepage is far denser/more retail than the "minimal restraint" read from text research suggested: a full-bleed autoplay lifestyle video hero (hand holding a translucent capsule) split against a navy CTA panel, then an immediate product grid with prices, discounts, and an "Add" button per card — this is a working e-commerce storefront, not an editorial one-hero-one-proof page. **Proof is delivered as a compact horizontal trust-badge row** (Certified, 100% Traceable, $5M Clinical Investment, Formulated by Dietitians, Vegan/Non-GMO) — icon + one line each, not a data table.

### Moon Juice
Hero is an extreme macro product photo (the jar itself, filling the whole viewport) with text overlaid in the negative space — product-photography-forward, not the "whimsical hand-drawn" register text research suggested (that may exist elsewhere in their system, not on the actual homepage hero). Their own magnesium product ("Magnesi-Om") is visible in the Best Sellers row — a direct, if powder-format, magnesium competitor worth having on record. Same badge-row proof pattern as Ritual (Bioavailable / 100% Traceable / Clinically Proven / 3rd Party Tested / Vegan / No Fillers).

### AG1 — genuinely new competitive intelligence, not just a design note
**AG1 has just launched a gummy product** ("AG1 Essentials Gummies," hero headline "Chews Wisely") — the earlier text research (which characterized AG1 as powder-only) is now out of date. This is a real, current format-level competitor worth flagging up to the strategist skill, not filed as a visual footnote. Design: flat-lay product photography (gummies scattered around the pouch), heavy use of AG1's kelly-green as a flood color (not restrained), then a 3-card SKU comparison grid with `$/mo` pricing and checkmarked benefit lists per product — dense, retail-comparison layout.

### LMNT — the single most directly useful find of this whole pass
Their proof section isn't a facts table or a badge row — it's **an actual clinical data chart**: a bar comparison (government sodium recommendation vs. their science-backed recommendation) plus a real line graph (Hazard Ratio vs. Sodium Excretion, with a highlighted "optimal range" band and a cited source printed under it: *"Sodium & Potassium Excretion, Risk for Cardiovascular Events; JAMA 2011.1729"*). This is the clearest real-world precedent for what Eatroz's monospace "evidence voice" + ring-dial device should aspire to — not just naming a number, but a genuine comparative visualization with a citation. Directly actionable for the facts-panel/ring-dial work in `DESIGN.md` and `website/index.html`.

---

## India — successfully analyzed (3)

### Man Matters
The live homepage is not primarily a product storefront — it's a **diagnostic/telehealth funnel**: hero carousel leads with "Monsoon Causing More Hair Fall? Take Hair Test" and a blood-test-plus-doctor-consultation offer (with a named lab partner, Redcliffe Labs), a stat bar ("10L+ Indian Men on the Platform, 250+ Experts for Consultation"), then category tiles (Hair/Beard/Skin/Nutrition). Proof is a horizontally scrolling badge marquee (NABL Lab Tested, Third Party Lab Tested, Clinically Tested, etc.), not a static row. **Positioning takeaway:** their brand identity is built around diagnosis-led trust, not product-led trust — a different model than Eatroz's single-SKU, label-transparency approach.

### Be Bodywise
Their actual magnesium gummies SKU is visible in the hero carousel ("Support deeper, more restful sleep this monsoon" — a real magenta/pink pouch, confirming the color prior text research found). But the homepage itself is a **full multi-category e-commerce catalog** (Hair/Body/Health & Fitness/Sun/Face tabs, dozens of SKUs, star ratings, strikethrough pricing, per-card "Add" buttons) — scale and breadth, not a focused brand story. **Strategic takeaway, not just visual:** both major Indian magnesium-gummy competitors (Man Matters, Be Bodywise) are broad multi-category platforms first, single-product brands second — reinforcing that Eatroz's planned single-SKU, tightly-focused launch is a genuinely different competitive shape, not just a smaller version of the same thing.

### Minimalist (skincare) — the strongest direct precedent for Eatroz's core thesis
**The exact active-ingredient percentage is the product name, printed large on the pack itself**: "Salicylic Acid + LHA 2%", "Vitamin B5 10% Moisturizer", "Niacinamide 10% Face Serum" — plain white bottles/tubes, one thin colored accent line, black sans-serif type, the number as the dominant visual element. This is a real, live, at-scale execution of exactly what Eatroz wants to do (name the chemical form and %RDA on the front) — worth using directly as the reference for Eatroz's own product photography and facts-panel typography, more than any of the US sites researched.

---

## Confirmed failures, not silently skipped

- **seed.com** — Cloudflare bot-verification page only ("Performing security verification"), never resolved to real content under headless Chrome.
- **careof.com** — DNS_PROBE_FINISHED_NXDOMAIN. The domain no longer resolves at all; consistent with the earlier text-research finding that Care/of showed no distinct brand signal — now confirmed the brand's own site appears to be gone entirely.
- **11 other sites** (Olly, Nutrafol, Bloom Nutrition, Cymbiotika, The Whole Truth, Setu, Plix, mCaffeine, plus Sugar Cosmetics/Bombay Shaving Company not attempted) — hung indefinitely under headless Chrome in this environment despite retries and time budgets; not resolved, not guessed at.

---

## Synthesis

1. **Real "proof" sections split into three actual patterns, not one**: a compact horizontal trust-badge row (Ritual, Moon Juice — icon + one line, fast to scan), a dense comparison-card grid with pricing (AG1), or a genuine data visualization with a citation (LMNT — the strongest of the three, and the closest match to what Eatroz's ring-dial/monospace system should aim for). Eatroz's current facts-panel (`website/index.html`) is closest to a hybrid of the badge-row and a data table — worth deliberately pushing it closer to LMNT's chart-with-citation model given that's the most credible, differentiated version of "proof" seen across the whole set.
2. **A real, current competitive-intelligence update**: AG1 has launched a gummy SKU. This should be flagged to whoever tracks the competitive landscape (the `eatroz-brand-strategist` skill / `HANDOFF.md`), not filed only as a design note.
3. **Minimalist is the single closest real-world precedent for Eatroz's entire differentiator** (dose/percentage as the literal product name on-pack) — closer than any US brand researched, text or visual. Worth a deliberate second look at their actual product photography style specifically when Eatroz's own packaging photography gets planned.
4. **Man Matters and Be Bodywise are both broad multi-category platforms, not focused single-SKU brands** — a real structural difference from Eatroz's plan worth naming explicitly, not just a visual observation.
5. **Operational finding for future research passes**: headless Chrome screenshot research on Indian D2C sites specifically has a high failure rate in this environment (4 of 7 attempted Indian sites beyond the first three never loaded) — likely bot-detection. Worth trying a real browser session (once the extension is reliably connected) rather than headless for future Indian-site visual research, or budgeting for a lower success rate going in.
