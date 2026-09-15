# Eatroz E-commerce Redesign Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a visual-first, switchable pre-launch/live-launch Eatroz storefront with a Runway-generated `Four Forms Fall` hero, honest product data states, and verified desktop/mobile behavior.

**Architecture:** Replace the monolithic static prototype with a Next.js App Router application composed around a typed product-content contract. Presentation components consume a fail-closed commerce configuration; pre-launch lead capture and live checkout are adapters, so neither mode requires duplicated markup. Generated media is stored in a manifest and remains replaceable without component edits.

**Tech Stack:** Next.js 16.3.5, React 19.3.0, TypeScript 5.9.3, GSAP 3.15.0, Lenis 1.3.26, Vitest 5.0.1, Testing Library 16.3.3, Playwright 1.63.0, axe-core Playwright 4.13.0. Lenis is progressively enhanced only for fine-pointer devices without reduced-motion; native scrolling remains the fallback.

---

## File Map

Create this structure under `website/`:

```text
website/
  app/
    api/leads/route.ts          # Validated lead webhook adapter; fails closed when unconfigured
    globals.css                 # Tokens, responsive layout, reduced-motion rules
    layout.tsx                  # Metadata, fonts, global shell
    page.tsx                    # Ordered eight-section storefront composition
    privacy/page.tsx            # Lead-capture privacy disclosure
    terms/page.tsx              # Pre-launch and live commerce terms surface
  components/
    commerce/
      cart-drawer.tsx           # Single-product quantity and checkout surface
      lead-drawer.tsx           # Pre-launch capture UI and retry state
      purchase-dock.tsx         # Mode-aware first-screen commercial module
      sticky-mobile-cta.tsx     # Persistent post-hero mobile conversion action
    facts/facts-disclosure.tsx  # Accessible Supplement Facts disclosure
    formula/exploded-formula.tsx# Seek-safe four-form scroll story
    gallery/product-gallery.tsx # Product media gallery
    hero/hero-film.tsx          # Video/poster fallback and playback controls
    motion/smooth-scroll.tsx    # Guarded Lenis lifecycle and native fallback
    proof/oxide-proof.tsx       # Evidence visualization and source treatment
    trust/trust-section.tsx     # Pre-launch/live trust content gating
    storefront.tsx              # Client orchestration for drawers and sticky CTA
  content/product.ts            # Typed, claim-safe product content
  lib/commerce/config.ts        # Commerce mode parsing and fail-closed defaults
  lib/commerce/checkout.ts      # Approved checkout URL builder
  lib/leads/submit.ts           # Lead request client
  scripts/build-media-manifest.mjs # Hashes and dimensions for generated assets
  media-production/runway-generation-log.md # Model, generation ID, decision, and credit ledger
  public/media/eatroz/
    source/eatroz-pouch-reference.png
    hero-four-forms-fall-poster.webp
    hero-four-forms-fall.mp4
    pouch-beauty.webp
    gummy-macro.webp
    ritual-evening.webp
    manifest.json
  tests/
    commerce-config.test.ts
    content-safety.test.ts
    hero-film.test.tsx
    purchase-dock.test.tsx
    lead-route.test.ts
    storefront.test.tsx
    smooth-scroll.test.tsx
  e2e/storefront.spec.ts
  eslint.config.mjs
  next.config.ts
  package.json
  playwright.config.ts
  tsconfig.json
  vitest.config.ts
  vitest.setup.ts
```

The current `website/` prototype is user-owned and untracked in the main worktree. Leave it untouched there. Build the replacement only inside the feature worktree; branch integration later requires an explicit reconciliation of that untracked directory so Git never overwrites it silently.

### Task 1: Create an Isolated Worktree and Scaffold the App

**Files:**
- Modify: `.gitignore`
- Create: `website/package.json`
- Create: `website/tsconfig.json`
- Create: `website/next.config.ts`
- Create: `website/eslint.config.mjs`
- Create: `website/vitest.config.ts`
- Create: `website/vitest.setup.ts`
- Create: `website/playwright.config.ts`

- [ ] **Step 1: Create the isolated worktree**

Run from the repository root:

```bash
apply_patch <<'PATCH'
*** Begin Patch
*** Update File: .gitignore
@@
+.worktrees/
*** End Patch
PATCH
git check-ignore -q .worktrees
git add .gitignore
git commit -m "chore: ignore agent worktrees"
git worktree add .worktrees/eatroz-storefront -b feat/eatroz-storefront HEAD
```

Expected: `git check-ignore` exits 0, and a clean worktree exists at `.worktrees/eatroz-storefront` on `feat/eatroz-storefront`, based on the commit containing this plan. If `.gitignore` already ends with `.worktrees/`, skip the patch and commit. The untracked prototype and research files in the main worktree remain untouched; inspect them read-only by absolute path when needed.

For Steps 2 onward, change directory to `/Users/dirghpatel/Documents/india-gummy-d2c/.worktrees/eatroz-storefront`; every relative path in the remainder of this plan is rooted there.

- [ ] **Step 2: Scaffold the tracked application in the isolated worktree**

Create `website/package.json`:

```json
{
  "name": "eatroz-storefront",
  "private": true,
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "lint": "eslint .",
    "test": "vitest run",
    "test:watch": "vitest",
    "test:e2e": "playwright test"
  },
  "dependencies": {
    "gsap": "3.15.0",
    "lenis": "1.3.26",
    "next": "16.3.5",
    "react": "19.3.0",
    "react-dom": "19.3.0"
  },
  "devDependencies": {
    "@axe-core/playwright": "4.13.0",
    "@playwright/test": "1.63.0",
    "@testing-library/jest-dom": "6.9.1",
    "@testing-library/react": "16.3.3",
    "@types/node": "22.19.8",
    "@types/react": "19.2.14",
    "@types/react-dom": "19.2.3",
    "eslint": "10.10.0",
    "eslint-config-next": "16.3.5",
    "jsdom": "30.0.1",
    "typescript": "5.9.3",
    "vitest": "5.0.1"
  }
}
```

Create `website/tsconfig.json`:

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "lib": ["dom", "dom.iterable", "esnext"],
    "allowJs": false,
    "skipLibCheck": true,
    "strict": true,
    "noEmit": true,
    "esModuleInterop": true,
    "module": "esnext",
    "moduleResolution": "bundler",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "jsx": "react-jsx",
    "incremental": true,
    "plugins": [{ "name": "next" }],
    "paths": { "@/*": ["./*"] }
  },
  "include": ["next-env.d.ts", "**/*.ts", "**/*.tsx", ".next/types/**/*.ts"],
  "exclude": ["node_modules"]
}
```

Create `website/next.config.ts`:

```ts
import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  poweredByHeader: false,
  images: { formats: ["image/avif", "image/webp"] },
};

export default nextConfig;
```

Create `website/eslint.config.mjs`:

```js
import { defineConfig, globalIgnores } from "eslint/config";
import nextVitals from "eslint-config-next/core-web-vitals";
import nextTs from "eslint-config-next/typescript";

export default defineConfig([
  ...nextVitals,
  ...nextTs,
  globalIgnores([".next/**", "playwright-report/**", "test-results/**"]),
]);
```

Create `website/vitest.config.ts`:

```ts
import { defineConfig } from "vitest/config";
import path from "node:path";

export default defineConfig({
  test: { environment: "jsdom", setupFiles: ["./vitest.setup.ts"] },
  resolve: { alias: { "@": path.resolve(__dirname, ".") } },
});
```

Create `website/vitest.setup.ts`:

```ts
import "@testing-library/jest-dom/vitest";

Object.defineProperty(window, "matchMedia", {
  writable: true,
  value: (query: string) => ({
    matches: false,
    media: query,
    onchange: null,
    addEventListener: () => undefined,
    removeEventListener: () => undefined,
    addListener: () => undefined,
    removeListener: () => undefined,
    dispatchEvent: () => false
  })
});
```

Create `website/playwright.config.ts`:

```ts
import { defineConfig, devices } from "@playwright/test";

export default defineConfig({
  testDir: "./e2e",
  use: { baseURL: "http://127.0.0.1:3000", trace: "on-first-retry" },
  webServer: { command: "npm run dev", url: "http://127.0.0.1:3000", reuseExistingServer: true },
  projects: [
    { name: "desktop", use: { ...devices["Desktop Chrome"] } },
    { name: "mobile", use: { ...devices["iPhone 13"] } }
  ]
});
```

- [ ] **Step 3: Install and verify the empty scaffold**

Run:

```bash
cd website
npm install
npx tsc --noEmit
```

Expected: dependencies install and TypeScript reports no errors.

- [ ] **Step 4: Commit the scaffold**

```bash
git add website/package.json website/package-lock.json website/tsconfig.json website/next.config.ts website/eslint.config.mjs website/vitest.config.ts website/vitest.setup.ts website/playwright.config.ts
git commit -m "chore: scaffold Eatroz storefront"
```

### Task 2: Add the Fail-Closed Product and Commerce Contracts

**Files:**
- Create: `website/content/product.ts`
- Create: `website/lib/commerce/config.ts`
- Create: `website/lib/commerce/checkout.ts`
- Create: `website/tests/content-safety.test.ts`
- Create: `website/tests/commerce-config.test.ts`

- [ ] **Step 1: Write failing contract tests**

Create `website/tests/commerce-config.test.ts`:

```ts
import { describe, expect, it } from "vitest";
import { parseCommerceConfig } from "@/lib/commerce/config";

