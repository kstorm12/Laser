# Laser: settings library and job files

Personal project. Vault: **The Vault**, page `[[Laser Engraving]]`. Commit rule: global
`~/.claude/CLAUDE.md` (wait for "commit, sync, and push", or `/cs` / `/csp`).

**GitHub-only by design** (`kstorm12/Laser`): no Gitea mirror, unlike most personal repos. Do not
add one in any remote-wiring or mirror-consistency pass.

Not a code project: no build, no tests, no `typecheck`/`test`/`lint` declared. The deliverables
are proven laser settings, design files, and printable jigs.

## Machine (details in `machine.md`)

OMTech FMM-5RW2-US: 50W **Raycus Q-switched** fiber (1064nm), **F290 lens**, 200x200mm field,
rotary included. Driven by **EzCad2 on Windows** only, for now. No LightBurn license.

**Frequency floor: 50 kHz** (RFL-P50QB range is 50-100 kHz; below it overdrives the source). Most
community recipes say 20-30 kHz because they are for other sources: never copy those.

Q-switched, not MOPA: no adjustable pulse width, no color marking on stainless, weak black
annealing. Do not suggest MOPA-only settings.

## Layout

| Path | What |
|---|---|
| `machine.md` | Machine facts + calibration results (working distance, field check) |
| `materials/<material>.md` | **The settings library.** One file per material, proven settings only marked `PROVEN` |
| `materials/_template.md` | Copy this for a new material |
| `research/community-settings.md` | Sourced community/manufacturer settings for every material, with confidence. Starting points to feed test grids, never `PROVEN` |
| `test-grids/` | How to build a parameter test grid in EzCad2, plus the grid parameter tables |
| `projects/<category>/<job>/` | One folder per job, grouped by category (e.g. `golf/p790-irons`): `runbook.md`, `designs/` (vector art + `.ezd`), `photos/` |
| `logos/<name>/` | Reusable art. `storm/make_logo.py` regenerates the STORM bolt-T wordmark as SVG + R12 DXF (`--width MM`); needs only fontTools |
| `jigs/` | FreeCAD source (`.FCStd`) + exported `.stl` for printed fixtures |

## Rules

- **EzCad2 has no material library.** Pen parameters live inside each `.ezd` file, so the
  markdown in `materials/` is the source of truth. A setting is `PROVEN` only after it worked on
  a real piece and the photo is committed. Everything else is `STARTING POINT`.
- Every setting row names the lens (F290) and working distance. A setting without them is not
  reusable.
- Never test a setting on the customer piece (the P790s count). Test on a coupon first.
- Files reach the Windows/EzCad2 machine by **LocalSend**, not git. This repo on Omarchy is the
  master copy: an `.ezd` edited on Windows gets sent back and committed here.
