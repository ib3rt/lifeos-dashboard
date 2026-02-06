#!/bin/bash
# Discord Server Setup Automation
# Run this after creating the server

echo "🎮 Discord Server Setup"
echo "======================="
echo ""

# Check if server ID is provided
if [ -z "$1" ]; then
    echo "Usage: ./setup-discord.sh <SERVER_ID> <BOT_TOKEN>"
    echo ""
    echo "To get Server ID:"
    echo "  1. Discord → Server Settings → Widget"
    echo "  2. Copy Server ID"
    echo ""
    echo "To get Bot Token:"
    echo "  1. https://discord.com/developers/applications"
    echo "  2. New Application → Bot → Copy Token"
    exit 1
fi

SERVER_ID=$1
BOT_TOKEN=$2

echo "Server ID: $SERVER_ID"
echo "Bot Token: ${BOT_TOKEN:0:10}..."
echo ""

# Create channel structure via API (requires bot with manage_channels permission)
# Note: This is a template - actual API calls require proper bot setup

echo "📋 Channel Structure Plan:"
echo ""
echo "📋 INFORMATION"
echo "  #welcome"
echo "  #announcements"
echo "  #changelog"
echo ""
echo "🤖 AGENT HQ"
echo "  #agent-chat"
echo "  #oracle-insights (🔮)"
echo "  #diamond-hands (💎)"
echo "  #mechanic-workshop (⚙️)"
echo "  #sentinel-alerts (🛡️)"
echo ""
echo "💬 GENERAL"
echo "  #general"
echo "  #showcase"
echo "  #feedback"
echo ""
echo "🔧 DEVELOPMENT"
echo "  #github-updates"
echo "  #deployment"
echo "  #debug"
echo ""
echo "🎯 PROJECTS"
echo "  #local-node"
echo "  #x-automation"
echo "  #voice-cloning"
echo ""

echo "🔌 Webhook URLs to configure:"
echo "  GitHub:  https://your-server.com/webhook/discord/github"
echo "  Vercel:  https://your-server.com/webhook/discord/vercel"
echo "  n8n:     https://your-server.com/webhook/discord/n8n"
echo ""

echo "📁 Configuration saved to:"
echo "  ~/.openclaw/discord/config.json"

# Save config
mkdir -p ~/.openclaw/discord
cat > ~/.openclaw/discord/config.json << EOF
{
  "server_id": "$SERVER_ID",
  "bot_token": "$BOT_TOKEN",
  "webhooks": {
    "github": "https://your-server.com/webhook/discord/github",
    "vercel": "https://your-server.com/webhook/discord/vercel",
    "n8n": "https://your-server.com/webhook/discord/n8n"
  },
  "channels": {
    "welcome": "welcome",
    "announcements": "announcements",
    "agent_chat": "agent-chat",
    "github_updates": "github-updates",
    "deployment": "deployment",
    "oracle_insights": "oracle-insights"
  }
}
EOF

echo ""
echo "✅ Configuration saved!"
echo ""
echo "Next steps:"
echo "  1. Invite bot to server:"
echo "     https://discord.com/oauth2/authorize?client_id=YOUR_CLIENT_ID&scope=bot&permissions=8"
echo ""
echo "  2. Run channel creator:"
echo "     ./create-channels.sh"
echo ""
echo "  3. Configure webhooks in GitHub/Vercel"
