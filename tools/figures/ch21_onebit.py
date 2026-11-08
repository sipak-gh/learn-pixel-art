"""Ch. 21 figures: 1-bit style (two colours, design by mapping materials to patterns)."""
from _v import *
from styles import mono, common as C

D, L = mono.ONEBIT
SL_NES = C.slice_build()[0]
SL_NES.alpha_composite(kitimg(), (40, 152))
room_q = mono.onebit_room()
room_d = mono.onebit_room(dotted=True)
naive = C.naive_threshold(SL_NES, mono.ONEBIT)
CROP = (0, 32, 256, 208)


def kit_1bit(img):
    """Kit's NES colours -> ink/paper: outline + face opening ink, suit + eyes + lamp paper."""
    return remap(img, {nes(0x0F)[:3]: D, nes(0x16)[:3]: L, nes(0x37)[:3]: L})


def place(room, x=40, y=152, img=None):
    im = room.copy()
    im.alpha_composite(img if img is not None else mono.onebit_kit(), (x, y))
    return im.crop(CROP)


save(panel([(nv(SL_NES.crop(CROP), 2), "NES original"),
            (nv(naive.crop(CROP), 2), "naive: threshold by brightness"),
            (nv(place(room_q), 2), "designed: each material chosen")],
           title="Converting is not designing",
           note="A brightness threshold keeps only the lightest pixels: the walls and Kit "
                "(red is a dark value) vanish. The designed version decides per material: void = ink, solid = paper, "
                "mid-tones = one pattern."), "ch21-naive-vs-designed.png")

# material by material: the same three crops in NES colours and in both 1-bit mappings
SL_BARE = C.slice_build()[0]
CROPS = [("stone, moss rim, planter", (16, 144, 64, 192)),
         ("back wall, glass pane", (32, 16, 80, 64)),
         ("pod on a stone ledge", (96, 56, 144, 104))]
cells = []
for name, box in CROPS:
    cells += [label(nv(SL_BARE.crop(box), 4), "NES: " + name, 13, FIG_FG),
              label(nv(room_q.crop(box), 4), "quiet mapping", 13, FIG_FG),
              label(nv(room_d.crop(box), 4), "dotted mapping", 13, FIG_FG)]
save(figure(grid_layout(cells, 3, 16),
            "Every slot gets a job",
            "Quiet: slot 0 ink, slot 1 ink, slot 2 checker, slot 3 paper. Dotted back wall: slot 1 "
            "becomes 1-in-3 dots and slot 2 paper. Stone always keeps the quiet mapping."),
     "ch21-mapping.png")

save(panel([(nv(place(room_q), 3), "quiet back wall (wall lines dropped)"),
            (nv(place(room_d), 3), "dotted back wall (lines as 1-in-3 dots)")],
           title="How loud is the background?",
           note="With two colours, every background mark competes with the hero. "
                "Keep backgrounds sparse or broken (dots), keep solids solid."), "ch21-quiet-vs-dotted.png")

# pattern library: 8 fills on 16x16 swatches
PATS = [
    ("ink", lambda x, y: 0), ("paper", lambda x, y: 1),
    ("checker 50%", lambda x, y: (x + y) % 2 == 0),
    ("dots 25%", lambda x, y: x % 2 == 0 and y % 2 == 0),
    ("dots 12%", lambda x, y: y % 2 == 0 and (x + 2 * (y // 2 % 2)) % 4 == 0),
    ("h-lines", lambda x, y: y % 2 == 0),
    ("v-lines", lambda x, y: x % 2 == 0),
    ("diagonal", lambda x, y: (x + y) % 4 == 0),
    ("bricks", lambda x, y: y % 4 == 3 or (x + (4 if (y // 4) % 2 else 0)) % 8 == 0),
    ("grass top", lambda x, y: y == 0 or (y == 1 and x % 3 != 1) or (y == 2 and x % 3 == 0)),
]


def swatch(f, n=16):
    im = Image.new("RGBA", (n, n))
    px = im.load()
    for y in range(n):
        for x in range(n):
            px[x, y] = (L if f(x, y) else D) + (255,)
    return im


items = [(label(view(swatch(f), 6, grid=False, bg=FIG_BG), name, 13, FIG_FG)) for name, f in PATS]
save(figure(grid_layout(items, 5, 14), "A 1-bit pattern library",
            "Patterns are your 'colours'. Use few, reuse them, and give each a job "
            "(checker = mid-tone surface, dots = distance/air, lines = metal)."), "ch21-patterns.png")

k_nes = kitimg()
k_l = kit_1bit(k_nes)   # paper suit, ink outline + eyes
k_s = Image.new("RGBA", k_l.size)
k_s.paste(Image.new("RGBA", k_l.size, L + (255,)), mask=k_l.split()[3])  # pure silhouette
bg_dark = Image.new("RGBA", (40, 32), D + (255,))
bg_check = swatch(lambda x, y: (x + y) % 2 == 0, 40).crop((0, 0, 40, 32))


def on(bg, spr):
    im = bg.copy()
    im.alpha_composite(spr, (8, 4))
    return im


save(panel([(view(k_nes, 6, bg=SPR_BG), "NES Kit"),
            (view(on(bg_dark, k_s), 6, bg=FIG_BG), "pure silhouette"),
            (view(on(bg_dark, k_l), 6, bg=FIG_BG), "ink lines inside"),
            (view(on(bg_check, k_l), 6, bg=FIG_BG), "same, on a checker: lost")],
           title="Kit in two colours",
           note="Interior ink lines (hood edge, eye, belt) keep the read; any pattern behind "
                "the hero destroys it, so the hero stands on solid ink."), "ch21-kit.png")

foe_solid = C.map_grid(C.creature_grid("hopper"), {"1": D, "2": L, "3": L})
foe_pat = mono.onebit_foe("hopper")
pair = Image.new("RGBA", (72, 32), D + (255,))
pair.alpha_composite(k_l, (4, 4))
pair.alpha_composite(foe_solid, (44, 12))
pair2 = Image.new("RGBA", (72, 32), D + (255,))
pair2.alpha_composite(k_l, (4, 4))
pair2.alpha_composite(foe_pat, (44, 12))
save(compare(view(pair, 6, bg=FIG_BG), view(pair2, 6, bg=FIG_BG),
             "hero and enemy both solid", "enemy patterned",
             "Friend or foe at a glance",
             "In 1-bit you cannot colour-code danger, so code it with fill: the hero is "
             "solid paper, hazards are patterned."), "ch21-foe.png")


# walking scene gif
wf, wd = kit.frames("walk")


def draw(t):
    x = 24 + (t // 35) % 120
    i = (t // wd[0]) % len(wf)
    im = room_d.copy()
    im.alpha_composite(kit_1bit(wf[i]), (x, 152))
    return im.crop(CROP)


fr_, d_ = timeline(4200, 70, draw)
gif("ch21-scene.gif", fr_, d_, k=3)
