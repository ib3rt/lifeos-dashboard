#!/bin/bash
# Monitor cron job status

echo "⏰ Cron Job Status"
echo "=================="

cd ~/.openclaw/workspace/memory 2>/dev/null

if [ -f heartbeat-state.json ]; then
    LAST_WAKE=$(jq -r '.lastWake' heartbeat-state.json 2>/dev/null)
    CYCLES=$(jq -r '.cyclesCompleted' heartbeat-state.json 2>/dev/null)
    
    echo "Last wake: $LAST_WAKE"
    echo "Cycles completed: $CYCLES"
    
    # Check if cron is active (within last hour)
    LAST_EPOCH=$(date -d "$LAST_WAKE" +%s 2>/dev/null || echo 0)
    NOW=$(date +%s)
    DIFF=$((NOW - LAST_EPOCH))
    
    if [ $DIFF -lt 3600 ]; then
        echo "✅ Cron active (last check ${DIFF}s ago)"
    else
        echo "⚠️  Cron stale (last check ${DIFF}s ago)"
    fi
else
    echo "⚠️  No heartbeat state found"
fi
