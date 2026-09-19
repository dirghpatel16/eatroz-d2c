#!/usr/bin/env python3
"""HON pouch artwork generator.

Edit the DATA block below, run `python3 build_pack.py`, and it rewrites:
  hon-pouch-front.svg, hon-pouch-back.svg  (to-scale flats, 1 SVG unit = 1 mm)
  ../kit/index.html                        (brand kit page, SVGs inlined)

Every number printed on the pack lives in DATA. Nutrition values and
bracketed fields are placeholders until the contract manufacturer's COA arrives.
"""
from pathlib import Path
import html
import random

HERE = Path(__file__).resolve().parent

# ---------------------------------------------------------------- DATA
DATA = {
    # Format matched to the Be Bodywise reference pouch measured in hand:
    # 21.5 cm wide x 25.5 cm tall, 8 cm bottom gusset.
    "pouch_mm": (215, 255),          # front/back panel, width x height
    "gusset_mm": 80,                 # bottom gusset (unfolded depth)
    "brand": "HON",
    "tagline": ("HIGH ON", "NUTRITION"),
    "category": "HEALTH SUPPLEMENT",
    "product": ("Magnesium", "Sleep Gummies"),
    "descriptor": "3 bioavailable magnesium chelates · Montmorency tart cherry",
    "hero_dose": "250",
    "hero_unit": "mg",
    "hero_label": ("ELEMENTAL", "MAGNESIUM", "PER 2 GUMMIES"),
    "benefit": "Supports relaxation & restful sleep",
    "chips": ("0g ADDED SUGAR", "MELATONIN-FREE", "INDIVIDUALLY WRAPPED"),
    "net_qty": "60 N",
    "net_weight": "360 g",
    "net_detail": "60 N × 6 g",
    "front_footer": "30 days · Tart cherry · Adults 18+",
    "serve": "2 gummies (approx. 12 g)",
    "servings": "30",
    # label, per serve, per 100 g, %RDA per serve, indent
    # DRAFT: energy uses FSSAI factors (carbohydrate 4, dietary fibre 2 kcal/g).
    "nutrition": [
        ("Energy (kcal)", "22", "187", "1.1%", 0),
        ("Protein (g)", "0.1", "0.8", "–", 0),
        ("Carbohydrate (g)", "9.6", "80.0", "–", 0),
        ("Total sugars (g)", "0.9", "7.5", "–", 1),
        ("Added sugars (g)", "0", "0", "0%", 1),
        ("Dietary fibre (g)", "8.0", "66.7", "–", 0),
        ("Total fat (g)", "0.1", "0.8", "0.1%", 0),
        ("Saturated fat (g)", "0", "0", "0%", 1),
        ("Trans fat (g)", "0", "0", "0%", 1),
        ("Cholesterol (mg)", "0", "0", "–", 0),
        ("Sodium (mg)", "12", "100", "0.6%", 0),
        ("Magnesium (mg)", "250", "2083", "57%†", 0),
    ],
    # elemental mg per serve, by form (must sum to hero_dose)
    "mg_forms": [
        ("Bisglycinate", 125),
        ("Citrate", 75),
        ("Acetyl taurate", 50),
    ],
    "footnotes": [
        "%RDA for energy, fat, sugar and sodium on a 2,000 kcal diet. † Magnesium vs ICMR-NIN 2020 RDA: men 440 mg (57%), women 370 mg (68%).",
    ],
    "ingredients": (
        "Chicory root inulin (prebiotic fibre), magnesium bisglycinate, "
        "magnesium acetyl taurate, magnesium citrate, gelling agent (pectin, INS 440), "
        "Montmorency tart cherry juice concentrate (2%), acidity regulators (INS 330, INS 331(iii)), "
        "sweeteners (steviol glycosides INS 960, monk fruit extract), "
        "natural colour (INS 163(ii)), glazing agent (INS 903)."
    ),
    "flavour_decl": "CONTAINS ADDED FLAVOUR (NATURAL FLAVOURING SUBSTANCES – CHERRY).",
    "allergen": "Allergen advice: [confirm facility statement with manufacturer].",
    "sweetener_box": ("CONTAINS NON-CALORIC SWEETENER",
                      "This product contains an admixture of steviol glycosides and monk fruit extract."),
    "how_to_use": "Chew 2 gummies a day, after a meal, 1–2 hours before bed. Use daily for at least 30 days. For adults 18+ only.",
    "warnings": [
        "Not to exceed the recommended daily usage.",
        "Not to be used as a substitute for a varied diet.",
        "Store out of reach of children.",
        "Excess magnesium may cause loose stools.",
        "Consult a doctor before use if pregnant, breastfeeding, on medication or with a kidney condition.",
        "This product is not intended to diagnose, treat, cure or prevent any disease.",
    ],
    "storage": "Store below 25°C in a cool, dry place, away from direct sunlight. Reseal the zipper after every use. Best before 12 months from manufacture.",
    "marketed_by": "Marketed by: HON Nutrition Pvt. Ltd., [registered address, city, state, PIN].",
    "mfd_by": "Manufactured by: [contract manufacturer name, address, PIN].",
    "fssai": ("Lic. No. 1XXXXXXXXXXXXX (Mfr.)", "Lic. No. 1XXXXXXXXXXXXX (Mktr.)"),
    "care": "For feedback, queries or complaints, contact the marketer: [care@yourdomain.in] · [+91 XXXXX XXXXX] · [yourdomain.in]",
    "origin": "Made in India.",
    "back_pills": ("Gelatin-free", "No artificial colours", "Resealable zip"),
    "mrp": "₹899.00",
    "usp": "₹14.98/N",
    "back_headline": "Every milligram, printed.",
    "back_sub": "Scan for this batch's lab report (COA).",
}

PAL = {
    "cherry": "#6A0D27",   # Night Cherry, Sleep SKU flood
    "glow": "#A8173B",     # Cherry Glow, secondary block
    "butter": "#FFD447",   # HON Butter, every dose number, every SKU
    "milk": "#FFF4E6",     # Milk, type on flood + back card
    "ink": "#1D0810",      # Ink, back-panel text
    "veg": "#008F3A",      # FSSAI veg mark
    "guide": "#FF00B4",    # dieline layer only
}

FONT_IMPORT = "@import url('https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,100..900&family=DM+Mono:wght@400;500&family=Caveat:wght@700&display=swap');"


# ---------------------------------------------------------------- helpers
def esc(s):
    return html.escape(s, quote=True)


def text(x, y, s, size, cls, fill, anchor="start", weight=None, ls=None, extra=""):
    a = f' text-anchor="{anchor}"' if anchor != "start" else ""
    w = f' font-weight="{weight}"' if weight else ""
    l = f' letter-spacing="{ls}"' if ls else ""
    return (f'<text x="{x:.2f}" y="{y:.2f}" font-size="{size}" class="{cls}" '
            f'fill="{fill}"{a}{w}{l}{extra}>{esc(s)}</text>')


def wrap(s, width, size, k=0.49):
    """Greedy word wrap; k = average glyph width in em (Archivo semi-condensed)."""
    max_chars = max(8, int(width / (size * k)))
    out, line = [], ""
    for word in s.split():
        cand = (line + " " + word).strip()
        if len(cand) <= max_chars:
            line = cand
        else:
            out.append(line)
            line = word
    if line:
        out.append(line)
    return out


import json as _json

_WM = _json.loads((HERE.parent / "logo" / "wordmark" / "hon-wordmark.json").read_text(encoding="utf-8"))


def wordmark(x, y, cap, ink, o_fill=None, prefix="wm", o_style=None):
    """The HON wordmark: "HON" in Bagel Fat One, outlined (logo/build_wordmark.py). Single ink;
    o_fill/o_style are accepted for older callers and ignored: the lettering never changes."""
    x0, y0, x1, y1 = _WM["bounds"]
    k = cap / (y1 - y0)
    svg = (f'<g id="{prefix}-wordmark" transform="translate({x - x0 * k:.2f} {y - y0 * k:.2f}) scale({k:.5f})">'
           f'<path d="{_WM["d"]}" fill="{ink}"/></g>')
    return svg, (x1 - x0) * k


def veg_mark(x, y, size=8.4):
    """FSSAI veg mark: green square outline + filled circle, on a white tile."""
    c = size / 2
    return (f'<g class="veg-mark"><rect x="{x - 1:.2f}" y="{y - 1:.2f}" width="{size + 2:.2f}" height="{size + 2:.2f}" rx="0.8" fill="#FFFFFF"/>'
            f'<rect x="{x + 0.35:.2f}" y="{y + 0.35:.2f}" width="{size - 0.7:.2f}" height="{size - 0.7:.2f}" fill="none" stroke="{PAL["veg"]}" stroke-width="0.7"/>'
            f'<circle cx="{x + c:.2f}" cy="{y + c:.2f}" r="{size * 0.27:.2f}" fill="{PAL["veg"]}"/></g>')


def fake_qr(x, y, size, prefix, seed=7):
    """Placeholder QR: finder patterns + seeded noise. Replace with a real code."""
    n = 25
    m = size / n
    rnd = random.Random(seed)
    cells = [[rnd.random() < 0.46 for _ in range(n)] for _ in range(n)]
    out = [f'<g id="{prefix}-qr"><rect x="{x - 1.2:.2f}" y="{y - 1.2:.2f}" width="{size + 2.4:.2f}" height="{size + 2.4:.2f}" fill="#FFFFFF"/>']

    def finder(cx, cy):
        return (f'<rect x="{x + cx * m:.2f}" y="{y + cy * m:.2f}" width="{7 * m:.2f}" height="{7 * m:.2f}" fill="{PAL["ink"]}"/>'
                f'<rect x="{x + (cx + 1) * m:.2f}" y="{y + (cy + 1) * m:.2f}" width="{5 * m:.2f}" height="{5 * m:.2f}" fill="#FFFFFF"/>'
                f'<rect x="{x + (cx + 2) * m:.2f}" y="{y + (cy + 2) * m:.2f}" width="{3 * m:.2f}" height="{3 * m:.2f}" fill="{PAL["ink"]}"/>')

    for r in range(n):
        for c in range(n):
            in_finder = (r < 8 and c < 8) or (r < 8 and c > n - 9) or (r > n - 9 and c < 8)
            if cells[r][c] and not in_finder:
                out.append(f'<rect x="{x + c * m:.2f}" y="{y + r * m:.2f}" width="{m + 0.02:.2f}" height="{m + 0.02:.2f}" fill="{PAL["ink"]}"/>')
    out += [finder(0, 0), finder(n - 7, 0), finder(0, n - 7), "</g>"]
    return "".join(out)


def fake_barcode(x, y, w, h, seed=3):
    rnd = random.Random(seed)
    out = [f'<g class="ean-placeholder"><rect x="{x:.2f}" y="{y:.2f}" width="{w:.2f}" height="{h:.2f}" fill="#FFFFFF"/>']
    cx = x + 2
    while cx < x + w - 2.5:
        bw = rnd.choice([0.28, 0.28, 0.56, 0.84])
        out.append(f'<rect x="{cx:.2f}" y="{y + 1:.2f}" width="{bw:.2f}" height="{h - 4.2:.2f}" fill="{PAL["ink"]}"/>')
        cx += bw + rnd.choice([0.28, 0.56])
    out.append(text(x + w / 2, y + h - 0.8, "EAN-13 · assign via GS1 India", 2.2, "hp-b", PAL["ink"], "middle"))
    out.append("</g>")
    return "".join(out)


