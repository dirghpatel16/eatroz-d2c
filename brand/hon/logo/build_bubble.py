#!/usr/bin/env python3
"""HON bubble badge, built to the exact construction of the founder's reference (the LEC badge):

- every letter is the same width (360 u), made of pill stems and narrow slots with round ends
- tops are aligned; bottoms bounce: first letter medium, middle letter short, last letter longest
  (reference proportions: 755 / 652 / 820 u tall)
- the letters fill 72.8% of the circle's width, top edge at 25.4% of its height
- colours sampled from the reference: mustard #F3C75A, chocolate #513223

Run:  python3 build_bubble.py   (no dependencies; pure geometry)
"""
from pathlib import Path

HERE = Path(__file__).resolve().parent

LW, S, G, GAP = 360, 146, 82, 30       # letter width, stem, slot, letter gap (heavier than LEC's 130/100: H and N have legs, not bowls)
R = S / 2
HEIGHTS = (755, 652, 820)              # H, O, N: tops aligned, bottoms bounce like the reference


def stroke(d, w=S, col="white"):
    return (f'<path d="{d}" fill="none" stroke="{col}" stroke-width="{w}" '
            f'stroke-linecap="round" stroke-linejoin="round"/>')


def slot(x, y1, y2):
    return stroke(f"M{x:.1f},{y1:.1f} V{y2:.1f}", G, "black")


def letter_h(x, h):
    l, r = x + R, x + LW - R
    mid = h * 0.5
    bodies = [stroke(f"M{l},{R} V{h - R}"), stroke(f"M{r},{R} V{h - R}"),
              f'<rect x="{l}" y="{R}" width="{r - l}" height="{h - 2 * R}" fill="white"/>']
    cx = x + LW / 2
    slots = [slot(cx, -300, mid - R - G / 2), slot(cx, mid + R + G / 2, h + 300)]
    return bodies, slots


def letter_o(x, h):
    body = f'<rect x="{x}" y="0" width="{LW}" height="{h}" rx="{LW / 2}" fill="white"/>'
    cx = x + LW / 2
    c = h * 0.3 / 2   # short counter, like the reference's notches
    return [body], [slot(cx, h / 2 - c, h / 2 + c)]


def letter_n(x, h):
    l, r = x + R, x + LW - R
    return [stroke(f"M{l},{h - R} V{R} L{r},{h - R} V{R}")], []


def wordmark():
    b, s, x = [], [], 0
    for fn, h in zip((letter_h, letter_o, letter_n), HEIGHTS):
        bb, ss = fn(x, h)
        b += bb
        s += ss
        x += LW + GAP
    return b, s, x - GAP, max(HEIGHTS)


def mark_svg(ink, bg_circle, circle=True, label="HON logo", mid="m"):
    b, s, w, h = wordmark()
    mask = (f'<mask id="{mid}" maskUnits="userSpaceOnUse" x="-400" y="-400" width="{w + 800}" height="{h + 800}">'
            f'<rect x="-400" y="-400" width="{w + 800}" height="{h + 800}" fill="black"/>{"".join(b)}{"".join(s)}</mask>')
    letters = f'<rect x="-400" y="-400" width="{w + 800}" height="{h + 800}" fill="{ink}" mask="url(#{mid})"/>'
    if circle:
        D = w / 0.728
        tx, ty = (D - w) / 2, D * 0.254
        return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {D:.0f} {D:.0f}" role="img" aria-label="{label}">'
                f'<title>{label}</title><defs>{mask}</defs><circle cx="{D / 2:.1f}" cy="{D / 2:.1f}" r="{D / 2:.1f}" fill="{bg_circle}"/>'
                f'<g transform="translate({tx:.1f} {ty:.1f})">{letters}</g></svg>')
    pad = 60
    bg = f'<rect x="{-pad}" y="{-pad}" width="{w + 2 * pad}" height="{h + 2 * pad}" fill="{bg_circle}"/>' if bg_circle else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{-pad} {-pad} {w + 2 * pad} {h + 2 * pad}" role="img" aria-label="{label}">'
            f'<title>{label}</title><defs>{mask}</defs>{bg}{letters}</svg>')


VERSIONS = {
    "hon-bubble-badge-mustard.svg": dict(ink="#513223", bg_circle="#F3C75A"),   # exact reference colours
    "hon-bubble-badge-cherry.svg": dict(ink="#FFD447", bg_circle="#6A0D27"),
    "hon-bubble-badge-butter.svg": dict(ink="#6A0D27", bg_circle="#FFD447"),
    "hon-bubble-wordmark-chocolate.svg": dict(ink="#513223", bg_circle=None, circle=False),
    "hon-bubble-wordmark-cherry.svg": dict(ink="#6A0D27", bg_circle=None, circle=False),
    "hon-bubble-wordmark-white.svg": dict(ink="#FFFFFF", bg_circle=None, circle=False),
}

if __name__ == "__main__":
    for name, kw in VERSIONS.items():
        (HERE / name).write_text('<?xml version="1.0" encoding="UTF-8"?>\n' + mark_svg(**kw, mid="m-" + name.removesuffix(".svg")) + "\n", encoding="utf-8")
    print("wrote", ", ".join(VERSIONS))
