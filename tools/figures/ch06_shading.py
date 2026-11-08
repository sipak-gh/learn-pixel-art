"""Ch. 6 figures: shading with 3 colours - directional vs pillow, clusters, black."""
import random
from _v import *

SUB = GH["bg"][0]


BOULDERS = {
    "flat": g("""
.....000000.....
...0022222200...
..022222222220..
.02222222222220.
.02222222222220.
0222222222222220
0222222222222220
0222222222222220
0222222222222220
0222222222222220
.02222222222220.
.02222222222220.
..002222222200..
....00000000....
"""),
    "pillow": g("""
.....000000.....
...0011111100...
..011111111110..
.01122222222110.
.01222222222210.
0112223333222110
0122233333322210
0122233333322210
0112223333222110
0112222222222110
.01122222222110.
.01111111111110.
..001111111100..
....00000000....
"""),
    "light": g("""
.....000000.....
...0033333200...
..033333322220..
.03333332222220.
.03333222222210.
0333322222222110
0233222222221110
0222222222211110
0222222222111110
0122222221111110
.01222211111110.
.01111111111110.
..001111111100..
....00000000....
"""),
}


def boulder(mode):
    return BOULDERS[mode]


bl = lambda m: sv(render(boulder(m), SUB), 8, grid=False, major=None)
save(panel([(bl("flat"), "flat"), (bl("pillow"), "Avoid: pillow (dark ring, bright centre)", FIG_BAD),
            (bl("light"), "Better: lit from top-left", FIG_GOOD)],
           title="Shading = deciding where the light comes from",
           note="Pillow shading follows the outline, not the light. Pick a light and shade the planes."),
     "ch06-pillow.png")

# 2. clusters vs noise
gt = T.ground(T.E | T.W | T.S, 0)
rnd = random.Random(4)
noisy = [list(r) for r in gt]
for _ in range(40):
    x, y = rnd.randrange(16), rnd.randrange(4, 16)
    noisy[y][x] = rnd.choice("123")
noisy = ["".join(r) for r in noisy]
three = lambda gr: render(gpaste(gpaste(gblank(48, 16, "0"), gr, 0, 0), gr, 16, 0) and
                          gpaste(gpaste(gpaste(gblank(48, 16, "0"), gr, 0, 0), gr, 16, 0), gr, 32, 0),
                          SUB, True)
save(compare(nv(three(noisy), 5), nv(three(gt), 5), "Avoid: scattered single pixels (noise)",
             "Better: pixels grouped into clusters", title="Clusters: every pixel should belong to a shape"),
     "ch06-clusters.png")

# 3. Kit shading steps (3 colours = outline, mid, light)
g0 = kit.kit()
flat = [r.replace("1", "2").replace("3", "2") for r in g0]
lines = [r.replace("3", "2") for r in g0]
save(panel([(sv(kit.img(flat), 6), "1. one colour ($16)"), (sv(kit.img(lines), 6), "2. + black ($0F)"),
            (sv(kit.img(g0), 6), "3. + cream ($37)")],
           title="Kit is built from three colours, added in order",
           note="Black outlines and features first; then the lightest colour only where it matters "
                "(hood rim, face, lantern)."), "ch06-kit-steps.png")

# 4. use of black: outlined sprites vs outline-less tiles
scene = world.scene("greenhouse", 0)[0].crop((16, 144, 144, 208))
nokit = world.background("greenhouse", with_hud=False)[0].crop((16, 144, 144, 208)).copy()
k_no = kit.img([r.replace("1", "2") for r in kit.kit()])
nokit.alpha_composite(k_no, (100 - 16, 168 - 144 + 0)) if False else None
act = [x for x in world.ROOMS["greenhouse"]["actors"] if x[0] == "kit"][0]
kx, ky = act[2] - 16, act[3] - 144
nokit.alpha_composite(k_no, (kx, ky))
withk = world.background("greenhouse", with_hud=False)[0].crop((16, 144, 144, 208)).copy()
withk.alpha_composite(kitimg(), (kx, ky))
save(compare(nv(nokit, 4), nv(withk, 4), "Without outline: the hood merges with dark areas",
             "With black outline: a clean silhouette on any tile",
             title="Use of black: sprites outlined, background tiles mostly not"), "ch06-black.png")

# 5. ground tile anatomy
gt = T.ground(T.E | T.W | T.S, 1)
big = sv(render(gt, SUB, True), 14, major=8)
cap = column([sub_chips(SUB, 30),
              label(Image.new("RGBA", (1, 1)), "", 1),
              ], 4)
notes = ["$2B  moss rim: 1 px light line + drips", "$1C  brick faces", "$0C  mortar + shadow side",
         "$0F  gaps / deep ground"]
txt = Image.new("RGBA", (300, 120), FIG_BG + (255,))
for i, n in enumerate(notes):
    draw_text(txt, 0, i * 26, n, 15, FIG_FG)
save(figure(row([big, column([sub_chips(SUB, 30), txt], 12, center=False)], 24),
            "Anatomy of a ground metatile (16 x 16, BG0)",
            "Light from above: brightest on the walkable top, darkest at the bottom. Four colours, "
            "one sub-palette."), "ch06-ground-anatomy.png")

# 6. props sheet in their sub-palettes
items = []
for name, (grid, subs) in P.PROPS.items():
    wcells = len(grid[0]) // 16
    im = Image.new("RGBA", (len(grid[0]), len(grid)), (0, 0, 0, 0))
    for j in range(len(grid) // 16):
        for i in range(wcells):
            cell = [r[i * 16:i * 16 + 16] for r in grid[j * 16:j * 16 + 16]]
            im.alpha_composite(render(cell, GH["bg"][subs[j * wcells + i]], backdrop=True), (i * 16, j * 16))
    items.append((nv(im, 4), "%s (BG%s)" % (name, "/".join(str(s) for s in sorted(set(subs))))))
save(panel(items, title="Props: each 16 x 16 cell uses one background sub-palette", gap=16),
     "ch06-props.png")
