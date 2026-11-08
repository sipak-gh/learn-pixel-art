"""Ch. 22 (dithered monochrome, Obra Dinn-like): a tiny analytic 3D render of a vault
alcove - the seed pod on its stalk, a crate, a floor and back wall, lit by Kit's lantern -
then reduced to 1 bit with different threshold maps. Everything is computed (no assets),
so the chapter can show the *pipeline*: shade -> outline -> dither.
"""
from __future__ import annotations

import math

from PIL import Image

from nes import bayer, blue_noise

W, H = 256, 160
INK = (22, 22, 30)        # original 2-colour pair (dark ink / warm paper)
PAPER = (232, 226, 206)
LIGHT = (62.0, 76.0, 70.0)  # lantern position (x, y on screen, z towards viewer)


def _norm(v):
    m = math.sqrt(sum(c * c for c in v)) or 1.0
    return tuple(c / m for c in v)


def _shade(p, n, amb=0.06):
    lx, ly, lz = LIGHT
    d = (lx - p[0], ly - p[1], lz - p[2])
    dist = math.sqrt(sum(c * c for c in d))
    l = _norm(d)
    lam = max(0.0, sum(a * b for a, b in zip(n, l)))
    fall = 1.0 / (1.0 + (dist / 170.0) ** 2)
    return min(1.0, amb + 1.25 * lam * fall)


def render():
    """-> (grey [[0..1]], ids [[int]]) with ids 0 wall, 1 floor, 2 pod, 3 stalk, 4 crate,
    5 crate side, 6 lantern, 7 crate top."""
    grey = [[0.0] * W for _ in range(H)]
    ids = [[0] * W for _ in range(H)]
    horizon = 104
    for y in range(H):
        for x in range(W):
            if y < horizon:  # back wall facing the viewer, panel seams every 32 px
                p, n, i = (x, y, -40.0), (0.0, 0.0, 1.0), 0
                v = _shade(p, n) * 0.6  # keep the wall a step darker than the objects
                if x % 48 == 0 or y % 40 == 0:
                    v *= 0.55
            else:  # floor receding: depth from row
                z = -40.0 + (y - horizon) * 3.0
                p, n, i = (x, horizon + 4, z), (0.0, -1.0, 0.0), 1
                v = _shade(p, n) * 0.9
            grey[y][x], ids[y][x] = v, i
    # crate (front face + right side), behind the pod
    cx0, cx1, cy0, cy1 = 150, 196, 84, 128
    for y in range(cy0, cy1):
        for x in range(cx0, cx1):
            grey[y][x], ids[y][x] = _shade((x, y, 0.0), (0.0, 0.0, 1.0)), 4
    for x in range(cx1, cx1 + 14):  # right side face (receding up-right)
        k = (x - cx1) * 10 // 14
        for y in range(cy0 - k, cy1 - k):
            grey[y][x], ids[y][x] = _shade((x, y, -10.0), _norm((1.0, 0.0, 0.4))) * 0.8, 5
    for x in range(cx0, cx1 + 14):  # top face
        for y in range(cy0 - 10, cy0):
            if x - cx0 >= (cy0 - y) * 14 // 10 and x < cx1 + (cy0 - y) * 14 // 10:
                grey[y][x], ids[y][x] = _shade((x, y, -5.0), _norm((0.0, -1.0, 0.3))), 7
    # stalk (cylinder)
    sx, sr = 104, 4
    for y in range(70, 128):
        for x in range(sx - sr, sx + sr + 1):
            u = (x - sx) / (sr + 0.5)
            n = (u, 0.0, math.sqrt(max(0.0, 1 - u * u)))
            grey[y][x], ids[y][x] = _shade((x, y, 10.0), n), 3
    # pod (sphere)
    px, py, pr = 104, 52, 26
    for y in range(py - pr, py + pr + 1):
        for x in range(px - pr, px + pr + 1):
            dx, dy = x + 0.5 - px, y + 0.5 - py
            r2 = dx * dx + dy * dy
            if r2 <= pr * pr:
                dz = math.sqrt(pr * pr - r2)
                n = (dx / pr, dy / pr, dz / pr)
                v = _shade((x, y, 20.0 + dz), n)
                if abs(math.atan2(dy, dx) * 6 / math.pi % 2 - 1) < 0.08:  # seams
                    v *= 0.6
                grey[y][x], ids[y][x] = v, 2
    # lantern glow (the light source itself)
    lx, ly = int(LIGHT[0]), int(LIGHT[1]) + 2
    for y in range(ly - 4, ly + 5):
        for x in range(lx - 3, lx + 4):
            if (x - lx) ** 2 / 9 + (y - ly) ** 2 / 16 <= 1:
                grey[y][x], ids[y][x] = 1.0, 6
    return grey, ids


def grey_image(grey):
    im = Image.new("RGBA", (W, H))
    px = im.load()
    for y in range(H):
        for x in range(W):
            v = int(grey[y][x] * 255)
            px[x, y] = (v, v, v, 255)
    return im


def posterize(grey, levels=4):
    im = Image.new("RGBA", (W, H))
    px = im.load()
    for y in range(H):
        for x in range(W):
            v = int(min(levels - 1, grey[y][x] * levels)) * 255 // (levels - 1)
            px[x, y] = (v, v, v, 255)
    return im


_BN = None


def dither(grey, method="bayer4", colors=(INK, PAPER)):
    global _BN
    if method == "threshold":
        m, norm = [[0.5]], None
    elif method.startswith("bayer"):
        n = int(method[5:])
        b = bayer(n)
        m = [[(v + 0.5) / (n * n) for v in r] for r in b]
    elif method == "blue":
        if _BN is None:
            _BN = blue_noise(32, 32)
        m = _BN
    else:
        raise ValueError(method)
    mh, mw = len(m), len(m[0])
    im = Image.new("RGBA", (W, H))
    px = im.load()
    for y in range(H):
        for x in range(W):
            px[x, y] = tuple(colors[1] if grey[y][x] > m[y % mh][x % mw] else colors[0]) + (255,)
    return im


def outlines(im, ids, color=PAPER, grey=None, ink=INK):
    """Draw 1 px lines where the object id changes (silhouette edges), as Lucas Pope's
    renderer outlines objects so form survives dithering."""
    out = im.copy()
    px = out.load()
    for y in range(H - 1):
        for x in range(W - 1):
            a = ids[y][x]
            if a != ids[y][x + 1] or a != ids[y + 1][x]:
                if {a, ids[y][x + 1], ids[y + 1][x]} != {0, 1}:  # skip the floor/wall seam
                    v = grey[y][x] if grey else 0.0
                    px[x, y] = tuple(color if v < 0.5 else ink) + (255,)
    return out
