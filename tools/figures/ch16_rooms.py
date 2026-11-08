"""Ch. 16 figures: room composition."""
from _v import *

r = world.ROOMS["greenhouse"]
L = r["layout"].strip("\n").split("\n") if False else [x for x in r["layout"].split("\n")[1:-1]]
COL = {"#": (90, 200, 170), "=": (160, 160, 170), "_": (160, 160, 170), " ": (0, 0, 0)}
blk = Image.new("RGBA", (16, 15), (20, 20, 28, 255))
px = blk.load()
for y, rw in enumerate(L):
    for x, c in enumerate(rw):
        px[x, y] = COL.get(c, (30, 34, 50)) + (255,)
for _, mx, my in r["props"]:
    px[mx, my] = (240, 160, 60, 255)
for k_, a, x, y, f in r["actors"]:
    if not k_.startswith("fx"):
        px[(x + 8) // 16, (y + 16) // 16] = (255, 80, 80, 255) if k_ == "kit" else (230, 90, 230, 255)
save(figure(view(blk, 16, grid=True, bg=BLACK), "Blockout: one pixel per metatile",
            "Teal ground · grey platforms · orange props · red Kit · pink creatures. "
            "Decide the route before drawing a single tile."), "ch16-blockout.png")

steps = []
lay = r["layout"]
s1, _, _ = rooms.build("\n".join(l_ if i < 2 else "".join(c if c in "#=_ " else " " for c in l_)
                                for i, l_ in enumerate(lay.split("\n"))), "greenhouse")
s2, _, _ = rooms.build(lay, "greenhouse")
s3, _ = world.background("greenhouse", with_hud=False)
s4 = world.scene("greenhouse", 0)[0]
save(panel([(nv(s1, 1), "1 solid ground"), (nv(s2, 1), "2 + walls, glass, vines"),
            (nv(s3, 1), "3 + props"), (nv(s4, 1), "4 + actors, HUD")], gap=12,
           title="Building a room in passes"), "ch16-passes.png")

# composition overlay: route + focal points
comp = s4.copy()
ov = Image.new("RGBA", comp.size, (0, 0, 0, 0))
d = ImageDraw.Draw(ov)
route = [(72, 206), (170, 206), (176, 190), (190, 190), (192, 174), (206, 174), (208, 158), (240, 158)]
d.line(route, fill=(255, 220, 60, 220), width=2)
d.line([(40, 158), (60, 132), (82, 126), (172, 126)], fill=(255, 220, 60, 160), width=2)
for cx, cy in ((120, 112), (64, 188)):
    d.ellipse([cx - 14, cy - 14, cx + 14, cy + 14], outline=(255, 90, 90, 230), width=2)
comp.alpha_composite(ov)
save(figure(nv(comp, 2), "Composition: the route (yellow) and focal points (red)",
            "Lower route: floor to the stairs. Upper route: girder to the pod platform. Kit and the pod are the two focal points; lamps mark the way."),
     "ch16-composition.png")

busy = s3.copy()
for i, (x, y) in enumerate([(32, 96), (48, 96), (96, 64), (176, 64), (208, 96), (176, 128), (32, 128), (144, 160)]):
    busy.alpha_composite(render(gpaste(T.back_wall(), P.PROPS[["crate", "lamp", "terminal", "drawers"][i % 4]][0][:16], 0, 0),
                                GH["bg"][[3, 3, 2, 2][i % 4]], True), (x, y))
save(compare(nv(busy.crop((0, 32, 256, 224)), 2), nv(s3.crop((0, 32, 256, 224)), 2),
             "Avoid: props everywhere", "Better: props where the route needs them",
             title="Clutter: empty wall is part of the composition"), "ch16-clutter.png")

save(panel([(nv(world.scene(a, 0)[0], 1), AREAS[a]["name"]) for a in ORDER], gap=12,
           title="Four rooms, one set of rules"), "ch16-rooms.png")

# overscan + HUD: where the status bar lives and what is BG vs sprite
sc = world.scene("greenhouse", 0)[0]
k = 2
big = nv(sc, k)
d = ImageDraw.Draw(big)
for y0 in (0, 232):
    d.rectangle([0, y0 * k, big.width - 1, (y0 + 8) * k - 1], outline=(255, 90, 90), width=2)
d.rectangle([2, 8 * k + 2, big.width - 3, 32 * k - 3], outline=(250, 210, 60), width=2)
d.rectangle([2, 32 * k + 2, big.width - 3, 232 * k - 3], outline=(90, 220, 120), width=2)
hb = nv(sc.crop((0, 0, 256, 32)), 3)
d2 = ImageDraw.Draw(hb)
for _, x, y in hud.hud_sprites(GH["spr"][0], GH["spr"][2], **world.ROOMS["greenhouse"]["hud"]):
    d2.rectangle([x * 3 - 1, y * 3 - 1, (x + 8) * 3, (y + 8) * 3], outline=(90, 170, 255), width=2)
save(panel([(big, "red: overscan (8 px) · yellow: HUD rows (BG3) · green: playfield"),
            (hb, "HUD at 3x: blue boxes are 8 x 8 sprites, the rest is BG tiles")], gap=16,
           title="Overscan and the HUD",
           note="The HUD is the top two metatile rows (32 px); its art starts at y = 12, inside the safe area. "
                "The bottom row loses 8 px to overscan, so it holds only ground."),
     "ch16-overscan-hud.png")
