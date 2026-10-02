# Eatroz D2C storefront preview

Next.js 16 / React 19 single-product storefront, built around the original Eatroz pouch. Start locally with `npm install && npm run dev`, then open <http://localhost:3000>.

## Current state

- Product gallery, pouch-plan preview, first-access flow, product education, comparison checklist, FAQ, and responsive sticky action are implemented.
- Pricing, serving size, elemental magnesium, ingredients, FSSAI details, reviews, checkout, and delivery are **not live or verified**. The UI deliberately does not invent them. See `content/product.ts` for the fact contract.
- Without a lead provider, first access saves only non-personal preview interest in that browser. It does not collect email or register anyone. To enable actual email registration, set HTTPS `EATROZ_WAITLIST_WEBHOOK_URL` and `EATROZ_PRIVACY_URL`, plus optional `EATROZ_WAITLIST_WEBHOOK_TOKEN`. The webhook must return a success response only after it persists the registration. Add bot protection and provider-side rate limiting before a public campaign.
- Gallery media is copied from the project-owned `assets/media/eatroz/`; hashes and caveats are in `public/media/eatroz/README.md`.
- The site is set `noindex` while it is a preview.

## Before a public sale

1. Approve the final pouch artwork and legally compliant on-pack copy.
2. Verify formulation, serving, nutritional panel, cautions, FSSAI information, price, tax, shipping and returns.
3. Create the real Shopify product/variants and connect checkout to actual catalog data. The pack cards are only previews until then.
4. Connect and test a real lead provider, publish the privacy notice, and add bot protection before accepting public signups.
5. Replace `noindex`, add privacy/terms/customer support pages, and re-run the full verification suite.

## Verification

`npm run lint`, `npm run typecheck`, `npm test`, `npm run build`, and `npm run test:e2e`.

## Design tooling used

The local Codex skills installation includes [Taste Skill](https://github.com/Leonxlnx/taste-skill) (`taste-skill`, `redesign-skill`), [Anthropic Frontend Design](https://github.com/anthropics/skills/tree/main/skills/frontend-design), and [Marketing Skills](https://github.com/coreyhaines31/marketingskills) (`cro`, `copywriting`). They guided the visual and conversion audit, but no third-party storefront layout or artwork was copied. Eatroz's existing pouch direction, system-font preference, factual product claims, and accessible buying flow take precedence over generic skill recipes.
