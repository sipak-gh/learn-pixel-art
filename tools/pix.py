"""pix.py - a tiny, reproducible pixel-art figure toolkit (Pillow only).

Sprites are written as text grids: one character per pixel, '.' is transparent.
Characters map to the ENDESGA 32 palette through LEGEND (see PALETTE_NAMES below).
Everything is drawn at 1x and enlarged with nearest-neighbour integer scaling.

Run any script with:
    uv run --no-project --python 3.12 --with pillow==13.0.0 python tools/figures/ch01_x.py
"""
from __future__ import annotations

import json
import math
import os
import textwrap
from dataclasses import dataclass

from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMAGES = os.path.join(ROOT, "images")
PROJECT = os.path.join(ROOT, "project")

# ---------------------------------------------------------------------------
# Palette: ENDESGA 32 by ENDESGA (https://lospec.com/palette-list/endesga-32)
# ---------------------------------------------------------------------------
# (code, name, hex) in the palette's original order.
PALETTE_NAMES = [
    ("r", "rust", "be4a2f"),
    ("O", "copper", "d77643"),
    ("S", "sand", "ead4aa"),
    ("t", "tan", "e4a672"),
    ("c", "clay", "b86f50"),
    ("b", "brown", "733e39"),
    ("d", "umber", "3e2731"),
    ("m", "crimson", "a22633"),
    ("R", "red", "e43b44"),
    ("o", "orange", "f77622"),
    ("y", "gold", "feae34"),
    ("Y", "yellow", "fee761"),
    ("G", "leaf", "63c74d"),
    ("g", "green", "3e8948"),
    ("h", "pine", "265c42"),
    ("j", "deep", "193c3e"),
    ("n", "navy", "124e89"),
    ("u", "blue", "0099db"),
    ("a", "aqua", "2ce8f5"),
    ("W", "white", "ffffff"),
    ("1", "grey1", "c0cbdc"),
    ("2", "grey2", "8b9bb4"),
    ("3", "grey3", "5a6988"),
    ("4", "grey4", "3a4466"),
    ("5", "grey5", "262b44"),
    ("K", "ink", "181425"),
    ("X", "hot", "ff0044"),
    ("p", "plum", "68386c"),
    ("P", "mauve", "b55088"),
    ("k", "salmon", "f6757a"),
    ("f", "skin", "e8b796"),
    ("F", "skin2", "c28569"),
]


def hex2rgb(h: str) -> tuple[int, int, int]:
    h = h.lstrip("#")
    return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))


PAL = {name: hex2rgb(hx) for _, name, hx in PALETTE_NAMES}  # name -> rgb
PAL_LIST = [hex2rgb(hx) for _, _, hx in PALETTE_NAMES]  # palette order
LEGEND = {code: hex2rgb(hx) + (255,) for code, _, hx in PALETTE_NAMES}  # char -> rgba
LEGEND["."] = (0, 0, 0, 0)
LEGEND[" "] = (0, 0, 0, 0)
CODE_OF = {name: code for code, name, _ in PALETTE_NAMES}  # name -> char

# Ramps used throughout the course (dark -> light).
RAMPS = {
    "stone": ["K", "5", "4", "3", "2", "1", "W"],
    "earth": ["d", "b", "c", "t", "S"],
    "foliage": ["j", "h", "g", "G", "Y"],
    "fire": ["m", "r", "o", "y", "Y"],
    "water": ["5", "n", "u", "a", "W"],
    "skin": ["b", "F", "f", "S"],
    "magic": ["5", "p", "P", "k", "S"],
}

# Figure styling (outside the art itself).
FIG_BG = (36, 36, 44)
FIG_FG = (232, 232, 238)
FIG_DIM = (150, 150, 165)
FIG_BAD = (255, 92, 92)
FIG_GOOD = (110, 214, 120)
GRID_LINE = (0, 0, 0, 60)
CHECK_A = (58, 58, 70)
CHECK_B = (70, 70, 84)


