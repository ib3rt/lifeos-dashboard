# Auto-Todo System

## Purpose
Automatically capture tasks discussed in conversation and add them to the todo list.

## How It Works
1. When a task is mentioned in conversation ("I need to...", "Add to todo...", etc.)
2. Claw extracts the task
3. Adds to memory/daily-tasks.md
4. Posts to Discord #master-todo channel
5. Confirms with user

## Trigger Phrases
- "Add to my todo list..."
- "I need to..."
- "Put this on my todo..."
- "Remind me to..."
- "I should..."
- "Can you add..."

## Task Format
```markdown
- [ ] Task description (added: YYYY-MM-DD from conversation)
```

## Categories
Tasks auto-categorized as:
- High Priority (urgent, blocking, time-sensitive)
- Medium Priority (important, not urgent)
- Low Priority (nice to have, delegated)
- This Week (scheduled for current week)
- Backlog (future ideas)

## Discord Integration
New tasks auto-posted to #master-todo with:
- Task description
- Priority level
- Source (what conversation triggered it)
- Due date (if mentioned)

## Examples of Auto-Capture
User: "I need to call the bank tomorrow"
→ Auto-added: "- [ ] Call the bank (tomorrow)"

User: "Add installing that skill to my todo"
→ Auto-added: "- [ ] Install [skill name]"

User: "Remind me to review the PR when it's ready"
→ Auto-added: "- [ ] Review PR when ready"

## Manual Override
User can always say:
- "Don't add that to my todo" → Cancel
- "Mark that as high priority" → Re-categorize
- "Add it for next week" → Schedule

## Created
2026-02-03
