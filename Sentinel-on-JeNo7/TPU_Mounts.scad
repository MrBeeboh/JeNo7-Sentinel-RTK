// TPU Mounts — LR900-P, RP3 V2, CV50 — JeNo 7" Sentinel RTK
// ============================================================
// Three separate TPU mounting brackets for the 915 MHz telemetry
// radio, ELRS receiver, and rangefinder sensor.
//
// Select one: LR900, RP3, or CV50
//
// All mount with M3 screws + nuts (or zip ties) to the JeNo
// frame, arm, or top plate.
// ============================================================

// ============================================================
// MAKE SELECTION HERE — enable only ONE
// ============================================================
PART = "LR900";   // "LR900", "RP3", "CV50", "ALL"

// ============================================================
// COMMON
// ============================================================
tpu_t = 2.0;      // wall thickness
gap   = 0.5;      // clearance gap around the device
m3_d  = 3.2;      // M3 clearance
stl_fn = 24;      // facet count

// ============================================================
// LR900-P — 915 MHz LoRa Telemetry Module
// ============================================================
// Dimensions (vendor): 43.4 × 25.8 × 11 mm
// Mount: SMA whip on one end, UART header on one side
// Place on arm or inside body, ≥200mm from RP3 antennas

module lr900_mount() {
    lx = 43.4;  // length
    ly = 25.8;  // width
    lz = 11.0;  // height

    // Base plate with the module sitting in a cradle
    // Zip-tie slots at each end for the SMA end and loose wire end

    difference() {
        // Base + wall cradle
        union() {
            // Base plate
            linear_extrude(tpu_t)
                offset(r = 3)
                    square([lx + 8, ly + 8], center = true);

            // Side walls (cradle)
            for (y = [-1, 1])
                translate([0, y * (ly/2 + 1.5), 0])
                    cube([lx + 6, tpu_t + 1, lz + 2], center = true);

            // End walls
            for (x = [-1, 1])
                translate([x * (lx/2 + 1.5), 0, 0])
                    cube([tpu_t + 1, ly + 6, lz + 2], center = true);

            // Bottom pad (under the module)
            cube([lx - 2, ly - 2, tpu_t], center = true);
        }

        // Module cavity
        translate([0, 0, tpu_t])
            cube([lx, ly, lz + 1], center = true);

        // Zip-tie slots (lengthwise)
        for (x = [-1, 1])
            translate([x * lx/3, 0, 0])
                cube([3, ly + 10, tpu_t + 1], center = true);

        // Zip-tie slots (crosswise)
        for (y = [-1, 1])
            translate([0, y * ly/3, 0])
                cube([lx + 10, 3, tpu_t + 1], center = true);

        // M3 mount holes in the base
        for (x = [-1, 1], y = [-1, 1])
            translate([x * (lx/2 + 3), y * (ly/2 + 3), 0])
                cylinder(d = m3_d, h = tpu_t + 2, $fn = 12);
    }
}

// ============================================================
// RP3 V2 — ELRS Receiver
// ============================================================
// Dimensions: 22 × 13 × 4 mm
// Dual 65mm 2.4GHz antennas (IPEX/uFL)
// Mount: 4 pads for soldered wires, or zip-tie
// Needs antennas clear of carbon, not toward Q39

module rp3_mount() {
    rx = 22;  // length
    ry = 13;  // width
    rz = 4;   // height

    difference() {
        union() {
            // Thin base plate
            linear_extrude(tpu_t)
                offset(r = 3)
                    square([rx + 6, ry + 6], center = true);

            // Side rails
            for (y = [-1, 1])
                translate([0, y * (ry/2 + 1), 0])
                    cube([rx + 4, tpu_t, rz + 2], center = true);

            // End rail (antenna side)
            translate([rx/2 + 1, 0, 0])
                cube([tpu_t, ry + 5, rz + 2], center = true);
        }

        // Module cavity (open at the back for wire routing)
        translate([-1, 0, tpu_t])
            cube([rx, ry, rz + 1], center = true);

        // Zip-tie slot
        cube([rx + 8, 2.5, tpu_t + 1], center = true);

        // Antenna exit notch
        translate([rx/2 + 2, 0, tpu_t])
            cube([4, 4, rz + 2], center = true);

        // M3 mount holes
        for (x = [-1, 1], y = [-1, 1])
            translate([x * (rx/2 + 2), y * (ry/2 + 2), 0])
                cylinder(d = m3_d, h = tpu_t + 2, $fn = 12);
    }
}

// ============================================================
// CV50 — 50m dToF Rangefinder
// ============================================================
// Mounts under the bottom plate (or arm area) with clear nadir view
// 28.5 × 13.6 × 21.4 mm (enclosure)
// Lens points down (-Z), UART ribbon goes to FC
//

module cv50_mount() {
    cx = 28.5;  // length
    cy = 13.6;  // width (narrow direction)
    cz = 21.4;  // height (lens-down direction)

    difference() {
        union() {
            // Top plate (mounts to frame)
            linear_extrude(tpu_t)
                offset(r = 3)
                    square([cx + 10, cy + 10], center = true);

            // Corner standoffs (bottom bezel)
            for (x = [-1, 1], y = [-1, 1])
                translate([x * cx/3, y * cy/3, -cz/2])
                    cylinder(d = 4, h = cz/2 + tpu_t, $fn = 8);
        }

        // Sensor cavity (lens-down)
        translate([0, 0, -cz/2])
            cube([cx + 1, cy + 1, cz + 1], center = true);

        // Lens view port (clear aperture)
        translate([0, 0, -cz - 0.5])
            cylinder(d = 10, h = cz + 2, $fn = 24);

        // Ribbon cable exit slot
        translate([cx/2 + 1, 0, -cz/4])
            cube([6, 8, cz/2], center = true);

        // M3 mount holes (top plate → frame bottom)
        for (x = [-1, 1], y = [-1, 1])
            translate([x * (cx/2 + 3), y * (cy/2 + 3), 0])
                cylinder(d = m3_d, h = tpu_t + 2, $fn = 12);
    }
}

// ============================================================
// RENDER
// ============================================================
$fn = stl_fn;

if (PART == "LR900") {
    translate([0, 0, 0]) lr900_mount();
} else if (PART == "RP3") {
    translate([0, 0, 0]) rp3_mount();
} else if (PART == "CV50") {
    translate([0, 0, 0]) cv50_mount();
} else if (PART == "ALL") {
    $fn = 16;
    translate([-30, 0, 0]) lr900_mount();
    translate([30, 0, 0]) rp3_mount();
    translate([0, -30, 0]) cv50_mount();
}
