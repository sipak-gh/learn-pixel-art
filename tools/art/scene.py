"""Scene composition for mossy-ruins: the gameplay layer (tiles + props + characters),
the ch08 value blockout, the final mockup and the animated preview."""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pix import blank, flip, paste, parallax_frame, rgba, rows, silhouette, tilemap  # noqa
import bg  # noqa: E402
import hero  # noqa: E402
import props  # noqa: E402
import slime  # noqa: E402
import tiles  # noqa: E402
import vfx  # noqa: E402

VIEW_W, VIEW_H = 320, 180
WORLD_W = 640
T = 16
GROUND_ROW = 4  # terrain row whose top the characters stand on
LAYER_Y = VIEW_H - 7 * T  # gameplay layer is 7 tiles tall, bottom aligned
FLOOR_Y = LAYER_Y + GROUND_ROW * T

# '#' terrain (autotiled), '~' water surface, '=' water, 'R' ruin block,
# 'l' 'm' 'r' plank bridge, 'w' background wall.  40 x 7 tiles = 640 x 112.
LAYOUT = """
................wwwwww..................
................wwwwww....lmmr..........
................wwwwww..................
................wRRRRw..................
#########lmmmmmmRRRRRRmmmmmmmr##########
#########~~~~~~~RRRRRR~~~~~~~~##########
#########=======RRRRRR========##########
"""


def ruin_keys(layout):
    """{(x, y): ruin piece name}: the top row gets moss, left/right ends get edges."""
    g = rows(layout)
    out = {}

    def is_r(x, y):
        return 0 <= y < len(g) and 0 <= x < len(g[0]) and g[y][x] == "R"

    for y, r in enumerate(g):
        for x, ch in enumerate(r):
            if ch != "R":
                continue
            top = not is_r(x, y - 1)
            left, right = not is_r(x - 1, y), not is_r(x + 1, y)
            if top:
                k = "top_left" if left else ("top_right" if right else "top")
            else:
                k = "left" if left else ("right" if right else
                                         ("brick_cracked" if (x * 3 + y) % 5 == 0 else "brick"))
            out[(x, y)] = k
    return out


def _ruin_tiles(layout):
    rs = tiles.ruin_set()
    return {xy: rs[k] for xy, k in ruin_keys(layout).items()}


