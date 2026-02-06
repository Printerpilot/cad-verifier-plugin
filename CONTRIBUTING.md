# Contributing to CAD Verifier Plugin

Thanks for your interest in contributing!

## Development Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/Printerpilot/cad-verifier-plugin.git
   cd cad-verifier-plugin
   ```

2. Install dependencies:
   ```bash
   pip install mcp --break-system-packages
   ```

3. Run the MCP server locally:
   ```bash
   python mcp-servers/cad_verifier_mcp/server.py
   ```

## Adding New Components

To add support for a new mechanical component:

1. Add the tool definition in `server.py` under `list_tools()`
2. Add the handler logic in `call_tool()`
3. Include verification checks that mathematically validate the geometry
4. Update `SKILL.md` with usage examples

## Pull Request Guidelines

- Keep changes focused and atomic
- Include verification tests for new components
- Update documentation as needed
- Follow existing code style

## Questions?

Open an issue or reach out to Troy at tkdtroy@gmail.com
