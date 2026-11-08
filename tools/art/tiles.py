"""Environment tiles for mossy-ruins (16x16, side view, light from the upper left).

Terrain is built the way many artists build it in an editor: a hand-drawn seamless fill,
hand-drawn edge overlays (grass cap, cliff lips, roots), and corner pieces. The 13 'template'
tiles (fill, 4 edges, 4 outer corners, 4 inner corners) are then cut into 8x8 quarters to
generate every autotile combination (ch10).
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pix import (blank, paste, put, recolor, rgba, rows, sprite, tiled, wrap_shift)  # noqa

T = 16


def stamp(dst, grid, x, y, wrap=True):
    """Draw a small grid onto dst with wrap-around (keeps tiles seamless)."""
    g = rows(grid) if isinstance(grid, str) else grid
    for j, r in enumerate(g):
        for i, ch in enumerate(r):
            if ch == ".":
                continue
            px, py = x + i, y + j
            if wrap:
                px %= dst.width
                py %= dst.height
            put(dst, px, py, ch)
    return dst


# ---------------------------------------------------------------------------
# Hand-drawn texture stamps
# ---------------------------------------------------------------------------
PEBBLE = """
.tc.
tccd
.cdd
"""
PEBBLE_S = """
tc
cd
"""
STREAK = """
dd..
.ddd
"""
STREAK2 = """
.dd
dd.
"""
ROOT = """
d.
d.
.d
"""


DIRT = [
    """
bbbbbbbbbbbbbbbb
bbbbbbbbbbbdbbbb
bbcbbbbbbbddbbbb
bctdbbbbbbbbbbbb
bbddbbbbbbbbbbbb
bbbbbbbddbbbbbbb
dbbbbbddbbbbbbbd
ddbbbbbbbbbbbbdd
bbbbbbbbbbcbbbbb
bbbbbbbbbctdbbbb
bbbbbbbbbbddbbbb
bbbbbbbbbbbbbbbb
bbbcbbbbbbbbbbbb
bbbddbbbbbbbbdbb
bbbbbddbbbbbbddb
bbbbbbbbbbbbbbbb
""",
    """
bbbbbbbbbbbbbbbb
bbbbbbcbbbbbbbbb
bbbbbctdbbbbbbbb
bbbbbbddbbbbbbbb
bbbbbbbbbbbbddbb
dbbbbbbbbbbddbbb
bdbbbbbbbbbbbbbb
bbbbbbbbbbbbbbbb
bbbbbbbbbbbbbcbb
bbbbddbbbbbbbddb
bbbbbddbbbbbbbbb
bbbbbbbbbbbbbbbb
bcbbbbbbbbddbbbb
bddbbbbbbbbddbbb
bbbbbbbbbbbbbbbb
bbbbbbbbbbbbbbbb
""",
    """
