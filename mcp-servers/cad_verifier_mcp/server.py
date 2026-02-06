#!/usr/bin/env python3
"""Product Engineering Agent MCP Server v2.0.0

Mathematical specs, verified CAD generation, assembly verification,
and BOM with vendor pricing.
"""

import json, math
from mcp.server import Server
from mcp.types import Tool, TextContent

app = Server("cad-verifier-mcp")

# ---------------------------------------------------------------------------
# Gear math helpers
# ---------------------------------------------------------------------------

def pitch_diameter(m, t): return m * t
def outer_diameter(m, t): return m * (t + 2)
def root_diameter(m, t): return m * (t - 2.5)
def gear_ratio(driven, driver): return driven / driver
def center_distance(m, t1, t2): return m * (t1 + t2) / 2


def verify_gear(m, t, w):
    """Return a verification dict for a single gear."""
    issues = []
    if t == 0:
        issues.append("CRITICAL: Zero teeth detected — blank cylinder")
    if 0 < t < 17:
        issues.append(f"Teeth {t}<17 risks undercutting")
    standard_modules = {0.5, 0.8, 1.0, 1.25, 1.5, 2.0, 2.5, 3.0, 4.0, 5.0, 6.0, 8.0, 10.0}
    if m not in standard_modules:
        issues.append(f"Module {m} is non-standard (ISO 54)")
    ratio = w / m if m else 0
    if ratio and not (8 <= ratio <= 12):
        issues.append(f"Face-width/module ratio {ratio:.1f} outside ideal 8-12")
    return {"passed": len(issues) == 0, "teeth": t, "pitch_diameter": pitch_diameter(m, t),
            "outer_diameter": outer_diameter(m, t), "root_diameter": root_diameter(m, t), "issues": issues}


# ---------------------------------------------------------------------------
# Assembly verification helpers
# ---------------------------------------------------------------------------

_TOLERANCE_GRADES = {
    "press":      {"min_interference_mm": 0.01, "max_interference_mm": 0.05},
    "transition": {"min_clearance_mm": -0.02, "max_clearance_mm": 0.02},
    "clearance":  {"min_clearance_mm": 0.02, "max_clearance_mm": 0.10},
}


def verify_assembly_fit(shaft_dia, hole_dia, fit_type="clearance"):
    """Check shaft/hole fit against standard tolerance grades."""
    issues = []
    diff = hole_dia - shaft_dia
    spec = _TOLERANCE_GRADES.get(fit_type, _TOLERANCE_GRADES["clearance"])

    if fit_type == "press":
        interference = shaft_dia - hole_dia
        if interference < spec["min_interference_mm"]:
            issues.append(f"Interference {interference:.4f} mm below minimum {spec['min_interference_mm']} mm")
        if interference > spec["max_interference_mm"]:
            issues.append(f"Interference {interference:.4f} mm exceeds maximum {spec['max_interference_mm']} mm")
    else:
        if diff < spec["min_clearance_mm"]:
            issues.append(f"Clearance {diff:.4f} mm below minimum {spec['min_clearance_mm']} mm")
        if diff > spec["max_clearance_mm"]:
            issues.append(f"Clearance {diff:.4f} mm exceeds maximum {spec['max_clearance_mm']} mm")

    return {"passed": len(issues) == 0, "shaft_diameter": shaft_dia, "hole_diameter": hole_dia,
            "fit_type": fit_type, "actual_clearance_mm": round(diff, 4), "issues": issues}


# ---------------------------------------------------------------------------
# BOM / vendor pricing helpers
# ---------------------------------------------------------------------------

_VENDOR_CATALOG = {
    "steel_round_bar":   {"unit": "per_kg", "price_usd": 2.50, "vendor": "MetalsDepot"},
    "aluminum_6061":     {"unit": "per_kg", "price_usd": 4.80, "vendor": "MetalsDepot"},
    "brass_360":         {"unit": "per_kg", "price_usd": 7.20, "vendor": "MetalsDepot"},
    "nylon_6":           {"unit": "per_kg", "price_usd": 5.00, "vendor": "McMaster-Carr"},
    "bearing_608zz":     {"unit": "each",   "price_usd": 1.25, "vendor": "McMaster-Carr"},
    "bearing_6001":      {"unit": "each",   "price_usd": 3.40, "vendor": "McMaster-Carr"},
    "m3_socket_cap":     {"unit": "per_100", "price_usd": 4.50, "vendor": "McMaster-Carr"},
    "m5_socket_cap":     {"unit": "per_100", "price_usd": 7.80, "vendor": "McMaster-Carr"},
    "dowel_pin_3mm":     {"unit": "per_50",  "price_usd": 6.00, "vendor": "McMaster-Carr"},
    "retaining_ring_8mm":{"unit": "per_50",  "price_usd": 5.50, "vendor": "McMaster-Carr"},
}


