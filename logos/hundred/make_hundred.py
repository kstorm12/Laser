"""Cropped, angled $100 bill for a frost image engrave (P790 back panel, second design).

Source: `hundred-source.png`, the left part of the series 2009 $100 obverse (portrait, seal,
serial, the two left "100"s), cropped before the blue security ribbon and made grayscale. From
Wikimedia Commons, "Obverse of the series 2009 $100 Federal Reserve Note.jpg", public domain
(US government work). One-sided, well under 75% of real size, so it meets 18 USC 504.

Frost reads lighter than bare chrome, so the bill's paper is frost and its ink stays bare chrome:
mirror linework on a matte note. The note is rotated and placed so it bleeds off the panel edges;
the cut edge at the ribbon fades out instead of ending on a hard line. Outside the note, the
chrome stays bare.

Writes next to this script (same set as `logos/swamp/`):
  hundred-gray.png     8-bit, black = fire. For LightBurn's own dithering (Image mode)
  hundred-dither.png   1-bit Jarvis dither at --dpi, black = fire. Import as-is (EzCad2 Bitmap,
                       Fixed DPI = --dpi, no further dithering; LightBurn Pass-Through)
  hundred-preview.png  roughly how it should look on chrome (light = frost)

Usage: python3 make_hundred.py --width 60 --height 24 --dpi 600 [--zoom 0.5] [--angle -14]
       [--x -6] [--y 0] [--gamma 1.0] [--invert] [--strip]
--zoom is the note's size as a fraction of a real bill (0.5 puts Franklin's face, brow to chin, about 11mm tall).
--angle tilts the note (degrees; negative lifts the right end). --x/--y move the source's center on the
panel, in mm from the panel's center (+x right, +y down).
--invert frosts the ink instead of the paper, for when the coupon shows frost reading darker.
Stdlib only; the dither and PNG writer come from `logos/swamp/make_swamp.py`.
"""

import argparse
import math
import struct
import sys
import zlib
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent / "swamp"))
from make_swamp import jarvis, write_png  # noqa: E402

SOURCE = HERE / "hundred-source.png"
SRC_MM_PER_PX = 156.0 / 1200  # the full Commons scan is 1200 px across a 156 mm bill
INK, PAPER = 0.18, 0.82        # source levels mapped to bare chrome (0) and full frost (1)
FADE = 0.12                    # right-hand fraction of the source that fades out (ribbon cut)


