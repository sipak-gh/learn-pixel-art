"""Shared helpers for the v2 (hollow-vault) figure scripts.
Usage:  from _v import *   (also re-exports _fig / pix, nes and the vault modules)."""
from _fig import *  # noqa: F401,F403
from _fig import IMAGES, os  # noqa: F401

from nes import *  # noqa: F401,F403
from nes import nes, nhex, render, check_attributes, scanline_counts  # noqa: F401
from vault import kit, creatures, fx, tiles as T, rooms, props as P, world, hud, bg as BGM  # noqa
from vault.palettes import AREAS, ORDER  # noqa: F401

BLACK = (0, 0, 0)
NESBLACK = nes(0x0F)[:3]
GH = AREAS["greenhouse"]
SUB_TINT = [(255, 90, 90), (90, 220, 120), (90, 150, 255), (250, 210, 60)]  # BG0..BG3 overlay


def nv(img, k=4, grid=False, major=None):
    """NES view: integer upscale on the black backdrop."""
    return view(img, k, grid=grid, bg=BLACK, major=major)


def sv(img, k=8, grid=True, major=8):
    """Sprite view: upscale on the neutral sprite background with pixel + tile grid."""
    return view(img, k, grid=grid, bg=SPR_BG, major=major)


def gif(name, frames, durations, k=3, bg=BLACK):
    save_gif(frames, os.path.join(IMAGES, name), durations, k, bg)
    print("wrote images/" + name)


def kitimg(**pose):
    return kit.img(kit.kit(**pose))


def sub_chips(sub, size=28, labels=True, sprite=False):
    """Four chips of a sub-palette with $xx labels (slot 0 of a sprite palette = 'transp.')."""
    chips = []
    for i, c in enumerate(sub):
        if sprite and i == 0:
            chip = checker(size, size, 7)
            lab = "transp."
        else:
            chip = Image.new("RGBA", (size, size), nes(c))
            lab = "$%02X" % c
        chips.append(label(chip, lab, 12, FIG_DIM, pad=3) if labels else chip)
    return row(chips, 2)


def tile_grid_view(img, k=3, tile=8, meta=16):
    """Upscaled image with an 8 px tile grid (thin) and 16 px metatile grid (strong)."""
    big = view(img, k, bg=BLACK)
    d = ImageDraw.Draw(big)
    for x in range(0, img.width + 1, tile):
        c = (255, 255, 255, 150) if x % meta == 0 else (255, 255, 255, 50)
        d.line([(x * k, 0), (x * k, big.height)], fill=c)
    for y in range(0, img.height + 1, tile):
        c = (255, 255, 255, 150) if y % meta == 0 else (255, 255, 255, 50)
        d.line([(0, y * k), (big.width, y * k)], fill=c)
    return big


