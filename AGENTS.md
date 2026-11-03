# AGENTS.md

Guidance for any coding agent (opencode, Claude Code, others) working in this repo. Layout and
the human workflow are in `README.md`; vocabulary is in `GLOSSARY.md` (use its words: Pen, Loop
count, Line distance, Coupon, `PROVEN` / `STARTING POINT`).

This is a **settings library**, not an app: no build, no tests, no lint. The deliverables are
laser settings, vector art, EzCad2 job files, and printable jigs.

## The machine (every setting assumes it)

OMTech FMM-5RW2-US: 50W **Raycus Q-switched** fiber, 1064nm, **F290 lens**, 200x200mm field,
rotary. Run from **EzCad2 on a Windows PC**; files reach it by LocalSend, and this repo is the
master copy. Facts and calibration live in `machine.md`.

- **Frequency 50 to 100 kHz.** That is the RFL-P50QB source's rated range; below 50 kHz
  overdrives it. Community recipes at 20 to 30 kHz were written for other sources: translate them
  to 50 kHz or higher.
- **Q-switched**, so keep to engraving, coating removal, frosting, and light marking. Color on
  stainless, deep black anneal, and pulse-width settings are MOPA features this source lacks.
- **F290 cuts shallower per loop** than smaller lenses. Scale another lens's loop count by
  (290 / their lens) squared.

## Settings rules

- `materials/<material>.md` is the source of truth for settings (EzCad2 has no material
  library; pens live inside each `.ezd`). One file per material, from `materials/_template.md`.
- Every row names lens, working distance, and status. New rows start as `STARTING POINT`; only
  Kyle promotes a row to `PROVEN`, after it worked on a real piece and the photo is committed.
- `research/community-settings.md` is sourced input for starting points, never proof.
- Tune one variable at a time, usually Loop count, so a result is traceable.
- Test on a coupon of the same material before the real piece.

## Materials that are off-limits

PVC, vinyl, and PTFE release toxic gas under a laser. Decline settings for them and say why.

## Writing files

- EzCad2 imports **DXF** reliably: closed polylines in mm, R12. `logos/storm/make_logo.py` holds
  a minimal writer (`write_dxf`) to reuse. Shapes must not overlap: EzCad2 hatches even-odd, so
  overlaps engrave as holes.
- Python helpers stay stdlib plus fontTools, run with `python3`.
- Docs: American English, ISO dates, no em dashes.

## Remote

`origin` is GitHub `kstorm12/Laser` only, with no Gitea mirror, by design. Keep it that way.
