"""Ch. 5 figures: the NES palette, sub-palettes, per-area palettes, palette swaps."""
from _v import *

# 1. the master palette, hardware layout, with $xx labels
cells = []
for r in range(4):
    for c in range(16):
        i = r * 16 + c
        chip = Image.new("RGBA", (40, 30), nes(i))
        d = ImageDraw.Draw(chip)
        if i in (0x0D, 0x0E, 0x1D, 0x1E, 0x1F, 0x2E, 0x2F, 0x3E, 0x3F):
            d.line([(2, 2), (37, 27)], fill=(200, 60, 60), width=2)
        lum_ = luma(nes(i))
        draw_text(chip, 3, 8, "$%02X" % i, 12, (0, 0, 0) if lum_ > 120 else (230, 230, 230))
        cells.append(chip)
pal_img = grid_layout(cells, 16, gap=2)
save(figure(pal_img, "The NES master palette ($00-$3F, hardware order)",
            "Columns are hues, rows are brightness. Crossed cells are duplicates of black - or $0D, "
            "which can upset real TVs: never use it. Rendering: Lospec \"Nintendo Entertainment System\"."),
     "ch05-nes-palette.png")

# 2. all area palettes
rows_ = []
for a in ORDER:
    A = AREAS[a]
    bgc = row([label(sub_chips(s, 22, labels=False), "BG%d" % i, 12, FIG_DIM) for i, s in enumerate(A["bg"])], 10)
    spc = row([label(sub_chips(s, 22, labels=False, sprite=True), "SP%d" % i, 12, FIG_DIM)
               for i, s in enumerate(A["spr"])], 10)
    rows_.append(row([label(Image.new("RGBA", (120, 1), FIG_BG + (255,)), A["name"], 16, FIG_FG, top=True),
                      bgc, spc], 24, align="center"))
save(figure(column(rows_, 14, center=False), "One palette set per area: 4 background + 4 sprite sub-palettes",
            "Slot 0 is the shared backdrop ($0F black) for backgrounds and 'transparent' for sprites. "
            "SP0 (Kit) never changes, so the hero looks the same everywhere."), "ch05-area-palettes.png")

# 3. shared dark slot: the back wall looks identical under every BG sub-palette
wall = gpaste(T.back_wall(part=0), T.vine(2), 0, 0)
same = [nv(render(T.back_wall(part=0), s, backdrop=True), 5) for s in GH["bg"]]
diff_pals = [(0x0F, 0x0C, 0x1C, 0x2B), (0x0F, 0x0A, 0x1A, 0x2A), (0x0F, 0x00, 0x00, 0x10), (0x0F, 0x07, 0x17, 0x38)]
diff = [nv(render(T.back_wall(part=0), s, backdrop=True), 5) for s in diff_pals]
save(figure(column([label(row(same, 6), "Better: slot 1 = $0C in all four -> the wall never changes",
                          14, FIG_GOOD),
                    label(row(diff, 6), "Avoid: a different dark per sub-palette -> the wall shifts colour",
                          14, FIG_BAD)], 16),
            "The shared-dark trick: one dark colour in every background sub-palette",
            "Each 16 x 16 area picks one sub-palette. If they all share slots 0 and 1, the dark "
            "back wall can sit behind anything."), "ch05-shared-dark.png")

# 4. Kit on all four areas (same SP0)
items = []
for a in ORDER:
    img, _ = world.background(a, with_hud=False)
    act = [x for x in world.ROOMS[a]["actors"] if x[0] == "kit"][0]
    _, _, x, y, _ = act
    if a == "ridge":
        x, y = 12, 152  # stand on the left ledge (the scene has Kit mid-jump)
    cx, cy = max(0, min(256 - 96, x - 36)), max(0, min(240 - 64, y - 30))
    c = img.crop((cx, cy, cx + 96, cy + 64)).copy()
    c.alpha_composite(kitimg(), (x - cx, y - cy))
    items.append((nv(c, 3), AREAS[a]["name"]))
save(panel(items, title="One hero palette that works on every area",
           note="SP0 = $0F/$16/$37 everywhere. Only the Furnace shares Kit's red, so there the black outline and cream carry the read."),
     "ch05-kit-areas.png")

# 5. palette swaps: one hopper, four palettes
swaps = [((0x0F, 0x0F, 0x14, 0x34), "$14/$34"), ((0x0F, 0x0F, 0x19, 0x39), "$19/$39"),
         ((0x0F, 0x0F, 0x16, 0x27), "$16/$27"), ((0x0F, 0x0F, 0x00, 0x10), "$00/$10")]
items = [(nv(creatures.frames("hopper", "idle", s)[0][0], 6), t) for s, t in swaps]
save(panel(items, title="Palette swap: one set of tiles, four enemies",
           note="On the NES a palette swap costs no tile memory - a classic way to make 'stronger' variants."),
     "ch05-palette-swap.png")

# 6. hue-shifted ramp vs straight ramp on the ground tile
gt = T.ground(T.E | T.W | T.S, 1)
straight = (0x0F, 0x0C, 0x1C, 0x2C)
shifted = GH["bg"][0]
save(compare(row([nv(render(gt, straight, True), 6), sub_chips(straight)], 10, align="center"),
             row([nv(render(gt, shifted, True), 6), sub_chips(shifted)], 10, align="center"),
             "Straight ramp: one hue column", "Hue-shifted: top step leans to green ($2B)",
             title="Ramps: one row darker (-$10) for shadow, a column sideways for warmth"),
     "ch05-ramps.png")
