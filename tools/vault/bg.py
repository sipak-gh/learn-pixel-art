"""Antenna Ridge background bands for NES-style parallax (one sub-palette per band; on
hardware each band is a horizontal strip scrolled at its own speed by a mid-frame scroll
split, so bands never overlap vertically). All bands tile horizontally with period 256.
"""
from __future__ import annotations

from nes import render
from vault.tiles import stars

W = 256


def _blank(h, ch="0"):
    return [[ch] * W for _ in range(h)]


def _join(a):
    return ["".join(r) for r in a]


def _peaks(h, peaks, base):
    """Height profile from peaks (x, height, left_run, right_run): each slope climbs 1 px per
    `run` px, so every slope is a clean, jaggy-free line."""
    prof = [base] * W
    for px, ph, lr, rr in peaks:
        for x in range(W):
            d = (x - px) % W
            d = d - W if d > W // 2 else d
            run = lr if d < 0 else rr
            hh = ph - abs(d) // run
            if hh > prof[x]:
                prof[x] = hh
    return [min(h - 1, p) for p in prof]


def far_hills(h=48):
    """BG2 far hills: slot 1 mass, slot 2 lit rim on left-facing slopes, slot 3 snow caps."""
    prof = _peaks(h, [(20, 34, 2, 3), (70, 24, 2, 2), (118, 40, 3, 3), (176, 28, 2, 3),
                      (214, 36, 3, 2)], 10)
    a = _blank(h)
    for x in range(W):
        top = h - prof[x]
        for y in range(top, h):
            a[y][x] = "1"
        lit = prof[(x + 1) % W] < prof[x] or prof[(x - 1) % W] < prof[x]
        rising = prof[(x + 1) % W] > prof[x]  # left-facing slope (towards the moon)
        if rising:
            a[top][x] = "2"
            if top + 1 < h:
                a[top + 1][x] = "2"
        else:
            a[top][x] = "2"
        if prof[x] > 30:
            a[top][x] = "3"
            if rising and top + 1 < h:
                a[top + 1][x] = "3"
        _ = lit
    return _join(a)


def towers(h=64):
    """BG1 mid layer: a low ridge (slot 1, slot 2 rim) with lattice antenna masts. Mast legs
    are slot 2 grey on the moon-lit (right) side, slot 1 on the shadow side; beacons slot 3."""
    a = _blank(h)
    prof = _peaks(h, [(40, 16, 4, 5), (150, 12, 5, 4), (226, 14, 4, 4)], 5)
    for x in range(W):
        for y in range(h - prof[x], h):
            a[y][x] = "1"
        a[h - prof[x]][x] = "2"
    for mx, mh in ((40, 58), (150, 46), (204, 34)):
        base = h - prof[mx]
        top = h - mh
        span = base - top
        for y in range(top, base + 1):
            half = 1 + (y - top) * 4 // span  # taper from 3 px wide to 9 px wide
            lx, rx = mx - half, mx + half
            a[y][lx] = "1"
            a[y][rx] = "2"
            k = (y - top) % 6
            if k == 0:
                for x in range(lx, rx + 1):
                    a[y][x] = "2" if x >= mx else "1"
            elif half > 2:  # X bracing
                off = k * half // 3
                for x in (lx + off, rx - off):
                    if lx < x < rx:
                        a[y][x] = "1"
        for x in range(mx - 5, mx + 6):  # dish arm
            a[top + 4][x] = "2" if x > mx else "1"
        a[top + 3][mx + 5] = "2"
        a[top + 5][mx + 5] = "2"
        for y in range(top - 3, top):
            a[y][mx] = "2"
        a[top - 4][mx] = "3"
    return _join(a)


def sky(h=96, seed=11):
    """BG1 sky: star metatiles in a fixed (non-scrolling) band, plus a moon (16x16 x4)."""
    a = _blank(h)
    for my in range(h // 16):
        for mx in range(W // 16):
            s = stars((seed + mx * 7 + my * 13) % 6, density=3)  # 6 star tiles reused
            for y in range(16):
                for x in range(16):
                    a[my * 16 + y][mx * 16 + x] = s[y][x]
    # moon: 28 px disc with craters, lit from the right, inside a 32x32 metatile block
    cx, cy, r = 200, 36, 13
    for y in range(cy - r - 2, cy + r + 2):
        for x in range(cx - r - 2, cx + r + 2):
            d2 = (x + 0.5 - cx) ** 2 + (y + 0.5 - cy) ** 2
            if d2 <= r * r:
                a[y][x] = "3" if (x - cx) * 0.8 + (y - cy) * -0.2 > -6 else "2"
            elif d2 <= (r + 1) ** 2 and a[y][x] == "0":
                a[y][x] = "0"
    for (x, y, rr) in ((194, 30, 2), (204, 42, 3), (197, 44, 1), (208, 30, 1)):
        for yy in range(y - rr, y + rr + 1):
            for xx in range(x - rr, x + rr + 1):
                if (xx - x) ** 2 + (yy - y) ** 2 <= rr * rr:
                    a[yy][xx] = "2"
    return _join(a)


def band_images(area_bg):
    """-> dict of rendered bands (RGBA) for the Ridge parallax."""
    return {"sky": render(sky(), area_bg[1], backdrop=True),
            "hills": render(far_hills(), area_bg[2], backdrop=True),
            "towers": render(towers(), area_bg[1], backdrop=True)}
