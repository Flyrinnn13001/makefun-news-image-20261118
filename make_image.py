#!/usr/bin/env python3
"""Draw the entry image for make.fun's news-image-20261118 bounty.

The picture sums up the world news of Wednesday 18 November 2026 in one
1024x1024 editorial poster: a dated header, six story panels drawn as flat
pictograms with short factual labels, and a ticker of four more stories.

Everything is drawn with Pillow (no AI image generation), so every letter is
crisp and no text can come out garbled. Run it to (re)build entry.png:

    python3 make_image.py

The stories, as reported on 18 November 2026:
  * The APEC summit opens in Shenzhen, China. US President Trump flew in
    from Quad talks in Manila; a first US-China-Russia trilateral meeting
    is set for Thursday on the summit's sidelines.
  * Ukraine struck the Crimean (Kerch) Bridge for a second day; Russia
    pounded bridges in Kyiv in reply.
  * Iran-US drone clashes over the Gulf: Iranian drones targeted a US radar
    in Bahrain, Kuwait reported drone interceptions, and US forces struck
    Iran's Qeshm Island.
  * North Korea launched a ballistic missile toward the Sea of Japan,
    South Korea's Joint Chiefs of Staff said.
  * NVIDIA reported a record quarter: revenue of $115.8 billion, about
    double a year earlier; its board ruled out a return for ousted CEO
    Jensen Huang.
  * Cyclone Akvan strengthened over the Bay of Bengal, forecast to make
    landfall on India's Andhra Pradesh coast around 20 November.
  Ticker: MS Dhoni retired from the IPL (staying on as Chennai Super Kings
  mentor); France test-fired its upgraded M51.3 submarine missile; crowds
  in Prague marched for media independence; Gaza's ceasefire was warned to
  be at risk of collapse.
"""

import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
OUT = HERE / "entry.png"

FONT_DIR = Path("/usr/share/fonts/truetype/noto")
BLACK = str(FONT_DIR / "NotoSans-Black.ttf")
BOLD = str(FONT_DIR / "NotoSans-Bold.ttf")
REGULAR = str(FONT_DIR / "NotoSans-Regular.ttf")

W = H = 1024

PAPER = (247, 242, 231)
INK = (24, 32, 48)
GREY = (84, 90, 102)
NAVY = (20, 44, 84)
GOLD = (232, 179, 60)
RED = (192, 57, 43)
WHITE = (255, 255, 255)
CARD_LINE = (203, 196, 178)
CREAM = (247, 242, 231)
PALE_BLUE = (170, 205, 235)


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_width):
    """Split text into lines that fit max_width, word by word."""
    lines, line = [], ""
    for word in text.split():
        trial = word if not line else line + " " + word
        if draw.textlength(trial, font=fnt) <= max_width:
            line = trial
        else:
            lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines


def text_block(draw, xy, text, fnt, fill, max_width, line_gap):
    """Draw wrapped text starting at xy; return the y just past it."""
    x, y = xy
    ascent, descent = fnt.getmetrics()
    step = ascent + descent + line_gap
    for line in wrap(draw, text, fnt, max_width):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += step
    return y


# ---------------------------------------------------------------- pictograms
# Each painter receives the draw object and the panel band box (x0, y0, x1, y1)
# and draws a simple flat motif, centred, in pale colours on the band colour.

def paint_skyline(d, box):
    x0, y0, x1, y1 = box
    cx, base = (x0 + x1) // 2, y1 - 12
    # Sun disc, clear of the towers.
    d.ellipse([cx + 66, y0 + 10, cx + 118, y0 + 62], fill=GOLD)
    towers = [(-118, 52, 30), (-82, 82, 26), (-50, 64, 34), (-8, 98, 30),
              (28, 70, 26), (60, 86, 32), (98, 56, 26)]
    for dx, hgt, wdt in towers:
        d.rectangle([cx + dx, base - hgt, cx + dx + wdt, base], fill=CREAM)
        # A few windows, in the band's red, so the blocks read as buildings.
        for wy in range(base - hgt + 10, base - 12, 16):
            for wx in (cx + dx + 6, cx + dx + wdt - 11):
                d.rectangle([wx, wy, wx + 5, wy + 7], fill=(179, 58, 46))
    # Flag poles rising from three tower tops.
    for dx, hgt, wdt, col in [(-82, 82, 26, GOLD), (-8, 98, 30, WHITE),
                              (60, 86, 32, (140, 190, 235))]:
        px = cx + dx + wdt // 2
        d.line([px, base - hgt - 24, px, base - hgt], fill=CREAM, width=3)
        d.rectangle([px, base - hgt - 24, px + 19, base - hgt - 13], fill=col)
    d.rectangle([x0, base, x1, base + 4], fill=CREAM)


