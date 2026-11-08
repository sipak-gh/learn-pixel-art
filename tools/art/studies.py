"""Small study subjects for the fundamentals figures: spheres and cubes under one light,
line and curve specimens, perspective boxes. Everything is drawn in ENDESGA 32."""
from __future__ import annotations

import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from PIL import ImageDraw  # noqa: E402

from pix import blank, put, rgba, steps_line  # noqa: E402

LIGHT = (-0.55, -0.65, 0.52)  # upper left, slightly toward the viewer


def _norm(v):
    m = math.sqrt(sum(c * c for c in v))
    return tuple(c / m for c in v)


def _outline(img, color):
    src = img.copy()
    sp = src.load()
    for y in range(img.height):
        for x in range(img.width):
            if sp[x, y][3]:
                continue
            for ex, ey in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nx, ny = x + ex, y + ey
                if 0 <= nx < img.width and 0 <= ny < img.height and sp[nx, ny][3]:
                    put(img, x, y, color)
                    break
    return img


def sphere(d=24, ramp=("5", "4", "3", "2", "1"), mode="lit", outline="K", cast=False,
           highlight="W", reflect=True):
    """A shaded ball, d pixels across.

    mode: 'lit'    - directional light, core shadow, reflected light, one highlight cluster
          'pillow' - shading by distance from the centre (the classic beginner mistake)
          'flat'   - a single colour
    ramp: darkest .. lightest codes. cast=True adds a ground shadow to the lower right
    (the canvas grows to make room).
    """
    ball = blank(d + 2, d + 2)
    r = d / 2
    cx = cy = 1 + r
    L = _norm(LIGHT)
    n = len(ramp)
    for y in range(d + 2):
        for x in range(d + 2):
            dx, dy = (x + 0.5 - cx) / r, (y + 0.5 - cy) / r
            dd = dx * dx + dy * dy
            if dd > 1:
                continue
            dz = math.sqrt(1 - dd)
            if mode == "flat":
                i = n // 2
            elif mode == "pillow":
                i = min(n - 1, int((1 - math.sqrt(dd)) * n * 1.15))
            else:
                lam = dx * L[0] + dy * L[1] + dz * L[2]
                if lam < 0:
                    # core shadow next to the terminator, reflected light near the rim below
                    i = 1 if (reflect and lam < -0.45 and dy > 0.1) else 0
                else:
                    i = min(n - 1, 1 + int(lam * (n - 1) * 1.05))
            put(ball, x, y, ramp[i])
    if mode == "lit" and highlight:
        hx, hy = int(cx - r * 0.42), int(cy - r * 0.45)
        put(ball, hx, hy, highlight)
        if d >= 16:
            put(ball, hx + 1, hy, highlight)
            put(ball, hx, hy + 1, highlight)
    if outline:
        ball = _outline(ball, outline)
    if not cast:
        return ball
    img = blank(d + 2 + d // 2, d + 2 + 3)
    sh = ramp[0]
    ex, ey, erx, ery = cx + d * 0.2, d + 1.5, r * 1.05, 2.6
    for y in range(img.height):
        for x in range(img.width):
            if ((x + 0.5 - ex) / erx) ** 2 + ((y + 0.5 - ey) / ery) ** 2 <= 1:
                put(img, x, y, sh)
    img.alpha_composite(ball, (0, 0))
    return img


def cube(s=16, faces=("2", "3", "4"), outline="K"):
    """A box seen slightly from above (3/4 view): top, front, side faces lit from upper left.
    faces = (top, front, right side)."""
    depth = s // 2
    img = blank(s + depth + 2, s + depth + 2)
    d = ImageDraw.Draw(img)
    x0, y0 = 1, 1 + depth
    d.polygon([(x0, y0), (x0 + depth, y0 - depth), (x0 + s + depth - 1, y0 - depth),
               (x0 + s - 1, y0)], fill=rgba(faces[0]))
    d.rectangle([x0, y0, x0 + s - 1, y0 + s - 1], fill=rgba(faces[1]))
    d.polygon([(x0 + s - 1, y0), (x0 + s + depth - 1, y0 - depth),
               (x0 + s + depth - 1, y0 + s - depth - 1), (x0 + s - 1, y0 + s - 1)],
              fill=rgba(faces[2]))
    if outline:
        d.line([(x0, y0), (x0 + depth, y0 - depth), (x0 + s + depth - 1, y0 - depth),
                (x0 + s + depth - 1, y0 + s - depth - 1), (x0 + s - 1, y0 + s - 1),
                (x0, y0 + s - 1), (x0, y0)], fill=rgba(outline))
    return img


def iso_cube(s=16, faces=("2", "3", "4"), outline="K"):
    """Pixel-art isometric (2:1) cube, s = edge length in pixels along the 2:1 lines."""
    w = 2 * s
    img = blank(w + 2, 2 * s + 2)
    top = [(1 + s, 1), (w, 1 + s // 2), (1 + s, 1 + s), (1, 1 + s // 2)]
    # faces via polygons (left = lit, right = shadow)
    d = ImageDraw.Draw(img)
    d.polygon([(1, 1 + s // 2), (1 + s, 1 + s), (1 + s, 1 + 2 * s - 1), (1, 1 + s + s // 2 - 1)],
              fill=rgba(faces[1]))
    d.polygon([(1 + s, 1 + s), (w, 1 + s // 2), (w, 1 + s + s // 2 - 1), (1 + s, 1 + 2 * s - 1)],
              fill=rgba(faces[2]))
    d.polygon(top, fill=rgba(faces[0]))
    if outline:
        d.line(top + [top[0]], fill=rgba(outline))
        d.line([(1, 1 + s // 2), (1, 1 + s + s // 2 - 1), (1 + s, 1 + 2 * s - 1),
                (w, 1 + s + s // 2 - 1), (w, 1 + s // 2)], fill=rgba(outline))
        d.line([(1 + s, 1 + s), (1 + s, 1 + 2 * s - 1)], fill=rgba(outline))
    return img


def slope_line(segments, color="K", horizontal=True, size=None):
    """A line built from run lengths, on a canvas just big enough."""
    n = sum(segments)
    m = len(segments)
    w, h = (n, m) if horizontal else (m, n)
    if size:
        w, h = size
    img = blank(w, h)
    steps_line(img, 0, 0, segments, color, horizontal)
    return img


def arc(radius=12, color="K", jaggy=False):
    """Quarter circle from top to right side, as runs. jaggy=True uses an irregular,
    non-monotonic run sequence (what freehand mouse drawing produces)."""
    runs = [5, 3, 2, 1, 1] if not jaggy else [5, 1, 3, 1, 2]
    img = blank(2 * radius, 2 * radius)
    x, y = 0, 0
    pts = []
    for n in runs:
        for _ in range(n):
            pts.append((x, y))
            x += 1
        y += 1
    # mirror runs across the diagonal for the steep half
    ex, ey = pts[-1]
    for px, py in reversed(pts[:-1]):
        dx, dy = ex - px, ey - py
        pts.append((ex + dy, ey + dx))
    for px, py in pts:
        put(img, px + 1, py + 1, color)
    return img.crop(img.getbbox() if img.getbbox() else (0, 0, 1, 1))


def doubles_line(clean=True, color="K"):
    """A 2:1-ish freehand stroke with L-shaped corners ('doubles') vs a pixel-perfect one."""
    img = blank(16, 8)
    x, y = 0, 0
    for n in (3, 2, 3, 2, 3, 2):
        for _ in range(n):
            put(img, x, y, color)
            x += 1
        if not clean:
            put(img, x - 1, y + 1, color)  # the extra corner pixel
        y += 1
    return img
