# Sentinel on JeNo 7" — Design plan

**What this is:** A plan to move the **F450 Sentinel electronics and mission** (RTK rover, Walksnail dual, ArduPilot stack, radios) onto a **JeNo 7"** carbon frame, and to list what must be redesigned so you can reshape plates and mounts freely later.

**What this is not:** A finished CAD package yet. You asked to modify parts so everything fits — this document is the map of *what* has to change and *where* each Sentinel piece goes, so CAD work has a target instead of guesswork.

**Source of truth for electronics:**  
`Documents/DRONE Builds/F450-Sentinel/Current design folder/`  
especially `README.md`, `Stack_and_Wiring.md`, `ArduPilot_Configuration.md`.

**Source of truth for frame geometry:**  
`Documents/DRONE Builds/custom 7 inch frame/Editable/`  
and official `JeNo-7-main/`.

---

## 1. Goal in one paragraph

You want one aircraft that flies as a **7" long-range / freeride FPV platform** (JeNo) but carries the **Sentinel payload**: ArduPilot H743 stack, Walksnail Avatar HD Pro Dual, UM980 + Waveshare Q39 helix, UBEC for the GNSS, LR900 telemetry (RTCM path), RP3 ELRS, and the optical flow / rangefinder path you already run on the F450. The ground base station (second UM980 + LicheeRV Nano) stays on the ground — it does not move onto the airframe.

---

## 2. Assumptions (top three)

If any of these is wrong, say so and we adjust the plan.

1. **You are transplanting the Sentinel *avionics and wiring philosophy*, not the F450 airframe as a whole.** The F450’s 10" props and A2212 motors do **not** bolt onto JeNo 7" arms. The 7" needs its own motors and props (typically 2806–3008 class, 16–19 mm mount, 7" props).  
2. **Firmware and serial map stay Sentinel-style** (H743, Avatar on the O3/HD VTX plug as SERIAL2, UM980 on GPS/SERIAL3, LR900 on telemetry, RP3 on ELRS). Frame changes do not change that map.  
3. **Base station stays ground-side.** Only the **rover** UM980 + Q39 fly on the JeNo.

---

## 3. Why the stock JeNo is not enough by itself

The JeNo 7" is a **clean FPV frame**: one compact body (~30 mm tall inside), Wide-X arms, camera plates aimed at DJI O3/O4 or Walksnail, room for a 30×30 stack, battery straps on the bottom plate. It was **not** designed as a multi-layer “pagoda” RTK ship like the F450 Sentinel.

On the F450 you solved space by stacking plates:

- Battery under the bottom  
- Avatar VTX on a lower deck  
- FC/ESC higher up  
- Roof plate with Q39 + UM980 and UBEC under the roof  

On the JeNo you only have about **30 mm of body height** between bottom and top carbon, plus whatever you hang outside (TPU, antenna masts, a small roof add-on). So “fit everything” means **re-packing** Sentinel gear into a flatter layout, and **cutting or printing** a few custom pieces — not dropping the F450 pagoda unchanged onto a 7".

That is the real design problem. It is mechanical packaging, not a FreeCAD mystery.

---

## 4. What already fits stock JeNo (little or no carbon change)

| Sentinel item | Size / need | Stock JeNo support |
|---------------|-------------|--------------------|
| AERO SELFIE H743 + 45A 4-in-1 | 30.5×30.5 mm stack | **Yes** — main stack pattern is 30×30 M3 |
| Battery (strap) | Underslung | **Yes** — bottom plate has strap slots |
| Walksnail Avatar camera | FPV cam forward | **Mostly** — use Walksnail-friendly camera plates / soft mount; JeNo is O3/O4-first but README lists Walksnail as supported VTX class |
| Walksnail VTX board | ~33.5 mm class, heat, 9V | **Yes with placement care** — rear / bottom bay or soft mount; not as spacious as F450 L1 deck |
| RP3 V2 ELRS | 22×13 mm + two antennas | **Yes** — TPU / zip / arm; keep antennas away from Q39 and LR900 |
| LR900-P | ~43×26×11 mm + 915 MHz whip | **Yes** — rear bay or arm; **≥200 mm** from RP3 antennas (same rule as F450) |
| UBEC | Small | **Yes** — under top plate or beside stack, clear of Q39 |
| Wiring philosophy | UBEC → UM980 only; ESC BAT for pack | **Unchanged** — does not depend on F450 plates |