bbbbbbbbbbbbbbbb
bbbbbbbbbbbdbbbb
bbbbbbbbbbddbbbb
bbbbbbbbbbbbbbbb
bbbbbtSSbbbbbbbb
bbbbtSttcbbbbbbb
bbbbtttcFdbbbbbd
bbbbbccFddbbbbdd
bbbbbbdddbbbbbbb
bbbbbbbbbbbbbbbb
bcbbbbbbbbbbbbbb
bddbbbbbbbbbbcbb
bbbbbbbbbbbbbddb
bbbbbbbddbbbbbbb
bbbbbbbbddbbbbbb
bbbbbbbbbbbbbbbb
""",
]


def dirt(variant=0):
    """Seamless earth fill, hand drawn. Variant 2 has a buried pale stone (use rarely)."""
    return sprite(rows(DIRT[variant]))


def dirt_busy():
    """The beginner version: evenly spaced, high-contrast specks (an 'Avoid' example)."""
    t = blank(T, T, "b")
    for x, y in ((2, 2), (10, 2), (6, 6), (14, 6), (2, 10), (10, 10), (6, 14), (14, 14)):
        stamp(t, PEBBLE_S, x, y)
        stamp(t, "S", x, y)
    return t


# Grass cap: 16 wide, seamless horizontally. Rows 0-1 are blade tips above the surface.
GRASS_CAP = """
....G.......G...
.G..GG.Y...GGG..
GGGGGGGGGGGGGGGG
GGGGgGGGGGGGgGGG
gGgggggGgggggggg
gghgggghhggghggh
hhhhghhhhhhhhhhh
jhhjhhhjjhhhjhhj
.jhj.jhj..jhj.jj
..j...j....j....
dd.dd.d.dd.d.dd.
"""
# Cap ends for outer corners (rounded), drawn over the corner of the tile.
GRASS_CAP_L = """
........
...G..Y.
..GGGGGG
.GGGgGGG
gGgggggG
gghggggh
jhhhghhh
.jhjhhhj
.jhj.jhj
..j...j.
.d.dd.d.
"""
GRASS_CAP_R = """
....G...
.G.GG...
GGGGGG..
GGGGgGG.
gGgggggg
gghgggh.
hhhhghhj
jhhjhhj.
.jhj.jj.
..j..j..
dd.dd...
"""


def _shade_left(t, top=0, bottom=T):
    for y in range(top, bottom):
        put(t, 0, y, "d")
        if t.getpixel((1, y))[:3] == rgba("b")[:3]:
            put(t, 1, y, "c")


def _shade_right(t, top=0, bottom=T):
    for y in range(top, bottom):
        put(t, T - 1, y, "d")
        if t.getpixel((T - 2, y))[:3] == rgba("b")[:3]:
            put(t, T - 2, y, "d")


def _shade_bottom(t, left=0, right=T, roots=True):
    # Bottom 3 rows: an outline and dangling roots; the rest becomes transparent.
    for x in range(left, right):
        put(t, x, T - 4, "d")
        for y in range(T - 3, T):
            t.putpixel((x, y), (0, 0, 0, 0))
    if roots:
        for rx in (3, 10):
            if left <= rx < right - 1:
                stamp(t, ROOT, rx, T - 3, wrap=False)


def _cap(t, grid, x=0):
    stamp(t, grid, x, 0, wrap=False)
    return t


def _clear(t, pts):
    for x, y in pts:
        t.putpixel((x, y), (0, 0, 0, 0))


def terrain_templates(variant=0):
    """The 13 template tiles, keyed by name."""
    d = lambda: dirt(variant)  # noqa: E731
    tiles = {}
    tiles["fill"] = d()

    top = d()
    _clear(top, [(x, y) for x in range(T) for y in range(2)])
    tiles["top"] = _cap(top, GRASS_CAP)

    left = d()
    _shade_left(left)
    tiles["left"] = left

    right = d()
    _shade_right(right)
    tiles["right"] = right

    bot = d()
    _shade_bottom(bot)
    tiles["bottom"] = bot

    tl = d()
    _shade_left(tl)
    _clear(tl, [(x, y) for x in range(T) for y in range(2)])
    _cap(tl, GRASS_CAP)
    _clear(tl, [(x, y) for x in range(8) for y in range(8)])
    _cap(tl, GRASS_CAP_L)
    tiles["top_left"] = tl

    tr = d()
    _shade_right(tr)
    _clear(tr, [(x, y) for x in range(T) for y in range(2)])
    _cap(tr, GRASS_CAP)
    _clear(tr, [(x, y) for x in range(8, 16) for y in range(8)])
    _cap(tr, GRASS_CAP_R, 8)
    tiles["top_right"] = tr

    bl = d()
    _shade_left(bl, 0, T - 4)
    _shade_bottom(bl)
    _clear(bl, [(0, T - 4)])
    put(bl, 1, T - 4, "d")
    tiles["bottom_left"] = bl

    br = d()
    _shade_right(br, 0, T - 4)
    _shade_bottom(br)
    _clear(br, [(T - 1, T - 4)])
    tiles["bottom_right"] = br

    # Inner corners: solid tile whose diagonal neighbour is empty.
    itl = d()  # empty up-left: a small grass cap wraps the corner
    stamp(itl, """