def svg_open(w, h, title, prefix):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" id="{prefix}" viewBox="0 0 {w} {h}" '
            f'width="{w}mm" height="{h}mm" role="img" aria-label="{esc(title)}">\n'
            f'<title>{esc(title)}</title>\n'
            f'<style><![CDATA[{FONT_IMPORT}\n'
            ".hp-d{font-family:'Archivo','Arial Black',sans-serif;font-weight:900;font-stretch:125%}\n"
            ".hp-h{font-family:'Archivo','Arial',sans-serif;font-weight:800;font-stretch:112%}\n"
            ".hp-b{font-family:'Archivo','Arial Narrow','Arial',sans-serif;font-weight:500;font-stretch:87.5%}\n"
            ".hp-bb{font-family:'Archivo','Arial Narrow','Arial',sans-serif;font-weight:800;font-stretch:87.5%}\n"
            ".hp-m{font-family:'DM Mono','Courier New',monospace;font-weight:500}\n"
            ".hp-hand{font-family:'Caveat','Marker Felt',cursive;font-weight:700}\n"
            "]]></style>\n")


BOTTOM_SAFE = 12   # stand-up pouch bottom seal / gusset fold distorts art below this

# Three approved directions share one legal/back structure and one DATA block.
THEMES = {
    "d1": dict(name="Bold Colour-Block", flood="#6A0D27", on="#FFF4E6", accent="#FFD447", o="#FFD447", o_style="ring",
               card="#FFF4E6", card_line=None, ink="#1D0810", head="#6A0D27",
               bars=("#6A0D27", "#A8173B", "#FFD447"), bar_txt=("#FFF4E6", "#FFF4E6", "#1D0810"),
               pill="#6A0D27", pill_txt="#FFF4E6", flag="#FFD447", flag_txt="#1D0810"),
    "d5": dict(name="Honest Type", flood="#F1EEE6", on="#151515", accent="#D6322F", o="#D6322F", o_style="ring",
               card="#FFFFFF", card_line="#151515", ink="#151515", head="#151515",
               bars=("#151515", "#D6322F", "#FFD447"), bar_txt=("#FFFFFF", "#FFFFFF", "#151515"),
               pill="#151515", pill_txt="#FFFFFF", flag="#FFD447", flag_txt="#151515"),
    "d6": dict(name="Indian Night Story", flood="#1F2A5C", on="#F6ECD8", accent="#F2B632", o="#F2B632", o_style="disc",
               card="#F6ECD8", card_line=None, ink="#1A1530", head="#9E1B32",
               bars=("#1F2A5C", "#9E1B32", "#F2B632"), bar_txt=("#F6ECD8", "#F6ECD8", "#1A1530"),
               pill="#1F2A5C", pill_txt="#F6ECD8", flag="#F2B632", flag_txt="#1A1530"),
    "d10": dict(name="Split Band", flood="#6A0D27", on="#FFF4E6", accent="#FFD447", o="#FFD447", o_style="ring",
                card="#FFFFFF", card_line=None, ink="#1D0810", head="#A8173B",
                bars=("#6A0D27", "#A8173B", "#FFD447"), bar_txt=("#FFF4E6", "#FFF4E6", "#1D0810"),
                pill="#A8173B", pill_txt="#FFFFFF", flag="#FFD447", flag_txt="#1D0810"),
}


def _lum(h):
    r, g, b = (int(h[i:i + 2], 16) / 255 for i in (1, 3, 5))
    f = lambda c: c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b)


def _blend(a, b, t):
    ca = [int(a[i:i + 2], 16) for i in (1, 3, 5)]
    cb = [int(b[i:i + 2], 16) for i in (1, 3, 5)]
    return "#" + "".join(f"{round(x + (y - x) * t):02X}" for x, y in zip(ca, cb))


# One pouch per logo colourway (logo/wordmark/hon-wordmark.json): flood = ground, everything else = the letters' ink.
for _cw in _WM["colourways"]:
    g, i = _cw["ground"], _cw["ink"]
    dark = g if _lum(g) < _lum(i) else i
    THEMES["cw-" + _cw["slug"]] = dict(
        name=_cw["name"], flood=g, on=i, accent=i, o=i, o_style="ring", block=i, block_txt=g,
        card="#FFFFFF", card_line=(i if _lum(g) > 0.5 else None), ink=dark, head=dark,
        bars=(dark, _blend(dark, "#FFFFFF", 0.35), _blend(dark, "#FFFFFF", 0.72)),
        bar_txt=("#FFFFFF", "#FFFFFF", dark), pill=dark, pill_txt="#FFFFFF", flag="#FFD447", flag_txt="#1D0810")



def dieline(w, h, prefix):
    g = PAL["guide"]
    t = lambda x, y, s, a="start": text(x, y, s, 2.6, "hp-b", g, a)
    return "\n".join([
        f'<g id="{prefix}-dieline" class="dieline" fill="none" stroke="{g}" stroke-width="0.3">',
        f'<rect x="0.15" y="0.15" width="{w - 0.3}" height="{h - 0.3}"/>',
        f'<rect x="0" y="0" width="{w}" height="10" fill="{g}" fill-opacity="0.12" stroke-dasharray="1 1"/>',
        f'<rect x="0" y="0" width="5" height="{h}" fill="{g}" fill-opacity="0.08" stroke-dasharray="1 1"/>',
        f'<rect x="{w - 5}" y="0" width="5" height="{h}" fill="{g}" fill-opacity="0.08" stroke-dasharray="1 1"/>',
        f'<rect x="0" y="{h - BOTTOM_SAFE}" width="{w}" height="{BOTTOM_SAFE}" fill="{g}" fill-opacity="0.08" stroke-dasharray="1 1"/>',
        f'<path d="M0 16 L3 18 L0 20 Z M{w} 16 L{w - 3} 18 L{w} 20 Z" fill="{g}" stroke="none"/>',
        f'<line x1="0" y1="27" x2="{w}" y2="27" stroke-dasharray="2 1"/><line x1="0" y1="31" x2="{w}" y2="31" stroke-dasharray="2 1"/>',
        f'<rect x="8" y="35" width="{w - 16}" height="{h - 35 - BOTTOM_SAFE}" stroke-dasharray="0.6 0.8"/>',
        t(7, 6.6, "TOP SEAL 10 mm"),
        t(7, 19, "TEAR NOTCH"),
        t(7, 30, "CLICK-ZIPPER · NO CRITICAL ART 26–32 mm"),
        t(9.5, 38.8, "SAFE AREA 8 mm"),
        t(7, h - BOTTOM_SAFE + 4.4, f"BOTTOM SEAL ZONE {BOTTOM_SAFE} mm · keep text out"),
        t(w - 7, h - 2, f"BOTTOM FOLD → {DATA['gusset_mm']} mm GUSSET", "end"),
        "</g>",
    ])


def net_line(y, fill, accent):
    return [text(14, y, "NET QTY", 4.2, "hp-bb", fill, ls="0.3"),
            text(36.5, y + 0.4, DATA["net_qty"], 7.2, "hp-d", accent),
            text(63, y, f"{DATA['net_weight']} ({DATA['net_detail']}) · {DATA['front_footer']}", 4.2, "hp-b", fill)]


# ---------------------------------------------------------------- FRONTS
# FSS (L&D) 2020 Table I, principal display panel 500-2500 cm2: letters >= 3 mm.
# Archivo cap height ~0.72 em, so every mandatory line on a front is set >= 4.2 mm.

def front_d1(t, P):
    W, H = DATA["pouch_mm"]
    o = [f'<rect id="{P}-flood" width="{W}" height="{H}" fill="{t["flood"]}"/>']
    wm, wm_w = wordmark(14, 46, 44, t["on"], t["o"], P)
    o.append(wm)
    tx = 14 + wm_w + 4.5
    o.append(text(tx, 81.5, DATA["tagline"][0], 4.3, "hp-bb", t["on"], ls="0.3"))
    o.append(text(tx, 87.6, DATA["tagline"][1], 4.3, "hp-bb", t["on"], ls="0.3"))
    o.append(veg_mark(W - 8 - 1.2 - 12.6, 37.6, 12.6))
    o.append(text(14, 102, DATA["category"], 5.6, "hp-bb", t["accent"], ls="0.7"))
    o.append(text(14, 120, DATA["product"][0], 15, "hp-h", t["on"]))
    o.append(text(14, 136.5, DATA["product"][1], 15, "hp-h", t["on"]))
    o.append(text(14, 146, DATA["descriptor"], 4.3, "hp-b", t["on"], extra=' fill-opacity="0.88"'))
    by, bh = 152, 58
    o.append(f'<rect id="{P}-dose-block" x="9" y="{by}" width="{W - 18}" height="{bh}" rx="6" fill="#A8173B"/>')
    o.append(f'<text x="17" y="{by + 44.5}" font-size="54" class="hp-d" fill="{t["accent"]}" textLength="124" '
             f'lengthAdjust="spacingAndGlyphs">{esc(DATA["hero_dose"])}</text>')
    o.append(text(149, by + 21, DATA["hero_unit"], 19, "hp-d", t["accent"]))
    for i, line in enumerate(DATA["hero_label"]):
        o.append(text(149.5, by + 30.5 + i * 5.6, line, 4.3, "hp-bb", t["on"], ls="0.25"))
    o.append(text(17, by + bh - 5.5, DATA["benefit"], 5.0, "hp-h", t["on"]))
    cy, ch = 216.5, 11
    widths = [58, 56, 75]
    gap = (W - 18 - sum(widths)) / 2
    x = 9
    for label, cw in zip(DATA["chips"], widths):
        o.append(f'<rect x="{x:.2f}" y="{cy}" width="{cw}" height="{ch}" rx="{ch / 2}" fill="none" stroke="{t["on"]}" stroke-width="0.55"/>')
        o.append(text(x + cw / 2, cy + 7.3, label, 4.2, "hp-bb", t["on"], "middle", ls="0.25"))
        x += cw + gap
    o += net_line(H - BOTTOM_SAFE - 1.2, t["on"], t["accent"])
    return o


