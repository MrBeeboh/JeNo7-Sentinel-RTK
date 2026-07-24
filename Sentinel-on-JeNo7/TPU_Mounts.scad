// TPU Mounts — LR900-P, RP3 V2, CV50 — JeNo 7" Sentinel RTK
// ============================================================
// Three separate TPU mounting brackets.
//
// Select one: PART = "LR900", "RP3", or "CV50"
//
// All build as a single solid block with cavities carved out
// of the top — always manifold-safe.
//
// Examples:
//   openscad -o LR900_Mount.stl -D 'PART="LR900"' TPU_Mounts.scad
//   openscad -o RP3_Mount.stl   -D 'PART="RP3"'   TPU_Mounts.scad
//   openscad -o CV50_Mount.stl  -D 'PART="CV50"'  TPU_Mounts.scad
// ============================================================

PART = "LR900"; // "LR900", "RP3", "CV50", "ALL"

// ============================================================
// COMMON PARAMETERS
// ============================================================
wall = 2.0;     // wall thickness
base = 1.8;     // thickness of material under the device
m3_d = 3.2;     // M3 clearance
m2_d = 2.2;     // M2 clearance
zip = 3.0;      // zip-tie slot width

// ============================================================
// LR900-P — 915 MHz LoRa Telemetry Module
// ============================================================
// Dimensions: 43.4 × 25.8 × 11 mm (body)
// Mount: SMA whip on one end, UART header on side
// Can be zip-tied to arm or screwed to plate

module lr900_mount() {
    dx = 43.4;  // device length (X)
    dy = 25.8;  // device width (Y)
    dz = 11.0;  // device height

    ox = dx + 8;   // outer X
    oy = dy + 8;   // outer Y
    oz = dz + 2;   // total Z (base + cavity height)

    // SMA end extends 4mm beyond the end — make room
    sx = 4;  // extra on SMA end

    difference() {
        // — SOLID BLOCK —
        linear_extrude(height = oz, convexity = 4)
            offset(r = 3)
                square([ox, oy], center = true);

        // — DEVICE POCKET (carved from top, base remains) —
        translate([0, 0, oz - dz - 0.1])
            linear_extrude(height = dz + 0.2, convexity = 4)
                square([dx + 0.5, dy + 0.5], center = true);

        // — CABLE RELIEF (UART side) —
        translate([dx/2 + wall - 1, 0, base + 1])
            cube([4, 6, dz - 2], center = true);

        // — ZIP-TIE SLOTS (long axis) —
        for (x = [-1, 1])
            translate([x * 10, 0, 0])
                linear_extrude(height = oz + 1, convexity = 2)
                    square([zip, oy + 2], center = true);

        // — M3 MOUNT HOLES (through base) —
        for (x = [-1, 1], y = [-1, 1])
            translate([x * (ox/2 - 3), y * (oy/2 - 3), -0.5])
                cylinder(d = m3_d, h = base + 1, $fn = 12);
    }
}

// ============================================================
// RP3 V2 — ELRS Receiver
// ============================================================
// Dimensions: 22 × 13 × 4 mm
// Dual 65 mm 2.4 GHz antennas via IPEX

module rp3_mount() {
    dx = 22;
    dy = 13;
    dz = 4;

    ox = dx + 8;
    oy = dy + 8;
    oz = dz + 2;

    difference() {
        // — SOLID BLOCK —
        linear_extrude(height = oz, convexity = 4)
            offset(r = 3)
                square([ox, oy], center = true);

        // — DEVICE POCKET —
        translate([1, 0, oz - dz - 0.1])
            linear_extrude(height = dz + 0.2, convexity = 4)
                square([dx, dy + 0.5], center = true);

        // — ANTENNA CABLE NOTCH (rear) —
        translate([-ox/2 - 1, 0, base + 2])
            cube([4, 5, dz - 1], center = true);

        // — ZIP-TIE SLOT —
        translate([0, 0, -0.5])
            linear_extrude(height = oz + 1, convexity = 2)
                square([ox + 1, zip], center = true);

        // — M3 MOUNT HOLES —
        for (x = [-1, 1], y = [-1, 1])
            translate([x * (ox/2 - 3), y * (oy/2 - 3), -0.5])
                cylinder(d = m3_d, h = base + 1, $fn = 12);
    }
}

// ============================================================
// CV50 — 50m dToF Rangefinder
// ============================================================
// Dimensions: 28.5 × 13.6 × 21.4 mm
// Lens points down (-Z), ribbon exits one end
// Mounts under bottom plate, nadir view must be clear

module cv50_mount() {
    dx = 28.5;
    dy = 13.6;
    dz = 21.4;

    // Mounting margin
    mx = dx + 10;
    my = dy + 10;

    // Total height: base + device depth
    oz = base + dz + 1;

    difference() {
        // — SOLID BLOCK (mounts to frame top, device hangs down) —
        linear_extrude(height = oz, convexity = 4)
            offset(r = 3)
                square([mx, my], center = true);

        // — DEVICE POCKET (carved from bottom up) —
        // The device sits inside the block, lens near the bottom
        translate([0, 0, -0.1])
            linear_extrude(height = oz - base + 0.1, convexity = 4)
                square([dx + 1, dy + 1], center = true);

        // — LENS WINDOW (clear viewing aperture, bottom face) —
        translate([0, 0, -0.5])
            linear_extrude(height = base + 1, convexity = 2)
                circle(d = 12, $fn = 24);

        // — RIBBON EXIT SLOT (one narrow end) —
        translate([mx/2 - 2, 0, base + 2])
            cube([4, 8, dz - 3], center = true);

        // — M3 MOUNT HOLES (top plate, through base) —
        for (x = [-1, 1], y = [-1, 1])
            translate([x * (mx/2 - 3), y * (my/2 - 3), -0.5])
                cylinder(d = m3_d, h = base + 1, $fn = 12);

        // — WEIGHT REDUCTION (sides of the tall block) —
        for (x = [-1, 1])
            translate([x * (mx/2 - 3), 0, oz/2])
                cube([4, my - 6, oz - base - 3], center = true);
    }
}

// ============================================================
// RENDER
// ============================================================
$fn = 16;

if (PART == "LR900") {
    lr900_mount();
} else if (PART == "RP3") {
    rp3_mount();
} else if (PART == "CV50") {
    cv50_mount();
} else if (PART == "ALL") {
    translate([-35, 0, 0]) lr900_mount();
    translate([ 35, 0, 0]) rp3_mount();
    translate([  0, -35, 0]) cv50_mount();
}
