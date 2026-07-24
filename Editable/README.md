# JeNo 7" — Editable CAD pack

Converted from the official open-source **JeNo 7 v1.1.1** export so you can open **one part at a time** in FreeCAD, Fusion 360, or AutoCAD LT.

**License:** CC BY 4.0 (credit WE are FPV / JeNo authors).  
**Source:** `../JeNo-7-main/` (unchanged originals).

---

## Which tool should I use?

| Goal | Best tool | Open these |
|------|-----------|------------|
| Edit a carbon plate 3D (holes, outline, thickness) | **Fusion** or **FreeCAD** | `01-CARBON-3D/*.step` |
| Send carbon to CNC / edit 2D cut paths | **AutoCAD LT** (or Fusion sketch) | `02-CARBON-2D-DXF/` |
| Edit TPU print parts | **FreeCAD** or **Fusion** | `03-TPU-3D/from-assembly-STEP/` first; full kit in `from-STL-mesh/` |
| Print TPU as-is (no edit) | Slicer | original `../JeNo-7-main/02-TPU/*.stl` |
| See whole assembled frame | FreeCAD / Fusion | `00-MASTER/JeNo7_Assembly_from_STEP.step` |

**Recommended workflow for most changes**

1. **Fusion (other PC):** File → Open → pick a single `01-CARBON-3D/*.step`  
2. Right‑click body → **Convert** / work in **Parametric** design (or capture design history if offered)  
3. Edit, then export STEP (for FreeCAD) and DXF (for CNC)  

or

1. **FreeCAD:** File → Open → `01-CARBON-3D/Bottom_plate_3mm.FCStd` (or `.step`)  
2. Use **Part Design** / **Part** to cut holes, pad, boolean  
3. Export STEP / TechDraw DXF when done  

or

1. **AutoCAD LT:** open a file under `02-CARBON-2D-DXF/from-all-versions-dxf/`  
2. Layers: `CUT`, `POCKET`, `CHAMFER`, `COUNTERSINK`  
3. Edit polylines → save DXF for the CNC shop  

---

## Folder map

```
Editable/
├── README.md                          ← this file
├── 00-MASTER/
│   ├── JeNo7_Assembly_from_STEP.step  ← full assembly (one config)
│   ├── JeNo7_Assembly_from_STEP.FCStd
│   └── PARTS_MANIFEST.txt
├── 01-CARBON-3D/                      ← BEST for Fusion + FreeCAD
│   ├── Arm_8mm.step / .FCStd
│   ├── Arm_key.step / .FCStd
│   ├── Bottom_plate_3mm.step / .FCStd
│   ├── Middle_plate_2p5mm.step / .FCStd
│   ├── Top_plate_2p5mm.step / .FCStd
│   └── Camera_plate_25deg_O4.step / .FCStd
├── 02-CARBON-2D-DXF/
│   ├── from-all-versions-dxf/         ← BEST for AutoCAD LT (all options)
│   │   ├── 00_ALL_VERSIONS_English_layers.dxf
│   │   ├── Bottom_plate_variant_*.dxf
│   │   ├── Top_plate_variant_*.dxf
│   │   ├── Middle_plate_variant_*.dxf
│   │   ├── Camera_plate_variant_*.dxf
│   │   ├── Arm_or_reinforcement_*.dxf
│   │   └── PART_INDEX.txt
│   └── from-step-projection/          ← 2D of the STEP config only
├── 03-TPU-3D/                         ← TPU / print parts
│   ├── from-assembly-STEP/            ← cleaner BREP solids (prefer for edit)
│   └── from-STL-mesh/                 ← full kit from official STLs (heavy meshes)
├── 04-HARDWARE-REF/                   ← standoff reference solids
└── scripts/                           ← re-run converters if needed
```

---

## Important limitations (so you don’t fight the tools)

