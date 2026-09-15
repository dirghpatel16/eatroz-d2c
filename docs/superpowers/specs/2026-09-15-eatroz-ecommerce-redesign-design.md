# Eatroz E-commerce Website Redesign

Date: 15 September 2026  
Status: Approved design direction; implementation requires a separate plan  
Product state: Pre-launch magnesium gummy; packaging and formulation remain provisional

## 1. Outcome

Build a visual-first, high-end D2C storefront for Eatroz that can switch from pre-launch lead capture to live commerce without a structural redesign.

The experience combines three approved directions:

1. **Film → Shop:** a cinematic product film opens the site, with the primary commercial action present immediately.
2. **The Exploded Formula:** product motion transitions into a scroll-led explanation of the four magnesium forms.
3. **The First Drop:** launch energy, limited first-batch framing, and bold commercial typography give the pre-launch experience urgency without fabricated scarcity.

The opening Runway sequence is **Four Forms Fall**: one macro gummy becomes four, the four move around the pouch, and the composition resolves into a clean `DROP 01` purchase frame.

## 2. Design Principles

### 2.1 Product first

The site is a store, not a long brand manifesto. Product, price state, and primary action appear within the first viewport. Product imagery appears in every major selling section.

### 2.2 Visual abundance with role discipline

The first release uses at least four distinct visual roles:

- cinematic hero film;
- pouch beauty shot;
- translucent gummy macro;
- ingredient/proof visualization;
- evening-use lifestyle frame when it passes realism review; otherwise a second pouch-detail composition fills this role.

The same centered pack photograph must not be repeated as the answer to every section.

### 2.3 Micro-to-macro storytelling

The visual sequence moves between gummy surface detail, individual chemical forms, the complete pouch, and the nightly-use context. Scientific complexity is revealed through scale and interaction instead of long uninterrupted copy.

### 2.4 Editorial density, not empty minimalism

Information is deliberately present but hierarchically controlled. Large product moments alternate with compact labels, diagrams, buying controls, and source notes. Spaciousness supports comprehension; it must not create product-free screens.

### 2.5 Clarity plus one memorable surprise

Commerce behavior stays conventional and understandable. `Four Forms Fall` is the signature surprise. Additional animation must support orientation, product inspection, or evidence comprehension rather than compete with the hero.

### 2.6 Evidence honesty

The site must not invent reviews, stock scarcity, countdowns, certifications, clinical claims, ingredient quantities, percentage RDA, manufacturing facts, or shipping promises.

Unconfirmed product facts use a controlled `verification_pending` state in content data. Customer-facing rendering uses plain language such as “Final formulation details will be published before orders open”; internal bracketed notes must never leak into live customer copy.

## 3. Brand Treatment

The supplied product photograph is a provisional reference, not final packaging artwork.

Preserve from the reference:

- warm terracotta photographic world;
- tactile off-white pouch material;
- large editorial product typography;
- fine mineral/topographic line device;
- visible, appetizing product presence.

Rework before production:

- remove or withhold unverified “liposomal delivery” language;
- withhold sleep, stress, and muscle-recovery claims until substantiated and approved;
- replace generic bear-shaped gummies if an ownable, adult-coded form becomes feasible;
- composite final label typography and regulatory text from approved artwork rather than trusting generative text;
- use the final verified formula, dose, serving count, percentage RDA, FSSAI declarations, batch/expiry fields, and tamper-evidence specification.

Existing sage, warm canvas, ink, and terracotta tokens remain the base system. The website uses terracotta more assertively in `DROP 01` launch moments than the earlier restrained draft, while limiting it to product, action, and transition emphasis rather than decorative confetti.

## 4. Page Architecture

### Section 1 — Four Forms Fall hero

