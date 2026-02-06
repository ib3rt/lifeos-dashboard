#!/bin/bash
# Haiku Heartbeat Test
# Tests the Anthropic Haiku model for heartbeat functionality

API_KEY=$(cat ~/.openclaw/keys/anthropic.key 2>/dev/null)

if [ -z "$API_KEY" ]; then
    echo "❌ No Anthropic API key found"
    exit 1
fi

echo "🧪 Testing Haiku for Heartbeat..."
echo ""

# Test heartbeat-style prompt
RESPONSE=$(curl -s https://api.anthropic.com/v1/messages \
  -H "Content-Type: application/json" \
  -H "x-api-key: $API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -d '{
    "model": "claude-3-haiku-20240307",
    "max_tokens": 50,
    "temperature": 0.3,
    "messages": [
      {"role": "user", "content": "Life OS status check: 30 agents active, 60+ tasks running, all systems nominal. Respond with a brief status confirmation suitable for a heartbeat message."}
    ]
  }')

# Check if response is valid
if echo "$RESPONSE" | grep -q "error"; then
    echo "❌ API Error:"
    echo "$RESPONSE" | head -1
    exit 1
fi

# Extract response text
TEXT=$(echo "$RESPONSE" | grep -o '"text":"[^"]*"' | head -1 | sed 's/"text":"//;s/"$//')

if [ -n "$TEXT" ]; then
    echo "✅ Haiku Response:"
    echo "   $TEXT"
    echo ""
    echo "✅ Haiku is working correctly for heartbeat tasks!"
else
    echo "⚠️ Could not parse response"
    echo "Raw response:"
    echo "$RESPONSE" | head -50
fi
