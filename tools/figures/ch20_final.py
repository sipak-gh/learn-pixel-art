"""Ch. 20 figures: final scenes, sheets, budgets, export."""
from _v import *
import json

for a in ORDER:
    fr_, d_ = world.gif_frames(a, 2400, 100)
    gif("ch20-%s.gif" % a, fr_, d_, k=2)

# Kit sprite sheet (24x24 cells, one row per animation)
rows_ = []
for name in kit.ANIMS:
    fr, du = kit.frames(name)
    rows_.append(fr)
cols = max(len(r) for r in rows_)
sheet_img = Image.new("RGBA", (cols * 24, len(rows_) * 24), (0, 0, 0, 0))
for j, fr in enumerate(rows_):
    for i, f in enumerate(fr):
        sheet_img.alpha_composite(f, (i * 24, j * 24))
labels = Image.new("RGBA", (70, sheet_img.height * 5), FIG_BG + (255,))
for j, name in enumerate(kit.ANIMS):
    draw_text(labels, 0, j * 120 + 50, name, 15, FIG_FG)
save(figure(row([labels, view(sheet_img, 5, bg=SPR_BG, major=24)], 6),
            "Kit's sprite sheet: 24 x 24 cells, one row per animation",
            "%d frames. Exported with a JSON file of frame rectangles and durations." % sum(len(r) for r in rows_)),
     "ch20-kit-sheet.png")

# CHR budgets per area
items = []
for a in ORDER:
    img, attrs, grids = room_grids(a)
    t = chr_tiles(grids)
    items.append((chr_view(t, k=2, rows_min=16), "%s: %d / 256" % (AREAS[a]["name"], len(t))))
save(panel(items, cols=2, gap=16, title="Background pattern tables, one per area",
           note="Each screen's unique background tiles in CHR form. All fit in one 256-tile table."),
     "ch20-chr.png")

# scanline graph for each area
items = []
for a in ORDER:
    img, objs = world.scene(a, 0)
    items.append((row([nv(img, 1), scanline_graph(objs, 240, 2)], 6), "%s: max %d sprites on a line"
                  % (AREAS[a]["name"], max(scanline_counts(objs)))))
save(panel(items, cols=2, gap=16, title="Sprites per scanline (limit 8)",
           note="HUD hearts + seed icon = 5 on the HUD lines. Keep enemies on different heights to stay under 8."),
     "ch20-scanlines.png")

img = world.scene("greenhouse", 0)[0]
save(panel([(nv(img, 1), "1x  256 x 240 (source)"), (nv(img, 2), "2x  512 x 480"),
            (nv(img.crop((0, 0, 128, 120)), 4), "4x (crop)")], gap=16,
           title="Export: keep a 1x master, scale by whole numbers",
           note="Use the largest whole number that fits: 4x (1024 x 960) on a 1080p screen, 6x (1536 x 1440) on 1440p. Never 2.5x."),
     "ch20-export.png")

# Engine export: the metatile tileset with tile ids, and the map rebuilt from the .tmj data
import build_project as BP


def pixdiff(a, b):
    A, B = a.convert("RGB").tobytes(), b.convert("RGB").tobytes()
    return sum(1 for i in range(0, len(A), 3) if A[i:i + 3] != B[i:i + 3])


