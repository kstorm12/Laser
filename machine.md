# Machine

| Fact | Value |
|---|---|
| Model | OMTech FMM-5RW2-US, split fiber marker |
| Source | Raycus 50W, Q-switched (not MOPA), 1064nm |
| Lens | F290 |
| Field | 200 x 200mm (7.9 x 7.9in) |
| Software | EzCad2 (Windows), primary. LightBurn galvo planned, side by side: `lightburn.md` |
| Accessories | Rotary axis |
| Working distance | **TBD: run the focus test below and record it here** |
| Raycus frequency range | **50-100 kHz if the source is an RFL-P50QB** (Raycus manual: never mark outside it). Confirm the model on the source's label |

## Focus test (do this first, once)

1. Put a flat scrap of stainless or a painted metal plate on the bed.
2. Measure from the bottom of the lens to the plate with a ruler. The two red pointer dots (if the
   machine has dual pointers) converge at focus; use that as the first guess.
3. In EzCad2 draw a 5mm filled square. Pen: 50% power, 1000mm/s, 50kHz, loop 1, hatch 0.05.
4. Mark it. Raise the column 1mm, slide the plate over, mark again. Repeat for -3 to +3mm.
5. The square that is brightest, crispest, and loudest (sharp crackle) is focus. Measure lens
   bottom to plate there and record it above.

Glue a printed or cut **focus gauge** (a block exactly the working distance tall) to the machine
once known, so every job starts at focus in seconds.

## Safety

- OD5+ glasses rated for 1064nm, every time. The beam is invisible.
- Fume extraction on for chrome and coatings: lasering chrome plating can release hexavalent
  chromium. Vent outside.
- Never leave a running job.
