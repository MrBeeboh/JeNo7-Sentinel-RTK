#!/usr/bin/env python3
"""
Split JeNo7_ALL_VERSIONS DXF into individual plate drawings for AutoCAD LT.

- Clusters cut geometry by proximity
- Renames French layers to English CNC-friendly names
- Moves each part near origin
- Names parts by size heuristics + index (see PART_INDEX.txt)
"""
from __future__ import annotations

from collections import deque
from pathlib import Path

import ezdxf
from ezdxf import bbox as ezbbox
from ezdxf.math import Vec3

ROOT = Path(__file__).resolve().parent.parent.parent
SRC = ROOT / "JeNo-7-main" / "01-FRAME" / "JeNo7_ALL_VERSIONS_1.1.1.dxf"
OUT = ROOT / "Editable" / "02-CARBON-2D-DXF" / "from-all-versions-dxf"
OUT.mkdir(parents=True, exist_ok=True)

# Layers that define actual cut/machining geometry
CUT_LAYERS = {
    "Calque1",
    "Calque1_pocket",
    "Calque1_chamfered",
    "Calque1_countersunk",
    "pocket",
    "0",  # some outlines live on 0
}

LAYER_RENAME = {
    "Calque1": "CUT",
    "Calque1_pocket": "POCKET",
    "Calque1_chamfered": "CHAMFER",
    "Calque1_countersunk": "COUNTERSINK",
    "pocket": "POCKET",
    "0": "CUT",
    "Calque2": "ANNOTATION",
    "DIMENSION": "DIMENSION",
    "Defpoints": "Defpoints",
}

GEOM_TYPES = {"LINE", "LWPOLYLINE", "POLYLINE", "CIRCLE", "ARC", "SPLINE", "ELLIPSE"}


def entity_bbox(e):
    try:
        box = ezbbox.extents([e])
        if box is None:
            return None
        return box.extmin.x, box.extmin.y, box.extmax.x, box.extmax.y
    except Exception:
        return None


def name_for_size(w: float, h: float, idx: int) -> str:
    """Heuristic names from known JeNo plate footprints (mm)."""
    a, b = (w, h) if w >= h else (h, w)  # a = long side
    # bottoms ~94 x 217
    if 90 <= w <= 100 and 200 <= h <= 230:
        return f"Bottom_plate_variant_{idx:02d}"
    if 200 <= w <= 230 and 90 <= h <= 100:
        return f"Bottom_plate_variant_{idx:02d}"
    # tops ~74 x 195
    if 70 <= w <= 80 and 180 <= h <= 210:
        return f"Top_plate_variant_{idx:02d}"
    if 180 <= w <= 210 and 70 <= h <= 80:
        return f"Top_plate_variant_{idx:02d}"
    # middle-ish ~94 x 78
    if 90 <= w <= 100 and 70 <= h <= 85:
        return f"Middle_plate_variant_{idx:02d}"
    if 70 <= w <= 85 and 90 <= h <= 100:
        return f"Middle_plate_variant_{idx:02d}"
    # camera plates ~57-92 x 40-60
    if 50 <= min(w, h) <= 95 and 35 <= max(w, h) <= 100 and max(w, h) < 120:
        return f"Camera_plate_variant_{idx:02d}"
    # arms / long narrow ~23 x 140-200
    if min(w, h) < 30 and max(w, h) > 130:
        return f"Arm_or_reinforcement_{idx:02d}"
    # key-ish
    if 30 <= min(w, h) <= 40 and 14 <= max(w, h) <= 20:
        return f"Key_variant_{idx:02d}"
    if 14 <= min(w, h) <= 20 and 30 <= max(w, h) <= 40:
        return f"Key_variant_{idx:02d}"
    # short thin strip
    if min(w, h) < 20 and max(w, h) > 100:
        return f"Strip_or_brace_{idx:02d}"
    return f"Plate_{idx:02d}_{int(round(w))}x{int(round(h))}mm"