GG
gG
hg
jh
.j
""", 0, 0, wrap=False)
    put(itl, 2, 0, "g")
    put(itl, 2, 1, "h")
    put(itl, 3, 0, "j")
    tiles["inner_top_left"] = itl
    itr = d()
    stamp(itr, """
GG
Gg
gh
hj
j.
""", 14, 0, wrap=False)
    put(itr, 13, 0, "g")
    put(itr, 13, 1, "h")
    put(itr, 12, 0, "j")
    tiles["inner_top_right"] = itr
    ibl = d()
    put(ibl, 0, 15, "d")
    put(ibl, 1, 15, "d")
    put(ibl, 0, 14, "d")
    tiles["inner_bottom_left"] = ibl
    ibr = d()
    put(ibr, 15, 15, "d")
    put(ibr, 14, 15, "d")
    put(ibr, 15, 14, "d")
    tiles["inner_bottom_right"] = ibr
    return tiles


# Layout of the 13 templates as an artist would draw them (3x3 island + inner corners).
TEMPLATE_LAYOUT = [
    ["top_left", "top", "top_right", "inner_top_left", "inner_top_right"],
    ["left", "fill", "right", "inner_bottom_left", "inner_bottom_right"],
    ["bottom_left", "bottom", "bottom_right", None, None],
]


def template_sheet(variant=0):
    tl = terrain_templates(variant)
    out = blank(5 * T, 3 * T)
    for j, r in enumerate(TEMPLATE_LAYOUT):
        for i, n in enumerate(r):
            if n:
                paste(out, tl[n], i * T, j * T)
    return out


# ---------------------------------------------------------------------------
# Autotiling by quarters (ch10)
# ---------------------------------------------------------------------------
# For each quarter: which template to take it from, given (vertical neighbour,
# horizontal neighbour, diagonal neighbour) being solid.
QUARTER_RULES = {
    # quarter: (vertical dir, horizontal dir, diagonal dir, outer, v-edge, h-edge, inner)
    "tl": ((0, -1), (-1, 0), (-1, -1), "top_left", "top", "left", "inner_top_left"),
    "tr": ((0, -1), (1, 0), (1, -1), "top_right", "top", "right", "inner_top_right"),
    "bl": ((0, 1), (-1, 0), (-1, 1), "bottom_left", "bottom", "left", "inner_bottom_left"),
    "br": ((0, 1), (1, 0), (1, 1), "bottom_right", "bottom", "right", "inner_bottom_right"),
}
QUARTER_BOX = {"tl": (0, 0), "tr": (8, 0), "bl": (0, 8), "br": (8, 8)}


def quarter_source(solid, x, y, q):
    """Name of the template tile that supplies quarter q of cell (x, y)."""
    vd, hd, dd, outer, vedge, hedge, inner = QUARTER_RULES[q]
    v = solid(x + vd[0], y + vd[1])
    h = solid(x + hd[0], y + hd[1])
    dg = solid(x + dd[0], y + dd[1])
    if not v and not h:
        return outer
    if not v:
        return vedge  # open above/below: the top or bottom edge
    if not h:
        return hedge  # open to the side: the left or right edge
    if not dg:
        return inner
    return "fill"


def blob_index(solid, x, y):
    """8-bit neighbour mask (N=1, NE=2, E=4, SE=8, S=16, SW=32, W=64, NW=128) with
    diagonals ignored unless both adjacent sides are solid -> one of 47 blob tiles."""
    n, e, s, w = solid(x, y - 1), solid(x + 1, y), solid(x, y + 1), solid(x - 1, y)
    m = (n * 1) | (e * 4) | (s * 16) | (w * 64)
    if n and e and solid(x + 1, y - 1):
        m |= 2
    if s and e and solid(x + 1, y + 1):
        m |= 8
    if s and w and solid(x - 1, y + 1):
        m |= 32
    if n and w and solid(x - 1, y - 1):
        m |= 128
    return m


def autotile_cell(templates, solid, x, y):
    out = blank(T, T)
    for q, (qx, qy) in QUARTER_BOX.items():
        src = templates[quarter_source(solid, x, y, q)]
        paste(out, src.crop((qx, qy, qx + 8, qy + 8)), qx, qy)
    return out


def autotile_map(layout, variant_of=None, templates_by_variant=None):
    """layout: list of strings, '#' = terrain. Returns an image. variant_of(x, y) picks
    a dirt variant per cell (adds variety without breaking seams)."""
    from pix import rows as _rows
    if isinstance(layout, str):
        layout = _rows(layout)
    h, w = len(layout), len(layout[0])

    def solid(x, y):
        if x < 0 or x >= w:
            return layout[y][min(max(x, 0), w - 1)] == "#" if 0 <= y < h else False
        if y < 0 or y >= h:
            return y >= h and layout[h - 1][x] == "#"
        return layout[y][x] == "#"

    tv = templates_by_variant or {}
    out = blank(w * T, h * T)
    for y in range(h):
        for x in range(w):
            if layout[y][x] != "#":
                continue
            v = variant_of(x, y) if variant_of else 0
            if v not in tv:
                tv[v] = terrain_templates(v)
            paste(out, autotile_cell(tv[v], solid, x, y), x * T, y * T)
    return out


def blob47(templates=None):
    """All 47 distinct blob tiles generated from the templates, as (mask, image) pairs."""
    templates = templates or terrain_templates(0)
    seen = {}
    for bits in range(256):
        cells = {(0, 0)}
        for k, (dx, dy) in enumerate([(0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1),
                                      (-1, 0), (-1, -1)]):
            if bits >> k & 1:
                cells.add((dx, dy))
        solid = (lambda c: (lambda x, y: (x, y) in c))(cells)
        m = blob_index(solid, 0, 0)
        if m not in seen:
            seen[m] = autotile_cell(templates, solid, 0, 0)
    return sorted(seen.items())


# ---------------------------------------------------------------------------
# Ruins: stone bricks (running bond), moss, background wall
# ---------------------------------------------------------------------------
BRICK = [
    """
