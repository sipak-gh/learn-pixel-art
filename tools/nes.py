"""NES-style helpers for the `hollow-vault` project.

Art is stored as *indexed grids*: lists of strings whose characters are palette slots, the way
the NES stores 2-bit tiles.

    '.'  transparent (sprites) / backdrop (backgrounds: drawn with slot 0)
    '0'  slot 0 (the shared backdrop colour, black $0F in this project)
    '1' '2' '3'  slots 1..3 of the 4-colour sub-palette

A sub-palette is a tuple of four NES colour indices, e.g. (0x0F, 0x07, 0x17, 0x27). Rendering
a grid with a different sub-palette is a palette swap, exactly as on the hardware.

Constraint checkers (colours per tile, attribute areas, sprites per scanline, unique tiles)
report problems instead of silently drawing illegal art; figures print their results.
"""
from __future__ import annotations

import os
import random

from pix import Image, blank, rgba, rows, hex2rgb

# ---------------------------------------------------------------------------
# The master palette: Lospec "Nintendo Entertainment System" (55 colours), arranged by
# hardware index $00-$3F. https://lospec.com/palette-list/nintendo-entertainment-system
# Unused/duplicate black entries ($0D-$0F, $1D-$1F, $2E-$2F, $3E-$3F) map to 000000.
# ---------------------------------------------------------------------------
_NES_HEX = """
7c7c7c 0000fc 0000bc 4428bc 940084 a80020 a81000 881400 503000 007800 006800 005800 004058 000000 000000 000000
bcbcbc 0078f8 0058f8 6844fc d800cc e40058 f83800 e45c10 ac7c00 00b800 00a800 00a844 008888 000000 000000 000000
f8f8f8 3cbcfc 6888fc 9878f8 f878f8 f85898 f87858 fca044 f8b800 b8f818 58d854 58f898 00e8d8 787878 000000 000000
fcfcfc a4e4fc b8b8f8 d8b8f8 f8b8f8 f8a4c0 f0d0b0 fce0a8 f8d878 d8f878 b8f8b8 b8f8d8 00fcfc f8d8f8 000000 000000
""".split()
NES = [hex2rgb(h) for h in _NES_HEX]                       # index -> rgb
NES_HEX = list(_NES_HEX)
BLACK = 0x0F
USABLE = [i for i in range(64) if i not in (0x0D, 0x0E, 0x1D, 0x1E, 0x1F, 0x2E, 0x2F, 0x3E, 0x3F)]
# 0x0F is the canonical black; the other black slots are left out of USABLE.
# Lospec order (the order the .hex file lists colours) - for palette files:
LOSPEC_ORDER = [0x0F, 0x30, 0x20, 0x10, 0x00, 0x31, 0x21, 0x11, 0x01, 0x32, 0x22, 0x12, 0x02,
                0x33, 0x23, 0x13, 0x03, 0x34, 0x24, 0x14, 0x04, 0x35, 0x25, 0x15, 0x05,
                0x36, 0x26, 0x16, 0x06, 0x37, 0x27, 0x17, 0x07, 0x38, 0x28, 0x18, 0x08,
                0x39, 0x29, 0x19, 0x09, 0x3A, 0x2A, 0x1A, 0x0A, 0x3B, 0x2B, 0x1B, 0x0B,
                0x3C, 0x2C, 0x1C, 0x0C, 0x3D, 0x2D]


def nes(i: int) -> tuple[int, int, int, int]:
    return NES[i] + (255,)


def nhex(i: int) -> str:
    return "$%02X" % i


def pal_rgba(sub) -> list:
    return [nes(i) for i in sub]


# ---------------------------------------------------------------------------
# Indexed grids
# ---------------------------------------------------------------------------
def g(text) -> list[str]:
    """Triple-quoted block -> rows (blank-edged, dedented, padded with '.')."""
    return rows(text) if isinstance(text, str) else list(text)


def render(grid, sub, backdrop=False) -> Image.Image:
    """Indexed grid + sub-palette (4 NES indices) -> RGBA. '.' is transparent unless
    backdrop=True (then '.' is drawn with slot 0, as background tiles are)."""
    grid = g(grid)
    cols = pal_rgba(sub)
    h, w = len(grid), max(len(r) for r in grid)
    img = Image.new("RGBA", (w, h), cols[0] if backdrop else (0, 0, 0, 0))
    px = img.load()
    for y, r in enumerate(grid):
        for x, ch in enumerate(r):
            if ch in "0123":
                px[x, y] = cols[int(ch)]
            elif ch != ".":
                raise ValueError(f"bad slot {ch!r} at {x},{y}")
    return img


def gflip(grid) -> list[str]:
    return [r[::-1] for r in g(grid)]


