# Orelius investor deck

## Sources and formula-development brief

This document supports `deck/orelius.html`. It records the source, evidence type, and limitation behind each material statement. Access date: **12 September 2026**, unless a source date is stated otherwise.

## Evidence convention

- **Verified**: official current source, regulator, stored primary transcript, or reproducible local model.
- **Benchmark / assumption**: planning input, not a claim about Orelius.
- **Proposed target**: requires formulation, testing, and commercial validation.
- **Open diligence**: requires an external professional or internal proof before use.

## Slide-by-slide sources

The final HTML deck contains 20 slides. During design, one planned transition slide was removed; the narrative and source records below retain their working sequence so the evidence trail remains intact. Match by slide title rather than the printed section number where the two differ.

### 1. Orelius

**Proposed target.** Orelius is a proposed India-first daily-nutrition brand. The deck does not assert an existing market launch, final formula, FSSAI approval, or confirmed trademark.

### 2. The adherence problem

**Inference.** The deck synthesises the convenience language used by official brand pages and the global product format. It does not assert a quantified India-wide pill-fatigue rate. [Grüns](https://gruns.co/products/gruns); [Man Matters](https://manmatters.com/dp/multivitamin-gummies/13410495); [Be Bodywise](https://bebodywise.com/product/multivitamin-gummies).

### 3. Grüns: public reference product

**Verified.** One 20g daily pack; 28 packs; 50 kcal; 15g carbohydrate; 6g fibre; 8g added sugar; 20+ vitamins/minerals; 8.7g Core Nutrients Blend; pectin base. [Grüns product page](https://gruns.co/products/gruns).

### 4. India needs a different product

**Verified / inference.** Grüns’ public label carries 8g added sugar and an eight-gummy serving. Man Matters specifies two gummies/day and Be Bodywise one gummy/day. The lower-count Orelius design is a proposal based on these observed norms, not a proven consumer preference. [Grüns](https://gruns.co/products/gruns); [Man Matters](https://manmatters.com/dp/multivitamin-gummies/13410495); [Be Bodywise](https://bebodywise.com/product/multivitamin-gummies).

### 5. India feasibility

**Verified transcript evidence.** Mosaic founder Revant Bhate says the VMS market is below ₹10,000 crore. The conditional feasibility conclusion is analyst judgment. `video-research/transcripts/decoding_d2c_revant_bhate_full.txt`, lines 911–920.

### 6. Competition: what each brand proves

**Verified.** Mosaic confirms Man Matters, Be Bodywise and Little Joys as portfolio brands. [Mosaic Wellness](https://mosaicwellness.in/). Man Matters: 60 gummies/₹749/two daily. [Man Matters](https://manmatters.com/dp/multivitamin-gummies/13410495). Be Bodywise: ₹699/one daily/no added refined sugar. [Be Bodywise](https://bebodywise.com/product/multivitamin-gummies). Siens: Dabur’s premium D2C supplement entry, 2025. [Dabur](https://www.dabur.com/press-releases/dabur-enters-nutraceutical-category-with-siens). Little Joys: age-specific gummies and batch-quality communication. [Little Joys](https://ourlittlejoys.com/brand-facts/). Kapiva: ₹999/60 Shilajit gummies, one daily and NABL-report claim. [Kapiva](https://kapiva.in/trending-products/kapiva-gummies/).

### 7. The competitive opening

**Inference.** The cited current brand pages support targeted, concern-specific propositions. The assertion that an evidence-first daily-nutrition ritual is an available opening is a research inference, not a census of every Indian SKU.

### 8. Orelius positioning

**Proposed target.** Positioning: “daily nutrition made credible and convenient for India.” This is a strategic choice, not a verified claim.

### 9. Product target profile

**Proposed target.** Three to five pectin gummies/day; low/no added sugar target; 7-day trial pack and 28-day replenishment pack; declared active amounts; no claim that this is final or approved.

### 10. Formula logic

**Verified benchmark / proposed target.** Grüns’ public label combines vitamins/minerals, fibre/prebiotic, and a broad food/botanical blend. Orelius proposes transparent amounts, a more limited and meaningful blend, and finished-product testing. [Grüns](https://gruns.co/products/gruns).

### 11. Development gates

**Open diligence.** Ingredient eligibility, permitted levels, shelf-life, stability, microbiology, contaminants, and claim wording require finished-product work and qualified regulatory review. [FSSAI Health Supplements](https://www.fssai.gov.in/standards/health-supplements); [FSSAI 2022 operationalised framework](https://www.fssai.gov.in/upload/advisories/2022/03/6243ef28079ceDirection_Nutra_30_03_2022.pdf).

### 12. Trust system

**Verified benchmark / proposed target.** Little Joys describes third-party heavy-metal testing and report access. Kapiva says its Shilajit gummy carries an NABL report. Orelius’ lot-specific finished-product reports remain a proposed system. [Little Joys](https://ourlittlejoys.com/brand-facts/); [Kapiva](https://kapiva.in/trending-products/kapiva-gummies/).

### 13. Audience and occasion

**Proposed target.** India 18–35, time-poor consumers who want convenient nutrition. No population-size statistic is asserted. The initial customer research plan tests convenience, taste, trust, and repurchase rather than treating intent as purchase.

### 14. Go-to-market

**Benchmark / proposed target.** D2C and Amazon first; prepaid incentives; creator learning loop; later quick-commerce discovery. The source report contains the modelled/order-level rationale. `strategy.md`, Part F5 and Part G3.

### 15. Retention gate

**Verified transcript evidence / proposed decision rule.** Aarti Gill’s statement: scaled Indian adult-nutrition brands saw a maximum of two boxes/year. The ≥35% Month-2/3 gate is a proposed investment control, not an industry statistic. `video-research/transcripts/oziva_aarti_gill_neonshow_full.txt`, lines 865–892; `strategy.md`, Part G7.

### 16. Unit economics

**Benchmark / assumption.** AOV ₹699; contribution margin before marketing ₹370–420; CAC ₹350–600. These are model inputs, not Orelius results. `strategy.md`, Part F5.

### 17. Financial scenarios

**Verified model output.** Fresh local run of `model/cohort_model.py` on 12 Sep 2026: ₹50L minimum cash falls negative; ₹2Cr reaches ~₹5.5Cr month-36 annualised run-rate; ₹5Cr reaches ~₹20.8Cr under the optimistic curve. The India-repeat stress test in `strategy.md` Part G7 produces ~₹1.45Cr for the ₹5Cr scenario. The stress test does not use audited Orelius data.

### 18. Capital logic

**Analytical judgment.** Release larger growth capital only when the final formula, quality system, first-order contribution, prepaid mix, and retention gate are proven. This avoids presenting a capital input as a substitute for product-market fit.

### 19. Risks and controls

**Verified/open diligence.** FSSAI framework: disease claims sit outside the category unless specifically permitted. [FSSAI framework](https://www.fssai.gov.in/upload/advisories/2022/03/6243ef28079ceDirection_Nutra_30_03_2022.pdf). ASCI: paid/incentivised influencer promotion requires disclosure and technical health advice needs relevant qualifications. [ASCI](https://www.ascionline.in/the-asci-code-guidelines/). GST, trademark, and non-WHO-GMP certification are open diligence items. `strategy.md`, Parts F4b and H0.

### 20. Investment thesis

**Analytical judgment.** The deck recommends a controlled validation investment, not an immediate India-only billion-dollar outcome. The conclusion follows from the competitor, founder-transcript, regulatory, and model evidence above.

## Formula-development brief for Softpills and regulatory review

### Product intent

Create a vegetarian pectin daily-nutrition gummy for Indian adults. The goal is habitual convenience without representing the product as a replacement for a varied diet, vegetables, a medical treatment, or a formula-equivalent version of Grüns.

### Reference and boundaries

| Public Grüns category | Orelius development response | Boundary |
|---|---|---|
| Vitamins and minerals | Select permitted micronutrients with transparent finished-product label amounts | Do not transplant Grüns percentages or US Daily Values into India. |
| Fibre and prebiotic | Evaluate a tolerable, stable fibre/prebiotic system | Establish gastrointestinal tolerance and labelling after formulator review. |
| Fruit/vegetable/botanical blend | Use a limited, traceable blend only where ingredient eligibility and meaningful dosage are demonstrated | Do not hide negligible quantities inside a large marketing blend. |
| Pectin base | Develop a pectin matrix compatible with shelf-life and sensory objectives | Finished-product stability testing defines performance. |
| Sweetness | Prioritise no added sugar or low added sugar without misleading “sugar-free” language | Validate the actual nutrition panel and legal definition. |

### Required technical package

1. Master formula and supplier specification for every raw material.
2. Regulatory eligibility and permitted-level review for the intended adult population.
3. Pilot-batch sensory, texture, and packaging trials.
4. Active assay and stability protocol at release, interim, and end-of-shelf-life points.
5. Microbiological, heavy-metal, and contaminant plan for every finished batch.
6. Pack label, claims matrix, warnings, use instructions, and a review trail.
7. Consumer test protocol that measures reorder intent and actual second-order behaviour separately.

## Research methods and limitations

Composio Search and Fetch URL Content supported current-source discovery and official-page extraction. Tavily supplied a second independent search pass. The deck treats commercial market reports as secondary source candidates and does not use their headline market-size forecasts to override first-party/transcript limitations. `yt-transcript` and `yt-video-ask` remain available for a targeted video question but were not used to manufacture evidence where official sources already provided the relevant claim.

## Mandatory pre-circulation checks

1. Human-supervised trademark clearance for Orelius in relevant Indian classes.
2. Exact final product GST/HSN advice.
3. Certificate pack for all manufacturing claims beyond Sanode’s publicly stated WHO-GMP.
4. Finished Orelius formula, nutrition panel, and claims approval by the appropriate food/regulatory professionals.
5. Finished-product lab results before “lab tested,” “heat stable,” or any specific quality assertion enters external material.
