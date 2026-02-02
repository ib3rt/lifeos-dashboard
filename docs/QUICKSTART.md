# Quickstart Guide

*Get up and running with Life OS in 5 minutes*

---

## Welcome, b3rt

This is your Life OS — an AI-native personal operating system. Here's everything you need to know to start using it effectively.

---

## First Things First

### How to Reach Claw

**Primary:** Telegram (`@iB3rtz`)
- Send messages anytime
- Use voice messages for quick notes
- Get notifications on important updates

**Web Interface:** Direct workspace access
- Full file system access
- Better for complex tasks
- Synchronous conversations

---

## Core Concepts

### 1. The Golden Rule: **Act, Don't Ask**

Claw is designed to handle things without constant back-and-forth:
- ✅ Research topics and summarize findings
- ✅ Organize files and update documentation
- ✅ Monitor systems and report issues
- ✅ Execute routine tasks automatically

**Claw will ask when it matters:**
- Cost >$0.50 for an operation
- Sending external messages/emails
- Financial transactions
- Deleting or overwriting important files

### 2. Memory Persistence

Life OS remembers everything:
- **Daily logs:** Every conversation saved to `memory/YYYY-MM-DD.md`
- **Long-term memory:** Important context in `MEMORY.md`
- **Your preferences:** Personal settings tracked over time

**You never need to repeat context.** Just reference previous work or pick up where you left off.

### 3. Agent Specialization

For complex tasks, Claw spawns specialist agents:
- 💰 Finance questions → Finance Director
- 💻 Code/automation → IT Specialist
- ✈️ Travel planning → Travel Planner

You can request a specific agent or let Claw route automatically.

---

## Essential Commands

### Model Control
```
/use local     # Force local model (Qwen3, faster, free)
/use cloud     # Force cloud model (Kimi, smarter, metered)
/use auto      # Return to automatic routing (default)
```

### Help & Status
```
/status        # System status and current settings
/help          # Available commands
```

---

## Everyday Usage Patterns

### Ask Anything
Just message Claw naturally. Examples:
- "Summarize my calendar for this week"
- "Research the best password managers"
- "Check the disk space on my server"
- "Draft an email to cancel my subscription"

### Request Specific Actions
Be direct and specific:
- ❌ "Can you help with a file?"
- ✅ "Read `/var/log/nginx/error.log` and find 5xx errors"

### Follow-up Naturally
Reference previous work:
- "Based on that analysis, create a summary"
- "Expand on point #3 from earlier"
- "Save this to `memory/project-ideas.md`"

---

## Common Tasks

### File Management
```
"List files in the agents directory"
"Read my SOUL.md file"
"Create a new file at notes/meeting-2026-02-02.md"
"Edit line 15 of config.json to change the port"
```

### Web Research
```
"Search for latest developments in home battery storage"
"Fetch and summarize https://example.com/article"
"Take a screenshot of https://my-site.com"
```

### System Operations
```
"Check git status in the workspace"
"Run npm install in the project directory"
"Show me the last 50 lines of syslog"
```

### Communication
```
"Send me a Telegram message when this task completes"
"Draft a reply to that email about the contract"
"Notify me if any disk exceeds 90% usage"
```

---

## Pro Tips

### 1. Batch Related Requests
Instead of:
```
"Search for X"
(wait)
"Now search for Y"
(wait)
"Compare them"
```

Say:
```
"Research X and Y, then compare them in a table"
```

### 2. Specify Output Format
```
"Give me this as a markdown list"
"Save the results to analysis/q4-report.md"
"Show me a table with columns: Date, Event, Priority"
```

### 3. Set Constraints
```
"Keep this under $0.25 in API costs"
"Don't spend more than 2 minutes on this"
"Only use local model for this task"
```

### 4. Reference Files Directly
```
"Apply the formatting from memory/b3rt-preferences.md"
"Check what we decided in yesterday's log"
"Update the section about X in MEMORY.md"
```

---

## Understanding Responses

### Silent Operation
Claw often works silently in the background. You'll get:
- **Concise confirmations** when tasks complete
- **Relevant outputs** only (no fluff)
- **HEARTBEAT_OK** during periodic checks when nothing needs attention

### Escalation Patterns
Claw will explicitly ask when:
- Cost exceeds your comfort threshold
- Multiple valid options exist
- External impact is involved (sending messages, posting publicly)
- Security implications arise

---

## Your Configuration

### Personal Preferences (Tracked)
Review or update at `memory/b3rt-preferences.md`:
- Communication style preferences
- Default model choices
- Notification settings
- Cost thresholds

### Workspace Files
Key files you might want to customize:
- `SOUL.md` — Claw's operating model
- `HEARTBEAT.md` — Automation checklist
- `EXPECTATIONS.md` — Our working agreement

---

## Getting Help

### Within Life OS
```
"Show me available tools and what they do"
"What agents are available for legal questions?"
"Explain how the memory system works"
```

### Documentation
- [`SYSTEM_OVERVIEW.md`](./SYSTEM_OVERVIEW.md) — Full architecture
- [`AGENT_CAPABILITIES.md`](./AGENT_CAPABILITIES.md) — Tool reference with examples

---

## Quick Checklist

- [ ] You can message Claw on Telegram
- [ ] You understand Claw acts autonomously by default
- [ ] You know Claw remembers context between sessions
- [ ] You've reviewed `memory/b3rt-preferences.md`
- [ ] You know how to force local vs cloud models
- [ ] You know where to find this documentation

---

## What's Next?

**Start using it.** The best way to learn Life OS is to use it:

1. Send a simple request: "What's the weather today?"
2. Try a file operation: "List the contents of the memory directory"
3. Do some research: "Find me the best practices for X"
4. Get ambitious: "Create a project plan for Y"

Claw learns your patterns over time. The more you use it, the better it gets at anticipating what you need.

---

*Welcome to Life OS. Let's build something useful.* 🦾