So the FC stack, radios, and power tree can live on JeNo **if** you decide placement and print a few TPU pieces. The hard parts are **GNSS roof**, **Walksnail dual packaging**, and **nadir sensor view**.

---

## 5. What does *not* fit as a simple “drop in”

### 5.1 UM980 + Waveshare Q39 (must redesign mount)

- **UM980 carrier:** about **26 × 38 × 7.6 mm**  
- **Q39 helix:** tall multi-band antenna that needs **clear sky**, nothing metal above it, short SMA run to the UM980  

On F450 these live on a dedicated **roof plate (L4)** with the UBEC on the underside. Stock JeNo **top plate** is only about **58 × 195 × 2.5 mm** and is already the lid of a tight FPV body. You cannot honestly park a Q39 “wherever” next to props and carbon and expect good RTK.

**You need one of these (pick later in CAD):**

- **A)** A small **add-on GNSS roof plate** (new carbon or thick G10) on standoffs above the JeNo top plate, with:  
  - flat pad for UM980 (M2/M3 or VHB pattern)  
  - Q39 mount (SMA bulkhead or antenna base footprint)  
  - hole for short coax  
  - optional UBEC pads on the **underside** of that roof (same idea as Sentinel)  
- **B)** A tall **TPU mast** on the rear/top that holds Q39 high and the UM980 just below it, still with sky view  

**Recommendation:** Option **A** — closest to what already works on Sentinel, easiest to keep RF clean, and you can design that one plate in Fusion as a freeform part.

### 5.2 Walksnail Avatar HD Pro Dual

- **Camera** wants a solid forward mount and tilt (your choice of angle).  
- **VTX** wants airflow and 9V from the FC HD/VTX path (same as today: O3 Air Unit plug = Avatar = SERIAL2).  
- Dual antenna paths need TPU SMA mounts (JeNo already has SMA TPU options; may need remix for dual Walksnail antennas).

Stock **O3/O4 camera plates** are not the same as a dual Avatar camera cage. Plan on either:

- community Walksnail plate for JeNo 7, or  
- **custom camera plates** (3 mm carbon) sized to the Avatar dual camera module.

### 5.3 Optical flow / rangefinder (MTF-01 and/or CV50)

Your current Ardu docs lean on **MTF-01** on SERIAL4; build sheet history also has **CV50** nadir. Whichever you fly:

- Needs a **clear view straight down** (or as designed for that sensor).  
- On F450 that was an underside mount on a transverse deck.  
- On JeNo, bottom plate is busy with battery strap and arms. Typical approach: **rear or side cutout / small printed bracket** under the middle/bottom plate so the sensor sees ground between the battery and the props.

This is a **new small part** (TPU or 2.5 mm plate tab), not a stock JeNo feature.

### 5.4 Motors and props (new purchase, not a frame hole problem)

| F450 Sentinel | JeNo 7" |
|---------------|---------|
| A2212-class, **10"** props | **7"** props, 16–19 mm motor pattern on arms |
| Larger, slower cruise setup | Faster / different disc loading |

**Do not plan to reuse the 10" prop/motor set on JeNo arms.** Budget new 7" motors/props (and retune Ardu later). Frame CAD work is separate from that shopping list.

---

## 6. Proposed layout on JeNo (target packaging)

Think in layers again, but flatter than the F450 pagoda.

```
                    [ Q39 helix ]     clear sky
                    [ UM980  ]       short SMA
                 ── GNSS roof plate (NEW) ──
                         │ short standoffs
                 ── JeNo top plate ──
                    UBEC underside or side
                    FC + ESC 30.5 stack (center)
                    LR900 / RP3 (sides or rear, antennas split)
                 ── middle / body volume ──
                    Avatar VTX (rear or side bay, airflow)
                 ── JeNo bottom plate ──
                    battery strap underslung
                    flow/lidar looking down (clear FOV)
        ── camera plates ──  Avatar dual camera forward
        ── 8 mm arms ──  7" motors (new)
```

### Placement rules carried over from Sentinel (still valid)

- Q39: nothing above it; short coax to UM980.  
- UBEC: not directly under the helix if you can avoid it; if it is under the roof, verify sat quality before you call the layout final.  
- LR900 915 MHz whip and RP3 2.4 GHz antennas: **at least ~200 mm apart**, opposite corners of the frame if possible.  
- Avatar 5.8 GHz antennas: clear of battery and big carbon walls; not tied in the same zip as GNSS coax.  
- UM980 UART cable: twisted, away from ESC battery leads and VTX coax.  
- UM980 power: **only from UBEC**, not from the FC GPS 5V pin (same hard rule as F450).

