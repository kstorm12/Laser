# Test grid: chrome frost (surface mark, no depth)

Goal: find the power x speed that gives an even, matte, cloudy-white mark that **stays inside the
plating**. Decorative chrome is about 1.3 to 5 um over 10 to 25 um of nickel
(`research/community-settings.md`). Nickel does not rust; the carbon steel under it does. A frost
that reaches nickel is fine. One that reaches steel is not.

Run on the **coupon** (junk chrome iron), back cavity, same orientation as the real job.

Fixed for every cell: Loop 1, Frequency 60 kHz, Line distance 0.03 mm, cross hatch 45/135,
at focus.

## Grid: 5 x 4, pens 1 to 20

Cell size 5mm, gap 1.5mm (about 25 x 31mm).

| Pen | Speed 1500 | Speed 2000 | Speed 2500 | Speed 3000 |
|---|---|---|---|---|
| **Power 15** | 1 | 2 | 3 | 4 |
| **Power 20** | 5 | 6 | 7 | 8 |
| **Power 25** | 9 | 10 | 11 | 12 |
| **Power 30** | 13 | 14 | 15 | 16 |
| **Power 40** | 17 | 18 | 19 | 20 |

Columns go left to right, rows go top to bottom on the part. The range follows OMTech's 50W
white/frost chart (15 to 25% at 2000 to 2500 mm/s) and the Thunder nickel-whiten row
(30% at 3000), pushed a step higher because the F290's larger spot puts less energy on each
spot than the F160 those charts assume.

## Build it in EzCad2

1. Draw a 5 x 5mm rectangle at the top left of where the grid will go.
2. Hatch (Ctrl+H): Hatch 1 on, line distance 0.03, angle 45. Hatch 2 on, line distance 0.03,
   angle 135. Mark contour **off** (a contour line shows as a hard edge on a frost). OK.
3. Edit > Array: 4 columns, 5 rows, spacing 6.5mm both ways.
4. Set pens 1 to 20 from the table: Loop 1, Frequency 60, Power and Speed per cell.
5. Assign each square its pen. Save as `test-grids/chrome-frost-grid.ezd`.
6. Red-light preview on the flattest part of the coupon. Mark. One loop per cell, so heat is not
   a concern.

## Read the result

Look at each cell from several angles under a single light (a phone flashlight). For each one:

| What you see | Means |
|---|---|
| Barely visible, only at an angle | Too little: move toward more power or less speed |
| Even matte white/light gray, no lines | **The target** |
| Hatch lines visible | Line distance down to 0.02 for the winner (one change, re-test) |
| Darker gray, brown, or a fingernail catches | Too much: likely through the chrome and into the nickel or deeper |

Then the **rust check** on the coupon, so "stays in the plating" is proven rather than assumed:

1. Pick the 2 to 3 best cells plus the strongest cell (pen 17).
2. Wipe with isopropyl. Put a drop of salt water on each, leave it 24h, wipe off.
3. Any orange or brown spot = through to steel. That cell and everything stronger is out.
4. The winner is the brightest cell that passes. It becomes the `PROVEN` frost row in
   `materials/chrome-plated-steel.md`. Photo to `projects/golf/p790-irons/photos/`.

Frost contrast depends on the finish under it: strong on polished chrome, subtle on satin. Check
the coupon's finish matches the P790's back panel, or the result will not transfer.
