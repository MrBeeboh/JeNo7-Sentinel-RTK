# JeNo 7" + Sentinel RTK (work in progress)

Open packaging work to run an **F450 Sentinel–class RTK / ArduPilot / Walksnail** avionics stack on a **[JeNo 7"](https://github.com/WE-are-FPV/JeNo-7)** long-range FPV frame.

This repo is **not** a finished airframe release. It is shared so others can reuse the **editable CAD pack**, the **Sentinel-on-JeNo layout plan**, and contribute mounts (GNSS roof, Walksnail dual plates, TPU).

---

## What’s in here

| Path | Contents |
|------|----------|
| **`Sentinel-on-JeNo7/`** | Design plan: how Sentinel gear maps onto JeNo (UM980, Q39, Walksnail dual, LR900, RP3, stack) |
| **`Editable/`** | Split CAD for FreeCAD / Fusion / AutoCAD LT — one part per file where possible |
| **`JeNo-7-main/`** | Upstream JeNo 7" v1.1.1 sources (frame DXF/STEP/STL + official TPU) |

### Editable CAD pack (start here for redesign)

- `Editable/01-CARBON-3D/` — individual plate/arm **STEP** + **FCStd** (Fusion / FreeCAD)
- `Editable/02-CARBON-2D-DXF/` — per-plate **DXF** for CNC / AutoCAD LT (English layers: CUT, POCKET, …)
- `Editable/00-MASTER/` — full assembly STEP from the official export
- `Editable/README.md` — which tool opens what
- `Editable/FREECAD-HOWTO.md` — FreeCAD notes (imported solids are not parametric history)

### Sentinel packaging plan

- `Sentinel-on-JeNo7/DESIGN.md` — plain-language fit plan, what stock JeNo covers, what must be redesigned (GNSS roof, camera plates, sensors, 7" motors)

---

## License and attribution

### Upstream JeNo 7"

Frame and official TPU files in `JeNo-7-main/` are **[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)** by **WE are FPV / JeNo** (nochamo and community).  

Upstream project: [github.com/WE-are-FPV/JeNo-7](https://github.com/WE-are-FPV/JeNo-7)

If you redistribute or remix JeNo geometry, **credit WE are FPV / JeNo** and keep the license notice.

### This repository’s additions

Layout docs, split CAD packaging scripts, and Sentinel integration notes are provided for the community. When in doubt, treat remixes of JeNo geometry as still under **CC BY 4.0** with attribution to the original authors.

---

## Not included (on purpose)

- `JeNo-7-main.zip` — duplicate of the extracted tree  
- `Editable/03-TPU-3D/from-STL-mesh/` — huge mesh-derived STEP files; use official STLs under `JeNo-7-main/02-TPU/` instead  

---

## Related projects

- **JeNo 7" upstream:** https://github.com/WE-are-FPV/JeNo-7  
- **F450 Sentinel** (avionics / RTK source of truth for this build) lives in the builder’s local `F450-Sentinel` tree and is not fully mirrored here yet  

---

## Status

| Item | Status |
|------|--------|
| Official JeNo files | Vendored v1.1.1 |
| Split editable CAD | Done (carbon + DXF + partial TPU solids) |
| Sentinel-on-JeNo design plan | Draft in `Sentinel-on-JeNo7/DESIGN.md` |
| GNSS roof plate CAD | **Not designed yet** |
| Walksnail dual camera plates | **Not designed yet** |
| Built / flown 7" Sentinel | **Not yet** |

Contributions welcome: roof plate DXF/STEP, Walksnail dual plates, TPU mounts, BOM for 7" motors/props with this stack.
