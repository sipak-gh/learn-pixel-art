"""Ch. 4 figures: value, light direction, contrast."""
from _v import *


def _grey(img):
    out = img.copy().convert("RGBA")
    px = out.load()
    for y in range(out.height):
        for x in range(out.width):
            r, g, b, a = px[x, y]
            v = int(0.299 * r + 0.587 * g + 0.114 * b)
            px[x, y] = (v, v, v, a)
    return out


scene, _ = world.scene("greenhouse", 0)
save(panel([(nv(scene, 2), "colour"), (nv(_grey(scene), 2), "value only")],
           title="Value carries the read: the same screen in greys",
           note="Brightest: Kit's cream eyes and lantern, the moss rims. Darkest: the backdrop. Mid: everything else."),
     "ch04-value-study.png")

# Kit values
k0 = kitimg()
save(panel([(nv(k0, 8), "Kit"), (nv(_grey(k0), 8), "values"),
            (sub_chips(kit.PAL, sprite=True), "SP0: transp., $0F, $16, $37")],
           title="Kit's three colours are three clearly separate values"), "ch04-kit-values.png")

# light direction on a stone block
lit = render(T.ground(4, 0), GH["bg"][0], backdrop=True)  # exposed top/left/right? mask S only
flat = render([r.replace("3", "2").replace("1", "2") for r in T.ground(4, 0)], GH["bg"][0], backdrop=True)
save(panel([(nv(flat, 10), "flat: no light"), (nv(lit, 10), "lit from above: bright rim, dark base")],
           title="One light direction for the whole set (top, slightly left)"), "ch04-light-direction.png")

# foreground vs background values
lay = """
................
................
.....######.....
................
################
################
"""
img_good, _, _ = rooms.build(lay, "greenhouse")
bright_wall = img_good.copy()
pal = GH["bg"][0]
bright_wall = remap(bright_wall, {nes(0x0C)[:3]: nes(0x2C)[:3], nes(0x0F)[:3]: nes(0x1C)[:3]})
save(compare(nv(bright_wall.crop((32, 0, 224, 96)), 2), nv(img_good.crop((32, 0, 224, 96)), 2), "Avoid: wall as bright as the ground",
             "Better: dark back wall, bright walkable edges",
             title="Separate what you can stand on from what is behind"), "ch04-fg-bg.png")

# NES palette by value
rows_ = []
for r in range(4):
    chips = [nes(r * 16 + i) for i in range(13)]
    rows_.append(row([Image.new("RGBA", (24, 24), c) for c in chips], 2))
rows_g = [row([Image.new("RGBA", (24, 24), (int(luma(nes(r * 16 + i))),) * 3 + (255,))
               for i in range(13)], 2) for r in range(4)]
save(panel([(column(rows_, 2), "$00-$3C (hardware layout)"), (column(rows_g, 2), "as values")],
           title="NES colours come in four brightness rows",
           note="Moving down one row ($x0 -> $x0 + $10) is a value step - the basis of NES shading ramps."),
     "ch04-nes-values.png")

# squint test: blur both versions of the fg/bg study (what survives when you narrow your eyes)
from PIL import ImageFilter


def _squint(img):
    flat = Image.new("RGBA", img.size, (0, 0, 0, 255))
    flat.alpha_composite(img)
    return flat.filter(ImageFilter.GaussianBlur(2.5))


bad_c, good_c = bright_wall.crop((32, 0, 224, 96)), img_good.crop((32, 0, 224, 96))
save(compare(column([nv(bad_c, 2), nv(_squint(bad_c), 2)], 8),
             column([nv(good_c, 2), nv(_squint(good_c), 2)], 8),
             "Avoid: squinted, wall and ground melt together",
             "Better: squinted, the walkable band still stands out",
             title="Squint test: blur away the detail and look at what is left"), "ch04-squint.png")
