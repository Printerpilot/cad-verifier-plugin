---
name: cad-verifier
description: Mathematical verification for CAD geometry - prevents toothless gears
triggers:
  - gear
  - differential
  - verify CAD
  - tooth count
  - bevel gear
  - spur gear
  - generate gear
  - mechanical assembly
---

# CAD Verifier Skill

Mathematical verification system for AI-generated CAD geometry.

## The Problem

AI-generated gears with **zero teeth** were passing visual inspection - they looked like smooth cylinders but had no actual gear teeth. This plugin provides mathematical verification to catch these issues.

## When to Use

Use this skill when:
- Generating gears (spur, bevel, helical)
- Creating differentials or gearboxes
- Verifying CAD models before manufacturing
- Calculating gear ratios and dimensions

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

## Gear Formulas

```
Pitch Diameter = module × num_teeth
Outer Diameter = module × (num_teeth + 2)
Root Diameter  = module × (num_teeth - 2.5)
Gear Ratio     = driven_teeth / driver_teeth
Center Distance = module × (teeth1 + teeth2) / 2
```

## Verification Checks

1. **Toothless Detection**: Rejects gears with zero teeth
2. **Undercut Warning**: Flags gears with <17 teeth
3. **Module Validation**: Warns on non-standard modules
4. **Face Width Ratio**: Checks width/module ratio (ideal: 8-12)
