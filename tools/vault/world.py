"""The final `hollow-vault` area: one finished screen per zone (HUD + 13-row playfield),
with actors (Kit, creatures, effects) and ambient particles, rendered at any time t (ms).

scene(area, t) -> (RGBA 256x240 image, objects) where objects are (x, y, w, h) sprite boxes
for the 8-sprites-per-scanline check.
"""
from __future__ import annotations

import random

from PIL import Image

from nes import render, gflip
from pix import paste
from vault import kit, creatures, fx, rooms, hud, bg as B
from vault.palettes import AREAS

ROOMS = {
    "greenhouse": dict(layout="""
                
                
################
#..g.g.g..g.g..#
#..g.G.g..g.g..#
#v.....v.......#
#v..........v..#
#...........v..#
#....######....#
#..............#
#==..........###
#.....|.....####
#.....|.t..#####
########-+######
################
""", props=[("lamp", 4, 9), ("planter", 2, 12), ("fern", 2, 11), ("terminal", 9, 12),
            ("pod", 7, 6), ("lamp", 12, 5)],
        actors=[("kit", "idle", 56, 184, False), ("hopper", "idle", 96, 112, False),
                ("drone", "hover", 148, 60, False), ("fx:seed", None, 30, 136, False),
                ("fx:seed", None, 216, 136, False)],
        particles="spore", hud=dict(hp=3, seeds=7, area="GREENHOUSE", oil=5)),
    "cistern": dict(layout="""
                
                
################
#....o....o....#
#..............#
#..............#
#...######.....#
#..............#
#.........==...#
###.......|....#
###.......|.####
####......|.####
####wwwwwwww####
####WWWWWWWW####
################
""", props=[("door", 1, 7), ("lamp", 13, 4), ("rubble", 5, 5), ("drawers", 8, 5)],
        actors=[("kit", "walk", 160, 104, False), ("slug", "crawl", 72, 80, False),
                ("slug", "crawl", 200, 144, True), ("fx:splash", None, 96, 184, False)],
        particles="drip", hud=dict(hp=2, seeds=12, area="CISTERN", oil=3)),
    "furnace": dict(layout="""
                
                
################
#..o.......o.|.#
#............|.#
#.......rrrr.|.#
#............|.#
#........----+.#
##.............#
##...rrr.......#
##.............#
##..........####
####.......#####
####mmmmmmm#####
####MMMMMMM#####
""", props=[("crate", 12, 10), ("crate", 13, 10), ("crate", 13, 9), ("lamp", 6, 3),
            ("terminal", 2, 10)],
        actors=[("kit", "run", 84, 120, False), ("drone", "alert", 140, 54, False),
                ("hopper", "hop", 204, 128, False)],
        particles="ember", hud=dict(hp=4, seeds=19, area="FURNACE", oil=6)),
    "ridge": dict(layout="""
                
                
                
                
                
                
                
                
                
                
              ##
###          ###
####  ____  ####
################
################
""", props=[], bands=[(B.sky(h=64), 1, 2), (B.far_hills(), 2, 6), (B.towers(), 1, 9)],
        actors=[("kit", "jump", 64, 152, False), ("drone", "hover", 170, 120, False),
                ("hopper", "idle", 232, 144, False)],
        particles="star", hud=dict(hp=4, seeds=24, area="RIDGE", oil=4)),
}

SPRITE_SUB = {"kit": 0, "hopper": 1, "slug": 1, "drone": 3}


def _anim_frame(frames_durs, t):
    imgs, durs = frames_durs
    t %= sum(durs)
    for im, d in zip(imgs, durs):
        if t < d:
            return im
        t -= d
    return imgs[-1]


def background(area, frame=0, with_hud=True):
    r = ROOMS[area]
    img, attrs, grids = rooms.build(r["layout"], area, props=r["props"], frame=frame,
                                    bands=r.get("bands", ()))
    if with_hud:
        paste(img, hud.hud_img(AREAS[area]["bg"][3], **r["hud"]), 0, 0)
        for y in range(2):
            attrs[y] = [3] * 16
    return img, attrs


def actor_frames(area, kind, anim):
    sp = AREAS[area]["spr"]
    if kind == "kit":
        return kit.frames(anim)
    if kind.startswith("fx:"):
        name = kind[3:]
        return fx.frames(name, sp[0] if name == "dust" else sp[2])
    return creatures.frames(kind, anim, sp[SPRITE_SUB[kind]])


def particles(area, kind, t, n=10):
    """Ambient 1-2 px particles drawn as sprites (deterministic in t)."""
    rnd = random.Random(area)
    out = []
    for i in range(n):
        x0, y0, sp = rnd.randrange(16, 240), rnd.randrange(40, 200), rnd.uniform(0.6, 1.4)
        ph = rnd.randrange(4000)
        if kind == "spore":  # drift up and sway
            y = 40 + (y0 - int((t + ph) * 0.012 * sp)) % 168
            x = x0 + (2 if ((t + ph) // 600) % 2 else 0)
            out.append((x, y, "spore"))
        elif kind == "ember":  # rise faster, flicker
            y = 40 + (y0 - int((t + ph) * 0.03 * sp)) % 168
            x = x0 + ((t + ph) // 200) % 3 - 1
            out.append((x, y, "ember"))
        elif kind == "drip" and i < 4:  # fall from the ceiling into the pool
            y = 48 + int((t + ph) * 0.06 * sp) % 144
            out.append((64 + i * 40, y, "drip"))
        elif kind == "star" and i < 3:  # twinkle (BG stars are tiles; these are sprites)
            if ((t + ph) // 300) % 3 == 0:
                out.append((x0, 40 + y0 % 60, "twinkle"))
    return out


def scene(area, t=0, with_hud=True):
    frame = (t // 200) % 4
    img, _ = background(area, frame, with_hud)
    sp = AREAS[area]["spr"]
    objects = []
    if with_hud:
        for im, x, y in hud.hud_sprites(sp[0], sp[2], **ROOMS[area]["hud"]):
            img.alpha_composite(im, (x, y))
            objects.append((x, y, 8, 8))
    for kind, anim, x, y, flip in ROOMS[area]["actors"]:
        im = _anim_frame(actor_frames(area, kind, anim), t)
        if flip:
            im = im.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
        img.alpha_composite(im, (x, y))
        if kind == "kit":
            objects.append((x + 4, y, 16, 24))
        else:
            objects.append((x, y, im.width, im.height))
    pal = sp[2]
    for x, y, k in particles(area, ROOMS[area]["particles"], t):
        grid = {"spore": ["3"], "ember": ["3", "2"], "drip": ["3", "3"],
                "twinkle": [".3.", "323", ".3."]}[k]
        img.alpha_composite(render(grid, pal), (x, y))
        objects.append((x, y, 8, 8))
    return img, objects


def gif_frames(area, length=2400, step=100):
    return [scene(area, t)[0] for t in range(0, length, step)], [step] * (length // step)
