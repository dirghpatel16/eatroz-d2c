# Orelius — Runway Packaging Prompt System

Date: 12 September 2026

## Recommended Runway workflow

Use **GPT Image 2 inside Runway** for still packaging concepts when legible words matter. Use the selected still as the input image for **Gen-4.5 Image to Video**, where the prompt should describe motion rather than repeat the pack design.

Create and save these references before generating:

1. `@orelius_logo` — a clean black-on-white vector or high-resolution wordmark.
2. `@orelius_layout` — a simple front-panel sketch showing the intended text hierarchy and location of the logo, product name, proof line, serving count, vegetarian mark, and flavor.
3. One route-specific material/color moodboard. Avoid combining several competitor packs into one reference; that encourages imitation instead of a distinct Orelius system.

Generate in this order: blank structural pack → approved hero still → alternate views → packaging family → image-to-video motion. Keep final FSSAI declarations, nutrition facts, barcode, batch data, claims, and QR code as artwork composited after generation.

## Shared brand and copy architecture

The concepts assume the proposed masterbrand `ORELIUS` and a hero daily-nutrition gummy. Replace every bracketed item only after formulation and regulatory review.

### Front panel

1. `ORELIUS`
2. `ONE DAILY` or the approved product name
3. `DAILY NUTRITION GUMMIES`
4. `[APPROVED ACTIVE / NUTRIENT PROOF LINE]`
5. `28 DAILY SERVINGS`
6. `[APPROVED FLAVOR]`
7. Small proof row: `PECTIN BASED · [APPROVED SUGAR CLAIM] · VEG`

### Back or side panel

- What it is: one plain-language sentence.
- Daily use: serving size and timing.
- Exact active amounts and nutrition information.
- Ingredient list and allergen statement.
- Storage guidance suitable for Indian heat and humidity.
- Warnings and “not for medicinal use” language as advised.
- FSSAI licence and mandatory manufacturer/marketer declarations.
- Net quantity, batch, MRP, manufacturing date, expiry/best-before, barcode.
- QR position reserved for a lot-specific finished-product test page only when operational.

### Visual constants across all three routes

- Adult, premium, sensorial Indian wellness.
- Hero palette: jamun purple `#5A1837`, mineral cream `#F1DFC0`, marigold `#E3A321`, dark cacao `#241419`.
- One type family with an expressive, heavy display face; one condensed or monospaced face for dose and evidence.
- Large product name and serving count readable at marketplace-thumbnail size.
- Restrained use of amla, jamun, kokum, or citrus as material studies rather than generic leaf decoration.
- Precise packaging geometry, believable folds, seals, closures, label stock, and scale.
- Vegetarian green-dot symbol and regulatory layout treated as small structured zones, not invented certification badges.

---

## H1 — Daily Reserve dispenser with 28 sealed sachets

### Strategic role

The strongest habit-design route. A slim countertop carton dispenses one sealed daily sachet at a time. It combines premium Indian food cues with visible daily counting and evidence-led transparency.

### Master still prompt — full packaging family

```text
Premium Indian daily nutrition gummy packaging system for the brand ORELIUS. A slim upright countertop dispenser carton in warm mineral-cream uncoated paperboard, approximately 110 mm wide, 175 mm tall and 65 mm deep, with a precise die-cut side drawer that releases one sachet at a time. Twenty-eight individually sealed pillow sachets are arranged inside in a disciplined vertical stack. The sachets use deep jamun-purple high-barrier film with a narrow marigold edge and large sequential day numbers from 01 to 28.

The front of the carton carries the exact hierarchy: small widely spaced ORELIUS wordmark at the top, very large two-line product name ONE DAILY in dark cacao, smaller line DAILY NUTRITION GUMMIES, one compact proof line reading [APPROVED ACTIVE / NUTRIENT PROOF LINE], and 28 DAILY SERVINGS near the bottom. A small pectin-based, approved sugar statement and vegetarian mark sit in a disciplined footer. Typography feels like contemporary premium food and editorial publishing, with an expressive heavy grotesk for ONE DAILY and a precise condensed sans for dose information.

The carton has a marigold pull tab labeled PULL, a perforated opening strip, crisp folded edges, tactile uncoated paper fibers, one selective gloss detail on the day-count line, and a structured side panel reserved for exact ingredients, directions, FSSAI information, batch data, barcode and QR code. A single opened sachet reveals three translucent jewel-like jamun-berry gummies with a soft pectin texture and realistic surface sheen.

The complete family is arranged on a pale sandstone tabletop: one closed dispenser facing front, one dispenser shown three-quarter open with numbered sachets visible, four loose sachets numbered 01, 02, 03 and 04, and three gummies. Refined contemporary Indian food styling uses one cut jamun, one amla and a small marigold pigment circle as restrained ingredients. Warm directional morning light, soft natural shadows, 50 mm commercial product photography, three-quarter eye-level angle, extremely sharp pack geometry, premium ecommerce campaign, sophisticated adult wellness, generous negative space, realistic print and material behavior, 4:5 vertical composition.
```