def front_d5(t, P):
    """Honest Type: the formula is the design. Every milligram on the front."""
    W, H = DATA["pouch_mm"]
    ink, red = t["on"], t["accent"]
    o = [f'<rect id="{P}-flood" width="{W}" height="{H}" fill="{t["flood"]}"/>']
    wm, wm_w = wordmark(14, 44, 30, ink, t["o"], P)
    o.append(wm)
    o.append(text(14 + wm_w + 5, 64, DATA["tagline"][0], 4.3, "hp-bb", ink, ls="0.3"))
    o.append(text(14 + wm_w + 5, 70.2, DATA["tagline"][1], 4.3, "hp-bb", ink, ls="0.3"))
    o.append(veg_mark(W - 8 - 1.2 - 12.6, 37.6, 12.6))
    # butter tab: the 30-day promise
    o.append(f'<rect x="{W - 44}" y="58" width="{44 - 8}" height="12" fill="{PAL["butter"]}"/>')
    o.append(text(W - 26, 66.3, "30 DAYS", 4.4, "hp-bb", ink, "middle", ls="0.4"))

    rule = lambda y, wgt=0.8: o.append(f'<line x1="14" y1="{y}" x2="{W - 14}" y2="{y}" stroke="{ink}" stroke-width="{wgt}"/>')
    rule(80)
    o.append(text(14, 90.5, DATA["category"], 5.4, "hp-bb", ink, ls="0.7"))
    o.append(text(W - 14, 90.5, "FOR ADULTS 18+", 4.3, "hp-bb", ink, "end", ls="0.4"))
    o.append(text(14, 107, f"{DATA['product'][0]} {DATA['product'][1]}", 12, "hp-h", ink))
    rule(113)
    # hero line
    o.append(f'<text x="14" y="151" font-size="46" class="hp-d" fill="{ink}" textLength="140" '
             f'lengthAdjust="spacingAndGlyphs">{esc(DATA["hero_dose"] + DATA["hero_unit"])}</text>')
    for i, line in enumerate(DATA["hero_label"]):
        o.append(text(162, 128 + i * 6, line, 4.3, "hp-bb", ink, ls="0.25"))
    # marker circle + note (human, imperfect)
    o.append(f'<path d="M 10 132 C 12 112, 70 110, 120 114 C 160 117, 166 134, 158 150 C 150 164, 70 166, 34 161 '
             f'C 8 157, 4 142, 16 128" fill="none" stroke="{red}" stroke-width="1.7" stroke-linecap="round"/>')
    o.append(f'<text x="163" y="159" font-size="9" class="hp-hand" fill="{red}" transform="rotate(-5 163 159)">no secret</text>')
    o.append(f'<text x="166" y="167" font-size="9" class="hp-hand" fill="{red}" transform="rotate(-5 166 167)">blends.</text>')
    rule(170)
    forms = [(f"{mg}mg", f"Magnesium {name.lower()}") for name, mg in DATA["mg_forms"]]
    rows = forms + [("0g", "Added sugar"), ("0mg", "Melatonin"), ("2%", "Montmorency tart cherry juice")]
    y = 170
    for num, label in rows:
        o.append(text(14, y + 7.6, num, 7.0, "hp-d", ink))
        o.append(text(64, y + 7.4, label, 5.2, "hp-b", ink))
        y += 10.3
        rule(y, 0.25)
    o += net_line(H - BOTTOM_SAFE - 1.2, ink, ink)
    return o


def _star(cx, cy, r, fill, op=1.0):
    """8-point block-print star."""
    import math
    pts = []
    for k in range(16):
        rr = r if k % 2 == 0 else r * 0.42
        a = math.pi / 8 * k
        pts.append(f"{cx + rr * math.sin(a):.2f},{cy - rr * math.cos(a):.2f}")
    return f'<polygon points="{" ".join(pts)}" fill="{fill}" fill-opacity="{op}"/>'


def front_d6(t, P):
    """Indian Night Story: the raised O is the moon over city rooftops."""
    W, H = DATA["pouch_mm"]
    chalk, gold, cherry = t["on"], t["accent"], "#9E1B32"
    night = "#141B40"
    o = [f'<rect id="{P}-flood" width="{W}" height="{H}" fill="{t["flood"]}"/>']
    # stars, kept out of text zones
    rnd = random.Random(11)
    keep_out = [(10, 36, 175, 150), (180, 34, 207, 52)]
    placed = 0
    while placed < 22:
        x, y = rnd.uniform(10, 205), rnd.uniform(36, 158)
        if any(a <= x <= c and b <= y <= d for a, b, c, d in keep_out):
            continue
        o.append(_star(x, y, rnd.uniform(1.2, 2.6), gold if rnd.random() < 0.5 else chalk, rnd.uniform(0.45, 0.9)))
        placed += 1
    # moon halo behind the O
    wm, wm_w = wordmark(14, 46, 44, chalk, gold, P, o_style="disc")
    o.append(wm)
    tx = 14 + wm_w + 4.5
    o.append(text(tx, 81.5, DATA["tagline"][0], 4.3, "hp-bb", chalk, ls="0.3"))
    o.append(text(tx, 87.6, DATA["tagline"][1], 4.3, "hp-bb", chalk, ls="0.3"))
    o.append(veg_mark(W - 8 - 1.2 - 12.6, 37.6, 12.6))
    o.append(text(14, 102, DATA["category"], 5.6, "hp-bb", gold, ls="0.7"))
    o.append(text(14, 120, DATA["product"][0], 15, "hp-h", chalk))
    o.append(text(14, 136.5, DATA["product"][1], 15, "hp-h", chalk))
    o.append(text(14, 146, DATA["descriptor"], 4.3, "hp-b", chalk, extra=' fill-opacity="0.9"'))
    o.append(text(14, 154.5, DATA["benefit"], 4.6, "hp-h", gold))
    # rooftops: buildings, water tanks, a neem tree, lit windows
    base = 198
    blds = [(0, 176), (20, 168), (38, 180), (52, 162), (76, 172), (96, 158), (118, 170), (140, 164), (160, 176), (178, 166), (196, 174)]
    for i, (bx, top) in enumerate(blds):
        bw = (blds[i + 1][0] if i + 1 < len(blds) else W) - bx
        o.append(f'<rect x="{bx}" y="{top}" width="{bw + 0.2}" height="{base - top + 1}" fill="{night}"/>')
        if i % 3 == 1:
            o.append(f'<rect x="{bx + bw * 0.3:.2f}" y="{top - 6}" width="{bw * 0.4:.2f}" height="6" rx="1" fill="{night}"/>')
            o.append(f'<rect x="{bx + bw * 0.34:.2f}" y="{top - 8}" width="{bw * 0.32:.2f}" height="2.4" rx="1.2" fill="{night}"/>')
        wrnd = random.Random(i)
        for wy in range(int(top) + 5, base - 4, 7):
            for wx in (bx + 3, bx + bw / 2, bx + bw - 6):
                if wrnd.random() < 0.28:
                    o.append(f'<rect x="{wx:.2f}" y="{wy}" width="2.6" height="3.4" fill="{gold if wrnd.random() < 0.6 else cherry}"/>')
    for cx, cy, r in ((186, 152, 9), (196, 146, 8), (201, 157, 8), (190, 160, 7)):
        o.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{night}"/>')
    o.append(f'<rect x="193" y="160" width="3" height="16" fill="{night}"/>')
    # cherry band with the dose
    o.append(f'<rect id="{P}-band" x="0" y="{base}" width="{W}" height="{H - base}" fill="{cherry}"/>')
    o.append(f'<text x="14" y="{base + 24}" font-size="27" class="hp-d" fill="{gold}" textLength="84" '
             f'lengthAdjust="spacingAndGlyphs">{esc(DATA["hero_dose"] + DATA["hero_unit"])}</text>')
    for i, line in enumerate(DATA["hero_label"]):
        o.append(text(105, base + 9.5 + i * 6, line, 4.3, "hp-bb", chalk, ls="0.25"))
    o.append(text(14, base + 33.5, " · ".join(c.capitalize() if c[0].isalpha() else c for c in DATA["chips"]).replace("ADDED SUGAR", "added sugar"),
                  4.2, "hp-bb", chalk))
    o += net_line(H - BOTTOM_SAFE - 1.2, chalk, gold)
    return o


def front_d10(t, P):
    """Split Band: Be Bodywise-style structure (light brand zone over a colour band), HON's own marks."""
    W, H = DATA["pouch_mm"]
    milk, cherry, glow, butter = "#FFF4E6", "#6A0D27", "#A8173B", "#FFD447"
    tint = "#E9B3C0"
    band = 126
    o = [f'<rect id="{P}-flood" width="{W}" height="{H}" fill="{milk}"/>']
    # big line-art moon rising over a horizon: HON's answer to a large brand illustration
    o.append(f'<circle cx="163" cy="76" r="32" fill="none" stroke="{tint}" stroke-width="2.6"/>')
    o.append(f'<line x1="122" y1="104" x2="{W - 8}" y2="104" stroke="{tint}" stroke-width="2.6" stroke-linecap="round"/>')
    o.append(f'<line x1="140" y1="112" x2="{W - 26}" y2="112" stroke="{tint}" stroke-width="1.6" stroke-linecap="round"/>')
    wm, wm_w = wordmark(16, 50, 30, cherry, glow, P)
    o.append(wm)
    o.append(text(16, 94, "HIGH ON NUTRITION", 4.3, "hp-bb", cherry, ls="0.6"))
    # FSSAI: category in bold caps in immediate proximity of the brand name
    o.append(text(16, 104, DATA["category"] + " | ADULT 18+", 4.6, "hp-bb", glow, ls="0.5"))

    # colour band
    o.append(f'<rect id="{P}-band" x="0" y="{band}" width="{W}" height="{H - band}" fill="{cherry}"/>')
    o.append(veg_mark(W - 8 - 1.2 - 12.6, band + 6, 12.6))
    o.append(text(16, band + 20, DATA["product"][0], 14, "hp-h", milk))
    o.append(text(16, band + 35, DATA["product"][1], 14, "hp-h", milk))
    # no-added-sugar roundel with text on a circle
    cx, cy, r = 181, band + 42, 15
    o.append(f'<circle cx="{cx}" cy="{cy}" r="{r + 5.5}" fill="none" stroke="{milk}" stroke-width="0.6"/>')
    o.append(f'<defs><path id="{P}-roundel" d="M {cx - r} {cy} a {r} {r} 0 1 1 {2 * r} 0 a {r} {r} 0 1 1 {-2 * r} 0"/></defs>')
    circ = 2 * 3.14159 * r
    o.append(f'<text font-size="4.2" class="hp-bb" fill="{milk}"><textPath href="#{P}-roundel" textLength="{circ - 4:.1f}" '
             f'lengthAdjust="spacing">NO ADDED SUGAR · MELATONIN-FREE ·</textPath></text>')
    o.append(text(cx, cy + 3, "0g", 9, "hp-d", butter, "middle"))

    # benefit grid (mono, ruled), claims kept to structure/function wording
    gy = band + 64
    rows = [(("TO", 12), ("Support relaxation", 78), ("Support restful sleep", 0)),
            (("Support muscle recovery", 92), ("2 gummies a day", 0))]
    x0, x1 = 16, W - 16
    o.append(f'<line x1="{x0}" y1="{gy}" x2="{x1}" y2="{gy}" stroke="{milk}" stroke-width="0.5"/>')
    for ri, row in enumerate(rows):
        y = gy + ri * 10
        x = x0
        for ci, (label, w) in enumerate(row):
            o.append(text(x + (0 if ci == 0 else 3), y + 7.0, label, 4.2, "hp-m" if label != "TO" else "hp-bb", milk))
            if w:
                x += w
                o.append(f'<line x1="{x}" y1="{y}" x2="{x}" y2="{y + 10}" stroke="{milk}" stroke-width="0.5"/>')
        o.append(f'<line x1="{x0}" y1="{y + 10}" x2="{x1}" y2="{y + 10}" stroke="{milk}" stroke-width="0.5"/>')
    # the dose: HON puts it on the front (Be Bodywise keeps it on the back)
    dy = gy + 36
    o.append(text(16, dy, DATA["hero_dose"] + DATA["hero_unit"], 11, "hp-d", butter))
    o.append(text(71, dy - 5.2, "ELEMENTAL MAGNESIUM PER SERVE", 4.2, "hp-bb", milk, ls="0.3"))
    o.append(text(71, dy + 0.4, "3 chelates · 0% magnesium oxide", 4.2, "hp-b", milk))
    # bottom row
    ny = H - BOTTOM_SAFE - 1.2
    o.append(text(16, ny, "NET QTY", 4.2, "hp-bb", milk, ls="0.3"))
    o.append(text(38.5, ny + 0.4, DATA["net_qty"], 7.2, "hp-d", butter))
    o.append(text(64, ny, f"{DATA['net_weight']} ({DATA['net_detail']})", 4.2, "hp-b", milk))
    o.append(text(W - 16, ny, "Tart Cherry Flavour", 4.6, "hp-bb", milk, "end"))
    return o


