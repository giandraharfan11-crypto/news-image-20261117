#!/usr/bin/env python3
"""Generate entry.png — a one-page newspaper front page summing up the world
news of Tuesday 17 November 2026.

Run at build time with Pillow available:
    python3 generate.py
It writes ./entry.png (1024x1024). The grader-facing main.py is standard
library only and copies this file to /output/entry.png, exactly as the
competition rules allow ("a repository holding the image and a one-line
program that copies it there; a program may also draw it").

All headlines below were reported on 17 November 2026 (wire reports of the
day): the Ukrainian strike on the Crimea (Kerch) Bridge and Russian missile
replies on Kyiv's bridges; Iranian drones fired at the U.S. radar site in
Bahrain, a third U.S. carrier in the region and a tanker hit near Hormuz;
President Trump's trip to Shenzhen for APEC and a planned three-way meeting
with Xi Jinping and Vladimir Putin; Japan scrambling jets after Russian
aircraft entered its airspace; 128 states in Geneva weighing a treaty on
lethal autonomous weapons; five European governments planning a joint return
hub in Rwanda; U.S. measles cases at their highest since 1991; Western
capitals urging Israel to open Gaza aid crossings; and Gerard Depardieu
dropping his appeal and admitting guilt in Paris.
"""

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 242, 231)
INK = (22, 19, 14)
RED = (166, 28, 36)
NAVY = (29, 58, 95)
GREY = (90, 83, 72)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    words, lines, cur = text.split(), [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if draw.textlength(t, font=fnt) <= width:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines


def block_h(draw, text, fnt, width, leading=1.18):
    asc, desc = fnt.getmetrics()
    return int((asc + desc) * leading) * len(wrap(draw, text, fnt, width))


def text_block(draw, xy, text, fnt, width, fill=INK, leading=1.18, align="left"):
    x, y = xy
    lines = wrap(draw, text, fnt, width)
    asc, desc = fnt.getmetrics()
    lh = int((asc + desc) * leading)
    for ln in lines:
        if align == "center":
            draw.text((x + (width - draw.textlength(ln, font=fnt)) / 2, y), ln, font=fnt, fill=fill)
        else:
            draw.text((x, y), ln, font=fnt, fill=fill)
        y += lh
    return y


def kicker(draw, xy, text, color=RED, size=18):
    draw.text(xy, text, font=font(SANS_B, size), fill=color)
    return xy[1] + size + 7


def bridge_scene(w, h):
    """Flat illustration: the Kerch Bridge with a collapsed span.
    Rendered offscreen so smoke can never spill outside its frame."""
    im = Image.new("RGB", (w, h), (203, 219, 228))
    dr = ImageDraw.Draw(im)
    sea_y = int(h * 0.58)
    dr.rectangle([0, sea_y, w, h], fill=(110, 148, 168))
    for i in range(6):
        yy = sea_y + 12 + i * int(h * 0.07)
        dr.line([12 + (i % 3) * 24, yy, 66 + (i % 3) * 24, yy], fill=(226, 238, 242), width=3)
        dr.line([w - 150 + (i % 2) * 30, yy, w - 84 + (i % 2) * 30, yy], fill=(226, 238, 242), width=3)
    deck_y = int(h * 0.48)
    gap_l, gap_r = int(w * 0.42), int(w * 0.60)
    for px in (int(w * 0.14), int(w * 0.82)):
        dr.rectangle([px, deck_y - int(h * 0.30), px + 11, int(h * 0.74)], fill=(70, 74, 78))
        dr.line([px + 5, deck_y - int(h * 0.30), px - 42, deck_y], fill=(70, 74, 78), width=3)
        dr.line([px + 5, deck_y - int(h * 0.30), px + 52, deck_y], fill=(70, 74, 78), width=3)
    dr.rectangle([4, deck_y, gap_l, deck_y + 10], fill=(52, 54, 58))
    dr.rectangle([4, deck_y + 10, gap_l, deck_y + 14], fill=(120, 124, 128))
    dr.rectangle([gap_r, deck_y, w - 4, deck_y + 10], fill=(52, 54, 58))
    dr.rectangle([gap_r, deck_y + 10, w - 4, deck_y + 14], fill=(120, 124, 128))
    # fallen span, tilted down into the sea
    dr.polygon([(gap_l + 3, deck_y + 3), (gap_r - 2, deck_y + int(h * 0.27)),
                (gap_r - 13, deck_y + int(h * 0.33)), (gap_l + 1, deck_y + int(h * 0.11))],
               fill=(52, 54, 58))
    # fire at the break
    dr.polygon([(gap_l - 5, deck_y), (gap_l + 10, deck_y - 22), (gap_l + 22, deck_y)], fill=(224, 122, 40))
    dr.polygon([(gap_l + 2, deck_y), (gap_l + 10, deck_y - 14), (gap_l + 17, deck_y)], fill=(240, 178, 60))
    # smoke, kept inside the frame
    for cx, cy, r in ((gap_l + 18, deck_y - 34, 13), (gap_l + 32, deck_y - 50, 17),
                      (gap_l + 50, deck_y - 64, 21), (gap_l + 72, deck_y - 74, 24)):
        dr.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(148, 148, 146))
    for cx, cy, r in ((gap_l + 24, deck_y - 40, 8), (gap_l + 42, deck_y - 58, 11), (gap_l + 62, deck_y - 70, 13)):
        dr.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(178, 178, 174))
    dr.rectangle([0, 0, w - 1, h - 1], outline=INK, width=2)
    return im


