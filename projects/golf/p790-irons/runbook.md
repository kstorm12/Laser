# P790 irons: back-cavity engraving

TaylorMade P790, chrome finish. Target: back cavity. Technique: engrave through chrome,
cleanup pass, paint fill.

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
3. [ ] **Test grid** on the coupon: `test-grids/chrome-depth-grid.md`. Pick the winning cell.
4. [ ] **Paint test** on the coupon: degrease (isopropyl), fill with enamel (One Shot or Testors),
       wipe across the recess with a lightly solvent-damp rag or card, cure 24h. Check sharpness.
5. [ ] **Jig**: print it (`jigs/`), check the head sits level (phone level app on the back
       cavity) and does not rock.
6. [ ] **Design**: vector art in `designs/`, sized to the cavity. Import to EzCad2 (DXF or AI),
       hatch it, assign the proven pen, save `designs/p790-<design>.ezd`.
7. [ ] **Dry run** on the coupon in the jig with the real design file.
8. [ ] **First real iron**: the one you hit least (PW or a long iron). Red-light preview, then mark
       in bursts, cool between.
9. [ ] Paint fill, cure, inspect. Then the rest of the set, one at a time.

## Heat discipline (hollow body)

The P790 has SpeedFoam behind the face. Split the loop count into bursts (for example 8 loops as
2 runs of 4) and let the head cool to warm-to-the-touch between them.

## Notes

- Do not engrave the face: thin face, and marking it can affect conformance.
- Modifying the finish may void the TaylorMade warranty.