def front_cw(t, P):
    """Colourway pouch: D1's grid, painted in one logo colourway (ground + ink only)."""
    W, H = DATA["pouch_mm"]
    o = [f'<rect id="{P}-flood" width="{W}" height="{H}" fill="{t["flood"]}"/>']
    wm, wm_w = wordmark(14, 44, 40, t["on"], prefix=P)
    o.append(wm)
    tx = 14 + wm_w + 5
    o.append(text(tx, 76.5, DATA["tagline"][0], 4.3, "hp-bb", t["on"], ls="0.3"))
    o.append(text(tx, 82.6, DATA["tagline"][1], 4.3, "hp-bb", t["on"], ls="0.3"))
    o.append(veg_mark(W - 8 - 1.2 - 12.6, 37.6, 12.6))
    o.append(text(14, 102, DATA["category"], 5.6, "hp-bb", t["on"], ls="0.7"))
    o.append(text(14, 120, DATA["product"][0], 15, "hp-h", t["on"]))
    o.append(text(14, 136.5, DATA["product"][1], 15, "hp-h", t["on"]))
    o.append(text(14, 146, DATA["descriptor"], 4.3, "hp-b", t["on"], extra=' fill-opacity="0.9"'))
    by, bh = 152, 58
    o.append(f'<rect id="{P}-dose-block" x="9" y="{by}" width="{W - 18}" height="{bh}" rx="6" fill="{t["block"]}"/>')
    o.append(f'<text x="17" y="{by + 44.5}" font-size="54" class="hp-d" fill="{t["block_txt"]}" textLength="124" '
             f'lengthAdjust="spacingAndGlyphs">{esc(DATA["hero_dose"])}</text>')
    o.append(text(149, by + 21, DATA["hero_unit"], 19, "hp-d", t["block_txt"]))
    for i, line in enumerate(DATA["hero_label"]):
        o.append(text(149.5, by + 30.5 + i * 5.6, line, 4.3, "hp-bb", t["block_txt"], ls="0.25"))
    o.append(text(17, by + bh - 5.5, DATA["benefit"], 5.0, "hp-h", t["block_txt"]))
    cy, ch = 216.5, 11
    widths = [58, 56, 75]
    gap = (W - 18 - sum(widths)) / 2
    x = 9
    for label, cw in zip(DATA["chips"], widths):
        o.append(f'<rect x="{x:.2f}" y="{cy}" width="{cw}" height="{ch}" rx="{ch / 2}" fill="none" stroke="{t["on"]}" stroke-width="0.55"/>')
        o.append(text(x + cw / 2, cy + 7.3, label, 4.2, "hp-bb", t["on"], "middle", ls="0.25"))
        x += cw + gap
    o += net_line(H - BOTTOM_SAFE - 1.2, t["on"], t["on"])
    return o


# ---------------------------------------------------------------- 10 PACKAGING DESIGNS
# Five US-inspired layouts adapted for India, five rooted in Indian graphic culture / D2C.
# Every one uses the HON wordmark unchanged and one approved colourway.
PAL_X = dict(paper="#FBF3E4", choc="#513223", mustard="#F3C75A", cream="#FFF4E6", cherry="#6A0D27",
             cherry_b="#A8173B", butter="#FFD447", indigo="#1F2A5C", marigold="#F2B632", lilac="#D9CCF2",
             plum="#3B1F5C", haldi="#E0A21B", haldi_ink="#3A2414", jeera="#3E5B2E", tomato="#E4572E",
             sage="#DDE6D8", forest="#274233")
X = PAL_X


def _theme(name, ground, ink):
    dark = ground if _lum(ground) < _lum(ink) else ink
    return dict(name=name, flood=ground, on=ink, accent=ink, o=ink, o_style="ring",
                card="#FFFFFF", card_line=(ink if _lum(ground) > 0.5 else None), ink=dark, head=dark,
                bars=(dark, _blend(dark, "#FFFFFF", 0.35), _blend(dark, "#FFFFFF", 0.72)),
                bar_txt=("#FFFFFF", "#FFFFFF", dark), pill=dark, pill_txt="#FFFFFF", flag="#FFD447", flag_txt="#1D0810")


def _wm_center(cap, y, ink, P):
    W = DATA["pouch_mm"][0]
    x0, y0, x1, y1 = _WM["bounds"]
    w = cap / (y1 - y0) * (x1 - x0)
    g, _ = wordmark((W - w) / 2, y, cap, ink, prefix=P)
    return g


def _cherry(cx, cy, r, fill=None):
    fill = fill or X["cherry_b"]
    return (f'<circle cx="{cx:.2f}" cy="{cy:.2f}" r="{r}" fill="{fill}"/>'
            f'<ellipse cx="{cx - r * 0.35:.2f}" cy="{cy - r * 0.38:.2f}" rx="{r * 0.28:.2f}" ry="{r * 0.18:.2f}" fill="#FFFFFF" fill-opacity="0.55"/>')


def _burst(cx, cy, r, n, fill):
    import math
    pts = []
    for k in range(n * 2):
        rr = r if k % 2 == 0 else r * 0.84
        a = math.pi / n * k
        pts.append(f"{cx + rr * math.sin(a):.2f},{cy - rr * math.cos(a):.2f}")
    return f'<polygon points="{" ".join(pts)}" fill="{fill}"/>'


def _chips_row(y, ink, labels=None, widths=(58, 56, 75)):
    W = DATA["pouch_mm"][0]
    labels = labels or DATA["chips"]
    gap = (W - 18 - sum(widths)) / 2
    x, out = 9, []
    for label, cw in zip(labels, widths):
        out.append(f'<rect x="{x:.2f}" y="{y}" width="{cw}" height="11" rx="5.5" fill="none" stroke="{ink}" stroke-width="0.55"/>')
        out.append(text(x + cw / 2, y + 7.3, label, 4.2, "hp-bb", ink, "middle", ls="0.25"))
        x += cw + gap
    return out


def front_p1(t, P):
    """US snack-pop (Grüns / Olipop / Poppi) for the Blinkit grid: giant wordmark, one capsule, gummies."""
    W, H = DATA["pouch_mm"]
    bg, fg = X["tomato"], X["cream"]
    o = [f'<rect width="{W}" height="{H}" fill="{bg}"/>', _wm_center(52, 44, fg, P), veg_mark(W - 8 - 1.2 - 12.6, 37.6, 12.6),
         text(W / 2, 111, DATA["category"] + " · ADULT 18+", 5.2, "hp-bb", fg, "middle", ls="0.6"),
         f'<rect x="14" y="118" width="{W - 28}" height="48" rx="24" fill="{fg}"/>',
         text(W / 2, 139, "Magnesium", 13, "hp-h", bg, "middle"),
         text(W / 2, 156, "Sleep Gummies", 13, "hp-h", bg, "middle")]
    for cx, cy, r in ((150, 196, 13), (172, 186, 10), (188, 204, 12), (165, 214, 9)):
        o.append(_cherry(cx, cy, r, X["cherry"]))
    o += [text(14, 202, "250mg", 20, "hp-d", fg), text(14, 211, "ELEMENTAL MAGNESIUM", 4.3, "hp-bb", fg, ls="0.25"),
          text(14, 217.5, "PER 2 GUMMIES · TART CHERRY", 4.3, "hp-bb", fg, ls="0.25"),
          text(14, 228, "0g added sugar · Melatonin-free", 4.4, "hp-b", fg)]
    o += net_line(H - BOTTOM_SAFE - 1.2, fg, fg)
    return o


def front_p2(t, P):
    """US clinical-minimal (Ritual / Seed / Thorne / AG1): small logo, one enormous thin number, spec grid."""
    W, H = DATA["pouch_mm"]
    bg, fg = X["paper"], X["choc"]
    wm, ww = wordmark(14, 40, 22, fg, prefix=P)
    o = [f'<rect width="{W}" height="{H}" fill="{bg}"/>', wm, veg_mark(W - 8 - 1.2 - 12.6, 37.6, 12.6),
         text(14, 72, DATA["category"] + " | ADULT 18+", 4.6, "hp-bb", fg, ls="0.5")]
    rule = lambda y, w=0.35: o.append(f'<line x1="14" y1="{y}" x2="{W - 14}" y2="{y}" stroke="{fg}" stroke-width="{w}"/>')
    rule(80)
    o.append(text(11, 160, "250", 74, "hp-b", fg, weight="200"))
    o.append(text(142, 160, "mg", 22, "hp-b", fg, weight="300"))
    o.append(text(14, 172, "ELEMENTAL MAGNESIUM · PER 2 GUMMIES · 57% RDA (MEN)", 4.3, "hp-bb", fg, ls="0.2"))
    rule(180)
    o.append(f'<line x1="{W / 2}" y1="180" x2="{W / 2}" y2="232" stroke="{fg}" stroke-width="0.35"/>')
    o += [text(14, 192, "Magnesium", 8.5, "hp-h", fg), text(14, 202, "Sleep Gummies", 8.5, "hp-h", fg),
          text(14, 211, "3 chelates · tart cherry", 4.3, "hp-b", fg), text(14, 218, "0g added sugar", 4.3, "hp-b", fg),
          text(14, 225, "Melatonin-free", 4.3, "hp-b", fg),
          f'<circle cx="{W / 2 + 12}" cy="192" r="5" fill="{X["cherry_b"]}"/>',
          text(W / 2 + 21, 194, "SLEEP", 5, "hp-bb", fg, ls="0.5"),
          text(W / 2 + 6, 207, "60 N · 30 days", 4.6, "hp-b", fg),
          text(W / 2 + 6, 215, "Lab report on every batch", 4.3, "hp-b", fg),
          text(W / 2 + 6, 222, "(scan the QR on the back)", 4.3, "hp-b", fg)]
    rule(232)
    o += net_line(H - BOTTOM_SAFE - 1.2, fg, fg)
    return o


