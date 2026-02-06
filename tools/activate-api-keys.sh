#!/bin/bash
# Activate all API keys

export ANTHROPIC_API_KEY=$(cat ~/.openclaw/keys/haiku.key 2>/dev/null)
export DEEPSEEK_API_KEY=$(cat ~/.openclaw/keys/deepseekv3.key 2>/dev/null)
export GEMINI_API_KEY=$(cat ~/.openclaw/keys/gemini25flash.key 2>/dev/null)

echo "✅ API Keys Activated:"
echo "  - Anthropic Haiku: ${ANTHROPIC_API_KEY:0:20}..."
echo "  - DeepSeek V3: ${DEEPSEEK_API_KEY:0:20}..."
echo "  - Gemini 2.0: ${GEMINI_API_KEY:0:20}..."