# ---------------------------------------------------------------------------
# Grids -> images
# ---------------------------------------------------------------------------
def rows(text: str) -> list[str]:
    """Turn a triple-quoted block into grid rows (dedent, drop blank edge lines).

    Use '|' at the end of a row if you need to keep trailing transparency visible
    in your editor; it is stripped."""
    lines = textwrap.dedent(text).strip("\n").split("\n")
    out = [ln.rstrip().rstrip("|") for ln in lines]
    width = max(len(r) for r in out)
    return [r.ljust(width, ".") for r in out]


def sprite(grid, legend: dict | None = None) -> Image.Image:
    """Grid (str or list of rows) -> RGBA image at 1x. Unknown chars raise."""
    if isinstance(grid, str):
        grid = rows(grid)
    lg = dict(LEGEND)
    if legend:
        for k, v in legend.items():
            lg[k] = rgba(v)
    h, w = len(grid), max(len(r) for r in grid)
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    px = img.load()
    for y, r in enumerate(grid):
        for x, ch in enumerate(r):
            if ch not in lg:
                raise ValueError(f"unknown pixel code {ch!r} at {x},{y}")
            px[x, y] = lg[ch]
    return img


def to_grid(img: Image.Image) -> list[str]:
    """Inverse of sprite(): RGBA image -> rows using LEGEND codes (for debugging)."""
    inv = {v[:3]: k for k, v in LEGEND.items() if v[3] == 255}
    px = img.convert("RGBA").load()
    out = []
    for y in range(img.height):
        out.append("".join("." if px[x, y][3] == 0 else inv.get(px[x, y][:3], "?")
                           for x in range(img.width)))
    return out


def blank(w: int, h: int, color=None) -> Image.Image:
    if color is None:
        return Image.new("RGBA", (w, h), (0, 0, 0, 0))
    return Image.new("RGBA", (w, h), rgba(color))


def rgba(c) -> tuple[int, int, int, int]:
    """Accept a LEGEND code, a palette name, a hex string or an rgb(a) tuple."""
    if isinstance(c, str):
        if c in LEGEND:
            return LEGEND[c]
        if c in PAL:
            return PAL[c] + (255,)
        return hex2rgb(c) + (255,)
    return tuple(c) + ((255,) if len(c) == 3 else ())


def paste(dst: Image.Image, src: Image.Image, x: int, y: int) -> Image.Image:
    """Alpha-composite src onto dst at (x, y) in place, clipping at the edges."""
    sx, sy = max(0, -x), max(0, -y)
    ex, ey = min(src.width, dst.width - x), min(src.height, dst.height - y)
    if ex > sx and ey > sy:
        dst.alpha_composite(src.crop((sx, sy, ex, ey)), (x + sx, y + sy))
    return dst


def flip(img: Image.Image) -> Image.Image:
    return img.transpose(Image.Transpose.FLIP_LEFT_RIGHT)


def recolor(img: Image.Image, mapping: dict) -> Image.Image:
    """Swap colours: mapping of code/name/hex -> code/name/hex."""
    m = {rgba(k)[:3]: rgba(v) for k, v in mapping.items()}
    out = img.copy()
    px = out.load()
    for y in range(out.height):
        for x in range(out.width):
            p = px[x, y]
            if p[3] and p[:3] in m:
                px[x, y] = m[p[:3]]
    return out


def silhouette(img: Image.Image, color="K") -> Image.Image:
    """Every opaque pixel becomes one colour (readability test)."""
    c = rgba(color)
    out = img.copy()
    px = out.load()
    for y in range(out.height):
        for x in range(out.width):
            if px[x, y][3]:
                px[x, y] = c
    return out


