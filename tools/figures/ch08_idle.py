"""Ch. 8 figures: timing and the idle loop."""
import random
from _v import *

fr, du = kit.frames("idle")
stage = floor_strip(cells=3, rows_=3)
gif("ch08-idle.gif", [on_stage(stage, f, 12, 8) for f in fr], du, k=6)
save(figure(filmstrip(fr, 6, du, bg=SPR_BG), "Kit's idle: 4 frames, 1420 ms loop",
            "1 stand · 2 settle (body 1 px down, arm swings back) · 3 blink (120 ms) · 4 back up."),
     "ch08-idle-strip.png")
save(figure(timing_chart(du, ["stand", "settle", "blink", "rise"], scale=0.5),
            "Timing: hold the rest poses, make the blink short",
            "Durations differ per frame. A 120 ms blink inside a ~1.4 s loop reads as alive, not twitchy."),
     "ch08-timing.png")

# creature idles together (common 100 ms clock)
anims = [("hopper", "idle", 1), ("slug", "crawl", 1), ("drone", "hover", 3)]
st = floor_strip(cells=5, rows_=3)


def draw(t):
    im = st.copy()
    for i, (k_, a, s) in enumerate(anims):
        f = anim_frames(creatures.frames(k_, a, GH["spr"][s]), t)
        im.alpha_composite(f, (4 + i * 26, 4 if k_ == "drone" else 16))
    return im


frames_, d_ = timeline(1600, 100, draw)
gif("ch08-creature-idles.gif", frames_, d_, k=5)

# boiling: avoid
rnd = random.Random(3)
boil = []
base = kit.kit()
for i in range(4):
    a = [list(r) for r in base]
    for _ in range(10):
        y, x = rnd.randrange(24), rnd.randrange(24)
        if a[y][x] != "." and 0 < x < 23:
            a[y][x] = a[y][x + rnd.choice((-1, 1))] if a[y][x + 1] != "." else a[y][x]
    boil.append(kit.img(["".join(r) for r in a]))
st2 = floor_strip(cells=3, rows_=3)


def draw2(t):
    a = on_stage(st2, boil[(t // 120) % 4], 12, 8)
    b = on_stage(st2, anim_frames((fr, du), t), 12, 8)
    return row([label(view(a, 5, bg=BLACK), "Avoid: random pixels change (boiling)", 16, FIG_BAD),
                label(view(b, 5, bg=BLACK), "Better: whole shapes move on purpose", 16, FIG_GOOD)], 16)


frames_, d_ = timeline(2840, 40, draw2)
gif("ch08-boiling.gif", frames_, d_, k=1, bg=FIG_BG)

# onion skin, clearer: frame 2 over a red ghost of frame 1, wrong vs right, on a floor line
def staged(im, dy=0):
    spr = Image.new("RGBA", (24, 27))
    spr.alpha_composite(im, (0, dy))
    return spr


floor_ = Image.new("RGBA", (24, 27), SPR_BG + (255,))
for y_ in (24, 25, 26):
    for x_ in range(24):
        floor_.putpixel((x_, y_), nes(0x2B) if y_ == 24 else nes(0x1C))
base_ = kit.img(kit.kit())


def onion_on_floor(prev, cur):
    out = floor_.copy()
    out.alpha_composite(onion([prev, cur], 1, 1, 0))
    return out


bad_ = onion_on_floor(staged(fr[0]), staged(base_, 1))
good_ = onion_on_floor(staged(fr[0]), staged(fr[1]))
save(compare(view(bad_, 8, bg=SPR_BG), view(good_, 8, bg=SPR_BG),
             "Avoid: whole sprite moved, feet sink", "Better: body down 1 px, feet locked",
             title="Onion skin: frame 2 over a red ghost of frame 1",
             note="Red shows where frame 1 was. On the right, hood, face and body drop 1 px, the lantern 2 px; "
                  "the legs leave no ghost."), "ch08-onion.png")

# frames cost tiles: new 8x8 sprite tiles per idle frame
seen, cells, counts = set(), [], []
for f in fr:
    body = f.crop((4, 0, 20, 24))
    new = []
    for ty in range(3):
        for tx in range(2):
            key = body.crop((tx * 8, ty * 8, tx * 8 + 8, ty * 8 + 8)).tobytes()
            if key not in seen:
                seen.add(key)
                new.append((tx * 8, ty * 8))
    cells.append(new)
    counts.append(len(new))
items = []
for i, (f, new) in enumerate(zip(fr, cells)):
    body = f.crop((4, 0, 20, 24))
    big = view(body, 8, bg=SPR_BG, major=8, major_color=(255, 255, 255, 120))
    d = ImageDraw.Draw(big)
    for x, y in new:
        d.rectangle([x * 8 + 1, y * 8 + 1, (x + 8) * 8 - 2, (y + 8) * 8 - 2], outline=(255, 60, 200), width=3)
    items.append((big, "%d: %d new tile%s" % (i + 1, len(new), "" if len(new) == 1 else "s")))
save(panel(items, gap=20, title="Frames cost tiles: new 8 x 8 sprite tiles per idle frame",
           note="Pink = a tile the pattern table did not hold yet. Idle total: %d tiles "
                "(the 1 px drop touches all six; the blink only one)." % sum(counts)),
     "ch08-idle-tiles.png")
