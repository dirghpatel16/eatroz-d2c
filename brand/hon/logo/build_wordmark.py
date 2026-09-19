#!/usr/bin/env python3
"""HON wordmark: "HON" set in Bagel Fat One (OFL), outlined to paths. Founder's pick.
The letterforms are never changed; only colourways vary.

Run:  uv run --with fonttools python3 build_wordmark.py
Writes wordmark/hon-wordmark-<slug>.svg (letters on their ground) and wordmark/sheet.html.
"""
from pathlib import Path

from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont

HERE = Path(__file__).resolve().parent
FONT = HERE.parent / "ds" / "fonts" / "BagelFatOne-Regular.ttf"
OUT = HERE / "wordmark"

# slug, name, ground, letters, best for, founder note
COLOURWAYS = [
    ("paper-chocolate", "Paper + Chocolate", "#FBF3E4", "#513223", "Master logo, website, back panels", "The one you picked: warm, honest, premium-casual."),
    ("mustard-chocolate", "Mustard + Chocolate", "#F3C75A", "#513223", "Pouch flood, Blinkit/Amazon tile", "Loudest on a white marketplace grid; nobody in Indian gummies owns mustard."),
    ("chocolate-mustard", "Chocolate + Mustard", "#513223", "#F3C75A", "Instagram, wrappers, dark ads", "Reads rich and night-time; strong thumb-stop."),
    ("cherry-butter", "Night Cherry + Butter", "#6A0D27", "#FFD447", "Sleep SKU pouch", "Colour of the actual gummy; owns 'tart cherry' at a glance."),
    ("indigo-marigold", "Midnight Indigo + Marigold", "#1F2A5C", "#F2B632", "Premium sleep, gifting", "Instantly says night and moon; most premium read."),
    ("lilac-plum", "Lilac + Plum", "#D9CCF2", "#3B1F5C", "Gen-Z sleep, women-first", "Soft and dreamy; close to crowded sleep-purple, so test it."),
    ("cream-cherry", "Cream + Cherry", "#FFF4E6", "#A8173B", "Clean pharmacy shelf", "Light, clean, trustworthy; the cherry keeps it from looking generic."),
    ("black-cream", "Black + Cream", "#151412", "#F4EDE1", "Luxe limited editions, merch", "Premium and gender-neutral; the weakest shelf standout."),
    ("haldi-chocolate", "Haldi + Chocolate", "#E0A21B", "#3A2414", "Curcumin SKU", "The turmeric product's own colour, same wordmark."),
    ("jeera-cream", "Jeera Green + Cream", "#3E5B2E", "#F6EEDC", "Gut / jeera SKU", "Earthy and calm for digestion; keeps the range consistent."),
    ("tomato-cream", "Tomato + Cream", "#E4572E", "#FFF4E6", "Energy / daytime SKU", "Bright day energy against the night range."),
    ("sage-forest", "Sage + Forest", "#DDE6D8", "#274233", "Calm wellness, ayurvedic-leaning", "Gentle and natural; lowest impact on a busy grid."),
]


def outline(text="HON"):
    f = TTFont(FONT)
    upm, cmap, gs, hm = f["head"].unitsPerEm, f.getBestCmap(), f.getGlyphSet(), f["hmtx"]
    d, x = [], 0
    bp = BoundsPen(gs)
    for ch in text:
        g = cmap[ord(ch)]
        pen = SVGPathPen(gs)
        gs[g].draw(TransformPen(pen, (1, 0, 0, -1, x, 0)))
        gs[g].draw(TransformPen(bp, (1, 0, 0, -1, x, 0)))
        d.append(pen.getCommands())
        x += hm[g][0]
    xmin, ymin, xmax, ymax = bp.bounds
    return " ".join(d), (xmin, ymin, xmax, ymax), upm


def wordmark_svg(ground, ink, label, pad=0.22):
    d, (x0, y0, x1, y1), _ = outline()
    w, h = x1 - x0, y1 - y0
    p = w * pad
    W, H = w + 2 * p, h + 2 * p
    bg = f'<rect x="{x0 - p:.0f}" y="{y0 - p:.0f}" width="{W:.0f}" height="{H:.0f}" fill="{ground}"/>' if ground else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x0 - p:.0f} {y0 - p:.0f} {W:.0f} {H:.0f}" role="img" aria-label="{label}">'
            f'<title>{label}</title>{bg}<path d="{d}" fill="{ink}"/></svg>')


def avatar_svg(ground, ink):
    d, (x0, y0, x1, y1), _ = outline()
    w, h = x1 - x0, y1 - y0
    D = w * 1.45
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{cx - D / 2:.0f} {cy - D / 2:.0f} {D:.0f} {D:.0f}" aria-hidden="true">'
            f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="{D / 2:.0f}" fill="{ground}"/><path d="{d}" fill="{ink}"/></svg>')


def main():
    OUT.mkdir(exist_ok=True)
    import json
    d, bounds, upm = outline()
    (OUT / "hon-wordmark.json").write_text(json.dumps({"d": d, "bounds": bounds, "upm": upm,
        "colourways": [dict(zip(("slug", "name", "ground", "ink", "use", "note"), c)) for c in COLOURWAYS]}), encoding="utf-8")
    tiles = []
    for slug, name, ground, ink, use, note in COLOURWAYS:
        body = wordmark_svg(ground, ink, f"HON logo, {name}")
        (OUT / f"hon-wordmark-{slug}.svg").write_text('<?xml version="1.0" encoding="UTF-8"?>\n' + body + "\n", encoding="utf-8")
        tiles.append(f'''<figure>
  <div class="big">{body}</div>
  <figcaption><div class="row"><b>{name}</b><span class="av">{avatar_svg(ground, ink)}</span></div>
  <code>{ground} · {ink}</code><div class="use">{use}</div><div class="note">{note}</div></figcaption>
</figure>''')
    for slug, ink in (("chocolate", "#513223"), ("white", "#FFFFFF"), ("black", "#000000")):
        (OUT / f"hon-wordmark-letters-{slug}.svg").write_text(
            '<?xml version="1.0" encoding="UTF-8"?>\n' + wordmark_svg(None, ink, f"HON logo, {slug} letters", pad=0.04) + "\n", encoding="utf-8")
    sheet = f'''<!doctype html><html><head><meta charset="utf-8"><title>HON colourways</title>
<style>body{{margin:0;background:#EFE9E1;font-family:-apple-system,system-ui,sans-serif;color:#2a1d16;padding:28px}}
h1{{font-size:22px;margin:0 0 4px}}p{{margin:0 0 18px;color:#6b5a4f}}
.grid{{display:grid;grid-template-columns:repeat(4,1fr);gap:16px}}figure{{margin:0;background:#fff;border-radius:14px;overflow:hidden}}
.big svg{{display:block;width:100%;height:auto}}figcaption{{padding:10px 12px 12px;font-size:12.5px;line-height:1.35}}
.row{{display:flex;justify-content:space-between;align-items:center}}.av svg{{width:34px;height:34px;display:block}}
code{{font-size:11px;color:#8a776b}}.use{{font-weight:600;margin-top:4px}}.note{{color:#6b5a4f}}</style></head>
<body><h1>HON: one wordmark, twelve colourways</h1><p>Lettering unchanged (Bagel Fat One, outlined). The circle beside each name is the Instagram / app-icon size.</p>
<div class="grid">{"".join(tiles)}</div></body></html>'''
    (OUT / "sheet.html").write_text(sheet, encoding="utf-8")
    print("wrote", len(COLOURWAYS), "colourways + 3 letter-only files")


if __name__ == "__main__":
    main()