2222222522222225
2333333423333334
2333333423333334
2333333423333334
2333333423333334
2333333423333334
4444444544444445
5555555555555555
2225222222252222
3345233333342333
3345233333342333
3345233333342333
3345233333342333
3345233333342333
4445444444454444
5555555555555555
""",
    """
2222222522222225
2333333423333334
2333333423333334
2333334423333334
2333343423333334
2333433423333334
4444444544444445
5555555555555555
2225222222252222
3345233333342333
3345233333442333
3345233334342333
3345233343342333
3345233333342333
4445444444454444
5555555555555555
""",
]
MOSS_CAP = """
................
...G......G.....
.GGGGG..GGGGG.GG
GGgGGGGGGGgGGGGG
gggghggggggghggg
hghh5hgh5hhg5hgh
5h55.5h5.55h.5h5
.5....5.....5...
"""


def brick(variant=0):
    return sprite(rows(BRICK[variant]))


def ruin_top(variant=0):
    """A brick tile with a moss cap (walkable top surface of ruins)."""
    t = brick(variant)
    for x in range(T):
        for y in range(2):
            t.putpixel((x, y), (0, 0, 0, 0))
    stamp(t, MOSS_CAP, 0, 0, wrap=False)
    return t


def _end(t, side):
    x0, x1 = (0, 1) if side == "left" else (T - 1, T - 2)
    for y in range(T):
        if t.getpixel((x0, y))[3]:
            put(t, x0, y, "5")
            if t.getpixel((x1, y))[:3] == rgba("3")[:3]:
                put(t, x1, y, "2" if side == "left" else "4")
    return t


def ruin_set():
    """Ruin platform pieces keyed by name."""
    s = {}
    s["brick"] = brick(0)
    s["brick_cracked"] = brick(1)
    s["top"] = ruin_top(0)
    s["top_left"] = _end(ruin_top(0), "left")
    s["top_right"] = _end(ruin_top(0), "right")
    s["left"] = _end(brick(0), "left")
    s["right"] = _end(brick(0), "right")
    # Corners of the moss cap get rounded off.
    for k, xs in (("top_left", (0, 1)), ("top_right", (15, 14))):
        for y in range(2, 4):
            s[k].putpixel((xs[0], y), (0, 0, 0, 0))
        s[k].putpixel((xs[1], 2), (0, 0, 0, 0))
    return s


BG_WALL_MAP = {"1": "3", "2": "4", "3": "4", "4": "5", "5": "K"}


def bg_wall(variant=0):
    """Background ruin wall: the same bricks pushed back by darkening every value."""
    return recolor(brick(variant), {k: v for k, v in BG_WALL_MAP.items()})


# ---------------------------------------------------------------------------
# Wood: one-way platform (left, middle, right) and a support post
# ---------------------------------------------------------------------------
PLANK = {
    "left": """