def outline(img: Image.Image, color="K", diagonal=False) -> Image.Image:
    """Add a 1px outline around opaque pixels (grows the canvas by 1 on each side)."""
    w, h = img.width + 2, img.height + 2
    out = blank(w, h)
    out.alpha_composite(img, (1, 1))
    src = out.load()
    res = out.copy()
    px = res.load()
    c = rgba(color)
    nb = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    if diagonal:
        nb += [(1, 1), (-1, -1), (1, -1), (-1, 1)]
    for y in range(h):
        for x in range(w):
            if src[x, y][3] == 0 and any(
                    0 <= x + dx < w and 0 <= y + dy < h and src[x + dx, y + dy][3]
                    for dx, dy in nb):
                px[x, y] = c
    return res


def selout(img: Image.Image, mapping: dict, light=(-1, -1), dark="K",
           default="K") -> Image.Image:
    """Selective outline, same canvas size (leave a 1px margin when authoring).

    Each empty pixel touching the sprite becomes an outline pixel. On the side facing
    the light (light=(-1,-1) means from the upper left) it takes mapping[fill colour]
    (a darker shade of the colour it touches); on the shadow side it takes `dark`.
    mapping: {fill code/name/hex: outline code/name/hex}."""
    m = {rgba(k)[:3]: rgba(v) for k, v in mapping.items()}
    src = img.load()
    out = img.copy()
    px = out.load()
    w, h = img.size
    dk, df = rgba(dark), rgba(default)
    for y in range(h):
        for x in range(w):
            if src[x, y][3]:
                continue
            best = None
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nx, ny = x + dx, y + dy
                if not (0 <= nx < w and 0 <= ny < h) or not src[nx, ny][3]:
                    continue
                # (-dx, -dy) points from the fill towards this outline pixel.
                lit = (-dx) * light[0] + (-dy) * light[1] > 0
                c = m.get(src[nx, ny][:3], df) if lit else dk
                if best is None or luma(c) < luma(best):
                    best = c
            if best is not None:
                px[x, y] = best
    return out


def outline_in(img: Image.Image, color="K") -> Image.Image:
    """1px outline without growing the canvas (leave a margin when authoring)."""
    return outline(img, color).crop((1, 1, img.width + 1, img.height + 1))


def grayscale(img: Image.Image) -> Image.Image:
    """Luminance view (keeps alpha). Use it to check values."""
    a = img.getchannel("A")
    g = img.convert("RGB").convert("L").convert("RGBA")
    g.putalpha(a)
    return g


def tiled(tile: Image.Image, nx: int, ny: int) -> Image.Image:
    out = blank(tile.width * nx, tile.height * ny)
    for j in range(ny):
        for i in range(nx):
            out.alpha_composite(tile, (i * tile.width, j * tile.height))
    return out


def wrap_shift(img: Image.Image, dx: int, dy: int) -> Image.Image:
    """Offset with wrap-around (the 'offset' filter used to check tile seams)."""
    out = Image.new("RGBA", img.size)
    w, h = img.size
    dx %= w
    dy %= h
    out.paste(img.crop((w - dx, h - dy, w, h)), (0, 0))
    out.paste(img.crop((0, h - dy, w - dx, h)), (dx, 0))
    out.paste(img.crop((w - dx, 0, w, h - dy)), (0, dy))
    out.paste(img.crop((0, 0, w - dx, h - dy)), (dx, dy))
    return out


# ---------------------------------------------------------------------------
# Pixel drawing helpers (for procedural parts of figures)
# ---------------------------------------------------------------------------
def put(img: Image.Image, x: int, y: int, c) -> None:
    if 0 <= x < img.width and 0 <= y < img.height:
        img.putpixel((x, y), rgba(c))


def rect(img, x, y, w, h, c) -> None:
    for j in range(y, y + h):
        for i in range(x, x + w):
            put(img, i, j, c)


