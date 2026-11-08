"""Common setup for figure scripts: puts tools/ and tools/art/ on the path and re-exports
the pix toolkit. Usage in a figure script:  from _fig import *"""
import math  # noqa: F401
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TOOLS = os.path.dirname(HERE)
sys.path[:0] = [TOOLS, os.path.join(TOOLS, "art")]

from pix import *  # noqa: E402,F401,F403
from pix import Image, ImageDraw  # noqa: E402,F401

SPR_BG = (110, 124, 156)   # neutral mid blue-grey behind sprites
LIGHT_BG = (192, 203, 220)  # palette '1', for silhouettes and line art


def ball_frame(w, h, x, y, d=8, sx=1.0, sy=1.0, color="R", floor=None):
    """A w x h frame with a ball (diameter d, scaled sx/sy, bottom-centred at x, y)."""
    img = blank(w, h)
    if floor is not None:
        rect(img, 0, floor, w, h - floor, "4")
    rw, rh = d * sx / 2, d * sy / 2
    cy = y - rh
    for yy in range(h):
        for xx in range(w):
            if ((xx + 0.5 - x) / rw) ** 2 + ((yy + 0.5 - cy) / rh) ** 2 <= 1:
                put(img, xx, yy, color)
    return img


def anim_gif(name, frames, durations, k=4, bg="FIG"):
    save_gif(frames, os.path.join(IMAGES, name), durations, k, bg)
    print("wrote images/" + name)


def side_by_side(*anims, gap=4):
    """Frames of several Anims (same frame count) combined left to right, for a GIF."""
    out = []
    for i in range(len(anims[0])):
        fs = [a[i % len(a)] for a in anims]
        img = blank(sum(f.width for f in fs) + gap * (len(fs) - 1), max(f.height for f in fs))
        x = 0
        for f in fs:
            img.alpha_composite(f, (x, img.height - f.height))
            x += f.width + gap
        out.append(img)
    return out


def with_bg(frames, color):
    out = []
    for f in frames:
        b = blank(*f.size, color)
        b.alpha_composite(f)
        out.append(b)
    return out
