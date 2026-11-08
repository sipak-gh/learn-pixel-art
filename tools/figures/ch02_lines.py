"""Ch. 2 figures: pixel lines, slopes, curves, jaggies, doubles."""
from _v import *

C1, C2 = nes(0x30), nes(0x1C)


def canvas(w, h):
    return Image.new("RGBA", (w, h), (0, 0, 0, 255))


def plot(im, pts, c=C1, ox=0, oy=0):
    for x, y in pts:
        im.putpixel((x + ox, y + oy), c)
    return im


def runs_line(runs, vertical=False):
    pts, x, y = [], 0, 0
    for r in runs:
        for _ in range(r):
            pts.append((y, x) if vertical else (x, y))
            x += 1
        y += 1
    return pts


# 1. clean slopes
items = []
for runs, name in (([1] * 12, "1:1"), ([2] * 8, "2:1"), ([3] * 6, "3:1"), ([4] * 5, "4:1"),
                   ([1] * 12, "1:2 (steep)")):
    w = sum(runs) + 2
    h = len(runs) + 2
    v = "steep" in name
    im = canvas(h if v else w, w if v else h)
    if v:
        pts = [(y, x) for x, y in runs_line([2] * 8)]
        im = canvas(10, 18)
    else:
        pts = runs_line(runs)
    plot(im, pts, ox=1, oy=1)
    items.append((nv(im, 8), name))
save(panel(items, title="Clean pixel lines: equal runs per step",
           note="Each step moves the same number of pixels. Lines with ratios 1:1, 2:1, 3:1... read as straight."),
     "ch02-slopes.png")

# 2. jaggies
bad = plot(canvas(20, 10), runs_line([1, 3, 2, 1, 4, 2, 1, 3]), ox=1, oy=1)
good = plot(canvas(20, 10), runs_line([2, 2, 2, 2, 2, 2, 2, 3]), ox=1, oy=1)
save(compare(nv(bad, 10), nv(good, 10), "Avoid: uneven runs (jaggies)", "Better: even runs",
             title="Jaggies: irregular runs make a line wobble"), "ch02-jaggies.png")

# 3. curves
smooth = runs_line([5, 3, 2, 1, 1])
bumpy = runs_line([4, 1, 3, 1, 2])
a = plot(canvas(16, 8), bumpy, ox=1, oy=1)
b = plot(canvas(16, 8), smooth, ox=1, oy=1)
save(compare(nv(a, 12), nv(b, 12), "Avoid: runs go up and down (4,1,3,1,2)",
             "Better: runs shrink steadily (5,3,2,1,1)", title="Curves: runs change gradually"),
     "ch02-curves.png")

# 4. doubles / L-corners
dbl = canvas(12, 10)
plot(dbl, [(1, 1), (2, 1), (3, 2), (3, 3), (4, 3), (5, 4), (6, 4), (6, 5), (7, 6), (8, 6), (8, 7)])
cln = canvas(12, 10)
plot(cln, [(1, 1), (2, 1), (3, 2), (4, 3), (5, 3), (6, 4), (7, 5), (8, 5), (9, 6)])
save(compare(nv(dbl, 12), nv(cln, 12), "Avoid: doubles / L-corners", "Better: single-pixel steps",
             title="Line weight: remove the extra corner pixels"), "ch02-doubles.png")

# 5. pod curves (prop) on the grid
pod = render(P.POD, GH["bg"][1], backdrop=True)
save(panel([(view(pod, 10, grid=True, bg=BLACK, major=8), "seed pod prop, 16 x 32")],
           title="Curves in a real prop",
           note="Count the runs around the bulb: they grow and shrink steadily. The stalk is a 1 px line plus a 1 px shadow."),
     "ch02-pod-curves.png")

# 6. circles at small sizes
items = []
for d in (4, 6, 8, 12, 16):
    im = canvas(d + 2, d + 2)
    r = d / 2
    for y in range(d):
        for x in range(d):
            inside = (x + 0.5 - r) ** 2 + (y + 0.5 - r) ** 2 <= r * r
            edge = inside and any(not ((xx + 0.5 - r) ** 2 + (yy + 0.5 - r) ** 2 <= r * r)
                                  or not (0 <= xx < d and 0 <= yy < d)
                                  for xx, yy in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)))
            if edge:
                im.putpixel((x + 1, y + 1), C1)
    items.append((nv(im, 10), f"{d} px"))
save(panel(items, title="Small circles: tiny sizes need hand-picked pixels"), "ch02-circles.png")
