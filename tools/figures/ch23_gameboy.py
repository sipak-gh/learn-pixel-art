"""Ch. 23 figures: Game Boy (DMG) style: 4 shades, 160x144, BGP/OBP0/OBP1, window HUD."""
from _v import *
from nes import gpaste, gblank
from styles import mono, common as C
from vault import hud as H

GBC = mono.GB
FLOOR_Y = 152  # Kit's top-left y on the slice floor


def gb_kit_img(grid):
    return C.map_grid(grid, mono.GB_KIT)


def with_kit(room, x=60, grid=None):
    im = room.copy()
    im.alpha_composite(gb_kit_img(grid or kit.kit()), (x, FLOOR_Y))
    return im


light, dark = mono.gb_room("light"), mono.gb_room("dark")
WIN = (8, 64, 168, 208)  # a 160x144 window over the slice

# palette chips
chips = []
for i, c in enumerate(GBC):
    sw = Image.new("RGBA", (64, 48), c + (255,))
    chips.append(label(view(sw, 1, grid=False, bg=FIG_BG), "shade %d  #%02x%02x%02x" % ((3 - i,) + c), 14, FIG_FG))
save(figure(row(chips, 10), "The four shades",
            "A popular rendering of the original green screen (Lospec 'Nintendo Gameboy (BGB)'), "
            "darkest to lightest. The hardware numbers shades 0 (lightest) to 3 (darkest)."), "ch23-palette.png")

# BGP: the same tile data, three palette registers
_g = C.slice_build()[2]
brick = next(_g[y][x] for y in range(len(_g)) for x in range(len(_g[0]))
             if len({c for r in _g[y][x] for c in r} & set("0123")) == 4)  # first 4-colour metatile
regs = [("BGP = %11100100 (normal)", {"0": GBC[3], "1": GBC[2], "2": GBC[1], "3": GBC[0]}),
        ("BGP = %00011011 (inverted)", {"0": GBC[0], "1": GBC[1], "2": GBC[2], "3": GBC[3]}),
        ("BGP = %11111001 (darker)", {"0": GBC[2], "1": GBC[1], "2": GBC[0], "3": GBC[0]})]
save(panel([(view(C.map_grid(brick, m), 8, grid=True, major=8, bg=FIG_BG), n) for n, m in regs],
           title="One palette register remaps the whole background",
           note="Tiles store colour numbers 0-3; the BGP register says which shade each number "
                "shows. Fades and flashes are just new BGP values."), "ch23-bgp.png")

# screen size: GB vs NES at the same scale
nes_screen = world.scene("greenhouse", 0)[0]
gb_scr = with_kit(light).crop(WIN)
save(panel([(nv(nes_screen, 2), "NES 256 x 240 (32 x 30 tiles)"),
            (view(gb_scr, 2, grid=False, bg=FIG_BG), "Game Boy 160 x 144 (20 x 18 tiles)")],
           title="A smaller window on the world",
           note="The GB screen is 37.5% of the NES frame (about 40% of its visible 256 x 224). Same 8x8 "
                "tiles and 16 x 24 hero, so the hero looks bigger and you see less around them."),
     "ch23-screen.png")

save(figure(tile_grid_view(gb_scr, 3), "160 x 144 = 20 x 18 tiles",
            "Thin lines: 8x8 tiles. Thick lines: 16x16 metatiles (an authoring habit; the GB "
            "itself has no attribute grid)."), "ch23-grid.png")

save(panel([(view(with_kit(dark).crop(WIN), 3, grid=False, bg=FIG_BG), "dark mode: shades copied slot for slot"),
            (view(with_kit(light).crop(WIN), 3, grid=False, bg=FIG_BG), "light mode: void light, solids dark")],
           title="Two ways to map the vault to four shades",
           note="Dark mode keeps the NES mood but the hero has only one shade to stand on. Light "
                "mode is the classic handheld look: a pale field, dark solids, dark hero."),
     "ch23-modes.png")

