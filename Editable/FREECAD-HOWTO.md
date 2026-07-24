# FreeCAD how-to: JeNo carbon plates

You’re not doing anything wrong. The plate is a **finished solid** (imported STEP), not a sketch with dimensions. FreeCAD lets you **select** it, but it will **not** act like Fusion’s parametric timeline until you use the right tools.

Open this file (easiest start):

```text
Editable/01-CARBON-3D/Bottom_plate_3mm_EditReady.FCStd
```

(or the plain `Bottom_plate_3mm.FCStd` — measuring works on both)

---

## 1) Measure distance between two holes

### Method A — Measure tool (FreeCAD 1.0 / 1.1)

1. Switch workbench: **Part** or **Part Design** (top dropdown).
2. Menu: **Tools → Measure**  
   (or toolbar: ruler / “Measure” icon — looks like a measuring tape).
3. In the Measure panel, choose **Distance** (or **Linear distance**).
4. Click **first** hole edge (or the circle edge of the hole).
5. Click **second** hole edge.
6. Read the distance in the panel / on-screen.

**Tips**

- Zoom in so you click the **circular edge** of the hole, not a random face.
- If it measures face-to-face oddly, click **vertex** (corner points on the circle) or use Method B.
- Units are **mm** for these files.

### Method B — Two centers via Draft (very reliable)

1. Workbench: **Draft**.
2. Select the bottom plate solid in the tree (left).
3. Menu: **Draft → Utils → Shape 2D view** is optional; often skip.
4. Easier: Workbench **Part** → select a **circular hole edge** (one click on the circle).
5. Look at the bottom status / **Combo View → Model → Data** — or use:

**Part → Measure → Linear length** (older builds) / **Tools → Measure**.

### Method C — Python console (always works)

1. Menu: **View → Panels → Python console**.
2. Select **hole edge 1** (one circular edge), note it, or run after selecting two edges:

```python
# Select TWO circular edges (Ctrl+click), then run:
import FreeCAD as App
import FreeCADGui as Gui
sel = Gui.Selection.getSelectionEx()[0]
e1, e2 = sel.SubObjects[0], sel.SubObjects[1]
c1 = e1.Curve.Center
c2 = e2.Curve.Center
d = c1.distanceToPoint(c2)
print(f"Center-to-center: {d:.3f} mm")
print(f"  hole1 center: ({c1.x:.3f}, {c1.y:.3f}, {c1.z:.3f})")
print(f"  hole2 center: ({c2.x:.3f}, {c2.y:.3f}, {c2.z:.3f})")
```

That’s the **true hole spacing** CNC cares about.

### Method D — Bounding box of whole plate

```python
s = App.ActiveDocument.ActiveObject.Shape  # or get by name
print(s.BoundBox.XLength, s.BoundBox.YLength, s.BoundBox.ZLength)
```

Bottom plate should be about **97 × 217 × 3 mm**.

---

## 2) Why you “can’t do anything” with it

| What you expect (Fusion-style) | What this file is |
|--------------------------------|-------------------|
| Drag a dimension, holes move | **No history** — solid only |
| Double-click sketch | There is **no sketch** yet |
| Edit feature tree | Only one solid: `Part::Feature` or `BaseFeature` |

So: **selecting ≠ editing**. You must **add** features (sketch + pocket, or boolean cut).

---

## 3) How to actually modify the plate

### A) Cut a new hole (Part Design) — recommended

1. Open `Bottom_plate_3mm_EditReady.FCStd`.
2. Workbench: **Part Design**.
3. In the tree, **double-click `Body`** (active body is bold/highlighted).
4. Click the **large flat face** of the plate (the top surface).
5. Toolbar: **Create sketch**.
6. Draw a **circle** where you want a hole.
7. Close sketch (right-click → Close / same sketch icon).
8. **Pocket** → type Through all (or 3 mm).
9. You now have an editable feature in the tree.

### B) Boolean cut (Part workbench) — simple

1. Workbench: **Part**.
2. Create a cylinder: **Part → Primitives → Cylinder** (radius = hole, height = 10 mm).
3. Place it through the plate (Placement in Data tab: Position X/Y/Z).
4. Select **plate**, then **Ctrl+select cylinder**.
5. **Part → Boolean → Cut**.

### C) Don’t fight FreeCAD — use AutoCAD LT for 2D hole moves

If you only need to move holes for CNC:

1. Open  
   `Editable/02-CARBON-2D-DXF/from-all-versions-dxf/Bottom_plate_variant_01.dxf`  
   in **AutoCAD LT**.
2. Move circles / polylines.
3. Save DXF → send to CNC.

That’s often faster than FreeCAD for pure 2D carbon.

### D) Fusion (other PC) — often easiest for “edit solid”

1. Copy `Bottom_plate_3mm.step` to the Fusion PC.
2. **File → Open** the STEP.
3. **Create → Create Sketch** on the face → project geometry / draw holes → extrude cut.
4. Or **Modify → Press Pull** on faces/holes where it allows.

---

## 4) Selection tips in FreeCAD

| Want to select… | How |
|-----------------|-----|
| Whole solid | Click in **tree** (left), not the 3D view |
| One face | Click face once; hover shows face |
| Hole circle | Zoom in, click the **edge** of the hole |
| Second object | **Ctrl+click** |
| Clear selection | Click empty space |

Tree icons:

- **Solid / ImportedSolid** — fine for measure + Part boolean  
- **Body → BaseFeature** — use this path for **Sketch / Pocket**  

---

## 5) Common “it won’t let me” fixes

1. **Sketch icon greyed out**  
   - Activate **Body** (double-click it).  
   - Select a **flat face** first.  
   - Must be on **Part Design** workbench.

2. **Measure does nothing**  
   - Need **two** selections (two edges/vertices).  
   - Or use Python method C above.

3. **Can’t drag the solid**  
   - Imported solids don’t “drag dimensions.”  
   - Change **Placement** in **Data** tab (X/Y/Z) only moves the whole part.

4. **Everything is tiny or huge**  
   - Scroll middle mouse to zoom; these parts are ~200 mm — if the view is empty, press **V then F** (view fit / fit all) or click **Fit all** in the view toolbar.

5. **Accidental “Transform” mode**  
   - Press **Esc** or right-click → clear transform.

---

## 6) Quick checklist for “measure two motor holes”

1. Open `Bottom_plate_3mm_EditReady.FCStd`  
2. **V then F** (fit all)  
3. Zoom to two holes  
4. **Tools → Measure → Distance**  
5. Click circle edge 1, circle edge 2  
6. Or: select two edges → paste Method C in Python console  

---

## 7) If you want Fusion-like editing long term

Best path for big redesigns:

1. Edit in **Fusion** from the `.step`, **or**  
2. Rebuild critical holes as a **new sketch** on the face in FreeCAD Part Design, then pocket — leave the import as BaseFeature.

You’re not blocked by a lock; FreeCAD is just treating this as a **brick of geometry** until you add sketches/features on top.
