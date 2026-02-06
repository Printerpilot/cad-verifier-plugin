---
name: cad-verifier
description: "Product Engineering Agent — mathematical specs, verified CAD, assembly verification, BOM with vendor pricing"
triggers:
  - gear
  - differential
  - verify CAD
  - tooth count
  - bevel gear
  - spur gear
  - generate gear
  - mechanical assembly
  - assembly fit
  - tolerance
  - bill of materials
  - BOM
  - vendor pricing
  - math spec
---

# Product Engineering Agent — Skill Reference

Mathematical verification system for AI-generated CAD geometry, assembly fit
checking, and Bill of Materials generation with vendor pricing.

## The Problem

AI-generated gears with **zero teeth** were passing visual inspection — they
looked like smooth cylinders but had no actual gear teeth.  This plugin provides
mathematical verification to catch these issues **and** extends into full
product-engineering workflows.

## When to Use

Use this skill when:
- Generating gears (spur, bevel, helical)
- Creating differentials or gearboxes
- Verifying CAD models before manufacturing
- Calculating gear ratios and dimensions
- **Checking assembly fit** (shaft/hole tolerances)
- **Generating a priced Bill of Materials**
- **Producing mathematical specification sheets**

## Available Tools

### cad_generate_spur_gear
Generate a verified spur gear with mathematical tooth counting.

Parameters:
- `module`: Gear module (tooth size in mm)
- `num_teeth`: Number of teeth
- `face_width`: Width of gear face in mm

### cad_generate_bevel_gear
Generate a verified bevel gear for angular power transmission.

Parameters:
- `module`: Gear module
- `num_teeth`: Number of teeth
- `face_width`: Face width in mm
- `cone_angle`: Pitch cone angle (default: 45°)

### cad_generate_differential
Generate a complete differential assembly with verified gears.

Parameters:
- `module`: Gear module for all gears
- `ring_gear_teeth`: Ring gear tooth count
- `pinion_teeth`: Pinion tooth count
- `spider_teeth`: Spider gear count (default: 10)
- `side_gear_teeth`: Side gear count (default: 16)

### cad_calculate_gear_ratio
Calculate gear ratio and dimensions from tooth counts.

Parameters:
- `driver_teeth`: Number of teeth on the driver gear
- `driven_teeth`: Number of teeth on the driven gear
- `module`: Gear module (default: 2.0)

### cad_math_spec *(v2)*
Generate a full mathematical specification sheet for a gear.

Parameters:
- `module`: Gear module (mm)
- `num_teeth`: Number of teeth
- `face_width`: Face width (mm)
- `pressure_angle`: Pressure angle in degrees (default: 20°)

Returns pitch diameter, outer diameter, root diameter, base circle diameter,
addendum, dedendum, clearance, circular pitch, tooth thickness, and
face-width/module ratio.

### cad_verify_assembly *(v2)*
Verify shaft/hole assembly fit against standard tolerance grades.

Parameters:
- `shaft_diameter`: Shaft outer diameter in mm
- `hole_diameter`: Hole inner diameter in mm
- `fit_type`: `press`, `transition`, or `clearance` (default: `clearance`)

### cad_generate_bom *(v2)*
Generate a Bill of Materials with vendor pricing.

Parameters:
- `items`: Array of objects, each with:
  - `part`: Part name
  - `material`: Material key (e.g. `steel_round_bar`, `bearing_608zz`)
  - `quantity`: Quantity (default: 1)
  - `weight_kg`: Weight in kg (default: 1.0)

Supported materials: `steel_round_bar`, `aluminum_6061`, `brass_360`,
`nylon_6`, `bearing_608zz`, `bearing_6001`, `m3_socket_cap`, `m5_socket_cap`,
`dowel_pin_3mm`, `retaining_ring_8mm`.

## Gear Formulas

```
Pitch Diameter    = module × num_teeth
Outer Diameter    = module × (num_teeth + 2)
Root Diameter     = module × (num_teeth - 2.5)
Base Circle Dia.  = pitch_diameter × cos(pressure_angle)
Addendum          = module
Dedendum          = 1.25 × module
Circular Pitch    = π × module
Tooth Thickness   = circular_pitch / 2
Gear Ratio        = driven_teeth / driver_teeth
Center Distance   = module × (teeth1 + teeth2) / 2
```

## Verification Checks

1. **Toothless Detection**: Rejects gears with zero teeth
2. **Undercut Warning**: Flags gears with <17 teeth
3. **Module Validation**: Warns on non-standard modules (ISO 54)
4. **Face Width Ratio**: Checks width/module ratio (ideal: 8-12)
5. **Assembly Fit** *(v2)*: Validates press / transition / clearance tolerances
6. **BOM Pricing** *(v2)*: Cross-references vendor catalog for line totals