nes_slice = C.slice_build()[0]
nes_slice.alpha_composite(kitimg(), (60, FLOOR_Y))
naive = C.naive_threshold(nes_slice, GBC)
save(panel([(view(naive.crop(WIN), 3, grid=False, bg=FIG_BG), "naive: nearest shade by brightness"),
            (view(with_kit(light).crop(WIN), 3, grid=False, bg=FIG_BG), "designed: shade chosen per material")],
           title="Converting vs designing (again)",
           note="Brightness conversion flattens the back wall and the walls into the same shades and "
                "turns red Kit into a dark smudge on dark ground."), "ch23-naive.png")

# sprite palettes
k = gb_kit_img(kit.kit())
hop = C.map_grid(C.creature_grid("hopper"), mono.GB_FOE)
k_alt = C.map_grid(kit.kit(), mono.GB_FOE)


def sw(bg, *ims):
    im = Image.new("RGBA", (64, 32), bg + (255,))
    x = 4
    for s in ims:
        im.alpha_composite(s, (x, 32 - s.height - 2))
        x += s.width + 6
    return im


save(panel([(view(sw(GBC[3], k, hop), 6, grid=False, bg=FIG_BG), "on the pale field"),
            (view(sw(GBC[1], k, hop), 6, grid=False, bg=FIG_BG), "on a mid shade"),
            (view(sw(GBC[3], k_alt, hop), 6, grid=False, bg=FIG_BG), "Kit with OBP1 too")],
           title="OBP0 for the hero, OBP1 for everything else",
           note="Sprites get two palettes of 3 shades + transparent. Kit: darkest, dark, lightest; "
                "foes: darkest, light, lightest. Different mid-tones keep friend and foe apart."),
     "ch23-obp.png")

# window HUD: a 160x16 status bar drawn with the window layer
hud_g = gblank(160, 16, "0")
for i in range(4):
    hud_g = gpaste(hud_g, H.HEART if i < 3 else H.HEART_EMPTY, 4 + i * 9, 4)
hud_g = gpaste(hud_g, H.SEED, 48, 4)
hud_g = gpaste(hud_g, H.text_grid("x07"), 58, 4)
hud_g = gpaste(hud_g, H.LANTERN, 96, 4)
for i in range(6):
    for y in range(6, 11):
        for x in range(106 + i * 5, 110 + i * 5):
            hud_g[y] = hud_g[y][:x] + ("2" if i < 5 else "1") + hud_g[y][x + 1:]
hud_g = [r.replace(".", "0") for r in hud_g]
hud_g[0] = "3" * 160
HUD_MAP = {"0": GBC[0], "1": GBC[1], "2": GBC[2], "3": GBC[3]}
hud_im = C.map_grid(hud_g, HUD_MAP)

wf = kit.grids("walk")
wd = kit.ANIMS["walk"][1]
big = light.copy()


def gb_frame(t):
    u = (t // 30) % 240  # ping-pong along the floor, x 24..144
    back = u >= 120
    x = 24 + (240 - u if back else u)
    cam = max(0, min(light.width - 160, x + 8 - 72))
    im = big.copy()
    i = (t // wd[0]) % len(wf)
    spr = gb_kit_img(wf[i])
    if back:
        spr = spr.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
    im.alpha_composite(spr, (x, FLOOR_Y))
    scr = im.crop((cam, 64, cam + 160, 208))
    scr.alpha_composite(hud_im, (0, 128))
    return scr


save(panel([(view(gb_frame(600), 3, grid=False, bg=FIG_BG), "window layer pinned to the bottom 16 lines")],
           title="The window: a second, non-scrolling background",
           note="The DMG has one background, a 'window' layer drawn on top of it, and sprites. "
                "The window makes a fixed status bar without any raster tricks."), "ch23-window.png")

fr_, d_ = timeline(7200, 60, gb_frame)
gif("ch23-scene.gif", fr_, d_, k=3, bg=BLACK)
