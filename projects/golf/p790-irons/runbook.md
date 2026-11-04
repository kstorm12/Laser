# P790 irons: back-cavity engraving

TaylorMade P790, chrome finish. Target: back cavity. Technique: **frost**, a single-pass
surface mark that stays in the plating. No recess, no paint fill. (Changed 2026-11-03 from engrave +
paint fill: a recess through the chrome exposes steel that rusts unless filled.)

Generation: **2019 P790**. Zone: **lower back panel** (below the crease, between the TM logo and
the hosel). Design: back panel = **swamp scene with an alligator** (`logos/swamp/`); face = **"FORE RIGHT"
chalkboard lines** (`logos/fore-right/`).

| Club | 3i | 4i | 5i | 6i | 7i | 8i | 9i | PW |
|---|---|---|---|---|---|---|---|---|
| Loft | 19 | 21 | 23.5 | 26.5 | 30.5 | 35 | 40 | 45 |
| Lie | 60.5 | 61 | 61.5 | 62 | 62.5 | 63 | 63.5 | 64 |

Stock 2019 spec (retailer charts), not measured. Matters for the jig: with the back cavity facing
up, the shaft points **down** from horizontal by roughly loft minus the back's taper, so 19 to 45
degrees across the set.

## Steps (each one done before the next starts)

1. [ ] **Focus test**: record working distance in `machine.md`.
2. [ ] **Coupon**: buy a junk chrome iron (used golf shop, about $5).
3. [ ] **Test grid** on the coupon: `test-grids/chrome-frost-grid.md`. Pick the winning cell.
4. [ ] **Rust check** on the coupon: salt-water drop on the winning cells, 24h (frost grid). The
       winner must show no rust.
5. [ ] **Jig**: print it (`jigs/`), check the head sits level (phone level app on the back
       cavity) and does not rock.
6. [ ] **Design**: vector art in `designs/`, sized to the cavity. Import to EzCad2 (DXF or AI),
       hatch it, assign the proven frost pen, save `designs/p790-<design>.ezd`.
7. [ ] **Dry run** on the coupon in the jig with the real design file.
8. [ ] **First real iron**: the one you hit least (PW or a long iron). Red-light preview, then mark
       once.
9. [ ] Inspect under one light from several angles. Then the rest of the set, one at a time.

## Back panel: swamp scene (image frost)

A made-up swamp at dusk: low sun, cypress trees with Spanish moss, cattails, lily pads, and an
alligator gliding through the sun's reflection. Frost is the light (sky, water, wake); bare
chrome is the dark (silhouettes). Art: `logos/swamp/` (generated, stdlib Python).

1. [ ] **Coupon strip first.** `python3 make_swamp.py --strip` also writes
       `swamp-strip-<dpi>-dither.png` at 400, 500, 600, 800 dpi: the gator, wake, and sun
       reflection, about 15.6 x 6.2mm each. Import all four (see step 3) as a 2 x 2 grid on the junk iron's
       back, each at its own Fixed DPI, same frost pen. Mark once.
       - Pick the DPI where the sky glow looks smooth and the gator's ridges stay sharp. Too low:
         visible dots. Too high: dots merge into flat frost and mid-tones wash out.
       - Tones: too bright overall, regenerate with `--gamma 1.3`; too dim, `--gamma 0.75`.
         Re-mark one strip to confirm before the real club.
       - Frost reads darker than chrome on this finish: regenerate with `--invert`.
       Why dots, not one pen per tone: frost brightness jumps over a narrow power range and
       burns through the plating above it. Dot density gives smooth tones at one proven,
       rust-checked setting.
2. [ ] Measure the back panel's usable area. Regenerate (Omarchy, `cd logos/swamp`):
       `python3 make_swamp.py --width <mm> --height <mm> --dpi <winner> --gamma <winner>`. The panel
       is not a rectangle: trim the image's corners to the panel's shape in EzCad2/LightBurn, or size it
       to fit inside.
3. [ ] Import the **pre-dithered** `swamp-dither.png` (black = fire):
       - EzCad2: File > Import bitmap. Bitmap parameters: **Fixed DPI = the winner**, Dither **off** (it is
         already dithered), Invert off, Bidirectional scan on. Field names vary by build.
       - LightBurn: Image layer, mode **Pass-Through**, DPI = the winner. (Or `swamp-gray.png` with
         LightBurn's own Jarvis dither, same DPI, to compare.)
4. [ ] Real club: jig level, at focus, red-light the image's bounding box, mark once.

## Face: "FORE RIGHT" chalkboard lines (one club first)

Rows of "FORE RIGHT" in a handwritten font across the face, trailing off at the toe end like
lines written on a chalkboard. Art: `logos/fore-right/` (Gochi Hand, OFL).

1. [ ] Measure the club's face: the usable width across the scoring lines and the height the rows
       should fill. Regenerate the art to fit (Omarchy, `cd logos/fore-right`):
       `python3 make_fore_right.py --width <mm> --height <mm> --rows 10`. Letters under about
       1.5mm tall get hard to read: use fewer rows rather than smaller ones.
2. [ ] Coupon: frost the art on the junk iron's face with the proven frost pen (frost grid).
       The face is blasted/satin, so contrast will be lower than on the back. Check it is
       readable at arm's length before going further.
3. [ ] Hatch: same as the frost card, but **Mark contour ON**. On letters this small, the outline
       keeps edges crisp.
4. [ ] One club (the one you hit least), in the jig face-up and level. Red-light, mark once,
       look, then decide on the rest.

## Heat (hollow body)

The P790 has SpeedFoam behind the face. A single frost pass puts in little heat, but if a second
loop is needed, let the head cool to warm-to-the-touch first.

## Notes

- Face: **frost only, never a depth engrave.** The P790 face is a thin forged insert. Frost is
  microns deep and does not weaken it, but markings in the impact area are likely
  non-conforming: a marked club is for casual rounds, not tournament or handicap play.
- Modifying the finish may void the TaylorMade warranty.
