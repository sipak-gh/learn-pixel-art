"""Ch. 27 figures: isometric pixel art (2:1 lines, diamonds, blocks, draw order)."""
from _v import *
from styles import iso as I

LINE_C = nes(0x2B)[:3]


def line_img(pts, w=None, h=None):
    w = w or max(x for x, _ in pts) + 1
    h = h or max(y for _, y in pts) + 1
    im = Image.new("RGBA", (w, h), NESBLACK + (255,))
    for x, y in pts:
        im.putpixel((x, y), LINE_C + (255,))
    return im


LW = max(x for x, _ in I.line_irregular(10)) + 1
clean = line_img(I.line_21(10), w=LW)
rough = line_img(I.line_irregular(10), w=LW)
one = line_img([(i, i) for i in range(10)], w=20)
save(panel([(view(clean, 12, grid=True, bg=FIG_BG), "2:1, runs of exactly 2"),
            (view(rough, 12, grid=True, bg=FIG_BG), "'about 2:1', uneven runs"),
            (view(one, 12, grid=True, bg=FIG_BG), "1:1 (45 degrees)")],
           title="The isometric line",
           note="Pixel isometric uses 2 across for 1 down (about 26.6 degrees, not the true 30). "
                "Equal runs make a smooth edge; uneven runs wobble."), "ch27-lines.png")

ft = I.floor_tile()
rws = I.diamond_rows()
tiled = Image.new("RGBA", (32 * 3, 16 * 3 + 8), NESBLACK + (255,))
for j in range(4):
    for i in range(4):
        x, y = 32 + (i - j) * 16, (i + j) * 8 - 8
        if -16 < y < tiled.height:
            tiled.alpha_composite(ft, (x, y))
save(panel([(view(ft, 12, grid=True, bg=FIG_BG), "one floor tile: 32 x 16"),
            (nv(tiled, 6), "tiles meet edge to edge")],
           title="The floor diamond",
           note="Rows grow by 4 px (2 each side) until the middle, then shrink. Grout lines follow "
                "the two 2:1 axes, so the pattern lines up across tiles."), "ch27-diamond.png")

blk = I.block("stone")
save(panel([(view(I.block(m), 8, bg=SPR_BG), m) for m in ("stone", "metal", "moss")] +
           [(view(I.crate(), 8, bg=SPR_BG), "crate")],
           title="Blocks: one light, three faces",
           note="Light from the upper left: top face lightest, left face mid, right face darkest. "
                "A 1 px highlight runs along the edges that face the light; outline the silhouette only."),
     "ch27-blocks.png")

# Exercise 3: moving the light to the upper right mirrors which side face is mid and which is dark.
ul = I.block("stone")
ur = ul.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
save(panel([(view(ul, 8, bg=SPR_BG), "light from the upper left"),
            (view(ur, 8, bg=SPR_BG), "light from the upper right")],
           title="Move the light, swap the side faces",
           note="The top stays lightest. With the light on the right, the right face takes the mid "
                "colour and the left face the dark one."), "ch27-light.png")

kit0 = kitimg()
full = I.room(kit0)
save(figure(nv(full, 3), "The Greenhouse corner, isometric",
            "Same NES colours and the same Kit sprite; walls, floor and crates rebuilt as 2:1 blocks."),
     "ch27-room.png")

items = I.room_items((2.0, 4.0))
kinds = [it[1] for it in items]
last_wall = max(n for n, k_ in enumerate(kinds) if k_ in ("stone", "moss")) + 1
kit_n = kinds.index("kit") + 1
stages = [(kinds.count("floor"), "1. floor"), (last_wall, "2. walls + planter (depth < 5)"),
          (kit_n, "3. Kit (depth 6)"), (len(items), "4. crates (depth 7-8)")]
save(panel([(nv(I.room(kit0, upto=n), 2), t) for n, t in stages],
           title="Painter's algorithm: draw back to front",
           note="Sort by depth (i + j, then height) and draw in that order; nearer things simply "
                "cover farther ones. Kit is inserted into the list like any block."),
     "ch27-order.png")

side = world.scene("greenhouse", 0)[0].crop((0, 128, 256, 240))
save(panel([(nv(side, 2), "side view: one face per object"),
            (nv(full.crop((0, 24, 256, 160)), 2), "isometric: three faces, more pixels per object")],
           title="Side view vs isometric",
           note="Isometric shows depth and lets the player move in two directions, but every "
                "object costs three faces and every sprite needs diagonal facings."),
     "ch27-side-vs-iso.png")

# Kit walking along the i axis (down-right on screen): 2 px across per 1 px down
wf, wd = kit.frames("walk")


def draw(t):
    u = (t % 3200) / 3200
    ii = 0.3 + 4.4 * (u * 2 if u < 0.5 else 2 - u * 2)  # ping-pong
    im_ = wf[(t // wd[0]) % len(wf)]
    if u >= 0.5:
        im_ = im_.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
    return I.room(im_, kit_cell=(ii, 5.0)).crop((0, 24, 256, 176))


fr_, d_ = timeline(3200, 80, draw)
gif("ch27-walk.gif", fr_, d_, k=3)
