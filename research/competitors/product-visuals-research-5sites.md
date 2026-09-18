# Product Visual Research — 5 Sites (AG1, Bloom, Olipop, Plix, Gelée)

Date: 16 Sep 2026. Done via real browser (claude-in-chrome, now connected — headless Chrome failed on several of these same-category sites in the prior research pass). Explicit trigger: the current `website/index.html` build has zero product imagery — text, tokens, and the ring-dial SVG only. This pass exists specifically to fix that gap before handing off to Codex for the real e-commerce build.

---

## drinkag1.com (AG1)
- Hero: full-bleed flood-green background, dramatic dual-product beauty shot (tube + shaker, condensation droplets, diagonal composition), monospace eyebrow label ("INTRODUCING AG1 PRO"), serif headline.
- **AG1 Essentials Gummies confirmed live** (already flagged in the earlier fork pass — reconfirmed here).
- Proof: trust-badge row (NSF Certified, industry research, athletes, 90-day guarantee), then a 3-card SKU comparison grid — each card has a bulleted benefit checklist plus a **separate "Supplement Facts" link/modal**, not a dense always-visible table. Real UX pattern worth adopting: keep the card scannable, put full disclosure one click away.

## bloomnu.com (Bloom Nutrition)
- Opens with a gamified "mystery discount" quiz popup (countdown timer + "Fitness Fuel / Gut Health / Energy Boost / I'm not sure" buttons) — real personalization-led conversion mechanic, high-energy register.
- **Hero is a product-in-motion action shot**: a stick packet caught mid-pour into a glass, liquid splashing, with real nutrition badges (0g sugar, 1350mg electrolytes, 8 vitamins) visible directly on the pack in the same shot. Chunky rounded display type + handwritten script accent word.

## drinkolipop.com (Olipop)
- **Split hero**: solid color block (headline + CTA) on the left, product photography block on the right — structurally close to what `DESIGN.md` already specifies (left-anchored copy, right-weighted object), even though Olipop's playful hand-drawn floral illustration style is a different register than Eatroz's.
- 3 real cans arranged with a large circular "25% off" promo badge overlaid, condensation droplets for realism.

## plixlife.com (Plix, India)
- Loaded cleanly on the real browser (had failed under headless Chrome in the prior pass — confirms that was an environment/bot-detection issue, not a real access block).
- **Product-in-motion again**: chocolate protein pouch with a dramatic chocolate-splash effect around it, "100% Moneyback Guarantee — Don't like the taste? Get your Refund" badge overlay.
- Dense mega-nav (Build Your Own Box, Shop by Concern/Category/Plant, Kids, Mini Store, New Launches, Gifting, Loyalty) — confirms the earlier text-research finding that major Indian D2C wellness sites read as broad retail platforms, not focused single-product brand sites.

## geleegelee.com (Gelée) — the standout of the five
- **Genuine full-bleed cinematic video hero** (confirmed real motion, not a still — the jelly composition visibly shifted between two screenshots taken seconds apart): translucent jelly molds, dark top-to-bottom gradient vignette, elegant italic serif wordmark, editorial copy overlaid directly on the video ("Gelée is luminous jelly euphoria. Delight for the body, mind, and soul.").
- Further down: genuinely **editorial lifestyle photography** — a vintage metal jelly mold shot on a wooden surface like fine food photography, a dessert glass in natural window light with real shadow play — not catalog/e-commerce shots.
- Monospace product labels (name, serving count, price) with thin underlined text links — restrained, not badge-heavy.
- **This is the closest visual register to Eatroz's own locked "calm, precise, premium" direction of anything researched across every pass so far** — proof that high-end + motion + calm are compatible, not a contradiction, directly relevant to the Next.js/GSAP/Lenis stack conversation.

---

## Synthesis — the actual pattern, repeated 3 times independently

**"Product caught in dynamic motion" is not a one-off technique — it showed up independently at Bloom (pouring), Olipop (implied via droplets/energy), and Plix (splashing) — three unrelated brands, same instinct.** Static, well-lit pack shots are treated as the baseline, not the hero. For Eatroz, the direct equivalent: gummies genuinely in motion (mid-toss, scattering from an open pouch, one gummy held up catching light with the ring-dial's terracotta echoed in a translucent gummy), not a flat product-on-white shot.

**Gelée proves the calm register can still be "high-end e-commerce," not just editorial.** It has a real product grid, real prices, real add-to-cart flow underneath the cinematic hero — the video/editorial treatment doesn't come at the cost of being a working store. This directly answers the tension in the earlier tech-stack conversation: Eatroz doesn't need to choose between "calm brand" and "high-end e-commerce site," Gelée is a live proof point that both can coexist.

**The "Supplement Facts as a separate linked view" pattern (AG1) is worth adopting.** The current `website/index.html` facts panel is always-visible and fairly dense; a lighter always-visible benefit line plus a genuine facts modal/page (ideally styled like LMNT's real data chart, per the earlier 20-site research) would match how the category's best sites actually handle disclosure without sacrificing scannability.

**No product photography exists for Eatroz yet** (confirmed again when answering Claude Design's own question about this a few minutes ago) — everything above is technique and composition reference for when real photography/render assets exist, not a asset source itself.