.dddddddddddddd
dtttttttttStttt
dccccccccccccdc
dcbcccccccccccc
dbbbbbbbbbbbbbb
.dddddddddddddd
..db.......db..
..db.......db..
...d........d..
""",
    "mid": """
dddddddddddddddd
tttttStttttttttt
cccdcccccccccccd
ccccccccbccccccc
bbbbbbbbbbbbbbbb
dddddddddddddddd
................
................
................
""",
    "right": """
ddddddddddddddd.
ttttttttttttttdd
ccccccccdcccccbd
ccccbccccccccccd
bbbbbbbbbbbbbbbd
ddddddddddddddd.
..db.......db...
..db.......db...
..d.........d...
""",
}


def plank(kind):
    img = blank(T, T)
    g = sprite(rows(PLANK[kind]))
    paste(img, g, 0 if kind != "left" else 1, 0)
    return img


# ---------------------------------------------------------------------------
# Water (animated surface, ch17) and still water fill
# ---------------------------------------------------------------------------
WATER_SURFACE = [
    """
................
................
WW.......WW.....
aaWWa..aaaaWWa..
uuaaauuuuuuaaauu
uuuuuuuuuuuuuuuu
nuuuuuunuuuuuuun
""",
    """
................
................
.WW.......WW....
.aaaWWa..aaaaWWa
uuuuaaauuuuuuuaa
uuuuuuuuuuuuuuuu
uunuuuuuuunuuuuu
""",
    """
................
................
..WW.......WW...
a..aaaWWa..aaaaW
aauuuuuaaauuuuuu
uuuuuuuuuuuuuuuu
uuuuunuuuuuuuunu
""",
    """
................
................
W..WW.......WW..
Wa..aaaaWWa..aaa
uaaauuuuuaaauuuu
uuuuuuuuuuuuuuuu
nuuuuuuunuuuuuuu
""",
]


def water_fill():
    t = blank(T, T, "u")
    stamp(t, "nn", 3, 4)
    stamp(t, "nnn", 10, 11)
    stamp(t, "n", 7, 15)
    for x, y in ((12, 2), (2, 9)):
        stamp(t, "a", x, y)
    return t


def water_top(frame=0):
    t = water_fill()
    for x in range(T):
        for y in range(7):
            t.putpixel((x, y), (0, 0, 0, 0))
    stamp(t, WATER_SURFACE[frame], 0, 0, wrap=False)
    return t
