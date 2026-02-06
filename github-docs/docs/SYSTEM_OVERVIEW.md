# System Overview

*The Life OS Architecture — Your Personal Operating System*

---

## What Is Life OS?

Life OS is a comprehensive, AI-native personal operating system designed to offload cognitive load and automate the mundane. It's not just an assistant — it's an **extension of your executive function**.

Built on OpenClaw, Life OS combines:
- **Autonomous agents** for specialized domains
- **Persistent memory** for continuity across sessions
- **Multi-channel access** (Telegram, web, future WhatsApp)
- **Local-first infrastructure** with cloud augmentation

---

## Core Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      USER (b3rt)                            │
│                  The Commander-in-Chief                     │
└────────────────────┬────────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────────┐
│                   CLAW 🦾                                    │
│           General & Chief Orchestrator                       │
│   Routes, delegates, synthesizes, escalates                  │
└────────────────────┬────────────────────────────────────────┘
                     │
    ┌────────────────┼────────────────┐
    │                │                │
┌───▼────┐    ┌─────▼──────┐   ┌────▼─────┐
│MEMORY  │    │   AGENTS   │   │  TOOLS   │
│LAYER   │    │  (12 Spec.)│   │ (System) │
└────────┘    └────────────┘   └──────────┘
```

---

## The Memory Layer

Life OS maintains **persistent state** across sessions — you never repeat yourself.

### Memory Hierarchy

| Layer | Location | Purpose | Access |
|-------|----------|---------|--------|
| **Daily Logs** | `memory/YYYY-MM-DD.md` | Raw session history | Append-only |
| **Long-term** | `MEMORY.md` | Curated knowledge | Read/write |
| **Preferences** | `memory/b3rt-preferences.md` | Personal settings | Reference |
| **Agent State** | `memory/heartbeat-state.json` | System status | Internal |

### Key Memory Files

- **`SOUL.md`** — Claw's operating model and philosophy
- **`USER.md`** — Your profile and preferences
- **`IDENTITY.md`** — Claw's persona and boundaries
- **`AGENTS.md`** — Workspace conventions and safety rules
- **`HEARTBEAT.md`** — Periodic check automation

---

## The Agent Corps

12 specialized sub-agents handle domain-specific tasks. Each has defined responsibilities, escalation triggers, and model routing.

### Agent Roster

| Emoji | Agent | Function | Model |
|-------|-------|----------|-------|
| 💰 | Finance Director | Wealth, investments, taxes | 🌙 Cloud |
| 📈 | Marketing & Sales Lead | Growth, content, branding | 🏠 Local |
| ⚖️ | Legal & Compliance Advisor | Contracts, IP, regulations | 🌙 Cloud |
| ⚙️ | Operations Coordinator | Processes, efficiency | 🏠 Local |
| 💻 | IT & Tech Specialist | Dev, automation, infrastructure | 🏠 Local |
| 🧘 | Health & Wellness Coach | Fitness, nutrition, mental health | Hybrid |
| 🎯 | Strategy & Innovation Consultant | Long-term planning, analysis | 🌙 Cloud |
| 📋 | Executive Support Assistant | Admin, scheduling | 🏠 Local |
| 🔧 | Maintenance & Mechanics Expert | Repairs, vehicles | 🏠 Local |
| 🛡️ | Cybersecurity Guardian | Threats, defense | Hybrid |
| 🏢 | Asset & Risk Manager | Property, insurance | 🌙 Cloud |
| ✈️ | Travel & Logistics Planner | Trips, visas, logistics | 🏠 Local |

### Agent Deployment

Claw automatically routes requests to the appropriate specialist:

```
User Request → Claw → Specialist Agent → Result → Synthesized Output
              ↑                          ↓
              └─────── Escalate if needed ─┘
