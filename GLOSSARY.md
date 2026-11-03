# GLOSSARY.md

Vocabulary for this repo: laser settings, EzCad2 terms, and job workflow. EzCad2's own UI names
are used where one exists, so the docs match what is on screen. LightBurn's name for each is in
`lightburn.md`.

## Machine and optics

#### Field
The 200x200mm square the galvo can reach at the F290 lens's focal plane. Also called work area.

#### Working distance
Measured distance from the bottom of the lens to the work surface when it is in focus. Found by
the focus test in `machine.md`. Every setting assumes this distance unless it lists a defocus.

#### Defocus
Deliberately moving the work off focus (+ = farther from lens). Spreads the spot: softer, wider
marks. Used for annealing and cleanup passes.

## EzCad2 parameters

#### Pen
EzCad2's named parameter set (Pen 0 to 255) assigned to an object. Holds Loop count, Speed,
Power, Frequency. One test-grid cell = one pen.

#### Loop count
EzCad2's name for passes: how many times the pen repeats the object.

#### Speed
Galvo travel speed in mm/s. Slower = more energy per mm = deeper/darker.

#### Power
Percent of the 50W source.

#### Frequency
Pulse rate in kHz. Lower = fewer, harder pulses (deeper, rougher). Higher = more, softer pulses
(smoother, shallower, better for cleanup).

#### Hatch
The fill pattern EzCad2 uses to engrave an area. Set per object, not per pen. Recommendations
by goal: `hatch.md`.

#### Line distance
Hatch spacing in mm. Smaller = denser fill, more time, more heat.

#### Cross hatch
Two or more hatch sets at different angles (45/135) so the fill has no visible grain.

## Workflow

#### Setting
One row in a `materials/*.md` file: pen parameters + hatch + lens + working distance + result.
Status is `PROVEN` (worked on a real piece, photo committed) or `STARTING POINT` (not yet).

#### Test grid
A grid of small squares, each assigned a different pen, used to find a setting on a coupon.

#### Coupon
A scrap test piece of the same material as the real job (a junk chrome iron for the P790 job).

#### Paint fill
Filling an engraved recess with enamel, then wiping the surface clean so paint stays only in the
recess. On chrome irons it also seals the exposed steel against rust.

#### Cleanup pass
A fast, low-power, high-frequency pass after engraving that clears soot and smooths the floor of
the recess before paint fill.