### Alternate still prompts

**Front/back technical presentation**

```text
Orthographic packaging design presentation of the ORELIUS ONE DAILY 28-day gummy dispenser. Front view, back view, left side panel, right side panel, open top view and one unfolded sachet shown on a warm neutral background. Mineral-cream uncoated carton, jamun-purple daily sachets, marigold pull tab, dark cacao typography. The front preserves the approved hierarchy; the back uses a clean modular grid with distinct zones for product explanation, serving instructions, exact active amounts, ingredients, nutrition facts, storage, warning, manufacturer and marketer details, FSSAI licence, net quantity, MRP, batch, barcode and QR. Precise dieline logic, believable folds and seals, professional packaging designer presentation, even studio lighting, high resolution.
```

**Unboxing lifestyle frame**

```text
Premium morning ritual featuring the ORELIUS ONE DAILY countertop dispenser on a contemporary Indian kitchen counter in Bengaluru. A well-groomed adult hand pulls one numbered jamun-purple sachet from the marigold side drawer. Pale limestone, ribbed glass, a stainless-steel tumbler and soft cotton create a refined lived-in scene. Early sun creates warm geometric shadows. The package remains the visual hero and its shape, palette and day-number system remain consistent. Calm, appetizing, modern, realistic commercial photography, 9:16.
```

### Gen-4.5 image-to-video prompt

```text
The camera makes a slow controlled 30-degree arc around the dispenser as a hand pulls one sachet smoothly from the side drawer. The numbered sachets shift subtly inside the carton. Morning sunlight moves gently across the paper texture. The hand tears the sachet cleanly and three gummies fall onto the palm. Premium product-film motion, natural hand movement, restrained pace, stable packaging geometry, shallow depth of field.
```

### Production guardrail

Use AI for structure, material, lighting and composition. Composite the exact day numbers and regulatory artwork in Illustrator or the final 3D render so the sequence and mandatory copy are correct.

---

## H2 — Grown-up daily snack pouch

### Strategic role

The fastest acquisition and ecommerce route. It treats daily nutrition like premium food, using an energetic pouch silhouette and large appetite-led typography while keeping one disciplined evidence panel.

### Master still prompt — full packaging family

```text
Bold premium Indian functional-gummy packaging for ORELIUS. A substantial high-barrier stand-up pouch with a broad stable base, soft-square shoulders, a crisp tear notch, press-to-close zipper and realistic heat-sealed top. The pouch is deep jamun purple with a warm mineral-cream front label field occupying the central sixty percent. A narrow transparent-look vertical product-view strip runs near the right edge as a glossy printed visual device; the principal packaging remains protective and opaque.

The front reads in a powerful editorial hierarchy: ORELIUS at the top, oversized stacked words GOOD EVERYDAY, smaller DAILY NUTRITION GUMMIES, one precise line [APPROVED ACTIVE / NUTRIENT PROOF LINE], 28 DAILY SERVINGS, [APPROVED FLAVOR], and a small footer for pectin based, approved sugar language and vegetarian mark. The display typography is broad, joyful and grown-up, closer to premium snacks and fashion magazines than a pharmacy label. Dose and evidence information use a contrasting condensed technical sans.

The pouch uses a marigold tear strip, a dark cacao side gusset, selective gloss on GOOD EVERYDAY, fine tactile film grain, clean seal details, and a large structured back-panel grid for exact active amounts, directions, nutrition, ingredients, warnings, storage, FSSAI declarations, manufacturer and marketer data, batch information, barcode and QR position. The pack communicates appetite first and proof immediately second.

Hero ecommerce arrangement on a saturated warm apricot-to-jamun studio set: one front-facing pouch, one three-quarter pouch showing the side gusset, one back-facing pouch showing the modular information grid, one small opened serving packet and six translucent berry-toned pectin gummies. Sculptural jamun, amla and kokum forms appear as sparse art-directed ingredients. Direct but refined studio light, crisp shadow edges, slight wide-angle energy without distortion, tactile high-end food photography, adult Indian culture, highly legible hierarchy, 4:5 vertical composition.
```

