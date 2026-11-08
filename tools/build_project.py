"""Generate the course project snapshots.

project/ch01 .. project/ch20 : the `hollow-vault` asset pack (NES-style) as it stands at the
    end of each chapter. Chapter steps are applied in order to one dictionary of files, so later
    chapters overwrite (evolve) earlier art and everything else carries forward.
project/ch21 .. project/ch27 : one stand-alone folder per Part IV style mini-project.

    uv run --no-project --python 3.12 --with pillow==13.0.0 python tools/build_project.py [N ...]

Native assets are 1x. Enlarged copies (integer scale) and GIF previews go to preview/.
"""
from __future__ import annotations

import hashlib
import json
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "figures"))

from PIL import Image  # noqa: E402

import nes as N  # noqa: E402
from nes import nes, nhex, render  # noqa: E402
from pix import PROJECT, save_gif, up, write_palette_files  # noqa: E402
from vault import kit, creatures as CR, fx as FX, tiles as T, rooms, props as P, world, hud  # noqa: E402
from vault import bg as BGM  # noqa: E402
from vault.palettes import AREAS, ORDER  # noqa: E402
from _v import room_grids, chr_tiles  # noqa: E402

LAST_MAIN = 20
LAST = 27
GREYS4 = [(0, 0, 0, 255), (85, 85, 85, 255), (170, 170, 170, 255), (255, 255, 255, 255)]
SPR_BG = (40, 44, 60)  # preview backdrop for transparent sprites


# ---------------------------------------------------------------------------
# File records: ("png", img, preview_k) | ("gif", frames, durations, k, bg) | ("json", obj)
#               ("text", str) | ("bytes", b) | ("nespal",) | ("subpal", area) | ("e32pal",)
# ---------------------------------------------------------------------------
def png(img, k=None):
    return ("png", img, k)


def gif(frames, durations, k=4, bg=SPR_BG):
    return ("gif", frames, list(durations), k, bg)


def js(obj):
    return ("json", obj)


def strip(frames, cw=None, ch=None):
    cw = cw or max(f.width for f in frames)
    ch = ch or max(f.height for f in frames)
    im = Image.new("RGBA", (cw * len(frames), ch), (0, 0, 0, 0))
    for i, f in enumerate(frames):
        im.alpha_composite(f, (i * cw, 0))
    return im


def sheet_rows(rows_, cw, ch):
    cols = max(len(fr) for fr, _ in rows_.values())
    im = Image.new("RGBA", (cols * cw, len(rows_) * ch), (0, 0, 0, 0))
    for j, (fr, _) in enumerate(rows_.values()):
        for i, f in enumerate(fr):
            im.alpha_composite(f, (i * cw, j * ch))
    return im


def sheet_json(image, cw, ch, rows_, palette=None, anchor=None):
    """Engine-neutral sheet description: one row per animation."""
    d = {"image": image, "frameWidth": cw, "frameHeight": ch}
    if palette:
        d["palette"] = [nhex(i) for i in palette]
        d["paletteRGB"] = ["#%02x%02x%02x" % nes(i)[:3] for i in palette]
    if anchor:
        d["anchor"] = anchor
    d["animations"] = {n: {"row": j, "frames": len(fr), "durations": list(du), "loop": True}
                       for j, (n, (fr, du)) in enumerate(rows_.items())}
    return d


def anim_files(folder, name, frames, durs, cw=None, ch=None, palette=None, k=4):
    """name.png (strip) + name.json + preview/name.gif"""
    s = strip(frames, cw, ch)
    rows_ = {name: (frames, durs)}
    return {f"{folder}/{name}.png": png(s, k),
            f"{folder}/{name}.json": js(sheet_json(f"{name}.png", s.width // len(frames), s.height, rows_,
                                                  palette)),
            f"preview/{name}.gif": gif(frames, durs, k)}


