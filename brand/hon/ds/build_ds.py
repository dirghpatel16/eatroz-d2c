#!/usr/bin/env python3
"""Builds the HON Design System content under ds/project/ (published to the Design System artifact).

Sources: the HON wordmark (logo/build_wordmark.py: "HON" in Bagel Fat One, 12 colourways), the backlit
cherry-red gummy photo, the Be Bodywise pouch format (215 x 255 mm, wrapped gummies), and the pack DATA.

Run:  uv run --with fonttools python3 build_ds.py
Writes tokens, README, component previews, the cover, logo copies and outlined-text SVG mockups.
The index (project/design-system.json) is written at publish time, after the asset uploads.
"""
import json
import shutil
import sys
from io import BytesIO
from pathlib import Path

from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont

HERE = Path(__file__).resolve().parent
OUT = HERE / "project"
LOGO = HERE.parent / "logo"

MUSTARD, CHOC, CREAM, PAPER = "#F3C75A", "#513223", "#FFF4E6", "#FBF3E4"
CHERRY, CHERRY_BRIGHT, CHOC_SOFT, MUSTARD_DEEP, VEG = "#6A0D27", "#A8173B", "#7A5540", "#D9A93A", "#008F3A"

# ---------------------------------------------------------------- outlined type
_f = {}


def font(key):
    if key not in _f:
        if key == "bagel":
            _f[key] = TTFont(HERE / "fonts" / "BagelFatOne-Regular.ttf")
        else:
            w = {"archivo-bold": 700, "archivo": 500, "archivo-black": 850}[key]
            vf = TTFont(HERE / "fonts" / "Archivo-Variable.ttf")
            inst = instantiateVariableFont(vf, {"wght": w, "wdth": 100})
            buf = BytesIO()
            inst.save(buf)
            buf.seek(0)
            _f[key] = TTFont(buf)
    return _f[key]


def txt(s, key, size, x, y, fill, anchor="start", tracking=0.0):
    f = font(key)
    upm, cmap, gs, hm = f["head"].unitsPerEm, f.getBestCmap(), f.getGlyphSet(), f["hmtx"]
    k = size / upm
    names = [cmap.get(ord(c), cmap[ord("?")]) for c in s]
    adv = [hm[n][0] * k for n in names]
    total = sum(adv) + tracking * size * (len(s) - 1)
    x0 = x - (total if anchor == "end" else total / 2 if anchor == "middle" else 0)
    d = []
    for n, a in zip(names, adv):
        pen = SVGPathPen(gs)
        gs[n].draw(TransformPen(pen, (k, 0, 0, -k, x0, y)))
        d.append(pen.getCommands())
        x0 += a + tracking * size
    return f'<path d="{" ".join(d)}" fill="{fill}"/>'


# ---------------------------------------------------------------- the logo, embeddable
WM = json.loads((LOGO / "wordmark" / "hon-wordmark.json").read_text(encoding="utf-8"))


def logo(ink, x, y, width, mid=None, circle=None):
    """The HON wordmark ("HON" in Bagel Fat One, outlined) at (x, y), `width` wide.
    circle=colour puts a disc behind it (wrappers, avatars). Returns (svg, height)."""
    x0, y0, x1, y1 = WM["bounds"]
    k = width / (x1 - x0)
    h = (y1 - y0) * k
    out = ""
    if circle:
        D = width * 1.45
        out += f'<circle cx="{x + width / 2:.1f}" cy="{y + h / 2:.1f}" r="{D / 2:.1f}" fill="{circle}"/>'
    out += (f'<g transform="translate({x - x0 * k:.1f} {y - y0 * k:.1f}) scale({k:.5f})">'
            f'<path d="{WM["d"]}" fill="{ink}"/></g>')
    return out, h


def veg(x, y, s):
    return (f'<rect x="{x}" y="{y}" width="{s}" height="{s}" rx="{s * 0.08}" fill="#FFFFFF"/>'
            f'<rect x="{x + s * 0.1}" y="{y + s * 0.1}" width="{s * 0.8}" height="{s * 0.8}" fill="none" stroke="{VEG}" stroke-width="{s * 0.07}"/>'
            f'<circle cx="{x + s / 2}" cy="{y + s / 2}" r="{s * 0.22}" fill="{VEG}"/>')


