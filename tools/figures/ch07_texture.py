"""Ch. 7 figures: dithering and texture under NES limits."""
import random
from _v import *

SUB = GH["bg"][0]
A, B = nes(0x0C), nes(0x1C)


def pat(fn, w=24, h=24):
    im = Image.new("RGBA", (w, h))
    px = im.load()
    for y in range(h):
        for x in range(w):
            px[x, y] = B if fn(x, y) else A
    return im


pats = [(lambda x, y: False, "0%"), (lambda x, y: x % 4 == 0 and y % 4 == 0, "6% dots"),
        (lambda x, y: (x + 2 * (y % 2)) % 4 == 0 and y % 2 == 0 or (x % 4 == 2 and y % 4 == 2) and False, "12%"),
        (lambda x, y: (x + y) % 2 == 0 and y % 2 == 0, "25%"),
        (lambda x, y: (x + y) % 2 == 0, "50% checker"),
        (lambda x, y: not ((x + y) % 2 == 0 and y % 2 == 0), "75%"),
        (lambda x, y: y % 2 == 0, "50% lines"), (lambda x, y: True, "100%")]
pats.pop(2)
save(panel([(nv(pat(f), 6), t) for f, t in pats], gap=12,
           title="Two NES colours, many in-between tones",
           note="Checkers and dot grids read as a new tone at 1x. Use them in large, calm areas - "
                "never on a sprite that moves."), "ch07-patterns.png")

# 2. ground depth: surface -> interior
lay = """
................
....######......
...########.....
...########.....
...########.....
"""
img, _, _ = rooms.build(lay, "greenhouse")
save(panel([(nv(img.crop((32, 0, 208, 80)), 4), "")],
           title="Depth inside solid ground: bright rim, brick, then a dark checker",
           note="Interior metatiles (all four neighbours solid) drop each brick colour one step "
                "and turn the faces into a 50% checker - the mass recedes."), "ch07-deep-ground.png")

# 3. texture density: noisy back wall vs quiet
lay2 = """
........
........
########
"""
quiet, _, _ = rooms.build(lay2, "greenhouse")
noisy = quiet.copy()
px = noisy.load()
rnd = random.Random(2)
for _ in range(260):
    x, y = rnd.randrange(128), rnd.randrange(32)
    px[x, y] = nes(rnd.choice([0x0C, 0x1C, 0x1C]))
save(compare(nv(noisy, 4), nv(quiet, 4), "Avoid: texture everywhere", "Better: calm wall, detail at edges",
             title="Texture density: the background must stay quiet"), "ch07-density.png")

# 4. animated water + molten tiles
sub_w = AREAS["cistern"]["bg"][1]
water = []
for f in range(4):
    gr = gblank(64, 32, "0")
    for i in range(4):
        gr = gpaste(gr, T.water(f), i * 16, 0)
        gr = gpaste(gr, T.water(f, surface=False), i * 16, 16)
    water.append(render(gr, sub_w, True))
gif("ch07-water.gif", [im for im in water], [200] * 4, k=4)
save(panel([(nv(im, 4), "frame %d" % (i + 1)) for i, im in enumerate(water)], gap=10,
           title="Water: the crest shifts 4 px per frame; the dithered body stays still",
           note="Only the surface row animates - four 16 x 16 tiles swapped every 200 ms."),
     "ch07-water.png")

# 5. gradient: banding vs dithered transitions with NES blues
cols = [0x0F, 0x02, 0x12, 0x22]


def grad(dither):
    h = 64
    im = Image.new("RGBA", (64, h))
    px = im.load()
    for y in range(h):
        for x in range(64):
            band = y * 4 / h
            i = int(band)
            if dither and band - i > 0.75 and i < 3 and (x + y) % 2 == 0:
                i += 1
            px[x, y] = nes(cols[min(i, 3)])
    return im


save(compare(nv(grad(False), 4), nv(grad(True), 4), "Hard bands", "Checker seam between bands",
             title="Skies: four colours, soft seams",
             note="A row or two of checker where two bands meet is enough. Here: $0F $02 $12 $22."),
     "ch07-gradient.png")

# 6. wall panel anatomy: 2x2 metatiles (four parts) of one panel
wp = gblank(32, 32, "0")
for p in range(4):
    wp = gpaste(wp, T.back_wall(part=p), (p % 2) * 16, (p // 2) * 16)
save(panel([(sv(render(wp, SUB, True), 10, major=16), "one wall panel = 4 metatiles (parts 0-3)"),
            (nv(world.background("greenhouse", with_hud=False)[0].crop((16, 32, 112, 112)), 4), "tiled behind a room")],
           title="Back wall: low contrast, two colours, a repeating 32 x 32 panel",
           note="Only $0F and $0C (slot 1, shared by every sub-palette) - the wall can sit under any attribute."),
     "ch07-wall-panel.png")

# 7. dither on a sprite: Kit's shadow side as a checker vs a flat cluster
base = kit.kit()
dith = []
for y, r in enumerate(base):
    out = []
    for x, c in enumerate(r):
        # back half of hood and body (x < 11, below the highlight) -> checker of suit/black
        if c == "2" and x < 11 and y > 5 and (x + y) % 2 == 0:
            out.append("1")
        else:
            out.append(c)
    dith.append("".join(out))
bad, good = kit.img(dith), kit.img(base)


def sprite_pair(im):
    return row([sv(im, 6, grid=False, major=None), view(im, 1, bg=SPR_BG), view(im, 2, bg=SPR_BG)], 10,
               align="bottom")


save(compare(sprite_pair(bad), sprite_pair(good), "Avoid: checker 'shading' on a sprite",
             "Better: flat clusters (3 colours, no dither)",
             title="Dither does not belong on small moving sprites",
             note="Shown at 6x, 1x and 2x. At 1x the checker turns the suit muddy; when Kit moves "
                  "1 px, the pattern crawls."), "ch07-sprite-dither.png")