def gvflip(grid) -> list[str]:
    return list(reversed(g(grid)))


def gsize(grid):
    grid = g(grid)
    return max(len(r) for r in grid), len(grid)


def gblank(w, h, ch=".") -> list[str]:
    return [ch * w for _ in range(h)]


def gpaste(dst, src, x, y, transparent=True) -> list[str]:
    """Return dst with src pasted at x, y ('.' in src is skipped if transparent)."""
    out = [list(r) for r in g(dst)]
    for j, r in enumerate(g(src)):
        for i, ch in enumerate(r):
            yy, xx = y + j, x + i
            if 0 <= yy < len(out) and 0 <= xx < len(out[yy]) and (ch != "." or not transparent):
                out[yy][xx] = ch
    return ["".join(r) for r in out]


def gshift(grid, dx, dy) -> list[str]:
    w, h = gsize(grid)
    return gpaste(gblank(w, h), grid, dx, dy)


def gmap(grid, mapping: dict) -> list[str]:
    """Remap slots, e.g. {'3': '2'}."""
    return ["".join(mapping.get(c, c) for c in r) for r in g(grid)]


def gcrop(grid, x, y, w, h) -> list[str]:
    return [r[x:x + w].ljust(w, ".") for r in g(grid)[y:y + h]]


def tiles_of(grid, tw=8, th=8) -> list:
    """Cut a grid into tw x th tiles, row-major."""
    w, h = gsize(grid)
    return [gcrop(grid, x, y, tw, th) for y in range(0, h, th) for x in range(0, w, tw)]


# ---------------------------------------------------------------------------
# Constraint checkers
# ---------------------------------------------------------------------------
def colours_in(img: Image.Image, box=None, ignore_alpha=True) -> set:
    im = img.crop(box) if box else img
    out = set()
    for c in im.getdata():
        if ignore_alpha and c[3] == 0:
            continue
        out.add(c[:3])
    return out


def check_tiles(img: Image.Image, tw=8, th=8, limit=4, backdrop=None) -> list:
    """List of (x, y, n) for tiles with more than `limit` colours (the backdrop counts once
    for every tile, as on hardware; transparent pixels are ignored for sprites)."""
    bad = []
    for y in range(0, img.height, th):
        for x in range(0, img.width, tw):
            cs = colours_in(img, (x, y, x + tw, y + th))
            if backdrop is not None:
                cs.add(tuple(backdrop[:3]))
            if len(cs) > limit:
                bad.append((x, y, len(cs)))
    return bad


def check_attributes(img: Image.Image, subpals, area=16) -> list:
    """Every `area` x `area` block must fit inside ONE of the given sub-palettes.
    Returns a list of (x, y, colours-not-covered)."""
    sets = [set(NES[i] for i in sp) for sp in subpals]
    bad = []
    for y in range(0, img.height, area):
        for x in range(0, img.width, area):
            cs = colours_in(img, (x, y, x + area, y + area))
            if not any(cs <= s for s in sets):
                bad.append((x, y, len(cs)))
    return bad


def attribute_map(img: Image.Image, subpals, area=16) -> list[list[int]]:
    """Which sub-palette each area uses (first that fits; -1 if none)."""
    sets = [set(NES[i] for i in sp) for sp in subpals]
    out = []
    for y in range(0, img.height, area):
        rw = []
        for x in range(0, img.width, area):
            cs = colours_in(img, (x, y, x + area, y + area))
            rw.append(next((n for n, s in enumerate(sets) if cs <= s), -1))
        out.append(rw)
    return out


def sprite_tiles(objects, tile_h=8) -> list:
    """objects: (x, y, w, h) boxes of sprites/metasprites in screen pixels. Returns the list
    of 8 x tile_h hardware sprites (x, y) they decompose into."""
    out = []
    for x, y, w, h in objects:
        for ty in range(0, h, tile_h):
            for tx in range(0, w, 8):
                out.append((x + tx, y + ty))
    return out


def scanline_counts(objects, height=240, tile_h=8) -> list[int]:
    """Number of hardware sprites on every scanline (limit 8)."""
    counts = [0] * height
    for x, y, in sprite_tiles(objects, tile_h):
        for yy in range(max(0, y), min(height, y + tile_h)):
            counts[yy] += 1
    return counts


def unique_tiles(img: Image.Image, tw=8, th=8, flips=False) -> int:
    seen = set()
    for y in range(0, img.height, th):
        for x in range(0, img.width, tw):
            t = img.crop((x, y, x + tw, y + th))
            keys = [t.tobytes()]
            if flips:
                f = t.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
                keys += [f.tobytes(), t.transpose(Image.Transpose.FLIP_TOP_BOTTOM).tobytes(),
                         f.transpose(Image.Transpose.FLIP_TOP_BOTTOM).tobytes()]
            if not any(k in seen for k in keys):
                seen.add(keys[0])
    return len(seen)


