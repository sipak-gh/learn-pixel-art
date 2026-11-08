"""Parallax background layers for mossy-ruins (view 320x180, light from the upper left).

Back to front: sky (fixed) -> clouds -> mountains -> distant ruins & treeline -> mid forest
-> (gameplay layer) -> foreground leaves. Every layer is seamless horizontally: its width is
its wrap period and its shapes come from periodic functions or wrap-around drawing.
Further layers have less contrast and sit closer to the sky colour (atmospheric perspective).
"""
from __future__ import annotations

import math
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pix import Image, blank, parallax_frame, put, rgba  # noqa

W, H = 320, 180
BAYER = [[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]]


def periodic(x, period, terms, seed):
    """Sum of sines whose frequencies are whole numbers of cycles per period (seamless)."""
    rng = random.Random(seed)
    v = 0.0
    for k, amp in terms:
        v += amp * math.sin(2 * math.pi * k * x / period + rng.random() * 6.28)
    return v


def sky(w=W, h=H, bands=(("n", 0), ("u", 28), ("1", 150)), dither=16):
    """Banded gradient with short ordered-dither transitions between bands. Only a thin navy
    band at the top: the mid-blue keeps the sky lighter, closer to the ch08 value plan."""
    img = blank(w, h)
    for y in range(h):
        for x in range(w):
            c = bands[0][0]
            for i, (col, start) in enumerate(bands):
                if y >= start:
                    c = col
                elif i and y >= start - dither:
                    t = (y - (start - dither)) / dither  # 0..1 into the next band
                    if t * 16 > BAYER[y % 4][x % 4]:
                        c = col
                    break
            put(img, x, y, c)
    return img


def _wrap_put(img, x, y, c):
    if 0 <= y < img.height:
        put(img, x % img.width, y, c)


