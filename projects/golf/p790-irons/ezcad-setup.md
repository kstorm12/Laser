# P790 face text: EzCad2 setup card (frost)

Status: **STARTING POINT, not yet proven on this machine.** The real numbers come from
`test-grids/chrome-frost-grid.md` on the junk iron. Put the winning cell's Power and Speed into
Pen 1 below and change nothing else.

Technique: **frost**, a single fast pass that leaves a soft matte white/gray mark in the chrome.
There is no recess and no paint. The mark stays inside the plating (chrome over nickel), so no
steel is exposed and nothing rusts. Frost cannot be undone, but it can be made stronger: re-mark
with the same pen before the club moves.

Machine: 50W Raycus Q-switched, F290 lens, at focus (working distance in `machine.md`).

## Pen 1: Frost

| Field | Value |
|---|---|
| Loop count | 1 |
| Speed | 2000 mm/s (grid decides) |
| Power | 25 % (grid decides) |
| Frequency | 60 kHz |
| Start TC / Laser off TC / End TC / Polygon TC | leave at machine defaults |

## Hatch (select the logo, Ctrl+H, or the Hatch button)

| Field | Value |
|---|---|
| Mark contour | **OFF** (a contour line reads as a hard outline on a frost) |
| Hatch 1 | Enable, angle 45, line distance 0.03 mm, bidirectional |
| Hatch 2 | Enable, angle 135, line distance 0.03 mm, bidirectional |
| Edge offset / start / end offset | 0 |

Use the line distance the grid proved. If hatch lines show, try 0.02 on the coupon first.

## Setup, every iron

1. Import the art: File > Import vector, pick `logos/fore-right/fore-right.dxf` (the face text;
   the back panel is an image, see the runbook). Check the size in the property bar matches what
   the script printed. Unlock the aspect ratio only if you mean to.
2. Hatch it (table above), but with **Mark contour ON**: on letters this small the outline keeps
   edges crisp. Assign **Pen 1**.
3. Club in the jig face-up, face level (phone level reads 0), lens at focus. Frost is sensitive to
   focus: an uneven panel gives an uneven cloud.
4. Wipe the face with isopropyl alcohol. Fingerprints and oil mark as blotches.
5. **Red light** (F1): the outline traces on the face. Move/rotate the art in EzCad2 until the
   rows sit parallel to the scoring lines. Glasses on.
6. **Mark** (F2) once.
7. Look before moving the club, under one light from a few angles. Too faint: mark once more with
   the same pen now. Once the club moves, it will not line up again exactly.
8. Save as `designs/p790-fore-right.ezd` after the first iron, so the rest just load it.

## Reading the junk-iron result

| What you see | Change |
|---|---|
| Faint, only shows at an angle | Power up 5 points, or a second loop |
| Even matte white, no lines | Done: mark it `PROVEN` |
| Hatch lines visible | Line distance 0.02 |
| Darker gray or brown, fingernail catches | Too much: power down. Rust-check it (frost grid) |
| Blotchy | Not level, not at focus, or the panel was not clean |
