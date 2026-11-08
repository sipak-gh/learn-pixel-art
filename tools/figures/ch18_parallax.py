"""Ch. 18 figures: backgrounds, bands, parallax, scroll splits."""
from _v import *

R = AREAS["ridge"]["bg"]
bands = BGM.band_images(R)
items = [(nv(bands["sky"], 2), "sky band (BG1): 6 star tiles reused + moon"),
         (nv(bands["hills"], 2), "far hills (BG2)"), (nv(bands["towers"], 2), "towers (BG1)")]
save(panel(items, cols=1, gap=10, title="Antenna Ridge: three horizontal bands, each 256 px wide and tileable",
           note="Each band uses one sub-palette and is darker / less contrasted the further away it is."),
     "ch18-bands.png")

# ground strip, 512 wide (two rows of ground)
fg, _, _ = rooms.build(["#" * 32, "#" * 32], "ridge")
H = 208
speeds = [("sky", 0.125, 0), ("hills", 0.25, 64), ("towers", 0.5, 112)]
rf, rd = kit.frames("run")


def frame(t):
    cam = t * 0.06
    im = Image.new("RGBA", (256, H), nes(0x0F))
    for name, sp, y in speeds:
        b = bands[name]
        off = int(cam * sp) % 256
        im.alpha_composite(b, (-off, y))
        im.alpha_composite(b, (256 - off, y))
    off = int(cam) % 512
    im.alpha_composite(fg, (-off, 176))
    im.alpha_composite(fg, (512 - off, 176))
    im.alpha_composite(anim_frames((rf, rd), t), (100, 152))
    return im


fr_, d_ = timeline(4320, 40, frame)
gif("ch18-parallax.gif", fr_, d_, k=2)

# scroll-split diagram: a scrolling Ridge level planned as horizontal strips (the parallax
# composition above with the HUD on top), so no two strips share a scanline
hud_strip = world.scene("ridge", 0)[0].crop((0, 0, 256, 32))
s0 = Image.new("RGBA", (256, 240), nes(0x0F))
s0.alpha_composite(hud_strip, (0, 0))
s0.alpha_composite(frame(1200), (0, 32))
diag = nv(s0, 2)
d = ImageDraw.Draw(diag)
splits = [(0, "HUD: scroll 0 (fixed)"), (32, "sky: 1/8 speed"), (96, "hills: 1/4"), (144, "towers: 1/2"),
          (208, "play field: full speed")]
for y, txt in splits:
    d.line([(0, y * 2), (diag.width, y * 2)], fill=(255, 220, 60), width=2)
    draw_text(diag, 6, y * 2 + 4, txt, 14, (255, 230, 120))
save(figure(diag, "Scroll splits: the screen is cut into horizontal strips",
            "One scroll position per frame; games change it mid-frame (sprite-0 hit or a mapper IRQ). "
            "Strips can't overlap - plan bands as rows. Sprites (Kit) ignore the splits."),
     "ch18-scroll-splits.png")

# depth by value
save(panel([(nv(world.background("ridge", with_hud=False)[0].crop((0, 32, 256, 208)), 2), "colour"),
            (nv(value_study(world.background("ridge", with_hud=False)[0].crop((0, 32, 256, 208))), 2), "values")],
           title="Depth through value: far = dark and flat, near = bright and contrasted"),
     "ch18-depth.png")

sky = BGM.sky(h=64)
tiles = chr_tiles([[[r[x:x + 16] for r in sky[y:y + 16]] for x in range(0, 256, 16)] for y in range(0, 64, 16)])
rand_sky = [[T.stars(x * 7 + y * 131, density=3) for x in range(16)] for y in range(4)]
n_rand = len(chr_tiles(rand_sky))
save(figure(chr_view(tiles, k=4), "Sky band: %d unique tiles for 256 x 64 px" % len(tiles),
            "Six star metatiles are reused across the band; the moon adds the rest. A random star "
            "field with every metatile different would need %d tiles." % n_rand), "ch18-star-reuse.png")
