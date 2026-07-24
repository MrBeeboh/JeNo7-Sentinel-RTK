# -*- coding: utf-8 -*-
"""
Split JeNo 7 ALL_VERSIONS STEP into editable per-part files.

Run with FreeCAD AppImage:
  FreeCAD.AppImage -c Editable/scripts/01_split_step_to_parts.py
or:
  FreeCAD.AppImage Editable/scripts/01_split_step_to_parts.py
"""
from __future__ import annotations

import hashlib
import os
import re
import sys
from pathlib import Path

import FreeCAD as App
import Import
import Mesh
import MeshPart
import Part

# -----------------------------------------------------------------------------
# Paths
# -----------------------------------------------------------------------------
SCRIPT = Path(__file__).resolve()
EDITABLE = SCRIPT.parent.parent
ROOT = EDITABLE.parent
SRC_STEP = ROOT / "JeNo-7-main" / "01-FRAME" / "JeNo7_ALL_VERSIONS_1.1.1.step"
SRC_TPU = ROOT / "JeNo-7-main" / "02-TPU"

OUT_MASTER = EDITABLE / "00-MASTER"
OUT_CARBON = EDITABLE / "01-CARBON-3D"
OUT_TPU = EDITABLE / "03-TPU-3D"
OUT_HW = EDITABLE / "04-HARDWARE-REF"
OUT_DXF = EDITABLE / "02-CARBON-2D-DXF" / "from-step-projection"

for p in (OUT_MASTER, OUT_CARBON, OUT_TPU, OUT_HW, OUT_DXF):
    p.mkdir(parents=True, exist_ok=True)

# Solid names in STEP file order (MANIFOLD_SOLID_BREP sequence)
STEP_SOLID_NAMES = [
    "entretoise",
    "entretoise (1)",
    "entretoise (1) (1)",
    "entretoise (1) (1) (1)",
    "entretoise (1) (1) (1) (1)",
    "entretoise (1) (1) (1) (1) (1)",
    "entretoise (1) (1) (1) (2)",
    "entretoise (2)",
    "entretoise (2) (1)",
    "entretoise (2) (1) (1)",
    "bras 8mm",
    "mid (1)",
    "key (1)",
    "top 04",
    "bumper arriere",
    "antenne O3",
    "support antenne",
    "bottom 04",
    "bras 8mm (1)",
    "bras 8mm (2)",
    "bras 8mm (1) (1)",
    "support condo 35vx2",
    "bottom 04 (1)",
    "cam plate 25 O4",
    "entretoise 20mm 01 (3) (1) (1)",
    "entretoise 20mm 01 (3) (2)",
    "cam plate 25 O4 (1)",
]

# Map base French names -> (english_stem, category, export_2d_dxf)
# category: carbon | tpu | hardware
NAME_MAP = {
    "entretoise": ("Standoff_M3x30", "hardware", False),
    "entretoise 20mm 01": ("Standoff_M3x20", "hardware", False),
    "bras 8mm": ("Arm_8mm", "carbon", True),
    "mid": ("Middle_plate_2p5mm", "carbon", True),
    "key": ("Arm_key", "carbon", True),
    "top 04": ("Top_plate_2p5mm", "carbon", True),
    "bottom 04": ("Bottom_plate_3mm", "carbon", True),
    "cam plate 25 O4": ("Camera_plate_25deg_O4", "carbon", True),
    "bumper arriere": ("TPU_Rear_bumper", "tpu", False),
    "antenne O3": ("TPU_Antenna_O3", "tpu", False),
    "support antenne": ("TPU_Antenna_support", "tpu", False),
    "support condo 35vx2": ("TPU_Capacitor_support_35Vx2", "tpu", False),
}


def base_name(name: str) -> str:
    return re.sub(r"( \(\d+\))+$", "", name)


def geom_key(shape: Part.Shape) -> str:
    """Fingerprint so identical copies collapse to one export."""
    bb = shape.BoundBox
    payload = f"{len(shape.Faces)}|{len(shape.Edges)}|{shape.Volume:.3f}|{bb.XLength:.3f}|{bb.YLength:.3f}|{bb.ZLength:.3f}"
    return hashlib.md5(payload.encode()).hexdigest()[:12]


def sanitize(label: str) -> str:
    return re.sub(r"[^A-Za-z0-9._-]+", "_", label).strip("_")


def export_step(shape: Part.Shape, path: Path) -> None:
    shape.exportStep(str(path))


