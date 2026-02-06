#!/bin/bash
# Automated Discord Bot Deployment
# Run this after setting DISCORD_BOT_TOKEN

TOKEN=$1

if [ -z "$TOKEN" ]; then
    echo "Usage: ./deploy-bot.sh <DISCORD_BOT_TOKEN>"
    exit 1
fi

echo "🤖 Deploying Life OS Discord Bot..."
echo "===================================="
echo ""

# Save token
mkdir -p ~/.openclaw/discord
echo "$TOKEN" > ~/.openclaw/discord/bot.token
chmod 600 ~/.openclaw/discord/bot.token

echo "✅ Token saved securely"
echo ""

# Install dependencies
echo "📦 Installing dependencies..."
pip3 install discord.py --user -q
echo "  ✅ discord.py installed"
echo ""

# Configure bot
echo "⚙️ Configuring bot..."
export DISCORD_BOT_TOKEN="$TOKEN"

cat > ~/.openclaw/discord/config.json << EOF
{
  "bot_token": "$TOKEN",
  "command_prefix": "!",
  "server_id": "Life OS Command Center",
  "webhooks": {
    "github": "https://$(curl -s ipinfo.io/ip)/webhook/github",
    "vercel": "https://$(curl -s ipinfo.io/ip)/webhook/vercel",
    "n8n": "https://$(curl -s ipinfo.io/ip)/webhook/n8n"
  }
}
EOF

echo "  ✅ Configuration saved"
echo ""

# Test bot connection
echo "🧪 Testing bot connection..."
python3 << 'PYEOF'
import discord
import os
import sys

token = open(os.path.expanduser('~/.openclaw/discord/bot.token')).read().strip()

class TestBot(discord.Client):
    async def on_ready(self):
        print(f"  ✅ Bot authenticated: {self.user}")
        print(f"  ✅ Latency: {round(self.latency * 1000)}ms")
        await self.close()

intents = discord.Intents.default()
intents.message_content = True

client = TestBot(intents=intents)
try:
    client.run(token)
except Exception as e:
    print(f"  ❌ Error: {e}")
    sys.exit(1)
PYEOF

if [ $? -ne 0 ]; then
    echo ""
    echo "❌ Bot test failed. Check your token."
    exit 1
fi

echo ""
echo "🚀 Starting bot in background..."

# Create systemd service or use nohup
nohup python3 ~/workspace/bots/discord/lifeos-bot.py > ~/.openclaw/discord/bot.log 2>&1 &
BOT_PID=$!
echo $BOT_PID > ~/.openclaw/discord/bot.pid

echo "  ✅ Bot started (PID: $BOT_PID)"
echo ""

# Wait and verify
sleep 3
if ps -p $BOT_PID > /dev/null; then
    echo "✅ Bot is running!"
else
    echo "⚠️  Bot may have stopped. Check logs:"
    echo "   tail ~/.openclaw/discord/bot.log"
fi

echo ""
echo "===================================="
echo "🎉 Discord Bot Deployed!"
echo ""
echo "Commands available:"
echo "  !status     - Show Life OS status"
echo "  !agents     - List all agents"
echo "  !report     - Get research reports"
echo "  !deploy     - Trigger deployments"
echo "  !help       - Show all commands"
echo ""
echo "Try it: Go to Discord and type !status"
echo ""
echo "Logs: tail -f ~/.openclaw/discord/bot.log"
echo "Stop: kill $(cat ~/.openclaw/discord/bot.pid)"
echo "===================================="
