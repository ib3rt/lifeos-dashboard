#!/bin/bash
# Discord Bot Runner
# Starts the Life OS Discord bot

cd ~/.openclaw/workspace/bots/discord

# Check if discord.py is installed
if ! python3 -c "import discord" 2>/dev/null; then
    echo "Installing discord.py..."
    pip3 install discord.py --user
fi

# Check for bot token
if [ -z "$DISCORD_BOT_TOKEN" ]; then
    if [ -f ~/.openclaw/discord/config.json ]; then
        export DISCORD_BOT_TOKEN=$(jq -r '.bot_token' ~/.openclaw/discord/config.json)
    fi
fi

if [ -z "$DISCORD_BOT_TOKEN" ] || [ "$DISCORD_BOT_TOKEN" = "null" ]; then
    echo "❌ DISCORD_BOT_TOKEN not set"
    echo ""
    echo "Set it with:"
    echo "  export DISCORD_BOT_TOKEN='your_token_here'"
    echo ""
    echo "Get token from: https://discord.com/developers/applications"
    exit 1
fi

echo "🎮 Starting Life OS Discord Bot..."
echo "=================================="
echo ""

# Run bot
python3 lifeos-bot.py