def export_fcstd(shape: Part.Shape, label: str, path: Path) -> None:
    doc = App.newDocument(sanitize(label)[:50])
    obj = doc.addObject("Part::Feature", sanitize(label)[:50])
    obj.Label = label
    obj.Shape = shape
    doc.recompute()
    doc.saveAs(str(path))
    App.closeDocument(doc.Name)


def largest_face_normal_is_z(shape: Part.Shape) -> bool:
    """True if the largest face is roughly horizontal (carbon plate)."""
    if not shape.Faces:
        return False
    face = max(shape.Faces, key=lambda f: abs(f.Area))
    try:
        n = face.normalAt(0.5, 0.5)
        return abs(n.z) > 0.85
    except Exception:
        return shape.BoundBox.ZLength < max(shape.BoundBox.XLength, shape.BoundBox.YLength) * 0.5


def project_to_dxf(shape: Part.Shape, path: Path, label: str) -> bool:
    """
    Project solid to XY as 2D wire DXF for AutoCAD LT / CNC.
    Uses section of mid-plane for flat plates; falls back to all edges projected.
    """
    try:
        bb = shape.BoundBox
        # Mid-plane section for plates
        z = (bb.ZMin + bb.ZMax) / 2.0
        plane = Part.makePlane(
            max(bb.XLength, 1) * 2 + 50,
            max(bb.YLength, 1) * 2 + 50,
            App.Vector(bb.Center.x - bb.XLength - 25, bb.Center.y - bb.YLength - 25, z),
            App.Vector(0, 0, 1),
        )
        section = shape.section(plane)
        wires = section.Wires
        if not wires:
            # fallback: compound of edges projected to z=0
            edges = []
            for e in shape.Edges:
                try:
                    # sample and rebuild is heavy; just take edges if already planar
                    if abs(e.BoundBox.ZLength) < 1e-3:
                        edges.append(e)
                except Exception:
                    pass
            if not edges:
                return False
            comp = Part.Compound(edges)
            comp.exportDxf(str(path))
            return True

        # Translate section to Z=0 and origin-ish
        compound = Part.Compound(wires)
        compound.translate(App.Vector(0, 0, -z))
        # Move min corner near 0,0 for ACAD friendliness
        cbb = compound.BoundBox
        compound.translate(App.Vector(-cbb.XMin + 5, -cbb.YMin + 5, -cbb.ZMin))
        compound.exportDxf(str(path))
        return True
    except Exception as exc:
        print(f"  DXF fail {label}: {exc}")
        return False


def mesh_stl_to_step(stl_path: Path, out_step: Path, out_fcstd: Path) -> bool:
    """Best-effort STL -> solid STEP. Complex TPU may remain a mesh shell."""
    try:
        mesh = Mesh.Mesh(str(stl_path))
        # Clean mild noise
        mesh.removeDuplicatedPoints()
        mesh.removeDuplicatedFacets()
        shape = Part.Shape()
        shape.makeShapeFromMesh(mesh.Topology, 0.1)
        shape = shape.removeSplitter()
        solids = shape.Solids
        if solids:
            result = solids[0] if len(solids) == 1 else Part.Compound(solids)
        else:
            # keep shell as shape (still useful in Fusion as BREP shell)
            result = shape
        label = stl_path.stem
        export_step(result, out_step)
        export_fcstd(result, label, out_fcstd)
        return True
    except Exception as exc:
        print(f"  STL convert fail {stl_path.name}: {exc}")
        return False


