#!/usr/bin/env python3
"""news-image-20261119: one image summing up Thursday 19 November 2026.

Draws a 1024x1024 front page with the 15 verified stories of the day:
a masthead naming the date, the lead story in a large slot, and the
remaining 14 stories in a two-column grid. Every story gets its own
programmatically drawn thumbnail picture and its source line directly
beneath it. Deterministic: same bytes on every run. No network.
Writes to $MAKEFUN_OUTPUT_DIR/entry.png, default /output/entry.png.
"""

import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")

FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


NAVY = (15, 42, 74)
GOLD = (242, 193, 78)
WHITE = (255, 255, 255)
INK = (20, 24, 30)
GREY = (90, 96, 104)
LIGHT = (232, 236, 240)
RED = (178, 34, 34)

# (headline, source) — the 15 verified stories, worded as given.
STORIES = [
    ("Trump, Xi and Putin meet in Shenzhen and issue a four-point "
     "peace declaration that does not mention Ukraine or Iran.", "Reuters"),
    ("World court rules Myanmar committed genocide against the Rohingya "
     "in 2017; about 10,000 killed, 700,000 fled.", "Le Monde"),
    ("Ukraine hits the Crimean Bridge a third time in a week; "
     "rail traffic halted.", "Reuters"),
    ("Iran widens Gulf attacks: drones target Kuwait air base, missile "
     "alerts in Bahrain; both intercepted.", "Al Jazeera"),
    ("Tanker attacked in the Strait of Hormuz; one crew member "
     "missing, 11 injured.", "CBS News"),
    ("Israeli tanks push into central Gaza beyond the Yellow Line "
     "near Nuseirat.", "Reuters"),
    ("US Senate rejects Iran war-powers resolution, 51-48.", "AP"),
    ("Anthropic IPO sets a record: $83 a share, about $81.3 billion "
     "raised; shares close up 17%.", "Reuters"),
    ("Grand Theft Auto 6 releases today.", "BBC"),
    ("Nvidia drops 2.89% despite record $115.8 billion revenue.", "Reuters"),
    ("EU proposes a 45 billion euro loan to support Ukraine.", "Reuters"),
    ("Migrant boat sinks off Senegal; dozens missing.", "AP"),
    ("Denmark approves Greenland security deal, 109-0.", "Reuters"),
    ("IAEA: North Korea expanding uranium enrichment at Yongbyon.", "Reuters"),
    ("Bitcoin dips below $63,000, then recovers; ETF outflows "
     "of $157.8 million.", "Reuters"),
]