def svg(w, h, body, label):
    return (f'<?xml version="1.0" encoding="UTF-8"?>\n<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" '
            f'role="img" aria-label="{label}"><title>{label}</title>{body}</svg>\n')


# ---------------------------------------------------------------- mockups
def pouch():
    W, H = 900, 1060
    p = [f'<rect width="{W}" height="{H}" fill="{PAPER}"/>',
         f'<path d="M70 40 H830 Q850 40 850 60 V980 Q850 1020 810 1020 H90 Q50 1020 50 980 V60 Q50 40 70 40 Z" fill="{MUSTARD}"/>',
         f'<rect x="50" y="40" width="800" height="42" fill="{MUSTARD_DEEP}" opacity="0.45"/>',
         f'<line x1="60" y1="130" x2="840" y2="130" stroke="{MUSTARD_DEEP}" stroke-width="5" stroke-dasharray="14 8"/>']
    lg, lh = logo(CHOC, 130, 180, 420, "pm-logo")
    p.append(lg)
    p.append(veg(730, 170, 64))
    y = 180 + lh + 100
    p.append(txt("HEALTH SUPPLEMENT  |  ADULT 18+", "archivo-bold", 24, 130, y, CHOC, tracking=0.12))
    p.append(txt("Magnesium", "bagel", 70, 130, y + 84, CHOC))
    p.append(txt("Sleep Gummies", "bagel", 70, 130, y + 162, CHOC))
    cx, cy = 742, y + 95
    p.append(f'<circle cx="{cx}" cy="{cy}" r="90" fill="{CHERRY}"/>')
    p.append(txt("250", "bagel", 72, cx, cy + 14, MUSTARD, "middle"))
    p.append(txt("mg", "bagel", 32, cx, cy + 52, CREAM, "middle"))
    ty = y + 250
    p.append(txt("Elemental magnesium per 2 gummies", "archivo-bold", 27, 130, ty, CHOC))
    p.append(txt("3 bioavailable chelates · Montmorency tart cherry", "archivo", 25, 130, ty + 36, CHOC))
    x, cy2 = 130, ty + 86
    for label, w in (("0g added sugar", 198), ("Melatonin-free", 194), ("Individually wrapped", 262)):
        p.append(f'<rect x="{x}" y="{cy2}" width="{w}" height="54" rx="27" fill="none" stroke="{CHOC}" stroke-width="3.5"/>')
        p.append(txt(label, "archivo-bold", 21, x + w / 2, cy2 + 34, CHOC, "middle"))
        x += w + 12
    p.append(txt("NET QTY 60 N · 360 g · 30 days", "archivo-bold", 24, 130, 975, CHOC, tracking=0.04))
    return svg(W, H, "".join(p), "HON pouch front mockup")


def wrapper():
    W, H = 900, 560
    zig_l = " ".join(f"L{60 + (i % 2) * 22},{80 + i * 20}" for i in range(21))
    zig_r = " ".join(f"L{840 - (i % 2) * 22},{480 - i * 20}" for i in range(21))
    p = [f'<rect width="{W}" height="{H}" fill="{PAPER}"/>',
         f'<path d="M60,80 {zig_l} L840,480 {zig_r} Z" fill="{CHOC}"/>',
         f'<rect x="60" y="80" width="780" height="400" fill="{CHOC}"/>',
         f'<rect x="60" y="80" width="780" height="400" fill="none" stroke="#6B4632" stroke-width="2" stroke-dasharray="3 9"/>']
    lg, lh = logo(CHOC, 360, 245, 180, "wr-logo", circle=MUSTARD)
    p.append(lg)
    p.append(txt("ONE GUMMY · ONE NIGHT", "archivo-bold", 24, 450, 450, CREAM, "middle", tracking=0.16))
    return svg(W, H, "".join(p), "HON individually wrapped gummy")


