# OpenClaw CLI Toolkit

Your command center for managing OpenClaw and the Life OS. This toolkit provides
essential utilities for monitoring, managing agents, and maintaining system health.

## 📁 Files

| Script | Purpose |
|--------|---------|
| `openclaw-cli.sh` | Main entry point - gateway status, logs, agent list, memory search |
| `agent-manager.sh` | Agent lifecycle - create, deploy, and monitor agents |
| `system-health.sh` | Health monitoring - disk, memory, gateway, cron checks |

## 🚀 Quick Start

```bash
# Make scripts executable
chmod +x *.sh

# Check overall status
./openclaw-cli.sh status

# Create a new agent
./agent-manager.sh create MyAgent

# Run health check
./system-health.sh
```

---

## openclaw-cli.sh

Main entry point for OpenClaw management.

### Commands

| Command | Description | Example |
|---------|-------------|---------|
| `status` | Show gateway status, session count, errors | `./openclaw-cli.sh status` |
| `logs [n]` | Tail gateway logs (default 50 lines) | `./openclaw-cli.sh logs 100` |
| `restart` | Restart the gateway service | `./openclaw-cli.sh restart` |
| `agents` | List all agents with status | `./openclaw-cli.sh agents` |
| `memory search <q>` | Search MEMORY.md | `./openclaw-cli.sh memory search backup` |
| `session list` | Show recent sessions | `./openclaw-cli.sh session list` |

### Environment Variables

```bash
export OPENCLAW_WORKSPACE=/home/ubuntu/.openclaw/workspace
export OPENCLAW_LOG=/var/log/openclaw/gateway.log
```

---

## agent-manager.sh

Manage your agents throughout their lifecycle.

### Commands

| Command | Description | Example |
|---------|-------------|---------|
| `list` | Show all agents | `./agent-manager.sh list` |
| `create <name>` | Create new agent from template | `./agent-manager.sh create EmailAgent` |
| `deploy <name>` | Mark agent as deployed | `./agent-manager.sh deploy EmailAgent` |
| `status` | Check agent health | `./agent-manager.sh status` |

### Agent Structure

When you create an agent, you get:

```
agents/<name>/
├── README.md          # Agent documentation
├── .status            # Current status
├── src/
│   └── run.sh         # Execution script
├── output/            # Agent output files
└── memory/            # Agent-specific memories
```

### Agent Template

New agents come with a pre-filled README.md:

```markdown
# AgentName

## Purpose
<!-- What this agent does -->

## Responsibilities
- Task 1
- Task 2

## Schedule
When does this agent run?

## Status
IDLE
```

---

## system-health.sh

Monitor your OpenClaw infrastructure.

### Usage

```bash
./system-health.sh              # Full health check
./system-health.sh --quick      # Quick check
./system-health.sh --watch      # Continuous monitoring (30s)
```

### Checks Performed

| Check | Details |
|-------|---------|
| **Disk Usage** | Filesystem utilization, workspace size |
| **Memory** | RAM, swap, top consumers |
| **Gateway** | Process status, port 18789, uptime |
| **Cron** | Scheduled jobs, last execution |
| **Network** | Connectivity, load average |

### Thresholds

- Disk: 80% warning, 90% critical
- Memory: 80% warning, 95% critical

---

## 🎨 Output Colors

| Color | Meaning |
|-------|---------|
| 🟢 Green | OK / Success |
| 🟡 Yellow | Warning / Idle |
| 🔴 Red | Error / Critical |
| 🔵 Blue | Info |
| 🟣 Magenta | Headers |

---

## 📝 Agent Roster Integration

These tools reference `AGENTS_ROSTER_V2.md` when creating new agents. The roster
defines personality archetypes and roles that help guide agent creation.

Example archetypes:
- **The Archivist** - Memory and record keeping
- **The Scout** - Research and discovery
- **The Gatekeeper** - Security and access control

---

## 🔧 Tips

### Add to PATH

Add this to your `~/.bashrc`:

```bash
export PATH="$HOME/.openclaw/workspace/tools:$PATH"
alias openclaw-cli="openclaw-cli.sh"
alias agent-mgr="agent-manager.sh"
alias health="system-health.sh"
```

### Tab Completion

Basic tab completion:

```bash
# Add to ~/.bashrc
complete -W "status logs restart agents memory session" openclaw-cli.sh
complete -W "list create deploy status" agent-manager.sh
complete -W "--quick --watch --help" system-health.sh
```

### Cron Integration

Run health checks and save to log:

```bash
# Add to crontab
*/30 * * * * /home/ubuntu/.openclaw/workspace/tools/system-health.sh --quick >> /var/log/openclaw/health.log 2>&1
```

---

## 🆘 Troubleshooting

### Gateway not found

```bash
# Check if openclaw is installed
which openclaw

# Check PATH
echo $PATH
```

### Permission denied

```bash
# Make executable
chmod +x *.sh

# Or run with bash
bash openclaw-cli.sh status
```

### Log file not found

```bash
# Set custom log location
export OPENCLAW_LOG=/path/to/your/gateway.log
```

---

## 📄 License

Part of the OpenClaw Life OS. Use freely, modify as needed.

---

*Built for the Life OS by Neural Net Ned* 🤖🔧
