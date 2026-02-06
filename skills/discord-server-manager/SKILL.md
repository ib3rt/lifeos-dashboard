# Discord Server Manager
## Deploy and manage Discord servers with bot integrations

---

## Overview

Automated Discord server setup with bot integrations, webhooks, and role management for Life OS Command Center.

---

## Capabilities

### Server Setup
- Create channel structure (5 categories, 15+ channels)
- Configure roles and permissions
- Deploy bot integrations
- Set up webhook endpoints

### Bot Integrations

**Life OS Bot**
- Commands: !status, !agents, !report, !deploy, !help
- Agent personas: Oracle, Diamond Hands, Mechanic, Sentinel
- Smart mention routing
- GitHub/Vercel webhook forwarding

**GitHub Bot**
- Repository updates
- PR notifications
- Issue tracking

**n8n Bot**
- Workflow notifications
- Alert routing

---

## Quick Setup

### 1. Create Server
- Name: "Life OS Command Center"
- Region: US East
- Icon: 🔮 or custom

### 2. Add Bot
```bash
# Set token
export DISCORD_BOT_TOKEN='your_token'

# Start bot
cd ~/workspace/bots/discord
./start-bot.sh
```

### 3. Configure Webhooks
- GitHub → #github-updates
- Vercel → #deployment
- n8n → #general

---

## Channel Structure

```
📋 INFORMATION
├── #welcome
├── #announcements
└── #changelog

🤖 AGENT HQ
├── #agent-chat
├── #oracle-insights
├── #diamond-hands
├── #mechanic-workshop
└── #sentinel-alerts

💬 GENERAL
├── #general
├── #showcase
└── #feedback

🔧 DEVELOPMENT
├── #github-updates
├── #deployment
└── #debug

🎯 PROJECTS
├── #local-node
├── #x-automation
└── #voice-cloning
```

---

## Commands

| Command | Description |
|---------|-------------|
| !status | Show Life OS status |
| !agents | List all agents |
| !report <name> | Get research report |
| !deploy | Trigger deployment |
| !help | Show help |
| @mention | Route to appropriate agent |

---

## Files

- `bots/discord/lifeos-bot.py` — Main bot code
- `bots/discord/start-bot.sh` — Bot runner
- `bots/webhook-bridge.py` — Webhook forwarding
- `agents/bridge_operator/discord-server-plan.md` — Full plan

---

## Current Server

**Invite:** https://discord.gg/Bpq2DRAG
**Status:** Bot deployment pending

---

## Integration

**n8n:** Workflow notifications → Discord
**GitHub:** Repo events → Discord
**Telegram:** Bidirectional sync
**Dashboard:** Discord status widget
