# -*- coding: utf-8 -*-
"""Project carbon STEP plates to 2D DXF (largest-face plane)."""
from __future__ import annotations

import math
from pathlib import Path

import FreeCAD as App
import Part
import importDXF

EDITABLE = Path(__file__).resolve().parent.parent
CARBON = EDITABLE / "01-CARBON-3D"
OUT = EDITABLE / "02-CARBON-2D-DXF" / "from-step-projection"
OUT.mkdir(parents=True, exist_ok=True)


def best_plane_projection(shape: Part.Shape) -> Part.Shape | None:
    face = max(shape.Faces, key=lambda f: abs(f.Area))
    try:
        n = face.normalAt(0.5, 0.5)
    except Exception:
        n = App.Vector(0, 0, 1)
    if n.Length < 1e-9:
        n = App.Vector(0, 0, 1)
    n.normalize()
    c = shape.BoundBox.Center

    sec = None
    for d in (0.0, 0.25, -0.25, 0.5, -0.5, 1.0, -1.0):
        pl = Part.Plane(c + App.Vector(n.x * d, n.y * d, n.z * d), n)
        trial = shape.section(pl.toShape())
        if trial.Edges:
            sec = trial
            break
    if sec is None or not sec.Edges:
        return None

    z = App.Vector(0, 0, 1)
    if abs(n.dot(z)) > 0.999:
        rot = App.Rotation()
    else:
        axis = z.cross(n)
        if axis.Length < 1e-9:
            rot = App.Rotation()
        else:
            angle = math.degrees(math.acos(max(-1.0, min(1.0, z.dot(n)))))
            rot = App.Rotation(axis, angle)

    edges2d = []
    for e in sec.Edges:
        try:
            pts = e.discretize(Deflection=0.05)
            pts2 = []
            for p in pts:
                v = App.Vector(p.x - c.x, p.y - c.y, p.z - c.z)
                v2 = rot.inverted().multVec(v)
                pts2.append(App.Vector(v2.x, v2.y, 0))
            if len(pts2) >= 2:
                edges2d.append(Part.makePolygon(pts2))
        except Exception:
            continue
    if not edges2d:
        return None
    compound = Part.Compound(edges2d)
    bb = compound.BoundBox
    compound.translate(App.Vector(-bb.XMin + 5, -bb.YMin + 5, 0))
    return compound


def main() -> int:
    for step in sorted(CARBON.glob("*.step")):
        shape = Part.Shape()
        shape.read(str(step))
        comp = best_plane_projection(shape)
        if not comp:
            print("fail", step.name)
            continue
        doc = App.newDocument("dxf")
        obj = doc.addObject("Part::Feature", step.stem)
        obj.Shape = comp
        doc.recompute()
        path = OUT / f"{step.stem}.dxf"
        importDXF.export([obj], str(path))
        App.closeDocument(doc.Name)
        print(
            "ok",
            step.name,
            "edges",
            len(comp.Edges),
            "size",
            round(comp.BoundBox.XLength, 1),
            "x",
            round(comp.BoundBox.YLength, 1),
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
