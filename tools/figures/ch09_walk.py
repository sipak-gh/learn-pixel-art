"""Ch. 9 figures: walk and run cycles."""
from _v import *

wf, wd = kit.frames("walk")
rf, rd = kit.frames("run")
names_w = ["contact", "pass", "contact", "pass"]
save(figure(filmstrip(wf, 6, wd, bg=SPR_BG), "Walk: 4 frames x 140 ms",
            "Contact (legs apart) and passing (legs together, body 1 px up), then mirrored. "
            "The arm swings opposite to the front leg."), "ch09-walk-strip.png")
save(figure(filmstrip(rf, 6, rd, bg=SPR_BG), "Run: 4 frames x 90 ms",
            "Lean forward, longer stride, flat hood tail, pumping arm. Faster frames, not more frames."),
     "ch09-run-strip.png")
a13, n13 = changed(wf[0], wf[2])
a12, n12 = changed(wf[0], wf[1])
save(panel([(sv(a13, 6, grid=False, major=None), "1 -> 3 (both contacts): %d px" % n13),
            (sv(a12, 6, grid=False, major=None), "1 -> 2 (contact -> pass): %d px" % n12)],
           gap=24, title="What changes between walk frames (pink)",
           note="Between the two contacts only legs and arm swap. The 1 px bob on the passing frame "
                "shifts every edge of the body - that is what makes the walk feel weighted."),
     "ch09-changes.png")
save(panel([(sv(wf[0], 7, grid=False, major=None), "walk: upright, short stride"),
            (sv(rf[0], 7, grid=False, major=None), "run: lean 1 px, long stride, tail flat")],
           title="Walk vs run: same character, different attitude"), "ch09-walk-vs-run.png")
stage = floor_strip(cells=8, rows_=3)
gif("ch09-walk.gif", [on_stage(stage.crop((0, 0, 48, 48)), f, 12, 8) for f in wf], wd, k=6)
gif("ch09-run.gif", [on_stage(stage.crop((0, 0, 48, 48)), f, 12, 8) for f in rf], rd, k=6)


# Speed = stride / step time. The planted (near) foot sits 9 px further back on the second
# walk contact than on the first (x 11-13 -> 2-4), two 140 ms frames later: 18 px per 560 ms
# cycle. The run's planted foot travels 11 px per two 90 ms frames: 22 px per 360 ms cycle.
# Each GIF wraps after a whole number of cycles, so the loop is seamless.
def mover(frames_durs, px_per_cycle, wrap):
    cycle = sum(frames_durs[1])

    def draw(t):
        x = int(t * px_per_cycle / cycle) % wrap - 24
        return on_stage(stage, anim_frames(frames_durs, t), x, 8)
    return draw


fr_, d_ = timeline(9 * 560, 20, mover((wf, wd), 18, 9 * 18))
gif("ch09-walk-scene.gif", fr_, d_, k=4)
fr_, d_ = timeline(7 * 360, 20, mover((rf, rd), 22, 7 * 22))
gif("ch09-run-scene.gif", fr_, d_, k=4)

# foot sliding: contact 1 (red) and contact 2 (blue, two frames later) where the game draws them
fl = floor_strip(cells=4, rows_=3)
rows_fs = []
K = 7
for px2, cap, colr in [(4, "Avoid: 2 px per frame - foot slides back", FIG_BAD),
                       (9, "Better: 4.5 px per frame - foot stays put", FIG_GOOD),
                       (16, "Avoid: 8 px per frame - Kit skates", FIG_BAD)]:
    im = fl.copy()
    im.alpha_composite(tint(wf[0], (255, 80, 80), 170), (6, 8))
    im.alpha_composite(tint(wf[2], (80, 160, 255), 170), (6 + px2, 8))
    big = nv(im.crop((2, 18, 46, 36)), K)
    d = ImageDraw.Draw(big)
    fx0 = (6 + 4 + 11 - 2) * K            # contact 1: near foot spans body x 11-13
    d.rectangle([fx0 - 2, (30 - 18) * K - 2, fx0 + 3 * K + 1, (32 - 18) * K + 1],
                outline=(255, 255, 255), width=2)
    rows_fs.append((big, cap, colr))
save(panel(rows_fs, gap=16, size=14, title="Matching speed to stride (red: contact 1, blue: contact 2)",
           note="The near foot is planted from contact 1 to contact 2 (white box = where it touched down). "
                "At the right speed the blue copy lands on the same floor pixels."), "ch09-foot-slide.png")
