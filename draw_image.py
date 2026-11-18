#!/usr/bin/env python3
"""Draw the 18 November 2026 world-news front page (1024x1024 PNG).

Fresh design, drawn with PIL only. No network, deterministic output.
Layout is computed top-down: each block reports its own height, so
nothing overlaps a divider.
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (246, 241, 229)
INK = (20, 20, 20)
RED = (179, 32, 44)
BLUE = (29, 78, 137)
GREY = (90, 86, 76)
GOLD = (176, 132, 32)
BODY = (50, 50, 50)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(draw, x, y, text, fnt, max_w, fill=INK, spacing=4):
    for ln in wrap(draw, text, fnt, max_w):
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += fnt.size + spacing
    return y


def hline(draw, x0, x1, y, w=2, fill=INK):
    draw.line([(x0, y), (x1, y)], fill=fill, width=w)


def icon_plane(d, x, y, s, fill=BLUE):
    # side-view jet: fuselage, tail fin, swept wings
    d.polygon([(x, y + s * 0.42), (x + s * 0.80, y + s * 0.42),
               (x + s, y + s * 0.52), (x + s * 0.80, y + s * 0.60),
               (x, y + s * 0.60)], fill=fill)
    d.polygon([(x + s * 0.06, y + s * 0.42), (x + s * 0.10, y + s * 0.08),
               (x + s * 0.22, y + s * 0.42)], fill=fill)
    d.polygon([(x + s * 0.42, y + s * 0.60), (x + s * 0.58, y + s * 0.92),
               (x + s * 0.70, y + s * 0.60)], fill=fill)


def icon_bridge(d, x, y, s, fill=RED):
    d.rectangle([x, y + s * 0.55, x + s, y + s * 0.64], fill=fill)
    for i in range(3):
        ax = x + s * (0.06 + i * 0.30)
        d.arc([ax, y + s * 0.05, ax + s * 0.28, y + s * 0.72],
              start=180, end=360, fill=fill, width=5)
    for i in range(4):
        px = x + s * (0.05 + i * 0.30)
        d.line([(px, y + s * 0.55), (px, y + s * 0.64)], fill=fill, width=3)


def icon_radar(d, x, y, s, fill=INK):
    cx, cy = x + s / 2, y + s * 0.72
    for r in (s * 0.44, s * 0.29, s * 0.14):
        d.arc([cx - r, cy - r, cx + r, cy + r], start=180, end=360,
              fill=fill, width=4)
    d.line([(cx, cy), (cx + s * 0.36, cy - s * 0.36)], fill=RED, width=4)
    d.ellipse([cx + s * 0.30, cy - s * 0.42, cx + s * 0.42, cy - s * 0.30],
              fill=RED)
    d.line([(x, cy), (x + s, cy)], fill=fill, width=3)


def icon_chip(d, x, y, s, fill=BLUE):
    d.rectangle([x + s * 0.2, y + s * 0.2, x + s * 0.8, y + s * 0.8],
                outline=fill, width=5)
    d.rectangle([x + s * 0.38, y + s * 0.38, x + s * 0.62, y + s * 0.62],
                fill=fill)
    for i in range(3):
        px = x + s * (0.3 + i * 0.2)
        d.line([(px, y), (px, y + s * 0.2)], fill=fill, width=4)
        d.line([(px, y + s * 0.8), (px, y + s)], fill=fill, width=4)
        py = y + s * (0.3 + i * 0.2)
        d.line([(x, py), (x + s * 0.2, py)], fill=fill, width=4)
        d.line([(x + s * 0.8, py), (x + s, py)], fill=fill, width=4)


def icon_storm(d, x, y, s, fill=BLUE):
    cx, cy = x + s / 2, y + s / 2
    for k in range(3):
        r0 = s * (0.10 + k * 0.11)
        d.arc([cx - r0, cy - r0, cx + r0, cy + r0],
              start=20 + k * 55, end=200 + k * 55, fill=fill, width=5)


def icon_trade(d, x, y, s, fill=GOLD):
    d.line([(x, y + s * 0.30), (x + s * 0.75, y + s * 0.30)], fill=fill,
           width=6)
    d.polygon([(x + s * 0.75, y + s * 0.12), (x + s, y + s * 0.30),
               (x + s * 0.75, y + s * 0.48)], fill=fill)
    d.line([(x + s * 0.25, y + s * 0.70), (x + s, y + s * 0.70)], fill=INK,
           width=6)
    d.polygon([(x + s * 0.25, y + s * 0.52), (x, y + s * 0.70),
               (x + s * 0.25, y + s * 0.88)], fill=INK)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 30
    X1 = W - M
    f_kick = font(SANS_B, 22)

    # --- masthead ---
    f_mast = font(SERIF, 84)
    title = "THE WORLD TODAY"
    tw = d.textlength(title, font=f_mast)
    d.text(((W - tw) / 2, 20), title, font=f_mast, fill=INK)
    hline(d, M, X1, 118, 3)
    hline(d, M, X1, 124, 1)
    f_date = font(SANS_B, 26)
    date = "WEDNESDAY, 18 NOVEMBER 2026"
    dw = d.textlength(date, font=f_date)
    d.text(((W - dw) / 2, 136), date, font=f_date, fill=RED)
    f_sub = font(SANS, 21)
    sub = "One day's world news — in one image"
    sw = d.textlength(sub, font=f_sub)
    d.text(((W - sw) / 2, 168), sub, font=f_sub, fill=GREY)
    hline(d, M, X1, 198, 3)

    # --- lead story ---
    y = 210
    d.text((M, y), "ASIA  •  MANILA", font=f_kick, fill=RED)
    y = draw_wrapped(d, M, y + 32, "Trump lands in Manila for Quad talks",
                     font(SERIF, 44), 630, spacing=2)
    y = draw_wrapped(d, M, y + 8,
                     "US president opens his Asia tour at the ASEAN summit, "
                     "ahead of a China visit.",
                     font(SANS, 23), 630, fill=BODY, spacing=4)
    # illustration right: skyline + plane
    ix, iy = 700, 218
    d.rectangle([ix, iy + 128, ix + 264, iy + 144], fill=INK)
    for bx, bw, bh in [(0, 44, 76), (52, 36, 110), (96, 48, 58),
                       (152, 38, 92), (198, 52, 126), (252, 12, 50)]:
        d.rectangle([ix + bx, iy + 144 - bh, ix + bx + bw, iy + 144],
                    fill=(70, 70, 70))
    icon_plane(d, ix + 30, iy - 4, 110)
    d.text((ix, iy + 152), "Manila hosts the ASEAN summit",
           font=font(SANS, 17), fill=GREY)
    y = max(y, iy + 176)
    hline(d, M, X1, y + 10, 2)
    y += 24

    # --- two-column row ---
    col_w = (W - 2 * M - 24) // 2
    row_y = y
    # left: Ukraine
    d.text((M, row_y), "WAR IN UKRAINE", font=f_kick, fill=RED)
    yl = draw_wrapped(d, M, row_y + 32,
                      "Ukraine strikes Crimean Bridge for a second day",
                      font(SERIF, 32), col_w, spacing=1)
    yl = draw_wrapped(d, M, yl + 6,
                      "Kyiv hits the Kerch link again as Russian strikes "
                      "damage bridges in the capital.",
                      font(SANS, 20), col_w, fill=BODY, spacing=3)
    icon_bridge(d, M, yl + 8, 64)
    yl += 8 + 64
    # right: Gulf
    rx = M + col_w + 24
    d.text((rx, row_y), "GULF TENSIONS", font=f_kick, fill=RED)
    yr = draw_wrapped(d, rx, row_y + 32,
                      "Iran drones hit US radar in Bahrain",
                      font(SERIF, 32), col_w, spacing=1)
    yr = draw_wrapped(d, rx, yr + 6,
                      "Tehran targets a US military radar system as Gulf "
                      "tensions rise after a tanker attack.",
                      font(SANS, 20), col_w, fill=BODY, spacing=3)
    icon_radar(d, rx, yr + 8, 64)
    yr += 8 + 64
    y = max(yl, yr)
    hline(d, M, X1, y + 10, 2)
    y += 22

    # --- three-column row ---
    cw = (W - 2 * M - 48) // 3
    row_y = y
    cols = [
        ("MARKETS", "Nvidia revenue doubles",
         "First results since Huang's ouster; the board says the "
         "ex-CEO will not return.", icon_chip, BLUE),
        ("WEATHER", "Cyclone Akvan strengthens",
         "Storm builds over the Bay of Bengal; India's east coast "
         "is on alert.", icon_storm, BLUE),
        ("TRADE", "Canada, China extend trade deals",
         "Xi meets Carney ahead of the APEC summit in a thaw "
         "for both sides.", icon_trade, GOLD),
    ]
    y = row_y
    for i, (kick, head, deck, ic, col) in enumerate(cols):
        cx = M + i * (cw + 24)
        d.text((cx, row_y), kick, font=f_kick, fill=RED)
        yc = draw_wrapped(d, cx, row_y + 32, head, font(SERIF, 26), cw,
                          spacing=1)
        yc = draw_wrapped(d, cx, yc + 5, deck, font(SANS, 18), cw,
                          fill=BODY, spacing=3)
        ic(d, cx, yc + 6, 52, col)
        y = max(y, yc + 6 + 52)
    hline(d, M, X1, y + 10, 2)
    y += 22

    # --- also today ticker (kicker line, then full-width text) ---
    d.text((M, y), "ALSO TODAY", font=f_kick, fill=RED)
    y = draw_wrapped(d, M, y + 32,
                     "Britain sanctions Israeli settlement firms  •  Dhoni "
                     "retires from the IPL  •  India win a 10th SAFF crown  "
                     "•  Latvia's cabinet wins its confidence vote  •  UN: "
                     "372 civilians killed in Ukraine in October",
                     font(SANS, 19), X1 - M, fill=BODY, spacing=3)
    hline(d, M, X1, y + 8, 1)
    d.text((M, y + 16), "Reported 18 November 2026  •  Sources: wire services",
           font=font(SANS, 16), fill=GREY)

    img.save("entry.png", optimize=True)
    print("saved entry.png", img.size)


if __name__ == "__main__":
    main()
