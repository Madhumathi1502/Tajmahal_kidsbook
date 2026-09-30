"""
THE TAJ MAHAL MYSTERY — Stage D, Batch 1
Page generator: Pages 1–10
Output: 2550 × 3300 px PNG, 300 DPI, portrait
"""

import os
import math
from PIL import Image, ImageDraw, ImageFont, ImageFilter

# ─── PATHS ───────────────────────────────────────────────────────────────────
BRAIN = r"C:\Users\madhu\.gemini\antigravity\brain\ccd8974b-98bd-4581-bc97-2cd95007b824"
OUT   = r"C:\Users\madhu\OneDrive\Documents\tajmahal\pages"
FONTS = r"C:\Windows\Fonts"

os.makedirs(OUT, exist_ok=True)

# ─── PALETTE ──────────────────────────────────────────────────────────────────
C = {
    "ivory":        (245, 240, 232),
    "warm_white":   (250, 247, 242),
    "parchment":    (232, 217, 184),
    "aged_paper":   (212, 196, 160),
    "sandstone":    (181,  83,  60),
    "indigo":       ( 44,  62, 107),
    "teal":         ( 42, 123, 111),
    "yamuna":       ( 74, 127, 165),
    "gold":         (201, 144,  42),
    "emerald":      ( 74, 124,  89),
    "charcoal":     ( 43,  43,  43),
    "warm_black":   ( 26,  21,  18),
    "stone_grey":   (140, 128, 112),
    "veining":      (200, 188, 168),
    "fic_bg":       (245, 230, 208),
    "fic_text":     (122,  75,  26),
    "hist_bg":      (232, 239, 245),
    "hist_text":    ( 44,  62, 107),
    "adv_bg":       (237, 245, 232),
    "adv_text":     ( 42,  92,  58),
    "mod_bg":       (240, 235, 245),
    "mod_text":     ( 74,  44, 107),
    "act_bg":       (238, 228, 210),
    "think_bg":     (234, 243, 248),
    "vocab_bg":     (232, 217, 184),
    "reward_bg":    (220, 175,  60),
}

# ─── PAGE DIMENSIONS ──────────────────────────────────────────────────────────
W, H   = 2550, 3300
DPI    = 300
ML, MR = 220, 220
MT, MB = 250, 200
LW     = W - ML - MR   # 2110
LH     = H - MT - MB   # 2850

# ─── FONTS ────────────────────────────────────────────────────────────────────
def F(name, size):
    path = os.path.join(FONTS, name)
    try:
        return ImageFont.truetype(path, size)
    except:
        return ImageFont.load_default()

fnt = {
    "title":      F("cambriab.ttf",  84),
    "header":     F("cambriab.ttf",  52),
    "h2":         F("cambriab.ttf",  36),
    "h3":         F("calibrib.ttf",  30),
    "body":       F("calibri.ttf",   26),
    "body_bold":  F("calibrib.ttf",  26),
    "body_it":    F("calibrii.ttf",  26),
    "act":        F("calibrib.ttf",  28),
    "label":      F("calibri.ttf",   22),
    "caption":    F("calibrii.ttf",  20),
    "pgnum":      F("cambria.ttf",   22),
    "vocab_word": F("cambriab.ttf",  34),
    "badge":      F("calibrib.ttf",  20),
    "badge_sm":   F("calibrib.ttf",  17),
    "small":      F("calibri.ttf",   20),
    "small_bold": F("calibrib.ttf",  20),
    "reward":     F("cambriab.ttf",  30),
    "reward_sm":  F("calibrib.ttf",  22),
}

# ─── HELPERS ──────────────────────────────────────────────────────────────────

def new_page():
    return Image.new("RGB", (W, H), C["ivory"])

def draw_page_border(draw):
    bx1, by1 = ML - 10, MT - 10
    bx2, by2 = W - MR + 10, H - MB + 10
    draw.rectangle([bx1, by1, bx2, by2], outline=C["veining"], width=3)
    s = 12
    for cx, cy in [(bx1, by1), (bx2, by1), (bx1, by2), (bx2, by2)]:
        draw.polygon([cx, cy-s, cx+s, cy, cx, cy+s, cx-s, cy], fill=C["gold"])