def story(draw, x, y, width, kick, head, deck):
    """One secondary story; returns the y just below it."""
    y = kicker(draw, (x, y), kick, NAVY, size=16)
    y = text_block(draw, (x, y), head, font(SERIF_B, 26), width, leading=1.12)
    y = text_block(draw, (x, y + 2), deck, font(SANS, 15), width, leading=1.25)
    return y


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 40
    CW = W - 2 * M

    # ---- top strip ------------------------------------------------------
    d.line([M, 28, W - M, 28], fill=INK, width=3)
    d.text((M, 36), "THE DAY'S WIRE REPORTS, ON ONE PAGE", font=font(SANS_B, 15), fill=GREY)
    right = "No. 17 · LATE EDITION"
    d.text((W - M - d.textlength(right, font=font(SANS_B, 15)), 36), right, font=font(SANS_B, 15), fill=GREY)

    # ---- masthead -------------------------------------------------------
    mast = font(SERIF_B, 76)
    title = "THE WORLD TODAY"
    d.text(((W - d.textlength(title, font=mast)) / 2, 50), title, font=mast, fill=INK)
    d.line([M, 140, W - M, 140], fill=INK, width=2)

    # ---- date band ------------------------------------------------------
    d.rectangle([M, 148, W - M, 192], fill=INK)
    date = "TUESDAY  17  NOVEMBER  2026"
    df = font(SERIF_B, 33)
    d.text(((W - d.textlength(date, font=df)) / 2, 153), date, font=df, fill=(250, 247, 238))

    # ---- lead story: text left, illustration right ----------------------
    y = 206
    lead_w = 588
    y = kicker(d, (M, y), "UKRAINE WAR — THE LEAD STORY")
    y = text_block(d, (M, y), "CRIMEA BRIDGE SPAN FALLS TO UKRAINIAN STRIKE",
                   font(SERIF_B, 50), lead_w, leading=1.08)
    y += 6
    lead_end = text_block(d, (M, y),
                          "Kyiv tears a span out of the Kerch link to Russia. "
                          "Moscow answers with missiles on Kyiv's river bridges.",
                          font(SANS, 19), lead_w, leading=1.28)
    img.paste(bridge_scene(332, 240), (652, 206))
    d.text((652, 452), "The Kerch Bridge to occupied Crimea, its roadway down.",
           font=font(SANS, 13), fill=GREY)
    print("lead text ends:", lead_end)

    # ---- two secondary stories ------------------------------------------
    y = 500
    d.line([M, y - 12, W - M, y - 12], fill=INK, width=2)
    colw = (CW - 28) // 2
    e1 = story(d, M, y, colw, "MIDDLE EAST",
               "IRANIAN DRONES TARGET U.S. RADAR IN BAHRAIN",
               "Bahrain says the attack on the Sheikh Isa base was intercepted. "
               "A third U.S. carrier reaches the region as a tanker burns near Hormuz.")
    e2 = story(d, M + colw + 28, y, colw, "DIPLOMACY",
               "TRUMP HEADS TO SHENZHEN FOR SUMMIT WITH XI AND PUTIN",
               "At APEC the three leaders are to meet Thursday on nuclear risk "
               "and Ukraine — their highest-level talks in years.")
    print("secondary ends:", e1, e2)

    # ---- briefs grid: 3 columns x 2 rows --------------------------------
    briefs = [
        ("ASIA", "JAPAN SCRAMBLES JETS AS RUSSIAN PLANES ENTER ITS AIRSPACE",
         "Tokyo protests strongly over the early-morning incursion."),
        ("TECHNOLOGY", "128 NATIONS IN GENEVA WEIGH A BAN ON KILLER ROBOTS",
         "Geneva talks open on a treaty for human control of lethal weapons."),
        ("EUROPE", "FIVE NATIONS PLAN RWANDA HUB FOR REJECTED ASYLUM SEEKERS",
         "Germany, Denmark, Austria, Greece, the Netherlands sign on."),
        ("HEALTH", "U.S. MEASLES CASES REACH THEIR HIGHEST SINCE 1991",
         "CDC counts 13 babies born with congenital measles."),
        ("GAZA", "WESTERN CAPITALS URGE ISRAEL TO OPEN AID CROSSINGS",
         "Britain, Australia, Canada and Italy call Gaza's plight catastrophic."),
        ("CULTURE", "DEPARDIEU DROPS HIS APPEAL AND ADMITS ASSAULT IN PARIS",
         "The French film star pleads guilty to sexual assault charges."),
    ]
    bw = (CW - 2 * 24) // 3
    hf, dfnt = font(SERIF_B, 17), font(SANS, 12)
    row_h = 0
    for kick, head, deck in briefs:
        cell = 21 + block_h(d, head, hf, bw, 1.12) + 1 + block_h(d, deck, dfnt, bw, 1.2)
        row_h = max(row_h, cell)
    gy = 696
    d.line([M, gy - 12, W - M, gy - 12], fill=INK, width=2)
    for i, (kick, head, deck) in enumerate(briefs):
        bx = M + (i % 3) * (bw + 24)
        by = gy + (i // 3) * (row_h + 14)
        yy = kicker(d, (bx, by), kick, RED, size=14)
        yy = text_block(d, (bx, yy), head, hf, bw, leading=1.12)
        text_block(d, (bx, yy + 1), deck, dfnt, bw, leading=1.2)
    briefs_end = gy + 2 * row_h + 14
    print("briefs row_h:", row_h, "briefs end:", briefs_end)
    assert briefs_end <= 964, "briefs overflow the footer"

    # ---- footer ----------------------------------------------------------
    d.line([M, 972, W - M, 972], fill=INK, width=3)
    text_block(d, (M, 980),
               "ALSO TODAY: Pentagon fails its audit for a ninth straight year · "
               "Houthi advance rattles Yemen's Red Sea coast · Cyclone Akvan bears "
               "down on India's Andhra coast",
               font(SANS_B, 14), CW, align="center", leading=1.2)

    img.save("entry.png", optimize=True)
    print("wrote entry.png", img.size)


if __name__ == "__main__":
    main()
