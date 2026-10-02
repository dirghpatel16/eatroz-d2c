# Eatroz D2C Product Storefront Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Rebuild `website/` as an original, conversion-first single-product D2C PDP for Eatroz's pouch-format magnesium gummies.

**Architecture:** Next.js 16 App Router renders the static product page and typed product facts. Small React client islands own gallery, preview-pack selection, mobile sticky action, and early-access interaction. Facts fail closed: unverified commercial and supplement details cannot render as approved sale copy. Local Eatroz media is reused; Shopify integration remains an explicit adapter boundary until credentials and verified catalog data exist.

**Tech Stack:** Next.js 16, React 19, TypeScript, Tailwind CSS 4, CSS variables, Vitest, Testing Library, Playwright.

---

## File map

- `website/package.json`, `postcss.config.mjs`, `tsconfig.json`, `next.config.ts`, `eslint.config.mjs`, `vitest.config.ts`, `playwright.config.ts`: toolchain and verification.
- `website/app/layout.tsx`, `page.tsx`, `globals.css`: metadata, server-rendered page, visual system.
- `website/content/product.ts`: pending/verified product contract and local media list.
- `website/components/site-header.tsx`: utility/header navigation.
- `website/components/product-gallery.tsx`: accessible image and thumbnail gallery.
- `website/components/buy-box.tsx`: product identity, preview-pack selector and honest prelaunch action.
- `website/components/lead-panel.tsx`: prelaunch action state without pretending a provider received data.
- `website/components/storefront.tsx`: PDP composition and lower-page sections.
- `website/components/mobile-buy-bar.tsx`: mobile CTA after the main buy box.
- `website/tests/*.test.tsx`, `website/e2e/storefront.spec.ts`: claims and interaction behavior.
- `website/public/media/eatroz/`: copies of selected original Eatroz assets from `assets/media/eatroz/` for local Next asset serving.

## Task 1 — Scaffold and data contract

- [ ] Create the Next.js 16/React 19/Tailwind 4 project configuration and install dependencies. Use the Tailwind PostCSS plugin and `@import "tailwindcss"` per official docs.
- [ ] Write `tests/product.test.ts` first with cases for all pending numeric/commercial facts and verified facts:

```ts
expect(product.price.status).toBe("verification_pending");
expect(product.reviews.status).toBe("verification_pending");
expect(displayFact(product.price)).toBeNull();
expect(displayFact({ status: "verified", value: 899 })).toBe(899);
```

- [ ] Run `npm test -- tests/product.test.ts` and confirm the expected missing-module failure.
- [ ] Implement `ProductFact<T>` and `displayFact` in `content/product.ts`, with all unverified sale/claim fields pending and four local media paths.
- [ ] Re-run the focused test, then `npm run typecheck`.

## Task 2 — Product-detail opening

- [ ] Write `tests/pdp.test.tsx` first. Assert that the page renders a product gallery, title, three labeled bundle **previews**, a visible first-access CTA, and no fake price, reviews or Add to cart.
- [ ] Run the test and confirm it fails because the components do not exist.
- [ ] Implement semantic header, breadcrumb, image gallery, product buy box, and page composition. Desktop uses a 58/42 media/buy grid with sticky product info; mobile stacks gallery above action. Copy states pack and pricing details are not final.
- [ ] Implement gallery selection with button controls and accessible image alt text. Confirm `tests/pdp.test.tsx` passes.

## Task 3 — D2C lower page and action states

- [ ] Write `tests/interactions.test.tsx` first for gallery selection, bundle-preview selection, FAQ disclosure and first-access panel. The panel must say when live registration is not configured.
- [ ] Run focused tests and confirm missing behavior fails.
- [ ] Implement the lower sequence: short assurance strip, sensory imagery, “What to look for” comparison, chewable usage, pending-label facts, FAQ, final product action, footer, and mobile buy bar.
- [ ] Re-run focused tests and the complete unit suite.

## Task 4 — Visual system, media and browser QA

- [ ] Copy only the selected original Eatroz media into the new site and update a provenance manifest. Do not use jar imagery or new invented product packaging.
- [ ] Implement the native system-font visual system in `app/globals.css`: paper, ink, copper, deep green; clean product controls and disciplined 8 px spacing rhythm. No font downloads or full-page scroll hijacking.
- [ ] Write browser tests for the first-screen product/gallery/action hierarchy, mobile CTA, no horizontal overflow, and non-broken images. Run them against `npm run dev`.
- [ ] Inspect desktop and mobile screenshots and fix visual collisions before claiming quality.

## Task 5 — Verification and handoff

- [ ] Run `npm run lint`, `npm run typecheck`, `npm test`, `npm run build`, `npm run test:e2e`, and `git diff --check`; record actual output and exit codes.
- [ ] Re-check rendered copy against pending/verified fields and the originality/compliance guardrails.
- [ ] Keep work on `codex/eatroz-modern-merchant` until the user chooses integration; do not push, deploy, or claim checkout is live without Shopify credentials and verified product data.