### Alternate still prompts

**Quick-commerce thumbnail test**

```text
Front-facing ORELIUS GOOD EVERYDAY stand-up pouch isolated on a clean warm-white ecommerce background. Deep jamun-purple pouch, large mineral-cream label field, marigold tear strip, dominant GOOD EVERYDAY product name, clear DAILY NUTRITION GUMMIES and 28 DAILY SERVINGS. Perfectly symmetrical geometry, realistic soft pouch folds, subtle grounding shadow, high contrast, benefit readable at small marketplace-thumbnail scale, 1:1 square composition.
```

**Social flat lay**

```text
Energetic overhead flat lay of the ORELIUS GOOD EVERYDAY gummy pouch, one torn daily packet, translucent gummies, jamun halves, amla slices, a phone, keys and stainless-steel water bottle. Jamun purple, marigold and apricot color blocking. Premium grown-up snack energy, decisive direct flash, controlled composition, slight real-world imperfection, crisp textures, fashion editorial product photography, 9:16.
```

### Gen-4.5 image-to-video prompt

```text
The pouch lands softly upright on the tabletop as the camera makes a short energetic push-in. A hand tears the top strip along the seal and opens the zipper. Three glossy gummies tumble into the hand while the pouch settles naturally. Direct-flash highlights travel across the selective-gloss lettering. Fast premium food-commercial pacing, stable pack shape, realistic pouch physics, crisp final hero frame.
```

### Production guardrail

A real transparent window may reduce moisture, oxygen or light protection. Treat it as printed trompe-l’œil in concepts until the packaging supplier and stability programme validate a functional window.

---

## H3 — Translucent reusable jar with 28-day refill

### Strategic role

The strongest countertop brand object and subscription ecosystem. The starter order supplies a tactile reusable jar; repeat orders arrive as lighter refill packs.

### Master still prompt — full packaging family

```text
Premium refillable Indian wellness packaging system for ORELIUS. The hero object is a soft-square reusable jar in translucent UV-filtering amber resin, approximately 85 mm wide and 115 mm tall, with gently rounded corners, a wide mouth and a deep jamun-purple matte screw cap. The amber body reveals an impression of jewel-toned gummies while preserving a sophisticated protective appearance. A minimal warm mineral-cream wrap label uses a die-cut vertical reveal and one small marigold calibration mark.

The jar front carries the exact hierarchy: ORELIUS, oversized DAILY CORE, DAILY NUTRITION GUMMIES, [APPROVED ACTIVE / NUTRIENT PROOF LINE], 28 DAILY SERVINGS and [APPROVED FLAVOR]. The label footer reserves pectin-based, approved sugar language and the vegetarian mark. A compact back label uses a highly organized modular information grid for daily use, exact active quantities, nutrition information, ingredients, warnings, storage, FSSAI declarations, manufacturer and marketer information, batch, MRP, barcode and QR position.

Beside the jar is a compact 28-day refill pouch in deep jamun-purple high-barrier film with oversized mineral-cream typography, a marigold seal strip and a clear statement 28-DAY REFILL. The refill uses the same brand hierarchy and ingredient cues as the jar. A small mineral-paper starter carton holds the jar and first refill together, creating a premium subscription unboxing system.

Hero composition on a sunshine-marigold studio background: the translucent amber jar in front, the refill pouch slightly behind, the open starter carton to the side, and four translucent gummies on a pale stone plinth. Restrained jamun and amla material studies appear at the edge of frame. Bright diffused daylight, clean specular highlights through the amber material, premium beauty-meets-food photography, precise realistic closure threads and label edges, adult and sensorial, generous negative space, 4:5 vertical composition.
```