def paint_bridge(d, box):
    x0, y0, x1, y1 = box
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    deck_y = cy + 2
    # Two pylons and the standing deck.
    for px in (cx - 92, cx + 62):
        d.rectangle([px, deck_y - 56, px + 12, deck_y + 32], fill=CREAM)
    d.rectangle([x0 + 18, deck_y, cx - 26, deck_y + 9], fill=CREAM)
    d.rectangle([cx + 30, deck_y, x1 - 18, deck_y + 9], fill=CREAM)
    # Stay cables.
    for px in (cx - 86, cx + 68):
        for tx in (px - 58, px - 28, px + 34, px + 62):
            d.line([px + 6, deck_y - 54, tx, deck_y], fill=CREAM, width=2)
    # The broken middle span, tilted down into the water.
    d.polygon([(cx - 26, deck_y + 2), (cx + 28, deck_y + 28),
               (cx + 24, deck_y + 37), (cx - 28, deck_y + 11)], fill=CREAM)
    # Explosion starburst at the break.
    sx, sy = cx - 2, deck_y - 12
    for ang in range(0, 360, 30):
        r1, r2 = 6, 22 if ang % 60 == 0 else 14
        d.line([sx + r1 * math.cos(math.radians(ang)),
                sy + r1 * math.sin(math.radians(ang)),
                sx + r2 * math.cos(math.radians(ang)),
                sy + r2 * math.sin(math.radians(ang))], fill=GOLD, width=4)
    d.ellipse([sx - 6, sy - 6, sx + 6, sy + 6], fill=(240, 120, 40))
    # Water.
    for i, wy in enumerate((deck_y + 40, deck_y + 51)):
        for wx in range(x0 + 26, x1 - 60, 52):
            d.arc([wx + i * 18, wy, wx + 34 + i * 18, wy + 11], 180, 360,
                  fill=PALE_BLUE, width=3)


def paint_drone(d, box):
    x0, y0, x1, y1 = box
    cx, cy = (x0 + x1) // 2 - 24, (y0 + y1) // 2 - 14
    # Quadcopter: X arms, rotor discs, body.
    for dx, dy in [(-46, -24), (46, -24), (-46, 24), (46, 24)]:
        d.line([cx, cy, cx + dx, cy + dy], fill=CREAM, width=6)
        d.ellipse([cx + dx - 17, cy + dy - 6, cx + dx + 17, cy + dy + 6],
                  outline=CREAM, width=4)
    d.rounded_rectangle([cx - 17, cy - 12, cx + 17, cy + 12], 6, fill=CREAM)
    d.ellipse([cx - 5, cy + 2, cx + 5, cy + 11], fill=RED)
    # Radar dish at lower right, sweeping arcs up toward the drone.
    gx, gy = x1 - 84, y1 - 14
    d.polygon([(gx - 4, gy), (gx + 30, gy), (gx + 13, gy - 15)], fill=GOLD)
    d.pieslice([gx - 12, gy - 46, gx + 38, gy + 4], 180, 360, fill=GOLD)
    d.line([gx + 13, gy - 15, gx + 13, gy - 24], fill=GOLD, width=4)
    for r in (26, 42, 58):
        d.arc([gx + 13 - r, gy - 30 - r, gx + 13 + r, gy - 30 + r],
              195, 285, fill=GOLD, width=4)


