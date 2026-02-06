# Discord Message Policy

## User Requirement
**Each Discord message should be a NEW message — never replace/edit old messages.**

This allows the user to scroll back through conversation history.

## Implementation

### Bot Responses (lifeos-bot-v2.py)
✅ Uses `message.reply()` — creates new message every time
✅ Never uses `message.edit()`

### Automation Scripts
✅ Morning Brief → New embed sent to #morning-brief daily
✅ Afternoon Research → New embed sent to #afternoon-brief daily  
✅ 2nd Brain Poster → New embed for each document
✅ Auto-Todo → New embed for each task

### Message Structure
Each message includes:
- Timestamp (shows when posted)
- Unique content
- No reference to previous messages

## What This Means
- Every morning brief is a new message (can scroll back to yesterday's)
- Every research report is a new message
- Every agent response is a new message
- Chat history is preserved chronologically

## Verification
To verify this is working:
1. Check #morning-brief — should see multiple daily briefs
2. Check agent channels — each response is separate
3. Scroll back — history should be intact

## Date Configured
2026-02-03

## Status
✅ ACTIVE — All Discord messages are new posts