- Full-bleed muted autoplay film when device and user preferences allow.
- Sequence: gummy macro → four controlled gummies → orbit around pouch → `DROP 01` product lockup.
- Product name, current commercial state, and primary CTA remain visible over or beside the film.
- Provide visible pause/play and mute controls.
- Respect `prefers-reduced-motion` and use an approved still fallback.
- Mobile uses the final lockup still by default. A shorter video crop replaces it only after the implementation verification demonstrates acceptable loading, legibility, and motion behavior on the target mobile viewport.

### Section 2 — Immediate purchase dock

- Pouch gallery thumbnail or still.
- Product name.
- Price only when explicitly approved.
- Serving-count status.
- One-time/subscription selection only when both purchase models are operational.
- Delivery summary only when verified.
- Primary action tied to the active commerce mode.
- Persistent compact mobile CTA after the hero.

### Section 3 — The Exploded Formula

- Sticky pouch or pouch-derived visual.
- Four controlled product elements separate during scroll.
- Each element introduces one named form: glycinate, citrate, malate, or taurate.
- Explanations remain concise and source-backed.
- No dosage or bioavailability comparison is shown without approved evidence.

### Section 4 — Why zero oxide

- Comparative evidence visualization rather than a dense permanent table.
- Methodology and citations sit directly beneath the graphic.
- The ring dial renders real percentage RDA only after the formulation is verified.
- Before verification, the ring is replaced by a neutral formulation-status device; it must not show a decorative or arbitrary completion percentage.

### Section 5 — Product appetite gallery

- Pouch beauty photograph.
- Gummy macro with believable translucency and surface physics.
- Evening ritual or use-context photograph if realistic and claim-safe.
- Editorial crops alternate with clear product navigation or purchase actions.
- Every generated asset is labeled internally as provisional campaign art.

### Section 6 — Ritual and transparent facts

- Concise nightly-use sequence.
- Expandable Supplement Facts surface.
- Formulation status and tamper-evidence information.
- Future batch-specific Certificate of Analysis link when a real document exists.

### Section 7 — Trust without fabrication

- Pre-launch: founder intent, formulation commitments, verified sources, and an explicit description of what will be published before ordering opens.
- Live launch: genuine customer reviews may appear only after real review data exists.
- Never generate placeholder testimonials, rating counts, publication logos, or laboratory badges.

### Section 8 — Final conversion and footer

- Mode-aware CTA.
- Verified delivery and returns summary.
- FAQ.
- Contact and policy links.
- Appropriate formulation and generated-imagery disclosures.

## 5. Switchable Commerce Mode

Commerce mode is a single configuration value, not duplicated markup.

### `prelaunch`

- CTA: `Join the First Drop`.
- Opens a lead-capture drawer.
- Collect only fields approved for the launch campaign.
- Do not present a working cart, purchasable inventory, fake stock, or artificial countdown.
- Price can appear only if approved and clearly marked as launch pricing when applicable.

### `live`

- CTA: `Add to Bag` with approved price.
- Enables quantity, cart drawer, inventory response, and checkout link.
- Enables one-time/subscription choice only if the commerce backend supports both.
- Review components remain data-gated and do not appear merely because commerce mode is live.

### Failure behavior

- If configuration is missing or invalid, fail closed into `prelaunch`.
- If checkout or inventory services fail, retain product information but replace purchase actions with a non-transactional availability message.
- If lead submission fails, preserve the entered value locally for the current session and show a retry action; never show false success.

## 6. Runway Visual System and Credit Guardrail

Available allowance reported by the user: 500 Runway credits.

Budget ceiling for the initial approved website visual set:

- up to 100 credits for still/reference exploration;
- up to 200 credits for the `Four Forms Fall` hero generation and one targeted correction;
- up to 100 credits for supporting motion or alternate crops;
- keep at least 100 credits unspent until the integrated website is reviewed at desktop and mobile sizes.

Generation sequence:

1. Import the provisional pouch reference into the project asset workflow.
2. Generate three still keyframe candidates for `Four Forms Fall`.
3. Review pouch shape, label integrity, gummy physics, lighting, and negative space.
4. Approve one start/end-frame system.
5. Generate the shortest viable hero motion.
6. Make at most one targeted correction before testing it in the page.
7. Spend reserved credits only after the integrated page reveals a specific visual gap.

