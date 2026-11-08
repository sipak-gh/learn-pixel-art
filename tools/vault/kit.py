"""Kit, the hero of `hollow-vault`: a 16x24 hooded vault keeper with a lantern.

Built from parts on an indexed canvas (slots: 1 = black outline/shadow, 2 = suit, 3 = light),
so every pose shares the same construction. Frames are 24x24 cells; Kit's body occupies the
central 16 columns (x 4..19) = 2x3 hardware sprites; only attack frames use the third column.

Sprite sub-palette SP0 = (transparent, $0F black, $16 red, $37 cream).
"""
from __future__ import annotations

from nes import ICanvas, render, g

PAL = (0x0F, 0x0F, 0x16, 0x37)          # slot 0 unused (transparent)
FW, FH = 24, 24
OX = 4                                   # body x-offset inside the 24 px cell

# --- parts in body coordinates (16 x 24 box, feet on row 22, outline row 23) -------------
HEAD = {3: (7, 10), 4: (5, 12), 5: (4, 13), 6: (4, 13), 7: (4, 13), 8: (4, 13), 9: (4, 13),
        10: (4, 13), 11: (4, 12)}
TIPS = {
    "back": {6: (2, 3), 7: (1, 2), 8: (1, 1)},
    "flat": {5: (2, 3), 6: (0, 3), 7: (0, 0)},
    "up": {4: (2, 4), 3: (1, 3), 2: (0, 1)},
    "down": {7: (3, 3), 8: (2, 3), 9: (2, 2), 10: (2, 2)},
}
FACE = {6: (10, 12), 7: (9, 13), 8: (9, 14), 9: (9, 14), 10: (10, 13)}
EYES = {"open": [(10, 7), (10, 8), (12, 7), (12, 8)],
        "blink": [(10, 8), (12, 8)],
        "hurt": [(10, 8), (12, 8), (11, 7)],
        "focus": [(11, 7), (11, 8), (13, 7), (13, 8)]}
HILITE = [(7, 3), (8, 3), (5, 4), (6, 4), (4, 5)]
MANTLE = {12: (3, 11), 13: (3, 11), 14: (4, 10)}
TUNIC = {15: (5, 10), 16: (5, 10), 17: (5, 10), 18: (4, 10), 19: (4, 11)}
LEGS = {
    # near leg drawn in suit colour, far leg in black (reads as "further away")
    "stand": ({20: (8, 9), 21: (8, 9), 22: (8, 10)}, {20: (5, 6), 21: (5, 6), 22: (5, 7)}),
    "contact": ({20: (9, 10), 21: (10, 11), 22: (11, 13)}, {20: (4, 5), 21: (3, 4), 22: (2, 4)}),
    "contact2": ({20: (4, 5), 21: (3, 4), 22: (2, 4)}, {20: (9, 10), 21: (10, 11), 22: (11, 13)}),
    "pass": ({20: (7, 8), 21: (8, 9), 22: (8, 10)}, {20: (5, 6), 21: (5, 6), 22: (4, 6)}),
    "pass2": ({20: (6, 7), 21: (6, 7), 22: (6, 8)}, {20: (8, 9), 21: (9, 10), 22: (9, 11)}),
    "lift": ({20: (8, 9), 21: (9, 10), 22: (10, 11)}, {20: (5, 6), 21: (5, 6), 22: (4, 6)}),
    "run_a": ({20: (9, 10), 21: (11, 12), 22: (12, 14)}, {20: (4, 5), 21: (2, 4), 22: (1, 2)}),
    "run_b": ({20: (7, 9), 21: (8, 9)}, {20: (5, 6), 21: (4, 5), 22: (3, 4)}),
    "run_c": ({20: (4, 5), 21: (2, 4), 22: (1, 2)}, {20: (9, 10), 21: (11, 12), 22: (12, 14)}),
    "run_d": ({20: (5, 6), 21: (4, 5), 22: (3, 4)}, {20: (7, 9), 21: (8, 9)}),
    "tuck": ({20: (7, 10), 21: (9, 10)}, {20: (4, 6), 21: (4, 5)}),
    "dangle": ({20: (8, 9), 21: (8, 9), 22: (8, 9)}, {20: (5, 6), 21: (5, 6), 22: (4, 5)}),
    "squat": ({20: (9, 11), 21: (10, 12), 22: (10, 13)}, {20: (3, 5), 21: (2, 4), 22: (1, 4)}),
    "brace": ({20: (9, 10), 21: (10, 11), 22: (10, 12)}, {20: (4, 5), 21: (3, 4), 22: (2, 4)}),
}
# arm: (sleeve spans, hand pixel) ; lantern: top-left of the 2x3 glow (handle above it)
ARMS = {
    "hang": ({15: (11, 12)}, (13, 15), (13, 17)),
    "hang_b": ({15: (11, 12)}, (12, 16), (12, 18)),      # lantern swung back a pixel
    "hang_f": ({15: (11, 13)}, (14, 15), (14, 17)),      # swung forward
    "up": ({13: (11, 12), 12: (12, 13)}, (14, 11), (14, 13)),
    "back": ({15: (2, 4)}, (1, 15), (0, 17)),
    "reach": ({14: (11, 14)}, (15, 14), (16, 16)),
    "throw": ({13: (11, 15)}, (16, 13), (17, 14)),
    "pump_f": ({15: (11, 13), 16: (13, 13)}, (14, 16), (14, 18)),
    "pump_b": ({15: (2, 4)}, (1, 16), (1, 18)),
}


