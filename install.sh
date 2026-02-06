#!/bin/bash
# Product Engineering Agent (CAD Verifier Plugin) Installer
# Usage: curl -fsSL https://raw.githubusercontent.com/Printerpilot/cad-verifier-plugin/main/install.sh | bash

set -e
PLUGIN_DIR="${HOME}/.claude/plugins/cad-verifier-plugin"

echo "🔧 Installing Product Engineering Agent v2.0.0..."
mkdir -p "${HOME}/.claude/plugins"

if [ -d "$PLUGIN_DIR" ]; then
    echo "📦 Updating existing installation..."
    rm -rf "$PLUGIN_DIR"
fi

echo "📥 Downloading plugin..."
git clone --depth 1 https://github.com/Printerpilot/cad-verifier-plugin.git "$PLUGIN_DIR" 2>/dev/null

echo "📚 Installing dependencies..."
pip install mcp --break-system-packages --quiet 2>/dev/null || pip install mcp --quiet 2>/dev/null || true

echo ""
echo "✅ Product Engineering Agent v2.0.0 installed!"
echo "📍 Location: $PLUGIN_DIR"
echo "🔄 Restart Cowork to activate."