def attr_view(img, attrs, k=3, alpha=90, numbers=True):
    """Tint every 16x16 attribute cell by its sub-palette index (BG0 red, BG1 green, BG2 blue,
    BG3 yellow) and print the index."""
    big = view(img, k, bg=BLACK)
    ov = Image.new("RGBA", big.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    for y, r in enumerate(attrs):
        for x, s in enumerate(r):
            d.rectangle([x * 16 * k, y * 16 * k, (x + 1) * 16 * k - 1, (y + 1) * 16 * k - 1],
                        fill=SUB_TINT[s] + (alpha,), outline=(255, 255, 255, 60))
    big.alpha_composite(ov)
    if numbers:
        for y, r in enumerate(attrs):
            for x, s in enumerate(r):
                draw_text(big, x * 16 * k + 3, y * 16 * k + 2, str(s), 12, (255, 255, 255))
    return big


def mark_cells(img, cells, k=3, color=(255, 60, 60), size=8):
    """Outline cells (x, y) of `size` px in an upscaled copy."""
    big = view(img, k, bg=BLACK)
    d = ImageDraw.Draw(big)
    for x, y in cells:
        d.rectangle([x * k, y * k, (x + size) * k - 1, (y + size) * k - 1], outline=color, width=2)
    return big


def scanline_graph(objects, height=240, k=2, limit=8):
    """Horizontal bar per scanline: number of hardware sprites (red past the limit)."""
    counts = scanline_counts(objects, height)
    w = 12 * 8
    im = Image.new("RGBA", (w * k // 2 + 40, height * k // 2), FIG_BG + (255,))
    d = ImageDraw.Draw(im)
    for y, c in enumerate(counts):
        yy = y * k // 2
        col = (230, 80, 80) if c > limit else ((240, 200, 80) if c == limit else (110, 200, 140))
        d.line([(0, yy), (c * 6 * k // 2, yy)], fill=col)
    x8 = limit * 6 * k // 2
    d.line([(x8, 0), (x8, im.height)], fill=(255, 255, 255, 140))
    draw_text(im, x8 + 3, 2, "8", 12, FIG_FG)
    return im


def chr_sheet(img, cols=16, k=3, greys=True, sub=None):
    """Unique 8x8 tiles of an NES image as a pattern-table style sheet (16 per row). With
    greys=True the tiles are shown in 4 greys (how CHR data looks without a palette)."""
    tiles = tile_set(img)
    if greys and sub is not None:
        cmap = {nes(c)[:3]: g for c, g in zip(sub, [(0, 0, 0), (85, 85, 85), (170, 170, 170),
                                                      (255, 255, 255)])}
        tiles = [remap(t, cmap) for t in tiles]
    rows_ = (len(tiles) + cols - 1) // cols
    sheet_ = Image.new("RGBA", (cols * 8, rows_ * 8), (0, 0, 0, 255))
    for i, t in enumerate(tiles):
        sheet_.alpha_composite(t, ((i % cols) * 8, (i // cols) * 8))
    return view(sheet_, k, bg=BLACK, major=8, major_color=(90, 90, 120, 255)), len(tiles)


def note(*parts):
    return "  ·  ".join(parts)


def anim_frames(frames_durs, t):
    imgs, durs = frames_durs
    t %= sum(durs)
    for im, d in zip(imgs, durs):
        if t < d:
            return im
        t -= d
    return imgs[-1]


def timing_chart(durs, names=None, colors=None, scale=0.5, height=26):
    """Horizontal timeline: one block per frame, width proportional to its duration (ms)."""
    total = sum(durs)
    w = int(total * scale) + 2
    im = Image.new("RGBA", (w, height + 18), FIG_BG + (255,))
    d = ImageDraw.Draw(im)
    x = 0
    pal = [(110, 170, 240), (240, 170, 90), (130, 210, 140), (220, 120, 200), (230, 220, 100)]
    for i, du in enumerate(durs):
        c = colors[i] if colors else pal[i % len(pal)]
        x1 = x + int(du * scale)
        d.rectangle([x, 0, x1 - 2, height - 1], fill=c)
        draw_text(im, x + 3, 5, (names[i] if names else str(i + 1)), 12, (20, 20, 30))
        draw_text(im, x + 2, height + 2, "%d" % du, 11, FIG_DIM)
        x = x1
    return label(im, "total %d ms" % total, 12, FIG_DIM)


def floor_strip(area="greenhouse", cells=8, rows_=3, seed=0):
    """A small stage: back wall with one row of ground at the bottom."""
    lay = ["." * cells] * (rows_ - 1) + ["#" * cells]
    img, _, _ = rooms.build(lay, area, seed)
    return img


def on_stage(stage, sprite, x, y):
    out = stage.copy()
    out.alpha_composite(sprite, (x, y))
    return out


def timeline(total, step, draw):
    """Frames for a GIF: draw(t) -> image, sampled every `step` ms."""
    return [draw(t) for t in range(0, total, step)], [step] * (total // step)


def changed(prev, cur, color=(255, 60, 200)):
    """Copy of `cur` with every pixel that differs from `prev` marked by a coloured square."""
    out = cur.copy()
    a, b = prev.load(), cur.load()
    ov = Image.new("RGBA", cur.size, (0, 0, 0, 0))
    o = ov.load()
    n = 0
    for y in range(cur.height):
        for x in range(cur.width):
            if a[x, y] != b[x, y]:
                o[x, y] = color + (150,)
                n += 1
    out.alpha_composite(ov)
    return out, n


def room_grids(area, frame=0, with_hud=True):
    """(image, attrs, metatile grids) of a final room; with_hud replaces rows 0-1 by the HUD grid."""
    r = world.ROOMS[area]
    img, attrs, grids = rooms.build(r["layout"], area, props=r["props"], frame=frame,
                                    bands=r.get("bands", ()))
    if with_hud:
        hg = hud.hud(**r["hud"])
        for my in range(2):
            grids[my] = [[row_[mx * 16:mx * 16 + 16] for row_ in hg[my * 16:my * 16 + 16]] for mx in range(16)]
            attrs[my] = [3] * 16
        paste(img, hud.hud_img(AREAS[area]["bg"][3], **r["hud"]), 0, 0)
    return img, attrs, grids


def chr_tiles(grids, flips=False):
    """Unique 8x8 tiles (as tuples of 8 strings of slot digits) from metatile grids - CHR data
    is palette-free, so the same pattern under two sub-palettes is ONE tile."""
    seen, out = set(), []
    for rw in grids:
        for gr in rw:
            gr = [r_.replace(".", "0") for r_ in gr]
            for ty in (0, 8):
                for tx in (0, 8):
                    t = tuple(r_[tx:tx + 8] for r_ in gr[ty:ty + 8])
                    keys = [t]
                    if flips:
                        h = tuple(r_[::-1] for r_ in t)
                        keys += [h, t[::-1], h[::-1]]
                    if not any(k in seen for k in keys):
                        seen.add(t)
                        out.append(t)
    return out


GREYS4 = [(0, 0, 0), (85, 85, 85), (170, 170, 170), (255, 255, 255)]


def chr_view(tiles, cols=16, k=3, rows_min=0):
    """Pattern-table look: tiles in 4 greys, 16 per row, slot 0 black."""
    n = len(tiles)
    rws = max(rows_min, (n + cols - 1) // cols)
    im = Image.new("RGBA", (cols * 8, rws * 8), (24, 24, 32, 255))
    px = im.load()
    for i, t in enumerate(tiles):
        ox, oy = (i % cols) * 8, (i // cols) * 8
        for y, r_ in enumerate(t):
            for x, c in enumerate(r_):
                px[ox + x, oy + y] = GREYS4[int(c)] + (255,)
    return view(im, k, bg=BLACK, major=8, major_color=(90, 90, 140, 255))
