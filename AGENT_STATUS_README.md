# Agent Status Dashboard Documentation

## Overview

The Life OS Agent Status Dashboard provides real-time visibility into all 15+ AI agents with live status updates, current task tracking, and queue visualization.

## Quick Start

**Access the dashboard:**
- **Primary:** https://lifeos.b3rt.dev/lifeos-dashboard/agent-status.html
- **From main dashboard:** Click "📊 Open Real-Time Status Dashboard" in the Agents section

## Features

### 1. Real-Time Status Indicators
| Status | Icon | Meaning |
|--------|------|---------|
| Active | 🟢 | Agent is running and responsive |
| Busy | 🟡 | Agent has tasks in queue, processing |
| Idle | ⚪ | Agent is online but waiting |
| Offline | 🔴 | Agent is not running or unreachable |

### 2. Agent Cards
Each agent displays:
- **Icon & Name** - Visual identification
- **Role** - Agent's primary function
- **Current Task** - Live task indicator
- **Last Active** - Relative timestamp
- **Queue Count** - Number of pending tasks
- **Capabilities** - Agent's skill tags

### 3. Summary Stats
Top bar shows aggregate counts:
- Total Agents
- Active / Busy / Idle / Offline

### 4. Filtering
Filter agents by status using the toggle buttons.

## Data Source

**Location:** `/home/ubuntu/.openclaw/workspace/memory/agent-status.json`

**Schema:**
```json
{
  "lastUpdated": "ISO timestamp",
  "pollingInterval": 30000,
  "agents": [
    {
      "id": "unique-id",
      "name": "Agent Name",
      "fullName": "Full Role Title",
      "icon": "emoji",
      "role": "Category",
      "status": "active|busy|idle|offline",
      "currentTask": "Task description",
      "lastActive": "ISO timestamp",
      "queue": 0,
      "capabilities": ["skill1", "skill2"]
    }
  ],
  "summary": {
    "total": 16,
    "active": 10,
    "busy": 1,
    "idle": 3,
    "offline": 2
  }
}
```

## Technical Details

### Polling
- **Interval:** 30 seconds (configurable)
- **Endpoint:** `/memory/agent-status.json`
- **Auto-refresh:** Yes, with visual indicator

### Browser Support
- Chrome/Edge (recommended)
- Firefox
- Safari

### Animations
- Status pulse animation (2s cycle)
- Card hover effects
- Fade-in on data refresh

## API Endpoints

### GET /memory/agent-status.json
Returns current agent status.

**Response:** JSON object with agent data

### POST /memory/agent-status.json (optional)
Update agent status programmatically.

**Payload:**
```json
{
  "agentId": "goldfinger",
  "status": "active",
  "currentTask": "New task description"
}
```

## Adding New Agents

1. Add agent entry to `/home/ubuntu/.openclaw/workspace/memory/agent-status.json`
2. Include: id, name, fullName, icon, role, capabilities
3. Update summary counts

## Deployment

The dashboard is deployed via Vercel from `/lifeos-dashboard/`.

**Build command:** None (static HTML)
**Output directory:** `.`

## Troubleshooting

### Dashboard not loading
1. Check browser console for errors
2. Verify `agent-status.json` exists
3. Check file permissions

### Status not updating
1. Verify polling interval not exceeded
2. Check `lastUpdated` timestamp in JSON
3. Ensure no CORS issues

### Stale data
1. Manually refresh page
2. Check cron job updating the JSON
3. Verify server time sync

## Cron Integration

Recommended crontab entry to keep status fresh:
```bash
# Update agent status every minute
* * * * * cd /home/ubuntu/.openclaw/workspace && python3 -c "
import json
from datetime import datetime
# Your update logic here
"
```

## Related Files

- `/memory/genesis-tracking.json` - Genesis protocol tracking
- `/memory/heartbeat-state.json` - System health checks
- `lifeos-dashboard/index.html` - Main dashboard

---

*Last Updated: 2026-02-04*
*Life OS v2.0*