img, attrs, grids = room_grids("greenhouse")
ts, tmj, nmeta = BP.metatile_export("greenhouse", grids, attrs, img)
k = 3
ts_big = view(ts, k, bg=BLACK, major=16, major_color=(90, 90, 140, 255))
for i in range(nmeta):
    x, y = (i % 16) * 16 * k, (i // 16) * 16 * k
    rect(ts_big, x + 1, y + 1, 17 if i > 9 else 10, 13, (0, 0, 0, 200))
    draw_text(ts_big, x + 2, y + 1, str(i), 11, (255, 236, 140))
data = tmj["layers"][0]["data"]
rebuilt = Image.new("RGBA", (256, 240), (0, 0, 0, 255))
for n, gid in enumerate(data):
    tid = gid - tmj["tilesets"][0]["firstgid"]
    sx, sy = (tid % 16) * 16, (tid // 16) * 16
    rebuilt.alpha_composite(ts.crop((sx, sy, sx + 16, sy + 16)), ((n % 16) * 16, (n // 16) * 16))
diff = pixdiff(rebuilt, img)
save(panel([(ts_big, "greenhouse-metatiles.png: %d metatiles, tile ids 0-%d" % (nmeta, nmeta - 1)),
            (nv(rebuilt, 2), "rebuilt from greenhouse.tmj: %d pixels differ" % diff)], gap=24,
           title="Engine export: one metatile tileset + a Tiled map of 16 x 15 cells",
           note="The .tmj stores gid = tile id + 1 per cell (0 = empty). Same pattern under two sub-palettes = two metatiles."),
     "ch20-engine-export.png")

# Hardware export: decode the three binary files back into the screen
chr_b = BP.chr_bytes(chr_tiles(grids))
nt, ab = BP.nametable(grids, attrs, chr_tiles(grids))
nam_b = bytes(v for rw in nt for v in rw) + bytes(ab)
pal_b = BP.palette_ram("greenhouse")
dec = Image.new("RGBA", (256, 240))
px = dec.load()
for ty in range(30):
    for tx in range(32):
        t = nam_b[ty * 32 + tx]
        sub = (nam_b[960 + (ty // 4) * 8 + tx // 4] >> (((ty // 2) % 2) * 4 + ((tx // 2) % 2) * 2)) & 3
        for yy in range(8):
            lo, hi = chr_b[t * 16 + yy], chr_b[t * 16 + 8 + yy]
            for xx in range(8):
                c = (lo >> (7 - xx)) & 1 | ((hi >> (7 - xx)) & 1) << 1
                px[tx * 8 + xx, ty * 8 + yy] = nes(pal_b[0] if c == 0 else pal_b[sub * 4 + c])
diff = pixdiff(dec, img)
chr_img = Image.new("RGBA", (128, 128), (0, 0, 0, 255))
cp = chr_img.load()
for t in range(256):
    for yy in range(8):
        lo, hi = chr_b[t * 16 + yy], chr_b[t * 16 + 8 + yy]
        for xx in range(8):
            c = (lo >> (7 - xx)) & 1 | ((hi >> (7 - xx)) & 1) << 1
            cp[(t % 16) * 8 + xx, (t // 16) * 8 + yy] = GREYS4[c] + (255,)
chips = Image.new("RGBA", (4, 8))
for i, v in enumerate(pal_b):
    chips.putpixel((i % 4, i // 4), nes(v) if (i < 16 or i % 4) else (0, 0, 0, 0))
pal_big = view(chips, 20, bg=None, major=1, major_color=(40, 40, 50, 255))
pal_lab = Image.new("RGBA", (64, pal_big.height), FIG_BG + (255,))
for j, nm in enumerate(["BG0", "BG1", "BG2", "BG3", "SP0", "SP1", "SP2", "SP3"]):
    draw_text(pal_lab, 4, j * 20 + 2, nm, 13, FIG_DIM)
nam_view = Image.new("RGBA", (32, 30))
for ty in range(30):
    for tx in range(32):
        v = nam_b[ty * 32 + tx]
        nam_view.putpixel((tx, ty), (v, v, v, 255))
save(panel([(view(chr_img, 2, bg=BLACK, major=8, major_color=(70, 70, 110, 255)),
             "greenhouse-bg.chr\n4096 bytes = 256 tiles"),
            (view(nam_view, 6, bg=BLACK), "greenhouse.nam\n960 tile numbers (brighter = higher)\n+ 64 attribute bytes"),
            (row([pal_lab, pal_big], 0), "greenhouse.pal\n32 bytes ($3F00-$3F1F)"),
            (nv(dec, 1), "decoded from the 3 files\n%d pixels differ from greenhouse.png" % diff)], gap=20,
           title="Hardware export: three files describe one screen",
           note="CHR holds colour numbers 0-3 only; the nametable picks a tile per 8 x 8 cell; attributes pick a sub-palette per 16 x 16; palette RAM turns numbers into NES colours."),
     "ch20-hardware-export.png")
