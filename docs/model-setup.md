# Model Setup Instructions

## Haiku (Claude 3) - For Heartbeat

### API Access (Recommended)
**Provider:** Anthropic
**Website:** https://www.anthropic.com

**Steps:**
1. Sign up at https://console.anthropic.com
2. Get API key from dashboard
3. Add to environment: `export ANTHROPIC_API_KEY=your_key`
4. Test: `curl https://api.anthropic.com/v1/messages -H "x-api-key: $ANTHROPIC_API_KEY" ...`

**Pricing:** 
- Input: $0.25 / 1M tokens
- Output: $1.25 / 1M tokens

### Local Setup (Experimental)
**Note:** Claude models are NOT open-source. Cannot be downloaded locally.
**Alternative:** Use Ollama with smaller open models
```bash
# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Run lightweight model for heartbeat
ollama run llama3.2:1b
```

---

## MiniMax 2.5 - For Coding

### API Access (Recommended)
**Provider:** MiniMax
**Website:** https://www.minimaxi.com

**Steps:**
1. Sign up at https://www.minimaxi.com/en
2. Create API key in developer console
3. Add to environment: `export MINIMAX_API_KEY=your_key`
4. Test API call

**API Endpoint:**
```bash
curl https://api.minimaxi.chat/v1/text/chatcompletion_v2 \
  -H "Authorization: Bearer $MINIMAX_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "MiniMax-Text-01",
    "messages": [{"role": "user", "content": "Hello"}]
  }'
```

**Pricing:**
- Check https://www.minimaxi.com/en/pricing for current rates

### Local Setup
**Note:** MiniMax models are NOT open-source. API-only access.

---

---

## 🔍 DeepSeek V3 - For Web Search

### API Access (Recommended)
**Provider:** DeepSeek
**Website:** https://platform.deepseek.com

**Steps:**
1. Sign up at https://platform.deepseek.com
2. Create API key in developer settings
3. Add to environment: `export DEEPSEEK_API_KEY=your_key`
4. Test API call

**API Endpoint:**
```bash
curl https://api.deepseek.com/v1/chat/completions \
  -H "Authorization: Bearer $DEEPSEEK_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "deepseek-v3",
    "messages": [{"role": "user", "content": "Search for..."}]
  }'
```

**Pricing:**
- Input: $0.27 / 1M tokens
- Output: $1.10 / 1M tokens
- Very cost-effective for search tasks

### Local Setup
**Note:** DeepSeek V3 is NOT open-source. API-only access.

---

## 🎙️ ChatGPT 4.0 - For Voice / Audio

### API Access (Recommended)
**Provider:** OpenAI
**Website:** https://platform.openai.com

**Steps:**
1. Sign up at https://platform.openai.com
2. Get API key from API keys section
3. Add to environment: `export OPENAI_API_KEY=your_key`
4. Test API call

**API Endpoint:**
```bash
curl https://api.openai.com/v1/chat/completions \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-4",
    "messages": [{"role": "user", "content": "Write a podcast script"}]
  }'
```

**Pricing:**
- GPT-4: $30 / 1M input tokens, $60 / 1M output tokens
- Check https://openai.com/pricing for current rates

### For Voice (Text-to-Speech)
```bash
curl https://api.openai.com/v1/audio/speech \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "tts-1",
    "input": "Hello from Life OS",
    "voice": "alloy"
  }' \
  --output speech.mp3
```

### Local Setup
**Note:** ChatGPT models are NOT open-source. API-only access.

---

## 🤔 Gemini 2.5 Flash - For Understanding

### API Access (Recommended)
**Provider:** Google AI Studio
**Website:** https://aistudio.google.com

**Steps:**
1. Sign up at https://aistudio.google.com
2. Get API key from settings
3. Add to environment: `export GEMINI_API_KEY=your_key`
4. Test API call

**API Endpoint:**
```bash
curl "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key=$GEMINI_API_KEY" \
  -H 'Content-Type: application/json' \
  -X POST \
  -d '{
    "contents": [{"parts":[{"text": "Explain this document..."}]}]
  }'
```

**Pricing:**
- Free tier: 15 requests/minute
- Paid tier: Check https://ai.google.dev/pricing

---

## Alternative: Local Models

### For Heartbeat (Lightweight)
```bash
# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Download tiny model for status checks
ollama pull llama3.2:1b        # 1.3GB - very fast
ollama pull qwen2.5:0.5b       # 400MB - ultra lightweight
ollama pull phi3:mini          # 2GB - good balance

# Run
ollama run llama3.2:1b
```

### For Coding (Local)
```bash
# Code-optimized models
ollama pull codellama:7b       # 3.8GB - code generation
ollama pull qwen2.5-coder:7b   # 4.4GB - coding tasks
ollama pull deepseek-coder:6.7b # 3.8GB - code completion

# Run
ollama run codellama:7b
```

---

## Environment Setup

Add to `~/.bashrc` or `~/.zshrc`:
```bash
# API Keys
export ANTHROPIC_API_KEY="your_anthropic_key"
export MINIMAX_API_KEY="your_minimax_key"
export MOONSHOT_API_KEY="your_moonshot_key"
export DEEPSEEK_API_KEY="your_deepseek_key"
export GEMINI_API_KEY="your_gemini_key"

# Model Routing
export BRAIN_MODEL="moonshot/kimi-k2.5"              # Life OS Brain
export HEARTBEAT_MODEL="anthropic/claude-3-haiku"     # Status checks
export CODING_MODEL="minimax/minimax-2.5"             # Code generation
export SEARCH_MODEL="deepseek/deepseek-v3"            # Web search
export CONTENT_MODEL="moonshot/kimi-k2.5"             # Content creation
export VOICE_MODEL="openai/gpt-4"                     # Voice / Audio
export UNDERSTANDING_MODEL="google/gemini-2.5-flash"  # Comprehension
```

---

## Quick Test

```bash
# Test Haiku (Heartbeat)
curl https://api.anthropic.com/v1/messages \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "content-type: application/json" \
  -d '{
    "model": "claude-3-haiku-20240307",
    "max_tokens": 100,
    "messages": [{"role": "user", "content": "Status check"}]
  }'

# Test MiniMax (Coding)
curl https://api.minimaxi.chat/v1/text/chatcompletion_v2 \
  -H "Authorization: Bearer $MINIMAX_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "MiniMax-Text-01",
    "messages": [{"role": "user", "content": "Write a bash script"}]
  }'
```

---

*Setup Guide v1.0 | Life OS*
