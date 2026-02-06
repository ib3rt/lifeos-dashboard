#!/bin/bash
# 🤵 Daily Briefing System - The Butler
# Generates smart daily briefings with agent activity, tasks, decisions, and priorities
# Usage: ./daily-briefing-system.sh [output-path]

set -e

# Configuration
WORKSPACE_DIR="${WORKSPACE_DIR:-/home/ubuntu/.openclaw/workspace}"
OUTPUT_DIR="${1:-$WORKSPACE_DIR/butler}"
DATE=$(date +%Y-%m-%d)
TIMESTAMP=$(date +%Y-%m-%dT%H:%M:%SZ)
BRIEFING_FILE="$OUTPUT_DIR/daily-briefing-$DATE.md"

# Colors for terminal output (disabled if not TTY)
if [ -t 1 ]; then
    RED='\033[0;31m'
    GREEN='\033[0;32m'
    YELLOW='\033[1;33m'
    BLUE='\033[0;34m'
    NC='\033[0m' # No Color
else
    RED='' GREEN='' YELLOW='' BLUE='' NC=''
fi

log() {
    echo -e "${BLUE}[BUTLER]${NC} $1"
}

warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Ensure output directory exists
mkdir -p "$OUTPUT_DIR"

log "Generating daily briefing for $DATE..."
log "Workspace: $WORKSPACE_DIR"
log "Output: $BRIEFING_FILE"

# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 1: AGENT ACTIVITY SUMMARY
# ═══════════════════════════════════════════════════════════════════════════════

gather_agent_activity() {
    local agent_dir="$WORKSPACE_DIR/agent-tasks/$DATE"
    local activity_summary=""
    local active_count=0
    local complete_count=0
    local pending_count=0
    
    if [ -d "$agent_dir" ]; then
        # Count tasks by status
        for task_file in "$agent_dir"/*-task.md; do
            [ -f "$task_file" ] || continue
            
            if grep -q "Status:.*COMPLETE" "$task_file" 2>/dev/null; then
                ((complete_count++)) || true
            elif grep -q "Status:.*ACTIVE" "$task_file" 2>/dev/null; then
                ((active_count++)) || true
            elif grep -q "Status:.*PENDING" "$task_file" 2>/dev/null; then
                ((pending_count++)) || true
            fi
        done
        
        # Get recent agent reports (last 24h)
        activity_summary="| Agent | Status | Summary |\n|-------|--------|---------|"
        
        for report_file in "$agent_dir"/*-report.md; do
            [ -f "$report_file" ] || continue
            local agent_name=$(basename "$report_file" -report.md)
            local first_line=$(head -1 "$report_file" 2>/dev/null | sed 's/#* *//')
            local status="📊 Report"
            activity_summary="$activity_summary\n| $agent_name | $status | $first_line |"
        done
        
        # Check for Discord summaries
        if [ -f "$agent_dir/goldfinger-discord-summary.md" ]; then
            local discord_count=$(grep -c "^###" "$agent_dir/goldfinger-discord-summary.md" 2>/dev/null || echo "0")
            activity_summary="$activity_summary\n| goldfinger-discord | 📱 Active | $discord_count channels monitored |"
        fi
    fi
    
    # Also check genesis tracking for broader context
    local genesis_status=""
    if [ -f "$WORKSPACE_DIR/memory/genesis-tracking.json" ]; then
        genesis_status=$(cat "$WORKSPACE_DIR/memory/genesis-tracking.json" | grep -o '"status": "[^"]*"' | cut -d'"' -f4 || echo "UNKNOWN")
    fi
    
    echo -e "$activity_summary"
    echo "ACTIVE_COUNT:$active_count"
    echo "COMPLETE_COUNT:$complete_count"
    echo "PENDING_COUNT:$pending_count"
    echo "GENESIS_STATUS:$genesis_status"
}

# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 2: COMPLETED TASKS
# ═══════════════════════════════════════════════════════════════════════════════