def box():
    W, H = 1000, 800
    front = "180,300 620,380 620,700 180,620"
    side = "620,380 840,300 840,620 620,700"
    top = "180,300 400,220 840,300 620,380"
    p = [f'<rect width="{W}" height="{H}" fill="{PAPER}"/>',
         f'<polygon points="{front}" fill="{MUSTARD}"/>', f'<polygon points="{side}" fill="{MUSTARD_DEEP}"/>',
         f'<polygon points="{top}" fill="#F7D98A"/>',
         f'<polyline points="290,260 730,340" stroke="{CHOC}" stroke-width="10" fill="none" opacity="0.25"/>']
    lg, _ = logo(CHOC, 0, 0, 200, "bx-logo")
    p.append(f'<g transform="matrix(1 0.18 0 1 300 470)">{lg}</g>')
    p.append(f'<g transform="matrix(1 -0.36 0 1 650 520)">{txt("Open at bedtime.", "bagel", 30, 0, 0, CHOC)}</g>')
    return svg(W, H, "".join(p), "HON shipper box mockup")


def insta():
    W, H = 1080, 1350
    p = [f'<rect width="{W}" height="{H}" fill="{CHOC}"/>']
    lg, lh = logo(CHOC, 360, 330, 360, "ig-logo", circle=MUSTARD)
    p.append(lg)
    p.append(txt("250mg.", "bagel", 150, 540, 960, MUSTARD, "middle"))
    p.append(txt("Every night.", "bagel", 110, 540, 1080, CREAM, "middle"))
    p.append(txt("Magnesium Sleep Gummies · 0g added sugar · Melatonin-free", "archivo-bold", 28, 540, 1210, MUSTARD, "middle"))
    return svg(W, H, "".join(p), "HON Instagram post")


def stamp_card():
    W, H = 860, 540
    p = [f'<rect width="{W}" height="{H}" fill="{PAPER}"/>',
         f'<rect x="40" y="40" width="780" height="460" rx="28" fill="{CREAM}" stroke="{CHOC}" stroke-width="4"/>']
    lg, _ = logo(CHOC, 104, 112, 100, "sc-logo", circle=MUSTARD)
    p.append(lg)
    p.append(txt("30-night card", "bagel", 54, 270, 128, CHOC))
    p.append(txt("Stamp a night. Your refill ships on night 25.", "archivo-bold", 22, 270, 166, CHOC_SOFT))
    for r in range(3):
        for c in range(10):
            n = r * 10 + c
            cx, cy = 112 + c * 70, 262 + r * 72
            filled = n < 11
            p.append(f'<circle cx="{cx}" cy="{cy}" r="26" fill="{MUSTARD if filled else "none"}" stroke="{CHOC}" stroke-width="3"/>')
            p.append(txt(str(n + 1), "archivo-bold", 19, cx, cy + 7, CHOC, "middle"))
    return svg(W, H, "".join(p), "HON 30-night stamp card")


MOCKUPS = {"hon-pouch-front.svg": pouch, "hon-gummy-wrapper.svg": wrapper, "hon-shipper-box.svg": box,
           "hon-instagram-post.svg": insta, "hon-30-night-card.svg": stamp_card}
LOGOS = [f"hon-wordmark-{c['slug']}.svg" for c in WM["colourways"]] + \
    [f"hon-wordmark-letters-{n}.svg" for n in ("chocolate", "white", "black")]

