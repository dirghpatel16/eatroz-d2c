# Eatroz D2C Product Storefront — Design Specification

Date: 2026-09-19  
Status: e-commerce-first redesign after rejection of campaign/editorial layouts

## Decision

Build a real single-product D2C product-detail page, not a brand manifesto or bio-research site. The first screen must answer: **What is it? What does the pouch look like? What pack can I choose? What will I pay? How do I act?** Until commercial facts are verified, the price and checkout are explicitly unavailable and the action is early access. The commerce layout remains visible so the page can switch to verified selling without structural redesign.

The existing cream-and-copper Eatroz pouch artwork is the visual identity. Website typography is a native system sans stack. The site has warm paper surfaces, ink text, copper actions, and one deep-green proof chapter. A product photograph is the hero, not an oversized headline.

## Desktop wireframe

```text
┌─────────────────────────────────────────────────────────────────────┐
│ Small launch-status / India utility strip                           │
├─────────────────────────────────────────────────────────────────────┤
│ EATROZ      Shop  Why Eatroz  Ingredients  FAQs       First access   │
├─────────────────────────────────────────────────────────────────────┤
│ Home / Magnesium Gummies                                             │
│ ┌────────────────────────────────┐ ┌───────────────────────────────┐ │
│ │  large product photograph      │ │ Drop 01 · Magnesium Gummies   │ │
│ │  (zoom / gallery controls)     │ │ honest short product summary  │ │
│ │                                │ │ Price: revealed before sale    │ │
│ │                                │ │ Choose: 1 / 2 / 3 pouches*     │ │
│ │                                │ │ [Get first access]            │ │
│ │  01  02  03  04  05 thumbnails │ │ what is known / pending       │ │
│ └────────────────────────────────┘ └───────────────────────────────┘ │
│ * Bundle options are design previews, not launched offers.          │
├─────────────────────────────────────────────────────────────────────┤
│ concise product assurances / verified facts only                    │
├─────────────────────────────────────────────────────────────────────┤
│ tactile gummy/ritual photo + why this format                         │
├─────────────────────────────────────────────────────────────────────┤
│ The Eatroz Standard: an original evidence-first comparison          │
├─────────────────────────────────────────────────────────────────────┤
│ Ingredients & label disclosure / how to chew / FAQs                 │
├─────────────────────────────────────────────────────────────────────┤
│ Final product action + footer                                        │
└─────────────────────────────────────────────────────────────────────┘
```

## Mobile wireframe

Compact header → breadcrumb and title → swipeable primary image with visible slide count → thumbnail rail → pack selection and large action → short transparent disclosure → sticky bottom action after the main CTA leaves view. Do not move science/storytelling ahead of the purchase interface. All tap targets at least 44 px; no horizontal overflow.

## Product media

Use the original Eatroz pouch enhancement and its existing product, gummy, and corrected chewable ritual images. Gallery views should cover front/scale, gummy detail, pouch context, and lifestyle. Generate missing stills against the *original pouch reference*, and mark all renders conceptual. Never show a gummy dissolving in water. No invented final back-label copy.

## Commerce and claims contract

Use a typed `pending | verified` fact model. Before verification, no numerical price, discount, elemental dose, serving count, review count, stock, ETA, COD/UPI availability, returns, subscription, certification, FSSAI number, or efficacy result is presented as fact. The 1/2/3 pouch selector is explicitly a bundle **preview** and cannot add to cart. The CTA captures early interest; its success state must distinguish client-side demo behavior from a connected email provider. Verified Shopify data later enables price, availability, cart and checkout without replacing the visual system.

## Distinctive brand layer beneath the PDP

1. Sensory but honest product photography: pouch and bead-shaped gummies are tangible and appetizing.
2. A dark “What to look for” standard: form disclosure, elemental dose, full ingredients, batch testing. Eatroz receives a positive status only when evidence exists. Do not clone Cymbiotika's layout or compare named brands without substantiation.
3. A short, useful chewable ritual; no water requirement or treatment promise.
4. Clear label and FAQ disclosures where unknowns are plainly marked before orders open.

## Technical and acceptance criteria

- Next.js 16 App Router, React 19, TypeScript, Tailwind CSS 4, with client code isolated to interactive controls. No unnecessary scroll hijacking.
- System-font stack; WCAG-aware color contrast and visible focus; reduced-motion support; semantic table/accordions/form controls.
- Responsive gallery, bundle-preview selector, mobile sticky CTA, and accessible early-access dialog/form.
- Product data and rendering tests prove unverified facts do not appear; gallery/selection/form tests prove behavior.
- Lint, type check, unit tests, production build, browser tests, and desktop/mobile visual inspection pass before handoff.

## External design and implementation references

- [Shopify Dawn product structure](https://github.com/Shopify/dawn/blob/main/templates/product.json): media, title, price, variants, quantity and buy controls co-located; sticky product information.
- [Vercel Next.js Commerce](https://github.com/vercel/commerce) and [Vercel Shop](https://github.com/vercel/shop): official Next/Shopify integration models, not copied storefront design.
- [Baymard product-page research](https://baymard.com/research/product-page): product images and a clear buy section drive evaluation.
- Current Indian category pages: [Wellbeing Nutrition](https://wellbeingnutrition.com/), [Be Bodywise magnesium gummies](https://bebodywise.com/product/magnesium-glycinate-capsules-60), [Kapiva](https://kapiva.in/), and [Man Matters](https://manmatters.com/dp/magnesium-gummies/2025021) inform local purchase conventions, not Eatroz claims.
