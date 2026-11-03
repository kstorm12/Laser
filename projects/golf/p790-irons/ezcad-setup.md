# P790 logo: EzCad2 setup card

Status: **STARTING POINT, not yet proven on this machine.** Run it once exactly as written on the
junk iron. If depth is wrong, change **only Loop count** (more = deeper). Everything else stays.
When it works, mark the rows `PROVEN` in `materials/chrome-plated-steel.md`.

Machine: 50W Raycus Q-switched, F290 lens, at focus (working distance in `machine.md`).

## Pen 1: Engrave (the logo)

| Field | Value |
|---|---|
| Loop count | 5 per run, 4 runs = 20 total, cool between (the test grid sets the real number) |
| Speed | 1000 mm/s |
| Power | 80 % |
| Frequency | 50 kHz (never below: the source's floor) |
| Start TC / Laser off TC / End TC / Polygon TC | leave at machine defaults |

## Pen 2: Cleanup

| Field | Value |
|---|---|
| Loop count | 1 |
| Speed | 3000 mm/s |
| Power | 20 % |
| Frequency | 60 kHz |

## Hatch (select the logo, Ctrl+H, or the Hatch button)

| Field | Value |
|---|---|
| Mark contour | ON (crisp edges) |
| Hatch 1 | Enable, angle 0, line distance 0.02 mm, bidirectional |
| Hatch 2 | Enable, angle 90, line distance 0.02 mm, bidirectional |
| Edge offset / start / end offset | 0 |
| Auto rotate hatch angle (if your version has it) | ON, increment 37 deg. Better than fixed 0/90 for an even floor; if you use it, Hatch 2 can be off |

## Setup, every iron

1. Import the logo: File > Import vector, pick the `.dxf` from `logos/storm/`. Check the size
   in the property bar (about 10 mm tall). Unlock the aspect ratio only if you mean to.
2. Hatch it (table above). Assign **Pen 1**.
3. Duplicate it (Ctrl+C, Ctrl+V, same position). Assign the copy **Pen 2** and set its hatch
   line distance to 0.05 mm, single hatch at 45 deg. Uncheck it in the object list for now.
4. Club in the jig, back panel level (phone level reads 0), lens at focus.
5. **Red light** (F1): the outline traces on the panel. Move/rotate the logo in EzCad2 until it
   sits where you want and is square to the crease. Glasses on.
6. **Mark** (F2) with only Pen 1 checked, 5 loops. Touch the head: if too hot to hold, wait.
   Every 5 loops, run the cleanup copy once (soot left in the recess blocks the next loops).
   Repeat until 20 loops.
7. Check the Pen 2 copy, uncheck Pen 1, mark once (cleanup).
8. Do not move the club until you have looked: if it needs more depth, re-mark Pen 1 with 2 to 3
   loops now. Once the club moves, it will not line up again exactly.
9. Save as `designs/p790-storm.ezd` after the first iron, so the rest just load it.

## Paint fill

1. Wipe with isopropyl alcohol, let dry.
2. Overfill the recess with enamel (One Shot or Testors), using a toothpick or fine brush.
3. Wait 5 to 10 min until it skins, then wipe across the logo with a lint-free rag or a credit
   card wrapped in paper towel, lightly damp with mineral spirits. Wipe across, never along, the
   strokes.
4. Cure 24 h before hitting balls.

## Reading the junk-iron result

| What you see | Change |
|---|---|
| Fingernail barely catches, paint wipes out | Loop count up (20 -> 30) |
| Floor black, crusty, edges ragged | Loop count down, or power to 70 % |
| Uneven depth across the logo | Not level or not at focus: fix the jig, not the settings |
| Stripes in the floor | Turn on auto rotate hatch, or line distance 0.015 |
