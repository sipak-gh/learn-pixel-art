"""Ch. 12 figures: enemies and creatures."""
from _v import *

SP = GH["spr"]
k0 = kitimg()
hop = creatures.frames("hopper", "idle", SP[1])[0][0]
slug = creatures.frames("slug", "crawl", SP[1])[0][0]
drn = creatures.frames("drone", "hover", SP[3])[0][0]
line = Image.new("RGBA", (24 + 16 * 3 + 24, 28), (0, 0, 0, 0))
line.alpha_composite(k0, (0, 4))
for i, im in enumerate((hop, slug, drn)):
    line.alpha_composite(im, (28 + i * 22, 12 if i < 2 else 0))
save(panel([(nv(line, 1), "1x"), (nv(line, 5), "5x")], title="The cast to scale",
           note="Kit 16 x 24 · spore hopper 16 x 16 · drip slug 16 x 10 · warden drone 16 x 16 (floats)."),
     "ch12-lineup.png")

anims = [("hopper", "idle", 1), ("hopper", "hop", 1), ("slug", "crawl", 1), ("drone", "hover", 3),
         ("drone", "alert", 3)]


def draw(t):
    ims = [view(anim_frames(creatures.frames(k_, a, SP[s]), t), 5, bg=SPR_BG) for k_, a, s in anims]
    return row([label(im, "%s %s" % (k_, a), 14, FIG_FG) for im, (k_, a, s) in zip(ims, anims)], 12)


fr_, d_ = timeline(2080, 40, draw)
gif("ch12-creatures.gif", fr_, d_, k=1, bg=FIG_BG)

hf, hd = creatures.frames("hopper", "hop", SP[1])
save(figure(filmstrip(hf, 7, hd, bg=SPR_BG), "Spore hopper hop: crouch, launch, hang, land",
            "The cap rises 4 px in the air frames; crouch frames squash the stalk."), "ch12-hop-strip.png")

# metasprite tiles + flips: as drawn vs a mirrored design
img16 = hop
sym = img16.copy()
sym.alpha_composite(Image.new("RGBA", (8, 16), (0, 0, 0, 0)), (8, 0))
sym = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
sym.alpha_composite(img16.crop((0, 0, 8, 16)), (0, 0))
sym.alpha_composite(img16.crop((0, 0, 8, 16)).transpose(Image.Transpose.FLIP_LEFT_RIGHT), (8, 0))
save(panel([(sv(img16, 10, major=8), "as drawn: %d unique tiles (%d with flips)"
             % (unique_tiles(img16), unique_tiles(img16, flips=True))),
            (sv(sym, 10, major=8), "mirrored design: %d tiles + H-flip" % unique_tiles(sym, flips=True))],
           title="Symmetry saves tiles: NES sprites can be flipped per tile",
           note="The hopper's off-centre highlights cost 2 extra tiles. Worth it for a hero; for a "
                "common enemy, a mirrored design halves its CHR space."),
     "ch12-flip.png")

# palette variants per area
items = []
for a in ORDER:
    s = AREAS[a]["spr"][1]
    items.append((nv(creatures.frames("hopper", "idle", s)[0][0], 6), "%s SP1" % AREAS[a]["name"]))
save(panel(items, title="Each area recolours its creatures through SP1"), "ch12-area-variants.png")

save(panel([(sv(creatures.frames("drone", "hover", SP[3])[0][0], 8, major=None), "hover: lens open, slow bob"),
            (sv(creatures.frames("drone", "alert", SP[3])[0][1], 8, major=None), "alert: lens blinks, rotor at 80 ms")],
           title="Telegraphing: show the state change before the attack"), "ch12-drone-states.png")

# mirroring a metasprite: every tile has its own flip bit, so the tiles must also swap places
hgrid = creatures.grids("hopper", "idle")[0]
hsub = SP[1]


def tile_flip_only(grid):
    """Flip each 8x8 tile in place (what the flip bits alone do)."""
    out = gblank(16, 16)
    for ty in (0, 8):
        for tx in (0, 8):
            out = gpaste(out, gflip(gcrop(grid, tx, ty, 8, 8)), tx, ty)
    return out


save(panel([(sv(render(hgrid, hsub), 10), "as drawn: faces left"),
            (sv(render(tile_flip_only(hgrid), hsub), 10), "Avoid: flip bits only", FIG_BAD),
            (sv(render(gflip(hgrid), hsub), 10), "Better: flip bits + swap columns", FIG_GOOD)],
           title="Mirroring a 16 x 16 metasprite",
           note="Each 8 x 8 sprite flips on its own. To face right, set H-flip on all four sprites "
                "and swap the left and right columns."),
     "ch12-metasprite-flip.png")

# friend or foe: the hopper in the hero's palette vs its own
room, _ = world.background("greenhouse", with_hud=False)
box = (24, 152, 152, 216)


def foe_scene(sub):
    im = room.copy()
    im.alpha_composite(k0, (56, 184))
    im.alpha_composite(creatures.frames("hopper", "idle", sub)[0][0], (104, 192))
    return nv(im.crop(box), 3)


save(panel([(foe_scene(SP[0]), "Avoid: hopper in Kit's SP0", FIG_BAD),
            (foe_scene(SP[1]), "Better: hopper in SP1", FIG_GOOD)],
           title="Friend or foe: never give a foe the hero's palette",
           note="In SP0 the hopper reads as Kit's pet or a pickup. Its own hue says 'something else' "
                "before the player has read its shape."),
     "ch12-friend-or-foe.png")
