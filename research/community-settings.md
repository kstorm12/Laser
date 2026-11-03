# Community and manufacturer settings research

Researched 2026-11-03 for the OMTech FMM-5RW2-US (50W Raycus Q-switched, 1064nm, F290, 200x200mm,
EzCad2). Every number below is **STARTING POINT** for this machine (see `GLOSSARY.md`). Nothing here
is `PROVEN` until it works on a coupon and the photo is committed to `materials/`.

Vocabulary matches EzCad2: Power %, Speed mm/s, Frequency kHz, Loop count, Line distance mm.
Where a source gives DPI/LPI it is converted (1270 DPI = 0.02mm, 1016 = 0.025mm, 635 = 0.04mm,
504 = 0.05mm).

## Summary

- **Frequency floor is the biggest finding.** The Raycus RFL-P50QB datasheet rates the 50W source
  at **50 to 100 kHz** (1 mJ at 50 kHz, 120 to 150 ns pulse). OMTech's own listing for this SKU
  also gives 50 to 100 kHz (seen in a search excerpt; the page itself blocked fetching). Most
  community deep-engrave recipes (and OMTech's own generic blog) say 20 to 30 kHz, which is below
  this source's rated range. Other "Raycus 50W" units (Gweike G2 Pro: 20 to 200 kHz) are a
  different source variant, so their low-kHz recipes do not transfer.
- **Well established:** deep engraving on a 50W Q-switch = high power (80 to 95%), moderate speed
  (500 to 1500 mm/s), dense Line distance (0.015 to 0.03mm), **many** Loops (OMTech: 5 to 30 on
  F160; one well-documented coin job: 256 loops for about 0.8mm on F210), periodic cleanup passes,
  and rotating hatch angles.
- **Well established:** cleanup pass = low power, fast, high frequency. OMTech's chart
  (10 to 15%, 2000 mm/s, 60 kHz) matches Kyle's 20% / 3000 / 60 kHz closely.
- **Varies a lot:** power % between units and source brands, usable frequency range, and above
  all **lens focal length**. An F290 spot has roughly 3.3x less area density of energy than F160
  and 1.3x less than F254, so recipes written for F160 (most charts) under-deliver on Kyle's
  machine.
- **Thin data:** no source gives tested chrome-iron paint-fill numbers for a Q-switched 50W.
  Chrome golf work online is almost all MOPA marketing with no numbers.
- **Q5 answer:** power, speed, Line distance and the cleanup pass are in line with community
  practice. Change **frequency 30 to 50 kHz** (verify the source label first), expect **10 loops
  to be too shallow** on F290 (grid 10 / 20 / 40), interleave the cleanup every 5 loops instead of
  only at the end, and rotate the hatch angle per loop instead of fixed 0/90.
- `machine.md`'s focus-test pen also uses 30 kHz; same issue (not edited here).

## Machine facts that ground the frequency advice

| Fact | Value | Source |
|---|---|---|
| Raycus RFL-P50QB repetition rate | 50 to 100 kHz | [Raycus 10Q/20QE/30Q/50QB User's Guide V2.1, Table 2](https://cdn.shopify.com/s/files/1/0651/8158/1563/files/RFL-P10Q_20QE_30Q_50QB.pdf) |
| Single pulse energy | 1 mJ @ 50 kHz | same |
| Pulse duration | 120 to 150 ns @ 50 kHz (fixed, not adjustable) | same |
| Beam quality / beam diameter | M2 < 1.6 / 6 to 8 mm | same |
| Power tunability | 10 to 100%; "actual laser power may not be strictly linear with the setting value" | same, section on DB25 PIN control |
| General Raycus rule | "Make sure the pulse repetition rate higher than 20kHz" (applies to the whole family; the 50QB's own rated range starts at 50) | same, section 1.3 |
| FMM-5RW2-US frequency range | 50 to 100 kHz (search excerpt of the OMTech product page; direct fetch blocked) | [OMTech product page](https://omtech.com/products/50w-fmm-5rw2-us) |
| Same-maker 50W, different variant | Gweike G2 Pro 50W Raycus, 20 to 200 kHz, 210mm lens | [LightBurn forum, Shellhopper](https://forum.lightburnsoftware.com/t/coin-engraving-settings-50-watt-gweike-fiber/166363) |
| Seller claims for "Raycus 50W QB" units | 30 to 60 kHz, 40 to 60 kHz (seller listings, not Raycus; secondhand) | eBay listings surfaced by search, not cited as data |

Why it matters: Q-switched pulse energy is capped near 1 mJ. Below the rated rate the source
cannot store more energy per pulse in a controlled way, so either average power falls (roughly
1 mJ x 30 kHz = 30W at most) or the source runs outside its spec. Neither helps depth. One
LightBurn user (gamerpaddy) reports the same thing empirically on a 30W unit: below the "charge
point" frequency, pulse energy does not rise
([thread](https://forum.lightburnsoftware.com/t/effect-on-different-lenses-for-fiber-lasers/135818)).
**Action:** read the model off the Raycus source label and record it in `machine.md`. If it says
RFL-P50QB (or the EzCad2 config caps at 50 to 100), keep every pen at 50 kHz or above.

## Transferability (question 4)

Concrete answer, by parameter, for a community recipe moving to Kyle's machine:

| Parameter | Transfers? | Why | What to do |
|---|---|---|---|
| Speed, Line distance, hatch pattern | **Yes, directly** | Galvo motion is geometry; same EzCad2 meaning on every JCZ board | Use as given |
| Power % | **Within about +/-20%** | Raycus says power vs setting is not linear; sources age; different brands at "50W" differ | Grid power in 10% steps around the recipe |
| Frequency | **Only within the same source model** | 50QB is 50 to 100 kHz; JPT, Hans, MAX and other Raycus variants have different ranges and pulse widths | Re-pick inside your own range; 50 kHz is the deep-engrave floor here |
| Loops (depth) | **Poorly across lenses** | Spot diameter scales with focal length; energy per area scales with 1/f squared | First guess: multiply loops by (290 / their f) squared, then grid |
| Focus | **Never** | Every unit's working distance differs; must be measured | Run the `machine.md` focus test |
| EzCad2 version | Minor | Same pen fields; later builds add options (auto-rotate hatch, wobble) | Check your Hatch dialog |

Lens math (my calculation, approximate; assumes the 7mm Raycus beam reaches the lens without an
expander, M2 1.6): focused spot is about 50 um on F160, 65 um on F210, 79 um on F254, **90 um on
F290**. Relative energy per area at the same pen: F160 = 3.3x, F210 = 1.9x, F254 = 1.3x Kyle's
F290. The upside: depth of focus on F290 is roughly +/-3.7mm (Rayleigh range) vs about +/-1.1mm
on F160, so F290 is forgiving on curved iron backs and deep multi-loop jobs where the floor drops.
OMTech's own chart says the same direction in words: its values are on an F160 baseline, and on
F290 you "increase power or reduce speed" ([OMTech stainless guide](https://omtech.com/blogs/knowledge/best-laser-engraving-stainless-steel-settings-fiber-and-diode-laser-engravers)).
Two other sources agree that speed and frequency transfer while power needs adjusting
([Barch chrome page](https://www.barchlaser.com/laser-engraving-settings-for-chrome/),
[Thunder slate KB](https://support.thunderlaser.com/portal/en/kb/articles/how-to-engrave-on-slate-with-a-fiber-laser)).

**Bottom line:** a community row is a test-grid center, not a setting. Expect speed and Line
distance to hold, power to move up to 20%, frequency to need re-picking unless the source is a
50QB, and depth per loop on F290 to be 1.3x (vs F254) to 3.3x (vs F160) lower.

## Metals

### Chrome-plated steel and golf club heads

Plating context: decorative chrome is about 1.3 to 5 um over a nickel layer of about 10 to 25 um
(patent figures, my unit conversion) ([US6346052](https://patents.google.com/patent/US6346052)); a
Japanese patent measured 5 to 30 um Ni-Cr on one face ([JPH10277185A](https://patents.google.com/patent/JPH10277185A/en)).
So breaking through plating takes very little; all useful paint-fill depth is in the 8620 steel.
A golf patent gives laser feature depth of 0 to 0.02 in (0 to 0.5mm)
([US 12109460](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/12109460)). Epilog
says general metal-engraving settings ablate through plating and polishing settings are for when
breaking the plating is not allowed ([Epilog FiberMark chart](https://www.epiloglaser.com/assets/downloads/fibermark-material-settings.pdf)).

| Goal | Power % | Speed | Freq | Loops | Line dist / angles | Lens | Source | Reported result | Confidence |
|---|---|---|---|---|---|---|---|---|---|
| Chrome engrave (surface ablation) | 40 (30W) | 1500 | 730 (unit not stated; above any Q-switch range, likely a typo or a different unit) | not stated | 0.05, 0 or 90, unidirectional | 100x100 (about F160) | [Barch Laser](https://www.barchlaser.com/laser-engraving-settings-for-chrome/) | none shown | Low |
| Chrome iron deep engrave for paint fill | no reliable data found | | | | | | Searched LightBurn forum, OMTech, JPT, ComMarker, Monport | Golf pages ([OMTech](https://omtech.com/blogs/knowledge/golf-club-engraving), [JPT](https://jpt-laser.com/applications/golf-club-engraving/), [ComMarker](https://blog.commarker.com/archives/58437)) give no numbers | none |
| Golf paint fill layout | n/a | | | | engrave the whole fill area, leave only outlines unlasered so colors do not bleed | | [LightBurn forum, Golf Club Engraving](https://forum.lightburnsoftware.com/t/golf-club-engraving/172226) | advice | Medium |
| Wedge (raw or black finish), stainless putter, forged carbon head | use the stainless / carbon steel / coated-metal rows below; no golf-specific numbers found | | | | | | | | |

### Stainless steel

| Goal | Power % | Speed | Freq | Loops | Line dist / angles | Lens | Source | Reported result | Confidence |
|---|---|---|---|---|---|---|---|---|---|
| Deep engrave (50W row) | 85 to 95 | 1000 to 1500 | 20 to 30 (below 50QB range; use 50) | 5 to 30 | multi-hatch 0/45/90 | F160 | [OMTech stainless guide](https://omtech.com/blogs/knowledge/best-laser-engraving-stainless-steel-settings-fiber-and-diode-laser-engravers) | official chart, no photos | Medium (official, but F160 and freq conflicts with this source) |
| Cleanup after deep engrave | 10 to 15 | 2000 | 60 | 1 | not stated | not stated | same | official chart | Medium |
| White / frost (50W row) | 15 to 25 | 2000 to 2500 | 50 to 60 | 1 | 0.03 to 0.04 | F160 | same | official chart | Medium |
| Dark mark (50W row; OMTech calls it annealing) | 35 to 45 | 500 to 700 | 40 to 50 | not stated | 0.015 to 0.02, 90 cross | F160 | same | official chart | Low (40 kHz below range; dark anneal is weak on Q-switch per repo `CLAUDE.md`) |
| Blacken, 304 | 10 | 200 | 100 | 10 | 0.02 | not stated (Aurora Lite std 150x150) | [Thunder Laser 50W chart](https://www.thunderlaser.com/laser-settings/2.html) | official chart; source is a Hans 50W Q-switch | Medium |
| Whiten | 20 | 1700 | 50 | 1 | 0.02 | same | same | official chart | Medium |
| Mirror stainless blacken | 20 | 100 | 90 | 1 | 0.02 | same | same | official chart | Medium |
| Mirror stainless whiten | 30 | 1000 | 80 | 1 | 0.04 | same | same | official chart | Medium |
| Polish (white) | Epilog % scales only (35 to 40% power, 50 to 60% freq) | | | | | | [Epilog FiberMark](https://www.epiloglaser.com/assets/downloads/fibermark-material-settings.pdf) | official, non-EzCad units | Low (units do not transfer) |
| Deep engrave 316L test matrix | 70 rough / 20 to 30 finish | 300 / 400 | 45 / 60 to 120 | 10 to 20 rough + 10 finish | 0.01 to 0.03 | not stated | [LightBurn forum, 316L](https://forum.lightburnsoftware.com/t/316l-deep-engraving-help/190658) | no results yet | **Not applicable** (MOPA, Q-pulse 200 ns) |
| Color marking | | | | | | | various | | **Not applicable** (MOPA-only) |

### Mild / carbon steel

| Goal | Power % | Speed | Freq | Loops | Line dist / angles | Lens | Source | Reported result | Confidence |
|---|---|---|---|---|---|---|---|---|---|
| Blacken | 10 | 100 | 50 | 1 | 0.02 | Aurora Lite | [Thunder 50W chart](https://www.thunderlaser.com/laser-settings/2.html) | official chart | Medium |
| Whiten | 20 | 900 | 60 | 1 | 0.02 | same | same | official chart | Medium |
| Deep engrave attempt (Gweike G2 Max 50W) | 90 | 300 | 20 | 5 | 0.03, cross hatch | not stated | [LightBurn forum, mild steel](https://forum.lightburnsoftware.com/t/deep-engraving-settings-mild-steel/189748) | "still not particularly deep" | Low (failed, and the reply was AI-generated advice) |
| Rust after coating removal | n/a | | | | | | [ComMarker golf guide](https://blog.commarker.com/archives/58437) | exposed carbon steel rusts; oil or paint fill | Medium |

### Tool steel

| Goal | Power % | Speed | Freq | Loops | Line dist / angles | Lens | Source | Reported result | Confidence |
|---|---|---|---|---|---|---|---|---|---|
| any | no reliable data found | | | | | | | start from stainless rows | none |

### Aluminum (raw and anodized)

| Goal | Power % | Speed | Freq | Loops | Line dist / angles | Lens | Source | Reported result | Confidence |
|---|---|---|---|---|---|---|---|---|---|
| Raw, whiten | 80 | 3500 | 50 | 1 | 0.02 | Aurora Lite | [Thunder 50W chart](https://www.thunderlaser.com/laser-settings/2.html) | official chart | Medium |
| Raw, deep/dark etch (30W example) | 50 to 70 | 500 to 800 | 20 to 30 (use 50) | not stated | not stated | not stated | [OMTech aluminum guide](https://omtech.com/blogs/knowledge/laser-engraving-aluminum) | official blog | Low |
| Raw, 3D slice (ComMarker B4 50W Q-switch) | 50 | 600 | 30 | 10 | 0.025, 0 deg | not stated | [LightBurn forum, B4 50W](https://forum.lightburnsoftware.com/t/2-5d-3d-slice-engraving-on-aluminum-brass-with-commarker-b4-50w-best-settings-in-lightburn/180275) | no result reported | Low |
| Anodized, remove dye to white | Epilog: 100% power, lowest freq, defocus +0.06 to +0.07 in | | | | | | [Epilog FiberMark](https://www.epiloglaser.com/assets/downloads/fibermark-material-settings.pdf) | official; defocus gives brighter mark | Medium (direction), Low (numbers) |
| Anodized, guidance | "a little more speed but a very low frequency" | | | | | | [Monport 50W manual](https://cdn.shopify.com/s/files/1/0591/5128/6471/files/Monport_Fiber_50W_User_Manual_af59b7df-4eb0-46c3-ab15-35f5fd61f81f.pdf) | manual, no numbers | Low |
| Aluminum tests (OMTech) | 80 / 30 | 500 / 1200 | 100 / 30 | | 0.005 / 0.05 | | [OMTech aluminum guide](https://omtech.com/blogs/knowledge/laser-engraving-aluminum) | | **Not applicable** (60W MOPA, 100/200 ns Q-pulse) |
| Black on raw aluminum | | | | | | | | needs MOPA short pulse | **Not applicable** |

### Brass

| Goal | Power % | Speed | Freq | Loops | Line dist / angles | Lens | Source | Reported result | Confidence |
|---|---|---|---|---|---|---|---|---|---|
| Blacken | 50 | 100 | 50 | 1 | 0.02 | Aurora Lite | [Thunder 50W chart](https://www.thunderlaser.com/laser-settings/2.html) | official chart | Medium |
| Whiten | 30 | 100 | 50 | 1 | 0.02 | same | same | official chart | Medium |
| 3D slice (B4 50W Q-switch) | 50 | 600 | 30 | 10 | 0.025, 0 deg | not stated | [LightBurn forum, B4 50W](https://forum.lightburnsoftware.com/t/2-5d-3d-slice-engraving-on-aluminum-brass-with-commarker-b4-50w-best-settings-in-lightburn/180275) | no result | Low |
| Brass coin 3D (bulldog) | 90 | 1800 | 120 | 256 | 0.025 (1000 DPI) | | quoted in [coin thread](https://forum.lightburnsoftware.com/t/coin-engraving-settings-50-watt-gweike-fiber/166363) | | **Not applicable** (100 ns MOPA, 120 kHz) |

### Copper

| Goal | Power % | Speed | Freq | Loops | Line dist / angles | Lens | Source | Reported result | Confidence |
|---|---|---|---|---|---|---|---|---|---|
| any | no reliable data found | | | | | | [LightBurn lens thread](https://forum.lightburnsoftware.com/t/effect-on-different-lenses-for-fiber-lasers/135818): 175mm lens "couldn't even touch copper", 110x110 worked | F290 is worse than 175mm for copper; expect poor results | Medium (direction) |

### Titanium

| Goal | Power % | Speed | Freq | Loops | Line dist / angles | Lens | Source | Reported result | Confidence |
|---|---|---|---|---|---|---|---|---|---|
| "Icy crystal" | 20 | 1000 | 100 | 5 | 0.02 | Aurora Lite | [Thunder 50W chart](https://www.thunderlaser.com/laser-settings/2.html) | official chart | Medium |
| Blue-gray | 10 | 100 | 90 | 1 | 0.01 (2450 DPI) | same | same | official chart (oxide color on Q-switch is possible on Ti, unlike stainless) | Medium |
| Full color palette | | | | | | | [Epilog](https://www.epiloglaser.com/assets/downloads/fibermark-material-settings.pdf) varies freq 1 to 100% | | Low; broad palettes are a MOPA strength |

### Coated metals: powder coat (tumblers), PVD/DLC, painted metal

| Goal | Power % | Speed | Freq | Loops | Line dist / angles | Lens | Source | Reported result | Confidence |
|---|---|---|---|---|---|---|---|---|---|
| Powder coat removal (30W) | 50 to 70 | 600 to 900 | 30 to 60 (use 50 to 60) | 1 to 2 | not stated | not stated | [StyleCNC](https://www.stylecnc.com/blog/laser-engraving-powder-coated-tumblers-settings.html) | vendor blog | Low |
| Bare stainless under coat, dark (30W) | 40 to 60 | 300 to 500 | 40 to 60 | 1 | not stated | not stated | same | vendor blog | Low |
| Powder coat method | high freq, 2 to 3 passes: ablate then polish; slight defocus +0.05 to +0.07 in | | | | | | [Epilog FiberMark](https://www.epiloglaser.com/assets/downloads/fibermark-material-settings.pdf), [Monport 50W manual](https://cdn.shopify.com/s/files/1/0591/5128/6471/files/Monport_Fiber_50W_User_Manual_af59b7df-4eb0-46c3-ab15-35f5fd61f81f.pdf) | two official sources agree | High (method), no EzCad numbers |
| Powder coat color variation | | | | | | | [LightBurn, 50W galvo vs Yeti](https://forum.lightburnsoftware.com/t/50w-galvo-laser-vs-jds-yeti-powder-coating/192792) | every color/maker needs its own setting (search excerpt) | Medium |
| Galvanized blacken / whiten | 40 / 50 | 100 / 800 | 100 / 100 | 1 | 0.028 / 0.042 | Aurora Lite | [Thunder 50W chart](https://www.thunderlaser.com/laser-settings/2.html) | official chart | Medium |
| Nickel plate whiten / blacken | 30 / 40 | 3000 / 100 | 50 / 60 | 1 | 0.02 / 0.005 | same | same | official chart; closest analog to the nickel under chrome | Medium |
| PVD / DLC | no reliable data found | | | | | | | | none |
| Painted metal | no reliable data found (Tyvok row seen only in a search excerpt with unlabeled columns) | | | | | | | | none |

## Gun parts

### Legal note (primary sources; not legal advice)

- **Serial numbers and required markings:** 18 U.S.C. 922(k) makes it a federal crime to
  transport, ship, possess or receive a firearm whose serial number has been removed, obliterated
  or altered ([Ninth Circuit model jury instruction 14.19](https://www.ce9.uscourts.gov/jury-instructions/criminal/chapter-14/14-19-firearms-transportation-shipment-possession-or-receipt-in-commerce-with-removed-or-altered-serial-number-18-u-s-c-922-k/)).
  27 CFR 478.92 sets the required manufacturer markings
  ([ATF eRegs 478.92](https://regulations.atf.gov/478-92/)). A court held that making a number
  hard to read can count as "altered" ([US v. Harris, 4th Cir. 2013](https://hallapproved.com/us/cases/ca4/2013/933595), secondhand case summary).
  **Never engrave over, through or near a serial number or a required marking**, and keep artwork
  clear of them by a margin.
- **Business engraving needs a license:** ATF's Q&A "Is a license needed to engage in the
  business of engraving, customizing, refinishing or repairing firearms?" answers yes: a person
  doing this as a business is a gunsmith within the definition of a dealer
  ([ATF Q&A](https://atf.gov/node/26386); text from search excerpt, page blocks automated fetch).
  ATF's frame/receiver training aid says the current rule supersedes Ruling 2009-1 and
  distinguishes gunsmithing from manufacturing by purpose; per ATF Q&A, decorative engraving done
  for sale or distribution needs a manufacturing license
  ([ATF training aid](https://www.atf.gov/media/14631/download); search excerpt). State law can be
  stricter. Engraving Kyle's own firearms is not business activity; engraving other people's for
  money is.

### Settings

| Part / finish | Goal | Power % | Speed | Freq | Loops | Line dist / angles | Lens | Source | Reported result | Confidence |
|---|---|---|---|---|---|---|---|---|---|---|
| Nitride / Melonite / Tenifer slide | any | no reliable data found for Q-switch; only an 80W MOPA thread | | | | | | [LightBurn, Glock slide 80W MOPA](https://forum.lightburnsoftware.com/t/black-background-relief-for-glock-slide-engraving-80w-mopa/186312) | light green background on deep engraves | **Not applicable** (MOPA) |
| Contoured slides, general | clean mark | "high speed, low power, high frequency"; adjust speed and freq before power | | | | | | [Sawmill Creek, contoured slides](https://sawmillcreek.org/goto/post?id=2962625) (search excerpt) | advice | Low |
| Cerakote imaging (tonal, no removal) | 500 to 800 kHz, short pulse | | | | | | | [Cerakote Laser Imaging](https://www.cerakoteeu.com/cerakote-laser-imaging/) | official | **Not applicable** (beyond 100 kHz ceiling; pulse-width tuning is MOPA) |
| Cerakote removal to metal | | no reliable data found; Cerakote gives no removal numbers | | | | | | [Cerakote](https://www.cerakoteeu.com/cerakote-laser-imaging/) | removal exposes substrate and drops corrosion protection there | none |
| DLC, bluing, bare stainless barrel | | no reliable data found; bare stainless uses stainless rows | | | | | | | | none |
| Anodized aluminum receiver | dye removal | use anodized aluminum rows | | | | | | | serial/marking rule above applies to receivers | Low |
| Polymer frame (Glock-type, 30W) | mark/engrave | 20 | 500 | 50 | 2 x 2 (cross hatch) | cross hatch; another user: single 0 deg works best | not stated | [Sawmill Creek, Glock/Pmags](https://sawmillcreek.org/goto/post?id=2911175) (search excerpt; page blocks fetch) | reported success | Low |
| Polymer frame risk | | | | | | | | [laser-engraving-glock guide](https://laser-engraving-glock.pages.dev/) (secondhand) | too much energy burns through or embrittles the grip; Polymer80 frames are a different polymer | Low |

Frames are the serialized part on most polymer pistols: the legal note applies with full force.

## Plastics

**Fume hazards first.** Never laser **PVC, vinyl, PVB** (chlorine / HCl), **PTFE/Teflon**
(fluorine), or Cr(VI)-tanned artificial leather ([Monport 50W manual, Material Safety](https://cdn.shopify.com/s/files/1/0591/5128/6471/files/Monport_Fiber_50W_User_Manual_af59b7df-4eb0-46c3-ab15-35f5fd61f81f.pdf);
[Stanford EH&S](https://ehs.stanford.edu/wp-content/uploads/Laser-Cutters-Safety-Guidance.pdf)).
**ABS** releases hydrogen cyanide ([Emory TechLab list](https://ats.emory.edu/_includes/documents/Emory%20TechLab%20Prohibited%20Laser%20Cutter%20Materials.pdf)):
marking only, with extraction. **Polycarbonate** is banned for laser processing at Yale
([Yale EHS](https://ehs.yale.edu/resource/download/1142)). Monport also lists phenolic/epoxy resins
as prohibited (relevant to carbon fiber, which is epoxy-matrix).

**Engine covers are not ABS.** Sources point to glass- or mineral-filled **PA66** (an engine-cover
grade listed as PA66-MF30, [UL Prospector Lumid GP3300B(W)](https://plastics.ulprospector.com/plastics/en/datasheet/137445/lumid-gp3300bw);
PA66-GF30 for engine covers per a lower-quality vendor guide,
[nylonplastic.com](https://nylonplastic.com/wp-content/uploads/2026/06/automotive-plastics-guide.pdf)),
with glass-filled **PP** as a PA66 replacement in some under-hood covers
([Teknor Apex](https://www.teknorapex.com/en-us/news/teknor-apex-replaces-standard-pa66-gf-materials-with-polypropylene-gf)).
Check the recycling code molded on the back (`>PA66-GF30<`, `>PP-T20<`) before testing.

| Material | Goal | Power % | Speed | Freq | Loops | Line dist / angles | Lens | Source | Reported result | Confidence |
|---|---|---|---|---|---|---|---|---|---|---|
| ABS | blacken | 20 | 1000 | 50 | 1 | 0.04 (635 DPI) | Aurora Lite | [Thunder 50W chart](https://www.thunderlaser.com/laser-settings/2.html) | official chart | Medium |
| PET | blacken | 45 | 4000 | 50 | 1 | 0.02 | same | same | official chart | Medium |
| PBT | blacken | 40 | 3000 | 100 | 1 | 0.02 | same | same | official chart | Medium |
| Black acrylic | whiten | 15 | 3500 | 100 | 2 | 0.02 | same | same | official chart | Medium |
| Clear acrylic, clear glass | any | 1064nm largely passes through; not a fiber job | | | | | | [Boss Laser KB](https://team.bosslaser.com/topic/fiber-lasers/) (search excerpt) | | Medium |
| Laser-additive plastics | mark | Epilog % scales only (60 to 70% power, 50% freq) | | | | | | [Epilog FiberMark](https://www.epiloglaser.com/assets/downloads/fibermark-material-settings.pdf) | official | Low |
| Plastics, general | | low power, high speed; too much energy melts, fumes, fire | | | | | | [Monport 50W manual](https://cdn.shopify.com/s/files/1/0591/5128/6471/files/Monport_Fiber_50W_User_Manual_af59b7df-4eb0-46c3-ab15-35f5fd61f81f.pdf) | | High (direction) |
| PA6 / PA66 GF (engine covers, frames) | | no reliable data found beyond the polymer-frame rows | | | | | | | | none |
| Polycarbonate | | do not process (Yale EHS) | | | | | | | | |
| Delrin/POM, PP/PE | | no reliable data found | | | | | | | | none |

## Non-metals

| Material | Goal | Power % | Speed | Freq | Loops | Line dist / angles | Lens | Source | Reported result | Confidence |
|---|---|---|---|---|---|---|---|---|---|---|
| Slate | whiten | 20 | 200 | 60 | 1 | 0.02 | Aurora Lite (50W) | [Thunder 50W chart](https://www.thunderlaser.com/laser-settings/2.html) | official chart | Medium |
| Slate (20W Raycus) | engrave | 90 | 200 | 20 (outside 50QB range) | 2, bidirectional | not stated | 110mm | [Thunder slate KB](https://support.thunderlaser.com/portal/en/kb/articles/how-to-engrave-on-slate-with-a-fiber-laser) | official; too much power makes slate bubble ([Snapmaker forum](https://forum.snapmaker.com/t/engraving-slate/39075)) | Low |
| PU leather | blacken | 25 | 1000 | 50 | 1 | 0.045 (564 DPI) | Aurora Lite | [Thunder 50W chart](https://www.thunderlaser.com/laser-settings/2.html) | official chart | Medium |
| Real leather | | no reliable data found; avoid Cr(VI)-tanned artificial leather | | | | | | [Monport manual](https://cdn.shopify.com/s/files/1/0591/5128/6471/files/Monport_Fiber_50W_User_Manual_af59b7df-4eb0-46c3-ab15-35f5fd61f81f.pdf) | | none |
| Wood | | **fiber is poor on wood**: 1064nm absorbs badly, scorches, fire risk; use CO2. Monport prohibits wood on its 50W fiber | | | | | | [Boss Laser KB](https://team.bosslaser.com/topic/fiber-lasers/), [Monport manual](https://cdn.shopify.com/s/files/1/0591/5128/6471/files/Monport_Fiber_50W_User_Manual_af59b7df-4eb0-46c3-ab15-35f5fd61f81f.pdf) | | High |
| Stone (granite, marble) | | moderate power and speed, low frequency | | | | | | [Monport manual](https://cdn.shopify.com/s/files/1/0591/5128/6471/files/Monport_Fiber_50W_User_Manual_af59b7df-4eb0-46c3-ab15-35f5fd61f81f.pdf) | manual, no numbers | Low |
| Ceramic tile (60W) | engrave + darken | 90 | 2000 | 45 / 105 | 10 | 0.025 / 0.003 | | [coin thread, bulldog](https://forum.lightburnsoftware.com/t/coin-engraving-settings-50-watt-gweike-fiber/166363) | | **Not applicable** (MOPA, 200/100 ns) |
| Coated ceramic / glass (Cermark etc.) | | no reliable data found | | | | | | | | none |
| Carbon fiber | | no reliable data found; epoxy matrix fumes (Monport bans phenolic/epoxy) | | | | | | | | none |

## Kyle's chrome starting settings vs community (question 5)

Kyle's card: 80% / 1000 mm/s / 30 kHz / 10 loops / 0.02mm at 0 and 90 / contour on, plus cleanup
20% / 3000 / 60 kHz.

| Parameter | Community says | Verdict | Change to (grid center) |
|---|---|---|---|
| Power 80% | OMTech 50W deep: 85 to 95% (F160); Monport warns sustained >80% shortens source life | Supported | Keep 80; grid 70 / 80 / 90 |
| Speed 1000 mm/s | OMTech 50W deep: 1000 to 1500 | Supported | Keep; at 50 kHz pulse pitch is 20 um vs a ~90 um spot, plenty of overlap |
| Frequency 30 kHz | Charts say 20 to 30, but they are F160 and other source variants; Raycus 50QB is rated 50 to 100 | **Contradicted for this source** | **50 kHz** (grid 50 / 60) after confirming the source label |
| Loops 10 | OMTech: 5 to 30 on F160; coin: 256 loops for 0.8mm on F210; F290 delivers 1.3 to 3.3x less per loop | **Likely too shallow** | Grid 10 / 20 / 40, measure depth; plating is only ~10 to 35 um so steel is reached early |
| Line distance 0.02 | OMTech 0.015 to 0.025; Thunder 0.02; coin 0.05 | Supported | Keep |
| Hatch 0 / 90 fixed | OMTech: 0/45/90 multi-hatch; coin: 10 deg increment, auto rotate; forum: 15 or 45 deg per pass | Partly | Rotate angle each loop if your EzCad2 Hatch dialog has auto-rotate; otherwise 0/45/90/135 |
| Contour on | Golf paint-fill: engrave full area, outline crisp | Supported | Keep |
| Cleanup 20% / 3000 / 60 kHz, once at end | OMTech: 10 to 15% / 2000 / 60, single pass; coin: 80% / 1500 / 50 kHz every 8 passes | Settings supported; timing not | Run it every 5 loops, not just at the end; add a 40% variant to the grid since F290 needs more |
| Frosted mark 40 / 1500 / 50 | OMTech white/frost 50W: 15 to 25% / 2000 to 2500 / 50 to 60, 0.03 to 0.04 | Roughly | Grid 20 / 30 / 40 at 2000 |

Heat caution stands: many loops on a hollow P790 with foam behind the face; pause between blocks.

## Gaps

- No tested chrome-iron paint-fill recipe for any Q-switched 50W was found anywhere.
- OMTech product page and manuals.plus copies of the FMM-5RW2 manual blocked fetching (403/429);
  the 50 to 100 kHz figure for this SKU is from a search excerpt. The Raycus datasheet is direct.
- No reliable numbers for tool steel, copper, PVD/DLC, painted metal, nitride/DLC/blued gun
  finishes, Cerakote removal, POM, PP/PE, PA GF, real leather, coated glass, carbon fiber.
- Reddit r/fiberlaser threads did not surface in search.

## Sources

- Raycus RFL-P10Q/20QE/30Q/50QB User's Guide V2.1: https://cdn.shopify.com/s/files/1/0651/8158/1563/files/RFL-P10Q_20QE_30Q_50QB.pdf
- OMTech FMM-5RW2-US product page: https://omtech.com/products/50w-fmm-5rw2-us
- OMTech stainless settings guide: https://omtech.com/blogs/knowledge/best-laser-engraving-stainless-steel-settings-fiber-and-diode-laser-engravers
- OMTech aluminum guide: https://omtech.com/blogs/knowledge/laser-engraving-aluminum
- OMTech golf club engraving: https://omtech.com/blogs/knowledge/golf-club-engraving
- Thunder Laser 50W fiber settings (Aurora Lite): https://www.thunderlaser.com/laser-settings/2.html
- Thunder Laser slate KB: https://support.thunderlaser.com/portal/en/kb/articles/how-to-engrave-on-slate-with-a-fiber-laser
- Epilog FiberMark material settings: https://www.epiloglaser.com/assets/downloads/fibermark-material-settings.pdf
- Monport 50W fiber user manual: https://cdn.shopify.com/s/files/1/0591/5128/6471/files/Monport_Fiber_50W_User_Manual_af59b7df-4eb0-46c3-ab15-35f5fd61f81f.pdf
- Barch Laser chrome settings: https://www.barchlaser.com/laser-engraving-settings-for-chrome/
- StyleCNC powder coat tumblers: https://www.stylecnc.com/blog/laser-engraving-powder-coated-tumblers-settings.html
- ComMarker golf guide: https://blog.commarker.com/archives/58437
- JPT golf page: https://jpt-laser.com/applications/golf-club-engraving/
- LightBurn forum: coin engraving 50W Gweike: https://forum.lightburnsoftware.com/t/coin-engraving-settings-50-watt-gweike-fiber/166363
- LightBurn forum: deep engraving mild steel: https://forum.lightburnsoftware.com/t/deep-engraving-settings-mild-steel/189748
- LightBurn forum: 316L deep engraving: https://forum.lightburnsoftware.com/t/316l-deep-engraving-help/190658
- LightBurn forum: B4 50W aluminum/brass 3D: https://forum.lightburnsoftware.com/t/2-5d-3d-slice-engraving-on-aluminum-brass-with-commarker-b4-50w-best-settings-in-lightburn/180275
- LightBurn forum: lenses on fiber: https://forum.lightburnsoftware.com/t/effect-on-different-lenses-for-fiber-lasers/135818
- LightBurn forum: golf club engraving: https://forum.lightburnsoftware.com/t/golf-club-engraving/172226
- LightBurn forum: powder coat vs Yeti: https://forum.lightburnsoftware.com/t/50w-galvo-laser-vs-jds-yeti-powder-coating/192792
- LightBurn forum: Glock slide 80W MOPA: https://forum.lightburnsoftware.com/t/black-background-relief-for-glock-slide-engraving-80w-mopa/186312
- Sawmill Creek: Glock/Pmags: https://sawmillcreek.org/goto/post?id=2911175
- Sawmill Creek: contoured slides: https://sawmillcreek.org/goto/post?id=2962625
- Cerakote Laser Imaging: https://www.cerakoteeu.com/cerakote-laser-imaging/
- Snapmaker forum, slate: https://forum.snapmaker.com/t/engraving-slate/39075
- Boss Laser fiber KB: https://team.bosslaser.com/topic/fiber-lasers/
- Patents: https://patents.google.com/patent/US6346052 , https://patents.google.com/patent/JPH10277185A/en , https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/12109460
- ATF Q&A, engraving license: https://atf.gov/node/26386
- ATF frame/receiver training aid: https://www.atf.gov/media/14631/download
- 27 CFR 478.92: https://regulations.atf.gov/478-92/
- 18 U.S.C. 922(k) jury instruction: https://www.ce9.uscourts.gov/jury-instructions/criminal/chapter-14/14-19-firearms-transportation-shipment-possession-or-receipt-in-commerce-with-removed-or-altered-serial-number-18-u-s-c-922-k/
- US v. Harris summary: https://hallapproved.com/us/cases/ca4/2013/933595
- Stanford EH&S laser cutter guidance: https://ehs.stanford.edu/wp-content/uploads/Laser-Cutters-Safety-Guidance.pdf
- Emory TechLab prohibited materials: https://ats.emory.edu/_includes/documents/Emory%20TechLab%20Prohibited%20Laser%20Cutter%20Materials.pdf
- Yale EHS: https://ehs.yale.edu/resource/download/1142
- UL Prospector Lumid GP3300B(W): https://plastics.ulprospector.com/plastics/en/datasheet/137445/lumid-gp3300bw
- Teknor Apex PP-GF: https://www.teknorapex.com/en-us/news/teknor-apex-replaces-standard-pa66-gf-materials-with-polypropylene-gf
- nylonplastic.com automotive guide (low quality): https://nylonplastic.com/wp-content/uploads/2026/06/automotive-plastics-guide.pdf