def clouds(w=640, h=60, seed=2):
    """Flat, soft-edged cloud banks: white tops lit from the left, grey-blue undersides."""
    img = blank(w, h)
    rng = random.Random(seed)
    for cx in range(30, w, 150):
        cx += rng.randint(-20, 20)
        cy = rng.randint(18, 40)
        puffs = [(cx + dx, cy - abs(dx) // 4 + rng.randint(-2, 2), rng.randint(6, 11))
                 for dx in range(-30, 31, 10)]
        for px, py, r in puffs:
            for y in range(py - r, cy + 4):
                for x in range(px - r, px + r + 1):
                    if (x - px) ** 2 + (y - py) ** 2 <= r * r:
                        under = y >= cy
                        _wrap_put(img, x, y, "1" if under else "W")
        for x in range(cx - 38, cx + 39):  # flat underside line
            _wrap_put(img, x, cy + 4, "1")
    return img


def mountains(w=W, h=90, seed=3):
    """Two ranges; the lit (left) face of each peak is a lighter value."""
    img = blank(w, h)
    rng = random.Random(seed)
    for rng_i, (body, lit, base, n_peaks, hmin, hmax) in enumerate(
            [("2", "1", 30, 5, 20, 55), ("3", "2", 45, 4, 10, 35)]):
        peaks = []
        for i in range(n_peaks):
            px = int((i + rng.random() * 0.6) * w / n_peaks)
            peaks.append((px, base - rng.randint(hmin, hmax) + 50, rng.uniform(0.9, 1.3)))
        for x in range(w):
            top, lit_side = h, False
            for px, py, s in peaks:
                for wrap in (-w, 0, w):
                    d = x - (px + wrap)
                    t = py + abs(d) * s * 0.9 + periodic(x, w, [(9, 1.0), (23, 0.6)], seed + rng_i)
                    if t < top:
                        top, lit_side = int(t), d < 0
            for y in range(max(0, top), h):
                put(img, x, y, lit if lit_side and y < top + 30 else body)
    return img


def treeline(w=W, h=88, seed=5):
    """Distant ruins (towers with windows) in front of a bumpy treeline, all in two values."""
    img = blank(w, h)
    rng = random.Random(seed)
    # towers
    for tx in range(20, w, 110):
        tx += rng.randint(0, 30)
        tw, th = rng.randint(12, 18), rng.randint(58, 76)
        top = h - th
        for y in range(top, h):
            for x in range(tx, tx + tw):
                _wrap_put(img, x, y, "3" if x - tx < 3 else "4")
        for x in range(tx, tx + tw, 3):  # crenellations
            for y in range(top - 3, top):
                _wrap_put(img, x, y, "4")
                _wrap_put(img, x + 1, y, "4")
        for wy in range(top + 6, h - 20, 9):  # windows (sky shows through)
            for y in range(wy, wy + 4):
                _wrap_put(img, tx + tw // 2, y, "2")
        # broken side
        for y in range(top, top + rng.randint(6, 12)):
            _wrap_put(img, tx + tw - 1, y, "2" if y % 3 == 0 else "4")
    # treeline in front
    for x in range(w):
        t = h - 44 + periodic(x, w, [(16, 4.0), (37, 2.0), (71, 1.0)], seed)
        for y in range(int(t), h):
            put(img, x, y, "4" if (y - int(t)) > 1 or x % 7 else "3")
    return img


def forest(w=W, h=130, seed=8):
    """Mid layer: a continuous, bumpy canopy band of overlapping trees (no outlines, a
    darker ramp than the gameplay trees), trunks in the gaps below, undergrowth."""
    from props import canopy
    rng = random.Random(seed)
    img = blank(w, h)
    trees = []
    x = 0
    while x < w:
        trees.append((x, rng.randint(30, 50), rng.randint(15, 22)))
        x += rng.randint(28, 44)
    # trunks first (behind the canopy)
    for tx, cy, r in trees:
        tw = rng.randint(6, 9)
        for y in range(cy + r - 4, h):
            for dx in range(tw):
                col = "j" if dx == 0 else ("K" if dx == tw - 1 else "5")
                _wrap_put(img, tx + dx - tw // 2, y, col)
    for n, (tx, cy, r) in enumerate(trees):
        clumps = [(r + 8, r + 4, r, True),
                  (r + 8 - r // 2, r + 4 + r // 3, r * 2 // 3, False),
                  (r + 8 + r // 2, r + 4 + r // 3, r * 2 // 3, False),
                  (r + 8 - r // 4, r + 4 - r // 3, r // 2, False),
                  (r + 8 + r // 3, r + 4 + r // 2 + 2, r // 2, False)]
        c = canopy(2 * r + 16, 2 * r + 12, clumps, seed=seed + n, outline=None)
        c = _ramp_shift(c, {"G": "h", "g": "j", "h": "5"})
        ox, oy = tx - (r + 8), cy - (r + 4)
        for y in range(c.height):
            for x2 in range(c.width):
                p = c.getpixel((x2, y))
                if p[3] and 0 <= oy + y < h:
                    img.putpixel(((ox + x2) % w, oy + y), p)
    for x in range(w):
        t = h - 16 + periodic(x, w, [(20, 3.0), (45, 1.5)], seed)
        for y in range(int(t), h):
            put(img, x, y, "5" if y > t + 1 else "j")
    return img


def _ramp_shift(img, mapping):
    from pix import recolor
    return recolor(img, mapping)


FG_CLUMPS = (14, 318, 470)  # clump centres: the two bottom corners of the opening view + one


def foreground(w=640, h=32, seed=11, centres=FG_CLUMPS):
    """Near grass clumps in the darkest foliage colours; they pass quickly in front of the
    action (speed > 1) and frame the bottom corners. Each clump is a solid mound that runs
    off the bottom edge with a fan of tapered blades (thick base, 1 px tip), so it reads as
    one mass of near grass rather than loose strokes. Lit (left) edges get the next ramp step."""
    img = blank(w, h)
    rng = random.Random(seed)
    for cx in centres:
        mw = rng.randint(20, 26)  # mound half-width
        n = rng.randint(16, 20)
        blades = []
        for i in range(n):
            u = (i + 0.5) / n * 2 - 1  # -1 (left) .. 1 (right)
            length = int(h * (1.0 - 0.5 * abs(u)) + rng.randint(-4, 2))
            blades.append((cx + int(u * mw * 0.7), length, u * 0.6 + rng.uniform(-0.2, 0.2)))
        blades.sort(key=lambda b: b[1])  # short blades first, so long blades are drawn over them
        for bx, length, lean in blades:
            for t in range(length):
                y = h - 1 - t
                x = bx + round(lean * t * t / length)
                width = 4 if t < length * 0.3 else (3 if t < length * 0.55 else
                                                    (2 if t < length * 0.8 else 1))
                for k in range(width):
                    _wrap_put(img, x + k, y, "h" if k == 0 and width > 1 else "j")
        for x in range(cx - mw, cx + mw + 1):  # mound
            top = h - 1 - int(9 * (1 - ((x - cx) / mw) ** 2))
            for y in range(top, h):
                _wrap_put(img, x, y, "h" if y == top and x < cx else "j")
    return img


def layers(stage="final"):
    """(name, image, speed, y) back to front. The gameplay layer goes between forest and
    foreground (speed 1)."""
    out = [
        ("sky", sky(), 0.0, 0),
        ("clouds", clouds(), 0.08, 6),
        ("mountains", mountains(), 0.15, 60),
        ("treeline", treeline(), 0.3, 92),
        ("forest", forest(), 0.55, 50),
    ]
    return out


def composite(cam_x=0, include_fg=False, gameplay=None):
    ls = [(img, speed, y) for _, img, speed, y in layers()]
    if gameplay is not None:
        ls.append((gameplay, 1.0, H - gameplay.height))
    if include_fg:
        ls.append((foreground(), 1.4, H - 40))
    return parallax_frame(ls, W, H, cam_x)
