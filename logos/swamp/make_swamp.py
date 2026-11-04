"""Made-up swamp at dusk with a gliding alligator, for a frost image engrave (P790 back panel).

Frost reads lighter than bare chrome, so the scene is built as a frost map: 1.0 = full frost,
0.0 = bare chrome. A low sun lights the sky and water (frost); cypress trees with Spanish moss,
cattails, lily pads, and the gator (snout, eyes, back ridges, V wake) stand out as dark
silhouettes. Silhouettes keep it readable at panel size. Fixed seed: same args, same art.

Writes next to this script:
  swamp-gray.png     8-bit, black = fire. For LightBurn's own dithering (Image mode)
  swamp-dither.png   1-bit Jarvis dither at --dpi, black = fire. Import as-is in EzCad2
                     (Bitmap, Fixed DPI = --dpi, no further dithering) or LightBurn (Pass-Through)
  swamp-preview.png  roughly how it should look on chrome (light = frost)

Usage: python3 make_swamp.py --width 60 --height 24 --dpi 600 [--gamma 1.0] [--invert] [--strip]
--strip also writes the coupon test strip: the gator area at 400/500/600/800 dpi.
--gamma tunes mid-tones once the coupon shows how frost density reads (>1 dimmer, <1 brighter).
--invert swaps fire/no-fire, for when the coupon shows frost reading darker than chrome.
Stdlib only.
"""

import argparse
import math
import random
import struct
import zlib
from pathlib import Path

HERE = Path(__file__).parent
SEED = 11


# ---------- 1D terrain ----------

def ridge(n, rough, rng, octaves=7):
    """n heights in 0..1 from summed sine-free value noise (smooth, mountain-like)."""
    out = [0.0] * n
    amp, freq, total = 1.0, 2, 0.0
    for _ in range(octaves):
        pts = [rng.random() for _ in range(freq + 2)]
        for i in range(n):
            t = i / (n - 1) * freq
            k = int(t)
            f = t - k
            f = f * f * (3 - 2 * f)
            out[i] += amp * (pts[k] * (1 - f) + pts[k + 1] * f)
        total += amp
        amp *= rough
        freq *= 2
    lo, hi = min(out), max(out)
    return [(v - lo) / (hi - lo) for v in out]


class Noise2:
    """Smooth 2D value noise in 0..1, summed over a few octaves."""

    def __init__(self, rng, octaves):
        self.oct = octaves
        self.grid = [[rng.random() for _ in range(257)] for _ in range(257)]

    def _one(self, x, y):
        ix, iy = int(x) % 256, int(y) % 256
        fx, fy = x - int(x), y - int(y)
        fx, fy = fx * fx * (3 - 2 * fx), fy * fy * (3 - 2 * fy)
        g = self.grid
        a = g[iy][ix] * (1 - fx) + g[iy][ix + 1] * fx
        b = g[iy + 1][ix] * (1 - fx) + g[iy + 1][ix + 1] * fx
        return a * (1 - fy) + b * fy

    def at(self, x, y):
        v, amp, tot = 0.0, 1.0, 0.0
        for o in range(self.oct):
            v += amp * self._one(x * 2 ** o, y * 2 ** o)
            tot += amp
            amp *= 0.5
        return v / tot


# ---------- the scene (frost map, rows top to bottom) ----------

def fill_ellipse(img, cx, cy, rx, ry, v):
    h, w = len(img), len(img[0])
    for y in range(max(0, int(cy - ry)), min(h, int(cy + ry) + 1)):
        dy = (y - cy) / ry
        if abs(dy) > 1:
            continue
        half = rx * math.sqrt(1 - dy * dy)
        for x in range(max(0, int(cx - half)), min(w, int(cx + half) + 1)):
            img[y][x] = v


