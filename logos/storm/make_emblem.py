"""Storm emblem concepts (symbol only), as closed outlines for laser engraving.

Writes emblem-<variant>.svg and .dxf next to this script, sized to --height MM.
Stdlib only. Shapes never overlap (EzCad2 hatches even-odd, so overlaps would leave holes).
"""

import argparse
import math
from pathlib import Path

from make_logo import write_dxf, write_svg  # same writers as the wordmark

HERE = Path(__file__).parent

# Bolt in a 1 x 1 box, y up: top edge, step, tip, step back.
BOLT = [(0.45, 1.0), (0.85, 1.0), (0.50, 0.56), (0.82, 0.56),
        (0.12, 0.0), (0.48, 0.44), (0.18, 0.44)]


def place(poly, x, y, w, h):
    return [(x + px * w, y + py * h) for px, py in poly]


def circle(cx, cy, r, n=96):
    return [(cx + r * math.cos(2 * math.pi * i / n), cy + r * math.sin(2 * math.pi * i / n))
            for i in range(n)]


def hexagon(cx, cy, r):
    return [(cx + r * math.cos(math.pi / 2 + i * math.pi / 3),
             cy + r * math.sin(math.pi / 2 + i * math.pi / 3)) for i in range(6)]


def ring_bolt():
    """Bolt inside a ring. Ring stroke 0.12, gap to bolt by construction."""
    return [circle(0.5, 0.5, 0.5), circle(0.5, 0.5, 0.38)[::-1],
            place(BOLT, 0.27, 0.2, 0.46, 0.6)]


def hex_bolt():
    """Bolt inside a hexagon frame, uniform stroke (inner hexagon is a true offset)."""
    outer, stroke = 0.5, 0.1
    inner = outer - stroke / math.cos(math.pi / 6)
    return [hexagon(0.5, 0.5, outer), hexagon(0.5, 0.5, inner)[::-1],
            place(BOLT, 0.29, 0.22, 0.42, 0.56)]


def cloud_bolt():
    """Solid cloud (upper envelope of three circles over a flat base) with a bolt beneath."""
    base = 0.45  # cloud bottom
    # outer bumps centered just above the base so the cloud's ends round off instead of squaring
    bumps = [(0.25, 0.50, 0.15), (0.51, 0.63, 0.25), (0.78, 0.51, 0.14)]
    x0, x1 = 0.10, 0.92
    top = []
    n = 120
    for i in range(n + 1):
        x = x0 + (x1 - x0) * i / n
        ys = [cy + math.sqrt(r * r - (x - cx) ** 2) for cx, cy, r in bumps if abs(x - cx) <= r]
        top.append((x, max(ys + [base])))
    cloud = [(x1, base), (x0, base)] + top  # flat bottom, then the bumpy top left to right
    bolt = place(BOLT, 0.28, 0.0, 0.46, base - 0.06)  # gap of 0.06 under the cloud
    return [cloud, bolt]


VARIANTS = {"ring": ring_bolt, "hex": hex_bolt, "cloud": cloud_bolt}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--height", type=float, default=10.0, help="overall height in mm")
    args = ap.parse_args()
    for name, fn in VARIANTS.items():
        shapes = fn()
        pts = [p for c in shapes for p in c]
        x0, y0 = min(p[0] for p in pts), min(p[1] for p in pts)
        y1, x1 = max(p[1] for p in pts), max(p[0] for p in pts)
        k = args.height / (y1 - y0)
        shapes = [[((x - x0) * k, (y - y0) * k) for x, y in c] for c in shapes]
        w = (x1 - x0) * k
        write_svg(HERE / f"emblem-{name}.svg", shapes, w, args.height)
        write_dxf(HERE / f"emblem-{name}.dxf", shapes)
        print(f"emblem-{name}: {w:.1f} x {args.height:.1f} mm")


if __name__ == "__main__":
    main()