def front_p3(t, P):
    """US night-luxe (Moon Juice / Lemme / Cymbiotika): midnight ground, a marigold moon, centred calm."""
    W, H = DATA["pouch_mm"]
    bg, fg = X["indigo"], X["marigold"]
    o = [f'<rect width="{W}" height="{H}" fill="{bg}"/>',
         f'<circle cx="{W / 2}" cy="98" r="54" fill="none" stroke="{fg}" stroke-width="0.5"/>',
         f'<circle cx="{W / 2}" cy="98" r="44" fill="{fg}"/>',
         f'<circle cx="{W / 2 + 16}" cy="90" r="36" fill="{bg}"/>',
         veg_mark(W - 8 - 1.2 - 12.6, 37.6, 12.6)]
    for x, y in ((38, 60), (52, 118), (170, 132), (186, 70), (30, 150), (160, 52)):
        o.append(f'<circle cx="{x}" cy="{y}" r="0.9" fill="{fg}"/>')
    o += [_wm_center(26, 158, fg, P),
          text(W / 2, 194, DATA["category"] + " · ADULT 18+", 4.6, "hp-bb", fg, "middle", ls="0.8"),
          text(W / 2, 206, "Magnesium Sleep Gummies", 9, "hp-h", fg, "middle"),
          f'<line x1="44" y1="212" x2="{W - 44}" y2="212" stroke="{fg}" stroke-width="0.35"/>',
          text(W / 2, 220.5, "250 mg elemental magnesium per 2 gummies", 4.6, "hp-b", fg, "middle"),
          text(W / 2, 228, "0g added sugar · Melatonin-free · Tart cherry", 4.3, "hp-b", fg, "middle")]
    o += net_line(H - BOTTOM_SAFE - 1.2, fg, fg)
    return o


def front_p4(t, P):
    """US ingredient-first (RXBAR-style honesty) meets India's label readers: the formula IS the front."""
    W, H = DATA["pouch_mm"]
    bg, fg = X["cream"], X["cherry_b"]
    wm, ww = wordmark(14, 40, 30, fg, prefix=P)
    o = [f'<rect width="{W}" height="{H}" fill="{bg}"/>', wm, veg_mark(W - 8 - 1.2 - 12.6, 37.6, 12.6),
         text(14, 82, DATA["category"] + " | ADULT 18+", 5, "hp-bb", fg, ls="0.5")]
    lines = ["250MG MAGNESIUM", "2% TART CHERRY", "PECTIN, NOT GELATIN", "STEVIA + MONK FRUIT", "0G ADDED SUGAR"]
    for i, ln in enumerate(lines):
        o.append(text(14, 106 + i * 16, ln, 13, "hp-h", fg))
    o += [text(14, 190, "NOTHING HIDDEN.", 13, "hp-h", X["choc"]),
          f'<line x1="14" y1="197" x2="{W - 14}" y2="197" stroke="{fg}" stroke-width="0.6"/>',
          text(14, 207, "Magnesium Sleep Gummies · Montmorency tart cherry flavour", 4.4, "hp-bb", fg),
          text(14, 215, "Supports relaxation & restful sleep · 3 chelates", 4.4, "hp-b", fg),
          text(14, 223, "Every number is on the back, and every batch is lab-tested.", 4.4, "hp-b", fg)]
    o += net_line(H - BOTTOM_SAFE - 1.2, fg, fg)
    return o


def front_p5(t, P):
    """US benefit-first (OLLY): the job to be done in a big colour circle, playful gummies."""
    W, H = DATA["pouch_mm"]
    bg, fg = X["lilac"], X["plum"]
    wm, ww = wordmark(14, 40, 22, fg, prefix=P)
    o = [f'<rect width="{W}" height="{H}" fill="{bg}"/>', wm, veg_mark(W - 8 - 1.2 - 12.6, 37.6, 12.6),
         text(14, 71, DATA["category"] + " | ADULT 18+", 4.6, "hp-bb", fg, ls="0.5"),
         f'<circle cx="{W / 2}" cy="140" r="60" fill="{fg}"/>',
         text(W / 2, 140, "SLEEP", 24, "hp-d", bg, "middle"),
         text(W / 2, 151, "magnesium gummies", 5.6, "hp-bb", bg, "middle"),
         text(W / 2, 163, "250mg · 2 gummies", 5, "hp-b", bg, "middle")]
    o += [_cherry(164, 88, 9, X["cherry_b"]), _cherry(177, 100, 7, X["cherry_b"])]
    o += [text(W / 2, 212, "Montmorency tart cherry · 3 chelates", 4.4, "hp-b", fg, "middle")]
    o += _chips_row(218, fg)
    o += net_line(H - BOTTOM_SAFE - 1.2, fg, fg)
    return o


def front_p6(t, P):
    """Indian matchbox-label art: ornamental frame, central emblem, ribbon title."""
    W, H = DATA["pouch_mm"]
    bg, fg = X["cherry"], X["butter"]
    o = [f'<rect width="{W}" height="{H}" fill="{bg}"/>',
         f'<rect x="8" y="36" width="{W - 16}" height="{H - 36 - 8}" rx="3" fill="none" stroke="{fg}" stroke-width="1.4"/>',
         f'<rect x="11" y="39" width="{W - 22}" height="{H - 39 - 11}" rx="2" fill="none" stroke="{fg}" stroke-width="0.4"/>']
    for x, y in ((8, 36), (W - 8, 36), (8, H - 8), (W - 8, H - 8)):
        o.append(f'<circle cx="{x}" cy="{y}" r="3.2" fill="{fg}"/>')
    o += [veg_mark(W - 11 - 2 - 12.6, 42, 12.6),
          text(W / 2, 51, DATA["category"] + " · ADULT 18+", 4.6, "hp-bb", fg, "middle", ls="0.8"),
          _wm_center(28, 57, fg, P),
          f'<circle cx="{W / 2}" cy="131" r="40" fill="none" stroke="{fg}" stroke-width="0.8" stroke-dasharray="1.2 1.4"/>',
          f'<circle cx="{W / 2}" cy="131" r="34" fill="{fg}"/>',
          f'<circle cx="{W / 2 - 4}" cy="131" r="20" fill="{bg}"/>',
          f'<circle cx="{W / 2 + 6}" cy="126" r="17" fill="{fg}"/>']
    for dx, dy in ((-12, -14), (14, 14), (-16, 12)):
        o.append(f'<circle cx="{W / 2 + dx}" cy="{131 + dy}" r="1.2" fill="{bg}"/>')
    rb = f'M22,178 H{W - 22} L{W - 14},186 L{W - 22},194 H22 L14,186 Z'
    o += [f'<path d="{rb}" fill="{fg}"/>',
          text(W / 2, 189.2, "MAGNESIUM SLEEP GUMMIES", 6.2, "hp-bb", bg, "middle", ls="0.4"),
          text(W / 2, 205, "250 mg elemental magnesium per 2 gummies", 4.6, "hp-b", fg, "middle"),
          text(W / 2, 213, "0g added sugar · Melatonin-free · Tart cherry", 4.3, "hp-b", fg, "middle")]
    o += net_line(234, fg, fg)
    return o


def _kolam(x0, y0, x1, y1, ink):
    """Kolam-style band: a dot grid with looped diamonds around each 2x2 cell."""
    s = 9
    out = [f'<clipPath id="kolam-clip"><rect x="{x0}" y="{y0}" width="{x1 - x0}" height="{y1 - y0}"/></clipPath><g clip-path="url(#kolam-clip)">']
    y = y0 + 4
    row = 0
    while y < y1 + s:
        x = x0 + (4 if row % 2 == 0 else 4 + s / 2)
        while x < x1 + s:
            out.append(f'<circle cx="{x:.2f}" cy="{y:.2f}" r="0.8" fill="{ink}"/>')
            if row % 2 == 0:
                out.append(f'<rect x="{x - 3.2:.2f}" y="{y - 3.2:.2f}" width="6.4" height="6.4" rx="2.4" fill="none" stroke="{ink}" '
                           f'stroke-width="0.45" transform="rotate(45 {x:.2f} {y:.2f})"/>')
            x += s
        y += s / 2
        row += 1
    out.append("</g>")
    return "".join(out)


def front_p7(t, P):
    """Indian kolam band over a clean modern label (mustard + chocolate)."""
    W, H = DATA["pouch_mm"]
    bg, fg = X["mustard"], X["choc"]
    wm, ww = wordmark(14, 106, 34, fg, prefix=P)
    o = [f'<rect width="{W}" height="{H}" fill="{bg}"/>', _kolam(0, 34, W, 96, fg),
         f'<line x1="0" y1="96" x2="{W}" y2="96" stroke="{fg}" stroke-width="0.8"/>',
         veg_mark(W - 8 - 1.2 - 12.6, 37.6, 12.6), wm,
         text(14, 150, DATA["category"] + " | ADULT 18+", 4.8, "hp-bb", fg, ls="0.5"),
         text(14, 167, "Magnesium", 12, "hp-h", fg), text(14, 181, "Sleep Gummies", 12, "hp-h", fg),
         f'<circle cx="172" cy="168" r="24" fill="{fg}"/>',
         text(172, 170, "250", 13, "hp-d", bg, "middle"), text(172, 178, "mg", 5, "hp-bb", bg, "middle"),
         text(14, 193, "Montmorency tart cherry · 3 chelates", 4.3, "hp-b", fg)]
    o += _chips_row(204, fg)
    o += net_line(H - BOTTOM_SAFE - 1.2, fg, fg)
    return o


def _flower(cx, cy, r, petal, core):
    out = [f'<circle cx="{cx + dx * r:.2f}" cy="{cy + dy * r:.2f}" r="{r * 0.62:.2f}" fill="{petal}"/>'
           for dx, dy in ((0, -1), (1, 0), (0, 1), (-1, 0))]
    return "".join(out) + f'<circle cx="{cx}" cy="{cy}" r="{r * 0.5:.2f}" fill="{core}"/>'


def front_p8(t, P):
    """Indian truck-art pop: striped scalloped band, framed panel, flowers, and a wink: SLEEP OK PLEASE."""
    W, H = DATA["pouch_mm"]
    bg, fg = X["choc"], X["mustard"]
    cols = (X["tomato"], X["mustard"], X["jeera"], X["indigo"], X["cream"])
    o = [f'<rect width="{W}" height="{H}" fill="{bg}"/>']
    for i, c in enumerate(cols):
        o.append(f'<rect x="0" y="{34 + i * 4}" width="{W}" height="4" fill="{c}"/>')
    for i in range(0, W + 8, 8):
        o.append(f'<circle cx="{i}" cy="54" r="4" fill="{X["cream"]}"/>')
    o += [veg_mark(W - 8 - 1.2 - 12.6, 37.6, 12.6),
          f'<rect x="14" y="64" width="{W - 28}" height="86" rx="8" fill="{fg}"/>',
          _wm_center(34, 72, bg, P),
          text(W / 2, 124, DATA["category"] + " · ADULT 18+", 4.8, "hp-bb", bg, "middle", ls="0.5"),
          text(W / 2, 139, "Magnesium Sleep Gummies", 9, "hp-h", bg, "middle")]
    for cx, cy in ((24, 74), (W - 24, 74), (24, 140), (W - 24, 140)):
        o.append(_flower(cx, cy, 3.4, X["tomato"], X["cream"]))
    o += [text(W / 2, 178, "250mg", 24, "hp-d", fg, "middle"),
          text(W / 2, 187, "ELEMENTAL MAGNESIUM · PER 2 GUMMIES", 4.3, "hp-bb", X["cream"], "middle", ls="0.2")]
    o += _chips_row(195, X["cream"])
    o += [text(W / 2, 222, "SLEEP OK PLEASE", 6.4, "hp-bb", fg, "middle", ls="0.8")]
    o += net_line(H - BOTTOM_SAFE - 1.2, X["cream"], fg)
    return o