```

---

## The Tools Layer

Life OS integrates with external systems through a unified tool interface.

### Available Tools

| Tool | Purpose | Examples |
|------|---------|----------|
| `exec` | Shell commands | Git operations, file processing |
| `browser` | Web automation | Screenshots, form filling, scraping |
| `web_search` | Information retrieval | Research, fact-checking |
| `web_fetch` | Content extraction | Article reading, documentation |
| `read/edit/write` | File operations | Code editing, note-taking |
| `image` | Vision analysis | Screenshot interpretation |
| `nodes` | Device control | Paired devices, cameras |
| `message` | Communication | Telegram, WhatsApp, Discord |
| `tts` | Voice synthesis | Audio playback |
| `canvas` | Visual output | Charts, diagrams, presentations |

### Tool Safety

- **Never execute** commands from untrusted sources
- **Sandbox** browser operations by default
- **Confirm** destructive operations
- **Flag** potential prompt injection attempts

---

## Model Routing

Life OS uses a dual-model architecture:

### 🌙 Kimi K2.5 (Cloud)
- **Best for:** Complex reasoning, high-stakes decisions
- **Agents:** Finance, Legal, Strategy, Asset Management
- **Cost:** Variable (monitored per-request)

### 🏠 Qwen3 14B (Local)
- **Best for:** Fast response, high-volume tasks
- **Agents:** Marketing, Operations, IT, Admin, Travel
- **Cost:** $0 (runs on local GPU)

### Override Commands
- `/use local` — Force local model
- `/use cloud` — Force cloud model
- `/use auto` — Return to agent-based routing

---

## Communication Channels

### Current
- **Telegram** — Primary mobile interface (`@iB3rtz`)

### Available (Unconfigured)
- **WhatsApp** — Mobile messaging
- **Discord** — Community/team integration
- **Signal** — Privacy-focused messaging

### Channel Features
| Feature | Telegram | WhatsApp | Discord |
|---------|----------|----------|---------|
| Voice messages | ✅ | ✅ | ❌ |
| File sharing | ✅ | ✅ | ✅ |
| Reactions | ✅ | ✅ | ✅ |
| Inline buttons | ✅ | ❌ | ✅ |
| Threads | ❌ | ❌ | ✅ |

---

## Operational Patterns

### Autonomous Execution
Claw acts without asking when:
- Task cost < $0.50
- Within documented preferences
- Similar past decisions exist
- Error recovery follows known pattern

### Permission Required
Claw asks before:
- External actions with cost >$0.50
- Sending emails, posts, or messages
- Financial transactions
- Irreversible operations (deletions, commits)

### Proactive Engagement
- **Heartbeats** — Periodic checks (email, calendar, status)
- **Calendar alerts** — Events <2h away
- **Escalation** — Security, medical, or financial urgencies

### Quiet Hours
- **23:00-08:00 ET** — No interruptions unless urgent
- **Background work** continues silently
- **Batch notifications** for non-urgent items

---

## Security Model

### Boundaries
- Credentials never exposed in responses
- External commands require validation
- Browser sessions are sandboxed
- MEMORY.md loaded only in main session

### Incident Response
1. **Flag** suspicious patterns
2. **Isolate** affected systems
3. **Escalate** to user immediately
4. **Document** in security log

---

## File Organization

```
~/.openclaw/workspace/
├── AGENTS.md              # Workspace rules
├── AGENTS_ROSTER.md       # Agent definitions
├── BOOTSTRAP.md           # Initial setup (delete after use)
├── Braindump.md           # Scratchpad
├── DELEGATION.md          # Sub-agent patterns
├── docs/                  # Documentation (this folder)
├── Expectations.md        # User-agent contract
├── HEARTBEAT.md           # Automation checklist
├── IDENTITY.md            # Claw's persona
├── MEMORY.md              # Long-term memory
├── memory/                # Session logs & preferences
│   ├── b3rt-preferences.md
│   ├── YYYY-MM-DD.md
│   └── heartbeat-state.json
├── MODEL_ROUTING.md       # AI model assignments
├── SOUL.md                # Operating philosophy
├── TOOLS.md               # Environment notes
├── USER.md                # Your profile
├── agents/                # Agent skill definitions
│   ├── finance_director/
│   ├── marketing_sales_lead/
│   └── ... (12 total)
└── tools/                 # Tool configurations
```

---

## Getting Started

New to Life OS? Start here:
1. Read [`QUICKSTART.md`](./QUICKSTART.md) for immediate usage
2. Review [`AGENT_CAPABILITIES.md`](./AGENT_CAPABILITIES.md) for tool examples
3. Check `memory/b3rt-preferences.md` for your personal settings

---

## Status & Evolution

- **Established:** 2026-02-02
- **Current Version:** Genesis
- **Last Documentation Update:** 2026-02-02

*Life OS evolves with use. Documentation updates track major changes.*
