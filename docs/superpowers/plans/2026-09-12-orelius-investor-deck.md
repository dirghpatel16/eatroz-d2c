# Orelius Investor Deck Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Deliver an editable, evidence-first HTML investor deck and print-ready source report that define Orelius, test its India-first feasibility, and outline a compliant formula-development and capital path.

**Architecture:** Build the deck from a single slide-content/source manifest so claims, visible citations, and the accompanying source document remain consistent. Generate an editable browser-based slide deck matching the project’s existing `deck/index.html` format; produce a print-ready source report with the installed PDF renderer; revise only from the verified source manifest.

**Tech Stack:** HTML, CSS, browser JavaScript, project-native slide navigation, installed `make-pdf` renderer, Markdown source ledger, existing Python cohort model.

---

## File map

| Path | Responsibility |
|---|---|
| `strategy.md` | Baseline research and documented limitations from the prior project. |
| `model/cohort_model.py` | Reproducible 36-month cohort model and scenario output. |
| `video-research/transcripts/*.txt` | Primary founder statements on market size, capital efficiency, CAC pressure, and retention. |
| `research/orelius_research_refresh.md` | Refreshed source notes and explicitly dated claims used in the deck. |
| `deck/orelius.html` | Final interactive investor deck, following the existing HTML deck’s navigation contract. |
| `Orelius_Investor_Deck_Sources.pdf` | Print-ready evidence and formula-development report. |
| `Orelius_Investor_Deck_Sources.md` | Slide-level source ledger, slide manifest, and formula-development brief. |

### Task 1: Reconcile the evidence base

**Files:**
- Create: `research/orelius_research_refresh.md`
- Read: `strategy.md`, `model/cohort_model.py`, `video-research/transcripts/oziva_aarti_gill_neonshow_full.txt`, `video-research/transcripts/decoding_d2c_revant_bhate_full.txt`, `video-research/transcripts/plix_satiya_zaveri_lifeboat_full.txt`

- [x] **Step 1: Capture current first-party product references**

Record the access date, URL, quoted product characteristic, and slide use for: Grüns product page; Man Matters multivitamin gummies; Be Bodywise multivitamin gummies; Dabur Siens product/launch page; Kapiva gummies; Mosaic Wellness brand portfolio; Little Joys brand facts.

- [x] **Step 2: Capture regulatory primary sources**

Record FSSAI’s current health-supplements standards page, the 2022 operationalisation directions, and ASCI’s 2025 health-influencer guidance. State that the final formulation requires a qualified FSSAI/regulatory review and that GST classification remains unresolved.

- [x] **Step 3: Re-run the cohort model**

Run:

```bash
python3 model/cohort_model.py
```

Record only the reported ₹50L, ₹2Cr, and ₹5Cr scenario outputs. State the model’s optimistic-retention limitation next to its use in the deck.

- [x] **Step 4: Extract primary founder evidence**

Record the transcript locations and exact context for: Aarti Gill’s two-boxes/year retention statement, Revant Bhate’s sub-₹10,000Cr VMS market assessment, and Plix’s CAC-inflation and capital-discipline observations.

- [x] **Step 5: Reconcile claims**

For every claim that has an unresolved conflict, label it `Verified`, `Benchmark / assumption`, `Proposed target`, or `Open diligence`. Exclude unsupported revenue, certification, exit-value, and clinical-efficacy claims.

### Task 2: Write the slide manifest and source ledger

**Files:**
- Create: `Orelius_Investor_Deck_Sources.md`
- Read: `docs/superpowers/specs/2026-09-12-orelius-investor-deck-design.md`

- [x] **Step 1: Define 20 core slides and 6 appendix slides**

Use the approved design’s slide order. The source ledger records each slide’s number, title, evidence type, short citation, full source, and scope limitation.

- [x] **Step 2: Write the product and formulation slides**

Use public Grüns label categories as a benchmark. Describe Orelius only as a proposed target profile: 3–5 pectin gummies/day, low/zero-added-sugar preference, daily pack, testing and stability gates. Do not claim formula equivalence, final dosage, approval, clinical efficacy, or verified 60°C performance for Orelius.

- [x] **Step 3: Write feasibility, economics, and capital slides**

Present India feasibility as conditional. Show competitor roles, category limits, retention dependence, order-level economics, and three model scenarios. Display the ₹5Cr sensitivity as ₹1.5–20Cr Month-36 run-rate, depending on retention assumptions.

- [x] **Step 4: Write operational and risk slides**

Include D2C-first rollout, prepaid bias, creator-learning process, Month-2/3 retention gate, quality/testing plan, regulatory claims controls, GST/trademark/certification diligence, and incumbent response risk.

- [x] **Step 5: Build the source document**