# ---------------------------------------------------------------------------
# NES data helpers
# ---------------------------------------------------------------------------
def chr_image(tiles, cols=16, rows_min=16):
    """Pattern table in 4 greys, 1x (128 px wide)."""
    rws = max(rows_min, (len(tiles) + cols - 1) // cols)
    im = Image.new("RGBA", (cols * 8, rws * 8), GREYS4[0])
    px = im.load()
    for i, t in enumerate(tiles):
        ox, oy = (i % cols) * 8, (i // cols) * 8
        for y, r in enumerate(t):
            for x, c in enumerate(r):
                px[ox + x, oy + y] = GREYS4[int(c)]
    return im


def chr_bytes(tiles, total=256):
    """NES 2bpp planar CHR: 16 bytes per tile (8 bytes plane 0, then 8 bytes plane 1)."""
    out = bytearray()
    for t in list(tiles) + [("0" * 8,) * 8] * (total - len(tiles)):
        lo = [sum(((int(c) & 1) << (7 - x)) for x, c in enumerate(r)) for r in t]
        hi = [sum((((int(c) >> 1) & 1) << (7 - x)) for x, c in enumerate(r)) for r in t]
        out += bytes(lo) + bytes(hi)
    return bytes(out)


def tile_key(gr, tx, ty):
    return tuple(r.replace(".", "0")[tx:tx + 8] for r in gr[ty:ty + 8])


def nametable(grids, attrs, tiles):
    """-> (32x30 tile indices, 64 attribute bytes). Background tiles cannot be flipped."""
    index = {t: i for i, t in enumerate(tiles)}
    nt = [[0] * 32 for _ in range(30)]
    for my, rw in enumerate(grids):
        for mx, gr in enumerate(rw):
            for ty in (0, 8):
                for tx in (0, 8):
                    nt[my * 2 + ty // 8][mx * 2 + tx // 8] = index[tile_key(gr, tx, ty)]
    ab = []
    for by in range(8):
        for bx in range(8):
            def a(dy, dx):
                y, x = by * 2 + dy, bx * 2 + dx
                return attrs[y][x] if y < len(attrs) else 0
            ab.append(a(0, 0) | a(0, 1) << 2 | a(1, 0) << 4 | a(1, 1) << 6)
    return nt, ab


def palette_ram(area):
    """32 bytes as written to $3F00-$3F1F (sprite slot 0 mirrors the backdrop)."""
    a = AREAS[area]
    return bytes([c for sp in a["bg"] for c in sp] +
                 [c if i else a["bg"][0][0] for sp in a["spr"] for i, c in enumerate(sp)])


def metatile_export(area, grids, attrs, img):
    """Unique (pattern, sub-palette) metatiles -> tileset image, Tiled map, metatile JSON."""
    keys, index, cells = [], {}, []
    for my, rw in enumerate(grids):
        crow = []
        for mx, gr in enumerate(rw):
            k = ("\n".join(gr), attrs[my][mx])
            if k not in index:
                index[k] = len(keys)
                keys.append((k, (mx, my)))
            crow.append(index[k])
        cells.append(crow)
    cols = 16
    rws = (len(keys) + cols - 1) // cols
    ts = Image.new("RGBA", (cols * 16, rws * 16), (0, 0, 0, 0))
    for i, (_, (mx, my)) in enumerate(keys):
        ts.alpha_composite(img.crop((mx * 16, my * 16, mx * 16 + 16, my * 16 + 16)), ((i % cols) * 16, (i // cols) * 16))
    tmj = {"type": "map", "version": "1.10", "tiledversion": "1.10.2", "orientation": "orthogonal",
           "renderorder": "right-down", "width": 16, "height": 15, "tilewidth": 16, "tileheight": 16,
           "infinite": False, "nextlayerid": 2, "nextobjectid": 1,
           "layers": [{"id": 1, "name": "background", "type": "tilelayer", "visible": True, "opacity": 1,
                       "x": 0, "y": 0, "width": 16, "height": 15,
                       "data": [c + 1 for rw in cells for c in rw]}],
           "tilesets": [{"firstgid": 1, "name": f"{area}-metatiles", "image": f"{area}-metatiles.png",
                         "imagewidth": ts.width, "imageheight": ts.height, "tilewidth": 16, "tileheight": 16,
                         "columns": cols, "tilecount": len(keys), "margin": 0, "spacing": 0}]}
    return ts, tmj, len(keys)


def subpal_chips(area):
    """8 rows x 4 px: BG0..BG3 then SP0..SP3, 1x."""
    a = AREAS[area]
    im = Image.new("RGBA", (4, 8))
    for j, sp in enumerate(a["bg"] + a["spr"]):
        for i, c in enumerate(sp):
            im.putpixel((i, j), nes(c) if (j < 4 or i) else (0, 0, 0, 0))
    return im


def kit_rows(names=None):
    return {n: kit.frames(n) for n in (names or kit.ANIMS)}


def creature_rows(kind, area="greenhouse"):
    sub = AREAS[area]["spr"][world.SPRITE_SUB[kind]]
    return {f"{kind}-{a}": CR.frames(kind, a, sub) for a in CR.CREATURES[kind][1]}


def fx_frames(name, area="greenhouse"):
    sp = AREAS[area]["spr"]
    return FX.frames(name, sp[0] if name == "dust" else sp[2])


def area_room(area, props=True):
    r = world.ROOMS[area]
    img, _, _ = rooms.build(r["layout"], area, props=r["props"] if props else (),
                                    bands=r.get("bands", ()))
    return img


def silhouette(img, c=(255, 255, 255, 255)):
    out = Image.new("RGBA", img.size, (0, 0, 0, 0))
    px, src = out.load(), img.load()
    for y in range(img.height):
        for x in range(img.width):
            if src[x, y][3]:
                px[x, y] = c
    return out


def greys(img):
    out = img.copy()
    px = out.load()
    for y in range(out.height):
        for x in range(out.width):
            r, g, b, a = px[x, y]
            if a:
                v = int(round(0.299 * r + 0.587 * g + 0.114 * b))
                px[x, y] = (v, v, v, a)
    return out


# ---------------------------------------------------------------------------
# Main project steps (cumulative). Each returns (history lines, {relpath: record}, removed)
# ---------------------------------------------------------------------------
def screen_template():
    im = Image.new("RGBA", (256, 240), nes(0x0F))
    px = im.load()
    for y in range(240):
        for x in range(256):
            if y < 8 or y >= 232:
                px[x, y] = (60, 20, 30, 255)            # overscan: may be hidden on a TV
            elif x % 16 == 0 or y % 16 == 0:
                px[x, y] = (52, 52, 72, 255)           # metatile / attribute grid
            elif x % 8 == 0 or y % 8 == 0:
                px[x, y] = (30, 30, 42, 255)           # 8x8 tile grid
    return im


def sprite_template():
    im = Image.new("RGBA", (24, 24), (0, 0, 0, 0))
    px = im.load()
    for y in range(24):
        for x in range(24):
            if 4 <= x < 20:
                px[x, y] = (52, 52, 72, 255) if ((x - 4) // 8 + y // 8) % 2 else (40, 40, 56, 255)
    return im


SPEC = """# hollow-vault: the spec

| Item | Value |
|---|---|
| Screen | 256 x 240 (keep key art inside 256 x 224) |
| Tiles | 8 x 8, 4 colours each (2 bits per pixel) |
| Metatiles / attribute areas | 16 x 16; one screen = 16 x 15 metatiles |
| Palette | NES master palette, Lospec "Nintendo Entertainment System" rendering |
| Backdrop | $0F black, shared by all background sub-palettes |
| BG sub-palettes | 4 per area: backdrop + 3 colours |
| Sprite sub-palettes | 4 per area: transparent + 3 colours |
| Kit | 16 x 24 = 2 x 3 sprites of 8 x 8, drawn in a 24 x 24 cell |
| Enemies | 16 x 16 = 2 x 2 sprites |
| Limits | 8 sprites per scanline, 64 on screen, 256 BG tiles + 256 sprite tiles per pattern table |
| Display | integer scale only: x3 = 768 x 720, x4 = 1024 x 960 |

Never use $0D. Relaxations: square pixels; scroll splits are described, not coded.
"""


def ch01():
    return (["Set up the NES palette files, the screen template and the spec sheet."],
            {"palette/nes": ("nespal",), "templates/screen-256x240.png": png(screen_template(), 3),
             "templates/sprite-24x24.png": png(sprite_template(), 8), "spec.md": ("text", SPEC)}, ())


def ch02():
    pod = render(P.POD, AREAS["greenhouse"]["bg"][1], backdrop=True)
    return (["Line and curve practice: the seed pod prop drawn with clean runs."],
            {"props/pod.png": png(pod, 8)}, ())


def ch03():
    poses = [kit.grids(a)[i] for a, i in (("idle", 0), ("walk", 0), ("run", 0), ("jump", 1),
                                          ("jump", 3), ("attack", 1), ("hurt", 0))]
    sils = [silhouette(kit.img(g)) for g in poses]
    return (["Kit's silhouette: the stand pose and six key poses as solid shapes."],
            {"concept/kit-silhouette.png": png(sils[0], 8),
             "concept/kit-pose-silhouettes.png": png(strip(sils), 4)}, ())


def ch04():
    return (["Value study of Kit (greys only) to check the read before colour."],
            {"concept/kit-values.png": png(greys(kit.img(kit.kit())), 8)}, ())


def ch05():
    flat = kit.img([r.replace("3", "2") for r in kit.kit()])
    return (["Greenhouse sub-palettes (BG0-3, SP0-3) and Kit blocked in with SP0."],
            {"palette/greenhouse.gpl": ("subpal", "greenhouse"),
             "palette/greenhouse-subpalettes.png": png(subpal_chips("greenhouse"), 16),
             "sprites/kit-stand.png": png(flat, 8)}, ())


def ch06():
    gh = AREAS["greenhouse"]
    ground = render(T.ground(T.E | T.W | T.S, 1), gh["bg"][0], True)
    crate, subs = P.PROPS["crate"]
    return (["Kit fully shaded (black, mid, light); first ground metatile and the crate prop."],
            {"sprites/kit-stand.png": png(kit.img(kit.kit()), 8),
             "tiles/ground-top.png": png(ground, 8),
             "props/crate.png": png(render(crate, gh["bg"][subs[0]], True), 8)}, ())


def ch07():
    gh = AREAS["greenhouse"]["bg"][0]
    wp = N.gblank(32, 32, "0")
    for p_ in range(4):
        wp = N.gpaste(wp, T.back_wall(part=p_), (p_ % 2) * 16, (p_ // 2) * 16)
    var = strip([render(T.ground(T.E | T.W | T.S, s), gh, True) for s in range(4)])
    return (["Textures: the quiet back-wall panel (4 metatiles) and four ground variants."],
            {"tiles/wall-panel.png": png(render(wp, gh, True), 6),
             "tiles/ground-variants.png": png(var, 6)}, ())


def ch08():
    f = kit_rows(["idle"])["idle"]
    h = CR.frames("hopper", "idle", AREAS["greenhouse"]["spr"][1])
    out = anim_files("sprites", "kit-idle", *f, cw=24, palette=kit.PAL)
    out.update(anim_files("enemies", "hopper-idle", *h, cw=16, palette=AREAS["greenhouse"]["spr"][1]))
    return (["Kit's idle (4 frames, held 500/400/120/400 ms) and the hopper's 2-frame idle."], out, ())


def ch09():
    out = {}
    for n in ("walk", "run"):
        out.update(anim_files("sprites", "kit-" + n, *kit.frames(n), cw=24, palette=kit.PAL))
    return (["Walk (4 frames) and run (4 frames, 90 ms) cycles."], out, ())


def ch10():
    out = anim_files("sprites", "kit-jump", *kit.frames("jump"), cw=24, palette=kit.PAL)
    out.update(anim_files("fx", "dust", *fx_frames("dust"), palette=AREAS["greenhouse"]["spr"][0]))
    return (["Jump/fall/land (5 frames) and the landing dust puff."], out, ())


def ch11():
    out = {}
    for n in ("attack", "hurt"):
        out.update(anim_files("sprites", "kit-" + n, *kit.frames(n), cw=24, palette=kit.PAL))
    for n in ("spark", "smear", "hit", "poof", "seed"):
        out.update(anim_files("fx", n, *fx_frames(n), palette=AREAS["greenhouse"]["spr"][2]))
    return (["Attack (lantern swing) and hurt; effects: spark, smear, hit, poof, and the seed pickup (2-frame shimmer)."], out, ())


def ch12():
    out = {}
    for kind in ("hopper", "slug", "drone"):
        rows_ = creature_rows(kind)
        s = sheet_rows(rows_, 16, 16)
        sub = AREAS["greenhouse"]["spr"][world.SPRITE_SUB[kind]]
        out[f"enemies/{kind}.png"] = png(s, 6)
        out[f"enemies/{kind}.json"] = js(sheet_json(f"{kind}.png", 16, 16, rows_, sub))
        for n, (fr, du) in rows_.items():
            out[f"preview/{n}.gif"] = gif(fr, du, 4)
    return (["Three creatures: spore hopper, drip slug, warden drone (sheets + JSON)."],
            out, ("enemies/hopper-idle.png", "enemies/hopper-idle.json", "preview/hopper-idle.gif"))


def ch13():
    cs = AREAS["cistern"]["bg"][1]
    fs = AREAS["furnace"]["bg"][3]
    water = [render(T.water(f), cs, True) for f in range(4)]
    molten = [render(T.molten(f), fs, True) for f in range(4)]
    out = {"tiles/water-anim.png": png(strip(water), 6), "preview/water-anim.gif": gif(water, [200] * 4, 6, (0, 0, 0)),
           "tiles/molten-anim.png": png(strip(molten), 6), "preview/molten-anim.gif": gif(molten, [200] * 4, 6, (0, 0, 0))}
    out.update(anim_files("fx", "splash", *fx_frames("splash", "cistern"), palette=AREAS["cistern"]["spr"][2]))
    return (["Secondary motion: animated water and molten tiles (4 frames, 200 ms) and the splash effect. "
             "Kit's files are unchanged: the hood-tip follow-through the chapter explains was already "
             "drawn into Kit's frames in Chapters 8-11."], out, ())


def ch14():
    img, attrs, grids = rooms.build(rooms.GREENHOUSE_TEST, "greenhouse")
    tiles = chr_tiles(grids)
    return ([f"The greenhouse test room cut into tiles: {len(tiles)} unique 8x8 tiles, attribute map."],
            {"rooms/test-room.png": png(img, 3), "tiles/greenhouse-chr.png": png(chr_image(tiles), 4),
             "rooms/test-room-attributes.json": js({"area": "greenhouse", "size": [16, len(attrs)],
                                                    "attributes": attrs})}, ())


def ch15():
    gh = AREAS["greenhouse"]["bg"]
    gset = Image.new("RGBA", (64, 64))
    for m in range(16):
        gset.alpha_composite(render(T.ground(m, 3), gh[0], True), ((m % 4) * 16, (m // 4) * 16))
    base = T.back_wall(part=0)
    ov = [render(N.gpaste(base, T.vine(s), 0, 0), gh[1], True) for s in (0, 2, 5)]
    ov += [render(N.gpaste(base, T.grass_tuft(s), 0, 0), gh[1], True) for s in (1, 4)]
    return (["The 16-metatile ground autotile set (index = N1+E2+S4+W8) and foliage overlays."],
            {"tiles/ground-set.png": png(gset, 6),
             "tiles/ground-set.json": js({"image": "ground-set.png", "tileSize": 16, "columns": 4,
                                          "index": "mask = N(1) + E(2) + S(4) + W(8): neighbours that are ground",
                                          "subPalette": "BG0"}),
             "tiles/overlays.png": png(strip(ov), 6)}, ())


def blockout(layout):
    lay = layout.strip("\n").split("\n")
    im = Image.new("RGBA", (16, len(lay)), (20, 20, 28, 255))
    for y, r in enumerate(lay):
        for x, c in enumerate(r):
            if c == "#":
                im.putpixel((x, y), (200, 200, 210, 255))
            elif c in "=-+_|":
                im.putpixel((x, y), (120, 160, 220, 255))
            elif c in "wWmM":
                im.putpixel((x, y), (60, 110, 200, 255))
    return im


def ch16():
    r = world.ROOMS["greenhouse"]
    return (["The greenhouse room: blockout (1 px per metatile) and the tiled room without props."],
            {"rooms/greenhouse-blockout.png": png(blockout(r["layout"]), 16),
             "rooms/greenhouse.png": png(area_room("greenhouse", props=False), 3)}, ())


def ch17():
    gh = AREAS["greenhouse"]
    out = {"rooms/greenhouse.png": png(area_room("greenhouse"), 3)}
    for name, (grid, subs) in P.PROPS.items():
        if name in ("pod", "crate"):
            continue
        out[f"props/{name}.png"] = png(render(grid, gh["bg"][subs[0]], True), 8)
    return (["Props (lamp, planter, fern, terminal, drawers, door, rubble) placed on the 16 x 16 grid."],
            out, ())


def ch18():
    R = AREAS["ridge"]["bg"]
    bands = BGM.band_images(R)
    frames = []
    for i in range(32):
        cam = i * 8
        im = Image.new("RGBA", (256, 176), nes(0x0F))
        for name, speed, y in (("sky", 0.125, 0), ("hills", 0.25, 64), ("towers", 0.5, 112)):
            b = bands[name]
            off = int(cam * speed) % 256
            im.paste(b.crop((off, 0, 256, b.height)), (0, y), b.crop((off, 0, 256, b.height)))
            if off:
                im.paste(b.crop((0, 0, off, b.height)), (256 - off, y), b.crop((0, 0, off, b.height)))
        frames.append(im)
    return (["Antenna Ridge background bands (sky, hills, towers) for 1/8, 1/4, 1/2 speed parallax."],
            {"bg/sky.png": png(bands["sky"], 2), "bg/hills.png": png(bands["hills"], 2),
             "bg/towers.png": png(bands["towers"], 2), "preview/parallax.gif": gif(frames, [80] * 32, 2, (0, 0, 0))},
            ())


def fade_sub(sub, steps):
    out = []
    for c in sub:
        for _ in range(steps):
            c = 0x0F if c < 0x10 or c == 0x0F else c - 0x10
        out.append(c)
    return tuple(out)


def ch19():
    out = {}
    for a in ORDER:
        out[f"palette/{a}.gpl"] = ("subpal", a)
        out[f"palette/{a}-subpalettes.png"] = png(subpal_chips(a), 16)
        out[f"rooms/{a}.png"] = png(area_room(a), 3)
    fades = {f"BG{n}": [[nhex(c) for c in fade_sub(sp, s)] for s in range(5)]
             for n, sp in enumerate(AREAS["greenhouse"]["bg"])}
    out["palette/greenhouse-fade.json"] = js({"note": "fade to black: subtract $10 per step; $0x colours become $0F",
                                             "steps": 5, "subPalettes": fades})
    return (["Palettes for all four areas; Cistern, Furnace and Ridge rooms; the 5-step fade."], out, ())


def ch20():
    out = {}
    for a in ORDER:
        img, attrs, grids = room_grids(a)
        tiles = chr_tiles(grids)
        nt, ab = nametable(grids, attrs, tiles)
        ts, tmj, nmeta = metatile_export(a, grids, attrs, img)
        out[f"export/{a}/{a}.png"] = png(img, 3)
        out[f"export/{a}/{a}-chr.png"] = png(chr_image(tiles), 4)
        out[f"export/{a}/{a}-bg.chr"] = ("bytes", chr_bytes(tiles))
        out[f"export/{a}/{a}.nam"] = ("bytes", bytes(v for rw in nt for v in rw) + bytes(ab))
        out[f"export/{a}/{a}.pal"] = ("bytes", palette_ram(a))
        out[f"export/{a}/{a}-metatiles.png"] = png(ts, 3)
        out[f"export/{a}/{a}.tmj"] = js(tmj)
        out[f"export/{a}/{a}.json"] = js({"area": AREAS[a]["name"], "uniqueTiles": len(tiles), "metatiles": nmeta,
                                          "bgSubPalettes": [[nhex(c) for c in s] for s in AREAS[a]["bg"]],
                                          "spriteSubPalettes": [[nhex(c) for c in s] for s in AREAS[a]["spr"]],
                                          "attributes": attrs, "nametable": nt})
        scn, objs = world.scene(a, 0)
        out[f"scene/{a}.png"] = png(scn, 3)
        fr, du = world.gif_frames(a, 2400, 100)
        out[f"preview/scene-{a}.gif"] = gif(fr, du, 2, (0, 0, 0))
    rows_ = kit_rows()
    out["export/kit-sheet.png"] = png(sheet_rows(rows_, 24, 24), 4)
    out["export/kit-sheet.json"] = js(sheet_json("kit-sheet.png", 24, 24, rows_, kit.PAL, anchor=[12, 24]))
    allc = {}
    for kind in ("hopper", "slug", "drone"):
        allc.update(creature_rows(kind))
    out["export/creatures-sheet.png"] = png(sheet_rows(allc, 16, 16), 4)
    out["export/creatures-sheet.json"] = js(sheet_json("creatures-sheet.png", 16, 16, allc))
    h = hud.hud_img(AREAS["greenhouse"]["bg"][3], **world.ROOMS["greenhouse"]["hud"])
    out["export/hud-bg.png"] = png(h, 3)
    return (["Final export: four finished areas (PNG, CHR, nametable, palette RAM, Tiled map), "
             "Kit and creature sheets with JSON, scene screenshots."], out, ())


# ---------------------------------------------------------------------------
# Part IV style folders (stand-alone)
# ---------------------------------------------------------------------------
def write_hex(colors):
    return ("text", "\n".join("%02x%02x%02x" % tuple(c[:3]) for c in colors) + "\n")


def write_gpl(name, colors):
    return ("text", f"GIMP Palette\nName: {name}\nColumns: {len(colors)}\n#\n" +
            "".join("%3d %3d %3d\tc%d\n" % (tuple(c[:3]) + (i,)) for i, c in enumerate(colors)))


def ch21():
    from styles import mono, common as C
    room_q, room_d = mono.onebit_room(), mono.onebit_room(dotted=True)
    kit_ = mono.onebit_kit()
    foe = mono.onebit_foe("hopper")
    walk = [C.map_grid(g, mono.ONEBIT_KIT) for g in kit.grids("walk")]
    return (["1-bit: ink #12101a + paper #ece4cc; quiet and dotted rooms, Kit, patterned foe."],
            {"palette/onebit.hex": write_hex(mono.ONEBIT), "palette/onebit.gpl": write_gpl("onebit", mono.ONEBIT),
             "rooms/greenhouse-quiet.png": png(room_q, 3), "rooms/greenhouse-dotted.png": png(room_d, 3),
             "sprites/kit.png": png(kit_, 8), "sprites/kit-walk.png": png(strip(walk, 24), 6),
             "preview/kit-walk.gif": gif(walk, kit.frames("walk")[1], 4, (90, 90, 110)),
             "enemies/hopper.png": png(foe, 8)}, ())


def ch22():
    from styles import dither as DI
    grey, ids = DI.render()
    out = {"palette/dither.hex": write_hex([DI.INK, DI.PAPER]),
           "scene/lighting-grey.png": png(DI.grey_image(grey), 3)}
    for m in ("threshold", "bayer4", "blue"):
        out[f"scene/{m}.png"] = png(DI.dither(grey, m), 3)
    out["scene/final.png"] = png(DI.outlines(DI.dither(grey, "bayer4"), ids, grey=grey), 3)
    return (["Dithered monochrome: a lit 3D-shaded room rendered to grey, then threshold / Bayer / "
             "blue-noise dithers and the outlined final."], out, ())


def ch23():
    from styles import mono, common as C
    gb = mono.GB
    walk = [C.map_grid(g, mono.GB_KIT) for g in kit.grids("walk")]
    return (["Game Boy: 4 shades (BGB palette), 160 x 144 screen, light and dark room modes, OBP0/OBP1."],
            {"palette/gameboy.hex": write_hex(gb), "palette/gameboy.gpl": write_gpl("gameboy (BGB)", gb),
             "rooms/greenhouse-light.png": png(mono.gb_room("light"), 3),
             "rooms/greenhouse-dark.png": png(mono.gb_room("dark"), 3),
             "scene/screen-160x144.png": png(mono.gb_screen("light"), 4),
             "sprites/kit.png": png(mono.gb_kit(), 8), "sprites/kit-walk.png": png(strip(walk, 24), 6),
             "preview/kit-walk.gif": gif(walk, kit.frames("walk")[1], 4, gb[3]),
             "enemies/hopper.png": png(mono.gb_foe("hopper"), 8)}, ())


def ch24():
    img, attrs, grids = room_grids("greenhouse")
    tiles = chr_tiles(grids)
    nt, ab = nametable(grids, attrs, tiles)
    spr = []
    seen = set()
    for g in sum((kit.grids(a) for a in kit.ANIMS), []):
        g = [r.replace(".", "0") for r in g]
        for ty in range(0, 24, 8):
            for tx in range(4, 20, 8):
                t = tuple(r[tx:tx + 8] for r in g[ty:ty + 8])
                if any(r != "0" * 8 for r in t) and t not in seen and tuple(r[::-1] for r in t) not in seen:
                    seen.add(t)
                    spr.append(t)
    banks = []
    cs = AREAS["cistern"]["bg"][1]
    for f in range(4):
        banks.append(render(T.water(f), cs, True))
    return (["Authentic NES data for the Greenhouse: CHR (2bpp planar), nametable + attribute bytes, "
             "palette RAM; Kit's sprite tiles; the 4 water CHR-bank frames."],
            {"chr/greenhouse-bg.chr": ("bytes", chr_bytes(tiles)), "chr/greenhouse-bg.png": png(chr_image(tiles), 4),
             "chr/kit.chr": ("bytes", chr_bytes(spr)), "chr/kit.png": png(chr_image(spr), 4),
             "nametable/greenhouse.nam": ("bytes", bytes(v for rw in nt for v in rw) + bytes(ab)),
             "nametable/greenhouse-attributes.txt": ("text", "\n".join(" ".join("$%02X" % ab[y * 8 + x] for x in range(8))
                                                                      for y in range(8)) + "\n"),
             "palette/greenhouse.pal": ("bytes", palette_ram("greenhouse")),
             "palette/nes": ("nespal",),
             "chr/water-banks.png": png(strip(banks), 6),
             "scene/greenhouse.png": png(img, 3)}, ())


def ch25():
    from styles import micro as M
    out = {"palette/greenhouse-micro.hex": write_hex([M.PAL[c] for c in "KdemlhRrC"]),
           "palette/cistern-micro.hex": write_hex([M.CISTERN[c] for c in "KdemlhRrC"]),
           "rooms/greenhouse-160x120.png": png(M.room(), 4), "rooms/cistern-160x120.png": png(M.room(M.CISTERN), 4),
           "sprites/kit.png": png(strip([M.kit(f) for f in ("stand", "step", "blink", "jump")], 5), 12)}
    hop = []
    for f in ("stand", "squash"):
        rows_ = M.HOPPER[f]
        im = Image.new("RGBA", (5, 4))
        for y, r in enumerate(rows_):
            for x, c in enumerate(r):
                if c != ".":
                    im.putpixel((x, y), M.PAL[c] + (255,))
        hop.append(im)
    out["enemies/hopper.png"] = png(strip(hop, 5), 12)
    fr = [M.scene(t) for t in range(0, 160 * 80, 160)]
    out["preview/scene.gif"] = gif(fr, [160] * len(fr), 4, (0, 0, 0))
    return (["Micro-res (ESA-like): 160 x 120 rooms in two 9-colour area palettes, 5 x 7 Kit, 5 x 4 hopper."],
            out, ())


def ch26():
    sys.path.insert(0, os.path.join(HERE, "art"))
    import hero
    import slime
    import scene as S
    run = hero.run()
    blob = slime.idle()
    return (["Hi-bit reference (the v1 mossy-ruins pack, condensed): ENDESGA 32, 32 x 32 Wren, slime, "
             "a 320 x 180 scene."],
            {"palette/endesga-32": ("e32pal",), "sprites/wren-stand.png": png(hero.stand(), 6),
             "sprites/wren-run.png": png(strip(run.frames), 4), "preview/wren-run.gif": gif(run.frames, run.durations, 4),
             "enemies/slime-idle.png": png(strip(blob.frames), 6),
             "scene/mossy-ruins.png": png(S.frame_at(0, 0), 3)}, ())


def ch27():
    from styles import iso as I
    blocks = strip([I.block(m) for m in ("stone", "metal", "moss")] + [I.crate()])
    kimg = kit.img(kit.kit())
    fr = [I.room(kit.frames("walk")[0][i % 4], (1.2 + 0.1 * i, 5.0)) for i in range(16)]
    return (["Isometric: 2:1 floor diamond (32 x 16), stone/metal/moss/crate blocks, the Greenhouse corner."],
            {"tiles/floor.png": png(I.floor_tile(), 8), "tiles/blocks.png": png(blocks, 6),
             "rooms/greenhouse-iso.png": png(I.room(kimg), 3),
             "preview/walk.gif": gif(fr, [120] * len(fr), 2, (0, 0, 0))}, ())


STEPS = [None, ch01, ch02, ch03, ch04, ch05, ch06, ch07, ch08, ch09, ch10, ch11, ch12, ch13, ch14,
         ch15, ch16, ch17, ch18, ch19, ch20, ch21, ch22, ch23, ch24, ch25, ch26, ch27]
STYLE_NAMES = {21: "1-bit", 22: "dithered monochrome", 23: "Game Boy", 24: "authentic NES",
               25: "micro-res (ESA-like)", 26: "hi-bit", 27: "isometric"}


# ---------------------------------------------------------------------------
# Writing
# ---------------------------------------------------------------------------
def write_file(root, rel, rec):
    path = os.path.join(root, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    kind = rec[0]
    if kind == "png":
        rec[1].save(path, optimize=True)
        if rec[2]:
            stem = os.path.splitext(os.path.basename(rel))[0]
            pv = os.path.join(root, "preview", f"{stem}-{rec[2]}x.png")
            os.makedirs(os.path.dirname(pv), exist_ok=True)
            up(rec[1], rec[2]).save(pv, optimize=True)
    elif kind == "gif":
        save_gif(rec[1], path, rec[2], rec[3], rec[4])
    elif kind == "json":
        with open(path, "w") as f:
            json.dump(rec[1], f, indent=1 if "nametable" in rec[1] else 2)
            f.write("\n")
    elif kind == "text":
        with open(path, "w") as f:
            f.write(rec[1])
    elif kind == "bytes":
        with open(path, "wb") as f:
            f.write(rec[1])
    elif kind == "nespal":
        N.write_nes_palette_files(os.path.dirname(path), os.path.basename(path))
    elif kind == "subpal":
        N.write_subpalettes(path, AREAS[rec[1]])
    elif kind == "e32pal":
        write_palette_files(os.path.dirname(path), os.path.basename(path))


def fingerprint(obj, h=None):
    top = h is None
    h = h or hashlib.sha256()
    if hasattr(obj, "tobytes") and hasattr(obj, "size"):
        h.update(f"img{obj.mode}{obj.size}".encode())
        h.update(obj.tobytes())
    elif isinstance(obj, (list, tuple)):
        h.update(f"seq{len(obj)}".encode())
        for o in obj:
            fingerprint(o, h)
    elif isinstance(obj, dict):
        h.update(f"map{len(obj)}".encode())
        for k in sorted(obj, key=str):
            h.update(str(k).encode())
            fingerprint(obj[k], h)
    else:
        h.update(repr(obj).encode())
    return h.hexdigest() if top else None


def listing(root):
    out = []
    for d, _, fs in os.walk(root):
        for f in fs:
            out.append(os.path.relpath(os.path.join(d, f), root))
    return sorted(out)


def report_lines(n):
    """Constraint reports for snapshots that contain finished screens."""
    lines = []
    if n == 14:
        img = rooms.build(rooms.GREENHOUSE_TEST, "greenhouse")[0]
        lines.append(N.report(img, AREAS["greenhouse"]["bg"], nes(0x0F), name="test-room"))
    if 16 <= n <= 19:
        for a in (ORDER if n == 19 else ["greenhouse"]):
            img = area_room(a, props=n >= 17)
            lines.append(N.report(img, AREAS[a]["bg"], nes(0x0F), name=a))
    if n == 20:
        for a in ORDER:
            scn, objs = world.scene(a, 0)
            img = room_grids(a)[0]
            loop_max = max(max(N.scanline_counts(world.scene(a, t)[1], 240)) for t in range(0, 2400, 100))
            lines.append(N.report(img, AREAS[a]["bg"], nes(0x0F), objects=objs, name=a) +
                         f" (frame 0; {loop_max} over the 2.4 s loop)"
                         f", CHR patterns (palette-free): {len(chr_tiles(room_grids(a)[2]))}/256")
    return lines


def readme(n, history, files, changed):
    if n > LAST_MAIN:
        title = f"# project/ch{n:02d}: style mini-project ({STYLE_NAMES[n]})"
        what = ("it holds the hi-bit reference pack (the v1 mossy-ruins art), set against "
                "hollow-vault in Chapter 26" if n == 26 else
                "it redraws a piece of the hollow-vault Greenhouse under this style's constraints")
        lines = [title, "", history[n][0], "",
                 f"This folder is stand-alone: {what}. It is not part of the cumulative main project.", ""]
    else:
        lines = [f"# project/ch{n:02d}: hollow-vault after Chapter {n}", "",
                 "The NES-style asset pack as it stands at the end of this chapter.", "",
                 "## This chapter", "", f"- {history[n][0]}", ""]
    rep = report_lines(n)
    if rep:
        lines += ["## Constraint report", "", "Produced by `tools/nes.py` (`report`):", ""]
        lines += [f"- {r}" for r in rep] + [""]
    lines += ["## Files", ""]
    if n <= LAST_MAIN:
        lines += ["Files marked * were added or changed in this chapter.", ""]
    for rel in sorted(files):
        lines.append(f"- `{rel}`" + (" *" if rel in changed and n <= LAST_MAIN else ""))
    lines += ["", "Native assets are 1x. `preview/` holds integer-scaled copies (`-4x` etc.) and GIF "
              "previews; never scale by non-integer factors.", ""]
    if 1 < n <= LAST_MAIN:
        lines += ["## Earlier chapters", ""]
        for k in range(n - 1, 0, -1):
            lines.append(f"- ch{k:02d}: " + history[k][0])
        lines.append("")
    return "\n".join(lines)


def emit(n, state, history, changed):
    root = os.path.join(PROJECT, f"ch{n:02d}")
    if os.path.isdir(root):
        shutil.rmtree(root)
    os.makedirs(root)
    for rel, rec in sorted(state.items()):
        write_file(root, rel, rec)
    files = listing(root)
    marked = set()
    for rel in files:
        stem = os.path.splitext(os.path.basename(rel))[0]
        for c in changed:
            cs = os.path.splitext(os.path.basename(c))[0]
            if rel == c or (rel.startswith("preview/") and (stem == cs or stem.rsplit("-", 1)[0] == cs)) \
                    or (state.get(c, ("",))[0] in ("nespal", "e32pal") and rel.startswith(os.path.dirname(c) + "/")
                        and os.path.basename(rel).startswith(os.path.basename(c))):
                marked.add(rel)
    with open(os.path.join(root, "README.md"), "w") as fh:
        fh.write(readme(n, history, files + ["README.md"], marked))
    print(f"wrote project/ch{n:02d} ({len(files) + 1} files)")


def build(targets):
    state, history, prints = {}, {}, {}
    main_targets = [t for t in targets if t <= LAST_MAIN]
    for n in range(1, max(main_targets, default=0) + 1):
        changes, files, removes = STEPS[n]()
        history[n] = changes
        changed = set()
        for rel, rec in files.items():
            fp = fingerprint(rec)
            if prints.get(rel) != fp:
                changed.add(rel)
            prints[rel] = fp
        state.update(files)
        for r in removes:
            state.pop(r, None)
            prints.pop(r, None)
        if n in targets:
            emit(n, state, history, changed)
    for n in sorted(t for t in targets if t > LAST_MAIN):
        changes, files, _ = STEPS[n]()
        history[n] = changes
        emit(n, dict(files), history, set())


if __name__ == "__main__":
    args = [int(a) for a in sys.argv[1:]] or list(range(1, LAST + 1))
    build(set(args))
