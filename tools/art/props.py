"""Props for mossy-ruins: crate, sign, rock (in four 'stages' for ch02-ch07), plus tree,
bush, broken pillar, mushrooms, grass tufts, vines and an animated wall torch.
Side view, light from the upper left, outlines in the darkest colour of each material."""
from __future__ import annotations

import math
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pix import (Anim, blank, line_art, paste, put, rgba, rows, sprite,  # noqa
                 value_study)

# ---------------------------------------------------------------------------
# Crate, sign, rock: 'shaded' grids are hand drawn; 'textured' adds material detail;
# 'line' and 'value' are derived so every stage matches exactly.
# ---------------------------------------------------------------------------
CRATE = """
.dddddddddddddd.
dtttttttttttttcd
dtccccccccccccbd
dtcddddddddddcbd
dtcdbbbbbbbtccbd
dtcdbbbbbbtcdcbd
dtcdbbbbbtcdbcbd
dtcdbbbbtcdbbcbd
dtcdbbbtcdbbbcbd
dtcdbbtcdbbbbcbd
dtcdbtcdbbbbbcbd
dtcdtcdbbbbbbcbd
dtctcdbbbbbbbcbd
dtccccccccccccbd
dbbbbbbbbbbbbbbd
.dddddddddddddd.
"""
# Texture: grain streaks, nail heads, a split in the plank.
CRATE_TEX = {
    "b": [(5, 1), (9, 1), (7, 2), (11, 2), (2, 6), (2, 9), (13, 5), (13, 10), (6, 13), (10, 13)],
    "d": [(5, 5), (6, 5), (5, 8), (9, 10), (10, 10), (11, 9), (4, 13), (5, 13), (12, 14)],
    "3": [(2, 2), (13, 2), (2, 13), (13, 13)],
    "S": [(3, 1)],
}

SIGN = """
................
.dddddddddddddd.
dtttttttttttttcd
dtcccccccdccccbd
dtcddddddddcccbd
dtcccccccdccccbd
dbbbbbbbbbbbbbbd
.dddddddddddddd.
......dtbd......
......dtbd......
......dtbd......
......dtbd......
......dtbd......
.....gdtbdg.....
....gGdcbdhg....
...ghhdddddhh...
"""
SIGN_TEX = {
    "b": [(4, 2), (10, 2), (12, 5), (3, 5)],
    "d": [(13, 3), (12, 4)],
    "c": [(7, 10)],
    "3": [(2, 3), (13, 3)],
}

ROCK = """
................
................
................
................
................
......555555....
....5522222355..
...522111223345.
..52211122233445
.522211222333445
.522222223333445
5222222233334445
5322222333344445
5332223333444455
.53333334444455.
..555555555555..
"""
ROCK_TEX = {
    "g": [(6, 5), (7, 5), (8, 5), (5, 6), (6, 6)],
    "G": [(7, 6), (8, 6), (9, 6), (7, 5)],
    "h": [(4, 6), (9, 5), (10, 6)],
    "4": [(10, 9), (11, 10), (11, 11), (12, 12), (4, 12), (5, 13)],
    "3": [(4, 8), (13, 7), (7, 11), (8, 11)],
    "1": [(3, 9)],
}


def _apply(img, tex):
    out = img.copy()
    for c, pts in tex.items():
        for x, y in pts:
            if out.getpixel((x, y))[3]:
                put(out, x, y, c)
    return out


_STAGED = {"crate": (CRATE, CRATE_TEX), "sign": (SIGN, SIGN_TEX), "rock": (ROCK, ROCK_TEX)}


def staged(name: str, stage: str = "textured"):
    """stage: 'line' (ch02), 'value' (ch04), 'shaded' (ch06), 'textured' (ch07+)."""
    grid, tex = _STAGED[name]
    shaded = sprite(rows(grid))
    if stage == "shaded":
        return shaded
    if stage == "line":
        return line_art(shaded)
    if stage == "value":
        return value_study(shaded)
    return _apply(shaded, tex)


# ---------------------------------------------------------------------------
# Foliage by clumps: each clump is a rough disc shaded light / mid / dark by its own
# facing, then the whole canopy gets a dark outline. Back clumps use a darker ramp.
# ---------------------------------------------------------------------------
FRONT = ("G", "g", "h")
BACK = ("g", "h", "j")


