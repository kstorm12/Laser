# Rotary: setup and calibration (EzCad2)

Status: **not yet calibrated on this machine.** Menu and field names below come from Cloudray's
EzCad2 rotary guide (same BJJCZ EzCad2 build family); your version may word them slightly
differently. Record the calibrated values in the table at the bottom once found.

Rotary type: **TBD (chuck or roller).** Chuck (jaws) for small round parts held at the end:
rings, pens, flashlights, handles. Roller for tumblers and bottles that sit on top.

## 1. Hardware

1. **Machine and control box powered OFF** before plugging or unplugging the rotary. Hot-plugging
   a stepper can kill its driver.
2. Plug the rotary into the **4-pin round port** on the control unit (OMTech manual).
3. Place the rotary so its axis runs **exactly parallel to the X or Y edge of the field**. Note
   which one: EzCad2 needs to know (X or Y axis, below). Square it against the bed's edge or a
   printed square.
4. Find the **stepper driver** (a small box with DIP switches, inside the control box or on the
   rotary). Its label has a table: the switch positions set **pulses per revolution**
   (subdivision, for example 6400, 12800, 25600). Write down what it is set to. Change the switches
   only with power off, and only together with the EzCad2 value.
5. Power on.

## 2. EzCad2 parameters

Two entry points, same parameter set:
- **Text:** create the text, fill (hatch) it, then **Laser > Rotate Text Mark**.
- **Vector art (DXF, logos):** import, hatch, then **Laser > Split Mark2**.

| Field | Set to | Why |
|---|---|---|
| Enable extended axis | ON | Turns the rotary on |
| Axis | X or Y, whichever the rotary is parallel to (step 1.3) | Wrong axis = rotary spins while the design marks flat |
| Reverse | OFF to start; toggle if the design comes out mirrored | Direction depends on which end the motor is |
| Pulses per revolution | **The driver's DIP-switch value** (step 1.4). Typical 12800 or 25600 | Must match the hardware exactly |
| Enable rotary | ON | |
| Gear ratio | The rotary's reduction ratio (on its label or spec, often 1 for direct drive) | |
| Workpiece diameter | **Chuck:** the part's diameter at the design (calipers). **Roller:** see below | Wrong diameter = design stretched or squashed |
| Split mark | ON (Split Mark2) | Marks in strips, rotating between them |
| Split size | From the table below, 1 to 5 mm | Smaller = sharper but slower |

### Split size by part diameter

Each strip is flat while the part is curved, so the strip's edges drift out of focus. Keep that
drift under about 0.1 mm: split size is about the square root of (0.4 x diameter).

| Part diameter | Split size |
|---|---|
| 10 mm (pen, ring) | 2 mm |
| 25 mm (flashlight, handle) | 3 mm |
| 50 mm | 4.5 mm |
| 75 mm+ (tumbler) | 5 mm |

### Roller rotaries: which diameter

With rollers, the part turns because the drive roller turns it, so its rotation per motor turn
depends on the roller, not the part. The usual approach is to enter the **drive roller's
diameter** as the workpiece diameter; then one setting works for any part size. Confirm with the
calibration test below; if it fails, fall back to the part's diameter and calibrate per part.

## 3. Calibration test (do once, before any real part)

Use a cheap part of known diameter: scrap steel or aluminum tube, an old powder-coated tumbler,
a painted metal can. Never PVC pipe (chlorine gas). Measure it with calipers.

1. Draw a **20 x 20 mm square outline** (no hatch). Light pen: 30% power, 1000 mm/s, 50 kHz,
   loop 1, so it barely frosts.
2. Set focus to the **top** of the part (the line directly under the lens).
3. Split Mark2 with the parameters above. Mark.
4. Measure the square **around the curve** (flexible tape, or a strip of paper wrapped on and
   marked): the side that wraps should be 20 mm.
5. Fix pulses per revolution if it is off:

   **new pulses per revolution = old x (20 / measured)**

   Example: measured 18 mm at 12800 -> 12800 x 20 / 18 = 14222.
   If the result is far from a DIP-switch value, the hardware setting and EzCad2 disagree, or the
   gear ratio is wrong: recheck those before trusting the number.
6. Repeat until it measures 20 mm, then mark a **360 degree** test: a ring line all the way round
   with a tick at the start. It should close exactly on the tick.
7. Mirrored text = toggle Reverse. Gaps or overlaps between strips = pulses per revolution still
   off.

## 4. Every rotary job

1. Part in the chuck or on the rollers, top line **level** (phone level on the part).
   **Tapered tumblers:** shim the low end of the rotary until the top line under the lens is
   level, and use the diameter at the middle of the design.
2. Focus to the top of the part.
3. Red light (F1) to check position along the axis. Rotation start point is wherever the part
   sits now: turn the part by hand (power off, or with the jog control if your EzCad2 shows one)
   so the spot you want faces up.
4. Mark (F2) through Rotate Text Mark or Split Mark2.

## 5. Troubleshooting

| Symptom | Cause |
|---|---|
| Rotary does not move | Extended axis not enabled, wrong axis selected, cable not seated (power off to reseat) |
| Design stretched or squashed around the part | Diameter wrong, or pulses per revolution / gear ratio wrong |
| Gaps or overlaps between strips | Pulses per revolution off (calibrate), or split size too big |
| Strip edges blurry or lighter | Split size too big for the diameter, or focus not at the top line |
| Design mirrored | Toggle Reverse |
| Rotary jerks at start/stop | Speed or acceleration too high for a heavy part; lower them if your version exposes them |

## Calibrated values (fill in)

| Field | Value | Date |
|---|---|---|
| Rotary type (chuck / roller) | | |
| Rotary parallel to (X / Y) | | |
| Driver DIP pulses per revolution | | |
| Gear ratio | | |
| Calibrated pulses per revolution | | |
| Reverse | | |
| Roller diameter (roller rotary) | | |