def cypress(img, cx, base_y, height, rng, noise):
    """Bald cypress: flared trunk, flat ragged crown, moss hanging under it. All bare (0)."""
    h, w = len(img), len(img[0])
    top = base_y - height
    trunk = height * 0.035
    for y in range(int(top + height * 0.25), base_y):
        t = (y - top) / height
        flare = trunk * (1 + 2.5 * max(0.0, t - 0.8) ** 2 * 25)  # buttress at the water
        for x in range(int(cx - flare), int(cx + flare) + 1):
            if 0 <= x < w and 0 <= y < h:
                img[y][x] = 0.0
    # Crown: a cluster of flat blobs along branches.
    blobs = []
    for _ in range(9):
        bx = cx + rng.uniform(-0.35, 0.35) * height
        by = top + rng.uniform(0.0, 0.35) * height
        blobs.append((bx, by, rng.uniform(0.10, 0.20) * height, rng.uniform(0.04, 0.08) * height))
    for bx, by, rx, ry in blobs:
        # branch from trunk to blob
        for k in range(60):
            t = k / 59
            x, y = cx + (bx - cx) * t, (top + height * 0.4) + (by - top - height * 0.4) * t
            for d in range(-1, 2):
                if 0 <= int(x) + d < w and 0 <= int(y) < h:
                    img[int(y)][int(x) + d] = 0.0
        for y in range(int(by - ry), int(by + ry) + 1):
            for x in range(int(bx - rx), int(bx + rx) + 1):
                if 0 <= x < w and 0 <= y < h:
                    e = ((x - bx) / rx) ** 2 + ((y - by) / ry) ** 2
                    if e < 0.75 + 0.5 * noise.at(x * 0.15, y * 0.15):
                        img[y][x] = 0.0
        # Spanish moss: ragged strands hanging from the blob's underside
        for _ in range(int(rx / 2)):
            mx = bx + rng.uniform(-0.8, 0.8) * rx
            length = rng.uniform(0.08, 0.22) * height
            for i in range(int(length)):
                x = int(mx + 1.5 * math.sin(i * 0.3 + mx))
                y = int(by + ry * 0.5 + i)
                if 0 <= x < w and 0 <= y < h:
                    img[y][x] = 0.0


def cattail(img, x0, base_y, height, lean):
    h, w = len(img), len(img[0])
    head_top, head_bot = base_y - height, base_y - height * 0.72
    for i in range(int(height)):
        y = base_y - i
        x = int(x0 + lean * i)
        thick = 3 if head_top <= y <= head_bot else 1
        if y < head_top - height * 0.08:
            continue
        for d in range(-thick, thick + 1):
            if 0 <= x + d < w and 0 <= y < h:
                img[y][x + d] = 0.0


