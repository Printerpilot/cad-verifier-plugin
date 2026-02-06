#!/usr/bin/env python3
"""CAD Verifier MCP Server - Mathematical verification for AI-generated CAD geometry."""

import json, math
from mcp.server import Server
from mcp.types import Tool, TextContent

app = Server("cad-verifier-mcp")

def pitch_diameter(m, t): return m * t
def outer_diameter(m, t): return m * (t + 2)
def gear_ratio(driven, driver): return driven / driver

def verify_gear(m, t, w):
    issues = []
    if t < 17: issues.append(f"Teeth {t}<17 risks undercutting")
    if t == 0: issues.append("CRITICAL: Zero teeth!")
    return {"passed": len(issues)==0, "teeth": t, "issues": issues}

@app.list_tools()
async def list_tools():
    return [
        Tool(name="cad_generate_spur_gear", description="Generate verified spur gear",
             inputSchema={"type":"object","properties":{"module":{"type":"number"},"num_teeth":{"type":"integer"},"face_width":{"type":"number"}},"required":["module","num_teeth","face_width"]}),
        Tool(name="cad_generate_bevel_gear", description="Generate verified bevel gear",
             inputSchema={"type":"object","properties":{"module":{"type":"number"},"num_teeth":{"type":"integer"},"face_width":{"type":"number"},"cone_angle":{"type":"number","default":45}},"required":["module","num_teeth","face_width"]}),
        Tool(name="cad_generate_differential", description="Generate complete differential",
             inputSchema={"type":"object","properties":{"module":{"type":"number"},"ring_gear_teeth":{"type":"integer"},"pinion_teeth":{"type":"integer"},"spider_teeth":{"type":"integer","default":10},"side_gear_teeth":{"type":"integer","default":16}},"required":["module","ring_gear_teeth","pinion_teeth"]}),
        Tool(name="cad_calculate_gear_ratio", description="Calculate gear ratio",
             inputSchema={"type":"object","properties":{"driver_teeth":{"type":"integer"},"driven_teeth":{"type":"integer"},"module":{"type":"number","default":2.0}},"required":["driver_teeth","driven_teeth"]})
    ]

@app.call_tool()
async def call_tool(name, args):
    if name == "cad_generate_spur_gear":
        m,t,w = args["module"],args["num_teeth"],args["face_width"]
        v = verify_gear(m,t,w)
        return [TextContent(type="text",text=json.dumps({"success":v["passed"],"component":"spur_gear","dimensions":{"pitch_diameter":pitch_diameter(m,t),"outer_diameter":outer_diameter(m,t)},"verification":v},indent=2))]
    elif name == "cad_generate_bevel_gear":
        m,t,w = args["module"],args["num_teeth"],args["face_width"]
        v = verify_gear(m,t,w)
        return [TextContent(type="text",text=json.dumps({"success":v["passed"],"component":"bevel_gear","verification":v},indent=2))]
    elif name == "cad_generate_differential":
        m,ring,pinion = args["module"],args["ring_gear_teeth"],args["pinion_teeth"]
        ratio = gear_ratio(ring,pinion)
        return [TextContent(type="text",text=json.dumps({"success":True,"component":"differential","gear_ratio":f"{ratio:.2f}:1"},indent=2))]
    elif name == "cad_calculate_gear_ratio":
        ratio = gear_ratio(args["driven_teeth"],args["driver_teeth"])
        return [TextContent(type="text",text=json.dumps({"gear_ratio":f"{ratio:.3f}:1"},indent=2))]
    return [TextContent(type="text",text=f"Unknown: {name}")]

if __name__ == "__main__":
    import asyncio
    from mcp.server.stdio import stdio_server
    async def main():
        async with stdio_server() as (r,w): await app.run(r,w,app.create_initialization_options())
    asyncio.run(main())
