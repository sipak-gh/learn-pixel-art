"""Background tiles and 16x16 metatiles for `hollow-vault`.

Every metatile is a 16x16 indexed grid (slots '0'..'3'; '0' = backdrop black) drawn with ONE
background sub-palette, because the NES attribute table assigns one sub-palette per 16x16
area. Metatiles are made of four 8x8 tiles; `chr_tiles()` dedupes them like a CHR bank.

Generators are deterministic (seeded) and hand-tuned: textures are placed as small clusters,
never as single noisy pixels, and every exposed edge gets a deliberate treatment (moss rim on
top, a dark lip underneath, a 1 px shadow column on the sides).
"""
from __future__ import annotations

import random

from nes import g, gblank, gpaste, render, gflip

N, E, S, W = 1, 2, 4, 8


def _grid(w=16, h=16, ch="0"):
    return [[ch] * w for _ in range(h)]


def _join(a):
    return ["".join(r) for r in a]


def _set(a, x, y, ch):
    if 0 <= y < len(a) and 0 <= x < len(a[0]):
        a[y][x] = ch


# ---------------------------------------------------------------------------
# Bricks / stone
# ---------------------------------------------------------------------------
STONES = [g("""
3333333332033333
2222222221022222
2222222221022212
2211222221022112
2221222221022222
2222222221022222
1111111111011111
0000000000000000
3332033333333333
2221022222222222
2221022222212222
2221022222112222
2221022222222222
2221022222222222
1111011111111111
0000000000000000
"""), g("""
3333333332033333
2222222221022222
2222212221022222
2222112221022222
2221222221021222
2222222221022222
1111111111011111
0000000000000000
3332033333333333
2221022222222222
2221022112222222
2221022221222222
2221022222222212
2211022222222222
1111011111111111
0000000000000000
"""), g("""
3333333332033333
2222222221022222
2222222221022222
2222222221022222
2222222221022222
2222222221022222
1111111111011111
0000000000000000
3332033333333333
2221022222222222
2221022222222222
2221022222222222
2221022222222222
2221022222222222
1111011111111111
0000000000000000
""")]
DEEP = {"3": "1", "2": "1", "1": "0", "0": "0"}  # ("2" is checkered, see stone())


def stone(seed=0, dark=False):
    a = [list(r) for r in STONES[seed % len(STONES)]]
    if dark:  # interior mass: brick faces become a 50% checker of slot 1 over black
        a = [[("1" if (x + y) % 2 else "0") if c == "2" else DEEP[c] for x, c in enumerate(r)]
             for y, r in enumerate(a)]
    return a


def ground(mask: int, seed=0):
    """Autotiled ground metatile. mask bits N,E,S,W = neighbour is also ground."""
    deep = mask == 15
    a = stone(seed, dark=deep)
    rnd = random.Random(seed * 31 + mask)
    if not mask & N:  # moss rim + drips: bright 1px top line, irregular clusters below
        for x in range(16):
            _set(a, x, 0, "3")
            _set(a, x, 1, "3" if x % 5 not in (1,) else "2")
            _set(a, x, 2, "2")
        for x0 in (rnd.randint(1, 4), rnd.randint(8, 12)):
            ln = rnd.randint(2, 4)
            for y in range(2, 2 + ln):
                _set(a, x0, y, "3" if y < 2 + ln - 1 else "2")
                if y < 3 + ln // 2:
                    _set(a, x0 + 1, y, "2")
        for x in range(16):
            _set(a, x, 3, a[3][x] if a[3][x] in "23" else "1")
    if not mask & S:
        for x in range(16):
            _set(a, x, 15, "0")
            if a[14][x] != "0":
                _set(a, x, 14, "1")
    if not mask & W:
        for y in range(16):
            _set(a, 0, y, "0")
            if a[y][1] == "2":
                _set(a, 1, y, "1" if y > 3 else a[y][1])
        if not mask & N:
            _set(a, 0, 0, "0"); _set(a, 1, 0, "0"); _set(a, 0, 1, "0")
        if not mask & S:
            _set(a, 1, 15, "0"); _set(a, 0, 14, "0")
    if not mask & E:
        for y in range(16):
            _set(a, 15, y, "0")
            if a[y][14] in "23" and y > 2:
                _set(a, 14, y, "1")
        if not mask & N:
            _set(a, 15, 0, "0"); _set(a, 14, 0, "0"); _set(a, 15, 1, "0")
        if not mask & S:
            _set(a, 14, 15, "0"); _set(a, 15, 14, "0")
    return _join(a)


def ground_set(seed=3):
    """The 16 edge-mask metatiles, index = mask."""
    return [ground(m, seed + m) for m in range(16)]