def read_png_gray(path):
    """8-bit grayscale, non-interlaced PNG (what `hundred-source.png` is) -> rows of 0..1."""
    data = path.read_bytes()
    pos, idat = 8, b""
    while pos < len(data):
        n = struct.unpack(">I", data[pos:pos + 4])[0]
        tag, body = data[pos + 4:pos + 8], data[pos + 8:pos + 8 + n]
        if tag == b"IHDR":
            w, h, depth, ctype, _, _, lace = struct.unpack(">IIBBBBB", body)
            if (depth, ctype, lace) != (8, 0, 0):
                sys.exit(f"{path.name}: need 8-bit grayscale, non-interlaced")
        elif tag == b"IDAT":
            idat += body
        pos += n + 12
    raw = zlib.decompress(idat)
    rows, prev = [], bytearray(w)
    for y in range(h):
        f = raw[y * (w + 1)]
        line = bytearray(raw[y * (w + 1) + 1:(y + 1) * (w + 1)])
        for x in range(w):
            a = line[x - 1] if x else 0
            b, c = prev[x], prev[x - 1] if x else 0
            if f == 1:
                line[x] = (line[x] + a) & 255
            elif f == 2:
                line[x] = (line[x] + b) & 255
            elif f == 3:
                line[x] = (line[x] + (a + b) // 2) & 255
            elif f == 4:
                p = a + b - c
                pa, pb, pc = abs(p - a), abs(p - b), abs(p - c)
                line[x] = (line[x] + (a if pa <= pb and pa <= pc else b if pb <= pc else c)) & 255
        rows.append([v / 255 for v in line])
        prev = line
    return rows


def render(width, height, dpi, zoom, angle, ox, oy, invert, gamma):
    """Frost map (1 = frost) for a width x height mm panel at dpi."""
    src = read_png_gray(SOURCE)
    sh, sw = len(src), len(src[0])
    w, h = round(width / 25.4 * dpi), round(height / 25.4 * dpi)
    mm_px = 25.4 / dpi
    k = mm_px / (SRC_MM_PER_PX * zoom)       # source px per panel px
    ca, sa = math.cos(math.radians(angle)), math.sin(math.radians(angle))
    cx, cy = w / 2 + ox / mm_px, h / 2 + oy / mm_px
    fade_x = sw * (1 - FADE)
    out = []
    for y in range(h):
        row = []
        for x in range(w):
            dx, dy = x - cx, y - cy
            # panel -> source: undo the rotation, then scale
            u = (ca * dx - sa * dy) * k + sw / 2
            v = (sa * dx + ca * dy) * k + sh / 2
            if not (0 <= u < sw - 1 and 0 <= v < sh - 1):
                row.append(0.0)
                continue
            iu, iv = int(u), int(v)
            fu, fv = u - iu, v - iv
            s = (src[iv][iu] * (1 - fu) * (1 - fv) + src[iv][iu + 1] * fu * (1 - fv)
                 + src[iv + 1][iu] * (1 - fu) * fv + src[iv + 1][iu + 1] * fu * fv)
            t = min(1.0, max(0.0, (s - INK) / (PAPER - INK)))
            if invert:
                t = 1 - t
            t **= gamma
            if u > fade_x:
                t *= (sw - u) / (sw - fade_x)
            row.append(t)
        out.append(row)
    return out


def write_set(stem, frost, dpi, dither_only=False):
    """Laser files (black = fire = frost) plus a preview (chrome mid-gray, frost light)."""
    dots = jarvis(frost)
    write_png(HERE / f"{stem}-dither.png", [[1 - d for d in r] for r in dots], 1, dpi)
    if dither_only:
        return
    write_png(HERE / f"{stem}-gray.png", [[round(255 * (1 - v)) for v in r] for r in frost], 8, dpi)
    write_png(HERE / f"{stem}-preview.png", [[round(70 + 160 * v) for v in r] for r in frost], 8, dpi)


# Coupon strip: Franklin's nose and mouth, the mid-tones that show dot size first.
STRIP_DPIS = (400, 500, 600, 800)
STRIP_MM = (16.0, 8.0)  # w, h of each strip, centered on the face


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--width", type=float, default=60.0, help="panel width, mm")
    ap.add_argument("--height", type=float, default=24.0, help="panel height, mm")
    ap.add_argument("--dpi", type=int, default=600, help="dither resolution (600 = 0.042mm dots)")
    ap.add_argument("--zoom", type=float, default=0.5, help="note size vs a real bill")
    ap.add_argument("--angle", type=float, default=-14.0, help="tilt, degrees (- lifts the right end)")
    ap.add_argument("--x", type=float, default=-6.0, help="move the note right, mm")
    ap.add_argument("--y", type=float, default=0.0, help="move the note down, mm")
    ap.add_argument("--gamma", type=float, default=1.0, help="tone curve, tune from the coupon")
    ap.add_argument("--invert", action="store_true", help="frost the ink, not the paper")
    ap.add_argument("--strip", action="store_true",
                    help="also write hundred-strip-<dpi> crops of the face for the coupon at " +
                         ", ".join(map(str, STRIP_DPIS)) + " dpi")
    a = ap.parse_args()
    args = (a.zoom, a.angle, a.x, a.y, a.invert, a.gamma)
    frost = render(a.width, a.height, a.dpi, *args)
    write_set("hundred", frost, a.dpi)
    face_mm = 170 * SRC_MM_PER_PX * a.zoom  # brow to chin is about 170 source px
    print(f"hundred: {a.width:.1f} x {a.height:.1f} mm, {len(frost[0])} x {len(frost)} px at "
          f"{a.dpi} dpi, zoom {a.zoom} (face about {face_mm:.0f} mm), angle {a.angle}, "
          f"gamma {a.gamma}{' (inverted)' if a.invert else ''}")
    if a.strip:
        sw, shh = STRIP_MM
        for dpi in STRIP_DPIS:
            full = render(a.width, a.height, dpi, *args)
            h, w = len(full), len(full[0])
            # the face sits right of the source's center; find it on the panel
            mm_px = 25.4 / dpi
            r = math.radians(a.angle)
            du, dv = (470 - 309) * SRC_MM_PER_PX * a.zoom, (230 - 252) * SRC_MM_PER_PX * a.zoom
            fx = w / 2 + (a.x + math.cos(r) * du + math.sin(r) * dv) / mm_px
            fy = h / 2 + (a.y - math.sin(r) * du + math.cos(r) * dv) / mm_px
            x0, y0 = max(0, int(fx - sw / 2 / mm_px)), max(0, int(fy - shh / 2 / mm_px))
            crop = [row[x0:x0 + int(sw / mm_px)] for row in full[y0:y0 + int(shh / mm_px)]]
            write_set(f"hundred-strip-{dpi}", crop, dpi, dither_only=True)
            print(f"  strip {dpi} dpi: {len(crop[0]) * mm_px:.1f} x {len(crop) * mm_px:.1f} mm")


if __name__ == "__main__":
    main()
