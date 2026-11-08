"""Visual effects for mossy-ruins. Effects use the brightest colours in the palette and
very short frames; most have no outline and shrink or break apart rather than fading
(there is no transparency in the palette, so 'fading' = fewer, smaller pixels)."""
from __future__ import annotations

import math
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pix import Anim, blank, put  # noqa


def _disc(img, cx, cy, r, c, ring=0):
    for y in range(int(cy - r - 1), int(cy + r + 2)):
        for x in range(int(cx - r - 1), int(cx + r + 2)):
            d = math.hypot(x + 0.5 - cx, y + 0.5 - cy)
            if d <= r and (not ring or d > r - ring):
                put(img, x, y, c)


def dust() -> Anim:
    """Landing / skid dust, 24x12: two puff clusters spread sideways, rise and shrink."""
    frames = []
    spec = [(3, 2.5, 0), (5, 3.2, 1), (7, 3.2, 2), (9, 2.6, 3), (9, 1.6, 4)]
    for spread, r, i in spec:
        f = blank(24, 12)
        for side in (-1, 1):
            cx = 12 + side * spread
            cy = 9 - i * 0.7
            body, top = (("1", "W"), ("1", "W"), ("2", "1"), ("2", "1"), ("3", "2"))[i]
            _disc(f, cx, cy, r, body)
            _disc(f, cx - side * 0.8 - 0.4, cy - 0.8, r * 0.55, top)
            if i < 3:  # a smaller trailing puff
                _disc(f, cx - side * (r + 0.5), cy + 1, r * 0.5, body)
        frames.append(f)
    return Anim("dust", frames, [50, 60, 70, 80, 90], loop=False)


def spark() -> Anim:
    """Hit spark, 16x16: a white flash, a 4-point star, rays flying out, embers."""
    frames = []
    f = blank(16, 16)
    _disc(f, 8, 8, 3.5, "W")
    frames.append(f)
    f = blank(16, 16)
    for t in range(-6, 7):
        c = "W" if abs(t) < 3 else ("Y" if abs(t) < 5 else "y")
        put(f, 8 + t, 8, c)
        put(f, 8, 8 + t, c)
    _disc(f, 8, 8, 1.6, "W")
    frames.append(f)
    f = blank(16, 16)
    for a in range(8):
        ang = a * math.pi / 4
        for d in range(4, 7 + (a % 2)):
            put(f, 8 + round(math.cos(ang) * d), 8 + round(math.sin(ang) * d), "Y" if d < 6 else "o")
    frames.append(f)
    f = blank(16, 16)
    for a in range(8):
        ang = a * math.pi / 4 + 0.2
        put(f, 8 + round(math.cos(ang) * 7), 8 + round(math.sin(ang) * 7), "o")
    frames.append(f)
    return Anim("spark", frames, [40, 50, 60, 70], loop=False)


def sparkle() -> Anim:
    """Pickup / magic twinkle, 8x8, loops."""
    shapes = [
        [(3, 3, "W")],
        [(3, 3, "W"), (3, 2, "a"), (3, 4, "a"), (2, 3, "a"), (4, 3, "a")],
        [(3, 3, "W"), (3, 1, "a"), (3, 2, "W"), (3, 4, "W"), (3, 5, "a"), (1, 3, "a"),
         (2, 3, "W"), (4, 3, "W"), (5, 3, "a")],
        [(3, 3, "a"), (3, 1, "u"), (3, 5, "u"), (1, 3, "u"), (5, 3, "u")],
        [],
    ]
    frames = []
    for s in shapes:
        f = blank(8, 8)
        for x, y, c in s:
            put(f, x, y, c)
        frames.append(f)
    return Anim("sparkle", frames, [80, 70, 120, 80, 300])


def smoke() -> Anim:
    """Torch smoke / poof, 16x24: puffs rise, drift right, grow, then break up."""
    frames = []
    rng = random.Random(3)
    for i in range(6):
        f = blank(16, 24)
        for k in range(3):
            age = i - k
            if age < 0 or age > 4:
                continue
            cx = 7 + age * 0.8 + k * 0.5
            cy = 20 - age * 4
            r = 1.5 + age * 0.7
            col = ["2", "2", "3", "3", "4"][age]
            if age == 4:
                for _ in range(4):
                    put(f, int(cx + rng.randint(-2, 2)), int(cy + rng.randint(-2, 2)), col)
            else:
                _disc(f, cx, cy, r, col)
                _disc(f, cx - 0.6, cy - 0.6, max(0.8, r - 1.2), "1" if age < 2 else "2")
        frames.append(f)
    return Anim("smoke", frames, 100)


def slash() -> Anim:
    """A standalone slash arc, 32x32, for effects layers (the hero's smear is drawn into
    the attack frames; this is the 'add-on' version engines spawn separately)."""
    frames = []
    for i, (a0, a1, w) in enumerate([(-100, -40, 3), (-110, 40, 4), (-60, 70, 2), (10, 80, 1)]):
        f = blank(32, 32)
        for ang in range(a0, a1 + 1, 2):
            ra = math.radians(ang)
            for d in range(13 - w, 13):
                c = "W" if d >= 12 - w // 2 else "1"
                put(f, 16 + round(math.cos(ra) * d), 18 + round(math.sin(ra) * d), c)
        frames.append(f)
    return Anim("slash", frames, [40, 50, 60, 70], loop=False)


ANIMS = [dust, spark, sparkle, smoke, slash]


def all_anims():
    return [a() for a in ANIMS]
