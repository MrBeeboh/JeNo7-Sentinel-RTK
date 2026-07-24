// GNSS Roof Plate — JeNo 7" Sentinel RTK Build
// ==============================================
// A forward-cantilevered carbon roof plate that mounts on M3 standoffs
// above the JeNo 7 top plate. Carries the UM980 + Q39 helix forward of
// the battery so pack swaps stay unobstructed.
//
// Output modes:
//   3D model (default)    → export STL for visualization
//   export_2d = true      → export DXF for carbon cutting
//
// Example:
//   openscad -o GNSS_Roof_Plate.stl --export-format asciistl GNSS_Roof_Plate.scad
//   openscad -o GNSS_Roof_Plate.dxf -D 'export_2d=true' GNSS_Roof_Plate.scad
//
// NOTE: OpenSCAD 2021 binary STL writer is buggy on this system.
// Always use --export-format asciistl for STL output.
// The FreeCAD-generated files (GNSS_Roof_Plate_fc.*) are the
// production reference — use GNSS_Roof_Plate_fc.dxf for CNC.
//
// Coordinate system: matches JeNo 7 STEP file
//   X+ = right, Y+ = forward, Z+ = up
//   Top plate Z = 30.0–32.5mm

// ============================================================
// PARAMETERS — edit these to fit your hardware
// ============================================================

plate_thickness   = 2.5;   // [2, 2.5, 3] mm carbon plate
standoff_height   = 20;    // mm from JeNo top plate top face
screw_dia_m3      = 3.2;   // M3 clearance hole
screw_dia_m2_5    = 2.8;   // M2.5 clearance hole

// ============================================================
// STANDOFF MOUNTING — JENO 7 TOP PLATE HOLE PATTERN
// ============================================================

// These are the existing holes on the JeNo 7 top plate (Z=32.5mm).
// The roof plate uses M3 male-female standoffs screwed into these.
standoff_positions = [
    [ 20.08,  73.58],   // front right
    [-20.08,  73.58],   // front left
    [ 23.73,  41.18],   // rear right
    [-23.73,  41.18],   // rear left
];

// ============================================================
// GNSS PAYLOAD
// ============================================================

// UM980 carrier board: ~26x38mm, M2.5 on ~20x32mm pattern
um980_center   = [0, 76];
um980_mount_xy = [20, 30];           // M2.5 hole spacing (x, y)
um980_screw    = screw_dia_m2_5;

// Q39 helix antenna: 48mm dia, M3 on 38mm square
q39_center     = [0, 86];
q39_diameter   = 48;
q39_mount      = 38;                  // square spacing
q39_screw      = screw_dia_m3;
sma_hole       = 7.0;                 // SMA pass-through at Q39 center

// Cable pass-through for UM980 UART + power
cable_hole_pos = [0, 68];
cable_hole_dia = 9.0;

// UBEC — FPVKing Micro UBEC 5V/3A mounted on plate underside
// ~20×15×6mm body, zip-tie or VHB
ubec_center    = [0, 55];
ubec_size      = [20, 15, 6];

// Anti-rotation pin holes for zip-ties securing the UBEC
ubec_strap_slots = [
    [-16, 55], [16, 55]
];

// ============================================================
// PLATE OUTLINE (top-down polyline, Z=0 plane)
// ============================================================

// Matches the JeNo top plate profile in the mounting region,
// flares ~4mm wider at the GNSS section for payload clearance,
// then tapers to a rounded nose forward of the camera.
//
// The battery on the main top plate (roughly Y=-40 to Y=+55)
// is completely unobstructed — this roof only covers Y=37 to Y=94.

plate_outline = [
    // — rear edge (flat) —
    [-28, 37], [28, 37],
    // — right side, going forward —
    [28, 44],
    [27, 55],                        // matches top plate waist
    [28, 65],
    [30, 74],                        // flare starts near front standoffs
    [32, 78],
    [32, 86],                        // widest — Q39 fits with 8mm margin
    [31, 92],
    [26, 96],
    [0,  98],                         // rounded nose
    // — left side, coming back —
    [-26, 96],
    [-31, 92],
    [-32, 86],
    [-32, 78],
    [-30, 74],
    [-28, 65],
    [-27, 55],
    [-28, 44],
];

// ============================================================
// RENDER SWITCH
// ============================================================

export_2d = false;   // set true for DXF export

// ============================================================
// MODULES
// ============================================================

module main_shape_2d() {
    // Plate body with 3mm corner fillets
    offset(r = 3) polygon(plate_outline);
}

module standoff_holes_2d() {
    for (p = standoff_positions)
        translate(p) circle(d = screw_dia_m3, $fn = 24);
}

module um980_holes_2d() {
    for (x = [-1, 1], y = [-1, 1])
        translate([
            um980_center[0] + x * um980_mount_xy[0] / 2,
            um980_center[1] + y * um980_mount_xy[1] / 2
        ]) circle(d = um980_screw, $fn = 16);
}

module q39_holes_2d() {
    for (x = [-1, 1], y = [-1, 1])
        translate([
            q39_center[0] + x * q39_mount / 2,
            q39_center[1] + y * q39_mount / 2
        ]) circle(d = q39_screw, $fn = 24);
    // SMA pass-through at Q39 center
    translate(q39_center) circle(d = sma_hole, $fn = 24);
}

module cable_hole_2d() {
    translate(cable_hole_pos) circle(d = cable_hole_dia, $fn = 24);
}

module ubec_strap_slots_2d() {
    // Small slots for zip-ties securing the UBEC on the underside
    for (p = ubec_strap_slots)
        translate(p)
            square([3, 8], center = true);
}

module all_holes_2d() {
    standoff_holes_2d();
    um980_holes_2d();
    q39_holes_2d();
    cable_hole_2d();
    ubec_strap_slots_2d();
}

// ============================================================
// OUTPUT
// ============================================================

if (export_2d) {
    // 2D profile for DXF export (carbon cutter)
    difference() {
        main_shape_2d();
        all_holes_2d();
    }
} else {
    // 3D model for STL export (visualization / test print)
    color("DimGray") linear_extrude(height = plate_thickness, convexity = 10)
        difference() {
            main_shape_2d();
            all_holes_2d();
        }

    // Show the UM980 carrier as a translucent reference
    %translate([um980_center[0], um980_center[1], plate_thickness])
        color("RoyalBlue", 0.3)
            cube([26, 38, 1.6], center = true);

    // Show the Q39 helix as a translucent reference
    %translate([q39_center[0], q39_center[1], plate_thickness])
        color("MediumSeaGreen", 0.25)
            cylinder(d = q39_diameter, h = 10, $fn = 48);

    // Show standoff columns as reference
    for (p = standoff_positions) {
        %translate([p[0], p[1], -standoff_height])
            color("Silver", 0.3)
                cylinder(d = 5, h = standoff_height, $fn = 16);
    }

    // Show the UBEC on the underside as a translucent reference
    %translate([ubec_center[0], ubec_center[1], -6])
        color("Goldenrod", 0.25)
            cube([ubec_size[0], ubec_size[1], ubec_size[2]], center = true);
}