def generate_bom(items):
    """Build a priced BOM from a list of {part, material, quantity, weight_kg?} dicts."""
    bom_lines = []
    total = 0.0
    for item in items:
        mat = item.get("material", "").lower().replace(" ", "_").replace("-", "_")
        catalog = _VENDOR_CATALOG.get(mat)
        if catalog is None:
            bom_lines.append({**item, "unit_price": "N/A", "line_total": "N/A",
                              "vendor": "unknown", "note": f"Material '{item.get('material')}' not in catalog"})
            continue
        qty = item.get("quantity", 1)
        weight = item.get("weight_kg", 1.0)
        if catalog["unit"] == "per_kg":
            line_total = round(catalog["price_usd"] * weight * qty, 2)
        elif catalog["unit"] == "each":
            line_total = round(catalog["price_usd"] * qty, 2)
        else:
            line_total = round(catalog["price_usd"] * qty, 2)
        total += line_total
        bom_lines.append({**item, "unit_price_usd": catalog["price_usd"],
                          "unit": catalog["unit"], "line_total_usd": line_total,
                          "vendor": catalog["vendor"]})
    return {"bom": bom_lines, "total_usd": round(total, 2)}


# ---------------------------------------------------------------------------
# Mathematical specification helpers
# ---------------------------------------------------------------------------

def math_spec(module, num_teeth, face_width, pressure_angle_deg=20.0):
    """Return a full mathematical specification sheet for a gear."""
    pd = pitch_diameter(module, num_teeth)
    od = outer_diameter(module, num_teeth)
    rd = root_diameter(module, num_teeth)
    addendum = module
    dedendum = 1.25 * module
    clearance = 0.25 * module
    base_circle = pd * math.cos(math.radians(pressure_angle_deg))
    circular_pitch = math.pi * module
    tooth_thickness = circular_pitch / 2

    return {
        "module": module,
        "num_teeth": num_teeth,
        "pressure_angle_deg": pressure_angle_deg,
        "pitch_diameter_mm": round(pd, 4),
        "outer_diameter_mm": round(od, 4),
        "root_diameter_mm": round(rd, 4),
        "base_circle_diameter_mm": round(base_circle, 4),
        "addendum_mm": round(addendum, 4),
        "dedendum_mm": round(dedendum, 4),
        "clearance_mm": round(clearance, 4),
        "circular_pitch_mm": round(circular_pitch, 4),
        "tooth_thickness_mm": round(tooth_thickness, 4),
        "face_width_mm": face_width,
        "face_width_module_ratio": round(face_width / module if module else 0, 2),
    }


# ===================================================================
# MCP Tool definitions
# ===================================================================

@app.list_tools()
async def list_tools():
    return [
        # -- Existing gear tools --
        Tool(name="cad_generate_spur_gear", description="Generate verified spur gear with mathematical tooth counting",
             inputSchema={"type":"object","properties":{
                 "module":{"type":"number","description":"Gear module (tooth size in mm)"},
                 "num_teeth":{"type":"integer","description":"Number of teeth"},
                 "face_width":{"type":"number","description":"Width of gear face in mm"}
             },"required":["module","num_teeth","face_width"]}),

        Tool(name="cad_generate_bevel_gear", description="Generate verified bevel gear for angular power transmission",
             inputSchema={"type":"object","properties":{
                 "module":{"type":"number"},
                 "num_teeth":{"type":"integer"},
                 "face_width":{"type":"number"},
                 "cone_angle":{"type":"number","default":45,"description":"Pitch cone angle in degrees"}
             },"required":["module","num_teeth","face_width"]}),

        Tool(name="cad_generate_differential", description="Generate complete differential assembly with verified gears",
             inputSchema={"type":"object","properties":{
                 "module":{"type":"number"},
                 "ring_gear_teeth":{"type":"integer"},
                 "pinion_teeth":{"type":"integer"},
                 "spider_teeth":{"type":"integer","default":10},
                 "side_gear_teeth":{"type":"integer","default":16}
             },"required":["module","ring_gear_teeth","pinion_teeth"]}),

        Tool(name="cad_calculate_gear_ratio", description="Calculate gear ratio and dimensions from tooth counts",
             inputSchema={"type":"object","properties":{
                 "driver_teeth":{"type":"integer"},
                 "driven_teeth":{"type":"integer"},
                 "module":{"type":"number","default":2.0}
             },"required":["driver_teeth","driven_teeth"]}),

        # -- v2 Mathematical specification --
        Tool(name="cad_math_spec", description="Generate full mathematical specification sheet for a gear",
             inputSchema={"type":"object","properties":{
                 "module":{"type":"number","description":"Gear module (mm)"},
                 "num_teeth":{"type":"integer"},
                 "face_width":{"type":"number","description":"Face width (mm)"},
                 "pressure_angle":{"type":"number","default":20.0,"description":"Pressure angle in degrees"}
             },"required":["module","num_teeth","face_width"]}),

        # -- v2 Assembly verification --
        Tool(name="cad_verify_assembly", description="Verify shaft/hole assembly fit against tolerance grades",
             inputSchema={"type":"object","properties":{
                 "shaft_diameter":{"type":"number","description":"Shaft OD in mm"},
                 "hole_diameter":{"type":"number","description":"Hole ID in mm"},
                 "fit_type":{"type":"string","enum":["press","transition","clearance"],"default":"clearance",
                             "description":"Fit type: press, transition, or clearance"}
             },"required":["shaft_diameter","hole_diameter"]}),

        # -- v2 BOM with vendor pricing --
        Tool(name="cad_generate_bom", description="Generate Bill of Materials with vendor pricing",
             inputSchema={"type":"object","properties":{
                 "items":{"type":"array","items":{"type":"object","properties":{
                     "part":{"type":"string","description":"Part name"},
                     "material":{"type":"string","description":"Material key (e.g. steel_round_bar, bearing_608zz)"},
                     "quantity":{"type":"integer","default":1},
                     "weight_kg":{"type":"number","default":1.0}
                 },"required":["part","material"]}}
             },"required":["items"]}),
    ]


