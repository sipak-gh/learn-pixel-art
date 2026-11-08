"""Ch. 10 figures: the jump."""
from _v import *

jf, jd = kit.frames("jump")
names = ["squat", "rise", "apex", "fall", "land"]
save(figure(filmstrip(jf, 6, jd, bg=SPR_BG), "Jump: 5 poses",
            "1 squat (anticipation) · 2 rise (hood trails down) · 3 apex · 4 fall (hood lifts, legs reach) "
            "· 5 land (squash)."), "ch10-jump-strip.png")

# arc: poses placed along a parabola
W, H = 176, 72
arc = Image.new("RGBA", (W, H), (0, 0, 0, 0))
pts = [(0, 0, 0), (26, -24, 1), (52, -37, 1), (78, -41, 2), (104, -36, 3), (128, -22, 3), (152, 0, 4)]
for x, dy, i in pts:
    im = jf[i]
    arc.alpha_composite(im, (x, 44 + dy))
save(figure(view(arc, 4, bg=SPR_BG), "The arc: fast up, slow at the top, fast down",
            "Equal time steps: big vertical gaps near the ground, small ones near the apex. The pose changes at the turn-around."),
     "ch10-jump-arc.png")

# jump gif: physics in place
stage = floor_strip(cells=4, rows_=5).crop((0, 0, 64, 80))
G, V0 = 600.0, -230.0  # px/s^2, px/s


def draw(t):
    t %= 1500
    if t < 80:
        return on_stage(stage, jf[0], 20, 40)
    tt = (t - 80) / 1000
    dy = V0 * tt + 0.5 * G * tt * tt
    if dy >= 0:
        land_t = t - 80 - int(-2 * V0 / G * 1000)
        return on_stage(stage, jf[4] if land_t < 100 else kit.frames("idle")[0][0], 20, 40)
    vy = V0 + G * tt
    pose = jf[1] if vy < -80 else (jf[2] if vy < 60 else jf[3])
    return on_stage(stage, pose, 20, 40 + int(round(dy)))


fr_, d_ = timeline(1500, 20, draw)
gif("ch10-jump.gif", fr_, d_, k=5)

idle0 = kit.frames("idle")[0][0]
save(panel([(sv(idle0, 7, grid=False, major=None), "stand: 22 px tall"),
            (sv(jf[0], 7, grid=False, major=None), "squat: 20 px, wide"),
            (sv(jf[3], 7, grid=False, major=None), "fall: 24 px, hood up"),
            (sv(jf[4], 7, grid=False, major=None), "land: 20 px, wide")],
           title="Squash and stretch at 24 px: one pixel is enough",
           note="Each part moves 1 px: squash = body down 1, head 1 more, feet apart; "
                "stretch = body up 1, hood tip 1 more, legs reach."),
     "ch10-squash.png")

dust, dd = fx.frames("dust", GH["spr"][0])
st = floor_strip(cells=4, rows_=3)


def draw2(t):
    t %= 1200
    im = on_stage(st, jf[4] if t < 260 else idle0, 20, 8)
    if t < 260:
        f = anim_frames((dust, dd), min(t, 259))
        im.alpha_composite(f, (16, 24))
        im.alpha_composite(f.transpose(Image.Transpose.FLIP_LEFT_RIGHT), (36, 24))
    return im


fr_, d_ = timeline(1200, 20, draw2)
gif("ch10-landing-dust.gif", fr_, d_, k=6)
save(figure(filmstrip(dust, 8, dd, bg=SPR_BG), "Landing dust: 3 frames, one 8 x 8 sprite each side",
            "Uses Kit's palette (SP0) so it costs no extra sub-palette."), "ch10-dust.png")