# ---------------------------------------------------------------- tokens
TOKENS = {
    "name": "HON", "version": 1,
    "color": {"themes": [{"id": "light", "name": "Light"}], "tokens": [
        {"name": "mustard", "value": MUSTARD, "usage": "Primary brand colour: pouch flood, marketplace tiles, stamp fills. Carry `chocolate` text on it (7.6:1)."},
        {"name": "mustard-deep", "value": MUSTARD_DEEP, "usage": "Shade of mustard for pouch seals, box sides and pressed states. Decorative only; never a text ground below 24px."},
        {"name": "chocolate", "value": CHOC, "usage": "Brand ink: logo letters, headlines and body copy on `mustard`, `cream` and `paper`."},
        {"name": "chocolate-soft", "value": CHOC_SOFT, "usage": "Secondary text on `cream` and `paper` (captions, helper lines). 6.5:1 on `cream`."},
        {"name": "cream", "value": CREAM, "usage": "Light surface: cards, inserts, the back-panel card. Also text on `chocolate` and `cherry`."},
        {"name": "paper", "value": PAPER, "usage": "Page background for web and decks, one step warmer than `cream`."},
        {"name": "cherry", "value": CHERRY, "usage": "Sleep SKU colour and the dose disc on pack (the tart-cherry gummy). `mustard` or `cream` text on it."},
        {"name": "cherry-bright", "value": CHERRY_BRIGHT, "usage": "Flavour accent in photography and illustration. Not a text colour on `mustard` (low contrast)."},
        {"name": "veg-green", "value": VEG, "usage": "FSSAI vegetarian mark only. Never a brand colour."},
        {"name": "butter", "value": "#FFD447", "usage": "Letters on `cherry` (Sleep colourway)."},
        {"name": "indigo", "value": "#1F2A5C", "usage": "Ground of the Midnight Indigo colourway (premium sleep, gifting); `marigold` letters on it."},
        {"name": "marigold", "value": "#F2B632", "usage": "Letters on `indigo`."},
        {"name": "lilac", "value": "#D9CCF2", "usage": "Ground of the Lilac colourway (Gen-Z, women-first); `plum` letters on it."},
        {"name": "plum", "value": "#3B1F5C", "usage": "Letters on `lilac`."},
        {"name": "black", "value": "#151412", "usage": "Ground of the Black colourway (limited editions, merch); `bone` letters on it."},
        {"name": "bone", "value": "#F4EDE1", "usage": "Letters on `black`."},
        {"name": "haldi", "value": "#E0A21B", "usage": "Curcumin SKU ground; `haldi-ink` letters on it."},
        {"name": "haldi-ink", "value": "#3A2414", "usage": "Letters on `haldi`."},
        {"name": "jeera", "value": "#3E5B2E", "usage": "Gut / jeera SKU ground; `jeera-cream` letters on it."},
        {"name": "jeera-cream", "value": "#F6EEDC", "usage": "Letters on `jeera`."},
        {"name": "tomato", "value": "#E4572E", "usage": "Energy / daytime SKU ground; `cream` letters on it."},
        {"name": "sage", "value": "#DDE6D8", "usage": "Ground of the Sage colourway (calm, ayurvedic-leaning); `forest` letters on it."},
        {"name": "forest", "value": "#274233", "usage": "Letters on `sage`."},
    ]},
    "type": {
        "fonts": [
            {"family": "Bagel Fat One", "file": "fonts/BagelFatOne-Regular.ttf", "weight": "400"},
            {"family": "Archivo", "file": "fonts/Archivo-Variable.ttf", "weight": "100 900"},
        ],
        "families": {"display": "\"Bagel Fat One\", \"Archivo\", system-ui, sans-serif",
                     "sans": "\"Archivo\", system-ui, -apple-system, \"Segoe UI\", sans-serif"},
        "groups": [
            {"name": "Display", "family": "display", "styles": [
                {"name": "display-xl", "fontSize": "88px", "lineHeight": 0.95, "fontWeight": 400, "sample": "250mg. Every night.", "usage": "Ad headlines, pouch product name at print scale."},
                {"name": "display-lg", "fontSize": "56px", "lineHeight": 1, "fontWeight": 400, "sample": "Magnesium Sleep Gummies", "usage": "Section heroes, social posts."},
                {"name": "display-md", "fontSize": "34px", "lineHeight": 1.05, "fontWeight": 400, "sample": "30-night card", "usage": "Card titles, insert headlines."}]},
            {"name": "Text", "family": "sans", "styles": [
                {"name": "headline", "fontSize": "24px", "lineHeight": "30px", "fontWeight": 800, "sample": "Every milligram, printed.", "usage": "Sub-heads under a display line."},
                {"name": "body", "fontSize": "16px", "lineHeight": "24px", "fontWeight": 500, "sample": "Chew 2 gummies a day, 1–2 hours before bed.", "usage": "Body copy, PDP text."},
                {"name": "body-sm", "fontSize": "14px", "lineHeight": "20px", "fontWeight": 500, "sample": "Store below 25°C. Reseal after use.", "usage": "Helper text, captions."},
                {"name": "label", "fontSize": "12px", "lineHeight": "16px", "fontWeight": 800, "letterSpacing": "0.12em", "sample": "HEALTH SUPPLEMENT | ADULT 18+", "usage": "Caps labels, chips, category line."},
                {"name": "data", "fontSize": "15px", "lineHeight": "20px", "fontWeight": 700, "sample": "250 mg · 57% RDA", "usage": "Numbers in tables and callouts; use tabular figures."}]},
        ],
    },
    "spacing": {"tokens": [
        {"name": "space-1", "value": "4px", "usage": "Icon-to-label gaps."},
        {"name": "space-2", "value": "8px", "usage": "Chip padding, tight stacks."},
        {"name": "space-4", "value": "16px", "usage": "Card padding, stack gaps."},
        {"name": "space-8", "value": "32px", "usage": "Section gaps, poster margins."},
        {"name": "space-16", "value": "64px", "usage": "Hero padding."}]},
    "radius": {"tokens": [
        {"name": "radius-sm", "value": "8px", "usage": "Small tiles, inputs."},
        {"name": "radius-lg", "value": "28px", "usage": "Cards and inserts: soft like the letterforms."},
        {"name": "radius-pill", "value": "999px", "usage": "Chips and buttons: every straight edge ends round, like the logo strokes."}]},
}

