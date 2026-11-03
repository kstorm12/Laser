# Hatch: recommendations (EzCad2)

Hatch is set **per object** (select it, Ctrl+H or the Hatch button), not per pen. EzCad2 has no
hatch library, so a good hatch lives in the job's `.ezd`; copy a finished object into new jobs
to reuse it. Field names below follow EzCad2 2.14; your build may word some differently.

Status: these are **starting points**. Once one is proven on a material, its line distance and
angles go into that material's row in `materials/`.

## Why line distance matters on this machine

The F290 lens focuses to a spot roughly **0.08 to 0.1 mm** wide (calculated from the lens
and source; the seller lists about 0.1 mm). Line distance is the gap between hatch lines, so:

| Line distance | Overlap | Use |
|---|---|---|
| 0.01 mm | about 90% | Dark marks, very smooth floors. Slow, hot |
| 0.02 mm | about 75% | Deep engraving, paint fill, fine text |
| 0.03 mm | about 65% | General marking, frosting |
| 0.05 mm | about 45% | Coating removal, cleanup / polish passes |
| 0.08 mm+ | lines visible | Fast, textured. Rarely what you want |

Halving the line distance doubles the job time and the heat.

## By goal

| Goal | Line distance | Angles | Type | Contour | Notes |
|---|---|---|---|---|---|
| **Deep engrave / paint fill** (chrome, steel, brass) | 0.02 | Auto rotate per loop, increment 37 deg (or cross 0 / 90) | Bidirectional | ON | Cleanup pass every 5 loops. Rotating angles keep the floor flat instead of grooved |
| **Surface mark / frost** (stainless, chrome, aluminum) | 0.03 | Single, 45 | Bidirectional | ON for text, OFF for big fills | One loop |
| **Coating removal** (powder coat, paint, Cerakote-style) | 0.04 to 0.05 | Cross 0 / 90 | Bidirectional | ON | Then a cleanup pass to brighten the metal underneath |
| **Anodized aluminum** (dye to white) | 0.03 to 0.05 | Single, 45 | Bidirectional | ON | One loop; too dense goes gray |
| **Cleanup / polish pass** | 0.05 | Single, 45 (different from the engrave angles) | Bidirectional | OFF | Low power, high frequency (see the material file) |
| **Dark mark** (Q-switch, limited) | 0.01 | Single, 0 | Bidirectional | OFF | Slow speed, slight defocus. Weaker than a MOPA's black |
| **Fine text** (under 2 mm tall) | 0.02 | Single, along the text (0) | Unidirectional | ON | Unidirectional gives cleaner edges on tiny strokes |
| **Outlines only / very thin strokes** | none | | Ring (offset) or contour only | ON | A ring hatch follows the shape instead of crossing it |
| **Rotary jobs** | per the material | Lines parallel to the rotary axis | Bidirectional | ON | Each line then stays at one height on the curve, so focus is even across the strip. Avoid crosshatch until proven on rotary |

## The dialog, field by field

| Field | Recommended | What it does |
|---|---|---|
| Mark contour | ON for most jobs | Traces the outline. Gives crisp edges, especially on text and logos |
| Contour first | OFF (contour after fill) | Marking the outline last cleans up the hatch line ends |
| Enable (Hatch 1, 2, ...) | Hatch 1 always. Hatch 2 for cross hatch | Each enabled hatch is another full fill at its own angle |
| All calc | ON for logos and text | Hatches the objects as one, so lines line up across letters |
| Type | Bidirectional (default) | Back-and-forth, fastest. **Unidirectional**: cleanest edges, slower. **Ring**: concentric, follows the shape |
| Angle | Per the table | Direction of the hatch lines |
| Auto rotate hatch angle | ON for multi-loop engraving, increment 37 deg | Turns the angle each loop. Any increment that does not divide 180 evenly avoids repeating, so the floor stays smooth |
| Line distance | Per the table | Gap between lines |
| Edge offset | 0 (0.01 to 0.02 if edges look double-burned) | Keeps hatch lines off the contour |
| Start offset / End offset | 0 | Trims line ends. Fix dots at line ends with the pen's timing (Start TC / End TC), not here |
| Line reduction | 0 | Shortens lines; leave alone |
| Average distribute line | ON | Spreads lines evenly so the last line is not squeezed |
| Loop count (in hatch) | 1 | Use the **pen's** Loop count for passes so depth stays in one place |

## Reading the result

| What you see | Hatch fix |
|---|---|
| Visible stripes or grooves in the floor | Lower line distance, or turn on auto rotate |
| Floor black and crusty | Line distance too tight for the power: open to 0.03, or fewer loops |
| Edges ragged or furry | Contour ON; for small text try unidirectional |
| Edge darker than the fill (double burn) | Edge offset 0.01 to 0.02 |
| Dots at the start or end of each line | Pen timing (Start TC / End TC), not hatch |
| Lines misaligned between letters | All calc ON |
| Coating left in patches | Cross hatch 0 / 90, or one more loop |
