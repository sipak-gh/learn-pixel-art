"""Shared helpers for the Part IV style chapters: the Greenhouse slice every style re-draws,
and *designed* slot mappings (vault art is stored as slot grids '0'-'3', so a style is mostly
a deliberate mapping slot -> colour/pattern per material) vs naive luminance conversion."""
from __future__ import annotations

from PIL import Image

from vault import rooms, kit, creatures

SLICE = """
################
#..g.g.g..g.g..#
#..g.G.g..g.g..#
#v.....v.......#
#v..........v..#
#...........v..#
#....######....#
#..............#
#==..........###
#.....|.....####
#.....|.t..#####
########-+######
################
################
################
"""
SLICE_PROPS = [("lamp", 4, 8), ("planter", 2, 10), ("fern", 2, 9), ("terminal", 9, 10),
               ("pod", 7, 4), ("lamp", 12, 4)]


def slice_build(area="greenhouse"):
    return rooms.build(SLICE, area, props=SLICE_PROPS)


def lum(c):
    return 0.299 * c[0] + 0.587 * c[1] + 0.114 * c[2]


def naive_threshold(img, colors):
    """'Avoid' conversion: each pixel -> the colour whose luminance band it falls in."""
    out = Image.new("RGBA", img.size)
    src, dst = img.load(), out.load()
    cols = sorted(colors, key=lum)
    n = len(cols)
    for y in range(img.height):
        for x in range(img.width):
            r, g, b, a = src[x, y]
            if a:
                dst[x, y] = tuple(cols[min(n - 1, int(lum((r, g, b)) / 256 * n))]) + (255,)
    return out


def map_grid(grid, mapping, ox=0, oy=0):
    """Slot grid -> RGBA. mapping: slot -> colour | ('checker', a, b) | ('dots', a, b, step).
    ox/oy align patterns to the screen rather than the tile."""
    im = Image.new("RGBA", (len(grid[0]), len(grid)))
    px = im.load()
    for y, r in enumerate(grid):
        for x, ch in enumerate(r):
            m = mapping.get(ch)
            if m is None:
                continue
            X, Y = x + ox, y + oy
            if m[0] == "checker":
                m = m[1] if (X + Y) % 2 == 0 else m[2]
            elif m[0] == "dots":
                m = m[1] if (X + Y) % m[3] == 0 else m[2]
            px[x, y] = tuple(m) + (255,)
    return im


def room_mapped(grids, fg_map, bg_map, layout=SLICE, mass="#"):
    rows_ = layout.strip("\n").split("\n")
    h, w = len(grids), len(grids[0])
    out = Image.new("RGBA", (w * 16, h * 16))
    for y in range(h):
        for x in range(w):
            m = fg_map if rows_[y][x] in mass else bg_map
            out.alpha_composite(map_grid(grids[y][x], m, x * 16, y * 16), (x * 16, y * 16))
    return out


def kit_grid(**pose):
    return kit.kit(**pose)


def creature_grid(kind="hopper"):
    anim = list(creatures.CREATURES[kind][1])[0]
    return creatures.grids(kind, anim)[0]