README = """HON is a magnesium-first gummy brand from India. Its face is one word, "HON", set in fat, friendly Bagel Fat One letters, in twelve approved colourways. Everything rounds off: letters, chips and cards all end in curves. The mood is a 1970s sweet shop that happens to print its lab report.

## Content fundamentals

- Lead with the number. "250mg. Every night." beats any adjective. Every claim on pack or in ads must match the COA.
- Speak like a friend who read the label for you: short, plain, second person ("you"), no exclamation marks, no emoji in brand copy.
- Allowed benefit words: *supports relaxation, restful sleep, muscle recovery*. Never *cure, treat, insomnia*, or anything medical.
- Casing: sentence case for copy; caps only in `label` style (e.g. "HEALTH SUPPLEMENT | ADULT 18+").
- Brand lines in use: "Every milligram, printed." · "One gummy. One night." · "Open at bedtime."

## Visual foundations

**Colour.** Twelve colourways, each a ground plus a letter colour, used as a pair and never mixed:
Paper + Chocolate (`paper` / `chocolate`, the master), Mustard + Chocolate (`mustard` / `chocolate`, pouch flood and marketplace tiles), Chocolate + Mustard (Instagram, wrappers), Night Cherry + Butter (`cherry` / `butter`, Sleep), Midnight Indigo + Marigold (`indigo` / `marigold`, premium sleep), Lilac + Plum (`lilac` / `plum`, Gen-Z), Cream + Cherry (`cream` / `cherry-bright`, pharmacy), Black + Cream (`black` / `bone`, limited editions), Haldi + Chocolate (`haldi` / `haldi-ink`, curcumin SKU), Jeera Green + Cream (`jeera` / `jeera-cream`, gut SKU), Tomato + Cream (`tomato` / `cream`, energy SKU), Sage + Forest (`sage` / `forest`, calm). One colourway per surface. `veg-green` is for the FSSAI mark only.

**Logo.** "HON" in Bagel Fat One, outlined. Always place the supplied files (assets › Logos); never retype it, stretch it, add effects, or recolour it outside the twelve pairs. Minimum width 28px on screen, 12mm in print. Clear space: the height of the O on every side.

**Type.** Display lines in `display-xl`, `display-lg` or `display-md` (Bagel Fat One): short phrases only, never paragraphs. Everything else in the Archivo styles: `headline`, `body`, `body-sm`, `label`, `data`. Numbers in `data` with tabular figures.

**Shape.** Pills (`radius-pill`) for chips and buttons, `radius-lg` for cards; stroke outlines 3–4px in `chocolate`. No sharp corners, no drop shadows, no gradients.

**Imagery.** Backlit macro of the translucent cherry-red gummy, warm window light, mustard or cream surfaces. Real product, real hands, Indian homes at night. Composite the real pack artwork; never let an image model draw the label.

**Packaging.** Pouch 215 × 255 mm with an 80 mm gusset, individually wrapped 6 g gummies, 60 N / 360 g. Front: wordmark, HEALTH SUPPLEMENT by the brand name, product name in display type, the dose in a cherry disc, three claim pills, net quantity. Legal text sizes follow FSSAI Table I (front ≥ 3 mm letters on this panel size).

## Iconography

No icon set yet. Use simple filled circles and pills built from `radius-pill` in `chocolate`. No emoji, no line-icon packs. If an icon is needed, draw it from circles and rounded strokes like the letterforms.
"""

