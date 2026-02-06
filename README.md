# CAD Verifier Plugin

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Claude Cowork](https://img.shields.io/badge/Claude-Cowork%20Plugin-blueviolet)](https://claude.ai)

**Mathematical verification system for AI-generated CAD geometry.**

Prevents toothless gears from passing visual QA through mathematical tooth counting.

## Features

- **Mathematical Tooth Counting** — Counts gear teeth geometrically via polar coordinate analysis
- **Toothless Gear Detection** — Catches blank cylinders immediately  
- **Automatic Retry Loop** — Failed verifications trigger regeneration
- **Complete Differential Generation** — Ring gear, pinion, spider gears, side gears

## Installation

```bash
git clone https://github.com/Printerpilot/cad-verifier-plugin.git ~/.claude/plugins/cad-verifier-plugin
pip install build123d mcp --break-system-packages
```

## MCP Tools

| Tool | Description |
|------|-------------|
| `cad_generate_spur_gear` | Generate verified spur gear |
| `cad_generate_bevel_gear` | Generate verified bevel gear |
| `cad_generate_differential` | Generate complete differential |
| `cad_calculate_gear_ratio` | Calculate gear ratio |

## License

MIT
