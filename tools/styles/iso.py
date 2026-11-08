"""Ch. 27 (isometric): 2:1 pixel lines, the 32x16 floor diamond, a 32x32 block and a small
iso room of the vault, in Greenhouse NES colours (top = light, left = mid, right = dark,
black outline) so the chapter can compare it directly with the side view."""
from __future__ import annotations

from PIL import Image

from nes import nes

K = nes(0x0F)
MAT = {  # material: (top, left, right, top-edge highlight)
    "stone": (nes(0x2B), nes(0x1C), nes(0x0C), nes(0x3B)),
    "metal": (nes(0x30), nes(0x10), nes(0x00), nes(0x30)),
    "crate": (nes(0x38), nes(0x27), nes(0x17), nes(0x30)),
    "moss": (nes(0x2A), nes(0x1A), nes(0x0A), nes(0x39)),
    "floor": (nes(0x1C), nes(0x0C), nes(0x0C), nes(0x2B)),
}


def line_21(n_steps, step=2):
    """Pixels of a clean 2:1 line: every row advances exactly `step` px."""
    return [(i * step + j, i) for i in range(n_steps) for j in range(step)]


def line_irregular(n_steps, pattern=(2, 3, 1, 2, 2, 3)):
    """'Avoid': a hand-drawn 'roughly 2:1' line with uneven runs (reads as wobbly)."""
    out, x = [], 0
    for i in range(n_steps):
        r = pattern[i % len(pattern)]
        out += [(x + j, i) for j in range(r)]
        x += r
    return out


def _put(px, x, y, c, w, h):
    if 0 <= x < w and 0 <= y < h:
        px[x, y] = c[:3] + (255,)


