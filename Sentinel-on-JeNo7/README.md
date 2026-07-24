# Sentinel on JeNo 7"

Goal: fly the **F450 Sentinel** avionics and RTK mission on a **JeNo 7"** frame.

**Start here:** [DESIGN.md](DESIGN.md)

## Design files

| File | Type | What |
|------|------|------|
| `GNSS_Roof_Plate.scad` | OpenSCAD source | GNSS roof plate (parametrized) |
| `GNSS_Roof_Plate_fc.dxf` | DXF | **Use this for CNC cutting** — 14 circle holes + polyline outline |
| `GNSS_Roof_Plate_fc.step` | STEP | 3D solid for Fusion/FreeCAD |
| `GNSS_Roof_Plate_fc.stl` | STL | 3D print for test fit |
| `TPU_Mounts.scad` | OpenSCAD source | Parametric LR900/RP3/CV50 mounts |
| `LR900_Mount.stl` | STL | TPU cradle for MicoAir LR900-P |
| `RP3_Mount.stl` | STL | TPU cradle for RadioMaster RP3 V2 |
| `CV50_Mount.stl` | STL | Nadir bracket for CV50 rangefinder |

## Related paths

- Frame CAD pack: `../JeNo-7-main/01-FRAME/`
- Official JeNo files: `../JeNo-7-main/`
- Sentinel electronics source of truth:  
  `../../F450-Sentinel/Current design folder/`