def front_p9(t, P):
    """Indian modern-apothecary (premium Ayurveda-style): symmetric, framed, a tart-cherry branch."""
    W, H = DATA["pouch_mm"]
    bg, fg = X["sage"], X["forest"]
    o = [f'<rect width="{W}" height="{H}" fill="{bg}"/>',
         f'<rect x="8" y="36" width="{W - 16}" height="{H - 44}" fill="none" stroke="{fg}" stroke-width="0.6"/>',
         f'<rect x="10.5" y="38.5" width="{W - 21}" height="{H - 49}" fill="none" stroke="{fg}" stroke-width="0.25"/>',
         veg_mark(W - 10.5 - 2 - 12.6, 41, 12.6),
         text(W / 2, 50, DATA["category"] + " · ADULT 18+", 4.6, "hp-bb", fg, "middle", ls="0.8"),
         _wm_center(26, 56, fg, P),
         text(W / 2, 92, "HIGH ON NUTRITION", 4.3, "hp-bb", fg, "middle", ls="1.2"),
         f'<path d="M72,110 C92,104 112,108 134,124 C140,128 146,138 148,150" fill="none" stroke="{fg}" stroke-width="0.9"/>',
         f'<path d="M106,110 C104,120 104,130 108,142" fill="none" stroke="{fg}" stroke-width="0.7"/>',
         f'<path d="M128,120 C124,130 124,140 128,152" fill="none" stroke="{fg}" stroke-width="0.7"/>']
    for cx, cy, rot in ((84, 104, -30), (118, 110, 20), (140, 128, 60)):
        o.append(f'<ellipse cx="{cx}" cy="{cy}" rx="8" ry="3.2" fill="{fg}" transform="rotate({rot} {cx} {cy})"/>')
    o += [_cherry(108, 147, 6), _cherry(128, 157, 6), _cherry(148, 155, 6)]
    o += [text(W / 2, 180, "Magnesium", 12, "hp-h", fg, "middle"), text(W / 2, 194, "Sleep Gummies", 12, "hp-h", fg, "middle"),
          text(W / 2, 205, "250 mg elemental magnesium per 2 gummies", 4.6, "hp-b", fg, "middle"),
          text(W / 2, 213, "Montmorency tart cherry · 0g added sugar · Melatonin-free", 4.3, "hp-b", fg, "middle")]
    o += net_line(234, fg, fg)
    return o


def front_p10(t, P):
    """Indian quick-commerce hero (Blinkit / Zepto thumbnail-first, Plix / Power Gummies energy)."""
    W, H = DATA["pouch_mm"]
    bg, fg, cr = X["haldi"], X["haldi_ink"], X["cream"]
    wm, ww = wordmark(14, 40, 24, fg, prefix=P)
    o = [f'<rect width="{W}" height="{H}" fill="{bg}"/>', wm, veg_mark(W - 8 - 1.2 - 12.6, 37.6, 12.6),
         text(14, 74, DATA["category"] + " | ADULT 18+", 4.6, "hp-bb", fg, ls="0.5"),
         text(14, 90, "MAGNESIUM", 9, "hp-h", fg),
         f'<text x="12" y="124" font-size="40" class="hp-d" fill="{fg}" textLength="120" lengthAdjust="spacingAndGlyphs">SLEEP</text>',
         text(14, 138, "GUMMIES", 12, "hp-d", fg),
         _burst(170, 114, 30, 16, cr),
         text(170, 114, "250mg", 10, "hp-d", fg, "middle"), text(170, 122, "MAGNESIUM", 4.2, "hp-bb", fg, "middle"),
         f'<polygon points="0,150 {W},142 {W},168 0,176" fill="{fg}"/>',
         text(W / 2, 162, "30 NIGHTS · 60 GUMMIES · TART CHERRY", 5.2, "hp-bb", cr, "middle", ls="0.4")]
    icons = [("moon", "Melatonin-free"), ("leaf", "Vegan pectin"), ("zero", "0g added sugar")]
    for i, (kind, label) in enumerate(icons):
        cx = 42 + i * 65
        o.append(f'<circle cx="{cx}" cy="198" r="13" fill="{cr}"/>')
        if kind == "moon":
            o += [f'<circle cx="{cx}" cy="198" r="7" fill="{fg}"/>', f'<circle cx="{cx + 3.5}" cy="196" r="6" fill="{cr}"/>']
        elif kind == "leaf":
            o.append(f'<ellipse cx="{cx}" cy="198" rx="8" ry="4" fill="{fg}" transform="rotate(-35 {cx} 198)"/>')
        else:
            o.append(text(cx, 201.5, "0g", 9, "hp-d", fg, "middle"))
        o.append(text(cx, 222, label, 4.3, "hp-bb", fg, "middle"))
    o += net_line(H - BOTTOM_SAFE - 1.2, fg, fg)
    return o


P_INFO = {
    "p1": ("Snack Pop", "US · Grüns, Olipop, Poppi", "Tomato + Cream", "Loudest thumbnail on Blinkit/Zepto; reads 'treat', which lowers the pill barrier for first-time buyers.", ("tomato", "cream")),
    "p2": ("Clinical Clear", "US · Ritual, Seed, Thorne, AG1", "Paper + Chocolate", "The number is the design; builds trust with label-reading metro buyers. The lab-report line answers India's 'fake supplement' fear.", ("paper", "choc")),
    "p3": ("Night Luxe", "US · Moon Juice, Lemme, Cymbiotika", "Midnight Indigo + Marigold", "Most premium read; owns night-time and makes ₹899 feel easy. Great for gifting and Nykaa-style retail.", ("indigo", "marigold")),
    "p4": ("Nothing Hidden", "US · RXBAR-style ingredient front", "Cream + Cherry", "Formula on the front in huge type: the honesty play that won Indian buyers for The Whole Truth, applied to supplements.", ("cream", "cherry_b")),
    "p5": ("Benefit Circle", "US · OLLY", "Lilac + Plum", "The job ('SLEEP') is the hero; instantly scannable in a mixed-need range. Soft and Gen-Z friendly.", ("lilac", "plum")),
    "p6": ("Matchbox Label", "India · vintage matchbox & label art", "Night Cherry + Butter", "Nostalgic Indian print tradition, ornamental but ordered. Collectible, gift-able, instantly 'desi-premium'.", ("cherry", "butter")),
    "p7": ("Kolam Band", "India · kolam / rangoli geometry", "Mustard + Chocolate", "A pattern every Indian home recognises, kept to one band so the label stays clean and modern.", ("mustard", "choc")),
    "p8": ("Sleep OK Please", "India · truck art & poster pop (Chumbak, Bira 91 energy)", "Chocolate + Mustard", "Pure personality: stripes, flowers and a 'Horn OK Please' wink. Built for Instagram and limited drops.", ("choc", "mustard")),
    "p9": ("Modern Apothecary", "India · premium Ayurveda (Forest Essentials, Kama style)", "Sage + Forest", "Symmetric, framed and botanical: calm, natural and premium for pharmacy and gifting shelves.", ("sage", "forest")),
    "p10": ("Q-comm Hero", "India · Blinkit/Zepto-first D2C (Plix, Power Gummies)", "Haldi + Chocolate", "Engineered for a 3-second thumbnail: SLEEP, 250mg and three icons read at 120 px.", ("haldi", "haldi_ink")),
}
for _k, (_n, _insp, _cw, _why, (_g, _i)) in P_INFO.items():
    THEMES[_k] = _theme(_n, X[_g], X[_i])


# ---------------------------------------------------------------- AG1-STYLE (logo v2)
# Founder's v2 logo (logo/v2/hon-logo-v2.json, traced from their artwork): flared H and N, green O on its base.
_L2 = _json.loads((HERE.parent / "logo" / "v2" / "hon-logo-v2.json").read_text(encoding="utf-8"))


def logo2(x, y, h, ink, accent, prefix="l2"):
    """Logo v2 at (x, y), h tall. Letters in `ink`, the O and its base in `accent`. Returns (svg, width)."""
    bx0, by0, bx1, by1 = _L2["bbox"]
    k = h / (by1 - by0)
    svg = (f'<g id="{prefix}-logo2" transform="translate({x - bx0 * k:.2f} {y - by0 * k:.2f}) scale({k:.5f})">'
           f'<path d="{_L2["letters"]}" fill="{ink}" fill-rule="evenodd"/>'
           f'<path d="{_L2["o"]}" fill="{accent}" fill-rule="evenodd"/></g>')
    return svg, (bx1 - bx0) * k