def tile_set(img: Image.Image, tw=8, th=8) -> list:
    """Unique tiles (as images) in first-seen order."""
    seen, out = set(), []
    for y in range(0, img.height, th):
        for x in range(0, img.width, tw):
            t = img.crop((x, y, x + tw, y + th))
            k = t.tobytes()
            if k not in seen:
                seen.add(k)
                out.append(t)
    return out


def report(img, subpals=None, backdrop=None, objects=None, name="") -> str:
    """One-line constraint report used in figure notes and project READMEs."""
    parts = []
    parts.append(f"tiles over 4 colours: {len(check_tiles(img, backdrop=backdrop))}")
    if subpals:
        parts.append(f"attribute errors: {len(check_attributes(img, subpals))}")
    parts.append(f"unique 8x8 tiles: {unique_tiles(img)}")
    if objects:
        parts.append(f"max sprites/scanline: {max(scanline_counts(objects, img.height))}")
    return (name + ": " if name else "") + ", ".join(parts)


# ---------------------------------------------------------------------------
# Palette files
# ---------------------------------------------------------------------------
def write_nes_palette_files(dirpath: str, name="nes") -> None:
    """name.hex (Lospec order, 55 colours), name.gpl (hardware order, labelled $xx) and
    name.png (1 px per colour, Lospec order) and name-grid.png (16 x 4 hardware layout)."""
    os.makedirs(dirpath, exist_ok=True)
    with open(os.path.join(dirpath, name + ".hex"), "w") as f:
        f.write("\n".join(NES_HEX[i] for i in LOSPEC_ORDER) + "\n")
    with open(os.path.join(dirpath, name + ".gpl"), "w") as f:
        f.write("GIMP Palette\nName: NES (Lospec 'Nintendo Entertainment System')\nColumns: 16\n#\n")
        for i in [0x0F] + [i for i in USABLE if i != 0x0F]:
            r, gg, b = NES[i]
            f.write(f"{r:3d} {gg:3d} {b:3d}\t{nhex(i)}\n")
    strip = Image.new("RGBA", (len(LOSPEC_ORDER), 1))
    for n, i in enumerate(LOSPEC_ORDER):
        strip.putpixel((n, 0), nes(i))
    strip.save(os.path.join(dirpath, name + ".png"))
    gridimg = Image.new("RGBA", (16, 4))
    for i in range(64):
        gridimg.putpixel((i % 16, i // 16), nes(i))
    gridimg.save(os.path.join(dirpath, name + "-grid.png"))


def write_subpalettes(path: str, area: dict) -> None:
    """A sub-palette set as a tiny .gpl (16 entries: BG0..BG3 then SP0..SP3 would be 32;
    we write BG and SP sets as 4 x 4 rows)."""
    with open(path, "w") as f:
        f.write(f"GIMP Palette\nName: {area['name']}\nColumns: 4\n#\n")
        for kind in ("bg", "spr"):
            for n, sp in enumerate(area[kind]):
                for s, i in enumerate(sp):
                    r, gg, b = NES[i]
                    f.write(f"{r:3d} {gg:3d} {b:3d}\t{kind.upper()}{n}.{s} {nhex(i)}\n")


# ---------------------------------------------------------------------------
# Dithering / quantising helpers (Part IV)
# ---------------------------------------------------------------------------
BAYER2 = [[0, 2], [3, 1]]
BAYER4 = [[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]]


def bayer(n: int) -> list[list[int]]:
    """Bayer index matrix of size n (power of two)."""
    m = [[0]]
    while len(m) < n:
        s = len(m)
        m = [[4 * m[y % s][x % s] + [[0, 2], [3, 1]][y // s][x // s] for x in range(2 * s)]
             for y in range(2 * s)]
    return m


def blue_noise(w: int, h: int, seed: int = 7) -> list[list[float]]:
    """A cheap, deterministic blue-ish noise threshold map in [0, 1): a jittered best-
    candidate ranking (good enough for figures; not a true void-and-cluster)."""
    rnd = random.Random(seed)
    n = w * h
    order = []
    taken = [[False] * w for _ in range(h)]
    pts = []
    for k in range(n):
        best, bd = None, -1
        tries = 6 if k < n - 1 else 1
        cands = []
        while len(cands) < tries:
            x, y = rnd.randrange(w), rnd.randrange(h)
            if not taken[y][x]:
                cands.append((x, y))
            if k > n - 40:  # finish deterministically
                cands = [(x, y) for y in range(h) for x in range(w) if not taken[y][x]][:tries]
                break
        for (x, y) in cands:
            d = min(((min(abs(x - px), w - abs(x - px))) ** 2 + (min(abs(y - py), h - abs(y - py))) ** 2
                     for px, py in pts[-64:]), default=1e9)
            if d > bd:
                best, bd = (x, y), d
        taken[best[1]][best[0]] = True
        pts.append(best)
        order.append(best)
    out = [[0.0] * w for _ in range(h)]
    for r, (x, y) in enumerate(order):
        out[y][x] = r / n
    return out


def threshold_map(img: Image.Image, matrix, levels=2, colors=None, lum=None) -> Image.Image:
    """Ordered dither of a greyscale-ish image to `levels` colours using an index matrix
    (Bayer ints or a float map). colors: list of rgb from dark to light."""
    colors = colors or [(0, 0, 0), (255, 255, 255)]
    mh, mw = len(matrix), len(matrix[0])
    mx = max(max(r) for r in matrix)
    norm = (lambda v: (v + 0.5) / (mx + 1)) if isinstance(matrix[0][0], int) else (lambda v: v)
    out = Image.new("RGBA", img.size)
    src = img.convert("RGBA").load()
    dst = out.load()
    for y in range(img.height):
        for x in range(img.width):
            r, gg, b, a = src[x, y]
            v = (0.299 * r + 0.587 * gg + 0.114 * b) / 255 if lum is None else lum(src[x, y])
            t = norm(matrix[y % mh][x % mw])
            q = v * (levels - 1)
            lo = int(q)
            n = min(levels - 1, lo + (1 if q - lo > t else 0))
            dst[x, y] = tuple(colors[n]) + (255 if a else 0,)
    return out


def quantize_to(img: Image.Image, colors) -> Image.Image:
    """Nearest-luma mapping onto a ramp of colours (dark -> light), no dithering."""
    out = Image.new("RGBA", img.size)
    src = img.convert("RGBA").load()
    dst = out.load()
    lums = [0.299 * c[0] + 0.587 * c[1] + 0.114 * c[2] for c in colors]
    for y in range(img.height):
        for x in range(img.width):
            r, gg, b, a = src[x, y]
            v = 0.299 * r + 0.587 * gg + 0.114 * b
            n = min(range(len(colors)), key=lambda i: abs(lums[i] - v))
            dst[x, y] = tuple(colors[n][:3]) + (a,)
    return out


def remap(img: Image.Image, mapping: dict) -> Image.Image:
    """Exact colour remap {rgb: rgb}; colours not in the map are kept."""
    out = img.copy()
    px = out.load()
    for y in range(out.height):
        for x in range(out.width):
            c = px[x, y]
            if c[3] and c[:3] in mapping:
                px[x, y] = tuple(mapping[c[:3]][:3]) + (c[3],)
    return out


# ---------------------------------------------------------------------------
# A tiny indexed canvas for building sprites from spans + an automatic outline
# ---------------------------------------------------------------------------
class ICanvas:
    """Indexed drawing surface. Draw interiors with spans/px, then outline() adds a 1 px
    outline (slot '1' by default) around everything, then draw interior details."""

    def __init__(self, w=16, h=24):
        self.w, self.h = w, h
        self.a = [["."] * w for _ in range(h)]

    def span(self, y, x0, x1, ch="2"):
        for x in range(min(x0, x1), max(x0, x1) + 1):
            if 0 <= x < self.w and 0 <= y < self.h:
                self.a[y][x] = ch

    def spans(self, d: dict, ch="2", dx=0, dy=0):
        for y, v in d.items():
            for (x0, x1) in (v if isinstance(v, list) else [v]):
                self.span(y + dy, x0 + dx, x1 + dx, ch)

    def px(self, pts, ch, dx=0, dy=0):
        for x, y in pts:
            x, y = x + dx, y + dy
            if 0 <= x < self.w and 0 <= y < self.h:
                self.a[y][x] = ch

    def get(self, x, y):
        return self.a[y][x] if 0 <= x < self.w and 0 <= y < self.h else "."

    def outline(self, ch="1", diag=False):
        b = [r[:] for r in self.a]
        nb = [(1, 0), (-1, 0), (0, 1), (0, -1)] + ([(1, 1), (1, -1), (-1, 1), (-1, -1)] if diag else [])
        for y in range(self.h):
            for x in range(self.w):
                if self.a[y][x] == "." and any(self.get(x + i, y + j) not in (".", ch) for i, j in nb):
                    b[y][x] = ch
        self.a = b

    def paste(self, grid, x, y):
        for j, r in enumerate(g(grid)):
            for i, ch in enumerate(r):
                if ch != ".":
                    self.px([(x + i, y + j)], ch)

    def grid(self):
        return ["".join(r) for r in self.a]
