"""Ch. 25 (micro-res, Environmental Station Alpha-like *spirit*): the Greenhouse redrawn at
160x120 with 8x8 tiles and a 5x7 Kit. Free colours (not NES), but tiny palettes: one hue
family per area + black + the hero's warm accent. Original art - ESA is only described.
"""
from __future__ import annotations

from PIL import Image

W, H = 160, 120
PAL = {  # greenhouse micro palette (9 colours)
    "K": (8, 11, 16), "d": (14, 33, 35), "e": (22, 56, 50), "m": (44, 110, 76),
    "l": (128, 196, 96), "h": (226, 244, 170),
    "R": (226, 72, 52), "r": (150, 36, 40), "C": (252, 226, 168),
}
CISTERN = {"K": (6, 8, 18), "d": (14, 22, 52), "e": (24, 42, 96), "m": (44, 84, 160),
           "l": (100, 160, 230), "h": (210, 236, 255), "R": (226, 72, 52), "r": (150, 36, 40),
           "C": (252, 226, 168)}

KIT = {  # 5 x 7 frames, facing right. R hood, r shade, K face, C eye/lantern
    "stand": [".RR..", "RRRR.", "RRKC.", "rRRR.", ".rRRC", ".r.r.", ".r.r."],
    "step":  [".....", ".RR..", "RRRR.", "RRKC.", "rRRRC", ".rRr.", "r...r"],
    "blink": [".RR..", "RRRR.", "RRKK.", "rRRR.", ".rRRC", ".r.r.", ".r.r."],
    "jump":  [".RR..", "RRRR.", "RRKC.", "rRRRC", ".rRR.", "r..r.", "....."],
}
HOPPER = {  # 5 x 4: cap + feet. The micro foe uses the area's light tones, never the hero red.
    "stand": [".hhh.", "hlhlh", ".KlK.", ".l.l."],
    "squash": [".....", ".hhh.", "hlhlh", "ll.ll"],
}
KIT_ANIMS = {"idle": (["stand", "stand", "blink"], [600, 600, 150]),
             "walk": (["stand", "step"], [160, 160])}

T8 = {  # 8x8 tiles
    "ground_top": ["hhhhhhhh", "llllllll", "lmlmlmlm", "mmmmmmmm", "memememe", "eeeeeeee",
                   "edededed", "dddddddd"],
    "ground": ["dddddddd", "dKdddKdd", "dddddddd", "ddKddddd", "dddddddd", "dddddKdd",
               "dKdddddd", "dddddddd"],
    "wall": ["KKKKKKKK", "KKKKKKKK", "KKdKKKKK", "KKKKKKKK", "KKKKKKKK", "KKKKKKdK",
             "KKKKKKKK", "KKKKKKKK"],
    "wall_seam": ["dddddddd", "KKKKKKKK", "KKKKKKKK", "KKKKKKKK", "KKKKKKKK", "KKKKKKKK",
                  "KKKKKKKK", "KKKKKKKK"],
    "glass": ["dddddddd", "dKKKKKKd", "dKKKKeKd", "dKKKeKKd", "dKKeKKKd", "dKKKKKKd",
              "dKKKKKKd", "dddddddd"],
    "edge_l": ["hlmmeedd", "lmmeeddd", "mmeedddd", "meeddddd", "eedddddd", "eddddddd",
               "dddddddd", "dddddddd"],
    "plant": ["........", "...l....", "..lml...", "...m..l.", ".l.m.lm.", "..mm.m..",
              "...mmm..", "...me..."],
    "grass": ["........", "........", "........", "........", "........", "..l...l.",
              ".lm.l.ml", "lmmlmmml"],
    "vine": ["...m....", "...m....", "....m...", "....e...", "...m....", "...e.l..", "...m....",
             "....e..."],
    "vine_end": ["...m....", "....m...", "....l...", "........", "........", "........",
                 "........", "........"],
    "term": ["........", "........", ".eeeee..", ".eKlKe..", ".eKKKe..", ".eeeee..", "..eme...",
             ".emmme.."],
    "pod_tl": ["........", "........", "........", "........", "......mm", "....mmll", "...mllhl",
               "..mlllhh"],
    "pod_tr": ["........", "........", "........", "........", "mm......", "lmm.....", "llmm....",
               "lllm...."],
    "pod_bl": ["..mllllh", "..emllll", "...emlll", "....emmm", "......ee", ".......m", "......m.",
               ".....mmm"],
    "pod_br": ["lllm....", "llme....", "lmme....", "mme.....", "ee......", "........", "........",
               "m......."],
    "lamp": ["........", "...dd...", "..dCCd..", "..dCCd..", "...dd...", "...d....",
             "........", "........"],
}

