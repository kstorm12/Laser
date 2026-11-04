"""Damascus / topo swirl pattern for a frost engrave (P790 back panel, a design to consider).

Two tones, no gray: frost lines of one fixed width trace the contours of domain-warped noise,
on bare chrome, which gives the wavy loops of a Damascus or topo-map finish.
Being two-tone, it needs no dither and does not depend on a DPI test: only the frost pen and
the line width matter. Fixed seed: same args, same art. Change --seed for a different pattern
on each club.

Writes next to this script:
  swirl.png           1-bit at --dpi, black = fire = frost. Import as-is (EzCad2 Bitmap,
                      Fixed DPI = --dpi, Dither off; LightBurn Pass-Through)
  swirl-preview.png   roughly how it should look on chrome (light = frost)

Usage: python3 make_swirl.py --width 60 --height 24 [--dpi 600] [--cell 10] [--bands 10]
       [--warp 2] [--line 0.45] [--seed 3] [--invert]
--cell is the noise size in mm (bigger = larger, lazier loops). --bands is how many contour
lines the value range splits into (more = denser lines). --warp bends the contours (0 = plain
rings, 2+ = tight marbling). --line is the frost line width; keep it at 0.3mm or more so the
frost holds a clean edge (the spot is about 0.1mm). --invert gives chrome lines on frost.
The script reports the narrowest chrome gap: where it drops under about 0.2mm, lines merge.
Stdlib only; the noise and PNG writer come from `logos/swamp/make_swamp.py`.
"""

import argparse
import random
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent / "swamp"))
from make_swamp import Noise2, write_png  # noqa: E402

COARSE = 2  # the noise is sampled every 2 px and interpolated; edges are thresholded at full res


def field(w, h, mm_px, cell, warp, seed):
    """Warped noise on a coarse grid, normalized to 0..1, as a function (x, y) -> value."""
    rng = random.Random(seed)
    n1, n2, n3 = Noise2(rng, 2), Noise2(rng, 2), Noise2(rng, 3)
    cw, ch = w // COARSE + 2, h // COARSE + 2
    g = []
    for j in range(ch):
        row = []
        for i in range(cw):
            x, y = i * COARSE * mm_px / cell, j * COARSE * mm_px / cell
            qx, qy = n1.at(x, y), n2.at(x + 5.2, y + 1.3)
            row.append(n3.at(x + warp * qx, y + warp * qy))
        g.append(row)
    lo, hi = min(map(min, g)), max(map(max, g))
    g = [[(v - lo) / (hi - lo) for v in row] for row in g]

    def at(x, y):
        u, v = x / COARSE, y / COARSE
        i, j = int(u), int(v)
        fu, fv = u - i, v - j
        return (g[j][i] * (1 - fu) * (1 - fv) + g[j][i + 1] * fu * (1 - fv)
                + g[j + 1][i] * (1 - fu) * fv + g[j + 1][i + 1] * fu * fv)
    return at


def render(width, height, dpi, cell, bands, warp, seed, line, invert):
    """Rows of 0/1, 1 = frost. Frost lines of a fixed width trace the noise's contours."""
    mm_px = 25.4 / dpi
    w, h = round(width / 25.4 * dpi), round(height / 25.4 * dpi)
    at = field(w, h, mm_px, cell, warp, seed)
    half = line / 2 / mm_px  # half the line width, px
    out = []
    for y in range(h):
        row = []
        for x in range(w):
            v = at(x, y) * bands
            f = v - int(v)
            # distance to the nearest contour = level gap / slope, so every line draws the
            # same width whether the contours are packed tight or spread out
            gx = (at(min(x + 1, w - 1), y) - at(max(x - 1, 0), y)) / 2 * bands
            gy = (at(x, min(y + 1, h - 1)) - at(x, max(y - 1, 0))) / 2 * bands
            d = min(f, 1 - f) / max((gx * gx + gy * gy) ** 0.5, 1e-9)
            row.append(int(d < half) ^ invert)
        out.append(row)
    return out


def thinnest_band(img, mm_px):
    """Shortest run of 1s along rows and columns, in mm, ignoring runs cut by the edge."""
    best = None
    for lines in (img, list(zip(*img))):
        for line in lines:
            start = 0
            for i in range(1, len(line) + 1):
                if i == len(line) or line[i] != line[start]:
                    if line[start] and start > 0 and i < len(line):
                        n = i - start
                        best = n if best is None else min(best, n)
                    start = i
    return (best or 0) * mm_px


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--width", type=float, default=60.0, help="panel width, mm")
    ap.add_argument("--height", type=float, default=24.0, help="panel height, mm")
    ap.add_argument("--dpi", type=int, default=600, help="bitmap resolution")
    ap.add_argument("--cell", type=float, default=10.0, help="noise size, mm")
    ap.add_argument("--bands", type=int, default=10, help="contour lines across the range")
    ap.add_argument("--warp", type=float, default=2.0, help="contour bending")
    ap.add_argument("--line", type=float, default=0.45, help="frost line width, mm")
    ap.add_argument("--seed", type=int, default=3, help="pattern; change per club for variety")
    ap.add_argument("--invert", action="store_true", help="swap frost and chrome bands")
    a = ap.parse_args()
    img = render(a.width, a.height, a.dpi, a.cell, a.bands, a.warp, a.seed, a.line,
                 int(a.invert))
    write_png(HERE / "swirl.png", [[1 - v for v in r] for r in img], 1, a.dpi)
    write_png(HERE / "swirl-preview.png", [[70 + 160 * v for v in r] for r in img], 8, a.dpi)
    frost = sum(map(sum, img)) / (len(img) * len(img[0]))
    print(f"swirl: {a.width:.1f} x {a.height:.1f} mm at {a.dpi} dpi, cell {a.cell} mm, "
          f"{a.bands} bands, warp {a.warp}, seed {a.seed}; {frost:.0%} frost, "
          f"narrowest gap {thinnest_band([[1 - v for v in r] for r in img], 25.4 / a.dpi):.2f} mm")


if __name__ == "__main__":
    main()