describe("parseCommerceConfig", () => {
  it("fails closed to prelaunch", () => {
    expect(parseCommerceConfig({}, false)).toEqual({ mode: "prelaunch", checkoutUrl: null });
    expect(parseCommerceConfig({ NEXT_PUBLIC_COMMERCE_MODE: "broken" }, false)).toEqual({ mode: "prelaunch", checkoutUrl: null });
  });

  it("enables live mode only with verified sale data and an https checkout URL", () => {
    expect(parseCommerceConfig({ NEXT_PUBLIC_COMMERCE_MODE: "live", NEXT_PUBLIC_CHECKOUT_URL: "http://unsafe.test" }, true).mode).toBe("prelaunch");
    expect(parseCommerceConfig({ NEXT_PUBLIC_COMMERCE_MODE: "live", NEXT_PUBLIC_CHECKOUT_URL: "https://checkout.example.test/cart" }, false).mode).toBe("prelaunch");
    expect(parseCommerceConfig({ NEXT_PUBLIC_COMMERCE_MODE: "live", NEXT_PUBLIC_CHECKOUT_URL: "https://checkout.example.test/cart" }, true).mode).toBe("prelaunch");
    expect(parseCommerceConfig({ NEXT_PUBLIC_COMMERCE_MODE: "live", NEXT_PUBLIC_COMMERCE_APPROVED: "true", NEXT_PUBLIC_CHECKOUT_URL: "https://checkout.example.test/cart" }, true)).toEqual({
      mode: "live",
      checkoutUrl: "https://checkout.example.test/cart"
    });
  });
});
```

Create `website/tests/content-safety.test.ts`:

```ts
import { describe, expect, it } from "vitest";
import { product } from "@/content/product";

describe("product content", () => {
  it("keeps unresolved facts explicitly pending", () => {
    expect(product.price.status).toBe("verification_pending");
    expect(product.chemicalForms.status).toBe("verification_pending");
    expect(product.elementalMagnesium.status).toBe("verification_pending");
    expect(product.servingCount.status).toBe("verification_pending");
    expect(product.percentRda.status).toBe("verification_pending");
    expect(product.oxide.status).toBe("verification_pending");
    expect(product.delivery.status).toBe("verification_pending");
    expect(product.returns.status).toBe("verification_pending");
    expect(product.subscription.status).toBe("verification_pending");
    expect(product.reviews.status).toBe("verification_pending");
    expect(product.supplementFactsUrl.status).toBe("verification_pending");
    expect(product.certificateOfAnalysisUrl.status).toBe("verification_pending");
    expect(product.contactEmail.status).toBe("verification_pending");
  });

  it("contains no unsupported delivery or clinical claims", () => {
    const serialized = JSON.stringify(product).toLowerCase();
    expect(serialized).not.toContain("liposomal delivery");
    expect(serialized).not.toContain("clinically proven");
    expect(serialized).not.toContain("muscle recovery");
  });
});
```

- [ ] **Step 2: Run the tests and verify they fail**

Run: `cd website && npm test -- tests/commerce-config.test.ts tests/content-safety.test.ts`

Expected: FAIL because the imported modules do not exist.

- [ ] **Step 3: Implement the contracts**

Create `website/lib/commerce/config.ts`:

```ts
export type CommerceMode = "prelaunch" | "live";
export type CommerceConfig = { mode: CommerceMode; checkoutUrl: string | null };

export function parseCommerceConfig(env: Record<string, string | undefined>, saleDataVerified: boolean): CommerceConfig {
  const candidate = env.NEXT_PUBLIC_CHECKOUT_URL;
  let checkoutUrl: string | null = null;
  try { const parsed = new URL(candidate ?? ""); if (parsed.protocol === "https:") checkoutUrl = parsed.toString(); } catch { checkoutUrl = null; }
  if (env.NEXT_PUBLIC_COMMERCE_MODE === "live" && env.NEXT_PUBLIC_COMMERCE_APPROVED === "true" && checkoutUrl && saleDataVerified) return { mode: "live", checkoutUrl };
  return { mode: "prelaunch", checkoutUrl: null };
}
```

Create `website/lib/commerce/checkout.ts`:

```ts
export function buildCheckoutUrl(base: string, quantity: number): string {
  const url = new URL(base);
  const safeQuantity = Number.isFinite(quantity) ? Math.max(1, Math.min(12, Math.trunc(quantity))) : 1;
  url.searchParams.set("quantity", String(safeQuantity));
  return url.toString();
}
```

Create `website/content/product.ts`:

```ts
type PendingFact = { status: "verification_pending"; value: null };
type VerifiedFact<T> = { status: "verified"; value: T };
export type ProductFact<T> = PendingFact | VerifiedFact<T>;

type Product = {
  name: string; eyebrow: string; headline: string; launchLabel: string;
  price: ProductFact<number>;
  formulaIntent: readonly string[];
  chemicalForms: ProductFact<readonly string[]>;
  elementalMagnesium: ProductFact<number>;
  servingCount: ProductFact<number>;
  percentRda: ProductFact<number>;
  oxide: ProductFact<number>;
  delivery: ProductFact<string>;
  returns: ProductFact<string>;
  subscription: ProductFact<boolean>;
  reviews: ProductFact<{ count: number; average: number }>;
  supplementFactsUrl: ProductFact<string>;
  certificateOfAnalysisUrl: ProductFact<string>;
  contactEmail: ProductFact<string>;
  formulationPendingCopy: string;
  media: { heroPoster: string; heroVideo: string; pouch: string; gummy: string; ritual: string };
};