def bresenham(x0, y0, x1, y1) -> list[tuple[int, int]]:
    pts = []
    dx, dy = abs(x1 - x0), -abs(y1 - y0)
    sx, sy = (1 if x0 < x1 else -1), (1 if y0 < y1 else -1)
    err = dx + dy
    while True:
        pts.append((x0, y0))
        if x0 == x1 and y0 == y1:
            return pts
        e2 = 2 * err
        if e2 >= dy:
            err += dy
            x0 += sx
        if e2 <= dx:
            err += dx
            y0 += sy


def line(img, x0, y0, x1, y1, c) -> None:
    for x, y in bresenham(x0, y0, x1, y1):
        put(img, x, y, c)


def steps_line(img, x, y, segments, c, horizontal=True) -> tuple[int, int]:
    """Draw a line as a list of segment lengths (e.g. [3,2,1,1] for a curve).
    Each segment steps one pixel on the minor axis. Returns the end point."""
    for n in segments:
        for _ in range(n):
            put(img, x, y, c)
            if horizontal:
                x += 1
            else:
                y += 1
        if horizontal:
            y += 1
        else:
            x += 1
    return x, y


# ---------------------------------------------------------------------------
# Scaling and presentation
# ---------------------------------------------------------------------------
def up(img: Image.Image, k: int) -> Image.Image:
    """Integer nearest-neighbour scale. The only scaling pixel art should get."""
    return img.resize((img.width * k, img.height * k), Image.Resampling.NEAREST)