def draw_header_bar(draw, title, piece_num=None, piece_topic=None):
    bar_h = 110
    x1, y1 = ML, MT
    x2 = W - MR
    for i in range(bar_h):
        t = i / bar_h
        r = int(C["indigo"][0] * (1 + 0.15*t))
        g = int(C["indigo"][1] * (1 + 0.15*t))
        b = int(C["indigo"][2] * (1 + 0.15*t))
        draw.line([(x1, y1+i), (x2, y1+i)], fill=(min(r,255), min(g,255), min(b,255)))
    draw.rectangle([x1+12, y1+8, x1+28, y1+bar_h-8], fill=C["gold"])
    txt = title.upper()
    bb = draw.textbbox((0,0), txt, font=fnt["header"])
    tw = bb[2]-bb[0]
    tx = ML + (LW - tw) // 2
    ty = y1 + (bar_h - (bb[3]-bb[1])) // 2 - 2
    draw.text((tx, ty), txt, font=fnt["header"], fill=C["warm_white"])
    if piece_num:
        bx = x2 - 180
        by = y1 + 8
        bw, bh = 165, bar_h - 16
        draw.rounded_rectangle([bx, by, bx+bw, by+bh], radius=6, fill=C["gold"], outline=C["warm_black"], width=2)
        pb = draw.textbbox((0,0), f"PIECE #{piece_num}", font=fnt["badge"])
        draw.text((bx+(bw-(pb[2]-pb[0]))//2, by+6), f"PIECE #{piece_num}", font=fnt["badge"], fill=C["warm_black"])
        if piece_topic:
            sb = draw.textbbox((0,0), piece_topic, font=fnt["badge_sm"])
            draw.text((bx+(bw-(sb[2]-sb[0]))//2, by+30), piece_topic, font=fnt["badge_sm"], fill=C["warm_black"])
    return y1 + bar_h + 20

def draw_footer(draw, page_num):
    fy = H - MB + 20
    draw.line([(ML, fy), (W-MR, fy)], fill=C["veining"], width=2)
    fy += 10
    draw.text((ML, fy), "The Taj Mahal Mystery", font=fnt["caption"], fill=C["stone_grey"])
    pn = str(page_num)
    pb = draw.textbbox((0,0), pn, font=fnt["pgnum"])
    draw.text(((W-(pb[2]-pb[0]))//2, fy), pn, font=fnt["pgnum"], fill=C["stone_grey"])
    draw.text((W - MR - 80, fy), "Age 8-12", font=fnt["caption"], fill=C["stone_grey"])

def wrap_text(text, font, max_width, draw):
    words = text.split()
    lines = []
    current = ""
    for word in words:
        test = (current + " " + word).strip()
        bb = draw.textbbox((0,0), test, font=font)
        if bb[2]-bb[0] <= max_width:
            current = test
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines

def draw_text_block(draw, text, x, y, font, color, max_width, line_spacing=1.4):
    lines = wrap_text(text, font, max_width, draw)
    bb = draw.textbbox((0,0), "Ag", font=font)
    lh = int((bb[3]-bb[1]) * line_spacing)
    for line in lines:
        draw.text((x, y), line, font=font, fill=color)
        y += lh
    return y

def draw_vocab_box(draw, word, definition, x, y, width):
    pad = 20
    def_lines = wrap_text(definition, fnt["body_it"], width - 2*pad - 4, draw)
    bb_def = draw.textbbox((0,0), "Ag", font=fnt["body_it"])
    lh_def = int((bb_def[3]-bb_def[1]) * 1.4)
    bb_word = draw.textbbox((0,0), word, font=fnt["vocab_word"])
    strip_h = 36
    content_h = strip_h + 8 + (bb_word[3]-bb_word[1]) + 8 + len(def_lines)*lh_def + pad
    box_h = content_h + pad
    draw.rounded_rectangle([x, y, x+width, y+box_h], radius=12, fill=C["vocab_bg"], outline=C["gold"], width=2)
    draw.rounded_rectangle([x+2, y+2, x+width-2, y+2+strip_h], radius=10, fill=C["sandstone"])
    vb = draw.textbbox((0,0), "VOCABULARY", font=fnt["badge"])
    draw.text((x+(width-(vb[2]-vb[0]))//2, y+2+(strip_h-(vb[3]-vb[1]))//2), "VOCABULARY", font=fnt["badge"], fill=C["warm_white"])
    wy = y + strip_h + 14
    wb = draw.textbbox((0,0), word, font=fnt["vocab_word"])
    draw.text((x+(width-(wb[2]-wb[0]))//2, wy), word, font=fnt["vocab_word"], fill=C["indigo"])
    dy = wy + (wb[3]-wb[1]) + 8
    for line in def_lines:
        draw.text((x+pad, dy), line, font=fnt["body_it"], fill=C["charcoal"])
        dy += lh_def
    return y + box_h + 20

def draw_activity_zone(draw, title, x, y, width, height):
    draw.rounded_rectangle([x, y, x+width, y+height], radius=10, fill=C["act_bg"], outline=C["teal"], width=2)
    strip_h = 40
    draw.rounded_rectangle([x+2, y+2, x+width-2, y+2+strip_h], radius=8, fill=C["teal"])
    tb = draw.textbbox((0,0), title, font=fnt["act"])
    draw.text((x+(width-(tb[2]-tb[0]))//2, y+2+(strip_h-(tb[3]-tb[1]))//2), title, font=fnt["act"], fill=C["warm_white"])
    return x+20, y+strip_h+16

def draw_writing_lines(draw, x, y, width, count=2, spacing=45):
    for i in range(count):
        draw.line([(x, y+i*spacing), (x+width, y+i*spacing)], fill=C["veining"], width=1)
    return y + count*spacing + 10

def draw_drawing_box(draw, x, y, w, h, label=None):
    draw.rectangle([x, y, x+w, y+h], fill=C["warm_white"], outline=C["charcoal"], width=2)
    if label:
        lb = draw.textbbox((0,0), label, font=fnt["small_bold"])
        draw.text((x+(w-(lb[2]-lb[0]))//2, y+(h-(lb[3]-lb[1]))//2), label, font=fnt["small_bold"], fill=C["veining"])

def draw_fiction_badge(draw, text, x, y, badge_type="fic"):
    colours = {
        "fic":  (C["fic_bg"],  C["fic_text"]),
        "hist": (C["hist_bg"], C["hist_text"]),
        "adv":  (C["adv_bg"],  C["adv_text"]),
        "mod":  (C["mod_bg"],  C["mod_text"]),
    }
    bg, fg = colours.get(badge_type, (C["fic_bg"], C["fic_text"]))
    pad = 12
    bb = draw.textbbox((0,0), text, font=fnt["caption"])
    tw, th = bb[2]-bb[0], bb[3]-bb[1]
    draw.rounded_rectangle([x-pad, y-4, x+tw+pad, y+th+6], radius=8, fill=bg)
    draw.text((x, y), text, font=fnt["caption"], fill=fg)
    return y + th + 14

def draw_reward_box(draw, piece_num, topic, x, y, width):
    h = 100
    draw.rounded_rectangle([x, y, x+width, y+h], radius=8, fill=C["gold"], outline=C["indigo"], width=3)
    hx, hy = x+36, y+h//2
    draw.polygon([hx, hy-22, hx+19, hy-11, hx+19, hy+11, hx, hy+22, hx-19, hy+11, hx-19, hy-11], fill=C["indigo"])
    draw.text((hx-7, hy-10), "V", font=fnt["h3"], fill=C["gold"])
    t1 = f"YOU HAVE FOUND BLUEPRINT PIECE #{piece_num}!"
    t2 = f"Mark it off on Page 1:  Piece #{piece_num} -- {topic}  [CHECKED]"
    draw.text((x+65, y+18), t1, font=fnt["reward"], fill=C["warm_black"])
    draw.text((x+65, y+54), t2, font=fnt["reward_sm"], fill=C["warm_black"])
    return y + h + 20

def draw_checkbox_line(draw, x, y, text, font=None):
    if font is None:
        font = fnt["body"]
    box = 22
    draw.rectangle([x, y, x+box, y+box], outline=C["charcoal"], width=2, fill=C["warm_white"])
    draw.text((x+box+10, y+2), text, font=font, fill=C["charcoal"])
    bb = draw.textbbox((0,0), "A", font=font)
    return y + max(box, bb[3]-bb[1]) + 12

def place_image(page_img, img_path, x, y, w, h):
    if not img_path or not os.path.exists(img_path):
        draw = ImageDraw.Draw(page_img)
        draw.rectangle([x, y, x+w, y+h], fill=C["parchment"], outline=C["veining"], width=2)
        draw.text((x+10, y+10), "[Illustration]", font=fnt["caption"], fill=C["stone_grey"])
        return
    src = Image.open(img_path).convert("RGB")
    src = src.resize((w, h), Image.LANCZOS)
    page_img.paste(src, (x, y))

def draw_section_divider(draw, x, y, width):
    mid = x + width//2
    draw.line([(x, y), (mid-30, y)], fill=C["veining"], width=2)
    draw.ellipse([mid-8, y-4, mid+8, y+4], fill=C["gold"])
    draw.line([(mid+30, y), (x+width, y)], fill=C["veining"], width=2)
    return y + 16

def draw_fact_box(draw, text, x, y, width):
    pad = 16
    lines = wrap_text(text, fnt["body_it"], width-2*pad-6, draw)
    bb = draw.textbbox((0,0), "Ag", font=fnt["body_it"])
    lh = int((bb[3]-bb[1])*1.4)
    h = 2*pad + len(lines)*lh
    draw.rounded_rectangle([x, y, x+width, y+h], radius=8, fill=C["think_bg"])
    draw.rectangle([x, y, x+6, y+h], fill=C["yamuna"])
    dy = y + pad
    for line in lines:
        draw.text((x+20, dy), line, font=fnt["body_it"], fill=C["charcoal"])
        dy += lh
    return y + h + 16

def draw_think_box(draw, question, x, y, width, lines=2):
    pad = 16
    q_lines = wrap_text("Think: " + question, fnt["body_it"], width-2*pad, draw)
    bb = draw.textbbox((0,0), "Ag", font=fnt["body_it"])
    lh = int((bb[3]-bb[1])*1.4)
    h = 2*pad + len(q_lines)*lh + lines*50 + 10
    draw.rounded_rectangle([x, y, x+width, y+h], radius=8, fill=C["think_bg"])
    draw.rectangle([x, y, x+6, y+h], fill=C["yamuna"])
    dy = y + pad
    for line in q_lines:
        draw.text((x+20, dy), line, font=fnt["body_it"], fill=C["charcoal"])
        dy += lh
    dy += 8
    for i in range(lines):
        draw.line([(x+20, dy+i*46), (x+width-20, dy+i*46)], fill=C["veining"], width=1)
    return y + h + 16

def img_path(name):
    import glob
    matches = glob.glob(os.path.join(BRAIN, f"{name}_*.jpg"))
    if matches:
        return sorted(matches)[-1]
    return None

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 1
# ═══════════════════════════════════════════════════════════════════════════════
def make_page_01():
    img = new_page()
    draw = ImageDraw.Draw(img)
    draw_page_border(draw)
    y = draw_header_bar(draw, "THE MYSTERIOUS PORTFOLIO")

    ill_h = 760
    place_image(img, img_path("page01_portfolio_desk"), ML, y, LW, ill_h)
    draw = ImageDraw.Draw(img)
    draw_fiction_badge(draw, "[FICTIONAL ADVENTURE ELEMENT]", ML+10, y+ill_h-28, "fic")
    y += ill_h + 15

    y = draw_text_block(draw, "Something has arrived.", ML, y, fnt["body_bold"], C["charcoal"], LW)
    y += 4
    y = draw_text_block(draw, "On the desk in front of you is an old leather portfolio -- dusty, travel-worn, locked with a small brass key.", ML, y, fnt["body"], C["charcoal"], LW)
    y += 4
    y = draw_text_block(draw, "Inside, you find:", ML, y, fnt["body"], C["charcoal"], LW)
    y += 6
    items = [
        "  A blueprint of a famous monument -- but six sections are missing",
        "  A brass key, still warm from someone's pocket",
        "  A rolled map of a city by a great river",
        "  A magnifying glass with a cracked handle",
        "  A chip of white marble, smooth as glass",
        "  A folded note: \"The blueprint cannot be restored until you investigate. Six missing pieces. Six mysteries. Begin in Agra.\"",
    ]
    for item in items:
        y = draw_text_block(draw, item, ML+10, y, fnt["body"], C["charcoal"], LW-10)
        y += 3
    draw_fiction_badge(draw, "[FICTIONAL ADVENTURE NOTE]", ML+16, y, "fic")
    y += 28
    draw_section_divider(draw, ML, y, LW)
    y += 6

    act_x, act_y = draw_activity_zone(draw, "ACTIVITY: CREATE YOUR EXPLORER IDENTITY", ML, y, LW, 490)
    y = act_y
    draw.text((act_x, y), "Before you begin, introduce yourself.", font=fnt["body"], fill=C["charcoal"])
    y += 36
    draw.text((act_x, y), "Explorer Name:", font=fnt["body_bold"], fill=C["charcoal"])
    y += 30
    draw_writing_lines(draw, act_x+20, y, LW-60, 1, 44)
    y += 60
    col_w = (LW-60)//2
    draw.text((act_x, y), "Explorer Symbol (draw it here):", font=fnt["body_bold"], fill=C["charcoal"])
    draw.text((act_x+col_w+60, y), "Draw Yourself as an Explorer:", font=fnt["body_bold"], fill=C["charcoal"])
    y += 26
    draw_drawing_box(draw, act_x, y, col_w, 200)
    draw_drawing_box(draw, act_x+col_w+60, y, col_w, 200)
    y += 218

    draw_section_divider(draw, ML, y, LW)
    y += 6
    draw.text((ML, y), "WHAT YOU ARE LOOKING FOR", font=fnt["h2"], fill=C["indigo"])
    y += 38
    pieces = [
        ("PIECE #1", "AGRA & GEOGRAPHY",      C["yamuna"]),
        ("PIECE #2", "PEOPLE & PURPOSE",       C["sandstone"]),
        ("PIECE #3", "ARCHITECTURE",           C["indigo"]),
        ("PIECE #4", "ART & CRAFT",            C["emerald"]),
        ("PIECE #5", "GARDENS & ENGINEERING",  C["teal"]),
        ("PIECE #6", "EVIDENCE",               C["gold"]),
    ]
    pw = (LW-20)//2
    for i,(num,topic,colour) in enumerate(pieces):
        px = ML + (i%2)*pw
        py = y + (i//2)*50
        draw.rounded_rectangle([px, py, px+pw-10, py+40], radius=6, fill=C["warm_white"], outline=colour, width=2)
        draw.rectangle([px, py, px+36, py+40], fill=colour)
        draw.text((px+44, py+10), f"[ ]  {num} -- {topic}", font=fnt["small_bold"], fill=C["charcoal"])
    y += (len(pieces)//2)*50 + 12

    draw.text((ML, y), "THE BRASS KEY", font=fnt["h2"], fill=C["indigo"])
    y += 36
    y = draw_text_block(draw, "You hold the brass key in your hand. What do you think this key unlocks?", ML, y, fnt["body"], C["charcoal"], LW)
    y += 6
    draw_writing_lines(draw, ML+16, y, LW-16, 2, 44)
    y += 100
    y = draw_text_block(draw, "(Don't look ahead. You'll find out.)", ML+16, y, fnt["body_it"], C["stone_grey"], LW-16)
    y += 10
    y = draw_fact_box(draw, "Historians use clues from the past to investigate what happened. You are about to do exactly that.", ML, y, LW)
    bb = draw.textbbox((0,0), "Your adventure begins. Turn the page.", font=fnt["body_bold"])
    draw.text((ML+(LW-(bb[2]-bb[0]))//2, y), "Your adventure begins. Turn the page.", font=fnt["body_bold"], fill=C["indigo"])

    draw_footer(draw, 1)
    img.save(os.path.join(OUT, "page_01.png"), dpi=(DPI, DPI))
    print("page_01.png done")


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 2
# ═══════════════════════════════════════════════════════════════════════════════
def make_page_02():
    img = new_page()
    draw = ImageDraw.Draw(img)
    draw_page_border(draw)
    y = draw_header_bar(draw, "WELCOME TO AGRA", piece_num=1, piece_topic="AGRA & GEOGRAPHY")

    ill_h = 700
    place_image(img, img_path("page02_agra_panorama"), ML, y, LW, ill_h)
    draw = ImageDraw.Draw(img)
    draw_fiction_badge(draw, "HISTORICAL RECREATION -- Educational reconstruction based on historical context", ML+10, y+ill_h-28, "hist")
    y += ill_h + 12

    y = draw_text_block(draw, "The blueprint's first section shows a city by a river.", ML, y, fnt["body_it"], C["charcoal"], LW)
    y += 4
    y = draw_text_block(draw, "You study the map. A note reads: \"Find the city. Find the river. Find the monument.\"", ML, y, fnt["body_it"], C["charcoal"], LW)
    y += 10
    draw_section_divider(draw, ML, y, LW)
    y += 6
    draw.text((ML, y), "WHERE IS AGRA?", font=fnt["h2"], fill=C["indigo"])
    y += 40
    facts = [
        "Agra is a city in the northern part of India, in the state of Uttar Pradesh.",
        "In the 16th and 17th centuries, Agra was one of the most important cities of the Mughal Empire -- a powerful empire that ruled much of the Indian subcontinent.",
        "The city sits alongside a great river: the Yamuna.",
        "The Taj Mahal stands on the right bank of the Yamuna River.",
    ]
    for fact in facts:
        y = draw_text_block(draw, fact, ML, y, fnt["body"], C["charcoal"], LW)
        y += 6
    y = draw_fact_box(draw, "FACT: The Taj Mahal is not just a building -- it is a complex of gardens, gateways, and structures on a raised terrace above the river.", ML, y, LW)
    draw_section_divider(draw, ML, y, LW)
    y += 6

    act_x, act_y = draw_activity_zone(draw, "ACTIVITY: MAP INVESTIGATION", ML, y, LW, 590)
    y = act_y
    draw.text((act_x, y), "Look at the panorama above carefully. Find and circle each of these:", font=fnt["act"], fill=C["charcoal"])
    y += 36
    map_items = [
        "The city of Agra",
        "The Yamuna River",
        "The Taj Mahal complex",
        "The garden in front of the mausoleum",
        "A red sandstone building",
    ]
    col_w2 = (LW-40)//2
    for i,item in enumerate(map_items):
        ix = act_x + (i%2)*(col_w2+20)
        iy = y + (i//2)*44
        draw_checkbox_line(draw, ix, iy, item)
    y = act_y + 36 + ((len(map_items)+1)//2)*44 + 14
    draw.text((act_x, y), "OBSERVATION CHALLENGE -- Can you also spot:", font=fnt["body_bold"], fill=C["charcoal"])
    y += 32
    obs_items = [
        "A garden with straight pathways",
        "The river",
        "A red sandstone building",
        "A market area",
        "A cart on a road",
        "The hidden brass key symbol",
    ]
    for item in obs_items:
        y = draw_checkbox_line(draw, act_x, y, item)
    y += 6
    draw.text((act_x, y), "(Tick each one when you find it)", font=fnt["body_it"], fill=C["stone_grey"])
    y += 32
    draw_reward_box(draw, 1, "AGRA & GEOGRAPHY", ML, y, LW)

    draw_footer(draw, 2)
    img.save(os.path.join(OUT, "page_02.png"), dpi=(DPI, DPI))
    print("page_02.png done")


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 3
# ═══════════════════════════════════════════════════════════════════════════════
def make_page_03():
    img = new_page()
    draw = ImageDraw.Draw(img)
    draw_page_border(draw)
    y = draw_header_bar(draw, "MEET SHAH JAHAN", piece_num=2, piece_topic="PEOPLE & PURPOSE")

    ill_w = 640
    ill_h = 800
    place_image(img, img_path("page03_shah_jahan_portrait"), ML, y, ill_w, ill_h)
    draw = ImageDraw.Draw(img)
    draw_fiction_badge(draw, "HISTORICAL RECREATION -- Portrait in Mughal artistic style", ML+8, y+ill_h-28, "hist")

    rx = ML + ill_w + 40
    rw = LW - ill_w - 40
    ry = y + 8

    draw.text((rx, ry), "STORY", font=fnt["h2"], fill=C["sandstone"])
    ry += 40
    ry = draw_text_block(draw, "The blueprint's second section shows a timeline. But the dates have been shuffled.", rx, ry, fnt["body_it"], C["charcoal"], rw)
    ry += 8
    ry = draw_text_block(draw, '"Put the events in the correct order," reads a note. "Chronology is the historian\'s first tool."', rx, ry, fnt["body_it"], C["charcoal"], rw)
    ry += 16
    ry = draw_vocab_box(draw, "CHRONOLOGY", "Putting events in the order they happened. Historians ask: When? What came before? What came after?", rx, ry, rw)

    draw.text((rx, ry), "THE VERIFIED TIMELINE", font=fnt["h3"], fill=C["indigo"])
    ry += 34
    timeline = [
        ("1628", "Shah Jahan becomes Mughal emperor"),
        ("1631", "Mumtaz Mahal dies"),
        ("1632", "Construction of the Taj Mahal begins"),
        ("1648", "The principal mausoleum is completed"),
        ("1653", "Mosque, gateway & outer buildings completed"),
    ]
    for year, event in timeline:
        draw.rounded_rectangle([rx, ry, rx+86, ry+30], radius=5, fill=C["indigo"])
        yb = draw.textbbox((0,0), year, font=fnt["small_bold"])
        draw.text((rx+(86-(yb[2]-yb[0]))//2, ry+5), year, font=fnt["small_bold"], fill=C["warm_white"])
        ev_lines = wrap_text(event, fnt["small"], rw-100, draw)
        ebb = draw.textbbox((0,0), "Ag", font=fnt["small"])
        for ei, el in enumerate(ev_lines):
            draw.text((rx+98, ry+4+ei*(ebb[3]-ebb[1]+3)), el, font=fnt["small"], fill=C["charcoal"])
        ry += max(34, len(ev_lines)*(ebb[3]-ebb[1]+3)+8)
        if year != "1653":
            draw.line([(rx+42, ry), (rx+42, ry+12)], fill=C["indigo"], width=2)
            draw.polygon([(rx+38, ry+12), (rx+42, ry+18), (rx+46, ry+12)], fill=C["indigo"])
            ry += 22

    ry += 6
    ry = draw_fact_box(draw, "HISTORIAN'S NOTE: The mausoleum was completed in 1648. The outlying buildings -- mosque, gateway, guest house -- were completed by 1653. A large project like this was built in stages.", rx, ry, rw)

    y = y + ill_h + 18
    draw_section_divider(draw, ML, y, LW)
    y += 8

    act_x, act_y = draw_activity_zone(draw, "ACTIVITY: PUT THE TIMELINE IN ORDER", ML, y, LW, 490)
    y = act_y
    draw.text((act_x, y), "The five events below have been mixed up. Write 1-5 in the boxes to put them in the correct chronological order:", font=fnt["act"], fill=C["charcoal"])
    y += 44

    scrambled = [
        "Construction of the Taj Mahal begins",
        "Shah Jahan becomes Mughal emperor",
        "The mosque, gateway, and outer buildings are completed",
        "Mumtaz Mahal dies",
        "The principal mausoleum is completed",
    ]
    row_h = 54
    for i, event in enumerate(scrambled):
        ey = y + i*row_h
        draw.rounded_rectangle([act_x, ey, act_x+LW-40, ey+row_h-6], radius=6, fill=C["warm_white"], outline=C["veining"], width=1)
        # Number box at right
        nbx = act_x+LW-40-70
        draw.rectangle([nbx, ey+2, nbx+66, ey+row_h-8], fill=C["parchment"], outline=C["veining"], width=1)
        draw.text((nbx+16, ey+14), "___", font=fnt["body_bold"], fill=C["veining"])
        draw.text((act_x+14, ey+14), event, font=fnt["body"], fill=C["charcoal"])
    y += len(scrambled)*row_h + 10
    draw.text((act_x, y), "(Correct order: 2  1  3  4  5 -- verified against historical records)", font=fnt["small"], fill=C["stone_grey"])
    y += 36
    draw_reward_box(draw, 2, "PEOPLE & PURPOSE", ML, y, LW)

    draw_footer(draw, 3)
    img.save(os.path.join(OUT, "page_03.png"), dpi=(DPI, DPI))
    print("page_03.png done")


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 4
# ═══════════════════════════════════════════════════════════════════════════════
def make_page_04():
    img = new_page()
    draw = ImageDraw.Draw(img)
    draw_page_border(draw)
    y = draw_header_bar(draw, "WHY WAS THE TAJ MAHAL BUILT?")

    ill_h = 660
    place_image(img, img_path("page04_memorial_scene"), ML, y, LW, ill_h)
    draw = ImageDraw.Draw(img)
    draw_fiction_badge(draw, "HISTORICAL RECREATION", ML+10, y+ill_h-28, "hist")
    y += ill_h + 14

    y = draw_text_block(draw, "Every building has a reason. The explorer's portfolio contains a question card:", ML, y, fnt["body_it"], C["charcoal"], LW)
    y += 6
    y = draw_fact_box(draw, '"Why was this monument built? What does it commemorate?"', ML, y, LW)

    draw.text((ML, y), "THE PURPOSE OF THE MONUMENT", font=fnt["h2"], fill=C["indigo"])
    y += 40
    paras = [
        "Shah Jahan was the Mughal emperor from 1628 to 1658.",
        "His wife, Mumtaz Mahal, died in 1631.",
        "Shah Jahan commissioned the Taj Mahal as a mausoleum -- a building made as a tomb and memorial -- in her memory.",
        "After Shah Jahan died, he was also buried there.",
    ]
    for para in paras:
        y = draw_text_block(draw, para, ML, y, fnt["body"], C["charcoal"], LW)
        y += 10

    y = draw_vocab_box(draw, "MAUSOLEUM", "A building made as a tomb or memorial for one or more people.", ML, y, LW)
    y = draw_fact_box(draw, "THE BIG IDEA: A monument can preserve memory. The Taj Mahal has stood for nearly 400 years -- and people from all over the world still visit it today.", ML, y, LW)
    draw_section_divider(draw, ML, y, LW)
    y += 8

    act_x, act_y = draw_activity_zone(draw, "ACTIVITY: DESIGN A MEMORIAL SYMBOL", ML, y, LW, 680)
    y = act_y
    y = draw_text_block(draw, "If you wanted to design a symbol for a memorial -- something to represent remembrance -- what would it look like?", act_x, y, fnt["act"], C["charcoal"], LW-40)
    y += 14
    draw.text((act_x, y), "Choose ideas to include:", font=fnt["body_bold"], fill=C["charcoal"])
    y += 32
    ideas = ["  Remembrance", "  Peace", "  Honour", "  Beauty", "  Memory", "  Strength"]
    col_w3 = (LW-40)//3
    for i,idea in enumerate(ideas):
        ix = act_x + (i%3)*col_w3
        iy = y + (i//3)*44
        draw_checkbox_line(draw, ix, iy, idea)
    y += (len(ideas)//3)*44 + 12
    draw.text((act_x, y), "Your own idea:", font=fnt["body_bold"], fill=C["charcoal"])
    draw_writing_lines(draw, act_x+148, y+8, 400, 1, 40)
    y += 56
    draw.text((act_x, y), "Now design your memorial symbol inside this medallion:", font=fnt["body_bold"], fill=C["charcoal"])
    y += 30
    cx = ML + LW//2
    cr = 175
    draw.ellipse([cx-cr, y, cx+cr, y+2*cr], fill=C["warm_white"], outline=C["gold"], width=4)
    draw.ellipse([cx-cr+14, y+14, cx+cr-14, y+2*cr-14], outline=C["veining"], width=1)
    draw.ellipse([cx-cr+26, y+26, cx+cr-26, y+2*cr-26], outline=C["veining"], width=1)
    draw.text((cx-90, y+cr-14), "Draw your symbol here", font=fnt["small"], fill=C["veining"])
    y += 2*cr + 14
    draw.text((act_x, y), "What does your symbol mean?", font=fnt["body_bold"], fill=C["charcoal"])
    y += 30
    draw_writing_lines(draw, act_x, y, LW-40, 2, 44)

    draw_footer(draw, 4)
    img.save(os.path.join(OUT, "page_04.png"), dpi=(DPI, DPI))
    print("page_04.png done")


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 5
# ═══════════════════════════════════════════════════════════════════════════════
def make_page_05():
    img = new_page()
    draw = ImageDraw.Draw(img)
    draw_page_border(draw)
    y = draw_header_bar(draw, "THE ARCHITECT'S TABLE")

    ill_h = 680
    place_image(img, img_path("page05_architect_table"), ML, y, LW, ill_h)
    draw = ImageDraw.Draw(img)
    draw_fiction_badge(draw, "ADVENTURE RECREATION -- Fictional workshop scene", ML+10, y+ill_h-28, "adv")
    y += ill_h + 14

    y = draw_text_block(draw, "On the adventure table, a detailed plan is pinned flat. Parts of the complex are labelled with blank tags. The explorer needs to match each component to its correct description.", ML, y, fnt["body_it"], C["charcoal"], LW)
    y += 12
    draw_section_divider(draw, ML, y, LW)
    y += 6
    draw.text((ML, y), "THE TAJ MAHAL IS A COMPLEX", font=fnt["h2"], fill=C["indigo"])
    y += 40
    y = draw_text_block(draw, "The Taj Mahal is a complex -- a group of connected buildings, gardens, and spaces that all work together. Here are the main components:", ML, y, fnt["body"], C["charcoal"], LW)
    y += 12

    components = [
        ("The Mausoleum",    "The central white marble building -- the tomb itself",           C["indigo"]),
        ("The Dome",         "The large curved dome at the top of the mausoleum",              C["indigo"]),
        ("The Minarets",     "Four tall slender towers -- one at each corner of the platform", C["indigo"]),
        ("The Platform",     "The raised white marble terrace the mausoleum stands on",        C["stone_grey"]),
        ("The Mosque",       "A place of worship on the western side -- red sandstone",        C["sandstone"]),
        ("The Jawab",        "A mirror building on the eastern side -- balances the mosque",   C["sandstone"]),
        ("The Great Gateway","The tall red sandstone entrance gate to the complex",             C["sandstone"]),
        ("The Garden",       "A large four-part garden between the gateway and mausoleum",     C["emerald"]),
    ]
    row_h5 = 46
    for i,(name,desc,colour) in enumerate(components):
        ry2 = y + i*row_h5
        alt_bg = C["warm_white"] if i%2==0 else C["parchment"]
        draw.rectangle([ML, ry2, ML+LW, ry2+row_h5-4], fill=alt_bg)
        draw.rectangle([ML, ry2, ML+190, ry2+row_h5-4], fill=colour)
        nb = draw.textbbox((0,0), name, font=fnt["small_bold"])
        draw.text((ML+(190-(nb[2]-nb[0]))//2, ry2+(row_h5-4-(nb[3]-nb[1]))//2), name, font=fnt["small_bold"], fill=C["warm_white"])
        draw.text((ML+198, ry2+(row_h5-4-24)//2+3), desc, font=fnt["small"], fill=C["charcoal"])
    y += len(components)*row_h5 + 14

    draw_section_divider(draw, ML, y, LW)
    y += 6

    act_x, act_y = draw_activity_zone(draw, "ACTIVITY: MATCH THE PART", ML, y, LW, 440)
    y = act_y
    draw.text((act_x, y), "Draw a line to connect each component name on the left to its correct description on the right:", font=fnt["act"], fill=C["charcoal"])
    y += 40
    left_terms  = ["Mausoleum", "Mosque", "Jawab", "Great Gateway", "Garden"]
    right_descs = ["The central white marble tomb building",
                   "A place of worship on the western side",
                   "A mirror building on the eastern side",
                   "The entrance gate to the complex",
                   "The four-part garden"]
    # Shuffle right column (scrambled order for activity)
    right_shuffled5 = ["The entrance gate to the complex",
                       "The central white marble tomb building",
                       "The four-part garden",
                       "A place of worship on the western side",
                       "A mirror building on the eastern side"]
    col_w5 = (LW-40-30)//2
    row_h5b = 54
    for i,(lt,rd) in enumerate(zip(left_terms, right_shuffled5)):
        ly5 = y + i*row_h5b
        draw.rounded_rectangle([act_x, ly5, act_x+col_w5, ly5+row_h5b-8], radius=5, fill=C["warm_white"], outline=C["teal"], width=2)
        lb5 = draw.textbbox((0,0), lt, font=fnt["body_bold"])
        draw.text((act_x+(col_w5-(lb5[2]-lb5[0]))//2, ly5+(row_h5b-8-(lb5[3]-lb5[1]))//2), lt, font=fnt["body_bold"], fill=C["indigo"])
        rx5 = act_x+col_w5+30
        rd_lns5 = wrap_text(rd, fnt["body"], col_w5-16, draw)
        rbb5 = draw.textbbox((0,0), "Ag", font=fnt["body"])
        rh5 = len(rd_lns5)*(rbb5[3]-rbb5[1]+3)
        draw.rounded_rectangle([rx5, ly5, rx5+col_w5, ly5+row_h5b-8], radius=5, fill=C["warm_white"], outline=C["veining"], width=1)
        dy5 = ly5+(row_h5b-8-rh5)//2
        for line in rd_lns5:
            draw.text((rx5+8, dy5), line, font=fnt["body"], fill=C["charcoal"])
            dy5 += rbb5[3]-rbb5[1]+3
    y += len(left_terms)*row_h5b + 14
    draw.text((act_x, y), "Answer key: Mausoleum=Central tomb  Mosque=Western worship  Jawab=Eastern mirror  Gateway=Entrance  Garden=Four-part garden", font=fnt["small"], fill=C["stone_grey"])

    draw_footer(draw, 5)
    img.save(os.path.join(OUT, "page_05.png"), dpi=(DPI, DPI))
    print("page_05.png done")


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 6
# ═══════════════════════════════════════════════════════════════════════════════
def make_page_06():
    img = new_page()
    draw = ImageDraw.Draw(img)
    draw_page_border(draw)
    y = draw_header_bar(draw, "REBUILD THE SYMMETRY", piece_num=3, piece_topic="ARCHITECTURE")

    y = draw_text_block(draw, "The blueprint piece for architecture is only half there. The other half is missing. The explorer must complete it.", ML, y, fnt["body_it"], C["charcoal"], LW)
    y += 6
    y = draw_fact_box(draw, '"The missing half is the same as the half you can see," the portfolio note says. "Study the left side carefully. Then rebuild the right."', ML, y, LW)
    y = draw_vocab_box(draw, "SYMMETRY", "Symmetry means that one half of a design mirrors the other half exactly. If you fold a symmetrical design down the middle, both halves match.", ML, y, LW)

    draw.text((ML, y), "SYMMETRY IN THE TAJ MAHAL", font=fnt["h2"], fill=C["indigo"])
    y += 40
    points6 = [
        "The Taj Mahal complex is designed with strong bilateral symmetry -- symmetry across a central axis.",
        "If you drew an imaginary line down the centre of the building, the left side and the right side would match.",
        "The four minarets are placed symmetrically -- two on each side.",
        "Even the mosque on the west and the jawab on the east are mirror buildings of each other.",
        "Symmetry gives buildings a sense of balance, order, and calm.",
    ]
    for pt in points6:
        y = draw_text_block(draw, "  " + pt, ML+10, y, fnt["body"], C["charcoal"], LW-10)
        y += 5
    y += 8
    draw_section_divider(draw, ML, y, LW)
    y += 8
    draw.text((ML, y), "ACTIVITY: COMPLETE THE OTHER HALF", font=fnt["h2"], fill=C["teal"])
    y += 40
    y = draw_text_block(draw, "The left half of the mausoleum's front elevation is shown below. Study it carefully. Then draw the right half to complete the symmetrical design. Use the central axis line as your guide.", ML, y, fnt["act"], C["charcoal"], LW)
    y += 20

    # Diagram zone
    diag_h = H - y - MB - 180
    diag_h = max(diag_h, 500)
    half_w = LW // 2
    # Left half: blueprint illustration
    ill_path6 = img_path("page06_symmetry_diagram")
    if ill_path6 and os.path.exists(ill_path6):
        src6 = Image.open(ill_path6).convert("RGB")
        iw6, ih6 = src6.size
        left_half6 = src6.crop((0, 0, iw6//2, ih6))
        left_half6 = left_half6.resize((half_w-2, diag_h-2), Image.LANCZOS)
        img.paste(left_half6, (ML+1, y+1))
    else:
        draw.rectangle([ML, y, ML+half_w, y+diag_h], fill=C["hist_bg"], outline=C["veining"], width=1)
    draw = ImageDraw.Draw(img)
    # Right half: blank
    draw.rectangle([ML+half_w, y, ML+LW, y+diag_h], fill=C["warm_white"], outline=C["charcoal"], width=2)
    dot_sp = 60
    for gx in range(ML+half_w+dot_sp, ML+LW, dot_sp):
        for gy in range(y+dot_sp, y+diag_h, dot_sp):
            draw.ellipse([gx-3, gy-3, gx+3, gy+3], fill=C["stone_grey"])
    lb6 = "COMPLETE THIS HALF"
    lbb6 = draw.textbbox((0,0), lb6, font=fnt["body_bold"])
    draw.text((ML+half_w+(half_w-(lbb6[2]-lbb6[0]))//2, y+diag_h//2-14), lb6, font=fnt["body_bold"], fill=C["veining"])
    # Axis line
    for dy6 in range(y, y+diag_h, 16):
        draw.line([(ML+half_w, dy6), (ML+half_w, min(dy6+10, y+diag_h))], fill=C["sandstone"], width=3)
    y += diag_h + 14

    draw.text((ML, y), "What shapes do you see on the left half?", font=fnt["body_bold"], fill=C["charcoal"])
    y += 30
    draw_writing_lines(draw, ML, y, LW, 2, 44)
    y += 102
    draw_reward_box(draw, 3, "ARCHITECTURE", ML, y, LW)

    draw_footer(draw, 6)
    img.save(os.path.join(OUT, "page_06.png"), dpi=(DPI, DPI))
    print("page_06.png done")


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 7
# ═══════════════════════════════════════════════════════════════════════════════
def make_page_07():
    img = new_page()
    draw = ImageDraw.Draw(img)
    draw_page_border(draw)
    y = draw_header_bar(draw, "THE FOUR MINARETS")

    y = draw_text_block(draw, "A second blueprint fragment shows the platform from above -- but something is wrong. One minaret marker is in the wrong place.", ML, y, fnt["body_it"], C["charcoal"], LW)
    y += 6
    y = draw_fact_box(draw, '"A building this precise would never have an error like this," reads the portfolio note. "Can you find it?"', ML, y, LW)

    draw.text((ML, y), "THE FOUR MINARETS", font=fnt["h2"], fill=C["indigo"])
    y += 40
    paras7 = [
        "The Taj Mahal mausoleum stands on a large raised platform. At each of the four corners of this platform stands a tall, slender tower called a minaret.",
        "The four minarets are placed symmetrically -- one at each corner, the same distance from the mausoleum on every side.",
        "This arrangement creates a strong sense of balance when you look at the mausoleum from any direction.",
    ]
    for p in paras7:
        y = draw_text_block(draw, p, ML, y, fnt["body"], C["charcoal"], LW)
        y += 8
    y = draw_fact_box(draw, "NOTE: Historians have not documented a single specific purpose for the minarets in the original construction records. What is clear from the structure itself is that they frame the mausoleum and contribute to the balanced composition.", ML, y, LW)
    draw_section_divider(draw, ML, y, LW)
    y += 8

    act_x7, act_y7 = draw_activity_zone(draw, "ACTIVITY: FIND THE MISPLACED MINARET", ML, y, LW, 1000)
    y = act_y7

    draw.text((act_x7, y), "The diagram below shows the mausoleum platform from above.", font=fnt["act"], fill=C["charcoal"])
    y += 32
    draw.text((act_x7, y), "Four minarets should be placed -- one at each CORNER. But one minaret marker is in the WRONG position.", font=fnt["act"], fill=C["charcoal"])
    y += 32
    draw.text((act_x7, y), "Circle the minaret that is in the wrong place:", font=fnt["body_bold"], fill=C["sandstone"])
    y += 42

    # Platform diagram
    plat_w, plat_h7 = 800, 540
    px0 = ML + (LW-plat_w)//2
    py0 = y

    draw.rectangle([px0, py0, px0+plat_w, py0+plat_h7], fill=C["parchment"], outline=C["indigo"], width=3)
    # Mausoleum centre
    mx7, my7 = px0+plat_w//2, py0+plat_h7//2
    ms7 = 95
    draw.rectangle([mx7-ms7, my7-ms7, mx7+ms7, my7+ms7], fill=(245,242,236), outline=C["indigo"], width=2)
    draw.ellipse([mx7-26, my7-26, mx7+26, my7+26], fill=C["stone_grey"], outline=C["indigo"], width=2)
    mb7 = draw.textbbox((0,0), "Mausoleum", font=fnt["small"])
    draw.text((mx7-(mb7[2]-mb7[0])//2, my7+30), "Mausoleum", font=fnt["small"], fill=C["charcoal"])

    mr7 = 34
    # Three correct minarets (top-left, top-right, bottom-left)
    correct_pos = [
        (px0+58, py0+56),
        (px0+plat_w-58, py0+56),
        (px0+58, py0+plat_h7-56),
    ]
    for (mx2, my2) in correct_pos:
        draw.ellipse([mx2-mr7, my2-mr7, mx2+mr7, my2+mr7], fill=C["indigo"], outline=C["warm_black"], width=2)
        mb = draw.textbbox((0,0), "M", font=fnt["small_bold"])
        draw.text((mx2-(mb[2]-mb[0])//2, my2-(mb[3]-mb[1])//2), "M", font=fnt["small_bold"], fill=C["warm_white"])

    # WRONG minaret: middle of bottom edge
    wx7, wy7 = px0+plat_w//2, py0+plat_h7-44
    draw.ellipse([wx7-mr7, wy7-mr7, wx7+mr7, wy7+mr7], fill=C["sandstone"], outline=C["warm_black"], width=3)
    mb = draw.textbbox((0,0), "M", font=fnt["small_bold"])
    draw.text((wx7-(mb[2]-mb[0])//2, wy7-(mb[3]-mb[1])//2), "M", font=fnt["small_bold"], fill=C["warm_white"])
    # Label it as wrong
    draw.text((wx7-28, wy7+mr7+4), "?", font=fnt["h2"], fill=C["sandstone"])

    # Empty bottom-right (where it should be) -- dashed circle
    bx7, by7 = px0+plat_w-58, py0+plat_h7-56
    for angle7 in range(0, 360, 18):
        a1 = math.radians(angle7)
        a2 = math.radians(angle7+9)
        draw.line([(bx7+(mr7+6)*math.cos(a1), by7+(mr7+6)*math.sin(a1)),
                   (bx7+(mr7+6)*math.cos(a2), by7+(mr7+6)*math.sin(a2))],
                  fill=C["stone_grey"], width=2)
    draw.text((bx7-28, by7-14), "?", font=fnt["h3"], fill=C["stone_grey"])

    # Legend
    draw.text((px0, py0+plat_h7+10), "M = Minaret position    Filled circle = placed    Dashed circle = empty corner    Orange = misplaced", font=fnt["small"], fill=C["stone_grey"])

    y = py0 + plat_h7 + 46

    draw.text((act_x7, y), "Where should the misplaced minaret actually be?", font=fnt["body_bold"], fill=C["charcoal"])
    y += 32
    draw_writing_lines(draw, act_x7, y, LW-40, 1, 44)
    y += 58
    y = draw_think_box(draw, "Why do you think placing the minarets at the corners (rather than the middle of the sides) creates a more balanced look?", act_x7, y, LW-40, lines=2)

    draw_footer(draw, 7)
    img.save(os.path.join(OUT, "page_07.png"), dpi=(DPI, DPI))
    print("page_07.png done")


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 8
# ═══════════════════════════════════════════════════════════════════════════════
def make_page_08():
    img = new_page()
    draw = ImageDraw.Draw(img)
    draw_page_border(draw)
    y = draw_header_bar(draw, "THE DOME CHALLENGE")

    y = draw_text_block(draw, "The explorer finds a set of dome sketches in the portfolio. Some are marked STABLE. Some are marked UNSTABLE. But the labels have been removed.", ML, y, fnt["body_it"], C["charcoal"], LW)
    y += 6
    y = draw_fact_box(draw, '"Engineers must think about weight," the note says. "Which structures can stand?"', ML, y, LW)

    draw.text((ML, y), "HOW DOES A DOME STAY UP?", font=fnt["h2"], fill=C["indigo"])
    y += 40
    y = draw_text_block(draw, "The Taj Mahal's most famous feature is its large central dome. A dome is a curved structure that covers a large space without needing a column in the middle to hold it up.", ML, y, fnt["body"], C["charcoal"], LW)
    y += 10
    draw.text((ML, y), "For a dome to stay up, the building beneath it must:", font=fnt["body_bold"], fill=C["charcoal"])
    y += 34
    pts8 = [
        ("OK ", C["teal"],      "Have a wide, stable base to spread the weight"),
        ("OK ", C["teal"],      "Use arches that direct weight downward and outward"),
        ("OK ", C["teal"],      "Be balanced -- weight distributed evenly on all sides"),
        ("NO ", C["sandstone"], "A very narrow base cannot support a heavy dome"),
        ("NO ", C["sandstone"], "A lopsided structure will lean or fail"),
    ]
    for icon, col, text in pts8:
        draw.rounded_rectangle([ML, y, ML+46, y+30], radius=5, fill=col)
        draw.text((ML+6, y+5), icon, font=fnt["small_bold"], fill=C["warm_white"])
        draw.text((ML+54, y+5), text, font=fnt["body"], fill=C["charcoal"])
        y += 36
    y += 8
    draw_fiction_badge(draw, "MODERN ACTIVITY INSPIRED BY HISTORICAL ARCHITECTURE -- Not a reconstruction of the Taj Mahal's exact construction process.", ML, y, "mod")
    y += 36
    draw_section_divider(draw, ML, y, LW)
    y += 10

    act_x8, act_y8 = draw_activity_zone(draw, "ACTIVITY: STABLE OR UNSTABLE?", ML, y, LW, 1140)
    y = act_y8

    draw.text((act_x8, y), "Look at the four structures. Write STABLE or UNSTABLE under each one:", font=fnt["act"], fill=C["charcoal"])
    y += 42

    cell_w8 = (LW-40-30)//2
    cell_h8 = 380
    structures8 = [
        ("A", "Wide base, large arch, dome centred\n(Answer: STABLE)", True),
        ("B", "Narrow base, dome off-centre\n(Answer: UNSTABLE)", False),
        ("C", "Wide base, dome supported by arches\n(Answer: STABLE)", True),
        ("D", "Base narrower at bottom than top\n(Answer: UNSTABLE)", False),
    ]
    for i,(label8,desc8,stable8) in enumerate(structures8):
        cx8 = act_x8 + (i%2)*(cell_w8+30)
        cy8 = y + (i//2)*(cell_h8+16)
        draw.rectangle([cx8, cy8, cx8+cell_w8, cy8+cell_h8], fill=C["warm_white"], outline=C["veining"], width=1)
        draw.text((cx8+10, cy8+10), label8, font=fnt["h3"], fill=C["indigo"])
        mid8 = cx8 + cell_w8//2
        base_y8 = cy8 + cell_h8 - 90

        if label8 == "A":
            bw8 = int(cell_w8*0.7)
            draw.rectangle([mid8-bw8//2, base_y8, mid8+bw8//2, base_y8+44], fill=C["parchment"], outline=C["charcoal"], width=2)
            aw8 = bw8//3
            draw.arc([mid8-aw8, base_y8-aw8*2, mid8+aw8, base_y8], 180, 0, fill=C["indigo"], width=3)
            draw.line([(mid8-aw8, base_y8-aw8*2), (mid8-aw8, base_y8)], fill=C["indigo"], width=3)
            draw.line([(mid8+aw8, base_y8-aw8*2), (mid8+aw8, base_y8)], fill=C["indigo"], width=3)
            dr8 = 42
            draw.arc([mid8-dr8, base_y8-aw8*2-dr8*2, mid8+dr8, base_y8-aw8*2], 180, 0, fill=C["stone_grey"], width=3)
        elif label8 == "B":
            bw8 = int(cell_w8*0.25)
            sh8 = 35
            draw.rectangle([mid8-bw8//2+sh8, base_y8, mid8+bw8//2+sh8, base_y8+44], fill=C["parchment"], outline=C["charcoal"], width=2)
            aw8 = bw8//2+4
            draw.arc([mid8-aw8+sh8, base_y8-aw8*2, mid8+aw8+sh8, base_y8], 180, 0, fill=C["indigo"], width=3)
            draw.line([(mid8-aw8+sh8, base_y8-aw8*2), (mid8-aw8+sh8, base_y8)], fill=C["indigo"], width=3)
            draw.line([(mid8+aw8+sh8, base_y8-aw8*2), (mid8+aw8+sh8, base_y8)], fill=C["indigo"], width=3)
            dr8 = 42
            draw.arc([mid8-dr8+sh8+20, base_y8-aw8*2-dr8*2, mid8+dr8+sh8+20, base_y8-aw8*2], 180, 0, fill=C["sandstone"], width=3)
            draw.line([(mid8+bw8//2+sh8, base_y8+24), (mid8+bw8//2+sh8+28, base_y8+50)], fill=C["sandstone"], width=3)
        elif label8 == "C":
            bw8 = int(cell_w8*0.7)
            draw.rectangle([mid8-bw8//2, base_y8, mid8+bw8//2, base_y8+44], fill=C["parchment"], outline=C["charcoal"], width=2)
            draw.rectangle([mid8-bw8//3, base_y8-100, mid8-bw8//3+14, base_y8], fill=C["indigo"])
            draw.rectangle([mid8+bw8//3-14, base_y8-100, mid8+bw8//3, base_y8], fill=C["indigo"])
            draw.arc([mid8-bw8//3+14, base_y8-70, mid8+bw8//3-14, base_y8], 180, 0, fill=C["teal"], width=2)
            dr8 = 46
            draw.arc([mid8-dr8, base_y8-100-dr8*2, mid8+dr8, base_y8-100], 180, 0, fill=C["stone_grey"], width=3)
        elif label8 == "D":
            bw_top8 = int(cell_w8*0.7)
            bw_bot8 = int(cell_w8*0.22)
            pts8d = [(mid8-bw_top8//2, base_y8), (mid8+bw_top8//2, base_y8),
                     (mid8+bw_bot8//2, base_y8+44), (mid8-bw_bot8//2, base_y8+44)]
            draw.polygon(pts8d, fill=C["parchment"], outline=C["charcoal"])
            dr8 = 46
            draw.arc([mid8-dr8, base_y8-dr8*2, mid8+dr8, base_y8], 180, 0, fill=C["sandstone"], width=3)
            draw.line([(mid8, base_y8+50), (mid8, base_y8+68)], fill=C["sandstone"], width=3)
            draw.polygon([(mid8-10, base_y8+63), (mid8+10, base_y8+63), (mid8, base_y8+78)], fill=C["sandstone"])

        # Description
        for li8, dl8 in enumerate(desc8.split('\n')):
            draw.text((cx8+10, cy8+cell_h8-72+li8*24), dl8.strip(), font=fnt["small"], fill=C["charcoal"])
        # Answer blank
        draw.line([(cx8+10, cy8+cell_h8-18), (cx8+cell_w8-10, cy8+cell_h8-18)], fill=C["veining"], width=1)
        draw.text((cx8+10, cy8+cell_h8-40), "Write STABLE or UNSTABLE:", font=fnt["small_bold"], fill=C["stone_grey"])

    y += 2*(cell_h8+16) + 14
    y = draw_think_box(draw, "If you were designing a building to last for hundreds of years, what would you make sure the base was like?", act_x8, y, LW-40, lines=2)

    draw_footer(draw, 8)
    img.save(os.path.join(OUT, "page_08.png"), dpi=(DPI, DPI))
    print("page_08.png done")


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 9
# ═══════════════════════════════════════════════════════════════════════════════
def make_page_09():
    img = new_page()
    draw = ImageDraw.Draw(img)
    draw_page_border(draw)
    y = draw_header_bar(draw, "THE MARBLE MISSION")

    # Materials display illustration (programmatic)
    ill_h9 = 480
    ill_bg9 = Image.new("RGB", (LW, ill_h9), (196, 176, 140))
    ill_draw9 = ImageDraw.Draw(ill_bg9)
    # White marble slab
    ill_draw9.rectangle([30, 50, 360, 320], fill=C["warm_white"], outline=C["stone_grey"], width=3)
    for vx in range(60, 360, 45):
        ill_draw9.line([(vx, 50), (vx+18, 320)], fill=C["veining"], width=1)
    for hy in range(70, 320, 60):
        ill_draw9.line([(30, hy), (360, hy)], fill=C["veining"], width=1)
    ill_draw9.text((50, 330), "WHITE MARBLE", font=fnt["small_bold"], fill=C["charcoal"])
    ill_draw9.text((50, 355), "Makrana, Rajasthan", font=fnt["small"], fill=C["stone_grey"])
    # Red sandstone block
    ill_draw9.rectangle([410, 50, 740, 320], fill=C["sandstone"], outline=C["warm_black"], width=3)
    for rx9 in range(440, 740, 55):
        ill_draw9.line([(rx9, 50), (rx9, 320)], fill=(155, 55, 35), width=1)
    for ry9 in range(80, 320, 50):
        ill_draw9.line([(410, ry9), (740, ry9)], fill=(155, 55, 35), width=1)
    ill_draw9.text((440, 330), "RED SANDSTONE", font=fnt["small_bold"], fill=C["charcoal"])
    # Semiprecious stones
    stone_c9 = [(74,127,165),(181,83,60),(74,124,89),(130,100,50),(44,44,44)]
    stone_n9 = ["Lapis lazuli","Carnelian","Malachite","Jasper","Onyx"]
    for si9,(sc9,sn9) in enumerate(zip(stone_c9,stone_n9)):
        sx9 = 790 + (si9%3)*110
        sy9 = 55 + (si9//3)*160
        ill_draw9.ellipse([sx9, sy9, sx9+85, sy9+85], fill=sc9, outline=C["charcoal"], width=2)
        ill_draw9.text((sx9, sy9+90), sn9, font=fnt["small"], fill=C["charcoal"])
    ill_draw9.text((790, 375), "SEMIPRECIOUS STONES", font=fnt["small_bold"], fill=C["charcoal"])
    ill_draw9.text((790, 398), "(for inlay decoration)", font=fnt["small"], fill=C["stone_grey"])
    img.paste(ill_bg9, (ML, y))
    draw = ImageDraw.Draw(img)
    y += ill_h9 + 14

    y = draw_text_block(draw, "The portfolio contains a materials list -- but the descriptions have been separated from the materials. The explorer must reconnect them.", ML, y, fnt["body_it"], C["charcoal"], LW)
    y += 10
    draw_section_divider(draw, ML, y, LW)
    y += 6

    draw.text((ML, y), "WHAT IS THE TAJ MAHAL MADE FROM?", font=fnt["h2"], fill=C["indigo"])
    y += 40
    mats9 = [
        ("White Marble", C["stone_grey"], "The exterior of the mausoleum and the raised platform are covered in white marble. This marble came from Makrana in the state of Rajasthan, India. It is prized for its quality and bright appearance."),
        ("Red Sandstone", C["sandstone"], "The mosque, the jawab (mirror building), the great gateway, and much of the outer complex are built from red sandstone. This gives these buildings their warm, reddish colour."),
        ("Semiprecious Stones", C["teal"], "The decorative inlay work on the marble uses coloured semiprecious stones -- including lapis lazuli (blue), carnelian (orange-red), jasper, malachite (green), and others. These stones were brought from different regions."),
    ]
    for mat9, col9, desc9 in mats9:
        draw.text((ML, y), mat9 + ":", font=fnt["body_bold"], fill=col9)
        y += 30
        y = draw_text_block(draw, desc9, ML+20, y, fnt["body"], C["charcoal"], LW-20)
        y += 14

    draw_section_divider(draw, ML, y, LW)
    y += 6

    act_x9, act_y9 = draw_activity_zone(draw, "ACTIVITY: MATERIAL TO USE", ML, y, LW, 420)
    y = act_y9
    draw.text((act_x9, y), "Draw a line to match each material to how it was used in the Taj Mahal:", font=fnt["act"], fill=C["charcoal"])
    y += 42

    left9  = ["White marble", "Red sandstone", "Semiprecious stones"]
    right9 = ["Coloured stone inlay decoration", "The mausoleum exterior and platform", "The mosque, gateway, and outer buildings"]
    right_s9 = ["Coloured stone inlay decoration", "The mausoleum exterior and platform", "The mosque, gateway, and outer buildings"]
    col9w = (LW-40-30)//2
    row9h = 66
    for i9,(lt9,rd9) in enumerate(zip(left9,right_s9)):
        ly9 = y + i9*row9h
        lc9 = [C["stone_grey"],C["sandstone"],C["teal"]][i9]
        draw.rounded_rectangle([act_x9, ly9, act_x9+col9w, ly9+row9h-10], radius=6, fill=lc9)
        lb9 = draw.textbbox((0,0), lt9, font=fnt["body_bold"])
        draw.text((act_x9+(col9w-(lb9[2]-lb9[0]))//2, ly9+(row9h-10-(lb9[3]-lb9[1]))//2), lt9, font=fnt["body_bold"], fill=C["warm_white"])
        rx9b = act_x9+col9w+30
        rd9_lns = wrap_text(rd9, fnt["body"], col9w-16, draw)
        rbb9 = draw.textbbox((0,0), "Ag", font=fnt["body"])
        rh9 = len(rd9_lns)*(rbb9[3]-rbb9[1]+3)
        draw.rounded_rectangle([rx9b, ly9, rx9b+col9w, ly9+row9h-10], radius=6, fill=C["warm_white"], outline=C["veining"], width=1)
        dy9 = ly9+(row9h-10-rh9)//2
        for line9 in rd9_lns:
            draw.text((rx9b+8, dy9), line9, font=fnt["body"], fill=C["charcoal"])
            dy9 += rbb9[3]-rbb9[1]+3
    y += len(left9)*row9h + 14

    y = draw_think_box(draw, "Why do you think the builders used two different types of stone -- white marble and red sandstone -- in the same complex?", act_x9, y, LW-40, lines=2)

    draw_footer(draw, 9)
    img.save(os.path.join(OUT, "page_09.png"), dpi=(DPI, DPI))
    print("page_09.png done")


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 10
# ═══════════════════════════════════════════════════════════════════════════════
def make_page_10():
    img = new_page()
    draw = ImageDraw.Draw(img)
    draw_page_border(draw)
    y = draw_header_bar(draw, "BECOME A STONE-INLAY ARTIST", piece_num=4, piece_topic="ART & CRAFT")

    # Artisan scene (programmatic illustration)
    ill_h10 = 360
    ill_bg10 = Image.new("RGB", (LW, ill_h10), (174, 152, 115))
    ill_d10 = ImageDraw.Draw(ill_bg10)
    # Marble panel being inlaid
    ill_d10.rectangle([40, 30, 700, ill_h10-20], fill=C["warm_white"], outline=C["stone_grey"], width=3)
    # Inlay pattern
    cx10, cy10 = 370, ill_h10//2
    petal_c10 = [(74,127,165),(181,83,60),(74,124,89),(130,100,50),(44,62,107),(201,144,42),(181,83,60),(74,127,165)]
    for ai10 in range(0, 360, 45):
        rad10 = math.radians(ai10)
        px10 = cx10 + 62*math.cos(rad10)
        py10 = cy10 + 62*math.sin(rad10)
        ill_d10.ellipse([px10-16, py10-16, px10+16, py10+16], fill=petal_c10[ai10//45], outline=C["charcoal"], width=1)
    ill_d10.ellipse([cx10-20, cy10-20, cx10+20, cy10+20], fill=C["gold"], outline=C["charcoal"], width=2)
    for gi10 in range(4):
        a10 = math.radians(gi10*90+22)
        for r10 in range(86, 155, 12):
            vx10 = cx10+r10*math.cos(a10)
            vy10 = cy10+r10*math.sin(a10)
            ill_d10.ellipse([vx10-4, vy10-4, vx10+4, vy10+4], fill=C["emerald"])
    for bi10 in range(3):
        off10 = 10+bi10*14
        ill_d10.rectangle([40+off10, 30+off10, 700-off10, ill_h10-20-off10], outline=C["gold"] if bi10==0 else C["veining"], width=1)
    # "Artisan at work" indicator
    ill_d10.ellipse([710, ill_h10//2-35, 790, ill_h10//2+35], fill=(190,155,105), outline=C["charcoal"], width=2)
    ill_d10.text((716, ill_h10//2-14), "Artisan", font=fnt["small"], fill=C["charcoal"])
    # Stone swatches
    sc10 = [(74,127,165),(181,83,60),(74,124,89),(130,100,50),(44,44,44)]
    sn10 = ["Lapis lazuli\n(deep blue)","Carnelian\n(red-orange)","Malachite\n(deep green)","Jasper\n(earthy)","Onyx\n(black/white)"]
    for si10,(sc2,sn2) in enumerate(zip(sc10,sn10)):
        sx10 = 840+(si10%3)*105
        sy10 = 40+(si10//3)*155
        ill_d10.rounded_rectangle([sx10, sy10, sx10+82, sy10+52], radius=5, fill=sc2, outline=C["charcoal"], width=2)
        for li10,ln10 in enumerate(sn2.split('\n')):
            ill_d10.text((sx10+2, sy10+54+li10*18), ln10, font=fnt["small"], fill=C["charcoal"])
    img.paste(ill_bg10, (ML, y))
    draw = ImageDraw.Draw(img)
    draw_fiction_badge(draw, "INSPIRED BY HISTORICAL CRAFT TECHNIQUES", ML+10, y+ill_h10-28, "hist")
    y += ill_h10 + 14

    y = draw_text_block(draw, "One of the pieces of the blueprint is covered in tiny, beautiful coloured patterns. The explorer realises that the Taj Mahal's decoration isn't just stone -- it's art.", ML, y, fnt["body_it"], C["charcoal"], LW)
    y += 10
    y = draw_vocab_box(draw, "STONE INLAY", "Contrasting stones are shaped and set into a stone surface to create decoration. In Italian: pietra dura. In the Mughal/Indian context: parchinkari.", ML, y, LW)

    draw.text((ML, y), "THE ART OF STONE INLAY", font=fnt["h2"], fill=C["indigo"])
    y += 40
    y = draw_text_block(draw, "The surfaces of the Taj Mahal are not plain white marble. They are covered in intricate patterns -- flowers, leaves, geometric shapes -- all made from tiny pieces of carefully cut and shaped stones.", ML, y, fnt["body"], C["charcoal"], LW)
    y += 10
    steps10 = ["1. Design the pattern", "2. Cut tiny grooves into the marble", "3. Shape each small stone piece to fit perfectly", "4. Set the stones into the grooves -- so precisely that the joins are almost invisible"]
    for s10 in steps10:
        draw.text((ML+20, y), s10, font=fnt["body"], fill=C["charcoal"])
        y += 34
    y += 8
    draw_section_divider(draw, ML, y, LW)
    y += 8

    act_x10, act_y10 = draw_activity_zone(draw, "ACTIVITY: DESIGN YOUR OWN INLAY PATTERN", ML, y, LW, 780)
    y = act_y10
    y = draw_text_block(draw, "You are a craftsperson creating a panel for a marble wall. Design a pattern that includes:", act_x10, y, fnt["act"], C["charcoal"], LW-40)
    y += 16
    check10 = ["At least one flower", "Leaves or vines", "A border around the edge", "At least two different stone colours"]
    for c10 in check10:
        y = draw_checkbox_line(draw, act_x10, y, c10)
    y += 10
    draw.text((act_x10, y), "Design your pattern in the frame below:", font=fnt["body_bold"], fill=C["charcoal"])
    y += 28

    frame_h10 = H - y - MB - 200
    frame_h10 = max(frame_h10, 300)
    # Ornamental frame
    draw.rounded_rectangle([act_x10, y, act_x10+LW-40, y+frame_h10], radius=10, fill=C["warm_white"], outline=C["gold"], width=4)
    draw.rounded_rectangle([act_x10+18, y+18, act_x10+LW-58, y+frame_h10-18], radius=6, fill=C["warm_white"], outline=C["veining"], width=1)
    # Corner motifs
    for (cx3,cy3) in [(act_x10+32,y+32),(act_x10+LW-72,y+32),(act_x10+32,y+frame_h10-32),(act_x10+LW-72,y+frame_h10-32)]:
        draw.ellipse([cx3-12,cy3-12,cx3+12,cy3+12], fill=C["gold"])
        for a3 in range(0,360,90):
            r3 = math.radians(a3)
            draw.ellipse([cx3+15*math.cos(r3)-5,cy3+15*math.sin(r3)-5,cx3+15*math.cos(r3)+5,cy3+15*math.sin(r3)+5], fill=C["sandstone"])
    hint10 = "Draw your inlay design here"
    hb10 = draw.textbbox((0,0), hint10, font=fnt["body_it"])
    draw.text((act_x10+(LW-40-(hb10[2]-hb10[0]))//2, y+frame_h10//2-14), hint10, font=fnt["body_it"], fill=C["veining"])
    y += frame_h10 + 14

    draw.text((act_x10, y), "What stone colours did you choose?", font=fnt["body_bold"], fill=C["charcoal"])
    draw_writing_lines(draw, act_x10+306, y+8, LW-40-306, 1, 40)
    y += 52
    draw.text((act_x10, y), "What is the central image in your design?", font=fnt["body_bold"], fill=C["charcoal"])
    draw_writing_lines(draw, act_x10+354, y+8, LW-40-354, 1, 40)
    y += 52
    draw_reward_box(draw, 4, "ART & CRAFT", ML, y, LW)

    draw_footer(draw, 10)
    img.save(os.path.join(OUT, "page_10.png"), dpi=(DPI, DPI))
    print("page_10.png done")

# ═══════════════════════════════════════════════════════════════════════════════
# BATCH 2 — PAGES 11–20
# ═══════════════════════════════════════════════════════════════════════════════


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 11
# THE CALLIGRAPHER'S SECRET
# ═══════════════════════════════════════════════════════════════════════════════

def make_page_11():
    img = new_page()
    draw = ImageDraw.Draw(img)
    draw_page_border(draw)

    y = draw_header_bar(draw, "THE CALLIGRAPHER'S SECRET")

    y = draw_text_block(
        draw,
        "A new clue appears on the blueprint: a line of beautiful writing. "
        "The explorer discovers that writing itself can be part of architecture.",
        ML, y, fnt["body_it"], C["charcoal"], LW
    )
    y += 8

    y = draw_fact_box(
        draw,
        "The Taj Mahal contains inscriptions in Arabic calligraphy. "
        "The calligraphy is associated with Amanat Khan, whose signature appears on the monument.",
        ML, y, LW
    )

    draw.text(
        (ML, y),
        "CALLIGRAPHY AS ARCHITECTURE",
        font=fnt["h2"],
        fill=C["indigo"]
    )
    y += 40

    y = draw_text_block(
        draw,
        "Calligraphy is the art of beautiful handwriting. At the Taj Mahal, "
        "calligraphic inscriptions form part of the decoration of the buildings.",
        ML, y, fnt["body"], C["charcoal"], LW
    )
    y += 8

    y = draw_text_block(
        draw,
        "The inscriptions use a formal style of Arabic script called Thuluth. "
        "A master calligrapher associated with the Taj Mahal was Amanat Khan.",
        ML, y, fnt["body"], C["charcoal"], LW
    )
    y += 10

    draw_fiction_badge(
        draw,
        "HISTORICAL INFORMATION — NOT A TRANSLATION OF THE INSCRIPTION",
        ML, y, "hist"
    )
    y += 38

    # Decorative calligraphy panel — deliberately NOT real Arabic text
    panel_h = 390
    draw.rounded_rectangle(
        [ML, y, ML+LW, y+panel_h],
        radius=12,
        fill=C["warm_white"],
        outline=C["gold"],
        width=3
    )

    draw.text(
        (ML+30, y+25),
        "CALLIGRAPHY PRACTICE PANEL",
        font=fnt["h3"],
        fill=C["sandstone"]
    )

    # Decorative non-text strokes
    base_y = y + 205

    for i in range(7):
        sx = ML + 150 + i * 260
        draw.arc(
            [sx, base_y-75, sx+170, base_y+80],
            200, 340,
            fill=C["indigo"],
            width=7
        )

    draw.line(
        [(ML+100, base_y+55), (ML+LW-100, base_y+55)],
        fill=C["gold"],
        width=3
    )

    draw.text(
        (ML+30, y+285),
        "Practice graceful lines and curves — do not copy real inscription text.",
        font=fnt["caption"],
        fill=C["stone_grey"]
    )

    y += panel_h + 18

    act_x, act_y = draw_activity_zone(
        draw,
        "ACTIVITY: BECOME A CALLIGRAPHER",
        ML, y, LW, 530
    )
    y = act_y

    y = draw_text_block(
        draw,
        "Create your own decorative title for an imaginary explorer's journal. "
        "Focus on smooth curves, even spacing, and a balanced shape.",
        act_x, y, fnt["act"], C["charcoal"], LW-40
    )
    y += 16

    draw.text(
        (act_x, y),
        "Write your explorer title:",
        font=fnt["body_bold"],
        fill=C["charcoal"]
    )
    y += 35

    draw.rounded_rectangle(
        [act_x, y, act_x+LW-40, y+150],
        radius=8,
        fill=C["warm_white"],
        outline=C["veining"],
        width=2
    )

    draw.text(
        (act_x+30, y+55),
        "Your decorative title",
        font=fnt["body_it"],
        fill=C["veining"]
    )

    y += 175

    draw.text(
        (act_x, y),
        "What makes your lettering look balanced?",
        font=fnt["body_bold"],
        fill=C["charcoal"]
    )
    y += 32
    draw_writing_lines(draw, act_x, y, LW-40, 2, 44)

    draw_footer(draw, 11)
    img.save(os.path.join(OUT, "page_11.png"), dpi=(DPI, DPI))
    print("page_11.png done")


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 12
# WHO BUILT IT?
# ═══════════════════════════════════════════════════════════════════════════════

def make_page_12():
    img = new_page()
    draw = ImageDraw.Draw(img)
    draw_page_border(draw)

    y = draw_header_bar(draw, "WHO BUILT IT?")

    y = draw_text_block(
        draw,
        "The explorer expected to find the name of one architect. "
        "Instead, the evidence points to something much bigger: a huge team of specialists.",
        ML, y, fnt["body_it"], C["charcoal"], LW
    )
    y += 8

    y = draw_fact_box(
        draw,
        "The Taj Mahal was a large building project involving many different kinds "
        "of craftspeople and workers. Historical sources do not give us a simple, "
        "certain list of every person involved.",
        ML, y, LW
    )

    draw.text(
        (ML, y),
        "A TEAM OF SPECIALISTS",
        font=fnt["h2"],
        fill=C["indigo"]
    )
    y += 40

    roles = [
        ("Calligraphers", "Created decorative inscriptions"),
        ("Stoneworkers", "Cut, shaped and worked stone"),
        ("Inlay artisans", "Created detailed stone-inlay decoration"),
        ("Masons", "Built and assembled masonry"),
        ("Garden workers", "Created and maintained the planned garden"),
        ("Water specialists", "Worked with the complex's water system"),
    ]

    role_w = (LW-30)//2
    role_h = 100

    for i, (role, desc) in enumerate(roles):
        rx = ML + (i % 2) * (role_w + 30)
        ry = y + (i // 2) * (role_h + 18)

        draw.rounded_rectangle(
            [rx, ry, rx+role_w, ry+role_h],
            radius=8,
            fill=C["warm_white"],
            outline=C["veining"],
            width=2
        )

        draw.text(
            (rx+18, ry+14),
            role,
            font=fnt["body_bold"],
            fill=C["indigo"]
        )

        draw_text_block(
            draw,
            desc,
            rx+18,
            ry+48,
            fnt["small"],
            C["charcoal"],
            role_w-36,
            line_spacing=1.25
        )

    y += 3*(role_h+18) + 12

    draw_section_divider(draw, ML, y, LW)
    y += 8

    act_x, act_y = draw_activity_zone(
        draw,
        "ACTIVITY: MATCH THE SPECIALIST",
        ML, y, LW, 620
    )
    y = act_y

    draw.text(
        (act_x, y),
        "Match each specialist to the work they are associated with.",
        font=fnt["act"],
        fill=C["charcoal"]
    )
    y += 45

    left = [
        "Calligrapher",
        "Inlay artisan",
        "Stoneworker",
        "Garden worker",
        "Water specialist"
    ]

    right = [
        "Worked with planned gardens",
        "Created decorative writing",
        "Worked with the water system",
        "Worked with stone decoration",
        "Cut or shaped stone"
    ]

    # Scrambled right side
    right = [
        "Created decorative writing",
        "Cut or shaped stone",
        "Worked with stone decoration",
        "Worked with planned gardens",
        "Worked with the water system"
    ]

    cw = (LW-40-30)//2
    rh = 70

    for i in range(len(left)):
        yy = y + i*rh

        draw.rounded_rectangle(
            [act_x, yy, act_x+cw, yy+rh-10],
            radius=6,
            fill=C["warm_white"],
            outline=C["teal"],
            width=2
        )

        draw.text(
            (act_x+15, yy+20),
            left[i],
            font=fnt["body_bold"],
            fill=C["indigo"]
        )

        rx = act_x + cw + 30

        draw.rounded_rectangle(
            [rx, yy, rx+cw, yy+rh-10],
            radius=6,
            fill=C["warm_white"],
            outline=C["veining"],
            width=1
        )

        lines = wrap_text(right[i], fnt["small"], cw-20, draw)
        ly = yy + 12

        for line in lines:
            draw.text(
                (rx+10, ly),
                line,
                font=fnt["small"],
                fill=C["charcoal"]
            )
            ly += 24

    y += len(left)*rh + 12

    y = draw_think_box(
        draw,
        "Why is it useful for historians to think about all the different people "
        "who were needed to create a huge monument?",
        act_x, y, LW-40, lines=2
    )

    draw_footer(draw, 12)
    img.save(os.path.join(OUT, "page_12.png"), dpi=(DPI, DPI))
    print("page_12.png done")


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 13
# THE MATERIALS JOURNEY
# ═══════════════════════════════════════════════════════════════════════════════

def make_page_13():
    img = new_page()
    draw = ImageDraw.Draw(img)
    draw_page_border(draw)

    y = draw_header_bar(draw, "THE MATERIALS JOURNEY")

    y = draw_text_block(
        draw,
        "The explorer discovers that the Taj Mahal's materials did not all come "
        "from the same place. The next clue is a journey across the map.",
        ML, y, fnt["body_it"], C["charcoal"], LW
    )
    y += 8

    y = draw_fact_box(
        draw,
        "White marble used at the Taj Mahal came from Makrana in Rajasthan. "
        "Decorative stones came from different regions.",
        ML, y, LW
    )

    draw.text(
        (ML, y),
        "FOLLOW THE MATERIALS",
        font=fnt["h2"],
        fill=C["indigo"]
    )
    y += 40

    # Stylised India map / route panel
    map_h = 720

    draw.rounded_rectangle(
        [ML, y, ML+LW, y+map_h],
        radius=12,
        fill=(238, 232, 216),
        outline=C["veining"],
        width=2
    )

    # Simplified India silhouette — educational diagram, not geographic map
    cx = ML + LW//2
    top = y + 55

    india_pts = [
        (cx-190, top),
        (cx+50, top+20),
        (cx+190, top+150),
        (cx+125, top+300),
        (cx+80, top+460),
        (cx, top+610),
        (cx-90, top+470),
        (cx-130, top+330),
        (cx-220, top+220),
        (cx-240, top+90),
    ]

    draw.polygon(
        india_pts,
        fill=C["warm_white"],
        outline=C["stone_grey"]
    )

    # Agra
    agra = (cx-15, top+180)

    draw.ellipse(
        [agra[0]-14, agra[1]-14, agra[0]+14, agra[1]+14],
        fill=C["indigo"]
    )
    draw.text(
        (agra[0]+25, agra[1]-15),
        "AGRA",
        font=fnt["body_bold"],
        fill=C["indigo"]
    )

    # Makrana / Rajasthan
    mak = (cx-155, top+225)

    draw.ellipse(
        [mak[0]-14, mak[1]-14, mak[0]+14, mak[1]+14],
        fill=C["sandstone"]
    )
    draw.text(
        (mak[0]-170, mak[1]+20),
        "MAKRANA\nRAJASTHAN",
        font=fnt["small_bold"],
        fill=C["sandstone"]
    )

    # Route
    draw.arc(
        [mak[0]-80, mak[1]-70, agra[0]+80, agra[1]+100],
        180, 360,
        fill=C["gold"],
        width=6
    )

    draw.polygon(
        [
            (agra[0]-5, agra[1]+55),
            (agra[0]+5, agra[1]+55),
            (agra[0], agra[1]+72)
        ],
        fill=C["gold"]
    )

    draw.text(
        (ML+60, y+map_h-95),
        "Simplified route diagram — not to scale",
        font=fnt["caption"],
        fill=C["stone_grey"]
    )

    y += map_h + 18

    act_x, act_y = draw_activity_zone(
        draw,
        "ACTIVITY: TRACE THE JOURNEY",
        ML, y, LW, 520
    )
    y = act_y

    y = draw_text_block(
        draw,
        "Use the map above to answer the questions.",
        act_x, y, fnt["act"], C["charcoal"], LW-40
    )
    y += 20

    questions = [
        "1. Which city is the Taj Mahal in?",
        "2. Where did the white marble come from?",
        "3. Why would transporting heavy stone have required planning?"
    ]

    for q in questions:
        draw.text(
            (act_x, y),
            q,
            font=fnt["body_bold"],
            fill=C["charcoal"]
        )
        y += 34
        draw_writing_lines(draw, act_x+20, y, LW-80, 1, 40)
        y += 58

    draw_footer(draw, 13)
    img.save(os.path.join(OUT, "page_13.png"), dpi=(DPI, DPI))
    print("page_13.png done")


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 14
# THE GARDEN MYSTERY
# ═══════════════════════════════════════════════════════════════════════════════

def make_page_14():
    img = new_page()
    draw = ImageDraw.Draw(img)
    draw_page_border(draw)

    y = draw_header_bar(draw, "THE GARDEN MYSTERY")

    y = draw_text_block(
        draw,
        "The next blueprint section is green. The explorer expects a random garden, "
        "but the lines form a careful pattern.",
        ML, y, fnt["body_it"], C["charcoal"], LW
    )
    y += 8

    y = draw_vocab_box(
        draw,
        "CHARBAGH",
        "A four-part garden design divided by paths or water channels.",
        ML, y, LW
    )

    draw.text(
        (ML, y),
        "THE GARDEN IS PART OF THE DESIGN",
        font=fnt["h2"],
        fill=C["indigo"]
    )
    y += 40

    y = draw_text_block(
        draw,
        "The Taj Mahal garden is organized around a strong geometric plan. "
        "Straight paths and water channels divide the garden into four main parts.",
        ML, y, fnt["body"], C["charcoal"], LW
    )
    y += 10

    # Charbagh diagram
    garden_size = 620
    gx = ML + (LW-garden_size)//2
    gy = y

    draw.rectangle(
        [gx, gy, gx+garden_size, gy+garden_size],
        fill=C["emerald"],
        outline=C["indigo"],
        width=4
    )

    # Four quadrants
    draw.line(
        [(gx+garden_size//2, gy),
         (gx+garden_size//2, gy+garden_size)],
        fill=C["warm_white"],
        width=18
    )

    draw.line(
        [(gx, gy+garden_size//2),
         (gx+garden_size, gy+garden_size//2)],
        fill=C["warm_white"],
        width=18
    )

    # Water channels
    draw.line(
        [(gx+garden_size//2, gy+20),
         (gx+garden_size//2, gy+garden_size-20)],
        fill=C["yamuna"],
        width=8
    )

    draw.line(
        [(gx+20, gy+garden_size//2),
         (gx+garden_size-20, gy+garden_size//2)],
        fill=C["yamuna"],
        width=8
    )

    # Central tank
    tank = 75
    draw.rectangle(
        [
            gx+garden_size//2-tank//2,
            gy+garden_size//2-tank//2,
            gx+garden_size//2+tank//2,
            gy+garden_size//2+tank//2
        ],
        fill=C["yamuna"],
        outline=C["gold"],
        width=4
    )

    draw.text(
        (gx+garden_size//2-52, gy+garden_size//2-14),
        "TANK",
        font=fnt["small_bold"],
        fill=C["warm_white"]
    )

    y += garden_size + 20

    act_x, act_y = draw_activity_zone(
        draw,
        "ACTIVITY: SOLVE THE GARDEN MYSTERY",
        ML, y, LW, 720
    )
    y = act_y

    draw.text(
        (act_x, y),
        "Label these features on the garden plan:",
        font=fnt["act"],
        fill=C["charcoal"]
    )
    y += 42

    labels = [
        "1. Four garden sections",
        "2. Main paths",
        "3. Water channels",
        "4. Central tank"
    ]

    for item in labels:
        draw.text(
            (act_x, y),
            item,
            font=fnt["body_bold"],
            fill=C["charcoal"]
        )
        y += 48

    y += 10

    y = draw_think_box(
        draw,
        "Why might a geometric garden make a large complex feel organized?",
        act_x, y, LW-40, lines=2
    )

    draw_footer(draw, 14)
    img.save(os.path.join(OUT, "page_14.png"), dpi=(DPI, DPI))
    print("page_14.png done")


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 15
# BECOME THE WATER ENGINEER
# ═══════════════════════════════════════════════════════════════════════════════

def make_page_15():
    img = new_page()
    draw = ImageDraw.Draw(img)
    draw_page_border(draw)

    y = draw_header_bar(draw, "BECOME THE WATER ENGINEER")

    y = draw_text_block(
        draw,
        "The explorer follows a narrow blue line across the blueprint. "
        "It connects the river, the garden and the fountains.",
        ML, y, fnt["body_it"], C["charcoal"], LW
    )
    y += 8

    y = draw_fact_box(
        draw,
        "The Taj Mahal complex included a planned water system. "
        "Water was supplied and distributed through channels and pipes to support "
        "the garden and fountains.",
        ML, y, LW
    )

    draw.text(
        (ML, y),
        "THINK LIKE AN ENGINEER",
        font=fnt["h2"],
        fill=C["indigo"]
    )
    y += 40

    y = draw_text_block(
        draw,
        "Your job is to find a route from the water source to the garden tank "
        "without crossing a blocked section.",
        ML, y, fnt["body"], C["charcoal"], LW
    )
    y += 15

    # Maze
    maze_size = 900
    mx = ML + (LW-maze_size)//2
    my = y

    draw.rectangle(
        [mx, my, mx+maze_size, my+maze_size],
        fill=C["warm_white"],
        outline=C["indigo"],
        width=4
    )

    cells = 9
    cell = maze_size // cells

    # Grid
    for i in range(1, cells):
        draw.line(
            [(mx+i*cell, my), (mx+i*cell, my+maze_size)],
            fill=C["veining"],
            width=2
        )
        draw.line(
            [(mx, my+i*cell), (mx+maze_size, my+i*cell)],
            fill=C["veining"],
            width=2
        )

    # Blocked cells
    blocked = {
        (1,1),(2,1),(4,1),(5,1),(7,1),
        (1,2),(4,2),(7,2),
        (3,3),(4,3),(6,3),
        (0,4),(1,4),(6,4),
        (3,5),(6,5),(7,5),
        (1,6),(3,6),(4,6),
        (1,7),(4,7),(7,7),
        (3,8),(4,8),(7,8)
    }

    for r,c in blocked:
        draw.rectangle(
            [
                mx+c*cell+5,
                my+r*cell+5,
                mx+(c+1)*cell-5,
                my+(r+1)*cell-5
            ],
            fill=C["parchment"]
        )

    # Start
    draw.ellipse(
        [
            mx+8,
            my+cell//2-28,
            mx+cell-8,
            my+cell//2+28
        ],
        fill=C["yamuna"]
    )
    draw.text(
        (mx+18, my+cell//2-14),
        "WATER",
        font=fnt["small_bold"],
        fill=C["warm_white"]
    )

    # Goal
    gx15 = mx+8*cell+10
    gy15 = my+8*cell+10

    draw.rectangle(
        [gx15, gy15, gx15+cell-20, gy15+cell-20],
        fill=C["emerald"],
        outline=C["gold"],
        width=3
    )
    draw.text(
        (gx15+8, gy15+cell//2-12),
        "TANK",
        font=fnt["small_bold"],
        fill=C["warm_white"]
    )

    y += maze_size + 20

    act_x, act_y = draw_activity_zone(
        draw,
        "ACTIVITY: FIND THE WATER ROUTE",
        ML, y, LW, 500
    )
    y = act_y

    draw.text(
        (act_x, y),
        "Trace a path from WATER to TANK.",
        font=fnt["act"],
        fill=C["charcoal"]
    )
    y += 45

    draw.text(
        (act_x, y),
        "Did your route avoid every blocked section?",
        font=fnt["body_bold"],
        fill=C["charcoal"]
    )
    y += 40

    draw_writing_lines(draw, act_x, y, LW-40, 2, 44)

    draw_footer(draw, 15)
    img.save(os.path.join(OUT, "page_15.png"), dpi=(DPI, DPI))
    print("page_15.png done")


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 16
# THE REFLECTION PUZZLE
# ═══════════════════════════════════════════════════════════════════════════════

def make_page_16():
    img = new_page()
    draw = ImageDraw.Draw(img)
    draw_page_border(draw)

    y = draw_header_bar(draw, "THE REFLECTION PUZZLE")

    y = draw_text_block(
        draw,
        "At the centre of the garden, the explorer notices something strange: "
        "the water seems to create a second Taj Mahal.",
        ML, y, fnt["body_it"], C["charcoal"], LW
    )
    y += 8

    y = draw_fact_box(
        draw,
        "Still water can reflect objects on its surface. The Taj Mahal's garden "
        "and water features create opportunities for striking reflections.",
        ML, y, LW
    )

    draw.text(
        (ML, y),
        "REFLECTION AND SYMMETRY",
        font=fnt["h2"],
        fill=C["indigo"]
    )
    y += 40

    # Reflection diagram
    diagram_h = 780

    draw.rectangle(
        [ML, y, ML+LW, y+diagram_h],
        fill=C["warm_white"],
        outline=C["veining"],
        width=2
    )

    # Sky / building
    horizon = y + 360

    draw.rectangle(
        [ML, y, ML+LW, horizon],
        fill=(232,239,245)
    )

    draw.rectangle(
        [ML, horizon, ML+LW, y+diagram_h],
        fill=(205,220,225)
    )

    cx = ML + LW//2

    # Simplified Taj silhouette
    base_y = horizon-90

    draw.rectangle(
        [cx-230, base_y-160, cx+230, base_y],
        fill=C["warm_white"],
        outline=C["stone_grey"],
        width=2
    )

    draw.ellipse(
        [cx-125, base_y-340, cx+125, base_y-100],
        fill=C["warm_white"],
        outline=C["stone_grey"],
        width=2
    )

    # Minarets
    for dx in [-300, 300]:
        draw.rectangle(
            [cx+dx-18, base_y-230, cx+dx+18, base_y],
            fill=C["warm_white"],
            outline=C["stone_grey"],
            width=2
        )

    # Reflection guide
    draw.line(
        [(ML+50, horizon), (ML+LW-50, horizon)],
        fill=C["yamuna"],
        width=4
    )

    draw.text(
        (ML+70, horizon-30),
        "WATER LINE",
        font=fnt["small_bold"],
        fill=C["yamuna"]
    )

    # Blank reflection area
    draw.text(
        (cx-190, horizon+230),
        "DRAW THE REFLECTION",
        font=fnt["body_bold"],
        fill=C["stone_grey"]
    )

    y += diagram_h + 20

    act_x, act_y = draw_activity_zone(
        draw,
        "ACTIVITY: COMPLETE THE REFLECTION",
        ML, y, LW, 560
    )
    y = act_y

    y = draw_text_block(
        draw,
        "Draw the Taj Mahal's reflection below the water line. "
        "Try to keep the left and right sides balanced.",
        act_x, y, fnt["act"], C["charcoal"], LW-40
    )
    y += 20

    draw.text(
        (act_x, y),
        "What happens to the image when it meets the water?",
        font=fnt["body_bold"],
        fill=C["charcoal"]
    )
    y += 35
    draw_writing_lines(draw, act_x, y, LW-40, 2, 44)

    draw_footer(draw, 16)
    img.save(os.path.join(OUT, "page_16.png"), dpi=(DPI, DPI))
    print("page_16.png done")


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 17
# THE TAJ MAHAL FROM ABOVE
# ═══════════════════════════════════════════════════════════════════════════════

def make_page_17():
    img = new_page()
    draw = ImageDraw.Draw(img)
    draw_page_border(draw)

    y = draw_header_bar(draw, "THE TAJ MAHAL FROM ABOVE")

    y = draw_text_block(
        draw,
        "The explorer turns the blueprint over. Suddenly the whole complex makes "
        "more sense when viewed from above.",
        ML, y, fnt["body_it"], C["charcoal"], LW
    )
    y += 8

    y = draw_fact_box(
        draw,
        "The Taj Mahal complex includes the mausoleum, four minarets, mosque, "
        "jawab, garden, main gateway, platform and other surrounding structures.",
        ML, y, LW
    )

    draw.text(
        (ML, y),
        "READ THE COMPLEX AS A MAP",
        font=fnt["h2"],
        fill=C["indigo"]
    )
    y += 40

    plan_h = 900
    px = ML
    py = y

    draw.rectangle(
        [px, py, px+LW, py+plan_h],
        fill=C["parchment"],
        outline=C["indigo"],
        width=3
    )

    # Main axis
    center_x = px + LW//2

    # Garden
    garden_top = py + 180
    garden_bottom = py + 650

    draw.rectangle(
        [center_x-500, garden_top,
         center_x+500, garden_bottom],
        fill=C["emerald"],
        outline=C["indigo"],
        width=2
    )

    draw.line(
        [(center_x, garden_top),
         (center_x, garden_bottom)],
        fill=C["warm_white"],
        width=10
    )

    draw.line(
        [(center_x-500, (garden_top+garden_bottom)//2),
         (center_x+500, (garden_top+garden_bottom)//2)],
        fill=C["warm_white"],
        width=10
    )

    # Central tank
    tank = 100
    tx = center_x
    ty = (garden_top+garden_bottom)//2

    draw.rectangle(
        [tx-tank//2, ty-tank//2,
         tx+tank//2, ty+tank//2],
        fill=C["yamuna"],
        outline=C["gold"],
        width=3
    )

    # Mausoleum platform
    platform_w = 500
    platform_h = 240
    platform_y = py + 700

    draw.rectangle(
        [center_x-platform_w//2, platform_y,
         center_x+platform_w//2, platform_y+platform_h],
        fill=C["warm_white"],
        outline=C["stone_grey"],
        width=3
    )

    # Mausoleum
    draw.rectangle(
        [center_x-145, platform_y+60,
         center_x+145, platform_y+190],
        fill=C["ivory"],
        outline=C["indigo"],
        width=2
    )

    # Minarets
    for dx in [-210, 210]:
        for dy in [35, 205]:
            draw.ellipse(
                [center_x+dx-22,
                 platform_y+dy-22,
                 center_x+dx+22,
                 platform_y+dy+22],
                fill=C["indigo"]
            )

    # Mosque and jawab
    draw.rectangle(
        [center_x-430, platform_y+65,
         center_x-275, platform_y+175],
        fill=C["sandstone"]
    )

    draw.rectangle(
        [center_x+275, platform_y+65,
         center_x+430, platform_y+175],
        fill=C["sandstone"]
    )

    # Gateway
    draw.rectangle(
        [center_x-180, py+45,
         center_x+180, py+125],
        fill=C["sandstone"]
    )

    # Labels outside diagram
    labels17 = [
        ("MAIN GATEWAY", center_x, py+20),
        ("CHARBAGH GARDEN", center_x, garden_top+20),
        ("CENTRAL TANK", center_x, ty-18),
        ("MAUSOLEUM", center_x, platform_y+105),
        ("MOSQUE", center_x-350, platform_y+30),
        ("JAWAB", center_x+350, platform_y+30),
    ]

    for text17, lx17, ly17 in labels17:
        bb17 = draw.textbbox((0,0), text17, font=fnt["small_bold"])
        draw.text(
            (lx17-(bb17[2]-bb17[0])//2, ly17),
            text17,
            font=fnt["small_bold"],
            fill=C["charcoal"]
        )

    y += plan_h + 20

    act_x, act_y = draw_activity_zone(
        draw,
        "ACTIVITY: LABEL THE PLAN",
        ML, y, LW, 540
    )
    y = act_y

    items17 = [
        "Mausoleum",
        "Four minarets",
        "Mosque",
        "Jawab",
        "Garden",
        "Main gateway"
    ]

    draw.text(
        (act_x, y),
        "Find and label all six features on the plan above.",
        font=fnt["act"],
        fill=C["charcoal"]
    )
    y += 45

    for item in items17:
        draw_checkbox_line(draw, act_x, y, item)
        y += 42

    draw_footer(draw, 17)
    img.save(os.path.join(OUT, "page_17.png"), dpi=(DPI, DPI))
    print("page_17.png done")


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 18
# THE COMPLEX DETECTIVE
# ═══════════════════════════════════════════════════════════════════════════════

def make_page_18():
    img = new_page()
    draw = ImageDraw.Draw(img)
    draw_page_border(draw)

    y = draw_header_bar(draw, "THE COMPLEX DETECTIVE")

    y = draw_text_block(
        draw,
        "The explorer receives a set of clues. Each clue describes one part of "
        "the Taj Mahal complex. Can you identify where it belongs?",
        ML, y, fnt["body_it"], C["charcoal"], LW
    )
    y += 8

    clues = [
        ("CLUE A", "A place of worship on the western side of the mausoleum."),
        ("CLUE B", "A matching building on the eastern side."),
        ("CLUE C", "The large white marble tomb building."),
        ("CLUE D", "The entrance structure visitors pass through."),
        ("CLUE E", "The planned four-part garden."),
    ]

    y = draw_fact_box(
        draw,
        "Detectives identify places by combining clues. Historians do something "
        "similar when they study buildings and historical evidence.",
        ML, y, LW
    )

    draw.text(
        (ML, y),
        "SOLVE THE CLUES",
        font=fnt["h2"],
        fill=C["indigo"]
    )
    y += 40

    for label, clue in clues:
        draw.rounded_rectangle(
            [ML, y, ML+LW, y+100],
            radius=8,
            fill=C["warm_white"],
            outline=C["veining"],
            width=2
        )

        draw.text(
            (ML+20, y+15),
            label,
            font=fnt["body_bold"],
            fill=C["sandstone"]
        )

        draw_text_block(
            draw,
            clue,
            ML+150, y+18,
            fnt["body"],
            C["charcoal"],
            LW-180
        )

        y += 118

    y += 5

    act_x, act_y = draw_activity_zone(
        draw,
        "ACTIVITY: PLACE THE COMPONENTS",
        ML, y, LW, 730
    )
    y = act_y

    draw.text(
        (act_x, y),
        "Write the correct component beside each location.",
        font=fnt["act"],
        fill=C["charcoal"]
    )
    y += 45

    locations = [
        "WEST OF MAUSOLEUM: __________________",
        "EAST OF MAUSOLEUM: __________________",
        "CENTER: ______________________________",
        "SOUTHERN ENTRANCE: ___________________",
        "BETWEEN GATEWAY AND MAUSOLEUM: ______"
    ]

    for loc in locations:
        draw.text(
            (act_x, y),
            loc,
            font=fnt["body_bold"],
            fill=C["charcoal"]
        )
        y += 70

    y = draw_think_box(
        draw,
        "Which clue was easiest to solve? Which required the most thinking?",
        act_x, y, LW-40, lines=2
    )

    draw_footer(draw, 18)
    img.save(os.path.join(OUT, "page_18.png"), dpi=(DPI, DPI))
    print("page_18.png done")


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 19
# GEOMETRY HUNT
# ═══════════════════════════════════════════════════════════════════════════════

def make_page_19():
    img = new_page()
    draw = ImageDraw.Draw(img)
    draw_page_border(draw)

    y = draw_header_bar(draw, "GEOMETRY HUNT")

    y = draw_text_block(
        draw,
        "The explorer discovers that the blueprint is full of shapes. "
        "Architecture can be studied using geometry.",
        ML, y, fnt["body_it"], C["charcoal"], LW
    )
    y += 8

    y = draw_fact_box(
        draw,
        "Look for symmetry, circles, arches, rectangles, repeated patterns and "
        "other geometric forms in the Taj Mahal's architecture and gardens.",
        ML, y, LW
    )

    draw.text(
        (ML, y),
        "BECOME A GEOMETRY DETECTIVE",
        font=fnt["h2"],
        fill=C["indigo"]
    )
    y += 40

    # Shape cards
    shapes = [
        ("CIRCLE", "○"),
        ("RECTANGLE", "▭"),
        ("ARCH", "⌒"),
        ("SYMMETRY", "│"),
        ("REPEATED PATTERN", "◆ ◆ ◆")
    ]

    sw = (LW-40)//2
    sh = 150

    for i, (name, symbol) in enumerate(shapes):
        sx = ML + (i%2)*(sw+40)
        sy = y + (i//2)*(sh+20)

        draw.rounded_rectangle(
            [sx, sy, sx+sw, sy+sh],
            radius=10,
            fill=C["warm_white"],
            outline=C["gold"],
            width=2
        )

        draw.text(
            (sx+20, sy+18),
            name,
            font=fnt["body_bold"],
            fill=C["indigo"]
        )

        bb = draw.textbbox((0,0), symbol, font=fnt["title"])
        draw.text(
            (sx+(sw-(bb[2]-bb[0]))//2,
             sy+65),
            symbol,
            font=fnt["title"],
            fill=C["sandstone"]
        )

    y += 3*(sh+20) + 10

    act_x, act_y = draw_activity_zone(
        draw,
        "ACTIVITY: FIND THE GEOMETRY",
        ML, y, LW, 650
    )
    y = act_y

    draw.text(
        (act_x, y),
        "Find examples of these geometric ideas in the Taj Mahal.",
        font=fnt["act"],
        fill=C["charcoal"]
    )
    y += 45

    hunts = [
        "A circular shape: __________________________",
        "A rectangle or square: ______________________",
        "An arch: ___________________________________",
        "An example of symmetry: _____________________",
        "A repeated pattern: _________________________"
    ]

    for hunt in hunts:
        draw.text(
            (act_x, y),
            hunt,
            font=fnt["body_bold"],
            fill=C["charcoal"]
        )
        y += 68

    y = draw_think_box(
        draw,
        "Why might repeating the same shapes make a building look organized?",
        act_x, y, LW-40, lines=2
    )

    draw_footer(draw, 19)
    img.save(os.path.join(OUT, "page_19.png"), dpi=(DPI, DPI))
    print("page_19.png done")


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 20
# THE INSCRIPTION INVESTIGATION
# ═══════════════════════════════════════════════════════════════════════════════

def make_page_20():
    img = new_page()
    draw = ImageDraw.Draw(img)
    draw_page_border(draw)

    y = draw_header_bar(draw, "THE INSCRIPTION INVESTIGATION")

    y = draw_text_block(
        draw,
        "The explorer reaches the final clue of this section: writing carved into "
        "the architecture. But historians have to observe carefully before making claims.",
        ML, y, fnt["body_it"], C["charcoal"], LW
    )
    y += 8

    y = draw_fact_box(
        draw,
        "The Taj Mahal contains extensive calligraphic inscriptions. "
        "The inscriptions are part of the monument's decoration and architecture.",
        ML, y, LW
    )

    draw.text(
        (ML, y),
        "LOOK CLOSELY",
        font=fnt["h2"],
        fill=C["indigo"]
    )
    y += 40

    # Decorative inscription observation panel
    panel_h = 520

    draw.rounded_rectangle(
        [ML, y, ML+LW, y+panel_h],
        radius=12,
        fill=(245,242,236),
        outline=C["stone_grey"],
        width=3
    )

    # Simulated non-real inscription: decorative marks only
    for row in range(5):
        yy = y + 80 + row*75

        draw.line(
            [(ML+100, yy), (ML+LW-100, yy)],
            fill=C["gold"],
            width=2
        )

        for i in range(10):
            xx = ML + 150 + i*190

            draw.arc(
                [xx-45, yy-40, xx+45, yy+40],
                200, 340,
                fill=C["indigo"],
                width=5
            )

    draw_fiction_badge(
        draw,
        "DECORATIVE STUDY — NOT THE ACTUAL TAJ MAHAL INSCRIPTION",
        ML+30, y+panel_h-55, "fic"
    )

    y += panel_h + 18

    draw.text(
        (ML, y),
        "WHAT CAN YOU OBSERVE?",
        font=fnt["h2"],
        fill=C["indigo"]
    )
    y += 40

    observations = [
        "Does the writing repeat in a regular pattern?",
        "Are the letters tall, curved or angular?",
        "How is the writing arranged around the architecture?",
        "Why might a building use writing as decoration?"
    ]

    for q in observations:
        draw.text(
            (ML, y),
            "□ " + q,
            font=fnt["body"],
            fill=C["charcoal"]
        )
        y += 46

    y += 8

    act_x, act_y = draw_activity_zone(
        draw,
        "ACTIVITY: HISTORIAN'S OBSERVATION NOTES",
        ML, y, LW, 600
    )
    y = act_y

    draw.text(
        (act_x, y),
        "Write three things you can observe without guessing their meaning.",
        font=fnt["act"],
        fill=C["charcoal"]
    )
    y += 45

    for i in range(3):
        draw.text(
            (act_x, y),
            f"{i+1}.",
            font=fnt["body_bold"],
            fill=C["indigo"]
        )
        draw_writing_lines(
            draw,
            act_x+45, y+8,
            LW-85,
            2, 40
        )
        y += 95

    draw.text(
        (act_x, y),
        "Remember: observation comes before interpretation.",
        font=fnt["body_bold"],
        fill=C["sandstone"]
    )

    draw_footer(draw, 20)
    img.save(os.path.join(OUT, "page_20.png"), dpi=(DPI, DPI))
    print("page_20.png done")


# ═══════════════════════════════════════════════════════════════════════════════
# BATCH 2 MAIN
# ═══════════════════════════════════════════════════════════════════════════════

def generate_batch_02():
    print("Generating Batch 2 — Pages 11–20...")

    make_page_11()
    make_page_12()
    make_page_13()
    make_page_14()
    make_page_15()
    make_page_16()
    make_page_17()
    make_page_18()
    make_page_19()
    make_page_20()

    print("\nBatch 2 complete — Pages 11–20 generated.")
    print(f"Output: {OUT}")

# ═══════════════════════════════════════════════════════════════════════════════
# BATCH 3 — PAGES 21–30
# ═══════════════════════════════════════════════════════════════════════════════


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 21 — MYTH OR HISTORY?
# ═══════════════════════════════════════════════════════════════════════════════

def make_page_21():
    img = new_page()
    draw = ImageDraw.Draw(img)
    draw_page_border(draw)

    y = draw_header_bar(draw, "MYTH OR HISTORY?")

    y = draw_text_block(
        draw,
        "The explorer discovers a box labelled CLAIMS. Some statements are "
        "supported by historical evidence. Others are stories that have been "
        "repeated over time.",
        ML, y, fnt["body_it"], C["charcoal"], LW
    )
    y += 10

    y = draw_fact_box(
        draw,
        "Historians do not treat every story about the past as a fact. "
        "They ask: What is the evidence? Where did the claim come from? "
        "Can it be checked against reliable sources?",
        ML, y, LW
    )

    draw.text(
        (ML, y),
        "CLAIM OR EVIDENCE?",
        font=fnt["h2"],
        fill=C["indigo"]
    )
    y += 42

    claims = [
        (
            "The Taj Mahal was commissioned by Shah Jahan in memory of Mumtaz Mahal.",
            "HISTORY"
        ),
        (
            "The Taj Mahal was built as a black-marble twin across the Yamuna.",
            "MYTH / UNSUPPORTED CLAIM"
        ),
        (
            "The principal mausoleum was completed in 1648.",
            "HISTORY"
        ),
        (
            "The workers who built the Taj Mahal had their hands cut off.",
            "MYTH / UNSUPPORTED CLAIM"
        ),
        (
            "White marble used at the Taj Mahal came from Makrana in Rajasthan.",
            "HISTORY"
        ),
        (
            "Secret rooms prove that the monument hides a lost black Taj.",
            "MYTH / UNSUPPORTED CLAIM"
        ),
    ]

    row_h = 105

    for i, (claim, category) in enumerate(claims):
        bg = C["warm_white"] if i % 2 == 0 else C["parchment"]

        draw.rounded_rectangle(
            [ML, y, ML+LW, y+row_h-8],
            radius=7,
            fill=bg,
            outline=C["veining"],
            width=1
        )

        draw.text(
            (ML+20, y+15),
            f"{i+1}.",
            font=fnt["body_bold"],
            fill=C["indigo"]
        )

        lines = wrap_text(
            claim,
            fnt["body"],
            LW-450,
            draw
        )

        ly = y + 14
        for line in lines:
            draw.text(
                (ML+65, ly),
                line,
                font=fnt["body"],
                fill=C["charcoal"]
            )
            ly += 31

        draw.rounded_rectangle(
            [ML+LW-360, y+22, ML+LW-20, y+row_h-30],
            radius=6,
            fill=C["hist_bg"] if "HISTORY" == category else C["fic_bg"],
            outline=C["stone_grey"],
            width=1
        )

        # Do not reveal answer — child chooses.
        draw.text(
            (ML+LW-335, y+42),
            "□ HISTORY",
            font=fnt["small_bold"],
            fill=C["indigo"]
        )

        draw.text(
            (ML+LW-335, y+68),
            "□ MYTH / CLAIM",
            font=fnt["small_bold"],
            fill=C["sandstone"]
        )

        y += row_h

    y += 12

    y = draw_think_box(
        draw,
        "What should a historian do before deciding that a surprising story is true?",
        ML, y, LW, lines=2
    )

    draw_footer(draw, 21)
    img.save(os.path.join(OUT, "page_21.png"), dpi=(DPI, DPI))
    print("page_21.png done")


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 22 — THE HISTORIAN'S EVIDENCE BOX
# ═══════════════════════════════════════════════════════════════════════════════

def make_page_22():
    img = new_page()
    draw = ImageDraw.Draw(img)
    draw_page_border(draw)

    y = draw_header_bar(
        draw,
        "THE HISTORIAN'S EVIDENCE BOX",
        piece_num=6,
        piece_topic="EVIDENCE"
    )

    y = draw_text_block(
        draw,
        "The final blueprint clue is not a picture. It is a question: "
        "How do we know what we know?",
        ML, y, fnt["body_it"], C["charcoal"], LW
    )
    y += 8

    y = draw_vocab_box(
        draw,
        "EVIDENCE",
        "Information that can help us investigate and support a claim about the past.",
        ML, y, LW
    )

    draw.text(
        (ML, y),
        "BUILD AN EVIDENCE BOX",
        font=fnt["h2"],
        fill=C["indigo"]
    )
    y += 42

    evidence = [
        (
            "INSCRIPTIONS",
            "Writing on a monument can provide information about people, dates or purpose."
        ),
        (
            "BUILDINGS",
            "The surviving architecture can be examined directly."
        ),
        (
            "HISTORICAL RECORDS",
            "Documents and records can provide information about the past."
        ),
        (
            "ARCHAEOLOGICAL EVIDENCE",
            "Objects and physical remains can help historians investigate."
        ),
        (
            "RELIABLE SCHOLARSHIP",
            "Researchers compare evidence and interpretations."
        ),
    ]

    card_w = (LW-30)//2
    card_h = 170

    for i, (title, desc) in enumerate(evidence):
        if i < 4:
            cx = ML + (i % 2) * (card_w + 30)
            cy = y + (i // 2) * (card_h + 18)
        else:
            cx = ML + (LW-card_w)//2
            cy = y + 2 * (card_h + 18)

        draw.rounded_rectangle(
            [cx, cy, cx+card_w, cy+card_h],
            radius=10,
            fill=C["warm_white"],
            outline=C["gold"],
            width=2
        )

        draw.text(
            (cx+20, cy+18),
            title,
            font=fnt["body_bold"],
            fill=C["indigo"]
        )

        draw_text_block(
            draw,
            desc,
            cx+20,
            cy+60,
            fnt["small"],
            C["charcoal"],
            card_w-40,
            line_spacing=1.25
        )

    y += 3 * (card_h + 18) + 10

    draw_section_divider(draw, ML, y, LW)
    y += 8

    act_x, act_y = draw_activity_zone(
        draw,
        "ACTIVITY: SORT THE EVIDENCE",
        ML, y, LW, 700
    )
    y = act_y

    draw.text(
        (act_x, y),
        "For each clue, decide whether it is stronger evidence, "
        "a question to investigate, or an unsupported story.",
        font=fnt["act"],
        fill=C["charcoal"]
    )
    y += 45

    clues = [
        "An inscription carved on the monument",
        "A story someone posts online without a source",
        "A surviving part of the Taj Mahal complex",
        "A historical document that can be examined",
        "A claim repeated many times but with no evidence"
    ]

    for clue in clues:
        draw.rounded_rectangle(
            [act_x, y, act_x+LW-40, y+72],
            radius=6,
            fill=C["warm_white"],
            outline=C["veining"],
            width=1
        )

        draw.text(
            (act_x+15, y+18),
            clue,
            font=fnt["small_bold"],
            fill=C["charcoal"]
        )

        y += 82

    y = draw_reward_box(
        draw,
        6,
        "EVIDENCE",
        ML, y+8, LW
    )

    draw_footer(draw, 22)
    img.save(os.path.join(OUT, "page_22.png"), dpi=(DPI, DPI))
    print("page_22.png done")


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 23 — THE DAMAGED BLUEPRINT
# ═══════════════════════════════════════════════════════════════════════════════

def make_page_23():
    img = new_page()
    draw = ImageDraw.Draw(img)
    draw_page_border(draw)

    y = draw_header_bar(draw, "THE DAMAGED BLUEPRINT")

    y = draw_text_block(
        draw,
        "You have collected all six missing blueprint pieces. "
        "Now the explorer finally has enough information to rebuild the damaged plan.",
        ML, y, fnt["body_it"], C["charcoal"], LW
    )
    y += 8

    y = draw_fact_box(
        draw,
        "The six pieces are an adventure device created for this book. "
        "They are not historical artifacts from the Taj Mahal.",
        ML, y, LW
    )

    draw.text(
        (ML, y),
        "ASSEMBLE THE SIX CLUES",
        font=fnt["h2"],
        fill=C["indigo"]
    )
    y += 42

    topics = [
        ("1", "AGRA & GEOGRAPHY", C["yamuna"]),
        ("2", "PEOPLE & PURPOSE", C["sandstone"]),
        ("3", "ARCHITECTURE", C["indigo"]),
        ("4", "ART & CRAFT", C["emerald"]),
        ("5", "GARDENS & ENGINEERING", C["teal"]),
        ("6", "EVIDENCE", C["gold"]),
    ]

    # Large blueprint assembly area
    board_h = 1100

    draw.rounded_rectangle(
        [ML, y, ML+LW, y+board_h],
        radius=12,
        fill=(238, 235, 225),
        outline=C["indigo"],
        width=4
    )

    # Central Taj schematic
    bx = ML + LW//2
    by = y + 560

    # Platform
    draw.rectangle(
        [bx-350, by-100, bx+350, by+100],
        fill=C["warm_white"],
        outline=C["indigo"],
        width=3
    )

    # Mausoleum
    draw.rectangle(
        [bx-170, by-60, bx+170, by+80],
        fill=C["ivory"],
        outline=C["indigo"],
        width=2
    )

    # Dome
    draw.ellipse(
        [bx-110, by-230, bx+110, by-30],
        fill=C["warm_white"],
        outline=C["indigo"],
        width=3
    )

    # Four minarets
    for mx, my in [
        (bx-310, by-90),
        (bx+310, by-90),
        (bx-310, by+90),
        (bx+310, by+90)
    ]:
        draw.ellipse(
            [mx-22, my-22, mx+22, my+22],
            fill=C["indigo"]
        )

    # Garden
    draw.rectangle(
        [bx-500, y+120, bx+500, y+300],
        fill=C["emerald"],
        outline=C["teal"],
        width=2
    )

    draw.line(
        [(bx, y+120), (bx, y+300)],
        fill=C["warm_white"],
        width=8
    )

    draw.line(
        [(bx-500, y+210), (bx+500, y+210)],
        fill=C["warm_white"],
        width=8
    )

    # Gateway
    draw.rectangle(
        [bx-180, y+45, bx+180, y+95],
        fill=C["sandstone"]
    )

    # Piece labels around blueprint
    positions = [
        (ML+50, y+350),
        (ML+50, y+500),
        (ML+50, y+650),
        (ML+LW-470, y+350),
        (ML+LW-470, y+500),
        (ML+LW-470, y+650)
    ]

    for (num, topic, colour), (tx, ty) in zip(topics, positions):
        draw.rounded_rectangle(
            [tx, ty, tx+390, ty+105],
            radius=8,
            fill=C["warm_white"],
            outline=colour,
            width=4
        )

        draw.ellipse(
            [tx+15, ty+22, tx+70, ty+77],
            fill=colour
        )

        draw.text(
            (tx+31, ty+33),
            num,
            font=fnt["body_bold"],
            fill=C["warm_white"]
        )

        draw.text(
            (tx+85, ty+34),
            topic,
            font=fnt["small_bold"],
            fill=C["charcoal"]
        )

    y += board_h + 18

    act_x, act_y = draw_activity_zone(
        draw,
        "ACTIVITY: CHECK YOUR BLUEPRINT",
        ML, y, LW, 560
    )
    y = act_y

    checks = [
        "□ I can locate Agra and the Yamuna.",
        "□ I can explain why the Taj Mahal was built.",
        "□ I can identify major parts of the complex.",
        "□ I can describe stone inlay and calligraphy.",
        "□ I can explain the garden and water-system ideas.",
        "□ I can tell the difference between evidence and an unsupported claim."
    ]

    for check in checks:
        draw.text(
            (act_x, y),
            check,
            font=fnt["body"],
            fill=C["charcoal"]
        )
        y += 52

    draw_footer(draw, 23)
    img.save(os.path.join(OUT, "page_23.png"), dpi=(DPI, DPI))
    print("page_23.png done")


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 24 — THE FINAL ARCHITECT'S CHALLENGE
# ═══════════════════════════════════════════════════════════════════════════════

def make_page_24():
    img = new_page()
    draw = ImageDraw.Draw(img)
    draw_page_border(draw)

    y = draw_header_bar(draw, "THE FINAL ARCHITECT'S CHALLENGE")

    y = draw_text_block(
        draw,
        "The explorer now has enough clues to design a monument of their own. "
        "But the challenge is not to copy the Taj Mahal. It is to use what you learned.",
        ML, y, fnt["body_it"], C["charcoal"], LW
    )
    y += 10

    y = draw_fact_box(
        draw,
        "Use real architectural ideas from the book: symmetry, a central axis, "
        "balanced structures, geometric gardens, decorative patterns and planned spaces.",
        ML, y, LW
    )

    draw.text(
        (ML, y),
        "DESIGN YOUR MONUMENT",
        font=fnt["h2"],
        fill=C["indigo"]
    )
    y += 42

    act_x, act_y = draw_activity_zone(
        draw,
        "ACTIVITY: DRAW YOUR ARCHITECTURAL PLAN",
        ML, y, LW, 1550
    )
    y = act_y

    draw.text(
        (act_x, y),
        "Your design must include:",
        font=fnt["act"],
        fill=C["charcoal"]
    )
    y += 38

    requirements = [
        "A central building",
        "A clear line of symmetry",
        "At least four balanced surrounding features",
        "A planned garden or open space",
        "One decorative pattern",
        "A special feature of your own"
    ]

    for req in requirements:
        draw.text(
            (act_x, y),
            "□ " + req,
            font=fnt["small_bold"],
            fill=C["charcoal"]
        )
        y += 38

    y += 10

    draw.rectangle(
        [act_x, y, act_x+LW-40, y+850],
        fill=C["warm_white"],
        outline=C["indigo"],
        width=3
    )

    # Central axis guide
    axis_x = act_x + (LW-40)//2

    for gy in range(y+30, y+820, 40):
        draw.line(
            [(axis_x, gy), (axis_x, min(gy+20, y+850))],
            fill=C["veining"],
            width=2
        )

    draw.text(
        (axis_x-95, y+395),
        "CENTRAL AXIS",
        font=fnt["caption"],
        fill=C["veining"]
    )

    y += 875

    draw.text(
        (act_x, y),
        "Name your monument:",
        font=fnt["body_bold"],
        fill=C["charcoal"]
    )

    draw_writing_lines(
        draw,
        act_x+330, y+8,
        LW-40-330,
        1, 40
    )

    y += 55

    draw.text(
        (act_x, y),
        "What is the most important feature of your design?",
        font=fnt["body_bold"],
        fill=C["charcoal"]
    )

    y += 35
    draw_writing_lines(draw, act_x, y, LW-40, 2, 40)

    draw_footer(draw, 24)
    img.save(os.path.join(OUT, "page_24.png"), dpi=(DPI, DPI))
    print("page_24.png done")


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 25 — DESIGN YOUR OWN MUGHAL-INSPIRED GARDEN
# ═══════════════════════════════════════════════════════════════════════════════

def make_page_25():
    img = new_page()
    draw = ImageDraw.Draw(img)
    draw_page_border(draw)

    y = draw_header_bar(draw, "DESIGN YOUR OWN MUGHAL-INSPIRED GARDEN")

    y = draw_text_block(
        draw,
        "The garden is your turn to design. Start with a clear geometric plan, "
        "then add water, plants and spaces for people.",
        ML, y, fnt["body_it"], C["charcoal"], LW
    )
    y += 8

    y = draw_fact_box(
        draw,
        "The Taj Mahal garden follows a charbagh-style four-part arrangement. "
        "Your design is a creative activity inspired by historical garden planning.",
        ML, y, LW
    )

    draw.text(
        (ML, y),
        "YOUR FOUR-PART GARDEN",
        font=fnt["h2"],
        fill=C["indigo"]
    )
    y += 40

    # Large garden design grid
    garden = 1250
    gx = ML + (LW-garden)//2
    gy = y

    draw.rectangle(
        [gx, gy, gx+garden, gy+garden],
        fill=C["warm_white"],
        outline=C["emerald"],
        width=5
    )

    # Four sections
    draw.line(
        [(gx+garden//2, gy),
         (gx+garden//2, gy+garden)],
        fill=C["teal"],
        width=8
    )

    draw.line(
        [(gx, gy+garden//2),
         (gx+garden, gy+garden//2)],
        fill=C["teal"],
        width=8
    )

    # Central water feature
    tank = 180
    draw.rectangle(
        [
            gx+garden//2-tank//2,
            gy+garden//2-tank//2,
            gx+garden//2+tank//2,
            gy+garden//2+tank//2
        ],
        fill=C["yamuna"],
        outline=C["gold"],
        width=4
    )

    draw.text(
        (gx+garden//2-65, gy+garden//2-15),
        "WATER",
        font=fnt["small_bold"],
        fill=C["warm_white"]
    )

    # Decorative planting circles
    for row in range(3):
        for col in range(3):
            if row == 1 and col == 1:
                continue

            px = gx + 170 + col*460
            py = gy + 170 + row*460

            draw.ellipse(
                [px-35, py-35, px+35, py+35],
                outline=C["emerald"],
                width=4
            )

            draw.line(
                [(px, py-25), (px, py+25)],
                fill=C["emerald"],
                width=3
            )

    y += garden + 20

    act_x, act_y = draw_activity_zone(
        draw,
        "ACTIVITY: ADD YOUR DETAILS",
        ML, y, LW, 700
    )
    y = act_y

    details = [
        "□ Add at least 4 trees or planting areas.",
        "□ Add at least 2 water features.",
        "□ Add a path through each section.",
        "□ Add one special feature of your own.",
        "□ Give your garden a name."
    ]

    for detail in details:
        draw.text(
            (act_x, y),
            detail,
            font=fnt["body"],
            fill=C["charcoal"]
        )
        y += 48

    y += 5

    draw.text(
        (act_x, y),
        "Garden name:",
        font=fnt["body_bold"],
        fill=C["charcoal"]
    )

    draw_writing_lines(
        draw,
        act_x+200, y+8,
        LW-240,
        1, 40
    )

    y += 65

    draw.text(
        (act_x, y),
        "What makes your garden balanced?",
        font=fnt["body_bold"],
        fill=C["charcoal"]
    )

    y += 35
    draw_writing_lines(draw, act_x, y, LW-40, 2, 44)

    draw_footer(draw, 25)
    img.save(os.path.join(OUT, "page_25.png"), dpi=(DPI, DPI))
    print("page_25.png done")


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 26 — A DAY IN 17TH-CENTURY AGRA
# ═══════════════════════════════════════════════════════════════════════════════

def make_page_26():
    img = new_page()
    draw = ImageDraw.Draw(img)
    draw_page_border(draw)

    y = draw_header_bar(draw, "A DAY IN 17TH-CENTURY AGRA")

    draw_fiction_badge(
        draw,
        "HISTORICAL RECONSTRUCTION — Imaginative activity based on historical context",
        ML, y, "hist"
    )
    y += 40

    y = draw_text_block(
        draw,
        "Imagine walking through Agra centuries ago. You do not have a phone, "
        "car or modern map. You observe the city using your eyes, memory and the "
        "people around you.",
        ML, y, fnt["body_it"], C["charcoal"], LW
    )
    y += 10

    y = draw_fact_box(
        draw,
        "This page is an imaginative historical reconstruction. It is not a diary "
        "written by a real person and does not claim that every detail happened exactly this way.",
        ML, y, LW
    )

    draw.text(
        (ML, y),
        "OBSERVE THE WORLD AROUND YOU",
        font=fnt["h2"],
        fill=C["indigo"]
    )
    y += 42

    scenes = [
        (
            "THE CITY",
            "Agra was an important Mughal city. Think about streets, markets, "
            "craft workshops, gardens and river traffic."
        ),
        (
            "THE RIVER",
            "The Yamuna was an important geographical feature of the city."
        ),
        (
            "CRAFT",
            "Skilled craftspeople worked with materials such as stone, wood, "
            "metal, textiles and decorative materials."
        ),
        (
            "BUILDING",
            "Large construction projects required planning, materials and many "
            "different kinds of workers."
        )
    ]

    card_w = (LW-30)//2
    card_h = 260

    for i, (title, desc) in enumerate(scenes):
        sx = ML + (i%2)*(card_w+30)
        sy = y + (i//2)*(card_h+20)

        draw.rounded_rectangle(
            [sx, sy, sx+card_w, sy+card_h],
            radius=10,
            fill=C["warm_white"],
            outline=C["sandstone"],
            width=2
        )

        draw.text(
            (sx+20, sy+18),
            title,
            font=fnt["body_bold"],
            fill=C["indigo"]
        )

        draw_text_block(
            draw,
            desc,
            sx+20,
            sy+65,
            fnt["body"],
            C["charcoal"],
            card_w-40
        )

    y += 2*(card_h+20) + 20

    act_x, act_y = draw_activity_zone(
        draw,
        "ACTIVITY: BECOME THE OBSERVER",
        ML, y, LW, 720
    )
    y = act_y

    questions = [
        "What might you hear in a busy city?",
        "What might you see near the river?",
        "What kinds of crafts might you notice?",
        "What would be different from a modern city?"
    ]

    for q in questions:
        draw.text(
            (act_x, y),
            q,
            font=fnt["body_bold"],
            fill=C["charcoal"]
        )
        y += 35

        draw_writing_lines(
            draw,
            act_x+20,
            y,
            LW-80,
            2,
            42
        )

        y += 105

    draw_footer(draw, 26)
    img.save(os.path.join(OUT, "page_26.png"), dpi=(DPI, DPI))
    print("page_26.png done")


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 27 — THE FINAL HISTORIAN TEST
# ═══════════════════════════════════════════════════════════════════════════════

def make_page_27():
    img = new_page()
    draw = ImageDraw.Draw(img)
    draw_page_border(draw)

    y = draw_header_bar(draw, "THE FINAL HISTORIAN TEST")

    y = draw_text_block(
        draw,
        "You have followed the clues, investigated the architecture, studied the "
        "materials and separated evidence from unsupported stories. Now prove what you learned.",
        ML, y, fnt["body_it"], C["charcoal"], LW
    )
    y += 8

    y = draw_fact_box(
        draw,
        "Try the test without looking back at earlier pages.",
        ML, y, LW
    )

    questions = [
        (
            "1. Where is the Taj Mahal located?",
            ["Agra", "Delhi", "Jaipur"]
        ),
        (
            "2. Which river is beside the Taj Mahal?",
            ["Yamuna", "Ganga", "Godavari"]
        ),
        (
            "3. Who commissioned the Taj Mahal?",
            ["Shah Jahan", "Akbar", "Aurangzeb"]
        ),
        (
            "4. In which year did Mumtaz Mahal die?",
            ["1631", "1628", "1653"]
        ),
        (
            "5. Where did the white marble come from?",
            ["Makrana, Rajasthan", "Agra", "Kashmir"]
        ),
        (
            "6. What is a charbagh?",
            ["A four-part garden", "A type of stone", "A calligraphy style"]
        ),
        (
            "7. What is stone inlay?",
            ["Setting contrasting stones into a surface",
             "Painting a wall",
             "Carving a garden"]
        ),
        (
            "8. What is evidence?",
            ["Information that helps support a claim",
             "Any story we hear",
             "A guess"]
        ),
        (
            "9. When was the principal mausoleum completed?",
            ["1648", "1631", "1653"]
        ),
        (
            "10. What should a historian do with an unsupported story?",
            ["Investigate it",
             "Automatically accept it",
             "Treat it as proven"]
        )
    ]

    q_h = 205

    for i, (question, options) in enumerate(questions):
        if y + q_h > H-MB-80:
            # This should not normally happen; reduce spacing gracefully.
            q_h = 185

        draw.rounded_rectangle(
            [ML, y, ML+LW, y+q_h-10],
            radius=7,
            fill=C["warm_white"] if i%2 == 0 else C["parchment"],
            outline=C["veining"],
            width=1
        )

        draw.text(
            (ML+18, y+15),
            question,
            font=fnt["body_bold"],
            fill=C["charcoal"]
        )

        for j, option in enumerate(options):
            ox = ML + 45 + j*((LW-90)//3)

            draw.text(
                (ox, y+72),
                f"□ {option}",
                font=fnt["small"],
                fill=C["indigo"]
            )

        y += q_h

    draw_footer(draw, 27)
    img.save(os.path.join(OUT, "page_27.png"), dpi=(DPI, DPI))
    print("page_27.png done")


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 28 — THE TREASURE
# ═══════════════════════════════════════════════════════════════════════════════

def make_page_28():
    img = new_page()
    draw = ImageDraw.Draw(img)
    draw_page_border(draw)

    y = draw_header_bar(draw, "THE TREASURE")

    y = draw_text_block(
        draw,
        "The brass key finally turns. Inside the portfolio is one final object: "
        "a Historian's Scroll.",
        ML, y, fnt["body_it"], C["charcoal"], LW
    )
    y += 10

    draw_fiction_badge(
        draw,
        "[FICTIONAL ADVENTURE REWARD]",
        ML, y, "fic"
    )
    y += 40

    # Scroll
    scroll_h = 1250

    draw.rounded_rectangle(
        [ML+130, y, ML+LW-130, y+scroll_h],
        radius=20,
        fill=(239, 222, 181),
        outline=C["gold"],
        width=5
    )

    # Rolled ends
    draw.ellipse(
        [ML+90, y-30, ML+190, y+scroll_h+30],
        fill=C["aged_paper"],
        outline=C["gold"],
        width=3
    )

    draw.ellipse(
        [ML+LW-190, y-30, ML+LW-90, y+scroll_h+30],
        fill=C["aged_paper"],
        outline=C["gold"],
        width=3
    )

    title = "THE HISTORIAN'S SCROLL"

    bb = draw.textbbox((0,0), title, font=fnt["title"])

    draw.text(
        (ML+LW//2-(bb[2]-bb[0])//2, y+100),
        title,
        font=fnt["title"],
        fill=C["indigo"]
    )

    draw.text(
        (ML+LW//2-200, y+230),
        "Awarded to:",
        font=fnt["body_bold"],
        fill=C["sandstone"]
    )

    draw_writing_lines(
        draw,
        ML+LW//2-200,
        y+285,
        400,
        1,
        45
    )

    draw.text(
        (ML+LW//2-320, y+390),
        "For completing the Taj Mahal Mystery",
        font=fnt["h2"],
        fill=C["charcoal"]
    )

    achievements = [
        "Investigated historical clues",
        "Explored architecture",
        "Studied art and craft",
        "Followed the garden and water system",
        "Practised evidence-based thinking"
    ]

    yy = y + 500

    for achievement in achievements:
        draw.text(
            (ML+LW//2-320, yy),
            "✦ " + achievement,
            font=fnt["body"],
            fill=C["charcoal"]
        )
        yy += 65

    draw.text(
        (ML+LW//2-280, y+1050),
        "Keep asking questions. Keep checking evidence.",
        font=fnt["body_bold"],
        fill=C["indigo"]
    )

    y += scroll_h + 35

    draw.text(
        (ML, y),
        "Explorer signature:",
        font=fnt["body_bold"],
        fill=C["charcoal"]
    )

    draw_writing_lines(
        draw,
        ML+260, y+8,
        500,
        1, 40
    )

    draw_footer(draw, 28)
    img.save(os.path.join(OUT, "page_28.png"), dpi=(DPI, DPI))
    print("page_28.png done")


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 29 — MY TAJ MAHAL DISCOVERY CARD
# ═══════════════════════════════════════════════════════════════════════════════

def make_page_29():
    img = new_page()
    draw = ImageDraw.Draw(img)
    draw_page_border(draw)

    y = draw_header_bar(draw, "MY TAJ MAHAL DISCOVERY CARD")

    y = draw_text_block(
        draw,
        "Before the adventure ends, create your own historian's discovery card. "
        "Record the facts and ideas you want to remember.",
        ML, y, fnt["body_it"], C["charcoal"], LW
    )
    y += 15

    # Discovery card
    card_h = 1850

    draw.rounded_rectangle(
        [ML, y, ML+LW, y+card_h],
        radius=16,
        fill=C["warm_white"],
        outline=C["indigo"],
        width=4
    )

    draw.text(
        (ML+50, y+45),
        "MY DISCOVERY",
        font=fnt["title"],
        fill=C["indigo"]
    )

    y += 165

    fields = [
        ("One fact I will remember:", 2),
        ("The most interesting part of the Taj Mahal:", 2),
        ("One architectural idea I learned:", 2),
        ("One material I learned about:", 1),
        ("One thing I learned about evidence:", 2),
        ("A myth I now know to question:", 2),
    ]

    for label, lines in fields:
        draw.text(
            (ML+55, y),
            label,
            font=fnt["body_bold"],
            fill=C["sandstone"]
        )

        y += 38

        draw_writing_lines(
            draw,
            ML+55,
            y,
            LW-110,
            lines,
            48
        )

        y += lines*48 + 48

    # Final explorer identity
    draw.text(
        (ML+55, y),
        "My Explorer Name:",
        font=fnt["body_bold"],
        fill=C["indigo"]
    )

    draw_writing_lines(
        draw,
        ML+330, y+8,
        LW-440,
        1,
        44
    )

    y += 75

    draw.text(
        (ML+55, y),
        "My Explorer Symbol:",
        font=fnt["body_bold"],
        fill=C["indigo"]
    )

    draw.ellipse(
        [ML+400, y-20, ML+650, y+230],
        fill=C["ivory"],
        outline=C["gold"],
        width=4
    )

    draw.text(
        (ML+455, y+85),
        "DRAW",
        font=fnt["body_it"],
        fill=C["veining"]
    )

    y += 285

    draw.text(
        (ML+55, y),
        "My historian motto:",
        font=fnt["body_bold"],
        fill=C["indigo"]
    )

    draw_writing_lines(
        draw,
        ML+300, y+8,
        LW-410,
        2,
        44
    )

    y += 120

    draw.rounded_rectangle(
        [ML+55, y, ML+LW-55, y+100],
        radius=10,
        fill=C["reward_bg"],
        outline=C["gold"],
        width=2
    )

    draw.text(
        (ML+LW//2-330, y+30),
        "I AM READY TO THINK LIKE A HISTORIAN!",
        font=fnt["reward"],
        fill=C["warm_black"]
    )

    draw_footer(draw, 29)
    img.save(os.path.join(OUT, "page_29.png"), dpi=(DPI, DPI))
    print("page_29.png done")


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 30 — JUNIOR TAJ HISTORIAN CERTIFICATE
# ═══════════════════════════════════════════════════════════════════════════════

def make_page_30():
    img = new_page()
    draw = ImageDraw.Draw(img)
    draw_page_border(draw)

    y = draw_header_bar(draw, "JUNIOR TAJ HISTORIAN CERTIFICATE")

    y += 100

    # Certificate frame
    cert_x = ML+90
    cert_y = y
    cert_w = LW-180
    cert_h = 2100

    draw.rounded_rectangle(
        [cert_x, cert_y, cert_x+cert_w, cert_y+cert_h],
        radius=20,
        fill=(249,244,231),
        outline=C["gold"],
        width=7
    )

    draw.rounded_rectangle(
        [cert_x+25, cert_y+25,
         cert_x+cert_w-25, cert_y+cert_h-25],
        radius=15,
        outline=C["indigo"],
        width=2
    )

    # Decorative corner diamonds
    for cx, cy in [
        (cert_x+55, cert_y+55),
        (cert_x+cert_w-55, cert_y+55),
        (cert_x+55, cert_y+cert_h-55),
        (cert_x+cert_w-55, cert_y+cert_h-55)
    ]:
        draw.polygon(
            [
                (cx,cy-22),
                (cx+22,cy),
                (cx,cy+22),
                (cx-22,cy)
            ],
            fill=C["gold"]
        )

    title = "CERTIFICATE"

    bb = draw.textbbox((0,0), title, font=fnt["title"])

    draw.text(
        (cert_x+cert_w//2-(bb[2]-bb[0])//2,
         cert_y+180),
        title,
        font=fnt["title"],
        fill=C["indigo"]
    )

    subtitle = "JUNIOR TAJ HISTORIAN"

    bb = draw.textbbox((0,0), subtitle, font=fnt["h2"])

    draw.text(
        (cert_x+cert_w//2-(bb[2]-bb[0])//2,
         cert_y+330),
        subtitle,
        font=fnt["h2"],
        fill=C["sandstone"]
    )

    draw.text(
        (cert_x+cert_w//2-230, cert_y+500),
        "This certificate is awarded to",
        font=fnt["body"],
        fill=C["charcoal"]
    )

    draw_writing_lines(
        draw,
        cert_x+180,
        cert_y+590,
        cert_w-360,
        1,
        50
    )

    # Decorative Taj silhouette
    cx = cert_x+cert_w//2
    base_y = cert_y+1050

    draw.rectangle(
        [cx-230, base_y-80, cx+230, base_y+50],
        fill=C["warm_white"],
        outline=C["indigo"],
        width=2
    )

    draw.ellipse(
        [cx-120, base_y-250, cx+120, base_y-30],
        fill=C["warm_white"],
        outline=C["indigo"],
        width=3
    )

    for dx in [-280, 280]:
        draw.rectangle(
            [cx+dx-14, base_y-190,
             cx+dx+14, base_y+40],
            fill=C["warm_white"],
            outline=C["indigo"],
            width=2
        )

    draw.text(
        (cert_x+cert_w//2-330, cert_y+1330),
        "For completing the Taj Mahal Mystery",
        font=fnt["h2"],
        fill=C["charcoal"]
    )

    draw.text(
        (cert_x+cert_w//2-355, cert_y+1450),
        "and demonstrating curiosity, observation,",
        font=fnt["body"],
        fill=C["charcoal"]
    )

    draw.text(
        (cert_x+cert_w//2-325, cert_y+1500),
        "reasoning and evidence-based thinking.",
        font=fnt["body"],
        fill=C["charcoal"]
    )

    # Signature fields
    sig_y = cert_y+1740

    draw.text(
        (cert_x+120, sig_y),
        "Explorer",
        font=fnt["small_bold"],
        fill=C["indigo"]
    )

    draw.line(
        [(cert_x+70, sig_y-35),
         (cert_x+300, sig_y-35)],
        fill=C["stone_grey"],
        width=2
    )

    draw.text(
        (cert_x+cert_w-370, sig_y),
        "Date",
        font=fnt["small_bold"],
        fill=C["indigo"]
    )

    draw.line(
        [(cert_x+cert_w-410, sig_y-35),
         (cert_x+cert_w-90, sig_y-35)],
        fill=C["stone_grey"],
        width=2
    )

    draw.text(
        (cert_x+cert_w//2-180, cert_y+1930),
        "KEEP QUESTIONING. KEEP INVESTIGATING.",
        font=fnt["reward"],
        fill=C["indigo"]
    )

    draw_fiction_badge(
        draw,
        "[FICTIONAL BOOK CERTIFICATE]",
        cert_x+cert_w//2-110,
        cert_y+2020,
        "fic"
    )

    draw_footer(draw, 30)
    img.save(os.path.join(OUT, "page_30.png"), dpi=(DPI, DPI))
    print("page_30.png done")


# ═══════════════════════════════════════════════════════════════════════════════
# BATCH 3 MAIN
# ═══════════════════════════════════════════════════════════════════════════════

def generate_batch_03():
    print("Generating Batch 3 — Pages 21–30...")

    make_page_21()
    make_page_22()
    make_page_23()
    make_page_24()
    make_page_25()
    make_page_26()
    make_page_27()
    make_page_28()
    make_page_29()
    make_page_30()

    print("\nBatch 3 complete — Pages 21–30 generated.")
    print(f"Output: {OUT}")

# ─── MAIN ────────────────────────────────────────────────────────────────────
"""if __name__ == "__main__":
    print("Generating Batch 1 -- Pages 1-10...")
    make_page_01()
    make_page_02()
    make_page_03()
    make_page_04()
    make_page_05()
    make_page_06()
    make_page_07()
    make_page_08()
    make_page_09()
    make_page_10()
    print("\nAll 10 pages generated.")
    print(f"Output: {OUT}")


if __name__ == "__main__":
    print("Generating Batch 2 -- Pages 11-20...")

    make_page_11()
    make_page_12()
    make_page_13()
    make_page_14()
    make_page_15()
    make_page_16()
    make_page_17()
    make_page_18()
    make_page_19()
    make_page_20()

    print("\nAll 10 Batch 2 pages generated.")
    print(f"Output: {OUT}")
    """


if __name__ == "__main__":
    print("Generating Batch 3 — Pages 21–30...")

    make_page_21()
    make_page_22()
    make_page_23()
    make_page_24()
    make_page_25()
    make_page_26()
    make_page_27()
    make_page_28()
    make_page_29()
    make_page_30()

    print("\nAll 10 Batch 3 pages generated.")
    print(f"Output: {OUT}")