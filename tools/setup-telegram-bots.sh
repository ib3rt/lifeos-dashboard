#!/bin/bash
# Life OS Multi-Bot Telegram Setup Script
# Run this on your server after creating bots

echo "🤖 Life OS Multi-Bot Telegram Setup"
echo "===================================="
echo ""

# Check if tokens file exists
if [ ! -f "bot-tokens.txt" ]; then
    echo "❌ bot-tokens.txt not found!"
    echo ""
    echo "Create this file with format:"
    echo "ORACLE=123456:ABC..."
    echo "DIAMOND=123456:DEF..."
    echo "MECHANIC=123456:GHI..."
    echo "etc"
    exit 1
fi

echo "Step 1: Loading tokens..."
source bot-tokens.txt

echo "Step 2: Setting webhooks..."

# Set webhooks for each bot
set_webhook() {
    local token=$1
    local agent=$2
    local url="https://your-server.com/webhook/$agent"
    
    curl -s -X POST \
        "https://api.telegram.org/bot$token/setWebhook" \
        -d "url=$url" \
        -d "max_connections=40" \
        -d "allowed_updates=[\"message\", \"callback_query\"]"
}

set_webhook "$ORACLE" "oracle"
set_webhook "$DIAMOND" "diamond"
set_webhook "$MECHANIC" "mechanic"
set_webhook "$SENTINEL" "sentinel"
set_webhook "$LEGAL" "legal"
set_webhook "$HYPE" "hype"
set_webhook "$BRIDGE" "bridge"

echo "✅ Webhooks configured"
echo ""

# Test each bot
echo "Step 3: Testing bots..."

test_bot() {
    local token=$1
    local name=$2
    
    response=$(curl -s "https://api.telegram.org/bot$token/getMe")
    if echo "$response" | grep -q '"ok":true'; then
        username=$(echo "$response" | grep -o '"username":"[^"]*"' | cut -d'"' -f4)
        echo "  ✅ $name (@$username) - Online"
    else
        echo "  ❌ $name - Failed"
    fi
}

test_bot "$ORACLE" "Oracle"
test_bot "$DIAMOND" "Diamond Hands"
test_bot "$MECHANIC" "Mechanic"
test_bot "$SENTINEL" "Sentinel"
test_bot "$LEGAL" "Legal Eagle"
test_bot "$HYPE" "Hype Man"
test_bot "$BRIDGE" "The Bridge"

echo ""
echo "===================================="
echo "Setup complete!"
echo ""
echo "Next: Add all bots to your group"
echo "Then: Send a test message"