def kit(legs="stand", arm="hang", tip="back", eyes="open", bob=0, lean=0, squash=0,
        lantern=True, flash=False, mantle_line=False, hl=None):
    """One 24x24 indexed frame. bob: body y offset (+ = down); lean: head/torso x offset;
    squash: lowers the head onto the mantle by n px (landing)."""
    c = ICanvas(FW, FH)
    hx, hy = OX + lean, bob + squash
    tx, ty = OX + lean // 2 if lean > 0 else OX + lean, bob
    near, far = LEGS[legs]
    sleeve, hand, lamp = ARMS[arm]
    # interiors (suit colour) -> outline -> details
    c.spans(HEAD, "2", hx, hy)
    c.spans(TIPS[tip], "2", hx, hy)
    c.spans(MANTLE, "2", tx, ty + squash // 2)
    c.spans(TUNIC, "2", tx, ty)
    c.spans(near, "2", OX, 0)
    c.spans(far, "9", OX, 0)                      # placeholder slot -> black after outline
    c.spans(sleeve, "2", tx, ty)
    c.px([hand], "3", tx, ty)
    if lantern:
        lx, ly = lamp
        c.spans({ly: (lx, lx + 1), ly + 1: (lx, lx + 1)}, "3", tx, ty)
        c.spans({ly + 2: (lx, lx + 1)}, "2", tx, ty)
    c.outline("1")
    c.a = [["1" if ch == "9" else ch for ch in r] for r in c.a]
    if lantern:
        c.px([(lamp[0] + 1, lamp[1] - 1)], "1", tx, ty)     # handle
    # mantle shadow edge and belt
    if mantle_line:
        c.px([(x, 14) for x in range(4, 11)], "1", tx, ty + squash // 2)
    c.px([(x, 17) for x in range(5, 11)], "1", tx, ty)
    c.px([(7, 17)], "3", tx, ty)
    c.px([(10, 18), (10, 19), (11, 19), (9, 19)], "1", tx, ty)
    # face + eyes + highlights
    c.spans(FACE, "1", hx, hy)
    c.px(EYES[eyes], "3", hx, hy)
    c.px(HILITE if hl is None else hl, "3", hx, hy)
    grid = c.grid()
    if flash:  # hurt flash: everything light except outline
        grid = [r.replace("2", "3") for r in grid]
    return grid


def img(grid, pal=PAL):
    return render(grid, pal)


# --- animations: (name, [(pose kwargs)], durations ms) -----------------------------------
ANIMS = {
    "idle": ([dict(), dict(bob=1, arm="hang_b"), dict(bob=1, arm="hang_b", eyes="blink"),
              dict(arm="hang")], [500, 400, 120, 400]),
    "walk": ([dict(legs="contact", arm="hang_b"), dict(legs="pass", bob=-1, arm="hang"),
              dict(legs="contact2", arm="hang_f"), dict(legs="pass2", bob=-1, arm="hang")],
             [140, 140, 140, 140]),
    "run": ([dict(legs="run_a", lean=1, tip="flat", arm="pump_b"),
             dict(legs="run_b", lean=1, tip="flat", bob=-1, arm="hang"),
             dict(legs="run_c", lean=1, tip="flat", arm="pump_f"),
             dict(legs="run_d", lean=1, tip="flat", bob=-1, arm="hang")], [90, 90, 90, 90]),
    "jump": ([dict(legs="squat", squash=1, bob=1, arm="hang_b", tip="back"),
              dict(legs="tuck", tip="down", arm="up", bob=-1),
              dict(legs="tuck", tip="back", arm="up", bob=-1),
              dict(legs="dangle", tip="up", arm="hang_f", bob=-1),
              dict(legs="squat", squash=1, bob=1, arm="hang", tip="back")],
             [80, 160, 120, 160, 100]),
    "attack": ([dict(legs="brace", arm="back", eyes="focus", lean=-1),
                dict(legs="brace", arm="throw", eyes="focus", lean=1, tip="flat"),
                dict(legs="brace", arm="reach", eyes="focus", lean=1),
                dict(legs="stand", arm="hang_f")], [120, 60, 160, 120]),
    "hurt": ([dict(legs="brace", arm="up", eyes="hurt", lean=-1, tip="up", flash=True),
              dict(legs="brace", arm="up", eyes="hurt", lean=-1, tip="up")], [80, 80]),
}


def frames(name):
    poses, d = ANIMS[name]
    return [img(kit(**p)) for p in poses], d


def grids(name):
    return [kit(**p) for p in ANIMS[name][0]]
