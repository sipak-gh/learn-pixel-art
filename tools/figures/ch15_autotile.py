"""Ch. 15 figures: tilesets, autotiling, seams, variants, overlays."""
from _v import *

SUB = GH["bg"][0]
items = []
for m in range(16):
    im = render(T.ground(m, 3), SUB, True)
    nb = "".join(c for c, b in zip("NESW", (T.N, T.E, T.S, T.W)) if m & b) or "-"
    items.append(label(nv(im, 4), "%d %s" % (m, nb), 12, FIG_DIM))
save(figure(grid_layout(items, 8, gap=10), "The ground set: 16 metatiles, one per neighbour mask",
            "mask = N(1) + E(2) + S(4) + W(8): which neighbours are also ground. 15 = fully inside (dark interior)."),
     "ch15-ground-set.png")

lay = """
..........
.###...##.
.#####.##.
...###....
.......###
##########
"""
img, attrs, grids = rooms.build(lay, "greenhouse", 3)
L = [r for r in lay.strip("\n").split("\n")]
big = nv(img, 4)
for y, r in enumerate(L):
    for x, c in enumerate(r):
        if c == "#":
            sol = lambda xx, yy: not (0 <= xx < len(r)) or yy >= len(L) or (0 <= yy and L[yy][xx] == "#")
            m = (T.N if sol(x, y - 1) else 0) | (T.E if sol(x + 1, y) else 0) | (T.S if sol(x, y + 1) else 0) | (T.W if sol(x - 1, y) else 0)
            draw_text(big, x * 64 + 22, y * 64 + 24, str(m), 16, (255, 255, 0))
save(figure(big, "Autotiling: paint 'ground', the tool picks the metatile",
            "Numbers are the neighbour masks. Edges outside the map count as solid."), "ch15-autotile.png")

save(panel([(seam_preview(render(T.back_wall(part=0), SUB, True), 3, 4), "one wall metatile repeated"),
            (seam_preview(render(gpaste(gpaste(gpaste(gpaste(gblank(32, 32, "0"), T.back_wall(part=0), 0, 0),
                                                     T.back_wall(part=1), 16, 0), T.back_wall(part=2), 0, 16),
                                       T.back_wall(part=3), 16, 16), SUB, True), 3, 3), "the 2 x 2 panel repeated")],
           title="Seams: repeat a tile 3 x 3 before you trust it"), "ch15-seams.png")

save(panel([(nv(render(T.ground(T.E | T.W | T.S, s), SUB, True), 6), "variant %d" % s) for s in range(4)],
           title="Variants: four brick layouts for the same mask",
           note="Chosen by position ((x*7 + y*13) mod 4), so the floor never repeats in an obvious rhythm."),
     "ch15-variants.png")

base = T.back_wall(part=0)
ov = [("wall", base, 0), ("+ vine", gpaste(base, T.vine(2), 0, 0), 1), ("+ grass tuft", gpaste(base, T.grass_tuft(1), 0, 0), 1),
      ("+ pipe", gpaste(base, T.PIPE_H, 0, 0), 2), ("+ ladder", gpaste(base, T.LADDER, 0, 0), 2)]
save(panel([(nv(render(gr, GH["bg"][s], True), 6), "%s (BG%d)" % (n, s)) for n, gr, s in ov],
           title="Overlays: details drawn over the wall in a new metatile",
           note="Because every sub-palette shares $0F and $0C, the wall underneath looks the same."),
     "ch15-overlays.png")