export const product: Product = {
  name: "Eatroz Magnesium Gummies",
  eyebrow: "MAGNESIUM, FULLY NAMED",
  headline: "Sleepmaxxing, done properly.",
  launchLabel: "DROP 01",
  price: { status: "verification_pending", value: null },
  formulaIntent: ["Glycinate", "Citrate", "Malate", "Taurate"],
  chemicalForms: { status: "verification_pending", value: null },
  elementalMagnesium: { status: "verification_pending", value: null },
  servingCount: { status: "verification_pending", value: null },
  percentRda: { status: "verification_pending", value: null },
  oxide: { status: "verification_pending", value: null },
  delivery: { status: "verification_pending", value: null },
  returns: { status: "verification_pending", value: null },
  subscription: { status: "verification_pending", value: null },
  reviews: { status: "verification_pending", value: null },
  supplementFactsUrl: { status: "verification_pending", value: null },
  certificateOfAnalysisUrl: { status: "verification_pending", value: null },
  contactEmail: { status: "verification_pending", value: null },
  formulationPendingCopy: "Final formulation details will be published before orders open.",
  media: {
    heroPoster: "/media/eatroz/hero-four-forms-fall-poster.webp",
    heroVideo: "/media/eatroz/hero-four-forms-fall.mp4",
    pouch: "/media/eatroz/pouch-beauty.webp",
    gummy: "/media/eatroz/gummy-macro.webp",
    ritual: "/media/eatroz/ritual-evening.webp"
  }
} as const;
```

- [ ] **Step 4: Run the contract tests**

Run: `cd website && npm test -- tests/commerce-config.test.ts tests/content-safety.test.ts`

Expected: both test files PASS.

- [ ] **Step 5: Commit the contracts**

```bash
git add website/content website/lib website/tests/commerce-config.test.ts website/tests/content-safety.test.ts
git commit -m "feat: add fail-closed storefront contracts"
```

### Task 3: Produce and Validate the Runway Media Set

**Files:**
- Create: `website/public/media/eatroz/source/eatroz-pouch-reference.png`
- Create: `website/public/media/eatroz/hero-four-forms-fall-poster.webp`
- Create: `website/public/media/eatroz/hero-four-forms-fall.mp4`
- Create: `website/public/media/eatroz/pouch-beauty.webp`
- Create: `website/public/media/eatroz/gummy-macro.webp`
- Create: `website/public/media/eatroz/ritual-evening.webp`
- Create: `website/public/media/eatroz/manifest.json`
- Create: `website/scripts/build-media-manifest.mjs`
- Create: `website/media-production/runway-generation-log.md`

- [ ] **Step 1: Establish the exact reference asset**

Copy the user-supplied pouch image unchanged from `/Users/dirghpatel/Downloads/Agent%20Image%20-%20Photorealistic%20premium%20product%20photograph%20of%20the%20exact%20Eatroz%20Magnesium%20Gummies%20pouch.png` to `website/public/media/eatroz/source/eatroz-pouch-reference.png`, then run:

```bash
file website/public/media/eatroz/source/eatroz-pouch-reference.png
shasum -a 256 website/public/media/eatroz/source/eatroz-pouch-reference.png
```

Expected: a 2752 × 1536 RGB PNG with SHA-256 `3ebb287c8546e14bcb00c6974b8b7144cf5611b118c2151b4b10373cd9ed4774`. Confirm the source and copy have identical hashes. If that exact local file becomes unavailable, stop this task and ask the user to save the image at the target path; do not substitute a different pouch. `ffmpeg`, `ffprobe`, and `cwebp` were confirmed available during planning.

- [ ] **Step 2: Generate three keyframe stills in Runway**

Upload the reference image to the user’s authorized Runway workspace. Record the displayed credit balance before generation.

Create `website/media-production/runway-generation-log.md` with one row per attempt: timestamp, Runway model, generation ID, output role, credits before, credits after, keep/reject decision, and rejection reason. Never record account credentials or session URLs.

Use this still prompt for three variants:

```text
Photorealistic premium campaign keyframe for Eatroz Magnesium Gummies, using the supplied pouch as the exact product reference. Upright tactile off-white resealable pouch, large editorial black product typography, fine mineral contour-line artwork, warm terracotta studio world. Four translucent deep-red gummies are suspended at distinct depths around the pouch in a controlled falling arc, with believable gravity, varied rotation, soft contact shadows, subtle surface imperfections, and realistic internal light transmission. Product remains immediately recognizable and commercially dominant. Wide 16:9 composition with clean negative space on the left for website copy. Refined food photography, cinematic but natural directional light, adult premium D2C wellness, sharp pouch silhouette, stable label geometry, one product only.
```

Reject any variant with altered brand spelling, extra packages, duplicated/merged gummies, plastic-looking candy, impossible shadows, warped zipper geometry, or fake certification marks.

- [ ] **Step 3: Select and animate the hero**

Use the best still as the reference/start frame. Use this image-to-video motion prompt:

```text
The camera begins in an extreme macro view of one translucent gummy with subtle handheld micro-movement and realistic surface reflections. It pulls back smoothly as three additional gummies enter under natural gravity, each rotating at a different speed and depth. The four gummies follow a controlled arc around the upright pouch, slow gently, and settle into a clean product-lockup composition. The pouch stays rigid, sharp, and geometrically stable throughout. Printed label artwork remains visually unchanged. Lighting shifts only through natural parallax and moving reflections. End with the pouch dominant on the right and clean negative space on the left, holding steady for the commerce overlay.
```

Generate the shortest duration that communicates the sequence. Make only one targeted correction before integration. Record credits after every generation and stop when Task 3 spend reaches 400 credits, preserving at least 100 credits.

- [ ] **Step 4: Produce supporting stills**

Use the selected reference system to generate:

`pouch-beauty.webp` prompt:

```text
Exact Eatroz pouch reference, upright three-quarter product beauty photograph on a warm stone surface, directional late-evening light, subtle terracotta reflection, tactile packaging texture, one pouch, clean shadow, generous crop room, premium adult wellness commerce photography.
```

`gummy-macro.webp` prompt:

```text
Extreme macro photograph of one adult-coded translucent deep-red magnesium gummy, non-character geometric form, believable gelatin texture, tiny surface variation, internal refraction, warm directional light, dark mineral background, appetizing but precise, no packaging text.
```

`ritual-evening.webp` prompt:

```text
Editorial evening-use scene in a contemporary Indian bedroom, exact Eatroz pouch on a bedside surface beside a water glass and one ceramic dish, warm low lamp light, calm lived-in material detail, no visible person, no medical props, product label legible and dominant, premium D2C campaign photography.
```

If the ritual image fails realism review, replace it with a close pouch-material and zipper-detail composition using the same product reference.

- [ ] **Step 5: Convert media and write the manifest**

Convert selected assets with installed media tooling:

```bash
ffmpeg -i runway-hero-source.mp4 -an -c:v libx264 -crf 24 -preset slow -movflags +faststart -pix_fmt yuv420p website/public/media/eatroz/hero-four-forms-fall.mp4
cwebp -q 88 selected-hero-still.png -o website/public/media/eatroz/hero-four-forms-fall-poster.webp
cwebp -q 88 selected-pouch.png -o website/public/media/eatroz/pouch-beauty.webp
cwebp -q 88 selected-gummy.png -o website/public/media/eatroz/gummy-macro.webp
cwebp -q 88 selected-ritual.png -o website/public/media/eatroz/ritual-evening.webp
```

Create `website/scripts/build-media-manifest.mjs`:

```js
import { createHash } from "node:crypto";
import { execFileSync } from "node:child_process";
import { readFileSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const root = join(dirname(fileURLToPath(import.meta.url)), "..", "public", "media", "eatroz");
const sourceFile = "source/eatroz-pouch-reference.png";
const inputs = [
  ["hero-four-forms-fall-poster.webp", "hero poster"],
  ["hero-four-forms-fall.mp4", "hero motion"],
  ["pouch-beauty.webp", "product beauty"],
  ["gummy-macro.webp", "gummy macro"],
  ["ritual-evening.webp", "ritual or approved detail substitute"]
];

const assets = inputs.map(([file, role]) => {
  const path = join(root, file);
  const probe = JSON.parse(execFileSync("ffprobe", ["-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height", "-of", "json", path], { encoding: "utf8" }));
  const { width, height } = probe.streams[0];
  return { file, role, sha256: createHash("sha256").update(readFileSync(path)).digest("hex"), width, height };
});

writeFileSync(join(root, "manifest.json"), `${JSON.stringify({
  provisional: true,
  source: {
    file: sourceFile,
    sha256: createHash("sha256").update(readFileSync(join(root, sourceFile))).digest("hex")
  },
  generator: "Runway",
  creditBudget: 500,
  creditFloor: 100,
  assets
}, null, 2)}\n`);
```

Run: `cd website && node scripts/build-media-manifest.mjs`

Expected: `public/media/eatroz/manifest.json` contains five 64-character hashes and non-zero image/video dimensions.

- [ ] **Step 6: Commit the approved media set**

```bash
git add website/public/media/eatroz website/scripts/build-media-manifest.mjs website/media-production/runway-generation-log.md
git commit -m "feat: add provisional Eatroz campaign media"
```

### Task 4: Build the Site Shell and Token System

**Files:**
- Create: `website/app/layout.tsx`
- Create: `website/app/globals.css`
- Create: `website/components/storefront.tsx`
- Create: `website/components/motion/smooth-scroll.tsx`
- Create: `website/tests/smooth-scroll.test.tsx`
- Create: `website/app/page.tsx`

- [ ] **Step 1: Add the semantic shell**

Create `website/app/layout.tsx`:

```tsx
import type { Metadata } from "next";
import { Fraunces, Inter, IBM_Plex_Mono } from "next/font/google";
import { SmoothScroll } from "@/components/motion/smooth-scroll";
import "./globals.css";

const display = Fraunces({ subsets: ["latin"], variable: "--font-display" });
const body = Inter({ subsets: ["latin"], variable: "--font-body" });
const data = IBM_Plex_Mono({ weight: ["400", "500"], subsets: ["latin"], variable: "--font-data" });

export const metadata: Metadata = {
  title: "Eatroz — Magnesium, fully named",
  description: "A transparent first look at Eatroz Magnesium Gummies. Final formulation details publish before orders open."
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return <html lang="en" className={`${display.variable} ${body.variable} ${data.variable}`}><body><SmoothScroll>{children}</SmoothScroll></body></html>;
}
```

Create `website/app/page.tsx`:

```tsx
import { Storefront } from "@/components/storefront";
import { product } from "@/content/product";
import { parseCommerceConfig } from "@/lib/commerce/config";

export default function Home() {
  const saleDataVerified = product.price.status === "verified"
    && product.chemicalForms.status === "verified"
    && product.elementalMagnesium.status === "verified"
    && product.servingCount.status === "verified"
    && product.percentRda.status === "verified"
    && product.oxide.status === "verified";
  return <Storefront commerce={parseCommerceConfig(process.env, saleDataVerified)} />;
}
```

Create `website/components/storefront.tsx` initially:

```tsx
"use client";

import type { CommerceConfig } from "@/lib/commerce/config";

export function Storefront({ commerce }: { commerce: CommerceConfig }) {
  return <main id="main-content" data-commerce-mode={commerce.mode}><h1>Eatroz storefront</h1></main>;
}
```

- [ ] **Step 2: Add global tokens and base behavior**

Create `website/app/globals.css` with the complete base:

```css
:root{--sage:#e7ece3;--canvas:#f7f5f0;--terra:#c1552f;--terra-deep:#8f3f22;--ink:#1c1b18;--ink-soft:#55524a;--stone:#d8d2c4;--surface:#fff;--max:1240px;color-scheme:light}
*{box-sizing:border-box}html{scroll-behavior:auto}body{margin:0;background:var(--canvas);color:var(--ink);font-family:var(--font-body),sans-serif}button,input{font:inherit}button,a{color:inherit}img,video{display:block;max-width:100%}a:focus-visible,button:focus-visible,input:focus-visible{outline:3px solid var(--terra);outline-offset:3px}.wrap{width:min(calc(100% - 32px),var(--max));margin-inline:auto}.display{font-family:var(--font-display),serif}.data{font-family:var(--font-data),monospace;font-variant-numeric:tabular-nums}.eyebrow{font:500 .72rem/1.2 var(--font-data),monospace;letter-spacing:.09em;text-transform:uppercase}.section{padding:clamp(72px,10vw,144px) 0}.button{display:inline-flex;min-height:48px;align-items:center;justify-content:center;border:1px solid var(--ink);border-radius:2px;background:var(--ink);color:var(--canvas);padding:0 20px;text-decoration:none;cursor:pointer}.button:hover{background:var(--terra);border-color:var(--terra)}
@media(max-width:760px){.wrap{width:min(calc(100% - 24px),var(--max))}.section{padding:64px 0}}
@media(prefers-reduced-motion:reduce){*,*::before,*::after{animation-duration:.01ms!important;animation-iteration-count:1!important;scroll-behavior:auto!important;transition-duration:.01ms!important}}
```

- [ ] **Step 3: Write the failing progressive-scroll test**

Create `website/tests/smooth-scroll.test.tsx`:

```tsx
import { render } from "@testing-library/react";
import { beforeEach, describe, expect, it, vi } from "vitest";
import Lenis from "lenis";
import { SmoothScroll } from "@/components/motion/smooth-scroll";

vi.mock("lenis", () => ({ default: vi.fn(() => ({ destroy: vi.fn() })) }));

describe("SmoothScroll", () => {
  beforeEach(() => { vi.mocked(Lenis).mockClear(); });

  it("keeps native scrolling when reduced motion is requested", () => {
    window.matchMedia = vi.fn((query: string) => ({ matches: query.includes("reduced-motion"), media: query } as unknown as MediaQueryList));
    render(<SmoothScroll><p>Content</p></SmoothScroll>);
    expect(Lenis).not.toHaveBeenCalled();
  });

  it("enhances scrolling only on a fine pointer", () => {
    window.matchMedia = vi.fn((query: string) => ({ matches: query.includes("pointer: fine"), media: query } as unknown as MediaQueryList));
    render(<SmoothScroll><p>Content</p></SmoothScroll>);
    expect(Lenis).toHaveBeenCalledOnce();
  });
});
```

Run: `cd website && npm test -- tests/smooth-scroll.test.tsx`

Expected: FAIL because `SmoothScroll` does not exist.

- [ ] **Step 4: Add guarded Lenis enhancement**

Create `website/components/motion/smooth-scroll.tsx`:

```tsx
"use client";
import { useEffect, type ReactNode } from "react";
import Lenis from "lenis";

export function SmoothScroll({ children }: { children: ReactNode }) {
  useEffect(() => {
    const reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    const finePointer = window.matchMedia("(pointer: fine)").matches;
    if (reduced || !finePointer) return;
    const lenis = new Lenis({ autoRaf: true, anchors: true });
    return () => lenis.destroy();
  }, []);
  return <>{children}</>;
}
```

- [ ] **Step 5: Verify and commit the shell**

Run:

```bash
cd website
npm run lint
npm test -- tests/smooth-scroll.test.tsx
npm run build
```

Expected: lint and production build succeed.

```bash
git add website/app website/components/storefront.tsx website/components/motion website/tests/smooth-scroll.test.tsx
git commit -m "feat: add Eatroz storefront shell"
```

### Task 5: Implement the Accessible Hero Film

**Files:**
- Create: `website/components/hero/hero-film.tsx`
- Create: `website/tests/hero-film.test.tsx`
- Modify: `website/components/storefront.tsx`
- Modify: `website/app/globals.css`

- [ ] **Step 1: Write the failing hero test**

Create `website/tests/hero-film.test.tsx`:

```tsx
import { fireEvent, render, screen } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";
import { HeroFilm } from "@/components/hero/hero-film";

describe("HeroFilm", () => {
  it("exposes playback control and product action", () => {
    window.HTMLMediaElement.prototype.pause = vi.fn();
    window.HTMLMediaElement.prototype.play = vi.fn().mockResolvedValue(undefined);
    render(<HeroFilm mode="prelaunch" onAction={vi.fn()} />);
    expect(screen.getByRole("heading", { name: /sleepmaxxing/i })).toBeInTheDocument();
    const control = screen.getByRole("button", { name: /pause film/i });
    fireEvent.click(control);
    expect(screen.getByRole("button", { name: /play film/i })).toBeInTheDocument();
    expect(screen.getByRole("button", { name: /unmute film/i })).toBeInTheDocument();
    expect(screen.getByRole("button", { name: /join the first drop/i })).toBeInTheDocument();
  });
});
```

- [ ] **Step 2: Run it and verify failure**

Run: `cd website && npm test -- tests/hero-film.test.tsx`

Expected: FAIL because `HeroFilm` does not exist.

- [ ] **Step 3: Implement the hero**

Create `website/components/hero/hero-film.tsx`:

```tsx
"use client";

import { useEffect, useRef, useState } from "react";
import { product } from "@/content/product";
import type { CommerceMode } from "@/lib/commerce/config";

export function HeroFilm({ mode, onAction }: { mode: CommerceMode; onAction: () => void }) {
  const videoRef = useRef<HTMLVideoElement>(null);
  const [playing, setPlaying] = useState(true);
  const [muted, setMuted] = useState(true);
  useEffect(() => {
    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
      videoRef.current?.pause();
      setPlaying(false);
    }
  }, []);
  const toggle = async () => {
    if (!videoRef.current) return;
    if (playing) videoRef.current.pause(); else await videoRef.current.play();
    setPlaying(!playing);
  };
  const toggleMute = () => {
    if (!videoRef.current) return;
    videoRef.current.muted = !muted;
    setMuted(!muted);
  };
  const canSell = mode === "live" && product.price.status === "verified";
  return (
    <section id="hero" className="hero" aria-labelledby="hero-title">
      <video ref={videoRef} className="hero__media" autoPlay muted={muted} loop playsInline poster={product.media.heroPoster} aria-hidden="true">
        <source src={product.media.heroVideo} type="video/mp4" />
      </video>
      <div className="hero__shade" />
      <div className="hero__content wrap">
        <p className="eyebrow">{product.eyebrow}</p>
        <p className="hero__drop data">{product.launchLabel}</p>
        <h1 id="hero-title" className="display">{product.headline}</h1>
        <button className="button" onClick={onAction}>{canSell ? `Add to Bag — ₹${product.price.value}` : "Join the First Drop"}</button>
      </div>
      <div className="hero__controls data"><button onClick={toggle} aria-label={`${playing ? "Pause" : "Play"} film`}>{playing ? "PAUSE" : "PLAY"}</button><button onClick={toggleMute} aria-label={`${muted ? "Unmute" : "Mute"} film`}>{muted ? "SOUND ON" : "MUTE"}</button></div>
    </section>
  );
}
```

Append to `website/app/globals.css`:

```css
.hero{position:relative;min-height:100svh;overflow:hidden;background:#21150f;color:#fff}.hero__media,.hero__shade{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}.hero__shade{background:linear-gradient(90deg,#120b08d9 0%,#120b0866 48%,transparent 75%)}.hero__content{position:relative;z-index:1;min-height:100svh;display:flex;flex-direction:column;align-items:flex-start;justify-content:flex-end;padding-bottom:clamp(52px,8vw,104px)}.hero__drop{margin:12px 0 0;font-size:clamp(4rem,14vw,10rem);line-height:.75;letter-spacing:-.08em}.hero h1{max-width:650px;margin:24px 0;font-size:clamp(2.5rem,6vw,5.5rem);line-height:.92;font-style:italic}.hero__controls{position:absolute;z-index:2;right:20px;bottom:20px;display:flex;gap:8px}.hero__controls button{border:1px solid #fff8;background:#0007;color:#fff;padding:10px 12px}.hero__controls button:hover{background:#000}
@media(max-width:760px){.hero__media{display:none}.hero{background-image:linear-gradient(#140d0888,#140d08cc),url('/media/eatroz/hero-four-forms-fall-poster.webp');background-size:cover;background-position:center}.hero__shade{display:none}}
```

- [ ] **Step 4: Run the test and commit**

Run: `cd website && npm test -- tests/hero-film.test.tsx && npm run lint`

Expected: PASS and lint succeeds.

```bash
git add website/components/hero website/tests/hero-film.test.tsx website/app/globals.css
git commit -m "feat: add accessible Four Forms Fall hero"
```

### Task 6: Implement Switchable Purchase, Lead, and Cart Flows

**Files:**
- Create: `website/components/commerce/purchase-dock.tsx`
- Create: `website/components/commerce/sticky-mobile-cta.tsx`
- Create: `website/components/commerce/lead-drawer.tsx`
- Create: `website/components/commerce/cart-drawer.tsx`
- Create: `website/lib/leads/submit.ts`
- Create: `website/app/api/leads/route.ts`
- Create: `website/tests/purchase-dock.test.tsx`
- Create: `website/tests/lead-route.test.ts`
- Modify: `website/components/storefront.tsx`
- Modify: `website/app/globals.css`

- [ ] **Step 1: Write failing commerce tests**

Create `website/tests/purchase-dock.test.tsx`:

```tsx
import { fireEvent, render, screen } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";
import { PurchaseDock } from "@/components/commerce/purchase-dock";

describe("PurchaseDock", () => {
  it("uses lead capture in prelaunch", () => {
    const action = vi.fn();
    render(<PurchaseDock mode="prelaunch" onAction={action} />);
    fireEvent.click(screen.getByRole("button", { name: /join the first drop/i }));
    expect(action).toHaveBeenCalledOnce();
    expect(screen.queryByText(/in stock/i)).not.toBeInTheDocument();
  });

  it("uses bag action in live mode", () => {
    render(<PurchaseDock mode="live" price={{ status: "verified", value: 899 }} onAction={vi.fn()} />);
    expect(screen.getByRole("button", { name: /add to bag/i })).toBeInTheDocument();
  });

  it("fails back to lead capture when price is pending", () => {
    render(<PurchaseDock mode="live" price={{ status: "verification_pending", value: null }} onAction={vi.fn()} />);
    expect(screen.getByRole("button", { name: /join the first drop/i })).toBeInTheDocument();
  });
});
```

Create `website/tests/lead-route.test.ts`:

```ts
import { afterEach, describe, expect, it, vi } from "vitest";
import { POST } from "@/app/api/leads/route";

afterEach(() => { vi.unstubAllEnvs(); vi.restoreAllMocks(); });

describe("lead route", () => {
  it("fails closed when no webhook is configured", async () => {
    vi.stubEnv("LEAD_WEBHOOK_URL", "");
    vi.stubEnv("LEAD_CAPTURE_APPROVED", "");
    const response = await POST(new Request("http://local/api/leads", { method: "POST", body: JSON.stringify({ email: "person@example.com" }) }));
    expect(response.status).toBe(503);
  });

  it("rejects invalid email", async () => {
    vi.stubEnv("LEAD_WEBHOOK_URL", "https://hooks.example.test/eatroz");
    vi.stubEnv("LEAD_CAPTURE_APPROVED", "true");
    const response = await POST(new Request("http://local/api/leads", { method: "POST", body: JSON.stringify({ email: "broken" }) }));
    expect(response.status).toBe(400);
  });
});
```

- [ ] **Step 2: Run tests and verify failure**

Run: `cd website && npm test -- tests/purchase-dock.test.tsx tests/lead-route.test.ts`

Expected: FAIL because components and route do not exist.

- [ ] **Step 3: Implement the purchase dock and adapters**

Create `website/components/commerce/purchase-dock.tsx`:

```tsx
import Image from "next/image";
import { product, type ProductFact } from "@/content/product";
import type { CommerceMode } from "@/lib/commerce/config";

export function PurchaseDock({ mode, price = product.price, onAction }: { mode: CommerceMode; price?: ProductFact<number>; onAction: () => void }) {
  const canSell = mode === "live" && price.status === "verified";
  return <section className="purchase wrap" aria-labelledby="purchase-title">
    <Image src={product.media.pouch} alt="Provisional Eatroz Magnesium Gummies pouch" width={800} height={800} />
    <div><p className="eyebrow">{product.launchLabel}</p><h2 id="purchase-title" className="display">{product.name}</h2>
      <p>{product.formulationPendingCopy}</p><p className="data">{product.servingCount.status === "verified" ? `${product.servingCount.value} servings` : "Serving count pending final label"}</p><p className="data">{price.status === "verified" ? `₹${price.value}` : "Launch price will be announced"}</p>
      <button className="button" onClick={onAction}>{canSell ? `Add to Bag — ₹${price.value}` : "Join the First Drop"}</button>
    </div>
  </section>;
}
```

Create `website/components/commerce/sticky-mobile-cta.tsx`:

```tsx
"use client";
import { useEffect, useState } from "react";
import { product } from "@/content/product";
import type { CommerceMode } from "@/lib/commerce/config";

export function StickyMobileCta({ mode, onAction }: { mode: CommerceMode; onAction: () => void }) {
  const [pastHero, setPastHero] = useState(false);
  useEffect(() => {
    const update = () => setPastHero((document.getElementById("hero")?.getBoundingClientRect().bottom ?? 1) <= 0);
    update();
    window.addEventListener("scroll", update, { passive: true });
    return () => window.removeEventListener("scroll", update);
  }, []);
  const canSell = mode === "live" && product.price.status === "verified";
  return <div className="sticky-cta" data-visible={pastHero} aria-hidden={!pastHero}><span>{product.name}</span><button className="button" onClick={onAction} tabIndex={pastHero ? 0 : -1}>{canSell ? `Add to Bag — ₹${product.price.value}` : "Join the First Drop"}</button></div>;
}
```

Create `website/lib/leads/submit.ts`:

```ts
export async function submitLead(email: string): Promise<void> {
  const response = await fetch("/api/leads", { method: "POST", headers: { "content-type": "application/json" }, body: JSON.stringify({ email }) });
  if (!response.ok) throw new Error("lead_submission_failed");
}
```

Create `website/app/api/leads/route.ts`:

```ts
import { NextResponse } from "next/server";

const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

export async function POST(request: Request) {
  const webhook = process.env.LEAD_WEBHOOK_URL;
  if (process.env.LEAD_CAPTURE_APPROVED !== "true" || !webhook?.startsWith("https://")) return NextResponse.json({ error: "capture_unavailable" }, { status: 503 });
  const body = await request.json().catch(() => null) as { email?: unknown } | null;
  if (!body || typeof body.email !== "string" || !emailPattern.test(body.email)) return NextResponse.json({ error: "invalid_email" }, { status: 400 });
  const upstream = await fetch(webhook, { method: "POST", headers: { "content-type": "application/json" }, body: JSON.stringify({ email: body.email, source: "eatroz-first-drop" }), cache: "no-store", signal: AbortSignal.timeout(5000) }).catch(() => null);
  if (!upstream?.ok) return NextResponse.json({ error: "capture_unavailable" }, { status: 503 });
  return NextResponse.json({ ok: true });
}
```

Create `website/components/commerce/lead-drawer.tsx` and `website/components/commerce/cart-drawer.tsx` as complete native-dialog components:

```tsx
// lead-drawer.tsx
"use client";
import { FormEvent, useEffect, useRef, useState } from "react";
import { submitLead } from "@/lib/leads/submit";

export function LeadDrawer({ open, onClose }: { open: boolean; onClose: () => void }) {
  const dialog = useRef<HTMLDialogElement>(null); const [status, setStatus] = useState<"idle"|"sending"|"success"|"error">("idle");
  useEffect(() => { if (open && !dialog.current?.open) dialog.current?.showModal(); if (!open && dialog.current?.open) dialog.current.close(); }, [open]);
  async function submit(event: FormEvent<HTMLFormElement>) { event.preventDefault(); setStatus("sending"); const form = new FormData(event.currentTarget); try { await submitLead(String(form.get("email"))); setStatus("success"); } catch { setStatus("error"); } }
  return <dialog ref={dialog} className="drawer" onClose={onClose} aria-labelledby="lead-title"><button onClick={onClose} aria-label="Close first drop form">Close</button><h2 id="lead-title" className="display">Join the First Drop</h2>{status === "success" ? <p>You're on the list.</p> : <form onSubmit={submit}><label>Email<input name="email" type="email" required autoComplete="email" /></label><p>By joining, you agree to receive Eatroz launch updates. Read the <a href="/privacy">privacy notice</a>.</p><button className="button" disabled={status === "sending"}>{status === "sending" ? "Joining…" : "Join"}</button>{status === "error" && <p role="alert">We couldn't save your place. Your email remains in the form; please retry.</p>}</form>}</dialog>;
}
```

```tsx
// cart-drawer.tsx
"use client";
import { useEffect, useRef, useState } from "react";
import { product } from "@/content/product";
import { buildCheckoutUrl } from "@/lib/commerce/checkout";

export function CartDrawer({ open, checkoutUrl, onClose }: { open: boolean; checkoutUrl: string; onClose: () => void }) {
  const dialog = useRef<HTMLDialogElement>(null); const [quantity, setQuantity] = useState(1);
  useEffect(() => { if (open && !dialog.current?.open) dialog.current?.showModal(); if (!open && dialog.current?.open) dialog.current.close(); }, [open]);
  if (product.price.status !== "verified") return null;
  return <dialog ref={dialog} className="drawer" onClose={onClose} aria-labelledby="cart-title"><button onClick={onClose} aria-label="Close bag">Close</button><h2 id="cart-title" className="display">Your bag</h2><p>{product.name}</p><label>Quantity<input type="number" min="1" max="12" value={quantity} onChange={e => setQuantity(Number(e.target.value))} /></label><a className="button" href={buildCheckoutUrl(checkoutUrl, quantity)}>Checkout — ₹{product.price.value * quantity}</a></dialog>;
}
```

- [ ] **Step 4: Wire drawers through `Storefront`**

Replace `website/components/storefront.tsx` with:

```tsx
"use client";
import { useState } from "react";
import type { CommerceConfig } from "@/lib/commerce/config";
import { HeroFilm } from "@/components/hero/hero-film";
import { PurchaseDock } from "@/components/commerce/purchase-dock";
import { LeadDrawer } from "@/components/commerce/lead-drawer";
import { CartDrawer } from "@/components/commerce/cart-drawer";
import { StickyMobileCta } from "@/components/commerce/sticky-mobile-cta";

export function Storefront({ commerce }: { commerce: CommerceConfig }) {
  const [open, setOpen] = useState(false); const action = () => setOpen(true);
  return <><main id="main-content" data-commerce-mode={commerce.mode}><HeroFilm mode={commerce.mode} onAction={action}/><PurchaseDock mode={commerce.mode} onAction={action}/></main><StickyMobileCta mode={commerce.mode} onAction={action}/>{commerce.mode === "live" && commerce.checkoutUrl ? <CartDrawer open={open} checkoutUrl={commerce.checkoutUrl} onClose={() => setOpen(false)}/> : <LeadDrawer open={open} onClose={() => setOpen(false)}/>}</>;
}
```

Append to `website/app/globals.css`:

```css
.purchase{display:grid;grid-template-columns:1fr 1fr;gap:clamp(28px,7vw,96px);align-items:center;padding-block:clamp(64px,9vw,128px)}.purchase img{width:100%;aspect-ratio:1;object-fit:cover}.purchase h2{font-size:clamp(2rem,5vw,4.6rem);line-height:.95;margin:12px 0}.purchase .data{font-size:1.1rem;margin:16px 0}.drawer{width:min(480px,calc(100% - 24px));margin:0 0 0 auto;min-height:100%;border:0;border-left:1px solid var(--stone);padding:28px;background:var(--canvas);color:var(--ink)}.drawer::backdrop{background:#0009}.drawer form,.drawer label{display:grid;gap:10px}.drawer input{min-height:48px;border:1px solid var(--ink);background:#fff;padding:10px}.sticky-cta{display:none}
@media(max-width:760px){.purchase{grid-template-columns:1fr}.drawer{margin:auto 0 0;width:100%;min-height:auto;max-height:90svh;border-left:0;border-top:1px solid var(--stone)}.sticky-cta{position:fixed;z-index:20;inset:auto 0 0;display:flex;align-items:center;justify-content:space-between;gap:12px;padding:10px 12px;background:var(--canvas);border-top:1px solid var(--stone);transform:translateY(110%);transition:transform .2s}.sticky-cta[data-visible="true"]{transform:translateY(0)}.sticky-cta span{max-width:42%;font-size:.78rem}.sticky-cta .button{min-height:44px}}
```

- [ ] **Step 5: Run tests and commit**

Run: `cd website && npm test -- tests/purchase-dock.test.tsx tests/lead-route.test.ts && npm run lint`

Expected: tests and lint pass.

```bash
git add website/components/commerce website/lib/leads website/app/api website/components/storefront.tsx website/tests website/app/globals.css
git commit -m "feat: add switchable lead and checkout flows"
```

### Task 7: Build the Exploded Formula and Evidence Sections

**Files:**
- Create: `website/components/formula/exploded-formula.tsx`
- Create: `website/components/proof/oxide-proof.tsx`
- Modify: `website/components/storefront.tsx`
- Modify: `website/app/globals.css`

- [ ] **Step 1: Implement the seek-safe formula story**

Create `website/components/formula/exploded-formula.tsx`:

```tsx
"use client";
import Image from "next/image";
import { useEffect, useRef } from "react";
import gsap from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";
import { product } from "@/content/product";

export function ExplodedFormula() {
  const root = useRef<HTMLElement>(null);
  useEffect(() => {
    if (matchMedia("(prefers-reduced-motion: reduce)").matches) return;
    gsap.registerPlugin(ScrollTrigger);
    const context = gsap.context(() => { gsap.fromTo("[data-form]", { y: 60, opacity: 0 }, { y: 0, opacity: 1, stagger: .15, scrollTrigger: { trigger: root.current, start: "top 65%", end: "bottom 65%", scrub: true } }); }, root);
    return () => context.revert();
  }, []);
  return <section ref={root} className="formula section" aria-labelledby="formula-title"><div className="wrap formula__grid"><div className="formula__visual"><Image src={product.media.pouch} alt="Eatroz pouch surrounded by four intended formula markers" width={900} height={1100}/></div><div><p className="eyebrow">FORMULA INTENT — PENDING FINAL CONFIRMATION</p><h2 id="formula-title" className="display">Four named forms in development.</h2><ol>{product.formulaIntent.map((form,index)=><li data-form key={form}><span className="data">0{index+1}</span><strong>{form}</strong></li>)}</ol></div></div></section>;
}
```

Create `website/components/proof/oxide-proof.tsx`:

```tsx
import { product } from "@/content/product";

export function OxideProof() {
  const oxideCopy = product.oxide.status === "verified" ? `${product.oxide.value}%` : "Pending final formula";
  const rdaCopy = product.percentRda.status === "verified" ? `${product.percentRda.value}%` : "Pending final label";
  return <section className="proof section" aria-labelledby="proof-title"><div className="wrap"><p className="eyebrow">THE PROOF</p><h2 id="proof-title" className="display">No decorative numbers.</h2><div className="proof__grid"><div><span className="data">MAGNESIUM OXIDE</span><strong className="display">{oxideCopy}</strong></div><div><span className="data">% RDA</span><strong>{rdaCopy}</strong></div></div><p className="proof__source">Comparative absorption or efficacy graphics remain hidden until an approved source and final formulation are attached.</p></div></section>;
}
```

Append to `website/app/globals.css`:

```css
.formula{background:var(--sage)}.formula__grid{display:grid;grid-template-columns:1fr 1fr;gap:clamp(36px,8vw,110px);align-items:center}.formula__visual{position:sticky;top:10vh}.formula__visual img{max-height:80vh;width:100%;object-fit:contain}.formula h2,.proof h2{font-size:clamp(2.5rem,6vw,5.8rem);line-height:.92}.formula ol{list-style:none;padding:0;margin:48px 0 0}.formula li{display:grid;grid-template-columns:56px 1fr;gap:16px;padding:22px 0;border-top:1px solid var(--ink)}.formula li strong{font-size:clamp(1.4rem,3vw,2.6rem)}.proof{background:var(--ink);color:var(--canvas)}.proof__grid{display:grid;grid-template-columns:1fr 1fr;margin-top:48px;border-top:1px solid #ffffff55}.proof__grid>div{display:grid;gap:18px;padding:32px 0;border-bottom:1px solid #ffffff55}.proof__grid>div:first-child{border-right:1px solid #ffffff55}.proof__grid strong{font-size:clamp(2rem,8vw,7rem)}.proof__source{max-width:700px;color:#b7b0a0}
@media(max-width:760px){.formula__grid,.proof__grid{grid-template-columns:1fr}.formula__visual{position:relative;top:auto}.proof__grid>div:first-child{border-right:0}}
```

- [ ] **Step 2: Add sections to `Storefront` and verify**

Replace `website/components/storefront.tsx` with:

```tsx
"use client";
import { useState } from "react";
import type { CommerceConfig } from "@/lib/commerce/config";
import { HeroFilm } from "@/components/hero/hero-film";
import { PurchaseDock } from "@/components/commerce/purchase-dock";
import { LeadDrawer } from "@/components/commerce/lead-drawer";
import { CartDrawer } from "@/components/commerce/cart-drawer";
import { ExplodedFormula } from "@/components/formula/exploded-formula";
import { OxideProof } from "@/components/proof/oxide-proof";
import { StickyMobileCta } from "@/components/commerce/sticky-mobile-cta";

export function Storefront({ commerce }: { commerce: CommerceConfig }) {
  const [open, setOpen] = useState(false);
  const action = () => setOpen(true);
  return <>
    <main id="main-content" data-commerce-mode={commerce.mode}>
      <HeroFilm mode={commerce.mode} onAction={action}/>
      <PurchaseDock mode={commerce.mode} onAction={action}/>
      <ExplodedFormula />
      <OxideProof />
    </main>
    <StickyMobileCta mode={commerce.mode} onAction={action}/>
    {commerce.mode === "live" && commerce.checkoutUrl
      ? <CartDrawer open={open} checkoutUrl={commerce.checkoutUrl} onClose={() => setOpen(false)}/>
      : <LeadDrawer open={open} onClose={() => setOpen(false)}/>}
  </>;
}
```

Run: `cd website && npm test && npm run build`

Expected: all unit tests and the production build pass.

- [ ] **Step 3: Commit**

```bash
git add website/components/formula website/components/proof website/components/storefront.tsx website/app/globals.css
git commit -m "feat: add formula and evidence storytelling"
```

### Task 8: Complete Gallery, Facts, Trust, and Final Conversion

**Files:**
- Create: `website/components/gallery/product-gallery.tsx`
- Create: `website/components/facts/facts-disclosure.tsx`
- Create: `website/components/trust/trust-section.tsx`
- Create: `website/app/privacy/page.tsx`
- Create: `website/app/terms/page.tsx`
- Create: `website/tests/storefront.test.tsx`
- Modify: `website/components/storefront.tsx`
- Modify: `website/app/globals.css`

- [ ] **Step 1: Write the failing storefront integrity test**

Create `website/tests/storefront.test.tsx`:

```tsx
import { render, screen } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";
import { Storefront } from "@/components/storefront";

vi.mock("gsap", () => ({ default: { registerPlugin: vi.fn(), context: vi.fn(() => ({ revert: vi.fn() })), fromTo: vi.fn() } }));
vi.mock("gsap/ScrollTrigger", () => ({ ScrollTrigger: {} }));

describe("Storefront", () => {
  it("renders the complete prelaunch journey without reviews or stock claims", () => {
    render(<Storefront commerce={{ mode: "prelaunch", checkoutUrl: null }}/>);
    expect(screen.getByRole("heading", { name: /sleepmaxxing/i })).toBeInTheDocument();
    expect(screen.getByRole("heading", { name: /four named forms/i })).toBeInTheDocument();
    expect(screen.getByRole("heading", { name: /product, from every angle/i })).toBeInTheDocument();
    expect(screen.getByRole("heading", { name: /what we will publish/i })).toBeInTheDocument();
    expect(screen.queryByText(/customer reviews/i)).not.toBeInTheDocument();
    expect(screen.queryByText(/in stock/i)).not.toBeInTheDocument();
  });
});
```

- [ ] **Step 2: Run it and verify failure**

Run: `cd website && npm test -- tests/storefront.test.tsx`

Expected: FAIL because the remaining sections do not exist.

- [ ] **Step 3: Implement the remaining sections**

Create `website/components/gallery/product-gallery.tsx`:

```tsx
"use client";
import Image from "next/image";
import { useState } from "react";
import { product } from "@/content/product";

const images = [
  { src: product.media.pouch, alt: "Provisional Eatroz pouch in warm evening light", label: "Pouch" },
  { src: product.media.gummy, alt: "Macro view of a translucent Eatroz gummy", label: "Gummy macro" },
  { src: product.media.ritual, alt: "Eatroz pouch in an evening ritual setting", label: "Evening ritual" }
];
export function ProductGallery() {
  const [selected, setSelected] = useState(0);
  const image = images[selected];
  return <section className="gallery section" aria-labelledby="gallery-title"><div className="wrap"><p className="eyebrow">PRODUCT APPETITE</p><h2 id="gallery-title" className="display">The product, from every angle.</h2><figure className="gallery__stage"><Image src={image.src} alt={image.alt} width={1600} height={1200} priority={false}/><figcaption className="data">PROVISIONAL CAMPAIGN VISUAL</figcaption></figure><div className="gallery__nav" aria-label="Choose product view">{images.map((item,index)=><button type="button" aria-pressed={selected === index} onClick={() => setSelected(index)} key={item.src}><Image src={item.src} alt="" width={180} height={130}/><span>{item.label}</span></button>)}</div></div></section>;
}
```

Create `website/components/facts/facts-disclosure.tsx`:

```tsx
import { product } from "@/content/product";
export function FactsDisclosure() {
  const forms = product.chemicalForms.status === "verified" ? product.chemicalForms.value.join(" · ") : `${product.formulaIntent.join(" · ")} — pending final confirmation`;
  const elemental = product.elementalMagnesium.status === "verified" ? `${product.elementalMagnesium.value} mg` : product.formulationPendingCopy;
  const rda = product.percentRda.status === "verified" ? `${product.percentRda.value}%` : product.formulationPendingCopy;
  return <section className="facts section" aria-labelledby="facts-title"><div className="wrap"><p className="eyebrow">THE NIGHTLY RITUAL + LABEL</p><h2 id="facts-title" className="display">Simple use. Facts open by default.</h2><ol className="ritual"><li>Place it where your evening wind-down already happens.</li><li>Follow the serving direction on the final approved label.</li><li>Reseal the pouch and store it exactly as the final label directs.</li></ol><details open><summary>Supplement Facts status</summary><dl><div><dt>Forms</dt><dd>{forms}</dd></div><div><dt>Magnesium oxide</dt><dd>{product.oxide.status === "verified" ? `${product.oxide.value}%` : product.formulationPendingCopy}</dd></div><div><dt>Elemental magnesium</dt><dd>{elemental}</dd></div><div><dt>% RDA</dt><dd>{rda}</dd></div></dl></details></div></section>;
}
```

Create `website/components/trust/trust-section.tsx`:

```tsx
export function TrustSection() { return <section className="trust section" aria-labelledby="trust-title"><div className="wrap"><p className="eyebrow">TRUST, BEFORE TESTIMONIALS</p><h2 id="trust-title" className="display">What we will publish before orders open.</h2><ul><li>Final elemental magnesium and percentage RDA</li><li>Complete Supplement Facts and FSSAI declarations</li><li>Tamper-evident packaging construction</li><li>Batch-specific Certificate of Analysis when available</li></ul></div></section>; }
```

Create `website/app/privacy/page.tsx`:

```tsx
export default function PrivacyPage() {
  return <main className="policy wrap"><p className="eyebrow">DRAFT — OWNER/LEGAL APPROVAL REQUIRED</p><h1 className="display">Privacy notice</h1><h2>First Drop email</h2><p>If you join the First Drop, Eatroz collects the email address you submit to send launch updates. The configured email service provider processes that address for Eatroz.</p><h2>Choice and retention</h2><p>You may unsubscribe through an email link. The approved policy must define the final deletion contact and retention period before capture is enabled.</p><p>No production lead webhook may be enabled while this draft marker remains.</p></main>;
}
```

Create `website/app/terms/page.tsx`:

```tsx
export default function TermsPage() {
  return <main className="policy wrap"><p className="eyebrow">DRAFT — OWNER/LEGAL APPROVAL REQUIRED</p><h1 className="display">Site terms</h1><p>Eatroz is currently presented in pre-launch mode. Product visuals, packaging, formulation, price, delivery, returns, and availability are provisional unless the site explicitly marks them verified.</p><p>Final purchase, shipping, returns, warranty, product-use terms, and the contact channel must be approved and published before live checkout is enabled.</p></main>;
}
```

Do not enable a production lead webhook or checkout until the draft markers are replaced with approved text.

- [ ] **Step 4: Complete `Storefront` composition**

Replace `website/components/storefront.tsx` with:

```tsx
"use client";
import { useState } from "react";
import { product } from "@/content/product";
import type { CommerceConfig } from "@/lib/commerce/config";
import { HeroFilm } from "@/components/hero/hero-film";
import { PurchaseDock } from "@/components/commerce/purchase-dock";
import { LeadDrawer } from "@/components/commerce/lead-drawer";
import { CartDrawer } from "@/components/commerce/cart-drawer";
import { ExplodedFormula } from "@/components/formula/exploded-formula";
import { OxideProof } from "@/components/proof/oxide-proof";
import { StickyMobileCta } from "@/components/commerce/sticky-mobile-cta";
import { ProductGallery } from "@/components/gallery/product-gallery";
import { FactsDisclosure } from "@/components/facts/facts-disclosure";
import { TrustSection } from "@/components/trust/trust-section";

export function Storefront({ commerce }: { commerce: CommerceConfig }) {
  const [open, setOpen] = useState(false);
  const action = () => setOpen(true);
  const canSell = commerce.mode === "live" && product.price.status === "verified";
  const actionLabel = canSell ? `Add to Bag — ₹${product.price.value}` : "Join the First Drop";
  return <>
    <main id="main-content" data-commerce-mode={commerce.mode}>
      <HeroFilm mode={commerce.mode} onAction={action}/>
      <PurchaseDock mode={commerce.mode} onAction={action}/>
      <ExplodedFormula />
      <OxideProof />
      <ProductGallery />
      <FactsDisclosure />
      <TrustSection />
      <section className="final-cta section" aria-labelledby="final-title">
        <div className="wrap"><p className="eyebrow">DROP 01</p><h2 id="final-title" className="display">Meet your evening magnesium ritual.</h2><p>{product.delivery.status === "verified" ? product.delivery.value : "Delivery timing will be published before orders open."} {product.returns.status === "verified" ? product.returns.value : "Returns terms will be published before orders open."}</p><button className="button" onClick={action}>{actionLabel}</button><div className="faq"><details><summary>Is the formula final?</summary><p>No. Every unresolved formulation field is marked pending until the approved label is available.</p></details><details><summary>Are these final product photographs?</summary><p>No. They are provisional AI-generated campaign concepts based on a provisional pouch design.</p></details><details><summary>Can I order now?</summary><p>{canSell ? "Yes—use Add to Bag to continue to the configured checkout." : "Not yet. Join the First Drop for the launch update."}</p></details></div></div>
      </section>
    </main>
    <footer className="site-footer"><div className="wrap"><p>Eatroz Nutraceutical</p><nav aria-label="Footer"><span>Contact channel pending approval</span> · <a href="/privacy">Privacy</a> · <a href="/terms">Terms</a></nav><p className="data">PRODUCT AND CAMPAIGN VISUALS ARE PROVISIONAL AI-GENERATED CONCEPTS.</p></div></footer>
    <StickyMobileCta mode={commerce.mode} onAction={action}/>
    {commerce.mode === "live" && commerce.checkoutUrl
      ? <CartDrawer open={open} checkoutUrl={commerce.checkoutUrl} onClose={() => setOpen(false)}/>
      : <LeadDrawer open={open} onClose={() => setOpen(false)}/>}
  </>;
}
```

Append to `website/app/globals.css`:

```css
.gallery h2,.facts h2,.trust h2{font-size:clamp(2.5rem,6vw,5.8rem);line-height:.92}.gallery__stage{margin:48px 0 0}.gallery__stage>img{width:100%;aspect-ratio:4/3;object-fit:cover}.gallery figcaption{padding:8px 0}.gallery__nav{display:grid;grid-template-columns:repeat(3,1fr);gap:12px}.gallery__nav button{display:grid;gap:8px;border:1px solid transparent;background:transparent;padding:8px;text-align:left;cursor:pointer}.gallery__nav button[aria-pressed="true"]{border-color:var(--ink)}.gallery__nav img{width:100%;aspect-ratio:4/3;object-fit:cover}.facts{background:var(--sage)}.ritual{display:grid;grid-template-columns:repeat(3,1fr);gap:24px;padding-left:24px}.facts details{margin-top:40px;border-top:1px solid var(--ink);border-bottom:1px solid var(--ink)}.facts summary{cursor:pointer;padding:22px 0}.facts dl>div{display:grid;grid-template-columns:1fr 2fr;padding:18px 0;border-top:1px solid var(--stone)}.facts dd{margin:0}.trust ul{display:grid;grid-template-columns:1fr 1fr;gap:0;list-style:none;padding:0;margin-top:40px}.trust li{padding:24px;border-top:1px solid var(--stone)}.final-cta{background:var(--terra);color:#fff;text-align:center}.final-cta h2{font-size:clamp(2.5rem,7vw,6rem)}.faq{max-width:760px;margin:56px auto 0;text-align:left}.faq details{border-top:1px solid #ffffff88;padding:16px 0}.site-footer{padding:32px;background:var(--ink);color:var(--canvas)}.policy{max-width:760px;padding-block:72px}.policy h1{font-size:clamp(2.5rem,7vw,5rem)}
@media(max-width:760px){.gallery__nav,.ritual,.trust ul{grid-template-columns:1fr}.facts dl>div{grid-template-columns:1fr;gap:8px}}
```

- [ ] **Step 5: Run tests and commit**

Run: `cd website && npm test && npm run lint && npm run build`

Expected: all tests, lint, and build pass.

```bash
git add website/components website/tests/storefront.test.tsx website/app/globals.css
git commit -m "feat: complete Eatroz product story"
```

### Task 9: Add End-to-End Accessibility and Mode Verification

**Files:**
- Create: `website/e2e/storefront.spec.ts`

- [ ] **Step 1: Write the end-to-end checks**

Create `website/e2e/storefront.spec.ts`:

```ts
import { expect, test } from "@playwright/test";
import AxeBuilder from "@axe-core/playwright";

test("prelaunch journey is complete and claim-safe", async ({ page }) => {
  await page.goto("/");
  await expect(page.locator("main")).toHaveAttribute("data-commerce-mode", "prelaunch");
  await expect(page.getByRole("button", { name: "Join the First Drop" }).first()).toBeVisible();
  await expect(page.getByText("Final formulation details will be published before orders open.").first()).toBeVisible();
  await expect(page.getByText(/in stock/i)).toHaveCount(0);
  const results = await new AxeBuilder({ page }).analyze();
  expect(results.violations).toEqual([]);
});

test("lead failure never reports false success", async ({ page }) => {
  await page.goto("/");
  await page.getByRole("button", { name: "Join the First Drop" }).first().click();
  await page.getByLabel("Email").fill("person@example.com");
  await page.getByRole("button", { name: "Join", exact: true }).click();
  await expect(page.getByRole("alert")).toContainText("couldn't save");
  await expect(page.getByText("You're on the list.")).toHaveCount(0);
});

test("media and controls survive reduced motion", async ({ page }) => {
  await page.emulateMedia({ reducedMotion: "reduce" });
  await page.goto("/");
  await expect(page.getByRole("button", { name: "Play film" })).toBeVisible();
  await expect(page.getByRole("heading", { name: /four named forms/i })).toBeVisible();
});
```

- [ ] **Step 2: Run browser tests**

Run:

```bash
cd website
npx playwright install chromium
npm run test:e2e
```

Expected: desktop and mobile projects pass all three tests with zero axe violations.

- [ ] **Step 3: Commit**

```bash
git add website/e2e website/playwright.config.ts
git commit -m "test: verify storefront modes and accessibility"
```

### Task 10: Perform Visual, Media, and Final Verification

**Files:**
- Create: `website/README.md`
- Modify after reproducing a specific verification defect: the exact file owned by Tasks 4–9 that causes it

- [ ] **Step 1: Verify the media manifest mechanically**

Run:

```bash
cd website
node scripts/build-media-manifest.mjs
node -e 'const m=require("./public/media/eatroz/manifest.json"); if(!/^[a-f0-9]{64}$/.test(m.source.sha256)||m.assets.length!==5||m.assets.some(a=>!/^[a-f0-9]{64}$/.test(a.sha256)||a.width<1||a.height<1)) process.exit(1)'
for f in hero-four-forms-fall-poster.webp hero-four-forms-fall.mp4 pouch-beauty.webp gummy-macro.webp ritual-evening.webp; do test -s "public/media/eatroz/$f"; done
ffprobe -v error -show_entries format=duration,size -of default=noprint_wrappers=1 public/media/eatroz/hero-four-forms-fall.mp4
```

Expected: the manifest validation exits 0, every asset is non-empty, and `ffprobe` reports a valid duration and size.

- [ ] **Step 2: Capture desktop and mobile screenshots**

Run the app with `npm run dev`, then capture:

- desktop: 1440 × 1000;
- mobile: 390 × 844;
- pre-launch default;
- an attempted live configuration with the current pending product data, confirming that it still renders pre-launch;
- the live drawer/component test fixture only after real sale facts are marked verified—never change pending facts merely to obtain a screenshot;
- reduced-motion mobile.

Save evidence under `website/test-results/visual/` and inspect each full page for product visibility, CTA visibility, text contrast, crop quality, generated-image defects, drawer overflow, and factual leakage.

- [ ] **Step 3: Run the complete verification suite**

Run:

```bash
cd website
npm test
npm run lint
npm run build
npm run test:e2e
```

Expected: every command exits 0.

- [ ] **Step 4: Document operation and disclosure**

Create `website/README.md` containing:

```markdown
# Eatroz Storefront

## Modes

- Default: `prelaunch`; lead capture requires an HTTPS `LEAD_WEBHOOK_URL` and `LEAD_CAPTURE_APPROVED=true` after the privacy notice receives owner/legal approval.
- Live: after policy and commerce approval, set `NEXT_PUBLIC_COMMERCE_MODE=live`, `NEXT_PUBLIC_COMMERCE_APPROVED=true`, and an HTTPS `NEXT_PUBLIC_CHECKOUT_URL`; all sale-data fields must also be verified.
- Invalid or incomplete live configuration fails closed to pre-launch.

## Commands

- `npm run dev`
- `npm test`
- `npm run lint`
- `npm run build`
- `npm run test:e2e`

## Media

Files in `public/media/eatroz/` are provisional AI-generated campaign visuals based on a provisional pouch concept. They are not final product photography or approved packaging artwork. See `manifest.json` for provenance and hashes.

## Content safety

Unverified formulation fields remain in `verification_pending` state. Do not replace them with estimates. Reviews, stock status, certifications, a Certificate of Analysis, and structured-data claims remain hidden until backed by real data.
```

- [ ] **Step 5: Commit final documentation and any verified corrections**

```bash
git add website/README.md website/app website/components website/content website/lib website/tests website/e2e website/public/media/eatroz
git commit -m "docs: document Eatroz storefront operation"
```

- [ ] **Step 6: Review the branch before integration**

Run:

```bash
git status --short
git log --oneline main..HEAD
git diff --check main..HEAD
git diff --stat main..HEAD
```

Expected: clean status, the planned sequence of focused feature commits, no whitespace errors, and changes limited to `website/`.
