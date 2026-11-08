"""Status bar (HUD) for `hollow-vault`: a 256x32 black strip (two metatile rows) drawn with
background tiles. On hardware the HUD sits above a scroll split, so the playfield below can
scroll while the bar stays put. Glyphs are 8x8 tiles (3 colours + backdrop)."""
from __future__ import annotations

from nes import gblank, gpaste, render

# 5x7 glyphs inside 8x8 cells; '3' = face, '1' = drop shadow added automatically
_FONT = {
    "0": ".333.|3...3|3..33|3.3.3|33..3|3...3|.333.", "1": "..3..|.33..|..3..|..3..|..3..|..3..|.333.",
    "2": ".333.|3...3|....3|..33.|.3...|3....|33333", "3": "3333.|....3|....3|.333.|....3|....3|3333.",
    "4": "...3.|..33.|.3.3.|3..3.|33333|...3.|...3.", "5": "33333|3....|3333.|....3|....3|3...3|.333.",
    "6": "..33.|.3...|3....|3333.|3...3|3...3|.333.", "7": "33333|....3|...3.|..3..|.3...|.3...|.3...",
    "8": ".333.|3...3|3...3|.333.|3...3|3...3|.333.", "9": ".333.|3...3|3...3|.3333|....3|...3.|.33..",
    "A": ".333.|3...3|3...3|33333|3...3|3...3|3...3", "C": ".333.|3...3|3....|3....|3....|3...3|.333.",
    "D": "3333.|3...3|3...3|3...3|3...3|3...3|3333.", "E": "33333|3....|3....|3333.|3....|3....|33333",
    "F": "33333|3....|3....|3333.|3....|3....|3....", "G": ".333.|3...3|3....|3.333|3...3|3...3|.3333",
    "H": "3...3|3...3|3...3|33333|3...3|3...3|3...3", "I": ".333.|..3..|..3..|..3..|..3..|..3..|.333.",
    "K": "3...3|3..3.|3.3..|33...|3.3..|3..3.|3...3", "L": "3....|3....|3....|3....|3....|3....|33333",
    "N": "3...3|33..3|3.3.3|3.3.3|3..33|3...3|3...3", "O": ".333.|3...3|3...3|3...3|3...3|3...3|.333.",
    "R": "3333.|3...3|3...3|3333.|3.3..|3..3.|3...3", "S": ".3333|3....|3....|.333.|....3|....3|3333.",
    "T": "33333|..3..|..3..|..3..|..3..|..3..|..3..", "U": "3...3|3...3|3...3|3...3|3...3|3...3|.333.",
    "V": "3...3|3...3|3...3|3...3|3...3|.3.3.|..3..", "W": "3...3|3...3|3...3|3.3.3|3.3.3|33.33|3...3",
    "X": "3...3|3...3|.3.3.|..3..|.3.3.|3...3|3...3", "Y": "3...3|3...3|.3.3.|..3..|..3..|..3..|..3..",
    "x": ".....|.....|3...3|.3.3.|..3..|.3.3.|3...3", " ": ".....|.....|.....|.....|.....|.....|.....",
    "-": ".....|.....|.....|.333.|.....|.....|.....",
}


def glyph(ch):
    rows = [list("." * 8) for _ in range(8)]
    for y, r in enumerate(_FONT[ch].split("|")):
        for x, c in enumerate(r):
            if c == "3":
                rows[y][x + 1] = "3"
                if rows[y + 1][x + 2] == ".":
                    rows[y + 1][x + 2] = "1"
    return ["".join(r) for r in rows]


HEART = ["........", ".22.22..", "2332222.", "2322222.", "2222222.", ".22222..", "..222...", "...2...."]
HEART_EMPTY = ["........", ".22.22..", "2..2..2.", "2.....2.", "2.....2.", ".2...2..", "..2.2...", "...2...."]
SEED = ["........", "...33...", "..3223..", ".322223.", ".322221.", ".322221.", "..1221..", "...11..."]
LANTERN = ["...11...", "..1..1..", ".111111.", ".133331.", ".133331.", ".122221.", ".111111.", "........"]


def text_grid(s):
    out = gblank(8 * len(s), 8, ".")
    for i, ch in enumerate(s):
        out = gpaste(out, glyph(ch), i * 8, 0)
    return out


def hud(hp=3, hp_max=4, seeds=7, area="GREENHOUSE", oil=5):
    """-> 256x32 grid using one sub-palette (slot 1 shadow, 2 accent, 3 face)."""
    g = gblank(256, 32, "0")
    g = gpaste(g, text_grid(f"x{seeds:02d}"), 66, 12)
    g = gpaste(g, LANTERN, 98, 12)
    for i in range(6):  # oil meter
        for y in range(14, 19):
            for x in range(108 + i * 5, 112 + i * 5):
                g[y] = g[y][:x] + ("2" if i < oil else "1") + g[y][x + 1:]
    name = text_grid(area.upper())
    g = gpaste(g, name, 240 - len(name[0]), 12)
    g = gpaste(g, gblank(256, 1, "1"), 0, 30)  # divider line
    return [r.replace(".", "0") for r in g]


def hud_img(sub, **kw):
    return render(hud(**kw), sub, backdrop=True)


def hud_sprites(kit_pal, fx_pal, hp=3, hp_max=4, **_):
    """Hearts and the seed icon are 8x8 *sprites* (so they can be red/yellow whatever the
    area's background palettes are): 5 sprites on the HUD scanlines, well under 8.
    -> [(img, x, y)]"""
    out = [(render(HEART if i < hp else HEART_EMPTY, kit_pal), 16 + i * 9, 12) for i in range(hp_max)]
    out.append((render(SEED, fx_pal), 56, 12))
    return out
