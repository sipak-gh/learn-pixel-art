"""Ch. 24 figures: authentic NES - pattern tables, nametable + attribute bytes, sprite
overflow and flicker, the status-bar split, CHR bank animation, overlay sprites."""
from _v import *
from vault import fx as FXM, creatures as CR

AREA = "greenhouse"
img, attrs, grids = room_grids(AREA)


# ---------------------------------------------------------------- pattern tables
def sprite_chr(grid_list):
    """Unique non-empty 8x8 tiles of sprite grids, tiled from each frame's bounding box."""
    seen, out = set(), []
    for gr in grid_list:
        gr = [r.replace(".", "0") for r in gr]
        h, w = len(gr), len(gr[0])
        xs = [x for r in gr for x, c in enumerate(r) if c != "0"]
        ys = [y for y, r in enumerate(gr) if r.strip("0")]
        if not xs:
            continue
        x0, y0 = min(xs), min(ys)
        for ty in range(y0, max(ys) + 1, 8):
            for tx in range(x0, max(xs) + 1, 8):
                t = tuple((r[tx:tx + 8] + "0" * 8)[:8] for r in (gr[ty:ty + 8] + ["0" * w] * 8)[:8])
                if all(r == "0" * 8 for r in t):
                    continue
                h_ = tuple(r[::-1] for r in t)
                if t in seen or h_ in seen:
                    continue
                seen.add(t)
                out.append(t)
    return out


bg_tiles = chr_tiles(grids)  # background tiles cannot be flipped on the NES
kit_g = sum((kit.grids(a) for a in kit.ANIMS), [])
cre_g = sum((CR.grids(k_, a) for k_ in CR.CREATURES for a in CR.CREATURES[k_][1]), [])
fx_g = sum((FXM.FX[n][0] for n in FXM.FX), [])
spr_kit, spr_cre, spr_fx = sprite_chr(kit_g), sprite_chr(cre_g), sprite_chr(fx_g)
spr_tiles = spr_kit + spr_cre + spr_fx
print("CHR: bg", len(bg_tiles), "sprites", len(spr_tiles), "(kit", len(spr_kit), "creatures",
      len(spr_cre), "fx", len(spr_fx), ")")
save(panel([(chr_view(bg_tiles, k=3, rows_min=16), "background table: %d / 256" % len(bg_tiles)),
            (chr_view(spr_tiles, k=3, rows_min=16), "sprite table: %d / 256" % len(spr_tiles))],
           title="The two pattern tables (8 KB of CHR)",
           note="Kit %d tiles, 3 creatures %d, effects %d (mirrored sprite tiles counted once: the PPU "
                "flips sprites for free, but not background tiles). Tiles hold colour numbers only; palettes are applied later."
                % (len(spr_kit), len(spr_cre), len(spr_fx))), "ch24-pattern-tables.png")


# ---------------------------------------------------------------- nametable + attribute bytes
def attr_bytes(attrs):
    """30 rows of 16 metatile palette numbers -> 8x8 attribute bytes (bits: BR BL TR TL)."""
    out = []
    for by in range(8):
        rw = []
        for bx in range(8):
            def a(dy, dx):
                y, x = by * 2 + dy, bx * 2 + dx
                return attrs[y][x] if y < len(attrs) else 0
            rw.append(a(0, 0) | a(0, 1) << 2 | a(1, 0) << 4 | a(1, 1) << 6)
        out.append(rw)
    return out


AB = attr_bytes(attrs)
k = 3
base = attr_view(img, attrs, k=k, alpha=70, numbers=False)
ov = base.copy()
dr = ImageDraw.Draw(ov)
for by in range(8):
    for bx in range(8):
        x0, y0 = bx * 32 * k, by * 32 * k
        dr.rectangle([x0, y0, x0 + 32 * k - 1, y0 + 32 * k - 1], outline=(255, 255, 255), width=2)
        if by * 32 < 240:
            draw_text(ov, x0 + 6, y0 + 4, "$%02X" % AB[by][bx], 18, (255, 255, 255))
save(figure(ov, "The attribute table: 64 bytes, one per 32 x 32 block",
            "Each byte packs four 2-bit palette numbers, one per 16 x 16 quarter (bottom-right, "
            "bottom-left, top-right, top-left from the high bits down). The last row is half off-screen."),
     "ch24-attribute-bytes.png")

save(figure(tile_grid_view(img, 3), "The nametable: 32 x 30 tile numbers",
            "960 bytes name the tiles, 64 bytes colour them: 1 KB describes a whole screen."),
     "ch24-nametable.png")


