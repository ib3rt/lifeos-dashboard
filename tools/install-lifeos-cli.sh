#!/bin/bash
# Life OS CLI Installer
# One-command installation for OpenClaw/Life OS

set -e

INSTALL_DIR="${INSTALL_DIR:-$HOME/.lifeos}"
WORKSPACE_DIR="${WORKSPACE_DIR:-$HOME/.openclaw/workspace}"
BIN_DIR="${BIN_DIR:-$HOME/.local/bin}"

echo "🦾 Life OS CLI Installer"
echo "========================"
echo ""

# Create directories
mkdir -p "$INSTALL_DIR" "$WORKSPACE_DIR" "$BIN_DIR"
mkdir -p "$WORKSPACE_DIR/agents" "$WORKSPACE_DIR/memory" "$WORKSPACE_DIR/tools"

echo "✅ Directories created"

# Create main lifeos command
cat > "$BIN_DIR/lifeos" << 'EOF'
#!/bin/bash
# Life OS Main Command

WORKSPACE="${LIFEOS_WORKSPACE:-$HOME/.openclaw/workspace}"

case "${1:-help}" in
  status|health)
    echo "🦾 Life OS Status"
    echo "Workspace: $WORKSPACE"
    echo "Agents: $(find "$WORKSPACE/agents" -type d 2>/dev/null | wc -l)"
    echo "Disk: $(df -h "$WORKSPACE" 2>/dev/null | tail -1 | awk '{print $5}')"
    free -h 2>/dev/null | grep Mem | awk '{print "Memory: "$3"/"$2}'
    ;;
  agents)
    echo "🤖 Agents"
    ls "$WORKSPACE/agents" 2>/dev/null || echo "No agents yet"
    ;;
  help|*)
    echo "Life OS CLI"
    echo "Usage: lifeos <command>"
    echo ""
    echo "Commands:"
    echo "  status     Show system status"
    echo "  agents     List agents"
    echo "  help       Show this help"
    ;;
esac
EOF

chmod +x "$BIN_DIR/lifeos"

# Add to PATH
if ! grep -q "$BIN_DIR" "$HOME/.bashrc" 2>/dev/null; then
    echo "export PATH=\"$BIN_DIR:\$PATH\"" >> "$HOME/.bashrc"
    echo "✅ Added to PATH in ~/.bashrc"
fi

echo ""
echo "✅ Installation complete!"
echo ""
echo "Usage:"
echo "  lifeos status    - Show system status"
echo "  lifeos agents    - List agents"
echo ""
echo "Run 'source ~/.bashrc' or restart shell to use 'lifeos' command"
