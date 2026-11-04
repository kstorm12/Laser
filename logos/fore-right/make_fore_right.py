"""Chalkboard-style "FORE RIGHT" lines for an iron face, as closed outlines for laser engraving.

Rows of the phrase repeated across a WIDTH x HEIGHT mm area, in Gochi Hand (fonts/, OFL).
A letter that would cross the row's end is dropped, and each row ends at a slightly different
point, so rows trail off like lines written on a chalkboard. Each row also gets a small fixed
jitter so it reads handwritten, not typeset.

Writes fore-right.svg (preview) and fore-right.dxf (R12, mm, for EzCad2/LightBurn) here.
Usage: python3 make_fore_right.py --width 55 --height 28 --rows 10
Measure the face's usable area on the real club first (see the P790 runbook).
"""

import argparse
import random
from pathlib import Path

from fontTools.pens.recordingPen import RecordingPen
from fontTools.ttLib import TTFont

HERE = Path(__file__).parent

FONT = HERE / "fonts" / "GochiHand-Regular.ttf"
TEXT = "FORE RIGHT"
WORD_GAP = 1.2   # gap between repeats, in space widths
CAP_FILL = 0.62  # cap height as a fraction of row pitch (the rest is line spacing)
SEED = 7         # fixed, so the same arguments always give the same art
CURVE_STEPS = 12  # line segments per curve: EzCad2 hatches polylines more reliably than splines


# ---------- glyph outlines -> closed polylines ----------

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


# ---------- writers (SVG preview, R12 DXF for EzCad2) ----------

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


# ---------- layout ----------


def row_glyphs(font, scale, width, x_start):
    """Glyph contours (mm) for one row; stops at the first letter that would cross width."""
    hmtx, cmap = font["hmtx"], font.getBestCmap()
    space = hmtx[cmap[ord(" ")]][0] * scale
    x, out = x_start, []
    while True:
        for ch in TEXT:
            adv = hmtx[cmap[ord(ch)]][0] * scale
            if ch != " ":
                contours = [[(px * scale + x, py * scale) for px, py in c]
                            for c in glyph_contours(font, ch)]
                if max(p[0] for c in contours for p in c) > width:
                    return out
                out += contours
            x += adv
        x += space * WORD_GAP


def build(width, height, rows):
    font = TTFont(FONT)
    cap_units = font["OS/2"].sCapHeight or font["head"].unitsPerEm * 0.7
    pitch = height / rows
    scale = pitch * CAP_FILL / cap_units
    rng = random.Random(SEED)
    shapes = []
    for r in range(rows):
        dx = rng.uniform(0, 0.35 * pitch)   # each line starts a little differently
        dy = rng.uniform(-0.06, 0.06) * pitch
        end = width * rng.uniform(0.82, 1.0)  # rows run out of room at different points
        base = height - (r + 1) * pitch + (1 - CAP_FILL) * pitch / 2 + dy
        shapes += [[(x, y + base) for x, y in c] for c in row_glyphs(font, scale, end, dx)]
    return shapes


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--width", type=float, default=55.0, help="usable face width, mm")
    ap.add_argument("--height", type=float, default=28.0, help="height the rows fill, mm")
    ap.add_argument("--rows", type=int, default=10)
    a = ap.parse_args()
    shapes = build(a.width, a.height, a.rows)
    write_svg(HERE / "fore-right.svg", shapes, a.width, a.height)
    write_dxf(HERE / "fore-right.dxf", shapes)
    print(f"fore-right: {a.width:.1f} x {a.height:.1f} mm, {a.rows} rows, "
          f"letters {a.height / a.rows * CAP_FILL:.2f} mm tall")


if __name__ == "__main__":
    main()