### Alternate still prompts

**Refill action frame**

```text
Close commercial product photograph of an adult hand pouring ORELIUS gummies from the deep jamun 28-DAY REFILL pouch into the open translucent amber DAILY CORE jar. The wide-mouth jar, matte jamun cap, mineral label and marigold calibration mark remain precise. Gummies form a clean controlled arc and catch warm sunlight. Pale stone counter, modern Indian home, premium refill ritual, realistic materials and scale, shallow depth of field, 9:16.
```

**Three-SKU portfolio**

```text
Three coordinated ORELIUS translucent amber jars and matching refill pouches arranged as a premium wellness family. DAILY CORE uses marigold, GUT DAILY uses amla green, NIGHT REST uses jamun violet. The amber jar geometry, jamun caps, mineral labels, brand placement and evidence grid remain identical across all SKUs. Only the product name, one calibration color and one ingredient specimen change. High-end retail shelf presentation, warm neutral studio, even light, unmistakable masterbrand block, 16:9.
```

### Gen-4.5 image-to-video prompt

```text
The camera slowly pushes toward the open amber jar as a hand pours gummies from the refill pouch in one smooth controlled stream. The gummies catch the light inside the translucent jar. The hand closes the matte cap with a single confident twist, then the camera settles on the complete jar-and-refill system. Bright premium beauty-commercial motion, realistic object physics, clean reflections, stable label placement.
```

### Production guardrail

Specify UV-filtering or opaque material only as an aesthetic target until packaging engineering and stability tests confirm the product’s protection requirements. The sustainability story must use verified material and lifecycle facts.

---

## Reference-photo shortlist

### United States

- [Grüns official product](https://gruns.co/products/gruns) — reference for the 28-pack portable snack ritual and high-impact pouch, not its green palette or bear identity.
- [OLLY Sleep](https://www.olly.com/products/sleep-strawberry-sunset) — reference for squat geometry, benefit-first naming and a navigable color portfolio.
- [Ritual Essential for Women](https://ritual.com/products/essential-for-women-multivitamin) — reference for transparency, product visibility, whitespace and one recognizable yellow asset.
- [AG1 seven-count travel packs](https://drinkag1.com/products/greens-powder-7ct) — reference for a disciplined single-system brand and travel-dose packaging.
- [Lemme](https://lemmelive.com/) — reference for beauty-category desirability and collectible countertop objects.

### India

- [What’s Up Wellness catalog](https://www.whatsupwellness.in/collections/whatsup-catalog) — reference for benefit color and quick-commerce recognition; also evidence that bright cylindrical jars are crowded.
- [Kapiva gummies](https://kapiva.in/product/gummies/) — reference for ingredient provenance, dose cues and premium authority.
- [Little Joys gummies](https://ourlittlejoys.com/shop/gummies) — reference for portfolio navigation, approachability and quality communication.
- [Be Bodywise multivitamin gummies](https://bebodywise.com/product/multivitamin-gummies) — reference for concern-first ecommerce architecture and established no-added-refined-sugar language.
- [Man Matters multivitamin gummies](https://manmatters.com/dp/multivitamin-gummies/13410495) — reference for explicit serving count, active-led copy and men’s-wellness shelf codes.
- [Supply6 360](https://supplysix.com/products/supply6_360) — reference for India-specific daily sachet behavior and measured routine framing.

## Selection criteria after generating

Score each route from 1–5 on:

1. Brand recognition at 120-pixel thumbnail size.
2. Ability to identify brand, product type, benefit and 28-day count in five seconds.
3. Premium credibility at the intended selling price.
4. Adult appetite appeal without looking like confectionery for children.
5. Distinctiveness from Grüns, OLLY, What’s Up Wellness and Kapiva.
6. Believability of the material and closure in Indian distribution.
7. Ease of extending the system to Gut, Night and Daily Multi.
8. Packaging cost and fulfilment complexity.

Take the highest-scoring still from each route into consumer concept testing before choosing the production architecture.
