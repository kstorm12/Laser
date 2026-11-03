# Chrome-plated carbon steel (golf irons)

Thin chrome (over nickel) on carbon steel. TaylorMade P790 is chrome over forged 8620.

**Gotchas**
- Plating stack: chrome about 1.3 to 5 um over nickel about 10 to 25 um. Nickel does not rust, so
  a mark that stays in the plating (frost) needs no fill. Only a mark that reaches steel does.
- Once the laser cuts through the plating, the steel underneath **will rust**. Every
  engraving deep enough to show steel must be paint-filled (or sealed).
- The plating is thin; most of the depth is in the steel. Depth for paint fill is a judgment call:
  enough that a fingernail catches, not so much that the floor turns rough and black.
- Hollow-body irons (P790) have foam behind the face: run in short bursts and let the head cool.
  If it is too hot to hold, wait.

Lens: F290 · Working distance: TBD (see `machine.md`)

| Goal | Power % | Speed mm/s | Freq kHz | Loop | Line dist mm | Hatch angles | Defocus | Status | Result / photo |
|---|---|---|---|---|---|---|---|---|---|
| Engrave for paint fill | 80 | 1000 | 50 | 20 (4 x 5), grid decides | 0.02 | rotate per loop (or 0 / 90), contour on | 0 | STARTING POINT | grid: `test-grids/chrome-depth-grid.md` |
| Cleanup pass | 20 | 3000 | 60 | 1 | 0.05 | 45 | 0 | STARTING POINT | |
| Surface mark, no depth (frosted) | 25 | 2000 | 60 | 1 | 0.03 | 45 / 135, contour off | 0 | STARTING POINT | P790 card: `projects/golf/p790-irons/ezcad-setup.md`; grid: `test-grids/chrome-frost-grid.md` |

Find the real numbers on the coupon: `test-grids/chrome-frost-grid.md` (frost) or
`test-grids/chrome-depth-grid.md` (engrave for paint fill).

## Log

- 2026-11-03: starting points from generic 50W Q-switched community values. Nothing tested yet.
- 2026-11-03: frequency 30 -> 50 kHz (RFL-P50QB floor), loops 10 -> 20 (F290 cuts shallower per
  loop than the F160/F254 lenses most recipes assume). See `research/community-settings.md`.
- 2026-11-03: P790 job switched to frost (no paint fill). Frost row moved to 25% / 2000 / 60 kHz,
  cross hatch, contour off: middle of the OMTech 50W white/frost chart, one step up for the F290.
