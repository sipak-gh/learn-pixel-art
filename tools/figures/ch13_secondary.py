"""Ch. 13 figures: secondary motion and ambient life."""
from _v import *

tips = ["back", "flat", "up", "down"]
save(panel([(sv(kitimg(tip=t), 7, grid=False, major=None), "tip=%s" % t) for t in tips],
           title="The hood tail: one shape, four positions",
           note="It trails behind motion: flat when running, down while rising, up while falling."),
     "ch13-hood-tips.png")

# tail lags: run + jump strips with tail highlighted
rf, rd = kit.frames("run")
jf, jd = kit.frames("jump")


def mark_tail(im):
    out = im.copy()
    ov = Image.new("RGBA", im.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    d.rectangle([3, 1, 9, 11], outline=(80, 220, 255, 255))
    out.alpha_composite(ov)
    return out


save(figure(filmstrip([mark_tail(f) for f in jf], 6, jd, bg=SPR_BG),
            "Follow-through: the hood tail reacts one beat late",
            "Rise: tail drags down. Apex: settles back. Fall: flips up. Land: back to rest."),
     "ch13-tail-jump.png")

# ambient scenes (cropped): greenhouse spores, cistern drips
for a, box in (("greenhouse", (0, 32, 256, 240)), ("cistern", (0, 32, 256, 240))):
    fr_, d_ = timeline(2400, 100, lambda t, a=a: world.scene(a, t, with_hud=False)[0].crop(box))
    gif("ch13-ambient-%s.gif" % a, fr_, d_, k=2)

# animated tiles: water + molten
wsub = AREAS["cistern"]["bg"][1]
msub = AREAS["furnace"]["bg"][3]


def tiles_frame(f):
    gw = gblank(64, 32, "0")
    gm = gblank(64, 32, "0")
    for i in range(4):
        gw = gpaste(gpaste(gw, T.water(f), i * 16, 0), T.water(f, False), i * 16, 16)
        gm = gpaste(gm, T.molten(f), i * 16, 0)
        gm = gpaste(gm, T.molten(f, False), i * 16, 16)
    return row([render(gw, wsub, True), render(gm, msub, True)], 4, bg=(0, 0, 0))


gif("ch13-tile-anim.gif", [tiles_frame(f) for f in range(4)], [200] * 4, k=4)

# palette cycling: the furnace's molten glow rotates slot 2/3 colours instead of redrawing tiles
furn, _ = world.background("furnace", with_hud=False)
cyc = [(0x07, 0x16, 0x27, 0x38), (0x07, 0x17, 0x28, 0x38), (0x07, 0x27, 0x38, 0x30), (0x07, 0x17, 0x28, 0x38)]
base = AREAS["furnace"]["bg"][3]
frames_ = []
for c in cyc:
    m = {nes(base[1])[:3]: nes(c[0])[:3], nes(base[2])[:3]: nes(c[2])[:3], nes(base[3])[:3]: nes(c[3])[:3]}
    frames_.append(remap(furn.crop((0, 120, 256, 240)), {nes(base[2])[:3]: nes(c[2])[:3], nes(base[3])[:3]: nes(c[3])[:3]}))
gif("ch13-palette-cycle.gif", frames_, [160] * 4, k=2)
save(figure(row([sub_chips((0x0F,) + c[:1] + c[2:], 26) for c in cyc], 14),
            "Palette cycling: 4 palette states, zero new tiles",
            "Changing BG3's colours every 160 ms makes every glowing tile pulse at once (and anything else "
            "in BG3 - choose what shares the sub-palette)."), "ch13-palette-cycle.png")

# looping a scrolling tile: the shift per loop must equal the pattern repeat (16 px)
band = gcrop(T.water(0), 0, 0, 16, 8)
band = [r + r for r in band]  # two tiles wide


def rot(grid, n):
    return [r[n % len(r):] + r[:n % len(r)] for r in grid]


def loop_row(step, good):
    shifts = [step * f for f in range(4)] + [0]
    items = []
    for i, s in enumerate(shifts):
        d = ((s - shifts[i - 1]) + 8) % 16 - 8 if i else 0  # nearest step on a 16 px repeat
        cap = "frame 1" if i == 0 else ("frame 1 again: %+d px" % -d if i == 4 else
                                        "frame %d: %+d px" % (i + 1, -d))
        items.append(label(nv(render(rot(band, s), wsub, True), 5), cap, 14, FIG_DIM))
    text = ("Better: 4 px x 4 frames = 16 px, one pattern repeat" if good
            else "Avoid: 3 px x 4 frames = 12 px; the last step is 7 px, a lurch")
    return label(row(items, 10), text, 16, FIG_GOOD if good else FIG_BAD, top=True)


save(figure(column([loop_row(3, False), loop_row(4, True)], 18, center=False),
            "A flowing tile loops only if one loop moves exactly one pattern repeat",
            "Negative = the crests move left. With 4 px steps, frame 4 -> frame 1 is just another "
            "4 px step, so the water flows forever."), "ch13-loop-seam.png")
gif("ch13-loop-seam.gif",
    [column([render(rot(band, 3 * (f % 4)), wsub, True), render(rot(band, 4 * (f % 4)), wsub, True)],
            4, bg=(0, 0, 0)) for f in range(8)], [200] * 8, k=5)