gather_completed_tasks() {
    local completed=""
    local recent_days=3
    
    # Check memory files for completed work
    for day_offset in $(seq 0 $((recent_days - 1))); do
        local check_date=$(date -d "-$day_offset days" +%Y-%m-%d 2>/dev/null || date -v-${day_offset}d +%Y-%m-%d)
        local mem_file="$WORKSPACE_DIR/memory/$check_date.md"
        
        if [ -f "$mem_file" ]; then
            # Extract completed items from daily logs
            local day_completed=$(grep -E "^- \[x\]|^- ✅|Complete|Finished|Deployed" "$mem_file" 2>/dev/null | head -10 || true)
            if [ -n "$day_completed" ]; then
                completed="$completed\n### $check_date\n$day_completed"
            fi
        fi
    done
    
    # Check genesis tracking for main deliverables
    if [ -f "$WORKSPACE_DIR/memory/genesis-tracking.json" ]; then
        local genesis_complete=$(cat "$WORKSPACE_DIR/memory/genesis-tracking.json" | grep -o '"mainAgentCompleted": \[[^]]*\]' | sed 's/.*\[\(.*\)\].*/\1/' | tr ',' '\n' | sed 's/"//g' || true)
        if [ -n "$genesis_complete" ]; then
            completed="$completed\n### Genesis Deliverables\n$genesis_complete"
        fi
    fi
    
    # Check agent task summaries
    local agent_dir="$WORKSPACE_DIR/agent-tasks/$DATE"
    if [ -d "$agent_dir" ]; then
        for report in "$agent_dir"/*-report.md; do
            [ -f "$report" ] || continue
            local agent=$(basename "$report" -report.md)
            local summary=$(grep -E "^(Verdict|Status|Summary|Top Story):" "$report" 2>/dev/null | head -1 | cut -d':' -f2- | sed 's/^ *//' || true)
            if [ -n "$summary" ]; then
                completed="$completed\n- **$agent**: $summary"
            fi
        done
    fi
    
    if [ -z "$completed" ]; then
        completed="- No completed tasks recorded in tracking system"
    fi
    
    echo -e "$completed"
}

# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 3: PENDING DECISIONS
# ═══════════════════════════════════════════════════════════════════════════════