Runway must not be trusted to render final regulatory copy. Final pack-facing text is composited in deterministic web or design layers where practical.

## 7. Interaction and Motion

- Hero film supplies the primary cinematic moment.
- Exploded Formula uses seek-safe scroll progress so elements remain correct when users scroll backward or jump.
- Purchase controls never depend on animation completion.
- Reduced-motion users receive direct state changes and still imagery.
- Decorative smooth scrolling must not interfere with native focus, anchor navigation, or browser history.
- Product gallery supports pointer, touch, and keyboard operation.
- Animations stop when off-screen or when the page becomes hidden.

## 8. Content and Data Boundaries

Store product facts in structured content rather than embedding them inside generated images.

Minimum product fields:

- `commerce_mode`;
- `product_name`;
- `price_status` and approved price value;
- `formulation_status`;
- chemical forms;
- elemental magnesium status/value/unit;
- serving-count status/value;
- percentage-RDA status/value;
- delivery status/copy;
- subscription availability;
- checkout availability;
- review availability;
- supplement-facts document availability;
- certificate-of-analysis availability.

Each unverified factual field is absent or explicitly marked `verification_pending`. Presentation components must not substitute estimates.

## 9. Technical Direction

Use a maintainable component structure rather than extending the monolithic prototype indefinitely. The implementation plan will choose the lightest production-capable stack after verifying current dependencies and commerce requirements.

Required component boundaries:

- site shell and mode configuration;
- hero media and controls;
- purchase dock;
- lead-capture drawer;
- cart drawer and checkout adapter;
- exploded-formula story;
- evidence visualization;
- product gallery;
- facts disclosure;
- trust section;
- footer and policies.

The commerce adapter must allow a hosted checkout or headless commerce backend to be introduced without rewriting presentation components.

## 10. Accessibility, Performance, and SEO

- Semantic headings and landmark regions.
- Keyboard-accessible drawers, gallery, media controls, and purchase options.
- Focus trapping and restoration for modal surfaces.
- Meaningful alternative text for product imagery; decorative motion is hidden from assistive technology.
- Sufficient contrast across terracotta, sage, dark, and canvas surfaces.
- Responsive art direction rather than desktop video merely scaled down.
- Reserve media dimensions to prevent layout shift.
- Load a poster image before video and defer non-critical media below the fold.
- Product structured data includes only approved, currently true commercial fields.
- Pre-launch pages must not emit in-stock or review schema without real supporting data.

## 11. Verification

Before handoff, verify:

- desktop and mobile screenshots against this specification;
- pre-launch and live modes separately;
- invalid/missing configuration fails into pre-launch;
- reduced-motion behavior;
- keyboard and focus behavior;
- media fallback when video fails;
- lead-capture success and failure paths;
- cart and checkout unavailable states;
- no unverified claims, fake reviews, stock pressure, badges, or schema;
- generated product imagery for warped packaging, label corruption, duplicated gummies, implausible shadows, rigid liquid-like surfaces, and over-perfect camera motion;
- performance with hero video enabled and disabled.

## 12. Explicit Non-goals for the First Build

- Final packaging artwork or print-ready compliance layout.
- Inventing the final formulation.
- Publishing a fabricated Certificate of Analysis.
- Full customer account system.
- Loyalty program, quizzes, or broad multi-SKU navigation.
- Heavy 3D/WebGL effects that compete with the product film.
- Fake reviews, influencer content, press coverage, scarcity, or countdowns.

## 13. Approval Record

The user approved:

- full rejection of the earlier website concept;
- a visual-first e-commerce restart;
- the combined `Film → Shop`, `Exploded Formula`, and `First Drop` direction;
- `Four Forms Fall` as the hero-film storyboard;
- switchable pre-launch/live-launch commerce;
- the eight-section page architecture;
- the additional design principles derived from current US brand, design-studio, and product-page research.
