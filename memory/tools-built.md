# CLI Toolkit — Built 2026-02-02

Four production-ready shell scripts for Life OS operations.

## Tools

| Tool | Purpose | Usage |
|------|---------|-------|
| `logday` | Daily log creator | `logday "Started new project"` |
| `taskprio` | Eisenhower Matrix tasks | `taskprio add "Task" -i -u` |
| `healthchk` | System health | `healthchk` |
| `quicknote` | Fast notes | `quicknote "Idea here"` |

## Installation

Already in `workspace/tools/`. Add to PATH:
```bash
export PATH="$HOME/.openclaw/workspace/tools:$PATH"
```

## Details

### logday
- Creates `memory/YYYY-MM-DD.md` entries
- Categories via `-c work`
- List recent: `logday -l`

### taskprio
- Quadrants: Q1 (do first), Q2 (schedule), Q3 (delegate), Q4 (eliminate)
- Flags: `-i` (important), `-u` (urgent)
- JSON storage in `workspace/tasks.json`

### healthchk
- Disk, memory, load, service checks
- Thresholds: WARN at 80%, CRIT at 90%

### quicknote
- Appends to `memory/inbox.md`
- Timestamped entries
- View all: `quicknote` (no args)

## Status
✅ All tools written, executable, tested