gather_pending_decisions() {
    local decisions=""
    
    # Check heartbeat state for queued operations
    if [ -f "$WORKSPACE_DIR/memory/heartbeat-state.json" ]; then
        local queued=$(cat "$WORKSPACE_DIR/memory/heartbeat-state.json" | grep -o '"queuedOperations": \[[^]]*\]' | sed 's/.*\[\(.*\)\].*/\1/' | tr ',' '\n' | sed 's/"//g' || true)
        if [ -n "$queued" ] && [ "$queued" != " " ]; then
            decisions="$decisions\n### Queued Operations\n$queued"
        fi
        
        local failed=$(cat "$WORKSPACE_DIR/memory/heartbeat-state.json" | grep -o '"failedRetries": \[[^]]*\]' | sed 's/.*\[\(.*\)\].*/\1/' | tr ',' '\n' | sed 's/"//g' || true)
        if [ -n "$failed" ] && [ "$failed" != " " ] && [ "$failed" != "" ]; then
            decisions="$decisions\n### Failed Operations (Need Attention)\n$failed"
        fi
    fi
    
    # Check MASTER_TODO.md for high priority items
    if [ -f "$WORKSPACE_DIR/MASTER_TODO.md" ]; then
        local high_priority=$(grep -E "^- \[ \].*\[HIGH\]|^- \[ \].*🚨|^- \[ \].*urgent" "$WORKSPACE_DIR/MASTER_TODO.md" 2>/dev/null | head -5 || true)
        if [ -n "$high_priority" ]; then
            decisions="$decisions\n### High Priority TODOs\n$high_priority"
        fi
    fi
    
    # Check for perpetual tasks with issues
    local perp_dir="$WORKSPACE_DIR/perpetual-tasks"
    if [ -d "$perp_dir" ]; then
        for task in "$perp_dir"/*/status.json; do
            [ -f "$task" ] || continue
            local task_name=$(basename $(dirname "$task"))
            local task_status=$(cat "$task" | grep -o '"status": "[^"]*"' | cut -d'"' -f4 || echo "unknown")
            if [ "$task_status" = "blocked" ] || [ "$task_status" = "failed" ]; then
                decisions="$decisions\n- **$task_name**: Status $task_status - needs decision"
            fi
        done
    fi
    
    if [ -z "$decisions" ]; then
        decisions="- No pending decisions requiring immediate attention"
    fi
    
    echo -e "$decisions"
}

# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 4: SYSTEM HEALTH
# ═══════════════════════════════════════════════════════════════════════════════

gather_system_health() {
    local health_info=""
    local status="✅ HEALTHY"
    
    # Disk usage
    local disk_usage=$(df -h "$WORKSPACE_DIR" | awk 'NR==2 {print $5}' | sed 's/%//')
    local disk_status="✅"
    if [ "$disk_usage" -gt 90 ]; then
        disk_status="🚨"
        status="⚠️ WARNING"
    elif [ "$disk_usage" -gt 75 ]; then
        disk_status="⚠️"
        status="⚠️ WARNING"
    fi
    
    # Memory usage
    local mem_info=$(free -m 2>/dev/null || echo "")
    local mem_usage="N/A"
    local mem_status="ℹ️"
    if [ -n "$mem_info" ]; then
        local mem_total=$(echo "$mem_info" | awk 'NR==2{print $2}')
        local mem_used=$(echo "$mem_info" | awk 'NR==2{print $3}')
        mem_usage=$(( mem_used * 100 / mem_total ))
        mem_status="✅"
        if [ "$mem_usage" -gt 90 ]; then
            mem_status="🚨"
            status="⚠️ WARNING"
        elif [ "$mem_usage" -gt 80 ]; then
            mem_status="⚠️"
        fi
    fi
    
    # Check OpenClaw gateway
    local gateway_status="🔴"
    if curl -s http://localhost:18789/status >/dev/null 2>&1 || pgrep -f "openclaw.*gateway" >/dev/null 2>&1; then
        gateway_status="🟢"
    fi
    
    # Check agent processes
    local active_agents=$(pgrep -c -f "subagent" 2>/dev/null || echo "0")
    
    # Last heartbeat
    local last_heartbeat="Unknown"
    if [ -f "$WORKSPACE_DIR/memory/heartbeat-state.json" ]; then
        last_heartbeat=$(cat "$WORKSPACE_DIR/memory/heartbeat-state.json" | grep -o '"lastWake": "[^"]*"' | cut -d'"' -f4 || echo "Unknown")
    fi
    
    # Genesis completion
    local genesis_health="Unknown"
    if [ -f "$WORKSPACE_DIR/memory/genesis-tracking.json" ]; then
        genesis_health=$(cat "$WORKSPACE_DIR/memory/genesis-tracking.json" | grep -o '"completionPercentage": [0-9]*' | awk '{print $2}' || echo "0")
        genesis_health="${genesis_health}%"
    fi
    
    health_info="| Metric | Value | Status |
|--------|-------|--------|
| Disk Usage | ${disk_usage}% | $disk_status |
| Memory Usage | ${mem_usage}% | $mem_status |
| OpenClaw Gateway | $gateway_status | Active |
| Active Sub-agents | $active_agents | Monitoring |
| Genesis Complete | $genesis_health | $([ "$genesis_health" = "100%" ] && echo "✅" || echo "🔄") |
| Last Heartbeat | $last_heartbeat | - |"
    
    echo -e "$health_info"
    echo "OVERALL_STATUS:$status"
}

# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 5: TODAY'S PRIORITIES
# ═══════════════════════════════════════════════════════════════════════════════

generate_priorities() {
    local priorities=""
    local priority_count=1
    
    # Priority 1: Complete any incomplete genesis tasks
    if [ -f "$WORKSPACE_DIR/memory/genesis-tracking.json" ]; then
        local genesis_pct=$(cat "$WORKSPACE_DIR/memory/genesis-tracking.json" | grep -o '"completionPercentage": [0-9]*' | awk '{print $2}' | head -1 | tr -d '[:space:]' || echo "100")
        genesis_pct=${genesis_pct:-100}
        if [ "$genesis_pct" -lt 100 ] 2>/dev/null; then
            priorities="$priorities\n$priority_count. **Complete Genesis** ($genesis_pct% done) - Finish remaining deliverables"
            ((priority_count++)) || true
        fi
    fi
    
    # Priority 2: Address failed retries
    if [ -f "$WORKSPACE_DIR/memory/heartbeat-state.json" ]; then
        local has_failures=$(cat "$WORKSPACE_DIR/memory/heartbeat-state.json" | grep '"failedRetries": \[' | grep -v '"failedRetries": \[\]' || true)
        if [ -n "$has_failures" ]; then
            priorities="$priorities\n$priority_count. **Resolve Failed Operations** - Check heartbeat-state.json for retries"
            ((priority_count++)) || true
        fi
    fi
    
    # Priority 3: Process queued operations
    if [ -f "$WORKSPACE_DIR/memory/heartbeat-state.json" ]; then
        local queued=$(cat "$WORKSPACE_DIR/memory/heartbeat-state.json" | grep -o '"queuedOperations": \[[^]]*\]' | grep -v '\[\]' || true)
        if [ -n "$queued" ]; then
            priorities="$priorities\n$priority_count. **Process Queue** - Execute queued operations from heartbeat"
            ((priority_count++)) || true
        fi
    fi
    
    # Priority 4: High priority TODOs
    if [ -f "$WORKSPACE_DIR/MASTER_TODO.md" ]; then
        local high_count=$(grep -c "\[HIGH\]" "$WORKSPACE_DIR/MASTER_TODO.md" 2>/dev/null | head -1 | tr -d '[:space:]' || echo "0")
        high_count=${high_count:-0}
        if [ "$high_count" -gt 0 ] 2>/dev/null; then
            priorities="$priorities\n$priority_count. **Address HIGH Priority TODOs** ($high_count items) - Check MASTER_TODO.md"
            ((priority_count++)) || true
        fi
    fi
    
    # Priority 5: Daily memory maintenance
    priorities="$priorities\n$priority_count. **Memory Maintenance** - Review yesterday's logs, update MEMORY.md"
    ((priority_count++)) || true
    
    # Priority 6: Agent task review (if active agents)
    local agent_dir="$WORKSPACE_DIR/agent-tasks/$DATE"
    if [ -d "$agent_dir" ]; then
        local report_count=$(ls -1 "$agent_dir"/*-report.md 2>/dev/null | wc -l)
        if [ "$report_count" -gt 0 ]; then
            priorities="$priorities\n$priority_count. **Review Agent Reports** ($report_count reports) - Process findings from today"
            ((priority_count++)) || true
        fi
    fi
    
    echo -e "$priorities"
}

# ═══════════════════════════════════════════════════════════════════════════════
# GENERATE BRIEFING
# ═══════════════════════════════════════════════════════════════════════════════

log "Gathering data..."

# Gather all sections
AGENT_DATA=$(gather_agent_activity)
COMPLETED=$(gather_completed_tasks)
DECISIONS=$(gather_pending_decisions)
HEALTH=$(gather_system_health)
PRIORITIES=$(generate_priorities)

# Parse counts from agent data
ACTIVE_COUNT=$(echo "$AGENT_DATA" | grep "^ACTIVE_COUNT:" | head -1 | cut -d: -f2 | tr -d '[:space:]' || echo "0")
COMPLETE_COUNT=$(echo "$AGENT_DATA" | grep "^COMPLETE_COUNT:" | head -1 | cut -d: -f2 | tr -d '[:space:]' || echo "0")
PENDING_COUNT=$(echo "$AGENT_DATA" | grep "^PENDING_COUNT:" | head -1 | cut -d: -f2 | tr -d '[:space:]' || echo "0")
GENESIS_STATUS=$(echo "$AGENT_DATA" | grep "^GENESIS_STATUS:" | head -1 | cut -d: -f2 | tr -d '[:space:]' || echo "UNKNOWN")
OVERALL_STATUS=$(echo "$HEALTH" | grep "^OVERALL_STATUS:" | head -1 | cut -d: -f2 | tr -d '[:space:]' || echo "✅ HEALTHY")

# Clean up any multi-line values
ACTIVE_COUNT=$(echo "$ACTIVE_COUNT" | head -1)
COMPLETE_COUNT=$(echo "$COMPLETE_COUNT" | head -1)
PENDING_COUNT=$(echo "$PENDING_COUNT" | head -1)

# Clean up data (remove metadata lines)
AGENT_TABLE=$(echo "$AGENT_DATA" | grep -v "^ACTIVE_COUNT:" | grep -v "^COMPLETE_COUNT:" | grep -v "^PENDING_COUNT:" | grep -v "^GENESIS_STATUS:" || true)
HEALTH_TABLE=$(echo "$HEALTH" | grep -v "^OVERALL_STATUS:" || true)

log "Generating briefing document..."

# Create the briefing
cat > "$BRIEFING_FILE" << EOF
# 📋 Daily Briefing — $DATE

**Generated:** $TIMESTAMP  
**System Status:** $OVERALL_STATUS  
**Genesis Status:** $GENESIS_STATUS

---

## 🎯 Executive Summary

| Metric | Count |
|--------|-------|
| Active Agents | $ACTIVE_COUNT |
| Completed Tasks | $COMPLETE_COUNT |
| Pending Tasks | $PENDING_COUNT |

---

## 🤖 Agent Activity

$AGENT_TABLE

---

## ✅ Completed Tasks

$COMPLETED

---

## ⏳ Pending Decisions

$DECISIONS

---

## 🏥 System Health

$HEALTH_TABLE

---

## 🚀 Today's Priorities

$PRIORITIES

---

## 📝 Notes & Context

*Generated by The Butler daily briefing system*  
*For questions, check: heartbeat-state.json, genesis-tracking.json, MASTER_TODO.md*

---

**Next briefing:** $(date -d "+1 day" +%Y-%m-%d 2>/dev/null || date -v+1d +%Y-%m-%d)
EOF

log "Briefing saved to: $BRIEFING_FILE"

# Display summary
echo ""
echo "═══════════════════════════════════════════════════════════"
echo "  📋 DAILY BRIEFING GENERATED"
echo "═══════════════════════════════════════════════════════════"
echo ""
echo "  Date:        $DATE"
echo "  Status:      $OVERALL_STATUS"
echo "  Agents:      $ACTIVE_COUNT active, $COMPLETE_COUNT completed"
echo "  Location:    $BRIEFING_FILE"
echo ""
echo "═══════════════════════════════════════════════════════════"

# Optional: Output file path for piping
if [ "${OUTPUT_PATH_ONLY:-false}" = "true" ]; then
    echo "$BRIEFING_FILE"
fi

exit 0