def gator(img, x0, y0, length, wake_v):
    """Gliding gator facing left: snout tip at (x0, y0) on the waterline. Bare (0) silhouette
    above the water, a light V wake behind it, a dark broken reflection below."""
    h, w = len(img), len(img[0])
    L = length
    # Profile above the waterline, as (fraction of length, height above water as fraction of L).
    prof = [(0.00, 0.000), (0.01, 0.030), (0.04, 0.042), (0.06, 0.036), (0.16, 0.034),
            (0.20, 0.050), (0.22, 0.080), (0.25, 0.084), (0.27, 0.060), (0.33, 0.052),
            (0.36, 0.034)]
    x = 0.38
    while x < 1.0:  # back ridges, shrinking toward the tail
        s = 0.040 * (1.1 - x)
        prof += [(x, 0.004), (x + 0.02, s), (x + 0.04, 0.004)]
        x += 0.06 if x < 0.7 else 0.05
    def height_at(f):
        for (fa, ha), (fb, hb) in zip(prof, prof[1:]):
            if fa <= f <= fb:
                return ha + (hb - ha) * (f - fa) / max(1e-9, fb - fa)
        return 0.0
    for px in range(int(L)):
        f = px / L
        top = height_at(f) * L
        x = int(x0 + px)
        for dy in range(int(top) + 1):
            y = int(y0 - dy)
            if 0 <= x < w and 0 <= y < h:
                img[y][x] = 0.0
        for dy in range(1, int(top * 0.8) + 1):  # reflection, broken by ripples
            y = int(y0 + dy)
            if 0 <= x < w and 0 <= y < h and (y // 2) % 3 != 0:
                img[y][x] = 0.05
    # Eye glint: a frost dot on the eye bump.
    ex, ey = int(x0 + 0.235 * L), int(y0 - 0.068 * L)
    fill_ellipse(img, ex, ey, max(1.5, L * 0.006), max(1.5, L * 0.006), 0.95)
    # V wake from the snout, opening behind.
    for side in (-1, 1):
        for i in range(int(L * 0.7)):
            x = int(x0 + i)
            # near arm opens toward the viewer; far arm stays flat (perspective)
            y = int(y0 + 2 + (0.09 if side > 0 else 0.025) * i)
            for d in range(2):
                if 0 <= x < w and 0 <= y + d < h and img[y + d][x] != 0.0:
                    img[y + d][x] = wake_v * (1 - i / (L * 0.8))


def scene(w, h, rng):
    img = [[0.0] * w for _ in range(h)]
    horizon = int(h * 0.56)
    sun_x, sun_y, sun_r = 0.66 * w, horizon - 0.13 * h, 0.075 * h
    noise = Noise2(rng, 4)

    # Sky: dark (bare chrome) at the top, glowing down to the low sun.
    for y in range(horizon):
        for x in range(w):
            d2 = ((x - sun_x) ** 2 + (y - sun_y) ** 2) / (0.35 * h) ** 2
            img[y][x] = min(1.0, 0.10 + 0.45 * (y / horizon) ** 1.5 + 0.45 * math.exp(-d2))
    fill_ellipse(img, sun_x, sun_y, sun_r, sun_r, 1.0)

    # Far treeline: a low, hazy band.
    line = ridge(w, 0.8, rng, octaves=8)  # rough: treetops, not mountains
    for x in range(w):
        for y in range(int(horizon - h * (0.03 + 0.05 * line[x])), horizon):
            img[y][x] = 0.22

    # Water: mirror of the sky and treeline, darker, with ripple lines.
    for y in range(horizon, h):
        src = 2 * horizon - y
        for x in range(w):
            sx = min(w - 1, max(0, x + int(3 * math.sin(y * 0.7))))
            v = img[src][sx] * 0.8 if src >= 0 else 0.1
            if (y - horizon) % max(3, h // 45) == 0 and noise.at(x * 0.02, y * 0.3) > 0.5:
                v *= 0.6  # broken ripple lines
            img[y][x] = v

    # Cypress trees, standing in the water, then their dark reflections.
    trees = [(0.10, 0.55), (0.24, 0.42), (0.88, 0.60), (0.78, 0.38)]
    for fx, th in trees:
        cypress(img, fx * w, horizon + int(0.03 * h), int(th * h), rng, noise)
    for y in range(horizon + int(0.03 * h), h):
        src = 2 * (horizon + int(0.03 * h)) - y
        if src < 0:
            continue
        for x in range(w):
            if img[src][x] == 0.0 and (y // 2) % 4 != 0:
                img[y][x] = 0.04

    # Lily pads: flat ellipses, bigger and flatter toward the viewer.
    for _ in range(14):
        py = rng.uniform(0.72, 0.95) * h
        k = (py - horizon) / (h - horizon)
        px = rng.uniform(0.15, 0.85) * w
        fill_ellipse(img, px, py, 0.012 * w * (0.5 + k), 0.004 * h * (1 + 2 * k), 0.0)

    # The gator, gliding left through the sun's reflection.
    gator(img, 0.34 * w, 0.78 * h, 0.36 * w, 0.95)

    # Cattails in the corners.
    for _ in range(9):
        cattail(img, rng.uniform(0.0, 0.10) * w, h - 1, rng.uniform(0.30, 0.50) * h,
                rng.uniform(-0.05, 0.12))
        cattail(img, rng.uniform(0.92, 1.0) * w, h - 1, rng.uniform(0.25, 0.45) * h,
                rng.uniform(-0.12, 0.05))
    return img


# ---------- output ----------

def jarvis(img):
    """1-bit Jarvis-Judice-Ninke dither, serpentine (alternate rows run right to left, so error
    does not drift one way and leave diagonal worms). Returns rows of 0/1 (1 = frost)."""
    h, w = len(img), len(img[0])
    buf = [row[:] for row in img]
    out = [[0] * w for _ in range(h)]
    k = [(1, 0, 7), (2, 0, 5), (-2, 1, 3), (-1, 1, 5), (0, 1, 7), (1, 1, 5), (2, 1, 3),
         (-2, 2, 1), (-1, 2, 3), (0, 2, 5), (1, 2, 3), (2, 2, 1)]
    for y in range(h):
        flip = -1 if y % 2 else 1
        for x in (range(w) if flip == 1 else range(w - 1, -1, -1)):
            v = buf[y][x]
            q = 1 if v >= 0.5 else 0
            out[y][x] = q
            e = (v - q) / 48
            for dx, dy, wt in k:
                xx, yy = x + dx * flip, y + dy
                if 0 <= xx < w and yy < h:
                    buf[yy][xx] += e * wt
    return out


def write_png(path, rows, bitdepth, dpi):
    h, w = len(rows), len(rows[0])
    raw = bytearray()
    for r in rows:
        raw.append(0)
        if bitdepth == 8:
            raw += bytes(r)
        else:
            for i in range(0, w, 8):
                byte = 0
                for j, b in enumerate(r[i:i + 8]):
                    byte |= (b & 1) << (7 - j)
                raw.append(byte)

    def chunk(tag, data):
        c = tag + data
        return struct.pack(">I", len(data)) + c + struct.pack(">I", zlib.crc32(c))

    ppm = round(dpi / 0.0254)
    path.write_bytes(b"\x89PNG\r\n\x1a\n"
                     + chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, bitdepth, 0, 0, 0, 0))
                     + chunk(b"pHYs", struct.pack(">IIB", ppm, ppm, 1))
                     + chunk(b"IDAT", zlib.compress(bytes(raw), 9))
                     + chunk(b"IEND", b""))


def render(width, height, dpi, invert, gamma):
    """Frost map for a width x height mm panel at dpi. gamma > 1 thins the dots in mid-tones
    (use when the coupon reads too bright), < 1 fills them in (too dim)."""
    w, h = round(width / 25.4 * dpi), round(height / 25.4 * dpi)
    frost = scene(w, h, random.Random(SEED))
    if invert:
        frost = [[1 - v for v in row] for row in frost]
    return [[v ** gamma for v in row] for row in frost]


def write_set(stem, frost, dpi, dither_only=False):
    """Laser files (black = fire = frost) plus a preview (chrome mid-gray, frost light)."""
    dots = jarvis(frost)
    write_png(HERE / f"{stem}-dither.png", [[1 - d for d in r] for r in dots], 1, dpi)
    if dither_only:
        return
    write_png(HERE / f"{stem}-gray.png", [[round(255 * (1 - v)) for v in r] for r in frost], 8, dpi)
    write_png(HERE / f"{stem}-preview.png", [[round(70 + 160 * v) for v in r] for r in frost], 8, dpi)


# Coupon strip: the gator, sun reflection, and a tree edge, the parts that show dot size first.
STRIP = (0.32, 0.64, 0.58, 0.90)  # x0, y0, x1, y1 as fractions of the panel
STRIP_DPIS = (400, 500, 600, 800)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--width", type=float, default=60.0, help="panel width, mm")
    ap.add_argument("--height", type=float, default=24.0, help="panel height, mm")
    ap.add_argument("--dpi", type=int, default=600, help="dither resolution (600 = 0.042mm dots)")
    ap.add_argument("--gamma", type=float, default=1.0, help="tone curve, tune from the coupon")
    ap.add_argument("--invert", action="store_true", help="fire where chrome stays bare instead")
    ap.add_argument("--strip", action="store_true",
                    help="also write swamp-strip-<dpi> crops for the coupon at " +
                         ", ".join(map(str, STRIP_DPIS)) + " dpi")
    a = ap.parse_args()
    frost = render(a.width, a.height, a.dpi, a.invert, a.gamma)
    write_set("swamp", frost, a.dpi)
    print(f"swamp: {a.width:.1f} x {a.height:.1f} mm, {len(frost[0])} x {len(frost)} px "
          f"at {a.dpi} dpi, gamma {a.gamma}{' (inverted)' if a.invert else ''}")
    if a.strip:
        x0, y0, x1, y1 = STRIP
        for dpi in STRIP_DPIS:
            full = render(a.width, a.height, dpi, a.invert, a.gamma)
            h, w = len(full), len(full[0])
            crop = [row[int(x0 * w):int(x1 * w)] for row in full[int(y0 * h):int(y1 * h)]]
            write_set(f"swamp-strip-{dpi}", crop, dpi, dither_only=True)
            print(f"  strip {dpi} dpi: {(x1 - x0) * a.width:.1f} x {(y1 - y0) * a.height:.1f} mm")


if __name__ == "__main__":
    main()
