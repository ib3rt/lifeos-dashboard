# TOOLS.md - Environment-Specific Notes

*Your infrastructure, nicknames, preferences. My cheat sheet for your setup.*

---

## Compute

**Primary Host:** ip-172-31-24-50 (AWS)  
**OpenClaw Workspace:** `/home/ubuntu/.openclaw/workspace`  
**Gateway:** localhost:18789 (loopback)  
**OS:** Linux 6.14.0-1018-aws

---

## Model Configuration

**Primary:** moonshot/kimi-k2.5  
**Fallback:** moonshot/kimi-k2-0905-preview  
**Image Model:** (default from config)

**Cost Reference:**
- Kimi K2.5: Check current pricing
- Local embeddings: Free (if configured)

---

## Channels

| Channel | Status | Notes |
|---------|--------|-------|
| Telegram | ✅ Active | @iB3rtz, id: 6307161005 |
| WhatsApp | ❌ Not configured | Available via plugin |
| Discord | ❌ Not configured | Available via plugin |
| Signal | ❌ Not configured | Available via plugin |

---

## External Services

| Service | Status | API Key | Notes |
|---------|--------|---------|-------|
| Moonshot | ✅ Active | Configured | Primary LLM |
| Brave Search | ❌ Missing | Needed | Web search |
| Anthropic | ⚠️ Profile exists | Check | Backup option |

---

## File Locations

```
~/.openclaw/
├── openclaw.json          # Main config
├── workspace/             # Your working directory
│   ├── AGENTS.md          # This workspace docs
│   ├── SOUL.md            # My operating model
│   ├── USER.md            # Your profile
│   ├── IDENTITY.md        # Who I am
│   ├── MEMORY.md          # Curated knowledge
│   ├── HEARTBEAT.md       # Checklist
│   ├── Braindump.md       # Your scratchpad
│   ├── Expectations.md    # Our contract
│   ├── TOOLS.md           # This file
│   └── memory/            # Daily logs + preferences
│       ├── b3rt-preferences.md
│       └── YYYY-MM-DD.md
```

---

## Naming Conventions

*Your preferences for how I refer to things.*

- You: **b3rt**
- Me: **Claw** 🦾
- System: **Life OS** / **OpenClaw**

---

## TTS Preferences

*If/when voice is configured.*

- Preferred voice: (not set)
- Default speaker: (not set)
- Auto-TTS: Disabled

---

## Quick Commands

```bash
# Check OpenClaw status
openclaw status

# View config
openclaw config

# Restart gateway
openclaw gateway restart

# Add Brave API key
openclaw configure --section web
```

---

*Add hardware details, SSH aliases, camera names, etc. as needed.*
