"""The enemy: a mauve slime, 24x24 frames, faces left (toward the hero), light upper left.

The body is a dome generated from (width, height): squash and stretch keep the area about
constant, which is exactly the rule taught in ch15. Eyes ride on the body so they squash too.
"""
from __future__ import annotations

import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pix import Anim, blank, outline_in, put, silhouette  # noqa

FW, FH = 24, 24
LIGHT, BODY, DARK, SPEC = "k", "P", "p", "W"


def body(w: float, h: float, lift: int = 0, eyes=True, look=-1, blink=False, cx=12.0):
    """Dome of width w and height h sitting on y=22 minus lift."""
    img = blank(FW, FH)
    base = FH - 1.5 - lift
    for y in range(FH):
        for x in range(FW):
            nx = (x + 0.5 - cx) / (w / 2)
            ny = (y + 0.5 - base) / h  # -1 at the top, 0 at the base
            if ny > 0.02 or nx * nx + ny * ny > 1:
                continue
            # crescents in normalised space: lit upper-left rim, shadow lower-right
            lit = math.hypot(nx - 0.25, ny - 0.25) > 1.08 and nx < 0.05
            shade = math.hypot(nx + 0.3, ny + 0.25) > 0.95 or ny > -0.15
            put(img, x, y, DARK if shade else (LIGHT if lit else BODY))
    # specular glint
    gx, gy = int(cx - w * 0.22), int(base - h * 0.72)
    put(img, gx, gy, SPEC)
    if h > 6:
        put(img, gx, gy + 1, SPEC)
    if eyes:
        ey = int(base - h * 0.5)
        ex = int(cx + look * w * 0.12)
        for dx in (-2, 2):
            x = ex + dx - (1 if dx > 0 else 0) * 0
            if blink or h < 6:
                put(img, x, ey, "K")
                put(img, x + 1, ey, "K")
            else:
                put(img, x, ey, "K")
                put(img, x, ey - 1, "K")
                put(img, x + (1 if look > 0 else 0), ey - 1, "K")
    return outline_in(img, "K")


def idle() -> Anim:
    f = [body(16, 9), body(17, 8.5), body(18, 8), body(17, 8.5, blink=True)]
    return Anim("idle", f, [180, 140, 180, 140])


def hop() -> Anim:
    f = [
        body(20, 6),             # anticipation: squash
        body(12, 12, lift=1),    # launch: stretch
        body(14, 10, lift=5),    # rising
        body(16, 9, lift=7),     # apex: round
        body(14, 10, lift=3),    # falling: stretch again
        body(22, 5),             # landing: big squash
        body(17, 8.5),           # settle
    ]
    return Anim("hop", f, [140, 60, 70, 110, 70, 90, 120], loop=True)


def hurt() -> Anim:
    flash = silhouette(body(13, 10), "W")
    f = [flash, body(13, 10, cx=13.5, blink=True), body(17, 8.5, cx=12.5)]
    return Anim("hurt", f, [60, 120, 140], loop=False)


def death() -> Anim:
    flash = silhouette(body(16, 9), "W")
    splat = body(22, 4, eyes=False)
    puddle = blank(FW, FH)
    for x in range(3, 21):
        put(puddle, x, FH - 2, DARK if x in (3, 20) else BODY)
        put(puddle, x, FH - 1, "K" if 4 <= x <= 19 else DARK)
    for x in range(6, 18):
        put(puddle, x, FH - 3, BODY if x not in (6, 17) else DARK)
    put(puddle, 8, FH - 3, LIGHT)
    bubbles = puddle.copy()
    for x, y in ((7, FH - 6), (14, FH - 8), (11, FH - 10)):
        put(bubbles, x, y, LIGHT)
    fade = blank(FW, FH)
    for x in range(5, 19, 3):
        put(fade, x, FH - 1, DARK)
    put(fade, 12, FH - 13, LIGHT)
    f = [flash, body(19, 6, blink=True), splat, puddle, bubbles, fade, blank(FW, FH)]
    return Anim("death", f, [60, 80, 90, 160, 160, 160, 200], loop=False)


ANIMS = [idle, hop, hurt, death]


def all_anims():
    return [a() for a in ANIMS]