def wrap(text, fnt, width):
    """Wrap text to fit width in pixels; returns a list of lines."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if fnt.getlength(trial) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def badge(d, x, y, num):
    """Small numbered circle in the top-left corner of a thumbnail."""
    r = 13
    d.ellipse([x + 4, y + 4, x + 4 + 2 * r, y + 4 + 2 * r],
              fill=(0, 0, 0), outline=WHITE, width=2)
    f = font(FONT_BOLD, 15)
    t = str(num)
    tw = f.getlength(t)
    d.text((x + 4 + r - tw / 2, y + 4 + r - 9), t, font=f, fill=WHITE)


def skyline(d, x, y, w, h, colour, base):
    """Simple building silhouettes inside box (x, y, w, h)."""
    import random
    rng = random.Random(7)
    bx = x
    while bx < x + w - 8:
        bw = rng.randint(14, 30)
        bh = rng.randint(int(h * 0.35), int(h * 0.8))
        d.rectangle([bx, base - bh, min(bx + bw, x + w), base], fill=colour)
        bx += bw + 3


def draw_thumb(d, idx, x, y, w, h):
    """Draw one distinct story-matching illustration in box (x, y, w, h)."""
    sea = (28, 110, 160)
    sky = (135, 190, 230)
    if idx == 0:
        # Shenzhen summit: skyline at dusk, three flags, handshake sun.
        d.rectangle([x, y, x + w, y + h], fill=(38, 64, 110))
        d.ellipse([x + w - 52, y + 8, x + w - 12, y + 48], fill=GOLD)
        skyline(d, x + 4, y + 30, w - 8, h - 40, (18, 32, 58),
                y + h - 8)
        for i, c in enumerate([(178, 34, 34), (255, 255, 255),
                               (200, 40, 40)]):
            fx = x + 18 + i * 34
            d.line([fx, y + h - 58, fx, y + h - 18], fill=WHITE, width=3)
            d.polygon([(fx, y + h - 58), (fx + 26, y + h - 52),
                       (fx, y + h - 46)], fill=c)
        d.rectangle([x, y + h - 8, x + w, y + h], fill=(90, 60, 30))
    elif idx == 1:
        # World court: courthouse columns and scales of justice.
        d.rectangle([x, y, x + w, y + h], fill=(226, 222, 210))
        d.polygon([(x + 6, y + 26), (x + w / 2, y + 6),
                   (x + w - 6, y + 26)], fill=(120, 90, 60))
        for i in range(4):
            cx = x + 16 + i * (w - 32) / 3
            d.rectangle([cx - 5, y + 28, cx + 5, y + h - 16], fill=WHITE)
        d.rectangle([x + 8, y + h - 16, x + w - 8, y + h - 8],
                    fill=(120, 90, 60))
        mx = x + w / 2
        d.line([mx, y + 34, mx, y + 52], fill=(60, 50, 40), width=3)
        d.line([mx - 26, y + 38, mx + 26, y + 38], fill=(60, 50, 40),
               width=3)
        d.polygon([(mx - 34, y + 44), (mx - 18, y + 44),
                   (mx - 26, y + 56)], fill=GOLD)
        d.polygon([(mx + 18, y + 44), (mx + 34, y + 44),
                   (mx + 26, y + 56)], fill=GOLD)
    elif idx == 2:
        # Crimean Bridge: bridge over water with a broken gap.
        d.rectangle([x, y, x + w, y + h], fill=sky)
        d.rectangle([x, y + h - 26, x + w, y + h], fill=sea)
        mid = x + w / 2
        d.rectangle([x + 4, y + 34, mid - 12, y + 44], fill=(70, 70, 80))
        d.rectangle([mid + 12, y + 34, x + w - 4, y + 44],
                    fill=(70, 70, 80))
        d.line([x + 10, y + 34, x + 10, y + h - 26], fill=(70, 70, 80),
               width=4)
        d.line([x + w - 10, y + 34, x + w - 10, y + h - 26],
               fill=(70, 70, 80), width=4)
        d.line([mid - 12, y + 44, mid, y + 62], fill=(200, 60, 40), width=4)
        d.line([mid + 12, y + 44, mid, y + 62], fill=(200, 60, 40), width=4)
        d.ellipse([mid - 8, y + 52, mid + 8, y + 68], fill=(200, 60, 40))
        d.rectangle([x + 8, y + 22, x + 46, y + 33], fill=(178, 34, 34))
    elif idx == 3:
        # Gulf attacks: desert sky, drone, intercept burst.
        d.rectangle([x, y, x + w, y + h], fill=(240, 200, 120))
        d.rectangle([x, y + h - 22, x + w, y + h], fill=(190, 140, 70))
        d.ellipse([x + w - 44, y + 8, x + w - 12, y + 40], fill=(255, 240, 180))
        d.rectangle([x + 18, y + 30, x + 52, y + 40], fill=(60, 60, 70))
        d.line([x + 10, y + 26, x + 60, y + 26], fill=(60, 60, 70), width=2)
        d.line([x + 10, y + 44, x + 60, y + 44], fill=(60, 60, 70), width=2)
        cx, cy = x + w - 34, y + h - 38
        for ang in range(0, 360, 45):
            import math
            ex = cx + 16 * math.cos(math.radians(ang))
            ey = cy + 16 * math.sin(math.radians(ang))
            d.line([cx, cy, ex, ey], fill=(178, 34, 34), width=3)
        d.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=(178, 34, 34))
        d.rectangle([x + 14, y + h - 30, x + 40, y + h - 22],
                    fill=(90, 90, 100))
    elif idx == 4:
        # Hormuz tanker: oil tanker on the sea, smoke plume.
        d.rectangle([x, y, x + w, y + h], fill=sky)
        d.rectangle([x, y + h - 30, x + w, y + h], fill=sea)
        d.rectangle([x + 10, y + h - 52, x + w - 10, y + h - 30],
                    fill=(40, 40, 48))
        d.rectangle([x + w - 44, y + h - 72, x + w - 16, y + h - 52],
                    fill=(200, 200, 205))
        d.ellipse([x + 22, y + 10, x + 46, y + 34], fill=(90, 90, 95))
        d.ellipse([x + 34, y + 4, x + 58, y + 28], fill=(110, 110, 115))
        d.ellipse([x + 46, y + 12, x + 66, y + 32], fill=(90, 90, 95))
        for i in range(3):
            wx = x + 16 + i * 34
            d.arc([wx, y + h - 26, wx + 26, y + h - 10], 0, 180,
                  fill=WHITE, width=2)
    elif idx == 5:
        # Gaza tanks: tank silhouette on sand, yellow line.
        d.rectangle([x, y, x + w, y + h], fill=(238, 214, 160))
        d.line([x, y + h - 34, x + w, y + h - 34], fill=(220, 180, 40),
               width=4)
        d.rectangle([x + 18, y + h - 56, x + 78, y + h - 38],
                    fill=(74, 88, 60))
        d.rectangle([x + 34, y + h - 68, x + 58, y + h - 56],
                    fill=(74, 88, 60))
        d.line([x + 58, y + h - 62, x + 92, y + h - 66],
               fill=(74, 88, 60), width=5)
        for i in range(5):
            cx = x + 26 + i * 12
            d.ellipse([cx, y + h - 38, cx + 9, y + h - 29],
                      fill=(40, 48, 34))
        d.ellipse([x + w - 40, y + 10, x + w - 12, y + 38],
                  fill=(255, 220, 130))
        d.rectangle([x + 8, y + 10, x + 34, y + 20], fill=(150, 120, 80))
    elif idx == 6:
        # US Senate: Capitol dome and a 51-48 vote tally.
        d.rectangle([x, y, x + w, y + h], fill=(200, 220, 235))
        d.rectangle([x + 8, y + h - 24, x + w - 8, y + h - 14],
                    fill=(240, 240, 240))
        d.rectangle([x + 22, y + h - 44, x + w - 22, y + h - 24],
                    fill=(240, 240, 240))
        d.pieslice([x + w / 2 - 26, y + 12, x + w / 2 + 26, y + 64], 180,
                   360, fill=WHITE)
        d.rectangle([x + w / 2 - 3, y + 6, x + w / 2 + 3, y + 16],
                    fill=WHITE)
        for i in range(3):
            cx = x + 30 + i * (w - 60) / 2
            d.rectangle([cx - 4, y + h - 44, cx + 4, y + h - 24],
                        fill=(180, 180, 185))
        f = font(FONT_BOLD, 20)
        d.text((x + w / 2 - 26, y + h - 20), "51-48", font=f,
               fill=(178, 34, 34))
    elif idx == 7:
        # Anthropic IPO: rising chart arrow and dollar sign.
        d.rectangle([x, y, x + w, y + h], fill=(24, 40, 56))
        pts = [(x + 8, y + h - 24), (x + 34, y + h - 44),
               (x + 56, y + h - 36), (x + 80, y + h - 58),
               (x + w - 10, y + 18)]
        d.line(pts, fill=(80, 200, 120), width=4, joint="curve")
        d.polygon([(x + w - 22, y + 12), (x + w - 6, y + 12),
                   (x + w - 10, y + 28)], fill=(80, 200, 120))
        f = font(FONT_BOLD, 20)
        t = "$83"
        d.text((x + w - f.getlength(t) - 8, y + h - 26), t, font=f, fill=GOLD)
        f2 = font(FONT_BOLD, 13)
        d.text((x + 12, y + h - 18), "+17%", font=f2, fill=(80, 200, 120))
    elif idx == 8:
        # GTA 6: neon city at sunset, palm trees.
        d.rectangle([x, y, x + w, y + h], fill=(64, 20, 80))
        d.rectangle([x, y + h - 30, x + w, y + h], fill=(20, 20, 40))
        d.ellipse([x + w / 2 - 18, y + 8, x + w / 2 + 18, y + 44],
                  fill=(255, 120, 80))
        skyline(d, x + 4, y + 30, w - 8, h - 40, (30, 10, 50), y + h - 30)
        for wx in (x + 20, x + 70):
            d.line([wx, y + h - 52, wx, y + h - 30], fill=(20, 90, 40),
                   width=3)
            d.arc([wx - 12, y + h - 62, wx + 12, y + h - 44], 200, 340,
                  fill=(20, 120, 50), width=3)
        f = font(FONT_BOLD, 24)
        d.text((x + w - 44, y + 6), "VI", font=f, fill=(255, 220, 90))
    elif idx == 9:
        # Nvidia: computer chip with a falling chart.
        d.rectangle([x, y, x + w, y + h], fill=(16, 60, 30))
        cx, cy = x + w / 2, y + h / 2 + 6
        d.rectangle([cx - 26, cy - 22, cx + 26, cy + 22], fill=(30, 110, 50),
                    outline=(120, 220, 140), width=2)
        d.rectangle([cx - 12, cy - 10, cx + 12, cy + 10], fill=(120, 220, 140))
        for i in range(3):
            d.line([cx - 26 + i * 26, cy - 22, cx - 26 + i * 26, cy - 30],
                   fill=(120, 220, 140), width=3)
            d.line([cx - 26 + i * 26, cy + 22, cx - 26 + i * 26, cy + 30],
                   fill=(120, 220, 140), width=3)
        d.line([(x + 8, y + 14), (x + 40, y + 30), (x + 66, y + 22),
                (x + w - 8, y + 44)], fill=(255, 90, 70), width=4)
        d.polygon([(x + w - 20, y + 34), (x + w - 4, y + 34),
                   (x + w - 8, y + 50)], fill=(255, 90, 70))
    elif idx == 10:
        # EU loan: circle of gold stars and a euro sign.
        d.rectangle([x, y, x + w, y + h], fill=(20, 50, 130))
        import math
        cx, cy = x + w / 2, y + h / 2
        for k in range(12):
            ang = math.radians(k * 30 - 90)
            sx = cx + 38 * math.cos(ang)
            sy = cy + 34 * math.sin(ang)
            d.ellipse([sx - 3, sy - 3, sx + 3, sy + 3], fill=GOLD)
        f = font(FONT_BOLD, 30)
        t = "\u20ac"
        d.text((cx - f.getlength(t) / 2, cy - 16), t, font=f, fill=WHITE)
    elif idx == 11:
        # Migrant boat: small boat tipping on rough waves.
        d.rectangle([x, y, x + w, y + h], fill=(30, 90, 140))
        d.polygon([(x + 18, y + 42), (x + w - 18, y + 30),
                   (x + w - 30, y + 52), (x + 30, y + 56)],
                  fill=(120, 70, 40))
        d.line([x + w / 2, y + 42, x + w / 2, y + 16], fill=(90, 60, 35),
               width=3)
        d.polygon([(x + w / 2, y + 16), (x + w / 2 + 22, y + 38),
                   (x + w / 2, y + 38)], fill=(240, 240, 235))
        for i in range(3):
            wy = y + h - 26 + i * 8
            d.arc([x + 6, wy - 8, x + w - 6, wy + 8], 0, 180, fill=WHITE,
                  width=2)
    elif idx == 12:
        # Greenland deal: iceberg and a unanimous 109-0 vote.
        d.rectangle([x, y, x + w, y + h], fill=(170, 210, 235))
        d.rectangle([x, y + h - 26, x + w, y + h], fill=(40, 110, 170))
        d.polygon([(x + 12, y + h - 26), (x + 40, y + 18),
                   (x + 66, y + h - 26)], fill=WHITE)
        d.polygon([(x + 52, y + h - 26), (x + 82, y + 30),
                   (x + w - 12, y + h - 26)], fill=(230, 240, 250))
        f = font(FONT_BOLD, 18)
        t = "109-0"
        d.text((x + w - f.getlength(t) - 8, y + 6), t, font=f, fill=NAVY)
    elif idx == 13:
        # IAEA / North Korea: atom symbol over a facility.
        d.rectangle([x, y, x + w, y + h], fill=(40, 44, 52))
        cx, cy = x + w / 2, y + h / 2 - 4
        for k in range(3):
            d.ellipse([cx - 34, cy - 14, cx + 34, cy + 14],
                      outline=(255, 200, 60), width=2)
        d.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=(255, 200, 60))
        d.rectangle([x + 8, y + h - 22, x + w - 8, y + h - 12],
                    fill=(90, 95, 105))
        d.rectangle([x + 16, y + h - 40, x + 34, y + h - 22],
                    fill=(120, 125, 135))
        d.rectangle([x + 44, y + h - 34, x + 58, y + h - 22],
                    fill=(120, 125, 135))
    else:
        # Bitcoin: gold coin with a dip-then-recovery chart.
        d.rectangle([x, y, x + w, y + h], fill=(20, 30, 44))
        cx, cy = x + 34, y + 34
        d.ellipse([cx - 24, cy - 24, cx + 24, cy + 24], fill=(247, 147, 26))
        f = font(FONT_BOLD, 26)
        t = "\u20bf"
        d.text((cx - f.getlength(t) / 2, cy - 15), t, font=f, fill=WHITE)
        d.line([(x + 8, y + h - 22), (x + 40, y + h - 40),
                (x + 66, y + h - 14), (x + w - 8, y + h - 34)],
               fill=(80, 200, 120), width=4)


def main():
    img = Image.new("RGB", (W, H), WHITE)
    d = ImageDraw.Draw(img)

    # --- Masthead ---
    d.rectangle([0, 0, W, 104], fill=NAVY)
    f_title = font(FONT_BOLD, 34)
    f_date = font(FONT_BOLD, 42)
    t = "THE WORLD TODAY"
    d.text(((W - f_title.getlength(t)) / 2, 10), t, font=f_title, fill=GOLD)
    t = "Thursday 19 November 2026"
    d.text(((W - f_date.getlength(t)) / 2, 50), t, font=f_date, fill=WHITE)
    d.rectangle([0, 104, W, 108], fill=GOLD)

    # --- Lead story (index 0), big slot ---
    lx, ly, lw, lh = 16, 122, 330, 186
    draw_thumb(d, 0, lx, ly, lw, lh)
    badge(d, lx, ly, 1)
    d.rectangle([lx, ly, lx + lw, ly + lh], outline=(0, 0, 0), width=2)
    tx = lx + lw + 18
    tw = W - 16 - tx
    f_kick = font(FONT_BOLD, 16)
    d.text((tx, ly + 2), "LEAD STORY", font=f_kick, fill=RED)
    f_lead = font(FONT_BOLD, 25)
    lines = wrap(STORIES[0][0], f_lead, tw)
    yy = ly + 28
    for line in lines:
        d.text((tx, yy), line, font=f_lead, fill=INK)
        yy += 31
    f_src = font(FONT_REG, 15)
    d.text((tx, ly + lh - 22), "Source: " + STORIES[0][1], font=f_src,
           fill=GREY)
    d.line([16, 322, W - 16, 322], fill=LIGHT, width=2)

    # --- Grid: stories 2-15, two columns x seven rows ---
    f_head = font(FONT_BOLD, 16)
    f_src2 = font(FONT_REG, 13)
    row_h = 100
    top = 326
    for i, (headline, source) in enumerate(STORIES[1:], start=2):
        pos = i - 2
        col, row = pos % 2, pos // 2
        cx = 16 + col * 496
        cy = top + row * row_h
        if row > 0:
            d.line([16, cy - 2, W - 16, cy - 2], fill=LIGHT, width=1)
        if col == 1:
            d.line([cx - 8, cy, cx - 8, cy + row_h - 6], fill=LIGHT, width=1)
        tx0, ty0, tw0, th0 = cx, cy + 6, 118, 84
        draw_thumb(d, i - 1, tx0, ty0, tw0, th0)
        badge(d, tx0, ty0, i)
        d.rectangle([tx0, ty0, tx0 + tw0, ty0 + th0], outline=(0, 0, 0),
                    width=1)
        text_x = tx0 + tw0 + 10
        text_w = 496 - tw0 - 10 - 12
        lines = wrap(headline, f_head, text_w)[:4]
        yy = ty0
        for line in lines:
            d.text((text_x, yy), line, font=f_head, fill=INK)
            yy += 20
        d.text((text_x, yy + 2), "Source: " + source, font=f_src2,
               fill=GREY)

    os.makedirs(OUT_DIR, exist_ok=True)
    out = os.path.join(OUT_DIR, "entry.png")
    img.save(out, "JPEG", quality=90, optimize=True)
    print("wrote", out)


if __name__ == "__main__":
    main()
