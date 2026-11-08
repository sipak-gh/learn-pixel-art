"""Ch. 25 figures: micro-res (ESA-like spirit) at 160x120 with a 5x7 Kit."""
from _v import *
from styles import micro as M

room = M.room()
k5 = M.kit("stand")


def chips(pal, keys="KdemlhRrC"):
    return row([view(Image.new("RGBA", (1, 1), pal[c] + (255,)), 22, grid=False, bg=FIG_BG) for c in keys], 2)


# size comparison
nes_k = kitimg()
save(panel([(nv(nes_k, 6), "NES Kit 16 x 24 (6 sprites)"), (nv(k5, 6), "micro Kit 5 x 7"),
            (nv(nes_k, 1), "1x"), (nv(k5, 1), "1x")],
           title="Same character, 11x fewer pixels",
           note="384 pixels become 35 (22 drawn). There is no room for a face, hands or shading: "
                "only a shape, a colour and one bright pixel that says where Kit looks."),
     "ch25-sizes.png")

save(panel([(nv(room, 1), "1x: 160 x 120"), (nv(M.scene(0), 4), "4x")],
           title="The Greenhouse at micro-res",
           note="20 x 15 tiles of 8 x 8. Big quiet voids, bright 1 px rims on every edge you can "
                "stand on or bump into, one hue family plus the hero's red."), "ch25-room.png")

frames = [(f, M.kit(f)) for f in ("stand", "step", "blink", "jump")]
save(panel([(sv(im, 16, grid=True, major=None), n) for n, im in frames],
           title="All of micro Kit",
           note="Four frames cover idle, walk and jump. 'step' bobs the body 1 px down and opens "
                "the legs; 'blink' swaps one pixel."), "ch25-kit-frames.png")


def eye_variants():
    base = M.KIT["stand"]
    no_eye = [r.replace("C", "R") if i == 2 else r for i, r in enumerate(base)]
    no_lamp = [r.replace("C", ".") if i == 4 else r for i, r in enumerate(base)]
    out = []
    for name, rows_ in (("no eye", no_eye), ("eye", base), ("eye, no lamp", no_lamp)):
        M.KIT["_v"] = rows_
        im = Image.new("RGBA", (11, 11), M.PAL["K"] + (255,))
        im.alpha_composite(M.kit("_v"), (3, 2))
        out.append((view(im, 14, grid=False, bg=FIG_BG), name))
    del M.KIT["_v"]
    return out


save(panel(eye_variants(), title="One pixel is a feature",
           note="The cream eye pixel gives Kit a facing direction; the lamp pixel at the hip "
                "repeats it and links Kit to the lights in the room."), "ch25-one-pixel.png")

# micro foe
hop = [M.HOPPER[f] for f in ("stand", "squash")]


def grid_img(rows_, pal):
    im = Image.new("RGBA", (len(rows_[0]), len(rows_)))
    for y, r in enumerate(rows_):
        for x, c in enumerate(r):
            if c != ".":
                im.putpixel((x, y), pal[c] + (255,))
    return im


stage = Image.new("RGBA", (28, 12), M.PAL["K"] + (255,))
for x in range(28):
    stage.putpixel((x, 10), M.PAL["h"] + (255,))
    stage.putpixel((x, 11), M.PAL["l"] + (255,))
stage.alpha_composite(k5, (4, 3))
stage.alpha_composite(grid_img(hop[0], M.PAL), (18, 6))
st2 = stage.copy()
st2.paste(Image.new("RGBA", (6, 5), M.PAL["K"] + (255,)), (18, 5))
st2.alpha_composite(grid_img(hop[1], M.PAL), (18, 6))
save(panel([(view(stage, 14, grid=False, bg=FIG_BG), "hopper 5 x 4"),
            (view(st2, 14, grid=False, bg=FIG_BG), "squash frame")],
           title="Friend and foe at 5 pixels",
           note="Kit owns the warm red; every hazard is drawn from the area's light tones. "
                "Two frames are enough for a hop."), "ch25-foe.png")

