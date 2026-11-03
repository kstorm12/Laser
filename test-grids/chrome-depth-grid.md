# Test grid: chrome depth (for paint fill)

Goal: find the speed x passes combo that gives a clean, paint-holding recess on chrome.
Run on the **coupon** (junk chrome iron), back cavity, same orientation as the real job.

Fixed for every cell: Power 85%, Frequency 50kHz (the source's floor), Line distance 0.02mm, cross hatch 45/135,
at focus.

## Grid: 5 x 5, pens 1 to 25

Cell size 5mm, gap 1.5mm (whole grid about 31 x 31mm, fits the back of most irons).

| Pen | Speed 800 | Speed 1000 | Speed 1200 | Speed 1500 | Speed 2000 |
|---|---|---|---|---|---|
| **Loop 5** | 1 | 2 | 3 | 4 | 5 |
| **Loop 10** | 6 | 7 | 8 | 9 | 10 |
| **Loop 20** | 11 | 12 | 13 | 14 | 15 |
| **Loop 30** | 16 | 17 | 18 | 19 | 20 |
| **Loop 40** | 21 | 22 | 23 | 24 | 25 |

Columns go left to right, rows go top to bottom on the part.

## Build it in EzCad2

1. Draw a 5 x 5mm rectangle at the top left of where the grid will go.
2. Select it, Hatch (Ctrl+H): enable Hatch 1, line distance 0.02, angle 45. Enable Hatch 2, line
   distance 0.02, angle 135. Leave Mark contour off. OK.
3. Edit > Array: 5 columns, 5 rows, spacing 6.5mm both ways (5mm cell + 1.5mm gap).
4. Set pens 1 to 25 in the Pen panel (right side) from the table above: Power 85, Frequency 50,
   Speed and Loop count per cell. Double-click a pen to edit its parameters.
5. Assign each square its pen: select square, click the pen.
6. Save as `test-grids/chrome-depth-grid.ezd`.
7. Red-light preview to check the grid sits on the flattest part of the coupon. Mark.

Let the part cool between rows if it gets hot (pause and resume). Rows 30 and 40 are long: mark
them in chunks.

## Read the result

For each cell: does a fingernail catch? Is the floor bright gray (good) or black and crusty
(too much)? Is the edge crisp? Then:

1. Run the cleanup pass (see `materials/chrome-plated-steel.md`) over the best 3 to 4 cells.
2. Paint-fill those cells, wipe, let cure, and check which ones held clean, sharp paint.
3. The winner becomes the `PROVEN` row. Photo to `projects/golf/p790-irons/photos/`.
