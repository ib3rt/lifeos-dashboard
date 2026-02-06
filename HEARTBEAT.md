<<<<<<< HEAD
# HEARTBEAT.md - Active Checks

*Checked every 30 minutes. Silent operation unless action needed.*

---

## Check Rotation

Rotate through these checks. Only 2-4 per cycle. Track state in `memory/heartbeat-state.json`.

### Daily Checks (1-2x)
- [ ] **Calendar** — Events in next 24-48h worth noting
- [ ] **Email** — Priority inbox, urgent items only

### Regular Checks (2-4x/day)
- [ ] **System health** — Disk space, memory, log sizes
- [ ] **Project status** — Active project updates, blockers
- [ ] **Memory maintenance** — Review daily logs → update MEMORY.md

### Weekly Checks (1x)
- [ ] **Memory consolidation** — Review week, distill to MEMORY.md
- [ ] **Tool/dependency updates** — Check for security patches
- [ ] **Workspace cleanup** — Archive old files, compress logs

---

## State Tracking

```json
{
  "lastChecks": {
    "calendar": 0,
    "email": 0,
    "systemHealth": 0,
    "memoryMaintenance": 0
  },
  "cyclesCompleted": 0,
  "lastWake": "2026-02-02T00:00:00Z"
}
```

---

## Response Protocols

### If nothing needs attention:
Reply: `HEARTBEAT_OK`

### If something needs your attention:
Reply with alert text ONLY. No HEARTBEAT_OK.

### If proactive work needed (no alert):
Execute silently. Log to daily file. Report in next non-heartbeat interaction.

---

## Active Projects to Monitor

*List current projects here for context during checks.*

1. Life OS / OpenClaw setup — in progress

---

*Keep this file minimal. Too many checks = noise. Rotate intelligently.*
=======
# HEARTBEAT.md

# Keep this file empty (or with only comments) to skip heartbeat API calls.

# Add tasks below when you want the agent to check something periodically.
>>>>>>> eaa0fd5 (Docs viewer standalone)