def checker(w: int, h: int, cell: int = 8) -> Image.Image:
    bg = Image.new("RGBA", (w, h), CHECK_A + (255,))
    d = ImageDraw.Draw(bg)
    for y in range(0, h, cell):
        for x in range(0, w, cell):
            if (x // cell + y // cell) % 2:
                d.rectangle([x, y, x + cell - 1, y + cell - 1], fill=CHECK_B + (255,))
    return bg


def flatten(img: Image.Image, bg=None) -> Image.Image:
    """Composite onto a solid colour (code/name/rgb) or a checkerboard (bg=None)."""
    base = checker(img.width, img.height) if bg is None else Image.new(
        "RGBA", img.size, rgba(bg))
    base.alpha_composite(img)
    return base


def view(img: Image.Image, k: int = 8, grid: bool = False, bg=None,
         major: int | None = None, grid_color=(0, 0, 0, 70),
         major_color=(255, 255, 255, 90)) -> Image.Image:
    """Enlarge for display: integer scale, background, optional pixel grid.

    bg: None = checkerboard (shows transparency), 'none' = keep transparent,
    or any colour. major: draw a stronger line every N pixels (tile grid)."""
    big = up(img, k)
    if bg != "none":
        cell = max(4, k) if k >= 4 else 8
        base = checker(big.width, big.height, cell) if bg is None else Image.new(
            "RGBA", big.size, rgba(bg))
        base.alpha_composite(big)
        big = base
    if grid or major:
        ov = Image.new("RGBA", big.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(ov)
        if grid:
            for x in range(0, big.width + 1, k):
                d.line([(x, 0), (x, big.height)], fill=grid_color)
            for y in range(0, big.height + 1, k):
                d.line([(0, y), (big.width, y)], fill=grid_color)
        if major:
            for x in range(0, big.width + 1, k * major):
                d.line([(x, 0), (x, big.height)], fill=major_color)
            for y in range(0, big.height + 1, k * major):
                d.line([(0, y), (big.width, y)], fill=major_color)
        big.alpha_composite(ov)
    return big


_FONTS: dict[int, ImageFont.FreeTypeFont] = {}


def font(size: int = 16) -> ImageFont.FreeTypeFont:
    if size not in _FONTS:
        _FONTS[size] = ImageFont.load_default(size=size)
    return _FONTS[size]


def text_size(text: str, size: int = 16) -> tuple[int, int]:
    f = font(size)
    lines = text.split("\n")
    w = max(int(f.getlength(ln)) for ln in lines)
    return w, len(lines) * (size + 4)


def draw_text(img, x, y, text, size=16, color=FIG_FG, anchor="la") -> None:
    d = ImageDraw.Draw(img)
    for i, ln in enumerate(text.split("\n")):
        d.text((x, y + i * (size + 4)), ln, font=font(size), fill=color, anchor=anchor)


def label(img: Image.Image, text: str, size: int = 16, color=FIG_FG, top=False,
          pad: int = 6, bg=FIG_BG) -> Image.Image:
    """Add a centred caption below (or above) an image."""
    tw, th = text_size(text, size)
    w = max(img.width, tw + 2 * pad)
    h = img.height + th + pad
    out = Image.new("RGBA", (w, h), rgba(bg))
    iy = th + pad if top else 0
    out.alpha_composite(img, ((w - img.width) // 2, iy))
    ty = 2 if top else img.height + pad // 2 + 1
    for i, ln in enumerate(text.split("\n")):
        lw = int(font(size).getlength(ln))
        draw_text(out, (w - lw) // 2, ty + i * (size + 4), ln, size, color)
    return out


def row(items, gap: int = 16, bg=FIG_BG, align="top", pad: int = 0) -> Image.Image:
    """Lay images out left to right."""
    w = sum(i.width for i in items) + gap * (len(items) - 1) + 2 * pad
    h = max(i.height for i in items) + 2 * pad
    out = Image.new("RGBA", (w, h), rgba(bg))
    x = pad
    for i in items:
        y = pad + (0 if align == "top" else (h - 2 * pad - i.height) // (1 if align == "bottom" else 2))
        out.alpha_composite(i, (x, y))
        x += i.width + gap
    return out


def column(items, gap: int = 16, bg=FIG_BG, center=True, pad: int = 0) -> Image.Image:
    w = max(i.width for i in items) + 2 * pad
    h = sum(i.height for i in items) + gap * (len(items) - 1) + 2 * pad
    out = Image.new("RGBA", (w, h), rgba(bg))
    y = pad
    for i in items:
        out.alpha_composite(i, (pad + ((w - 2 * pad - i.width) // 2 if center else 0), y))
        y += i.height + gap
    return out


def grid_layout(items, cols: int, gap: int = 16, bg=FIG_BG, pad: int = 0) -> Image.Image:
    rws = [items[i:i + cols] for i in range(0, len(items), cols)]
    cw = max(i.width for i in items)
    ch = max(i.height for i in items)
    out = Image.new("RGBA", (cols * cw + (cols - 1) * gap + 2 * pad,
                             len(rws) * ch + (len(rws) - 1) * gap + 2 * pad), rgba(bg))
    for r, its in enumerate(rws):
        for c, i in enumerate(its):
            out.alpha_composite(i, (pad + c * (cw + gap) + (cw - i.width) // 2,
                                    pad + r * (ch + gap) + (ch - i.height) // 2))
    return out


def figure(body: Image.Image, title: str | None = None, note: str | None = None,
           pad: int = 16) -> Image.Image:
    """Frame a composed figure with padding, an optional title and footnote."""
    parts = []
    if title:
        tw, th = text_size(title, 20)
        t = Image.new("RGBA", (tw + 4, th), rgba(FIG_BG))
        draw_text(t, 0, 0, title, 20)
        parts.append(t)
    parts.append(body)
    if note:
        tw, th = text_size(note, 14)
        t = Image.new("RGBA", (tw + 4, th), rgba(FIG_BG))
        draw_text(t, 0, 0, note, 14, FIG_DIM)
        parts.append(t)
    return column(parts, gap=10, pad=pad, center=False)


def panel(items, cols: int | None = None, gap: int = 24, size: int = 16,
          title: str | None = None, note: str | None = None) -> Image.Image:
    """items: list of (image, caption) or (image, caption, colour). One call figure."""
    labelled = []
    for it in items:
        img, cap = it[0], it[1]
        col = it[2] if len(it) > 2 else FIG_FG
        labelled.append(label(img, cap, size, col) if cap else img)
    body = row(labelled, gap) if not cols else grid_layout(labelled, cols, gap)
    return figure(body, title, note)


def compare(bad: Image.Image, good: Image.Image, bad_text="Avoid", good_text="Better",
            title: str | None = None, note: str | None = None) -> Image.Image:
    """The standard side-by-side 'avoid vs better' figure (images already enlarged)."""
    return panel([(bad, bad_text, FIG_BAD), (good, good_text, FIG_GOOD)],
                 title=title, note=note)


def arrow(img, x0, y0, x1, y1, color=FIG_FG, width=2, head=8) -> None:
    d = ImageDraw.Draw(img)
    d.line([(x0, y0), (x1, y1)], fill=rgba(color), width=width)
    a = math.atan2(y1 - y0, x1 - x0)
    for s in (-0.5, 0.5):
        d.line([(x1, y1), (x1 - head * math.cos(a + s), y1 - head * math.sin(a + s))],
               fill=rgba(color), width=width)


# ---------------------------------------------------------------------------
# Palettes, ramps, swatches
# ---------------------------------------------------------------------------
def swatches(colors, size: int = 32, cols: int | None = None, names=False,
             gap: int = 0, text_size_: int = 12) -> Image.Image:
    """Colour chips. colors: codes/names/hex. names=True prints the hex under each chip."""
    chips = []
    for c in colors:
        chip = Image.new("RGBA", (size, size), rgba(c))
        if names:
            hx = "%02x%02x%02x" % rgba(c)[:3]
            chip = label(chip, hx, text_size_, FIG_DIM, pad=4)
        chips.append(chip)
    if cols:
        return grid_layout(chips, cols, gap)
    return row(chips, gap)


def palette_strip(colors=None) -> Image.Image:
    """1px-per-colour strip (the format Lospec and most editors import)."""
    colors = colors or PAL_LIST
    img = Image.new("RGBA", (len(colors), 1))
    for i, c in enumerate(colors):
        img.putpixel((i, 0), rgba(c))
    return img


def write_palette_files(dirpath: str, name="endesga-32") -> None:
    os.makedirs(dirpath, exist_ok=True)
    with open(os.path.join(dirpath, name + ".hex"), "w") as f:
        f.write("\n".join(hx for _, _, hx in PALETTE_NAMES) + "\n")
    with open(os.path.join(dirpath, name + ".gpl"), "w") as f:
        f.write("GIMP Palette\nName: ENDESGA 32\nColumns: 8\n#\n")
        for _, nm, hx in PALETTE_NAMES:
            r, g, b = hex2rgb(hx)
            f.write(f"{r:3d} {g:3d} {b:3d}\t{nm}\n")
    palette_strip().save(os.path.join(dirpath, name + ".png"))


def hsv(c) -> tuple[float, float, float]:
    """(hue degrees, saturation %, value %) of a colour."""
    import colorsys
    r, g, b = [v / 255 for v in rgba(c)[:3]]
    h, s, v = colorsys.rgb_to_hsv(r, g, b)
    return round(h * 360), round(s * 100), round(v * 100)


def luma(c) -> float:
    r, g, b = rgba(c)[:3]
    return 0.299 * r + 0.587 * g + 0.114 * b


# ---------------------------------------------------------------------------
# Animation: sheets, GIFs, onion skins, strips
# ---------------------------------------------------------------------------
@dataclass
class Anim:
    """A named animation: equally sized frames and per-frame durations (ms)."""
    name: str
    frames: list
    durations: list
    loop: bool = True

    def __post_init__(self):
        if isinstance(self.durations, int):
            self.durations = [self.durations] * len(self.frames)
        assert len(self.durations) == len(self.frames), self.name


def sheet(frames, cols: int | None = None, pad: int = 0) -> Image.Image:
    """Pack equally sized frames into a grid (left to right, top to bottom)."""
    cols = cols or len(frames)
    fw, fh = frames[0].size
    rws = math.ceil(len(frames) / cols)
    out = blank(cols * (fw + pad) - pad if cols else 0, rws * (fh + pad) - pad)
    for i, f in enumerate(frames):
        out.alpha_composite(f, ((i % cols) * (fw + pad), (i // cols) * (fh + pad)))
    return out


def split(img: Image.Image, fw: int, fh: int, count: int | None = None) -> list:
    out = []
    for y in range(0, img.height, fh):
        for x in range(0, img.width, fw):
            out.append(img.crop((x, y, x + fw, y + fh)))
    return out[:count] if count else out


def save_gif(frames, path: str, durations, k: int = 4, bg="FIG", loop: int = 0) -> None:
    """Animated GIF at integer scale. durations: int or list (ms). bg='FIG' uses the
    figure background; pass a colour to use a scene colour."""
    if isinstance(durations, int):
        durations = [durations] * len(frames)
    bgc = FIG_BG if bg == "FIG" else rgba(bg)[:3]
    out = []
    for f in frames:
        base = Image.new("RGBA", f.size, bgc + (255,))
        base.alpha_composite(f)
        out.append(up(base, k).convert("RGB"))
    # Build one shared palette so colours never shift between frames.
    w = out[0].width
    strip = Image.new("RGB", (w, out[0].height * len(out)))
    for i, f in enumerate(out):
        strip.paste(f, (0, i * f.height))
    pal = strip.quantize(colors=255, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE)
    q = [f.quantize(palette=pal, dither=Image.Dither.NONE) for f in out]
    os.makedirs(os.path.dirname(path), exist_ok=True)
    q[0].save(path, save_all=True, append_images=q[1:], duration=durations, loop=loop,
              disposal=1, optimize=False)


def tint(img: Image.Image, color, alpha: int = 110) -> Image.Image:
    """Single colour version with reduced opacity (onion-skin ghost)."""
    c = rgba(color)
    out = img.copy()
    px = out.load()
    for y in range(out.height):
        for x in range(out.width):
            if px[x, y][3]:
                px[x, y] = c[:3] + (alpha,)
    return out


def onion(frames, i: int, before: int = 1, after: int = 1, before_color=(255, 70, 70),
          after_color=(70, 200, 255), alpha: int = 100) -> Image.Image:
    """Frame i with tinted ghosts of previous (red) and next (blue) frames under it."""
    out = blank(*frames[0].size)
    for d in range(before, 0, -1):
        if i - d >= 0:
            out.alpha_composite(tint(frames[i - d], before_color, alpha // d))
    for d in range(after, 0, -1):
        if i + d < len(frames):
            out.alpha_composite(tint(frames[i + d], after_color, alpha // d))
    out.alpha_composite(frames[i])
    return out


def filmstrip(frames, k: int = 4, durations=None, bg=None, grid=False, numbers=True,
              gap: int = 8) -> Image.Image:
    """Frames side by side, enlarged, numbered (and with durations if given)."""
    items = []
    for n, f in enumerate(frames):
        v = view(f, k, grid=grid, bg=bg)
        cap = None
        if numbers:
            cap = str(n + 1) if durations is None else f"{n + 1}: {durations[n]}ms"
        items.append(label(v, cap, 14, FIG_DIM) if cap else v)
    return row(items, gap)


def frames_overlay(frames, colors=None, alpha=150) -> Image.Image:
    """All frames stacked as tinted ghosts (shows arcs and spacing)."""
    out = blank(*frames[0].size)
    n = len(frames)
    for i, f in enumerate(frames):
        if colors:
            c = colors[i % len(colors)]
        else:
            t = i / max(1, n - 1)
            c = (int(255 * (1 - t) + 60 * t), int(90 + 80 * t), int(60 + 195 * t))
        out.alpha_composite(tint(f, c, alpha))
    return out


# ---------------------------------------------------------------------------
# Environments: tile previews, parallax
# ---------------------------------------------------------------------------
def seam_preview(tile: Image.Image, n: int = 3, k: int = 4, show_tile=True) -> Image.Image:
    """The tile repeated n x n, with the centre copy outlined. Seams jump out here."""
    big = view(tiled(tile, n, n), k, bg="none")
    if show_tile:
        d = ImageDraw.Draw(big)
        x0, y0 = (n // 2) * tile.width * k, (n // 2) * tile.height * k
        d.rectangle([x0, y0, x0 + tile.width * k - 1, y0 + tile.height * k - 1],
                    outline=(255, 255, 255, 160))
    return big


def tilemap(tiles: dict, layout, tw: int = 16, th: int = 16) -> Image.Image:
    """Compose a map from a dict of tiles and a list of strings (one char per tile,
    '.' = empty). tiles: {char: Image}."""
    if isinstance(layout, str):
        layout = rows(layout)
    out = blank(len(layout[0]) * tw, len(layout) * th)
    for j, r in enumerate(layout):
        for i, ch in enumerate(r):
            if ch in tiles:
                out.alpha_composite(tiles[ch], (i * tw, j * th))
    return out


def hwrap(img: Image.Image, x: int) -> Image.Image:
    """Horizontal wrap-around offset (for scrolling a seamless layer)."""
    return wrap_shift(img, x, 0)


def parallax_frame(layers, w: int, h: int, cam_x: float, sky=None) -> Image.Image:
    """layers: list of (image, speed, y) back to front. speed 0 = fixed, 1 = moves with
    the world. Each layer must tile horizontally (its width is the wrap period)."""
    out = Image.new("RGBA", (w, h), rgba(sky) if sky else (0, 0, 0, 0))
    for img, speed, y in layers:
        off = -int(round(cam_x * speed)) % img.width
        x = off - img.width
        while x < w:
            paste(out, img, x, y)
            x += img.width
    return out


# ---------------------------------------------------------------------------
# Output
# ---------------------------------------------------------------------------
def save(img: Image.Image, path: str) -> str:
    """Save a PNG; relative names go to images/. Prints the path written."""
    if not os.path.isabs(path):
        path = os.path.join(IMAGES, path)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    img.save(path, optimize=True)
    print("wrote", os.path.relpath(path, ROOT))
    return path


def save_sheet_json(path: str, image_name: str, fw: int, fh: int, anims: list) -> None:
    """Write a simple, engine-neutral JSON description of a sprite sheet where each
    Anim occupies one row: {frame size, animations: {name: {row, frames, durations}}}."""
    data = {"image": image_name, "frameWidth": fw, "frameHeight": fh, "animations": {}}
    for r, a in enumerate(anims):
        data["animations"][a.name] = {"row": r, "frames": len(a.frames),
                                      "durations": a.durations, "loop": a.loop}
    with open(path, "w") as f:
        json.dump(data, f, indent=2)
        f.write("\n")


def value_study(img: Image.Image, greys=("K", "4", "3", "2", "1"), gain=1.1) -> Image.Image:
    """Map every opaque colour to one of a few greys by its luminance (a value study)."""
    g = grayscale(img)
    out = img.copy()
    px, gp = out.load(), g.load()
    n = len(greys)
    for y in range(img.height):
        for x in range(img.width):
            if px[x, y][3]:
                i = min(n - 1, int(gp[x, y][0] / 256 * n * gain))
                px[x, y] = rgba(greys[i])
    return out


def line_art(img: Image.Image, codes="dK5j", color="K") -> Image.Image:
    """Keep only the darkest 'line' colours of a sprite (recovers its line art)."""
    keep = {LEGEND[c][:3] for c in codes}
    out = blank(img.width, img.height)
    src, dst = img.load(), out.load()
    for y in range(img.height):
        for x in range(img.width):
            if src[x, y][3] and src[x, y][:3] in keep:
                dst[x, y] = rgba(color)
    return out