def paint_missile(d, box):
    x0, y0, x1, y1 = box
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    # Dashed trajectory arc.
    for t in range(6, 100, 9):
        a0 = math.radians(200 - t * 1.1)
        a1 = math.radians(200 - (t + 4) * 1.1)
        rx, ry = 116, 68
        d.line([cx + rx * math.cos(a0), cy + 22 + ry * math.sin(a0),
                cx + rx * math.cos(a1), cy + 22 + ry * math.sin(a1)],
               fill=PALE_BLUE, width=3)
    # Missile body, angled up to the right; red nose, gold fins.
    ang = math.radians(-38)
    ux, uy = math.cos(ang), math.sin(ang)
    px, py = -uy, ux
    bx, by = cx + 8, cy - 12
    nose = (bx + 54 * ux, by + 54 * uy)
    tail = (bx - 38 * ux, by - 38 * uy)
    wdt = 11
    d.polygon([(tail[0] + wdt * px, tail[1] + wdt * py),
               (bx + 28 * ux + wdt * px, by + 28 * uy + wdt * py),
               nose,
               (bx + 28 * ux - wdt * px, by + 28 * uy - wdt * py),
               (tail[0] - wdt * px, tail[1] - wdt * py)], fill=CREAM)
    tip = (bx + 34 * ux, by + 34 * uy)
    d.polygon([(tip[0] + 8 * px, tip[1] + 8 * py), nose,
               (tip[0] - 8 * px, tip[1] - 8 * py)], fill=RED)
    for sgn in (1, -1):
        fin_base = (tail[0] + 8 * ux, tail[1] + 8 * uy)
        d.polygon([(fin_base[0], fin_base[1]),
                   (tail[0] + sgn * 20 * px, tail[1] + sgn * 20 * py),
                   (tail[0] - 6 * ux + sgn * 4 * px,
                    tail[1] - 6 * uy + sgn * 4 * py)], fill=GOLD)
    # Flame.
    fx, fy = tail[0] - 4 * ux, tail[1] - 4 * uy
    d.polygon([(fx + 8 * px, fy + 8 * py), (fx - 28 * ux, fy - 28 * uy),
               (fx - 8 * px, fy - 8 * py)], fill=(240, 120, 40))
    d.polygon([(fx + 4 * px, fy + 4 * py), (fx - 15 * ux, fy - 15 * uy),
               (fx - 4 * px, fy - 4 * py)], fill=GOLD)
    # Sea waves.
    for wx in range(x0 + 24, x1 - 56, 52):
        d.arc([wx, y1 - 26, wx + 34, y1 - 15], 180, 360,
              fill=PALE_BLUE, width=3)


def paint_chip(d, box):
    x0, y0, x1, y1 = box
    cx, cy = (x0 + x1) // 2 - 34, (y0 + y1) // 2
    s = 42
    # Pins on all four sides.
    for i in range(-2, 3):
        off = i * 17
        d.line([cx + off, cy - s - 11, cx + off, cy - s], fill=CREAM, width=5)
        d.line([cx + off, cy + s, cx + off, cy + s + 11], fill=CREAM, width=5)
        d.line([cx - s - 11, cy + off, cx - s, cy + off], fill=CREAM, width=5)
        d.line([cx + s, cy + off, cx + s + 11, cy + off], fill=CREAM, width=5)
    d.rounded_rectangle([cx - s, cy - s, cx + s, cy + s], 10, outline=CREAM,
                        width=6)
    d.rounded_rectangle([cx - 20, cy - 20, cx + 20, cy + 20], 6,
                        outline=CREAM, width=4)
    # Rising bars to the right of the chip.
    bx = cx + 80
    for i, hgt in enumerate((24, 40, 60)):
        d.rectangle([bx + i * 26, cy + 36 - hgt, bx + i * 26 + 18, cy + 36],
                    fill=GOLD if i == 2 else CREAM)
    d.line([bx - 4, cy - 30, bx + 64, cy - 56], fill=GOLD, width=5)
    d.polygon([(bx + 64, cy - 56), (bx + 50, cy - 54), (bx + 60, cy - 42)],
              fill=GOLD)


def paint_cyclone(d, box):
    x0, y0, x1, y1 = box
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2 - 4
    # Spiral of concentric arc segments.
    for i, r in enumerate((45, 35, 25, 15)):
        start = i * 55
        d.arc([cx - r, cy - r, cx + r, cy + r], start, start + 265,
              fill=CREAM, width=7)
    d.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=GOLD)
    # Rain dashes below.
    for dx in (-40, -14, 12, 38):
        d.line([cx + dx, cy + 48, cx + dx - 7, cy + 60], fill=PALE_BLUE,
               width=4)


# ------------------------------------------------------------------- layout

