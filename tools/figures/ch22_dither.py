"""Ch. 22 figures: dithered monochrome (Obra Dinn-like): shade -> outline -> dither."""
from _v import *
import math

from styles import dither as DI

grey, ids = DI.render()
INK, PAPER = DI.INK, DI.PAPER
b4 = DI.dither(grey, "bayer4")

save(figure(row([label(nv(DI.grey_image(grey), 2), "1. greyscale render", 14, FIG_FG),
                 label(nv(DI.posterize(grey, 4), 2), "2. values planned (4 bands)", 14, FIG_FG),
                 label(nv(b4, 2), "3. dithered to 2 colours", 14, FIG_FG),
                 label(nv(DI.outlines(b4, ids, grey=grey), 2), "4. + object outlines", 14, FIG_FG)], 12),
            "The 1-bit pipeline: light first, pattern last",
            "Get the values right in grey, then let a threshold map turn them into two colours. "
            "Outlines where objects meet keep the forms apart."), "ch22-pipeline.png")

# threshold maps and a dithered ramp under each
ramp = [[x / 255 for x in range(256)] for _ in range(24)]


def ramp_img(method):
    old_w, old_h = DI.W, DI.H
    DI.W, DI.H = 256, 24
    try:
        return DI.dither(ramp, method)
    finally:
        DI.W, DI.H = old_w, old_h


def matrix_img(n):
    b = bayer(n)
    im = Image.new("RGBA", (n, n))
    for y in range(n):
        for x in range(n):
            v = int((b[y][x] + 0.5) / (n * n) * 255)
            im.putpixel((x, y), (v, v, v, 255))
    return im


bn = blue_noise(32, 32)
bn_im = Image.new("RGBA", (32, 32))
for y in range(32):
    for x in range(32):
        v = int(bn[y][x] * 255)
        bn_im.putpixel((x, y), (v, v, v, 255))
rows_ = []
for name, m, mat in (("single threshold", "threshold", None), ("Bayer 2x2", "bayer2", matrix_img(2)),
                     ("Bayer 4x4", "bayer4", matrix_img(4)), ("Bayer 8x8", "bayer8", matrix_img(8)),
                     ("blue noise 32x32", "blue", bn_im)):
    cells = [label(view(ramp_img(m), 3, grid=False, bg=FIG_BG), name, 14, FIG_FG)]
    if mat is not None:
        k = 72 // mat.width
        cells.append(label(view(mat, k, grid=mat.width <= 8, bg=FIG_BG), "map", 13, FIG_FG))
    rows_.append(row(cells, 16))
save(figure(column(rows_, 10), "Threshold maps: same ramp, different patterns",
            "A pixel turns light where its value beats the map. Bayer maps give tidy, "
            "regular hatching; blue noise gives an even grain with no visible grid."), "ch22-matrices.png")

save(panel([(nv(DI.dither(grey, m), 2), t) for m, t in
            (("threshold", "single threshold"), ("bayer2", "Bayer 2x2"), ("bayer8", "Bayer 8x8"),
             ("blue", "blue noise"))],
           title="One scene, four threshold maps",
           note="A single threshold throws away every mid-tone. Bigger maps give more in-between "
                "steps; noise hides the grid but looks grainier up close."), "ch22-methods.png")

save(compare(nv(b4, 3), nv(DI.outlines(b4, ids, grey=grey), 3), "no outlines", "outlines on object edges",
             "Why Obra Dinn draws outlines",
             "Where two surfaces have similar values, their dither patterns merge. A 1 px line "
             "(paper on dark, ink on light) separates them again."), "ch22-outlines.png")

# shower-door: pan the camera with a screen-locked vs a world-locked threshold map
VW = 176
full = DI.outlines(b4, ids, grey=grey)
crops = []


def screen_locked(ox):
    sub = [r[ox:ox + VW] for r in grey]
    old_w = DI.W
    DI.W = VW
    try:
        im = DI.dither(sub, "bayer4")
    finally:
        DI.W = old_w
    sids = [r[ox:ox + VW] for r in ids]
    out = im.copy()
    px = out.load()
    for y in range(DI.H - 1):
        for x in range(VW - 1):
            a = sids[y][x]
            if (a != sids[y][x + 1] or a != sids[y + 1][x]) and {a, sids[y][x + 1], sids[y + 1][x]} != {0, 1}:
                px[x, y] = tuple(PAPER if sub[y][x] < 0.5 else INK) + (255,)
    return out


frames = []
offs = list(range(0, 80, 1)) + list(range(80, 0, -1))
for ox in offs:
    a = nv(screen_locked(ox), 2)
    b = nv(full.crop((ox, 0, ox + VW, DI.H)), 2)
    frames.append(panel([(a, "pattern fixed to the screen: it 'swims'"),
                         (b, "pattern fixed to the world: it moves with the scene")]))
gif("ch22-swim.gif", frames, [40] * len(frames), k=1, bg=FIG_BG)

# moving light: values change, pattern responds
lframes = []
for i in range(24):
    a = i / 24 * 2 * math.pi
    DI.LIGHT = (128 + 70 * math.cos(a), 76 + 10 * math.sin(a), 70.0)
    gr, idd = DI.render()
    lframes.append(nv(DI.outlines(DI.dither(gr, "bayer4"), idd, grey=gr), 2))
DI.LIGHT = (62.0, 76.0, 70.0)
gif("ch22-light.gif", lframes, [90] * len(lframes), k=1, bg=FIG_BG)

PAIRS = [("ink / paper", (INK, PAPER)), ("black / white", ((0, 0, 0), (255, 255, 255))),
         ("green phosphor", ((10, 26, 14), (120, 230, 120))), ("amber", ((30, 16, 4), (255, 176, 64))),
         ("night blue", ((14, 18, 44), (170, 200, 255)))]
save(panel([(nv(DI.outlines(DI.dither(grey, "bayer4", c), ids, c[1], grey, c[0]).crop((40, 0, 216, 160)), 1), n)
            for n, c in PAIRS], title="Two colours, five moods",
           note="The pair is the whole palette. Pure black/white is harshest; a slightly warm or "
                "tinted pair is easier on the eye over a long game."), "ch22-pairs.png")
