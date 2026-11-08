"""Ch. 26 figures: hi-bit / modern detail - the v1 `mossy-ruins` pack (ENDESGA 32, 16 px
tiles, 32 px hero 'Wren', 320x180) set against the NES project."""
import sys

from _v import *

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "art"))
import hero  # noqa: E402
import props as AP  # noqa: E402
import scene  # noqa: E402
import slime  # noqa: E402
from pix import RAMPS, swatches  # noqa: E402

SUB3 = GH["bg"][3]


def ncol(img):
    return len({c[1][:3] for c in img.getcolors(1 << 20) if c[1][3]})


kit0 = kitimg()
wren = hero.stand()
blob = slime.idle().frames[0]
hop = creatures.frames("hopper", "idle", GH["spr"][1])[0][0]
cast_n = Image.new("RGBA", (48, 32))
cast_n.alpha_composite(kit0, (0, 8))
cast_n.alpha_composite(hop, (28, 16))
cast_h = Image.new("RGBA", (64, 32))
cast_h.alpha_composite(wren, (0, 0))
cast_h.alpha_composite(blob, (36, 8))
save(panel([(view(cast_n, 6, bg=SPR_BG), "NES: Kit %d colours, hopper %d" % (ncol(kit0), ncol(hop))),
            (view(cast_h, 6, bg=SPR_BG), "hi-bit: Wren %d colours, slime %d" % (ncol(wren), ncol(blob)))],
           title="The same job with more pixels and colours",
           note="Kit: 16 x 24, one 3-colour sprite palette. Wren (the v1 hero): 32 x 32 frame, "
                "free choice from a 32-colour palette, selective outline, hue-shifted ramps."),
     "ch26-heroes.png")

nes_scene = world.scene("greenhouse", 0)[0]
hb_scene = scene.frame_at(0, 0)
save(panel([(nv(nes_scene, 2), "NES: 256 x 240, %d colours on screen" % ncol(nes_scene)),
            (view(hb_scene, 2, bg=FIG_BG), "hi-bit: 320 x 180, %d colours on screen" % ncol(hb_scene))],
           title="Screens side by side",
           note="Hi-bit keeps the pixel grid and a limited palette but drops the hardware rules: "
                "16:9 framing, more colours per tile, soft parallax layers, no attribute grid."),
     "ch26-scenes.png")

kr, kd = kit.frames("run")
wr = hero.run()


def draw(t):
    a = view(anim_frames((kr, kd), t), 5, bg=SPR_BG)
    b = view(anim_frames((wr.frames, wr.durations), t), 5, bg=SPR_BG)
    return row([label(a, "Kit run: %d frames" % len(kr), 14, FIG_FG),
                label(b, "Wren run: %d frames" % len(wr.frames), 14, FIG_FG)], 16)


fr_, d_ = timeline(1440, 30, draw)
gif("ch26-run.gif", fr_, d_, k=1, bg=FIG_BG)

crate_n = render(P.PROPS["crate"][0], SUB3)
crate_h = AP.staged("crate")
save(panel([(view(crate_n, 10, bg=SPR_BG), "NES crate: 16 x 16, %d colours (BG3)" % ncol(crate_n)),
            (view(crate_h, 10, bg=SPR_BG), "hi-bit crate: %d x %d, %d colours" % (crate_h.width, crate_h.height,
                                                                                ncol(crate_h)))],
           title="One prop, two budgets",
           note="With one sub-palette (black + 3) the planks read from black gaps and one highlight. With "
                "a ramp of browns, each plank can carry light, grain and wear."), "ch26-crates.png")

nes_ramps = [("stone", GH["bg"][0]), ("plants", GH["bg"][1]), ("metal", GH["bg"][2]), ("warm", GH["bg"][3])]
rows_ = []
for (nm, sub), (hn, codes) in zip(nes_ramps, list(RAMPS.items())[:4]):
    a = swatches([nes(i)[:3] for i in sub], 26)
    b = swatches(codes, 26)
    rows_.append(row([label(a, "NES %s" % nm, 13, FIG_FG), label(b, "ENDESGA 32 %s" % hn, 13, FIG_FG)], 40))
save(figure(column(rows_, 10, center=False), "Ramps: 4 fixed entries vs free hue-shifted runs",
            "NES ramps are rows of the master palette (shared black included). Hi-bit ramps "
            "shift hue as they brighten (cool shadows, warm lights) and can be 5-7 steps long."),
     "ch26-ramps.png")

def black_edge(img):
    """Recolour every opaque pixel that touches transparency (the outline ring) to ink."""
    out = img.copy()
    src = img.load()
    for y in range(img.height):
        for x in range(img.width):
            if src[x, y][3] and any(not (0 <= x + dx < img.width and 0 <= y + dy < img.height)
                                    or not src[x + dx, y + dy][3]
                                    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                put(out, x, y, "K")
    return out


save(panel([(view(hero.frame(stage="flat"), 8, bg=SPR_BG), "1. flat colours, black outline"),
            (view(black_edge(hero.stand()), 8, bg=SPR_BG), "2. shaded, black outline"),
            (view(hero.stand(), 8, bg=SPR_BG), "3. shaded, selective outline")],
           title="Outline choices open up",
           note="NES sprites lean on black outlines because black is free in every palette. "
                "With more colours, the lit top and left edges can take a dark shade of the "
                "material they border; the shadow side keeps the ink."),
     "ch26-selout.png")

# Anti-aliasing (taught in v1 ch06): a curve without and with in-between pixels.
aa_off = blank(20, 12, "1")
aa_on = blank(20, 12, "1")
for img_ in (aa_off, aa_on):
    steps_line(img_, 0, 2, [6, 4, 3, 2, 1, 1], "K")
for x, y in ((6, 2), (10, 3), (13, 4)):
    put(aa_on, x, y, "3")
for x, y in ((4, 3), (8, 4), (11, 5), (14, 6)):
    put(aa_on, x, y, "2")
save(compare(view(aa_off, 12, bg=LIGHT_BG, grid=True), view(aa_on, 12, bg=LIGHT_BG, grid=True),
             "No AA: hard steps", "AA: in-between greys at the step ends",
             title="Anti-aliasing: in-between colours where the steps meet",
             note="Runs 6-4-3-2-1-1. Grey 3 extends each long run; grey 2 tucks under it. "
                  "The single-pixel steps at the end get no AA."), "ch26-aa.png")

# Outer-edge AA bakes in one background colour.
rock = AP.staged("rock", "shaded")


def edge_aa(img, c):
    out = img.copy()
    src = img.load()
    for y in range(1, img.height - 1):
        for x in range(1, img.width - 1):
            if not src[x, y][3] and sum(1 for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))
                                        if src[x + dx, y + dy][3]) >= 2:
                put(out, x, y, c)
    return out


rock_aa = edge_aa(rock, "3")
save(panel([(view(rock, 8, bg=LIGHT_BG), "hard edge, light bg"),
            (view(rock_aa, 8, bg=LIGHT_BG), "outer AA, light bg", FIG_GOOD),
            (view(rock, 8, bg="j"), "hard edge, dark bg"),
            (view(rock_aa, 8, bg="j"), "same AA, dark bg: halo", FIG_BAD)],
           title="Outer-edge AA only works on the background it was made for",
           note="The grey corner pixels blend into a light background; on a dark one they "
                "become a bright fringe. Keep a moving sprite's outer edge hard."),
     "ch26-edge-aa.png")

pan = scene.preview_frames(40, 160)
gif("ch26-parallax.gif", pan, [80] * len(pan), k=2, bg=FIG_BG)