def gameplay_layer(t=0, stage="final", water_frame=None, torch_frame=None):
    """The world at time step t (drives water and torch); stage 'blockout' = flat values."""
    g = rows(LAYOUT)
    terrain = ["".join("#" if c == "#" else "." for c in r) for r in g]
    img = tiles.autotile_map(terrain, variant_of=lambda x, y: 2 if (x * 7 + y * 5) % 23 == 0
                             else (1 if (x + y) % 3 == 0 else 0))
    wf = (t // 2) % 4 if water_frame is None else water_frame
    tm = {"~": tiles.water_top(wf), "=": tiles.water_fill(), "w": tiles.bg_wall(0),
          "l": tiles.plank("left"), "m": tiles.plank("mid"), "r": tiles.plank("right")}
    walls = tilemap({"w": tm["w"]}, ["".join(c if c == "w" else "." for c in r) for r in g])
    out = blank(img.width, img.height)
    out.alpha_composite(walls)
    # ruined back wall: knock some bricks out of its top edge
    for x in range(16 * T, 22 * T):
        for y in range(0, (5 if (x // 5) % 3 == 0 else (1 if (x // 3) % 2 else 0))):
            out.putpixel((x, y), (0, 0, 0, 0))
    out.alpha_composite(img)
    out.alpha_composite(tilemap({k: v for k, v in tm.items() if k in "~="}, LAYOUT))
    for (x, y), tile in _ruin_tiles(LAYOUT).items():
        out.alpha_composite(tile, (x * T, y * T))
    out.alpha_composite(tilemap({k: v for k, v in tm.items() if k in "lmr"}, LAYOUT))
    gy = GROUND_ROW * T  # ground top inside this layer
    # props (x, image, bottom y)
    tf = (t // 2) % 4 if torch_frame is None else torch_frame
    placed = [
        (2 * T, props.tree(), gy + 1),
        (6 * T, props.bush(), gy),
        (8 * T - 2, props.staged("sign"), gy + 1),
        (5 * T, props.tuft(0), gy),
        (33 * T, props.pillar(), gy + 1),
        (31 * T, props.staged("rock"), gy + 1),
        (36 * T, props.bush(5), gy),
        (37 * T, props.mushrooms(), gy),
        (17 * T + 4, props.staged("crate"), 3 * T),
        (19 * T + 8, props.torch().frames[tf], 2 * T + 14),
        (21 * T + 4, props.vines(20), 3 * T + 20),
        (27 * T + 4, props.tuft(1), 1 * T + 1),
        (39 * T, props.tuft(0), gy),
    ]
    for x, im, bottom in placed:
        out.alpha_composite(im, (x, bottom - im.height))
    return out


def characters(t=0, hero_x=80, slime_x=34 * T, hero_anim="idle"):
    """Return [(image, x, y)] in layer coordinates for frame step t."""
    h = {a.name: a for a in hero.all_anims("final", True)}[hero_anim]
    s = slime.idle()
    hf = h.frames[t % len(h.frames)]
    sf = s.frames[t % len(s.frames)]
    gy = GROUND_ROW * T
    return [(hf, hero_x, gy - 31), (sf, slime_x, gy - 23)]


STEP_MS = 90  # one time step t of the scene previews


def _frame_at_ms(anim, ms):
    """The frame of a looping Anim that is showing ms milliseconds after it started."""
    ms %= sum(anim.durations)
    for f, d in zip(anim.frames, anim.durations):
        if ms < d:
            return f
        ms -= d
    return anim.frames[-1]


def effects(t=0):
    """Ambient effects in layer coordinates: smoke rising from the wall torch and a sparkle
    marking the crate on the ruin ledge (a pickup hint). Each runs on its own clock."""
    ms = t * STEP_MS
    return [(_frame_at_ms(vfx.smoke(), ms + 250), 19 * T + 6, 2 * T - 26),
            (_frame_at_ms(vfx.sparkle(), ms), 17 * T + 16, 2 * T - 6)]


def world(t=0, with_chars=True, with_fx=True):
    lay = gameplay_layer(t)
    if with_chars:
        for im, x, y in characters(t):
            lay.alpha_composite(im, (x, y))
    if with_fx:
        for im, x, y in effects(t):
            lay.alpha_composite(im, (x, y))
    return lay


def frame_at(cam_x=0, t=0, fg=True):
    layers = [(img, speed, y) for _, img, speed, y in bg.layers()]
    layers.append((world(t), 1.0, LAYER_Y))
    if fg:
        layers.append((bg.foreground(), 1.4, VIEW_H - 32))
    return parallax_frame(layers, VIEW_W, VIEW_H, cam_x)


def preview_frames(n=48, pan=256):
    """Ping-pong camera pan with everything animating. A pan of 256 px brings the slime
    (world x 544) fully into view at the far end."""
    out = []
    for i in range(n):
        u = i / (n - 1)
        cam = pan * (1 - abs(1 - 2 * u))
        out.append(frame_at(cam, i))
    return out


def blockout():
    """ch08: the planned scene as flat value masses only (no detail): each depth plane
    gets one value, the hero gets the single accent colour."""
    vals = {"sky": "1", "clouds": "1", "mountains": "2", "treeline": "3", "forest": "4"}
    layers = [(silhouette(img, vals[name]), speed, y) for name, img, speed, y in bg.layers()]
    world_img = silhouette(gameplay_layer(0), "5")
    for im, x, y in characters(0):
        world_img.alpha_composite(silhouette(im, "R"), (x, y))
    layers.append((world_img, 1.0, LAYER_Y))
    layers.append((silhouette(bg.foreground(), "K"), 1.4, VIEW_H - 32))
    return parallax_frame(layers, VIEW_W, VIEW_H, 0)


def thumbnails():
    """Three composition thumbnails (64x36) for the ch08 exercise example."""
    a = blank(64, 36, "1")
    for x in range(64):
        for y in range(36):
            if y > 26 - (x // 16) % 2 * 2:
                a.putpixel((x, y), rgba("5"))
            elif y > 16 + abs(x - 40) // 3 and x > 24:
                a.putpixel((x, y), rgba("3"))
    for y in range(20, 27):
        a.putpixel((14, y), rgba("R"))
        a.putpixel((15, y), rgba("R"))
    b = blank(64, 36, "1")
    for x in range(64):
        for y in range(36):
            if y > 28:
                b.putpixel((x, y), rgba("5"))
            elif y > 12 + abs(x - 20) // 2:
                b.putpixel((x, y), rgba("4"))
    for y in range(22, 29):
        for x in (44, 45):
            b.putpixel((x, y), rgba("R"))
    c = blank(64, 36, "2")
    for x in range(64):
        for y in range(36):
            if x < 12 or x > 52 or y > 30:
                c.putpixel((x, y), rgba("K"))
            elif y > 24:
                c.putpixel((x, y), rgba("4"))
    for y in range(18, 25):
        for x in (31, 32):
            c.putpixel((x, y), rgba("R"))
    return [a, b, c]