def diamond_rows(w=32):
    """Row spans (x0, x1) of a 2:1 diamond w x w/2 (pixel-perfect: 2 px steps)."""
    h = w // 2
    out = []
    for y in range(h):
        k = y if y < h // 2 else h - 1 - y
        out.append((w // 2 - 2 - 2 * k, w // 2 + 1 + 2 * k))
    return out


def block(mat="stone", h=16, w=32, top=True):
    """Iso block: w wide, top diamond w x w/2, side height h. -> RGBA (w, w/2 + h)."""
    top_c, left_c, right_c, hi = MAT[mat]
    H = w // 2 + h
    im = Image.new("RGBA", (w, H))
    px = im.load()
    rows = diamond_rows(w)
    half = w // 4
    for x in range(w):  # sides
        if x < w // 2:
            y0 = half + x // 2
            c = left_c
        else:
            y0 = half + (w - 1 - x) // 2
            c = right_c
        for y in range(y0, y0 + h + 1):
            _put(px, x, y, c, w, H)
    if top:
        for y, (x0, x1) in enumerate(rows):
            for x in range(x0, x1 + 1):
                _put(px, x, y, top_c, w, H)
    # outline: silhouette edges black, front vertical edge + top front edges highlighted
    for y, (x0, x1) in enumerate(rows[: w // 4]):
        for x in (x0, x0 + 1, x1 - 1, x1):
            _put(px, x, y, K, w, H)
    for x in range(w):
        yb = (half + x // 2 if x < w // 2 else half + (w - 1 - x) // 2) + h
        _put(px, x, yb, K, w, H)
    for y in range(half, half + h + 1):
        _put(px, 0, y, K, w, H)
        _put(px, w - 1, y, K, w, H)
    for x in range(1, w - 1):  # top front edges: highlight
        y = half + (x // 2 if x < w // 2 else (w - 1 - x) // 2)
        _put(px, x, y, hi, w, H)
    for y in range(half + w // 4 - 1, half + w // 4 + h - 1):
        _put(px, w // 2 - 1, y, hi if y == half + w // 4 - 1 else left_c, w, H)
    return im


def floor_tile(mat="floor", w=32):
    im = Image.new("RGBA", (w, w // 2))
    px = im.load()
    top, side, _, hi = MAT[mat]
    for y, (x0, x1) in enumerate(diamond_rows(w)):
        for x in range(x0, x1 + 1):
            c = top
            if (x + 2 * y) % 16 in (0, 1) or (x - 2 * y) % 16 in (0, 1):
                c = side  # grout lines follow the 2:1 axes
            px[x, y] = c[:3] + (255,)
    return im


def plant():
    from vault.props import FERN
    from nes import render
    from vault.palettes import AREAS
    return render(FERN, AREAS["greenhouse"]["bg"][1])


def _iso_line(px, p0, p1, c, w, h):
    (x0, y0), (x1, y1) = p0, p1
    n = max(abs(x1 - x0), abs(y1 - y0)) or 1
    for i in range(n + 1):
        _put(px, round(x0 + (x1 - x0) * i / n), round(y0 + (y1 - y0) * i / n), c, w, h)


def crate(w=32, h=16):
    """A block with plank frames and a diagonal brace on both visible sides."""
    im = block("crate", h, w)
    px = im.load()
    H = im.height
    half = w // 4
    dark_l, dark_r = MAT["crate"][2], nes(0x07)
    yl = lambda x: half + x // 2           # top edge of the left face at column x
    yr = lambda x: half + (w - 1 - x) // 2  # top edge of the right face
    for (xa, xb, top, c) in ((2, w // 2 - 3, yl, dark_l), (w // 2 + 2, w - 3, yr, dark_r)):
        for x in range(xa, xb + 1):
            _put(px, x, top(x) + 2, c, w, H)
            _put(px, x, top(x) + h - 2, c, w, H)
        for y in range(top(xa) + 2, top(xa) + h - 1):
            _put(px, xa, y, c, w, H)
        for y in range(top(xb) + 2, top(xb) + h - 1):
            _put(px, xb, y, c, w, H)
        _iso_line(px, (xa, top(xa) + h - 2), (xb, top(xb) + 2), c, w, H)
    return im


def shadow(w=14):
    """Small ellipse in the floor's dark ($0C) under a character: solid, so no off-palette blend."""
    im = Image.new("RGBA", (w, 5))
    px = im.load()
    for y in range(5):
        for x in range(w):
            if ((x - (w - 1) / 2) / (w / 2)) ** 2 + ((y - 2) / 2.5) ** 2 <= 1:
                px[x, y] = MAT["floor"][1][:3] + (255,)
    return im


TW = 32
ORIGIN = (256 // 2 - TW // 2, 40)


def at(i, j, z=0):
    """Screen position (top-left of a 32-wide block image) of grid cell (i, j) at height z px."""
    return ORIGIN[0] + (i - j) * TW // 2, ORIGIN[1] + (i + j) * TW // 4 - z


def room_items(kit_cell=None):
    """Draw list for the 6 x 6 room, sorted back to front: (depth, kind, i, j, z)."""
    cols, rws = 6, 6
    items = []
    for j in range(rws):
        for i in range(cols):
            items.append((i + j - 20, "floor", i, j, 0))  # floor first, always behind
    for i in range(cols):  # back-right wall (j = -1)
        for z in (0, 1):
            items.append((i - 1 + z * 0.01, "stone" if z == 0 else "moss", i, -1, z))
    for j in range(rws):  # back-left wall (i = -1)
        for z in (0, 1):
            items.append((j - 1 + z * 0.01, "stone" if z == 0 else "moss", -1, j, z))
    items += [(4 + 3, "crate", 4, 3, 0), (4 + 4, "crate", 4, 4, 0), (4 + 4 + 0.01, "crate", 4, 4, 1),
              (1 + 2, "metal", 1, 2, 0), (1 + 2 + 0.01, "plant", 1, 2, 1)]
    if kit_cell is not None:
        ki, kj = kit_cell
        items.append((ki + kj + 0.005, "kit", ki, kj, 0))
    return sorted(items, key=lambda t: t[0])


def room(kit_img=None, kit_cell=(2.0, 4.0), upto=None):
    """A 6 x 6 iso room: back walls of stone blocks topped with moss, a crate stack, a metal
    block with a fern on it, Kit standing on the floor. `upto` = draw only the first n items
    (for the painter's-algorithm figure)."""
    W, H = 256, 176
    im = Image.new("RGBA", (W, H), K[:3] + (255,))
    items = room_items(kit_cell if kit_img is not None else None)
    for n, (depth, kind, i, j, z) in enumerate(items):
        if upto is not None and n >= upto:
            break
        x, y = at(i, j, z * 16)
        x, y = int(round(x)), int(round(y))
        if kind == "floor":
            im.alpha_composite(floor_tile(), (x, y + 16))
        elif kind == "crate":
            im.alpha_composite(crate(), (x, y))
        elif kind == "plant":
            p = plant()
            im.alpha_composite(p, (x + 8, y + 16 - p.height + 8 + 2))
        elif kind == "kit":
            cx, cy = x + 16, y + 16 + 8  # centre of the floor diamond
            im.alpha_composite(shadow(), (cx - 7, cy - 2))
            im.alpha_composite(kit_img, (cx - 12, cy - 23))
        else:
            im.alpha_composite(block(kind), (x, y))
    return im
