"""Wren, the hero of the mossy-ruins pack (32x32 frames, faces right, light from upper left).

The sprite is assembled from hand-drawn parts (head, scarf, torso, arms, legs, tail). A frame
is a list of parts with offsets, so the same drawing is reused across animations the way an
artist copies and nudges parts between frames. Every visible pixel is still a hand-placed
pixel from a grid below.

Stages (how far the course has developed the character):
  'silhouette' solid shape (ch03)    'value'  greyscale value study (ch04)
  'flat'       base colours (ch05)    'final'  shaded + selective outline (ch06+)
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pix import (Anim, blank, grayscale, outline_in, paste, recolor, rgba, rows,  # noqa: E402
                 selout, silhouette, sprite, flip)

W = H = 32

# ---------------------------------------------------------------------------
# Parts (shaded colours; light from the upper left)
# ---------------------------------------------------------------------------
P = {}
P["head"] = """
.....bc.....
....bbbb....
..bbccccbb..
.bccccccccb.
bcccbbbbbbcb
bccbbbbbbbbb
dbbbbbfbbfbb
dbbbbbffffff
dbbbbfffffKf
ddbbbFffffKff
.ddbbFFfkfff
..ddddFFFFF.
"""
# Head turned slightly down/forward (used on hard landings and attacks).
P["head_down"] = """
............
.....bc.....
...bbbbbb...
..bccccccbb.
.bcccbbbbbcb
bccbbbbbbbbb
dbbbbbfbbfbb
dbbbbbffffff
dbbbbfffffKf
ddbbbFffffKff
.ddbbFFfkfff
..dddFFFFFF.
"""
# Eyes shut (hurt).
P["head_hurt"] = """
.....bc.....
....bbbb....
..bbccccbb..
.bccccccccb.
bcccbbbbbbcb
bccbbbbbbbbb
dbbbbbfbbfbb
dbbbbbffffff
dbbbbffffKKf
ddbbbFfffffff
.ddbbFFfkfff
..ddddFFFFF.
"""
P["scarf"] = """
..mRRRRRRRm.
.mRkRRRRRRRm
"""
P["torso"] = """
...uuuuuun..
..uuuuuuunn.
..uuuuuuunn.
..uuuuuuunn.
..dbbbbybdd.
.uuuuuuunnn.
"""
# Torso leaning forward (run, attack).
P["torso_lean"] = """
....uuuuun..
...uuuuuuunn
..uuuuuuunn.
..uuuuuuunn.
..dbbbbybdd.
.uuuuuuunn..
"""

# Scarf tails: the end that trails behind (to the left). Several shapes for motion.
P["tail_rest"] = """
....mR
..mRRm
.mRmm.
mRm...
mm....
"""
P["tail_sway"] = """
....mR
...mRm
.mRRm.
mRmm..
mm....
"""
P["tail_lift"] = """
.....mR
mRRRRRm
.mmmm..
"""
P["tail_flow"] = """
......mR
..mRRRRm
mRRmmm..
mm......
"""
P["tail_high"] = """
mm....
mRm...
.mRm..
..mRmR
....mR
"""
P["tail_drop"] = """
...mR
..mRm
..Rm.
.mR..
.m...
"""

# Near arm (in front of the body). Anchor = top-left of the grid at the shoulder.
P["arm_down"] = """
nuu
nuu
nuu
nnu
Ff.
"""
P["arm_fwd"] = """
nuu..
nuuu.
.nuuu
..nnF
...Ff
"""
P["arm_back"] = """
.nuu
.nuu
nuu.
nn..
Ff..
"""
P["arm_up"] = """
...Ff
..nuF
.nuu.
nuu..
nu...
"""
P["arm_raise_back"] = """
Ff..
nu..
nuu.
.nuu
..nu
"""
P["arm_reach"] = """
nuuuuFf
.nnnnFF
"""
# Far arm (behind the body, darker).
P["farm_fwd"] = """
nnn..
.nnn.
..nnF
...FF
"""
P["farm_back"] = """
.nnn
nnn.
nn..
F...
"""

# Legs: near leg uses 3/4 + c/b, far leg 4/5 + b/d. Anchor = top-left (hip row).
P["legs_idle"] = """
...4444444...
...5554344...
..555..3444..
..555...3444.
.dddb...bbcb.
.dddd...ddddb
"""
P["legs_contact"] = """
....4444444..
...5554.3444.
..5554...3444
.555......344
.dd5......bcb
ddd.......dddd
"""
P["legs_down"] = """
....4444444..
...5554.3444.
..555...3444.
..555...3444.
..ddd...bbcb.
..dddd..ddddb
"""
P["legs_pass"] = """
....444444...
....55344....
....55344....
....d5344....
....dd344....
.....dbbcb...
"""
P["legs_up"] = """
....4444444..
....5534444..
...5554.3444.
...ddd...344.
....dd...bcb.
.........dddd
"""
# The same four poses with the far leg in front (second half of a cycle).
P["legs_contact2"] = """
....4444444..
...3444.5554.
..3444...5555
.344......d55
.bcb......ddd
bbbd.......dd
"""
P["legs_down2"] = """
....4444444..
...3444.5554.
..344...5554.
..344...5554.
..bcb...dddd.
..bbbd..dddd.
"""
P["legs_pass2"] = """
....444444...
....34455....
....34455....
....3445d....
....344dd....
...bcbbd.....
"""
P["legs_up2"] = """
....4444444..
....3444455..
...3444.5554.
...bcb...555.
....bb...ddd.
.........ddd.
"""
# Run legs (longer stride, flight phases).
P["legs_run_push"] = """
....4444444..
...5554..3444
..555.....344
.555......bcb
ddd.......ddd
dd...........
"""
P["legs_run_fly"] = """
....4444444..
...555..34444
..555...3..44
.ddd.....bcb4
.dd......bbbd
.............
"""
P["legs_run_land"] = """
....4444444..
....5534444..
...555..3444.
..ddd....344.
..dd.....bcb.
.........dddd
"""
P["legs_run_push2"] = """
....4444444..
...3444..5554
..344.....555
.344......ddd
bcb.......ddd
bb...........
"""
P["legs_run_fly2"] = """
....4444444..
...444..55555
..344...5..55
.bcb.....ddd5
.bb......ddd.
.............
"""
P["legs_run_land2"] = """
....4444444..
....3445555..
...344..5555.
..bcb....555.
..bb.....ddd.
.........ddd.
"""
# Jump legs.
P["legs_crouch"] = """
...4444444...
..55544344...
.5555.33444..
.ddd...bbcb..
.dddd..ddddb.
"""
P["legs_tuck"] = """
....4444444..
....555344...
...ddd.344...
...dd.bbcb...
.......bbd...
"""
P["legs_stretch"] = """
....444444...
....55344....
....55344....
....55344....
....d5344....
....dd344....
.....ddbcb...
......dddd...
"""
P["legs_fall"] = """
....4444444..
...5554.3444.
..555....344.
..ddd....bcb.
...dd....bbbd
"""
P["legs_land"] = """
..4444444444..
.55554.344444.
dddd5...3bbcb.
ddddd...ddddd.
"""
P["legs_lunge"] = """
....44444444...
...5554..34444.
..555......3444
.555.......bbcb
dddd.......dddd
"""

# Sword (held in the near hand; points right).
P["sword_fwd"] = """
yy........
dy1111111W
y.322222..
"""
P["sword_up"] = """
.1
W1
12
12
12
12
12
y3
dy
.y
"""

# Sword cocked back over the shoulder (points up and back).
P["sword_back"] = """
W......
12.....
.12....
..12...
...12..
....3y.
....yd.
.....yy
"""

# Smear: the arc the blade sweeps in one frame (ch16).
P["smear"] = """
..SSS11..........
.....SSS111W.....
........SS111WW..
..........SS111W.
............SS11W
.............SS1W
..............S1W
..............S1W
..............S1W
.............SS1W
............SS11W
...........SS11W.
..........SS1WW..
.........S11W....
"""

# Colours used for the outline of each fill colour (selective outline, ch06).
SELOUT = {"b": "d", "c": "d", "d": "d", "f": "b", "F": "b", "k": "b", "R": "m", "m": "d",
          "u": "n", "n": "5", "y": "b", "3": "5", "4": "5", "5": "K", "1": "4", "2": "4",
          "W": "3", "S": "2"}

# Flat colours: every shade of a material collapses to its base colour (ch05).
FLAT = {"c": "b", "d": "b", "F": "f", "k": "f", "m": "R", "n": "u", "3": "4", "5": "4"}


# ---------------------------------------------------------------------------
# Frame assembly
# ---------------------------------------------------------------------------
# Default part positions for the standing pose (top-left of each grid in the frame).
BASE = {
    "tail": (8, 18), "torso": (10, 19), "legs": (10, 25), "head": (10, 6), "scarf": (10, 17),
    "arm": (16, 19), "farm": (14, 19),
}

_cache: dict = {}


def part(name: str):
    if name not in _cache:
        _cache[name] = sprite(rows(P[name]))
    return _cache[name]


def frame(legs="legs_idle", legs_at=(0, 0), body=(0, 0), head="head", head_at=(0, 0),
          torso="torso", tail="tail_rest", tail_at=(0, 0), arm="arm_down", arm_at=(0, 0),
          farm=None, farm_at=(0, 0), sword=None, sword_at=(0, 0), sword_back=False, smear_at=None,
          stage="final", flash=False):
    """Assemble one 32x32 frame. Offsets are relative to BASE. body moves everything above
    the legs (head, scarf, torso, arms, tail)."""
    bx, by = body
    layers = []

    def at(key, off, extra=(0, 0)):
        x, y = BASE[key]
        return x + off[0] + extra[0], y + off[1] + extra[1]

    if farm:
        layers.append((farm, at("farm", farm_at, body)))
    if tail:
        layers.append((tail, at("tail", tail_at, body)))
    layers.append((legs, at("legs", legs_at)))
    layers.append((torso, at("torso", (0, 0), body)))
    layers.append((head, at("head", head_at, body)))
    layers.append(("scarf", at("scarf", head_at if head_at[1] > 0 else (0, 0), body)))
    if sword and sword_back:
        layers.insert(0, (sword, at("arm", sword_at, body)))
    elif sword:
        layers.append((sword, at("arm", sword_at, body)))
    if arm:
        layers.append((arm, at("arm", arm_at, body)))
    img = blank(W, H)
    for name, (x, y) in layers:
        p = part(name)
        if stage == "flat":
            p = recolor(p, FLAT)
        paste(img, p, x, y)
    if smear_at is not None:
        paste(img, part("smear"), *smear_at)
    return finish(img, stage, flash)


def finish(img, stage="final", flash=False):
    if stage == "silhouette":
        return silhouette(img, "K")
    if stage == "value":
        return outline_in(value_study(img), "K")
    if stage == "flat":
        return outline_in(img, "K")
    out = selout(img, SELOUT)
    if flash:
        out = silhouette(out, "W")
    return out


def value_study(img):
    """Map each colour to one of five greys by its luminance (a value study)."""
    greys = ["K", "4", "3", "2", "1"]
    g = grayscale(img)
    out = img.copy()
    px, gp = out.load(), g.load()
    for y in range(img.height):
        for x in range(img.width):
            if px[x, y][3]:
                v = gp[x, y][0]
                i = min(4, int(v / 256 * 5 * 1.1))
                px[x, y] = rgba(greys[i])
    return out


def stand(stage="final"):
    return frame(stage=stage)


# ---------------------------------------------------------------------------
# Animations (durations in milliseconds)
# ---------------------------------------------------------------------------
def idle(stage="final") -> Anim:
    f = [
        frame(stage=stage),
        frame(body=(0, 1), head_at=(0, 0), tail="tail_rest", stage=stage),
        frame(body=(0, 1), tail="tail_sway", stage=stage),
        frame(body=(0, 0), head_at=(0, 1), tail="tail_sway", stage=stage),
    ]
    return Anim("idle", f, [400, 160, 400, 160])


def walk(stage="final", secondary=True) -> Anim:
    t = (lambda a, b: a if secondary else b)
    poses = [
        dict(legs="legs_contact", body=(0, 0), arm="arm_back", farm="farm_fwd",
             tail=t("tail_sway", "tail_rest")),
        dict(legs="legs_down", body=(0, 1), arm="arm_back", farm="farm_fwd",
             tail=t("tail_rest", "tail_rest")),
        dict(legs="legs_pass", body=(0, 0), arm="arm_down", tail=t("tail_rest", "tail_rest")),
        dict(legs="legs_up", body=(0, -1), arm="arm_fwd", farm="farm_back",
             tail=t("tail_drop", "tail_rest")),
        dict(legs="legs_contact2", body=(0, 0), arm="arm_fwd", farm="farm_back",
             tail=t("tail_sway", "tail_rest")),
        dict(legs="legs_down2", body=(0, 1), arm="arm_fwd", farm="farm_back",
             tail=t("tail_rest", "tail_rest")),
        dict(legs="legs_pass2", body=(0, 0), arm="arm_down", tail=t("tail_rest", "tail_rest")),
        dict(legs="legs_up2", body=(0, -1), arm="arm_back", farm="farm_fwd",
             tail=t("tail_drop", "tail_rest")),
    ]
    return Anim("walk", [frame(stage=stage, **p) for p in poses], 100)


def run(stage="final", secondary=True) -> Anim:
    t = (lambda a, b: a if secondary else b)
    common = dict(torso="torso_lean", head_at=(1, 0))
    poses = [
        dict(legs="legs_run_push", body=(1, 0), arm="arm_back", farm="farm_fwd",
             tail=t("tail_lift", "tail_rest")),
        dict(legs="legs_run_fly", body=(1, -1), arm="arm_back", farm="farm_fwd",
             tail=t("tail_flow", "tail_rest")),
        dict(legs="legs_run_land", body=(1, 1), arm="arm_down", tail=t("tail_lift", "tail_rest")),
        dict(legs="legs_run_push2", body=(1, 0), arm="arm_fwd", farm="farm_back",
             tail=t("tail_flow", "tail_rest")),
        dict(legs="legs_run_fly2", body=(1, -1), arm="arm_fwd", farm="farm_back",
             tail=t("tail_lift", "tail_rest")),
        dict(legs="legs_run_land2", body=(1, 1), arm="arm_down", tail=t("tail_flow", "tail_rest")),
    ]
    return Anim("run", [frame(stage=stage, **common, **p) for p in poses], 80)


def jump(stage="final", secondary=True) -> Anim:
    t = (lambda a, b: a if secondary else b)
    f = [
        frame(legs="legs_crouch", legs_at=(0, 1), body=(0, 2), head="head_down",
              head_at=(0, -1), arm="arm_back", tail=t("tail_lift", "tail_rest"), stage=stage),
        frame(legs="legs_stretch", legs_at=(0, -2), body=(0, -2), arm="arm_up",
              arm_at=(0, -1), tail=t("tail_drop", "tail_rest"), stage=stage),
        frame(legs="legs_tuck", body=(0, -1), arm="arm_fwd", tail=t("tail_drop", "tail_rest"),
              stage=stage),
        frame(legs="legs_tuck", body=(0, 0), arm="arm_down", tail=t("tail_flow", "tail_rest"),
              stage=stage),
        frame(legs="legs_fall", body=(0, 0), arm="arm_raise_back", arm_at=(0, -3),
              tail=t("tail_high", "tail_rest"), tail_at=(0, -3), stage=stage),
        frame(legs="legs_land", legs_at=(-1, 2), body=(0, 2), head="head_down", head_at=(0, -1),
              arm="arm_down", tail=t("tail_lift", "tail_rest"), stage=stage),
    ]
    # Rise and fall frames hold while the game moves the hero; the strip times are for
    # previewing one jump in place.
    return Anim("jump", f, [90, 70, 140, 160, 160, 120], loop=False)


def attack(stage="final", secondary=True) -> Anim:
    t = (lambda a, b: a if secondary else b)
    f = [
        frame(legs="legs_idle", body=(-1, 0), arm="arm_raise_back", arm_at=(-3, -4),
              sword="sword_back", sword_at=(-12, -12), sword_back=True, tail=t("tail_rest", "tail_rest"),
              stage=stage),
        frame(legs="legs_lunge", legs_at=(0, 1), body=(1, 1), torso="torso_lean",
              arm="arm_reach", tail=t("tail_lift", "tail_rest"), smear_at=(14, 4), stage=stage),
        frame(legs="legs_lunge", legs_at=(0, 1), body=(1, 1), torso="torso_lean",
              arm="arm_reach", sword="sword_fwd", sword_at=(5, -1),
              tail=t("tail_flow", "tail_rest"), stage=stage),
        frame(legs="legs_lunge", legs_at=(0, 1), body=(1, 1), torso="torso_lean",
              arm="arm_reach", sword="sword_fwd", sword_at=(5, -1),
              tail=t("tail_lift", "tail_rest"), stage=stage),
        frame(legs="legs_idle", body=(0, 0), arm="arm_fwd", sword="sword_fwd", sword_at=(4, 3),
              tail=t("tail_sway", "tail_rest"), stage=stage),
    ]
    return Anim("attack", f, [120, 50, 60, 120, 140], loop=False)


def hurt(stage="final", secondary=True) -> Anim:
    t = (lambda a, b: a if secondary else b)
    kw = dict(legs="legs_idle", legs_at=(-1, 0), body=(-2, 0), head="head_hurt",
              head_at=(-1, 0), arm="arm_raise_back", arm_at=(-2, -3), stage=stage)
    f = [frame(tail=t("tail_flow", "tail_rest"), flash=True, **kw),
         frame(tail=t("tail_flow", "tail_rest"), **kw),
         frame(tail=t("tail_lift", "tail_rest"), **kw)]
    return Anim("hurt", f, [60, 120, 160], loop=False)


ANIMS = ["idle", "walk", "run", "jump", "attack", "hurt"]


def all_anims(stage="final", secondary=True) -> list:
    g = globals()
    return [g[n](stage) if n == "idle" else g[n](stage, secondary) for n in ANIMS]


def silhouette_options() -> list:
    """ch03 exploration: four silhouettes, (name, image). 'plain' is the beginner lump
    (no gaps, nothing sticking out); 'hat' and 'cloak' are readable but generic; the last
    one is the keeper: hair tuft, scarf tail, and clear gaps at arm and legs."""
    from PIL import ImageDraw
    plain = frame(tail=None, stage="silhouette")
    px = plain.load()
    for y in range(16, 31):  # arms glued to the body, no gap between the legs: a lump
        xs = [x for x in range(W) if px[x, y][3]]
        for x in range(min(xs), max(xs) + 1) if xs else ():
            px[x, y] = rgba("K")
    hat = frame(tail=None, stage="silhouette")
    d = ImageDraw.Draw(hat)
    d.rectangle([7, 9, 24, 10], fill=rgba("K"))
    d.rectangle([11, 3, 20, 8], fill=rgba("K"))
    cloak = frame(tail=None, stage="silhouette")
    d = ImageDraw.Draw(cloak)
    d.polygon([(10, 17), (21, 17), (24, 29), (7, 29)], fill=rgba("K"))
    keeper = frame(tail="tail_high", stage="silhouette")
    return [("plain", plain), ("hat", hat), ("cloak", cloak), ("scarf", keeper)]
