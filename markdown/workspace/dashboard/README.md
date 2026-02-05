# Agent Status System

## Quick Status Check

Run this command to see who's working:
```bash
openclaw agents status
```

## Visual Indicators

| Status | Emoji | Color | Meaning |
|--------|-------|-------|---------|
| 🔥 **Active** | Working | Green | Currently on task, don't interrupt |
| ⏳ **Idle** | Standing By | Yellow | Ready for assignment |
| 💤 **Offline** | Offline | Red | Not available/needs setup |
| ⚠️ **Blocked** | Needs Help | Orange | Stuck, requires intervention |

## Telegram Commands

**Check individual agent:**
```
/status @ClawTechBot
```

**Check all agents:**
```
/status all
```

**Get activity log:**
```
/log @ClawResearchBot
```

## Dashboard Access

**Web Dashboard:**
```
https://[your-domain]/agent-status.html
```

Or locally:
```
open workspace/dashboard/agent-status.html
```

## Auto-Updates

The dashboard refreshes every 30 seconds via WebSocket (when implemented).

Current refresh: Manual (F5)
