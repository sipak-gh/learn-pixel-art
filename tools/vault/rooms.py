"""Rooms: 16x15 metatile screens (256x240) composed from layouts.

A layout is 15 strings of 16 characters. Each character names a metatile *recipe*: a base
(backdrop or back wall) plus an optional overlay, rendered with ONE background sub-palette
(legal on the NES because all BG sub-palettes of an area share slot 1, the wall colour).
"""
from __future__ import annotations

from nes import g, gpaste, render, gblank
from pix import blank, paste
from vault import tiles as T
from vault.palettes import AREAS

EMPTY = gblank(16, 16, "0")


def _over(base, top):
    return gpaste(base, top, 0, 0)


def recipes(area: str, seed: int = 0, frame: int = 0) -> dict:
    """char -> (grid or callable(mask, x, y), sub-palette index, solid?)"""
    wall = T.back_wall()
    return {
        " ": (EMPTY, 0, False),
        ".": (wall, 0, False),
        "#": ("ground", 0, True),
        "=": (_over(wall, T.girder()), 2, True),
        "_": (_over(EMPTY, T.girder()), 2, True),
        "v": ("vine", 1, False),
        "g": (T.glass_pane(), 0, False),
        "G": (T.glass_pane(True), 0, False),
        "H": (_over(wall, T.LADDER), 2, False),
        "-": (_over(wall, T.PIPE_H), 2, False),
        "+": (_over(wall, T.PIPE_JOINT), 2, False),
        "|": (_over(wall, T.pipe_v()), 2, False),
        "t": ("tuft", 1, False),
        "T": ("tuft_empty", 1, False),
        "w": (T.water(frame), 1, False),
        "W": (T.water(frame, surface=False), 1, False),
        "r": (gpaste(EMPTY, T.grate(), 0, 0), 2, True),
        "m": (T.molten(frame), 3, False),
        "M": (T.molten(frame, surface=False), 3, False),
        "*": ("stars", 1, False),
        "o": (T.back_grate(), 0, False),
    }


def build(layout, area="greenhouse", seed=0, props=(), frame=0, bands=()):
    """-> (image 256x240, attribute map [[sub]], metatile grids [[grid]])"""
    layout = layout.strip("\n").split("\n") if isinstance(layout, str) else list(layout)
    rec = recipes(area, seed, frame)
    pals = AREAS[area]["bg"]
    hgt, wid = len(layout), len(layout[0])
    from vault.props import PROPS
    over = {}  # (mx, my) -> (16x16 grid, sub)
    for name, mx, my in props:
        grid, subs = PROPS[name]
        gw, gh = len(grid[0]) // 16, len(grid) // 16
        for j in range(gh):
            for i in range(gw):
                over[(mx + i, my + j)] = ([r[i * 16:i * 16 + 16] for r in grid[j * 16:j * 16 + 16]],
                                          subs[j * gw + i])
    for bgrid, bsub, my in bands:  # wide background strips sliced into metatiles
        for j in range(len(bgrid) // 16):
            for i in range(len(bgrid[0]) // 16):
                if layout[my + j][i] == " " and (i, my + j) not in over:
                    over[(i, my + j)] = ([r[i * 16:i * 16 + 16] for r in bgrid[j * 16:j * 16 + 16]], bsub)
    solid = lambda x, y: (0 <= y < hgt and 0 <= x < wid and rec.get(layout[y][x], (0, 0, False))[2]
                          and layout[y][x] == "#") or not (0 <= x < wid) or y >= hgt
    img = blank(wid * 16, hgt * 16)
    attrs, grids = [], []
    for y, rw in enumerate(layout):
        arow, grow = [], []
        for x, ch in enumerate(rw):
            grid, sub, _ = rec[ch]
            if isinstance(grid, list) and grid == rec["."][0]:
                grid = T.back_wall(part=(x % 2) + 2 * (y % 2))
            if grid == "ground":
                m = (T.N if solid(x, y - 1) else 0) | (T.E if solid(x + 1, y) else 0) | \
                    (T.S if solid(x, y + 1) else 0) | (T.W if solid(x - 1, y) else 0)
                grid = T.ground(m, seed + (x * 7 + y * 13) % 4)
            elif grid == "vine":
                grid = _over(T.back_wall(part=(x % 2) + 2 * (y % 2)), T.vine(seed + x * 3 + y))
            elif grid == "tuft":
                grid = _over(T.back_wall(part=(x % 2) + 2 * (y % 2)), T.grass_tuft(seed + x))
            elif grid == "stars":
                grid = T.stars((x * 7 + y * 13) % 6, density=3)
            elif grid == "tuft_empty":
                grid = _over(EMPTY, T.grass_tuft(seed + x))
            if (x, y) in over:
                og, sub = over[(x, y)]
                grid = _over(grid, og)
            paste(img, render(grid, pals[sub], backdrop=True), x * 16, y * 16)
            arow.append(sub)
            grow.append(grid)
        attrs.append(arow)
        grids.append(grow)
    return img, attrs, grids


GREENHOUSE_TEST = """
################
#..g.g.g..g.g..#
#..g.G.g..g.g..#
#v.........v...#
#v...........v.#
#.....tt.....v.#
#....#####.....#
#..............#
#==...........##
#.....|......###
#..t..|..t..####
########-+######
################
################
################
"""