# ===================================================================
# MCP Tool handlers
# ===================================================================

@app.call_tool()
async def call_tool(name, args):
    # -- Gear generation tools (v1) --
    if name == "cad_generate_spur_gear":
        m, t, w = args["module"], args["num_teeth"], args["face_width"]
        v = verify_gear(m, t, w)
        spec = math_spec(m, t, w)
        return [TextContent(type="text", text=json.dumps({
            "success": v["passed"], "component": "spur_gear",
            "dimensions": {"pitch_diameter": pitch_diameter(m, t), "outer_diameter": outer_diameter(m, t)},
            "specification": spec, "verification": v
        }, indent=2))]

    elif name == "cad_generate_bevel_gear":
        m, t, w = args["module"], args["num_teeth"], args["face_width"]
        v = verify_gear(m, t, w)
        spec = math_spec(m, t, w)
        return [TextContent(type="text", text=json.dumps({
            "success": v["passed"], "component": "bevel_gear",
            "cone_angle": args.get("cone_angle", 45),
            "specification": spec, "verification": v
        }, indent=2))]

    elif name == "cad_generate_differential":
        m = args["module"]
        ring, pinion = args["ring_gear_teeth"], args["pinion_teeth"]
        spider = args.get("spider_teeth", 10)
        side = args.get("side_gear_teeth", 16)
        ratio = gear_ratio(ring, pinion)
        verifications = {
            "ring_gear": verify_gear(m, ring, m * 10),
            "pinion": verify_gear(m, pinion, m * 10),
            "spider_gears": verify_gear(m, spider, m * 8),
            "side_gears": verify_gear(m, side, m * 8),
        }
        all_passed = all(v["passed"] for v in verifications.values())
        return [TextContent(type="text", text=json.dumps({
            "success": all_passed, "component": "differential",
            "gear_ratio": f"{ratio:.2f}:1", "verifications": verifications
        }, indent=2))]

    elif name == "cad_calculate_gear_ratio":
        m = args.get("module", 2.0)
        driven, driver = args["driven_teeth"], args["driver_teeth"]
        ratio = gear_ratio(driven, driver)
        return [TextContent(type="text", text=json.dumps({
            "gear_ratio": f"{ratio:.3f}:1",
            "center_distance_mm": center_distance(m, driven, driver)
        }, indent=2))]

    # -- v2 tools --
    elif name == "cad_math_spec":
        m, t, w = args["module"], args["num_teeth"], args["face_width"]
        pa = args.get("pressure_angle", 20.0)
        spec = math_spec(m, t, w, pa)
        return [TextContent(type="text", text=json.dumps({"specification": spec}, indent=2))]

    elif name == "cad_verify_assembly":
        shaft = args["shaft_diameter"]
        hole = args["hole_diameter"]
        fit = args.get("fit_type", "clearance")
        result = verify_assembly_fit(shaft, hole, fit)
        return [TextContent(type="text", text=json.dumps(result, indent=2))]

    elif name == "cad_generate_bom":
        result = generate_bom(args["items"])
        return [TextContent(type="text", text=json.dumps(result, indent=2))]

    return [TextContent(type="text", text=f"Unknown tool: {name}")]


if __name__ == "__main__":
    import asyncio
    from mcp.server.stdio import stdio_server
    async def main():
        async with stdio_server() as (r, w):
            await app.run(r, w, app.create_initialization_options())
    asyncio.run(main())