# ---------------------------------------------------------------- sprite overflow & flicker
SP = AREAS[AREA]["spr"]
hop = CR.frames("hopper", "idle", SP[1])[0][0]
STAGE_W, STAGE_H = 144, 40


def hop_line(drop):
    """Five hoppers (2 sprites wide each) + nothing else on one line = 10 sprites. `drop`
    = indices of the 8x8 sprites the PPU fails to draw this frame."""
    im = Image.new("RGBA", (STAGE_W, STAGE_H), NESBLACK + (255,))
    for i in range(5):
        for half in range(2):
            sid = i * 2 + half
            if sid in drop:
                continue
            im.alpha_composite(hop.crop((half * 8, 0, half * 8 + 8, 16)), (8 + i * 26 + half * 8, 16))
    return im


no_cycle = [hop_line({8, 9})] * 4
cycle = [hop_line({(8 + 2 * f) % 10, (9 + 2 * f) % 10}) for f in range(5)]
frames = []
for f in range(10):
    a = nv(no_cycle[f % 4], 3)
    b = nv(cycle[f % 5], 3)
    frames.append(panel([(a, "fixed order: the 9th and 10th sprites never draw"),
                         (b, "OAM order rotated each frame: everyone flickers")],
                        title="Ten sprites on one line, room for eight"))
gif("ch24-flicker.gif", frames, [50] * len(frames), k=1, bg=FIG_BG)
save(panel([(nv(no_cycle[0], 3), "frame shown by the PPU"),
            (nv(hop_line(set()), 3), "what the game asked for")],
           title="Sprite overflow", note="Only the first 8 sprites (in OAM order) on a scanline are "
           "drawn. The rest vanish for that line."), "ch24-overflow.png")


# ---------------------------------------------------------------- status-bar split
play = world.background(AREA, 0, with_hud=False)[0]
hud_strip = world.background(AREA, 0, with_hud=True)[0].crop((0, 0, 256, 32))
for im_, x, y in hud.hud_sprites(SP[0], SP[2], **world.ROOMS[AREA]["hud"]):
    hud_strip.alpha_composite(im_, (x, y))
wide = Image.new("RGBA", (512, 240))
wide.paste(play, (0, 0))
wide.paste(play, (256, 0))


def split_frame(sx, split):
    scr = wide.crop((sx, 0, sx + 256, 240))
    if split:
        scr.paste(hud_strip, (0, 0))
    else:
        h = Image.new("RGBA", (512, 32))
        h.paste(hud_strip, (0, 0))
        h.paste(play.crop((0, 0, 256, 32)), (256, 0))
        scr.paste(h.crop((sx, 0, sx + 256, 32)), (0, 0))
    return scr


sframes = []
for i in range(48):
    sx = int(128 * (1 - math.cos(i / 48 * 2 * math.pi)) / 2 * 2)
    a = nv(split_frame(sx, False), 2)
    b = nv(split_frame(sx, True), 2)
    dr = ImageDraw.Draw(b)
    dr.line([0, 64, b.width, 64], fill=(255, 60, 200), width=2)
    sframes.append(panel([(a, "one scroll value for the whole frame"),
                          (b, "scroll changed at line 32 (pink)")],
                         title="The status-bar split"))
gif("ch24-split.gif", sframes, [60] * len(sframes), k=1, bg=FIG_BG)


# ---------------------------------------------------------------- CHR bank animation
WATER = "cistern"
cframes = []
for f in range(4):
    im_, at_, gr_ = room_grids(WATER, frame=f)
    wt = [t for t in chr_tiles(gr_) if t not in set(chr_tiles(room_grids(WATER, frame=(f + 1) % 4)[2]))]
    cframes.append((im_, wt))
bank_views = [chr_view(w, cols=2, k=8) for _, w in cframes]


def banks_row(active):
    cells = []
    for i, bv in enumerate(bank_views):
        c = bv.copy()
        if i == active:
            ImageDraw.Draw(c).rectangle([0, 0, c.width - 1, c.height - 1], outline=(255, 60, 200), width=4)
        cells.append(label(c, "bank %d" % i, 14, (255, 120, 220) if i == active else FIG_FG))
    return row(cells, 10)


bframes = []
for f, (im_, wt) in enumerate(cframes):
    bframes.append(figure(row([nv(im_.crop((0, 136, 256, 240)), 3), banks_row(f)], 20),
                          "Animating by swapping a CHR bank",
                          "The pool is drawn with the same %d water tiles everywhere; switching which "
                          "bank is mapped in redraws all of them at once, at no CPU cost." % len(wt)))
gif("ch24-chr-banks.gif", bframes, [140] * 4, k=1, bg=FIG_BG)
print("animated water tiles per bank:", [len(w) for _, w in cframes])


