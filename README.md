# Product Engineering Agent (CAD Verifier Plugin)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Claude Cowork](https://img.shields.io/badge/Claude-Cowork%20Plugin-blueviolet)](https://claude.ai)

**v2.0.0 — Mathematical specs, verified CAD generation, assembly verification, and BOM with vendor pricing.**

Prevents toothless gears from passing visual QA through mathematical tooth counting, verifies assembly tolerances, and generates priced Bills of Materials.

## Features

- **Mathematical Tooth Counting** — Counts gear teeth geometrically via polar coordinate analysis
- **Toothless Gear Detection** — Catches blank cylinders immediately
- **Automatic Retry Loop** — Failed verifications trigger regeneration
- **Complete Differential Generation** — Ring gear, pinion, spider gears, side gears
- **Mathematical Specification Sheets** *(v2)* — Full gear geometry specs (diameters, addendum, dedendum, base circle, etc.)
- **Assembly Fit Verification** *(v2)* — Validates press / transition / clearance fits against tolerance grades
- **BOM with Vendor Pricing** *(v2)* — Generates a Bill of Materials with line-item costs from a vendor catalog

## Installation

```bash
git clone https://github.com/Printerpilot/cad-verifier-plugin.git ~/.claude/plugins/cad-verifier-plugin
pip install build123d mcp --break-system-packages
```

Or use the one-liner:

```bash
curl -fsSL https://raw.githubusercontent.com/Printerpilot/cad-verifier-plugin/main/install.sh | bash
```

## MCP Tools

| Tool | Description |
|------|-------------|
| `cad_generate_spur_gear` | Generate verified spur gear |
| `cad_generate_bevel_gear` | Generate verified bevel gear |
| `cad_generate_differential` | Generate complete differential |
| `cad_calculate_gear_ratio` | Calculate gear ratio |
| `cad_math_spec` | Full mathematical specification sheet *(v2)* |
| `cad_verify_assembly` | Verify shaft/hole assembly fit *(v2)* |
| `cad_generate_bom` | Bill of Materials with vendor pricing *(v2)* |

## Quick Examples

### Generate a gear with full spec sheet
```
cad_generate_spur_gear(module=2, num_teeth=24, face_width=20)
```

### Verify a shaft/hole fit
```
cad_verify_assembly(shaft_diameter=8.01, hole_diameter=8.00, fit_type="press")
```

### Price a Bill of Materials
```
cad_generate_bom(items=[
  {"part": "Main Shaft", "material": "steel_round_bar", "quantity": 1, "weight_kg": 0.45},
  {"part": "Bearing A", "material": "bearing_608zz", "quantity": 2}
])
```

## License

MIT
