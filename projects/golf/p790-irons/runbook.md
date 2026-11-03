# P790 irons: back-cavity engraving

TaylorMade P790, chrome finish. Target: back cavity. Technique: **frost**, a single-pass
surface mark that stays in the plating. No recess, no paint fill. (Changed 2026-11-03 from engrave +
paint fill: a recess through the chrome exposes steel that rusts unless filled.)

Generation: **2019 P790**. Zone: **lower back panel** (below the crease, between the TM logo and
the hosel). Design: **STORM wordmark, T as a lightning bolt** (`logos/storm/`, variant TBD).

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

## Heat (hollow body)

The P790 has SpeedFoam behind the face. A single frost pass puts in little heat, but if a second
loop is needed, let the head cool to warm-to-the-touch first.

## Notes

- Do not engrave the face: thin face, and marking it can affect conformance.
- Modifying the finish may void the TaylorMade warranty.