# ---------------------------------------------------------------- overlay sprite (extra colours)
kg = kit.kit()
glow = [["."] * 8 for _ in range(8)]
LX, LY = 16, 16
for y in range(8):
    for x in range(8):
        X, Y = LX + x, LY + y
        if Y < len(kg) and X < len(kg[0]) and kg[Y][X] == "3":
            glow[y][x] = "2"
glow[2][1] = "3" if glow[2][1] == "2" else glow[2][1]
glow_g = ["".join(r) for r in glow]
base_im = kit.img(kg)
ov_im = render(glow_g, SP[2])
both = base_im.copy()
both.alpha_composite(ov_im, (LX, LY))
outline = Image.new("RGBA", (24, 24), (0, 0, 0, 0))
outline.alpha_composite(ov_im, (LX, LY))
dr = ImageDraw.Draw(outline)
save(panel([(sv(base_im, 8, grid=False, major=None), "6 sprites, 3 colours"),
            (sv(outline, 8, grid=True, major=8), "+1 overlay sprite (SP2)"),
            (sv(both, 8, grid=False, major=None), "7 sprites, 5 colours")],
           title="Layering sprites for more colours",
           note="A second sprite with another palette is drawn over the first. The lamp glows "
                "yellow; the price is one more sprite on those scanlines (3 instead of 2)."),
     "ch24-overlay.png")


# ---------------------------------------------------------------- one tile as 16 bytes
TILE_NO = 0x24
tile = bg_tiles[TILE_NO]
TK = 20


def plane_view(t, bit):
    """One bit plane of a tile, enlarged, with the byte of each row written beside it."""
    im = Image.new("RGBA", (8, 8))
    px = im.load()
    vals = []
    for y, r in enumerate(t):
        v = 0
        for x, c in enumerate(r):
            b = (int(c) >> bit) & 1
            v |= b << (7 - x)
            px[x, y] = (255, 255, 255, 255) if b else (0, 0, 0, 255)
        vals.append(v)
    big = view(im, TK, grid=True, bg=BLACK)
    out = Image.new("RGBA", (big.width + 70, big.height), FIG_BG + (255,))
    out.alpha_composite(big, (0, 0))
    for y, v in enumerate(vals):
        draw_text(out, big.width + 10, y * TK + 2, "$%02X" % v, 15)
    return out, vals


def digits_view(t):
    big = chr_view([t], cols=1, k=TK)
    for y, r in enumerate(t):
        for x, c in enumerate(r):
            draw_text(big, x * TK + 6, y * TK + 2, c, 13, (255, 60, 200))
    return big


p0, v0 = plane_view(tile, 0)
p1, v1 = plane_view(tile, 1)
save(panel([(digits_view(tile), "tile $%02X: colour numbers 0-3" % TILE_NO),
            (p0, "plane 0 = low bit -> bytes 0-7"),
            (p1, "plane 1 = high bit -> bytes 8-15")],
           title="One 8 x 8 tile = 16 bytes (2 bits per pixel, planar)",
           note="Bytes in the .chr file: " + " ".join("%02X" % v for v in v0 + v1)
                + ". Colour 3 = both bits set, 2 = high bit only, 1 = low bit only, 0 = neither."),
     "ch24-tile-bytes.png")


# ---------------------------------------------------------------- decoding attribute bytes
def attr_block(by, bx, k=8):
    crop = img.crop((bx * 32, by * 32, bx * 32 + 32, by * 32 + 32))
    sub = [r[bx * 2:bx * 2 + 2] for r in attrs[by * 2:by * 2 + 2]]
    big = attr_view(crop, sub, k=k, alpha=80, numbers=False)
    names = (("TL", 0, 0), ("TR", 0, 1), ("BL", 1, 0), ("BR", 1, 1))
    for n, dy, dx in names:
        draw_text(big, dx * 16 * k + 6, dy * 16 * k + 4, "%s=%d" % (n, sub[dy][dx]), 16, (255, 255, 255))
    b = AB[by][bx]
    bits = "%{:02b} {:02b} {:02b} {:02b}".format(b >> 6 & 3, b >> 4 & 3, b >> 2 & 3, b & 3)
    return big, "$%02X = %s  (BR BL TR TL)" % (b, bits)


blocks = [attr_block(3, 3), attr_block(6, 4)]
save(panel(blocks, title="Decoding an attribute byte",
           note="Read the byte as four 2-bit pairs from the high end: bottom-right, bottom-left, "
                "top-right, top-left. Each pair is the BG sub-palette (0-3) of one 16 x 16 quarter."),
     "ch24-attribute-decode.png")
