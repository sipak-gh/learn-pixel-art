"""Ch. 3 figures: silhouette, readability, shape language, metasprites."""
from _v import *


def sil(img, c=(255, 255, 255)):
    out = Image.new("RGBA", img.size)
    px, src = out.load(), img.load()
    for y in range(img.height):
        for x in range(img.width):
            if src[x, y][3]:
                px[x, y] = c + (255,)
    return out


# 1. silhouette candidates: which parts carry the read?
def clear(img, test):
    out = img.copy()
    px = out.load()
    for y in range(out.height):
        for x in range(out.width):
            if test(x, y):
                px[x, y] = (0, 0, 0, 0)
    return out


full = kitimg()
no_lantern = clear(full, lambda x, y: x >= 17 and y >= 15 or (x >= 16 and y >= 20))
no_tail = clear(no_lantern, lambda x, y: x <= 6 and y <= 9)
items = [(view(sil(im), 6, bg=(30, 30, 40)), n) for im, n in
         ((no_tail, "plain hood: a blob"), (no_lantern, "+ hood tail"), (full, "+ lantern (final)"))]
save(panel(items, title="Silhouette first: which shapes make Kit read?",
           note="Fill the sprite with one colour. The hood tail (back) and the lantern (front) make the pose readable."),
     "ch03-silhouettes.png")

# 2. key poses as silhouettes
poses = [kit.grids(a)[i] for a, i in (("idle", 0), ("walk", 0), ("run", 0), ("jump", 1),
                                       ("jump", 3), ("attack", 1), ("hurt", 0))]
names = ["idle", "walk", "run", "jump", "fall", "attack", "hurt"]
save(panel([(view(sil(kit.img(g_)), 5, bg=(30, 30, 40)), n) for g_, n in zip(poses, names)],
           title="Every key pose must read as a silhouette", gap=12), "ch03-pose-silhouettes.png")

# 3. readability at 1x: Kit + creatures on their background
bgimg, _ = world.background("greenhouse", with_hud=False)
crop = bgimg.crop((16, 144, 208, 208)).copy()
crop.alpha_composite(kitimg(), (20, 40))
crop.alpha_composite(creatures.frames("hopper", "idle", GH["spr"][1])[0][0], (70, 48))
crop.alpha_composite(creatures.frames("slug", "crawl", AREAS["greenhouse"]["spr"][1])[0][0], (110, 48))
crop.alpha_composite(creatures.frames("drone", "hover", GH["spr"][3])[0][0], (150, 20))
save(panel([(nv(crop, 1), "1x"), (nv(crop, 2), "2x"), (nv(crop, 4), "4x")],
           title="Judge readability at 1x, not zoomed in"), "ch03-readability.png")

# 4. hero vs background colours
gk = kit.img(kit.kit(), (0x0F, 0x0F, 0x1A, 0x2A))  # Kit recoloured in the plants' greens
bad = crop.copy(); good = crop.copy()
bad.alpha_composite(gk, (20, 40))
save(compare(nv(bad.crop((0, 16, 96, 64)), 4), nv(crop.crop((0, 16, 96, 64)), 4),
             "Avoid: hero in the background's hues", "Better: hero in a hue the room never uses",
             title="Figure-ground: the hero must not blend into the set"), "ch03-hero-vs-bg.png")

# 5. shape language
items = []
for kind, anim, sub, txt in (("hopper", "idle", 1, "hopper: round = soft, bouncy"),
                             ("slug", "crawl", 1, "slug: long + low = slow"),
                             ("drone", "hover", 3, "drone: hard geometry = machine")):
    im = creatures.frames(kind, anim, GH["spr"][sub])[0][0]
    items.append((row([view(sil(im), 5, bg=(30, 30, 40)), nv(im, 5)], 8), txt))
save(panel(items, title="Shape language: the silhouette tells you what a creature does"),
     "ch03-shape-language.png")

# 6. metasprite grid: Kit = 2 x 3 hardware sprites
cell = kitimg().crop((4, 0, 20, 24))
save(panel([(view(cell, 10, grid=True, bg=SPR_BG, major=8), "16 x 24 = 2 x 3 sprites of 8 x 8")],
           title="Kit as a metasprite",
           note="The NES draws sprites as 8 x 8 tiles. Kit's body box fills six of them; attack poses borrow a third column."),
     "ch03-metasprite.png")

# 7. building Kit's silhouette from big shapes (the parts in kit.py, added one group at a time)
from nes import ICanvas  # noqa: E402

steps = [("1. head", [(kit.HEAD, 0)]),
         ("2. + hood tail", [(kit.TIPS["back"], 0)]),
         ("3. + mantle, tunic", [(kit.MANTLE, 0), (kit.TUNIC, 0)]),
         ("4. + legs", [(kit.LEGS["stand"][0], 1), (kit.LEGS["stand"][1], 1)]),
         ("5. + arm, lantern", [(kit.ARMS["hang"][0], 0), ([kit.ARMS["hang"][1]], 2),
                                ({17: (13, 14), 18: (13, 14), 19: (13, 14)}, 0)])]
acc, items = [], []
for name, parts in steps:
    acc += parts
    c = ICanvas(kit.FW, kit.FH)
    for spans, kind in acc:
        if kind == 2:                                  # single pixels (x, y): the hand
            c.px(spans, "2", kit.OX, 0)
        else:
            c.spans(spans, "2", kit.OX, 0)
    c.outline("1")
    items.append((view(sil(kit.img(c.grid())), 6, grid=True, bg=(30, 30, 40), major=8), name))
save(panel(items, title="Building Kit's silhouette from big shapes (24 x 24 cell, 8 px grid)",
           gap=14,
           note="Each step adds one group of shapes; a 1 px outline ring is included. "
                "Step 5 is the final silhouette (project/ch03/concept/kit-silhouette.png)."),
     "ch03-kit-build.png")

# 8. proportions: head, body and legs in rows of the 24 px cell
k = 8
pv = view(full, k, grid=True, bg=SPR_BG, major=8)
bands = [(2, 12, "head: rows 2-11 = 10 px"), (12, 20, "body: rows 12-19 = 8 px"),
         (20, 24, "legs: rows 20-23 = 4 px")]
side = Image.new("RGBA", (pv.width + 230, pv.height), FIG_BG + (255,))
side.alpha_composite(pv, (0, 0))
d = ImageDraw.Draw(side)
for y0, y1, txt in bands:
    for yy in (y0, y1):
        d.line([(0, yy * k), (pv.width + 12, yy * k)], fill=(250, 210, 60, 255), width=2)
    draw_text(side, pv.width + 18, (y0 + y1) * k // 2 - 9, txt, 16)
save(figure(side, "Kit's proportions: about 2.2 heads (22 px tall, head 10 px)",
            "Big head and big eyes read at 1x. The figure stands on row 22; row 23 is the outline under the feet."),
     "ch03-proportion.png")