LOGOS_README = """The HON wordmark ("HON" in Bagel Fat One, outlined) in its twelve approved colourways, plus letters-only files. Place them as supplied; never retype or redraw.

- `hon-wordmark-<colourway>.svg`: letters on their ground, one file per approved pair (paper-chocolate is the master).
- `hon-wordmark-letters-chocolate.svg`, `-white.svg`, `-black.svg`: letters only, for placing on photography or an approved ground. Single-ink files: the ink is in the file name.
"""

MOCKUPS_README = """How the system lands on real materials. They're built from the logo files and tokens, with all type outlined.

- `hon-pouch-front.svg`: Mustard + Chocolate pouch front with the wordmark, product name, cherry dose disc and claim pills.
- `hon-gummy-wrapper.svg`: chocolate flow-wrap sachet with the wordmark on a mustard disc.
- `hon-shipper-box.svg`: mustard mailer box.
- `hon-instagram-post.svg`: 4:5 launch post, "250mg. Every night."
- `hon-30-night-card.svg`: insert card for tracking nights; drives the refill on night 25.
"""

CLAIM_README = """# ClaimChip

A pill that states one provable claim, e.g. "0g added sugar" or "Melatonin-free". Provide the text; keep it under 20 characters and make sure the claim is on the COA. Use outlined chips (`chocolate` stroke) on `mustard` or `cream`, and a filled chip (`chocolate` ground, `cream` text) when one claim must lead. Maximum three in a row.
"""

CLAIM_PREVIEW = """<!-- @dsCard group="Packaging" height=120 subtitle="Outlined and filled" -->
<div style="display:flex;gap:12px;flex-wrap:wrap;padding:24px;background:var(--mustard)">
  <span class="label" style="border:3px solid var(--chocolate);color:var(--chocolate);border-radius:var(--radius-pill);padding:10px 18px">0G ADDED SUGAR</span>
  <span class="label" style="border:3px solid var(--chocolate);color:var(--chocolate);border-radius:var(--radius-pill);padding:10px 18px">MELATONIN-FREE</span>
  <span class="label" style="background:var(--chocolate);color:var(--cream);border-radius:var(--radius-pill);padding:13px 21px">INDIVIDUALLY WRAPPED</span>
</div>
<script></script>
"""

DOSE_README = """# DoseDisc

The dose, shown as a solid disc: the number in `display` type in `mustard` on `cherry`, with the unit underneath in `cream`. Provide the number and unit ("250" / "mg"). It's the biggest number on any layout, and the only place `cherry` is used as a fill on pack. Put a `label` line beside it saying what the number is ("Elemental magnesium per 2 gummies").
"""

DOSE_PREVIEW = """<!-- @dsCard group="Packaging" height=200 subtitle="The number is the hero" -->
<div style="display:flex;align-items:center;gap:24px;padding:24px;background:var(--mustard)">
  <div style="width:150px;height:150px;border-radius:50%;background:var(--cherry);display:grid;place-items:center;text-align:center">
    <div><div class="display-lg" style="color:var(--mustard)">250</div><div class="headline" style="color:var(--cream);margin-top:-4px">mg</div></div>
  </div>
  <div><div class="headline" style="color:var(--chocolate)">Elemental magnesium</div><div class="body" style="color:var(--chocolate)">per 2 gummies · 3 chelates</div></div>
</div>
<script></script>
"""

