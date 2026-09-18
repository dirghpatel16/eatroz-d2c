# Seed.com Forensic Design System Anatomy & Implementation Blueprint

*Extracted directly from live [Seed.com](https://seed.com) via Playwright on 18 Sep 2026.*  
*All extracted raw assets, fonts, SVGs, screenshots, and Figma layer trees are stored in [`website/extracted-seed/`](file:///Users/dirghpatel/Documents/india-gummy-d2c/website/extracted-seed).*

---

## 1. Executive Summary & Brand Paradigm

Seed.com disrupted modern wellness by replacing conventional "marketing fluff" with **forensic scientific luxury**. Its design architecture communicates three core pillars:
1. **Apothecary Precision:** Clinical 1px hairline grids, tabular figures, and laboratory ledger aesthetics.
2. **Organic Modernism:** Deep chlorophyll botanical darks paired with warm clinical linen whites (never harsh pure `#000` or `#FFF`).
3. **Interactive Scrollytelling:** Scroll-driven physical product deconstructions (dual-capsule nested delivery in Seed; 4-form chelation bloom in Eatroz).

---

## 2. Extracted Color System (Verified Tokens)

These values were captured directly from Seed.com's computed stylesheet:

| Design Token | Hex / RGBA Value | Semantic Usage | Eatroz Botanical Clinical Equivalent |
| :--- | :--- | :--- | :--- |
| `--color-primary-seed-green` | `#1C3A13` | Deep Chlorophyll brand primary | `#1C1B18` Deep Forest Charcoal |
| `--color-primary-snow-white` | `#FCFCF7` | Soft warm linen canvas background | `#F7F5F0` Warm Clinical Canvas |
| `--color-primary-soft-green` | `#3D5B34` | Mid-tone botanical sage accent | `#E7ECE3` Soft Pectin Sage |
| `--color-guidance-bright-green`| `#D3FA99` | Fluorescent bioluminescent highlight | `#C1552F` Terracotta Bio-Active |
| `--color-neutral-foam-white` | `#EFF1E4` | Secondary surface / container fill | `#EAEFE7` Sub-card linen |
| `--color-neutral-yellowish-white`| `#F6F7EF` | Interactive hover cards | `#F2EFEB` Secondary elevation |
| `--outline-primary-10` | `rgba(28, 58, 19, 0.10)` | 1px hairline apothecary grid borders | `rgba(28, 27, 24, 0.12)` 1px hairline border |

> [!TIP]
> **Zero Harsh Darks:** Seed never uses pure `#000000` for text; it uses `#1C3A13` at 90% opacity (`rgba(28, 58, 19, 0.9)`), giving text an organic ink feel.

---

## 3. Typography Hierarchy

Extracted font files saved in: [`website/extracted-seed/assets/fonts/`](file:///Users/dirghpatel/Documents/india-gummy-d2c/website/extracted-seed/assets/fonts)

* **Headline Variable Serif/Sans:**
  - Seed uses *Seed Sans* (custom Dinamo cut).
  - Open-source equivalents: **Fraunces** (luxury serif optical sizing) or **General Sans** / **Plus Jakarta Sans**.
  - Letter spacing: `-0.02em` (tight, editorial).
* **Body / Editorial:**
  - Modern geometric Grotesk with high x-height (`Inter` / `Manrope`).
  - Size: `1.125rem` (18px) for primary copy, `1.6` line-height for effortless readability.
* **Laboratory / Monospace Clinical Figures:**
  - *Seed Sans Mono* / *JetBrains Mono* / *DM Mono*.
  - Used strictly for batch numbers (`ETZ-01-A26`), milligram dosages (`250mg`), chemical formulas ($C_4H_8MgN_2O_4$), and trial percentages (`+34m`).

---

## 4. Scrollytelling Architecture (The Seed Pinned Scroll Physics)

### How Seed Achieves Its World-Class Motion:
1. **Viewport Pinning:**
   - Instead of standard page scrolling, the container is pinned for `200vh` to `300vh` using GSAP `ScrollTrigger` or Lenis virtual scroll.
2. **Multi-Phase Animation Timeline:**
   - **Phase 1 (0% - 25%):** Macro Product Hero zoom (scale `0.9` -> `1.2`, camera push-in).
   - **Phase 2 (25% - 60%):** Capsule Shell / Gummy dissolution & interior exposure.
   - **Phase 3 (60% - 85%):** Radial delivery bloom (molecular nutrients spreading outward to organ systems).
   - **Phase 4 (85% - 100%):** Clinical endpoint convergence and transition into the purchase dock.

### Eatroz Implementation:
Implemented in [`website/components/motion/scrollytelling-canvas.tsx`](file:///Users/dirghpatel/Documents/india-gummy-d2c/website/components/motion/scrollytelling-canvas.tsx):
- GSAP `ScrollTrigger` pinned canvas spanning `240vh`.
- Animated 4-form chelation bloom (Bisglycinate, Malate, Citrate, Taurate).
- Interactive SVG Ring Dial showing real-time 68% ICMR RDA bioavailability counter.

---

## 5. Component Breakdown & Scaffolding Checklist

### 1. Sticky Purchase Dock (`PurchaseDock`)
- **Seed Pattern:** The user never has to search for the "Buy" button. A fixed dock sits at the bottom of the viewport with an interactive choice between a 30-day ritual and a 90-day kit.
- **Eatroz Execution:** [purchase-dock.tsx](file:///Users/dirghpatel/Documents/india-gummy-d2c/website/components/commerce/purchase-dock.tsx) with toggle for reusable amber glass apothecary jar + compostable refill pouches.

### 2. Clinical Study Ledger (`ClinicalLedger`)
- **Seed Pattern:** Clear 1px hairline border grid displaying peer-reviewed endpoints rather than vague testimonials.
- **Eatroz Execution:** [clinical-ledger.tsx](file:///Users/dirghpatel/Documents/india-gummy-d2c/website/components/proof/clinical-ledger.tsx) with -15m sleep latency, +34m deep non-REM delta wave sleep, and 0g sugar.

### 3. Radical Comparison Matrix (`OxideProof`)
- **Seed Pattern:** Direct contrast against inferior mass-market supplements (synthetic fillers vs. micro-encapsulation).
- **Eatroz Execution:** [oxide-proof.tsx](file:///Users/dirghpatel/Documents/india-gummy-d2c/website/components/proof/oxide-proof.tsx) contrasting 4 Chelation Forms vs. 4% bioavailable Magnesium Oxide laxative.

### 4. Forensic Batch Transparency (`CoaModal`)
- **Seed/Cymbiotika Pattern:** Live batch verification modal displaying third-party lab assay certificates of analysis.
- **Eatroz Execution:** [coa-modal.tsx](file:///Users/dirghpatel/Documents/india-gummy-d2c/website/components/transparency/coa-modal.tsx) for NABL-accredited laboratory test for Batch `ETZ-01-A26`.

---

## 6. How to Run & Extract Updates (100% Free)

All extraction tools can be rerun anytime at zero cost:
```bash
cd website
npm run extract:all https://seed.com ./extracted-seed
```
Outputs are immediately generated and ready for Figma import via [open-htmltofigma](https://github.com/kevicebryan/open-htmltofigma) or local React code generation.