def _clump(img, cx, cy, r, ramp, rng, light=(-0.7, -0.7)):
    rough = [r + rng.choice((-1, 0, 0, 0, 1)) for _ in range(16)]
    for y in range(int(cy - r - 2), int(cy + r + 3)):
        for x in range(int(cx - r - 2), int(cx + r + 3)):
            dx, dy = x + 0.5 - cx, y + 0.5 - cy
            d = math.hypot(dx, dy)
            a = int((math.atan2(dy, dx) + math.pi) / (2 * math.pi) * 16) % 16
            if d > rough[a]:
                continue
            # Crescent shading: lit where a disc shifted toward the light still covers the
            # pixel's far side; shadow where a disc shifted away no longer covers it.
            lx, ly = dx + light[0] * r * 0.45, dy + light[1] * r * 0.45
            sx, sy = dx - light[0] * r * 0.35, dy - light[1] * r * 0.35
            if math.hypot(sx, sy) > r * 0.95:
                c = ramp[2]
            elif math.hypot(lx, ly) > r * 0.85:
                c = ramp[0]
            else:
                c = ramp[1]
            put(img, x, y, c)


def _outline_alpha(img, color):
    out = img.copy()
    src = img.load()
    for y in range(img.height):
        for x in range(img.width):
            if src[x, y][3]:
                continue
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nx, ny = x + dx, y + dy
                if 0 <= nx < img.width and 0 <= ny < img.height and src[nx, ny][3]:
                    put(out, x, y, color)
                    break
    return out


def canopy(w, h, clumps, seed=1, outline="j"):
    rng = random.Random(seed)
    img = blank(w, h)
    for cx, cy, r, back in clumps:
        _clump(img, cx, cy, r, BACK if back else FRONT, rng)
    return _outline_alpha(img, outline) if outline else img


def _trunk(img, x0, top, bottom, w_top, w_bot):
    for y in range(top, bottom + 1):
        t = (y - top) / max(1, bottom - top)
        w = round(w_top + (w_bot - w_top) * t ** 3)
        left = x0 - w // 2
        for i in range(w):
            c = "c" if i == 0 else ("b" if i < w - 1 else "d")
            if i == 1 and w > 4:
                c = "c"
            put(img, left + i, y, c)
        put(img, left - 1, y, "d")
        put(img, left + w, y, "d")
    # bark marks
    for y in range(top + 3, bottom - 2, 5):
        put(img, x0 + (y % 2), y, "d")
        put(img, x0 + (y % 2), y + 1, "d")


def tree():
    """A 48x64 broadleaf tree."""
    img = blank(48, 64)
    _trunk(img, 24, 30, 61, 4, 10)
    # branches into the canopy
    for x, y in ((21, 34), (20, 33), (19, 32), (27, 35), (28, 34), (29, 33), (30, 32)):
        put(img, x, y, "b")
        put(img, x, y + 1, "d")
    can = canopy(48, 44, [
        (12, 26, 8, True), (36, 25, 8, True), (24, 14, 10, True),
        (14, 18, 8, False), (31, 16, 9, False), (22, 27, 8, False),
        (36, 30, 6, False), (10, 30, 6, False), (23, 8, 7, False),
    ], seed=7)
    paste(img, can, 0, 0)
    # root flare and grass at the foot
    for x, c in ((17, "d"), (18, "c"), (30, "b"), (31, "d")):
        put(img, x, 62, c)
    for x in range(14, 35):
        put(img, x, 63, "d")
    for x in (15, 16, 19, 29, 32, 33):
        put(img, x, 62, "g")
        put(img, x, 61 - (x % 2), "G")
    return img


def bush(seed=3):
    img = canopy(24, 16, [(7, 10, 5, True), (17, 10, 5, True), (12, 8, 6, False),
                          (5, 11, 4, False), (19, 11, 4, False)], seed=seed)
    for x in range(1, 23):
        if img.getpixel((x, 15))[3]:
            put(img, x, 15, "j")
    return img


