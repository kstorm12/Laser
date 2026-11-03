"""STORM wordmark with a lightning-bolt T, as closed outlines for laser engraving.

Writes, next to this script:
  storm-<variant>.svg   preview / LightBurn-ready art
  storm-<variant>.dxf   R12 DXF of closed polylines for EzCad2 (mm)

Usage: python3 make_logo.py [--width MM]
Only dependency: fontTools (system package). Curves are flattened to short line segments,
because EzCad2 hatches closed polylines reliably and splines less so.
"""

import argparse
from pathlib import Path

from fontTools.pens.recordingPen import RecordingPen
from fontTools.ttLib import TTFont

HERE = Path(__file__).parent

FONTS = {
    "black": "/usr/share/fonts/noto/NotoSans-Black.ttf",
    "narrow": "/usr/share/fonts/gsfonts/NimbusSansNarrow-Bold.otf",
}
TRACKING = 0.06  # extra letter spacing, fraction of cap height
CURVE_STEPS = 12  # line segments per curve


# ---------- glyph outlines -> polylines ----------

def _quad(p0, p1, p2, n):
    return [((1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t * t * p2[0],
             (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t * t * p2[1])
            for t in (i / n for i in range(1, n + 1))]


def _cubic(p0, p1, p2, p3, n):
    out = []
    for i in range(1, n + 1):
        t = i / n
        a, b, c, d = (1 - t) ** 3, 3 * (1 - t) ** 2 * t, 3 * (1 - t) * t * t, t ** 3
        out.append((a * p0[0] + b * p1[0] + c * p2[0] + d * p3[0],
                    a * p0[1] + b * p1[1] + c * p2[1] + d * p3[1]))
    return out


def glyph_contours(font, char):
    """Closed polylines (font units, y up) for one character."""
    gs = font.getGlyphSet()
    pen = RecordingPen()
    gs[font.getBestCmap()[ord(char)]].draw(pen)
    contours, cur = [], []
    for op, pts in pen.value:
        if op == "moveTo":
            cur = [pts[0]]
        elif op == "lineTo":
            cur.append(pts[0])
        elif op == "qCurveTo":
            # TrueType implied on-curve points between consecutive off-curve points
            start, offs, end = cur[-1], pts[:-1], pts[-1]
            for i, off in enumerate(offs):
                nxt = end if i == len(offs) - 1 else (
                    (off[0] + offs[i + 1][0]) / 2, (off[1] + offs[i + 1][1]) / 2)
                cur += _quad(start, off, nxt, CURVE_STEPS)
                start = nxt
        elif op == "curveTo":
            cur += _cubic(cur[-1], *pts, CURVE_STEPS)
        elif op in ("closePath", "endPath"):
            if len(cur) > 2:
                contours.append(cur)
            cur = []
    return contours


def t_metrics(font):
    """Cap height, crossbar bottom, stem width, advance of the font's own T (all straight lines)."""
    (c,) = glyph_contours(font, "T")
    ys = sorted({round(p[1]) for p in c})
    xs = sorted({round(p[0]) for p in c})
    cap, bar_bottom = ys[-1], ys[-2]
    stem = xs[-2] - xs[1]
    left, right = xs[0], xs[-1]
    return cap, bar_bottom, stem, left, right


# ---------- the bolt T ----------

def bolt_t(cap, bar_bottom, stem, left, right, drop):
    """One closed polygon: the T's crossbar with a zig-zag bolt for a stem.

    drop: how far the bolt tip falls below the baseline, as a fraction of cap height.
    """
    cx = (left + right) / 2
    s = stem
    yb = -drop * cap  # tip height
    h = bar_bottom - yb
    hi, lo = yb + 0.58 * h, yb + 0.42 * h  # the step of the zig-zag
    return [
        (left, cap), (right, cap), (right, bar_bottom),
        (cx + 0.75 * s, bar_bottom),   # bolt top, right corner
        (cx + 0.10 * s, hi),           # down-left to the step
        (cx + 1.05 * s, hi),           # step out to the right
        (cx - 0.70 * s, yb),           # down-left to the tip
        (cx - 0.10 * s, lo),           # back up to the lower step
        (cx - 1.05 * s, lo),           # step out to the left
        (cx - 0.45 * s, bar_bottom),   # up to bolt top, left corner
        (left, bar_bottom),
    ]


# ---------- layout + writers ----------

def build(font_path, drop):
    font = TTFont(font_path)
    hmtx = font["hmtx"]
    cmap = font.getBestCmap()
    cap, bar_bottom, stem, left, right = t_metrics(font)
    track = TRACKING * cap
    x, shapes = 0.0, []
    for ch in "STORM":
        if ch == "T":
            contours = [bolt_t(cap, bar_bottom, stem, left, right, drop)]
        else:
            contours = glyph_contours(font, ch)
        shapes += [[(px + x, py) for px, py in c] for c in contours]
        x += hmtx[cmap[ord(ch)]][0] + track
    return shapes


def normalize(shapes, width_mm):
    """Scale to width_mm, origin at bottom-left of the bounding box (mm, y up)."""
    pts = [p for c in shapes for p in c]
    x0, y0 = min(p[0] for p in pts), min(p[1] for p in pts)
    x1, y1 = max(p[0] for p in pts), max(p[1] for p in pts)
    k = width_mm / (x1 - x0)
    return [[((px - x0) * k, (py - y0) * k) for px, py in c] for c in shapes], (y1 - y0) * k


def write_svg(path, shapes, w, h):
    d = " ".join("M" + " L".join(f"{x:.3f},{h - y:.3f}" for x, y in c) + " Z" for c in shapes)
    path.write_text(
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w:.3f}mm" height="{h:.3f}mm" '
        f'viewBox="0 0 {w:.3f} {h:.3f}">\n'
        f'  <path fill="#111" fill-rule="evenodd" d="{d}"/>\n</svg>\n')


def write_dxf(path, shapes):
    """Minimal R12 DXF: one closed POLYLINE per contour, units mm."""
    out = ["0", "SECTION", "2", "HEADER", "9", "$INSUNITS", "70", "4", "0", "ENDSEC",
           "0", "SECTION", "2", "ENTITIES"]
    for c in shapes:
        out += ["0", "POLYLINE", "8", "0", "66", "1", "70", "1"]
        for x, y in c:
            out += ["0", "VERTEX", "8", "0", "10", f"{x:.4f}", "20", f"{y:.4f}"]
        out += ["0", "SEQEND", "8", "0"]
    out += ["0", "ENDSEC", "0", "EOF"]
    path.write_text("\n".join(out) + "\n")


VARIANTS = {
    # name: (font, bolt drop below baseline as fraction of cap height)
    "a-black-inline": ("black", 0.0),
    "b-black-drop": ("black", 0.30),
    "c-narrow-drop": ("narrow", 0.30),
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--width", type=float, default=40.0, help="overall width in mm")
    args = ap.parse_args()
    for name, (font, drop) in VARIANTS.items():
        shapes, h = normalize(build(FONTS[font], drop), args.width)
        write_svg(HERE / f"storm-{name}.svg", shapes, args.width, h)
        write_dxf(HERE / f"storm-{name}.dxf", shapes)
        print(f"storm-{name}: {args.width:.1f} x {h:.1f} mm")


if __name__ == "__main__":
    main()