def main() -> int:
    if not SRC.is_file():
        print("Missing", SRC)
        return 1

    doc = ezdxf.readfile(str(SRC))
    msp = doc.modelspace()

    # Collect cut geometry entities
    items = []  # (bbox, entity)
    for e in msp:
        if e.dxftype() not in GEOM_TYPES:
            continue
        layer = e.dxf.layer
        if layer not in CUT_LAYERS:
            continue
        # Skip zero-size junk on layer 0 if it's not real geom - keep all for now
        bb = entity_bbox(e)
        if not bb:
            continue
        x0, y0, x1, y1 = bb
        if (x1 - x0) * (y1 - y0) < 1e-6 and e.dxftype() not in ("CIRCLE", "ARC"):
            # points/zero - skip unless circle
            if e.dxftype() not in ("CIRCLE", "ARC", "LINE"):
                continue
        items.append((bb, e))

    print(f"Cut geometry entities: {len(items)}")

    # Cluster
    THRESH = 8.0
    used = [False] * len(items)
    clusters = []
    for i in range(len(items)):
        if used[i]:
            continue
        q = deque([i])
        used[i] = True
        members = [i]
        while q:
            j = q.popleft()
            a, b, c, d = items[j][0]
            a -= THRESH
            b -= THRESH
            c += THRESH
            d += THRESH
            for k in range(len(items)):
                if used[k]:
                    continue
                a2, b2, c2, d2 = items[k][0]
                if a2 <= c and c2 >= a and b2 <= d and d2 >= b:
                    used[k] = True
                    q.append(k)
                    members.append(k)
        xs0 = [items[m][0][0] for m in members]
        ys0 = [items[m][0][1] for m in members]
        xs1 = [items[m][0][2] for m in members]
        ys1 = [items[m][0][3] for m in members]
        bb = (min(xs0), min(ys0), max(xs1), max(ys1))
        w, h = bb[2] - bb[0], bb[3] - bb[1]
        if w * h < 80:  # skip tiny debris
            continue
        clusters.append((bb, members))

    clusters.sort(key=lambda c: -((c[0][2] - c[0][0]) * (c[0][3] - c[0][1])))
    print(f"Clusters kept: {len(clusters)}")

    index_lines = [
        "JeNo 7 — split from JeNo7_ALL_VERSIONS_1.1.1.dxf",
        "Layers: CUT / POCKET / CHAMFER / COUNTERSINK",
        "Units: mm (as original)",
        "",
        f"{'#':3} {'filename':42} {'W':7} {'H':7} {'ents':5}",
        "-" * 70,
    ]

    # Also export a full sheet with English layer names (all versions still together)
    full = ezdxf.new(dxfversion=doc.dxfversion)
    full.header["$INSUNITS"] = 4  # mm
    for old, new in LAYER_RENAME.items():
        if new not in full.layers:
            full.layers.add(new)
    fmsp = full.modelspace()
    for e in msp:
        if e.dxftype() not in GEOM_TYPES and e.dxftype() not in ("TEXT", "MTEXT"):
            continue
        try:
            ne = e.copy()
        except Exception:
            continue
        old_layer = e.dxf.layer
        ne.dxf.layer = LAYER_RENAME.get(old_layer, old_layer)
        try:
            fmsp.add_entity(ne)
        except Exception:
            pass
    full_path = OUT / "00_ALL_VERSIONS_English_layers.dxf"
    full.saveas(str(full_path))
    print("Wrote", full_path.name)

    for idx, (bb, members) in enumerate(clusters, start=1):
        x0, y0, x1, y1 = bb
        w, h = x1 - x0, y1 - y0
        stem = name_for_size(w, h, idx)
        # ensure unique filename
        path = OUT / f"{stem}.dxf"
        n = 2
        while path.exists():
            path = OUT / f"{stem}_r{n}.dxf"
            n += 1

        new = ezdxf.new(dxfversion="AC1027")  # 2013, fine for ACAD LT
        new.header["$INSUNITS"] = 4  # millimeters
        for lyr in ("CUT", "POCKET", "CHAMFER", "COUNTERSINK", "ANNOTATION"):
            new.layers.add(lyr)
        nmsp = new.modelspace()

        # origin padding
        ox, oy = x0 - 5.0, y0 - 5.0
        for mi in members:
            e = items[mi][1]
            try:
                ne = e.copy()
            except Exception:
                continue
            old_layer = e.dxf.layer
            ne.dxf.layer = LAYER_RENAME.get(old_layer, "CUT")
            # translate entity geometry toward origin
            try:
                ne.translate(-ox, -oy, 0)
            except Exception:
                # older fallback: manual for common types
                try:
                    if e.dxftype() == "CIRCLE":
                        c = ne.dxf.center
                        ne.dxf.center = Vec3(c.x - ox, c.y - oy, c.z)
                    elif e.dxftype() == "LINE":
                        s, t = ne.dxf.start, ne.dxf.end
                        ne.dxf.start = Vec3(s.x - ox, s.y - oy, s.z)
                        ne.dxf.end = Vec3(t.x - ox, t.y - oy, t.z)
                except Exception:
                    pass
            try:
                nmsp.add_entity(ne)
            except Exception:
                pass

        new.saveas(str(path))
        index_lines.append(
            f"{idx:3d} {path.name:42} {w:7.1f} {h:7.1f} {len(members):5d}"
        )
        print(f"  {path.name:42} {w:7.1f}x{h:7.1f}  n={len(members)}")

    index_path = OUT / "PART_INDEX.txt"
    index_path.write_text("\n".join(index_lines) + "\n", encoding="utf-8")
    print("Index:", index_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
