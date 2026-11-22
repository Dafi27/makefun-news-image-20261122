#!/usr/bin/env python3
"""Render the 22 November 2026 world-news front page (1024x1024 PNG).

Run once, locally, to produce entry.png. The submitted entrypoint
(main.py) only copies that PNG to /output/entry.png, so the graded run
is byte-identical every time.
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (248, 244, 232)
INK = (24, 24, 24)
GREY = (90, 86, 76)
RED = (163, 22, 33)
BLUE = (29, 78, 137)
TEAL = (14, 116, 108)
RULE = (180, 172, 152)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    lines = []
    for para in text.split("\n"):
        line = ""
        for word in para.split(" "):
            trial = (line + " " + word).strip()
            if draw.textlength(trial, font=fnt) <= width:
                line = trial
            else:
                if line:
                    lines.append(line)
                line = word
        if line:
            lines.append(line)
    return lines


def para(draw, x, y, text, fnt, width, fill=INK, leading=6):
    for ln in wrap(draw, text, fnt, width):
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += fnt.size + leading
    return y


def kicker(draw, x, y, label, color, size=20):
    fnt = font(SANS_B, size)
    w = draw.textlength(label, font=fnt) + 18
    h = size + 10
    draw.rounded_rectangle([x, y, x + w, y + h], radius=4, fill=color)
    draw.text((x + 9, y + 5), label, font=fnt, fill=(255, 255, 255))
    return w, h


img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

# ---- masthead -------------------------------------------------------------
d.rectangle([0, 0, W, 10], fill=RED)
d.text((W // 2, 24), "THE WORLD TODAY", font=font(SERIF_B, 72),
       fill=INK, anchor="ma")
d.text((W // 2, 112), "SUNDAY  \u2022  22 NOVEMBER 2026  \u2022  THE DAY IN WORLD NEWS",
       font=font(SANS_B, 23), fill=RED, anchor="ma")
d.line([48, 156, W - 48, 156], fill=INK, width=3)
d.line([48, 162, W - 48, 162], fill=INK, width=1)

y = 180
# ---- lead story: Ukraine peace talks --------------------------------------
_, kh = kicker(d, 48, y, "UKRAINE  \u2022  PEACE TALKS", RED)
y += kh + 10
y = para(d, 48, y,
         "US envoys head to Moscow\nafter Abu Dhabi talks",
         font(SERIF_B, 44), W - 96, leading=4)
y += 4
y = para(d, 48, y,
         "After two days of trilateral talks in Abu Dhabi, US envoys Jared "
         "Kushner and Steve Witkoff fly to Moscow to brief President Putin, "
         "as Russia repeats its demand that NATO pull back to 1997 lines.",
         font(SANS, 22), W - 96, leading=6)
y += 10
d.line([48, y, W - 48, y], fill=RULE, width=2)
y += 16

# ---- 2x2 grid --------------------------------------------------------------
stories = [
    ("IRAN", RED,
     "Trump seeks lasting nuclear deal with Iran",
     "President Trump said he wants a permanent accord to stop Iran "
     "obtaining nuclear weapons, as two tankers were struck near Oman."),
    ("GAZA", BLUE,
     "Storms flood shelters across Gaza",
     "Heavy rain and cold have flooded tents across the Strip, leaving "
     "more than a million displaced people exposed to the cold."),
    ("MEXICO", TEAL,
     "Mexico captures cartel fugitive \u2018Chapo Isidro\u2019",
     "Mexican special forces, with US support, captured the FBI Ten Most "
     "Wanted fugitive in Sinaloa. Violence after the arrest killed 11."),
    ("MARKETS", (122, 90, 8),
     "Anthropic IPO meets tech\u2019s worst week since 2020",
     "Anthropic\u2019s record listing collided with a brutal week for tech "
     "stocks, while Nvidia faces a US SEC inquiry, sources say."),
]
cw = 452
gapx, gapy = 32, 16
row_h = 0
for i, (tag, color, head, body) in enumerate(stories):
    cx = 48 + (i % 2) * (cw + gapx)
    cy = y + (i // 2) * (row_h + gapy) if i >= 2 else y
    if i == 2:
        # measure row height from the first row's content
        pass
    _, kh = kicker(d, cx, cy, tag, color, size=19)
    yy = para(d, cx, cy + kh + 8, head, font(SERIF_B, 24), cw, leading=3)
    yy = para(d, cx, yy + 2, body, font(SANS, 18), cw, leading=4)
    if i % 2 == 0:
        d.line([cx + cw + 16, cy, cx + cw + 16, yy], fill=RULE, width=1)
    if i == 1:
        row_h = yy - y
y = y + 2 * row_h + gapy

# ---- sport band ------------------------------------------------------------
d.line([48, y, W - 48, y], fill=RULE, width=2)
y += 12
kw, kh = kicker(d, 48, y, "SPORT", RED, size=19)
d.text((48 + kw + 14, y + 2),
       "Messi makes history with back-to-back MLS Golden Boots",
       font=font(SERIF_B, 25), fill=INK)
y += kh + 8
y = para(d, 48, y,
         "Lionel Messi won a second straight MLS Golden Boot \u2014 and India "
         "posted 720/9, a record Test total in New Zealand.",
         font(SANS, 19), W - 96, leading=5)
y += 10

# ---- also today ------------------------------------------------------------
d.line([48, y, W - 48, y], fill=INK, width=2)
y += 10
d.text((48, y), "ALSO TODAY", font=font(SANS_B, 20), fill=RED)
y += 30
y = para(d, 48, y,
         "Peru hit by a magnitude 6.9 earthquake in Jun\u00edn  \u2022  COP31 "
         "climate talks deadlocked over fossil fuels  \u2022  Norway\u2019s top "
         "court voids disputed oil licences  \u2022  EU gives Ukraine "
         "\u20ac1bn more military aid",
         font(SANS, 19), W - 96, leading=5)

# ---- footer ----------------------------------------------------------------
d.line([48, H - 44, W - 48, H - 44], fill=RULE, width=1)
d.text((W // 2, H - 34), "22 NOVEMBER 2026 \u2014 THE WORLD IN ONE PAGE",
       font=font(SANS_B, 18), fill=GREY, anchor="ma")

assert y < H - 56, f"content overflow: y={y}"
img.save("/home/hatch/workspace/makefun/news22-bot/entry.png",
         optimize=True)
print("saved", img.size, "content ends y =", y)