ROOM = [  # 20 x 15 tiles (160x120)
    "####################",
    "#.vgg..gg..ggv.gg..#",
    "#.vgg..gg..ggv.gg.v#",
    "#.j......P...j....v#",
    "#.................j#",
    "#......^^^^^.......#",
    "#......#####.......#",
    "#..L...........L...#",
    "#..................#",
    "#...p.......,,..t..#",
    "#^^^^^^^...^^^^^^^^#",
    "########...#########",
    "########...#########",
    "########^^^#########",
    "####################",
]


def _tile(name, pal):
    rows = T8[name]
    im = Image.new("RGBA", (8, 8))
    px = im.load()
    for y, r in enumerate(rows):
        for x, c in enumerate(r):
            if c != ".":
                px[x, y] = pal[c] + (255,)
    return im


def room(pal=PAL):
    im = Image.new("RGBA", (W, H), pal["K"] + (255,))
    for ty, r in enumerate(ROOM):
        for tx, c in enumerate(r):
            x, y = tx * 8, ty * 8
            if c in ".pL,vjtP":
                im.alpha_composite(_tile("wall_seam" if ty % 4 == 0 else "wall", pal), (x, y))
            if c == "g":
                im.alpha_composite(_tile("glass", pal), (x, y))
            elif c == "#":
                above = ROOM[ty - 1][tx] if ty else "#"
                im.alpha_composite(_tile("ground" if above in "#^" else "ground_top", pal), (x, y))
            elif c == "^":
                im.alpha_composite(_tile("ground_top", pal), (x, y))
            elif c == "p":
                im.alpha_composite(_tile("plant", pal), (x, y + 0))
            elif c == "t":
                im.alpha_composite(_tile("term", pal), (x, y))
            elif c == ",":
                im.alpha_composite(_tile("grass", pal), (x, y))
            elif c == "v":
                im.alpha_composite(_tile("vine", pal), (x, y))
            elif c == "j":
                im.alpha_composite(_tile("vine_end", pal), (x, y))
            elif c == "L":
                im.alpha_composite(_tile("lamp", pal), (x, y))
    for ty, r in enumerate(ROOM):  # 2x2 seed pods last, over the wall tiles
        for tx, c in enumerate(r):
            if c == "P":
                for i, part in enumerate(("pod_tl", "pod_tr", "pod_bl", "pod_br")):
                    im.alpha_composite(_tile(part, pal), (tx * 8 + (i % 2) * 8, ty * 8 + (i // 2) * 8))
    return _rims(im, pal)


def _rims(im, pal):
    """1 px rims where solid ground meets open space (left/right faces and ceilings)."""
    px = im.load()
    solid = lambda tx, ty: 0 <= ty < len(ROOM) and 0 <= tx < len(ROOM[0]) and ROOM[ty][tx] in "#^"
    for ty, r in enumerate(ROOM):
        for tx, c in enumerate(r):
            if c not in "#^":
                continue
            x, y = tx * 8, ty * 8
            if 0 < tx and not solid(tx - 1, ty):
                for j in range(8):
                    px[x, y + j] = pal["e"] + (255,)
            if tx < len(r) - 1 and not solid(tx + 1, ty):
                for j in range(8):
                    px[x + 7, y + j] = pal["e"] + (255,)
            if ty < len(ROOM) - 1 and not solid(tx, ty + 1) and c == "#":
                for i in range(8):
                    px[x + i, y + 7] = pal["e"] + (255,)
    return im


def kit(frame="stand", pal=PAL, flip=False):
    rows = KIT[frame]
    im = Image.new("RGBA", (5, 7))
    px = im.load()
    for y, r in enumerate(rows):
        for x, c in enumerate(r):
            if c != ".":
                px[x, y] = pal[c] + (255,)
    return im.transpose(Image.Transpose.FLIP_LEFT_RIGHT) if flip else im


def kit_frames(anim="idle", pal=PAL):
    names, d = KIT_ANIMS[anim]
    return [kit(n, pal) for n in names], d


def scene(t=0, pal=PAL):
    """Room + Kit walking along the lower floor + drifting 1 px spores."""
    im = room(pal)
    u = (t // 160) % 80  # ping-pong along the lower floor
    back = u >= 40
    x = 20 + (80 - u if back else u)  # stays on the floor left of the pit
    fr = "step" if (t // 160) % 2 else "stand"
    im.alpha_composite(kit(fr, pal, flip=back), (x, 80 - 7))
    for i in range(7):
        sx = (17 + i * 23) % W
        sy = 20 + (i * 37 - t // 60) % 70
        im.putpixel((sx, sy), pal["l"] + (255,))
    return im
