#!/bin/bash
# Test MiniMax API Key
# Tests whatever key is in ~/.openclaw/keys/minimax.new

KEY_FILE="${1:-~/.openclaw/keys/minimax.new}"

echo "🧪 Testing MiniMax API key from: $KEY_FILE"
echo ""

if [ ! -f "$KEY_FILE" ]; then
    echo "❌ Key file not found: $KEY_FILE"
    echo ""
    echo "To provide key securely:"
    echo "1. SSH into server"
    echo "2. nano ~/.openclaw/keys/minimax.new"
    echo "3. Paste key, save"
    echo "4. Run this script"
    exit 1
fi

export MINIMAX_API_KEY=$(cat "$KEY_FILE" 2>/dev/null)

if [ -z "$MINIMAX_API_KEY" ]; then
    echo "❌ Key file is empty"
    exit 1
fi

echo "Testing with platform.minimax.io API..."
echo ""

curl -s https://api.minimaxi.chat/v1/text/chatcompletion_v2 \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $MINIMAX_API_KEY" \
  -d '{
    "model": "MiniMax-Text-01",
    "messages": [
      {"role": "user", "content": "Write a Python hello world function"}
    ],
    "max_tokens": 100
  }' 2>&1 | head -50

echo ""
echo ""
echo "If you see a code response above, the key is working!"
