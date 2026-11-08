"""Ch. 17 figures: props and foliage."""
from _v import *


def prop_img(name, sub_override=None, area="greenhouse", wall=True):
    grid, subs = P.PROPS[name]
    wc, hc = len(grid[0]) // 16, len(grid) // 16
    im = Image.new("RGBA", (wc * 16, hc * 16), (0, 0, 0, 255))
    for j in range(hc):
        for i in range(wc):
            cell = [r[i * 16:i * 16 + 16] for r in grid[j * 16:j * 16 + 16]]
            base = T.back_wall(part=i % 2 + 2 * (j % 2)) if wall else gblank(16, 16, "0")
            im.alpha_composite(render(gpaste(base, cell, 0, 0), AREAS[area]["bg"][subs[j * wc + i]], True),
                               (i * 16, j * 16))
    return im


items = [(attr_view(prop_img(n), [[s] * (len(P.PROPS[n][0][0]) // 16)
                                  for s in P.PROPS[n][1][::len(P.PROPS[n][0][0]) // 16]], 5, alpha=40),
          n) for n in P.PROPS]
save(panel(items, gap=14, title="Props sit on the 16 x 16 grid, one sub-palette per cell",
           note="Tinted by sub-palette: BG0 red · BG1 green · BG2 blue · BG3 yellow. Every prop is drawn over the back wall."),
     "ch17-props-grid.png")

# construction of the crate: silhouette, planes, details
cr = P.PROPS["crate"][0]
sil = ["".join("1" if c != "." else "." for c in r) for r in cr]
planes = ["".join({"3": "3", "2": "2", "1": "2", "0": "0", ".": "."}[c] for c in r) for r in cr]
SUB3 = GH["bg"][3]
save(panel([(sv(render(sil, (0x0F, 0x00, 0x00, 0x00)), 8, grid=False, major=None), "1 silhouette"),
            (sv(render(planes, SUB3), 8, grid=False, major=None), "2 lit top + face"),
            (sv(render(cr, SUB3), 8, grid=False, major=None), "3 shadow + details")],
           title="Drawing a prop in three passes (crate, BG3)"), "ch17-crate-steps.png")

# foliage
fol = [("vine", gpaste(T.back_wall(), T.vine(s), 0, 0), 1) for s in (0, 2, 5)]
fol += [("tuft", gpaste(T.back_wall(), T.grass_tuft(s), 0, 0), 1) for s in (0, 3)]
items = [(nv(render(gr, GH["bg"][s], True), 5), n) for n, gr, s in fol]
items += [(nv(prop_img("fern"), 5), "fern"), (nv(prop_img("pod"), 5), "seed pod (16 x 32)")]
save(panel(items, gap=12, title="Foliage: a few variants, reused everywhere",
           note="Vines are seeded variants of one generator; the fern and pod are hand-placed hero props."),
     "ch17-foliage.png")

# floating vs grounded
lay = """
....
....
####
"""
base, _, _ = rooms.build(lay, "greenhouse")
crate = render(P.PROPS["crate"][0], SUB3)
bad = base.copy(); bad.alpha_composite(crate, (24, 12))
good = base.copy(); good.alpha_composite(crate, (24, 16))
rub = render(P.PROPS["rubble"][0], GH["bg"][0])
good.alpha_composite(rub, (8, 16))
save(compare(nv(bad, 6), nv(good, 6), "Avoid: floating 4 px above the ground", "Better: sits on the moss line; rubble ties it in",
             title="Grounding: props must touch the surface"), "ch17-grounding.png")

img, _ = world.background("cistern", with_hud=False)
save(figure(nv(img.crop((0, 48, 240, 176)), 3), "Props in context (Cistern): door, drawers, rubble, lamp",
            "Props tell the story - who lived here? - and mark exits and save points."), "ch17-in-room.png")
