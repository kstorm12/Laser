# Laser

Proven settings, art, and job files for an **OMTech 50W fiber laser** (Raycus Q-switched,
F290 lens, 200x200mm field, EzCad2). The goal: every material gets dialed in once, written down,
and reused.

## Layout

| Path | What |
|---|---|
| `machine.md` | Machine facts, focus test, safety. **Start here.** |
| `hatch.md` | Hatch recommendations by goal, every EzCad2 hatch field explained |
| `rotary.md` | Rotary attachment: hookup, EzCad2 parameters, calibration test |
| `materials/` | The settings library, one file per material. Copy `_template.md` for a new one |
| `test-grids/` | How to build a parameter test grid in EzCad2 to find a setting |
| `research/community-settings.md` | Settings other people report, with sources and confidence |
| `projects/<category>/<job>/` | One folder per job: `runbook.md`, `designs/`, `photos/` |
| `logos/` | Reusable art, plus scripts that generate it |
| `jigs/` | 3D-printable fixtures (FreeCAD source + STL) |
| `GLOSSARY.md` | What the terms mean (Pen, Loop count, Coupon, ...) |
| `AGENTS.md` | Instructions for AI coding agents |

## How a material gets dialed in

1. Run the focus test in `machine.md` (once per machine).
2. Get a coupon: scrap of the same material.
3. Take starting values from `materials/` or `research/`, build a test grid, mark it.
4. Pick the winning cell, try it on the coupon for real, photo it.
5. Record it in `materials/<material>.md` as `PROVEN`.

Settings marked `STARTING POINT` have not been proven on this machine yet.

## Machine limits worth knowing

- Frequency stays **50 to 100 kHz** (the Raycus source's range). Many online recipes say 20 to
  30 kHz; those are for other lasers.
- Q-switched, not MOPA: no color marking on stainless, weak black marks.
- Fiber lasers are poor on wood and clear acrylic. **Never laser PVC, vinyl, or PTFE** (toxic gas).

## Current job

`projects/golf/p790-irons/`: STORM logo on the back panel of 2019 TaylorMade P790 irons,
engraved through the chrome and paint-filled. EzCad2 card: `ezcad-setup.md`.

## Regenerating the logos

```bash
cd logos/storm
python3 make_logo.py --width 32     # STORM wordmark variants, SVG + DXF
python3 make_emblem.py --height 10  # emblem variants, SVG + DXF
```

Needs Python 3 and `fontTools`.

## Safety

OD5+ glasses rated for 1064nm every time, fume extraction on (chrome and coatings), never leave
a running job.