Group full citations by slide and retain every access date. Add a formula-development brief that maps public benchmark categories to development decisions without reproducing proprietary blend allocations.

### Task 3: Create the interactive presentation

**Files:**
- Create: `deck/orelius.html`
- Read: `Orelius_Investor_Deck_Sources.md`

- [x] **Step 1: Read the existing deck’s interaction contract**

Reuse the keyboard, dot-rail, and touch/scroll navigation contract in `deck/index.html` without reusing its placeholder name or commercial claims.

- [x] **Step 2: Establish a visual system**

Use a restrained premium palette: mineral white, deep forest/ink, muted lime, and one citrus accent. Use one consistent type family, 42pt+ cover text, 32pt+ slide titles, 17pt+ body text, editable native tables/charts, and visible lower-corner source footers.

- [x] **Step 3: Build the slides in narrative sequence**

Create a minimal cover, evidence comparisons, one formatted product-label benchmark table, a competitor-positioning matrix, a gated-GTM timeline, financial scenario chart, risk register, and closing investment thesis. Keep no slide dependent on an unsupported claim.

- [x] **Step 4: Add visible sources and disclosures**

Use visible lower-corner source footers. Keep product-status, model-assumption, and regulatory caveats on the slide when an investor must see them to interpret the claim.

- [x] **Step 5: Validate the standalone deck**

Open `deck/orelius.html` as a standalone file and verify that the slide count, keyboard navigation, dot navigation, links, and mobile layout work without any build server.

### Task 4: Render and inspect the evidence report

**Files:**
- Create: `Orelius_Investor_Deck_Sources.pdf`
- Modify: `Orelius_Investor_Deck_Sources.md` if report defects appear

- [x] **Step 1: Render the evidence report**

Use `/Users/dirghpatel/.claude/skills/gstack/make-pdf/dist/pdf` to generate `Orelius_Investor_Deck_Sources.pdf` from the Markdown ledger.

- [x] **Step 2: Inspect the deck and report at readable scale**

Check slide count, text overflow, object overlap, contrast, legibility of source footers, label accuracy, chart axes, table alignment, and source/caveat visibility.

- [x] **Step 3: Correct defects**

Revise crowded copy before reducing font size. Re-render the report and recheck the deck after each layout correction until no clipping or overlap remains.

- [x] **Step 4: Verify source accessibility**

Confirm that the deck’s source footers point to the source ledger and that the report preserves all full URLs, access dates, evidence labels, and formula-development limits.

### Task 5: Final integrity pass and delivery

**Files:**
- Modify: `deck/orelius.html`
- Modify: `Orelius_Investor_Deck_Sources.pdf`
- Modify: `Orelius_Investor_Deck_Sources.md`
- Modify: `research/orelius_research_refresh.md`

- [x] **Step 1: Audit every factual claim**

Ensure every factual statement has a primary/current source or a clearly visible `Benchmark / assumption` label. Preserve uncertainty around GST, certification, trademarks, clinical evidence, final formula, and long-term scale.

- [x] **Step 2: Recheck financial statements**

Confirm that slide figures reconcile with a fresh model run. Do not display any India-only $1B or ₹150–400Cr self-funded conclusion.

- [x] **Step 3: Check delivery files**

Confirm the HTML deck opens, report page count matches, source-ledger links resolve, and all deliverables sit at the project root or `deck/` folder as stated in the file map.

- [x] **Step 4: Record completion**

Mark every executed plan step complete. This project folder is not a Git repository, so do not create a commit; preserve the source ledger and research refresh as the handoff record.

## Plan self-review

The tasks cover all approved requirements: investor audience, full product-to-capital narrative, public-label benchmarking, India competitor feasibility, compliant formula-development gates, GTM, retention, model-based economics, risks, source ledger, standalone HTML deck, rendered PDF, and integrity review. The plan does not claim a final formula, regulatory approval, verification of non-WHO-GMP certifications, a GST result, or a guaranteed outcome. No task contains a deferred implementation placeholder.

## Execution record — 12 September 2026

- [x] Captured and cross-checked first-party Grüns and Indian competitor references, FSSAI/ASCI primary sources, retained founder evidence, and local model output.
- [x] Produced the investor narrative, formula-development brief, feasibility analysis, unit-economics/risk content, source ledger, and open-diligence disclosures.
- [x] Built the standalone 20-slide HTML deck with source footers, keyboard/navigation controls, and a responsive layout.
- [x] Rendered the companion source packet as PDF and visually inspected representative pages.
- [x] Checked HTML structure and inline JavaScript; browser QA recorded 20 slides, 20 source footers, and no console errors.
- [x] Kept formula, claims, GST, trademark, and manufacturing-certificate matters explicitly pending qualified verification.