def main() -> int:
    if not SRC_STEP.is_file():
        print("Missing STEP:", SRC_STEP)
        return 1

    print("Reading", SRC_STEP)
    compound = Part.Shape()
    compound.read(str(SRC_STEP))
    solids = compound.Solids
    print(f"Solids found: {len(solids)}")
    if len(solids) != len(STEP_SOLID_NAMES):
        print(
            f"WARNING: solid count {len(solids)} != name list {len(STEP_SOLID_NAMES)}; "
            "using positional names where available."
        )

    # Master assembly doc
    master = App.newDocument("JeNo7_Assembly_Editable")
    unique: dict[str, tuple[str, str, Part.Shape, bool]] = {}
    # key -> (english, category, shape, want_dxf)

    for i, solid in enumerate(solids):
        raw = STEP_SOLID_NAMES[i] if i < len(STEP_SOLID_NAMES) else f"solid_{i:02d}"
        bname = base_name(raw)
        if bname not in NAME_MAP:
            eng, cat, want_dxf = (sanitize(bname), "carbon", True)
            print(f"  Unknown solid '{raw}' -> {eng}")
        else:
            eng, cat, want_dxf = NAME_MAP[bname]

        gkey = geom_key(solid)
        ukey = f"{eng}__{gkey}"
        if ukey in unique:
            print(f"  skip duplicate {raw} -> {eng}")
            # still add instance to master for assembly context
            obj = master.addObject("Part::Feature", f"{sanitize(eng)}_{i:02d}")
            obj.Label = f"{eng} (instance {i})"
            obj.Shape = solid
            continue

        unique[ukey] = (eng, cat, solid, want_dxf)
        obj = master.addObject("Part::Feature", sanitize(eng)[:40])
        obj.Label = eng
        obj.Shape = solid
        print(f"  keep {raw} -> {eng} [{cat}] faces={len(solid.Faces)} vol={solid.Volume:.1f}")

    master.recompute()
    master_path = OUT_MASTER / "JeNo7_Assembly_from_STEP.FCStd"
    master.saveAs(str(master_path))
    # Full assembly STEP (all instances as they sit)
    try:
        Import.export(
            [o for o in master.Objects if hasattr(o, "Shape") and o.Shape.Solids],
            str(OUT_MASTER / "JeNo7_Assembly_from_STEP.step"),
        )
    except Exception as exc:
        print("Assembly STEP export note:", exc)
        compound.exportStep(str(OUT_MASTER / "JeNo7_Assembly_from_STEP.step"))

    App.closeDocument(master.Name)

    # Per-unique-part exports (shape moved to origin for easy editing)
    print("\nExporting unique parts...")
    manifest = []
    for eng, cat, solid, want_dxf in unique.values():
        bb = solid.BoundBox
        moved = solid.copy()
        moved.translate(App.Vector(-bb.XMin, -bb.YMin, -bb.ZMin))

        if cat == "carbon":
            folder = OUT_CARBON
        elif cat == "tpu":
            folder = OUT_TPU
        else:
            folder = OUT_HW

        stem = eng
        step_path = folder / f"{stem}.step"
        fcstd_path = folder / f"{stem}.FCStd"
        export_step(moved, step_path)
        export_fcstd(moved, eng, fcstd_path)
        dxf_ok = False
        if want_dxf or (cat == "carbon" and largest_face_normal_is_z(moved)):
            dxf_path = OUT_DXF / f"{stem}.dxf"
            dxf_ok = project_to_dxf(moved, dxf_path, eng)
        manifest.append((stem, cat, str(step_path), dxf_ok))
        print(f"  wrote {stem} ({cat}) dxf={dxf_ok}")

    # Convert official TPU STLs (may include parts not in this STEP assembly)
    print("\nConverting TPU STLs...")
    if SRC_TPU.is_dir():
        for stl in sorted(SRC_TPU.glob("*.stl")):
            out_step = OUT_TPU / f"{stl.stem}.step"
            out_fc = OUT_TPU / f"{stl.stem}.FCStd"
            # Don't overwrite a better solid from STEP unless conversion succeeds and STEP missing
            if out_step.exists():
                print(f"  keep existing {out_step.name} (from STEP assembly)")
                # still write STL-derived alongside if different name
                alt_step = OUT_TPU / f"{stl.stem}__from_STL.step"
                alt_fc = OUT_TPU / f"{stl.stem}__from_STL.FCStd"
                ok = mesh_stl_to_step(stl, alt_step, alt_fc)
                print(f"  STL side-copy {stl.name}: {ok}")
            else:
                ok = mesh_stl_to_step(stl, out_step, out_fc)
                print(f"  STL {stl.name}: {ok}")

    # Manifest
    man = OUT_MASTER / "PARTS_MANIFEST.txt"
    lines = [
        "JeNo 7 editable parts (generated from official STEP export)",
        f"Source: {SRC_STEP.name}",
        "",
        f"{'Part':40} {'Cat':10} DXF",
        "-" * 60,
    ]
    for stem, cat, _, dxf_ok in sorted(manifest):
        lines.append(f"{stem:40} {cat:10} {'yes' if dxf_ok else 'no'}")
    man.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\nDone. Manifest:", man)
    return 0


if __name__ == "__main__":
    # FreeCAD -c runs as script; ensure exit code
    try:
        rc = main()
    except Exception as e:
        print("FATAL:", e)
        import traceback

        traceback.print_exc()
        rc = 1
    sys.exit(rc)