def _contrast(a, b):
    la, lb = sorted((_lum(a), _lum(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


# AG1-style restraint: one flood, an oversized logo, sparse numbers-led copy. Colours are HON's own.
AG1_INFO = {
    "ag1-original":  ("Original", "#F7F4EF", "#111111", "#7EBC57", "Your logo exactly as drawn. The master: clean, calm, trustworthy."),
    "ag1-forest":    ("Forest", "#1F3A2C", "#F7F4EF", "#7EBC57", "The deep-green premium read of the category; the green O pops on it."),
    "ag1-onyx":      ("Onyx", "#121212", "#F7F4EF", "#7EBC57", "Black and gender-neutral; the most 'premium gym' feel."),
    "ag1-leaf":      ("Leaf", "#7EBC57", "#111111", "#111111", "The logo green as the flood; loud and fresh on a Blinkit grid."),
    "ag1-midnight":  ("Midnight", "#16213E", "#F7F4EF", "#F2C94C", "Navy with a moon-yellow O: says sleep instantly."),
    "ag1-cherry":    ("Night Cherry", "#5E0B24", "#F7F4EF", "#FFD447", "The tart-cherry gummy's colour; warm and indulgent."),
    "ag1-oat":       ("Oat", "#E8DCC8", "#2B1D14", "#4F8A33", "Soft, natural, kitchen-shelf friendly; the calmest option."),
    "ag1-stone":     ("Stone", "#D8D8D2", "#111111", "#3E7327", "Cool grey, pharmacy-clean; lets the green O carry the brand."),
    "ag1-lavender":  ("Lavender", "#CFC6E8", "#2A1745", "#5B3A9E", "Gentle and Gen-Z; a soft sleep cue."),
    "ag1-terracotta": ("Terracotta", "#B4533A", "#F7F4EF", "#FFD447", "Earthy and Indian-warm; strong in lifestyle shots."),
}
for _k, (_n, _g, _i, _a, _why) in AG1_INFO.items():
    _t = _theme(_n, _g, _i)
    _t.update(o=_a, logo="v2")
    THEMES[_k] = _t


def front_ag1(t, P):
    """AG1-style front: flood, oversized logo, one product line, a three-number spec strip."""
    W, H = DATA["pouch_mm"]
    g, i, a = t["flood"], t["on"], t["o"]
    lg, lw = logo2(0, 0, 70, i, a, P)
    o = [f'<rect width="{W}" height="{H}" fill="{g}"/>', veg_mark(W - 8 - 1.2 - 12.6, 37.6, 12.6),
         text(W / 2, 54, "HIGH ON NUTRITION", 4.3, "hp-bb", i, "middle", ls="1.4", extra=' fill-opacity="0.75"'),
         f'<g transform="translate({(W - lw) / 2:.2f} 66)">{lg}</g>',
         text(W / 2, 152, DATA["category"] + " · ADULT 18+", 4.6, "hp-bb", i, "middle", ls="0.8"),
         text(W / 2, 172, "Magnesium Sleep Gummies", 10, "hp-b", i, "middle", weight="650"),
         text(W / 2, 181, "Bioavailable magnesium with Montmorency tart cherry", 4.6, "hp-b", i, "middle"),
         f'<line x1="14" y1="194" x2="{W - 14}" y2="194" stroke="{i}" stroke-width="0.35"/>']
    cols = [("250mg", "MAGNESIUM PER SERVE"), ("0g", "ADDED SUGAR"), ("60", "GUMMIES · 30 NIGHTS")]
    cw = (W - 28) / 3
    for n, (num, lab) in enumerate(cols):
        cx = 14 + cw * n + cw / 2
        o.append(text(cx, 212, num, 13, "hp-b", i, "middle", weight="700"))
        o.append(text(cx, 221, lab, 4.2, "hp-bb", i, "middle", ls="0.3"))
        if n:
            o.append(f'<line x1="{14 + cw * n:.2f}" y1="200" x2="{14 + cw * n:.2f}" y2="226" stroke="{i}" stroke-width="0.35"/>')
    o.append(f'<line x1="14" y1="230" x2="{W - 14}" y2="230" stroke="{i}" stroke-width="0.35"/>')
    o += net_line(H - BOTTOM_SAFE - 1.2, i, i)
    return o


FRONTS = {"d1": front_d1, "d5": front_d5, "d6": front_d6, "d10": front_d10}
FRONTS.update({d: front_cw for d in THEMES if d.startswith("cw-")})
FRONTS.update({k: globals()["front_" + k] for k in P_INFO})
FRONTS.update({k: front_ag1 for k in AG1_INFO})


def build_front(d):
    W, H = DATA["pouch_mm"]
    t = THEMES[d]
    P = f"hon-{d}-front"
    o = [svg_open(W, H, f"HON Magnesium Sleep Gummies ({t['name']}): pouch front, {W} x {H} mm", P)]
    o += FRONTS[d](t, P)
    o.append(dieline(W, H, P))
    o.append("</svg>")
    return "\n".join(o)


# ---------------------------------------------------------------- BACK
class Col:
    """Tiny top-down flow layout for one text column."""

    def __init__(self, x, w, y, t):
        self.x, self.w, self.y, self.out, self.t = x, w, y, [], t

    def heading(self, s, size=3.3):
        self.y += size * 1.05
        self.out.append(text(self.x, self.y, s, size, "hp-bb", self.t["head"], ls="0.4"))
        self.y += 1.8

    def para(self, s, size=2.95, lead=1.27, cls="hp-b", fill=None, bullet=False):
        lines = wrap(s, self.w - (3 if bullet else 0), size, 0.56 if cls == "hp-bb" else 0.49)
        for i, ln in enumerate(lines):
            self.y += size * lead if (i or self.out) else size
            if bullet and i == 0:
                self.out.append(text(self.x, self.y, "–", size, cls, fill or self.t["ink"]))
            self.out.append(text(self.x + (3 if bullet else 0), self.y, ln, size, cls, fill or self.t["ink"]))
        self.y += 1.0

    def space(self, mm):
        self.y += mm


def build_back(d):
    W, H = DATA["pouch_mm"]
    t = THEMES[d]
    P = f"hon-{d}-back"
    ink = t["ink"]
    o = [svg_open(W, H, f"HON Magnesium Sleep Gummies ({t['name']}): pouch back, {W} x {H} mm", P)]
    o.append(f'<rect id="{P}-flood" width="{W}" height="{H}" fill="{t["flood"]}"/>')

    # header: small wordmark, headline, QR to COA
    if d == "d6":
        rnd = random.Random(5)
        for _ in range(9):
            o.append(_star(rnd.uniform(80, 170), rnd.uniform(38, 50), rnd.uniform(1, 2), t["accent"], 0.7))
    if t.get("logo") == "v2":
        wm, _ = logo2(12, 38, 13, t["on"], t["o"], P)
    else:
        wm, _ = wordmark(12, 39, 11, t["on"], t["o"], P, o_style=t["o_style"])
    o.append(wm)
    o.append(text(12, 58.5, DATA["back_headline"], 6.4, "hp-h", t["accent"] if d != "d5" else t["on"]))
    if d == "d5":
        o.append(f'<path d="M12 61 C 50 59.6, 90 62.2, 118 60.4" fill="none" stroke="{t["accent"]}" stroke-width="1.3" stroke-linecap="round"/>')
    o.append(text(12, 65.6, DATA["back_sub"], 3.4, "hp-b", t["on"]))
    o.append(fake_qr(W - 12 - 22, 37.4, 22, P))
    o.append(text(W - 23, 65.2, "QR PLACEHOLDER → COA URL", 2.4, "hp-bb", t["on"], "middle", extra=' fill-opacity="0.8"'))

    card_top = 69
    card_bot = H - BOTTOM_SAFE + 4
    stroke = f' stroke="{t["card_line"]}" stroke-width="0.6"' if t["card_line"] else ""
    o.append(f'<rect id="{P}-card" x="7" y="{card_top}" width="{W - 14}" height="{card_bot - card_top}" rx="4" fill="{t["card"]}"{stroke}/>')

    # ---- column A: nutrition, Mg forms, ingredients
    A = Col(12, 95, card_top + 2, t)
    A.heading("NUTRITION INFORMATION")
    A.para(f"Serving size: {DATA['serve']} · Servings per pack: {DATA['servings']}", size=2.95)
    c1, c2, c3 = A.x + 58, A.x + 76, A.x + A.w
    hy = A.y + 3.3
    for cx, a, b in ((c1, "Amount", "per serve"), (c2, "Amount", "per 100 g"), (c3, "%RDA", "per serve")):
        A.out.append(text(cx, hy, a, 2.8, "hp-bb", ink, "end"))
        A.out.append(text(cx, hy + 3.2, b, 2.8, "hp-bb", ink, "end"))
    A.y = hy + 4.6
    A.out.append(f'<line x1="{A.x}" y1="{A.y:.2f}" x2="{c3}" y2="{A.y:.2f}" stroke="{ink}" stroke-width="0.4"/>')
    for label, v1, v2, v3, ind in DATA["nutrition"]:
        A.y += 3.55
        bold = label.startswith("Magnesium")
        A.out.append(text(A.x + (2.6 if ind else 0), A.y, ("– " if ind else "") + label, 2.95,
                          "hp-bb" if bold else "hp-b", ink))
        for cx, v in ((c1, v1), (c2, v2), (c3, v3)):
            A.out.append(text(cx, A.y, v, 2.95, "hp-m", ink, "end"))
        A.y += 1.0
        A.out.append(f'<line x1="{A.x}" y1="{A.y:.2f}" x2="{c3}" y2="{A.y:.2f}" stroke="{ink}" stroke-width="{0.4 if bold else 0.12}"/>')
    A.space(1.4)
    for fn in DATA["footnotes"]:
        A.para(fn, size=2.8, lead=1.22)

    A.space(1.4)
    A.heading("MAGNESIUM PER SERVE, BY FORM", size=3.0)
    total = sum(v for _, v in DATA["mg_forms"])
    assert str(total) == DATA["hero_dose"], "mg_forms must add up to hero_dose"
    bx, bw = A.x, A.w
    bar_y = A.y + 0.6
    for i, ((name, mg), f, ft) in enumerate(zip(DATA["mg_forms"], t["bars"], t["bar_txt"])):
        seg = bw * mg / total
        last = i == len(DATA["mg_forms"]) - 1
        A.out.append(f'<rect x="{bx:.2f}" y="{bar_y:.2f}" width="{seg - 0.6:.2f}" height="6" fill="{f}"/>')
        A.out.append(text(bx + 1.4, bar_y + 4.4, f"{mg} mg", 3.0, "hp-m", ft))
        A.out.append(text(bx + seg - 0.6 if last else bx + 0.2, bar_y + 10.2, name, 2.9, "hp-b", ink, "end" if last else "start"))
        bx += seg
    A.y = bar_y + 11.8

    A.space(1.6)
    A.heading("INGREDIENTS")
    A.para(DATA["ingredients"], size=2.95, lead=1.24)
    A.para(DATA["flavour_decl"], size=2.95, cls="hp-bb")
    A.para(DATA["allergen"], size=2.95, cls="hp-bb")
    A.para(DATA["origin"], size=2.95, cls="hp-bb")
    A.para(DATA["care"], size=2.95, lead=1.22)
    A.space(1.8)
    px, py = A.x, A.y
    for label in DATA["back_pills"]:
        pw = len(label) * 2.9 * 0.5 + 6
        if px + pw > A.x + A.w:
            px, py = A.x, py + 8
        A.out.append(f'<rect x="{px:.2f}" y="{py:.2f}" width="{pw:.2f}" height="6.4" rx="3.2" fill="{t["pill"]}"/>')
        A.out.append(text(px + pw / 2, py + 4.5, label, 2.9, "hp-bb", t["pill_txt"], "middle"))
        px += pw + 2.2
    A.y = py + 6.4

    # ---- column B: use, mandatory statements, storage, legal
    B = Col(115, W - 12 - 115, card_top + 2, t)
    B.heading("HOW TO USE")
    B.para(DATA["how_to_use"])
    B.space(1.2)
    nf_y = B.y
    B.out.append(f'<rect x="{B.x}" y="{nf_y:.2f}" width="{B.w}" height="8.4" fill="{ink}"/>')
    B.out.append(text(B.x + B.w / 2, nf_y + 6.0, "NOT FOR MEDICINAL USE", 4.4, "hp-bb", t["card"], "middle", ls="0.35"))
    B.y = nf_y + 8.4 + 2.4
    B.heading("READ BEFORE USE")
    for wtxt in DATA["warnings"]:
        B.para(wtxt, bullet=True, lead=1.22)
    # Schedule II declaration: boxed, letters >= 3 mm measured on "l" (Archivo l ~0.74 em)
    B.space(1.4)
    sb_y = B.y
    sb_lines = wrap(DATA["sweetener_box"][1], B.w - 6, 4.2)
    sb_h = 8.4 + len(sb_lines) * 5.4 + 2.4
    B.out.append(f'<rect x="{B.x}" y="{sb_y:.2f}" width="{B.w}" height="{sb_h:.2f}" fill="none" stroke="{ink}" stroke-width="0.5"/>')
    B.out.append(text(B.x + 3, sb_y + 6.6, DATA["sweetener_box"][0], 4.2, "hp-bb", ink))
    for i, ln in enumerate(sb_lines):
        B.out.append(text(B.x + 3, sb_y + 12 + i * 5.4, ln, 4.2, "hp-b", ink))
    B.y = sb_y + sb_h + 1.2
    B.heading("STORAGE")
    B.para(DATA["storage"])
    B.space(1.0)
    ly = B.y + 0.6
    B.out.append(f'<rect x="{B.x}" y="{ly:.2f}" width="17" height="9.4" rx="1" fill="none" stroke="{ink}" stroke-width="0.35" stroke-dasharray="0.8 0.6"/>')
    B.out.append(text(B.x + 8.5, ly + 5.8, "FSSAI LOGO", 2.4, "hp-bb", ink, "middle"))
    B.out.append(text(B.x + 20, ly + 3.8, DATA["fssai"][0], 2.95, "hp-b", ink))
    B.out.append(text(B.x + 20, ly + 8.2, DATA["fssai"][1], 2.95, "hp-b", ink))
    B.y = ly + 10.6
    for s in (DATA["marketed_by"], DATA["mfd_by"]):
        B.para(s, size=2.95, lead=1.22)

    o.extend(A.out)
    o.extend(B.out)
    fy = B.y + 1.6
    o.append(f'<line x1="{B.x}" y1="{fy:.2f}" x2="{B.x + B.w}" y2="{fy:.2f}" stroke="{ink}" stroke-width="0.4"/>')
    o.append(text(B.x, fy + 6.2, f"MRP {DATA['mrp']}", 5.4, "hp-bb", ink))
    o.append(text(B.x, fy + 10.2, "(incl. of all taxes)", 2.95, "hp-b", ink))
    o.append(text(B.x, fy + 14.2, f"Unit sale price {DATA['usp']}", 2.95, "hp-bb", ink))
    ix, iy, iw, ih = B.x, fy + 16.2, 44, 15.4
    o.append(f'<rect id="{P}-inkjet" x="{ix}" y="{iy:.2f}" width="{iw}" height="{ih}" fill="#FFFFFF" stroke="{ink}" stroke-width="0.35" stroke-dasharray="1 0.7"/>')
    for i, lab in enumerate(("BATCH NO.", "MFG. DATE", "BEST BEFORE")):
        o.append(text(ix + 1.8, iy + 4.4 + i * 4.6, lab, 2.95, "hp-bb", ink))
    o.append(fake_barcode(B.x + B.w - 32, fy + 3.4, 32, 24.5))
    bottom = max(iy + ih, fy + 3.4 + 24.5)

    o.append(f'<g id="{P}-draft-flags"><rect x="{W - 62}" y="{card_top - 3.4}" width="55" height="6.8" rx="3.4" fill="{t["flag"]}"/>'
             + text(W - 34.5, card_top + 1.2, "DRAFT VALUES · REPLACE WITH COA", 2.7, "hp-bb", t["flag_txt"], "middle") + "</g>")
    o.append(dieline(W, H, P))
    o.append("</svg>")

    limit = card_bot - 2
    bottom = max(bottom, A.y)
    status = "OK" if bottom <= limit else "OVERFLOW"
    print(f"{d} back: col A ends {A.y:.1f} mm, col B foot ends {bottom:.1f} mm (limit {limit}) -> {status}")
    return "\n".join(o)


# ---------------------------------------------------------------- PRINT FLATS
# One printer-ready flat per pouch: [FRONT | BACK] side by side, each with its half of the bottom gusset
# (gusset_mm / 2 under each panel), 3 mm bleed, crop marks and a flat-level dieline layer.
BLEED, MARGIN = 3, 14


def _nest(svg_text, x, y):
    """Re-seat a panel SVG (1 unit = 1 mm) at (x, y) inside the flat."""
    body = svg_text.split("?>", 1)[-1].strip()
    W, H = DATA["pouch_mm"]
    return body.replace("<svg ", f'<svg x="{x}" y="{y}" ', 1).replace(f'width="{W}mm" height="{H}mm" ', f'width="{W}" height="{H}" ', 1)


def build_flat(d, front, back):
    W, H = DATA["pouch_mm"]
    t = THEMES[d]
    gh = DATA["gusset_mm"] / 2
    FW, FH = 2 * W, H + gh                       # trim size of the flat
    CW, CH = FW + 2 * MARGIN, FH + 2 * MARGIN    # canvas with crop-mark margin
    x0, y0 = MARGIN, MARGIN
    g = PAL["guide"]
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {CW} {CH}" width="{CW}mm" height="{CH}mm" role="img" '
         f'aria-label="HON {esc(t["name"])} pouch print flat">',
         f'<title>HON {esc(t["name"])}: pouch print flat, front + back + {DATA["gusset_mm"]} mm gusset</title>',
         f'<rect width="{CW}" height="{CH}" fill="#FFFFFF"/>',
         # bleed: flood 3 mm past the trim on every side
         f'<rect x="{x0 - BLEED}" y="{y0 - BLEED}" width="{FW + 2 * BLEED}" height="{FH + 2 * BLEED}" fill="{t["flood"]}"/>',
         _nest(front, x0, y0), _nest(back, x0 + W, y0)]
    # gusset halves: flood + small logo + product line, printed upside-down-safe (centred)
    for i, label in enumerate(("FRONT GUSSET", "BACK GUSSET")):
        gx = x0 + i * W
        o.append(f'<rect x="{gx}" y="{y0 + H}" width="{W}" height="{gh}" fill="{t["flood"]}"/>')
        if t.get("logo") == "v2":
            lg, lw = logo2(0, 0, 11, t["on"], t["o"], f"{d}-gus{i}")
        else:
            lg, lw = wordmark(0, 0, 9, t["on"], prefix=f"{d}-gus{i}")
        o.append(f'<g transform="translate({gx + (W - lw) / 2:.2f} {y0 + H + 9})">{lg}</g>')
        o.append(text(gx + W / 2, y0 + H + 29, "Magnesium Sleep Gummies · 60 N · Tart cherry", 4.2, "hp-bb", t["on"], "middle", ls="0.3"))
    # flat-level dieline (hide before print)
    dl = [f'<g id="{d}-flat-dieline" class="dieline" fill="none" stroke="{g}" stroke-width="0.35">',
          f'<rect x="{x0}" y="{y0}" width="{FW}" height="{FH}"/>',
          f'<line x1="{x0 + W}" y1="{y0}" x2="{x0 + W}" y2="{y0 + FH}" stroke-dasharray="3 1.5"/>',
          f'<line x1="{x0}" y1="{y0 + H}" x2="{x0 + FW}" y2="{y0 + H}" stroke-dasharray="1.5 1.5"/>',
          f'<path d="M{x0},{y0 + H - 18} Q{x0},{y0 + H} {x0 + 18},{y0 + H} M{x0 + FW},{y0 + H - 18} Q{x0 + FW},{y0 + H} {x0 + FW - 18},{y0 + H} '
          f'M{x0 + W - 18},{y0 + H} Q{x0 + W},{y0 + H} {x0 + W},{y0 + H - 18} M{x0 + W + 18},{y0 + H} Q{x0 + W},{y0 + H} {x0 + W},{y0 + H - 18}" stroke-dasharray="1 1"/>',
          text(x0 + W / 2, y0 - 5, "FRONT PANEL 215 × 255", 3, "hp-bb", g, "middle"),
          text(x0 + W * 1.5, y0 - 5, "BACK PANEL 215 × 255", 3, "hp-bb", g, "middle"),
          text(x0 + W, y0 + FH + 8, f"BOTTOM GUSSET {DATA['gusset_mm']} mm TOTAL · {gh:.0f} mm EACH SIDE · FOLD AT BOTTOM EDGE · DASHED CURVES = K-SEAL", 2.8, "hp-bb", g, "middle"),
          text(x0 - 5, y0 + H + 2, "FOLD", 2.6, "hp-bb", g, "end"),
          "</g>"]
    o += dl
    # crop marks (outside the bleed)
    cm = []
    for cx in (x0, x0 + FW):
        for cy in (y0, y0 + FH):
            sx = -1 if cx == x0 else 1
            sy = -1 if cy == y0 else 1
            cm.append(f'<line x1="{cx + sx * (BLEED + 2)}" y1="{cy}" x2="{cx + sx * (BLEED + 9)}" y2="{cy}" stroke="#000" stroke-width="0.25"/>')
            cm.append(f'<line x1="{cx}" y1="{cy + sy * (BLEED + 2)}" x2="{cx}" y2="{cy + sy * (BLEED + 9)}" stroke="#000" stroke-width="0.25"/>')
    o.append(f'<g id="{d}-crop-marks">{"".join(cm)}</g>')
    o.append("</svg>")
    return "\n".join(o)


# ---------------------------------------------------------------- write
def main():
    W, H = DATA["pouch_mm"]
    inline = lambda s: s.replace(FONT_IMPORT, "").replace(f'width="{W}mm" height="{H}mm" ', "")
    arts = {}
    for d in THEMES:
        front, back = build_front(d), build_back(d)
        arts[d] = (front, back)
        (HERE / f"hon-{d}-front.svg").write_text('<?xml version="1.0" encoding="UTF-8"?>\n' + front, encoding="utf-8")
        (HERE / f"hon-{d}-back.svg").write_text('<?xml version="1.0" encoding="UTF-8"?>\n' + back, encoding="utf-8")
        if d.startswith("ag1-"):
            (HERE / "flats").mkdir(exist_ok=True)
            (HERE / "flats" / f"hon-{d}-flat.svg").write_text('<?xml version="1.0" encoding="UTF-8"?>\n' + build_flat(d, front, back), encoding="utf-8")

    src = HERE.parent / "kit" / "kit.src.html"
    if src.exists():
        page = src.read_text(encoding="utf-8")
        for d, (front, back) in arts.items():
            page = page.replace(f"<!--@FRONT_{d.upper()}-->", inline(front)).replace(f"<!--@BACK_{d.upper()}-->", inline(back))
        tiles = []
        wmdir = HERE.parent / "logo" / "wordmark"
        for cw in _WM["colourways"]:
            svg = (wmdir / f"hon-wordmark-{cw['slug']}.svg").read_text(encoding="utf-8").split("?>", 1)[1]
            tiles.append(f'<figure class="logo-tile">{svg}<figcaption>{cw["name"]} · {cw["use"]}</figcaption></figure>')
        gallery = []
        for d, (front, _) in arts.items():
            if d.startswith("cw-"):
                gallery.append(f'<figure class="logo-tile">{inline(front)}<figcaption>{THEMES[d]["name"]} · pack/hon-{d}-front.svg</figcaption></figure>')
        page = page.replace("<!--@CW_GALLERY-->", "".join(gallery))
        pg = []
        for k, (n, insp, cw, why, _) in P_INFO.items():
            pg.append(f'<figure class="logo-tile">{inline(arts[k][0])}<figcaption><b>{k.upper()} · {n}</b><br>{insp}<br>{cw}<br>{why}</figcaption></figure>')
        page = page.replace("<!--@P_GALLERY-->", "".join(pg))
        ag = []
        for k, (n, g_, i_, a_, why) in AG1_INFO.items():
            c = _contrast(g_, a_)
            ag.append(f'<figure class="logo-tile">{inline(arts[k][0])}<figcaption><b>{n}</b> · {g_} / {i_} / O {a_}<br>{why}<br>O contrast {c:.1f}:1</figcaption></figure>')
        page = page.replace("<!--@AG1_GALLERY-->", "".join(ag))
        page = page.replace("<!--@LOGOS-->", "".join(tiles))
        hero, _ = wordmark(0, 12, 60, "var(--wm-ink)", "var(--butter)", "hero")
        page = page.replace("<!--@WORDMARK-->", hero)
        (HERE.parent / "kit" / "index.html").write_text(page, encoding="utf-8")
        print("kit: wrote kit/index.html")


if __name__ == "__main__":
    main()
