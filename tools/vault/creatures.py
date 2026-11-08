"""Enemies of `hollow-vault` (16x16 each = 2x2 hardware sprites, one sprite sub-palette).

slots: 1 = black outline, 2 = main colour, 3 = light colour.
"""
from __future__ import annotations

from nes import ICanvas, render, gflip


# --- spore hopper: a mushroom-capped hopper (faces left) ----------------------------------
def hopper(cap_y=3, squash=0, legs="stand", spores=False):
    c = ICanvas(16, 16)
    y = cap_y
    cap = {y: (5, 10), y + 1: (3, 12), y + 2: (2, 13), y + 3: (1, 14), y + 4: (1, 14)}
    if squash > 0:
        cap = {y: (4, 11), y + 1: (2, 13), y + 2: (1, 14), y + 3: (0, 15), y + 4: (0, 15)}
    c.spans(cap, "2")
    by = y + 5
    body_h = 4 - squash
    body = {by + i: (4, 11) if i else (5, 10) for i in range(body_h)}
    c.spans(body, "3")
    fy = by + body_h
    feet = {"stand": {fy: [(4, 6), (9, 11)]},
            "crouch": {fy: [(3, 6), (9, 12)]},
            "air": {fy: [(5, 6), (9, 10)], fy + 1: [(5, 5), (10, 10)]},
            "none": {}}[legs]
    c.spans(feet, "2")
    c.outline("1")
    # gills: black band under the cap
    c.spans({by: (4, 11)}, "1")
    c.px([(5, by), (10, by)], "1")
    # cap spots + rim light (light from upper left)
    c.px([(4, y + 1), (5, y + 1), (3, y + 2), (8, y + 2), (9, y + 2), (9, y + 1), (12, y + 3), (6, y + 3)], "3")
    c.px([(13, y + 4), (12, y + 4)], "1")
    # eyes (facing left)
    c.px([(5, by + 1), (5, by + 2), (8, by + 1), (8, by + 2)], "1")
    return c.grid()


HOPPER_ANIMS = {
    "idle": ([dict(cap_y=4), dict(cap_y=5, squash=1, legs="stand")], [400, 400]),
    "hop": ([dict(cap_y=5, squash=1, legs="crouch"), dict(cap_y=1, legs="air"),
             dict(cap_y=2, legs="air"), dict(cap_y=5, squash=1, legs="crouch")], [160, 140, 140, 120]),
}


# --- drip slug: crawls along floors (or ceilings, flipped) --------------------------------
def slug(stretch=0, eye=0):
    c = ICanvas(16, 16)
    x0 = 2 - stretch
    body = {11: (x0 + 3, 12), 12: (x0 + 1, 13), 13: (x0, 14)}
    head = {8: (3, 5), 9: (2, 6), 10: (2, 7)}
    shell = {6: (8, 11), 7: (6, 13), 8: (6, 14), 9: (6, 14), 10: (7, 13)}
    c.spans(body, "2")
    c.spans(head, "2")
    c.spans(shell, "3")
    # eye stalks
    c.px([(3, 7 - eye), (3, 6 - eye), (5, 7 - eye), (5, 6 - eye)], "2")
    c.outline("1")
    c.px([(3, 5 - eye), (5, 5 - eye)], "3")
    # shell spiral (dark) + body underside shading
    c.px([(10, 8), (11, 8), (12, 9), (11, 10), (10, 10), (9, 9), (10, 9)], "1")
    c.px([(9, 7), (8, 8)], "2")
    c.spans({13: (x0 + 1, 13)}, "1") if stretch == 0 else c.spans({13: (x0 + 1, 13)}, "1")
    c.px([(x + x0, 13) for x in range(2, 12, 3)], "2")
    return c.grid()


SLUG_ANIMS = {"crawl": ([dict(stretch=0), dict(stretch=1, eye=1)], [260, 260])}


# --- warden drone: hovering maintenance drone with one eye -------------------------------
def drone(rotor=0, bob=0, eye="open"):
    c = ICanvas(16, 16)
    y = 4 + bob
    body = {y: (6, 9), y + 1: (4, 11), y + 2: (3, 12), y + 3: (3, 12), y + 4: (3, 12),
            y + 5: (3, 12), y + 6: (4, 11), y + 7: (6, 9)}
    c.spans(body, "2")
    c.spans({y - 1: (7, 8)}, "2")                          # mast
    c.spans([{y - 2: (2, 13)}, {y - 2: (5, 10)}][rotor], "2")  # rotor blur
    c.spans({y + 8: [(5, 5), (10, 10)]}, "2")             # little claws
    c.outline("1")
    # big lens (facing left): black ring with a green pupil
    c.spans({y + 2: (4, 7), y + 3: (3, 8), y + 4: (3, 8), y + 5: (4, 7)}, "1")
    if eye == "open":
        c.spans({y + 3: (4, 5), y + 4: (4, 5)}, "3")
        c.px([(6, y + 3)], "3")
    else:
        c.spans({y + 4: (4, 6)}, "3")
    # panel seam + shadow side (light from upper left)
    c.px([(10, y + 2), (11, y + 3), (11, y + 4), (10, y + 5), (9, y + 6)], "1")
    c.px([(x, y + 6) for x in range(5, 9)], "1")
    return c.grid()


DRONE_ANIMS = {"hover": ([dict(rotor=0, bob=0), dict(rotor=1, bob=0), dict(rotor=0, bob=1),
                          dict(rotor=1, bob=1)], [100, 100, 100, 100]),
               "alert": ([dict(rotor=0, eye="open"), dict(rotor=1, eye="blink")], [80, 80])}

CREATURES = {"hopper": (hopper, HOPPER_ANIMS), "slug": (slug, SLUG_ANIMS), "drone": (drone, DRONE_ANIMS)}


def frames(kind, anim, sub):
    fn, anims = CREATURES[kind]
    poses, d = anims[anim]
    return [render(fn(**p), sub) for p in poses], d


def grids(kind, anim):
    fn, anims = CREATURES[kind]
    return [fn(**p) for p in anims[anim][0]]
