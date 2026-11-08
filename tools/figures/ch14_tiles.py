"""Ch. 14 figures: tiles, metatiles, attributes, CHR budget."""
from _v import *

img, attrs, grids = room_grids("greenhouse")
save(figure(tile_grid_view(img.crop((0, 32, 128, 128)), 4),
            "Tiles (8 x 8, thin lines) inside metatiles (16 x 16, strong lines)",
            "You draw and place 16 x 16 metatiles; the hardware stores 8 x 8 tiles."), "ch14-grid.png")

# metatile anatomy: ground top = 4 tiles
gt = T.ground(T.E | T.W | T.S, 2)
parts = [render([r[x:x + 8] for r in gt[y:y + 8]], GH["bg"][0], True) for y in (0, 8) for x in (0, 8)]
save(panel([(sv(render(gt, GH["bg"][0], True), 10, major=8), "metatile 16 x 16"),
            (grid_layout([sv(p, 10, major=None) for p in parts], 2, gap=8), "= 4 CHR tiles + 1 attribute")],
           title="A metatile is 4 tiles that share one sub-palette"), "ch14-metatile.png")

# attribute map overlay
save(figure(attr_view(img, attrs, 2),
            "Attribute map: each 16 x 16 area picks BG0-BG3",
            "Red BG0 stone · green BG1 plants · blue BG2 metal · yellow BG3 warm props + HUD. "
            "Real NES attribute bytes cover 32 x 32 (four 16 x 16 quadrants) - same grid."),
     "ch14-attributes.png")

# attribute clash: a lamp (BG3) and a fern (BG1) in the same 16x16 cell
fern = P.PROPS["fern"][0]
lamp = P.PROPS["lamp"][0]
wall = T.back_wall(part=0)
both = gpaste(gpaste(wall, [r[0:8] for r in fern], 0, 0), [r[8:16] for r in lamp], 8, 0)
bad = render(both, GH["bg"][1], True)
good = row([render(gpaste(wall, fern, 0, 0), GH["bg"][1], True),
            render(gpaste(T.back_wall(part=1), lamp, 0, 0), GH["bg"][3], True)], 0, bg=(0, 0, 0))
save(compare(nv(bad, 8), nv(good, 8), "Avoid: half lamp + half fern in one area (lamp turns green)",
             "Better: one prop per 16 x 16 area",
             title="Attribute clash: one sub-palette per 16 x 16"), "ch14-clash.png")

# CHR sheet
tl = chr_tiles(grids)
tlf = chr_tiles(grids, flips=True)
save(figure(chr_view(tl, k=3), "Greenhouse screen: %d unique tiles out of 256" % len(tl),
            "Shown the way the NES stores them - 4 greys, no colour. Background tiles cannot be flipped "
            "(only sprites can), so a mirrored tile costs a slot: flips would save just %d here." % (len(tl) - len(tlf))),
     "ch14-chr.png")

# tile reuse heat map: how often each metatile appears
from collections import Counter
keys = [["\n".join(gr) for gr in rw] for rw in grids]
cnt = Counter(k for rw in keys for k in rw)
heat = img.copy()
ov = Image.new("RGBA", img.size, (0, 0, 0, 0))
d = ImageDraw.Draw(ov)
for y, rw in enumerate(keys):
    for x, k_ in enumerate(rw):
        n = cnt[k_]
        c = (255, 80, 80, 140) if n == 1 else ((250, 200, 60, 110) if n < 4 else (80, 200, 120, 90))
        d.rectangle([x * 16, y * 16, x * 16 + 15, y * 16 + 15], fill=c)
heat.alpha_composite(ov)
save(figure(nv(heat, 2), "Metatile reuse: %d different metatiles on 240 cells" % len(cnt),
            "Green: used 4+ times · yellow: 2-3 · red: once (props, HUD text). One-offs are where the budget goes."),
     "ch14-reuse.png")