# ---------------------------------------------------------------------------
# Background wall (low value so the play layer pops)
# ---------------------------------------------------------------------------
WALL_PANEL = g("""
1111111111111111111111111111111.
1000000000000000000000000000000.
1011000000000000000000000000110.
1010000000000000000000000000010.
1000000000000000000000000000000.
1000000000000000000000000000000.
1000000000000000000000000000000.
1000000000000000000000000000000.
1000000000000000000000000000000.
1000000000000000000000000000000.
1000001010101010101010101000000.
1000000101010101010101010100000.
1000001010101010101010101000000.
1000000000000000000000000000000.
1000000000000000000000000000000.
1000000000000000000000000000000.
1000000000000000000000000000000.
1000000000000000000000000000000.
1000000000000000000000000000000.
1000000000000000000000000000000.
1000000000000000000000000000000.
1000000000000000000000000000000.
1000000000000000000000000000000.
1000000000000000000000000000000.
1000000000000000000000000000000.
1000000000000000000000000000000.
1000000000000000000000000000000.
1000000000000000000000000000000.
1010000000000000000000000000010.
1011000000000000000000000000110.
1000000000000000000000000000000.
................................
""".replace(".", "0"))


def back_wall(seed=0, part=0):
    """One quarter (part 0..3 = TL, TR, BL, BR) of a 32x32 wall panel: mostly backdrop
    black with a thin slot-1 frame, corner bolts and a vent: reads as a far, dark wall and
    stays legal under any sub-palette (slot 1 is shared by all BG sub-palettes)."""
    x0, y0 = (part % 2) * 16, (part // 2) * 16
    return [r[x0:x0 + 16] for r in WALL_PANEL[y0:y0 + 16]]


def back_grate(seed=0):
    a = _grid()
    for y in range(16):
        for x in range(16):
            a[y][x] = "1" if (x % 4 == 1 or y % 4 == 1) else "0"
    return _join(a)


def glass_pane(broken=False):
    """Greenhouse window: a frame (metal) with dark glass and a diagonal glint."""
    a = _grid()
    for y in range(16):
        for x in range(16):
            if x in (0, 15) or y in (0, 15):
                a[y][x] = "0"
            elif x in (1, 14) or y in (1, 14) or x == 8 or y == 8:
                a[y][x] = "1"
            else:
                a[y][x] = "0"
    for i in range(4):
        _set(a, 3 + i, 6 - i, "2")
        _set(a, 11 + i, 13 - i, "2") if i < 3 else None
    for x in range(2, 14):
        _set(a, x, 1, "2")
    if broken:
        for x, y in ((10, 3), (11, 4), (12, 4), (11, 5), (10, 6), (12, 6), (13, 5)):
            _set(a, x, y, "1")
    return _join(a)


# ---------------------------------------------------------------------------
# Platforms, pipes, ladders
# ---------------------------------------------------------------------------
GIRDER = g("""
3333333333333333
2222222222222222
1200120012001200
1020102010201020
1002100210021002
1111111111111111
0000000000000000
................
................
................
................
................
................
................
................
................
""")


def girder():
    return GIRDER


PIPE_H = g("""
................
................
0000000000000000
1133333333333311
1222222222222221
1222222222222221
1111111111111111
0000000000000000
................
................
................
................
................
................
................
................
""")


def pipe_v():
    return ["".join(col) for col in zip(*PIPE_H)]


PIPE_JOINT = g("""
................
0000000000000000
1333333333333331
2122222222222212
2222222222222222
2122222222222212
1111111111111111
0000000000000000
................
................
................
................
................
................
................
................
""")

LADDER = g("""
.01100000000110.
.0120.....0120..
.0120.....0120..
.01233333331200.
.01211111111200.
.0120.....0120..
.0120.....0120..
.0120.....0120..
.01100000000110.
.0120.....0120..
.0120.....0120..
.01233333331200.
.01211111111200.
.0120.....0120..
.0120.....0120..
.0120.....0120..
""")


# ---------------------------------------------------------------------------
# Plants (BG1)
# ---------------------------------------------------------------------------
def vine(seed=0, length=16):
    """Hanging vine metatile: a 1-2 px stem that wanders, leaves as 3-px clusters."""
    rnd = random.Random(seed)
    a = [["."] * 16 for _ in range(16)]
    x = rnd.randint(5, 10)
    for y in range(length):
        _set(a, x, y, "1")
        _set(a, x + 1, y, "2" if y % 3 else "1")
        if y % 4 == 2:
            side = -1 if (y // 4) % 2 else 1
            lx = x + (2 if side > 0 else -2)
            for dx, dy, ch in ((0, 0, "3"), (side, 0, "2"), (0, 1, "2"), (side, -1, "3"), (2 * side, -1, "2")):
                _set(a, lx + dx, y + dy, ch)
        if rnd.random() < 0.25:
            x += rnd.choice((-1, 1))
            x = max(3, min(11, x))
    return _join(a)


def grass_tuft(seed=0):
    rnd = random.Random(seed)
    a = [["."] * 16 for _ in range(16)]
    for x in range(1, 15):
        h = rnd.choice((1, 2, 2, 3, 4)) if x % 2 else rnd.choice((1, 2))
        for y in range(16 - h, 16):
            _set(a, x, y, "3" if y == 16 - h else "2")
        if h >= 3:
            _set(a, x, 15, "1")
    return _join(a)


# ---------------------------------------------------------------------------
# Tile bookkeeping
# ---------------------------------------------------------------------------
def to_tiles(grid):
    """16x16 grid -> four 8x8 grids (TL, TR, BL, BR)."""
    grid = g(grid)
    return [[r[x:x + 8] for r in grid[y:y + 8]] for y in (0, 8) for x in (0, 8)]


def metatile_img(grid, sub, backdrop=True):
    return render(grid, sub, backdrop=backdrop)


# ---------------------------------------------------------------------------
# Area signatures: water (Cistern), grate + molten glow (Furnace), sky (Ridge)
# ---------------------------------------------------------------------------
def water(frame=0, surface=True):
    """BG1 water: a bright wave crest (animated by shifting 4 px per frame), dithered
    darker body. Surface cells animate; body cells are static."""
    a = _grid()
    for y in range(16):
        for x in range(16):
            a[y][x] = "1" if (x + y) % 2 == 0 and y > 9 else ("2" if y > 3 else "1")
            if y > 12:
                a[y][x] = "1" if (x + y) % 2 == 0 or y > 13 else "2"
    if surface:
        for x in range(16):
            xx = (x + frame * 4) % 16
            crest = [0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0][xx]
            a[0][x] = "0"
            a[1][x] = "3" if crest else "0"
            a[2][x] = "3" if crest or xx in (1, 5, 9, 14) else "2"
            a[3][x] = "2" if not crest or xx in (2, 12) else "3"
            if xx in (7,):
                a[5][x] = "3"
            if xx in (15,):
                a[7][x] = "3"
    else:
        a = [["1" if (x + y) % 2 == 0 else "2" for x in range(16)] for y in range(16)]
        for y in range(16):
            for x in range(16):
                if y > 8:
                    a[y][x] = "1" if (x + y) % 4 else "2"
    return _join(a)


def grate():
    """BG2 floor grate over a glowing pit (Furnace)."""
    a = _grid()
    for x in range(16):
        a[0][x] = "3"
        a[1][x] = "2"
        a[6][x] = "1"
        a[7][x] = "0"
    for y in range(2, 6):
        for x in range(16):
            a[y][x] = "2" if x % 4 in (0, 1) else "0"
            if x % 4 == 1:
                a[y][x] = "1"
    return _join(a) [:8] + ["." * 16] * 8


def molten(frame=0, surface=True):
    """BG3 molten slag. Surface cells: a bright rolling crest (slot 3) over orange (slot 2)
    that shifts 4 px per frame; body cells: dark crust (slot 1) with a few glowing cracks."""
    a = _grid(ch="1")
    if surface:
        for x in range(16):
            xx = (x + frame * 4) % 16
            crest = [1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1][xx]
            a[0][x] = "3" if crest else "0"
            a[1][x] = "3" if crest or xx in (3, 11) else "2"
            for y in range(2, 6):
                a[y][x] = "2"
            a[6][x] = "2" if (x + frame) % 2 else "1"
            a[7][x] = "1" if (x + frame) % 4 else "2"
        cracks = [(3, 10), (4, 10), (5, 11), (11, 13), (12, 13), (12, 12)]
    else:
        cracks = [(2, 3), (3, 3), (4, 4), (9, 8), (10, 8), (10, 9), (11, 10), (5, 13), (6, 13)]
    for x, y in cracks:
        a[y][x] = "2"
    return _join(a)


def stars(seed=0, density=6):
    """BG1 night sky: mostly black, a few 1 px stars and one 'twinkle' cross."""
    import random as _r
    rnd = _r.Random(seed)
    a = _grid()
    for _ in range(density):
        x, y = rnd.randrange(16), rnd.randrange(16)
        a[y][x] = rnd.choice("1123")
    if seed % 5 == 0:
        x, y = rnd.randrange(3, 13), rnd.randrange(3, 13)
        for dx, dy in ((0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)):
            a[y + dy][x + dx] = "3" if (dx, dy) == (0, 0) else "2"
    return _join(a)
