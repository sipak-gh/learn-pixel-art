"""Ch. 19 figures: mood, palettes, fades, particles."""
from _v import *

save(panel([(nv(world.scene(a, 0)[0], 2), AREAS[a]["name"]) for a in ORDER], cols=2, gap=16,
           title="Four moods from palette, light sources and particles"), "ch19-moods.png")

lay = world.ROOMS["greenhouse"]["layout"]
items = []
for a in ORDER:
    im, _, _ = rooms.build(lay, a, props=world.ROOMS["greenhouse"]["props"])
    items.append((nv(im.crop((0, 32, 256, 240)), 1), AREAS[a]["name"] + " palettes"))
save(panel(items, gap=12, title="Same tiles, four palette sets",
           note="Most of an area's identity is its palette. New tiles are only needed for signature features "
                "(water, molten slag, grates, stars)."), "ch19-same-layout.png")


def fade_sub(sub, steps):
    out = []
    for c in sub:
        if c == 0x0F:
            out.append(c)
            continue
        v = c - 0x10 * steps
        out.append(v if v >= 0 else 0x0F)
    return tuple(out)


RGB2IDX = {}
for i in USABLE:
    RGB2IDX.setdefault(nes(i)[:3], i)


def faded(area, steps):
    """The whole screen (BG + sprites) with every colour moved `steps` rows darker."""
    im = world.scene(area, 0)[0]
    cmap = {}
    for rgb, i in RGB2IDX.items():
        cmap[rgb] = nes(fade_sub((i,), steps)[0])[:3]
    return remap(im, cmap)


fades = [faded("greenhouse", s) for s in range(5)]
gif("ch19-fade.gif", fades + fades[::-1][1:-1], [160, 120, 120, 120, 400, 120, 120, 120], k=2)
save(panel([(nv(f, 1), "-$%02X" % (s * 0x10) if s else "full") for s, f in enumerate(fades)], gap=10,
           title="The NES fade: subtract $10 per step until black",
           note="Each step moves every colour one brightness row down; below row 0 it becomes $0F. "
                "Four steps, no new colours."), "ch19-fade.png")

for a, box in (("furnace", (0, 32, 256, 240)), ("ridge", (0, 32, 256, 240))):
    fr_, d_ = timeline(2400, 100, lambda t, a=a: world.scene(a, t, with_hud=False)[0].crop(box))
    gif("ch19-particles-%s.gif" % a, fr_, d_, k=2)

# light sources collage
crops = [("greenhouse", (176, 64, 224, 112), "lamp (BG3)"), ("furnace", (48, 160, 144, 224), "molten slag (BG3)"),
         ("ridge", (168, 40, 232, 96), "moon (BG1)"), ("cistern", (192, 48, 240, 96), "lamp (BG3)")]
save(panel([(nv(world.background(a, with_hud=False)[0].crop(b), 4), t) for a, b, t in crops], gap=12,
           title="Light sources: the brightest, warmest pixels on screen"), "ch19-lights.png")