1. **These are not parametric native Fusion/SolidWorks projects.**  
   They are **BREP solids** (STEP) and **2D polylines** (DXF) reverse-exported from the official cut files. You can edit them freely, but there is **no design history** (no sketch tree from the original author).

2. **The STEP assembly is one configuration only**  
   (8 mm arms + top/bottom “04” + 25° O4 camera plates + some TPU).  
   **All carbon options** (Classic/Light/Bando, 6 mm arms, other cam plates) live in the **DXF pack** under `from-all-versions-dxf/`.

3. **TPU from STLs** (`JeNo7_*.step`) can be heavy mesh-based solids. Prefer:
   - `TPU_Rear_bumper.step`, `TPU_Antenna_*.step` from the assembly when present  
   - or re-model from the STL as a size reference  

4. **CC BY 4.0:** if you publish a remix, credit JeNo / WE are FPV.

---

## Quick start by app

### Fusion 360 (Windows PC)

1. Copy `01-CARBON-3D/` (and optionally `03-TPU-3D/TPU_*.step`) to the other PC.  
2. **Insert → Insert Mesh** is **not** what you want. Use **File → Open** on the `.step`.  
3. If Fusion asks to capture design history: **yes** if you want timeline features.  
4. For CNC: create a sketch from the face → **DXF export**, or use the ready DXFs in `02-CARBON-2D-DXF/`.

### FreeCAD (this machine)

AppImage: `~/Applications/FreeCAD_1.1.1-Linux-x86_64-py311.AppImage`

```text
File → Open → Editable/01-CARBON-3D/Bottom_plate_3mm.FCStd
```

Or open the assembly:

```text
Editable/00-MASTER/JeNo7_Assembly_from_STEP.FCStd
```

Each body is a separate `Part::Feature` you can toggle visible and edit.

### AutoCAD LT

Open either:

- **One plate:** `02-CARBON-2D-DXF/from-all-versions-dxf/Bottom_plate_variant_01.dxf`  
- **Whole sheet, English layers:** `00_ALL_VERSIONS_English_layers.dxf`

Layer meanings:

| Layer | Meaning |
|-------|---------|
| `CUT` | Outer profile / through cuts |
| `POCKET` | Pockets (partial depth) |
| `CHAMFER` | Chamfers |
| `COUNTERSINK` | Countersinks |
| `ANNOTATION` | Labels (not cut) |

See `PART_INDEX.txt` for sizes of each split plate.

---

## Re-generate this pack

If you update the upstream JeNo zip:

```bash
# 1) Split STEP → per-part STEP/FCStd (FreeCAD)
~/Applications/FreeCAD_1.1.1-Linux-x86_64-py311.AppImage -c \
  "import runpy; runpy.run_path(r'.../Editable/scripts/01_split_step_to_parts.py', run_name='__main__')"

# 2) Split ALL_VERSIONS DXF for ACAD LT
python3 ".../Editable/scripts/02_split_dxf_all_versions.py"

# 3) Project carbon STEP → DXF
~/Applications/FreeCAD_1.1.1-Linux-x86_64-py311.AppImage -c \
  "import runpy; runpy.run_path(r'.../Editable/scripts/03_project_carbon_to_dxf.py', run_name='__main__')"
```

---

## What to open first (suggested)

| If you want to… | Open |
|-----------------|------|
| Lengthen the body / move stack holes | `01-CARBON-3D/Bottom_plate_3mm.step` + `Middle_plate_2p5mm.step` + `Top_plate_2p5mm.step` |
| Change motor spacing | `01-CARBON-3D/Arm_8mm.step` |
| Change camera angle / O3 vs O4 plate | DXF `Camera_plate_variant_*.dxf` (all options) or STEP `Camera_plate_25deg_O4.step` |
| Print TPU bumper | `03-TPU-3D/TPU_Rear_bumper.step` or `JeNo7_Back_Bumper.step` |

Original untouched sources remain in `../JeNo-7-main/`.