---

## 7. What to redesign in CAD (your “do whatever I want” list)

These are the **editable pieces** that make the transplant real. Prefer **Fusion** on your other PC with STEP/DXF from `Editable/`. FreeCAD is optional, not required.

| Priority | Part | Base file to start from | What you change |
|----------|------|-------------------------|-----------------|
| **P0** | **GNSS roof plate** (new) | Blank from dimensions, or top plate as size reference | Outline, standoff holes matching JeNo top, UM980 holes, Q39 base, wire pass-through |
| **P0** | **Camera plates for Avatar dual** | `Camera_plate_*` DXF/STEP or new from dual cam dimensions | Hole pattern and tilt for Walksnail dual, not O3 |
| **P1** | **Top plate** (optional mods) | `Top_plate_2p5mm.step` | Extra holes for roof standoffs, antenna bulkheads, cable exits |
| **P1** | **Bottom plate** (optional mods) | `Bottom_plate_3mm.step` | Sensor window / bracket holes; keep strap slots |
| **P1** | **TPU set** | Official JeNo TPU + new prints | Dual SMA for Walksnail, LR900 clip, RP3 mount, Q39 mast if no carbon roof, CV50/MTF-01 pod |
| **P2** | Middle plate | `Middle_plate_2p5mm.step` | Only if stack height or routing needs a cutout |
| **P2** | Arms | Stock 8 mm | Usually leave alone; motor holes already 16–19 mm |

**You do not need to redesign the entire ALL_VERSIONS DXF on day one.** Start with **GNSS roof + camera plates + TPU**. The stock bottom/middle/arms can stay JeNo 8 mm until something physically does not fit.

---

## 8. Electronics that stay the same (no frame math)

Copy from Sentinel as-is unless you choose to change:

- H743 + 45A ESC, ArduPilot params (motor class will need retune later)  
- Avatar on **O3 Air Unit plug** → SERIAL2 / DisplayPort (do not re-argue this)  
- UM980 on GPS plug → SERIAL3, `GPS1_TYPE=24`  
- LR900 on telemetry path for MAVLink + RTCM inject  
- RP3 on ELRS plug  
- UBEC 5V only to UM980  
- Base station on the ground  

When the airframe is 7" with new motors, you will retune rates and battery failsafe for the new AUW — that is flight testing, not carbon day one.

---

## 9. Suggested build sequence (so nothing is wasted)

1. **Decide layout on paper** using this doc (roof vs mast for Q39; where LR900/RP3 sit).  
2. **CAD the GNSS roof plate** in Fusion from scratch (simplest high-value part). Export DXF for cut + STEP for your records.  
3. **CAD or buy Walksnail dual camera plates** for JeNo width.  
4. **Print TPU** antenna and sensor brackets; dry-fit on a naked JeNo or printed dummy.  
5. **Order 8 mm JeNo carbon** (stock or your modified DXFs) + **7" motors/props**.  
6. **Wire like Sentinel** (same harness rules, re-measure lengths for the shorter stack).  
7. **Bench:** RTK Fixed with UBEC on, Avatar video, ELRS, LR900, no props.  
8. **Hover / tune** for 7" AUW.

---

## 10. What I will not pretend

- Stock JeNo files are **not** a ready “Sentinel edition.” They are a good FPV base that we **extend**.  
- FreeCAD fighting you does not mean the project is impossible; it means **use Fusion for freeform plate redesign**, and use DXF for the CNC shop.  
- Fitting UM980 + Q39 **without** a roof or mast is how you get a pretty drone that will not hold RTK. That mount is non-negotiable.

---

## 11. Next concrete step

When you are ready to move from planning to metal:

**Design the GNSS roof plate first** — outline, four standoff holes that match the JeNo top plate pattern, UM980 footprint (26×38 mm carrier), Q39 mount, and a small cable hole. That single part unlocks the whole Sentinel mission on this frame.

Say if you want that plate’s dimensions worked out next (hole coordinates from the top plate STEP), and whether you prefer **carbon roof on standoffs** or a **tall rear TPU mast**. That choice drives every other antenna placement.