save(panel([(nv(world.scene("greenhouse", 0)[0], 2), "NES 256 x 240 at 2x"),
            (nv(M.scene(0), 4), "micro 160 x 120 at 4x")],
           title="Same height on screen, very different pixels",
           note="At equal display size a micro pixel is 2x larger than an NES pixel; the micro "
                "room shows less detail but reads instantly."), "ch25-nes-vs-micro.png")

pals = [("Greenhouse", M.PAL), ("Cistern", M.CISTERN)]
save(panel([(column([nv(M.scene(0, p), 3), chips(p)], 8), n) for n, p in pals],
           title="One room, two area palettes (9 colours each)",
           note="Six tones of one hue for the world, plus Kit's two reds and a cream light. "
                "Changing six colours moves you to another part of the station."),
     "ch25-areas.png")

fr_, d_ = timeline(160 * 80, 80, lambda t: M.scene(t))
gif("ch25-walk.gif", fr_, d_, k=4)


# ---------------------------------------------------------------- building a room in passes
def room_pass(level, pal=M.PAL, rims=True):
    """The micro room built up to `level`: 1 masses, 2 rims, 3 wall detail, 4 plants and
    machines, 5 lights. Same tiles as styles.micro.room(); only the order is shown."""
    im = Image.new("RGBA", (M.W, M.H), pal["K"] + (255,))
    R = M.ROOM
    for ty, r in enumerate(R):
        for tx, c in enumerate(r):
            x, y = tx * 8, ty * 8
            above = R[ty - 1][tx] if ty else "#"
            if c in "#^":
                top = level >= 2 and rims and (c == "^" or above not in "#^")
                im.alpha_composite(M._tile("ground_top" if top else "ground", pal), (x, y))
            elif level >= 3:
                if c in ".pL,vjtP":
                    im.alpha_composite(M._tile("wall_seam" if ty % 4 == 0 else "wall", pal), (x, y))
                if c == "g":
                    im.alpha_composite(M._tile("glass", pal), (x, y))
            if level >= 4 and c in "p,vjt":
                im.alpha_composite(M._tile({"p": "plant", ",": "grass", "v": "vine", "j": "vine_end",
                                            "t": "term"}[c], pal), (x, y))
            if level >= 5 and c == "L":
                im.alpha_composite(M._tile("lamp", pal), (x, y))
    if level >= 4:
        for ty, r in enumerate(R):
            for tx, c in enumerate(r):
                if c == "P":
                    for i, part in enumerate(("pod_tl", "pod_tr", "pod_bl", "pod_br")):
                        im.alpha_composite(M._tile(part, pal), (tx * 8 + (i % 2) * 8, ty * 8 + (i // 2) * 8))
    return M._rims(im, pal) if (level >= 2 and rims) else im


assert room_pass(5).tobytes() == M.room().tobytes()
passes = [(room_pass(1), "1. masses: void + one dark"),
          (room_pass(2), "2. rims on every edge"),
          (room_pass(3), "3. quiet wall detail"),
          (room_pass(4), "4. plants and machines"),
          (room_pass(5), "5. two lamps (cream)"),
          (M.scene(0), "6. Kit + drifting spores")]
save(panel([(nv(im, 2), cap) for im, cap in passes], cols=3,
           title="A micro room in six passes",
           note="Each pass adds one job. The dark masses and the black void carry the layout; the "
                "rims make it playable; everything after that is mood."), "ch25-passes.png")

# ---------------------------------------------------------------- rims: avoid / better
no_rim = room_pass(5, rims=False)
box = (0, 64, 112, 120)
save(compare(column([nv(no_rim.crop(box), 4), nv(no_rim.crop(box), 1)], 8),
             column([nv(room.crop(box), 4), nv(room.crop(box), 1)], 8),
             "Avoid: flat masses, no rims", "Better: bright top rim, dim side rims",
             title="Rims tell you where you can stand",
             note="Same tiles and colours. Without rims, the floor, the pit and the wall are one dark "
                  "shape at 1x. The bright top row is the 'walk here' line."), "ch25-rims.png")

# ---------------------------------------------------------------- hero hue
greenkit = {**M.PAL, "R": M.PAL["l"], "r": M.PAL["m"], "C": M.PAL["h"]}
box2 = (8, 56, 96, 88)
bad = room.copy()
bad.alpha_composite(M.kit("stand", greenkit), (40, 73))
good = room.copy()
good.alpha_composite(M.kit("stand"), (40, 73))
save(compare(column([nv(bad.crop(box2), 5), nv(bad.crop(box2), 1)], 8),
             column([nv(good.crop(box2), 5), nv(good.crop(box2), 1)], 8),
             "Avoid: Kit in the area's greens", "Better: Kit in a hue the area never uses",
             title="The hero owns a hue",
             note="At 22 pixels, colour is the only thing that separates Kit from a plant. The red "
                  "appears nowhere else in the room, so the eye finds Kit at once."), "ch25-hero-hue.png")

# ---------------------------------------------------------------- colour jobs (measured)
from collections import Counter
scn = M.scene(0)
cnt = Counter(scn.get_flattened_data() if hasattr(scn, "get_flattened_data") else scn.getdata())
tot = M.W * M.H
JOBS = [("K", "void, wall faces"), ("d", "solid masses"), ("e", "wall lines, side rims"),
        ("m", "plant mid, vines"), ("l", "plant light, spores"), ("h", "top rims, highlights"),
        ("R", "Kit"), ("r", "Kit shade"), ("C", "lamps, Kit's eye")]
rows_img = []
for key, job in JOBS:
    n = cnt.get(M.PAL[key] + (255,), 0)
    sw = view(Image.new("RGBA", (1, 1), M.PAL[key] + (255,)), 26, grid=False, bg=FIG_BG)
    txt = Image.new("RGBA", (330, 26), FIG_BG + (255,))
    draw_text(txt, 8, 4, "#%02x%02x%02x  %-22s" % (M.PAL[key] + (job,)), 15)
    pct = Image.new("RGBA", (130, 26), FIG_BG + (255,))
    draw_text(pct, 0, 4, "%5d px  %4.1f%%" % (n, 100 * n / tot), 15)
    bar = Image.new("RGBA", (max(1, int(240 * n / tot)), 18), M.PAL[key] + (255,))
    rows_img.append(row([sw, txt, pct, bar], 6, align="center"))
print("colour jobs:", {k: cnt.get(M.PAL[k] + (255,), 0) for k, _ in JOBS})
save(figure(column(rows_img, 4, center=False), "Nine colours, nine jobs (pixels in one 160 x 120 frame)",
            "Half the screen is void and 40% is one dark tone. The three brightest colours cover "
            "about 3%: they are rare, so they are what you see."), "ch25-colour-jobs.png")

# ---------------------------------------------------------------- converting is not designing
nes_room = world.scene("greenhouse", 0)[0].convert("RGBA")


def shrink(im, method):
    out = Image.new("RGBA", (M.W, M.H), (0, 0, 0, 255))
    out.alpha_composite(im.resize((128, 120), method), (16, 0))
    return out


nn = shrink(nes_room, Image.Resampling.NEAREST)
box_ = shrink(nes_room, Image.Resampling.BOX)
ncol = len(set(box_.crop((16, 0, 144, 120)).get_flattened_data()))
print("box-shrunk colours:", ncol)
save(panel([(column([nv(nn, 3), nv(nn, 1)], 8), "Avoid: NES room halved (nearest)", FIG_BAD),
            (column([nv(box_, 3), nv(box_, 1)], 8), "Avoid: halved and smoothed (%d colours)" % ncol, FIG_BAD),
            (column([nv(M.scene(0), 3), nv(M.scene(0), 1)], 8), "Better: redrawn for 160 x 120", FIG_GOOD)],
           title="You cannot shrink your way to micro-res",
           note="Halving keeps every other pixel: thin lines break, the text turns to noise, and the room is "
                "as busy as before at half the size. Smoothing invents colours. Redesign instead."),
     "ch25-naive.png")