PANELS = [
    {"band": (179, 58, 46), "paint": paint_skyline,
     "headline": "APEC OPENS IN SHENZHEN",
     "sub": "Trump flies in from Quad talks in Manila; a first US-China-Russia "
            "trilateral is set for Thursday."},
    {"band": (47, 93, 138), "paint": paint_bridge,
     "headline": "UKRAINE HITS CRIMEAN BRIDGE AGAIN",
     "sub": "A second day of strikes on the Kerch Bridge; Russia pounds "
            "bridges in Kyiv in reply."},
    {"band": (23, 126, 108), "paint": paint_drone,
     "headline": "IRAN-US DRONE CLASHES IN THE GULF",
     "sub": "Drones target a US radar in Bahrain; Kuwait intercepts drones; "
            "US hits Qeshm Island."},
    {"band": (46, 58, 103), "paint": paint_missile,
     "headline": "NORTH KOREA FIRES BALLISTIC MISSILE",
     "sub": "A launch toward the Sea of Japan, South Korea's Joint Chiefs "
            "of Staff say."},
    {"band": (99, 153, 15), "paint": paint_chip,
     "headline": "NVIDIA POSTS RECORD $115.8BN QUARTER",
     "sub": "Revenue doubles in a year; no return for ousted CEO "
            "Jensen Huang."},
    {"band": (78, 115, 150), "paint": paint_cyclone,
     "headline": "CYCLONE AKVAN NEARS INDIA",
     "sub": "Strengthening over the Bay of Bengal; landfall on the Andhra "
            "Pradesh coast is due around 20 Nov."},
]

TICKER_LINES = [
    "DHONI RETIRES FROM THE IPL  •  FRANCE TEST-FIRES ITS M51.3 SUBMARINE MISSILE",
    "PRAGUE MARCHES FOR MEDIA FREEDOM  •  GAZA CEASEFIRE AT RISK OF COLLAPSE",
]


def draw_header(d):
    d.rectangle([0, 0, W, 170], fill=NAVY)
    d.rectangle([0, 170, W, 176], fill=RED)
    d.text((40, 22), "WEDNESDAY", font=font(BOLD, 34), fill=GOLD)
    d.text((38, 58), "18 NOVEMBER 2026", font=font(BLACK, 80), fill=WHITE)
    d.text((40, 144), "THE WORLD'S NEWS IN ONE PICTURE", font=font(BOLD, 20),
           fill=(170, 190, 230))
    # Small globe at the right of the band.
    cx, cy, r = 940, 82, 50
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=GOLD, width=4)
    d.ellipse([cx - 19, cy - r, cx + 19, cy + r], outline=GOLD, width=3)
    d.line([cx - r, cy, cx + r, cy], fill=GOLD, width=3)
    d.line([cx - 43, cy - 25, cx + 43, cy - 25], fill=GOLD, width=2)
    d.line([cx - 43, cy + 25, cx + 43, cy + 25], fill=GOLD, width=2)
    d.line([cx, cy - r, cx, cy + r], fill=GOLD, width=2)


def draw_panel(d, x, y, w, h, spec):
    d.rounded_rectangle([x, y, x + w, y + h], 10, fill=WHITE,
                        outline=CARD_LINE, width=2)
    band_h = 130
    d.rounded_rectangle([x, y, x + w, y + band_h], 10, fill=spec["band"])
    d.rectangle([x, y + band_h - 10, x + w, y + band_h], fill=spec["band"])
    spec["paint"](d, (x, y, x + w, y + band_h))
    ty = text_block(d, (x + 18, y + band_h + 10), spec["headline"],
                    font(BOLD, 30), INK, w - 36, 3)
    text_block(d, (x + 18, ty + 3), spec["sub"], font(REGULAR, 19), GREY,
               w - 36, 2)


def draw_ticker(d):
    top = H - 68
    d.rectangle([0, top, W, H], fill=NAVY)
    fnt = font(BOLD, 20)
    for i, line in enumerate(TICKER_LINES):
        tw = d.textlength(line, font=fnt)
        d.text(((W - tw) / 2, top + 7 + i * 29), line, font=fnt, fill=WHITE)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    draw_header(d)
    margin, gap = 22, 14
    pw = (W - 2 * margin - 2 * gap) // 3
    ph = 369
    top = 192
    for i, spec in enumerate(PANELS):
        row, col = divmod(i, 3)
        draw_panel(d, margin + col * (pw + gap), top + row * (ph + gap),
                   pw, ph, spec)
    draw_ticker(d)
    img.save(OUT, optimize=True)
    print(f"wrote {OUT} ({OUT.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
