"""Ch. 11 figures: attack, hits, effects."""
from _v import *

af, ad = kit.frames("attack")
hf, hd = kit.frames("hurt")
save(figure(filmstrip(af, 6, ad, bg=SPR_BG), "Lantern swing: anticipation, strike, follow-through, recover",
            "1 wind-up (120 ms, leaning back) · 2 strike (60 ms - the fastest frame) · 3 reach (160 ms hold) "
            "· 4 recover."), "ch11-attack-strip.png")
save(figure(timing_chart(ad, ["wind-up", "hit", "hold", "recover"], scale=0.9),
            "Attack timing: slow-fast-hold", "The strike frame is the shortest; the hold after it sells the impact."),
     "ch11-timing.png")

SP = GH["spr"]
names = ["dust", "spark", "smear", "hit", "poof", "seed", "splash"]
items = []
for n in names:
    fr, du = fx.frames(n, SP[0] if n == "dust" else SP[2])
    items.append((filmstrip(fr, 5, None, bg=SPR_BG, numbers=False, gap=4),
                  "%s: %d f, %s ms" % (n, len(fr), "/".join(str(d) for d in du))))
save(panel(items, cols=2, gap=16, title="Effect sprites (SP2 yellow/white; dust uses Kit's SP0)",
           note="Effects are short (2-4 frames), bright, and drawn on 8 x 8 or 16 x 16 tiles."),
     "ch11-fx-sheet.png")

# attack gif: Kit swings, hopper gets hit then poofs
stage = floor_strip(cells=6, rows_=3)
hop = creatures.frames("hopper", "idle", SP[1])
smear, sd = fx.frames("smear", SP[2])
spark, spd = fx.frames("spark", SP[2])
hit, hd2 = fx.frames("hit", SP[2])
poof, pd = fx.frames("poof", SP[2])
idle0 = kit.frames("idle")[0][0]


def hw_boxes(img, x, y):
    """8x8 hardware sprites needed for an image drawn at (x, y): per 8-row band, as many
    sprites as its opaque pixels span (sprites can sit at any x)."""
    a = img.getchannel("A").load()
    out = []
    for by in range(0, img.height, 8):
        xs = [xx for yy in range(by, min(by + 8, img.height)) for xx in range(img.width) if a[xx, yy]]
        if xs:
            out += [(x + min(xs) + 8 * i, y + by, 8, 8) for i in range((max(xs) - min(xs) + 8) // 8)]
    return out


def scene(t, extra_spark=False):
    """The attack moment at time t; returns (image, hardware sprite boxes). extra_spark adds a
    thrown 8x8 spark in front of the lantern (used only by the budget figure's 'Avoid')."""
    t %= 2400
    im = stage.copy()
    objs = []

    def put(sp, x, y):
        im.alpha_composite(sp, (x, y))
        objs.extend(hw_boxes(sp, x, y))
    if t < 400:
        k = idle0
    elif t < 400 + sum(ad):
        k = anim_frames((af, ad), t - 400)
    else:
        k = idle0
    put(k, 16, 8)
    ts = t - 520
    if 0 <= ts < 120:
        put(smear[0 if ts < 60 else 1], 36, 14)
    th = t - 520
    if t < 520:
        put(anim_frames(hop, t), 52, 16)
    elif th < 200:
        f = hop[0][0]
        fl = f if (th // 40) % 2 else remap(f, {nes(0x14)[:3]: nes(0x30)[:3], nes(0x34)[:3]: nes(0x30)[:3]})
        put(fl, 52 + (2 if th < 100 else 3), 16)
        put(hit[0 if th < 60 else 1], 52, 18)
    elif th < 200 + sum(pd):
        put(anim_frames((poof, pd), th - 200), 52, 16)
    elif t > 2000:
        put(anim_frames(hop, t), 52, 16)
    if extra_spark and 0 <= ts < 120:
        put(spark[0 if ts < 60 else 1], 37, 18)
    return im, objs


def draw(t):
    return scene(t)[0]


print("max sprites on a line (attack gif):",
      max(max(scanline_counts(scene(t)[1], 48)) for t in range(0, 2400, 20)))


fr_, d_ = timeline(2400, 20, draw)
gif("ch11-attack.gif", fr_, d_, k=5)

# hurt flash
st2 = floor_strip(cells=3, rows_=3)


def draw2(t):
    t %= 1400
    if t < 640:
        k = hf[(t // 80) % 2]
        x = 16 - min(6, t // 60)
    else:
        k, x = idle0, 10
    return on_stage(st2, k, x, 8)


fr_, d_ = timeline(1400, 40, draw2)
gif("ch11-hurt.gif", fr_, d_, k=6)
save(figure(filmstrip(hf, 7, hd, bg=SPR_BG), "Hurt: alternate a flash frame (all cream) with the hurt pose",
            "80 ms each, repeated while Kit is knocked back. A palette trick on real hardware; a frame here."),
     "ch11-hurt-strip.png")
save(figure(filmstrip(poof, 7, pd, bg=SPR_BG), "Poof: expand, break up, vanish",
            "Four frames, each a little longer than the last. The last frame is mostly empty space."),
     "ch11-poof.png")


# sprite budget at the moment of impact: line-by-line sprite counts next to the scene
def budget_view(t, extra, K=5):
    im, objs = scene(t, extra)
    counts = scanline_counts(objs, im.height)
    big = nv(im, K)
    bar = Image.new("RGBA", (9 * 12 + 30, big.height), FIG_BG + (255,))
    d = ImageDraw.Draw(bar)
    for y, c in enumerate(counts):
        col = (230, 80, 80) if c > 8 else ((240, 200, 80) if c == 8 else (110, 200, 140))
        if c:
            d.rectangle([0, y * K, c * 12 - 2, y * K + K - 2], fill=col)
    d.line([(8 * 12 - 1, 0), (8 * 12 - 1, bar.height)], fill=(255, 255, 255, 160), width=1)
    draw_text(bar, 8 * 12 + 4, 2, "8", 12, FIG_FG)
    return row([big, bar], gap=6), max(counts)


bad, nb = budget_view(540, True)
good, ng = budget_view(540, False)
save(compare(bad, good, "Avoid: one more 8 x 8 spark - %d on a line" % nb,
             "Better: as shipped - busiest line = %d" % ng,
             title="Effects cost sprites: count them per scanline",
             note="Bars: hardware sprites on each line of the scene (8 x 8 each). Kit's strike pose is "
                  "3 sprites wide on these lines, smear 1, foe 2, hit burst 2: exactly 8."),
     "ch11-budget.png")
