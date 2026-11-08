"""Ch. 1 figures: pixels, integer scaling, the NES screen."""
from _v import *

k0 = kitimg()
# 1. Kit at 1x .. 8x (integer nearest-neighbour)
save(panel([(nv(k0, n), f"{n}x") for n in (1, 2, 4, 8)],
           title="Kit (16 x 24 px) at integer zoom levels",
           note="Nearest-neighbour scaling: every art pixel becomes an n x n block."),
     "ch01-kit-zoom.png")

# 2. scaling: smooth vs non-integer vs integer
on_black = Image.new("RGBA", k0.size, (0, 0, 0, 255)); on_black.alpha_composite(k0)
smooth = on_black.resize((k0.width * 5, k0.height * 5), Image.Resampling.BILINEAR)
frac = on_black.resize((int(k0.width * 4.5), int(k0.height * 4.5)), Image.Resampling.NEAREST)
save(panel([(smooth, "Avoid: smooth (bilinear) scaling", FIG_BAD),
            (frac, "Avoid: 4.5x nearest (uneven pixels)", FIG_BAD),
            (nv(k0, 5), "Better: 5x nearest", FIG_GOOD)],
           title="Scaling pixel art for display"), "ch01-scaling.png")

# 3. NES screen anatomy over the finished Greenhouse
img, objs = world.scene("greenhouse", 0)
big = tile_grid_view(img, 3)
d = ImageDraw.Draw(big)
d.rectangle([0, 0, big.width - 1, 8 * 3 - 1], outline=(255, 90, 90), width=2)
d.rectangle([0, big.height - 8 * 3, big.width - 1, big.height - 1], outline=(255, 90, 90), width=2)
save(figure(big, "The NES screen: 256 x 240 = 32 x 30 tiles = 16 x 15 metatiles",
            "Thin lines: 8 x 8 tiles. Strong lines: 16 x 16 metatiles (= attribute areas). "
            "Red bands: the top and bottom 8 px many TVs hid (keep important art out)."),
     "ch01-nes-screen.png")

# 4. 8:7 pixel aspect ratio
st = on_black.resize((k0.width * 8 * 8 // 7, k0.height * 8), Image.Resampling.NEAREST)
save(panel([(nv(k0, 8), "square pixels (this course)"), (st, "8:7 (NES on a CRT TV)")],
           title="Pixel aspect ratio",
           note="NES pixels were slightly wider than tall (8:7). We draw and show square pixels."),
     "ch01-aspect.png")

# 5. canvas sizes to scale
items = []
for w, h, name in ((8, 8, "8 x 8 tile"), (16, 16, "16 x 16 metatile"), (16, 24, "Kit 16 x 24"),
                   (256, 240, "screen 256 x 240")):
    c = Image.new("RGBA", (w, h), nes(0x1C) if w < 200 else nes(0x0C))
    items.append((view(c, 2, bg=BLACK), name))
items[2] = (nv(k0, 2), "Kit 16 x 24")
items[3] = (nv(world.scene("greenhouse", 0)[0], 2), "screen 256 x 240")
save(panel(items, title="Canvas sizes used in this course (all at 2x)", gap=16), "ch01-canvases.png")

# 6. the destination: animated finished Greenhouse
frames = [world.scene("greenhouse", t)[0] for t in range(0, 2400, 100)]
gif("ch01-greenhouse.gif", frames, 100, k=2)
