#!/bin/bash
# Check if agents need new tasks assigned
echo "[$(date '+%Y-%m-%d %H:%M')] Checking perpetual task replenishment..."

# Count agents with less than 3 active tasks
NEED_TASKS=0
for agent_dir in ~/.openclaw/workspace/perpetual-tasks/*/; do
    if [ -d "$agent_dir" ]; then
        task_count=$(grep -c "^### TASK" "$agent_dir/active-tasks.md" 2>/dev/null || echo 0)
        if [ "$task_count" -lt 3 ]; then
            NEED_TASKS=$((NEED_TASKS + 1))
            echo "  ⚠️ $(basename $agent_dir) has only $task_count tasks"
        fi
    fi
done

if [ $NEED_TASKS -eq 0 ]; then
    echo "  ✅ All agents have 3 active tasks"
else
    echo "  🔄 $NEED_TASKS agents need task replenishment"
fi
