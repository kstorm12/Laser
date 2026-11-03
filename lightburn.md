# LightBurn (galvo): setup and EzCad2 translation

LightBurn runs side by side with EzCad2 on the laser PC. **EzCad2 stays primary** until LightBurn
has reproduced a `PROVEN` row on a coupon; then decide per job. LightBurn drives this machine's
BJJCZ (JCZ) board directly and needs the **Galvo** license, which is separate from the
DSP/G-code one.

The settings in `materials/` are physics (power, speed, frequency, passes, spacing), so a row
transfers between the two programs unchanged. Only the names differ (table below).

## Before installing: back up the EzCad2 calibration

The OMTech USB stick and the EzCad2 folder hold this machine's factory calibration. Copy these
into `machine-config/` in the repo (then `save.bat`), before anything changes:

| File | Where | Why |
|---|---|---|
| `markcfg7` (sometimes `markcfg0`) | EzCad2 folder `plug\` | Field size, galvo direction, lens correction, laser type. LightBurn imports it |
| `*.cor` | EzCad2 folder (if present) | Lens correction table for the F290 |

`markcfg7` has no file extension. If it is missing, the values can be typed in by hand from
EzCad2's Param (F3) screens; photograph every tab first.

## Install and add the device

1. Run the LightBurn installer and tick **Install EZCad2 driver**. Without it LightBurn cannot
   see the galvo.
2. **Close EzCad2.** Only one program can hold the laser's USB connection at a time.
3. Laser window > Devices > **Create Manually** > **JCZFiber**, connection **USB**.
4. When asked for an EzCad config, select the `markcfg7` copy. LightBurn imports the lens
   correction from it if the file contains one.
5. **Check the field size** after import: it must read 200 x 200mm (F290). Imports have been
   reported reading the wrong size; fix it in Device Settings if so.
6. Source settings: Q-switched (no MOPA pulse width), frequency limits 50 to 100 kHz.
7. Verify with the focus-test square from `machine.md`: same pen values in both programs, mark
   one square from each side by side. They should look identical. If LightBurn's is offset or
   scaled, reboot the laser and LightBurn and re-import `markcfg7` (a known fix).

Record the result here and in `machine.md` once done.

## Names: EzCad2 to LightBurn

| Repo / EzCad2 term | LightBurn galvo term | Notes |
|---|---|---|
| Pen (0 to 255) | Layer (color) / Cut Setting | One layer = one set of parameters |
| Loop count | Number of Passes | |
| Speed mm/s | Speed mm/s | |
| Power % | Power % | |
| Frequency kHz | Frequency kHz | Keep 50 to 100 |
| Hatch (per object) | Fill mode (per layer) | In LightBurn hatch belongs to the layer, not the object |
| Line distance | Interval | mm |
| Hatch angle | Angle | |
| Cross hatch | Cross-Hatch | |
| Rotate angle each loop | Angle increment (per pass) | |
| Contour on (outline the hatch) | Add a Line sub-layer, or a second Line layer | |
| Red light (F1) | Frame (Preview / red dot) | |
| `.ezd` job file | `.lbrn2` project file | Save next to the `.ezd` in `designs/` |
| Test grid (built by hand) | Material Test generator | Same grid idea, generated for you |

Field names follow LightBurn 1.x/2.x galvo docs; confirm against your build's Cut Settings
window and correct this table if it differs.

## Rotary

LightBurn has its own rotary settings for galvo. **Do not reuse EzCad2's numbers blindly**: redo
the calibration test in `rotary.md` once in LightBurn and record its values in a LightBurn column
there.

## Material library (later)

LightBurn can save cut settings into a material library (`.clb`). Once rows are `PROVEN`, a
library can be generated from `materials/*.md` so the PC has every setting one click away. Not
built yet: `materials/` stays the source of truth either way.
