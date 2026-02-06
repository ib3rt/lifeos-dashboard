# Brain Preferences — Model Routing Configuration

## Active Models (Working ✅)

### 🤖 Kimi 2.5 (Moonshot) — GENERALIST
**Model ID:** moonshot-kimi-k2.5  
**Status:** ✅ ACTIVE  
**Primary Use:** General reasoning, Content creation, Writing articles  
**Fallback Use:** Coding (if MiniMax unavailable)

### 💜 Haiku (Anthropic) — HEARTBEAT
**Model ID:** claude-3-haiku-20240307  
**Status:** ✅ ACTIVE  
**Use:** Heartbeat checks, Quick status tasks

### 🔍 DeepSeek V3 (DeepSeek) — SEARCH
**Model ID:** deepseek-chat  
**Status:** ✅ ACTIVE  
**Use:** Web search, Research, Information retrieval

### ⚡ Gemini 2.5 Flash (Google) — UNDERSTANDING
**Model ID:** gemini-2.5-flash  
**Status:** ✅ ACTIVE  
**Also Available:** gemini-2.5-flash-preview-tts (Voice/TTS)  
**Use:** Document understanding, Comprehension tasks, Voice generation

### 🚀 MiniMax-M2.1 (MiniMax) — PRIMARY CODING MODEL ⭐
**Model ID:** minimax-portal/MiniMax-M2.1  
**Status:** ✅ ACTIVE (via sub-agent)  
**Use:** Coding tasks ONLY  
**Access:** Sub-agent sessions (proven working!)  
**Evidence:** Mouse Macro Recorder built successfully in 2m12s  
**Fallback:** Kimi 2.5

### 🎉 X (Twitter) API — SOCIAL
**Status:** ✅ ACTIVE  
**Use:** Tweet automation, Social engagement

---

## Model Routing Rules

### ✅ Explicit Routing (Task → Model)

| Task Type | Primary Model | Fallback |
|-----------|---------------|----------|
| **Heartbeat** | Haiku ✅ | — |
| **Search/Research** | DeepSeek V3 ✅ | Kimi 2.5 |
| **Understanding** | Gemini 2.5 ✅ | Kimi 2.5 |
| **General/Brain** | Kimi 2.5 ✅ | — |
| **Content Writing** | Kimi 2.5 ✅ | — |
| **Coding** | **MiniMax-M2.1** ✅ | Kimi 2.5 ✅ |
| **Voice/TTS** | Gemini 2.5 TTS | Kimi 2.5 (scripts) |
| **Social/X** | Kimi 2.5 (compose) | — |

### 🚀 CODING MODEL DESIGNATION

**PRIMARY:** MiniMax-M2.1 (sub-agent)  
**FALLBACK:** Kimi 2.5 (direct)

**Evidence:** MiniMax-M2.1 successfully built Mouse Macro Recorder with 8 files in 2m12s.

---

## Cost Optimization

### Priority Order (Cheapest → Most Expensive)
1. **Haiku** — Heartbeat (cheapest)
2. **DeepSeek V3** — Search
3. **Gemini 2.5** — Understanding
4. **MiniMax-M2.1** — Coding (sub-agent model)
5. **Kimi 2.5** — General/Brain (most capable)

### Rule: Use cheapest model that can do the task

---

## Current Status: 5/7 Models Active

✅ Kimi 2.5 (General/Brain/Content)  
✅ Haiku (Heartbeat)  
✅ DeepSeek V3 (Search)  
✅ Gemini 2.5 (Understanding/TTS)  
✅ MiniMax-M2.1 (Coding) — PRIMARY!  
⏳ ChatGPT 4.0 (Voice - optional)  
✅ X API (Social)  

**All functions covered with fallbacks! 🎉**