def pillar():
    """A broken stone column, 16x40, with moss."""
    shaft_img = blank(16, 40)
    shaft = "3211223334444"  # left .. right: cylinder shading, highlight left of centre
    tops = [16, 15, 9, 9, 7, 4, 4, 8, 8, 13, 12, 12, 17]
    for i, c in enumerate(shaft):
        for y in range(tops[i], 34):
            put(shaft_img, 2 + i - 1 + 1, y, c)
        put(shaft_img, 2 + i, tops[i], "1" if c in "123" else "3")  # broken face catches light
    for y in range(12, 34):
        if shaft_img.getpixel((6, y))[3]:
            put(shaft_img, 6, y, "3" if y % 7 else "4")
        if shaft_img.getpixel((10, y))[3]:
            put(shaft_img, 10, y, "4")
    for x, y in ((7, 15), (8, 16), (8, 17), (9, 18), (4, 24), (5, 25), (11, 27), (12, 28)):
        put(shaft_img, x, y, "4")
    img = blank(16, 40)
    paste(img, _outline_alpha(shaft_img, "5"), 0, 0)
    for y, row in enumerate(["5555555555555555", "5222222223333345", "5233333333344445",
                             "5444444444444455", "5555555555555555"]):
        for x, c in enumerate(row):
            put(img, x, 34 + y, c)
    for x, y, c in ((0, 33, "g"), (1, 33, "G"), (2, 33, "g"), (12, 33, "g"), (13, 33, "h"),
                    (14, 33, "g"), (15, 33, "h"), (13, 31, "g"), (13, 30, "h"), (14, 29, "g"),
                    (13, 26, "h"), (12, 27, "g"), (7, 3, "G"), (8, 3, "g"), (6, 3, "g"),
                    (8, 6, "h"), (9, 7, "g")):
        put(img, x, y, c)
    return img


MUSHROOMS = """
..mmmm..........
.mkRRRm.........
mkSRRSRm..mmm...
mRRRRRRm.mkRRm..
.mppppm.mRSRRRm.
...Sc...mmpppm..
...Sc.....Sc....
..tSSc...tSc....
"""

TUFTS = [
    """
.G...G..
.G.G.G.G
GgGgGgG.
gghghgh.
""",
    """
...G....
.G.GG.G.
GgGgGGg.
gghgghg.
""",
]

FLAME = [
    """
....y...
...yo...
..yYyo..
..YWYo..
.oYWYyo.
.oyYyyo.
..ooyo..
""",
    """
...y....
...oy...
..oYy...
..yWYo..
.oYWWyo.
.oyYYyo.
..oyyo..
""",
    """
.....y..
....yo..
..oyYo..
..yYWy..
.oyWWYo.
.oyYyyo.
..oyoo..
""",
    """
........
...y.y..
...yYo..
..oYWyo.
.oYWWYo.
.oyYYyo.
..ooyo..
""",
]
TORCH_BASE = """
..dtcd..
...cb...
...cb...
.522235.
..5335..
...35...
..4335..
..5445..
........
"""


def mushrooms():
    return sprite(rows(MUSHROOMS))


def tuft(i=0):
    return sprite(rows(TUFTS[i]))


def torch(animated=True) -> Anim:
    frames = []
    for f in FLAME if animated else FLAME[:1]:
        img = blank(8, 16)
        paste(img, sprite(rows(f)), 0, 0)
        paste(img, sprite(rows(TORCH_BASE)), 0, 7)
        frames.append(img)
    return Anim("torch", frames, 110)


def vines(length=24, seed=5):
    rng = random.Random(seed)
    img = blank(8, length)
    for y in range(length):
        x = 3 + round(math.sin(y / 3.0))
        put(img, x, y, "h")
        if y % 4 == 1 and y < length - 1:
            side = -1 if (y // 4) % 2 else 1
            put(img, x + side, y, "g")
            put(img, x + 2 * side, y, "G" if side < 0 else "g")
            put(img, x + side, y + 1, "h")
    put(img, 3 + round(math.sin((length - 1) / 3.0)), length - 1, "g")
    _ = rng
    return img


def props_dict(stage="textured"):
    """Everything in the props sheet, at the given stage for the staged three."""
    d = {n: staged(n, stage) for n in _STAGED}
    if stage in ("shaded", "textured"):
        d.update(tree=tree(), bush=bush(), pillar=pillar(), mushrooms=mushrooms(),
                 tuft_a=tuft(0), tuft_b=tuft(1), vines=vines(), torch=torch(False).frames[0])
    return d
