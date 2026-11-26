#!/usr/bin/env python3
"""THE WORLD TODAY — Wednesday 25 November 2026.

Draws a newspaper front page summing up the day's verified world news
and writes it to /output/entry.png (1024x1024). Deterministic: no clock,
no randomness, no network — the same input always yields the same bytes.
"""
import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (246, 241, 231)
INK = (17, 17, 17)
RED = (178, 34, 34)
NAVY = (14, 26, 51)
GREY = (90, 86, 78)
RULE = (60, 56, 48)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


SERIF = "DejaVuSerif.ttf"
SERIF_B = "DejaVuSerif-Bold.ttf"
SANS = "DejaVuSans.ttf"
SANS_B = "DejaVuSans-Bold.ttf"


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap returning a list of lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def para(draw, x, y, text, fnt, max_w, fill=INK, leading=1.28):
    """Draw a wrapped paragraph; return the y just below it."""
    for line in wrap(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += int(fnt.size * leading)
    return y


def rule(draw, x0, x1, y, width=2, fill=RULE):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


def kicker(draw, x, y, text, size=16, fill=RED):
    draw.text((x, y), text, font=font(SANS_B, size), fill=fill)
    return y + size + 6


def draw_space_panel(img, x0, y0, x1, y1):
    """A small night-sky panel: stars, Earth curve, rocket, station ring.

    Drawn on its own layer so the Earth arc is clipped to the panel.
    """
    pw, ph = x1 - x0, y1 - y0
    layer = Image.new("RGB", (pw, ph), NAVY)
    ld = ImageDraw.Draw(layer)
    stars = [
        (0.08, 0.10, 2), (0.22, 0.06, 1), (0.35, 0.14, 2), (0.48, 0.05, 1),
        (0.60, 0.12, 2), (0.74, 0.07, 1), (0.88, 0.13, 2), (0.15, 0.28, 1),
        (0.42, 0.24, 1), (0.66, 0.26, 2), (0.82, 0.30, 1), (0.28, 0.38, 1),
        (0.55, 0.36, 1), (0.92, 0.42, 2), (0.10, 0.48, 2), (0.38, 0.50, 1),
    ]
    for fx, fy, r in stars:
        cx, cy = int(fx * pw), int(fy * ph)
        ld.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(240, 240, 220))
    # Earth arc along the bottom (clipped to the panel by the layer).
    ld.ellipse([-60, ph - 80, pw + 60, ph + 160], fill=(38, 78, 130))
    ld.ellipse([-60, ph - 80, pw + 60, ph + 160],
               outline=(120, 170, 220), width=2)
    # Station ring (Tiangong) upper right.
    sx, sy = int(0.68 * pw), int(0.30 * ph)
    ld.ellipse([sx - 46, sy - 12, sx + 46, sy + 12], outline=(230, 230, 210),
               width=3)
    ld.ellipse([sx - 8, sy - 8, sx + 8, sy + 8], fill=(230, 230, 210))
    # Rocket climbing, centre-left.
    rx, ry = int(0.30 * pw), int(0.50 * ph)
    body = [(rx - 9, ry + 42), (rx - 9, ry - 8), (rx, ry - 30),
            (rx + 9, ry - 8), (rx + 9, ry + 42)]
    ld.polygon(body, fill=(235, 235, 225))
    ld.polygon([(rx - 9, ry + 42), (rx - 20, ry + 58), (rx - 9, ry + 48)],
               fill=(200, 60, 50))
    ld.polygon([(rx + 9, ry + 42), (rx + 20, ry + 58), (rx + 9, ry + 48)],
               fill=(200, 60, 50))
    ld.polygon([(rx - 5, ry + 42), (rx, ry + 66), (rx + 5, ry + 42)],
               fill=(255, 176, 66))
    ld.ellipse([rx - 4, ry - 14, rx + 4, ry - 6], fill=NAVY)
    img.paste(layer, (x0, y0))


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    mx = 34
    rx = W - mx

    # ---- Masthead ----
    small = font(SANS, 15)
    tag = "THE WORLD IN ONE PAGE"
    d.text(((W - d.textlength(tag, font=small)) / 2, 26), tag,
           font=small, fill=GREY)
    mast = font(SERIF_B, 62)
    title = "THE WORLD TODAY"
    d.text(((W - d.textlength(title, font=mast)) / 2, 44), title,
           font=mast, fill=INK)
    rule(d, mx, rx, 122, width=3)
    rule(d, mx, rx, 127, width=1)
    date_f = font(SANS_B, 15)
    d.text((mx, 136), "WEDNESDAY, 25 NOVEMBER 2026", font=date_f, fill=INK)
    vol = "VOL. I — No. 329"
    d.text((rx - d.textlength(vol, font=date_f), 136), vol,
           font=date_f, fill=GREY)
    rule(d, mx, rx, 158, width=1)

    # ---- Lead story: space ----
    y = 178
    kicker(d, mx, y, "SPACE  ·  FIRST FOR PAKISTAN")
    head = font(SERIF_B, 50)
    d.text((mx, 208), "PAKISTAN", font=head, fill=INK)
    d.text((mx, 264), "REACHES ORBIT", font=head, fill=INK)
    rule(d, mx, 620, 322, width=2, fill=RED)
    dek = ("Shenzhou-24 lifts off from Jiuquan carrying Muhammad "
           "Zeeshan Ali — the first Pakistani in space, and the "
           "first foreigner aboard China's Tiangong station.")
    y = para(d, mx, 336, dek, font(SERIF, 20), 586, leading=1.32)
    body = ("The Long March-2F rocket rose at 08:18 Beijing time; "
            "docking followed about three and a half hours later. "
            "Ali, a Pakistan Air Force pilot, will spend about a week "
            "in orbit on four Pakistani biotechnology experiments.")
    para(d, mx, y + 8, body, font(SERIF, 16), 586, fill=(40, 38, 34))
    draw_space_panel(img, 650, 178, 990, 470)

    # ---- Markets band ----
    rule(d, mx, rx, 496, width=2)
    d.rectangle([mx, 512, mx + 7, 606], fill=RED)
    kicker(d, mx + 22, 512, "MARKETS IN TURMOIL")
    mhead = font(SERIF_B, 29)
    d.text((mx + 22, 540),
           "KOSPI PLUNGES 6.2% AS AI SELL-OFF SPREADS",
           font=mhead, fill=INK)
    mbody = ("Seoul's benchmark fell to a 10-month low at 4,697.51. Samsung "
             "slid 9.9%, SK Hynix 11.1%. Taiwan's Taiex lost 4.8%, Tokyo's "
             "Nikkei 2.8% and the Nasdaq 1.5% as the AI rally fizzled.")
    para(d, mx + 22, 578, mbody, font(SERIF, 15), 920,
         fill=(40, 38, 34), leading=1.3)

    # ---- Grid: four stories ----
    rule(d, mx, rx, 632, width=2)
    grid = [
        ("CAIRO", "31 KILLED AS TANKER FIRE ENGULFS CAIRO HIGHWAY",
         "A fuel tanker overturned on the Ring Road at Warraq, Giza, on "
         "Wednesday evening. At least 31 people died and 21 were injured."),
        ("WEST JAVA", "9 DEAD IN FLOODED GOLD MINE",
         "Rescuers search for 17 miners still missing after floodwater "
         "swept through a gold mine in West Java."),
        ("WASHINGTON", "TRUMP FIRES NEW TARIFF SALVO",
         "The US proposes new tariffs on 14 trading partners, including "
         "China at 20%, after a probe of excess factory capacity."),
        ("LONDON", "ENERGY BILLS TO RISE 26%",
         "Britain's price cap lifts annual bills to £2,166 from January — "
         "over £2,000 a year for a typical household."),
    ]
    gx0, gy0 = mx, 650
    cw, ch = 468, 116
    gap_x, gap_y = 20, 14
    for i, (place, head_txt, body_txt) in enumerate(grid):
        cx = gx0 + (i % 2) * (cw + gap_x)
        cy = gy0 + (i // 2) * (ch + gap_y)
        kicker(d, cx, cy, place, size=14)
        y = cy + 24
        y = para(d, cx, y, head_txt, font(SERIF_B, 21), cw, leading=1.18)
        para(d, cx, y + 2, body_txt, font(SERIF, 14), cw,
             fill=(40, 38, 34), leading=1.25)

    # ---- Bottom strip ----
    rule(d, mx, rx, 912, width=2)
    strip = font(SANS, 15)
    y = 928
    d.text((mx, y), "ALSO TODAY", font=font(SANS_B, 15), fill=RED)
    items = ("Huawei guilty on 10 of 12 counts in US case  ·  Nvidia falls 6% "
             "·  SoftBank slumps 14.8%  ·  Core PCE inflation 3.3%")
    para(d, mx, y + 24, items, strip, 956, fill=(40, 38, 34), leading=1.3)

    # ---- Footer ----
    rule(d, mx, rx, 988, width=1)
    foot = font(SANS, 12)
    ft = "THE WORLD TODAY  ·  WEDNESDAY 25 NOVEMBER 2026"
    d.text(((W - d.textlength(ft, font=foot)) / 2, 996), ft,
           font=foot, fill=GREY)

    img.save(os.path.join(out_dir, "entry.png"))


if __name__ == "__main__":
    main()