COVER = """<!-- @dsCard height=300 -->
<div style="position:relative;width:960px;height:300px;background:var(--paper);overflow:hidden">
<svg width="960" height="300" viewBox="0 0 960 300" style="position:absolute;inset:0" aria-hidden="true">
<!-- blocks: mustard 300x356 slab + chocolate 160x300 strip + cherry disc r96 + cream pills (tokens: mustard, chocolate, cherry, cream)
     arrangement: one tall mustard slab with a chocolate strip and two satellites, bleeding off top and right
     pattern: discs and pills from radius-pill: the gummy and the round-ended strokes of the logo ("everything rounds off")
     scales: space-4 16px gaps, space-8 32px steps; radius-pill for pills, radius-lg 28px on the slab -->
<style>.m{fill:var(--mustard)}.c{fill:var(--chocolate)}.r{fill:var(--cherry)}.k{fill:var(--cream)}</style>
<rect class="m" x="496" y="-28" width="300" height="356" rx="28"/>
<rect class="c" x="812" y="0" width="160" height="300"/>
<circle class="r" cx="646" cy="150" r="96"/>
<circle class="m" cx="646" cy="150" r="44"/>
<rect class="k" x="836" y="40" width="40" height="132" rx="20"/>
<rect class="k" x="892" y="96" width="40" height="164" rx="20"/>
<rect class="c" x="528" y="258" width="76" height="28" rx="14"/>
<rect class="c" x="620" y="258" width="112" height="28" rx="14"/>
<circle class="c" cx="752" cy="40" r="18"/>
</svg>
<div style="position:absolute;left:40px;bottom:40px;max-width:440px">
  <div class="display-xl" style="color:var(--chocolate);font-size:120px;line-height:0.92">HON</div>
  <div class="body-sm" style="color:var(--chocolate-soft);margin-top:10px">High On Nutrition. Fat letters, warm mustard, every milligram printed.</div>
</div>
</div>
<script></script>
"""


def main():
    if OUT.exists():
        shutil.rmtree(OUT)
    (OUT / "assets" / "Logos").mkdir(parents=True)
    (OUT / "assets" / "Mockups").mkdir(parents=True)
    (OUT / "fonts").mkdir()
    for f in ("BagelFatOne-Regular.ttf", "Archivo-Variable.ttf"):
        shutil.copy(HERE / "fonts" / f, OUT / "fonts" / f)
    for n in LOGOS:
        shutil.copy(LOGO / "wordmark" / n, OUT / "assets" / "Logos" / n)
    for n, fn in MOCKUPS.items():
        (OUT / "assets" / "Mockups" / n).write_text(fn(), encoding="utf-8")
    (OUT / "tokens.json").write_text(json.dumps(TOKENS, indent=2, ensure_ascii=False), encoding="utf-8")
    (OUT / "README.md").write_text(README, encoding="utf-8")
    (OUT / "assets" / "Logos" / "README.md").write_text(LOGOS_README, encoding="utf-8")
    (OUT / "assets" / "Mockups" / "README.md").write_text(MOCKUPS_README, encoding="utf-8")
    for comp, rd, pv in (("ClaimChip", CLAIM_README, CLAIM_PREVIEW), ("DoseDisc", DOSE_README, DOSE_PREVIEW)):
        (OUT / "components" / comp).mkdir(parents=True)
        (OUT / "components" / comp / "README.md").write_text(rd, encoding="utf-8")
        (OUT / "components" / comp / "preview.html").write_text(pv, encoding="utf-8")
    (OUT / "components" / "Cover").mkdir(parents=True)
    (OUT / "components" / "Cover" / "preview.html").write_text(COVER, encoding="utf-8")
    print("built", sum(1 for _ in OUT.rglob("*") if _.is_file()), "files in", OUT)


if __name__ == "__main__":
    main()
